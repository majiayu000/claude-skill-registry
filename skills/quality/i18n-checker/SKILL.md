# i18n Checker

i18n 硬編碼檢查和批量處理工具。

## 與 Style Guardian 的關係

| 工具 | 用途 | 適用場景 |
|-----|------|---------|
| **style-guardian** | 快速檢查 UI 層的樣式和 i18n | CI/CD、pre-commit hook、日常開發 |
| **i18n-checker** | 深入批量處理所有中文硬編碼 | 大規模重構、技術債務清理、ARB 建議生成 |

Style Guardian 的 i18n 檢查：
- 只檢查 `Text()`, `AppBar title`, `labelText/hintText`
- 適合快速發現明顯問題

i18n Checker 的優勢：
- 檢測所有中文字串（包括 Model、Service 層）
- 生成 ARB 鍵值建議
- 分別統計 lib/ 和 test/
- 支援批量處理工作流程

## 使用時機

- 當需要檢查專案中**所有**硬編碼中文字串（不只是 UI 層）
- 當需要進行大規模 i18n 修復
- 當需要生成 ARB 鍵值建議
- 技術債務評估

## 基本使用

### 快速摘要

```bash
uv run scripts/i18n_hardcode_checker.py
```

輸出：
```text
i18n 硬編碼檢查結果:
  總計: 11918 處
  lib/: 1966 處
  test/: 9952 處
```

### 詳細報告

```bash
uv run scripts/i18n_hardcode_checker.py --report > docs/i18n-report.md
```

生成 Markdown 格式的詳細報告，包含：
- 每個檔案的硬編碼位置
- 建議的 i18n 鍵名
- 分類統計（lib/ vs test/）

### ARB 建議

```bash
uv run scripts/i18n_hardcode_checker.py --arb
```

生成 JSON 格式的 ARB 鍵值建議：
```json
{
  "suggestedKey": {
    "value_zh": "原始中文字串",
    "value_en": "[TODO: 原始中文字串]",
    "description": "From file_path:line_number"
  }
}
```

### JSON 輸出

```bash
uv run scripts/i18n_hardcode_checker.py --json
```

生成結構化 JSON 資料，適合程式處理：
```json
{
  "summary": {
    "total": 11918,
    "lib": 1966,
    "test": 9952
  },
  "items": [...]
}
```

## 標準工作流程

### 1. 檢查階段

```bash
# 執行檢查
uv run scripts/i18n_hardcode_checker.py

# 如果發現大量硬編碼，生成報告
uv run scripts/i18n_hardcode_checker.py --report > docs/i18n-report.md
```

### 2. 分類階段

根據報告，將硬編碼分為：

| 分類 | 處理方式 |
|-----|---------|
| UI 層 (presentation/) | 直接使用 l10n |
| ViewModel 層 | 返回代碼，讓 UI 處理 |
| Domain/Model 層 | 移除 UI 文字，改用代碼 |
| Test 層 | 使用 MockAppLocalizations |

### 3. 批量處理階段

對於大量硬編碼：

1. 生成 ARB 建議
```bash
uv run scripts/i18n_hardcode_checker.py --arb > arb_suggestions.json
```

2. 手動審核建議
3. 添加到 ARB 檔案
4. 運行 `flutter gen-l10n`
5. 批量替換程式碼

### 4. 驗證階段

```bash
# 再次檢查
uv run scripts/i18n_hardcode_checker.py

# 確認數量減少
```

---

## 混合處理模式

大規模 i18n 技術債務的有效處理策略。

### 核心理念

**不同複雜度使用不同處理手段，最大化效率和品質**

### 複雜度分級

| 等級 | 描述 | 處理策略 | 範例 |
|------|------|---------|------|
| **A** | 簡單 UI 文字 | 腳本自動替換 | `Text('確認')` → `Text(l10n.confirm)` |
| **B** | 需評估內容 | 多代理人平行處理 | ViewModel 層訊息 |
| **C** | 需架構重構 | 建立獨立 Ticket | Domain 層硬編碼 |
| **D** | 測試檔案 | 逐案評估 | 測試輸出訊息 vs 驗證條件 |

### 等級判斷標準

**等級 A - 簡單 UI 文字**：
- 在 `presentation/` 或 `core/ui/` 目錄
- 直接在 Widget 中顯示的文字
- 已有對應 ARB 鍵值或可直接新增

**等級 B - 需評估內容**：
- ViewModel 層的訊息
- 需要判斷是 UI 文字還是業務邏輯
- 可能需要返回代碼讓 UI 處理

**等級 C - 需架構重構**：
- Domain/Model 層的中文字串
- 違反分層 i18n 規範
- 需要改為代碼/枚舉，由 UI 層翻譯

**等級 D - 測試檔案**：
- 測試輸出訊息：可使用 MockAppLocalizations
- 測試驗證條件：可能需要改用代碼比對
- 不應一概跳過

### 批量替換腳本

針對等級 A，使用批量替換腳本：

```bash
# Dry run（預設）
uv run scripts/i18n_batch_replace.py --target lib/presentation

# 實際替換
uv run scripts/i18n_batch_replace.py --target lib/presentation --apply

# 生成報告
uv run scripts/i18n_batch_replace.py --target lib/presentation --report
```

腳本會自動處理常見映射：
- 按鈕文字：確認、取消、提交、搜尋...
- 狀態文字：載入中、搜尋中、同步中...
- 連線狀態：已連線、離線中、未知狀態...

### 混合處理工作流程

```text
1. 分析階段
   └─ uv run scripts/i18n_hardcode_checker.py --json
   └─ 將結果分類為 A/B/C/D 等級

2. 等級 A 處理
   └─ 新增 ARB 鍵值
   └─ flutter gen-l10n
   └─ uv run scripts/i18n_batch_replace.py --apply

3. 等級 B 處理
   └─ 多代理人平行評估
   └─ 決定各項目歸屬（A/C/保留）

4. 等級 C 處理
   └─ 建立 Atomic Tickets
   └─ 按依賴順序排程

5. 等級 D 處理
   └─ 逐案評估
   └─ 不跳過，記錄評估結果
```

### Ticket 派生策略

當發現等級 C（需架構重構）項目時：

| 情況 | 處理方式 |
|------|---------|
| Domain 層包含 UI 文字 | 建立重構 Ticket（如 W2-001） |
| 默認參數硬編碼 | 建立策略 Ticket（如 W2-002） |
| 跨多檔案的模式 | 建立批量處理 Ticket |

### 實戰案例

**v0.25.1 i18n 技術債務處理**：

| 等級 | 數量 | 處理方式 | Ticket |
|------|------|---------|--------|
| A | 35 處 | 腳本替換 | W1-004 |
| B | 90 處 | 待評估 | W1-004 |
| C | 947 處 | 架構重構 | W2-001 |
| C | 3 處 | 默認參數 | W2-002 |

### 注意事項

1. **不要急於替換**：先分析、分類、再處理
2. **保留評估紀錄**：等級 B/D 項目需記錄評估結果
3. **尊重架構分層**：Domain 層不應直接包含 UI 文字
4. **測試檔案特殊**：測試中的硬編碼可能是有意為之

## 排除規則

腳本會自動排除以下模式：

- 註解（單行、多行、文檔）
- import 語句
- package 路徑
- ARB 檔案引用
- URL
- 生成的檔案 (.g.dart, generated/)
- l10n 目錄

## 建議鍵名邏輯

腳本會根據中文內容自動建議鍵名：

| 中文關鍵字 | 英文對應 |
|-----------|---------|
| 成功 | success |
| 失敗 | failed |
| 錯誤 | error |
| 匯入 | import |
| 匯出 | export |
| 書籍 | book |
| 載入 | loading |
| 完成 | completed |

## 與其他工具整合

### Style Guardian

```bash
# 先執行 style guardian 檢查
/style-guardian

# 再執行 i18n 檢查
uv run scripts/i18n_hardcode_checker.py
```

### CI/CD

可在 CI 中加入：
```yaml
- name: Check i18n
  run: |
    result=$(uv run scripts/i18n_hardcode_checker.py --json)
    lib_count=$(echo $result | jq '.summary.lib')
    if [ $lib_count -gt 100 ]; then
      echo "Warning: $lib_count hardcoded strings in lib/"
    fi
```

## 相關資源

- [分層 i18n 管理方法論]($CLAUDE_PROJECT_DIR/.claude/methodologies/layered-i18n-management-methodology.md)
- [DOC-003 ViewModel 層硬編碼規範]($CLAUDE_PROJECT_DIR/docs/work-logs/v0.25.1/tickets/0.25.1-DOC-003.md)
- [Style Guardian Skill]($CLAUDE_PROJECT_DIR/.claude/skills/style-guardian/)

## 維護資訊

**建立日期**: 2026-01-14
**更新日期**: 2026-01-15
**維護者**: 主線程
**腳本位置**:
- `scripts/i18n_hardcode_checker.py` - 硬編碼檢查腳本
- `scripts/i18n_batch_replace.py` - 批量替換腳本
