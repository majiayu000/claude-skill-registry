---
source: skills/refactoring-assistant/SKILL.md
source_version: 2.0.0
translation_version: 2.0.0
last_synced: 2026-01-21
status: current
name: refactor
description: |
  引導重構決策和大規模程式碼改進。
  使用時機：重構程式碼、遺留系統現代化、技術債、重寫決策。
  關鍵字：refactor, rewrite, legacy, strangler, technical debt, 重構, 重寫, 技術債.
---

# 重構助手

> **語言**: [English](../../../../skills/refactoring-assistant/SKILL.md) | 繁體中文

**版本**: 2.0.0
**最後更新**: 2026-01-21
**適用範圍**: Claude Code Skills

---

## 目的

本技能提供重構與重寫的決策框架、大規模重構模式，以及技術債管理。策略分為三個層級：戰術性（日常）、戰略性（架構）、安全防護（遺留程式碼）。

---

## 快速參考（YAML 壓縮格式）

```yaml
# === 決策：重構 vs 重寫 ===
decision_tree:
  - q: "程式碼在生產環境運行？"
    n: "→ 考慮重寫（風險較低）"
    y: next
  - q: "了解程式碼的功能？"
    n: "→ 先寫特徵測試"
    y: next
  - q: "測試覆蓋率 >60%？"
    n: "→ 先補測試"
    y: next
  - q: "核心架構可修復？"
    n: "→ Strangler Fig 模式"
    y: "→ 增量重構 ✓"

comparison_matrix:
  favor_refactor: [大型程式庫, 良好測試, 業務關鍵, 團隊熟悉, 架構健全, 時間緊迫, 低風險]
  favor_rewrite: [小型獨立, 無測試, 可容忍停機, 無人熟悉, 架構有缺陷, 時間充裕, 較高風險]

# === 警告：第二系統效應 ===
rewrite_antipatterns:
  - "加入原本沒有的功能"
  - "為未來彈性過度抽象"
  - "忽略現有系統的經驗教訓"
quote: "第二個系統是一個人設計過最危險的系統。— Fred Brooks"

# === 戰術性策略：日常重構 ===
tactical:
  preparatory_refactoring:
    definition: "在新增功能前調整結構，讓改變更容易"
    quote: "先把改變變容易（這可能很難），然後再做那個容易的改變。— Kent Beck"
    when: [功能被阻擋, 降低阻力, 即將變更]
    workflow:
      1: "識別要做的改變"
      2: "識別是什麼讓改變困難"
      3: "重構以讓改變變容易"
      4: "做那個（現在變容易的）改變"
    principles:
      - "預備性重構與功能分開提交"
      - "每一步都維持測試通過"
      - "不要混合重構與功能工作"

  boy_scout_rule:
    definition: "離開時讓程式碼比來時更乾淨（機會主義重構）"
    quote: "離開營地時，讓它比你來的時候更乾淨。— Robert C. Martin"
    when: [任何維護, Bug修復, 功能新增, 對抗熵]
    guidelines:
      - "只做小改進（分鐘，不是小時）"
      - "不改變行為"
      - "不破壞現有測試"
      - "保持範圍在當前任務內"
    examples:
      - "重新命名令人困惑的變數"
      - "將幾行程式碼提取為命名良好的方法"
      - "移除死程式碼"
      - "加入澄清註解"
    antipatterns:
      - "把 Bug 修復變成大重構"
      - "重構不相關的程式碼"
      - "沒有測試覆蓋就修改"
      - "範圍蔓延超出原始任務"

  red_green_refactor:
    definition: "TDD 重構階段"
    duration: "每循環 5-15 分鐘"
    scope: "單一方法/類別"
    techniques: [提取方法, 重新命名, 內聯變數, 替換魔術數字]
    reference: "→ 見 TDD 標準"

# === 戰略性策略：架構重構 ===
strategic:
  strangler_fig:
    definition: "逐步將功能路由到新系統，漸進替換舊系統"
    origin: "命名自絞殺榕樹"
    phases:
      1_攔截: "請求 → 門面 → 舊系統(100%)"
      2_遷移: "請求 → 門面 → [新系統(功能), 舊系統(其餘)]"
      3_完成: "請求 → 新系統(100%) [舊系統下線]"
    checklist:
      - "識別攔截點"
      - "建立事件捕獲層"
      - "在新系統實作第一個功能"
      - "漸進式路由流量"
      - "監控並比較"
      - "下線舊系統"

  anti_corruption_layer:
    definition: "防止遺留模型污染新系統的翻譯層"
    origin: "Eric Evans, 領域驅動設計 (2003)"
    when:
      - "新舊系統必須共存並互動"
      - "遺留系統有混亂的領域模型"
      - "保護新系統的限界上下文"
    components:
      facade: "簡化複雜的遺留介面"
      adapter: "將遺留資料轉換為新領域模型"
      translator: "映射遺留術語到通用語言"
    checklist:
      - "定義清晰的 ACL 介面"
      - "映射遺留實體到新模型"
      - "處理資料格式轉換"
      - "實作錯誤翻譯"
      - "加入日誌以便除錯"
      - "徹底測試 ACL 隔離性"
    vs_strangler:
      strangler: "目標是取代遺留"
      acl: "目標是與遺留共存"

  branch_by_abstraction:
    steps:
      1: "客戶端 → 抽象(介面) → 舊實作"
      2: "客戶端 → 抽象 → [舊實作, 新實作(切換)]"
      3: "客戶端 → 新實作 [舊實作已移除]"
    principles: [所有變更在主幹, 功能開關, 過渡期共存]

  parallel_change:
    aka: "Expand-Migrate-Contract"
    phases:
      expand: "新增新的在舊的旁邊，新程式碼用新的，舊的仍運作"
      migrate: "更新所有客戶端用新的，驗證，資料遷移"
      contract: "移除舊的，清理，更新文件"

# === 安全策略：遺留程式碼 ===
safety:
  legacy:
    definition: "沒有測試的程式碼（不論年齡）"
    dilemma: "安全修改需要測試 → 加測試需要修改程式碼"
    solution: "使用安全技術先加測試"

  characterization_tests:
    purpose: "捕捉現有行為（非驗證正確性）"
    process:
      1: "呼叫要理解的程式碼"
      2: "寫預期會失敗的斷言"
      3: "執行，觀察實際結果"
      4: "更新斷言以匹配實際行為"
      5: "重複直到涵蓋需要修改的行為"
    principle: "記錄程式碼做什麼，而非應該做什麼"

  scratch_refactoring:
    definition: "為了理解而重構，捨棄所有變更"
    workflow:
      1: "建立探針分支（或 git stash）"
      2: "大膽重構以理解"
      3: "記錄學到的內容"
      4: "捨棄變更（git reset --hard）"
      5: "應用學習撰寫特徵測試"
    when: [程式碼太複雜, 無文件, 需要快速建立心智模型]
    principle: "目標是理解，不是整潔程式碼"

  seams:
    definition: "可以在不編輯程式碼的情況下改變行為的地方"
    object: "透過多型覆寫（注入測試替身）"
    preprocessing: "編譯時替換（巨集）"
    link: "連結時替換（DI，模組替換）"

  sprout_wrap:
    sprout_method: "新邏輯 → 建立新方法，從舊的呼叫"
    sprout_class: "新邏輯獨立演進 → 新類別"
    wrap_method: "加入前後行為 → 重命名原方法，建立包裝器"
    wrap_class: "裝飾現有 → 裝飾者模式"
    principle: "新程式碼用 TDD；遺留程式碼在測試前保持不動"

# === 資料庫：重構 ===
db_expand_contract:
  expand: "新增新欄位/表，應用程式同時寫入，可安全回滾"
  migrate: "複製資料，驗證一致性，應用程式從新的讀取"
  contract: "確認舊的未使用，移除舊的，清理雙寫"

db_scenarios:
  rename_column: {strategy: "新增→遷移→刪除", risk: 中}
  split_table: {strategy: "新表+外鍵→遷移→調整", risk: 高}
  merge_tables: {strategy: "新表→合併→切換", risk: 高}
  change_datatype: {strategy: "新欄位→轉換→切換", risk: 中}
  add_not_null: {strategy: "填預設→加約束", risk: 低}

# === 工作流程：安全重構 ===
before: [定義成功標準, "覆蓋率>80%", 乾淨工作目錄, 建立分支, 與團隊溝通]
during: [一次一個小變更, 每次變更後測試, 失敗就復原, 頻繁提交, 不加新功能]
after: [所有測試通過, 可衡量地更好, 文件已更新, 團隊已審查, 沒有新功能]

# === 指標 ===
code_quality:
  cyclomatic_complexity: "每函式<10"
  cognitive_complexity: "越低越好"
  coupling: "降低"
  cohesion: "提高"
  duplication: "<3%"

test_quality:
  coverage: "≥80%，不降低"
  speed: "重構後更快"
  flaky_count: "降低"

# === 技術債管理 ===
quadrant: # Martin Fowler
  prudent_deliberate: "我們知道這是債務"
  reckless_deliberate: "沒時間做設計"
  prudent_inadvertent: "現在知道應該怎麼做了"
  reckless_inadvertent: "什麼是分層？"

priority:
  high: {criteria: "阻塞開發，頻繁出錯", action: "立即處理"}
  medium: {criteria: "拖慢開發，增加複雜度", action: "規劃到下個迭代"}
  low: {criteria: "小麻煩，影響局部", action: "有機會就處理"}

tracking:
  fields: [描述, 影響, 估計工作量, 忽視風險, 相關程式碼]

# === 決策矩陣摘要 ===
decision_matrix:
  - {strategy: "預備性重構", scale: "小", risk: "低", use: "降低功能開發阻力"}
  - {strategy: "童子軍規則", scale: "極小", risk: "低", use: "持續償債"}
  - {strategy: "紅-綠-重構", scale: "小", risk: "低", use: "TDD 開發循環"}
  - {strategy: "絞殺榕", scale: "大", risk: "中", use: "系統汰換"}
  - {strategy: "防腐層", scale: "中", risk: "低", use: "新舊共存"}
  - {strategy: "抽象分支", scale: "大", risk: "中", use: "主幹重構"}
  - {strategy: "平行變更", scale: "中", risk: "低", use: "介面/Schema 遷移"}
  - {strategy: "特徵測試", scale: "—", risk: "—", use: "遺留重構的前置條件"}
  - {strategy: "探針式重構", scale: "小", risk: "低", use: "理解黑盒程式碼"}

# === 策略選擇 ===
selection_guide:
  功能被混亂程式碼阻擋: "預備性重構"
  在Bug修復中接觸程式碼: "童子軍規則"
  用TDD寫新程式碼: "紅-綠-重構"
  取代整個遺留系統: "絞殺榕"
  整合遺留不被污染: "防腐層"
  在主幹重構共享程式碼: "抽象分支"
  變更廣泛使用的介面: "平行變更"
  處理未測試的遺留: "特徵測試 + 探針式重構 先做"
```

---

## 配置偵測

### 偵測順序

1. 檢查 `CONTRIBUTING.md` 中的「停用技能」區段
2. 檢查 `CONTRIBUTING.md` 中的「重構標準」區段
3. 如果未找到，**預設使用標準重構實踐**

---

## 詳細指南

完整標準請參閱：
- [重構標準](../../core/refactoring-standards.md)

---

## 相關標準

- [重構標準](../../core/refactoring-standards.md) - 核心標準
- [測試驅動開發](../../core/test-driven-development.md) - TDD 重構階段
- [程式碼審查檢查清單](../../core/code-review-checklist.md) - 重構 PR 審查
- [簽入標準](../../core/checkin-standards.md) - 提交前要求
- [TDD 助手](../tdd-assistant/SKILL.md) - TDD 工作流程

---

## 版本歷史

| 版本 | 日期 | 變更 |
|------|------|------|
| 2.0.0 | 2026-01-21 | 新增戰術性策略（預備性重構、童子軍規則）、防腐層、決策矩陣摘要。重組為戰術性/戰略性/安全防護三層。 |
| 1.0.0 | 2026-01-12 | 初始發布 |

---

## 授權

本技能以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授權發布。

**來源**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
