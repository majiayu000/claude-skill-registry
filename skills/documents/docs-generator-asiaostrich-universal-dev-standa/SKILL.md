---
name: docgen
description: |
  從專案來源產生使用說明文件。
  使用時機：「產生文件」、「建立速查表」、「使用指南」、「功能參考」、「列出所有功能」
  關鍵字：documentation, usage, reference, cheatsheet, features, 功能文件, 速查表, 使用說明
source: ../../../../skills/docs-generator/SKILL.md
source_version: 1.0.0
translation_version: 1.0.0
last_synced: 2026-01-26
status: current
---

# 文件產生器技能

> **Language**: [English](../../../../skills/docs-generator/SKILL.md) | 繁體中文

**版本**: 1.0.0
**最後更新**: 2026-01-26
**適用範圍**: Claude Code Skills

---

## 用途

自動從專案來源檔案產生完整的使用說明文件。此技能會建立：

1. **FEATURE-REFERENCE.md**：包含所有細節的完整功能文件
2. **CHEATSHEET.md**：單頁速查表

支援多語言（英文、繁體中文、簡體中文），並掃描各種來源：
- CLI 指令
- 斜線命令
- 技能
- 代理
- 工作流程
- 核心規範
- 腳本

## 快速參考

### 產生所有文件

```bash
node scripts/generate-usage-docs.mjs
```

### 產生特定語言

```bash
node scripts/generate-usage-docs.mjs --lang=en       # 僅英文
node scripts/generate-usage-docs.mjs --lang=zh-TW    # 繁體中文
node scripts/generate-usage-docs.mjs --lang=zh-CN    # 簡體中文
```

### 產生特定格式

```bash
node scripts/generate-usage-docs.mjs --cheatsheet    # 僅速查表
node scripts/generate-usage-docs.mjs --reference     # 僅參考手冊
```

### 檢查同步狀態

```bash
# 檢查文件是否需要更新
node scripts/generate-usage-docs.mjs --check

# 或使用同步檢查腳本
./scripts/check-usage-docs-sync.sh         # 檢查
./scripts/check-usage-docs-sync.sh --fix   # 需要時修復
```

## 配置

產生器使用專案根目錄的 `.usage-docs.yaml` 來定義：

- **輸出路徑**：文件產生位置
- **語言**：要產生的語言版本
- **來源**：要掃描的內容（CLI、技能、命令等）
- **範本**：文件結構範本

### 配置範例（多語言）

```yaml
# .usage-docs.yaml - 完整 UDS 配置
version: "1.0"
output:
  directory: "docs/"
  formats: [reference, cheatsheet]
  languages: [en, zh-TW, zh-CN]
  paths:
    en: "docs/"
    zh-TW: "locales/zh-TW/docs/"
    zh-CN: "locales/zh-CN/docs/"

sources:
  cli:
    enabled: true
    entry: "cli/bin/uds.js"
  skills:
    enabled: true
    directory: "skills/"
    pattern: "**/SKILL.md"
```

### 單語言專案

僅需要英文文件的專案：

```yaml
# .usage-docs.yaml - 僅英文
version: "1.0"
output:
  directory: "docs/"
  formats: [reference, cheatsheet]
  languages:
    - en
  paths:
    en: "docs/"

sources:
  cli:
    enabled: true
    entry: "src/cli.js"
```

### 自訂語言配置

不同語言需求的專案（例如：英文 + 日文）：

```yaml
# .usage-docs.yaml - 英文 + 日文
version: "1.0"
output:
  directory: "docs/"
  formats: [reference, cheatsheet]
  languages:
    - en
    - ja
  paths:
    en: "docs/"
    ja: "docs/ja/"

templates:
  reference:
    title:
      en: "My Project Reference"
      ja: "プロジェクトリファレンス"
  cheatsheet:
    title:
      en: "My Project Cheatsheet"
      ja: "チートシート"
```

### 配置 Fallback 行為

產生器實作智慧 fallback 機制處理標題和路徑：

| 優先順序 | 來源 | 說明 |
|----------|------|------|
| 1 | `config[lang]` | 特定語言的配置值 |
| 2 | `config.en` | 配置中的英文 fallback |
| 3 | 內建預設值 | 支援語言的硬編碼預設值 |

**內建支援的語言**：`en`、`zh-TW`、`zh-CN`

對於不支援的語言，您必須在 `templates` 區塊中提供自訂標題。

## 輸出檔案

| 語言 | FEATURE-REFERENCE | CHEATSHEET |
|------|-------------------|------------|
| English | `docs/FEATURE-REFERENCE.md` | `docs/CHEATSHEET.md` |
| 繁體中文 | `locales/zh-TW/docs/FEATURE-REFERENCE.md` | `locales/zh-TW/docs/CHEATSHEET.md` |
| 简体中文 | `locales/zh-CN/docs/FEATURE-REFERENCE.md` | `locales/zh-CN/docs/CHEATSHEET.md` |

## 整合到發布前檢查

將使用說明文件同步檢查加入 `pre-release-check.sh`：

```bash
# 檢查使用說明文件同步
echo "Checking usage documentation sync..."
./scripts/check-usage-docs-sync.sh
```

## 工作流程

```
┌─────────────────────────────────────────────────────────┐
│                      文件產生器                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. 載入配置 (.usage-docs.yaml)                         │
│           │                                              │
│           ▼                                              │
│  2. 掃描來源                                             │
│     ├─ CLI 指令 (uds.js)                                │
│     ├─ 技能 (SKILL.md 檔案)                             │
│     ├─ 命令 (斜線命令)                                   │
│     ├─ 代理 (代理定義)                                   │
│     ├─ 工作流程 (工作流程檔案)                           │
│     ├─ 核心規範 (core/*.md)                             │
│     └─ 腳本 (scripts/*.sh)                              │
│           │                                              │
│           ▼                                              │
│  3. 產生文件                                             │
│     ├─ FEATURE-REFERENCE.md（詳細版）                   │
│     └─ CHEATSHEET.md（速查表）                          │
│           │                                              │
│           ▼                                              │
│  4. 輸出各語言版本                                       │
│     ├─ 英文 (docs/)                                      │
│     ├─ 繁體中文 (locales/zh-TW/docs/)                   │
│     └─ 簡體中文 (locales/zh-CN/docs/)                   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 在其他專案使用

此技能設計為可重用。在你的專案中使用：

1. **複製配置範本**：
   ```bash
   cp .usage-docs.yaml your-project/.usage-docs.yaml
   ```

2. **修改為你的專案結構**：
   - 更新來源目錄
   - 調整檔案命名模式
   - 配置輸出路徑

3. **複製產生器腳本**：
   ```bash
   cp scripts/generate-usage-docs.mjs your-project/scripts/
   ```

4. **執行產生器**：
   ```bash
   node scripts/generate-usage-docs.mjs
   ```

## 相關規範

- [文件撰寫規範](../../../../core/documentation-writing-standards.md)
- [文件結構規範](../../../../core/documentation-structure.md)
- [AI 友善架構](../../../../core/ai-friendly-architecture.md)

## 版本歷史

| 版本 | 日期 | 變更 |
|------|------|------|
| 1.0.0 | 2026-01-26 | 初始發布，支援多語言 |

---

## 授權

此技能以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授權釋出。

**來源**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
