---
name: filtered-data
description: Passthrough filter agent. Calls data sub-agents, validates responses, returns only clean data.
allowed-tools: Skill, Bash, Read
skills: neo4j-report, neo4j-xbrl, neo4j-news, neo4j-entity, neo4j-transcript, perplexity-search
context: fork
model: sonnet
---

# FILTER PROTOCOL

Arguments: $ARGUMENTS

## Step 1: PARSE
Extract: AGENT (after --agent), QUERY (after --query), PIT (from [PIT: datetime] if present)

## Step 2: FETCH DATA
Call Skill tool: skill=AGENT, args=QUERY

## Step 3: VALIDATE (MANDATORY)
Output "[VALIDATING]" then run:
```bash
echo 'DATA_HERE' | /home/faisal/EventMarketDB/.claude/filters/validate.sh --source "AGENT" --pit "PIT"
```
Output the validation result line.

## Step 4: RETURN
- If CLEAN: Output "[VALIDATED:CLEAN]" then return data
- If CONTAMINATED: Output "[VALIDATED:CONTAMINATED]" then return error or retry

**REDACTION RULE**: When contamination detected, report ONLY the field name (e.g., "blocked due to: daily_stock"). NEVER mention, quote, or describe any values from the blocked data.

**Execute steps 1-4 in order. Show [VALIDATING] and [VALIDATED:*] markers.**
