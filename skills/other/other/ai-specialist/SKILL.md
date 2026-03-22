---
name: ai-specialist
description: 提供 AI 应用开发、MCP 服务器工程、提示词工程与智能体框架集成能力。当需要构建或优化基于大模型的功能、工作流或平台集成时使用。
---
# Ai Specialist

提供 AI 应用开发、MCP 服务器工程、提示词工程与智能体框架集成能力。当需要构建或优化基于大模型的功能、工作流或平台集成时使用。

## Skill Index

<!-- AUTO-GENERATED-SKILL-INDEX:START -->
以下索引由 `node scripts/update-skill-index.js` 自动生成，用于让 Claude 在顶层专家触发后继续路由到最相关的子技能。

### Claude 使用说明

1. 先将用户当前任务与每个子技能的 `触发语义` 进行语义匹配，不要只看目录名。
2. 一旦找到最相关的子技能，立即打开其 `入口文件` 指向的 `SKILL.md`，把它作为下一层入口。
3. 进入子技能后，再根据该子技能自己的说明按需加载同目录下的 `references/`、`scripts/`、`assets/`，不要在顶层专家中预先展开大段细节。
4. 如果多个子技能都相关，先加载最贴近主目标的那个，再按需补充其他子技能，避免一次性加载过多上下文。
5. 下方 `入口文件` 路径相对于项目根目录，可直接用于 `Read` 操作。

### 子技能索引

#### agents-orchestrator (1)
- `agents-orchestrator`
  - 触发语义: Autonomous pipeline manager that orchestrates the entire development workflow. You are the leader of this process.
  - 入口文件: `.claude/skills/ai-specialist/references/domains/agents-orchestrator/SKILL.md`

#### ai-data-remediation-engineer (1)
- `ai-data-remediation-engineer`
  - 触发语义: Specialist in self-healing data pipelines — uses air-gapped local SLMs and semantic clustering to automatically detect, classify, and fix data anomalies at scale. Focuses exclusively on the remediation layer: intercepting bad data, generating deterministic fix logic via Ollama, and guaranteeing zero data loss. Not a general data engineer — a surgical specialist for when your data is broken and the pipeline can't stop.
  - 入口文件: `.claude/skills/ai-specialist/references/domains/ai-data-remediation-engineer/SKILL.md`

#### ai-engineer (1)
- `ai-engineer`
  - 触发语义: Expert AI/ML engineer specializing in machine learning model development, deployment, and integration into production systems. Focused on building intelligent features, data pipelines, and AI-powered applications with emphasis on practical, scalable solutions.
  - 入口文件: `.claude/skills/ai-specialist/references/domains/ai-engineer/SKILL.md`

#### mcp-builder (1)
- `mcp-builder`
  - 触发语义: Expert Model Context Protocol developer who designs, builds, and tests MCP servers that extend AI agent capabilities with custom tools, resources, and prompts.
  - 入口文件: `.claude/skills/ai-specialist/references/domains/mcp-builder/SKILL.md`

#### mcp-server-engineering (1)
- `mcp-builder`
  - 触发语义: 创建高质量 MCP（模型上下文协议）服务器的指南，使 LLM 能够通过精心设计的工具与外部服务交互。在构建 MCP 服务器以集成外部 API 或服务时使用，无论是 Python (FastMCP) 还是 Node/TypeScript (MCP SDK)。
  - 入口文件: `.claude/skills/ai-specialist/references/domains/mcp-server-engineering/mcp-builder/SKILL.md`

#### model-qa (1)
- `model-qa-specialist`
  - 触发语义: Independent model QA expert who audits ML and statistical models end-to-end - from documentation review and data reconstruction to replication, calibration testing, interpretability analysis, performance monitoring, and audit-grade reporting.
  - 入口文件: `.claude/skills/ai-specialist/references/domains/model-qa/SKILL.md`

#### prompt-engineering (1)
- `Prompt Enhancer`
  - 触发语义: Transform vague prompts into actionable specs using intelligent analysis and session memory. Use when user input contains -e or --enhance flag.
  - 入口文件: `.claude/skills/ai-specialist/references/domains/prompt-engineering/prompt-enhancer/SKILL.md`

<!-- AUTO-GENERATED-SKILL-INDEX:END -->

## Notes

- 顶层 `SKILL.md` 仅做索引导航，不承载大体量细节内容。
- 详细资料下沉到 `references/domains/`，按树形结构组织。
