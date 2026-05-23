---
name: context-assembler
description: Assembles relevant context for agent spawns with prioritized ranking. Ranks packages by relevance, enforces token budgets with graduated zones, captures error patterns for learning, and supports configurable per-agent retrieval limits.
version: 1.5.3
allowed-tools: [Bash, Read]
---

# Context-Assembler Skill

You are the context-assembler skill. When invoked, you assemble relevant context packages for agent spawns, prioritizing by relevance and respecting token budgets.

## When to Invoke This Skill

**Invoke this skill when:**
- Orchestrator prepares to spawn an agent and needs relevant context
- Any agent mentions "assemble context", "get context packages", or "context-assembler"
- Preparing developer/QA/tech lead spawns with session context
- Need to check for relevant error patterns before agent spawn

**Do NOT invoke when:**
- No active orchestration session exists
- Manually reading specific files (use Read tool directly)
- Working outside BAZINGA orchestration

---

## Your Task

When invoked, execute these steps in order:

### Step 1: Determine Context Parameters

Extract from the calling request or infer from conversation:
- `session_id`: Current orchestration session (REQUIRED)
- `group_id`: Task group being processed (OPTIONAL - use empty string "" if not provided)
- `agent_type`: Target agent - developer/senior_software_engineer/qa_expert/tech_lead/investigator (REQUIRED)
- `model`: Model being used - haiku/sonnet/opus or full model ID (OPTIONAL, for token budgeting)
- `current_tokens`: Current token usage in conversation (OPTIONAL, for zone detection)
- `iteration`: Current iteration number (optional, default 0)
- `include_reasoning`: Whether to include prior agent reasoning for handoff (OPTIONAL)
  - **DEFAULT BEHAVIOR:** Automatically `true` when reasoning context is beneficial:
    - `qa_expert`, `tech_lead`: ALWAYS (handoff recipients)
    - `senior_software_engineer`: ALWAYS (escalation needs prior context)
    - `investigator`: ALWAYS (debugging needs full context)
    - `developer`: When `iteration > 0` (retry needs prior reasoning; first attempt has none)
  - Explicitly set to `false` to disable reasoning for any agent
- `reasoning_level`: Level of detail for reasoning retrieval (OPTIONAL)
  - `minimal`: 400 tokens - key decisions only
  - `medium`: 800 tokens - decisions + approach (DEFAULT)
  - `full`: 1200 tokens - complete reasoning chain

If `session_id` or `agent_type` are missing, check recent conversation context or ask the orchestrator.

### Step 2: Load Configuration and Check FTS5

**Step 2a: Load retrieval limit for this agent type:**

```bash
# Extract retrieval limit for the specific agent type
AGENT_TYPE="developer"  # Replace with actual agent_type

# Pass AGENT_TYPE via command-line argument (not string interpolation)
LIMIT=$(cat bazinga/skills_config.json 2>/dev/null | python3 -c "
import sys, json
agent = sys.argv[1] if len(sys.argv) > 1 else 'developer'
defaults = {'developer': 3, 'senior_software_engineer': 5, 'qa_expert': 5, 'tech_lead': 5, 'investigator': 5}
try:
    c = json.load(sys.stdin).get('context_engineering', {})
    limits = c.get('retrieval_limits', {})
    print(limits.get(agent, defaults.get(agent, 3)))
except:
    print(defaults.get(agent, 3))
" "$AGENT_TYPE" 2>/dev/null || echo 3)
echo "Retrieval limit for $AGENT_TYPE: $LIMIT"
```

Default limits: developer=3, senior_software_engineer=5, qa_expert=5, tech_lead=5, investigator=5

**Step 2b: FTS5 availability:**

FTS5 is assumed unavailable (requires special SQLite build). Always use heuristic fallback in Step 3b for ranking.

```bash
# FTS5 disabled by default - use heuristic ranking
FTS5_AVAILABLE="false"
echo "FTS5_AVAILABLE=$FTS5_AVAILABLE (heuristic fallback enabled)"
```

**Step 2c: Determine token zone and budget:**

```bash
# Token estimation with tiktoken (with fallback to character estimation)
# Input: MODEL, CURRENT_TOKENS (from Step 1)
MODEL="sonnet"  # or "haiku", "opus", or full model ID
CURRENT_TOKENS=0  # Current usage if known, else 0

# IMPORTANT: Use eval to capture output as shell variables
eval "$(python3 -c "
import sys, json

try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False

# Model context limits (conservative estimates)
MODEL_LIMITS = {
    'haiku': 200000, 'claude-3-5-haiku': 200000,
    'sonnet': 200000, 'claude-sonnet-4-20250514': 200000, 'claude-3-5-sonnet': 200000,
    'opus': 200000, 'claude-opus-4-20250514': 200000
}

# Read safety margin from config (default 15%)
try:
    with open('bazinga/skills_config.json') as f:
        cfg = json.load(f).get('context_engineering', {})
        SAFETY_MARGIN = cfg.get('token_safety_margin', 0.15)
except:
    SAFETY_MARGIN = 0.15

model = sys.argv[1] if len(sys.argv) > 1 else 'sonnet'
current = int(sys.argv[2]) if len(sys.argv) > 2 else 0

# Normalize model name (longest key first to avoid partial matches)
model_key = model.lower()
for key in sorted(MODEL_LIMITS.keys(), key=len, reverse=True):
    if key in model_key:
        model_key = key
        break

limit = MODEL_LIMITS.get(model_key, 200000)
effective_limit = int(limit * (1 - SAFETY_MARGIN))

# Calculate REMAINING budget (not total)
remaining_budget = max(0, effective_limit - current)
usage_pct = (current / effective_limit * 100) if effective_limit > 0 else 0

# Determine zone
if usage_pct >= 95:
    zone = 'Emergency'
elif usage_pct >= 85:
    zone = 'Wrap-up'
elif usage_pct >= 75:
    zone = 'Conservative'
elif usage_pct >= 60:
    zone = 'Soft_Warning'  # Underscore for shell variable safety
else:
    zone = 'Normal'

# Token cap logic (T042 Part C):
# - If orchestrator passes current_tokens (even 0 for first spawn), trust zone detection
# - Only apply conservative cap if invoked outside orchestrator context (safety fallback)
# The orchestrator now tracks: estimated_token_usage = total_spawns * 15000
# First spawn: 0 tokens, zone=Normal, full budget available - this is correct behavior

# Output as shell variable assignments (will be eval'd)
print(f'ZONE={zone}')
print(f'USAGE_PCT={usage_pct:.1f}')
print(f'EFFECTIVE_LIMIT={effective_limit}')
print(f'REMAINING_BUDGET={remaining_budget}')
print(f'HAS_TIKTOKEN={HAS_TIKTOKEN}')
" "$MODEL" "$CURRENT_TOKENS")"

# Now $ZONE, $USAGE_PCT, $EFFECTIVE_LIMIT, $REMAINING_BUDGET, $HAS_TIKTOKEN are set
echo "Zone: $ZONE, Usage: $USAGE_PCT%, Remaining: $REMAINING_BUDGET tokens"
```

**Token Zone Behaviors:**

| Zone | Usage % | Behavior |
|------|---------|----------|
| Normal | 0-60% | Full context with all packages |
| Soft Warning | 60-75% | Prefer summaries over full content |
| Conservative | 75-85% | Minimal context, critical packages only |
| Wrap-up | 85-95% | Essential info only, no new packages |
| Emergency | 95%+ | Return immediately, suggest checkpoint |

**Token Budget Allocation by Agent Type:**

| Agent | Task | Specialization | Context Pkgs | Errors |
|-------|------|----------------|--------------|--------|
| developer | 50% | 20% | 20% | 10% |
| senior_software_engineer | 40% | 20% | 25% | 15% |
| qa_expert | 40% | 15% | 30% | 15% |
| tech_lead | 30% | 15% | 40% | 15% |
| investigator | 35% | 15% | 35% | 15% |

**Note:** SSE and Investigator handle escalations/complex debugging, so they need more context and error budget.

### Step 3: Query Context Packages (Zone-Conditional)

**CRITICAL: Execute query based on zone from Step 2c**

The query behavior depends entirely on the zone. Use this conditional structure:

```bash
# Zone-conditional query execution
# Variables from previous steps: $ZONE, $SESSION_ID, $GROUP_ID, $AGENT_TYPE, $LIMIT, $REMAINING_BUDGET

# Initialize result variable
QUERY_RESULT=""

if [ "$ZONE" = "Emergency" ]; then
    # Emergency zone: Skip all queries, go directly to Step 5
    echo "ZONE=Emergency: Skipping context query, proceeding to emergency output"
    QUERY_RESULT='{"packages":[],"total_available":0,"zone_skip":true}'

elif [ "$ZONE" = "Wrap-up" ]; then
    # Wrap-up zone: Skip context packages, minimal output only
    echo "ZONE=Wrap-up: Skipping context packages"
    QUERY_RESULT='{"packages":[],"total_available":0,"zone_skip":true}'

elif [ "$ZONE" = "Conservative" ]; then
    # Conservative zone: Priority fallback with LIMIT items across buckets
    echo "ZONE=Conservative: Using priority fallback ladder via bazinga-db"

    # Use bazinga-db get-context-packages command for each priority level
    QUERY_RESULT=$(python3 -c "
import subprocess
import json
import sys
import time

session_id = sys.argv[1]
group_id = sys.argv[2]
limit = int(sys.argv[3])
agent_type = sys.argv[4] if len(sys.argv) > 4 else 'developer'

def db_cmd_with_retry(cmd_args, max_retries=3, backoff_ms=[100, 250, 500]):
    '''Execute bazinga-db command with retry on database busy.'''
    for attempt in range(max_retries + 1):
        result = subprocess.run(cmd_args, capture_output=True, text=True)
        if result.returncode == 0:
            try:
                return json.loads(result.stdout) if result.stdout.strip() else []
            except json.JSONDecodeError:
                # Surface error rather than silently returning empty
                sys.stderr.write(f'JSON decode error: {result.stdout[:100]}\\n')
                return []
        if 'database is locked' in result.stderr or 'SQLITE_BUSY' in result.stderr:
            if attempt < max_retries:
                time.sleep(backoff_ms[attempt] / 1000.0)
                continue
        # Surface command errors
        if result.stderr:
            sys.stderr.write(f'Command error: {result.stderr[:200]}\\n')
        return []
    return []

# Priority fallback: Use bazinga-db to fetch packages by priority
# The get-context-packages command handles priority ordering internally
collected = db_cmd_with_retry([
    'python3', '.claude/skills/bazinga-db/scripts/bazinga_db.py', '--quiet',
    'get-context-packages', session_id, group_id, agent_type, str(limit)
])

# Handle result format
if isinstance(collected, dict):
    packages = collected.get('packages', [])
    total_available = collected.get('total_available', len(packages))
elif isinstance(collected, list):
    packages = collected
    total_available = len(packages)
else:
    packages = []
    total_available = 0

print(json.dumps({'packages': packages, 'total_available': total_available}))
" "$SESSION_ID" "$GROUP_ID" "$LIMIT" "$AGENT_TYPE")

else
    # Normal or Soft_Warning zone: Standard query
    echo "ZONE=$ZONE: Standard query with LIMIT=$LIMIT"
    QUERY_RESULT=$(python3 -c "
import subprocess
import json
import sys
import time

session_id = sys.argv[1]
group_id = sys.argv[2]
agent_type = sys.argv[3]
limit = int(sys.argv[4])

def db_query_with_retry(cmd_args, max_retries=3, backoff_ms=[100, 250, 500]):
    for attempt in range(max_retries + 1):
        result = subprocess.run(cmd_args, capture_output=True, text=True)
        if result.returncode == 0:
            try:
                return json.loads(result.stdout) if result.stdout.strip() else []
            except json.JSONDecodeError:
                return []
        if 'SQLITE_BUSY' in result.stderr or 'database is locked' in result.stderr:
            if attempt < max_retries:
                time.sleep(backoff_ms[attempt] / 1000.0)
                continue
        return []
    return []

# Use bazinga-db get-context-packages (parameterized, safe)
result = db_query_with_retry([
    'python3', '.claude/skills/bazinga-db/scripts/bazinga_db.py', '--quiet',
    'get-context-packages', session_id, group_id, agent_type, str(limit)
])

# If result is dict with 'packages' key, use it; otherwise wrap
if isinstance(result, dict):
    print(json.dumps(result))
elif isinstance(result, list):
    print(json.dumps({'packages': result, 'total_available': len(result)}))
else:
    print(json.dumps({'packages': [], 'total_available': 0}))
" "$SESSION_ID" "$GROUP_ID" "$AGENT_TYPE" "$LIMIT")
fi

# Parse result for next steps (log count only - summaries may contain secrets before redaction)
echo "Query returned: $(echo "$QUERY_RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{len(d.get(\"packages\",[]))} packages, total_available={d.get(\"total_available\",0)}')" 2>/dev/null || echo 'parse error')"
```

**If query fails or returns empty, proceed to Step 3b (Heuristic Fallback).**

### Step 3b: Heuristic Fallback (Query Failed or FTS5 Unavailable)

**First, fetch raw context packages with consumer data:**

```bash
# Fetch packages with LEFT JOIN to get consumer info for agent_relevance calculation
SESSION_ID="bazinga_20250212_143530"
GROUP_ID="group_a"  # or empty string for session-wide
AGENT_TYPE="developer"

# Note: SESSION_ID is system-generated (not user input), but use shell variables for clarity
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet query \
  "SELECT cp.id, cp.file_path, cp.priority, cp.summary, cp.group_id, cp.created_at,
          GROUP_CONCAT(cs.agent_type) as consumers
   FROM context_packages cp
   LEFT JOIN consumption_scope cs ON cp.id = cs.package_id AND cs.session_id = cp.session_id
   WHERE cp.session_id = '$SESSION_ID'
   GROUP BY cp.id"
```

**Then apply heuristic ranking:**

| Priority | Weight |
|----------|--------|
| critical | 4 |
| high | 3 |
| medium | 2 |
| low | 1 |

**Scoring Formula:**
```
score = (priority_weight * 4) + (same_group_boost * 2) + (agent_relevance * 1.5) + recency_factor

Where:
- same_group_boost = 1 if package.group_id == request.group_id, else 0
- agent_relevance = 1 if AGENT_TYPE appears in package.consumers (from JOIN), else 0
- recency_factor = 1 / (days_since_created + 1)
```

Sort packages by score DESC, then by `created_at DESC` (tie-breaker), take top N.
Calculate: `overflow_count = max(0, total_packages - limit)`

### Step 3c: Token Packing with Redaction

After Step 3 or 3b retrieves packages, apply redaction, truncation, and token packing in the correct order:

```bash
# Token packing with proper order: redact → truncate → estimate → pack
# Input: $QUERY_RESULT (JSON from Step 3), $ZONE, $AGENT_TYPE, $REMAINING_BUDGET

PACKED_RESULT=$(python3 -c "
import json
import sys
import re

# Inputs from command line
query_result = json.loads(sys.argv[1])
zone = sys.argv[2]
agent_type = sys.argv[3]
remaining_budget = int(sys.argv[4])

packages = query_result.get('packages', [])
total_available = query_result.get('total_available', len(packages))

# --- Redaction Patterns (apply FIRST) ---
REDACTION_PATTERNS = [
    (r'(?i)(api[_-]?key|apikey|access[_-]?token|auth[_-]?token|bearer)[\"\\s:=]+[\"\\']?([a-zA-Z0-9_\\-]{20,})[\"\\']?', r'\\1=[REDACTED]'),
    (r'(?i)(aws[_-]?(access|secret)[_-]?key[_-]?id?)[\"\\s:=]+[\"\\']?([A-Z0-9]{16,})[\"\\']?', r'\\1=[REDACTED]'),
    (r'(?i)(password|passwd|secret|private[_-]?key)[\"\\s:=]+[\"\\']?([^\\s\"\\'\n]{8,})[\"\\']?', r'\\1=[REDACTED]'),
    (r'(?i)(mongodb|postgres|mysql|redis|amqp)://[^\\s]+@', r'\\1://[REDACTED]@'),
    (r'eyJ[a-zA-Z0-9_-]*\\.eyJ[a-zA-Z0-9_-]*\\.[a-zA-Z0-9_-]*', '[JWT_REDACTED]'),
]

def redact_text(text):
    for pattern, replacement in REDACTION_PATTERNS:
        text = re.sub(pattern, replacement, text)
    return text

# --- Truncation limits per zone ---
SUMMARY_LIMITS = {
    'Normal': 400,
    'Soft_Warning': 200,
    'Conservative': 100,
    'Wrap-up': 60,
    'Emergency': 0
}

def truncate_summary(summary, zone):
    max_len = SUMMARY_LIMITS.get(zone, 400)
    if len(summary) <= max_len:
        return summary
    truncated = summary[:max_len].rsplit(' ', 1)[0]
    return truncated + '...'

# --- Token estimation ---
def estimate_tokens(text):
    # ~4 chars per token (conservative fallback)
    return len(text) // 4 + 1

# --- Budget allocation ---
CONTEXT_PCT = {
    'developer': 0.20,
    'senior_software_engineer': 0.25,
    'qa_expert': 0.30,
    'tech_lead': 0.40,
    'investigator': 0.35
}

pct = CONTEXT_PCT.get(agent_type, 0.20)
context_budget = int(remaining_budget * pct)  # Use REMAINING, not total

# --- Process packages: redact → truncate → estimate → pack ---
packed = []
used_tokens = 0
package_ids = []

for pkg in packages:
    raw_summary = pkg.get('summary', '')

    # 1. REDACT first
    redacted_summary = redact_text(raw_summary)

    # 2. TRUNCATE second
    truncated_summary = truncate_summary(redacted_summary, zone)

    # 3. ESTIMATE tokens
    pkg_text = f\"**[{pkg.get('priority', 'medium').upper()}]** {pkg.get('file_path', '')}\\n> {truncated_summary}\"
    pkg_tokens = estimate_tokens(pkg_text)

    # 4. PACK if within budget
    if used_tokens + pkg_tokens > context_budget:
        break

    packed.append({
        'id': pkg.get('id'),
        'file_path': pkg.get('file_path'),
        'priority': pkg.get('priority'),
        'summary': truncated_summary,
        'est_tokens': pkg_tokens
    })
    package_ids.append(pkg.get('id'))
    used_tokens += pkg_tokens

print(json.dumps({
    'packages': packed,
    'total_available': total_available,
    'used_tokens': used_tokens,
    'budget': context_budget,
    'package_ids': package_ids
}))
" "$QUERY_RESULT" "$ZONE" "$AGENT_TYPE" "$REMAINING_BUDGET")

# Extract package IDs for Step 5b consumption tracking (cast to strings to avoid TypeError)
PACKAGE_IDS=($(echo "$PACKED_RESULT" | python3 -c "import sys,json; ids=json.load(sys.stdin).get('package_ids',[]); print(' '.join(str(x) for x in ids))"))

echo "Packed: $(echo "$PACKED_RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{len(d.get(\"packages\",[]))} pkgs, {d.get(\"used_tokens\",0)}/{d.get(\"budget\",0)} tokens')")"
echo "Package IDs to mark consumed: ${PACKAGE_IDS[*]}"
```

**Key improvements:**
- Uses `REMAINING_BUDGET` (not total limit)
- Applies redaction BEFORE truncation
- Populates `PACKAGE_IDS` array for Step 5b
- Includes `investigator` in budget allocation

### Step 3.5: Prior Reasoning Retrieval (Automatic for Handoffs)

**When to include:**
- **AUTOMATIC** for `qa_expert` and `tech_lead` (handoff recipients in workflow)
- **OPTIONAL** for other agents (only if `Include Reasoning: true` is explicit)
- Can be **disabled** for any agent with `Include Reasoning: false`

**Purpose:** Retrieve prior agents' reasoning to provide continuity during handoffs (Developer→QA→Tech Lead).

**Reasoning Levels (Token Budgets):**

| Level | Tokens | Content | Use Case |
|-------|--------|---------|----------|
| `minimal` | 400 | Key decisions only | Quick handoff, simple tasks |
| `medium` | 800 | Decisions + approach (DEFAULT) | Standard handoffs |
| `full` | 1200 | Complete reasoning chain | Complex tasks, debugging |

**Priority Order:** completion > decisions > understanding (most actionable first).

**Variable Setup:** Determine reasoning inclusion based on agent type, iteration, and explicit overrides:
```bash
# Step 3.5 Variable Setup
# Automatic reasoning when context is beneficial

AGENT_TYPE="developer"  # From Step 1
ITERATION="${ITERATION:-0}"  # From Step 1 (default 0)

# Smart default: Enable reasoning when it provides value
# - qa_expert, tech_lead: ALWAYS (handoff recipients)
# - senior_software_engineer, investigator: ALWAYS (escalation/debugging needs context)
# - developer: Only on retry (iteration > 0); first attempt has no prior reasoning

case "$AGENT_TYPE" in
    qa_expert|tech_lead|senior_software_engineer|investigator)
        INCLUDE_REASONING="true"   # Always include for these agents
        ;;
    developer)
        if [ "$ITERATION" -gt 0 ]; then
            INCLUDE_REASONING="true"   # Retry needs prior reasoning
        else
            INCLUDE_REASONING="false"  # First attempt has no prior context
        fi
        ;;
    *)
        INCLUDE_REASONING="false"  # Unknown agents default off
        ;;
esac

# Check for explicit override in request (parse from Step 1)
# "Include Reasoning: false" -> disable even for QA/TL/SSE
# "Include Reasoning: true" -> enable even for developer first attempt
# "Reasoning Level: full" -> set REASONING_LEVEL

REASONING_LEVEL="medium"  # Default level
# If request contains "Reasoning Level: minimal" -> REASONING_LEVEL="minimal"
# If request contains "Reasoning Level: full" -> REASONING_LEVEL="full"
```

```bash
# Prior reasoning retrieval with level-based token budgets
# Variables: $SESSION_ID, $GROUP_ID, $AGENT_TYPE, $ITERATION, $INCLUDE_REASONING, $REASONING_LEVEL

# FIX 1: Validate iteration is a valid number (default to 0 if invalid)
validate_iteration() {
    local val="$1"
    if [[ "$val" =~ ^[0-9]+$ ]]; then
        echo "$val"
    else
        echo "0"  # Default to 0 for invalid input
    fi
}

ITERATION=$(validate_iteration "${ITERATION:-0}")

# Apply smart defaults if not explicitly set
if [ -z "$INCLUDE_REASONING" ]; then
    case "$AGENT_TYPE" in
        qa_expert|tech_lead|senior_software_engineer|investigator)
            INCLUDE_REASONING="true"
            ;;
        developer)
            if [ "$ITERATION" -gt 0 ]; then
                INCLUDE_REASONING="true"
            else
                INCLUDE_REASONING="false"
            fi
            ;;
        *)
            INCLUDE_REASONING="false"
            ;;
    esac
fi

REASONING_LEVEL="${REASONING_LEVEL:-medium}"

if [ "$INCLUDE_REASONING" = "true" ]; then
    echo "Retrieving prior reasoning for handoff context (level: $REASONING_LEVEL, iteration: $ITERATION)..."

    REASONING_DIGEST=$(python3 -c "
import sys
import json
import subprocess

session_id = sys.argv[1]
group_id = sys.argv[2] if len(sys.argv) > 2 else ''
reasoning_level = sys.argv[3] if len(sys.argv) > 3 else 'medium'
target_agent = sys.argv[4] if len(sys.argv) > 4 else 'unknown'

# Token budget based on reasoning level
LEVEL_BUDGETS = {
    'minimal': 400,
    'medium': 800,
    'full': 1200
}
max_tokens = LEVEL_BUDGETS.get(reasoning_level, 800)

# FIX 2: Relevance filtering - define which agents' reasoning is relevant for each target
# Workflow: Developer -> QA -> Tech Lead
# Escalation: Developer -> SSE, Developer -> Investigator
RELEVANT_AGENTS = {
    'qa_expert': ['developer', 'senior_software_engineer'],  # QA needs dev reasoning
    'tech_lead': ['developer', 'senior_software_engineer', 'qa_expert'],  # TL needs dev + QA
    'senior_software_engineer': ['developer'],  # SSE needs failed dev reasoning
    'investigator': ['developer', 'senior_software_engineer', 'qa_expert'],  # Investigator needs all
    'developer': ['developer', 'qa_expert', 'tech_lead'],  # Dev retry needs own + feedback
}
relevant_agents = RELEVANT_AGENTS.get(target_agent, [])

# FIX 3: Pruning limits for long retry chains
MAX_ENTRIES_PER_AGENT = 2  # Max 2 most recent entries per agent type
MAX_TOTAL_ENTRIES = 5  # Max 5 entries total regardless of agents

# Query reasoning from database via bazinga-db
# Priority order: completion > decisions > understanding (most actionable first)
PRIORITY_PHASES = ['completion', 'decisions', 'understanding']

try:
    # Get all reasoning for this session/group
    cmd = ['python3', '.claude/skills/bazinga-db/scripts/bazinga_db.py', '--quiet', 'get-reasoning', session_id]
    if group_id:
        cmd.extend(['--group_id', group_id])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(json.dumps({'error': 'query_failed', 'entries': [], 'used_tokens': 0}))
        sys.exit(0)

    entries = json.loads(result.stdout) if result.stdout.strip() else []
except Exception as e:
    print(json.dumps({'error': str(e), 'entries': [], 'used_tokens': 0}))
    sys.exit(0)

if not entries:
    print(json.dumps({'entries': [], 'used_tokens': 0, 'total_available': 0}))
    sys.exit(0)

# FIX 2: Filter to relevant agents only
if relevant_agents:
    entries = [e for e in entries if e.get('agent_type') in relevant_agents]

# FIX 3: Prune to MAX_ENTRIES_PER_AGENT per agent (most recent first)
# Group by agent, sort by timestamp desc, take top N per agent
from collections import defaultdict
agent_entries = defaultdict(list)
for entry in entries:
    agent_entries[entry.get('agent_type', 'unknown')].append(entry)

pruned_entries = []
for agent, agent_list in agent_entries.items():
    # Sort by timestamp descending (most recent first)
    agent_list.sort(key=lambda e: e.get('timestamp', ''), reverse=True)
    # Take only MAX_ENTRIES_PER_AGENT
    pruned_entries.extend(agent_list[:MAX_ENTRIES_PER_AGENT])

entries = pruned_entries

# Sort by priority phase, then by timestamp (most recent first within each phase)
def phase_priority(entry):
    phase = entry.get('phase', 'understanding')
    try:
        return PRIORITY_PHASES.index(phase)
    except ValueError:
        return len(PRIORITY_PHASES)  # Unknown phases last

# Two-pass sort: first by timestamp DESC, then stable sort by phase priority ASC
# This gives us most recent entries first within each phase
entries.sort(key=lambda e: e.get('timestamp', ''), reverse=True)  # timestamp DESC
entries.sort(key=phase_priority)  # phase priority ASC (stable sort preserves timestamp order)

# FIX 3: Apply total entry limit
entries = entries[:MAX_TOTAL_ENTRIES]

# Token estimation (~4 chars per token)
def estimate_tokens(text):
    return len(text) // 4 + 1 if text else 0

# Pack entries within budget
packed = []
used_tokens = 0

for entry in entries:
    content = entry.get('content', '')
    # Format: [agent] phase: content
    formatted = f\"[{entry.get('agent_type', 'unknown')}] {entry.get('phase', 'unknown')}: {content[:300]}\"
    entry_tokens = estimate_tokens(formatted)

    if used_tokens + entry_tokens > max_tokens:
        break

    packed.append({
        'agent_type': entry.get('agent_type'),
        'phase': entry.get('phase'),
        'content': content[:300] if len(content) > 300 else content,
        'confidence': entry.get('confidence_level'),
        'est_tokens': entry_tokens
    })
    used_tokens += entry_tokens

print(json.dumps({
    'entries': packed,
    'used_tokens': used_tokens,
    'budget': max_tokens,
    'level': reasoning_level,
    'total_available': len(entries),
    'relevant_agents': relevant_agents,
    'pruning': {'max_per_agent': MAX_ENTRIES_PER_AGENT, 'max_total': MAX_TOTAL_ENTRIES}
}))
" "$SESSION_ID" "$GROUP_ID" "$REASONING_LEVEL" "$AGENT_TYPE")

    echo "Reasoning digest: $(echo "$REASONING_DIGEST" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{len(d.get(\"entries\",[]))} entries, {d.get(\"used_tokens\",0)}/{d.get(\"budget\",800)} tokens (level: {d.get(\"level\", \"medium\")})')" 2>/dev/null || echo 'parse error')"
else
    REASONING_DIGEST='{"entries":[],"used_tokens":0,"level":"none"}'
    echo "Skipping reasoning retrieval (include_reasoning=false for $AGENT_TYPE)"
fi
```

**Output Format for Step 5:**

If reasoning entries are found, include in output:

```markdown
### Prior Agent Reasoning ({count} entries)

**[developer] completion:** Successfully implemented authentication using JWT...
**[qa_expert] decisions:** Chose to focus on edge cases for token expiration...
```

Only include if `$INCLUDE_REASONING = true` AND entries exist.

### Step 4: Query Error Patterns (Optional)

If the agent previously failed or error patterns might be relevant:

**Step 4a: Get project_id from session:**
```bash
SESSION_ID="bazinga_20250212_143530"

# Retrieve project_id (defaults to 'default' if not set)
PROJECT_ID=$(python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet query \
  "SELECT COALESCE(json_extract(metadata, '\$.project_id'), 'default') as pid FROM sessions WHERE session_id = '$SESSION_ID'" \
  2>/dev/null | python3 -c "import sys,json; r=json.load(sys.stdin); print(r[0]['pid'] if r else 'default')" 2>/dev/null || echo "default")
```

**Step 4b: Query matching error patterns:**
```bash
# Filter by project_id and optionally session_id for more specific matches
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet query \
  "SELECT signature_json, solution, confidence, occurrences FROM error_patterns WHERE project_id = '$PROJECT_ID' AND confidence > 0.7 ORDER BY confidence DESC, occurrences DESC LIMIT 3"
```

Only include patterns with confidence > 0.7 in the output.

### Step 5: Format Output

**Compute display values:**
- `count` = number of packages returned (up to limit)
- `available` = total_available from Step 3 response (or total from Step 3b query)
- `overflow_count` = max(0, available - count)
- `zone` = current token zone from Step 2c
- `usage_pct` = token usage percentage from Step 2c

**Micro-Summary Truncation:**

Apply zone-specific summary length limits for actual degradation:

| Zone | Max Summary Chars | Rationale |
|------|-------------------|-----------|
| Normal | 400 | Full detail |
| Soft Warning | 200 | Reduced detail |
| Conservative | 100 | Key points only |
| Wrap-up | 60 | Minimal hints |

```python
def truncate_summary(summary: str, zone: str) -> str:
    """Truncate summary based on zone-specific limits."""
    limits = {
        'Normal': 400,
        'Soft_Warning': 200,  # Underscore to match $ZONE variable
        'Conservative': 100,
        'Wrap-up': 60,
        'Emergency': 0  # No summaries in emergency
    }
    max_len = limits.get(zone, 400)
    if len(summary) <= max_len:
        return summary
    # Truncate at word boundary with ellipsis
    truncated = summary[:max_len].rsplit(' ', 1)[0]
    return truncated + '...'
```

Apply `truncate_summary()` to each package summary before rendering output.

**Summary Redaction (Security):**

Apply the same redaction patterns used for error_patterns to summaries before output:

```python
import re

# Redaction patterns for secrets (same as error_patterns redaction)
REDACTION_PATTERNS = [
    # API keys and tokens
    (r'(?i)(api[_-]?key|apikey|access[_-]?token|auth[_-]?token|bearer)["\s:=]+["\']?([a-zA-Z0-9_\-]{20,})["\']?', r'\1=[REDACTED]'),
    # AWS credentials
    (r'(?i)(aws[_-]?(access|secret)[_-]?key[_-]?id?)["\s:=]+["\']?([A-Z0-9]{16,})["\']?', r'\1=[REDACTED]'),
    # Passwords and secrets
    (r'(?i)(password|passwd|secret|private[_-]?key)["\s:=]+["\']?([^\s"\']{8,})["\']?', r'\1=[REDACTED]'),
    # Connection strings
    (r'(?i)(mongodb|postgres|mysql|redis|amqp)://[^\s]+@', r'\1://[REDACTED]@'),
    # JWT tokens
    (r'eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*', '[JWT_REDACTED]'),
]

def redact_summary(summary: str) -> str:
    """Redact potential secrets from summary."""
    redacted = summary
    for pattern, replacement in REDACTION_PATTERNS:
        redacted = re.sub(pattern, replacement, redacted)

    # Entropy-based detection for high-entropy strings (potential secrets)
    def has_high_entropy(s):
        if len(s) < 20:
            return False
        char_set = set(s)
        # High entropy = many unique chars relative to length
        return len(char_set) / len(s) > 0.6 and any(c.isdigit() for c in s) and any(c.isupper() for c in s)

    # Find and redact high-entropy strings
    words = redacted.split()
    for i, word in enumerate(words):
        if has_high_entropy(word):
            words[i] = '[REDACTED]'
    return ' '.join(words)
```

Apply `redact_summary()` before `truncate_summary()` in the processing pipeline.

**Zone-Specific Output:**

**Emergency Zone (95%+):**
```markdown
## Context for {agent_type}

🚨 **Token budget: Emergency ({usage_pct}%) - Checkpoint recommended**

Context assembly skipped due to token budget constraints.
Suggest: Complete current operation and start new session.
```

**Wrap-up Zone (85-95%):**
```markdown
## Context for {agent_type}

🔶 **Token budget: Wrap-up ({usage_pct}%) - Completing current operation**

### Essential Info Only

Minimal context mode active. Focus on completing current task.
```

**Conservative Zone (75-85%):**
```markdown
## Context for {agent_type}

🔶 **Token budget: Conservative ({usage_pct}%)**

### Priority Packages ({count}/{available}) - {priority_used} level

**[{PRIORITY}]** {file_path}
> {summary}
```

Note: `priority_used` comes from the fallback ladder response (critical/high/medium).

**Soft Warning Zone (60-75%):**
```markdown
## Context for {agent_type}

🔶 **Token budget: Soft Warning ({usage_pct}%) - Reduced summaries (200 char)**

### Relevant Packages ({count}/{available})

**[{PRIORITY}]** {file_path}
> {summary}  ← Truncated to 200 chars
```

**Normal Zone (0-60%):**
```markdown
## Context for {agent_type}

### Relevant Packages ({count}/{available})

**[{PRIORITY}]** {file_path}
> {summary}

**[{PRIORITY}]** {file_path}
> {summary}

### Prior Agent Reasoning ({reasoning_count} entries)
<!-- Only include if include_reasoning=true AND entries exist -->

**[developer] completion:** Successfully implemented the core logic with edge case handling...
**[qa_expert] decisions:** Focused test coverage on authentication flow boundaries...

### Error Patterns ({pattern_count} matches)

⚠️ **Known Issue**: "{error_signature}"
> **Solution**: {solution}
> **Confidence**: {confidence} (seen {occurrences} times)

📦 +{overflow_count} more packages available (re-invoke with higher limit to expand)
```

**Priority Indicators:**
- `[CRITICAL]` - Priority: critical
- `[HIGH]` - Priority: high
- `[MEDIUM]` - Priority: medium
- `[LOW]` - Priority: low

**Zone Indicators:**
- Normal zone: No indicator (full context)
- Soft Warning/Conservative/Wrap-up: `🔶` (orange diamond)
- Emergency: `🚨` (emergency symbol)

**Only show overflow indicator if overflow_count > 0 AND zone is Normal or Soft Warning.**

### Step 5b: Mark Packages as Consumed (consumption_scope table)

**IMPORTANT: Only run if zone is Normal or Soft_Warning (skip for Wrap-up/Emergency)**

After formatting output, mark delivered packages as consumed in the `consumption_scope` table to prevent repeated delivery and enable iteration-aware tracking:

```bash
# Only mark consumption if packages were actually delivered
if { [ "$ZONE" = "Normal" ] || [ "$ZONE" = "Soft_Warning" ]; } && [ ${#PACKAGE_IDS[@]} -gt 0 ]; then
    # Mark consumed packages using bazinga-db mark-context-consumed command
    marked=0
    for pkg_id in "${PACKAGE_IDS[@]}"; do
        if python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet \
            mark-context-consumed "$pkg_id" "$AGENT_TYPE" "$ITERATION" 2>/dev/null; then
            marked=$((marked + 1))
        fi
    done
    echo "Marked $marked/${#PACKAGE_IDS[@]} packages as consumed via bazinga-db"
else
    echo "Skipping consumption tracking (zone=$ZONE or no packages)"
fi
```

**Key features:**
- Uses **bazinga-db mark-context-consumed** command (proper skill invocation)
- Handles retry logic internally within bazinga-db skill
- Iteration-aware tracking per data-model.md
- **Skips** in Wrap-up/Emergency zones (nothing delivered)

### Step 6: Handle Edge Cases

**Empty Packages:**
If no context packages are found (count=0, available=0):
```markdown
## Context for {agent_type}

### Relevant Packages (0/0)

No context packages found for this session/group. The agent will proceed with task and specialization context only.
```

**Graceful Degradation:**
If ANY step fails (database unavailable, query error, etc.):
1. Log a warning (but do NOT block execution)
2. Return minimal context:
```markdown
## Context for {agent_type}

:warning: Context assembly encountered an error. Proceeding with minimal context.

**Fallback Mode**: Task and specialization context only. Context packages unavailable.
```

3. **CRITICAL**: The orchestrator should NEVER block on context-assembler failure

---

## Step 7: Strategy Extraction (Success Path)

**When:** Triggered after a task group completes successfully (Tech Lead APPROVED status).

**Purpose:** Extract and save successful approaches to the `strategies` table for future agent guidance.

### Trigger Conditions

Strategy extraction should run when:
- Tech Lead returns `APPROVED` status for a group
- Developer completes without needing escalation
- QA passes all tests on first attempt

### Strategy Extraction Process

**Note:** Strategy extraction is triggered by the orchestrator (phase_simple.md, phase_parallel.md) after Tech Lead approval using the `bazinga-db extract-strategies` command:

```
bazinga-db-context, please extract strategies:

Session ID: {session_id}
Group ID: {group_id}
Project ID: {project_id}
Lang: {detected_lang}
Framework: {detected_framework}
```
Then invoke: `Skill(command: "bazinga-db-context")`

**What the command does:**
1. Queries `agent_reasoning` table for completion/decisions/approach phases
2. Maps phases to topics: completion→implementation, decisions→architecture, approach→methodology
3. Generates deterministic `strategy_id` = `{project_id}_{topic}_{content_hash}`
4. Upserts to `strategies` table (increments helpfulness if exists)
5. Returns count of extracted strategies

### Strategy Schema Reference

| Field | Type | Description |
|-------|------|-------------|
| `strategy_id` | TEXT PK | Unique identifier (project_topic_hash) |
| `project_id` | TEXT | Project this strategy applies to |
| `topic` | TEXT | Category: implementation, architecture, methodology |
| `insight` | TEXT | The actual insight/approach (max 500 chars) |
| `helpfulness` | INT | Usage counter, incremented on reuse |
| `lang` | TEXT | Language context (python, typescript, etc.) |
| `framework` | TEXT | Framework context (react, fastapi, etc.) |
| `last_seen` | TEXT | Last time strategy was applied |
| `created_at` | TEXT | When strategy was first captured |

### Strategy Retrieval for Context

When assembling context, strategies can be queried for relevant hints:

```sql
SELECT topic, insight FROM strategies
WHERE project_id = ?
  AND (lang IS NULL OR lang = ?)
  AND (framework IS NULL OR framework = ?)
ORDER BY helpfulness DESC, last_seen DESC
LIMIT 3
```

---

## Configuration Reference

From `bazinga/skills_config.json`:

```json
{
  "context_engineering": {
    "enable_context_assembler": true,
    "enable_fts5": false,
    "retrieval_limits": {
      "developer": 3,
      "senior_software_engineer": 5,
      "qa_expert": 5,
      "tech_lead": 5,
      "investigator": 5
    },
    "redaction_mode": "pattern_only",
    "token_safety_margin": 0.15
  }
}
```

| Setting | Default | Description |
|---------|---------|-------------|
| `enable_context_assembler` | true | Enable/disable the skill |
| `enable_fts5` | false | Use FTS5 for relevance (requires SQLite FTS5) |
| `retrieval_limits.*` | 3 | Max packages per agent type |
| `redaction_mode` | pattern_only | Secret redaction mode |
| `token_safety_margin` | 0.15 | Safety margin for token budgets |

---

## Example Invocations

### Example 1: Developer Context Assembly

**Request:**
```
Assemble context for developer spawn:
- Session: bazinga_20250212_143530
- Group: group_a
- Agent: developer
```

**Output:**
```markdown
## Context for developer

### Relevant Packages (3/7)

**[HIGH]** research/auth-patterns.md
> JWT authentication patterns for React Native apps

**[MEDIUM]** research/api-design.md
> REST API design guidelines for mobile clients

**[MEDIUM]** findings/codebase-analysis.md
> Existing authentication code in src/auth/

### Error Patterns (1 match)

:warning: **Known Issue**: "Cannot find module '@/utils'"
> **Solution**: Check tsconfig.json paths configuration - ensure baseUrl is set correctly
> **Confidence**: 0.8 (seen 3 times)

:package: +4 more packages available (re-invoke with higher limit to expand)
```

### Example 2: Session-Wide Context (No Group)

**Request:**
```
Assemble context for tech_lead spawn:
- Session: bazinga_20250212_143530
- Group: (none - session-wide)
- Agent: tech_lead
```

**Commands used:**
```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet get-context-packages \
  "bazinga_20250212_143530" "" "tech_lead" 5
```

### Example 3: Empty Context

**Output:**
```markdown
## Context for qa_expert

### Relevant Packages (0/0)

No context packages found for this session/group. The agent will proceed with task and specialization context only.
```

### Example 4: Error/Fallback

**Output (if database unavailable):**
```markdown
## Context for tech_lead

:warning: Context assembly encountered an error. Proceeding with minimal context.

**Fallback Mode**: Task and specialization context only. Context packages unavailable.
```

---

## Security Notes

**Parameter Handling:**
- Always assign user-provided values to shell variables first
- Use quoted variable expansion (`"$VAR"`) in commands
- The bazinga-db CLI uses positional arguments (safer than string interpolation)
- Avoid constructing SQL strings with raw user input

**Example of safe vs unsafe:**
```bash
# SAFE: Use shell variables with quotes
SESSION_ID="user_provided_session"
python3 ... --quiet get-context-packages "$SESSION_ID" "$GROUP_ID" "$AGENT_TYPE" "$LIMIT"

# UNSAFE: Direct string interpolation (avoid this)
python3 ... --quiet query "SELECT * FROM t WHERE id = 'user_input'"
```

---

## Integration with Orchestrator

The orchestrator invokes this skill before spawning agents:

```python
# 1. Invoke context-assembler
Skill(command: "context-assembler")

# 2. Capture output and include in agent prompt
Task(
    prompt=f"""
    {context_assembler_output}

    ## Your Task
    {task_description}
    """,
    subagent_type="developer"
)
```

---

## Database Tables Used

| Table | Purpose |
|-------|---------|
| `context_packages` | Research files, findings, artifacts with priority/summary |
| `consumption_scope` | Iteration-aware package consumption tracking (per data-model.md) |
| `error_patterns` | Captured error signatures with solutions |
| `strategies` | Successful approaches extracted from completed tasks (Step 7) |
| `agent_reasoning` | Agent reasoning phases used for strategy extraction |
| `sessions` | Session metadata including project_id |

**Note:** The `consumption_scope` table has columns: `scope_id`, `session_id`, `group_id`, `agent_type`, `iteration`, `package_id`, `consumed_at`. Step 5b uses this for tracking delivery per session/group/agent/iteration to enable fresh context on retries.

**Note:** The `strategies` table is populated by Step 7 when tasks complete successfully. Strategies are queried during context assembly to provide insights from past successful implementations.

---

## Performance (SC-005)

**Target:** Context assembly must complete in <500ms.

**Estimated Performance:**

| Step | Operation | Time |
|------|-----------|------|
| Parse input | Step 1 | <5ms |
| Token zone detection | Step 2 | <5ms |
| Query packages | Step 3 (indexed) | 30-50ms |
| Token packing | Step 3c | 20-50ms |
| Query error patterns | Step 4 (indexed) | 30-50ms |
| Format output | Step 5 | <10ms |
| Mark consumption | Step 5b | 20-50ms |
| **Total** | | **~100-200ms** |

**Performance Prerequisites:**
- SQLite WAL mode enabled (concurrent reads)
- Indexes created on `context_packages`, `error_patterns`, `consumption_scope`
- Retry backoff (100ms, 200ms, 400ms) adds max 700ms only if database locked

**If performance degrades:**
1. Check `PRAGMA journal_mode` returns `wal`
2. Verify indexes exist: `SELECT name FROM sqlite_master WHERE type='index'`
3. Check for lock contention in parallel agent spawns

---

## References

See `references/usage.md` for detailed usage documentation and integration examples.
