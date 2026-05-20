---
name: Git PR Description
description: 根據當前 branch 與目標 branch 的差異，自動產生 Pull Request 的 Title 與 Description。當使用者提到「PR」、「Pull Request」、「寫 PR」、「PR 描述」、「PR description」、「建立 PR」時觸發此 Skill。
---

# Git PR Description — 自動產生 PR 標題與描述

根據當前 branch 相對於目標 branch（預設 `master`）的所有 commit 與 diff，產出結構化的 PR Title 與 Description。

---

## 流程

### 1. 確認分支資訊

取得當前 branch 名稱與目標 branch：

```bash
git branch --show-current
```

預設目標 branch 為 `master`。若使用者指定其他 base branch，以使用者指定為準。

確認當前 branch 相對於目標 branch 有 commit 差異：

```bash
git log --oneline master..HEAD
```

若無差異，告知使用者「當前 branch 與目標 branch 沒有差異」後結束。

---

### 2. 蒐集變更資訊

取得完整的 commit 列表與 diff：

```bash
# commit 摘要
git log --oneline master..HEAD

# 詳細 commit 訊息
git log --format="%h %s%n%b" master..HEAD

# 變更檔案統計
git diff --stat master..HEAD

# 完整 diff（用於分析具體改動）
git diff master..HEAD
```

---

### 3. 分析變更內容

根據蒐集到的資訊，分析：

- **變更的目的**：這個 branch 要解決什麼問題或新增什麼功能
- **修改範圍**：涉及哪些元件、模組、設定檔
- **影響層面**：是否有破壞性變更、是否影響既有功能

---

### 4. 產生 PR Title

#### Title 格式

```
<type>: <簡短描述>
```

**type 對照表：**

| type | 使用時機 |
|------|----------|
| `feat` | 新增功能 |
| `fix` | 修復 bug |
| `refactor` | 重構 |
| `style` | 樣式調整 |
| `chore` | 雜務、設定 |
| `docs` | 文件更新 |
| `test` | 測試相關 |

**Title 規則：**

- 使用繁體中文描述
- 不超過 72 字
- 用動詞開頭：新增、調整、修正、移除、重構
- 精準描述此 PR 的核心目的

---

### 5. 產生 PR Description

使用 `references/pr-template.md` 中的模板產生 Description。

#### Description 結構

```markdown
## 🎯 為什麼要這樣做

簡述此 PR 的背景與動機

## ⚠️ 修改的內容

依功能與需求分組：
- **功能名稱 / 需求項目**：說明此組變更的業務目標
- **修改方向**：簡述（效能、修復、樣式等）
- **內容**：列出具體修改點，**禁止**出現任何檔案路徑（包含相對路徑），一律改用功能描述，例如「新增手風琴展開動畫」而非「修改 `src/components/FAQ.jsx`」

### [功能名稱 / 需求項目]
- **修改方向**：...
- **內容**：
  - 具體修改點 1（純功能描述）
  - 具體修改點 2（純功能描述）

### [另一個功能名稱]
- **修改方向**：...
- **內容**：
  - ...

## 🧪 測試步驟

> **規則：必須為「修改的內容」中列出的每一個模組 / 元件都產生至少一個對應的測試案例，確保所有變更皆被涵蓋。**

### 測試案例 1：[針對模組 A 的測試情境]

1. 操作步驟一
2. 操作步驟二
3. **預期結果**：描述預期行為

### 測試案例 2：[針對模組 B 的測試情境]

1. 操作步驟一
2. 操作步驟二
3. **預期結果**：描述預期行為

### 測試案例 N：[依此類推，直到所有變更模組皆有對應測試]
```

---

### 6. 輸出結果

將完整的 PR Title + Description 以 **markdown code block** 的形式輸出，讓使用者可以直接複製貼上到 GitHub PR。

輸出格式（整段用 markdown code block 包裹）：

````
```markdown
<title>

<description 完整 markdown 內容，包含 ##、###、列表等格式>
```
````

**注意事項：**
- 不要在 code block 外面加額外的 `📝 PR Title:` 等前綴，直接輸出可複製的 markdown
- code block 內的第一行為 PR Title，空一行後接 Description
- 使用者可要求調整任何部分後再複製使用
- **重要**：Description 中**禁止**出現任何檔案路徑（包含相對路徑），一律改用純功能描述。

---

## 🛑 格式嚴格規範

- **禁止任何 Markdown 連結格式**：`[文字](...)`
- **禁止任何 URI / scheme**：比如 `file://`、`cci:`
- **禁止出現任何檔案路徑**：不論相對或絕對路徑，一律不出現在 Description 中，改以純功能描述取代

## 邊界情況處理

- **存在未提交的變更**：提醒使用者先提交或 stash，避免遺漏

## Additional Resources

### Reference Files

- **`references/pr-template.md`** — PR Description 的完整模板，可依團隊需求客製化
