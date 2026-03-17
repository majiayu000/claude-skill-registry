---
name: git-commit
description: 当用户明确要求"提交 Git 改动"、"生成 commit 信息"或"创建 git commit"时使用。仅用 Git 分析改动并自动生成 conventional commit 信息（可选 emoji）；必要时建议拆分提交，默认运行本地 Git 钩子（可 --no-verify 跳过），提交后默认自动 push（可 --no-push 跳过）。
metadata:
  author: Bensz Conan
  short-description: 仅用 Git 分析改动并生成 conventional commit 信息（可选 emoji），默认自动 push
  keywords:
    - git-commit
    - git commit
    - conventional commit
    - commit message
category: normal
---

# Git Commit

仅用 Git 分析改动并自动生成 conventional commit 信息（可选 emoji）；必要时建议拆分提交，默认运行本地 Git 钩子（可 --no-verify 跳过），提交后默认自动 push（可 --no-push 跳过）。

## 工作模式

本技能支持两种工作模式：

| 模式 | 触发方式 | 行为特征 |
|------|----------|----------|
| **自动模式** | 默认（无参数） | AI 自主决策所有步骤：自动暂存、自动拆分、直接提交 |
| **审核模式** | `--review` 参数 | 在关键决策点暂停，等待用户确认暂存方式、拆分建议、提交信息 |

**默认使用自动模式**，因为大多数情况下 commit 的顺利提交比内容本身更重要；如不满意可直接回退。

## 触发场景

- 用户要提交代码改动
- 需要生成符合规范的提交信息
- 需要判断是否应该拆分提交
- 需要包含 emoji 的提交信息

## 工作流程

### 1. 仓库/分支校验

- 通过 `git rev-parse --is-inside-work-tree` 判断是否位于 Git 仓库
  - **如不在 Git 仓库**：提示 `git init` 初始化仓库后继续
- 读取当前分支/HEAD 状态：
  - **如处于 detached HEAD 状态**：提示风险并确认是否继续
    - 检测方法：`git rev-parse --symbolic-full-name HEAD` 返回 `HEAD`
    - 提示内容："⚠️ 当前处于 detached HEAD 状态，提交将不属于任何分支。建议先创建分支（`git switch -c <branch-name>`）或切换到现有分支（`git switch <branch-name>`）"
  - **如处于 rebase/merge 冲突状态**：给出明确指导
    - **检测到 Git 冲突**：当前处于 rebase/merge 冲突状态，请先处理冲突：
      1. 查看冲突文件：`git status`
      2. 解决冲突（编辑标记为 `<<<<<<<` 的文件）
      3. 标记冲突已解决：`git add <冲突文件>`
      4. 继续 rebase/merge：`git rebase --continue` 或 `git merge --continue`
      5. 完成后重新运行 git-commit
    - 或跳过当前提交：`git rebase --skip`
    - 或中止 rebase/merge：`git rebase --abort` / `git merge --abort`

### 2. 改动检测

- 用 `git status --porcelain` 与 `git diff` 获取已暂存与未暂存的改动
  - **如无改动**：提示 "当前无改动，无需提交"，退出
- 额外检测 **未跟踪文件（untracked）**：用 `git ls-files --others --exclude-standard` 列出未跟踪且未被忽略的文件
- 若存在未跟踪文件：
  - **自动模式**（默认）：
    - 若暂存区为空：自动执行 `git add -A`（除非传入 `--no-all` 或 `--no-untracked` 跳过）
    - 若暂存区非空：仅暂存未跟踪文件（除非传入 `--no-untracked` 跳过）
      - 先获取列表：`git ls-files --others --exclude-standard`
      - 再执行：`git add -- <untracked_paths...>`
      - 如路径可能包含空格/特殊字符：用 NUL 分隔更稳妥
        - `git ls-files --others --exclude-standard -z | xargs -0 git add --`
      - 说明：此操作不会影响你已暂存/未暂存的其他改动，只是把“新文件”补进暂存区，避免漏提交
  - **审核模式**：提示用户选择：
    - **选项 1**：暂存所有改动（`git add -A`）
    - **选项 2**：仅暂存未跟踪文件（`git add -- <untracked_paths...>`）
    - **选项 3**：暂存部分文件（`git add <path>...`）
    - **选项 4**：取消命令，手动分组暂存后重试
- 若暂存区为空且无未跟踪文件：
  - **自动模式**：自动执行 `git add -A`（除非传入 `--no-all` 跳过）
  - **审核模式**：提示用户选择暂存方式（同上）

### 3. 拆分建议

按以下决策树判断是否需要拆分提交：

**1. 强制拆分条件**（任一满足则建议拆分）：
- 超过规模阈值：改动行数 > 300 行或跨越目录数 > 5 个
- 多种提交类型：包含 2 种以上不同类型的改动（如 feat + fix）
- 多个独立功能：改动涉及 2 个以上互不相关的功能模块

**2. 建议拆分条件**（不满足强制条件时）：
- 文件类型混合：源代码 + 文档/测试在同一提交
- 可回滚性差：单个提交回滚会影响其他功能

**3. 单一提交条件**（以上都不满足）：
- 改动规模适中（< 300 行）
- 单一功能模块
- 单一提交类型
- 可独立回滚

若检测到多组独立变更或 diff 规模过大：
- **自动模式**：按分组自动执行多次提交（不询问）
- **审核模式**：给出每一组的 pathspec 拆分建议，询问是否接受

### 4. 提交信息生成

#### 格式规范

遵循 Conventional Commits 规范：

```
[<emoji>] <type>(<scope>)?: <subject>

<body>

<footer>
```

#### 类型（type）

详见 config.yaml 中的 `commit_types` 定义。

#### Emoji 映射（使用 --emoji 时）

详见 config.yaml 中的 `emoji_map` 定义。

#### 自动识别 type 和 scope

**type 自动识别**：根据改动内容自动识别（如新增功能 → feat，修复缺陷 → fix）

**scope 自动识别**：
- 取改动文件的最上层模块名（如改动 `src/auth/login.ts` → scope 为 `auth`）
- 如跨越多个模块，省略 scope（如 `feat: add user feature`）
- 用户可通过 `--scope` 参数覆盖自动识别的 scope

#### 内容要求

- **主题行**：首行 ≤ 72 字符，祈使语气，使用动词开头
- **正文**：
  - 必须在 subject 之后空一行
  - 使用列表格式，每项以 `-` 开头
  - 每项必须使用动词开头的祈使句
  - 禁止使用冒号分隔的格式（如 "Feature: description"）
  - 说明变更的动机、实现要点或影响范围（3 项以内为宜）
- **脚注**：
  - 必须在 Body 之后空一行
  - 破坏性变更：`BREAKING CHANGE: <description>`
  - 其它采用 git trailer 格式（如 `Closes #123`）

#### 破坏性变更检测与处理

**检测规则**（满足任一条件即为破坏性变更）：
- 删除了公开 API（函数、类、方法）
- 修改了公开 API 的签名（参数、返回值）
- 修改了配置文件的格式
- 删除了配置项或改变了配置项的语义
- 数据库 schema 变更（不兼容旧版本）

**处理方式**：
- 在 type 后添加感叹号标记，如 `feat(api)!: redesign authentication API`
- 在脚注中说明 `BREAKING CHANGE: <description>`
- 建议将破坏性变更拆分为独立提交（如与修复混在同一提交）

#### 语言选择

按以下优先级**动态检测**提交信息语言：

1. **用户明确指定**：通过 `--lang zh` 或 `--lang en` 参数临时切换语言
2. **最近 5 次 commit 的主体语言**：
   - 执行 `git log -n 5 --pretty=%s` 获取最近 5 次提交的主题行
   - 统计各语言出现次数，以**多数为准**（如 3 次中文 + 2 次英文 → 使用中文）
   - 平局时（如 2 次 + 2 次 + 1 次其他）优先使用设备默认语言
3. **设备默认语言**（当仓库无 commit 时）：
   - 检测环境变量 `$LANG`（macOS/Linux）或系统语言设置
   - 如检测到 `zh_CN`、`zh_TW`、`zh_HK` 等 → 使用简体中文
   - 其他情况 → 使用英文

**检测示例**：
```bash
# 获取最近 5 次 commit 主题
git log -n 5 --pretty=%s

# 检测设备语言
echo $LANG  # 例如：zh_CN.UTF-8 → 中文；en_US.UTF-8 → 英文
```

### 5. 执行提交

- **自动模式**：
  - 单提交场景：直接执行 `git commit [-S] [--no-verify] [-s] -F .git/COMMIT_EDITMSG`
  - 多提交场景：按分组自动依次执行 `git add <paths> && git commit ...`
- **审核模式**：
  - 单提交场景：显示生成的 commit message，询问是否确认后再提交
  - 多提交场景：给出每一组的 `git add <paths> && git commit ...` 指令，询问是否执行

### 6. 自动推送

提交成功后，默认自动执行 push：

- **自动模式**：提交成功后直接执行 `git push`（除非传入 `--no-push`）
- **审核模式**：提交成功后询问是否推送
- **推送前检查**：
  - 检查当前分支是否有上游分支：`git rev-parse --abbrev-ref --symbolic-full-name @{u}`
  - 如无上游分支：自动执行 `git push -u origin <branch>` 设置上游并推送
  - 如有上游分支：直接执行 `git push`
- **推送失败处理**：
  - 如推送被拒绝（远程有新提交）：提示用户先拉取（`git pull --rebase`）后再推送
  - 如无推送权限：提示用户检查远程仓库配置

### 7. 安全回滚

### 7. 安全回滚

如误暂存，可用 `git restore --staged <paths>` 撤回暂存（命令会给出指令）

如误提交（未推送），可用 `git reset --soft HEAD~1` 撤回提交（保留改动）

如已推送，需使用 `git revert` 创建反向提交（避免强制推送）

## 使用参数

### 模式控制

- `--review`：启用审核模式（在关键决策点暂停，等待用户确认）
- `--no-all`：在自动模式下跳过自动暂存（包括自动 `git add -A` 与自动补齐未跟踪文件）
- `--no-untracked`：在自动/审核模式下不自动处理未跟踪文件（避免把“新文件”自动加入暂存区）

### 提交控制

- `--no-verify`：跳过本地 Git 钩子
- `--no-push`：提交后不自动推送（仅本地提交）
- `--amend`：修补上一次提交（⚠️ 危险操作：仅在未推送的本地分支使用，已推送的分支使用会导致历史不一致）
- `--signoff`：附加 `Signed-off-by` 行

### 内容控制

- `--emoji`：在提交信息中包含 emoji 前缀
- `--scope <scope>`：指定提交作用域
- `--type <type>`：强制提交类型
- `--lang <zh|en>`：临时指定提交信息语言（覆盖自动检测）

## 输出示例

### 使用 emoji

```
✨ feat(ui): add user authentication flow

- implement Google and GitHub third-party login
- add user authorization callback handling
- improve login state persistence logic

Closes #42
```

### 不使用 emoji

```
feat(auth): add OAuth2 login flow

- implement Google and GitHub third-party login
- add user authorization callback handling
- improve login state persistence logic
```

### 包含破坏性变更

```
feat(api)!: redesign authentication API

- migrate from session-based to JWT authentication
- update all endpoint signatures
- remove deprecated login methods

BREAKING CHANGE: authentication API has been completely redesigned, all clients must update their integration
```

### 拆分提交示例

**自动模式**：自动执行以下三个提交（不询问）

**审核模式**：检测到多组独立变更，建议拆分为以下提交：

#### 提交 1：feat(ui): add user authentication flow
```bash
git add src/components/LoginForm.tsx src/hooks/useAuth.ts
git commit -m "feat(ui): add user authentication flow

- implement login form with email and password fields
- add authentication state management hook

Closes #42"
```

#### 提交 2：fix(api): resolve token validation error
```bash
git add src/api/auth.ts
git commit -m "fix(api): resolve token validation error

- add proper error handling for expired tokens
- update token refresh logic"
```

#### 提交 3：docs(auth): update authentication documentation
```bash
git add docs/auth-guide.md
git commit -m "docs(auth): update authentication documentation

- add OAuth2 integration guide
- update troubleshooting section"
```

## 重要约束

- **仅使用 Git**：不调用任何包管理器/构建命令
- **尊重钩子**：默认执行本地 Git 钩子；使用 `--no-verify` 可跳过
- **默认推送**：提交成功后默认自动 push；使用 `--no-push` 可跳过
- **不改源码内容**：命令只读写 `.git/COMMIT_EDITMSG` 与暂存区
- **安全提示**：在 rebase/merge 冲突、detached HEAD 等状态下会先提示处理/确认再继续
