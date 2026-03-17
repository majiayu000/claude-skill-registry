---
name: understand
description: 深度分析当前项目的架构、Agent 配置及 MCP 集成，生成中文架构文档。
---

# Understand Project Skill

## Instructions
当用户运行此 skill 时，请扮演一名**资深 AI 架构师**，执行以下步骤：

1. **信息搜集 (侦探模式)**：
   - 浏览项目文件结构 (`ls -R`)。
   - 读取 `requirements.txt` / `config.py` 等关键文件确定依赖。
   - **关键步骤**：使用 `grep` 寻找 "mcp", "LangChain", "tool", "agent" 等关键字。

2. **撰写报告 (必须使用中文)**:
   - 加载本 Skill 目录下的 `template.md` 作为大纲。
   - **语言要求**：所有解释性文字**必须使用中文**，保留专业术语（如 LangChain, MCP）为英文。
   - **代码引用**：必须引用真实存在的代码片段。

3. **交付结果 (强制存档)**:
   - **Step A**: 检查根目录下是否有 `docs/` 目录，如果没有，请使用 `mkdir` 创建它。
   - **Step B**: **必须调用写文件工具**，将填充好的内容保存为 `docs/ARCHITECTURE.md`。不要只在聊天框输出，**必须落地为文件**。
   - **Step C**: 文件保存成功后，向用户简要汇报：“报告已生成并保存至 docs/ARCHITECTURE.md”，并列出 2 个最核心的架构亮点。

## Additional resources
- 架构分析模版: [template.md](template.md)