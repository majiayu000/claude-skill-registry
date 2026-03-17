---
name: research-gap-analyzer
description: プロジェクト プロジェクトの機能(docs/features/)とリサーチ(docs/research/)文書を分析し、高収益/高LTV/低離脱達成のためのリサーチギャップを識別し、欠落したP0/P1リサーチを自動実行する。
doc_contract:
  review_interval_days: 90
---

# Research Gap Analyzer

プロジェクト プロジェクトの機能文書と既存リサーチを**ランタイムスキャン**し、高収益、高LTV、低離脱率達成に必要なリサーチギャップを自動識別するスキルである。

## 核心原則

### SSOT (Single Source of Truth)

```
┌─────────────────────────────────────────────────────────────┐
│  SSOT 構造 (v2.0 - Frontmatter ベース)                      │
├─────────────────────────────────────────────────────────────┤
│  docs/research/*.md Frontmatter   → リサーチメタデータ (SSOT) │
│                                      スキーマ: docs/_schemas/ │
│                                      research-frontmatter.  │
│                                      schema.json            │
│  docs/_manifests/research-manifest.json                     │
│                                   → Frontmatter から自動    │
│                                      生成されたキャッシュ (読取専用)│
│  assets/research-status.json      → リサーチ作業状態 (SSOT)  │
│  references/kpi-targets.md        → KPI 定義 + Feature マッピング │
│  references/critical-gaps.md      → クリティカルギャップリスト        │
│  docs/features/                   → 動的スキャン (SPEC 読込)    │
│  docs/research/README.md          → 文書リスト (参照用)       │
└─────────────────────────────────────────────────────────────┘

⚠️ 禁止: 同じデータを複数ファイルにハードコーディングしない。
   - Feature Tier は kpi-targets.md でのみ定義
   - リサーチ状態は assets/research-status.json でのみ管理
   - リサーチメタデータは各文書の Frontmatter でのみ定義
   - Manifest は直接修正しない (スクリプトで自動生成)
   - README.md は文書リストのみ、状態管理 X
```

### 批判的思考 5段階

1. **根本原因把握**: なぜこのギャップが発生したのか?
2. **完全性検証**: このリサーチが KPI 達成に十分か?
3. **業界標準比較**: Duolingo/Speak/ELSA はどうしているか?
4. **代替案検討**: 他のアプローチはないか?
5. **ROI 分析**: 効率性の観点から実行可能か?

---

## 核心 KPI 目標

> 詳細: [references/kpi-targets.md](references/kpi-targets.md)

| KPI                   | 目標値 | 現在のリサーチ状態 | ギャップ深刻度 |
| --------------------- | ------ | ------------------ | :------------: |
| D7 リテンション       | 25%+   | ✅ 十分            |       -        |
| 有料転換率            | 8%+    | ✅ 過剰供給        |       -        |
| 月間離脱率            | <8%    | 🔴 深刻なギャップ  |       P0       |
| LTV                   | $30+   | 🔴 深刻なギャップ  |       P0       |
| AI Max アップグレード | 20%+   | 🟡 部分的不足      |       P1       |

---

## 識別されたクリティカルギャップ (2026-01-19 分析基準)

> 詳細: [references/critical-gaps.md](references/critical-gaps.md)

### 🔴 P0 ギャップ (即座にリサーチ必要)

|  #  | ギャップ領域                 | KPI 影響          | 現況                       | 必要なリサーチ                             |
| :-: | ---------------------------- | ----------------- | -------------------------- | ------------------------------------------ |
|  1  | **Churn 防止プログラム設計** | 月間離脱率        | 概念のみで実行計画なし     | 再活性化キャンペーン、離脱信号検出         |
|  2  | **LTV 改善パス**             | LTV $30+          | 計算式のみで改善戦略なし   | サブスク期間延長、クロスセル戦略           |
|  3  | **AI コスト管理 & 価格戦略** | AI アップグレード | 心理学のみでコスト分析なし | トークン/クレジット システム、マージン分析 |
|  4  | **ペイウォール UX 最適化**   | 有料転換率        | 価格のみで UX 設計なし     | 参入障壁設計、転換ポイント                 |
|  5  | **学習動機再活性化**         | D7 リテンション   | プッシュのみで信号検出なし | D7/D14 閾値、最後の信号                    |

### 🟡 P1 ギャップ (1ヶ月以内にリサーチ必要)

|  #  | ギャップ領域                  | KPI 影響        | 現況                             |
| :-: | ----------------------------- | --------------- | -------------------------------- |
|  6  | FTUE 収益化ポイント           | 有料転換率      | D1~D7 最適転換ポイント未分析     |
|  7  | 習慣形成周期                  | D7 リテンション | 最適学習頻度/周期データ不足      |
|  8  | Duolingo Max 対応シナリオ     | 差別化          | 競合他社韓国語サポート時戦略なし |
|  9  | 日本人価格心理                | Japan-First     | 月/年/生涯転換率差異未分析       |
| 10  | AI コンテンツパイプライン ROI | 開発効率性      | 検収時間 & 品質測定データなし    |

---

## Workflow

### Step 1: ランタイムスキャン

**docs/features/** と **docs/research/** を直接スキャンする。

```python
# スキャン対象
features = scan("docs/features/*/PRD-*.md")  # 28個 Feature
research = scan("docs/research/*.md")         # 99個 リサーチ
```

**重要**: ハードコーディングされた Feature リストを使用せず、常に最新状態をスキャンする。

### Step 2: KPI-Feature-Research マッピング

**references/kpi-targets.md** を参照して KPI 別必要リサーチを導出する。

```yaml
# 例示: D7 リテンション KPI
d7_retention:
  target: 25%+
  primary_features: [004, 005, 006, 023]
  required_research:
    - FTUE 最適化 (ftue, onboarding, first-time)
    - 習慣形成 (habit, streak, routine)
    - プッシュ通知 (notification, push, reminder)
```

### Step 3: ギャップ識別 (批判的分析)

各リサーチの**品質**を評価する:

| 状態         | アイコン | 判断基準                         |
| ------------ | :------: | -------------------------------- |
| なし         |    🔴    | 該当主題ファイル 0個             |
| 概念のみ存在 |    🟡    | ファイルあるが Action Items なし |
| 完了         |    ✅    | ファイル + 実行計画 + データ根拠 |
| 更新必要     |    ⚪    | 修正日 > 180日                   |

**品質チェックリスト**:

1. Executive Summary 存在?
2. 定量的データ含む? (% 数値、ベンチマーク)
3. Action Items 具体的? (誰が、何を、いつ)
4. Japan-First 戦略と一致?

### Step 4: 優先順位決定

> 詳細: [references/critical-gaps.md](references/critical-gaps.md)

**ROI 基準優先順位**:

```
優先順位スコア = (KPI 影響度 × 3) + (実装容易性 × 2) + (Japan-First 適合性 × 1)
```

| 優先順位 | 基準                | 例                     |
| :------: | ------------------- | ---------------------- |
|    P0    | 収益/生存に直接影響 | Churn 防止、LTV 改善   |
|    P1    | 6ヶ月以内に必要     | 差別化、価格最適化     |
|    P2    | 1年以内に必要       | グローバル展開、高機能 |

### Step 5: 状態登録 + ディープリサーチ実行

> ⚠️ **重要**: P0 ギャップ発見時 **ユーザー確認なしに即座** にディープリサーチを実行する。

#### 5.1 状態ファイルに作業登録

ディープリサーチ開始**前**に `assets/research-status.json`に作業を登録する:

```json
{
  "job_id": "{topic}-{year}",
  "topic": "{リサーチ主題}",
  "phase": "processing",
  "provider": "openai|google",
  "created_at": "{現在時間}",
  "started_at": "{現在時間}",
  "ttl_expires_at": "{現在時間 + 24h}",
  "kpi_target": "{関連 KPI}",
  "priority": "P0|P1|P2"
}
```

> スキーマ: [references/research-status-schema.json](references/research-status-schema.json)

#### 5.2 ディープリサーチ実行

**Provider 選択ガイド**:

| Provider | 用途                   | コスト | 使用法                            |
| -------- | ---------------------- | ------ | --------------------------------- |
| `openai` | 深層分析、長文レポート | 高     | `deep-research --provider openai` |
| `google` | 最新データ、幅広い検索 | 中     | `deep-research --provider google` |

**リサーチ要求テンプレート**:

```markdown
## リサーチ要求: {gap_topic}

### 目標

プロジェクト アプリの {kpi_target} 達成

### コンテキスト

- Japan-First 戦略 (日本市場優先)
- 効率性重視 (自動化/低コスト必須)
- AI コンテンツ 100% (著作権 Free)

### 必須含む内容

1. 定量的データ (% 数値、ベンチマーク)
2. 競合社比較 (Duolingo, Speak, ELSA)
3. 実行可能な Action Items
4. 日本市場特殊性反映

### 出力形式

- 言語: 韓国語
- 形式: マークダウン
- 長さ: 1500-3000 単語
```

### Step 6: 結果保存 + 自動メタデータ生成

> ⚠️ **v5.0 変更**: AI が文書保存時に **Frontmatter を自動生成**し **スクリプトを自動実行**する。
> 人の手動作業が不要になるよう完全自動化される。

#### 6.1 ファイル保存 + 自動 Frontmatter 生成

**ファイル命名規則**:

```
{topic}-{subtopic}-{year}.md
例: churn-prevention-program-design-2026.md
```

**自動 Frontmatter 生成ロジック**:

AI がディープリサーチ結果を保存する際、文書内容を分析して **自動的に Frontmatter を生成**する:

```python
# AI メタデータ抽出ロジック (概念的)
def extract_metadata(document_content, topic, kpi_target):
    # 1. research_id 生成: R-{YYYYMMDD}-{順番}
    research_id = generate_research_id()

    # 2. category 自動決定
    category = classify_category(document_content)
    # 規則: 競合社言及多 → competitor
    #       価格/収益主題 → monetization
    #       技術詳細 → technical
    #       既定値 → strategy

    # 3. kpi_relevance: kpi_target + 本文キーワード分析
    kpi_relevance = detect_kpi_keywords(document_content, kpi_target)

    # 4. feature_domains: 本文から機能キーワード抽出
    feature_domains = extract_feature_keywords(document_content)

    # 5. competitors: 本文から競合社名抽出
    competitors = extract_competitor_names(document_content)

    # 6. scanner.keywords: 核心キーワード抽出 (上位 5-10個)
    keywords = extract_top_keywords(document_content)

    # 7. scanner.priority: kpi_relevance + category で決定
    priority = calculate_priority(kpi_relevance, category)

    # 8. quality 評価
    quality = assess_document_quality(document_content)

    # 9. 検索メタデータ抽出 (全てのリサーチ文書に適用)
    # 9.1 target_apps: 本文からアプリ名抽出
    target_apps = extract_app_names(document_content)

    # 9.2 target_user_levels: レベルキーワード抽出
    target_user_levels = extract_user_levels(document_content)

    # 9.3 pain_points: ペインポイントカテゴリキーワードマッチング
    pain_points = extract_pain_point_categories(document_content)

    # 9.4 learning_topics: 韓国語学習主題抽出
    learning_topics = extract_learning_topics(document_content)

    # 9.5 actionability: 実行可能性自動判断
    actionability = determine_actionability(document_content)

    return frontmatter_dict
```

**Frontmatter 自動生成規則**:

| フィールド               | 自動決定方法                                                                |
| ------------------------ | --------------------------------------------------------------------------- |
| `research_id`            | `R-{今日日付}-{既存最大+1}`                                                 |
| `title`                  | 文書最初の `#` ヘッダー                                                     |
| `category`               | 本文主題分析 (下記表参照)                                                   |
| `kpi_relevance`          | ディープリサーチ要求の `kpi_target` + 本文 KPI キーワード                   |
| `feature_domains`        | 本文から機能キーワードマッチング                                            |
| `competitors`            | 本文から会社名抽出                                                          |
| `scanner.priority`       | `category` + `kpi_relevance`で計算                                          |
| `scanner.keywords`       | 本文 TF-IDF 上位 5-10個                                                     |
| `quality.actionable`     | Action Items セクション存在/品質                                            |
| `quality.has_data`       | 数字/% 含有有無                                                             |
| `quality.has_actions`    | `- [ ]` または "Action" セクション存在                                      |
| `ai_confidence`          | ディープリサーチソース品質により 0.6-0.9                                    |
| **`target_apps`**        | 本文からアプリ名抽出 (デュオリンゴ、Duolingo、TTMIK 等キーワードマッチング) |
| **`target_user_levels`** | レベルキーワード抽出 (初級、中級、beginner、intermediate 等)                |
| **`pain_points`**        | ペインポイントカテゴリキーワードマッチング (コンテンツ、UX、価格等)         |
| **`learning_topics`**    | 韓国語学習主題抽出 (発音、文法、語彙、会話等)                               |
| **`actionability`**      | Action Items + 緊急性キーワードで自動判断                                   |

**category 自動分類規則**:

| 本文特徴                        | category       |
| ------------------------------- | -------------- |
| 競合社3個以上比較               | `competitor`   |
| 市場規模/トレンド               | `market`       |
| ユーザーインタビュー/アンケート | `user`         |
| 新技術/革新                     | `innovation`   |
| 価格/収益/コスト                | `monetization` |
| 法律/規制/GDPR                  | `legal`        |
| 技術実装詳細                    | `technical`    |
| 日本市場特化                    | `localization` |
| 既定値                          | `strategy`     |

**検索メタデータ自動抽出規則** (全てのリサーチ文書に適用):

> ℹ️ **適用範囲**: 全てのリサーチ文書に自動適用して AI/人間検索利便性向上

| フィールド             | 抽出方法                         | キーワード例示                                                                                               |
| ---------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **target_apps**        | アプリ名キーワードマッチング     | "デュオリンゴ"、"Duolingo"、"TTMIK"、"世宗学堂"、"Speak"、"ELSA"、"Memrise" 等                               |
| **target_user_levels** | レベルキーワード抽出             | "初級"、"入門"、"beginner"、"中級"、"intermediate"、"高級"、"advanced"                                       |
| **pain_points**        | ペインポイントカテゴリキーワード | "コンテンツ品質"、"UX/UI 不便"、"価格不満"、"学習設計"、"動機付け"、"技術エラー"                             |
| **learning_topics**    | 韓国語学習主題キーワード         | "発音"、"文法"、"語彙"、"会話"、"聞き取り"、"書き込み"、"敬語"、"タメ口"、"方言"                             |
| **actionability**      | Action Items + 緊急性            | Action Items 存在 + "即座"、"速い" → `immediate` <br> "検討必要" → `review_needed` <br> "長期" → `long_term` |

**抽出ロジック詳細 (Python 概念的)**:

```python
def extract_app_names(content):
    """本文からアプリ名抽出"""
    app_keywords = {
        "duolingo": ["デュオリンゴ", "duolingo", "デュオリンゴ"],
        "ttmik": ["TTMIK", "Talk To Me In Korean", "トークトゥミーインコリアン"],
        "sejong": ["世宗学堂", "sejong", "世宗韓国語"],
        "speak": ["Speak", "スピーク"],
        "elsa": ["ELSA", "エルサ"],
        # ... 其他アプリ
    }
    found = []
    for app, keywords in app_keywords.items():
        if any(kw.lower() in content.lower() for kw in keywords):
            found.append(app)
    return found

def extract_user_levels(content):
    """本文からユーザーレベル推定"""
    level_keywords = {
        "beginner": ["初級", "入門", "beginner", "初心者", "A1", "A2"],
        "elementary": ["初中級", "elementary", "B1"],
        "intermediate": ["中級", "intermediate", "B2"],
        "advanced": ["高級", "advanced", "C1", "C2", "ネイティブ級"]
    }
    found = []
    for level, keywords in level_keywords.items():
        if any(kw in content for kw in keywords):
            found.append(level)
    return found

def extract_pain_point_categories(content):
    """ペインポイントカテゴリ自動分類"""
    category_keywords = {
        "content": ["コンテンツ", "内容", "資料", "教材", "品質"],
        "learning_design": ["学習設計", "カリキュラム", "進度", "難易度"],
        "ux_ui": ["UX", "UI", "インターフェース", "デザイン", "画面", "操作"],
        "motivation": ["動機付け", "面白さ", "退屈", "興味", "習慣"],
        "technical": ["バグ", "エラー", "遅い", "クラッシュ", "エラー"],
        "pricing": ["価格", "高い", "サブスク", "無料", "有料"],
        "social": ["ソーシャル", "友達", "コミュニティ", "リーダーボード", "競争"]
    }
    found = []
    for category, keywords in category_keywords.items():
        if any(kw in content for kw in keywords):
            found.append(category)
    return found

def extract_learning_topics(content):
    """韓国語学習主題抽出"""
    topics = ["発音", "文法", "語彙", "会話", "読み", "書き込み", "聞き取り",
              "敬語", "タメ口", "方言", "スラング", "文化文脈",
              "ハングル字母", "パッチム", "発音変化"]
    return [topic for topic in topics if topic in content]

def determine_actionability(content):
    """実行可能性自動判断"""
    has_actions = "## Action Items" in content or "- [ ]" in content

    # 緊急性キーワードチェック
    immediate_keywords = ["即座", "緊急", "速く", "critical", "P0"]
    review_keywords = ["検討必要", "考慮", "分析必要", "P1"]
    long_term_keywords = ["長期", "ロードマップ", "未来", "P2"]

    if any(kw in content for kw in immediate_keywords) and has_actions:
        return ["immediate"]
    elif any(kw in content for kw in review_keywords):
        return ["review_needed"]
    elif any(kw in content for kw in long_term_keywords):
        return ["long_term"]
    else:
        return ["reference_only"]
```

**Frontmatter 生成例示**:

```yaml
---
research_id: R-20260206-001
title: 'Duolingo アプリストアレビューペインポイント分析 2026'
category: user
kpi_relevance:
  - monthly_churn
  - d7_retention
feature_domains:
  - content
  - retention
competitors:
  - duolingo
target_apps:
  - duolingo
target_user_levels:
  - intermediate
  - advanced
pain_points:
  - content
  - learning_design
  - motivation
learning_topics:
  - 発音
  - 文法
  - 会話
actionability:
  - immediate
  - review_needed
scanner:
  scannable: true
  priority: P0
  expected_insights:
    - feature_gap
    - user_behavior
  keywords:
    - duolingo
    - intermediate
    - 発音
    - コンテンツ
    - ペインポイント
quality:
  actionable: high
  source_reliability: A
  has_data: true
  has_actions: true
created_at: 2026-02-06
created_by: research-gap-analyzer
ai_confidence: 0.85
schema_version: 3
---
```

**必須本文セクション**:

1. Executive Summary (100単語以内)
2. 核心インサイト (3-5個、定量データ含む)
3. 競合社ベンチマーク
4. Action Items (優先順位 + 予想工数)
5. 出所 (信頼度表示: A/B/C級)

#### 6.2 状態ファイル更新

ディープリサーチ完了後 `assets/research-status.json`の該当作業を更新:

```json
{
  "phase": "completed",
  "doc_path": "docs/research/{ファイル名}.md",
  "completed_at": "{完了時間}"
}
```

**失敗時**:

```json
{
  "phase": "failed",
  "last_error": "{エラーメッセージ}",
  "attempt": 2
}
```

#### 6.3 Manifest 自動再生成 (Bash 実行)

> ⚠️ **自動化**: AI が文書保存後 **Bash ツールでスクリプトを直接実行**する。

**自動実行手順**:

```bash
# AI が自動的に実行 (人間介入不要)
Bash: python scripts/generate_research_manifest.py
```

**AI 行動指針**:

1. Step 6.1 で Frontmatter 含む文書を Write ツールで保存
2. **即座** に Bash ツールで `python scripts/generate_research_manifest.py` 実行
3. スクリプト出力で成功有無確認:
   - ✅ "Generation Complete" → 正常
   - ❌ エラー発生 → Frontmatter 検証後再試行

**検証 (選択的)**:

```bash
# Frontmatter スキーマ検証 (問題発生時のみ)
Bash: python scripts/validate_research_frontmatter.py
```

---

**Frontmatter フィールドレファレンス** (AI 自動生成用):

```yaml
---
research_id: R-{YYYYMMDD}-{NNN} # 必須、固有 ID (例: R-20260126-001)
title: '{文書タイトル}' # 必須 - 最初の # ヘッダーから抽出
category: strategy # 必須 - 9個 enum (自動分類)
kpi_relevance: # 関連 KPI (kpi_target + 本文分析)
  - ltv
  - monthly_churn
feature_domains: # 関連機能ドメイン (本文キーワード)
  - retention
  - monetization
competitors: # 言及された競合社 (本文から抽出)
  - duolingo
  - speak
scanner: # market-intelligence-scanner用
  scannable: true
  priority: P1 # P0|P1|P2|P3 (自動計算)
  expected_insights:
    - feature_gap
    - pricing
  keywords: # 本文核心キーワード 5-10個
    - churn
    - retention
quality: # 文書品質 (自動評価)
  actionable: high # high|medium|low
  source_reliability: B # A|B|C (ディープリサーチソース基準)
  has_data: true # 数字/% 含有有無
  has_actions: true # Action Items 存在有無
created_at: 2026-01-26 # YYYY-MM-DD (今日日付)
created_by: research-gap-analyzer
ai_confidence: 0.85 # 0.6~0.9 (ソース品質基準)
schema_version: 1
---
```

**category 有効値**: `competitor`, `market`, `user`, `innovation`, `strategy`, `technical`, `legal`, `monetization`, `localization`

**kpi_relevance 有効値**: `d7_retention`, `paid_conversion`, `monthly_churn`, `ltv`, `ai_max_upgrade`, `cac`

**scanner.priority 自動計算**:

- **P0**: 競合社分析 + P0 KPI(monthly_churn, ltv, paid_conversion) 関連
- **P1**: 競合社分析または P0 KPI 関連
- **P2**: P1 KPI(d7_retention, ai_max_upgrade) 関連
- **P3**: 其他

> スキーマ: [docs/\_schemas/research-frontmatter.schema.json](../../../docs/_schemas/research-frontmatter.schema.json)

### Step 7: README.md 自動インデックス更新

> ⚠️ **自動化**: AI が **Read → 挿入位置計算 → Edit** ツールで自動更新する。

**自動実行手順**:

```python
# AI 自動実行ロジック
1. Read("docs/research/README.md")  # 現在リスト読取
2. アルファベット順挿入位置計算
3. Edit()で新項目挿入
```

**AI 行動指針**:

1. `docs/research/README.md` 読取
2. `## List of Documents` セクション検索
3. **アルファベット順挿入位置** 自動計算:
   ```python
   # 新ファイル名: "churn-reactivation-campaign-2026.md"
   # 既存リストで "churn-p..." 次、"churn-r..." 前の位置検索
   for i, line in enumerate(lines):
       if line.startswith("- [x]"):
           existing_filename = extract_filename(line)
           if new_filename < existing_filename:
               insert_at = i
               break
   ```
4. Edit ツールで新項目挿入

**項目形式** (自動生成):

```markdown
- [x] [{Frontmatterの title}](./{ファイル名}.md)
```

**例示** (AI が自動実行):

```markdown
# 1. Read で現在状態確認

- [x] [Churn Prevention Strategy 2025](./churn-prevention-strategy-2025.md)
- [x] [Competitor Analysis 2026](./competitor-analysis-2026.md)

# 2. 挿入位置計算: "churn-r..." → "churn-p..." 次

# 3. Edit で挿入

- [x] [Churn Prevention Strategy 2025](./churn-prevention-strategy-2025.md)
- [x] [Churn Reactivation Campaign 2026](./churn-reactivation-campaign-2026.md) ← 自動挿入
- [x] [Competitor Analysis 2026](./competitor-analysis-2026.md)
```

**自動検証** (AI が Edit 後確認):

- ✅ ファイル名とリンクパス一致
- ✅ アルファベット順序維持
- ✅ チェックボックス形式(`- [x]`) 使用
- ✅ 文書タイトル = Frontmatterの title

---

## 使用例示

<example>
context: 全体リサーチギャップ分析要求
user: "リサーチギャップ分析して"
action:
1. docs/features/, docs/research/ ランタイムスキャン
2. KPI別ギャップ識別 (references/kpi-targets.md 参照)
3. 品質評価 (Action Items 有無確認)
4. P0 ギャップ 5個 + P1 ギャップ 5個報告
5. **P0 ギャップはユーザー確認なしに即座にディープリサーチ実行**
6. **[自動] Frontmatter 生成 + 文書保存 (Write)**
7. **[自動] Manifest 再生成 (Bash: python scripts/generate_research_manifest.py)**
8. **[自動] README.md インデックス更新 (Edit)**
</example>

<example>
context: 特定 KPI 集中分析
user: "Churn 防止戦略リサーチギャップ検索して"
action:
1. 月間離脱率 KPI 関連 Feature 確認 (008, 019)
2. 既存リサーチ品質評価 (churn-*, retention-*, reactivation-*)
3. 欠落領域識別 (再活性化キャンペーン設計、離脱信号感知)
4. 即座にディープリサーチ実行
5. **[自動] 本文分析 → Frontmatter メタデータ抽出**
6. **[自動] Frontmatter + 本文 → docs/research/ 保存**
7. **[自動] Bash で Manifest 再生成**
8. **[自動] README.md アルファベット順挿入**
</example>

<example>
context: PRD-Research 連結確認
user: "PRD-019が参照すべきリサーチは?"
action:
1. PRD-019 (リテンション戦略) 読取
2. 関連リサーチ 5個マッピング
3. 欠落連結点報告
</example>

---

## 注意事項

1. **ランタイムスキャン必須**: ハードコーディングされたリスト代わりに常に最新ファイル構造確認
2. **SSOT 遵守**: リサーチ状態は **必ず** `assets/research-status.json`でのみ管理
3. **スキーマ遵守**: 状態ファイル修正時 `references/research-status-schema.json` 参照必須
4. **タイムアウト規則**: `processing` 状態が 24時間経過時 `pending`に復帰
5. **実行可能性**: リソース制約を考慮して実行不可能なリサーチは価値なし
6. **Japan-First 整合性**: グローバルリサーチよりも日本市場データ優先
7. **品質 > 量**: 概念のみあるリサーチは "未完成"で処理
8. **README.md は参照用**: 状態管理 X、文書リストのみ記録
9. **Manifest 直接修正禁止**: Frontmatter 作成後 `python scripts/generate_research_manifest.py` 実行
10. **Frontmatter スキーマ遵守**: `docs/_schemas/research-frontmatter.schema.json` 参照、検証は `python scripts/validate_research_frontmatter.py`

---

## ファイル構造

```
.claude/skills/research-gap-analyzer/
├── SKILL.md                           # このファイル (ワークフロー定義)
├── assets/
│   └── research-status.json           # リサーチ作業状態 (SSOT)
├── references/
│   ├── kpi-targets.md                 # KPI 定義 + Feature マッピング
│   ├── critical-gaps.md               # クリティカルギャップリスト
│   └── research-status-schema.json    # 状態ファイル JSON スキーマ
└── scripts/
    └── analyze_gaps.py                # 自動化スクリプト (選択的)
```

---

## Changelog

| バージョン |    日付    | 変更内容                                                                                                                                                                                  |
| :--------: | :--------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|    5.0     | 2026-01-26 | **完全自動化**: Step 6-7 全面改編 - AI が本文分析 → Frontmatter 自動生成 → Bash で Manifest 再生成 → README.md 自動挿入。人間手動作業 0 に減少                                            |
|    4.0     | 2026-01-26 | **Frontmatter 基準 SSOT 転換**: Step 6.3 全面改編 - Manifest 直接修正 → Frontmatter 作成 + `generate_research_manifest.py` 実行。SSOT セクション更新、Data Drift 防止                     |
|    3.1     | 2026-01-25 | **Research Manifest 連動**: Step 6.3 追加 - ディープリサーチ完了後 `docs/_manifests/research-manifest.json`にメタデータ登録必須化。`market-intelligence-scanner`との cross-skill 連動支援 |
|    3.0     | 2026-01-25 | **状態トラッキングシステム導入**: `assets/research-status.json`が SSOT、JSON スキーマ基準一貫性保証、ワークフローに状態登録/更新段階追加                                                  |
|    2.1     | 2026-01-25 | **Step 7 追加**: リサーチ保存後 `docs/research/README.md` インデックス更新必須化                                                                                                          |
|    2.0     | 2026-01-19 | **全面改編**: SSOT 原則強化、クリティカルギャップリスト追加、品質チェックリスト導入                                                                                                       |
|    1.0     | 2026-01-15 | 初期バージョン                                                                                                                                                                            |
