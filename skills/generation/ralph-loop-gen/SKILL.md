---
name: "ralph-loop-gen"
description: "任务管理系统模板生成器 - 根据用户输入或JSON配置生成完整的任务管理结构（模板生成器，非直接执行器）"
---

# Ralph Loop Gen Skill

**任务管理系统模板生成器** - 根据用户输入或 JSON 配置生成完整的任务管理结构模板。

> ⚠️ **注意**：此 skill 仅生成任务模板文件，不负责实际执行任务。执行时需要其他 agent 手动或自动读取这些模板文件。

## 用法

### 方式 1: 命令行交互式输入

```bash
# 基本用法
bun ~/.pi/agent/skills/ralph-loop-gen/lib.ts

# 指定任务集名称
bun ~/.pi/agent/skills/ralph-loop-gen/lib.ts --name myProject

# 指定项目名称
bun ~/.pi/agent/skills/ralph-loop-gen/lib.ts --name myProject --project "我的项目"

# 指定输出目录
bun ~/.pi/agent/skills/ralph-loop-gen/lib.ts --name myProject --output ./task
```

### 方式 2: Python 脚本生成（推荐）

```bash
# 使用 Python 脚本从 JSON 生成任务
python3 ~/.pi/agent/skills/ralph-loop-gen/generate.py --config /path/to/tasks.json

# 指定输出目录
python3 ~/.pi/agent/skills/ralph-loop-gen/generate.py --config tasks.json --output ./task
```

### 输入格式

#### 格式 1: 简单列表（交互式输入）

```
任务1: 初始化项目结构
任务2: 安装依赖 -> 依赖: 任务1
任务3: 配置开发环境 -> 依赖: 任务2
任务4: 编写UI组件 (High, 4h) -> 依赖: 任务2
任务5: 编写API接口 (High, 4h) -> 依赖: 任务3
任务6: 集成测试 -> 依赖: 任务4, 任务5
```

#### 格式 2: JSON 配置（Python 脚本）

```json
{
  "taskSetName": "codmate-perf",
  "projectName": "CodMate 性能优化",
  "outputDir": "./task",
  "goals": [
    {"metric": "List 滚动 FPS", "before": "~30", "target": "60+", "improvement": "100%"},
    {"metric": "CPU 占用（空闲）", "before": "~15%", "target": "<5%", "improvement": "67%"}
  ],
  "tasks": [
    {
      "id": "001",
      "title": "建立性能基准测试",
      "priority": "High",
      "estimated": "3h",
      "description": "建立性能基准测试框架，用于量化优化效果",
      "steps": [
        "安装和配置 Instruments Time Profiler",
        "创建性能测试数据集（1000+ 会话）",
        "建立基准测试脚本（滚动、搜索、加载）",
        "记录当前性能指标（FPS、CPU、内存、响应时间）",
        "创建性能回归测试用例"
      ],
      "dependencies": [],
      "acceptance": [
        "性能测试脚本可运行",
        "基准数据已记录到 docs/performance-baseline.md",
        "测试数据集已创建"
      ]
    },
    {
      "id": "002",
      "title": "替换 SessionListColumnView 的 List 为 LazyVStack",
      "priority": "High",
      "estimated": "2h",
      "description": "将 SessionListColumnView 中的 List 组件替换为 LazyVStack，提升滚动性能",
      "steps": [
        "备份当前 SessionListColumnView.swift",
        "将 List + ForEach 替换为 ScrollView + LazyVStack",
        "保留 selection 绑定功能",
        "保留 Section header 功能",
        "保留 contextMenu 功能",
        "运行性能测试对比",
        "回归测试：选择、拖拽、右键菜单"
      ],
      "dependencies": ["001"],
      "acceptance": [
        "滚动 FPS 达到 60+（基准数据对比）",
        "选择功能正常",
        "拖拽功能正常",
        "右键菜单功能正常"
      ]
    }
  ]
}
```

## 输出结构

生成以下目录结构：

```
task/
└── {任务集名}/
    ├── 任务索引.md          # 任务总览、依赖关系、执行计划
    ├── 当前任务.md          # 当前待执行任务（指向第一个任务）
    ├── 任务001.md
    ├── 任务002.md
    ├── 任务003.md
    └── completed/           # 已完成任务目录
```

## 模板文件

模板文件位于 `templates/` 目录：

- `templates/index.md` - 任务索引模板
- `templates/task.md` - 单个任务模板

模板使用 `{{占位符}}` 语法，lib.ts/generate.py 会自动替换。

### index.md 模板变量

- `{{TOTAL_TASKS}}` - 总任务数
- `{{COMPLETED}}` - 已完成数量
- `{{IN_PROGRESS}}` - 进行中数量
- `{{TODO}}` - 待开始数量
- `{{LOCKED}}` - 已锁定数量
- `{{PROJECT_NAME}}` - 项目名称
- `{{CREATED_TIME}}` - 创建时间
- `{{TASK_ROWS}}` - 任务列表表格行
- `{{DEP_GRAPH}}` - 依赖关系图
- `{{PARALLEL_GROUPS}}` - 并行任务分组
- `{{PROGRESS_PERCENT}}` - 进度百分比
- `{{ELAPSED_TIME}}` - 已用时间
- `{{ESTIMATED_REMAINING}}` - 预计剩余时间
- `{{GOALS_TABLE}}` - 项目/性能目标表格（可选）
- `{{EXECUTION_PLAN}}` - 执行计划（可选）

### task.md 模板变量

- `{{TASK_ID}}` - 任务ID（如 任务001）
- `{{TASK_TITLE}}` - 任务标题
- `{{STATUS}}` - 任务状态
- `{{PRIORITY}}` - 优先级
- `{{ESTIMATED_TIME}}` - 预计时间
- `{{DESCRIPTION}}` - 任务描述
- `{{DEPENDENCIES_LIST}}` - 依赖任务列表
- `{{ACCEPTANCE_CRITERIA}}` - 验收标准
- `{{IMPLEMENTATION_STEPS}}` - 实施步骤
- `{{PARALLEL_HINT}}` - 并行提示
- `{{LOCK_OWNER}}` - 占用者
- `{{LOCK_TIME}}` - 锁定时间
- `{{LOCK_TIMEOUT}}` - 锁定超时

---

## 多 Agent 并行开发指南

### 依赖关系定义

在任务列表中指定依赖：

```
任务1: 基础设施 (无依赖)
任务2: 前端开发 -> 依赖: 任务1
任务3: 后端开发 -> 依赖: 任务1
任务4: 集成测试 -> 依赖: 任务2, 任务3
```

### 识别可并行任务

**规则**：如果两个任务依赖的相同任务，且彼此不依赖，则可并行。

**示例**：
- 任务2 依赖 任务1
- 任务3 依赖 任务1
- ✅ 任务2 和 任务3 可并行

### 手动调度策略

#### 策略 1：按批次执行

```
批次 1: 任务1 (所有 Agent 等待)
批次 2: 任务2 (Agent A) + 任务3 (Agent B) 并行
批次 3: 任务4 (等待批次2完成)
```

#### 策略 2：流水线执行

```
Agent A: 任务1 → 任务2 → 任务4
Agent B: 任务1 → 任务3 → 任务5
```

#### 策略 3：任务池模式

```
1. 将所有无依赖任务放入"待执行池"
2. 各 Agent 从池中取任务
3. 任务完成后，将依赖此任务的其他任务放入池
4. 重复直到所有任务完成
```

### 冲突避免

**文件级冲突**：
- 不同 Agent 修改同一文件 → 手动协调，或拆分任务
- 建议：在任务描述中明确涉及的文件

**分支管理建议**：
```bash
# 每个 Agent 使用独立分支
git checkout -b agent-a/task2
git checkout -b agent-b/task3

# 完成后合并到主分支
git checkout main
git merge agent-a/task2
git merge agent-b/task3
```

### 进度跟踪

定期查看 `task/{任务集名}/任务索引.md`：

1. 检查依赖任务是否都已完成
2. 更新任务状态
3. 识别下一个可执行任务

### 任务锁定机制

#### 锁定规则

1. **领用任务时立即锁定**
   ```bash
   # Agent A 领用任务002
   # 更新任务002.md
   状态: Locked → In Progress
   占用者: Agent A
   锁定时间: 2025-01-20 14:30:00
   ```

2. **同时更新任务索引**
   ```markdown
   | 002 | 任务标题 | Locked | ... | ... | Agent A | 14:30:00 |
   ```

3. **锁定超时释放**
   - 默认锁定时长：预计时间 × 2
   - 超时后自动释放，其他 Agent 可认领
   - 可在任务文件中调整锁定超时

4. **解锁条件**
   - 任务完成 → 状态更新为 `Done`，移至 `completed/` 目录
   - 阻塞 → 状态更新为 `Blocked`，释放锁定
   - 超时 → 自动释放
   - 手动释放：Agent 主动放弃

#### 锁定状态流转

```
Todo → Locked → In Progress → Done → [移至 completed/]
  ↓        ↓
Blocked  超时释放
```

#### 阻塞处理

**任务阻塞时**：

1. **记录阻塞原因**
   ```markdown
   ## 阻塞原因
   - 等待任务003完成（状态：In Progress）
   - 等待API密钥审批
   - 技术问题：需要解决XXX
   ```

2. **更新状态**
   - 状态：`In Progress` → `Blocked`
   - 释放锁定（占用者清空）

3. **Agent 选择**
   - 等待阻塞解除（推荐）
   - 认领其他可执行任务

**阻塞解除后**：

1. 检查依赖是否都完成
2. 重新锁定任务
3. 继续执行

#### 多 Agent 协作流程

```bash
# Agent A 开始工作
1. 读取 task/{任务集名}/任务索引.md
2. 查找状态为 Todo 的任务
3. 检查依赖任务是否都为 Done
4. 锁定任务（更新状态为 Locked，记录占用者）
5. 更新任务索引
6. 开始执行

# Agent B 同时开始工作
1. 读取 task/{任务集名}/任务索引.md
2. 查找状态为 Todo 的任务
3. 发现任务002已被 Agent A 锁定
4. 寻找下一个可执行任务
5. 锁定任务003
6. 开始执行

# 任务阻塞处理
1. Agent A 发现任务004被阻塞
2. 记录阻塞原因
3. 更新状态为 Blocked
4. 释放锁定
5. 查找其他可执行任务
```

### 示例：3 Agent 并行开发

```
任务列表：
001: 初始化项目 (无依赖)
002: 设计数据库 (依赖 001)
003: 设计 API (依赖 001)
004: 实现 API 接口 (依赖 003)
005: 实现前端页面 (依赖 003)
006: 编写单元测试 (依赖 004, 005)
007: 集成测试 (依赖 006)

调度方案：
阶段 1:
  - Agent A: 任务001 (3h)

阶段 2:
  - Agent A: 任务002 (2h)
  - Agent B: 任务003 (2h)

阶段 3:
  - Agent A: 任务004 (2h)
  - Agent B: 任务005 (2h)
  - Agent C: 等待

阶段 4:
  - Agent A: 任务006 (2h)
  - Agent B: 等待
  - Agent C: 等待

阶段 5:
  - Agent A: 任务007 (2h)

总耗时: ~11h (3 Agent 并行)
```

### 最佳实践

1. **任务粒度适中**：太大影响并行，太小增加协调成本
2. **明确依赖**：避免隐式依赖
3. **及时更新状态**：方便其他 Agent 判断是否可开始
4. **定期同步**：各 Agent 定期汇报进度
5. **预留缓冲**：考虑任务可能超时

---

## 进阶功能

### 批次自动分组

系统会根据依赖关系自动识别可并行批次，并在任务索引中显示：

```markdown
### 批次 1（可立即执行）
- 任务001: 建立性能基准测试 (Agent A)  ✅ 可并行执行

### 批次 2（等待批次1完成）
- 任务002: 替换 List 为 LazyVStack (Agent A)  ✅ 可并行执行
- 任务003: 优化动画性能 (Agent B)  ✅ 可并行执行
- 任务004: 搜索 debounce (Agent B)  ✅ 可并行执行
```

### 执行计划生成

系统会根据任务依赖和预计时间生成执行计划：

```markdown
## 执行计划（3 Agent 并行）

阶段 1: Agent A (3h)
└── 任务001: 建立性能基准测试

阶段 2: (3h)
├── Agent A: 任务002 (2h) + 等待 (1h)
├── Agent B: 任务003 (2h) + 等待 (1h)
└── Agent C: 任务004 (1.5h) + 任务005 (1.5h)

总耗时: ~18 小时（3 Agent 并行）
```

### 目标追踪

支持在任务索引中添加项目目标表格：

```markdown
## 性能优化目标

| 指标 | 优化前 | 目标 | 测量方法 |
|------|--------|------|----------|
| List 滚动 FPS | ~30 | 60+ | Instruments GPU/CPU |
| CPU 占用（空闲） | ~15% | <5% | Activity Monitor |
```

---

## 快速开始

### 1. 创建任务配置文件

```bash
# 创建 tasks.json
cat > tasks.json << 'EOF'
{
  "taskSetName": "my-project",
  "projectName": "我的项目",
  "outputDir": "./task",
  "tasks": [
    {
      "id": "001",
      "title": "初始化项目",
      "priority": "High",
      "estimated": "2h",
      "description": "初始化项目基础结构",
      "steps": [
        "创建项目目录",
        "初始化 Git",
        "创建 README"
      ],
      "dependencies": [],
      "acceptance": [
        "项目目录创建完成",
        "Git 仓库初始化完成",
        "README 文件创建完成"
      ]
    }
  ]
}
EOF
```

### 2. 生成任务模板

```bash
# 使用 Python 脚本生成
python3 ~/.pi/agent/skills/ralph-loop-gen/generate.py --config tasks.json
```

### 3. 查看生成的任务

```bash
# 查看任务索引
cat task/my-project/任务索引.md

# 查看当前任务
cat task/my-project/当前任务.md
```

### 4. 开始执行

```bash
# 编辑任务文件，更新状态
vim task/my-project/任务001.md

# 更新状态: Todo → Locked → In Progress
# 填写占用者和锁定时间
# 按照实施步骤执行
```

---

## 经验总结

### 任务设计原则

1. **单一职责**：每个任务只做一件事
2. **可验证**：有明确的验收标准
3. **可估计**：有合理的预计时间
4. **可并行**：尽可能减少依赖链深度

### 依赖关系设计

1. **避免循环依赖**：确保依赖图是 DAG
2. **最小化依赖**：只依赖必要的任务
3. **明确依赖**：在任务描述中说明为什么依赖
4. **测试依赖**：确保依赖任务完成后，当前任务可以立即开始

### 验收标准设计

1. **可量化**：使用可测量的指标
2. **可测试**：可以通过测试验证
3. **完整覆盖**：覆盖所有关键功能
4. **用户可见**：关注用户可感知的效果