---
name: thoughtful-commitment
description: "Git commits that capture context and intent"
license: MIT
tier: 2
allowed-tools: [read_file, write_file, list_dir, run_terminal_cmd, grep]
protocol: THOUGHTFUL-COMMITMENT
related: [cursor-mirror, session-log, plain-text, yaml-jazz, git-workflow]
tags: [git, commits, provenance, introspection]
---

# Thoughtful Commitment

> *Commits that capture context, not just changes.*

## Purpose

Git commits with traceability:
- What changed (git diff)
- Why it changed (cursor-mirror thinking)
- Who asked for it (user request)
- Session link for full context

## The Core Insight

Git and cursor-mirror are **two introspection systems** that mesh via commit IDs:

```
Git:           "What changed?"  →  abc123
Cursor-Mirror: "Why?"          →  events 140-148

Thoughtful Commitment: Links them together
```

## Protocol: THOUGHTFUL-COMMITMENT

### Commit Message Format

```
<type>: <summary> (imperative, <50 chars)

<narrative>
What happened, from whose perspective, and why it matters.
Focus on intent and motivation, not just mechanics.

<changes>
- Bullet list of mechanical changes
- For quick scanning

<thinking-ref>
Thinking: cursor-mirror://<composer>/<event-range>
```

### Types

| Type | Use |
|------|-----|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `refactor` | Code restructuring (no behavior change) |
| `docs` | Documentation only |
| `style` | Formatting (no code change) |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks |
| *narrative* | Story beat, character change, world evolution |

For MOOLLM narratives, the type can be the story beat:

```
Incarnation Ceremony: Kittens receive emoji souls
Midnight Prowl: Cats explore the moonlit garden
Cat Council: Biscuit accepted into family
```

### Context Gathering

Before writing commits or PRs, gather existing messages to match style and avoid repetition:

```bash
# Recent commit messages (style reference)
git log --oneline -20
git log origin/main..HEAD --format='%s%n%b%n---'

# PR descriptions
gh pr view --json title,body
gh pr list --state merged -L 10 --json number,title

# Combined context
git log origin/main..HEAD --oneline && \
git diff origin/main --stat | tail -5
```

See `examples/git-commands.yml` → `context_gathering` for complete reference.

## Method Specifications

---

## Primary Introspection — Start Here

These are the entry points. Get the timeline, then drill down.

### TIMELINE

**The master view.** Shows all events with timestamps, types, and IDs.

**Input:**
```yaml
method: TIMELINE
parameters:
  composer: string     # Composer ID (@1, name fragment, hash)
  limit: int           # How many events (default: 50)
  filter: string       # Event type filter (thinking, tool, user, all)
  since: string        # Time filter ("1 hour ago", event ID)
```

**Process:**
```bash
cursor-mirror timeline <composer> --limit <n>
```

**Output:**
```
🤔💭 ⏱️ Session Timeline — e8587ace

#141  16:46:12  📍 user      "Refactor auth module"
#142  16:46:15  🪟 context   3 files, ~4.2k tokens
#143  16:46:18  🧠 thinking  "Need to check for race conditions..."
#144  16:46:22  🔧 tool      Read auth/session.ts
#145  16:46:25  📤 result    247 lines loaded
#146  16:46:30  🧠 thinking  "Found race condition on line 47..."
#147  16:46:35  💡 insight   "Adding await fixes sequencing"
#148  16:46:40  🔧 tool      Write auth/session.ts
#149  16:46:45  📝 change    +3 -1 lines

→ Drill down: CONTEXT-FOCUS #142 | THINKING #143 | TOOLS #144
```

**Drill-down commands:**
- `CONTEXT-FOCUS #142` — What went into context at that point?
- `THINKING #143` — Full text of that thinking block
- `TOOLS #144-148` — Tool calls in that range
- `EXPLAIN #149` — Why was that change made?

The timeline is the **map**. Everything else is **zooming in**.

---

### CONTEXT-FOCUS

Analyze what went into the context window for a specific call. Shows the cursor state — what files, snippets, conversation, and rules were assembled.

**Input:**
```yaml
method: CONTEXT-FOCUS
parameters:
  composer: string     # Composer ID
  event_id: string     # Optional: specific event (default: latest)
```

**Process:**
```bash
# Get context sources for a composer
cursor-mirror context-sources <composer>

# Analyze what was in context at a specific event
cursor-mirror timeline <composer> --before <event_id> --type context
```

**Output:**
```
🤔💭 🪟 Context Window Analysis — event #142

Files read into context:
  auth/session.ts      247 lines   ████████████░░░░  58%
  auth/types.ts         89 lines   ████░░░░░░░░░░░░  21%
  tests/auth.test.ts   156 lines   ██████░░░░░░░░░░  37%

Snippets:
  session.ts:45-67 (highlighted by user)
  
Conversation turns: 12
Rules loaded: .cursorrules, workspace rules

Estimated tokens: ~4,200

Focus: auth module, session handling
```

The 🪟 tag marks context window analysis — showing what the LLM "saw" for this call.

---

### THINKING

Show reasoning blocks for an event or range.

**Input:**
```yaml
method: THINKING
parameters:
  composer: string
  event_id: string     # Specific event
  range: string        # Or range like "143-146"
```

**Process:**
```bash
cursor-mirror thinking <composer> --event <id>
```

**Output:**
```
🤔💭 🧠 Thinking Block #143

"I need to understand the current structure of the auth module before 
making changes. Let me read the session handling code first.

The user mentioned a race condition — I should look for any async 
operations that might not be properly awaited. Common patterns to 
check: cookie operations, token refresh, database calls..."

(247 chars, 16:46:18)
```

---

### TOOLS

Show tool calls for an event or session.

**Input:**
```yaml
method: TOOLS
parameters:
  composer: string
  event_id: string     # Specific event, or omit for all
  tool_filter: string  # Filter by tool name (Read, Write, Shell, etc.)
```

**Process:**
```bash
cursor-mirror tools <composer>
cursor-mirror tools <composer> --filter Read
```

**Output:**
```
🤔💭 🔧 Tool Calls — session e8587ace

#144  Read     auth/session.ts           247 lines
#148  Write    auth/session.ts           +3 -1
#150  Read     auth/types.ts              89 lines
#152  Shell    git diff --staged         +3 -1 lines
#153  Write    tests/auth.test.ts        +45 new

Distribution: Read 42% | Write 28% | Shell 18% | Grep 12%
```

---

## Commit Operations

### COMMIT

Create a thoughtful commit.

**Input:**
```yaml
method: COMMIT
parameters:
  files: [string]          # Files to commit (or '.' for all)
  summary: string          # What changed (auto-detect if omitted)
  include_thinking: bool   # Link to cursor-mirror (default: true)
  style: enum              # technical (default) | changelog | pr | burke
```

**Styles:**
| Style | Use | Output |
|-------|-----|--------|
| `technical` | **Default.** Concise, factual | `fix: race condition in auth` + bullets |
| `changelog` | Release notes | User-facing changes grouped by type |
| `pr` | Pull request body | Summary, changes, test plan |
| `burke` | James Burke storytelling | Facet-to-facet connections, disco ball |

**Process:**
1. Stage specified files (`git add`)
2. Gather context from conversation
3. If `include_thinking`, query cursor-mirror for recent events
4. Generate commit message per protocol
5. Create commit (`git commit -m "..."`)
6. Return commit ID and message

**Output:**
```yaml
commit_id: "abc123"
message: "Full commit message..."
thinking_link: "cursor-mirror://def456/events/140-148"
```

### EXPLAIN

Find the thinking that led to an existing commit.

**Input:**
```yaml
method: EXPLAIN
parameters:
  commit: string           # Commit hash (full or abbreviated)
```

**Process:**
1. Get commit details (`git show --format=...`)
2. Extract timestamp
3. Search cursor-mirror for events around that time
4. Find the git commit tool call
5. Trace back to thinking blocks and user request

**Output:**
```yaml
commit_message: "Incarnation Ceremony: ..."
timestamp: "2026-01-15T19:30:00Z"
author: "Coherence Engine"
user_request: "Incarnate the kittens with emoji souls"
thinking_blocks:
  - event_id: 141
    content: "I need to invoke INCARNATION protocol..."
  - event_id: 142
    content: "Myrcene's terpene is sedating..."
tool_calls:
  - event_id: 144
    tool: write_file
    args: {path: "kitten-myrcene/CHARACTER.yml"}
  - event_id: 148
    tool: git_commit
    args: {message: "..."}
```

### MESSAGE

Generate a commit message from current context.

**Input:**
```yaml
method: MESSAGE
parameters:
  diff_summary: string?    # Optional (auto-detect from staged)
  style: enum              # technical (default) | changelog | pr | burke
  detail: int              # 1-5 (default: 3)
```

**Process:**
1. If no diff_summary, run `git diff --staged --stat`
2. Analyze conversation context for intent
3. Generate message per perspective and protocol

**Output:**
```yaml
message: "Full commit message..."
sections:
  title: "Incarnation Ceremony: Kittens receive emoji souls"
  body: "The Cat Cave family gathered..."
  changes: ["Added emoji_identity...", "Added pronouns..."]
```

### LINK

Manually link a commit to cursor-mirror events.

**Input:**
```yaml
method: LINK
parameters:
  commit: string           # Commit hash
  events: [string]         # Event IDs from cursor-mirror
```

**Process:**
1. Validate commit exists
2. Validate events exist in cursor-mirror
3. Store link in `.moollm/skills/thoughtful-commitment/commit-links.yml`

**Output:**
```yaml
linked: true
reference: "cursor-mirror://abc123/events/140-148"
```

### HISTORY

Get narrative history of a file or directory.

**Input:**
```yaml
method: HISTORY
parameters:
  path: string             # File or directory
  depth: int               # Number of commits (default: 10)
  include_thinking: bool   # Include cursor-mirror links (default: true)
```

**Process:**
1. Get git log for path (`git log -n <depth> --format=... -- <path>`)
2. For each commit, attempt to find cursor-mirror link
3. Build narrative timeline

**Output:**
```yaml
timeline:
  - commit: "abc123"
    date: "2026-01-15"
    message: "Incarnation Ceremony: ..."
    thinking_link: "cursor-mirror://..."
    summary: "Kittens received emoji souls"
  - commit: "def456"
    date: "2026-01-14"
    message: "Initial character creation"
    thinking_link: null
    summary: "Created basic character files"
```

### DEEP-COMMIT

Technical analytics mining — extract quantitative metrics from cursor-mirror and git.

**When to use:**
- PR descriptions needing detailed appendices
- Post-mortem analysis of development sessions
- Documenting complex multi-hour sessions
- Generating reproducible verification commands

**Process:**

~~~bash
# 1. Raw metrics extraction
TRANSCRIPT="path/to/transcript.txt"
wc -l "$TRANSCRIPT"                           # line count
wc -c "$TRANSCRIPT"                           # byte count
grep -c "^\[Tool call\]" "$TRANSCRIPT"        # tool calls
grep -c "^\[Thinking\]" "$TRANSCRIPT"         # thinking blocks
grep -c "^user:" "$TRANSCRIPT"                # user turns

# 2. Tool distribution
grep "^\[Tool call\]" "$TRANSCRIPT" | cut -d' ' -f3 | sort | uniq -c | sort -rn

# 3. Thinking block analysis
grep "^\[Thinking\]" "$TRANSCRIPT" | while read l; do echo ${#l}; done | \
  sort -n | awk 'BEGIN{sum=0} {a[NR]=$1; sum+=$1} END{
    printf "Count: %d\nMin: %d\nMax: %d\nAvg: %.0f\nMedian: %d\n", 
           NR, a[1], a[NR], sum/NR, a[int(NR/2)]
  }'

# 4. Activity bursts
cursor-mirror timeline <composer> 2>&1 | \
  grep -E "^[0-9]{4}-" | cut -d: -f1-2 | uniq -c

# 5. Git commit metrics
git log --oneline <range>
git diff --numstat <range> | awk '{ins+=$1; del+=$2} END{print ins, del}'

# 6. Word frequency in thinking
grep "^\[Thinking\]" "$TRANSCRIPT" | tr '[:upper:]' '[:lower:]' | \
  tr -cs '[:alpha:]' '\n' | sort | uniq -c | sort -rn | head -20
~~~

**Input:**
~~~yaml
method: DEEP-COMMIT
parameters:
  composer: string       # Composer ID (@1, name fragment, hash)
  commit_range: string   # Git range (e.g., "f21d0d0^..085b94b")
~~~

**Output:**
~~~markdown
## Appendix: Technical Analytics — Session <composer>

### Raw Metrics
Transcript: 8,890 lines | 390.7 KB
Tool Calls: 85 total
Thinking:   74 blocks | 11.1 KB

### Tool Distribution
36x Shell
23x Read
11x StrReplace
...

### Activity Bursts (events/minute)
16:46  16 events  ████████████████
20:08  10 events  ██████████
20:22  12 events  ████████████

### Commit Metrics
| Commit | Files | +Lines | -Lines |
|--------|-------|--------|--------|
| f21d0d0 | 7 | 1,515 | 0 |
...

### Verification Commands
~~~bash
# Reproduce these metrics:
wc -l "$TRANSCRIPT"
grep -c "^\[Tool call\]" "$TRANSCRIPT"
...
~~~
~~~

**Example session e8587ace produced:**
- 8,890 transcript lines
- 85 tool calls (36 Shell, 23 Read, 11 StrReplace)
- 75 thinking blocks (avg 151 chars)
- 3 commits (+1,656 net lines)
- 4 files created (1,526 lines total)
- Activity burst at 20:22 (12 events/min during meta-commit)

## Implementation Notes

### Finding Cursor-Mirror Events for a Commit

```bash
# 1. Get commit timestamp
git show -s --format=%ci abc123
# 2026-01-15 19:30:00 -0800

# 2. Search cursor-mirror for events around that time
python3 cursor_mirror.py timeline <composer> --around "2026-01-15T19:30:00"

# 3. Find the git commit event
python3 cursor_mirror.py grep "git commit" --after "2026-01-15T19:00:00"

# 4. Trace back to preceding thinking blocks
python3 cursor_mirror.py thinking <composer> --before <commit-event-id>
```

### Storage of Links

Links are stored in `.moollm/skills/thoughtful-commitment/commit-links.yml`:

```yaml
# .moollm/skills/thoughtful-commitment/commit-links.yml
links:
  abc123:
    composer: def456
    events: [140, 141, 142, 143, 144, 145, 146, 147, 148]
    user_request: "Incarnate the kittens with emoji souls"
    timestamp: "2026-01-15T19:30:00Z"
    
  ghi789:
    composer: def456
    events: [200, 201, 202]
    user_request: "Fix the relationship field"
    timestamp: "2026-01-15T20:15:00Z"
```

### Cursor Shell Integration

In Cursor, the skill can be invoked via natural language:

```
User: "Commit these changes with a narrative message"

LLM: [Invokes COMMIT method, generates message, creates commit]

Output: Created commit abc123
  Incarnation Ceremony: Kittens receive emoji souls
  
  Linked to thinking: cursor-mirror://def456/events/140-148
```

Or explain an existing commit:

```
User: "Why did we set Myrcene's active to 0?"

LLM: [Invokes EXPLAIN, traces back through history]

Output: Found in commit abc123 (2026-01-15)
  
  Your request: "Incarnate the kittens with emoji souls"
  
  My reasoning: "Myrcene's terpene is sedating, so Active 
  should be 0. She's the Princess of Pillows — low energy
  is her whole identity."
```

## Dovetails With

### Sister Skills

| Skill | Relationship |
|-------|--------------|
| [cursor-mirror](../cursor-mirror/) | Source of thinking blocks |
| [session-log](../session-log/) | Logs can reference commits |
| [plain-text](../plain-text/) | Why text commits matter |
| [git-workflow](../git-workflow/) | Broader git patterns (planned) |

### Kernel Protocols

- `WHY-REQUIRED` — Tool calls explain themselves; commits should too
- `APPEND-ONLY` — Commit history is append-only by nature

---

## Reference: Detail Knob

Two axes: **style** (what kind of output) and **detail** (how verbose).

### Styles

| Style | Use | Default for |
|-------|-----|-------------|
| `technical` | **Default.** Factual, concise | git commits |
| `changelog` | User-facing release notes | CHANGELOG.md |
| `pr` | Pull request summary | GitHub PRs |
| `burke` | James Burke storytelling mode | Special occasions |

### Detail Levels

| Level | Name | Tokens | Example (technical style) |
|-------|------|--------|---------------------------|
| 1 | terse | ~10 | `fix: auth race condition` |
| 2 | brief | ~30 | Title + one sentence |
| 3 | standard | ~80 | Title + changes list |
| 4 | detailed | ~200 | Title + context + changes + session link |
| 5 | comprehensive | ~400+ | Full analysis + alternatives + metrics |

**Default:** `style: technical`, `detail: 3`

### Burke Mode

When `style: burke`, output jumps facet-to-facet like a James Burke *Connections* episode — making unexpected connections between changes. Use sparingly for big PRs or retrospectives.

---

## Reference: Emoji Palette

### Attribution
| Emoji | Meaning |
|-------|---------|
| 👤 | Human-written (place at top) |
| 🤖 | LLM-generated |
| 👤🤖 | Collaboration |
| 👁️ | Human-reviewed |

### Skill Signature
`🤔💭` — Thoughtful Commitment namespace anchor

### Section Markers
| Emoji | Section |
|-------|---------|
| ⏱️ | Timeline (master view, all events) |
| 📍 | Context (background, why we're here) |
| 🪟 | Context Window (what inputs were assembled) |
| 🧠 | Thinking |
| 🔧 | Tool call |
| 📤 | Tool result |
| 🔍 | Investigation |
| 💡 | Solution / Insight |
| 🔀 | Alternatives / Decision |
| 📝 | Changes |
| 📊 | Metrics |
| 🔗 | Session link |

### Output Structure
```
👤 User's prompt (head position, their words)
---
🤖🤔💭 LLM analysis (skill's voice)
```

### Thought Stream

Every line of reasoning prefixed with `🤔💭 <tag>`:

| Tag | Meaning | Example |
|-----|---------|---------|
| ⏱️ | Timeline | `🤔💭 ⏱️ Session e8587ace, 47 events` |
| 📍 | Prompt/context | `🤔💭 📍 User asked to refactor auth` |
| 🪟 | Context window | `🤔💭 🪟 Loaded 3 files, ~4k tokens` |
| 🧠 | Thinking | `🤔💭 🧠 Need to check for race conditions` |
| 🔧 | Tool call | `🤔💭 🔧 Read auth/session.ts` |
| 📤 | Tool result | `🤔💭 📤 Found race condition on line 47` |
| 💡 | Insight | `🤔💭 💡 Adding await fixes sequencing` |
| 🔀 | Decision | `🤔💭 🔀 Chose await over mutex (simpler)` |
| 📝 | Change | `🤔💭 📝 Modified auth/session.ts` |
| ⚠️ | Warning | `🤔💭 ⚠️ This might break legacy clients` |

**Example stream:**
```
🤔💭 📍 User asked to refactor the auth module
🤔💭 🧠 Need to understand current structure first
🤔💭 🔧 Read auth/session.ts
🤔💭 📤 Found race condition in line 47
🤔💭 🧠 The cookie check races with token refresh
🤔💭 💡 Adding await will fix the sequencing
🤔💭 🔀 Chose await over mutex (simpler, addresses root cause)
🤔💭 📝 Modified auth/session.ts
🤔💭 🧠 Should add a test for this edge case
🤔💭 🔧 Write auth/session.test.ts
🤔💭 📤 Test file created
🤔💭 💡 Ready to commit with full context
```

The stream shows the reasoning process — amazing and revealing.
Every thought is tagged. Every tool call visible. Fully transparent.

---

## Reference: Git Time Travel

### Archaeology Commands

```bash
# BLAME — Who wrote each line?
git blame <file>
git blame -L 10,20 <file>           # Specific range
git blame <commit>^ -- <file>       # Blame BEFORE a commit

# LOG — Trace evolution
git log --oneline <file>
git log -S 'pattern'                # Pickaxe: who added this?
git log --follow <file>             # Track through renames

# SHOW — Inspect any point
git show <commit>:<file>            # File at that moment
git show <commit> --stat            # What changed
```

### Planning Commands

```bash
# MERGE PLANNING
git log main..feature --oneline     # Commits to merge
git diff main...feature             # Changes to merge
git merge-base main feature         # Common ancestor

# CHERRY-PICK PLANNING
git cherry -v upstream branch       # What's not upstream?
git show <commit>                   # Inspect before picking
```

---

## Reference: Cursor-Mirror Integration

cursor-mirror provides 59 commands for introspection:

```bash
# Navigation
cursor-mirror tree                  # Browse workspaces
cursor-mirror tail --limit 20       # Recent activity

# Extraction
cursor-mirror timeline <composer>   # Full event stream
cursor-mirror thinking <composer>   # Reasoning blocks
cursor-mirror tools <composer>      # Tool call history

# Search
cursor-mirror tgrep 'pattern'       # Search transcripts
cursor-mirror sql --db <ref> 'query' # Direct SQL

# Analysis
cursor-mirror analyze <composer>    # Session statistics
```

---

## Reference: Shell Patterns

```bash
# Counting
wc -l file                          # Lines
grep -c 'pattern' file              # Matches

# Frequency
sort | uniq -c | sort -rn           # Histogram

# Extraction
grep -o 'pattern' file              # Matches only
awk '{print $1, $3}'                # Select columns

# Aggregation
awk '{sum+=$1} END{print sum}'      # Sum
```

---

## Reference: Trekify Integration

For privacy, compose with [trekify](../trekify/) to mask sensitive data:

```bash
trekify MASK-SESSION e8587ace -o masked.txt
```

| Sensitive | Trekified |
|-----------|-----------|
| API keys | Quantum entanglement tokens |
| Servers | Starbase {N} |
| Databases | Memory Core Alpha |

---

# Philosophy (The Rear End 🐕)

Where dogs sniff. The deep stuff.

## The Persistence Insight

> *"All those moments will be lost in time, like tears in rain."*
> — **Roy Batty**, Patron Saint of Thoughtful Commitment

**Git commits PERSIST ephemeral IDE state into permanent history.**

When you're working in Cursor, your session holds:
- **Thinking blocks** — the LLM's reasoning
- **Context assembly** — what files were gathered
- **Tool calls** — every action taken
- **Design process** — iterations, dead ends

**All of this vanishes** when you close the IDE.

Git commit FREEZES the NOW into FOREVER:
- Permanent record in repository
- Shareable with team
- Traceable through blame/log
- Survives years

## Full Disclosure

Every commit can disclose the complete development session:

| Level | What's Disclosed |
|-------|------------------|
| Minimal | Just the diff |
| Narrative | Intent summarized |
| Linked | `cursor-mirror://e8587ace` |
| Full | Complete transcript archived |

**Benefits:**
- Future self: Remember why you made decisions
- Team: Onboard with full history
- Auditing: Demonstrate AI assistance
- Debugging: See context that led to bugs

## Composition Philosophy

### Why Sister Scripts?

`cursor_mirror.py` is a "sister script" — standalone, invoked via shell, outputting text.

**NOT a library. NOT an import. A PROCESS you talk to via stdin/stdout.**

This matters because:
- The LLM invokes it the same way a human would
- Output is inspectable, greppable, pipeable
- No hidden state, no tight coupling
- The skill doesn't "own" cursor-mirror; it USES it

Sister scripts are tools in your belt, not organs in your body.

### Why Shell as Glue?

Shell pipelines are the universal connector:
```
cursor-mirror (Python) → grep (C) → awk (C) → git (C)
```

The LLM thinks in shell because:
- Lingua franca of Unix tools
- Pipes are dataflow made visible
- Each stage independently testable
- You can see the data at every step

**Shell isn't primitive — it's COMPOSABLE.**

### Why Not Monolith?

A monolithic tool would:
- Hide the data flow
- Couple components tightly
- Be hard to debug
- Not compose with other skills

By composing cursor-mirror + shell + git:
- Transparent data flow
- Loose coupling
- Reuse across skills
- Debuggable (run each stage manually)

### The Pattern

```
skill = ORCHESTRATION     (knows WHAT to do)
sister_scripts = CAPABILITY   (knows HOW)
shell = GLUE              (connects them)
```

The skill is the conductor. The tools are the orchestra.
