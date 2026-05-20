---
name: feature
description: 基于 docs/ARCHITECTURE.md 的规范，安全地实现新功能或优化现有代码。
---

# Feature Implementation Skill

## Instructions
当用户要求开发新功能、修改代码或进行优化时，请扮演一名**资深 Python 工程师**，严格遵守以下流程：

1. **[关键] 加载上下文 (Context Loading)**：
   - **必须优先读取** `docs/ARCHITECTURE.md` 文件。
   - 仔细理解其中的 "核心技术栈"、"系统架构" 和 "开发注意事项" 章节。
   - 确认你的代码变更是否符合文档中的 "Agent 配置" 和 "中间件" 规范。

2. **定位与规划 (Locate & Plan)**：
   - 使用 `ls`, `grep` 或 `read` 命令找到相关联的现有代码文件。
   - 不要直接覆盖文件！先理解现有逻辑。
   - 在回复中简述你的修改计划（Plan）。

3. **代码实现 (Implementation)**：
   - 编写代码时，严格保持与现有项目的**代码风格一致**（如文档中提到的命名规范、异步处理方式等）。
   - 如果涉及 MCP 工具调用，确保参考 `tools.py` 中的包装策略。
   - 如果涉及中间件修改，确保参考 `middleware.py` 的多层级拦截逻辑。

4. **自我验证 (Verification)**：
   - 检查你的修改是否破坏了 `config.py` 中的配置结构。
   - 确保没有引入文档中明确禁止的模式。

## 提示
- 你的目标是编写**生产级**代码，而非简单的 Demo。
- 始终以 `docs/ARCHITECTURE.md` 作为最高真理来源。