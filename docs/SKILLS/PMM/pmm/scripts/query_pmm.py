#!/usr/bin/env python
import argparse
import json
import re
import sys
from pathlib import Path

import pyodbc


DEFAULT_DRIVER = "ODBC Driver 18 for SQL Server"
FORBIDDEN_SQL = re.compile(
    r"\b(insert|update|delete|drop|alter|create|merge|truncate|exec|execute|grant|revoke)\b",
    re.IGNORECASE,
)
LEGACY_SERVER_PORT_PATTERN = re.compile(
    r"(?i)(^|;)Server\s*=\s*(?P<server>[^;]+?)\s*;\s*PORT\s*=\s*(?P<port>\d+)\s*(?=;|$)"
)
PORT_ATTRIBUTE_PATTERN = re.compile(r"(?i)(^|;)PORT\s*=\s*\d+\s*(?=;|$)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute read-only PMM SQL queries.")
    parser.add_argument("--config", default=None, help="Path to connection JSON. Defaults to ../config/connection.json")
    parser.add_argument("--sql", help="Inline SQL query to execute")
    parser.add_argument("--file", help="Path to a .sql file to execute")
    parser.add_argument("--find-table", help="Find tables or views by name pattern")
    parser.add_argument("--describe-table", help="Describe a table or view schema")
    parser.add_argument("--format", choices=("table", "json"), default="table", help="Output format")
    parser.add_argument("--timeout", type=int, default=30, help="SQL timeout in seconds")
    parser.add_argument("--max-rows", type=int, default=200, help="Maximum rows to print")
    parser.add_argument("--check-config", action="store_true", help="Validate config presence without connecting")
    parser.add_argument("--test-connection", action="store_true", help="Open and close a database connection")
    return parser.parse_args()


def resolve_config_path(raw_path: str | None) -> Path:
    if raw_path:
        return Path(raw_path).expanduser().resolve()
    return (Path(__file__).resolve().parent.parent / "config" / "connection.json").resolve()


def load_config(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"PMM connection file not found: {path}")

    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in PMM connection file: {exc}") from exc

    if not isinstance(config, dict):
        raise SystemExit("PMM connection file must contain a JSON object.")

    return config


def validate_config(config: dict) -> tuple[list[str], list[str]]:
    if config.get("connectionString"):
        present = ["connectionString"]
        for key in ("driver", "host", "port", "database", "user", "password", "encrypt", "trustServerCertificate"):
            if config.get(key) not in (None, ""):
                present.append(key)
        return present, []

    required = ["host", "database", "user", "password"]
    present = [key for key in required if config.get(key) not in (None, "")]
    missing = [key for key in required if key not in present]
    for key in ("driver", "port", "encrypt", "trustServerCertificate"):
        if config.get(key) not in (None, ""):
            present.append(key)
    return present, missing


def coerce_bool(value, default: bool) -> bool:
    if value in (None, ""):
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)

    normalized = str(value).strip().lower()
    if normalized in {"1", "true", "yes", "y", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False
    return default


def normalize_connection_string(connection_string: str) -> str:
    normalized = connection_string.strip()

    def replace_server_port(match: re.Match[str]) -> str:
        prefix = match.group(1)
        server = match.group("server").strip()
        port = match.group("port").strip()
        return f"{prefix}Server={server},{port}"

    normalized = LEGACY_SERVER_PORT_PATTERN.sub(replace_server_port, normalized)
    normalized = PORT_ATTRIBUTE_PATTERN.sub("", normalized)
    normalized = re.sub(r";{2,}", ";", normalized).strip().strip(";")
    return normalized


def build_connection_string(config: dict) -> str:
    connection_string = str(config.get("connectionString", "")).strip()
    driver = str(config.get("driver") or DEFAULT_DRIVER).strip()

    if connection_string:
        connection_string = normalize_connection_string(connection_string)
        lowered = connection_string.lower()
        if "driver=" not in lowered and "dsn=" not in lowered:
            connection_string = f"Driver={{{driver}}};{connection_string}"
        return connection_string

    host = str(config.get("host", "")).strip()
    database = str(config.get("database", "")).strip()
    user = str(config.get("user", "")).strip()
    password = str(config.get("password", "")).strip()
    port = int(config.get("port", 1433) or 1433)
    encrypt = "yes" if coerce_bool(config.get("encrypt", True), True) else "no"
    trust_server_certificate = "yes" if coerce_bool(config.get("trustServerCertificate", True), True) else "no"

    if not all([host, database, user, password]):
        raise SystemExit("PMM connection file is incomplete. Required fields: host, database, user, password.")

    return (
        f"Driver={{{driver}}};"
        f"Server={host},{port};"
        f"Database={database};"
        f"Uid={user};"
        f"Pwd={password};"
        f"Encrypt={encrypt};"
        f"TrustServerCertificate={trust_server_certificate};"
    )


def load_sql(args: argparse.Namespace) -> str | None:
    if args.sql and args.file:
        raise SystemExit("Use either --sql or --file, not both.")
    if args.sql:
        return args.sql
    if args.file:
        return Path(args.file).read_text(encoding="utf-8")
    return None


def validate_read_only_sql(sql: str) -> str:
    normalized = sql.lstrip("\ufeff").strip()
    if not normalized:
        raise SystemExit("SQL is empty.")
    lowered = normalized.lower()
    if not (lowered.startswith("select") or lowered.startswith("with")):
        raise SystemExit("Only read-only SELECT queries are allowed.")
    if FORBIDDEN_SQL.search(normalized):
        raise SystemExit("Only read-only SELECT queries are allowed. Forbidden keyword detected.")
    return normalized


def preflight_validate_sql(connection: pyodbc.Connection, sql: str) -> None:
    cursor = connection.cursor()
    row = cursor.execute(
        """
        SELECT TOP 1 error_number, error_message
        FROM sys.dm_exec_describe_first_result_set(?, NULL, 0)
        WHERE error_number IS NOT NULL
        """,
        sql,
    ).fetchone()

    if row:
        raise SystemExit(f"SQL validation failed: {row.error_message}")


def execute_query(connection: pyodbc.Connection, sql: str, max_rows: int) -> tuple[list[str], list[tuple], bool]:
    cursor = connection.cursor()
    cursor.execute(sql)
    if cursor.description is None:
        raise SystemExit("The SQL did not return a result set.")

    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchmany(max_rows + 1)
    truncated = len(rows) > max_rows
    if truncated:
        rows = rows[:max_rows]
    return columns, rows, truncated


def find_tables(connection: pyodbc.Connection, pattern: str, max_rows: int) -> tuple[list[str], list[tuple], bool]:
    sql = """
    SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_NAME LIKE ?
    ORDER BY TABLE_TYPE, TABLE_SCHEMA, TABLE_NAME
    """
    cursor = connection.cursor()
    cursor.execute(sql, f"%{pattern}%")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchmany(max_rows + 1)
    truncated = len(rows) > max_rows
    if truncated:
        rows = rows[:max_rows]
    return columns, rows, truncated


def describe_table(connection: pyodbc.Connection, table_name: str, max_rows: int) -> tuple[list[str], list[tuple], bool]:
    if "." in table_name:
        schema_name, object_name = table_name.split(".", 1)
    else:
        schema_name, object_name = None, table_name

    sql = """
    SELECT
        TABLE_SCHEMA,
        TABLE_NAME,
        COLUMN_NAME,
        DATA_TYPE,
        COALESCE(CAST(CHARACTER_MAXIMUM_LENGTH AS varchar(20)), '') AS CHARACTER_MAXIMUM_LENGTH,
        IS_NULLABLE,
        COALESCE(COLUMN_DEFAULT, '') AS COLUMN_DEFAULT,
        ORDINAL_POSITION
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = ?
    """
    params = [object_name]

    if schema_name:
        sql += " AND TABLE_SCHEMA = ?"
        params.append(schema_name)

    sql += " ORDER BY TABLE_SCHEMA, TABLE_NAME, ORDINAL_POSITION"

    cursor = connection.cursor()
    cursor.execute(sql, params)
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchmany(max_rows + 1)
    truncated = len(rows) > max_rows
    if truncated:
        rows = rows[:max_rows]
    if not rows:
        raise SystemExit(f"Table or view not found in INFORMATION_SCHEMA.COLUMNS: {table_name}")
    return columns, rows, truncated


def format_value(value) -> str:
    if value is None:
        return "NULL"
    return str(value)


def render_table(columns: list[str], rows: list[tuple]) -> str:
    string_rows = [[format_value(value) for value in row] for row in rows]
    widths = [len(column) for column in columns]
    for row in string_rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    header = " | ".join(column.ljust(widths[index]) for index, column in enumerate(columns))
    divider = "-+-".join("-" * widths[index] for index in range(len(columns)))
    body = [" | ".join(value.ljust(widths[index]) for index, value in enumerate(row)) for row in string_rows]
    return "\n".join([header, divider, *body]) if body else "\n".join([header, divider])


def render_json(columns: list[str], rows: list[tuple]) -> str:
    payload = [dict(zip(columns, row)) for row in rows]
    return json.dumps(payload, ensure_ascii=False, indent=2, default=str)


def main() -> int:
    args = parse_args()
    config_path = resolve_config_path(args.config)
    config = load_config(config_path)
    present, missing = validate_config(config)

    if args.check_config:
        print(f"Config file: {config_path}")
        print(f"Present fields: {', '.join(present) if present else '(none)'}")
        if missing:
            print(f"Missing required fields: {', '.join(missing)}")
            return 1
        print("Config is usable.")
        return 0

    connection_string = build_connection_string(config)

    if args.test_connection:
        with pyodbc.connect(connection_string, timeout=args.timeout) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT 1 AS ok")
            row = cursor.fetchone()
        print(f"Connection succeeded. Test query returned: {row[0]}")
        return 0

    if args.find_table:
        with pyodbc.connect(connection_string, timeout=args.timeout) as connection:
            columns, rows, truncated = find_tables(connection, args.find_table, args.max_rows)
    elif args.describe_table:
        with pyodbc.connect(connection_string, timeout=args.timeout) as connection:
            columns, rows, truncated = describe_table(connection, args.describe_table, args.max_rows)
    else:
        sql = load_sql(args)
        if not sql:
            raise SystemExit("Provide --sql, --file, --find-table, --describe-table, --check-config, or --test-connection.")

        normalized_sql = validate_read_only_sql(sql)
        with pyodbc.connect(connection_string, timeout=args.timeout) as connection:
            preflight_validate_sql(connection, normalized_sql)
            columns, rows, truncated = execute_query(connection, normalized_sql, args.max_rows)

    if args.format == "json":
        print(render_json(columns, rows))
    else:
        print(render_table(columns, rows))

    if truncated:
        print(f"\nOutput truncated to {args.max_rows} row(s).", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
