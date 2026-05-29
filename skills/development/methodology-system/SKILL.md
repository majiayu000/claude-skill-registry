---
source: ../../../../../skills/claude-code/methodology-system/SKILL.md
source_version: 1.0.0
translation_version: 1.0.0
last_synced: 2026-01-12
status: experimental
---

# 方法論系统 Skill

> **Language**: [English](../../../../../skills/claude-code/methodology-system/SKILL.md) | 简体中文

> [!WARNING]
> **实驗性功能 / Experimental Feature**
>
> 此功能正在積極开发中，可能在 v4.0 中有重大变更。
> This feature is under active development and may change significantly in v4.0.

**版本**: 1.0.0
**最後更新**: 2026-01-12

---

## 概述

方法論系统讓採用此规范的项目能夠选择、配置并遵循特定的开发方法論。內建支援 TDD、BDD、SDD 和 ATDD，并可建立自订方法論。

---

## 功能

### 核心功能

1. **方法論选择** - 從內建方法論中选择或建立自订方法論
2. **阶段追蹤** - 追蹤當前开发阶段，提供阶段特定的引導
3. **检查点系统** - 在关鍵时刻自动提醒和验证
4. **检查清单** - 每个阶段都有必須完成的检查项目
5. **AI 引導** - 根据當前阶段提供上下文感知的 AI 引導

### 內建方法論

| 方法論 | 说明 | 阶段 |
|--------|------|------|
| **TDD** | 测试驅动开发 | 紅燈 → 綠燈 → 重構 |
| **BDD** | 行为驅动开发 | 探索 → 制定 → 自动化 → 活文件 |
| **SDD** | 規格驅动开发 | 提案 → 审查 → 实作 → 验证 → 歸檔 |
| **ATDD** | 驗收测试驅动开发 | 工作坊 → 提煉 → 开发 → 展示 |

---

## 命令

| 命令 | 说明 |
|------|------|
| `/methodology` | 顯示當前方法論状态 |
| `/methodology status` | 顯示當前阶段和检查清单 |
| `/methodology switch <id>` | 切换到不同方法論 |
| `/methodology phase [name]` | 顯示或变更當前阶段 |
| `/methodology checklist` | 顯示當前阶段检查清单 |
| `/methodology skip` | 跳過當前阶段（会有警告） |
| `/methodology list` | 列出可用方法論 |
| `/methodology create` | 建立自订方法論 |

---

## 配置

在 `.standards/manifest.json` 中配置方法論：

```json
{
  "methodology": {
    "active": "tdd",
    "available": ["tdd", "bdd", "sdd", "atdd"],
    "config": {
      "checkpointsEnabled": true,
      "reminderIntensity": "suggest",
      "skipLimit": 3
    }
  }
}
```

### 配置选项

| 选项 | 类型 | 预设值 | 说明 |
|------|------|--------|------|
| `active` | string | null | 當前啟用的方法論 ID |
| `available` | string[] | all | 可用的方法論清单 |
| `checkpointsEnabled` | boolean | true | 是否啟用检查点提醒 |
| `reminderIntensity` | string | "suggest" | 提醒強度：suggest、warn、block |
| `skipLimit` | number | 3 | 連續跳過幾次後顯示警告 |

---

## AI 行为

當方法論啟用时，AI 会：

1. **顯示阶段指示器** - 使用表情符号標示當前阶段（如 🔴 RED）
2. **提供阶段引導** - 根据當前阶段建议適當的行动
3. **追蹤检查清单** - 自动追蹤和更新检查项目状态
4. **顯示检查点** - 在阶段转换或大量变更时提醒用戶
5. **建议提交** - 根据变更累積量建议適當的提交时机

---

## 自订方法論

可以建立自订方法論來符合团队需求：

1. 使用 `/methodology create` 啟动互动式建立精靈
2. 或手动在 `.standards/methodologies/` 建立 YAML 文件

詳見 [建立自订方法論](create-methodology.md)。

---

## 相关文件

- [命令文档](../commands/methodology.md) - `/methodology` 命令详细文档
- [执行时引導](runtime.md) - AI 行为規格
- [建立自订方法論](create-methodology.md) - 建立指南

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-01-12 | 初始方法論系统 |
