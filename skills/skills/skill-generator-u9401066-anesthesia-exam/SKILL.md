---
name: skill-generator
description: 自動生成符合標準的 SKILL.md 和資料夾結構。
---

---
name: skill-generator
description: Generate new skills with standardized structure and frontmatter. Triggers: SG, new skill, 新增 skill, 建立技能, create skill, 新技能, 產生技能, generate skill, 技能模板, skill template, add skill, 加技能, make skill.
category: meta
version: 1.0.0
compatibility:
  - claude-code
  - github-copilot
  - vscode
allowed-tools:
  - read_file
  - create_file
  - list_dir
---

# Skill 生成器

## 描述

自動生成符合標準的 SKILL.md 和資料夾結構。

## 觸發條件

- 「新增 skill」「建立技能」「create skill」「SG」

## 標準格式規範

### YAML Frontmatter（必要）

```yaml
---
name: skill-name          # kebab-case 必須（小寫 + 連字號）
description: 描述         # 包含 WHAT + WHEN + Triggers
category: core            # core/workflow/meta/integration
version: 1.0.0            # SemVer
compatibility:            # 支援的平台（可選）
  - claude-code
  - github-copilot
  - vscode
allowed-tools:            # 可使用的工具（可選）
  - read_file
  - write_file
orchestrates:             # 組合的其他 skills（workflow 用）
  - skill-a
  - skill-b
---
```

### 命名規則

| 規則 | 正確 ✅ | 錯誤 ❌ |
|------|---------|---------|
| kebab-case | `code-reviewer` | `codeReviewer`, `CodeReviewer` |
| 小寫 | `git-precommit` | `Git-Precommit` |
| 有意義 | `test-generator` | `tg`, `testgen` |
| 無底線 | `memory-bank` | `memory_bank` |

### 資料夾結構

```
.claude/skills/
└── skill-name/
    ├── SKILL.md           # 主要技能定義（必要）
    ├── references/        # 詳細參考文檔（可選）
    │   ├── examples.md
    │   └── api.md
    ├── templates/         # 範本檔案（可選）
    │   └── template.py
    └── scripts/           # 輔助腳本（可選）
        └── helper.ps1
```

## 生成流程

### Step 1: 收集資訊

```
❓ Skill 名稱：[輸入名稱，會自動轉 kebab-case]
❓ 描述：[一句話描述 + 觸發詞]
❓ 類別：[core/workflow/meta/integration]
❓ 需要額外資料夾嗎？[references/templates/scripts]
```

### Step 2: 驗證

- ✅ 名稱是 kebab-case
- ✅ 名稱不重複
- ✅ 描述包含觸發詞
- ✅ 類別有效

### Step 3: 生成

```
📁 建立 .claude/skills/{name}/
📄 建立 .claude/skills/{name}/SKILL.md
📁 建立子資料夾（如需要）
📝 更新 AGENTS.md skills 清單
```

## 使用範例

```
「新增 skill: api-tester」
「SG 建立 docker 管理技能」
「create skill for database migrations」
```

## 輸出範本

當你說「新增 skill: example-skill」，我會生成：

```markdown
---
name: example-skill
description: [描述]. Triggers: [觸發詞列表].
category: core
version: 1.0.0
compatibility:
  - claude-code
  - github-copilot
  - vscode
---

# [Skill 名稱]

## 描述

[詳細描述]

## 觸發條件

- 「[觸發詞 1]」「[觸發詞 2]」

## 執行流程

[流程圖或步驟]

## 參數

| 參數 | 說明 | 預設 |
|------|------|------|
| `--option` | 說明 | false |

## 使用範例

```
[範例 1]
[範例 2]
```

## 輸出格式

```
[預期輸出格式]
```
```

## Token 預算指南

| 項目 | 建議 | 上限 |
|------|------|------|
| SKILL.md 總行數 | < 300 行 | 500 行 |
| SKILL.md Token | < 3000 | 5000 |
| 單個區塊 | < 50 行 | 100 行 |

如果內容過長：
1. 拆分到 `references/` 子資料夾
2. 使用連結引用
3. 精簡主要邏輯
