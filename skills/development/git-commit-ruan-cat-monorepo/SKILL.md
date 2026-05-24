---
name: git-commit
description: "创建高质量的 git 提交：审查/暂存预期的变更，拆分为逻辑提交，并编写清晰的提交信息（遵循 Conventional Commits 规范，支持 Emoji）。当用户要求提交代码、编写提交信息、暂存变更或将工作拆分为多个提交时使用此技能。"
user-invocable: true
metadata:
  version: "0.0.2"
---

# Git Commit

## 来源说明

该技能本质上是参考 [agent-toolkit/skills/commit-work](https://github.com/softaworks/agent-toolkit/blob/main/skills/commit-work/SKILL.md) 文档的纯中文翻译版本，并进行了特定改写以适应当前环境。

## 目标

制作易于审查且安全发布的提交：

- 仅包含预期的变更
- 提交具有逻辑范围（必要时进行拆分）
- 提交信息描述了变更内容和原因

## 需要询问的输入（如果缺失）

- **单个提交还是多个提交？**（如果不确定：当存在不相关的变更时，默认为多个小提交。）
- **提交风格**：必须使用 Conventional Commits，并包含 Emoji。
- **任何规则**：最大标题长度，必需的作用域。

## 工作流程（清单）

1. **在暂存前检查工作树**
   - `git status`
   - `git diff` (未暂存)
   - 如果变更较多：`git diff --stat`
2. **决定提交边界（必要时拆分）**
   - 拆分依据：功能 vs 重构，后端 vs 前端，格式化 vs 逻辑，测试 vs 生产代码，依赖升级 vs 行为变更。
   - 如果变更混合在一个文件中，计划使用补丁暂存 (`patch staging`)。
3. **仅暂存属于下一个提交的内容**
   - 对于混合变更首选补丁暂存：`git add -p`
   - 取消暂存块/文件：`git restore --staged -p` 或 `git restore --staged <path>`
4. **审查实际将要提交的内容**
   - `git diff --cached`
   - **合规性检查**：
     - 无密钥或令牌
     - 无意外的调试日志
     - 无不相关的格式化变动
5. **用 1-2 句话描述暂存的变更（在编写信息之前）**
   - "变更了什么？" + "为什么？"
   - 如果你无法清晰地描述它，那么提交可能太大或混合了；返回第 2 步。
6. **编写提交信息**
   - **必须**使用中文编写提交信息。
   - 使用 **Conventional Commits**（必需）：
     - `<emoji> type(scope): short summary`
     - (空行)
     - body (内容/原因，而非实现流水账)
     - footer (BREAKING CHANGE) 如果需要
   - **Emoji 和 Type 规范**：必须查阅并遵循 [commit-types.ts](https://raw.githubusercontent.com/ruan-cat/monorepo/dev/configs-package/commitlint-config/src/commit-types.ts) 中的定义。
     - **主动查阅**：使用 `Read` 或 `WebFetch` 工具主动读取上述文件以获取最新的 Emoji 和 Type 列表。
   - 对于多行信息首选编辑器：`git commit -v`
   - 参考 `references/commit-message-template.md` 获取完整的模板和 Emoji 列表。
7. **运行最小的相关验证**
   - 在继续之前运行仓库中最快且有意义的检查（单元测试、lint 或构建）。
8. **重复下一个提交，直到工作树干净**

## 交付物

提供：

- 最终的提交信息（包含 Emoji，中文编写）
- 每个提交的简短摘要（内容/原因）
- 用于暂存/审查的命令（至少：`git diff --cached`，加上运行的任何测试）
