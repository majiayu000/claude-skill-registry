---
name: test-resume
description: Test subagent resumption - call agent twice, verify context preserved
allowed-tools: Read, Write, Task
permissionMode: dontAsk
---

# Test Subagent Resumption

**Goal**: Verify CSV-based subagent history and resumption works for all Neo4j agents.

**History file**: `.claude/skills/test-resume/subagent-history.csv`

**Subagents to test**: neo4j-entity, neo4j-report, neo4j-xbrl, neo4j-transcript, neo4j-news

## Test Steps

### Step 1: Initialize CSV
Create CSV with full header matching earnings-prediction/attribution:
```csv
accession_no,updated_at,primary_session_id,neo4j-entity,neo4j-report,neo4j-xbrl,neo4j-transcript,neo4j-news
```

Set `primary_session_id` to current session ID (this conversation's session).

### Step 2: Test neo4j-entity (Fresh + Resume)

**First call** (fresh):
> "Get sector for Apple (AAPL). Remember: secret word is BANANA."

Save agent ID to CSV column `neo4j-entity` for row `test-0001`.

**Second call** (resume):
> "What was the secret word? Also get sector for IBM."

Verify it remembers BANANA.

### Step 3: Test neo4j-report (Fresh + Resume)

**First call** (fresh):
> "How many 8-K reports exist for ticker AAPL? Remember: secret number is 42."

Save agent ID to CSV column `neo4j-report` for row `test-0001`.

**Second call** (resume):
> "What was the secret number? How many 10-K reports for AAPL?"

Verify it remembers 42.

### Step 4: Verify CSV Structure

Read and display CSV. Should have:
- 1 row for `test-0001`
- Both `neo4j-entity` and `neo4j-report` columns populated
- Other columns empty

### Step 5: Test Cell Overwrite

Call `neo4j-entity` again WITHOUT resume (fresh session):
> "Get sector for GOOGL. New secret: CHERRY."

Update CSV - overwrite `neo4j-entity` column with new agent ID.
Verify `neo4j-report` column is UNCHANGED.

### Step 6: Final Report

| Test | Agent | Result |
|------|-------|--------|
| Fresh call | neo4j-entity | |
| Resume + memory | neo4j-entity | |
| Fresh call | neo4j-report | |
| Resume + memory | neo4j-report | |
| Cell overwrite preserves others | | |

**Show final CSV contents.**

## Success Criteria
- All agents can be called and return agent IDs
- Resume preserves context (remembers secrets)
- CSV correctly tracks all agent IDs per accession
- Overwriting one cell doesn't affect others
