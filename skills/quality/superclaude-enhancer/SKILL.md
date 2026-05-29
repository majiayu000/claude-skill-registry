---
name: superclaude-enhancer
version: "1.0"
status: production
layer: skill
owner: wade
last_reviewed: 2025-12-07

description: |
  SuperClaude 增强层 Skill，为其他 Skills 提供 SuperClaude 能力增强。
  支持前置分析、后置审查、智能建议等增强模式。

enhancement_modes:
  - pre_analysis      # 执行前的代码/需求分析
  - post_review       # 执行后的代码审查
  - smart_suggest     # 智能建议和优化
  - troubleshoot      # 问题诊断
  - research          # 技术研究

superclaude_commands:
  - /sc:analyze
  - /sc:troubleshoot
  - /sc:research
  - /sc:explain
  - /sc:improve
  - /sc:design

baseline: AI_CODE_FACTORY_DEV_GUIDE_v2.4, SoT Freeze v2.6, SUPERCLAUDE_INTEGRATION_GUIDE_v2.2
---

# SuperClaude Enhancer Skill - 增强层

## 1. Purpose

为 AI 代码工厂的其他 Skills 提供 SuperClaude 能力增强，实现:
- **前置分析**: 在代码生成前进行深度分析
- **后置审查**: 在代码生成后进行质量审查
- **智能建议**: 提供优化建议和最佳实践
- **问题诊断**: 快速定位和解决问题
- **技术研究**: 调研技术方案和模式

## 2. Enhancement Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SuperClaude Enhancement Layer                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────┐   ┌────────────────┐   ┌────────────────┐       │
│  │  Pre-Analysis  │   │  Post-Review   │   │ Smart-Suggest  │       │
│  │  (/sc:analyze) │   │  (/sc:analyze) │   │  (/sc:improve) │       │
│  │  (/sc:research)│   │  (/sot-check)  │   │  (/sc:design)  │       │
│  └───────┬────────┘   └───────┬────────┘   └───────┬────────┘       │
│          │                    │                    │                 │
│          ▼                    ▼                    ▼                 │
│  ┌───────────────────────────────────────────────────────────┐      │
│  │                  Enhancement Hooks API                     │      │
│  │  enhance_before() | enhance_after() | suggest() | diagnose()│     │
│  └───────────────────────────────────────────────────────────┘      │
│                              │                                       │
└──────────────────────────────┼───────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Original Skills Layer                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │ ai-ad-be-gen│  │ai-ad-fe-gen │  │ai-ad-test-gen│ │ doc-auditor │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

## 3. Enhancement Modes

### 3.1 Pre-Analysis (前置分析)

在 Skill 执行前调用，提供上下文分析。

```typescript
interface PreAnalysisInput {
  mode: "pre_analysis";
  task: string;                    // 任务描述
  target_files: string[];          // 目标文件
  analysis_type: "code" | "design" | "research";
}

interface PreAnalysisOutput {
  insights: string[];              // 分析洞察
  recommendations: string[];       // 建议
  risks: string[];                 // 潜在风险
  context_enrichment: {            // 上下文增强
    patterns_found: string[];      // 发现的模式
    dependencies: string[];        // 识别的依赖
    constraints: string[];         // 约束条件
  };
}
```

**触发 SuperClaude 命令**:
- `/sc:analyze` - 代码质量分析
- `/sc:research` - 技术调研
- `/sc:explain` - 概念解释

### 3.2 Post-Review (后置审查)

在 Skill 执行后调用，审查生成的代码。

```typescript
interface PostReviewInput {
  mode: "post_review";
  generated_code: Record<string, string>;  // 生成的代码
  sot_refs: string[];                       // SoT 引用
  review_focus: ("quality" | "security" | "performance" | "sot_compliance")[];
}

interface PostReviewOutput {
  passed: boolean;
  issues: {
    severity: "error" | "warning" | "info";
    file: string;
    line?: number;
    message: string;
    suggestion?: string;
  }[];
  quality_score: number;           // 0-100
  sot_compliance: boolean;
  recommendations: string[];
}
```

**触发 SuperClaude 命令**:
- `/sc:analyze` - 代码审查
- `/sot-check` - SoT 合规检查

### 3.3 Smart-Suggest (智能建议)

提供优化建议和最佳实践。

```typescript
interface SmartSuggestInput {
  mode: "smart_suggest";
  code: Record<string, string>;
  suggest_type: "refactor" | "optimize" | "pattern" | "test";
}

interface SmartSuggestOutput {
  suggestions: {
    type: string;
    description: string;
    before: string;
    after: string;
    benefit: string;
  }[];
  best_practices: string[];
  patterns_recommended: string[];
}
```

**触发 SuperClaude 命令**:
- `/sc:improve` - 代码改进
- `/sc:design` - 设计建议

### 3.4 Troubleshoot (问题诊断)

快速定位和解决问题。

```typescript
interface TroubleshootInput {
  mode: "troubleshoot";
  error_message: string;
  context: {
    file: string;
    code_snippet: string;
    stack_trace?: string;
  };
}

interface TroubleshootOutput {
  root_cause: string;
  explanation: string;
  fix_steps: string[];
  prevention: string[];
}
```

**触发 SuperClaude 命令**:
- `/sc:troubleshoot` - 问题诊断
- `/sc:explain` - 解释错误

## 4. Hook Integration API

### 4.1 在 Skill Prompt 中集成

其他 Skills 可以在 Prompt 中调用增强 Hook：

```xml
<ENHANCEMENT_HOOKS>
<!-- 前置分析 Hook -->
<HOOK type="pre_analysis" enabled="{{ENABLE_ENHANCEMENT}}">
  <TRIGGER>开始生成代码前</TRIGGER>
  <ACTION>
    调用 /sc:analyze 分析现有代码
    调用 /sc:research 调研最佳实践
  </ACTION>
  <OUTPUT>
    将分析结果添加到 CONTEXT 中
  </OUTPUT>
</HOOK>

<!-- 后置审查 Hook -->
<HOOK type="post_review" enabled="{{ENABLE_ENHANCEMENT}}">
  <TRIGGER>代码生成完成后</TRIGGER>
  <ACTION>
    调用 /sc:analyze 审查生成的代码
    调用 /sot-check 验证 SoT 合规
  </ACTION>
  <OUTPUT>
    如果发现问题，返回修正建议
    如果通过，添加质量评分
  </OUTPUT>
</HOOK>
</ENHANCEMENT_HOOKS>
```

### 4.2 条件启用

增强可以根据任务复杂度条件启用：

```yaml
enhancement_rules:
  # 总是启用
  always_on:
    - post_review.sot_compliance

  # 复杂任务启用
  complex_tasks:
    triggers:
      - task_contains: ["重构", "架构", "设计"]
      - files_count: "> 3"
      - involves_state_machine: true
    enable:
      - pre_analysis
      - smart_suggest

  # Bug 修复启用
  bugfix:
    triggers:
      - task_contains: ["修复", "bug", "问题", "错误"]
    enable:
      - troubleshoot
      - post_review
```

## 5. Integration Examples

### 5.1 BE-Gen + SuperClaude Enhancement

```xml
<SKILL name="ai-ad-be-gen" enhanced="true">
<ENHANCEMENT>
  <!-- Phase 0: Pre-Analysis -->
  <PHASE id="pre" type="pre_analysis">
    <INSTRUCTION>
    在生成代码前，先执行 SuperClaude 分析：
    1. 使用 /sc:analyze 分析目标文件的现有代码
    2. 识别现有的代码模式和约定
    3. 检查是否有可复用的组件
    4. 将分析结果添加到上下文
    </INSTRUCTION>
  </PHASE>

  <!-- Phase 1-4: Original BE-Gen Logic -->
  <!-- ... -->

  <!-- Phase 5: Post-Review -->
  <PHASE id="post" type="post_review">
    <INSTRUCTION>
    代码生成后，执行 SuperClaude 审查：
    1. 使用 /sc:analyze 检查代码质量
       - 代码风格一致性
       - 潜在 Bug
       - 性能问题
       - 安全漏洞
    2. 使用 /sot-check 验证 SoT 合规
    3. 如果发现 P0 问题，返回修正建议
    4. 添加质量评分到输出
    </INSTRUCTION>
  </PHASE>
</ENHANCEMENT>
</SKILL>
```

### 5.2 Test-Gen + SuperClaude Enhancement

```xml
<SKILL name="ai-ad-test-gen" enhanced="true">
<ENHANCEMENT>
  <!-- Pre: 分析被测代码 -->
  <PHASE id="pre" type="pre_analysis">
    <INSTRUCTION>
    1. 使用 /sc:analyze 深度分析被测代码
       - 识别所有分支和边界条件
       - 识别隐式依赖
       - 识别潜在的边缘情况
    2. 使用 /sc:research 查找测试最佳实践
    3. 将分析结果用于测试用例设计
    </INSTRUCTION>
  </PHASE>

  <!-- Post: 验证测试覆盖 -->
  <PHASE id="post" type="post_review">
    <INSTRUCTION>
    1. 使用 /sc:analyze 检查测试质量
       - 测试是否覆盖所有分支
       - 断言是否充分
       - Mock 是否正确
    2. 建议补充的测试场景
    </INSTRUCTION>
  </PHASE>
</ENHANCEMENT>
</SKILL>
```

### 5.3 Doc-Agent + SuperClaude Enhancement

```xml
<SKILL name="doc-agent" enhanced="true">
<ENHANCEMENT>
  <!-- Pre: 文档分析 -->
  <PHASE id="pre" type="pre_analysis">
    <INSTRUCTION>
    1. 使用 /sc:analyze 分析文档结构
    2. 使用 /sc:research 查找文档最佳实践
    </INSTRUCTION>
  </PHASE>

  <!-- Post: 文档质量检查 -->
  <PHASE id="post" type="post_review">
    <INSTRUCTION>
    1. 使用 /sc:analyze 检查文档质量
       - 完整性
       - 一致性
       - 可读性
    2. 使用 /sc:document 生成缺失部分
    </INSTRUCTION>
  </PHASE>
</ENHANCEMENT>
</SKILL>
```

## 6. Output Format

增强后的 Skill 输出格式：

```json
{
  "success": true,
  "data": {
    "changes": [...],
    "notes": [...],
    "sot_refs": [...]
  },
  "enhancement": {
    "pre_analysis": {
      "executed": true,
      "insights": ["发现现有代码使用了 Repository 模式", "..."],
      "recommendations": ["建议复用 BaseRepository", "..."]
    },
    "post_review": {
      "executed": true,
      "passed": true,
      "quality_score": 85,
      "issues": [],
      "sot_compliance": true
    }
  }
}
```

## 7. Configuration

### 7.1 全局配置

在 `.claude/WORKFLOW_TEMPLATES.md` 或 `settings.local.json` 中配置：

```json
{
  "superclaude_enhancement": {
    "enabled": true,
    "default_modes": ["post_review"],
    "complex_task_modes": ["pre_analysis", "post_review", "smart_suggest"],
    "quality_threshold": 70,
    "auto_fix": false
  }
}
```

### 7.2 Skill 级配置

在各 Skill 的 front matter 中配置：

```yaml
enhancement:
  enabled: true
  modes:
    - pre_analysis
    - post_review
  config:
    pre_analysis:
      commands: ["/sc:analyze", "/sc:research"]
    post_review:
      commands: ["/sc:analyze", "/sot-check"]
      quality_threshold: 80
```

## 8. Usage Guide

### 8.1 自动增强 (推荐)

使用 `/dev-flow` 命令自动启用增强：

```bash
# 自动包含 SuperClaude 增强
/dev-flow feature 实现充值审批功能
```

### 8.2 手动增强

在任务描述中指定增强模式：

```bash
# 显式启用增强 (v2.4 命令)
/gen be 实现充值审批 --enhance=pre,post

# 显式禁用增强 (v2.4 命令)
/gen be 简单修改 --no-enhance
```

### 8.3 增强 Hook 示例

```python
# 在 Agent 执行流程中
class EnhancedBEAgent:
    def execute(self, task: str, files: list):
        # Phase 0: SuperClaude Pre-Analysis
        if self.enhancement_enabled("pre_analysis"):
            analysis = self.enhance_before(task, files)
            self.context.update(analysis)

        # Phase 1-4: Original Generation
        result = self.generate_code(task, files)

        # Phase 5: SuperClaude Post-Review
        if self.enhancement_enabled("post_review"):
            review = self.enhance_after(result)
            if not review.passed:
                result = self.apply_fixes(result, review.issues)

        return result
```

## 9. Self-Check

| 检查项 | 验证方法 | P0/P1 |
|--------|---------|-------|
| Enhancement Hook 正确触发 | 检查输出中 enhancement 字段 | P0 |
| SuperClaude 命令正确调用 | 检查日志 | P1 |
| 质量评分计算正确 | 对比人工审查 | P1 |
| SoT 合规检查完整 | 交叉验证 /sot-check | P0 |

## 10. Version History

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2025-12-07 | 初始版本：定义增强架构和 Hook API |

---

**文档控制**: Owner: wade | Baseline: SUPERCLAUDE_INTEGRATION_GUIDE v1.0
