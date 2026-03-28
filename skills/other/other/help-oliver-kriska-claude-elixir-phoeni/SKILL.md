---
name: phx:help
description: "Navigate Elixir/Phoenix plugin commands — recommend the right /phx: command, skill, or agent for planning, review, debug, deploy, ecto, liveview, or test tasks. Use when the user asks 'which command', 'what should I use', 'how do I', or needs help choosing between plugin workflows. DO NOT trigger for /help (built-in CLI command)."
argument-hint: "[description of what you want to do]"
---

# Plugin Help — Interactive Command Advisor

Helps users find the right command, skill, or agent for their situation.

## Usage

```
/phx:help                          # Analyze context, suggest commands
/phx:help how do I debug this?     # Route to /phx:investigate
/phx:help add a new feature        # Route to /phx:plan -> /phx:work
```

## Arguments

- `$ARGUMENTS` — optional description of what the user wants to do
- Empty = analyze current context (git status, existing plans, file patterns)

## Execution Flow

### Step 1: Gather Context

If `$ARGUMENTS` is non-empty, use it as primary signal.

Always gather ambient context (run in parallel):

1. Check for existing plans: `ls .claude/plans/` — active work in progress?
2. Check git status: uncommitted changes? which files?
3. Check for solution docs: `ls .claude/solutions/` — prior knowledge?

### Step 2: Classify Intent

Read `references/tool-catalog.md` for the full routing table.

Map the user's situation to one of these categories:

| Category | Signals | Primary Commands |
|----------|---------|-----------------|
| **Starting out** | No plans, new to plugin | `/phx:intro` |
| **New feature** | "add", "build", "implement", multi-file | `/phx:plan` → `/phx:work` |
| **Quick change** | Single file, <50 lines, "fix typo" | `/phx:quick` |
| **Bug** | Error, stack trace, "broken", "failing" | `/phx:investigate` |
| **Review** | "check", "review", PR ready | `/phx:review` |
| **Performance** | "slow", "N+1", "memory" | `/phx:perf`, `/ecto:n1-check`, `/lv:assigns` |
| **Research** | "how to", "best practice", "evaluate lib" | `/phx:research` |
| **Resume work** | Existing plan with unchecked tasks | `/phx:work --continue` |
| **Post-fix** | "that worked", solved a hard bug | `/phx:compound` |
| **Full cycle** | Large feature, new domain area | `/phx:full` |
| **Project health** | "audit", "tech debt", "overall quality" | `/phx:audit`, `/phx:techdebt` |
| **Deployment** | "deploy", "release", "production" | `/phx:verify` then deploy skill |
| **Permissions** | "too many prompts", "allow", "permission fatigue" | `/phx:permissions` |

### Step 3: Respond or Clarify

**If high confidence** (clear match to one category):
Present the recommendation with:

- The command to run (with exact syntax)
- One-line explanation of what it does
- What artifacts it creates (if any)
- Suggested next step after it completes

**If medium confidence** (2-3 possible matches):
Use `AskUserQuestion` with the top options, each with a one-line explanation.

**If low confidence** (vague or no signal):
Ask ONE focused clarifying question. Examples:

- "Are you starting something new or continuing existing work?"
- "Is this a bug fix or a new feature?"
- "How many files do you expect to change?"

Then recommend based on the answer.

### Step 4: Offer Follow-up

After recommending, always add:

- "Run `/phx:help` anytime to get routing advice"
- If they seem new: "Try `/phx:intro` for a full plugin walkthrough"

## Iron Laws

1. **ONE recommendation** — don't dump the full catalog, pick the best match
2. **MAX ONE clarifying question** — don't interrogate, make your best guess
3. **Show exact syntax** — `/phx:plan Add user notifications` not just "use the plan command"
4. **Context over keywords** — existing plans + git state matter more than word matching
5. **Never block** — if user already knows what they want, don't redirect

## Integration

- Complements `intent-detection` (auto-trigger) with explicit invocation
- References same routing logic but adds interactive clarification
- Can recommend `/phx:intro` for onboarding
