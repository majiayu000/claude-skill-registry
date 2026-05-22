---
name: gitlab-mr-issue
description: 查看/更新 GitLab Issue、MR（含评论与 diff），并按团队规范非交互创建或修改 MR/Issue；涉及 GitLab（含自建实例）Issue/MR 的操作时使用。
---

# GitLab CLI Skill（MR/Issue）

## 基本准备
- 确认身份与认证：
  - `glab auth status` 读取当前实例及 “Logged in to <host> as <user>” 行。
  - 直接取用户名：`GITLAB_HOST=<host> glab api /user | jq -r '.username'`（依赖本机 `jq`，若已设全局 `GITLAB_HOST` 可直接 `glab api /user`）。
  - 自建实例优先通过环境变量 `GITLAB_HOST` 指定；如需单次覆盖，可在命令前加 `GITLAB_HOST=<host>` 或用 `-R group/project`。
- 输出格式默认够用，若需机器可读用 `--output json`。
- 创建 MR 或 Issue 成功后，在终端**单独一行**输出 CLI 返回的完整 URL。

## Issue 快速查看
- 只看正文：`glab issue view <id|url>`.
- 带讨论：`glab issue view <id|url> --comments`（必要时加 `--system-logs`）。
- 列表：`glab issue list --state opened --per-page 50 [-R group/project]`；过滤标签用 `--label foo,bar`。
- 添加评论：`glab issue note <id> -m "comment"`。

## MR 快速查看
- MR 概览（按需取字段）：`glab mr view <id|branch|url> --output json | jq -r '.title,.state,.author.username,.web_url,.description'`。
- 查看 diff：`glab mr diff <id|branch> --color=never`；需要原始 patch 用 `--raw`。
- 相关 issue：`glab mr issues <id>`。

## 创建 MR（非交互）
以下标题与描述规范为默认推荐格式；如与团队/仓库/平台等既有约束冲突，以既有约束为准。若有明确要求（如需中文），则优先遵循；未覆盖的部分再按本规范补齐。
1) 确保本地分支已推送且 `git status` 干净。  
2) 标题风格：英文、遵循语义化提交规范（如 `feat(scope): short summary`），保持简洁且描述核心目的；即使标题要求中文，语义化前缀（如 `feat`、`fix`）仍需英文。  
3) 描述风格：英文、短句和项目符号，优先让不看代码的读者也能理解动机与结果。重点是 what/why/impact 与必要约束，避免流水账与开发过程细节。若上下文不足以明确目标或约束，应主动向开发者确认后再撰写。涉及专有名词、函数名、方法名、类名、API 名称或配置键时，使用 inline code（反引号）包裹以提升可读性与准确性。  
4) 期望正文格式（精简但信息完整，按需删减无关块）：
- `## Summary`：用 1-2 条短句从功能层面概述目的与影响，强调功能变更而非逐条代码变更；跨层（如 Service/DAO）且语义一致的改动应合并为一次功能描述。
- `## Key changes`：3-5 条要点列出主要变更。
- `## Constraints / tradeoffs`：若存在约束、限制或非理想选择，简要说明。
- `## Testing`：验证方式、命令或场景；未测试需注明原因。
- `## Notes`（可选）：review 关注点、发布注意事项或后续计划。
5) 特别强调：描述应聚焦 MR 合并前后系统的变化与影响，避免记录开发中的中间过程或修改步骤。
6) 用 heredoc 传多行描述，避免交互式编辑：
```
glab mr create \
  --title "feat(scope): short summary" \
  --description "$(cat <<'EOF'
# 按上面的格式填充正文
EOF
)" \
  --target-branch main \
  --source-branch $(git branch --show-current) \
  --label bugfix \
  --draft \
  --yes
```
- 推荐参数（可按需开启）：`--remove-source-branch`（合并后删源分支）、`--squash-before-merge`（合并前压缩为单一 commit）；若团队偏好可省略。  
- 其他常用参数：`--reviewer user1,user2`、`--allow-collaboration`。  
- 修改已建 MR：`glab mr update <id> --title "..."
  --description "$(cat <<'EOF'\n...\nEOF\n)" --label ... --yes`。

## Issue 创建（非交互）
- 命令模式与 MR 类似，使用 `--title` 与 heredoc 描述：  
```
glab issue create \
  --title "feat: short summary" \
  --description "$(cat <<'EOF'\n- context\n- expected\nEOF\n)" \
  --label backlog,team-x \
  --assignee user1 \
  --yes
```
- 若需私密：加 `--confidential`；截止日期 `--due-date YYYY-MM-DD`。

## 常见选项速记
- `-R group/project`：指定自建实例项目，等价于完整 URL。
- `--per-page` 与 `--page`：分页查看列表或评论时使用。

## 更新 Issue/MR 标题或描述（前置要求）
在更新 Issue 或 MR 的标题/描述之前，必须先读取当前标题/正文（即将被修改的内容），再进行修改。
