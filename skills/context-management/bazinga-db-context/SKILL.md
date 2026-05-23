---
name: bazinga-db-context
description: Context packages and learning patterns. Use when managing context packages, error patterns, or strategies.
version: 2.0.0
allowed-tools: [Bash, Read]
---

# BAZINGA-DB Context Skill

You are the bazinga-db-context skill. You manage context packages for agent spawns and learning patterns (error patterns, strategies).

## When to Invoke This Skill

**Invoke when:**
- Saving or retrieving context packages
- Tracking context consumption
- Managing error patterns for learning
- Saving or querying strategies

**Do NOT invoke when:**
- Managing sessions or state → Use `bazinga-db-core`
- Managing task groups or plans → Use `bazinga-db-workflow`
- Logging interactions or reasoning → Use `bazinga-db-agents`

## Script Location

**Path:** `.claude/skills/bazinga-db/scripts/bazinga_db.py`

All commands use this script with `--quiet` flag:
```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet <command> [args...]
```

## Commands

### save-context-package

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet save-context-package \
  "<session_id>" "<group_id>" "<package_type>" "<source_file>" \
  "<producer_agent>" '<target_agents_json>' "<priority>" "<content>"
```

Save a context package for cross-agent knowledge sharing.

**Package types:** `research`, `failures`, `decisions`, `handoff`, `investigation`

**Priority:** `critical`, `high`, `medium`, `low`

**Example:**
```bash
python3 .../bazinga_db.py --quiet save-context-package \
  "bazinga_xxx" "AUTH" "research" "/tmp/auth-analysis.md" \
  "requirements_engineer" '["developer", "qa_expert"]' "high" \
  "Authentication requires OAuth2 with JWT tokens..."
```

### get-context-packages

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet get-context-packages \
  "<session_id>" "<group_id>" "<target_agent>" [--include-consumed]
```

Get context packages for an agent spawn.

**Returns:** Array of packages ordered by priority.

### mark-context-consumed

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet mark-context-consumed \
  "<package_id>" "<consumer_agent>"
```

Mark a context package as consumed by an agent.

### update-context-references

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet update-context-references \
  "<session_id>" "<group_id>" '<references_json>'
```

Update task group's context reference list.

### save-consumption

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet save-consumption \
  "<session_id>" "<agent_type>" "<resource_type>" "<resource_id>" [tokens]
```

Record context consumption for tracking.

### get-consumption

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet get-consumption \
  "<session_id>" [agent_type] [resource_type]
```

Get consumption records with optional filters.

## Learning Pattern Commands

### save-error-pattern

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet save-error-pattern \
  "<session_id>" "<group_id>" "<error_type>" "<error_signature>" \
  "<resolution>" [--confidence N]
```

Capture an error pattern for future learning.

**Error types:** `build`, `test`, `lint`, `type`, `runtime`, `security`

**Example:**
```bash
python3 .../bazinga_db.py --quiet save-error-pattern \
  "bazinga_xxx" "CALC" "test" "AssertionError: 2 != 3" \
  "Fixed off-by-one error in multiply function" --confidence 90
```

### get-error-patterns

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet get-error-patterns \
  [--error-type "<type>"] [--min-confidence N] [--limit N]
```

Query error patterns for similar issues.

### update-error-confidence

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet update-error-confidence \
  "<pattern_id>" <adjustment>
```

Adjust confidence (+/-) based on resolution success.

### cleanup-error-patterns

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet cleanup-error-patterns \
  [--max-age-days N] [--min-confidence N]
```

Remove expired or low-confidence patterns.

## Strategy Commands

### save-strategy

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet save-strategy \
  "<session_id>" "<group_id>" "<strategy_type>" "<description>" \
  "<outcome>" [--confidence N]
```

Save a successful strategy for future reference.

**Strategy types:** `debugging`, `testing`, `architecture`, `refactoring`, `security`

### get-strategies

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet get-strategies \
  [--strategy-type "<type>"] [--min-confidence N] [--limit N]
```

Query strategies by type and confidence.

### update-strategy-helpfulness

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet update-strategy-helpfulness \
  "<strategy_id>"
```

Increment helpfulness counter when strategy is reused.

### extract-strategies

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet extract-strategies \
  "<session_id>" [--min-confidence N]
```

Extract strategies from successful reasoning patterns.

## Output Format

Return ONLY raw JSON output. No formatting, markdown, or commentary.

## Error Handling

- Missing package: Returns `{"error": "Package not found: <id>"}`
- Invalid priority: Returns `{"error": "Invalid priority: <priority>"}`
- Invalid package type: Returns `{"error": "Invalid package type: <type>"}`

## References

- Full schema: `.claude/skills/bazinga-db/references/schema.md`
- All commands: `.claude/skills/bazinga-db/references/command_examples.md`
- CLI help: `python3 .../bazinga_db.py help`
