---
name: ha-integration-reviewer
description: 严格的 Home Assistant 集成代码审查。用于提交 PR 前的全面检查，包括 Quality Scale 规则验证、代码风格、Config Flow、测试覆盖和文档。当用户说"审查我的 HA 集成"、"检查我的代码是否符合 HA 规范"、"帮我 review 一下准备提交的代码"时触发。
---

# HA Integration Reviewer

以最严格的 Home Assistant Reviewer 视角审查集成代码。

## 审查流程

### 1. 确定审查范围

```bash
# 获取待审查的文件（ha-core 使用 dev 分支）
git diff --name-only HEAD~1  # 最近一次提交
git diff --name-only dev     # 与 dev 分支的差异（ha-core 主分支）
```

或用户指定的目录/文件。

### 2. 并行启动检查 Agent

使用 Task 工具并行启动多个专项检查，详见 [review-workflow.md](references/review-workflow.md)：

```text
Agent 1: Quality Scale 规则检查
Agent 2: 代码风格检查
Agent 3: Config Flow 检查
Agent 4: 测试覆盖检查
Agent 5: 文档与 Manifest 检查
```

**并行执行方式**:

在 Claude Code 中，通过在同一轮对话中发起多个独立检查实现并行：

1. Quality Scale 验证 - 读取 quality_scale.yaml，验证 done 规则
2. 代码风格检查 - 对照 copilot-instructions.md
3. Config Flow 检查 - 验证 unique_id 和测试覆盖
4. 测试覆盖检查 - 确认 >= 95%
5. 文档检查 - 验证 strings.json 和 README

每个检查独立进行，最后汇总结果。

### 3. 动态获取最新规范

**不要使用过时的静态文档**，每次审查时动态获取：

#### Quality Scale 规则

```text
WebFetch: https://raw.githubusercontent.com/home-assistant/developers.home-assistant/refs/heads/master/docs/core/integration-quality-scale/rules/{rule_name}.md
```

#### 编码规范

```text
WebFetch: https://raw.githubusercontent.com/home-assistant/core/dev/.github/copilot-instructions.md
```

#### 开发者文档

使用 Context7 获取最新的 Home Assistant 开发者文档。

### 4. 参考其他集成

查看 ha-core 中类似集成的实现：

```bash
gh api repos/home-assistant/core/contents/homeassistant/components/{integration_name}
```

### 5. 汇总审查报告

输出结构化报告，包含：

- 每个检查维度的结果
- 具体问题及其文件位置
- 修复建议及优先级

## 检查清单速查

详见 [common-issues.md](references/common-issues.md)，包含：

- 代码风格常见问题
- 日志规范
- 异常处理
- 实体与设备
- Config Flow
- 服务注册
- 文档规范

## Quality Scale 验证要点

### 使用 quality-scale-rule-verifier Agent

ha-core 仓库提供了专门的 Quality Scale 验证 agent：

**位置**: `repos/ha-core/.claude/agents/quality-scale-rule-verifier.md`

**调用方式**:

```text
# 验证单个规则
"Check if the {integration} integration follows the {rule_name} rule"

# 验证整个等级
"Verify that this integration reaches the {tier} quality scale"
```

该 agent 会动态获取规则文档并验证实现，比静态检查更准确。

### Done 规则

验证代码是否真正符合规则要求，而非仅仅标记为 done。

### Todo 规则

检查是否接近完成，提示用户考虑完成以提升 Quality Scale 等级。

### Exempt 规则

评估豁免理由是否合理，是否真的不适用于该集成。

## 关键审查标准

### 异步编程

- 所有外部 I/O 必须 async
- 禁止在事件循环中阻塞
- 使用 `gather` 替代循环中的 await

### 异常处理

- 缩小 try 块范围
- 使用 `ServiceValidationError` 处理输入错误
- 使用 `HomeAssistantError` 处理通信故障

### Config Flow

- unique_id 正确设置
- 100% 测试覆盖
- UI 文本规范（避免 "Click"，加粗按钮标签）

### 测试

- 位于 `tests/components/{domain}/`
- 使用 fixture 和 snapshot testing
- 覆盖率 >= 95%
