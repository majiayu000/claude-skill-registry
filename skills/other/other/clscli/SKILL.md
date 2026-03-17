---
name: clscli
description: Query and analyze Tencent Cloud CLS logs
homepage: https://github.com/
metadata:
    {"requires": {"bin": ["clscli"], "env": ["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"]}}
---

# CLS Skill

Query and analyze Tencent Cloud CLS logs.

## Setup
1. Install clscli (Homebrew):
    ```bash
    brew tap dbwang0130/clscli
    brew install dbwang0130/clscli/clscli
    ```
2. Get credentials and region list: https://cloud.tencent.com/document/api/614/56474
3. Set environment variables (same as Tencent Cloud API common parameters):
    ```bash
    export TENCENTCLOUD_SECRET_ID="your-secret-id"
    export TENCENTCLOUD_SECRET_KEY="your-secret-key"
    ```
4. Specify region via `--region` (e.g. ap-guangzhou).

## Usage

!IMPORTANT: If you do not know the log topic, list topics first.

### List log topics
List topics in a region to determine which `--region` and topic ID to use for query/context.

```bash
clscli topics --region <region> [--topic-name name] [--logset-name name] [--logset-id id] [--limit 20] [--offset 0]
```
Examples: `--output=json`, `--output=csv`, `-o topics.csv`

| Option | Required | Description |
|--------|----------|-------------|
| --region | yes | CLS region, e.g. ap-guangzhou |
| --topic-name | no | Filter by topic name (fuzzy match) |
| --logset-name | no | Filter by logset name (fuzzy match) |
| --logset-id | no | Filter by logset ID |
| --limit | no | Page size, default 20, max 100 |
| --offset | no | Pagination offset, default 0 |
| --output, -o | no | Output: json, csv, or file path |

Output columns: Region, TopicId, TopicName, LogsetId, CreateTime, StorageType.

### Get log by query
```bash
clscli query -q "[query condition] | [SQL statement]" --region <region> -t <TopicId> --last 1h
```
Examples:
- Time: `--last 1h`, `--last 30m`; or `--from`/`--to` (Unix ms)
- Multiple topics: `--topics <id1>,<id2>` or multiple `-t <id>`
- Auto pagination and cap: `--max 5000` (paginate until 5000 logs or ListOver)
- Output: `--output=json`, `--output=csv`, `-o result.json` (write to file)

| Option | Required | Description |
|--------|----------|-------------|
| --region | yes | CLS region, e.g. ap-guangzhou |
| -q, --query | yes | Query condition or SQL, e.g. `level:ERROR` or `* \| select count(*) as cnt` |
| -t, --topic | one of -t/--topics | Single log topic ID |
| --topics | one of -t/--topics | Comma-separated topic IDs, max 50 |
| --last | one of --last/--from/--to | Time range, e.g. 1h, 30m, 24h |
| --from, --to | one of --last/--from/--to | Start/end time (Unix ms) |
| --limit | no | Logs per request, default 100, max 1000 |
| --max | no | Max total logs; when non-zero, auto-paginate until reached or ListOver |
| --output, -o | no | Output: json, csv, or file path |
| --sort | no | Sort: asc or desc, default desc |

#### Query condition syntax

Two syntaxes are supported:
- **CQL** (CLS Query Language): CLS-specific query syntax for logs, easy to use, recommended.
- **Lucene**: Open-source Lucene syntax; not designed for log search, has more restrictions on special chars, case, wildcards; not recommended.

##### CQL syntax
| Syntax | Description |
|--------|-------------|
| `key:value` | Key-value search; logs where field (key) contains value, e.g. `level:ERROR` |
| `value` | Full-text search; logs containing value, e.g. `ERROR` |
| `AND` | Logical AND, case-insensitive, e.g. `level:ERROR AND pid:1234` |
| `OR` | Logical OR, case-insensitive, e.g. `level:ERROR OR level:WARNING`, `level:(ERROR OR WARNING)` |
| `NOT` | Logical NOT, case-insensitive, e.g. `level:ERROR NOT pid:1234`, `level:ERROR AND NOT pid:1234` |
| `()` | Grouping for precedence, e.g. `level:(ERROR OR WARNING) AND pid:1234`. **Note: AND has higher precedence than OR when no parentheses.** |
| `"  "` | Phrase search; double-quoted string, words and order must match, e.g. `name:"john Smith"`. No logical operators inside phrase. |
| `'  '` | Phrase search; single quotes, same as `""`; use when phrase contains double quotes, e.g. `body:'user_name:"bob"'` |
| `*` | Wildcard; zero or more chars, e.g. `host:www.test*.com`. No prefix wildcard. |
| `>`, `>=`, `<`, `<=`, `=` | Range operators for numeric values, e.g. `status>400`, `status:>=400` |
| `\` | Escape; escaped char is literal. Escape space, `:`, `()`, `>`, `=`, `<`, `"`, `'`, `*` in values. |
| `key:*` | text: field exists (any value). long/double: field exists and is numeric, e.g. `response_time:*` |
| `key:""` | text: field exists and is empty. long/double: value is not numeric or field missing, e.g. `response_time:""` |

#### SQL statement syntax
| Syntax | Description |
|--------|-------------|
| SELECT | Select from table; data from current log topic matching query condition |
| AS | Alias for column (KEY) |
| GROUP BY | With aggregate functions, group by one or more columns (KEY) |
| ORDER BY | Sort result set by KEY |
| LIMIT | Limit rows, default 100, max 1M |
| WHERE | Filter raw data |
| HAVING | Filter after GROUP BY, before ORDER BY; WHERE filters raw data |
| Nested subquery | One SELECT inside another for multi-step analysis |
| SQL functions | Richer analysis: IP geo, time format, string split/join, JSON extract, math, distinct count, etc. |


### Describe log context

Retrieve log context around a given log.

```bash
clscli context <PkgId> <PkgLogId> --region <region> -t <TopicId>
```
Examples: `--output=json`, `--output=csv`, `-o context.json` (write to file)

| Option | Required | Type | Description | Example |
|--------|----------|------|-------------|---------|
| --region | yes | String | CLS region | ap-guangzhou |
| -t, --topic | yes | String | Log topic ID | - |
| PkgId | yes | String | Log package ID, i.e. SearchLog Results[].PkgId | 528C1318606EFEB8-1A7 |
| PkgLogId | yes | Integer | Index within package, i.e. SearchLog Results[].PkgLogId | 65536 |
| --output, -o | no | - | Output: json, csv, or file path | - |
