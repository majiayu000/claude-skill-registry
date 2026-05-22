---
source: skills/claude-code/documentation-guide/SKILL.md
source_version: 2.0.0
translation_version: 2.0.0
last_synced: 2026-01-12
status: current
name: documentation-guide
description: |
  引導文件结构、内容需求和项目文件最佳实踐。
  使用时机：建立 README、文件、docs 目录、项目设置、技術文件。
  关鍵字：README, docs, documentation, CONTRIBUTING, CHANGELOG, ARCHITECTURE, API docs, 文件, 说明文件, 技術文件.
---

# 文件指南

> **语言**: [English](../../../../../skills/claude-code/documentation-guide/SKILL.md) | 简体中文

**版本**: 2.0.0
**最後更新**: 2026-01-12
**適用範圍**: Claude Code Skills

---

## 目的

本 Skill 提供项目文件的全面指導，包括：
- 文件结构和文件組織
- 依项目类型的内容需求
- 技術文件的撰写标准
- 常見文件类型的範本

---

## 快速參考（YAML 壓縮格式）

```yaml
# === 项目类型 → 文件需求 ===
document_matrix:
  #           README  ARCH   API    DB     DEPLOY MIGRATE ADR    CHANGE CONTRIB
  new:        [REQ,   REQ,   if_app, if_app, REQ,   NO,     REC,   REQ,   REC]
  refactor:   [REQ,   REQ,   REQ,    REQ,    REQ,   REQ,    REQ,   REQ,   REC]
  migration:  [REQ,   REQ,   REQ,    REQ,    REQ,   REQ,    REQ,   REQ,   REC]
  maintenance:[REQ,   REC,   REC,    REC,    REC,   NO,     if_app, REQ,   if_app]
  # REQ=必要, REC=建议, if_app=如適用, NO=不需要

# === 文件金字塔 ===
pyramid:
  level_1: "README.md → 入口点，快速概覽"
  level_2: "ARCHITECTURE.md → 系统概述"
  level_3: "API.md, DATABASE.md, DEPLOYMENT.md → 技術細节"
  level_4: "ADR/, MIGRATION.md, CHANGELOG.md → 变更历史"

# === 必要文件 ===
root_files:
  README.md: {required: true, purpose: "项目概述、快速入門"}
  CONTRIBUTING.md: {required: "recommended", purpose: "貢獻指南"}
  CHANGELOG.md: {required: "recommended", purpose: "版本历史"}
  LICENSE: {required: "for OSS", purpose: "授权信息"}

docs_structure:
  INDEX.md: "文件索引"
  ARCHITECTURE.md: "系统架構"
  API.md: "API 文件"
  DATABASE.md: "数据庫綱要"
  DEPLOYMENT.md: "部署指南"
  MIGRATION.md: "迁移计画（如適用）"
  ADR/: "架構决策记录"

# === 文件命名 ===
naming:
  root: "UPPERCASE.md (README.md, CONTRIBUTING.md, CHANGELOG.md)"
  docs: "lowercase-kebab-case.md (getting-started.md, api-reference.md)"

# === 品质标准 ===
quality:
  format:
    language: "英文（或项目指定）"
    encoding: "UTF-8"
    line_length: "建议 ≤120 字元"
    diagrams: "優先使用 Mermaid，其次 ASCII Art"
    links: "內部連結使用相对路徑"
  maintenance:
    sync: "程序码变更时更新文件"
    version: "頂部標示版本和日期"
    review: "文件变更納入程序码审查"
    periodic: "每季检查文件是否過时"
```

---

## 项目类型文件需求

### 文件需求矩陣

| 文件 | 新项目 | 重構 | 迁移 | 維護 |
|------|:------:|:----:|:----:|:----:|
| **README.md** | ✅ 必要 | ✅ 必要 | ✅ 必要 | ✅ 必要 |
| **ARCHITECTURE.md** | ✅ 必要 | ✅ 必要 | ✅ 必要 | ⚪ 建议 |
| **API.md** | ⚪ 如適用 | ✅ 必要 | ✅ 必要 | ⚪ 建议 |
| **DATABASE.md** | ⚪ 如適用 | ✅ 必要 | ✅ 必要 | ⚪ 建议 |
| **DEPLOYMENT.md** | ✅ 必要 | ✅ 必要 | ✅ 必要 | ⚪ 建议 |
| **MIGRATION.md** | ❌ 不需要 | ✅ 必要 | ✅ 必要 | ❌ 不需要 |
| **ADR/** | ⚪ 建议 | ✅ 必要 | ✅ 必要 | ⚪ 如適用 |
| **CHANGELOG.md** | ✅ 必要 | ✅ 必要 | ✅ 必要 | ✅ 必要 |

### 项目类型快速參考

```
🆕 新项目     → README + ARCHITECTURE + DEPLOYMENT + CHANGELOG
🔄 重構       → 所有文件 + MIGRATION + ADR（记录「为何重構」）
🚚 迁移       → 所有文件 + MIGRATION（核心文件）+ 数据验证
🔧 維護       → README + CHANGELOG（依变更範圍更新）
```

---

## 文件金字塔

```
                    ┌─────────────┐
                    │   README    │  ← 入口点，快速概覽
                    ├─────────────┤
                 ┌──┴─────────────┴──┐
                 │   ARCHITECTURE    │  ← 系统概述
                 ├───────────────────┤
              ┌──┴───────────────────┴──┐
              │  API / DATABASE / DEPLOY │  ← 技術細节
              ├─────────────────────────┤
           ┌──┴─────────────────────────┴──┐
           │    ADR / MIGRATION / CHANGELOG │  ← 变更历史
           └───────────────────────────────┘
```

---

## 文件範本（YAML 壓縮格式）

```yaml
# === README.md ===
readme:
  minimum:
    - "# 项目名称"
    - "簡短的单行描述"
    - "## 安裝"
    - "## 使用"
    - "## 授权"
  recommended:
    - "# 项目名称 + 徽章"
    - "## 功能（项目符号列表）"
    - "## 安裝"
    - "## 快速入門 / 使用"
    - "## 文件（連結至 docs/）"
    - "## 貢獻（連結至 CONTRIBUTING.md）"
    - "## 授权"

# === ARCHITECTURE.md ===
architecture:
  required:
    - system_overview: "目的、範圍、主要功能"
    - architecture_diagram: "Mermaid 或 ASCII Art"
    - module_description: "職責、相依性"
    - technology_stack: "框架、语言、版本"
    - data_flow: "主要业务流程"
  recommended:
    - deployment_architecture: "生产環境拓撲"
    - design_decisions: "关鍵决策（或連結至 ADR）"

# === API.md ===
api:
  required:
    - api_overview: "版本、基礎 URL、身份验证"
    - authentication: "Token 取得、過期时间"
    - endpoint_list: "所有 API 端点"
    - endpoint_specs: "请求/响应格式"
    - error_codes: "错误码和说明"
  recommended:
    - code_examples: "常見语言的範例"
    - rate_limiting: "API 呼叫頻率限制"
  endpoint_format: |
    ### POST /api/v1/resource
    **请求**: | 欄位 | 类型 | 必要 | 说明 |
    **响应**: | 欄位 | 类型 | 说明 |
    **错误**: | 代码 | 说明 |

# === DATABASE.md ===
database:
  required:
    - db_overview: "类型、版本、連线信息"
    - er_diagram: "实体关系图"
    - table_list: "所有数据表及用途"
    - table_specs: "欄位定義"
    - index_docs: "索引策略"
    - migration_scripts: "脚本位置"
  recommended:
    - backup_strategy: "頻率、保留期限"
  table_format: |
    ### 数据表名称
    **欄位**: | 欄位 | 类型 | 可为空 | 预设值 | 说明 |
    **索引**: | 名称 | 欄位 | 类型 |
    **关联**: | 关联表 | 連接欄位 | 关系 |

# === DEPLOYMENT.md ===
deployment:
  required:
    - environment_requirements: "硬体、软体、网络"
    - installation_steps: "详细流程"
    - configuration: "设置檔參數"
    - verification: "确认部署成功"
    - troubleshooting: "常見問題和解决方案"
  recommended:
    - monitoring: "健康检查、日誌位置"
    - scaling_guide: "水平/垂直擴展"

# === MIGRATION.md ===
migration:
  required:
    - overview: "目標、範圍、时程"
    - prerequisites: "必要准备工作"
    - migration_steps: "详细流程"
    - verification_checklist: "迁移後检查"
    - rollback_plan: "失败时的步骤"
    - backward_compatibility: "API/数据庫相容性"
  recommended:
    - partner_notification: "需通知的外部系统"

# === ADR（架構决策记录）===
adr:
  filename: "NNN-kebab-case-title.md（例如：001-use-postgresql.md）"
  required:
    - title: "决策名称"
    - status: "proposed | accepted | deprecated | superseded"
    - context: "为何需要此决策"
    - decision: "具体决策内容"
    - consequences: "影響（正面/負面）"
  recommended:
    - alternatives: "考慮過的其他选项"
```

---

## 文件位置标准

```
project-root/
├── README.md                    # 项目入口文件
├── CONTRIBUTING.md              # 貢獻指南
├── CHANGELOG.md                 # 变更日誌
├── LICENSE                      # 授权文件
└── docs/                        # 文件目录
    ├── INDEX.md                 # 文件索引
    ├── ARCHITECTURE.md          # 架構文件
    ├── API.md                   # API 文件
    ├── DATABASE.md              # 数据庫文件
    ├── DEPLOYMENT.md            # 部署文件
    ├── MIGRATION.md             # 迁移文件（如需要）
    └── ADR/                     # 架構决策记录
        ├── 001-xxx.md
        └── ...
```

---

## README.md 必要章节

### 最小可行 README

```markdown
# 项目名称

簡短的单行描述。

## 安裝

```bash
npm install your-package
```

## 使用

```javascript
const lib = require('your-package');
lib.doSomething();
```

## 授权

MIT
```

### 建议的 README 章节

1. **项目名称与描述**
2. **徽章**（CI 状态、覆蓋率、npm 版本）
3. **功能**（项目符号列表）
4. **安裝**
5. **快速入門 / 使用**
6. **文件**（連結至 docs/）
7. **貢獻**（連結至 CONTRIBUTING.md）
8. **授权**

---

## ADR 範本

```markdown
# ADR-001: [决策標題]

## 状态
已接受

## 背景
[为何需要此决策...]

## 决策
[具体决策内容...]

## 影響

### 正面
- 好处 1
- 好处 2

### 負面
- 缺点 1
- 缺点 2

## 考慮過的替代方案
1. 方案 A - 因为...而被拒絕
2. 方案 B - 因为...而被拒絕
```

---

## 文件稽核检查清单

审查项目文件时：

```
□ README.md 存在且包含必要章节
□ 安裝说明清楚且經過测试
□ 使用範例已提供且可运作
□ 已指定授权
□ ARCHITECTURE.md 存在（非簡单项目）
□ API.md 存在（如有暴露 API）
□ DATABASE.md 存在（如使用数据庫）
□ DEPLOYMENT.md 存在（已部署的项目）
□ ADR/ 存在於重大决策
□ CHANGELOG.md 遵循 Keep a Changelog 格式
□ 所有內部連結正常运作
□ 图表是最新的
□ 無過时信息
```

---

## 配置偵测

### 偵测順序

1. 检查 `CONTRIBUTING.md` 中的「停用 Skills」區段
2. 检查 `CONTRIBUTING.md` 中的「文件语言」區段
3. 检查現有文件结构
4. 若未找到，**预设为英文**

### 首次设置

如果缺少文件：

1. 詢問：「此项目没有完整的文件。应該使用哪种语言？(English / 中文)」
2. 判斷项目类型（新项目/重構/迁移/維護）
3. 依矩陣建立必要文件
4. 建议在 `CONTRIBUTING.md` 中记录：

```markdown
## 文件标准

### 语言
此项目使用 **英文** 作为文件语言。

### 必要文件
根据项目类型，我們維護：
- README.md
- ARCHITECTURE.md
- DEPLOYMENT.md
- CHANGELOG.md
```

---

## 详细指南

完整标准請參阅：
- [文件撰写标准](../../../core/documentation-writing-standards.md)
- [文件结构标准](../../../core/documentation-structure.md)
- [README 範本](./readme-template.md)

---

## 相关标准

- [文件撰写标准](../../../core/documentation-writing-standards.md) - 内容需求
- [文件结构标准](../../../core/documentation-structure.md) - 文件組織
- [变更日誌标准](../../../core/changelog-standards.md) - CHANGELOG 格式
- [变更日誌指南技能](../changelog-guide/SKILL.md) - CHANGELOG 技能

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.0.0 | 2026-01-12 | 新增：项目类型矩陣、文件範本、文件金字塔 |
| 1.0.0 | 2025-12-24 | 初始版本 |

---

## 授权

本 Skill 以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授权發布。

**來源**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
