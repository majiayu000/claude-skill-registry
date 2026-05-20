---
name: startup-diagnostic
description: Use when starting a session and suspecting configuration issues, after hook failures, MCP connection errors, or degraded vault performance. Also useful as a periodic health audit.
---

# Startup Diagnostic

Examine all Claude Code startup components — configuration, hooks, MCP servers, indexes, plugins, and filesystem — report PASS/FAIL/WARN for each, and offer fixes for any failures.

## Parallelisation Strategy

**Batch 1 (may-fail-gracefully — use Bash with `2>/dev/null`, NOT Read tool):**
Steps 1–2 read files that may not exist. A failed Read cascades and kills all sibling parallel calls. Check 5 (graph index) can also ENOENT — include it here.

**Batch 2 (reliable — run in parallel):**
Steps 3–4 and 6–11 query indexes, npm, git, and filesystem. Safe to run together.

**Shell gotcha:** Never use `!!` (double-bang) in `node -e` strings — zsh expands it as history substitution. Use `'key' in obj` instead of `!!obj.key`.

---

## Checks

### 1. Configuration Files

Check these files exist and parse as valid JSON/markdown:

| File | Check |
|------|-------|
| `CLAUDE.md` | Exists at repo root |
| `.claude/settings.json` | Valid JSON, has `permissions`, `plansDirectory` |
| `.claude/settings.local.json` | Valid JSON, has `hooks` and `permissions` |
| `~/.claude/settings.json` | Valid JSON (global settings) |
| `.mcp.json` | Valid JSON, all `mcpServers` entries have `command` |
| `.claude/AGENDA.md` | Exists (WARN if missing) |
| `.claude/vault-conventions.md` | Exists |

```bash
node -e "JSON.parse(require('fs').readFileSync('.claude/settings.json','utf8')); console.log('OK')"
```

Flag any permission duplicates or contradictions between `.claude/settings.json` and `.claude/settings.local.json`.

### 2. Hook Execution

Test every configured hook can execute without crashing. Pass minimal JSON on stdin, check exit code.

**UserPromptSubmit:**
```bash
echo '{"query":"test"}' | python3 .claude/hooks/secret-detection.py; echo "exit:$?"
echo '{"query":"test"}' | bash .claude/hooks/skill-context-loader.sh; echo "exit:$?"
```

**PreToolUse:**
```bash
echo '{"tool_name":"Edit","tool_input":{"file_path":"/tmp/test.md","old_string":"a","new_string":"b"}}' | python3 .claude/hooks/file-protection.py; echo "exit:$?"
echo '{"tool_name":"Edit","tool_input":{"file_path":"/tmp/test.md"}}' | python3 .claude/hooks/secret-file-scanner.py; echo "exit:$?"
echo '{"tool_name":"Grep","tool_input":{"pattern":"test"}}' | bash .claude/hooks/graph-search-hint.sh; echo "exit:$?"
echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | python3 .claude/hooks/skill-rename-guard.py; echo "exit:$?"
echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | python3 .claude/hooks/bash-safety.py; echo "exit:$?"
```

**PostToolUse:**
```bash
echo '{"tool_name":"Edit","tool_input":{"file_path":"/tmp/test.md"},"tool_result":"ok"}' | python3 .claude/hooks/frontmatter-validator.py; echo "exit:$?"
echo '{"tool_name":"Edit","tool_input":{"file_path":"/tmp/test.md"},"tool_result":"ok"}' | python3 .claude/hooks/tag-taxonomy-enforcer.py; echo "exit:$?"
echo '{"tool_name":"Edit","tool_input":{"file_path":"/tmp/test.md"},"tool_result":"ok"}' | python3 .claude/hooks/wiki-link-checker.py; echo "exit:$?"
echo '{"tool_name":"Edit","tool_input":{"file_path":"/tmp/test.md"},"tool_result":"ok"}' | python3 .claude/hooks/filename-convention-checker.py; echo "exit:$?"
echo '{"tool_name":"Edit","tool_input":{"file_path":"/tmp/test.md"},"tool_result":"ok"}' | python3 .claude/hooks/code-formatter.py; echo "exit:$?"
echo '{"tool_name":"Edit","tool_input":{"file_path":"/tmp/test.md"},"tool_result":"ok"}' | bash .claude/hooks/auto-commit.sh; echo "exit:$?"
```

**Notification (Stop):**
```bash
python3 .claude/hooks/session-summary.py; echo "exit:$?"
```

| Result | Status |
|--------|--------|
| Exit 0 | PASS |
| Non-zero exit | FAIL (report stderr) |
| ImportError / ModuleNotFoundError | FAIL (missing dependency) |
| Timeout (>5s standard, >15s wiki-link-checker) | WARN |

### 3. MCP Server Connectivity

Test each server from `.mcp.json` can start and respond:

| Server | Test |
|--------|------|
| context7 | ToolSearch for context7 tools, trivial query |
| memory | ToolSearch for memory tools, call `read_graph` |
| hostinger-mcp | ToolSearch for hostinger tools (auth failure OK — server started) |

Also check plugin MCP servers (MCP_DOCKER for Notion/Diagrams/YouTube) via ToolSearch.

Flag: missing npx package, auth issue, or network problem.

### 4. SQLite Index (Legacy/Secondary)

```bash
sqlite3 .data/vault.db "SELECT COUNT(*) as total FROM notes"
sqlite3 .data/vault.db "SELECT type, COUNT(*) FROM notes GROUP BY type ORDER BY COUNT(*) DESC LIMIT 5"
sqlite3 .data/vault.db "PRAGMA integrity_check"
```

Check freshness — files newer than the index:
```bash
find . -name "*.md" -not -path "./.git/*" -not -path "./node_modules/*" -newer .data/vault.db 2>/dev/null | wc -l
```

| Result | Status |
|--------|--------|
| Database missing | WARN — `npm run vault:index` (secondary index) |
| Integrity check fails | WARN — rebuild with `npm run vault:index` |
| >20 files newer than index | WARN — suggest reindex |

**Note:** SQLite is a secondary index. The primary search index is the Graph index (Check 5).

### 5. Graph Index (PRIMARY)

**Run in Batch 1** (file may not exist — ENOENT crashes Node and cascades to siblings).

```bash
ls -la .graph/index.json .graph/search.json 2>/dev/null
node .claude/scripts/graph-query.js --stats 2>/dev/null | head -5
```

Check freshness — files newer than the graph index:
```bash
find . -name "*.md" -not -path "./.claude/*" -not -path "./.obsidian/*" -not -path "./node_modules/*" -not -path "./Templates/*" -newer .graph/index.json 2>/dev/null | head -1
```

Fallback if `graph-query.js --stats` is unavailable:
```bash
node -e "try{const g=JSON.parse(require('fs').readFileSync('.graph/graph.json','utf8'));console.log('Nodes:',Object.keys(g.nodes||{}).length,'Edges:',(g.edges||[]).length)}catch(e){console.log('MISSING:',e.code||e.message)}" 2>/dev/null
```

| Result | Status |
|--------|--------|
| Graph files missing | FAIL — `npm run graph:build` |
| Graph empty (0 nodes) | FAIL — rebuild with `npm run graph:build` |
| >0 files newer than index | WARN — suggest `npm run graph:build` |
| Stats available and current | PASS |

### 6. Filesystem Structure

```bash
for dir in Meetings Projects Tasks ADRs Emails Trips Daily Incubator Forms People Attachments Archive Templates Objectives .claude/skills .claude/context .claude/rules .claude/agents .claude/scripts .data; do
  [ -d "$dir" ] && echo "PASS $dir" || echo "FAIL $dir MISSING"
done
```

### 7. Git Health

```bash
git status --porcelain | head -20
git stash list
git log --oneline -3
```

| Symptom | Status |
|---------|--------|
| Uncommitted .env / credentials | FAIL |
| >20 untracked files | WARN |
| >5 stale stashes | WARN |
| Detached HEAD | WARN |

### 8. Sandbox Configuration

Sandbox config lives in `.claude/settings.local.json` (project-level), **not** `~/.claude/settings.json` (global).

Verify `.claude/settings.local.json` has:
- `sandbox.enabled: true`
- `sandbox.permissions.additionalWritePaths` includes `/Users/david.oliver/.cache/pre-commit`

```bash
node -e "const d=JSON.parse(require('fs').readFileSync('.claude/settings.local.json','utf8')); const s=d.sandbox||{}; console.log('enabled:', s.enabled); const paths=(s.permissions||{}).additionalWritePaths||[]; console.log('pre-commit:', paths.some(p=>p.includes('pre-commit'))?'PRESENT':'MISSING')"
```

Missing pre-commit path causes git hook failures.

### 9. Plugin Loading

Expected plugins (from `~/.claude/settings.json`):

| Plugin | Expected |
|--------|----------|
| superpowers | enabled |
| code-review | enabled |
| atlassian | enabled |
| compound-engineering | enabled |
| claude-md-management | enabled |
| ralph-loop | enabled |
| hookify | enabled |
| claude-code-setup | enabled (global) |
| context7 (plugin) | disabled (MCP server used instead) |

Count skills in system-reminder. Significantly fewer than ~150 suggests a plugin failed to load.

### 10. Skill Files Integrity

```bash
# Lowercase skill.md files (should be SKILL.md)
find .claude/skills -name "skill.md" -not -name "SKILL.md" 2>/dev/null

# Total skill count
find .claude/skills -name "SKILL.md" | wc -l
```

Any lowercase results = FAIL (rename to `SKILL.md`).

### 11. Vault-Review Readiness

```bash
cat "Daily/$(date +%Y)/Daily - $(date +%Y-%m-%d).md" 2>/dev/null && echo "EXISTS" || echo "MISSING"
cat .claude/AGENDA.md 2>/dev/null && echo "EXISTS" || echo "MISSING"
node .claude/scripts/graph-query.js --type=Task --where="status=active" --count 2>/dev/null || echo "QUERY FAILED"
```

---

## Report Format

```markdown
## Startup Diagnostic — YYYY-MM-DD HH:MM

| # | Section | Status | Details |
|---|---------|--------|---------|
| 1 | Configuration Files | ✅ | All 7 files valid |
| 2 | Hook Execution | ⚠️ | wiki-link-checker slow (8s) |
| 3 | MCP Servers | ✅ | 3/3 connected |
| 4 | SQLite Index (Secondary) | ⚠️ | 12 files newer than index |
| 5 | Graph Index (PRIMARY) | ✅ | 847 nodes, 2341 edges |
| 6 | Filesystem | ✅ | All 16 directories present |
| 7 | Git Health | ✅ | Clean, on main |
| 8 | Sandbox | ✅ | pre-commit path included |
| 9 | Plugins | ✅ | 8/8 loaded |
| 10 | Skill Files | ✅ | 91 skills, all uppercase |
| 11 | Vault-Review | ⚠️ | No daily note |

**Overall: HEALTHY / NEEDS ATTENTION / DEGRADED**

### Fixes Required
1. [Actionable fix for each FAIL]

### Recommendations
1. [Suggestion for each WARN]
```
