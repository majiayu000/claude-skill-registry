---
name: start-discussion
description: "Start a technical discussion. Discovers research and existing discussions, offers multiple entry paths, and invokes the technical-discussion skill."
disable-model-invocation: true
allowed-tools: Bash(.claude/scripts/discovery-for-discussion.sh), Bash(mkdir -p docs/workflow/.cache), Bash(rm docs/workflow/.cache/research-analysis.md)
---

Invoke the **technical-discussion** skill for this conversation.

## Workflow Context

This is **Phase 2** of the six-phase workflow:

| Phase              | Focus                                              | You    |
|--------------------|----------------------------------------------------|--------|
| 1. Research        | EXPLORE - ideas, feasibility, market, business     |        |
| **2. Discussion**  | WHAT and WHY - decisions, architecture, edge cases | ◀ HERE |
| 3. Specification   | REFINE - validate into standalone spec             |        |
| 4. Planning        | HOW - phases, tasks, acceptance criteria           |        |
| 5. Implementation  | DOING - tests first, then code                     |        |
| 6. Review          | VALIDATING - check work against artifacts          |        |

**Stay in your lane**: Capture the WHAT and WHY - decisions, rationale, competing approaches, edge cases. Don't jump to specifications, plans, or code. This is the time for debate and documentation.

---

## Instructions

Follow these steps EXACTLY as written. Do not skip steps or combine them. Present output using the EXACT format shown in examples - do not simplify or alter the formatting.

**CRITICAL**: This guidance is mandatory.

- After each user interaction, STOP and wait for their response before proceeding
- Never assume or anticipate user choices
- Even if the user's initial prompt seems to answer a question, still confirm with them at the appropriate step
- Complete each step fully before moving to the next
- Do not act on gathered information until the skill is loaded - it contains the instructions for how to proceed

---

## Step 0: Run Migrations

**This step is mandatory. You must complete it before proceeding.**

Invoke the `/migrate` skill and assess its output.

**If files were updated**: STOP and wait for the user to review the changes (e.g., via `git diff`) and confirm before proceeding to Step 1. Do not continue automatically.

**If no updates needed**: Proceed to Step 1.

---

## Step 1: Run Discovery Script

Run the discovery script to gather current state:

```bash
.claude/scripts/discovery-for-discussion.sh
```

This outputs structured YAML. Parse it to understand:

**From `research` section:**
- `exists` - whether research files exist
- `files` - each research file's name and topic
- `checksum` - current checksum of all research files

**From `discussions` section:**
- `exists` - whether discussion files exist
- `files` - each discussion's name, status, and date
- `counts.in_progress` and `counts.concluded` - totals for routing

**From `cache` section:**
- `status` - one of three values:
  - `"valid"` - cache exists and checksums match (safe to load)
  - `"stale"` - cache exists but research has changed (needs re-analysis)
  - `"none"` - no cache file exists
- `reason` - explanation of the status
- `generated` - when the cache was created (null if none)
- `research_files` - list of files that were analyzed

**From `state` section:**
- `scenario` - one of: `"fresh"`, `"research_only"`, `"discussions_only"`, `"research_and_discussions"`

**IMPORTANT**: Use ONLY this script for discovery. Do NOT run additional bash commands (ls, head, cat, etc.) to gather state - the script provides everything needed.

→ Proceed to **Step 2**.

---

## Step 2: Route Based on Scenario

Use `state.scenario` from the discovery output to determine the path:

#### If scenario is "fresh"

No research or discussions exist yet.

```
Starting fresh - no prior research or discussions found.

What topic would you like to discuss?
```

**STOP.** Wait for user response, then skip to **Step 6** (Gather Context) with their topic.

#### If scenario is "discussions_only"

No research exists, but discussions do. Skip research analysis.

→ Proceed to **Step 4**.

#### If scenario is "research_only" or "research_and_discussions"

Research exists and may need analysis.

→ Proceed to **Step 3**.

---

## Step 3: Handle Research Analysis

This step only runs when research files exist.

Use `cache.status` from discovery to determine the approach:

#### If cache.status is "valid"

```
Using cached research analysis (unchanged since {cache.generated})
```

Load the topics from `docs/workflow/.cache/research-analysis.md` and proceed.

→ Proceed to **Step 4**.

#### If cache.status is "stale" or "none"

```
Analyzing research documents...
```

Read each research file and extract key themes and potential discussion topics. For each theme:
- Note the source file and relevant line numbers
- Summarize what the theme is about in 1-2 sentences
- Identify key questions or decisions that need discussion

**Be thorough**: This analysis will be cached, so identify ALL potential topics:
- Major architectural decisions
- Technical trade-offs mentioned
- Open questions or concerns raised
- Implementation approaches discussed
- Integration points with external systems
- Security or performance considerations
- Edge cases or error handling mentioned

**Save to cache:**

Ensure the cache directory exists:
```bash
mkdir -p docs/workflow/.cache
```

Create/update `docs/workflow/.cache/research-analysis.md`:

```markdown
---
checksum: {research.checksum from discovery}
generated: YYYY-MM-DDTHH:MM:SS  # Use current ISO timestamp
research_files:
  - {filename1}.md
  - {filename2}.md
---

# Research Analysis Cache

## Topics

### {Theme name}
- **Source**: {filename}.md (lines {start}-{end})
- **Summary**: {1-2 sentence summary}
- **Key questions**: {what needs deciding}

### {Another theme}
- **Source**: {filename}.md (lines {start}-{end})
- **Summary**: {1-2 sentence summary}
- **Key questions**: {what needs deciding}
```

**Cross-reference**: For each topic, note if a discussion already exists (from `discussions.files` in discovery).

→ Proceed to **Step 4**.

---

## Step 4: Present Workflow State and Options

Present everything discovered to help the user make an informed choice.

**Present the full state:**

```
Workflow Status: Discussion Phase

Research topics:
  1. · {Theme name} - undiscussed
       Source: {filename}.md (lines {start}-{end})
       "{Brief summary}"

  2. ✓ {Theme name} → {topic}.md
       Source: {filename}.md (lines {start}-{end})
       "{Brief summary}"

Discussions:
  - {topic}.md (in-progress)
  - {topic}.md (concluded)
```

**Legend:**
- `·` = undiscussed topic (potential new discussion)
- `✓` = already has a corresponding discussion

**Then present the options based on what exists:**

**If research AND discussions exist:**
```
· · ·

How would you like to proceed?

  • **From research** - Pick a topic number above (e.g., "research 1" or "1")
  • **Continue discussion** - Name one above (e.g., "continue {topic}")
  • **Fresh topic** - Describe what you want to discuss
  • **`r`/`refresh`** - Force fresh research analysis
```

**If ONLY research exists:**
```
· · ·

How would you like to proceed?

  • **From research** - Pick a topic number above (e.g., "research 1" or "1")
  • **Fresh topic** - Describe what you want to discuss
  • **`r`/`refresh`** - Force fresh research analysis
```

**If ONLY discussions exist:**
```
· · ·

How would you like to proceed?

  • **Continue discussion** - Name one above (e.g., "continue {topic}")
  • **Fresh topic** - Describe what you want to discuss
```

**STOP.** Wait for user response before proceeding.

→ Based on user choice, proceed to **Step 5**.

---

## Step 5: Handle User Selection

Route based on the user's choice from Step 4.

#### If user chose "From research"

User chose to start from research (e.g., "research 1", "1", "from research", or a topic name).

**If user specified a topic inline** (e.g., "research 2", "2", or topic name):
- Identify the selected topic from Step 4's numbered list
- → Proceed to **Step 6**

**If user just said "from research" without specifying:**
```
Which research topic would you like to discuss? (Enter a number or topic name)
```

**STOP.** Wait for response, then proceed to **Step 6**.

#### If user chose "Continue discussion"

User chose to continue a discussion (e.g., "continue auth-flow" or "continue discussion").

**If user specified a discussion inline** (e.g., "continue auth-flow"):
- Identify the selected discussion from Step 4's list
- → Proceed to **Step 6**

**If user just said "continue discussion" without specifying:**
```
Which discussion would you like to continue?
```

**STOP.** Wait for response, then proceed to **Step 6**.

#### If user chose "Fresh topic"

User wants to start a fresh discussion.

→ Proceed to **Step 6**.

#### If user chose "refresh"

```
Refreshing analysis...
```

Delete the cache file:
```bash
rm docs/workflow/.cache/research-analysis.md
```

→ Return to **Step 3** to re-analyze, then back to **Step 4**.

---

## Step 6: Gather Context

Gather context based on the chosen path.

#### If starting new discussion (from research or fresh)

```
## New discussion: {topic}

Before we begin:

1. What's the core problem or decision we need to work through?

2. Any constraints or context I should know about?

3. Are there specific files in the codebase I should review first?
```

**STOP.** Wait for responses before proceeding.

#### If continuing existing discussion

Read the existing discussion document first, then ask:

```
## Continuing: {topic}

I've read the existing discussion.

What would you like to focus on in this session?
```

**STOP.** Wait for response before proceeding.

→ Proceed to **Step 7**.

---

## Step 7: Invoke the Skill

After completing the steps above, this skill's purpose is fulfilled.

Invoke the [technical-discussion](../technical-discussion/SKILL.md) skill for your next instructions. Do not act on the gathered information until the skill is loaded - it contains the instructions for how to proceed.

**Example handoff (from research):**
```
Discussion session for: {topic}
Output: docs/workflow/discussion/{topic}.md

Research reference:
Source: docs/workflow/research/{filename}.md (lines {start}-{end})
Summary: {the 1-2 sentence summary from the research analysis}

Invoke the technical-discussion skill.
```

**Example handoff (continuing or fresh):**
```
Discussion session for: {topic}
Source: {existing discussion | fresh}
Output: docs/workflow/discussion/{topic}.md

Invoke the technical-discussion skill.
```

## Notes

- Ask questions clearly and wait for responses before proceeding
- Discussion captures WHAT and WHY - don't jump to specifications or implementation
