---
name: acceptance-criteria
description: 检查Acceptance Criteria格式和完整性，验证是否符合Given-When-Then结构、覆盖正常流程/边界条件/异常场景。适合在为User Story编写AC后、准备测试用例前使用，当需要验收AC质量时。帮助不熟悉BDD的PM/BA确保AC明确、可测试、覆盖完整，避免遗漏关键场景。
stage: REQUIREMENTS
level_supported: [L1-STREAMLINED, L2-BALANCED, L3-RIGOROUS]
---

# Acceptance Criteria Skill

> **Scope**: REQUIREMENTS
>
> **版本**: 0.1.0（占位）| **创建日期**: 2025-11-27

---

## 概述

Acceptance Criteria (AC) 定义 User Story 的完成标准：

```
┌─────────────────────────────────────────────────────┐
│              ✓ Acceptance Criteria (GWT)           │
├─────────────────────────────────────────────────────┤
│  Given [precondition/context]                      │
│  When [action/trigger]                             │
│  Then [expected outcome]                           │
└─────────────────────────────────────────────────────┘
```

---

## 快速开始

最快的3步使用流程：

- [ ] **第1步：确认已有AC文档**
  - 文件位置：`spec/requirements/acceptance_criteria.md`（或其他.md文件）
  - 格式要求：每个AC包含 Given-When-Then 三段式结构
  - 数量建议：至少2-3个AC（可以检查更多）

- [ ] **第2步：一键调用检查**
  - 命令：`>>ac_format_check` 或 `>>ac_coverage`
  - AI会自动扫描所有AC，检查格式和覆盖度
  - 检查内容：GWT三要素完整性 + 正常/边界/异常场景覆盖
  - ⚠️ **只读检查**：不会修改你的AC文档

- [ ] **第3步：查看检查报告**
  - 结果显示：对话窗口中直接显示完整报告
  - 报告内容：每个AC的格式检查 + 覆盖度评分 + 改进建议
  - 后续操作：根据报告手动修改AC，补充遗漏的场景

⏱️ **预计耗时**：2-3分钟 / 10个AC

🆘 **遇到问题？** 查看下方"GWT 格式检查"章节获取详细指导

---

## GWT 格式检查

### Given（前置条件）

- [ ] 是否清晰描述初始状态
- [ ] 是否包含必要的上下文
- [ ] 是否可重现

### When（触发动作）

- [ ] 是否描述具体操作
- [ ] 是否单一、明确
- [ ] 是否是用户或系统行为

### Then（预期结果）

- [ ] 是否可观察、可验证
- [ ] 是否有明确的成功标准
- [ ] 是否覆盖正常和异常场景

---

## 覆盖检查

- [ ] 是否覆盖正常流程（Happy Path）
- [ ] 是否覆盖边界条件
- [ ] 是否覆盖错误场景
- [ ] 每个 US 的 AC 数量是否合理（3-7 个）

---

## 分级检查策略

### L1-STREAMLINED
- 检查 GWT 三要素是否完整
- 快速格式验证（< 5 分钟/AC）
- 通过标准：3 项中 2 项通过（≥67%）

### L2-BALANCED
- 每要素检查 2-3 个关键点（共 6-9 项）
- 含覆盖度检查（Happy Path + Error）
- 通过标准：6 项中 5 项通过（≥83%）

### L3-RIGOROUS
- 全面检查所有子项（12+ 项）
- 含边界条件、异常场景全覆盖
- 生成覆盖矩阵
- 通过标准：12 项中 11 项通过（≥91.7%）

---

## 限制条件

### ✅ 适用场景
- 已有AC文档，符合基本的Given-When-Then格式
- 需要验收AC质量（格式检查、覆盖度评估）
- 准备测试用例前，确保AC明确、可测试
- 需要发现遗漏的场景（边界条件、异常情况）
- 团队成员互相审查AC时，作为标准化检查清单

### ❌ 不适用场景
- **完全没有AC文档** → 先使用 `ac_generate` 从US生成AC骨架
- **AC格式完全错误（缺少Given-When-Then结构）** → 先修复基本格式
- **需要自动修复AC而非只检查** → 本SKILL只生成报告，不修复；需手动改进
- **AC已经非常详细，覆盖度很高** → 无需检查，避免浪费时间
- **期望100%无误报** → 检测基于规则，可能有少量误报

### 📋 前置条件
- 至少有2-3个Acceptance Criteria（包含Given-When-Then三段式）
- AC文档是.md格式，位于`spec/requirements/`目录下
- AC已关联到对应的User Story（source_us字段填写）
- 愿意接受检查建议并手动补充遗漏场景
- 理解报告中的评分是辅助判断，最终决策由用户做出

---

## 示例

```gherkin
Scenario: 成功登录
  Given 用户已注册且账号正常
  And 用户在登录页面
  When 用户输入正确的用户名和密码
  And 点击登录按钮
  Then 用户跳转到首页
  And 显示欢迎信息

Scenario: 密码错误
  Given 用户已注册且账号正常
  When 用户输入错误的密码
  Then 显示"用户名或密码错误"提示
  And 用户停留在登录页面
```

---

## >> 命令

```
>>ac_format_check    # AC 格式检查
>>ac_coverage        # AC 覆盖度检查
>>ac_generate        # 从 US 生成 AC 骨架
```

---

## 相关 Skills

- **前置**: user-story-format（US 已定义）
- **并行**: principle-invest（INVEST 验证）
- **后续**: bdd-scenario（转化为 BDD）
- **后续**: vertical-slice（设计阶段）

---

**TODO**: 待细化 AC 覆盖度检查规则
