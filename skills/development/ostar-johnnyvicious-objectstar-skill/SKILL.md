---
name: reviewing-Objectstar
description: Analyze, refactor, and migrate TIBCO Objectstar (Object Service Broker) legacy mainframe applications. Use when working with Objectstar/OSB source code files, rules, screen definitions, or table definitions. Triggers on .osr, .osb file extensions, or code containing Objectstar patterns like condition quadrants (Y N columns), FORALL loops, TRANSFERCALL, parameterized tables, or rules with LOCAL declarations.
---

# Objectstar Language Skill

Objectstar is a rules-based 4GL mainframe platform using condition quadrants instead of IF/THEN/ELSE, tables instead of objects, and rules instead of programs. Extended support ends March 30, 2027.

## Core Workflow

1. **Identify Objectstar code** → Look for condition quadrants, FORALL loops, parameterized tables
2. **Understand rule structure** → Parse the four-section format (declaration, conditions, actions, handlers)
3. **Analyze data flow** → Track LOCAL variable scope (visible in descendant rules)
4. **For refactoring** → Apply patterns from [patterns.md](references/patterns.md)
5. **For migration** → Map constructs using [migration.md](references/migration.md)

## Rule Structure (Fundamental Unit)

Every Objectstar rule has four sections:

```
RULE_NAME(arg1, arg2);              -- 1. Declaration
LOCAL var1, var2;                   -- Local variables (untyped)
---------------------------------------------------------------------------
condition1;                         | Y N N    -- 2. Conditions (Y/N columns)
condition2;                         |   Y N
------------------------------------------------------------+---------------
action1;                            | 1        -- 3. Actions (numbered sequence)
action2;                            |   1
action3;                            |     1
---------------------------------------------------------------------------
ON exception_name:                             -- 4. Exception handlers
    handler_statement;
```

**Condition quadrant logic**: Conditions evaluate top-to-bottom. The Y/N pattern in each column determines which action column executes. Numbers indicate execution order within a column.

## Critical Language Rules

### Variable Scoping (Non-Standard)
LOCAL variables are visible in the declaring rule AND all descendant rules (rules called from within). This breaks encapsulation—track carefully during migration.

### No Traditional Loops
- **No WHILE/FOR** — Use `FORALL` for iteration over table occurrences
- **No IF/THEN/ELSE** — Use condition quadrant Y/N patterns
- Loop termination via `UNTIL exception:` pattern

### Data Types Are Dual-Classified
Semantic types (C=Count, D=Date, I=Identifier, L=Logical, Q=Quantity, S=String) define meaning. Syntax types (B=Binary, C=Char, P=Packed, V=Variable, F=Float, UN=Unicode) define storage. Variables inherit type from assigned values.

### Everything Is a Table
Screens, reports, data stores, even rule storage—all tables. Table types: TDS (permanent), SCR (screen), TEM (temporary), SES (session), MAP (memory mapping), SUB (subview).

### OTP vs Batch Contexts

Objectstar rules run in two distinct contexts with different patterns:

| Aspect | OTP (Online Transaction Processing) | Batch Processing |
|--------|-------------------------------------|------------------|
| **Interface** | 3270 terminal screens | Job streams (JCL/scripts) |
| **User interaction** | Interactive, screen-driven | Unattended, scheduled |
| **Data passing** | Screen tables (SCR) | Session tables (SES), parameters |
| **Transaction model** | Short, user-paced commits | Long-running, periodic commits |
| **Error handling** | SCREENMSG for user feedback | MSGLOG for logging |
| **Typical patterns** | DISPLAY loops, TRANSFERCALL | FORALL with COMMIT windows |

**OTP Pattern** (screen-driven):
```
UNTIL EXIT_DISPLAY DISPLAY ORDER_SCREEN:
    CALL VALIDATE_ORDER;
    CALL SAVE_ORDER;
END;
ON EXIT_DISPLAY:
    CALL CLEANUP;
```

**Batch Pattern** (commit window):
```
LOCAL COUNT;
COUNT = 0;
FORALL INVOICES UNTIL GETFAIL:
    CALL PROCESS_INVOICE;
    COUNT = COUNT + 1;
    COUNT >= 1000;                      | Y N
    ----------------------------------------+-----
    COMMIT;                             | 1
    COUNT = 0;                          | 2
END;
COMMIT;  -- Final commit
```

**Migration implications**:
- OTP rules → Web controllers with form handling
- Batch rules → Scheduled jobs, message queues, or streaming APIs
- Classify rules early (OTP/Batch/Shared utility) before migration

## Essential Syntax Quick Reference

### Rule Invocation
```
CALL rule(args);                    -- Same transaction, returns
EXECUTE IN UPDATE rule(args);       -- Child transaction
SCHEDULE TO QUEUE rule(args);       -- Async batch
TRANSFERCALL rule(args);            -- Transfer control, no return
```

### Data Operations
```
GET TABLE WHERE field = value;
GET TABLE(param) ORDERED DESCENDING field WITH MINLOCK;
INSERT TABLE;
REPLACE TABLE;
DELETE TABLE WHERE field = value;
```

### Iteration
```
FORALL TABLE(param) WHERE condition
    ORDERED ASCENDING field
    UNTIL GETFAIL:
    -- process each occurrence
END;

UNTIL EXIT_DISPLAY DISPLAY SCREEN:
    -- process until exit
END;
```

### WHERE Clause Operators
```
=, >, <, >=, <=       -- Comparison
¬= or NOT =           -- Not equal
& or AND              -- Conjunction
| or OR               -- Disjunction
¬ or NOT              -- Negation
LIKE 'ABC*'           -- * matches any string
LIKE 'AB?D'           -- ? matches single char
```

### Exception Handling
```
ON GETFAIL:           -- Record not found
ON GETFAIL TABLE:     -- Table-specific
ON ACCESSFAIL:        -- Any access failure
ON ERROR:             -- Catch-all (use last)
SIGNAL CUSTOM_ERR;    -- Raise exception
```

### String Operations
```
str1 || str2                        -- Concatenation
LENGTH(s), SUBSTRING(s,start,len)
UPPERCASE(s), LOWERCASE(s)
MATCH(s, pattern), PAD(s,len,char,just)
```

## Reserved Keywords

```
AND        ASCENDING    BROWSE      CALL        COMMIT      CONTINUE
DELETE     DESCENDING   DISPLAY     END         EXECUTE     FORALL
GET        IN           INSERT      LIKE        LOCAL       NOT
NULL       ON           OR          ORDERED     PRINT       REPLACE
RETURN     ROLLBACK     SCHEDULE    SIGNAL      TO          TRANSFERCALL
UNTIL      UPDATE       WHERE
```

## Common Exception Hierarchy

```
ERROR (catch-all)
├── ACCESSFAIL
│   ├── GETFAIL, INSERTFAIL, REPLACEFAIL, DELETEFAIL
│   └── DISPLAYFAIL, SERVERFAIL
├── INTEGRITYFAIL
│   ├── COMMITLIMIT, LOCKFAIL, VALIDATEFAIL
└── RULEFAIL
    ├── ZERODIVIDE, OVERFLOW, CONVERSION
    └── NULLVALUE, STRINGSIZE, SECURITYFAIL
```

## Workflow Checklists

Copy these checklists to track progress on complex tasks.

### Code Analysis Workflow

```
## Objectstar Analysis Progress

### 1. Structure Identification
- [ ] Locate rule declaration and arguments
- [ ] Identify LOCAL variables
- [ ] Map condition quadrant columns
- [ ] List action sequence numbers

### 2. Data Flow Analysis
- [ ] Trace LOCAL variable scope chain (which descendant rules use them?)
- [ ] Document table access patterns (GET/REPLACE/INSERT/DELETE)
- [ ] Identify parameterized table usage (e.g., `TABLE(REGION)`)

### 3. Control Flow Analysis
- [ ] Map condition quadrant to equivalent branching logic
- [ ] Document FORALL iteration patterns and termination conditions
- [ ] Note TRANSFERCALL usage (breaks return flow)
- [ ] List all CALL/EXECUTE dependencies

### 4. Exception Analysis
- [ ] List all exception handlers (ON statements)
- [ ] Check handler specificity (table-specific before generic)
- [ ] Identify SIGNAL statements and custom exceptions
- [ ] Verify catch-all ON ERROR has proper handling

### 5. Documentation
- [ ] Summarize rule purpose
- [ ] Document non-obvious business logic
- [ ] Note migration concerns
```

### Migration Workflow

```
## Objectstar Migration Progress

### Phase 1: Inventory
- [ ] Extract complete MetaStor (tables, rules, screens)
- [ ] Classify rules: OTP screen logic vs batch vs shared utility
- [ ] Document all parameterized tables
- [ ] Map CALL/EXECUTE/TRANSFERCALL dependencies

### Phase 2: Schema Migration
- [ ] Map TDS tables to relational schema
- [ ] Convert parameterized tables to composite keys
- [ ] Define foreign key relationships
- [ ] Create JPA entities

### Phase 3: Logic Migration (per rule)
- [ ] Convert condition quadrants to decision logic
- [ ] Map LOCAL variables to typed Java fields
- [ ] Handle scope chain with context objects
- [ ] Convert FORALL to repository queries + streams

### Phase 4: Exception Handling
- [ ] Map Objectstar exceptions to Java exceptions
- [ ] Convert ON handlers to try-catch blocks
- [ ] Implement transaction boundaries (@Transactional)

### Phase 5: UI Migration (if OTP)
- [ ] Convert screens to web forms (MVC)
- [ ] Map screen tables to DTOs
- [ ] Implement validation rules

### Phase 6: Validation
- [ ] Create test cases from existing behavior
- [ ] Run → Compare outputs → Fix discrepancies → Repeat
- [ ] Verify transaction semantics preserved
```

### Refactoring Feedback Loop

For iterative improvement, use this pattern:

```
1. Identify anti-pattern (see patterns.md)
2. Apply refactoring
3. Verify rule still compiles/runs
4. Test affected functionality
5. If issues found → revert and retry with different approach
6. Document changes made
```

## Refactoring Guidelines

1. **Simplify condition quadrants** — Consolidate redundant Y/N columns
2. **Extract common patterns** — Repeated FORALL/GET sequences → separate rules
3. **Standardize exception handling** — Table-specific before generic
4. **Document scope dependencies** — LOCAL variables used across rule calls
5. **Add Browse hints** — Use Browse Mode for read-only operations

For anti-patterns to avoid during refactoring, see [pitfalls.md](references/pitfalls.md).

## Migration Priorities

For Java migration, address these semantic gaps (see [migration.md](references/migration.md) for details):

1. **Untyped LOCAL variables** → Type inference or wrapper classes
2. **Descendant scope visibility** → Custom scope chain management
3. **Parameterized tables** → Composite keys + filtered queries
4. **Condition quadrants** → Decision tables or switch expressions
5. **TRANSFERCALL** → Explicit control flow refactoring

## Reference Files

- [syntax.md](references/syntax.md) — Complete syntax reference with all data types
- [patterns.md](references/patterns.md) — Common code patterns with examples
- [pitfalls.md](references/pitfalls.md) — Anti-patterns and common mistakes to avoid
- [migration.md](references/migration.md) — Java migration mappings and strategies
- [tools.md](references/tools.md) — Built-in shareable tools reference
