---
name: supabase-integration
description: >
  Unified database operations for BidDeed.AI and Life OS ecosystems. 
  Use when: (1) logging insights, activities, or learning sessions, 
  (2) querying historical data from any table, (3) user says "log this" 
  or "save to database", (4) storing auction results, task states, 
  swim times, or health metrics. Database: mocerqjnksmhcjzxrewo.supabase.co
---

# Supabase Integration

## Overview

Centralized database layer for all Shapira ecosystem data persistence. Executes via GitHub Actions workflows - never local curl.

## Connection Details

- **Project URL:** `https://mocerqjnksmhcjzxrewo.supabase.co`
- **Service Role Key:** Stored in GitHub secrets as `SUPABASE_SERVICE_ROLE_KEY`
- **Key IAT:** 1764532526

## Table Schema

### BidDeed.AI Tables
| Table | Purpose | Key Fields |
|-------|---------|------------|
| `historical_auctions` | Auction records (1,393+ rows) | case_number, judgment, sale_price, outcome |
| `auction_results` | Active analysis | case_number, max_bid, recommendation, liens |
| `daily_metrics` | Pipeline performance | date, properties_analyzed, accuracy |

### Life OS Tables
| Table | Purpose | Key Fields |
|-------|---------|------------|
| `tasks` | Task state machine | id, description, state, complexity, domain |
| `activities` | Activity log (12+ rows) | id, category, description, timestamp |
| `learning_sessions` | YouTube/podcast insights | source, key_takeaways, business_application |
| `health_logs` | Sleep, energy tracking | date, sleep_hours, energy_1_10 |
| `michael_swim_times` | Race results | event, time, meet, date |
| `michael_nutrition` | Keto adherence | date, day_type, meals |
| `michael_recruiting` | D1 outreach | school, contact, status |
| `task_interventions` | ADHD intervention log | task_id, level, timestamp |

### Shared Tables
| Table | Purpose | Key Fields |
|-------|---------|------------|
| `insights` | Cross-domain knowledge | category, content, tags |
| `goals` | OKRs and targets | domain, objective, key_result, progress |

## Workflow: Insert Data

**Trigger:** User says "log this", task completion, auction analysis, learning capture

1. Identify target table from context
2. Format payload matching schema
3. Execute via GitHub Actions workflow

```bash
# GitHub Actions dispatch (not local curl)
# See: .github/workflows/insert_insight.yml in both repos
```

### Insert Patterns by Domain

**BidDeed.AI - Auction Result:**
```json
{
  "table": "auction_results",
  "data": {
    "case_number": "05-2024-CA-012345",
    "property_address": "123 Main St, Melbourne, FL",
    "judgment_amount": 150000,
    "max_bid": 82500,
    "recommendation": "BID",
    "liens": [{"type": "HOA", "amount": 5000}]
  }
}
```

**Life OS - Task:**
```json
{
  "table": "tasks",
  "data": {
    "description": "Review Q4 insurance renewals",
    "state": "INITIATED",
    "complexity": 6,
    "clarity": 8,
    "domain": "BUSINESS",
    "estimated_minutes": 45
  }
}
```

**Life OS - Learning Session:**
```json
{
  "table": "learning_sessions",
  "data": {
    "source": "YouTube: How to 10x Your Real Estate Portfolio",
    "key_takeaways": ["Leverage OPM", "Focus on cash flow"],
    "business_application": "Apply to Everest Capital deal structuring"
  }
}
```

## Workflow: Query Data

**Trigger:** "show me", "what were", "find", historical lookup

1. Construct query with filters
2. Execute via Supabase client
3. Return formatted results

### Query Examples

```sql
-- Recent tasks by domain
SELECT * FROM tasks 
WHERE domain = 'BUSINESS' 
AND state != 'COMPLETED'
ORDER BY created_at DESC LIMIT 10;

-- Auction performance
SELECT recommendation, COUNT(*) 
FROM auction_results 
GROUP BY recommendation;

-- Michael's best times by event
SELECT event, MIN(time) as pr 
FROM michael_swim_times 
GROUP BY event;
```

## LangGraph Integration

### Input Schema
```python
class SupabaseInput(TypedDict):
    operation: str  # "insert" | "query" | "update"
    table: str
    data: dict  # For insert/update
    filters: dict  # For query
```

### Output Schema
```python
class SupabaseOutput(TypedDict):
    success: bool
    rows_affected: int
    data: list  # Query results
    error: Optional[str]
```

### Node Implementation
```python
def supabase_node(state: dict) -> dict:
    """Execute Supabase operation as LangGraph node."""
    from supabase import create_client
    
    client = create_client(
        "https://mocerqjnksmhcjzxrewo.supabase.co",
        os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    )
    
    if state["operation"] == "insert":
        result = client.table(state["table"]).insert(state["data"]).execute()
    elif state["operation"] == "query":
        query = client.table(state["table"]).select("*")
        for k, v in state["filters"].items():
            query = query.eq(k, v)
        result = query.execute()
    
    return {"success": True, "data": result.data}
```

## Scripts

- `scripts/insert_insight.py` - Generic insert with validation
- `scripts/query_builder.py` - Dynamic query construction

## References

- `references/schema_details.md` - Full column definitions and constraints
- `references/migration_history.md` - Schema evolution log

## Best Practices

1. **Always use GitHub Actions** - Never local curl to Supabase
2. **Validate before insert** - Check required fields
3. **Use timestamps** - All tables have created_at/updated_at
4. **Category consistency** - Use defined categories (BUSINESS, MICHAEL, FAMILY, PERSONAL)
