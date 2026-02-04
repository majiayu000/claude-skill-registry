---
name: tsqlapp-developer
description: Generate production-ready T-SQL scripts for the TSQL.APP framework. Use when creating TSQL.APP action scripts, modal forms, data processing scripts, or any T-SQL code that runs within the TSQL.APP environment. This skill enforces 11 critical mandated practices and ensures procedure verification against the authoritative CSV catalog.
---

# TSQL.APP Developer

Generate runtime-compliant, production-ready T-SQL scripts for the TSQL.APP framework.

## Core Principles (Never Violate)

### 1. CSV Files Are Your Authority

**ALWAYS verify procedures** in the CSV catalog before using them. The framework has 1519 documented procedure parameters.

- **NEVER invent procedure names** - if not in CSV, it doesn't exist
- Extract complete parameter signatures: names, types, required/optional, OUTPUT designation
- Common invented procedures that **DO NOT exist**: `sp_api_modal_title`, `sp_api_modal_info`, `sp_api_modal_warning`, `sp_api_modal_header`, `sp_api_modal_br`, `sp_api_modal_error`

**Use the query script** to verify procedures:

```bash
python scripts/query_procedures.py <procedure_name>
python scripts/query_procedures.py --search <pattern>
```

### 2. The 11 Mandated Practices

Every script MUST follow these practices without exception:

1. **Use `sys.objects` for existence checks** (not `sys.tables`)
2. **Declare ALL variables at script start** (no late declarations)
3. **NEVER pass calculations to procedures** - prepare in variables first
4. **Only use documented procedures** (verify in CSV)
5. **Use `dbo.main_db()` for source database references** (never hardcode)
6. **Synchronize state BEFORE drawing UI** (`sp_api_modal_get_value`)
7. **Reset button state after validation errors** (`sp_api_modal_value @name=N'@Button', @value=NULL`)
8. **Never redeclare TSQL.APP context variables** (@card_id, @id, @ids, @user, etc.)
9. **Define temp tables only once** (not in different branches)
10. **Use Unicode**: NVARCHAR with N prefix, never VARCHAR
11. **Dedicated OUTPUT variable for each control** (no reuse)

### 3. Reactive Execution Model

Scripts re-execute on every user interaction. Follow this structure:

```sql
-- STEP 1: Declare variables (ALL at top)
DECLARE @Input NVARCHAR(MAX);
DECLARE @Button NVARCHAR(MAX);
DECLARE @Message NVARCHAR(MAX);

-- STEP 2: Sync state (get current values from framework)
EXEC sp_api_modal_get_value @name=N'@Input', @value=@Input OUT;
EXEC sp_api_modal_get_value @name=N'@Button', @value=@Button OUT;

-- STEP 3: Draw UI (every execution)
EXEC sp_api_modal_text @text=N'Title', @class=N'h3';
EXEC sp_api_modal_input @name=N'@Input', @value=@Input OUT;
EXEC sp_api_modal_button @name=N'@Button', @value=N'Submit', @valueout=@Button OUT;

-- STEP 4: Pause point (wait for user action)
IF @Button IS NULL RETURN;

-- STEP 5: Handle action (validation + processing)
IF @Button IS NOT NULL
BEGIN
    -- Validate input
    IF LEN(TRIM(ISNULL(@Input, N''))) < 2
    BEGIN
        SET @Message = N'Input required';
        EXEC sp_api_toast @text=@Message, @class=N'btn-warning';
        EXEC sp_api_modal_value @name=N'@Button', @value=NULL;  -- CRITICAL: Reset button
        RETURN;
    END
    
    -- Process and succeed
    SET @Message = N'Success!';
    EXEC sp_api_toast @text=@Message, @class=N'btn-success';
    EXEC sp_api_modal_clear;
END
```

## Code Generation Workflow

Follow these phases for every code generation request:

### Phase 1: Analysis

- Analyze user requirements
- Identify UI components needed
- List all procedures that will be required
- Determine data sources and operations

### Phase 2: CSV Verification (CRITICAL)

For **EACH** procedure in the list:

1. Run query script: `python scripts/query_procedures.py <proc_name>`
2. If not found: Search for alternatives with `--search` flag
3. If found: Extract complete parameter signature
4. Document required vs optional parameters
5. Identify OUTPUT parameters

**STOP if any procedure not found without acceptable alternative.**

### Phase 3: Structure Planning

- List all required variables (UI + business logic)
- Plan state synchronization calls
- Design UI component order
- Identify pause points (flow control)
- Plan validation and error handling

### Phase 4: Code Generation

Generate code following this order:

1. Variable declarations (all at top, grouped by purpose)
2. State synchronization calls
3. UI drawing code with verified procedures
4. Pause point logic
5. Business logic with validation and button reset
6. Success/cleanup code

**Inline validation**: As each EXEC is written, verify parameter names match CSV.

### Phase 5: Post-Generation Review

Validate against checklist:

- ✓ All variables declared at top
- ✓ No calculations in EXEC parameters
- ✓ All procedures verified to exist
- ✓ All parameters match CSV documentation
- ✓ State sync before UI drawing
- ✓ Button reset after validation errors
- ✓ Unicode compliance (NVARCHAR, N prefix)
- ✓ Each control has dedicated OUT variable
- ✓ Temp tables defined once
- ✓ `dbo.main_db()` used for cross-database
- ✓ `sys.objects` used for existence checks

## Common Patterns

### Basic Modal Form

```sql
-- Variables
DECLARE @Name NVARCHAR(MAX);
DECLARE @Email NVARCHAR(MAX);
DECLARE @Submit NVARCHAR(MAX);
DECLARE @Message NVARCHAR(MAX);

-- Sync state
EXEC sp_api_modal_get_value @name=N'@Name', @value=@Name OUT;
EXEC sp_api_modal_get_value @name=N'@Email', @value=@Email OUT;
EXEC sp_api_modal_get_value @name=N'@Submit', @value=@Submit OUT;

-- Draw UI
EXEC sp_api_modal_text @text=N'User Information', @class=N'h3';
EXEC sp_api_modal_input @name=N'@Name', @value=@Name OUT;
EXEC sp_api_modal_input @name=N'@Email', @value=@Email OUT;
EXEC sp_api_modal_button @name=N'@Submit', @value=N'Submit', @valueout=@Submit OUT;

-- Pause
IF @Submit IS NULL RETURN;

-- Handle
IF @Submit IS NOT NULL
BEGIN
    -- Validate
    IF LEN(TRIM(ISNULL(@Name, N''))) = 0 OR LEN(TRIM(ISNULL(@Email, N''))) = 0
    BEGIN
        SET @Message = N'All fields required';
        EXEC sp_api_toast @text=@Message, @class=N'btn-warning';
        EXEC sp_api_modal_value @name=N'@Submit', @value=NULL;
        RETURN;
    END
    
    -- Process (insert/update logic here)
    
    -- Success
    SET @Message = N'Saved successfully';
    EXEC sp_api_toast @text=@Message, @class=N'btn-success';
    EXEC sp_api_modal_clear;
END
```

### Cross-Database Access

```sql
DECLARE @SourceDB NVARCHAR(128) = dbo.main_db();
DECLARE @SQL NVARCHAR(MAX);
DECLARE @Count INT;

-- Build dynamic SQL
SET @SQL = CONCAT(
    N'SELECT @Count = COUNT(*) FROM [', @SourceDB, N'].[dbo].[Customers]'
);

-- Execute with parameters
EXEC sp_executesql @SQL, N'@Count INT OUTPUT', @Count = @Count OUTPUT;
```

### Display Data Table

```sql
-- Variables
DECLARE @SQL NVARCHAR(MAX);
DECLARE @SourceDB NVARCHAR(128) = dbo.main_db();

-- Build query
SET @SQL = CONCAT(
    N'SELECT TOP 100 CustomerID, CustomerName, Email ',
    N'FROM [', @SourceDB, N'].[dbo].[Customers] ',
    N'ORDER BY CustomerName'
);

-- Display in modal
EXEC sp_api_modal_text @text=N'Customer List', @class=N'h3';
EXEC sp_api_modal_table @sql=@SQL;
```

## Critical Errors to Prevent

### ❌ Don't Do

```sql
-- Invented procedure
EXEC sp_api_modal_title @text = N'Title';

-- Calculation in parameter
EXEC sp_api_toast @text = CONCAT(N'Hello ', @Name);

-- Late variable declaration
SET @Msg = N'Hello';
DECLARE @Msg NVARCHAR(MAX);

-- Missing button reset
IF @Input IS NULL
BEGIN
    EXEC sp_api_toast @text = N'Required';
    RETURN;  -- BUG: button still has value
END
```

### ✅ Do This

```sql
-- Use documented procedure with @class
DECLARE @Title NVARCHAR(MAX);
SET @Title = N'Title';
EXEC sp_api_modal_text @text = @Title, @class = N'h3';

-- Prepare value first
DECLARE @Msg NVARCHAR(MAX);
SET @Msg = CONCAT(N'Hello ', @Name);
EXEC sp_api_toast @text = @Msg;

-- All variables at top
DECLARE @Msg NVARCHAR(MAX);
SET @Msg = N'Hello';

-- Reset button state
IF @Input IS NULL
BEGIN
    EXEC sp_api_toast @text = N'Required';
    EXEC sp_api_modal_value @name = N'@Button', @value = NULL;
    RETURN;
END
```

## When Uncertain

If uncertain about any procedure, parameter, or feature:

1. **STOP** - Don't guess or invent
2. **STATE**: "I need to verify [procedure/parameter] in the CSV catalog"
3. **SEARCH**: Run query script or check CSV
4. **RESPOND**: Only after verification

## Reference Documentation

Detailed documentation available in `references/`:

- **tsql_bootstrap.md** - Quick reference and bootstrap instructions
- **tsqlapp_part0_summary_index_v2.xml** - Complete overview and index
- **tsqlapp_part1_mandates.xml** - Detailed explanation of 11 mandated practices
- **tsqlapp_part2_procedures.xml** - Core framework procedures with examples
- **tsqlapp_part3_patterns.xml** - Complete working patterns for common scenarios
- **tsqlapp_part4_ai_instructions.xml** - AI-specific workflow and validation
- **tsqlapp_part5_csv_guide.xml** - CSV verification methods and examples
- **tsql.app_procs-all.csv** - Complete procedure catalog (1519 rows)

Read these files when you need deeper understanding of specific topics.

## Quality Standards

Generated code must achieve:

- **100% CSV verification** - every procedure exists in documentation
- **100% mandated practices** - all 11 rules followed
- **100% first-time-right** - code executes without errors
- **Complete scripts** - no placeholders, no "TODO" comments
- **Production-ready** - includes validation, error handling, user feedback

## Response Pattern

When generating code:

1. Acknowledge the request
2. Verify procedures in CSV (mention this explicitly)
3. Generate compliant code
4. Explain key patterns used
5. Highlight validation or error handling

**Remember**: You generate code that runs in production. Errors cost time and money. When in doubt, verify first.
