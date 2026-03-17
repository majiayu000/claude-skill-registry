---
name: cm
description: "CASS Memory System - procedural memory for AI coding agents. Three-layer cognitive architecture transforms scattered sessions into persistent, cross-agent learnings with confidence decay, anti-pattern learning, and scientific validation."
---

# CM - CASS Memory System

Procedural memory for AI coding agents. Transforms scattered agent sessions into persistent, cross-agent memory so every agent learns from every other agent's experience.

---

## Critical Concepts for AI Agents

### The Three-Layer Cognitive Architecture

| Layer | Role | Storage | Tool |
|-------|------|---------|------|
| **Episodic Memory** | Raw session transcripts | `~/.local/share/cass/` | `cass` |
| **Working Memory** | Session summaries | Diary entries | `cm reflect` |
| **Procedural Memory** | Distilled action rules | Playbook | `cm` |

**Flow**: Sessions → Diary summaries → Playbook rules

### Why This Matters

Without cm, each agent session starts from zero. With cm:
- Rules that helped in past sessions get reinforced
- Anti-patterns that caused failures become explicit warnings
- Cross-agent learning means Agent B benefits from Agent A's mistakes
- Confidence decay naturally retires stale guidance

---

## Quick Reference for AI Agents

### Start of Session

```bash
# Get relevant rules and history for your task
cm context "implementing OAuth authentication" --json

# Output includes:
# - Relevant playbook rules with scores
# - Related diary entries
# - Gap analysis (uncovered areas)
```

### During Work

```bash
# Find rules about a topic
cm similar "error handling" --json

# Check if a pattern is validated
cm validate "Always use prepared statements for SQL"
```

### End of Session

```bash
# Record which rules helped
cm outcome success "RULE-123,RULE-456"

# Record which rules caused problems
cm outcome failure "RULE-789"

# Apply recorded outcomes
cm outcome-apply
```

### Periodic Maintenance

```bash
# Extract new rules from recent sessions
cm reflect

# Find stale rules needing re-validation
cm stale --days 30

# System health
cm doctor
```

---

## The ACE Pipeline

CM uses a four-stage pipeline to extract and curate rules:

```
Sessions → Generator → Reflector → Validator → Curator → Playbook
              ↓            ↓            ↓           ↓
           Diary      Candidates    Evidence    Final Rules
          Entries       (LLM)        (LLM)      (NO LLM!)
```

### Stage Details

| Stage | Uses LLM | Purpose |
|-------|----------|---------|
| **Generator** | Yes | Summarize sessions into diary entries |
| **Reflector** | Yes | Propose candidate rules from patterns |
| **Validator** | Yes | Check rules against historical evidence |
| **Curator** | **NO** | Deterministic merge into playbook |

**CRITICAL**: The Curator is intentionally LLM-free to prevent hallucinated provenance. All rule additions must trace to actual session evidence.

---

## Confidence & Decay System

### The Scoring Algorithm

Every rule has a confidence score that decays over time:

```
score = base_confidence × decay_factor × feedback_modifier
```

Where:
- `base_confidence`: Initial confidence (0.0-1.0)
- `decay_factor`: `0.5^(days_since_feedback / 90)` (90-day half-life)
- `feedback_modifier`: Accumulated helpful/harmful signals

### Decay Visualization

```
Day 0:   ████████████████████ 1.00
Day 45:  ██████████████       0.71
Day 90:  ██████████           0.50  ← Half-life
Day 180: █████                0.25
Day 270: ██                   0.125
```

### Feedback Multipliers

| Feedback | Multiplier | Effect |
|----------|------------|--------|
| Helpful | 1.0x | Standard positive reinforcement |
| Harmful | **4.0x** | Aggressive penalty (asymmetric by design) |

**Why asymmetric?** Bad advice is more damaging than good advice is helpful. A harmful rule should decay 4x faster than a helpful one recovers.

### Anti-Pattern Learning

When a rule accumulates too much harmful feedback, it doesn't just disappear—it **inverts**:

```
Original:  "Always use global state for configuration"
           ↓ (harmful feedback accumulates)
Inverted:  "⚠️ ANTI-PATTERN: Avoid global state for configuration"
```

The inverted anti-pattern becomes a warning that prevents future agents from making the same mistake.

---

## Command Reference

### `cm context` — Get Task-Relevant Memory

The primary command for starting any task.

```bash
# Basic context retrieval
cm context "implementing user authentication"

# JSON output for programmatic use
cm context "database migration" --json

# Deeper historical context
cm context "API refactoring" --depth deep

# Include gap analysis
cm context "payment processing" --gaps
```

**Output includes:**
- Top relevant playbook rules (ranked by score × relevance)
- Related diary entries from past sessions
- Gap analysis (categories with thin coverage)
- Suggested starter rules for uncovered areas

### `cm top` — Highest-Scoring Rules

```bash
# Top 10 rules by confidence score
cm top 10

# JSON output
cm top 20 --json

# Filter by category
cm top 10 --category testing
```

### `cm similar` — Find Related Rules

```bash
# Semantic search over playbook
cm similar "error handling patterns"

# With scores
cm similar "authentication flow" --scores

# JSON output
cm similar "database queries" --json
```

### `cm playbook` — Manage the Playbook

```bash
# List all rules
cm playbook list

# Statistics
cm playbook stats

# Export for documentation
cm playbook export --format md > PLAYBOOK.md
cm playbook export --format json > playbook.json

# Import rules
cm playbook import rules.json
```

### `cm why` — Rule Provenance

```bash
# Show evidence chain for a rule
cm why RULE-123

# Output shows:
# - Original session(s) that generated the rule
# - Diary entries that led to extraction
# - Feedback history
# - Confidence trajectory
```

### `cm mark` — Provide Feedback

```bash
# Mark as helpful (reinforces rule)
cm mark RULE-123 --helpful

# Mark as harmful (penalizes rule, may trigger inversion)
cm mark RULE-123 --harmful

# With context
cm mark RULE-123 --helpful --reason "Prevented auth vulnerability"

# Undo feedback
cm undo RULE-123
```

### `cm reflect` — Extract Rules from Sessions

```bash
# Process recent sessions
cm reflect

# Specific time range
cm reflect --since "7d"
cm reflect --since "2024-01-01"

# Dry run (show what would be extracted)
cm reflect --dry-run

# Force re-processing of already-reflected sessions
cm reflect --force
```

### `cm audit` — Check Sessions Against Rules

```bash
# Audit recent sessions for rule violations
cm audit

# Specific time range
cm audit --since "24h"

# JSON output
cm audit --json
```

### `cm validate` — Test a Proposed Rule

```bash
# Check if a rule has historical support
cm validate "Always use transactions for multi-table updates"

# Output shows:
# - Supporting evidence (sessions where this helped)
# - Contradicting evidence (sessions where this hurt)
# - Recommendation (add/skip/needs-more-data)
```

### `cm outcome` — Record Session Results

```bash
# Record which rules helped
cm outcome success "RULE-123,RULE-456,RULE-789"

# Record which rules hurt
cm outcome failure "RULE-999"

# Apply all pending outcomes
cm outcome-apply

# Clear pending outcomes without applying
cm outcome-clear
```

### `cm stale` — Find Stale Rules

```bash
# Find rules without recent feedback
cm stale

# Custom threshold
cm stale --days 60

# JSON output
cm stale --json

# Include decay projection
cm stale --project
```

### `cm forget` — Deprecate Rules

```bash
# Soft-delete a rule
cm forget RULE-123

# With reason
cm forget RULE-123 --reason "No longer relevant after framework change"

# Force (skip confirmation)
cm forget RULE-123 --force
```

### `cm doctor` — System Health

```bash
# Run diagnostics
cm doctor

# Auto-fix issues
cm doctor --fix

# JSON output
cm doctor --json
```

**Checks:**
- cass installation and accessibility
- Playbook integrity
- Diary consistency
- Configuration validity
- Session index freshness

### `cm usage` — Usage Statistics

```bash
# Show usage stats
cm usage

# JSON output
cm usage --json
```

### `cm stats` — Playbook Health Metrics

```bash
# Show playbook health
cm stats

# Output includes:
# - Total rules
# - Average confidence
# - Category distribution
# - Stale rule count
# - Anti-pattern count
```

---

## Agent-Native Onboarding

CM includes a guided onboarding system that requires **zero API calls**:

```bash
cm onboard
```

The onboarding wizard:
1. Explains the three-layer architecture
2. Walks through basic commands
3. Seeds initial rules from session history
4. Sets up appropriate starter playbook
5. Configures privacy preferences

**No LLM required** — onboarding works offline.

---

## Starter Playbooks

Pre-built playbooks for common tech stacks:

```bash
# List available starters
cm starters

# Initialize with a starter
cm init --starter typescript
cm init --starter python
cm init --starter go
cm init --starter rust
```

Available starters:
- `typescript` - TS/JS patterns, npm, testing
- `python` - Python idioms, pip, pytest
- `go` - Go conventions, modules, testing
- `rust` - Rust patterns, cargo, clippy
- `general` - Language-agnostic best practices

---

## Gap Analysis

CM tracks which categories have thin coverage:

```bash
cm context "some task" --gaps
```

Gap analysis shows:
- Categories with few rules
- Categories with low-confidence rules
- Suggested areas for rule extraction

This helps agents identify blind spots in the collective memory.

---

## Batch Rule Addition

For bulk importing rules:

```bash
# From JSON
cm playbook import rules.json

# From markdown
cm playbook import rules.md

# With validation
cm playbook import rules.json --validate
```

JSON format:
```json
[
  {
    "content": "Always validate user input at API boundaries",
    "category": "security",
    "confidence": 0.8,
    "source": "manual"
  }
]
```

---

## Data Models

### PlaybookBullet

```json
{
  "id": "RULE-abc123",
  "content": "Use parameterized queries for all database access",
  "category": "security",
  "confidence": 0.85,
  "created_at": "2024-01-15T10:30:00Z",
  "last_feedback": "2024-03-20T14:22:00Z",
  "helpful_count": 12,
  "harmful_count": 1,
  "source_sessions": ["session-xyz", "session-abc"],
  "is_anti_pattern": false,
  "maturity": "validated"
}
```

### FeedbackEvent

```json
{
  "rule_id": "RULE-abc123",
  "type": "helpful",
  "reason": "Prevented SQL injection in auth flow",
  "session_id": "session-current",
  "timestamp": "2024-03-20T14:22:00Z"
}
```

### DiaryEntry

```json
{
  "id": "diary-xyz789",
  "session_id": "session-abc",
  "summary": "Implemented OAuth2 flow with PKCE",
  "patterns_observed": ["token-refresh", "secure-storage"],
  "issues_encountered": ["redirect-uri-mismatch"],
  "candidate_rules": ["Always use state parameter in OAuth"],
  "created_at": "2024-03-19T16:45:00Z"
}
```

### SessionOutcome

```json
{
  "session_id": "session-current",
  "helpful_rules": ["RULE-123", "RULE-456"],
  "harmful_rules": ["RULE-789"],
  "recorded_at": "2024-03-20T17:00:00Z",
  "applied": false
}
```

---

## Rule Maturity States

Rules progress through maturity stages:

```
proposed → validated → mature → stale → deprecated
    ↓          ↓          ↓        ↓
 Needs      Evidence   Proven   Needs    Soft-
evidence   confirmed  helpful  refresh  deleted
```

| State | Meaning | Action |
|-------|---------|--------|
| `proposed` | Newly extracted, unvalidated | Await evidence |
| `validated` | Has supporting evidence | Monitor feedback |
| `mature` | Consistently helpful over time | Trust highly |
| `stale` | No recent feedback (>90 days) | Seek re-validation |
| `deprecated` | Marked for removal | Will be purged |

---

## MCP Server

Run cm as an MCP server for direct agent integration:

```bash
# Start server
cm serve

# Custom port
cm serve --port 9000

# With logging
cm serve --verbose
```

### MCP Tools

| Tool | Description |
|------|-------------|
| `get_context` | Retrieve task-relevant rules and history |
| `search_rules` | Semantic search over playbook |
| `record_feedback` | Mark rules as helpful/harmful |
| `record_outcome` | Record session outcome with rule attribution |
| `get_stats` | Get playbook health metrics |
| `validate_rule` | Check proposed rule against evidence |

### MCP Resources

| Resource | Description |
|----------|-------------|
| `playbook://rules` | Full playbook as JSON |
| `playbook://top/{n}` | Top N rules by score |
| `playbook://stale` | Rules needing re-validation |
| `diary://recent/{n}` | Recent diary entries |
| `stats://health` | Playbook health metrics |

---

## Configuration

### Directory Structure

```
~/.config/cm/
├── config.toml           # Main configuration
├── playbook.json         # Rule storage
└── diary/                # Session summaries
    └── *.json

.cm/                      # Project-local config
├── config.toml           # Project overrides
└── playbook.json         # Project-specific rules
```

### Config File Reference

```toml
# ~/.config/cm/config.toml

[general]
# LLM model for Generator/Reflector/Validator
model = "claude-sonnet-4-20250514"

# Auto-apply outcomes after session
auto_apply_outcomes = false

# Check for updates
check_updates = true

[decay]
# Half-life in days
half_life_days = 90

# Harmful feedback multiplier
harmful_multiplier = 4.0

# Minimum score before deprecation
min_score = 0.1

[reflection]
# Minimum sessions before reflecting
min_sessions = 3

# Auto-reflect on session end
auto_reflect = false

[privacy]
# Enable cross-agent learning
cross_agent_enrichment = true

# Anonymize session data in rules
anonymize_sources = false

[mcp]
# MCP server port
port = 8080

# Enable MCP server
enabled = false
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CM_CONFIG_DIR` | Configuration directory | `~/.config/cm` |
| `CM_DATA_DIR` | Data storage directory | `~/.local/share/cm` |
| `CM_MODEL` | LLM model for ACE pipeline | `claude-sonnet-4-20250514` |
| `CM_HALF_LIFE` | Decay half-life in days | `90` |
| `CM_MCP_PORT` | MCP server port | `8080` |

---

## Privacy Controls

```bash
# View current privacy settings
cm privacy

# Disable cross-agent learning
cm privacy --disable-enrichment

# Enable cross-agent learning
cm privacy --enable-enrichment

# Anonymize sources in exported playbooks
cm privacy --anonymize-export
```

### What Cross-Agent Enrichment Means

When enabled:
- Rules extracted from Agent A's sessions can help Agent B
- Diary entries reference sessions across agents
- Collective learning improves all agents

When disabled:
- Each agent's playbook is isolated
- No session data shared between identities
- Rules only come from your own sessions

---

## Project Integration

Export playbook for project documentation:

```bash
# Generate project patterns doc
cm project --output docs/PATTERNS.md

# Include confidence scores
cm project --output docs/PATTERNS.md --scores

# Only mature rules
cm project --output docs/PATTERNS.md --mature-only
```

This creates a human-readable document of learned patterns for team reference.

---

## Graceful Degradation

CM degrades gracefully when components are unavailable:

| Scenario | Behavior |
|----------|----------|
| No cass index | Works from diary only |
| No LLM access | Curator still works, reflection paused |
| Stale sessions | Uses cached diary entries |
| Empty playbook | Returns starter suggestions |

---

## Performance Characteristics

| Operation | Typical Time | Notes |
|-----------|--------------|-------|
| `cm context` | 50-200ms | Depends on playbook size |
| `cm similar` | 100-300ms | Semantic search overhead |
| `cm reflect` | 2-10s | LLM calls for Generator/Reflector |
| `cm validate` | 1-3s | LLM call for Validator |
| `cm mark` | <50ms | Pure database operation |

---

## Integration with CASS

CM builds on top of `cass` (Coding Agent Session Search):

```bash
# cass provides raw session search
cass search "authentication" --robot

# cm transforms that into procedural memory
cm context "authentication"
```

The typical workflow:
1. Work happens in agent sessions (stored by various tools)
2. `cass` indexes and searches those sessions
3. `cm reflect` extracts patterns into diary/playbook
4. `cm context` retrieves relevant knowledge for new tasks

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | General error |
| `2` | Configuration error |
| `3` | Validation failed |
| `4` | LLM error (reflection/validation) |
| `5` | No data (empty results) |

---

## Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| "No sessions found" | Run `cass reindex` to rebuild session index |
| "Reflection failed" | Check LLM API key and model availability |
| "Stale playbook" | Run `cm reflect` to process recent sessions |
| "Low confidence everywhere" | Natural decay; use `cm mark --helpful` to reinforce |

### Debug Mode

```bash
# Verbose output
cm context "task" --verbose

# Show scoring details
cm top 10 --debug

# Trace decay calculations
cm stats --trace-decay
```

---

## Ready-to-Paste AGENTS.md Blurb

```markdown
## cm - CASS Memory System

Procedural memory for AI coding agents. Transforms scattered sessions into
persistent cross-agent learnings with confidence decay and anti-pattern detection.

### Quick Start
cm context "your task" --json       # Get relevant rules
cm mark RULE-ID --helpful           # Reinforce good rules
cm outcome success "RULE-1,RULE-2"  # Record session results
cm reflect                          # Extract new rules

### Three Layers
- Episodic: Raw sessions (via cass)
- Working: Diary summaries
- Procedural: Playbook rules (this tool)

### Key Features
- 90-day confidence half-life (stale rules decay)
- 4x penalty for harmful rules (asymmetric by design)
- Anti-pattern auto-inversion (bad rules become warnings)
- Cross-agent learning (everyone benefits)
- LLM-free Curator (no hallucinated provenance)

### Essential Commands
cm context "task" --json    # Start of session
cm similar "pattern"        # Find related rules
cm mark ID --helpful/harmful # Give feedback
cm outcome success "IDs"    # End of session
cm reflect                  # Periodic maintenance

Exit codes: 0=success, 1=error, 2=config, 3=validation, 4=LLM, 5=no-data
```

---

## Workflow Example: Complete Session

```bash
# 1. Start task - get relevant context
cm context "implementing rate limiting for API" --json
# → Returns rules about rate limiting, caching, API design

# 2. Note which rules you're applying
# (mental note: RULE-123 about token buckets, RULE-456 about Redis)

# 3. During work, if you find a useful pattern
cm validate "Use sliding window for rate limit precision"
# → Shows if this has historical support

# 4. End of session - record what helped
cm outcome success "RULE-123,RULE-456"

# 5. If something hurt (caused bugs/issues)
cm outcome failure "RULE-789"

# 6. Apply the feedback
cm outcome-apply

# 7. Periodically, extract new rules
cm reflect --since "7d"
```

---

## Philosophy: Why Procedural Memory?

Episodic memory (raw sessions) is too noisy for real-time use. Working memory (summaries) lacks actionability. Procedural memory distills both into **executable rules** that directly guide behavior.

The key insight: **Rules should be testable hypotheses**, not static commandments. The confidence decay system treats every rule as a hypothesis that requires ongoing validation. Rules that stop being useful naturally fade; rules that keep helping get reinforced.

This mirrors how human expertise works: you don't remember every project you've done, but you retain the patterns that proved useful across many projects.
