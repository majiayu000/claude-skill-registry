---
name: memo-kontext
description: 双层结构化长效记忆专家 (Kontext-Aware)
---

# Kontext 专家技能 (kontext-expert)

本技能旨在为 Agent (Antigravity) 提供**持久化的双层结构化记忆**. 它通过“数据层”保证逻辑严密性，通过“表现层”提供人类可读的视觉概览，解决长周期任务中的记忆流失问题。

> [!IMPORTANT]
> **核心价值**: 当会话上下文过长导致 Agent 产生“幻觉”或“健忘”时，通过该技能将零散信息“固化”为 **Kontext (上下文珠子)**，并同步生成 Mermaid 依赖图，确保逻辑链条的绝对可靠。

## 1. 核心概念

- **双层记忆 (Dual-Layer Memory)**:
    - **Data Layer (JSONL)**: 存储原始数据，保证哈希 ID (`kx-a1b2`) 和依赖关系的机器可读性。
    - **View Layer (Markdown)**: 在 `.kontext/README.md` 中动态展示 Mermaid 依赖图和高风险标记。
- **Zero Conflict (零冲突)**: 基于哈希的短 ID 确保多 Agent/多分支协作时任务标识不冲突。
- **无损传递**: 通过 Git 驱动的 `.kontext/` 目录，让不同会话之间能无损接收任务上下文。

## 2. 自动化触发条件与常用语

### 推荐触发语 (记忆整理视角)

- **记忆固化**: "整理记忆", "强调记忆".
- **对抗遗忘**: "整理长期记忆", "整理上下文".
- **逻辑对齐**: "同步记忆", "恢复记忆", "展示记忆".
- **任务收官**: "持久化记忆", "打包记忆", "打包上下文".

## 3. 文件存放规范

1. **技能资源**: 脚本 (如 `id_gen.py`) 存放在 `${SKILL_DIR}/scripts/`.
2. **项目数据**: 产生的任务数据文件 (如 `.kontext/` 目录), **必须存放于项目根目录**, 随 Git 版本控制走。

## 4. 操作流程

### A. 初始化 (Init)

- 在项目根目录下创建 `.kontext/` 目录。
- 创建初始 `README.md` (表现层) 和 `issues.jsonl` (数据层)。

### B. 记录 Kontext (Create)

- 调用 `${SKILL_DIR}/scripts/id_gen.py` 生成以 `kx-` 为前缀的哈希 ID。
- 将节点存入 `issues.jsonl` 并同步更新 `README.md` 中的 Mermaid 图表。

### C. 依赖关联与更新

- 使用 `dependencies` 维护逻辑严密性，更新 `status` 保持记忆的新鲜度。

### D. 就绪检查 (Ready)

- 定期扫描 `README.md` 中的“待办/阻塞”状态，确保 Agent 始终聚焦于当前可执行动作。

## 5. 提示词建议

- "深度记忆整理, 防止逻辑混乱"
- "当前的上下文太长了, 请将记忆结构化存储"
- "展示一下目前的长期记忆依赖图"
