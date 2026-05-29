---
name: analyzing-Objectstar
description: >
  Skill for understanding, editing, analyzing, and migrating TIBCO Objectstar (Object Service Broker) code used in mainframe OTP and batch applications. Activate when user is working with Objectstar rules, asks about mainframe modernization, or legacy 4GL code involving GET, FORALL, or EXCEPTION blocks.
license: Proprietary
metadata:
  author: Legacy Modernization Team
  version: "1.0"
---

# Objectstar Programming Skill

## When to Use This Skill
- User provides Objectstar source code or mentions `.OSB` / MetaStore / screen rules
- User asks about migrating a legacy mainframe system using TIBCO OSB
- User asks about understanding code using `GET`, `FORALL`, `ON GETFAIL`, `DISPLAY`, `REPLACE`, etc.
- Static analysis, refactoring, or modernization of Objectstar code

## Language Overview

Objectstar rules are declarative procedures with four sections:
- **DECLARATION**: Rule name, parameters, LOCAL variables
- **CONDITIONS**: Y/N matrix logic (no IF/THEN/ELSE exists)
- **ACTIONS**: Numbered execution sequence per condition column
- **EXCEPTIONS**: Structured handlers (GETFAIL, LOCKFAIL, etc.)

Used in both interactive OTP (3270 screens) and batch (job stream) contexts.

## Condition Quadrants (Critical Concept)

Objectstar has **no IF/THEN/ELSE**. All conditional logic uses condition quadrants — a Y/N matrix that determines which actions execute.

### Rule Structure
```
RULE_NAME(param1, param2);
LOCAL var1, var2;                   -- Untyped local variables
---------------------------------------------------------------------------
condition1;                         | Y N N    -- Condition rows
condition2;                         |   Y N
------------------------------------------------------------+---------------
action1;                            | 1        -- Action rows (numbered)
action2;                            |   1
action3;                            |     1
---------------------------------------------------------------------------
ON GETFAIL:                                    -- Exception handlers
    handler_action;
```

### How It Works
1. Conditions evaluate top-to-bottom
2. Each column represents a unique combination (like switch cases)
3. Y/N pattern determines which column matches
4. Numbers indicate execution order within that column

### Example: Discount Calculation
```
CALC_DISCOUNT(CUST_TYPE, ORDER_AMT);
LOCAL DISCOUNT;
---------------------------------------------------------------------------
CUST_TYPE = 'PREMIUM';              | Y N N    -- Column 1: Premium
ORDER_AMT > 1000;                   |   Y N    -- Column 2: Large order
------------------------------------------------------------+---------------
DISCOUNT = 0.20;                    | 1        -- 20% for premium
DISCOUNT = 0.10;                    |   1      -- 10% for large orders
DISCOUNT = 0.05;                    |     1    -- 5% default
```

Equivalent pseudo-code:
```
if (CUST_TYPE == 'PREMIUM') { DISCOUNT = 0.20; }
else if (ORDER_AMT > 1000)  { DISCOUNT = 0.10; }
else                        { DISCOUNT = 0.05; }
```

### Key Points
- **No IF/ENDIF** — Always use condition quadrants
- **Columns are mutually exclusive** — Only one column executes
- **Numbers set order** — Multiple actions in a column run in numbered sequence
- **Blank cells** — Condition not evaluated for that column

## Parameterized Tables

Objectstar tables can be **parameterized** — creating logically separate data partitions using the same table definition.

### Syntax
```
TABLE(param1)                    -- Single parameter
TABLE(param1, param2)            -- Multiple parameters
```

### Example: Regional Sales
```
REGIONAL_REPORT(REGION_CODE);
LOCAL TOTAL;
---------------------------------------------------------------------------
TOTAL = 0;
FORALL SALES(REGION_CODE) WHERE YEAR = 2024
    ORDERED DESCENDING AMOUNT
    UNTIL GETFAIL:
    TOTAL = TOTAL + SALES.AMOUNT;
END;
CALL MSGLOG('Total for ' || REGION_CODE || ': ' || TOTAL);
```

Calling with different parameters accesses different data:
```
CALL REGIONAL_REPORT('WEST');    -- Accesses SALES('WEST')
CALL REGIONAL_REPORT('EAST');    -- Accesses SALES('EAST')
```

### Common Use Cases
| Pattern | Example |
|---------|---------|
| Regional partitioning | `SALES(REGION)`, `INVENTORY(WAREHOUSE)` |
| Temporal partitioning | `TRANSACTIONS(YEAR)`, `LOGS(MONTH)` |
| Multi-tenant | `CUSTOMERS(TENANT_ID)` |
| Configuration | `CONFIG(ENVIRONMENT)` |

### Migration Challenge

Parameterized tables have no direct SQL equivalent. Migration options:

**Option 1: Composite Key**
```java
@Entity
public class Sales {
    @EmbeddedId
    private SalesId id;  // Contains region + primary key
}

// Query with region filter
salesRepository.findByIdRegionAndYear("WEST", 2024);
```

**Option 2: Filtered Repository**
```java
public interface SalesRepository {
    @Query("SELECT s FROM Sales s WHERE s.region = :region AND s.year = :year")
    List<Sales> findByRegionAndYear(String region, int year);
}
```

**Option 3: Separate Tables** (for strict isolation)
- `SALES_WEST`, `SALES_EAST` with union views

## Syntax Reference
See [objectstar-syntax.md](references/objectstar-syntax.md) for language keywords and examples.

## Best Practices
✅ Always trap expected exceptions (GETFAIL, INSERTFAIL) locally  
✅ Use primary key WHERE clauses for GET and REPLACE to ensure intent list consistency  
✅ Use EXECUTE for sub-transactions that should commit independently  
✅ Commit periodically in batch jobs to avoid COMMITLIMIT errors  
✅ Use screen tables for passing data in OTP rules and session tables in batch  
✅ Favor BROWSE mode when writing read-only rules  

## Common Pitfalls
❌ Using `ON ERROR` as a general flow control — leads to masked bugs  
❌ FORALL with nested loops over large tables — performance killer  
❌ No COMMIT in long batch loops — causes memory and lock issues  
❌ Hardcoding dataset names and magic values — hinders migration  
❌ Reliance on implicit global state instead of parameter passing  

See [objectstar-pitfalls.md](references/objectstar-pitfalls.md) for deeper explanations.

## Idioms and Patterns
- **Exception loop idiom**:
  ```
  CALL FORALLA('TABLE', ...);
  UNTIL ENDFILE:
    CALL FORALLB('TABLE');
  END;
  CALL FORALLE('TABLE');
  ```

- **Screen data validation rule**:
  ```
  GET CUSTOMER WHERE ID = SCR.ID;
  ON GETFAIL:
    CALL SCREENMSG('SCR', 'Customer not found');
    SIGNAL ERROR;
  ```

- **Batch processing with commit window** (using condition quadrant):
  ```
  BATCH_PROCESS;
  LOCAL COUNT;
  ---------------------------------------------------------------------------
  COUNT = 0;
  FORALL INVOICES UNTIL GETFAIL:
      CALL PROCESS_INVOICE;
      COUNT = COUNT + 1;
      COUNT >= 1000;                      | Y N
      ----------------------------------------+-----
      COMMIT;                             | 1
      COUNT = 0;                          | 2
  END;
  COMMIT;  -- Final commit for remaining
  ```

## Refactoring Instructions
1. Identify use of outdated patterns (e.g. ON ERROR without handler logic)
2. Wrap database access with clear ON handlers
3. Isolate screen logic from core business logic
4. Convert monolithic rules into modular subrules
5. Externalize config (e.g. file names, limits) into control tables

## Static Analysis Checklist
- [ ] Any unhandled exceptions (GETFAIL, LOCKFAIL, etc.)?
- [ ] Large FORALLs without WHERE filters?
- [ ] Broad ON ERROR blocks without rollback or logging?
- [ ] Hardcoded screen transitions or filenames?
- [ ] Rule too long (>200 lines)? Consider modularizing.

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
- [ ] Trace LOCAL variable scope (visible in descendant rules)
- [ ] Document table access patterns (GET/REPLACE/INSERT/DELETE)
- [ ] Identify parameterized table usage

### 3. Control Flow Analysis
- [ ] Map condition quadrant to branching logic
- [ ] Document FORALL patterns and termination conditions
- [ ] Note TRANSFERCALL usage (no return)
- [ ] List all CALL/EXECUTE dependencies

### 4. Exception Analysis
- [ ] List all ON handlers
- [ ] Check handler specificity (table-specific before generic)
- [ ] Identify SIGNAL statements
- [ ] Verify ON ERROR has proper handling

### 5. Documentation
- [ ] Summarize rule purpose
- [ ] Document business logic
- [ ] Note migration concerns
```

### Migration Workflow
```
## Objectstar Migration Progress

### Phase 1: Inventory
- [ ] Extract MetaStor (tables, rules, screens)
- [ ] Classify rules: OTP vs batch vs utility
- [ ] Document parameterized tables
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
- [ ] Convert screens to web forms
- [ ] Map screen tables to DTOs
- [ ] Implement validation rules

### Phase 6: Validation
- [ ] Create test cases from existing behavior
- [ ] Run → Compare → Fix → Repeat
- [ ] Verify transaction semantics preserved
```

### Refactoring Feedback Loop
```
1. Identify anti-pattern (see pitfalls.md)
2. Apply refactoring
3. Verify rule compiles/runs
4. Test affected functionality
5. If issues → revert and retry
6. Document changes
```

## Migration Strategy
- Separate screen vs. data logic into callable modules
- Identify and replicate exception model in target platform (e.g., Java try/catch)
- Translate GET/REPLACE to SQL SELECT/UPDATE with transaction control
- Replace screen tables with data transfer objects (DTOs) or form models
- Use a translation matrix (see reference) to map idioms to modern equivalents

See [objectstar-migration.md](references/objectstar-migration.md).

## Resources
- [Syntax Reference](references/objectstar-syntax.md)
- [Built-in Tools](references/objectstar-tools.md)
- [Known Pitfalls](references/objectstar-pitfalls.md)
- [Migration Guide](references/objectstar-migration.md)
