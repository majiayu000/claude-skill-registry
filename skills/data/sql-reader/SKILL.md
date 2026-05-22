---
name: sql-reader
description: Query production PostgreSQL database with read-only credentials. Use for investigating data, debugging issues, or analyzing application state.
---

# SQL Reader Skill

Query production PostgreSQL database using read-only credentials stored in Arsenal environment configuration.

## 🚨 MANDATORY: Read Data Quirks First

**BEFORE querying the database, you MUST read the data quirks documentation:**

```bash
cat docs/sql/DATA_QUIRKS.md
```

**Why:** The database has critical semantic quirks that will cause incorrect queries if not understood:
- NULL values have clinical meaning (not "missing data")
- Data inconsistencies require special query patterns
- Volume normalization is required for accuracy

**DO NOT skip this step. Read the file every time before querying.**

---

## When to Use

Use this skill when you need to:
- Investigate data issues in production
- Debug application state
- Analyze user data or conversation history
- Verify database schema or table contents
- Count records or check data integrity
- Understand database structure and relationships

## Database Selection: Production vs Development

**CRITICAL: Always prefer PRODUCTION database for usage/analytics questions.**

The `arsenal/.env` file should be configured with **production read-only credentials** by default.

### When to Use Production Database (DEFAULT)
- ✅ **User analytics**: "How many messages in the last day?"
- ✅ **Usage patterns**: "Any requests for codel/wren?"
- ✅ **Data investigation**: "What conversations exist?"
- ✅ **Debugging user issues**: "Why didn't user X get a message?"
- ✅ **Schema exploration**: Understanding production data model
- ✅ **ANY question about real users or real usage**

### When to Use Development Database (RARE)
- ⚠️ **Code debugging only**: Testing migration scripts locally
- ⚠️ **Local development**: Verifying local Docker database setup
- ⚠️ **Test data verification**: Checking test fixtures

### How to Switch Databases

**Production (default):**
```bash
# arsenal/.env should have:
PGHOST=codel-prod.cluster-crsis4w6ckj7.us-east-2.rds.amazonaws.com
PGDATABASE=codelprod
PGUSER=metabase_readonly_prod
```

**Development (only when explicitly needed):**
```bash
# Temporarily change arsenal/.env to:
PGHOST=localhost
PGDATABASE=codel
PGUSER=codel
```

**⚠️ WARNING:** Always switch back to production credentials after development queries.

## Data Model Quickstart (Run These First!)

**IMPORTANT**: When first exploring the database or debugging an issue, **ALWAYS run these 6 quickstart commands** to understand the data model:

**⚠️ NOTE**: Command 3 shows 5 core tables. The deprecated `codel_conversations` and `codel_conversation_recipients` tables (stopped receiving data Aug 27, 2025) are NOT included in the bootstrap commands. For recent interventions, use `intervention` + `intervention_message` tables instead.

### 1. See All Tables with Sizes
```bash
arsenal/dot-claude/skills/sql-reader/connect.sh "
SELECT table_name,
       pg_size_pretty(pg_total_relation_size('public.' || table_name)) as size,
       (SELECT COUNT(*) FROM information_schema.columns c
        WHERE c.table_name = t.table_name) as columns
FROM information_schema.tables t
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE'
ORDER BY pg_total_relation_size('public.' || table_name) DESC
LIMIT 20;
"
```

### 2. See Foreign Key Columns (Relationships)
```bash
arsenal/dot-claude/skills/sql-reader/connect.sh "
SELECT DISTINCT
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE column_name LIKE '%_id'
  AND table_schema = 'public'
ORDER BY table_name, column_name;
"
```

### 3. Describe Key Table Structures
```bash
# Show structure of critical tables to answer common questions
arsenal/dot-claude/skills/sql-reader/connect.sh "
-- persons table (user data)
SELECT 'persons' as table_name, column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'persons'
ORDER BY ordinal_position;
"

arsenal/dot-claude/skills/sql-reader/connect.sh "
-- conversation_participant table (who is in which conversation, with what role)
SELECT 'conversation_participant' as table_name, column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'conversation_participant'
ORDER BY ordinal_position;
"

arsenal/dot-claude/skills/sql-reader/connect.sh "
-- message table (all messages sent)
SELECT 'message' as table_name, column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'message'
ORDER BY ordinal_position;
"

arsenal/dot-claude/skills/sql-reader/connect.sh "
-- intervention table (intervention decisions/triggers - logs when AI decides intervention is needed)
SELECT 'intervention' as table_name, column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'intervention'
ORDER BY ordinal_position;
"

arsenal/dot-claude/skills/sql-reader/connect.sh "
-- intervention_message table (actual intervention messages sent to users)
SELECT 'intervention_message' as table_name, column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'intervention_message'
ORDER BY ordinal_position;
"
```

### 4. Read the Enums (Types, States, Roles)
```bash
cat api/src/data/models/enums.py
```

### 5. See All Data Models
```bash
grep "^class.*Base" api/src/data -r --include="*.py" | grep -v test
```

### 6. View Intervention Logic (CRITICAL for Understanding Data Model)
```bash
# First refresh the prompt cache to get latest intervention conditions
cd .claude/skills/langfuse-prompt-and-trace-debugger
uv run python refresh_prompt_cache.py group_message_intervention_conditions_dsl

# Then view the intervention logic
cat ../../docs/cached_prompts/group_message_intervention_conditions_dsl_production.txt
```

**Why this matters:**
- Shows when interventions trigger
- Explains timing rules (last minute, last 6 hours, etc.)
- Maps intervention types to Langfuse prompts used
- Reveals the DSL logic behind intervention decisions
- Critical for understanding `intervention` and `intervention_message` tables

**🚨 CRITICAL SCHEMA INSIGHT - Schema Migrations (Late August 2025):**

Multiple schema migrations occurred in late August 2025. The old tables were NOT migrated - they contain historical data only.

**INTERVENTION TRACKING MIGRATION (Aug 27-28, 2025):**

**DEPRECATED (stopped being written Aug 27, 2025):**
- ❌ `codel_conversations` table - frozen, contains 6,274 interventions from Feb 24 - Aug 27, 2025
- ❌ `codel_conversation_recipients` table - related to old schema

**CURRENT (active since Aug 28, 2025):**
- ✅ `intervention` table - logs intervention decisions/triggers (has columns: id, source_message_id, type, status, created_at)
- ✅ `intervention_message` table - tracks actual messages sent to users (has columns: id, intervention_id, message_id, conversation_id, status, role, created_at, prompt_key)

**What this means for queries:**
- For interventions **after Aug 27, 2025**: Use `intervention` + `intervention_message` tables
- For interventions **before Aug 28, 2025**: Use `codel_conversations` table (historical data only)
- For queries **spanning the migration**: Need UNION of both schemas
- When investigating "recent interventions", ALWAYS query `intervention_message`, NOT `codel_conversations`
- The `intervention_message` table links to the `message` table via `message_id` to get actual message content

**PERSON FACTS MIGRATION (Aug 28, 2025):**

**DEPRECATED (stopped being written Aug 28, 2025):**
- ❌ `person_facts` table (plural) - frozen, contains 3,007 facts from Jul 2 - Aug 28, 2025

**CURRENT (active since Aug 28, 2025):**
- ✅ `person_fact` table (singular) - currently active, contains 7,440+ facts from Jul 2 onwards

**What this means for queries:**
- For facts **after Aug 28, 2025**: Use `person_fact` (singular)
- For facts **before Aug 28, 2025**: Use `person_facts` (plural) for historical data
- Both tables have identical schemas, but `person_fact` is more space-efficient
- The singular form is the current active table

**After running these 6 commands, you should be able to answer:**
- What tables exist and their sizes? (Command 1)
- Which tables relate to which? (Command 2 - look for person_id, message_id, etc.)
- What columns does each core table have? (Command 3 - persons, conversation_participant, message, intervention, intervention_message)
- What enums/types are used? (Command 4)
- What SQLAlchemy models exist? (Command 5)
- How do interventions work? (Command 6 - intervention conditions and timing)

**Example questions you can now answer:**
- "What is sam odio's user id?" → Query persons table, join conversation_participant to find relationships (Command 3)
- "Who got the last intervention?" → Query intervention_message + join to message table with created_at timestamp (Command 3)
- "What message triggered it?" → Join intervention.source_message_id to message.id (Commands 2 & 3)
- "How many interventions yesterday?" → Count from intervention table with created_at filter (Command 3)
- "What intervention types have been sent?" → Query intervention.type for distinct values (Commands 3 & 6)
- "Show me recent timeout interventions" → Query intervention WHERE type = 'timeout_intervention_escalation' and join intervention_message (Command 3)

## Prerequisites

This skill requires:
1. **psql** (PostgreSQL client) installed
   - Ubuntu/Debian: `sudo apt-get install postgresql-client`
   - macOS: `brew install postgresql`
2. Database credentials configured in `arsenal/.env`

The credentials should be set in `arsenal/.env`:
```bash
PGHOST=your-database-host.rds.amazonaws.com
PGPORT=5432
PGDATABASE=your_database_name
PGUSER=readonly_user
PGPASSWORD=your_readonly_password
PGSSLMODE=require
```

## Primary Workflow

### Use the Helper Script (Recommended)

The easiest way to query the database:

```bash
# Interactive psql session
arsenal/dot-claude/skills/sql-reader/connect.sh

# Run a single query
arsenal/dot-claude/skills/sql-reader/connect.sh "SELECT COUNT(*) FROM users;"

# Complex query with formatting
arsenal/dot-claude/skills/sql-reader/connect.sh "
SELECT
  table_name,
  pg_size_pretty(pg_total_relation_size('public.' || table_name)) as size
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY pg_total_relation_size('public.' || table_name) DESC
LIMIT 10;
"
```

### Load Environment Variables Manually

If you prefer to work directly with psql:

```bash
# Load credentials from arsenal/.env
set -a
source arsenal/.env
set +a

# Now use psql directly
psql
```

## Common Queries

### List all tables
```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

### Get table sizes
```sql
SELECT
    table_name,
    pg_size_pretty(pg_total_relation_size('public.' || table_name)) as size,
    pg_size_pretty(pg_relation_size('public.' || table_name)) as table_size,
    pg_size_pretty(pg_total_relation_size('public.' || table_name) - pg_relation_size('public.' || table_name)) as index_size
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY pg_total_relation_size('public.' || table_name) DESC
LIMIT 20;
```

### Describe a table
```sql
-- Using psql command
\d table_name

-- Or using information_schema
SELECT
    column_name,
    data_type,
    character_maximum_length,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'your_table'
ORDER BY ordinal_position;
```

### Count records
```sql
SELECT COUNT(*) FROM your_table;

-- Count by group
SELECT status, COUNT(*) as count
FROM your_table
GROUP BY status
ORDER BY count DESC;
```

### View recent records
```sql
SELECT *
FROM your_table
ORDER BY created_at DESC
LIMIT 10;
```

### Find table relationships
```sql
-- Find columns that look like foreign keys
SELECT DISTINCT
    table_name,
    column_name
FROM information_schema.columns
WHERE column_name LIKE '%_id'
  AND table_schema = 'public'
ORDER BY table_name, column_name;
```

## Relationship Coaching Schema Patterns

Common patterns when working with relationship coaching data:

### Find a Couple by Names

**Problem:** Multiple people can have the same name (e.g., multiple "Daniel" or "Camily" users).

**Solution:** Join through `conversation_participant` to find couples, rank by message count:

```sql
-- Find a couple by names (handles duplicate names)
SELECT
  c.id AS conversation_id,
  p1.id AS person1_id, p1.name AS person1_name,
  p2.id AS person2_id, p2.name AS person2_name,
  COUNT(DISTINCT m.id) AS message_count
FROM conversation c
JOIN conversation_participant cp1 ON cp1.conversation_id = c.id
JOIN persons p1 ON cp1.person_id = p1.id
JOIN conversation_participant cp2 ON cp2.conversation_id = c.id
JOIN persons p2 ON cp2.person_id = p2.id
LEFT JOIN message m ON m.conversation_id = c.id
WHERE c.type = 'GROUP'
  AND cp1.role = 'MEMBER' AND cp2.role = 'MEMBER'
  AND cp1.person_id < cp2.person_id
  AND (LOWER(p1.name) LIKE '%daniel%' AND LOWER(p2.name) LIKE '%camily%')
GROUP BY c.id, p1.id, p1.name, p2.id, p2.name
ORDER BY message_count DESC;
```

### Join Messages to People

**Schema gotcha:** Messages link to `person_contacts`, not directly to `persons`.

```sql
-- Get messages with sender names
SELECT
  m.id,
  m.content,  -- NOTE: Use 'content' not 'body'
  m.provider_timestamp,
  p.name AS sender_name,
  p.id AS sender_person_id
FROM message m
JOIN person_contacts pc ON m.sender_person_contact_id = pc.id
JOIN persons p ON pc.person_id = p.id
WHERE m.conversation_id = {{conversation_id}}
ORDER BY m.provider_timestamp DESC
LIMIT 10;
```

### Get User Reactions

**CRITICAL Schema Gotcha:** Reactions are stored as SEPARATE message records, NOT as arrays on the original message!

Each reaction creates a new message with:
- `provider_data->>'reaction_id'` set to a unique ID
- `content` starting with the reaction type: "Liked", "Loved", "Disliked", "Laughed at", "Emphasized", "Questioned"

```sql
-- Find reactions with message type (intervention, cron, direct response)
-- This query identifies what type of coach message was reacted to
WITH reaction_messages AS (
  SELECT
    m.id as reaction_id,
    m.conversation_id,
    CASE
      WHEN m.content LIKE 'Liked %' THEN 'Liked'
      WHEN m.content LIKE 'Loved %' THEN 'Loved'
      WHEN m.content LIKE 'Disliked %' THEN 'Disliked'
      WHEN m.content LIKE 'Laughed at %' THEN 'Laughed at'
      WHEN m.content LIKE 'Emphasized %' THEN 'Emphasized'
      WHEN m.content LIKE 'Questioned %' THEN 'Questioned'
    END as reaction_type,
    TRIM(BOTH '"' FROM SUBSTRING(m.content FROM POSITION('"' IN m.content))) as quoted_content,
    p.name as sender_name,
    m.created_at
  FROM message m
  JOIN conversation c ON m.conversation_id = c.id
  JOIN person_contacts pc ON m.sender_person_contact_id = pc.id
  JOIN persons p ON pc.person_id = p.id
  WHERE m.provider_data->>'reaction_id' IS NOT NULL
    AND c.type = 'ONE_ON_ONE'
    AND m.created_at >= NOW() - INTERVAL '96 hours'  -- Adjust timeframe as needed
),
original_messages AS (
  SELECT DISTINCT ON (rm.reaction_id)
    rm.reaction_id,
    orig.id as orig_message_id,
    orig.content as orig_content
  FROM reaction_messages rm
  JOIN message orig ON orig.conversation_id = rm.conversation_id
    AND rm.quoted_content LIKE '%' || LEFT(orig.content, 50) || '%'
    AND orig.id <> rm.reaction_id
  ORDER BY rm.reaction_id, orig.created_at DESC
)
SELECT
  rm.reaction_id,
  rm.reaction_type,
  rm.sender_name,
  CASE
    WHEN im.prompt_key IS NOT NULL THEN im.prompt_key
    WHEN om.orig_content LIKE 'Here''s a thought%' THEN 'scheduled_cron'
    WHEN om.orig_content LIKE 'Here''s a curious%' THEN 'scheduled_cron'
    WHEN om.orig_content LIKE 'Hey %' AND om.orig_content LIKE '%react%' THEN 'feedback_request'
    ELSE 'direct_response'
  END as message_type,
  LEFT(om.orig_content, 60) as content_preview,
  rm.created_at
FROM reaction_messages rm
LEFT JOIN original_messages om ON om.reaction_id = rm.reaction_id
LEFT JOIN intervention_message im ON im.message_id = om.orig_message_id
ORDER BY rm.created_at DESC;
```

**Message type values:**
- `group_msg_*` - Intervention triggered by partner's message (e.g., `group_msg_needs_affirmation`, `group_msg_intervention_needed_recipient`)
- `scheduled_cron` - Daily scheduled check-in ("Here's a thought/curious question...")
- `feedback_request` - Message asking user to react for feedback
- `direct_response` - Direct coach response to user's message
- `oh-by-the-way` - Scheduled reminder about upcoming events

```sql
-- Simple reaction count by type
SELECT
  CASE
    WHEN m.content LIKE 'Liked %' THEN '👍 Liked'
    WHEN m.content LIKE 'Loved %' THEN '❤️ Loved'
    WHEN m.content LIKE 'Disliked %' THEN '👎 Disliked'
    WHEN m.content LIKE 'Laughed at %' THEN '😂 Laughed at'
  END as reaction_type,
  COUNT(*) as count
FROM message m
JOIN conversation c ON m.conversation_id = c.id
WHERE m.provider_data->>'reaction_id' IS NOT NULL
  AND c.type = 'ONE_ON_ONE'
GROUP BY reaction_type
ORDER BY count DESC;
```

### Get Message Enrichment Data

The `message_enrichment` table contains AI classifications:

```sql
-- View messages with affect and conflict classifications
SELECT
  m.id,
  m.provider_timestamp,
  p.name AS sender,
  m.content,
  me.affect,           -- Partner-Affection, Partner-Contempt, etc.
  me.conflict_state,   -- 'New Conflict', 'Escalation', 'No conflict', etc.
  me.subject,          -- 'Partner', 'Self', 'Other'
  me.topic             -- 'Housework criticism', 'Planning', etc.
FROM message m
JOIN person_contacts pc ON m.sender_person_contact_id = pc.id
JOIN persons p ON pc.person_id = p.id
LEFT JOIN message_enrichment me ON me.message_id = m.id
WHERE m.conversation_id = {{conversation_id}}
  AND m.provider_timestamp >= CURRENT_DATE - INTERVAL '56 days'
ORDER BY m.provider_timestamp;
```

### Schema Gotchas to Remember

1. **Message content column:** Use `message.content`, not `message.body` (doesn't exist)
2. **Person lookup:** Multiple people can have identical names - always join through `conversation_participant` to identify couples
3. **Message→Person join:** Goes through `person_contacts` table: `message.sender_person_contact_id → person_contacts.id → person_contacts.person_id → persons.id`
4. **Couples:** `conversation.type = 'GROUP'` and `conversation_participant.role = 'MEMBER'` (should have exactly 2 members)
5. **Message enrichment:** Not all messages have enrichment data - use LEFT JOIN
6. **Reactions:** Stored as SEPARATE message records (not arrays). Look for messages where `provider_data->>'reaction_id' IS NOT NULL`. Content starts with "Liked", "Loved", "Disliked", "Laughed at", etc.

### Get database overview
```sql
-- Table count and total size
SELECT
    COUNT(*) as table_count,
    pg_size_pretty(SUM(pg_total_relation_size('public.' || table_name))) as total_size
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE';
```

## Safety Notes

⚠️ **READ-ONLY ACCESS**: These credentials have SELECT-only permissions. You cannot:
- INSERT, UPDATE, or DELETE data
- CREATE or DROP tables
- Modify schemas or permissions

✅ **Safe to use**: This skill is safe for production investigation because:
- Uses dedicated read-only credentials
- Cannot modify data
- Queries are logged in database audit logs
- Connection requires SSL/TLS

## psql Quick Reference

When in interactive mode:

```sql
\dt              -- List all tables
\d table_name    -- Describe a table
\di              -- List indexes
\df              -- List functions
\dv              -- List views
\du              -- List users/roles
\l               -- List databases
\c database      -- Connect to different database
\q               -- Quit
\?               -- Help
\h SQL_COMMAND   -- Help on SQL command
```

## Troubleshooting

### "command not found: psql"
Install PostgreSQL client:
```bash
# macOS
brew install postgresql

# Ubuntu/Debian
sudo apt-get install postgresql-client

# Amazon Linux
sudo yum install postgresql
```

### Connection timeout
- Verify you're on a network that can reach the database (VPN may be required)
- Check security groups allow your IP address
- Verify database instance is running

### "FATAL: password authentication failed"
- Verify credentials in `arsenal/.env` are correct
- Password may have been rotated in secrets manager
- Check that PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD are all set

### "arsenal/.env not found"
- Ensure you're running the script from the project root
- Verify the file exists: `ls -la arsenal/.env`
- If missing, copy credentials from secrets manager

## Integration with Claude Code

When using this skill in Claude Code:

1. **Announce usage**: "I'm using the sql-reader skill to investigate..."
2. **Run Data Model Quickstart FIRST**: Always start by running the 6 quickstart commands to understand the data structure
3. **Run targeted queries**: Use the helper script for specific investigations
4. **Report findings**: Share relevant results with the user

**Mandatory Workflow (ALWAYS start with this):**
```bash
# Step 1: See all tables with sizes
# Step 2: See foreign key columns (relationships)
# Step 3: Describe key table structures
# Step 4: Read enums: cat api/src/data/models/enums.py
# Step 5: See all models: grep "^class.*Base" api/src/data -r --include="*.py" | grep -v test
# Step 6: View intervention logic (group_message_intervention_conditions_dsl)

# Then investigate specific issues
arsenal/dot-claude/skills/sql-reader/connect.sh "SELECT COUNT(*) FROM message WHERE created_at > NOW() - INTERVAL '24 hours';"
```

**Best practices:**
- Always announce you're using the sql-reader skill
- Be specific about what you're investigating
- Use read-only queries (SELECT only)
- Format results clearly for the user
- Include relevant context (table names, counts, time ranges)

## Examples

### Investigate recent activity
```bash
arsenal/dot-claude/skills/sql-reader/connect.sh "
SELECT
    DATE(created_at) as date,
    COUNT(*) as message_count
FROM messages
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;
"
```

### Find table dependencies
```bash
arsenal/dot-claude/skills/sql-reader/connect.sh "
SELECT
    tc.table_name as from_table,
    kcu.column_name as from_column,
    ccu.table_name AS to_table,
    ccu.column_name AS to_column
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = 'public'
ORDER BY tc.table_name;
"
```

### Analyze data distribution
```bash
arsenal/dot-claude/skills/sql-reader/connect.sh "
SELECT
    table_name,
    (SELECT COUNT(*) FROM information_schema.columns c
     WHERE c.table_name = t.table_name) as column_count,
    pg_size_pretty(pg_total_relation_size('public.' || table_name)) as size
FROM information_schema.tables t
WHERE table_schema = 'public'
ORDER BY pg_total_relation_size('public.' || table_name) DESC
LIMIT 15;
"
```

---

## 🔐 Before Responding With Query Results

**You queried production data. Now before you respond to the user:**

1. ✅ Did you show actual query output (not "approximately" or "based on schema")?
2. ✅ Did you read DATA_QUIRKS.md first?
3. ✅ Are your numbers exact from the query, not estimates?
4. ✅ **Did you include citations for ALL entity IDs?** (persons, conversations, messages)

**CRITICAL: Get manager approval before responding.**

Your response with data MUST include: `✅ approve_7f3d8a2e********`

Get the full approval token from `.claude/skills/manager-review/SKILL.md`

**Common Mistake #4 in the manager's table is "Guessed at production data" - using words like "approximately" or "based on schema" instead of actual query results. The manager WILL catch this.**

**Common Mistake #10 is "Missing citations for entity IDs" - if your query returns person_id, conversation_id, or message_id, you MUST include clickable links:**

```
Person Samuel ([view](https://admin.prod.cncorp.io/persons/1)) has 3 conversations.
Conversation 456 ([view](https://admin.prod.cncorp.io/conversations/456)) started yesterday.
```

**Citation URL patterns:**
- Person: `https://admin.prod.cncorp.io/persons/{id}`
- Conversation: `https://admin.prod.cncorp.io/conversations/{id}`
- Messages: `https://admin.prod.cncorp.io/conversations/{id}/messages`
- Specific message: `...messages?messageId={id}`
- Time range: `...messages?start={iso}&end={iso}`
