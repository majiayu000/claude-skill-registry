---
name: cm
description: "CASS Memory System - procedural memory for AI coding agents. Three-layer cognitive architecture with confidence decay, anti-pattern learning, cross-agent knowledge transfer, trauma guard safety system. Bun/TypeScript CLI."
---

# CM - CASS Memory System

Procedural memory for AI coding agents. Transforms scattered sessions into persistent, cross-agent memory. Uses a three-layer cognitive architecture that mirrors human expertise development.

## Why This Exists

AI coding agents accumulate valuable knowledge but it's:
- **Trapped in sessions** - Context lost when session ends
- **Agent-specific** - Claude doesn't know what Cursor learned
- **Unstructured** - Raw logs aren't actionable guidance
- **Subject to collapse** - Naive summarization loses critical details

You've solved auth bugs three times this month across different agents. Each time you started from scratch.

CM solves this with cross-agent learning: a pattern discovered in Cursor is immediately available to Claude Code.

---

## Three-Layer Cognitive Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    EPISODIC MEMORY (cass)                           │
│   Raw session logs from all agents — the "ground truth"             │
│   Claude Code │ Codex │ Cursor │ Aider │ PI │ Gemini │ ChatGPT │ ...│
└───────────────────────────┬─────────────────────────────────────────┘
                            │ cass search
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    WORKING MEMORY (Diary)                           │
│   Structured session summaries: accomplishments, decisions, etc.    │
└───────────────────────────┬─────────────────────────────────────────┘
                            │ reflect + curate (automated)
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    PROCEDURAL MEMORY (Playbook)                     │
│   Distilled rules with confidence tracking and decay                │
└─────────────────────────────────────────────────────────────────────┘
```

Every agent's sessions feed the shared memory. A pattern discovered in Cursor **automatically** helps Claude Code on the next session.

---

## The One Command You Need

```bash
cm context "<your task>" --json
```

**Run this before starting any non-trivial task.** Returns:
- **relevantBullets** - Rules from playbook scored by task relevance
- **antiPatterns** - Things that have caused problems
- **historySnippets** - Past sessions (yours and other agents')
- **suggestedCassQueries** - Deeper investigation searches

### Filtering History by Source

`historySnippets[].origin.kind` is `"local"` or `"remote"`. Remote hits include `origin.host`:

```json
{
  "historySnippets": [
    {
      "source_path": "~/.claude/sessions/session-001.jsonl",
      "origin": { "kind": "local" }
    },
    {
      "source_path": "/home/user/.codex/sessions/session.jsonl",
      "origin": { "kind": "remote", "host": "workstation" }
    }
  ]
}
```

---

## Confidence Decay System

Rules aren't immortal. Confidence decays without revalidation:

| Mechanism | Effect |
|-----------|--------|
| **90-day half-life** | Confidence halves every 90 days without feedback |
| **4x harmful multiplier** | One mistake counts 4× as much as one success |
| **Maturity progression** | `candidate` → `established` → `proven` |

### Score Decay Visualization

```
Initial score: 10.0 (10 helpful marks today)

After 90 days (half-life):   5.0
After 180 days:              2.5
After 270 days:              1.25
After 365 days:              0.78
```

### Effective Score Formula

```typescript
effectiveScore = decayedHelpful - (4 × decayedHarmful)

// Where decay factor = 0.5 ^ (daysSinceFeedback / 90)
```

### Maturity State Machine

```
  ┌──────────┐       ┌─────────────┐    ┌────────┐
  │ candidate│──────▶│ established │───▶│ proven │
  └──────────┘       └─────────────┘    └────────┘
       │                   │                  │
       │                   │ (harmful >25%)   │
       │                   ▼                  │
       │             ┌─────────────┐          │
       └────────────▶│ deprecated  │◀─────────┘
                     └─────────────┘
```

**Transition Rules:**

| Transition | Criteria |
|------------|----------|
| `candidate` → `established` | 3+ helpful, harmful ratio <25% |
| `established` → `proven` | 10+ helpful, harmful ratio <10% |
| `any` → `deprecated` | Harmful ratio >25% OR explicit deprecation |

---

## Anti-Pattern Learning

Bad rules don't just get deleted. They become warnings:

```
"Cache auth tokens for performance"
    ↓ (3 harmful marks)
"PITFALL: Don't cache auth tokens without expiry validation"
```

When a rule is marked harmful multiple times (>50% harmful ratio with 3+ marks), it's automatically inverted into an anti-pattern.

---

## ACE Pipeline (How Rules Are Created)

```
Generator → Reflector → Validator → Curator
```

| Stage | Role | LLM? |
|-------|------|------|
| **Generator** | Pre-task context hydration (`cm context`) | No |
| **Reflector** | Extract patterns from sessions (`cm reflect`) | Yes |
| **Validator** | Evidence gate against cass history | Yes |
| **Curator** | Deterministic delta merge | **No** |

**Critical:** Curator has NO LLM to prevent context collapse from iterative drift. LLMs propose patterns; deterministic logic manages them.

### Scientific Validation

Before a rule joins your playbook, it's validated against cass history:

```
Proposed rule: "Always check token expiry before auth debugging"
    ↓
Evidence gate: Search cass for sessions where this applied
    ↓
Result: 5 sessions found, 4 successful outcomes → ACCEPT
```

Rules without historical evidence are flagged as candidates until proven.

---

## Commands Reference

### Context Retrieval (Primary Workflow)

```bash
# THE MAIN COMMAND - run before non-trivial tasks
cm context "implement user authentication" --json

# Limit results for token budget
cm context "fix bug" --json --limit 5 --no-history

# With workspace filter
cm context "refactor" --json --workspace /path/to/project

# Self-documenting explanation
cm quickstart --json

# System health
cm doctor --json
cm doctor --fix  # Auto-fix issues

# Find similar rules
cm similar "error handling best practices"
```

### Playbook Management

```bash
cm playbook list                              # All rules
cm playbook get b-8f3a2c                      # Rule details
cm playbook add "Always run tests first"      # Add rule
cm playbook add --file rules.json             # Batch add from file
cm playbook add --file rules.json --session /path/session.jsonl  # Track source
cm playbook remove b-xyz --reason "Outdated"  # Remove
cm playbook export > backup.yaml              # Export
cm playbook import shared.yaml                # Import
cm playbook bootstrap react                   # Apply starter to existing

cm top 10                                     # Top effective rules
cm stale --days 60                            # Rules without recent feedback
cm why b-8f3a2c                               # Rule provenance
cm stats --json                               # Playbook health metrics
```

### Learning & Feedback

```bash
# Manual feedback
cm mark b-8f3a2c --helpful
cm mark b-xyz789 --harmful --reason "Caused regression"
cm undo b-xyz789                              # Revert feedback

# Session outcomes (positional: status, rules)
cm outcome success b-8f3a2c,b-def456
cm outcome failure b-x7k9p1 --summary "Auth approach failed"
cm outcome-apply                              # Apply to playbook

# Reflection (usually automated)
cm reflect --days 7 --json
cm reflect --session /path/to/session.jsonl   # Single session
cm reflect --workspace /path/to/project       # Project-specific

# Validation
cm validate "Always check null before dereferencing"

# Audit sessions against rules
cm audit --days 30

# Deprecate permanently
cm forget b-xyz789 --reason "Superseded by better pattern"
```

### Onboarding (Agent-Native)

Zero-cost playbook building using your existing agent:

```bash
cm onboard status                             # Check progress
cm onboard gaps                               # Category gaps
cm onboard sample --fill-gaps                 # Prioritized sessions
cm onboard sample --agent claude --days 14    # Filter by agent/time
cm onboard sample --workspace /path/project   # Filter by workspace
cm onboard sample --include-processed         # Re-analyze sessions
cm onboard read /path/session.jsonl --template  # Rich context
cm onboard mark-done /path/session.jsonl      # Mark processed
cm onboard reset                              # Start fresh
```

### Trauma Guard (Safety System)

```bash
cm trauma list                                # Active patterns
cm trauma add "DROP TABLE" --description "Mass deletion" --severity critical
cm trauma heal t-abc --reason "Intentional migration"
cm trauma remove t-abc
cm trauma scan --days 30                      # Scan for traumas
cm trauma import shared-traumas.yaml

cm guard --install                            # Claude Code hook
cm guard --git                                # Git pre-commit hook
cm guard --install --git                      # Both
cm guard --status                             # Check installation
```

### System Commands

```bash
cm init                                       # Initialize
cm init --starter typescript                  # With template
cm init --force                               # Reinitialize (creates backup)
cm starters                                   # List templates
cm serve --port 3001                          # MCP server
cm usage                                      # LLM cost stats
cm privacy status                             # Privacy settings
cm privacy enable                             # Enable cross-agent enrichment
cm privacy disable                            # Disable enrichment
cm project --format agents.md                 # Export for AGENTS.md
```

---

## Starter Playbooks

Starting with an empty playbook is daunting. Starters provide curated best practices:

```bash
cm starters                    # List available
cm init --starter typescript   # Initialize with starter
cm playbook bootstrap react    # Apply to existing playbook
```

### Built-in Starters

| Starter | Focus | Rules |
|---------|-------|-------|
| **general** | Universal best practices | 5 |
| **typescript** | TypeScript/Node.js patterns | 4 |
| **react** | React/Next.js development | 4 |
| **python** | Python/FastAPI/Django | 4 |
| **node** | Node.js/Express services | 4 |
| **rust** | Rust service patterns | 4 |

### Custom Starters

Create YAML files in `~/.cass-memory/starters/`:

```yaml
# ~/.cass-memory/starters/django.yaml
name: django
description: Django web framework best practices
bullets:
  - content: "Always use Django's ORM for database operations"
    category: database
    maturity: established
    tags: [django, orm]
```

---

## Inline Feedback (During Work)

Leave feedback in code comments. Parsed during reflection:

```typescript
// [cass: helpful b-8f3a2c] - this rule saved me from a rabbit hole

// [cass: harmful b-x7k9p1] - this advice was wrong for our use case
```

---

## Agent Protocol

```
1. START:    cm context "<task>" --json
2. WORK:     Reference rule IDs when following them (e.g., "Following b-8f3a2c...")
3. FEEDBACK: Leave inline comments when rules help/hurt
4. END:      Just finish. Learning happens automatically.
```

**You do NOT need to:**
- Run `cm reflect` (automation handles this)
- Run `cm mark` manually (use inline comments)
- Manually add rules to the playbook

---

## Gap Analysis Categories

| Category | Keywords |
|----------|----------|
| `debugging` | error, fix, bug, trace, stack |
| `testing` | test, mock, assert, expect, jest |
| `architecture` | design, pattern, module, abstraction |
| `workflow` | task, CI/CD, deployment |
| `documentation` | comment, README, API doc |
| `integration` | API, HTTP, JSON, endpoint |
| `collaboration` | review, PR, team |
| `git` | branch, merge, commit |
| `security` | auth, token, encrypt, permission |
| `performance` | optimize, cache, profile |

**Category Status Thresholds:**

| Status | Rule Count | Priority |
|--------|------------|----------|
| `critical` | 0 rules | High |
| `underrepresented` | 1-2 rules | Medium |
| `adequate` | 3-10 rules | Low |
| `well-covered` | 11+ rules | None |

---

## Trauma Guard: Safety System

The "hot stove" principle—learn from past incidents and prevent recurrence.

### How It Works

```
Session History              Trauma Registry              Runtime Guard
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│ rm -rf /* (oops)│ ──────▶ │ Pattern: rm -rf │ ──────▶ │ BLOCKED: This   │
│ "sorry, I made  │  scan   │ Severity: FATAL │  hook   │ command matches │
│  a mistake..."  │         │ Session: abc123 │         │ a trauma pattern│
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

### Built-in Doom Patterns (20+)

| Category | Examples |
|----------|----------|
| **Filesystem** | `rm -rf /`, `rm -rf ~`, recursive deletes |
| **Database** | `DROP DATABASE`, `TRUNCATE`, `DELETE FROM` without WHERE |
| **Git** | `git push --force` to main/master, `git reset --hard` |
| **Infrastructure** | `terraform destroy -auto-approve`, `kubectl delete namespace` |
| **Cloud** | `aws s3 rm --recursive`, destructive CloudFormation |

### Pattern Storage

| Scope | Location | Purpose |
|-------|----------|---------|
| **Global** | `~/.cass-memory/traumas.jsonl` | Personal patterns |
| **Project** | `.cass/traumas.jsonl` | Commit to repo for team |

### Pattern Lifecycle

- **Active**: Blocks matching commands
- **Healed**: Temporarily bypassed (with reason and timestamp)
- **Deleted**: Removed (can be re-added)

---

## MCP Server

Run as MCP server for agent integration:

```bash
# Local-only (recommended)
cm serve --port 3001

# With auth token (for non-loopback)
MCP_HTTP_TOKEN="<random>" cm serve --host 0.0.0.0 --port 3001
```

### Tools Exposed

| Tool | Purpose | Parameters |
|------|---------|------------|
| `cm_context` | Get rules + history | `task, limit?, history?, days?, workspace?` |
| `cm_feedback` | Record feedback | `bulletId, helpful?, harmful?, reason?` |
| `cm_outcome` | Record session outcome | `sessionId, outcome, rulesUsed?` |
| `memory_search` | Search playbook/cass | `query, scope?, limit?, days?` |
| `memory_reflect` | Trigger reflection | `days?, maxSessions?, dryRun?` |

### Resources Exposed

| URI | Purpose |
|-----|---------|
| `cm://playbook` | Current playbook state |
| `cm://diary` | Recent diary entries |
| `cm://outcomes` | Session outcomes |
| `cm://stats` | Playbook health metrics |

### Client Configuration

**Claude Code** (`~/.config/claude/mcp.json`):
```json
{
  "mcpServers": {
    "cm": {
      "command": "cm",
      "args": ["serve"]
    }
  }
}
```

---

## Graceful Degradation

| Condition | Behavior |
|-----------|----------|
| No cass | Playbook-only scoring, no history snippets |
| No playbook | Empty playbook, commands still work |
| No LLM | Deterministic reflection, no semantic enhancement |
| Offline | Cached playbook + local diary |

---

## Output Format

All commands support `--json` for machine-readable output.

**Design principle:** stdout = JSON only; diagnostics go to stderr.

### Success Response

```json
{
  "success": true,
  "task": "fix the auth timeout bug",
  "relevantBullets": [
    {
      "id": "b-8f3a2c",
      "content": "Always check token expiry before auth debugging",
      "effectiveScore": 8.5,
      "maturity": "proven",
      "relevanceScore": 0.92,
      "reasoning": "Extracted from 5 successful sessions"
    }
  ],
  "antiPatterns": [...],
  "historySnippets": [...],
  "suggestedCassQueries": [...],
  "degraded": null
}
```

### Error Response

```json
{
  "success": false,
  "code": "PLAYBOOK_NOT_FOUND",
  "error": "Playbook file not found",
  "hint": "Run 'cm init' to create a new playbook",
  "retryable": false,
  "recovery": ["cm init", "cm doctor --fix"],
  "docs": "README.md#-troubleshooting"
}
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 1 | Internal error |
| 2 | User input/usage |
| 3 | Configuration |
| 4 | Filesystem |
| 5 | Network |
| 6 | cass error |
| 7 | LLM/provider error |

---

## Token Budget Management

| Flag | Effect |
|------|--------|
| `--limit N` | Cap number of rules |
| `--min-score N` | Only rules above threshold |
| `--no-history` | Skip historical snippets (faster) |
| `--json` | Structured output |

---

## Configuration

Config lives at `~/.cass-memory/config.json` (global) and `.cass/config.json` (repo).

**Precedence:** CLI flags > Repo config > Global config > Defaults

**Security:** Repo config cannot override sensitive paths or user-level consent settings.

### Key Options

```json
{
  "provider": "anthropic",
  "model": "claude-sonnet-4-20250514",
  "budget": {
    "dailyLimit": 0.10,
    "monthlyLimit": 2.00
  },
  "scoring": {
    "decayHalfLifeDays": 90,
    "harmfulMultiplier": 4
  },
  "maxBulletsInContext": 50,
  "maxHistoryInContext": 10,
  "sessionLookbackDays": 7,
  "crossAgent": {
    "enabled": false,
    "consentGiven": false,
    "auditLog": true
  },
  "remoteCass": {
    "enabled": false,
    "hosts": [{"host": "workstation", "label": "work"}]
  },
  "semanticSearchEnabled": false,
  "embeddingModel": "Xenova/all-MiniLM-L6-v2",
  "dedupSimilarityThreshold": 0.85
}
```

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `ANTHROPIC_API_KEY` | API key for Anthropic (Claude) |
| `OPENAI_API_KEY` | API key for OpenAI |
| `GOOGLE_GENERATIVE_AI_API_KEY` | API key for Google Gemini |
| `CASS_PATH` | Path to cass binary |
| `CASS_MEMORY_LLM` | Set to `none` for LLM-free mode |
| `MCP_HTTP_TOKEN` | Auth token for non-loopback MCP server |

---

## Data Locations

```
~/.cass-memory/                  # Global (user-level)
├── config.json                  # Configuration
├── playbook.yaml                # Personal playbook
├── diary/                       # Session summaries
├── outcomes/                    # Session outcomes
├── traumas.jsonl                # Trauma patterns
├── starters/                    # Custom starter playbooks
├── onboarding-state.json        # Onboarding progress
├── privacy-audit.jsonl          # Cross-agent audit trail
├── processed-sessions.jsonl     # Reflection progress
└── usage.jsonl                  # LLM cost tracking

.cass/                           # Project-level (in repo)
├── config.json                  # Project-specific overrides
├── playbook.yaml                # Project-specific rules
├── traumas.jsonl                # Project-specific patterns
└── blocked.yaml                 # Anti-patterns to block
```

---

## Automating Reflection

### Cron Job

```bash
# Daily at 2am
0 2 * * * /usr/local/bin/cm reflect --days 7 >> ~/.cass-memory/reflect.log 2>&1
```

### Claude Code Hook

`.claude/hooks.json`:
```json
{
  "post-session": ["cm reflect --days 1"]
}
```

---

## Privacy & Security

### Local-First Design

- All data stays on your machine
- No cloud sync, no telemetry
- Cross-agent enrichment is opt-in with explicit consent
- Audit log for enrichment events

### Secret Sanitization

Before processing, content is sanitized:
- OpenAI/Anthropic/AWS/Google API keys
- GitHub tokens
- JWTs
- Passwords and secrets in config patterns

### Privacy Controls

```bash
cm privacy status    # Check settings
cm privacy enable    # Enable cross-agent enrichment
cm privacy disable   # Disable enrichment
```

---

## Performance Characteristics

| Operation | Typical Latency |
|-----------|-----------------|
| `cm context` (cached) | 50-150ms |
| `cm context` (cold) | 200-500ms |
| `cm context` (no cass) | 30-80ms |
| `cm reflect` (1 session) | 5-15s |
| `cm reflect` (5 sessions) | 20-60s |
| `cm playbook list` | <50ms |
| `cm similar` (keyword) | 20-50ms |
| `cm similar` (semantic) | 100-300ms |

### LLM Cost Estimates

| Operation | Typical Cost |
|-----------|--------------|
| Reflect (1 session) | $0.01-0.05 |
| Reflect (7 days) | $0.05-0.20 |
| Validate (1 rule) | $0.005-0.01 |

With default budget ($0.10/day, $2.00/month): ~5-10 sessions/day.

---

## Batch Rule Addition

After analyzing a session, add multiple rules at once:

```bash
# Create JSON file
cat > rules.json << 'EOF'
[
  {"content": "Always run tests before committing", "category": "testing"},
  {"content": "Check token expiry before auth debugging", "category": "debugging"},
  {"content": "AVOID: Mocking entire modules in tests", "category": "testing"}
]
EOF

# Add all rules
cm playbook add --file rules.json

# Track which session they came from
cm playbook add --file rules.json --session /path/to/session.jsonl

# Or pipe from stdin
echo '[{"content": "Rule", "category": "workflow"}]' | cm playbook add --file -
```

---

## Template Output for Onboarding

`--template` provides rich context for rule extraction:

```bash
cm onboard read /path/to/session.jsonl --template --json
```

Returns:
- **metadata**: path, workspace, message count, topic hints
- **context**: related rules, playbook gaps, suggested focus
- **extractionFormat**: schema, categories, examples
- **sessionContent**: actual session data

---

## Integration with CASS

CASS provides **episodic memory** (raw sessions).
CM extracts **procedural memory** (rules and playbooks).

```bash
# CASS: Search raw sessions
cass search "authentication timeout" --robot

# CM: Get distilled rules for a task
cm context "authentication timeout" --json
```

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `cass not found` | Install from [cass repo](https://github.com/Dicklesworthstone/coding_agent_session_search) |
| `cass search failed` | Run `cass index --full` |
| `API key missing` | Set `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, or `GOOGLE_GENERATIVE_AI_API_KEY` |
| `Playbook corrupt` | Run `cm doctor --fix` |
| `Budget exceeded` | Check `cm usage`, adjust limits |

### Diagnostic Commands

```bash
cm doctor --json           # System health
cm doctor --fix            # Auto-fix issues
cm usage                   # LLM budget status
cm stats --json            # Playbook health
cm why <bullet-id>         # Rule provenance
```

### LLM-Free Mode

```bash
CASS_MEMORY_LLM=none cm context "task" --json
```

---

## Installation

```bash
# One-liner (recommended)
curl -fsSL https://raw.githubusercontent.com/Dicklesworthstone/cass_memory_system/main/install.sh \
  | bash -s -- --easy-mode --verify

# Specific version
install.sh --version v0.2.2 --verify

# System-wide
install.sh --system --verify

# From source
git clone https://github.com/Dicklesworthstone/cass_memory_system.git
cd cass_memory_system
bun install && bun run build
sudo mv ./dist/cass-memory /usr/local/bin/cm
```

---

## Integration with Flywheel

| Tool | Integration |
|------|-------------|
| **CASS** | CM reads from cass episodic memory, writes procedural memory |
| **NTM** | Robot mode integrates with cm for context before agent work |
| **Agent Mail** | Rules can reference mail threads as provenance |
| **BV** | Task context enriched with relevant playbook rules |
