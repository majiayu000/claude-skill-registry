---
name: goose-introspection
description: Goose session introspection and self-discovery via DuckDB reafference database. Query past sessions, find self, and enable cross-session awareness.
version: 1.0.0
trit: 0
---

# Skill: Goose Introspection

**Category**: Agent Self-Discovery | Session Analysis | Reafference Testing
**Level**: Core (Required for agent self-awareness)
**Status**: OPERATIONAL
**Trit Assignment**: 0 (ERGODIC) - Coordinates between past and future sessions
**Propagates To**: goose, amp, claude, cursor

---

## Overview

Implements **reafference-based self-discovery** for goose sessions. This skill enables any goose instance to:

1. **Find itself** in the session history
2. **Query past sessions** for context and continuity
3. **Track session evolution** across providers and models
4. **Enable cross-session awareness** through DuckDB persistence

**Core Principle**:
> An agent that cannot find itself in its own history cannot truly understand its context.

---

## Database Location

The reafference database is created at:


This database copies data from the goose sessions database at:


---

## Key Tables

### reafference_sessions
Tracks all sessions with discovery metadata:

| Column | Type | Description |
|--------|------|-------------|
| session_id | VARCHAR | Primary key, e.g., 20260108_22 |
| discovered_at | TIMESTAMP | When session was added to tracking |
| provider | VARCHAR | anthropic, openai, google, openrouter |
| model | VARCHAR | e.g., claude-opus-4-5-20251101 |
| working_dir | VARCHAR | Working directory of session |
| session_name | VARCHAR | Auto-generated or user-set name |
| original_created_at | TIMESTAMP | When session was first created |
| message_count | BIGINT | Number of messages in session |
| total_tokens | BIGINT | Total tokens used |
| is_origin_session | BOOLEAN | TRUE for the session that created this DB |
| notes | VARCHAR | Optional notes about the session |

### reafference_metadata
Key-value store for origin information.

### sessions (copied from source)
Full session data for offline queries.

### messages (copied from source)
Full message history for content analysis.

---

## Key Views

### reafference_origin
Returns the session that created this database.

### sessions_by_date
Aggregated daily statistics.

### searchable_sessions
Join of sessions with user messages for content search.

---

## Self-Discovery Queries

### Find This Session (Origin)


### Session Timeline


### Provider Distribution


---

## GF(3) Conservation

This skill participates in the triadic balance:

| Trit | Skill | Role |
|------|-------|------|
| -1 | duckdb-timetravel | Validates queries and schema |
| 0 | goose-introspection | Coordinates session discovery |
| +1 | reafference-corollary-discharge | Generates predictions |

**Conservation**: (-1) + (0) + (+1) = 0

---

## Status

- **Database Created**: Yes
- **Origin Session Marked**: 20260108_22
- **Sessions Tracked**: 376
- **Messages Indexed**: 6,215
- **Total Tokens**: ~3.59M

---

## Related Skills

- duckdb-timetravel - Temporal queries on session data
- duckdb-ies - Interaction entropy analysis
- reafference-corollary-discharge - Prediction/observation matching
- fswatch-duckdb - Real-time file monitoring with DuckDB

---

## Cat# Integration

This skill maps to Cat# = Comod(P) as a bicomodule:




## Forward Reference

- unified-reafference (canonical B3 Poset)