---
name: user-story-format
description: 验证User Story格式和质量，检查是否符合As-I-Want-So三要素结构、角色明确、功能具体、价值清晰。适合在编写新US后、准备Sprint Planning前使用，当需要审核US质量时。帮助不熟悉敏捷的PM/BA识别格式问题、模糊角色、缺失价值等常见问题，确保US可理解、可排序、可开发。
stage: REQUIREMENTS
level_supported: [L1-STREAMLINED, L2-BALANCED, L3-RIGOROUS]
---

# User Story Format Skill

> **Scope**: REQUIREMENTS
>
> **版本**: 0.1.0（占位）| **创建日期**: 2025-11-27

---

## 概述

User Story 是敏捷需求的标准格式：

```
┌─────────────────────────────────────────────────────┐
│              📋 User Story Template                 │
├─────────────────────────────────────────────────────┤
│  As a [role]                                       │
│  I want [feature/capability]                       │
│  So that [benefit/value]                           │
└─────────────────────────────────────────────────────┘
```

---

## 快速开始

最快的3步使用流程：

- [ ] **第1步：确认已有US文档**
  - 文件位置：`spec/requirements/user_stories.md`（或其他.md文件）
  - 格式要求：每个US需要尝试包含 As-I-Want-So 三段式结构
  - 数量建议：至少2-3个US（可以检查更多）

- [ ] **第2步：一键调用格式检查**
  - 命令：`>>us_format_check`
  - AI会自动扫描所有US，检查三要素完整性和表述质量
  - 检查内容：As（角色明确）/ I Want（功能具体）/ So That（价值清晰）
  - ⚠️ **只读检查**：不会修改你的US文档

- [ ] **第3步：查看检查报告**
  - 结果显示：对话窗口中直接显示完整报告
  - 报告内容：每个US的格式检查 + 质量评分 + 改进建议
  - 后续操作：根据报告手动修改US，或使用 `>>us_improve` 获取改进建议

⏱️ **预计耗时**：2-3分钟 / 10个US

🆘 **遇到问题？** 查看下方"格式检查"章节获取详细指导

---

## 格式检查

### As（角色）

- [ ] 角色是否明确定义
- [ ] 角色是否来自已识别的用户画像
- [ ] 避免使用"用户"这种模糊角色

### I Want（功能）

- [ ] 功能描述是否具体
- [ ] 是否描述行为而非实现
- [ ] 是否可理解、无歧义

### So That（价值）

- [ ] 是否说明业务价值
- [ ] 价值是否对角色有意义
- [ ] 是否可用于优先级排序

---

## 常见问题

❌ **不好的 User Story**:
- "作为用户，我想要一个按钮，以便点击"
- "作为管理员，我想要更好的性能"

✅ **好的 User Story**:
- "作为注册用户，我想要保存购物车，以便下次登录时继续购物"
- "作为店铺管理员，我想要导出销售报表，以便进行月度业绩分析"

---

## 分级检查策略

### L1-STREAMLINED
- 检查 3 个核心要素是否存在（As/I Want/So That）
- 快速格式验证（< 5 分钟/US）
- 通过标准：3 项中 2 项通过（≥67%）

### L2-BALANCED
- 每要素检查 2-3 个关键点（共 6-9 项）
- 含表述质量评估
- 通过标准：6 项中 5 项通过（≥83%）

### L3-RIGOROUS
- 全面检查所有子项（9+ 项）
- 含角色一致性、价值链分析
- 记录改进建议
- 通过标准：9 项中 8 项通过（≥89%）

---

## 限制条件

### ✅ 适用场景
- 已有US文档，需要验证格式正确性
- 编写新User Story后，需要质量自查
- 准备Sprint Planning前，确保US可理解、可排序
- 团队成员互相审查US时，作为标准化检查清单
- 新手学习编写US，不确定格式是否正确

### ❌ 不适用场景
- **完全没有US文档** → 先使用 `interview-to-us` 从访谈生成US，或使用 `us_template` 生成模板
- **US内容完全混乱，不是三段式** → 需要重新编写，而非格式检查
- **需要自动修复US而非只检查** → 本SKILL主要是检查，可使用 `us_improve` 获取改进建议
- **US已经非常规范，符合所有标准** → 无需检查，避免浪费时间
- **需要检查INVEST原则** → 使用 `principle-invest` SKILL，而非本格式检查

### 📋 前置条件
- 至少有2-3个User Story（尝试包含As-I-Want-So结构）
- US文档是.md格式，位于`spec/requirements/`目录下
- 愿意接受检查建议并手动修改US
- 理解报告中的评分是辅助判断，最终决策由用户做出
- 最好已了解User Story的基本概念（如不了解，查看"常见问题"章节）

---

## >> 命令

```
>>us_format_check    # User Story 格式检查
>>us_improve         # 改进 User Story 表述
>>us_template        # 生成 User Story 模板
```

---

## 相关 Skills

- **前置**: interview-to-us（从访谈生成US）, us-enrich-context（丰富场景感）
- **并行**: acceptance-criteria（同时编写 AC）
- **验证**: principle-invest（INVEST 检查）, us-readability-check（可读性检查）
- **后续**: vertical-slice（转化为 VS）

---

**TODO**: 待细化各角色的 User Story 示例
