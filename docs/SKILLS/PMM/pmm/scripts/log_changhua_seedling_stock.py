#!/usr/bin/env python
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pyodbc

from query_pmm import build_connection_string, load_config, resolve_config_path


PREFERRED_OBJECTS = ["View_苗株庫存數量", "苗株庫存數量", "YPProductionBatch_sum"]
FALLBACK_PATTERNS = ["%庫存%", "%YPProductionBatch%", "%YPPicking%"]

QUANTITY_COLUMNS = ["庫存數量", "庫存數", "目前庫存數", "TotalQuantity", "StockQuantity", "Inventory", "Quantity"]
LINE_NAME_COLUMNS = ["產線名稱", "產線", "ProductionLineName", "LineName", "ProductionLine"]
LINE_ID_COLUMNS = ["產線ID", "ProductionLineID", "ProductionLineId"]
SPEC_NAME_COLUMNS = ["規格名稱", "規格", "SpecName"]
SPEC_CODE_COLUMNS = ["規格代碼", "SpecCode"]
SPEC_ID_COLUMNS = ["規格ID", "SpecID", "SpecId", "CurrentSpecID"]
SPEC_PATTERN = re.compile(r"^(?P<number>\d+(?:\.\d+)?)(?P<suffix>[A-Za-z]+)?$", re.IGNORECASE)


@dataclass(frozen=True)
class SourcePlan:
    schema: str
    name: str
    table_type: str
    quantity_column: str
    line_name_column: str | None
    line_id_column: str | None
    spec_name_column: str | None
    spec_code_column: str | None
    spec_id_column: str | None

    @property
    def qualified_name(self) -> str:
        return f"{quote_identifier(self.schema)}.{quote_identifier(self.name)}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query 彰化生產部 4.5CM seedling stock and append one markdown line per run."
    )
    parser.add_argument("--config", default=None, help="Path to connection JSON. Defaults to ../config/connection.json")
    parser.add_argument("--production-line", default="彰化生產部", help="Production line name to filter")
    parser.add_argument("--spec", default="4.5CM", help="Spec name/code to filter")
    parser.add_argument("--source", default=None, help="Force a source table/view name instead of auto-discovery")
    parser.add_argument("--output", default=None, help="Markdown output path. Defaults to the desktop file 彰化苗株庫存.md")
    parser.add_argument("--timeout", type=int, default=30, help="SQL timeout in seconds")
    parser.add_argument("--print-sql", action="store_true", help="Print the generated SQL before execution")
    parser.add_argument("--dry-run", action="store_true", help="Query the quantity but do not append to a file")
    return parser.parse_args()


def normalize_identifier(value: str) -> str:
    return "".join(char for char in value.casefold() if char.isalnum())


def quote_identifier(value: str) -> str:
    return f"[{value.replace(']', ']]')}]"


def pick_column(columns: list[str], candidates: list[str]) -> str | None:
    normalized_to_original = {normalize_identifier(column): column for column in columns}

    for candidate in candidates:
        matched = normalized_to_original.get(normalize_identifier(candidate))
        if matched:
            return matched

    for candidate in candidates:
        candidate_normalized = normalize_identifier(candidate)
        for column in columns:
            if candidate_normalized and candidate_normalized in normalize_identifier(column):
                return column

    return None


def fetch_rows(connection: pyodbc.Connection, sql: str, params: list[str] | tuple[str, ...] | None = None) -> list[tuple]:
    cursor = connection.cursor()
    cursor.execute(sql, params or [])
    return cursor.fetchall()


def list_candidate_objects(connection: pyodbc.Connection, forced_name: str | None) -> list[tuple[str, str, str]]:
    if forced_name:
        rows = fetch_rows(
            connection,
            """
            SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_NAME = ?
            ORDER BY TABLE_SCHEMA, TABLE_NAME
            """,
            [forced_name],
        )
        return [(row[0], row[1], row[2]) for row in rows]

    conditions = ["TABLE_NAME = ?" for _ in PREFERRED_OBJECTS]
    conditions.extend("TABLE_NAME LIKE ?" for _ in FALLBACK_PATTERNS)
    params = [*PREFERRED_OBJECTS, *FALLBACK_PATTERNS]
    preferred_order = "\n".join(f"                WHEN ? THEN {index}" for index, _ in enumerate(PREFERRED_OBJECTS, start=1))
    sql = f"""
        SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
        FROM INFORMATION_SCHEMA.TABLES
        WHERE {" OR ".join(conditions)}
        ORDER BY
            CASE TABLE_NAME
{preferred_order}
                ELSE 9
            END,
            CASE TABLE_TYPE WHEN 'VIEW' THEN 0 ELSE 1 END,
            TABLE_SCHEMA,
            TABLE_NAME
    """
    params.extend(PREFERRED_OBJECTS)
    rows = fetch_rows(connection, sql, params)
    return [(row[0], row[1], row[2]) for row in rows]


def list_columns(connection: pyodbc.Connection, schema: str, name: str) -> list[str]:
    rows = fetch_rows(
        connection,
        """
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?
        ORDER BY ORDINAL_POSITION
        """,
        [schema, name],
    )
    return [row[0] for row in rows]


def score_candidate(name: str, table_type: str, columns: list[str]) -> int:
    score = 0
    if name in PREFERRED_OBJECTS:
        score += 100 - (PREFERRED_OBJECTS.index(name) * 10)
    if "苗株" in name:
        score += 50
    if table_type.upper() == "VIEW":
        score += 10
    if pick_column(columns, QUANTITY_COLUMNS):
        score += 30
    if pick_column(columns, LINE_NAME_COLUMNS) or pick_column(columns, LINE_ID_COLUMNS):
        score += 10
    if pick_column(columns, SPEC_NAME_COLUMNS) or pick_column(columns, SPEC_CODE_COLUMNS) or pick_column(columns, SPEC_ID_COLUMNS):
        score += 10
    return score


def build_spec_aliases(spec: str) -> list[str]:
    aliases: list[str] = []

    def add(value: str) -> None:
        candidate = value.strip()
        if candidate and candidate not in aliases:
            aliases.append(candidate)

    add(spec)
    normalized = spec.strip().upper()
    match = SPEC_PATTERN.fullmatch(normalized)
    if match:
        number = match.group("number")
        suffix = match.group("suffix") or ""
        if "." in number:
            whole_text, decimal = number.split(".", 1)
            whole = int(whole_text)
            add(f"{whole}.{decimal}{suffix}")
            add(f"{whole:02d}.{decimal}{suffix}")
        else:
            whole = int(number)
            add(f"{whole}{suffix}")
            add(f"{whole:02d}{suffix}")

    digits = "".join(char for char in normalized if char.isdigit())
    if digits:
        add(digits.zfill(4))

    return aliases


def build_equals_any_clause(column_sql: str, values: list[str], params: list[str]) -> str:
    placeholders = ", ".join("?" for _ in values)
    params.extend(values)
    return f"{column_sql} IN ({placeholders})"


def discover_source_plan(connection: pyodbc.Connection, forced_name: str | None) -> SourcePlan:
    candidates = list_candidate_objects(connection, forced_name)
    if not candidates:
        wanted = forced_name if forced_name else ", ".join(PREFERRED_OBJECTS)
        raise SystemExit(f"找不到可用的苗株庫存來源物件：{wanted}")

    ranked: list[tuple[int, SourcePlan]] = []
    for schema, name, table_type in candidates:
        columns = list_columns(connection, schema, name)
        quantity_column = pick_column(columns, QUANTITY_COLUMNS)
        line_name_column = pick_column(columns, LINE_NAME_COLUMNS)
        line_id_column = pick_column(columns, LINE_ID_COLUMNS)
        spec_name_column = pick_column(columns, SPEC_NAME_COLUMNS)
        spec_code_column = pick_column(columns, SPEC_CODE_COLUMNS)
        spec_id_column = pick_column(columns, SPEC_ID_COLUMNS)

        if not quantity_column:
            continue
        if not (line_name_column or line_id_column):
            continue
        if not (spec_name_column or spec_code_column or spec_id_column):
            continue

        plan = SourcePlan(
            schema=schema,
            name=name,
            table_type=table_type,
            quantity_column=quantity_column,
            line_name_column=line_name_column,
            line_id_column=line_id_column,
            spec_name_column=spec_name_column,
            spec_code_column=spec_code_column,
            spec_id_column=spec_id_column,
        )
        ranked.append((score_candidate(name, table_type, columns), plan))

    if not ranked:
        inspected = ", ".join(f"{schema}.{name}" for schema, name, _ in candidates)
        raise SystemExit(f"找到候選物件，但無法辨識產線/規格/數量欄位：{inspected}")

    ranked.sort(key=lambda item: item[0], reverse=True)
    return ranked[0][1]


def query_stock_quantity(
    connection: pyodbc.Connection,
    plan: SourcePlan,
    production_line: str,
    spec: str,
    print_sql: bool,
) -> int:
    sql, params = build_runtime_sql(plan, production_line, spec)
    if print_sql:
        print(sql)
        print(f"參數: {params}")

    cursor = connection.cursor()
    cursor.execute(sql, params)
    row = cursor.fetchone()
    return int(row[0] or 0)


def build_runtime_sql(plan: SourcePlan, production_line: str, spec: str) -> tuple[str, list[str]]:
    joins: list[str] = []
    where: list[str] = []
    params: list[str] = []
    spec_aliases = build_spec_aliases(spec)

    if plan.line_name_column:
        where.append(f"src.{quote_identifier(plan.line_name_column)} = ?")
        params.append(production_line)
    else:
        joins.append(
            "INNER JOIN [BIProductionLine] AS pl "
            f"ON pl.[ID] = src.{quote_identifier(plan.line_id_column or '')}"
        )
        where.append("(pl.[Name] = ? OR pl.[Code] = ?)")
        params.extend([production_line, production_line])

    spec_predicates: list[str] = []
    if plan.spec_name_column:
        spec_predicates.append(build_equals_any_clause(f"src.{quote_identifier(plan.spec_name_column)}", spec_aliases, params))
    if plan.spec_code_column:
        spec_predicates.append(build_equals_any_clause(f"src.{quote_identifier(plan.spec_code_column)}", spec_aliases, params))

    if spec_predicates:
        where.append(f"({' OR '.join(spec_predicates)})")
    else:
        joins.append("INNER JOIN [BISpec] AS sp " f"ON sp.[ID] = src.{quote_identifier(plan.spec_id_column or '')}")
        where.append(
            "("
            + " OR ".join(
                [
                    build_equals_any_clause("sp.[Name]", spec_aliases, params),
                    build_equals_any_clause("sp.[Code]", spec_aliases, params),
                ]
            )
            + ")"
        )

    sql = (
        "SELECT CAST(COALESCE(SUM(COALESCE("
        f"src.{quote_identifier(plan.quantity_column)}, 0)), 0) AS bigint) AS StockQuantity\n"
        f"FROM {plan.qualified_name} AS src\n"
        f"{chr(10).join(joins)}\n"
        f"WHERE {' AND '.join(where)}"
    )
    return sql, params


def resolve_default_output_path() -> Path:
    env_override = os.environ.get("PMM_STOCK_LOG_PATH", "").strip()
    if env_override:
        return Path(env_override).expanduser().resolve()

    desktop_dir = find_desktop_dir()
    if desktop_dir is None:
        raise SystemExit("找不到桌面資料夾，請使用 --output 指定彰化苗株庫存.md 的輸出路徑。")

    return (desktop_dir / "彰化苗株庫存.md").resolve()


def find_desktop_dir() -> Path | None:
    candidates: list[Path] = []
    for env_name in ("OneDriveCommercial", "OneDriveConsumer", "OneDrive", "USERPROFILE"):
        raw = os.environ.get(env_name, "").strip()
        if not raw:
            continue
        base = Path(raw)
        candidates.append(base / "Desktop")
        candidates.append(base / "桌面")

    home = Path.home()
    candidates.append(home / "Desktop")
    candidates.append(home / "桌面")

    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate).lower()
        if key in seen:
            continue
        seen.add(key)
        if candidate.exists() and candidate.is_dir():
            return candidate

    return None


def append_markdown_line(path: Path, production_line: str, spec: str, quantity: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
    line = f"- {timestamp} | {production_line} | {spec} | {quantity}"

    needs_prefix_newline = False
    if path.exists() and path.stat().st_size > 0:
        with path.open("rb") as handle:
            handle.seek(-1, os.SEEK_END)
            needs_prefix_newline = handle.read(1) not in {b"\n", b"\r"}

    with path.open("a", encoding="utf-8", newline="\n") as handle:
        if needs_prefix_newline:
            handle.write("\n")
        handle.write(line)


def main() -> int:
    args = parse_args()

    config_path = resolve_config_path(args.config)
    config = load_config(config_path)
    connection_string = build_connection_string(config)

    try:
        with pyodbc.connect(connection_string, timeout=args.timeout) as connection:
            plan = discover_source_plan(connection, args.source)
            quantity = query_stock_quantity(connection, plan, args.production_line, args.spec, args.print_sql)
    except pyodbc.Error as exc:
        raise SystemExit(f"PMM 連線或查詢失敗：{exc}") from exc

    if args.dry_run:
        print(f"查詢來源：{plan.schema}.{plan.name}")
        print(f"查詢結果：{quantity}")
        return 0

    output_path = Path(args.output).expanduser().resolve() if args.output else resolve_default_output_path()
    append_markdown_line(output_path, args.production_line, args.spec, quantity)

    print(f"查詢來源：{plan.schema}.{plan.name}")
    print(f"查詢結果：{quantity}")
    print(f"已追加寫入：{output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
