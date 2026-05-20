---
name: sap-odata-explorer
description: Query and explore SAP OData endpoints with secure logging and configurable output. Use this skill when the user needs to fetch data from SAP systems, explore SAP entity structures, or query SAP business objects like BusinessPartner, SalesOrder, Product, etc.
allowed-tools: [Bash, Read]
---

# SAP OData Explorer Skill

This skill enables Claude to query and explore SAP OData endpoints securely and efficiently.

## When to Use This Skill

Activate this skill when the user:
- Asks to fetch data from SAP
- Wants to query SAP entities or business objects
- Needs to explore SAP OData service structures
- Mentions SAP terms like BusinessPartner, SalesOrder, Material, Product, etc.
- Wants to see metadata or entity definitions
- Needs to understand what data is available in SAP

## Available Commands

### 1. Query Entities

Query SAP OData entities with filtering, selection, and pagination.

```bash
cd .claude/skills/sap-odata-explorer
npm run query -- --service <service> --entity <entity> [options]
```

**Required Arguments:**
- `--service`: OData service name (e.g., `API_BUSINESS_PARTNER`)
- `--entity`: Entity set name (e.g., `A_BusinessPartner`)

**Optional Arguments:**
- `--filter`: OData filter expression (e.g., `"Status eq 'Active'"`)
- `--select`: Comma-separated fields (e.g., `ID,Name,Status`)
- `--top`: Number of records (e.g., `10`)
- `--skip`: Skip records for pagination (e.g., `20`)
- `--orderby`: Sort expression (e.g., `Name asc`)
- `--expand`: Navigation properties (e.g., `to_Address`)
- `--output`: Custom output filename
- `--format`: Output format (`json` or `pretty`)
- `--no-file`: Print to console instead of file

**Examples:**

```bash
# Get first 10 business partners
npm run query -- --service API_BUSINESS_PARTNER --entity A_BusinessPartner --top 10

# Query with filter and select specific fields
npm run query -- --service API_BUSINESS_PARTNER --entity A_BusinessPartner \
  --filter "BusinessPartnerCategory eq '1'" \
  --select BusinessPartner,FirstName,LastName \
  --top 5

# Query with sorting
npm run query -- --service API_BUSINESS_PARTNER --entity A_BusinessPartner \
  --orderby LastName --top 10

# Pretty print to console
npm run query -- --service API_BUSINESS_PARTNER --entity A_BusinessPartner \
  --top 5 --format pretty --no-file
```

### 2. Get Metadata

Fetch and explore OData service metadata to understand available entities and their properties.

```bash
cd .claude/skills/sap-odata-explorer
npm run metadata -- --service <service> [options]
```

**Required Arguments:**
- `--service`: OData service name

**Optional Arguments:**
- `--format`: Output format (`summary`, `json`, or `pretty`)
- `--raw`: Get raw XML metadata
- `--output`: Custom output filename
- `--no-file`: Print to console

**Examples:**

```bash
# Get summary of service metadata
npm run metadata -- --service API_BUSINESS_PARTNER

# Get full JSON metadata
npm run metadata -- --service API_BUSINESS_PARTNER --format json

# Get raw XML metadata
npm run metadata -- --service API_BUSINESS_PARTNER --raw

# Print to console
npm run metadata -- --service API_BUSINESS_PARTNER --no-file
```

### 3. List Services

List common SAP OData services available in the system.

```bash
cd .claude/skills/sap-odata-explorer
npm run list-services
```

## Common SAP OData Services

- **API_BUSINESS_PARTNER**: Business partner data (customers, vendors, contacts)
- **API_SALES_ORDER_SRV**: Sales orders and related data
- **API_PRODUCT_SRV**: Product and material master data
- **API_PURCHASEORDER_PROCESS_SRV**: Purchase orders
- **API_MATERIAL_STOCK_SRV**: Material stock and inventory

## Workflow Examples

### Example 1: User asks "Show me the first 10 active business partners from SAP"

1. First, use the metadata command to understand the structure:
   ```bash
   cd .claude/skills/sap-odata-explorer
   npm run metadata -- --service API_BUSINESS_PARTNER --no-file
   ```

2. Then query with appropriate filter:
   ```bash
   npm run query -- --service API_BUSINESS_PARTNER --entity A_BusinessPartner \
     --filter "BusinessPartnerIsBlocked eq false" \
     --top 10 --format pretty --no-file
   ```

3. Read and interpret the results from the output

### Example 2: User asks "What customer data is available in SAP?"

1. Check available services:
   ```bash
   cd .claude/skills/sap-odata-explorer
   npm run list-services
   ```

2. Get metadata for relevant service:
   ```bash
   npm run metadata -- --service API_BUSINESS_PARTNER --no-file
   ```

3. Explain the available entities and properties to the user

### Example 3: User asks "Get sales orders from last month"

1. Query with date filter:
   ```bash
   cd .claude/skills/sap-odata-explorer
   npm run query -- --service API_SALES_ORDER_SRV --entity A_SalesOrder \
     --filter "CreationDate ge datetime'2024-01-01T00:00:00' and CreationDate le datetime'2024-01-31T23:59:59'" \
     --top 50 --format pretty --no-file
   ```

2. Analyze and present the results to the user

## OData Query Syntax

### Filter Operators
- **Comparison**: `eq` (equal), `ne` (not equal), `gt` (greater than), `lt` (less than), `ge` (>=), `le` (<=)
- **Logical**: `and`, `or`, `not`
- **Functions**: `startswith()`, `endswith()`, `contains()`, `length()`, `tolower()`, `toupper()`

### Filter Examples
```
Status eq 'Active'
Price gt 100
CreationDate ge datetime'2024-01-01T00:00:00'
startswith(Name, 'A')
contains(Description, 'premium') and Price lt 1000
```

### Select Syntax
```
--select ID,Name,Status
--select BusinessPartner,FirstName,LastName,City
```

### OrderBy Syntax
```
--orderby Name asc
--orderby CreationDate desc
--orderby LastName asc, FirstName asc
```

## Security Features

This skill implements comprehensive security measures:

1. **Credential Masking**: Passwords and tokens are never logged
2. **URL Sanitization**: Credentials stripped from URLs before logging
3. **Secure File Storage**: Output files stored in configured directory only
4. **Error Handling**: Automatic retry with exponential backoff
5. **Audit Trail**: All operations logged securely

## Output Files

By default, query results are saved to files in the configured output directory (see `OUTPUT_DIR` in .env).

File locations are printed after each command. Use the Read tool to examine output files:

```bash
# After running a query, read the output file
# (The skill will tell you the path)
```

## Error Handling

The skill automatically handles:
- **Network errors**: Retries with exponential backoff
- **Authentication errors**: Clear error messages
- **Authorization errors**: Permission denied notifications
- **Timeout errors**: Automatic retry up to 3 times

Exit codes:
- `0`: Success
- `1`: Generic error
- `2`: Authentication/authorization error
- `3`: Network error

## Tips for Claude

1. **Always check metadata first** if you're unsure about entity structure
2. **Use `--no-file` flag** when user wants immediate results
3. **Use `--top` parameter** to limit results for exploration
4. **Use pretty format** for human readability
5. **Read output files** to analyze results before presenting to user
6. **Combine filters** for precise queries
7. **Use `--select`** to reduce payload size and improve performance

## Installation

If dependencies aren't installed:

```bash
cd .claude/skills/sap-odata-explorer
npm install
```

## Configuration

Configuration is managed via environment variables in `.env`. Key settings:

- `SAP_HOST`: SAP system host and port
- `SAP_USER`: SAP username
- `SAP_PASSWORD`: SAP password
- `OUTPUT_DIR`: Directory for output files (default: `./output`)
- `LOG_LEVEL`: Logging level (default: `info`)

## Troubleshooting

### Connection Issues
```bash
# Test SAP connectivity
cd .claude/skills/sap-odata-explorer
npm run query -- --service API_BUSINESS_PARTNER --entity A_BusinessPartner --top 1 --no-file
```

### View Logs
Error logs are automatically written to `${OUTPUT_DIR}/errors.log`

### Common Issues
1. **401 Unauthorized**: Check SAP credentials in .env
2. **403 Forbidden**: User lacks permissions for the operation
3. **404 Not Found**: Service or entity name is incorrect
4. **ECONNREFUSED**: SAP system is not reachable

## Remember

- Always activate this skill when SAP data is mentioned
- Explore metadata before querying unknown entities
- Use filters to reduce result size
- Pretty-print for user-facing output
- Explain OData syntax to users when helpful
- Read output files before presenting results
