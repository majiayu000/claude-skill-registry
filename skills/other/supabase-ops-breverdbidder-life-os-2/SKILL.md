---
name: supabase-ops
description: Supabase database operations for BidDeed.AI and Life OS ecosystems. Handles inserts, queries, and data management for tables including insights, historical_auctions, activities, daily_metrics, michael_swim_times, learning_sessions. Use when logging data, querying Supabase, running insert_insight.yml workflows, or managing persistent storage. Database: mocerqjnksmhcjzxrewo.supabase.co
---

# Supabase Operations

## Connection Details

```
Host: mocerqjnksmhcjzxrewo.supabase.co
Service Role Key: eyJ... (in GitHub Secrets as SUPABASE_KEY)
IAT: 1764532526
```

## Core Tables

### insights
General-purpose logging table for all ecosystems.

```sql
CREATE TABLE insights (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMP DEFAULT NOW(),
  source VARCHAR(50),        -- 'biddeed', 'life_os', 'michael_swim'
  category VARCHAR(50),      -- 'learning', 'claude_performance', 'auction'
  title VARCHAR(255),
  content TEXT,
  metadata JSONB
);
```

**Insert Pattern:**
```python
def log_insight(source: str, category: str, title: str, content: str, metadata: dict = None):
    supabase.table('insights').insert({
        'source': source,
        'category': category,
        'title': title,
        'content': content,
        'metadata': metadata or {}
    }).execute()
```

### historical_auctions
BidDeed.AI auction data (1,393+ rows).

```sql
CREATE TABLE historical_auctions (
  id UUID PRIMARY KEY,
  case_number VARCHAR(50),
  property_address TEXT,
  plaintiff VARCHAR(255),
  judgment_amount DECIMAL,
  sale_date DATE,
  final_bid DECIMAL,
  third_party_won BOOLEAN,
  ml_predicted_probability FLOAT,
  our_recommendation VARCHAR(10),  -- 'BID', 'REVIEW', 'SKIP'
  actual_outcome TEXT
);
```

### daily_metrics
Smart Router cost tracking and API usage.

```sql
CREATE TABLE daily_metrics (
  id UUID PRIMARY KEY,
  date DATE,
  tier VARCHAR(20),
  model VARCHAR(50),
  calls INTEGER,
  input_tokens INTEGER,
  output_tokens INTEGER,
  cost_usd DECIMAL(10,4)
);
```

### michael_swim_times
Michael D1 Swimming performance tracking.

```sql
CREATE TABLE michael_swim_times (
  id UUID PRIMARY KEY,
  date DATE,
  meet_name VARCHAR(255),
  event VARCHAR(50),          -- '50 Free', '100 Fly', etc.
  time_seconds DECIMAL(6,2),
  time_formatted VARCHAR(10), -- '22.45'
  course VARCHAR(5),          -- 'SCY', 'LCM'
  is_pb BOOLEAN,
  notes TEXT
);
```

### auction_results
V14.4 lien discovery integration.

```sql
CREATE TABLE auction_results (
  id UUID PRIMARY KEY,
  case_number VARCHAR(50),
  run_date DATE,
  lien_discovery JSONB,       -- AcclaimWeb results
  do_not_bid BOOLEAN,
  reason TEXT,                -- 'Senior mortgage survives'
  recommendation VARCHAR(10)
);
```

## GitHub Actions Integration

Both repos use `insert_insight.yml` workflow:

```yaml
# .github/workflows/insert_insight.yml
name: Insert Insight
on:
  workflow_dispatch:
    inputs:
      source:
        required: true
      category:
        required: true
      title:
        required: true
      content:
        required: true

jobs:
  insert:
    runs-on: ubuntu-latest
    steps:
      - name: Insert to Supabase
        run: |
          curl -X POST '${{ secrets.SUPABASE_URL }}/rest/v1/insights' \
            -H "apikey: ${{ secrets.SUPABASE_KEY }}" \
            -H "Authorization: Bearer ${{ secrets.SUPABASE_KEY }}" \
            -H "Content-Type: application/json" \
            -d '{
              "source": "${{ inputs.source }}",
              "category": "${{ inputs.category }}",
              "title": "${{ inputs.title }}",
              "content": "${{ inputs.content }}"
            }'
```

## Query Patterns

### Get Recent Insights
```sql
SELECT * FROM insights 
WHERE source = 'biddeed' 
ORDER BY created_at DESC 
LIMIT 10;
```

### Auction Performance Analysis
```sql
SELECT 
  plaintiff,
  COUNT(*) as cases,
  AVG(CASE WHEN third_party_won THEN 1 ELSE 0 END) as third_party_rate,
  AVG(ml_predicted_probability) as avg_prediction
FROM historical_auctions
GROUP BY plaintiff
ORDER BY cases DESC;
```

### Michael Swim Progress
```sql
SELECT event, MIN(time_seconds) as best_time, COUNT(*) as races
FROM michael_swim_times
WHERE course = 'SCY'
GROUP BY event;
```

## CRITICAL RULES

1. **Never use local curl** - Always use GitHub Actions workflows
2. **Never expose service key** - Keep in GitHub Secrets only
3. **Use proper IAT** - Key with iat:1764532526 is current
4. **Log to insights first** - Generic logging table for all purposes
