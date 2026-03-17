---
name: check-updates
description: Check upstream repo changes since last analysis, assess impact on docs and demos, or stamp current commit
---

# Check Updates

Check if upstream repos have changed since the last analysis, assess the impact on docs and demos, or stamp the current commit as analyzed.

## Trigger

`/check-updates [--stamp] [agent-name]`

- Without arguments: check all agents with `analyzed_commit`
- With `agent-name`: check only that agent
- With `--stamp agent-name`: update commit tracking to current submodule HEAD

## Mode 1: Check (default)

`/check-updates [agent-name]`

### Steps

1. **Read agents.yaml** — find agents with `analyzed_commit` field. If `agent-name` is given, filter to that one.

2. **Get remote HEAD** — for each agent, extract `{owner}/{repo}` from the `repo:` URL and run:
   ```bash
   gh api repos/{owner}/{repo}/commits?per_page=1 --jq '.[0].sha'
   ```

3. **Compare** — if `analyzed_commit` == remote HEAD → report "UP TO DATE". Otherwise:
   ```bash
   gh api repos/{owner}/{repo}/compare/{analyzed_commit}...{remote_head}
   ```

4. **Classify changed files by dimension impact**:

   | File pattern | Likely affected dimension |
   |---|---|
   | `**/main.*`, `**/cli.*`, `**/core/**` | D1 Architecture, D2 Agent Loop |
   | `**/tool*`, `**/command*`, `**/action*` | D3 Tool System |
   | `**/prompt*`, `**/system*`, `**/template*` | D4 Prompt Engineering |
   | `**/context*`, `**/token*`, `**/repomap*` | D5 Context Management |
   | `**/error*`, `**/retry*`, `**/recover*` | D6 Error Handling |
   | `README*`, `CHANGELOG*` | D1 Overview |
   | `**/test*`, `*.md`, `.github/**` | Low impact |

5. **Assess demo impact** — read `demos/<agent>/README.md` to find completed demos (`[x]`). For each demo:
   - Read `demos/<agent>/<demo>/README.md` for source file references (look for lines like `核心源码:`, code file paths in "原理" or "相关文档" sections)
   - Match referenced files against changed files in the compare diff
   - If no explicit reference, use fuzzy match: demo name ↔ changed file name
   - Report which demos may need updating

6. **Output structured report**:

```
## <agent-name>

**Status**: ⚠️ DRIFT DETECTED (N commits behind)
**Analyzed at**: <commit_short> (<date>)
**Upstream HEAD**: <remote_short> (<date>)
**Compare**: <github_compare_url>

### 文档影响
- **高影响维度**: D2, D3（核心文件变更）
- **低影响维度**: D1（仅文档变更）
- **无影响维度**: D4, D5, D6, D7, D8

### Demo 影响
- ⚠️ **repomap**: `aider/repomap.py` 有 +30/-10 行变更 → 可能需要更新 demo
- ✅ **search-replace**: 相关文件无变更
- ✅ **reflection**: 相关文件无变更
- ⚠️ **architect**: `aider/coders/architect_coder.py` 有变更 → 可能需要更新 demo

### 建议
- [ ] 更新 submodule: `npm run update -- <agent>`
- [ ] 重新审查 D2, D3 部分
- [ ] 检查 repomap, architect demo 是否需要更新
- [ ] 或运行 `/check-updates --stamp <agent>` 确认当前内容仍有效
```

For agents that are up to date:
```
## <agent-name>

**Status**: ✅ UP TO DATE
**Analyzed at**: <commit_short> (<date>)
```

## Mode 2: Stamp

`/check-updates --stamp <agent-name>`

Update commit tracking after reviewing changes or completing a re-analysis.

### Steps

1. **Read current HEAD** from `projects/<agent-name>/`:
   ```bash
   git -C projects/<agent-name> rev-parse HEAD
   ```
   If the submodule doesn't exist, abort with error.

2. **Update agents.yaml** — set `analyzed_commit` and `analyzed_date` (today's date) for the agent.

3. **Update doc header** — in `docs/<agent-name>.md`, update the `> Analyzed at commit:` line with the new SHA and date. If the line doesn't exist, add it after the `> Repo:` line.

4. **Update demo overview** — in `demos/<agent-name>/README.md`, update the `> Based on commit:` line with the new SHA and date. If the line doesn't exist, add it after the first description paragraph.

5. **Report** what was updated.

## Key Design Decisions

- Uses `gh api` instead of local `git log` to avoid shallow clone limitations
- Check mode is read-only — it does NOT update the submodule or any files
- File→dimension mapping is assessed by Claude using the pattern table above as guidance
- Demo impact assessment uses source file references in demo READMEs + fuzzy file name matching

## MVP Coverage Hint

If the agent's demo overview (`demos/<agent>/README.md`) uses the three-tier format (MVP 组件/进阶机制/完整串联), append a line at the end of the report:

```
> 💡 如需检查 MVP 覆盖缺口，运行 `/audit-coverage <agent>`
```
