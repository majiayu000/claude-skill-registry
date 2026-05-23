---
name: agent-architecture-planner
description: "Use when designing an autonomous agent, planning agent architecture, building a scheduled automation, or creating a Claude Code agent workflow. Triggers: 'design an agent', 'build an automation', 'agent architecture', 'automate this workflow', 'create a scheduled agent', 'shell script agent'."
version: 1.0.0
---

# Agent Architecture Planner

Design autonomous agents using the "Shell Orchestrates, Claude Thinks" pattern. This skill takes a workflow description, selects the right architecture pattern, and produces a complete agent package: shell wrapper, system prompt, config, scheduling setup, and cost estimate.

The core principle: **the shell handles everything deterministic** (API calls, file I/O, scheduling, budget tracking), and **Claude handles everything that requires judgment** (scoring, filtering, writing, categorizing). This separation makes agents cheaper, more reliable, and easier to debug.

---

## Tools Used

| Tool | Purpose |
|---|---|
| `Read` | Check for existing agent docs, load reference files |
| `Write` | Output all agent architecture files |
| `Bash` | Make shell scripts executable, verify directory structure |
| `Glob` | Check for existing agents to avoid naming conflicts |

---

## Methodology

Follow these steps in order. Do not skip steps. Do not produce output files before completing the discovery interview and confirming the architecture with the user.

---

### Step 1 — Workflow Discovery (Interactive)

Present these questions to the user **all at once** in a numbered list. Tell the user they can answer inline or paste a block of text.

Ask exactly these questions:

```
I need to understand the workflow before designing the agent. Answer these 6 questions — be as specific as possible.

1. What task do you want to automate? (Describe the manual workflow as you do it today, step by step.)
2. How often should it run? (Every hour, daily, every 2 days, weekly, on-demand only?)
3. What data sources does it need? (APIs, websites to scrape, databases, local files, RSS feeds?)
4. What should it produce? (Report files, database entries, API calls, Slack messages, emails, CSV exports?)
5. What decisions does it need to make? (Scoring relevance, filtering noise, writing content, categorizing items, choosing actions?)
6. What's your budget constraint? (Max cost per run in dollars, or monthly ceiling. Include both API/data costs and LLM costs if you know them.)
```

**Rules for this step:**
- Wait for the user to respond before proceeding. Do NOT generate placeholder answers.
- If question 1 is vague (less than 3 concrete steps described), ask a focused follow-up: _"Walk me through the last time you did this manually. What did you open first? What did you check? What did you produce at the end?"_
- If question 3 mentions an API, ask: _"Does this API require authentication? What format does it return (JSON, XML, CSV)? Is there a rate limit?"_
- At most 2 follow-up rounds before proceeding.

---

### Step 2 — Architecture Pattern Selection

Based on the user's answers, recommend **one** of these four patterns. Present the recommended pattern and briefly explain why it fits. If two patterns are close, present both and let the user choose.

---

#### Pattern A: Simple Pipeline

```
Shell (acquire data) → JSON temp file → Claude (analyze + act) → Output
```

**Best for:** Single data source, single output. The most common pattern. Use this when the workflow is: get data, think about it, produce something.

**Examples:** Daily report generation, email draft writing from CRM data, log analysis, document summarization.

**When to use:**
- One data source (or multiple sources that can be merged trivially)
- No feedback loop needed
- Output is a single artifact (file, database push, message)

---

#### Pattern B: Dual-Layer Pipeline

```
Shell → Layer 1 (broad collection) → Layer 2 (targeted search) → Merge + Dedup → Claude (analyze + act) → Output
```

**Best for:** Monitoring and discovery workflows where comprehensive coverage matters. Layer 1 casts a wide net (e.g., scrape all new posts from 20 sources). Layer 2 does targeted searches for specific keywords or patterns. Results are merged and deduplicated before Claude sees them.

**Examples:** Social media monitoring, job posting tracking, competitor mention detection, market signal scanning.

**When to use:**
- You need to catch everything (missing a relevant item is costly)
- Data comes from overlapping sources that produce duplicates
- The volume of raw data is high but only 5-20% is relevant

---

#### Pattern C: Multi-Agent Decomposition

```
Orchestrator Shell → [Agent 1: Research] → [Agent 2: Analysis] → [Agent 3: Writing] → Merge → Output
```

**Best for:** Complex workflows where different steps need fundamentally different expertise or prompting strategies. Each sub-agent has its own system prompt optimized for its specific task.

**Examples:** Content production pipelines (research → outline → draft → edit), multi-step analysis (collect data → score → generate recommendations → format report), workflows where one step's output determines the next step's approach.

**When to use:**
- A single system prompt cannot cover all the judgment needed
- The workflow has 3+ distinct phases that require different thinking
- You need to be able to debug or improve each phase independently

---

#### Pattern D: Feedback Loop

```
Shell → Collect → Claude (score + filter) → Act → Log results → [wait] → Shell reads logs → Collect → Claude (score with history) → ...
```

**Best for:** Ongoing optimization workflows where each run should learn from previous runs. The shell maintains a log of past decisions and outcomes, and feeds them back to Claude as context on subsequent runs.

**Examples:** A/B testing content strategies, lead scoring with win/loss feedback, adaptive outreach sequences, quality improvement loops.

**When to use:**
- Performance should improve over time
- You have a feedback signal (open rates, conversion, engagement, human ratings)
- The agent runs repeatedly on similar data

---

**Present your recommendation to the user:**

_"Based on your workflow, I recommend **Pattern {X}: {Name}**. Here's why: {1-2 sentence justification}. Does this feel right, or should we look at an alternative?"_

Wait for confirmation before proceeding.

---

### Step 3 — Component Design

For the confirmed pattern, design each of the four components below. Present the designs to the user as you go. Do not write files yet — this step is about design, not output.

---

#### 3A: Shell Wrapper Design

The shell wrapper is the backbone. It handles everything deterministic. Design it with these sections:

**Environment Setup**
- Source API keys from environment variables (never hardcode secrets)
- Define paths (log directory, temp directory, prompt file, config file)
- Create directories if they don't exist
- Set timestamp for the current run

**Gate Check (prevents double-runs)**
```bash
GATE_FILE="logs/${AGENT_NAME}_last_run.txt"
MIN_HOURS_BETWEEN_RUNS=44  # adjust per agent

if [ -f "$GATE_FILE" ]; then
    last_run=$(cat "$GATE_FILE")
    now=$(date +%s)
    hours_since=$(( (now - last_run) / 3600 ))
    if [ "$hours_since" -lt "$MIN_HOURS_BETWEEN_RUNS" ]; then
        echo "Gate check: only ${hours_since}h since last run (min: ${MIN_HOURS_BETWEEN_RUNS}h). Skipping."
        exit 0
    fi
fi
```

**Data Acquisition**
- API calls using `curl` with error handling
- Write raw responses to temp files (NEVER store API responses in shell variables — they often contain unescaped control characters that break the shell)
- Validate that the response is not empty or an error

**Data Preprocessing**
- Strip JSON to essential fields before sending to Claude. This is the single biggest cost optimization. Example: a raw API response might be 12KB per item. After stripping to the 8-10 fields Claude actually needs, it drops to ~750 bytes per item — a 94% reduction in input tokens.
- Use a small Python or jq script to do the stripping. Write the stripped data to a new temp file.

**Claude Invocation**
- Pipe the prompt file to Claude: `cat "$PROMPT_FILE" | claude -p --model {model} --max-turns {turns} --allowedTools {tools}`
- NEVER use `claude -p "$(cat ...)"` — this hits shell ARG_MAX limits with large prompts (150+ items)
- Pass the scraped data path as a section in the prompt file, or prepend it to the prompt

**Budget Tracking**
```bash
SPEND_LOG="logs/apify_spend_${AGENT_NAME}.json"
# After each API call, log the cost
# Between batches, check cumulative spend against the daily cap
```

**Logging and Cleanup**
- Log start time, end time, items processed, items passed to Claude, and estimated cost
- Update the gate file with the current timestamp
- Clean up temp files

**Error Handling**
- If the API call fails (non-200 status), log the error and exit with a non-zero code
- If Claude returns an error, log it and exit
- If the data is empty (nothing to process), log "no data" and exit cleanly (code 0)

Present the shell wrapper design as a bulleted outline. Ask the user if any sections need adjustment.

---

#### 3B: System Prompt Design

The system prompt follows a strict structure. Design it section by section:

**1. Role Definition**
One paragraph. Who is this agent? What does it do? What does it NOT do? Set boundaries.

Example structure:
> You are a {role description}. Your job is to {primary task}. You receive {input description} and produce {output description}. You do NOT {explicit boundary — e.g., "write final copy", "make API calls", "access external systems"}.

**2. Context Section**
Describe what data the agent receives and in what format. This is where you document the pre-processed data structure so Claude knows what to expect.

Example structure:
> ## Input Data
> You receive a JSON array of items. Each item has these fields:
> - `title` (string): ...
> - `url` (string): ...
> - `score` (number): ...
> {list every field the stripped JSON contains}

**3. Task Steps**
Numbered, specific, unambiguous steps. Each step should be one action. No compound steps.

Rules for writing task steps:
- Start each step with a verb
- Include the decision criteria inline (e.g., "Score each item from 1-10 based on: relevance to {topic} (0-3), recency (0-3), engagement (0-2), authority (0-2)")
- Specify what to do with items that fail the filter (skip silently, log, or flag)
- Reference tool names explicitly if the agent uses MCP tools or file I/O

**4. Output Format**
Specify exactly what the agent should produce. Include a template or schema. If the output goes to a database, specify the column names and data types. If it's a file, specify the format.

**5. Rules and Constraints**
Numbered list of non-negotiable rules. These are the guardrails. Common rules:
- Never fabricate data
- Never exceed {N} output items per run
- Always deduplicate against {source} before writing
- If unsure about a classification, choose {default}
- Never mention {brand/product} directly in {context}

**6. Example Output**
One complete, realistic example of the agent's output. Not abbreviated. The full thing, including edge cases. This is the single most effective way to steer Claude's behavior.

Present the system prompt outline (section summaries, not the full text yet) and ask the user to confirm the scope and constraints.

---

#### 3C: Config File Design

Design the YAML configuration file. This file makes the agent portable and tunable without editing code.

```yaml
agent:
  name: [agent-name]            # lowercase, hyphens, no spaces
  type: [pipeline|dual-layer|multi-agent|feedback-loop]
  schedule: [description]       # e.g., "Mon-Fri 09:00" or "every 2 days"
  model: [claude-sonnet-4-6|claude-opus-4-6]
  max_turns: [number]           # how many tool-use turns Claude gets
  allowed_tools: []             # list of MCP tools or built-in tools

data_sources:
  - name: [source-name]
    type: [api|scrape|file|database]
    endpoint: [URL or path]
    auth_env_var: [env var name] # e.g., APIFY_TOKEN
    rate_limit: [requests/min]
    fields_to_keep: []          # list of fields to preserve after stripping
    max_items: [number]         # cap per source

budget:
  max_per_run: [dollar amount]  # total budget ceiling per execution
  tracking_file: [path]         # e.g., logs/spend_{agent-name}.json
  alert_threshold: [percentage] # warn when spend hits this % of max

output:
  type: [file|database|api|notification]
  destination: [path or endpoint]
  format: [markdown|json|csv]
  max_output_items: [number]    # cap on items produced per run

filters:
  min_score: [number]           # minimum relevance score to include
  max_age_hours: [number]       # ignore items older than this
  dedup_field: [field name]     # field to use for deduplication
  dedup_source: [path or DB]   # where to check for existing items

schedule:
  type: [launchd|cron|manual]
  weekdays_only: [true|false]
  min_hours_between_runs: [number]  # gate mechanism
  timezone: [timezone string]       # e.g., "America/New_York"
```

Present the proposed config values to the user and ask for adjustments.

---

#### 3D: Scheduling Design

Based on the user's OS and schedule requirements, design the scheduling configuration.

**For macOS (launchd):**

Generate a `.plist` file:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.{org}.{agent-name}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/run_{agent-name}.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <array>
        <!-- Weekday-only example: Monday through Friday -->
        <dict>
            <key>Weekday</key><integer>1</integer>
            <key>Hour</key><integer>9</integer>
            <key>Minute</key><integer>0</integer>
        </dict>
        <!-- Repeat for each weekday as needed -->
    </array>
    <key>StandardOutPath</key>
    <string>/path/to/logs/{agent-name}.stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/logs/{agent-name}.stderr.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
```

**Important macOS note:** If the agent needs to access files in `~/Desktop/` or `~/Documents/`, macOS TCC (Transparency, Consent, and Control) will block launchd-spawned processes. The fix is to use a compiled C launcher binary that has been granted Full Disk Access in System Settings. The launcher simply `execv()`s the real shell script, and FDA propagates to the child process.

**For Linux (cron):**

Generate a crontab entry:

```
# {agent-name} — runs Mon-Fri at 09:00
0 9 * * 1-5 /path/to/run_{agent-name}.sh >> /path/to/logs/{agent-name}.cron.log 2>&1
```

**Gate mechanism (both platforms):**
The schedule triggers the script, but the script's own gate check (Step 3A) decides whether to actually run. This means the schedule can fire daily, but the gate ensures minimum spacing between actual executions. This is simpler and more reliable than trying to encode complex scheduling logic in cron or launchd.

---

### Step 4 — Cost Estimation

Calculate the estimated cost per run and monthly projection. Present this as a table.

**Token Estimation:**

| Component | Calculation |
|---|---|
| System prompt | Word count x 1.3 = input tokens |
| Input data | Items x avg bytes per item x 0.25 = input tokens (1 token ~ 4 bytes for English) |
| Output | Expected output items x avg words per item x 1.3 = output tokens |

**Claude API Pricing (current as of 2026):**

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|---|---|---|
| claude-sonnet-4-6 | $3.00 | $15.00 |
| claude-opus-4-6 | $15.00 | $75.00 |

**Cost Per Run:**

| Line Item | Estimate |
|---|---|
| Data source API costs | $ {based on user's APIs} |
| Claude input tokens | $ {system prompt + data} |
| Claude output tokens | $ {expected output} |
| **Total per run** | **$ {sum}** |
| **Monthly projection** | **$ {total x runs per month}** |

**Present the estimate and ask:** _"Does this monthly cost work for your budget? If not, we can reduce cost by: (1) switching to Sonnet, (2) stripping more fields from the input data, (3) reducing the number of items per run, or (4) running less frequently."_

---

### Step 5 — Data Optimization Tips

Before writing files, present these optimization patterns. Highlight which ones are relevant to the user's specific agent.

**1. JSON Stripping (always relevant)**
Remove unnecessary fields from API responses before sending to Claude. This is the single biggest lever for reducing cost. Write a small preprocessing script that keeps only the fields Claude needs.

Example: Raw Reddit post from the API might include 40+ fields (user flair, CSS classes, award data, etc.). The agent only needs: `title`, `url`, `subreddit`, `score`, `num_comments`, `created_utc`, `selftext` (truncated to 500 chars), `author`. That's 8 fields instead of 40+.

**2. Prompt Piping (relevant when data volume > 50 items)**
For large prompts, pipe the prompt file to Claude instead of passing it as a command-line argument:
```bash
# Correct — works with any prompt size
cat "$PROMPT_FILE" | claude -p

# Incorrect — breaks when prompt exceeds shell ARG_MAX (~262KB on most systems)
claude -p "$(cat "$PROMPT_FILE")"
```

**3. Shell-Side Deduplication (relevant when data has overlapping sources)**
Dedup before Claude sees the data. It's cheaper to deduplicate 500 items in a shell script (free) than to ask Claude to deduplicate 500 items (costs tokens). Use URL or unique ID as the dedup key. Compare against a local log of previously processed items.

**4. Batch Processing with Budget Checks (relevant when processing > 100 items)**
If the agent processes many items, batch them in groups (e.g., 5 API calls at a time) and check cumulative spend between batches. Stop when the budget cap is hit. This prevents runaway costs if an API returns unexpectedly large volumes.

**5. Temp Files for API Responses (always relevant)**
Always write API responses to temp files, never to shell variables. API responses often contain unescaped control characters (`\n`, `\t`, `\r`, null bytes) that corrupt shell variables and cause silent data loss. Temp files are immune to this.

```bash
# Correct
curl -s "$API_URL" > "$TMPDIR/raw_response.json"
python3 strip_fields.py "$TMPDIR/raw_response.json" > "$TMPDIR/stripped.json"

# Incorrect — will break on special characters
RESPONSE=$(curl -s "$API_URL")
echo "$RESPONSE" | python3 strip_fields.py
```

**6. Rotation for Large Source Lists (relevant when monitoring 10+ sources)**
If the agent monitors many sources (e.g., 20 subreddits), don't hit all of them every run. Rotate through subsets (e.g., 5 per run, cycling through all 20 over 4 runs). Track rotation state in a JSON file. This reduces per-run cost and avoids rate limits.

---

### Step 6 — Output

After the user has confirmed all designs, write the following files. Use `Write` for each file. Use `Bash` to make the shell script executable.

Write all files to `docs/agents/{agent-name}/`:

---

#### File 1: `architecture.md`

```markdown
# {Agent Name} — Architecture

> Generated by Agent Architecture Planner v1.0.0 | {YYYY-MM-DD}

## Pattern: {Pattern Name}

{ASCII diagram of the data flow}

## Components

| Component | File | Purpose |
|---|---|---|
| Shell Wrapper | `run.sh` | {one-line description} |
| System Prompt | `prompt.md` | {one-line description} |
| Configuration | `config.yaml` | {one-line description} |
| Schedule | `schedule.plist` or `crontab.txt` | {one-line description} |

## Data Flow

1. {Step 1 description}
2. {Step 2 description}
...

## Cost Estimate

| Line Item | Per Run | Monthly ({N} runs) |
|---|---|---|
| Data source costs | ${X} | ${Y} |
| Claude API (input) | ${X} | ${Y} |
| Claude API (output) | ${X} | ${Y} |
| **Total** | **${X}** | **${Y}** |

## Key Design Decisions

- {Decision 1 and rationale}
- {Decision 2 and rationale}
- {Decision 3 and rationale}
```

---

#### File 2: `run.sh`

Write a **functional** shell script. Not pseudocode. It should run with minimal modifications (the user only needs to fill in API endpoints and paths). Include all sections from Step 3A.

Structure:
```bash
#!/usr/bin/env bash
set -euo pipefail

# ============================================================
# {Agent Name} — Shell Wrapper
# Pattern: {pattern name}
# Schedule: {schedule description}
# ============================================================

# --- Configuration ---
AGENT_NAME="{agent-name}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="${SCRIPT_DIR}/logs"
PROMPT_FILE="${SCRIPT_DIR}/prompt.md"
CONFIG_FILE="${SCRIPT_DIR}/config.yaml"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$LOG_DIR"

# --- Logging ---
LOG_FILE="${LOG_DIR}/${AGENT_NAME}_${TIMESTAMP}.log"
exec > >(tee -a "$LOG_FILE") 2>&1
echo "=== ${AGENT_NAME} starting at $(date) ==="

# --- Gate Check ---
GATE_FILE="${LOG_DIR}/${AGENT_NAME}_last_run.txt"
MIN_HOURS={min_hours_between_runs}

if [ -f "$GATE_FILE" ]; then
    last_run=$(cat "$GATE_FILE")
    now=$(date +%s)
    hours_since=$(( (now - last_run) / 3600 ))
    if [ "$hours_since" -lt "$MIN_HOURS" ]; then
        echo "Gate: ${hours_since}h since last run (min: ${MIN_HOURS}h). Skipping."
        exit 0
    fi
fi

# --- Data Acquisition ---
RAW_FILE=$(mktemp "${TMPDIR}/${AGENT_NAME}_raw_XXXXXX.json")
STRIPPED_FILE=$(mktemp "${TMPDIR}/${AGENT_NAME}_stripped_XXXXXX.json")

# {API call — customize per data source}
HTTP_STATUS=$(curl -s -o "$RAW_FILE" -w "%{http_code}" \
    -H "Authorization: Bearer ${API_TOKEN}" \
    "{API_ENDPOINT}")

if [ "$HTTP_STATUS" -ne 200 ]; then
    echo "ERROR: API returned HTTP ${HTTP_STATUS}"
    cat "$RAW_FILE"
    rm -f "$RAW_FILE" "$STRIPPED_FILE"
    exit 1
fi

# Check for empty response
if [ ! -s "$RAW_FILE" ]; then
    echo "No data returned. Nothing to process."
    rm -f "$RAW_FILE" "$STRIPPED_FILE"
    date +%s > "$GATE_FILE"
    exit 0
fi

# --- Data Preprocessing (strip to essential fields) ---
python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    data = json.load(f)
# Customize: keep only the fields Claude needs
stripped = [{k: item.get(k) for k in ['{field1}', '{field2}', '{field3}']} for item in data]
with open(sys.argv[2], 'w') as f:
    json.dump(stripped, f)
print(f'Stripped {len(data)} items to {len(stripped)} items, kept essential fields only.')
" "$RAW_FILE" "$STRIPPED_FILE"

ITEM_COUNT=$(python3 -c "import json; print(len(json.load(open('$STRIPPED_FILE'))))")
echo "Items to process: ${ITEM_COUNT}"

# --- Build Prompt ---
FULL_PROMPT=$(mktemp "${TMPDIR}/${AGENT_NAME}_prompt_XXXXXX.md")
{
    cat "$PROMPT_FILE"
    echo ""
    echo "## Pre-Scraped Data"
    echo '```json'
    cat "$STRIPPED_FILE"
    echo '```'
} > "$FULL_PROMPT"

# --- Claude Invocation ---
echo "Invoking Claude..."
cat "$FULL_PROMPT" | claude -p \
    --model {model} \
    --max-turns {max_turns} \
    --allowedTools {tools}

CLAUDE_EXIT=$?
if [ "$CLAUDE_EXIT" -ne 0 ]; then
    echo "ERROR: Claude exited with code ${CLAUDE_EXIT}"
    rm -f "$RAW_FILE" "$STRIPPED_FILE" "$FULL_PROMPT"
    exit 1
fi

# --- Budget Tracking ---
SPEND_LOG="${LOG_DIR}/spend_${AGENT_NAME}.json"
# {Append this run's estimated cost to the spend log}
# {Check cumulative spend against daily/monthly cap}

# --- Cleanup ---
rm -f "$RAW_FILE" "$STRIPPED_FILE" "$FULL_PROMPT"
date +%s > "$GATE_FILE"
echo "=== ${AGENT_NAME} completed at $(date) ==="
```

**This script must be functional.** Replace `{placeholders}` with sensible defaults based on the user's answers. Add comments explaining what the user needs to customize.

---

#### File 3: `prompt.md`

Write the complete system prompt following the structure from Step 3B. All six sections: Role, Context, Steps, Output Format, Rules, Example. The example output must be complete and realistic.

---

#### File 4: `config.yaml`

Write the complete config file following the schema from Step 3C. Fill in all values based on the user's answers and confirmed designs.

---

#### File 5: `schedule.plist` (macOS) or `crontab.txt` (Linux)

Write the scheduling configuration based on the user's OS and schedule requirements. Include the weekday-only restriction if specified. Add comments explaining how to install it.

For macOS launchd, include installation instructions as comments at the top:
```xml
<!--
  Installation:
  1. Copy this file to ~/Library/LaunchAgents/
  2. Load: launchctl load ~/Library/LaunchAgents/{filename}.plist
  3. Verify: launchctl list | grep {agent-name}

  Uninstall:
  1. Unload: launchctl unload ~/Library/LaunchAgents/{filename}.plist
  2. Delete the plist file

  Note: If the script needs access to ~/Desktop/ or ~/Documents/,
  you'll need a launcher binary with Full Disk Access. See architecture.md.
-->
```

---

#### File 6: `README.md`

Write a setup guide:

```markdown
# {Agent Name}

{One-sentence description.}

## Prerequisites

- {List runtime dependencies: bash, python3, jq, claude CLI, etc.}
- {List API keys needed and how to set them as env vars}
- {List any MCP servers or tools required}

## Quick Start

1. Clone this directory
2. Set environment variables:
   ```bash
   export API_TOKEN="your-token-here"
   ```
3. Make the script executable:
   ```bash
   chmod +x run.sh
   ```
4. Test with a manual run:
   ```bash
   ./run.sh
   ```
5. Check the output in {output location}
6. If it looks good, install the schedule:
   ```bash
   {installation command}
   ```

## Files

| File | Purpose |
|---|---|
| `run.sh` | Shell wrapper — orchestrates the entire pipeline |
| `prompt.md` | System prompt — defines what Claude does |
| `config.yaml` | Configuration — all tunable parameters |
| `schedule.plist` / `crontab.txt` | Scheduling — when and how often to run |
| `architecture.md` | Architecture doc — pattern, data flow, cost estimate |
| `logs/` | Created on first run — stores run logs, spend tracking, gate files |

## Customization

### Changing the schedule
Edit `schedule.plist` (macOS) or `crontab.txt` (Linux). Reload after editing.

### Adjusting the budget
Edit `config.yaml` → `budget.max_per_run`. The shell script checks this between batches.

### Adding data sources
1. Add the source to `config.yaml` → `data_sources`
2. Add the API call to `run.sh` (follow the existing pattern)
3. Update `prompt.md` → Context section to describe the new data format

### Changing what Claude does
Edit `prompt.md`. The shell script does not need to change unless you're adding new tools.

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Script exits immediately with "Gate check" | Ran too recently | Wait for the gate period to pass, or delete the gate file in `logs/` |
| "ERROR: API returned HTTP 401" | Bad or expired API token | Check the env var is set correctly |
| "ERROR: API returned HTTP 429" | Rate limited | Reduce `rate_limit` in config, or add a `sleep` between API calls |
| Claude produces no output | Prompt too large or malformed | Check `$TMPDIR` for the full prompt file and verify it's valid |
| Empty data after stripping | Wrong field names in the strip script | Check the raw API response format and update the field list |
```

---

### Post-Output Actions

After writing all files:

1. Run `chmod +x docs/agents/{agent-name}/run.sh` via Bash to make the script executable.
2. Use Glob to verify all 6 files were written.
3. Present a summary to the user:

```
Agent architecture written to docs/agents/{agent-name}/:

  - architecture.md  — pattern diagram and cost estimate
  - run.sh           — shell wrapper (executable)
  - prompt.md        — system prompt
  - config.yaml      — configuration
  - schedule.plist    — macOS scheduling
  - README.md        — setup guide

Pattern: {name}
Estimated cost: ${X}/run, ${Y}/month
Schedule: {description}

Next step: Set your API keys as environment variables, then run ./run.sh to test.
```

4. Ask if they want to adjust anything before testing.

---

## Rules (Non-Negotiable)

1. **Interactive first, output second.** Never skip the workflow discovery. Never design an agent from assumptions alone.
2. **Shell scripts must be functional.** Not pseudocode, not skeleton code. The script should run with only API endpoints and paths filled in. Include actual error handling, actual temp file management, actual gate checks.
3. **System prompts follow the 6-section structure.** Role, Context, Steps, Output Format, Rules, Example. No exceptions. The example must be complete and realistic.
4. **Always include budget tracking.** Even for hobby projects or free APIs, the Claude API costs money. Track it.
5. **Always strip JSON to essential fields.** This is not optional. Raw API responses are 5-20x larger than what Claude needs. Stripping is the single highest-leverage cost optimization.
6. **Always use temp files for API responses.** Never store API data in shell variables. Special characters in API responses corrupt shell variables silently.
7. **Always include a gate mechanism.** Prevent accidental double-runs from crashing budgets or creating duplicate outputs.
8. **Pipe prompts, don't pass them as arguments.** Use `cat "$PROMPT_FILE" | claude -p`, not `claude -p "$(cat ...)"`. The latter breaks at ~262KB.
9. **Get user confirmation at each milestone.** Confirm the pattern (Step 2), the component designs (Step 3), and the cost estimate (Step 4) before writing files.
10. **No proprietary references.** This skill is public. Do not reference internal company tools, client names, vendor-specific actor IDs, internal databases, or private infrastructure. All patterns are generic best practices.
