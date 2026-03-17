---
name: ccw
description: Stateless workflow orchestrator that automatically selects and executes the optimal workflow combination based on task intent. Supports rapid (lite-plan+execute), full (brainstorm+plan+execute), coupled (plan+execute), bugfix (lite-fix), and issue (multi-point fixes) workflows. Triggers on "ccw", "workflow", "自动工作流", "智能调度".
allowed-tools: Task(*), SlashCommand(*), AskUserQuestion(*), Read(*), Bash(*), Grep(*)
---

# CCW - Claude Code Workflow Orchestrator

无状态工作流协调器，根据任务意图自动选择并执行最优工作流组合。

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  CCW Orchestrator (Stateless)                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input Analysis                                                  │
│  ├─ Intent Classification (bugfix/feature/refactor/issue/...)  │
│  ├─ Complexity Assessment (low/medium/high)                     │
│  ├─ Context Detection (codebase familiarity needed?)            │
│  └─ Constraint Extraction (time/scope/quality)                  │
│                                                                  │
│  Workflow Selection (Decision Tree)                              │
│  ├─ 🐛 Bug? → lite-fix / lite-fix --hotfix                      │
│  ├─ ❓ Unclear? → brainstorm → plan → execute                   │
│  ├─ ⚡ Simple? → lite-plan → lite-execute                       │
│  ├─ 🔧 Complex? → plan → execute                                │
│  ├─ 📋 Issue? → issue:plan → issue:queue → issue:execute        │
│  └─ 🎨 UI? → ui-design → plan → execute                         │
│                                                                  │
│  Execution Dispatch                                              │
│  └─ SlashCommand("/workflow:xxx") or Task(agent)                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Workflow Combinations (组合技)

### 1. Rapid (快速迭代) ⚡
**Pattern**: 多模型协作分析 + 直接执行
**Commands**: `/workflow:lite-plan` → `/workflow:lite-execute`
**When to use**:
- 明确知道做什么和怎么做
- 单一功能或小型改动
- 快速原型验证

### 2. Full (完整流程) 📋
**Pattern**: 分析 + 头脑风暴 + 规划 + 执行
**Commands**: `/workflow:brainstorm:auto-parallel` → `/workflow:plan` → `/workflow:execute`
**When to use**:
- 不确定产品方向或技术方案
- 需要多角色视角分析
- 复杂新功能开发

### 3. Coupled (复杂耦合) 🔗
**Pattern**: 完整规划 + 验证 + 执行
**Commands**: `/workflow:plan` → `/workflow:action-plan-verify` → `/workflow:execute`
**When to use**:
- 跨模块依赖
- 架构级变更
- 团队协作项目

### 4. Bugfix (缺陷修复) 🐛
**Pattern**: 智能诊断 + 修复
**Commands**: `/workflow:lite-fix` or `/workflow:lite-fix --hotfix`
**When to use**:
- 任何有明确症状的Bug
- 生产事故紧急修复
- 根因不清楚需要诊断

### 5. Issue (长时间多点修复) 📌
**Pattern**: Issue规划 + 队列 + 批量执行
**Commands**: `/issue:plan` → `/issue:queue` → `/issue:execute`
**When to use**:
- 多个相关问题需要批量处理
- 长时间跨度的修复任务
- 需要优先级排序和冲突解决

### 6. UI-First (设计驱动) 🎨
**Pattern**: UI设计 + 规划 + 执行
**Commands**: `/workflow:ui-design:*` → `/workflow:plan` → `/workflow:execute`
**When to use**:
- 前端功能开发
- 需要视觉参考
- 设计系统集成

## Intent Classification

```javascript
function classifyIntent(input) {
  const text = input.toLowerCase()
  
  // Priority 1: Bug keywords
  if (/\b(fix|bug|error|issue|crash|broken|fail|wrong|incorrect)\b/.test(text)) {
    if (/\b(hotfix|urgent|production|critical|emergency)\b/.test(text)) {
      return { type: 'bugfix', mode: 'hotfix', workflow: 'lite-fix --hotfix' }
    }
    return { type: 'bugfix', mode: 'standard', workflow: 'lite-fix' }
  }
  
  // Priority 2: Issue batch keywords
  if (/\b(issues?|batch|queue|多个|批量)\b/.test(text) && /\b(fix|resolve|处理)\b/.test(text)) {
    return { type: 'issue', workflow: 'issue:plan → issue:queue → issue:execute' }
  }
  
  // Priority 3: Uncertainty keywords → Full workflow
  if (/\b(不确定|不知道|explore|研究|分析一下|怎么做|what if|should i|探索)\b/.test(text)) {
    return { type: 'exploration', workflow: 'brainstorm → plan → execute' }
  }
  
  // Priority 4: UI/Design keywords
  if (/\b(ui|界面|design|设计|component|组件|style|样式|layout|布局)\b/.test(text)) {
    return { type: 'ui', workflow: 'ui-design → plan → execute' }
  }
  
  // Priority 5: Complexity assessment for remaining
  const complexity = assessComplexity(text)
  
  if (complexity === 'high') {
    return { type: 'feature', complexity: 'high', workflow: 'plan → verify → execute' }
  }
  
  if (complexity === 'medium') {
    return { type: 'feature', complexity: 'medium', workflow: 'lite-plan → lite-execute' }
  }
  
  return { type: 'feature', complexity: 'low', workflow: 'lite-plan → lite-execute' }
}

function assessComplexity(text) {
  let score = 0
  
  // Architecture keywords
  if (/\b(refactor|重构|migrate|迁移|architect|架构|system|系统)\b/.test(text)) score += 2
  
  // Multi-module keywords
  if (/\b(multiple|多个|across|跨|all|所有|entire|整个)\b/.test(text)) score += 2
  
  // Integration keywords
  if (/\b(integrate|集成|connect|连接|api|database|数据库)\b/.test(text)) score += 1
  
  // Security/Performance keywords
  if (/\b(security|安全|performance|性能|scale|扩展)\b/.test(text)) score += 1
  
  if (score >= 4) return 'high'
  if (score >= 2) return 'medium'
  return 'low'
}
```

## Execution Flow

### Phase 1: Input Analysis

```javascript
// Parse user input
const input = userInput.trim()

// Check for explicit workflow request
if (input.startsWith('/workflow:') || input.startsWith('/issue:')) {
  // User explicitly requested a workflow, pass through
  SlashCommand(input)
  return
}

// Classify intent
const intent = classifyIntent(input)

console.log(`
## Intent Analysis

**Input**: ${input.substring(0, 100)}...
**Classification**: ${intent.type}
**Complexity**: ${intent.complexity || 'N/A'}
**Recommended Workflow**: ${intent.workflow}
`)
```

### Phase 2: User Confirmation (Optional)

```javascript
// For high-complexity or ambiguous intents, confirm with user
if (intent.complexity === 'high' || intent.type === 'exploration') {
  const confirmation = AskUserQuestion({
    questions: [{
      question: `Recommended: ${intent.workflow}. Proceed?`,
      header: "Workflow",
      multiSelect: false,
      options: [
        { label: `${intent.workflow} (Recommended)`, description: "Use recommended workflow" },
        { label: "Rapid (lite-plan)", description: "Quick iteration" },
        { label: "Full (brainstorm+plan)", description: "Complete exploration" },
        { label: "Manual", description: "I'll specify the commands" }
      ]
    }]
  })
  
  // Adjust workflow based on user selection
  intent.workflow = mapSelectionToWorkflow(confirmation)
}
```

### Phase 3: Workflow Dispatch

```javascript
switch (intent.workflow) {
  case 'lite-fix':
    SlashCommand('/workflow:lite-fix', args: input)
    break
    
  case 'lite-fix --hotfix':
    SlashCommand('/workflow:lite-fix --hotfix', args: input)
    break
    
  case 'lite-plan → lite-execute':
    SlashCommand('/workflow:lite-plan', args: input)
    // lite-plan will automatically dispatch to lite-execute
    break
    
  case 'plan → verify → execute':
    SlashCommand('/workflow:plan', args: input)
    // After plan, prompt for verify and execute
    break
    
  case 'brainstorm → plan → execute':
    SlashCommand('/workflow:brainstorm:auto-parallel', args: input)
    // After brainstorm, continue with plan
    break
    
  case 'issue:plan → issue:queue → issue:execute':
    SlashCommand('/issue:plan', args: input)
    // Issue workflow handles queue and execute
    break
    
  case 'ui-design → plan → execute':
    // Determine UI design subcommand
    if (hasReference(input)) {
      SlashCommand('/workflow:ui-design:imitate-auto', args: input)
    } else {
      SlashCommand('/workflow:ui-design:explore-auto', args: input)
    }
    break
}
```

## CLI Tool Integration

CCW **隐式调用** CLI 工具以获得三大优势：

### 1. Token 效率 (Context Efficiency)

CLI 工具在单独进程中运行，可以处理大量代码上下文而不消耗主会话 token：

| 场景 | 触发条件 | 自动注入 |
|------|----------|----------|
| 大量代码上下文 | 文件读取 ≥ 50k 字符 | `gemini --mode analysis` |
| 多模块分析 | 涉及 ≥ 5 个模块 | `gemini --mode analysis` |
| 代码审查 | review 步骤 | `gemini --mode analysis` |

### 2. 多模型视角 (Multi-Model Perspectives)

不同模型有不同优势，CCW 根据任务类型自动选择：

| Tool | 核心优势 | 最佳场景 | 触发关键词 |
|------|----------|----------|------------|
| Gemini | 超长上下文、深度分析、架构理解、执行流追踪 | 代码库理解、架构评估、根因分析 | "分析", "理解", "设计", "架构", "诊断" |
| Qwen | 代码模式识别、多维度分析 | Gemini备选、第二视角验证 | "评估", "对比", "验证" |
| Codex | 精确代码生成、自主执行、数学推理 | 功能实现、重构、测试 | "实现", "重构", "修复", "生成", "测试" |

### 3. 增强能力 (Enhanced Capabilities)

#### Debug 能力增强
```
触发条件: intent === 'bugfix' AND root_cause_unclear
自动注入: gemini --mode analysis (执行流追踪)
用途: 假设驱动调试、状态机错误诊断、并发问题排查
```

#### 规划能力增强
```
触发条件: complexity === 'high' OR intent === 'exploration'
自动注入: gemini --mode analysis (架构分析)
用途: 复杂任务先用CLI分析获取多模型视角
```

### 隐式注入规则 (Implicit Injection Rules)

CCW 在以下条件自动注入 CLI 调用（无需用户显式请求）：

```javascript
const implicitRules = {
  // 上下文收集：大量代码使用CLI可节省主会话token
  context_gathering: {
    trigger: 'file_read >= 50k chars OR module_count >= 5',
    inject: 'gemini --mode analysis'
  },

  // 规划前分析：复杂任务先用CLI分析
  pre_planning_analysis: {
    trigger: 'complexity === "high" OR intent === "exploration"',
    inject: 'gemini --mode analysis'
  },

  // 调试诊断：利用Gemini的执行流追踪能力
  debug_diagnosis: {
    trigger: 'intent === "bugfix" AND root_cause_unclear',
    inject: 'gemini --mode analysis'
  },

  // 代码审查：用CLI减少token占用
  code_review: {
    trigger: 'step === "review"',
    inject: 'gemini --mode analysis'
  },

  // 多任务执行：用Codex自主完成
  implementation: {
    trigger: 'step === "execute" AND task_count >= 3',
    inject: 'codex --mode write'
  }
}
```

### 用户语义触发 (Semantic Tool Assignment)

```javascript
// 用户可以通过自然语言指定工具偏好
const toolHints = {
  gemini: /用\s*gemini|gemini\s*分析|让\s*gemini|深度分析|架构理解/i,
  qwen: /用\s*qwen|qwen\s*评估|让\s*qwen|第二视角/i,
  codex: /用\s*codex|codex\s*实现|让\s*codex|自主完成|批量修改/i
}

function detectToolPreference(input) {
  for (const [tool, pattern] of Object.entries(toolHints)) {
    if (pattern.test(input)) return tool
  }
  return null // Auto-select based on task type
}
```

### 独立 CLI 工作流 (Standalone CLI Workflows)

直接调用 CLI 进行特定任务：

| Workflow | 命令 | 用途 |
|----------|------|------|
| CLI Analysis | `ccw cli --tool gemini` | 大型代码库快速理解、架构评估 |
| CLI Implement | `ccw cli --tool codex` | 明确需求的自主实现 |
| CLI Debug | `ccw cli --tool gemini` | 复杂bug根因分析、执行流追踪 |

## Index Files (Dynamic Coordination)

CCW 使用索引文件实现智能命令协调：

| Index | Purpose |
|-------|---------|
| [index/command-capabilities.json](index/command-capabilities.json) | 命令能力分类（explore, plan, execute, test, review...） |
| [index/workflow-chains.json](index/workflow-chains.json) | 预定义工作流链（rapid, full, coupled, bugfix, issue, tdd, ui...） |

### 能力分类

```
capabilities:
├── explore    - 代码探索、上下文收集
├── brainstorm - 多角色分析、方案探索
├── plan       - 任务规划、分解
├── verify     - 计划验证、质量检查
├── execute    - 任务执行、代码实现
├── bugfix     - Bug诊断、修复
├── test       - 测试生成、执行
├── review     - 代码审查、质量分析
├── issue      - 批量问题管理
├── ui-design  - UI设计、原型
├── memory     - 文档、知识管理
├── session    - 会话管理
└── debug      - 调试、问题排查
```

## TODO Tracking Integration

CCW 自动使用 TodoWrite 跟踪工作流执行进度：

```javascript
// 工作流启动时自动创建 TODO 列表
TodoWrite({
  todos: [
    { content: "CCW: Rapid Iteration (2 steps)", status: "in_progress", activeForm: "Running workflow" },
    { content: "[1/2] /workflow:lite-plan", status: "in_progress", activeForm: "Executing lite-plan" },
    { content: "[2/2] /workflow:lite-execute", status: "pending", activeForm: "Executing lite-execute" }
  ]
})

// 每个步骤完成后自动更新状态
// 支持暂停、继续、跳过操作
```

**进度可视化**:
```
✓ CCW: Rapid Iteration (2 steps)
✓ [1/2] /workflow:lite-plan
→ [2/2] /workflow:lite-execute
```

**控制命令**:
| Input | Action |
|-------|--------|
| `continue` | 执行下一步 |
| `skip` | 跳过当前步骤 |
| `abort` | 停止工作流 |
| `/workflow:*` | 执行指定命令 |

## Reference Documents

| Document | Purpose |
|----------|---------|
| [phases/orchestrator.md](phases/orchestrator.md) | 编排器决策逻辑 + TODO 跟踪 |
| [phases/actions/rapid.md](phases/actions/rapid.md) | 快速迭代组合 |
| [phases/actions/full.md](phases/actions/full.md) | 完整流程组合 |
| [phases/actions/coupled.md](phases/actions/coupled.md) | 复杂耦合组合 |
| [phases/actions/bugfix.md](phases/actions/bugfix.md) | 缺陷修复组合 |
| [phases/actions/issue.md](phases/actions/issue.md) | Issue工作流组合 |
| [specs/intent-classification.md](specs/intent-classification.md) | 意图分类规范 |
| [WORKFLOW_DECISION_GUIDE.md](/WORKFLOW_DECISION_GUIDE.md) | 工作流决策指南 |

## Examples

### Example 1: Bug Fix
```
User: 用户登录失败，返回 401 错误
CCW: Intent=bugfix, Workflow=lite-fix
→ /workflow:lite-fix "用户登录失败，返回 401 错误"
```

### Example 2: New Feature (Simple)
```
User: 添加用户头像上传功能
CCW: Intent=feature, Complexity=low, Workflow=lite-plan→lite-execute
→ /workflow:lite-plan "添加用户头像上传功能"
```

### Example 3: Complex Refactoring
```
User: 重构整个认证模块，迁移到 OAuth2
CCW: Intent=feature, Complexity=high, Workflow=plan→verify→execute
→ /workflow:plan "重构整个认证模块，迁移到 OAuth2"
```

### Example 4: Exploration
```
User: 我想优化系统性能，但不知道从哪入手
CCW: Intent=exploration, Workflow=brainstorm→plan→execute
→ /workflow:brainstorm:auto-parallel "探索系统性能优化方向"
```

### Example 5: Multi-Model Collaboration
```
User: 用 gemini 分析现有架构，然后让 codex 实现优化
CCW: Detects tool preferences, executes in sequence
→ Gemini CLI (analysis) → Codex CLI (implementation)
```
