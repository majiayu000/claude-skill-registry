---
name: principle-dry
description: 识别并消除知识重复，确保系统中每条知识有唯一权威表示。当需要重构代码、整理文档、优化配置、建立单一数据源时使用。覆盖代码重复、数据冗余、文档重复三大维度，提供具体消除策略和权衡建议。
stage: COMMON
level_supported: [L1-STREAMLINED, L2-BALANCED, L3-RIGOROUS]
---

# DRY Principle Skill

> **Scope**: COMMON（全阶段通用）
>
> **版本**: 0.1.0（占位）| **创建日期**: 2025-11-27

---

## 概述

DRY（Don't Repeat Yourself）是软件开发的核心原则：

```
┌─────────────────────────────────────────────────────┐
│              🔄 DRY Principle                       │
├─────────────────────────────────────────────────────┤
│  "Every piece of knowledge must have a single,     │
│   unambiguous, authoritative representation        │
│   within a system."                                │
│                        — Andy Hunt & Dave Thomas   │
└─────────────────────────────────────────────────────┘
```

---

## 检查维度

### 代码重复

- [ ] 是否有复制粘贴的代码块
- [ ] 相似逻辑是否抽象为函数/方法
- [ ] 常量是否集中定义

### 数据重复

- [ ] 同一数据是否在多处定义
- [ ] 配置是否有单一来源（SSOT）
- [ ] 数据库是否有冗余字段

### 文档重复

- [ ] 同一信息是否在多个文档中维护
- [ ] API 文档是否从代码自动生成
- [ ] 注释是否与代码重复

### 知识重复

- [ ] 业务规则是否集中管理
- [ ] 验证逻辑是否在多处实现
- [ ] 错误消息是否统一定义

---

## 分级检查策略

### L1-STREAMLINED
- 每维度检查 1 个核心点（共 4 项）
- 关注明显重复
- 通过标准：4 项中 3 项通过（≥75%）

### L2-BALANCED
- 每维度检查 2-3 个关键点（共 8-12 项）
- 使用工具扫描代码重复率
- 通过标准：8 项中 7 项通过（≥87.5%）

### L3-RIGOROUS
- 全面检查所有子项（12+ 项）
- 量化重复率指标（目标 < 5%）
- 识别 SSOT 候选并记录
- 通过标准：12 项中 11 项通过（≥91.7%）

---

## >> 命令

```
>>dry_check_l1       # DRY 快速检查（4维度各1个关键点）
>>dry_scan_code      # 扫描代码重复
>>dry_find_ssot      # 识别需要 SSOT 的地方
```

---

## 相关 Skills

- **同类**: principle-kiss, principle-yagni, principle-soc（设计原则家族）
- **应用**: refactoring（消除重复的重构技术）
- **验证**: code-review（代码审查时检查 DRY）
- **文档**: document-quality（文档中避免重复）

---

**TODO**: 待细化重复检测规则和重构建议
