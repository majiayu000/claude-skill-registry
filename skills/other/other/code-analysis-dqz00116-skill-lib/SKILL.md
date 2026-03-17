---
name: code-analysis
description: Standardized code reading and analysis workflow with attention-driven focus. Provides clear objectives, deliverables, content outline, and token cost estimation.
version: 1.2
---

# Code Analysis Skill

Standardized workflow for reading, analyzing, and documenting codebases.

## When to Use

Use this skill when you need to:
- Understand a new code module or system
- Analyze architecture and design patterns
- Document technical implementation details
- Prepare for code refactoring or integration
- Create technical documentation for teams
- **Focus on core components** (high-attention code analysis)

---

## Attention-Driven Code Analysis (NEW in v1.2)

基于启发式规则识别代码中的核心组件，优化分析重点。

### Attention Scoring System

```python
# 使用 attention_focus.py 模块
from attention_focus import CodeAttentionScorer

scorer = CodeAttentionScorer()
components = scorer.analyze_code_structure(file_content, file_name)
focus = scorer.get_analysis_focus(components)
```

### Scoring Criteria

| Factor | Weight | Description |
|--------|--------|-------------|
| **核心关键词** | +3 | Manager, Controller, Handler, System, Core |
| **重要关键词** | +2 | Helper, Util, Factory, Provider |
| **代码行数** | +2 (>100行) / +1 (50-100行) | 规模指标 |
| **被引用次数** | +2 (>5处) / +1 (2-5处) | 依赖度指标 |
| **复杂度** | +1 | 方法数>10 或 条件语句>5 |

### Attention Levels

| Level | Score | Analysis Depth |
|-------|-------|----------------|
| **High** | 8-10 | 详细分析 + 完整代码 + 设计原理 |
| **Medium** | 5-7 | 重点分析 + 关键代码段 |
| **Low** | 0-4 | 简要提及 + 功能描述 |

### Workflow with Attention Focus

```
1. Read code file
       ↓
2. Run attention_focus.py analysis
       ↓
3. Get prioritized component list
       ↓
4. Analyze HIGH attention components in detail
5. Analyze MEDIUM attention components briefly
6. Reference LOW attention components as needed
       ↓
7. Generate focused documentation
```

### Benefits

- **Reduce token consumption**: Focus on 20% core code that provides 80% value
- **Faster analysis**: Skip boilerplate and utility code
- **Better documentation**: Highlight architectural decisions and critical paths
- **Estimated improvement**: 20-30% token reduction, 30% faster analysis

## Workflow Template

Every code analysis task MUST follow this 4-step structure:

### 1. Objective (目标)

**Definition**: Clear statement of what needs to be understood

**Format**:
```
目标: [具体要理解的内容]
范围: [分析的范围边界]
深度: [概览/核心逻辑/详细实现]
```

**Examples**:
- 理解 Tinker 序列化库的工作原理
- 分析 PlayerSubsystem 的架构设计
- 掌握 SharedTable 数据表加载机制

### 2. Deliverables (产出物)

**Definition**: Concrete outputs that will be produced

**Format**:
```
产出文档:
- [文档名1] - [路径] - [内容描述]
- [文档名2] - [路径] - [内容描述]

附加产出:
- [代码示例/流程图/架构图]
```

**Documentation Standards**:
- Place in `repository/projects/[Project]/docs/` or `docs/`
- Use descriptive filenames: `[Topic]-[Type].md`
- Include code snippets and diagrams

### 3. Content (内容)

**Definition**: What will be covered in the analysis

**Format**:
```
分析内容:
1. [模块A] - [要点1, 要点2, 要点3]
2. [模块B] - [要点1, 要点2, 要点3]
3. [模块间关系] - [交互流程]

包含要素:
□ 核心类/接口设计
□ 数据流/控制流
□ 关键算法/逻辑
□ 设计模式
□ 依赖关系
```

### 4. Token Estimation (Token 评估)

**Definition**: Estimated token consumption for the analysis

**Format**:
```
Token 评估:
- 代码阅读: ~[X,000] tokens
- 文档编写: ~[X,000] tokens
- 总计: ~[X,000]-[Y,000] tokens
- 预计时间: [X]-[Y] 分钟
```

**Estimation Guidelines**:
| 复杂度 | 代码阅读 | 文档编写 | 总计 | 时间 |
|--------|----------|----------|------|------|
| 简单 (1-2文件) | 3K-5K | 2K-3K | 5K-8K | 15-20min |
| 中等 (模块级) | 10K-20K | 5K-10K | 15K-30K | 30-50min |
| 复杂 (系统级) | 30K-50K | 15K-25K | 45K-75K | 60-90min |

## Execution Flow

```
1. User Request
       │
       ▼
2. Clarify Requirements (if needed)
       │
       ├── 确认分析范围边界
       ├── 确认关键类的定义位置 (文件路径)
       └── ⚠️ 如果定义位置不明，必须要求发起人显式指出
       │
       ▼
3. Output Analysis Plan (4-step structure)
       │
       ├── 1. Objective
       ├── 2. Deliverables  
       ├── 3. Content
       └── 4. Token Estimation
       │
       ▼
4. Wait for "批准计划" Confirmation
       │
       ▼
5. Execute Analysis
       │
       ├── Read relevant code
       ├── Understand logic
       └── Extract key points
       │
       ▼
6. Produce Documentation
       │
       ├── Write technical doc
       ├── Include code examples
       └── Create diagrams if needed
       │
       ▼
7. Report Completion
       └── Summary of findings
```

## Usage Examples

### Example 1: Simple Module Analysis

**User**: "分析 PlayerQuest 的进度更新机制"

**Plan Output**:
```
## 代码分析计划

### 1. 目标
理解 PlayerQuest 的进度更新机制，包括：
- 进度如何存储和更新
- 任务完成判定逻辑
- 与勋章系统的交互

### 2. 产出物
- `PlayerQuest-Progress-Analysis.md` 
  - 路径: `repository/projects/BattleCore/docs/`
  - 包含：流程图 + 核心代码 + 数据流

### 3. 内容
1. PlayerQuest 类结构
2. updateProgress() / accumulateProgress() 实现
3. 任务完成判定逻辑
4. 与 PlayerMedal 的耦合关系

### 4. Token 评估
- 代码阅读: ~5,000 tokens
- 文档编写: ~3,000 tokens
- 总计: ~8,000 tokens
- 预计时间: 15-20 分钟
```

### Example 2: Complex System Analysis

**User**: "理解整个技能系统的架构"

**Plan Output**:
```
## 代码分析计划

### 1. 目标
全面理解 FAbility 技能系统架构：
- 核心类层次结构
- 状态机实现
- 技能生命周期
- 与战斗核心的集成

### 2. 产出物
- `FAbility-Architecture.md`
  - 路径: `repository/projects/BattleCore/docs/`
  - 包含：架构图 + 类图 + 实际案例
- `Skill-Lifecycle-Flow.md`
  - 技能完整生命周期流程

### 3. 内容
1. FAbility 基类设计
2. 状态机 (EAbilityState)
3. 具体技能实现案例
4. CD/消耗系统
5. 事件系统

### 4. Token 评估
- 代码阅读: ~30,000 tokens
- 文档编写: ~15,000 tokens
- 总计: ~45,000 tokens
- 预计时间: 60-80 分钟
```

## Important Rules

### 定义位置确认规则 (Critical)

**规则**: 代码分析时遇到定义位置不明，必须提前要求发起人显式指出位置

**执行步骤**:
1. 收到分析请求后，首先尝试定位关键类/函数的定义文件
2. 如果通过文件名、类名搜索无法确定位置，**立即停止分析**
3. 向发起人询问：**"请提供 [ClassName] 的定义文件路径"**
4. 收到明确路径后，再继续分析

**示例**:
```
❌ 错误做法:
用户: "分析 NetMessage 的实现"
AI: (盲目搜索，找不到正确位置，基于假设分析)

✅ 正确做法:
用户: "分析 NetMessage 的实现"
AI: "请提供 NetMessage 的定义文件路径，
       搜索发现可能的位置：
       - Server/Network/NetMessage.h
       - Server/Common/NetMessage.h
       请确认具体是哪个文件？"
用户: "在 Server/Network/NetMessage.h"
AI: (基于明确路径开始分析)
```

---

## Best Practices

### Do's
✅ 明确范围边界，避免过度分析
✅ 提供具体的文件路径和代码行号
✅ 包含实际的代码片段
✅ 使用图表辅助理解（文字描述）
✅ 评估要保守，留有余量

### Don'ts
❌ 不要模糊的范围（"分析整个项目"）
❌ 不要遗漏关键的产出物信息
❌ 不要低估复杂系统的 token 消耗
❌ 不要混合多个不相关的目标
❌ 不要在定义位置不明时盲目猜测（**必须要求发起人显式指出文件路径**）

## Integration with Other Skills

- **knowledge-base-cache**: Store analysis results in knowledge base
- **git-workflow**: Commit analysis documents
- **skill-creator**: Create specialized analysis skills from patterns

## Template Quick Reference

```markdown
## 代码分析计划

### 1. 目标
[具体目标描述]
范围: [范围边界]
深度: [概览/核心/详细]

### 2. 产出物
- [文档名] - [路径] - [描述]

### 3. 内容
1. [模块A] - [要点]
2. [模块B] - [要点]
3. [关系] - [流程]

### 4. Token 评估
- 代码阅读: ~[X,000] tokens
- 文档编写: ~[X,000] tokens
- 总计: ~[X,000]-[Y,000] tokens
- 预计时间: [X]-[Y] 分钟
```

## Version History

- **v1.2** (2026-02-12) - Added Attention-Driven Analysis
  - 新增：attention_focus.py 模块
  - 新增：启发式代码注意力评分
  - 新增：三级分析深度（High/Medium/Low）
  - 优化：减少20-30% token消耗
  - 优化：分析速度提升30%

- v1.1 (2026-02-10) - Added critical rule
  - 新增：定义位置确认规则
  - 新增：Important Rules 章节
  - 更新：Execution Flow 添加路径确认步骤
  - 更新：Best Practices 添加 Don'ts 规则

- v1.0 (2026-02-10) - Initial release
  - 4-step workflow structure
  - Token estimation guidelines
  - Usage examples and templates
