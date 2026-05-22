---
name: commit-convention
description: Git 提交信息规范。着重于提交信息的格式化、风格统一。优先学习并沿用项目已有的提交历史风格，若无明显风格或为新项目，则遵循 Conventional Commits 规范。
user-invocable: false
allowed-tools: Bash, Read, Grep
---

# Commit Convention

该 Skill 不直接执行 `git commit` 或 `git add` 操作，而是为当前 Agent 提供提交信息的**决策指导**和**格式标准**。

## 核心策略

### 1. 风格学习（优先）
在生成提交信息前，必须先观察项目已有的提交习惯：
- 执行 `git log -n 5 --oneline`。
- **匹配历史**：如果项目习惯使用特定的前缀（如 `[FEAT]`、`Update:` 等）或语言习惯，应优先模仿并保持一致。
- **语言一致性**：如果历史记录全是中文，则使用中文描述；如果全是英文，则使用英文。

### 2. 规范回退（Fallback）
如果项目提交记录为空、无明显规律，或项目明确要求使用规范化提交，请遵循 **Conventional Commits** 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type 类型定义
- `feat`: 新功能
- `fix`: 修补 bug
- `docs`: 文档变更
- `style`: 不影响代码含义的变更（空白、格式、缺少分号等）
- `refactor`: 重构（既不是修复 bug 也不是添加特征的代码更改）
- `perf`: 改进性能
- `test`: 添加缺失测试或更正现有测试
- `build`: 影响构建系统或外部依赖项的更改
- `ci`: 更改 CI 配置文件和脚本
- `chore`: 其他不修改 src 或测试文件的更改
- `revert`: 回退之前的提交

#### Subject 格式
- 使用祈使句（如 "add" 而不是 "added"）。
- 结尾不加句号。
- 首字母小写（除非是专有名词）。
- 长度控制在 50 字符以内。

## 操作指令 (仅供 Agent 参考)

当 Agent 需要生成提交信息时，应按以下逻辑思考：

1. **观察**：使用 `git log -n 5 --oneline` 观察项目风格。
2. **判断**：
   - 发现既定规律？→ 模仿该规律。
   - 发现 Conventional Commits 模式？→ 遵循本规范。
   - 初始提交/无规律？→ 采用 Conventional Commits。
3. **撰写**：
   - 简洁的 Subject。
   - 必要时提供 Body（解释 **Why** 而不是 How）。
   - 关联 Issue（如 `Closes #123`）。

## 注意事项
- **严禁过度设计**：不要生成过于复杂的提交信息，除非变更确实复杂。
- **原子性**：建议一个提交只做一件事。如果发现变更过多，建议提示用户拆分提交。
- **禁止执行命令**：本 Skill 仅提供“信息建议”，执行操作由主 Agent 决定。
