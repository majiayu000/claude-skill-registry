---
name: skill-lifecycle
description: Skill 生命周期管理的 Workflow。当需要创建新 Skill 并持续优化时触发。触发词：创建并优化 skill、skill 生命周期、从零开始创建 skill、新建一个完整的 skill。
---

# Skill 生命周期

创建和持续优化 Skill 的完整流程。

## 流程概览

```
clarify → research → create → evaluate → iterate(循环) → version
```

## 详细步骤

### 1. clarify（澄清）

**目的**：理解用户想要什么

**执行**：调用 clarify-skill

**输出**：`workspace/goal.md`

**完成标志**：用户确认目标

### 2. research（调研）

**目的**：了解最佳实践

**执行**：调用 research-skill

**输入**：`workspace/goal.md`

**输出**：`workspace/research.md`

**完成标志**：调研报告完成

**可选**：如果领域简单或已有经验，可跳过

### 3. create（创建）

**目的**：生成 Skill 文件

**执行**：调用 create-skill

**输入**：`workspace/goal.md`、`workspace/research.md`

**输出**：
- `SKILL.md`
- `criteria.md`

**完成标志**：两个文件都存在且格式正确

### 4. evaluate（评价）

**目的**：评价 Skill 执行效果

**前置**：先执行一次 Skill，获得产出

**执行**：调用 evaluate-skill

**输入**：`criteria.md`、执行产出

**输出**：
- `.meta/evaluation.json`
- `workspace/evaluation.md`

**完成标志**：评价结果存在

### 5. iterate（迭代）- 循环

**目的**：根据评价改进 Skill

**触发条件**：`evaluation.json.pass == false` 或 `needs_iteration == true`

**执行**：调用 iterate-skill

**输入**：`evaluation.json`、`evaluation.md`、`SKILL.md`

**输出**：
- 更新的 `SKILL.md`
- `versions/SKILL.v{n}.md`（旧版本备份）

**循环**：回到 step 4（evaluate）

**退出条件**：
- `evaluation.json.pass == true` 且 `needs_iteration == false`
- 或达到 `max_iterations`

### 6. version（版本管理）- 可选

**目的**：A/B test 或版本切换

**执行**：调用 version-skill

**场景**：
- 有多个版本需要对比
- 需要回滚到之前版本
- 确认某个版本为正式版

## 状态管理

### status.json

```json
{
  "current_step": "evaluate",
  "completed_steps": ["clarify", "research", "create"],
  "iteration": 2,
  "max_iterations": 5,
  "skill_name": "weekly-report"
}
```

### 状态流转

```
clarify → research → create → evaluate
                                 ↓
                         pass? ──→ done
                           ↓ no
                        iterate
                           ↓
                    (back to evaluate)
```

## 目录结构

```
.sop-engine/skills/<skill-name>/
├── SKILL.md              # Skill 本身
├── criteria.md           # 评价标准
├── versions/             # 历史版本
│   ├── SKILL.v1.md
│   └── SKILL.v2.md
├── .meta/                # 元数据（Hook 读取）
│   ├── status.json
│   └── evaluation.json
└── workspace/            # 工作空间（自由）
    ├── goal.md
    ├── research.md
    └── evaluation.md
```

## 原则

- 每个步骤完成后更新 status.json
- 循环有上限，防止无限迭代
- 保留历史版本，支持回滚
- workspace 内容自由，.meta 格式严格
