---
name: all-my-ai-needs-precommit-gate
description: 在 all-my-ai-needs 仓库执行“可否提交”前置门禁：完整性/隐私扫描/同步一致性/技能验证，并输出可提交结论。
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [git, pre-commit, all-my-ai-needs, sync, security]
---

# all-my-ai-needs 提交前门禁

## Trigger
当用户在 `all-my-ai-needs` 仓库询问“是否可以提交/能不能 commit/提交前检查”时使用。

## 核心结论口径
- **可以提交**：未发现阻塞项（完整性+隐私+结构一致性通过），允许进入 `git add/commit`。
- **暂不建议提交**：发现阻塞项（坏 diff、疑似密钥、明显漏同步、关键校验失败）。

## Steps
1) 基础状态检查
```bash
cd /path/to/all-my-ai-needs
git rev-parse --show-toplevel
git branch --show-current
git status --short
git status --ignored --short
```

2) 仓库硬性门禁（按 AGENTS.md，默认只读）
```bash
git diff --check
git diff --cached --check
git grep -nEI "AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|sk-[A-Za-z0-9]{20,}|PLAYWRIGHT_MCP_EXTENSION_TOKEN\\s*=\\s*\\\"[^<\\\"]+\\\"|x-api-key\\s*[:=]\\s*\\\"[^<\\\"]+\\\"" || true
git grep -nE "playwright/scripts/playwright_cli\\.sh|playwright/references/cli\\.md|playwright/references/workflows\\.md|\\$PWCLI\\b|@playwright/cli\\b" || true
git ls-files -o --exclude-standard -z | xargs -0 -r rg -nEI "AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|sk-[A-Za-z0-9]{20,}|PLAYWRIGHT_MCP_EXTENSION_TOKEN\\s*=\\s*\\\"[^<\\\"]+\\\"|x-api-key\\s*[:=]\\s*\\\"[^<\\\"]+\\\"" || true
```

3) staged 视角 whitespace 复查（不污染当前 index）
```bash
TMP_INDEX="$(mktemp)"
GIT_INDEX_FILE="$TMP_INDEX" git add -A
GIT_INDEX_FILE="$TMP_INDEX" git diff --cached --check
rm -f "$TMP_INDEX"
```
说明：很多 whitespace 问题（尤其是新文件）在未暂存阶段不一定暴露；用临时 index 复查可避免改动用户当前暂存区。

4) 改动概览
```bash
git diff --stat
git diff --cached --stat
```
- 若 `staged=0`，明确提示“当前可提交但尚未暂存，直接 commit 不会成功”。

5) 同步一致性门禁（all-my-ai-needs 特有）
- Codex/Claude：比较仓库与本地运行目录受管路径差异，重点识别“本地有应回写仓库的新内容”。
- Hermes：优先使用受管判定脚本，不再按目录名猜测：
```bash
bash platforms/hermes/scripts/managed_skills.sh status
bash platforms/hermes/scripts/managed_skills.sh likely-custom
bash platforms/hermes/scripts/managed_skills.sh official-review
bash platforms/hermes/scripts/managed_skills.sh unmanaged-repo
```
- 结果解释：
  - `likely-custom` 非空：优先作为回流候选（通常阻塞“可提交”）。
  - `official-review` 非空：进入人工审查清单（通常非阻塞）。
  - `unmanaged-repo` 非空：本地磁盘缺失的删除候选，必须人工确认。
  - `Repo Skills Not In Local Source (Present On Disk / Likely builtin-hub)`：通常非阻塞，不作为删除依据。

6) 新增 skill 的最小可用验证（若本次包含技能新增）
- 检查关键文件：`SKILL.md`（必需）；`runtime.yaml` / `README.md` 按平台规范检查（存在则校验，不强制每个 skill 都有）。
- 执行技能自带验证脚本（如 `scripts/validate-svg.sh`）。
- 若脚本中声明外部依赖缺失（例：`rsvg-convert`），可记为**非阻塞警告**，但需在结论里注明。

7) 收尾检查（必须）
```bash
git status --short
```
- 确认改动范围与结论一致，再输出“可提交/暂不建议提交”最终结论。

## 输出模板（建议）
- 结论：可提交 / 暂不建议提交
- 阻塞项：逐条列出（没有则写“无”）
- 警告项：依赖缺失、未暂存等
- 改动摘要：修改/新增数量、主要路径
- 同步清单：新增、更新、删除、跳过/未同步项
- 下一步：
  - 可提交时：建议 `git add ...` + commit message 规范（Conventional Commits + `[更新摘要]`）
  - 阻塞时：给出最短修复路径

## Pitfalls
- `git grep` 只扫已跟踪文件，未跟踪文件必须额外扫描，避免漏报。
- 不要在门禁阶段直接执行 `git add -A` 改写用户暂存区；优先使用临时 index 进行 staged 视角检查。
- `managed_skills.sh` 的 “Repo Skills Not In Local Source (Present On Disk / Likely builtin-hub)” 不是删除候选，不能据此删仓库 skill。
- `runtime.yaml` 应保留在仓库，不应要求同步到运行目录。
- `~/.hermes/cron` 常有运行态文件（如 `.tick.lock`、`output/`），通常不应作为阻塞。
- 校验脚本“部分步骤 skipped（依赖缺失）”不等于失败，需区分阻塞/非阻塞。
- 不主动执行 `git push`；仅在用户明确要求时执行。

## Done Criteria
- 已完成 AGENTS 规定的提交前检查。
- 明确给出“是否可提交”的单句结论。
- 输出中包含阻塞项/警告项/下一步，并附同步内容清单（新增/更新/删除/跳过）。
- 收尾已执行 `git status --short` 并确认改动范围与结论一致。
- 若涉及同步任务，向用户列出新增、更新、删除、跳过/未同步项。
