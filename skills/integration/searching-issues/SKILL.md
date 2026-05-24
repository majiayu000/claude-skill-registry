---
name: searching-issues
description: Search GitHub Issues and PRs with 30+ qualifiers including labels, dates, users, state, milestones, and content. Use when searching for issues by keywords, metadata, or complex filters.
---

# Issue Search & Discovery

**Capability:** Native GitHub CLI issue and PR search with 30+ qualifiers

**When to use:** Searching GitHub Issues/PRs by content, metadata, or complex filters

---

## Quick Commands

### Basic Search

```bash
# Search across all repositories
gh search issues "authentication error" --repo=owner/repo

# Search in current repository
gh issue list --search "bug"

# Search in multiple fields
gh search issues "database" --match=title,body
```

### Common Filters

```bash
# By state and labels
gh search issues --state=open --label=bug,priority:high

# By date range
gh search issues --created="2025-01-01..2025-01-31"

# By assignee or author
gh search issues --assignee=@me --author=username

# By engagement
gh search issues --sort=comments --order=desc
```

### Advanced Qualifiers (30+ available)

**Content:** `in:title`, `in:body`, `in:comments`
**State:** `is:open`, `is:closed`, `is:merged`, `is:draft`
**Labels:** `label:bug`, `-label:wontfix`, `no:label`
**Dates:** `created:>=2025-01-01`, `updated:<2025-01-31`, `closed:2025-01..2025-02`
**Users:** `author:username`, `assignee:username`, `mentions:username`, `commenter:username`
**Repos:** `repo:owner/name`, `org:orgname`, `user:username`

**Complete Syntax Reference:** [GITHUB_NATIVE_SEARCH_CAPABILITIES.md](/docs/research/GITHUB_NATIVE_SEARCH_CAPABILITIES.md)

---

## Output & Automation

```bash
# JSON output for scripting
gh search issues "bug" --json number,title,url,labels --jq '.[] | {number, title}'

# Limit results
gh search issues "bug" --limit=50

# Export to file
gh search issues --label=feature-request --json number,title,body > features.json
```

---

## Search Limitations

- **No regex** - Use literal strings only
- **No wildcards** - Exact match or phrase search
- **No context lines** - Shows only matching issues, not surrounding context
- **For file/code search** - Use `gh grep` extension (see file-searching skill)

---

## Common Workflows

### Find Your Assigned Issues

```bash
gh search issues --assignee=@me --state=open --repo=owner/repo
```

### Find Recent Bugs

```bash
gh search issues --label=bug --created=">=2025-10-01" --state=open --sort=created
```

### Search Knowledge Base

```bash
# Search Claude Code tips
gh search issues "plan mode" --repo=terrylica/claude-code-skills-github-issues --label=claude-code
```

---

## Tool Selection Decision

- **Search Issues/PRs** → Use `gh search issues` (this skill)
- **Search repository files** → Use `gh grep` (see file-searching skill)
- **AI-powered operations** → Use `gh models` (see ai-assisted-operations skill)

---

**Empirical Testing:** 200+ test cases, 100% coverage of search qualifiers

**Full Operational Guide:** [AI_AGENT_OPERATIONAL_GUIDE.md](/docs/guides/AI_AGENT_OPERATIONAL_GUIDE.md)
