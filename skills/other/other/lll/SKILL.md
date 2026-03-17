---
name: lll
description: List project status - show open issues, recent PRs, commits, and current focus. Use when user types 'lll' or asks for project overview/status.
model: haiku
---

# LLL - List Project Status

## Purpose
Provide a comprehensive overview of the project's current state including issues, PRs, commits, and focus areas.

## When to Use
- User explicitly types `lll`
- User asks "what's the status?" or "what are we working on?"
- Starting a session and need project context
- Before planning new work

## Steps

### 1. Use LLL Script (Uses Gemini Flash for analysis only)

This skill now uses `scripts/lll_status.py` which:
- Gathers all git/gh data automatically (no LLM)
- Formats output as markdown (no LLM)
- Uses Gemini Flash ONLY for "Current Focus" analysis
- Saves ~80% of LLM costs

### 2. Execute Script

```bash
python3 scripts/lll_status.py
```

The script will:
1. Gather all project data in parallel
2. Categorize issues by labels
3. Format visual markdown output
4. Analyze current focus with Gemini Flash (or simple analysis if unavailable)
5. Suggest next steps

### 3. Output Format

The script produces a complete markdown status report:

```markdown
# 📊 Project Status - [Current Date/Time GMT+7]

## 🌿 Current Branch
`[branch-name]`

## 📝 Working Directory
[If clean: "✅ Clean"]
[If changes: Show git status --short output]

## 🎯 Open Issues ([count])

### 🎨 Context Issues
- #[number] - [title] (created [relative-time])
- ...

### 📋 Plan Issues
- #[number] - [title] (created [relative-time])
- ...

### 🐛 Bugs
- #[number] - [title] (created [relative-time])
- ...

### ✨ Features
- #[number] - [title] (created [relative-time])
- ...

### 📚 Other
- #[number] - [title] (created [relative-time])
- ...

## 🔄 Open Pull Requests ([count])
- #[number] - [title] by @[author] (opened [relative-time])
- ...

## 📜 Recent Commits (Last 10)
```
[git log output]
```

## 🎯 Current Focus
[Analyze and summarize what's currently in progress based on:]
- Latest context issue
- Latest plan issue
- Open PRs
- Recent commits

[Provide 2-3 sentence summary of current work]

## 💡 Suggested Next Steps
Based on current state:
- [ ] [Most logical next action]
- [ ] [Follow-up suggestion]
- [ ] [Future consideration]
```

### 3. Provide Context

After the summary, add helpful context:

**If there are open plan issues:**
```
📋 You have [N] plan(s) ready to execute with `gogogo`
```

**If there are context issues but no plans:**
```
💭 You have context saved. Create a plan with `nnn`
```

**If working directory has changes:**
```
⚠️ You have uncommitted changes. Consider using `ccc` to save context.
```

**If there are no issues:**
```
🎉 No open issues! Start new work or create retrospective with `rrr`
```

## Important Notes
- **Visual**: Use emojis and formatting for clarity
- **Parallel**: Run all commands in parallel for speed
- **Relative Time**: Show "2 hours ago", "3 days ago" instead of absolute dates
- **Categories**: Group issues by labels (context, plan, bug, feature)
- **Summary**: Always provide "Current Focus" analysis
- **Actionable**: End with suggested next steps

## Output Format Example

```
# 📊 Project Status - 2026-01-06 14:30 GMT+7

## 🌿 Current Branch
`feat/issue-15-multi-agent`

## 📝 Working Directory
✅ Clean

## 🎯 Open Issues (5)

### 📋 Plan Issues
- #16 - Plan: Phase 2 & 3 Multi-Agent (created 2 hours ago)

### ✨ Features
- #15 - Gatekeeper Agent Implementation (created 1 day ago)
- #14 - Task Router System (created 1 day ago)

### 📚 Other
- #10 - Documentation Updates (created 5 days ago)

## 🔄 Open Pull Requests (2)
- #17 - feat: Implement Phase 2 Task Router by @user (opened 3 hours ago)
- #12 - docs: Update README by @user (opened 2 days ago)

## 📜 Recent Commits (Last 10)
54cfa1b docs: Add session retrospective 2026-01-06
75c4d07 docs: Add session retrospective 2026-01-05
ffd0d49 docs: Add Thai usage guide

## 🎯 Current Focus
Currently implementing multi-agent cost optimization system (Issue #15).
Phase 1 (Gatekeeper) complete. Working on Phase 2 (Task Router) with
plan ready in #16. PR #17 open for review.

## 💡 Suggested Next Steps
Based on current state:
- [ ] Review PR #17 for Phase 2 implementation
- [ ] Execute plan #16 with `gogogo` for Phase 3
- [ ] Create retrospective with `rrr` after Phase 2 merges
```

## Success Criteria
- ✅ All data gathered in parallel
- ✅ Visual formatting with emojis
- ✅ Issues categorized by labels
- ✅ Current focus analyzed and summarized
- ✅ Actionable next steps provided
- ✅ Response time < 5 seconds
