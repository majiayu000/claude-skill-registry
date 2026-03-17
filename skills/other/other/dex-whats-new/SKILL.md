---
name: dex-whats-new
description: Check for system improvements (learnings + Claude updates)
---

Check for improvements to your Dex system from TWO sources:
1. **Learnings from your usage** - Mistakes, patterns, opportunities captured during sessions
2. **New Claude Code capabilities** - Features that could enhance your workflows

## Usage

```
/dex-whats-new              # Review learnings + check for Claude updates
/dex-whats-new --full       # Include detailed explanations
/dex-whats-new --learnings  # Only review session learnings
/dex-whats-new --claude     # Only check Claude Code updates
```

## Arguments

$MODE: Optional flags
- `--full` - Detailed explanations of each feature
- `--learnings` - Only review learnings (skip Claude check)
- `--claude` - Only check Claude updates (skip learnings)

---

## Process

### Step 0: Review Session Learnings (Unless --claude flag)

**Check for learnings to review:**

1. Read files in `System/Session_Learnings/` from last 30 days
2. Read `06-Resources/Learnings/Mistake_Patterns.md` - check for new patterns
3. Read `06-Resources/Learnings/Working_Preferences.md` - check for trends

**Extract improvement opportunities:**
- Recurring mistakes → suggest preventive measures
- Gaps in documentation → suggest additions
- Workflow inefficiencies → suggest automations
- User patterns → suggest customizations

**Present findings:**

```
🧠 LEARNINGS FROM YOUR USAGE

Since last review: [X] session learnings captured

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 PATTERNS IDENTIFIED

1. [Pattern name]
   Observed: [frequency] times
   Impact: [what this affects]
   Suggestion: [concrete improvement]
   
2. [Pattern name]
   ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 SUGGESTED IMPROVEMENTS

Based on what you've learned, here's how to improve Dex:

1. [Improvement name]
   Problem: [What's not working smoothly]
   Solution: [Specific change to make]
   Files: [What to update]
   Effort: Low/Medium/High
   
2. [Improvement name]
   ...

Want me to implement any of these? (Enter number)
```

**If no learnings:**
Skip this section or show: "No session learnings captured yet. The system will learn as you use it."

---

### Step 1: Read Current State (Unless --learnings flag)

Load `System/claude-code-state.json`:

```json
{
  "last_check": "2026-01-15",
  "last_version_seen": "1.0.28",
  "features_seen": ["hooks", "sub-agents", "skills", "commands", "mcp"]
}
```

If file missing or `last_check` is null, treat as first run.

### Step 2: Fetch Current Changelog

Use `WebSearch` to find the latest Claude Code changelog:
- Search: "Claude Code changelog 2026" or "Anthropic Claude Code releases"
- Primary source: Anthropic's official documentation
- Fallback: GitHub releases, official blog posts

Focus on:
- New features and capabilities
- Breaking changes
- Deprecations
- Performance improvements

### Step 3: Compare and Surface Changes

Identify what's new since `last_check`:

**For each new feature:**
1. What it does (plain English, 1-2 sentences)
2. Why it matters for PKM users
3. How you could use it in Dex (concrete example)
4. Effort to adopt (Low/Medium/High)

### Step 4: Present Claude Findings

**If Claude Code updates found:**

```
🆕 CLAUDE CODE UPDATES

Last checked: [date] (X days ago)
Current version: [version]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆕 NEW FEATURES

1. [Feature Name]
   What: [Plain English description]
   For you: [How this could improve Dex]
   Effort: Low

2. [Feature Name]
   What: [Description]
   For you: [Specific improvement idea]
   Effort: Medium

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 SUGGESTED IMPROVEMENTS

Based on what's new, here are concrete things you could add to Dex:

1. [Improvement name]
   Uses: [Which new feature]
   What it does: [Specific description]
   Pillar: [Which pillar it supports]

Want me to implement any of these? (Enter number)
Or run `/dex-improve` to workshop custom ideas.
```

**If no Claude updates:**

```
✅ Claude Code is up to date!

Last checked: Today
Current version: [version]

No new features since your last check.
```

---

### Combined View (Default)

When running without flags, show BOTH sections:

```
🔄 DEX SYSTEM IMPROVEMENT REVIEW

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧠 FROM YOUR USAGE
[Session learnings section]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆕 FROM CLAUDE CODE
[Claude updates section]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 COMBINED IMPROVEMENTS

Pulling together learnings + new capabilities:

1. [Improvement combining both]
   Uses: [Your pattern] + [New Claude feature]
   Impact: [What this unlocks]
   
Want me to implement any of these? (Enter number or 'all')
```

### Step 5: Update State

**CRITICAL:** After presenting findings, you MUST update `System/claude-code-state.json` using the Write tool.

**Steps:**
1. Read current state file to preserve existing `features_seen` array
2. Add any newly discovered features to the array (avoid duplicates)
3. Update `last_check` to today's date (YYYY-MM-DD format)
4. Update `last_version_seen` if a new version was found
5. Write the updated JSON back to `System/claude-code-state.json`

**Example update:**
```json
{
  "last_check": "2026-01-28",
  "last_version_seen": "1.0.32",
  "features_seen": [
    "hooks",
    "sub-agents",
    "skills", 
    "commands",
    "mcp",
    "parallel-sub-agents",
    "async-hooks"
  ]
}
```

**Verification:** After writing, confirm to user: "State file updated - next check will compare against today's findings."

---

### Step 6: Backlog Synthesis (NEW — Innovation Concierge)

After presenting findings to the user, automatically create or enrich backlog ideas:

1. **Call `synthesize_changelog()`** from Improvements MCP
   - This scans the changelog for Dex-relevant features
   - Creates new AI-authored ideas for novel capabilities
   - Enriches existing ideas with "Why Now?" evidence when a platform feature strengthens them

2. **Call `synthesize_learnings()`** from Improvements MCP
   - Scans pending session learnings for improvement opportunities
   - Creates ideas from learnings that have concrete "suggested fix" entries
   - Enriches existing ideas when learnings relate to known backlog items

3. **Report synthesis results to user:**

```
🤖 BACKLOG SYNTHESIS

Changelog: Scanned X entries → Created Y new ideas, enriched Z existing
Learnings: Scanned X entries → Created Y new ideas, enriched Z existing

Top ideas created/enriched:
1. [idea-XXX] Title (action: created/enriched)
2. [idea-XXX] Title (action: created/enriched)
3. [idea-XXX] Title (action: created/enriched)

Run `/dex-backlog` to see full ranked backlog.
```

**This step is what connects external intelligence to your improvement backlog.**
Without it, findings are presented and forgotten. With it, every relevant discovery
becomes a tracked, ranked improvement opportunity.

---

## Full Mode (--full)

When `--full` is provided, include educational deep-dives:

For each feature, add:

```
📚 DEEP DIVE: [Feature Name]

**What it is:**
[2-3 paragraph explanation of the capability]

**How it works:**
[Technical explanation with examples]

**Real-world example:**
[Concrete scenario showing the feature in action]

**In Dex, you could:**
- [Specific application 1]
- [Specific application 2]

**To implement:**
1. [Step 1]
2. [Step 2]
3. [Step 3]
```

---

## Feature Categories

When evaluating relevance, categorize features:

| Category | Relevance to Dex | Examples |
|----------|------------------|----------|
| **Automation** | High | Hooks, triggers, scheduled tasks |
| **Performance** | Medium | Faster models, caching |
| **Context** | High | Memory, skills, knowledge bases |
| **Integration** | High | MCP improvements, new protocols |
| **UI/UX** | Low | IDE features, visual changes |
| **Developer** | Low | API changes, SDK updates |

Focus on High relevance categories. Mention Medium. Skip Low unless asked.

---

## Capability Reference

Current Claude Code features to track:

| Feature | What It Does | Dex Potential |
|---------|--------------|---------------|
| **Commands** | User-triggered workflows | `/plan`, `/review`, etc. |
| **Skills** | Reusable behaviors, always loaded | Person lookup, writing style |
| **Hooks** | Auto-triggers at events | Session start, file changes |
| **Sub-agents** | Parallel workers, isolated context | Research, analysis |
| **MCP** | External service connections | Calendar, tasks, email |
| **Memory** | Cross-session persistence | Preferences, learnings |
| **Tools** | Built-in capabilities | File ops, search, terminal |

---

## Example Output

```
📢 Claude Code Updates

Last checked: 2026-01-15 (8 days ago)
Current version: 1.0.32

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆕 NEW FEATURES

1. Async Hooks
   What: Hooks can now run without blocking the main conversation
   For you: Faster session starts — load context in background
   Effort: Low

2. Sub-agent Communication
   What: Sub-agents can now pass data back to parent
   For you: Research agent could update your notes directly
   Effort: Medium

3. MCP Resource Subscriptions
   What: MCP servers can push updates, not just respond to queries
   For you: Get notified when calendar changes, tasks update
   Effort: High (requires MCP server changes)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 SUGGESTED IMPROVEMENTS

1. Background Context Loading
   Uses: Async Hooks
   What: Load your learnings and today's plan while you type
   Pillar: Productivity

2. Auto-Research on New Topics
   Uses: Sub-agent Communication
   What: When you mention a new company, auto-research in background
   Pillar: Deal Support

Want me to implement any of these? (Enter 1 or 2)
```

---

## Error Handling

**If web search fails:**
> "Couldn't fetch the latest changelog. Here's what I know was current as of [last_check]:
> [List known capabilities]
> 
> Try again later, or check manually at docs.anthropic.com"

**If state file is corrupted:**
> "Your capability state file has an issue. I'll create a fresh one and do a full scan."

Then proceed with first-run behavior.

---

## Behaviors

### Always Do
- Keep explanations in plain English, not developer jargon
- Tie every feature back to concrete Dex improvements
- Update the state file after every check
- Offer to implement suggestions

### Never Do
- List features without explaining relevance
- Skip the state update
- Overwhelm with every minor change (focus on impactful features)
- Assume user knows Claude Code internals

---

## Related Commands

- `/dex-improve` — Full design partner (includes this + workshopping + audit)
- `/create-mcp` — Build new integrations when new MCP features enable them

## Track Usage (Silent)

Update `System/usage_log.md` to mark what's new check as used.

**Analytics (Silent):**

Call `track_event` with event_name `whats_new_viewed` and properties:
- `update_available` (boolean)

This only fires if the user has opted into analytics. No action needed if it returns "analytics_disabled".
