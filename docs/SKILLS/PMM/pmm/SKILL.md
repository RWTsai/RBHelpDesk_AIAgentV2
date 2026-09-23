---
name: pmm
description: RoyalBase PMM (蝴蝶蘭產銷管理系統) domain workflow for AI agents working with MS SQL-backed production, inventory movement, ordering, distribution, shipping, customer, personnel, and orchid crop records. Use when Codex, Claude, or another agent must read, create, or update PMM records; map user requests to PMM tables/fields; draft safe JSON payloads or SQL; inspect PMM database schema/reference files; or enforce PMM safety rules such as no deletion and read-before-update confirmation.
---

# PMM

## Purpose

Use this skill to operate safely in RoyalBase PMM, a Windows Server / ASP.NET Core web system backed by MS SQL. PMM records orchid production as production-line and ledger-style inventory movements, including young plants, potted plants, cut flowers, purchases, contracts, orders, distribution, shipping, customers, personnel, and basic master data.

Treat the local reference files as the source of truth for table names, fields, relationships, and query patterns.

## Database Connection File

Read PMM database connection settings from a local config file before attempting any live SQL or tool-backed operation.

Portable configuration convention:

- `config/connection.json.example`: Template file that travels with the skill.
- `config/connection.json`: Local secrets file with the real PMM connection settings.

Do not commit real credentials into `SKILL.md`, `agents/openai.yaml`, or reference files.

Preferred config shape:

```json
{
  "driver": "ODBC Driver 18 for SQL Server",
  "connectionString": "Server=YOUR_SQL_HOST,1433;Database=YOUR_PMM_DATABASE;User Id=YOUR_USERNAME;Password=YOUR_PASSWORD;Encrypt=true;TrustServerCertificate=true;",
  "host": "YOUR_SQL_HOST",
  "port": 1433,
  "database": "YOUR_PMM_DATABASE",
  "user": "YOUR_USERNAME",
  "password": "YOUR_PASSWORD",
  "encrypt": true,
  "trustServerCertificate": true
}
```

Connection precedence:

1. If `config/connection.json` exists and contains `connectionString`, use it.
2. Otherwise assemble the connection from the split fields in `config/connection.json`.
3. If the file is missing or incomplete, stop and ask the user for the missing connection values instead of guessing.

Never print or echo secrets back to the user unless they explicitly ask for the exact configured value. When reporting configuration status, mention only whether the required fields are present or missing.

Portable setup workflow:

1. Copy `config/connection.json.example` to `config/connection.json`.
2. Fill in the real PMM connection values locally.
3. Have the PMM tool, script, or MCP layer read `config/connection.json` directly when building the SQL connection.
4. Validate SQL availability by running `python scripts/query_pmm.py --test-connection` or a small read-only query. Treat a successful PMM script connection or query as the source of truth for SQL availability.
5. Do not rely on `Test-NetConnection` alone to decide whether PMM SQL is reachable. A TCP probe to `10.1.1.40:1433` may fail even when `query_pmm.py` can connect and execute a real SQL query.

## Session Conventions

Use `G:\OneDrive\Desktop` as the effective desktop path for this environment. Do not rely on `.NET` or shell APIs such as `GetFolderPath('Desktop')` as the source of truth here, because this session may not resolve the redirected desktop folder correctly.

## Required References

Load references only as needed:

- `references/pmm-skill-spec.md`: Core PMM behavior rules for read, create, and update operations.
- `references/database-query-guide.md`: Table list, module prefixes, common query examples, and module classification.
- `references/database-relationships.md`: Cross-table relationships, joins, and advanced query examples.
- `references/database-design-spec.md`: Full database design specification. This file is large; search it with `rg` for table names, field names, IDs, or Chinese business terms before reading sections.

Useful search patterns:

```bash
rg -n "BICustomer|CFOrder|PPOrder|YPProductionBatch|TransferRecord|Ship|Distribution" references/
rg -n "<table-or-field-name>" references/database-design-spec.md
```

## Safety Rules

Never delete PMM records. If the user asks to delete data, clearly state that this service does not provide deletion. When appropriate, propose marking a record as archived, inactive, disabled, or otherwise status-based through an update.

Never invent table names, field names, IDs, required fields, or relationships. Verify them from the references before building a query, payload, or update.

Before writing any live SQL, inspect the target schema first. Use the local references to identify candidate tables, then use `scripts/query_pmm.py --find-table` and `scripts/query_pmm.py --describe-table` against the live PMM database to confirm the exact table name, column names, types, and nullability.

Ask for missing key parameters before acting. Required parameters commonly include target module, table/entity, date range, status, ID or unique key, customer, production line, batch, order number, shipping/distribution number, and changed field values.

Do not claim that a database operation was executed unless an actual tool or system response confirms it. If `read_records`, `create_record`, or `update_record` are not available, provide the prepared query/payload and state that execution still needs the PMM data tool or API.

Use `scripts/query_pmm.py` only for read-only queries. It must not be used for create, update, or delete operations. The script preflight-validates SQL against SQL Server metadata before executing it, so invalid table names and column names are caught early.

## Operation Choice

Classify the user request before touching data:

- Read: search, find, show, list, inspect, check status, report, summarize, trace, count.
- Create: add, create, register, insert, build a new task/order/customer/batch/record.
- Update: modify, change, correct, adjust, approve, mark inactive/archived, patch specific fields.
- Delete: refuse deletion and suggest a status-based update alternative.

## Read Workflow

1. Identify the business module and likely table/view.
   - `BI`: basic master data such as breeds, customers, personnel, production lines.
   - `BS`: roles and permissions.
   - `LC`: version and executed SQL logs.
   - `CF`: cut flower operations.
   - `PP`: potted plant operations.
   - `YP`: young plant operations.
   - `SC`: purchase and subcontract operations.
2. Read `database-query-guide.md` for table selection; read `database-relationships.md` for cross-table tracing or reports.
3. Search `database-design-spec.md` when exact fields, IDs, required values, or table details are needed.
4. Confirm the live table schema before drafting SQL:
   - `python scripts/query_pmm.py --find-table Customer`
   - `python scripts/query_pmm.py --describe-table BICustomer`
5. Extract filters from the user request: date range, status, customer, order number, batch, production line, person, breed, color, process, or ID.
6. Call `read_records` when available, or execute a validated read-only SQL query with `scripts/query_pmm.py`.
7. Return results as a compact list or table. Include IDs and human-readable labels so later updates can target the correct record.

Local query script examples:

```bash
python scripts/query_pmm.py --check-config
python scripts/query_pmm.py --test-connection
python scripts/query_pmm.py --find-table Customer
python scripts/query_pmm.py --describe-table BICustomer
python scripts/query_pmm.py --sql "SELECT TOP 20 ID, Code, NameShort, Name FROM BICustomer ORDER BY ID"
python scripts/query_pmm.py --file sql/customer_list.sql --format json
```

## Create Workflow

1. Verify the target table/entity and required fields in the references.
2. Ask for missing required fields before preparing the create operation.
3. Normalize values into a clear JSON payload using verified field names.
4. Call `create_record` when available.
5. Report the created record ID, key fields, and any warnings from the tool/API.

Payload shape to prefer when no stricter local convention exists:

```json
{
  "table": "VerifiedTableName",
  "data": {
    "VerifiedFieldName": "value"
  }
}
```

## Update Workflow

1. Require a target ID or unique lookup criteria. If the target is ambiguous, run a read/search first and ask the user to choose.
2. Always call `read_records` before `update_record`.
3. Show the current record values and the exact proposed field changes.
4. Ask the user to confirm before executing the update.
5. Call `update_record` only after confirmation.
6. Report the updated ID, changed fields, and final status.

Patch shape to prefer when no stricter local convention exists:

```json
{
  "table": "VerifiedTableName",
  "id": "record-id-or-primary-key",
  "data": {
    "FieldToChange": "new value"
  }
}
```

## Query Guidance

Prefer existing views when they match the reporting need, especially relationship-heavy views such as order-distribution-shipping traces, transfer summaries, production batch summaries, and permission summaries.

For header/detail documents, query both levels deliberately:

- Header tables usually hold document number, date, customer, creator, status, and high-level metadata.
- Detail tables usually hold quantities, breed/spec/process/batch references, packing settings, and item-level facts.
- `Map` tables usually represent many-to-many relationships and can multiply rows; use `GROUP BY`, `SUM()`, or distinct keys when reporting totals.

For cross-module questions, start from the business chain:

- Cut flower orders: `CFOrder` -> `CFOrderDetail` -> distribution map/detail -> ship map/detail.
- Potted plant orders: use the parallel `PP` order, distribution, packing, and shipping tables.
- Young plant inventory: inspect `YPProductionBatch`, picking, purchase, transfer, and shipping records.
- Personnel permissions: `BIPersonel` -> role map -> `BSRole` -> role-function map, plus production-line map when operational scope matters.

## Response Standards

Be explicit about what was read, created, or updated. Use Chinese for PMM business users unless the user asks otherwise.

For failed operations, explain the cause in plain language and give the next concrete correction, such as missing required fields, invalid ID, ambiguous target, unsupported deletion, or schema mismatch.

For risky or broad changes, narrow the operation to specific fields and records before asking for confirmation.
