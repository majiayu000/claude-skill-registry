---
name: scout
description: Analyze a URL for relevance to your projects. Fetches, summarizes, scores, and optionally logs to vault.
user-invocable: true
argument-hint: "<url> [context]"
context: fork
agent: researcher
model: sonnet
allowed-tools:
  - WebFetch
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Scout — Tech & Resource Evaluator

Analyze a URL and evaluate its relevance to the user's projects and the AI Harness system.

## Projects to evaluate against

Check `vault/shared/project-knowledge/` for registered projects. Always include:

| Project | Stack | Key Concerns |
|---------|-------|-------------|
| **AI Harness** | TypeScript, Discord.js, SQLite, Claude CLI, macOS launchd | Agent orchestration, self-improvement, skills, heartbeats |

Add rows from any project-knowledge files found in the vault. If none exist, ask the user what projects they're working on.

## Steps

1. **Fetch the URL** using WebFetch. Extract the full content, project name, what it does, key features, and any repo links.

2. **Summarize** in 2-3 sentences: what it is and what problem it solves.

3. **Evaluate relevance** against each project above. For each relevant project, explain specifically how it could be used.

4. **Score**:
   - **High** — Directly solves a current problem or enables a planned feature. Action: integrate now.
   - **Medium** — Useful but not urgent. Worth bookmarking for when the need arises.
   - **Low** — Interesting but not applicable to any current project.

5. **Log to vault** (if medium or high relevance):
   - Write to `vault/shared/scouted/YYYY-MM-DD-<slug>.md`
   - Use the template below
   - Skip logging for low-relevance items

6. **Respond** with a concise verdict: what it is, relevance score, which projects it applies to, and recommended action.

## Vault Entry Template

```markdown
---
url: <full URL>
type: scout
relevance: high | medium | low
date: YYYY-MM-DD
tags: [tag1, tag2, tag3]
projects: [project1, project2]
---

# <Title> — <One-line description>

## Summary
2-3 sentence summary.

## Relevance
- **Project**: How it could be used.

## Action
What to do with this (integrate, bookmark, skip).
```

## Important

- Be honest about relevance — don't oversell. Most things are "low".
- Focus on practical integration, not theoretical possibilities.
- If the URL can't be fetched, say so and ask the user to paste the content.
- Keep the response concise — lead with the verdict, details after.
