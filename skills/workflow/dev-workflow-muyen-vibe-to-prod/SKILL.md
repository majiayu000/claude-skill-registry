---
name: dev-workflow
description: SDLC workflow with MCP tools. Triggers on "start", "implement", "work on", or unclear workflow.
---

# SDLC: Intake → Triage → Explore → Plan → Code → Test → Review → Commit → Deploy → Improve

## MCP Tools by Phase

| Phase | Tools |
|-------|-------|
| Intake | `mcp__linear__get_issue`, `mcp__notion__notion-search` |
| Explore | `mcp__memory__search_nodes`, `mcp__github__search_code`, `mcp__context7__query-docs` |
| Plan | `mcp__linear__create_issue` (subtasks), `mcp__notion__notion-create-pages`, `mcp__github__create_branch` |
| Code | `mcp__context7__query-docs`, Read, Write, Edit |
| Test | Bash (make test, npm test), `/quick-test` |
| Deploy | `mcp__github__create_pull_request`, `/smoke-test` |
| Improve | `mcp__memory__create_entities`, `mcp__linear__create_issue` |

## Triage Decision

| Change Type | Path |
|-------------|------|
| New feature, breaking change, architecture | OpenSpec → `/openspec:proposal` |
| Bug fix, config, tests, typo | Quick → `TodoWrite` |

## Phase Actions

**Intake**: Fetch Linear issue, search Notion for context
**Explore**: Search Memory for learnings, explore codebase, check related PRs
**Plan**: OpenSpec proposal OR TodoWrite, create branch
**Code**: Follow tasks, use platform rules, mark todos complete
**Test**: `/quick-test`, add tests for new logic
**Review**: `/code-review`, `/security-scan` if auth/data
**Commit**: `/commit` with `type: description`
**Deploy**: Create PR, run smoke tests after merge
**Improve**: Store learnings in Memory, create improvement tasks if needed

## Quick Reference

```bash
# Backend
cd backend && make test
cd backend && make build

# Web
cd web && npm test
cd web && npm run build

# iOS
cd mobile/ios && make test

# Android
cd mobile/android && ./gradlew test
```

## Anti-Patterns

- Coding without exploring → miss patterns
- Skipping Linear context → untracked work
- No Memory capture → repeat learnings
- Big commits → hard to review
