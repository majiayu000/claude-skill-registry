---
name: research-pilot
description: |
  プロジェクト プロジェクトの Product Discovery スキル。
  feature-pilot 進入前に「この機能を作るべきか？」と「どのように作るべきか？」を
  業界標準フレームワーク（OST + Double Diamond + Shape Up）で検証する。

  フルスクラッチ開発、リサーチ、妥当性検証、技術調査等のリクエストでトリガーされる。

  <example>
  user: "ディクテーション機能をゼロベースでリサーチしたい"
  assistant: "research-pilotを使用してProduct Discoveryを開始します"
  </example>

  <example>
  user: "AIチューターに文法校正機能を追加したいが妥当性から確認して"
  assistant: "research-pilotを使用して技術的妥当性と市場需要を検証します"
  </example>
version: 1.0.0
updated: 2026-02-09
doc_contract:
  review_interval_days: 30
---

# Research Pilot v1.0 (Product Discovery オーケストレーター)

> **核心コンセプト**: "Build the Right Thing, Then Build the Thing Right"
> (正しいものを作るか先に確認し、その次に正しく作る)

feature-pilotが **「正しく作ること」**に集中するなら、
research-pilotは **「正しいものを作ること」**に集中する。

---

## 理論的基盤：ハイブリッドフレームワーク

### 採用した業界標準

| フレームワーク                      | 採用要素                                     | 適用方式                                   | 出典                                                                                               |
| ----------------------------------- | -------------------------------------------- | ------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| **OST** (Teresa Torres)             | Outcome→Opportunity→Solution→Assumption Test | 全体構造の骨格                             | [producttalk.org](https://www.producttalk.org/opportunity-solution-trees/)                         |
| **Double Diamond** (Design Council) | Diverge→Converge×2                           | Diamond 1(問題), Diamond 2(ソリューション) | [productboard.com](https://www.productboard.com/blog/double-diamond-framework-product-management/) |
| **Shape Up** (Basecamp)             | Appetite(時間予算)                           | Tier別リサーチ深度の自動調節               | [basecamp.com/shapeup](https://basecamp.com/shapeup)                                               |
| **Triple Track**                    | Strategy+Discovery+Delivery 並列             | 戦略トラックをビジネスKPIと連結            | [caroli.org](https://caroli.org/en/triple-track-development/)                                      |

### 採用しなかったものとその理由

| フレームワーク        | 却下理由                                         |
| --------------------- | ------------------------------------------------ |
| Design Sprint (5日間) | 複雑な機能には時間不足、チームワークショップ前提 |
| Lean Startup (MVP)    | リリース前アプリのため市場フィードバック収集不可 |
| 純粋Design Thinking   | Empathize段階に実際のユーザーアクセスが必要      |

### AI主導開発への適応（独自のイノベーション）

Teresa Torresは「AI要約は原文の20-40%の詳細を見落とす可能性がある」と警告している。
これを補完するために：

| 元の方法                   | AI適応                                         | 補完手段             |
| -------------------------- | ---------------------------------------------- | -------------------- |
| ユーザーインタビュー       | 競合アプリレビュー分析 (`app-review-analyzer`) | レビュー原文引用必須 |
| チームブレインストーミング | multi-llm-debate (多視点ディスカッション)      | 最低3つの代替案強制  |
| プロトタイプテスト         | PoC spike + 技術ベンチマーク                   | 定量的結果必須       |
| 手動OST作成                | CONTEXT.json `research` セクション             | 構造化JSONで追跡     |

---

## 🚨 EXECUTION PROTOCOL (MANDATORY)

> **CRITICAL**: このセクションはスキップできません。

### Pre-flight Checklist (スキル開始前必須出力)

```markdown
## ✈️ Pre-flight Checklist (research-pilot)

|   ID   | 項目                            | 状態 |
| :----: | ------------------------------- | :--: |
| RP-001 | リサーチ対象 (機能/テーマ) 確定 |  ⬜  |
| RP-002 | Tier 判定 (S/M/L/XL) 完了       |  ⬜  |
| RP-003 | Appetite (時間予算) 設定        |  ⬜  |
| RP-004 | ビジネス Outcome 明示           |  ⬜  |
| RP-005 | 既存リサーチキャッシュ確認      |  ⬜  |
| RP-006 | CLAUDE.md ルール確認            |  ⬜  |

**リサーチ対象**: [機能名またはテーマ]
**Tier**: [S | M | L | XL]
**Appetite**: [30分 | 2時間 | 4時間 | 8時間+]
**ビジネス Outcome**: [達成しようとする指標]

---

Pre-flight 完了: ✅ 全て通過 / ❌ ブロック項目あり
```

### Post-flight Checklist (スキル終了前必須出力)

```markdown
## 🛬 Post-flight Checklist (research-pilot)

|   ID    | 項目                                           | 状態 |
| :-----: | ---------------------------------------------- | :--: |
| RPO-001 | 全Phase完了または明示的中断                    |  ⬜  |
| RPO-002 | Gate 1 判定完了 (GO/NO-GO/DEFER)               |  ⬜  |
| RPO-003 | Gate 2 判定完了 (GO/NO-GO/DEFER) — Tier M 以上 |  ⬜  |
| RPO-004 | RESEARCH.md 生成完了                           |  ⬜  |
| RPO-005 | 最終決定 (BUILD/BUY/SKIP/DEFER) 記録           |  ⬜  |
| RPO-006 | feature-pilot ハンドオフ準備 (BUILD 時)        |  ⬜  |

**最終決定**: [BUILD | BUY | SKIP | DEFER]
**Gate 1**: [GO | NO-GO | DEFER] — 根拠要約
**Gate 2**: [GO | NO-GO | DEFER | N/A] — 根拠要約
**Evidence 収集**: [Deep Research N件, 競合 N社, OSS N件, PoC N件]

---

Post-flight 完了: ✅ 全て通過 / ❌ 未完了項目あり
```

### Model Routing Policy

| 作業                      | モデル | コスト |
| ------------------------- | :----: | :----: |
| Tier 判定, キャッシュ確認 | Haiku  |   $    |
| 機会探索 (並列読み込み)   | Haiku  |   $    |
| Deep Research 分析        | Sonnet |   $$   |
| 競合/OSS 分析             | Sonnet |   $$   |
| Multi-LLM 評価            | Sonnet |   $$   |
| 最終決定合成              |  Opus  |  $$$   |

---

## Appetite 基盤 Tier システム

> Shape Upの "fixed time, variable scope" 原則適用

### Tier 自動判定基準

```
Tier XL (8時間+) — 以下のいずれか1つ以上:
  □ 新規外部API連携 (STT, TTS, 決済等)
  □ AI/ML 基盤機能 (Gemini, On-device ML)
  □ リアルタイム処理 (WebSocket, Streaming)
  □ 市場に類似製品が少なくベンチマーク困難

Tier L (4時間) — 以下のいずれか1つ以上:
  □ DBスキーマ変更が必要
  □ 複数画面にまたがる機能
  □ Edge Function 新規開発
  □ オフライン同期が必要

Tier M (2時間) — 以下のいずれか1つ以上:
  □ 既存API活用の新規機能
  □ 単一画面 + DB変更
  □ 競合に類似機能が存在

Tier S (30分) — 上記に該当なし:
  □ 単純UI改善
  □ 既存機能拡張
  □ テキスト/翻訳関連
```

### Tier別 Phase 範囲

|               Phase                |  S  |  M  |  L  | XL  | 説明                         |
| :--------------------------------: | :-: | :-: | :-: | :-: | ---------------------------- |
| **Phase 1**: Opportunity Discovery |  —  | ✅  | ✅  | ✅  | 機会探索 (Diverge)           |
|  **Phase 2**: Problem Definition   | ✅  | ✅  | ✅  | ✅  | 問題定義 (Converge) + Gate 1 |
| **Phase 3**: Solution Exploration  |  —  |  —  | ✅  | ✅  | ソリューション探索 (Diverge) |
|  **Phase 4**: Assumption Testing   |  —  |  —  | ✅  | ✅  | 仮説検証 (Converge) + Gate 2 |
|  **Phase 5**: Decision & Handoff   | ✅  | ✅  | ✅  | ✅  | 最終決定 + ハンドオフ        |

**Tier S**: Phase 2 (迅速な検証) → Phase 5 (決定)
**Tier M**: Phase 1-2 (Diamond 1) → Phase 5 (決定)
**Tier L/XL**: Phase 1-5 (全体 Double Diamond)

---

## Phase 詳細プロトコル

### Phase 1: Opportunity Discovery (機会探索) — Diamond 1 Diverge

> **OST マッピング**: Outcome → Opportunity 発見
> **目的**: 「この領域にどんな機会があるか？」を広く探索

#### 活動一覧

```markdown
## 🔍 Phase 1: Opportunity Discovery

### 1.1 ユーザーの声収集

→ ツール: app-review-analyzer (競合アプリレビュー CSV)
→ なければ: deep-researchで「ユーザーの不満/要求」検索
→ 成果物: Pain Points リスト (最低5件)

### 1.2 競合ギャップ分析

→ ツール: competitive-tracker (既存ギャップデータ確認)
→ 成果物: 該当領域の競合カバレッジ比較表

### 1.3 市場トレンド調査

→ ツール: deep-research --provider google
→ クエリ例: "[機能領域] language learning app trends 2026"
→ 成果物: トレンド要約 + 成長方向

### 1.4 既存機能との関係

→ ツール: Explore エージェント (コードベース探索)
→ 確認: 既存機能とのシナジー/衝突有無
→ 成果物: 関連機能リスト + 影響分析
```

#### 実行方式: turbo-mode 並列

```
バッチ 1 (並列, 4個同時):
├── Task 1: [Haiku] app-review-analyzer または deep-research (ユーザーの声)
├── Task 2: [Haiku] competitive-tracker (競合ギャップ)
├── Task 3: [Haiku] deep-research (市場トレンド)
└── Task 4: [Haiku] Explore (既存コードベース)

→ 4個の結果統合 → Opportunity Map 生成
```

#### Phase 1 成果物: Opportunity Map

```markdown
## Opportunity Map

### Outcome (ビジネス目標)

[例: 復習完了率 30% → 60%]

### Opportunities (発見された機会)

|  ID   | 機会     | Evidence | Impact | Source |
| :---: | -------- | -------- | :----: | ------ |
| OPP-1 | [機会 1] | [根拠]   |  HIGH  | [出典] |
| OPP-2 | [機会 2] | [根拠]   | MEDIUM | [出典] |
| OPP-3 | [機会 3] | [根拠]   |  LOW   | [出典] |
```

---

### Phase 2: Problem Definition (問題定義) — Diamond 1 Converge

> **OST マッピング**: Target Opportunity 選定
> **目的**: 「どの機会に集中するか？」を決定

#### 活動一覧

```markdown
## 🎯 Phase 2: Problem Definition

### 2.1 機会評価 (Multi-LLM Reflection)

→ ツール: multi-llm-reflection エージェント
→ 評価基準: Reach, Impact, Confidence, Business Fit
→ 成果物: 機会別評価スコア

### 2.2 Provisional RICE 算出

→ ツール: priority-analyzer (Provisional モード)
→ 成果物: Provisional RICE スコア
→ 注意: 正式RICEはSPEC作成後に算出。ここでは方向性確認用

### 2.3 Target Opportunity 選定

→ 基準: RICE × Business Fit × Technical Feasibility (直感)
→ 成果物: Target Opportunity + 選定根拠

### 2.4 Problem Statement 作成

→ 形式: "[誰]は[状況]で[問題]を抱える。これにより[結果]。"
→ 成果物: 明確な Problem Statement
```

#### ════ Gate 1: "この問題は解く価値があるか？" ════

```markdown
## 🚦 Gate 1: Problem Validation

| 基準                 | 通過条件                                      | 結果 |
| -------------------- | --------------------------------------------- | :--: |
| **Evidence 存在**    | Pain Point 根拠 最低2件                       |  ⬜  |
| **ビジネス整合性**   | プロジェクト目標（高収益/低離脱/高LTV）と連結 |  ⬜  |
| **競合検証**         | 競合3社以上が提供 OR 市場トレンドで成長確認   |  ⬜  |
| **既存機能と非重複** | 既存機能では解決不可を確認                    |  ⬜  |
| **Provisional RICE** | ≥ 4.0 (10点満点)                              |  ⬜  |

### 判定

| 判定                  | 条件                                                 |
| --------------------- | ---------------------------------------------------- |
| **🟢 GO**             | 5/5 通過                                             |
| **🟡 CONDITIONAL GO** | 4/5 通過 (未通過項目がEvidence不足ならPhase 3で補強) |
| **🔴 NO-GO**          | 3個以下通過                                          |
| **⏸️ DEFER**          | 条件付き価値ありだが現在の優先順位ではない           |
```

**NO-GO 時の処理**:

- ユーザーにNO-GO理由 + 代替案を提示
- RESEARCH.mdに記録 (今後の再検討可能)
- Phase 5に直行してSKIP/DEFER決定

**GO 時の進行**:

- Tier S/M → Phase 5 (ソリューション探索省略、実装段階で決定)
- Tier L/XL → Phase 3 (ソリューション探索開始)

---

### Phase 3: Solution Exploration (ソリューション探索) — Diamond 2 Diverge

> **OST マッピング**: Solution Candidates 生成
> **目的**: 「どの方法で解決できるか？」を広く探索

#### 活動一覧

```markdown
## 💡 Phase 3: Solution Exploration

### 3.1 競合実装方式 Deep Dive

→ ツール: deep-research --provider google
→ クエリ: "[機能名] implementation [競合アプリ] UX flow features 2026"
→ 成果物: 競合別実装方式比較表

### 3.2 OSS 設計決定分析 (該当時)

→ ツール: oss-analyzer (類似機能のOSSがある場合)
→ 成果物: PDR (Problem→Decision→Recipe)
→ 注意: OSSがなければ省略

### 3.3 Multi-LLM Debate (代替案導出)

→ ツール: multi-llm-debate エージェント
→ 役割: Proponent(賛成), Opponent(反対), Moderator(仲裁)
→ ルール: 最低3つの代替案導出必須
→ 成果物: 代替案比較表 (メリット/デメリット, コスト, リスク)

### 3.4 技術スタック適合性確認

→ ツール: context7 MCP (Next.js/React/TypeScript 最新ドキュメント)
→ 確認: 必要なAPI/SDKが当社スタックで使用可能か
→ 成果物: 技術互換性レポート
```

#### 実行方式

```
バッチ 1 (並列):
├── Task 1: [Sonnet] deep-research (競合実装方式)
├── Task 2: [Sonnet] oss-analyzer (該当時) または deep-research (代替技術)
└── Task 3: [Haiku] context7 MCP (技術ドキュメント確認)

バッチ 2 (順次, バッチ 1 結果が必要):
└── Task 4: [Sonnet] multi-llm-debate (バッチ 1 結果に基づく代替案ディスカッション)
```

#### Phase 3 成果物: Solution Candidates

```markdown
## Solution Candidates

|  ID   | ソリューション | 出典                        | メリット | デメリット | コスト見積 | リスク |
| :---: | -------------- | --------------------------- | -------- | ---------- | :--------: | :----: |
| SOL-1 | [方案 1]       | [競合/OSS/ディスカッション] | [...]    | [...]      |    LOW     |  LOW   |
| SOL-2 | [方案 2]       | [...]                       | [...]    | [...]      |   MEDIUM   | MEDIUM |
| SOL-3 | [方案 3]       | [...]                       | [...]    | [...]      |    HIGH    |  HIGH  |

### 推奨ソリューション: SOL-X

**選定根拠**: [なぜこのソリューションか？]
**却下根拠**: [他のソリューションをなぜ却下したか？]
```

---

### Phase 4: Assumption Testing (仮説検証) — Diamond 2 Converge

> **OST マッピング**: Assumption Test 実行
> **目的**: 「選択したソリューションが実際に動作するか？」を検証

#### 仮説タイプ分類 (Teresa Torres 基盤)

| タイプ                         | 質問                       | 検証方法                            |
| ------------------------------ | -------------------------- | ----------------------------------- |
| **Desirability** (価値)        | ユーザーが望むか？         | 競合レビュー分析, 市場データ        |
| **Feasibility** (実現)         | 技術的に可能か？           | PoC spike, API テスト, ベンチマーク |
| **Viability** (ビジネス)       | コスト対比で価値があるか？ | コスト見積, ROI 分析                |
| **Usability** (ユーザビリティ) | 使いやすいか？             | 競合UXパターン分析                  |

#### 活動一覧

```markdown
## 🧪 Phase 4: Assumption Testing

### 4.1 仮説リスト作成

→ 選択したソリューションから「真でなければならないこと」を抽出
→ リスク順にソート (HIGH → LOW)
→ 成果物: Assumption Register

### 4.2 Desirability 検証

→ ツール: app-review-analyzer または deep-research
→ 質問: 「ユーザーがこの機能を望むという証拠があるか？」
→ 判定: VALIDATED / INVALIDATED / INCONCLUSIVE

### 4.3 Feasibility 検証 (核心)

→ ツール: context7 MCP + PoC spike (条件付き)
→ PoC 判断基準:
□ 初めて使用する外部API → PoC 必須
□ リアルタイム処理 → PoC 必須
□ On-device 処理 → PoC 必須
□ 複雑なアルゴリズム → PoC 必須
□ その他 → APIドキュメント確認で十分

→ PoC 実行時:

1. 最小限のコードで核心技術を検証
2. パフォーマンス測定 (応答時間, 精度等)
3. 結果を定量的に記録
4. PoCコードは `poc/` ディレクトリに一時保存 (実装時に削除)

→ 成果物: Feasibility Report (定量的結果必須)

### 4.4 Viability 検証

→ 計算項目:

- Edge Function 呼び出しコスト (Gemini API トークンコスト)
- DB ストレージ増加量
- 開発時間 (Tier 基盤推定)
- メンテナンス複雑度増加
  → 成果物: Cost-Benefit Analysis

### 4.5 Usability 検証

→ ツール: deep-research (競合UXパターン)
→ 確認: 業界標準UXパターンの存在有無
→ 成果物: UX Pattern Reference
```

#### PoC Spike プロトコル (Tier XL 必須, L 条件付き)

```markdown
## PoC Spike 実行ルール

### 範囲制限

- 検証対象: 1つの核心仮説のみ
- コード量: 最大200行
- 時間: 最大2時間
- 場所: poc/<feature-name>/ (一時的、実装時に削除)

### 必須測定項目

| タイプ         | 測定項目          | 例                                  |
| -------------- | ----------------- | ----------------------------------- |
| パフォーマンス | 応答時間          | "Edge Function 平均 23ms, P99 89ms" |
| 精度           | 機能精度          | "STT 韓国語認識率 87%"              |
| コスト         | API呼び出しコスト | "Gemini 1回呼び出し $0.003"         |
| 互換性         | スタック互換      | "Next.js 16 + Vercel 互換確認"   |

### PoC 結果記録形式

| 仮説    | テスト       | 結果       | 判定  |
| ------- | ------------ | ---------- | :---: |
| [ASM-1] | [テスト内容] | [定量結果] | ✅/❌ |
```

#### ════ Gate 2: "技術的に実現可能でコスト対比で価値があるか？" ════

```markdown
## 🚦 Gate 2: Solution Validation

| 基準            | 通過条件                                     | 結果 |
| --------------- | -------------------------------------------- | :--: |
| **Feasibility** | 核心技術仮説 全て VALIDATED                  |  ⬜  |
| **Cost**        | 月間運用コストが予算内 (またはユーザー確認)  |  ⬜  |
| **Complexity**  | 実装複雑度がチーム能力(AIエージェント)範囲内 |  ⬜  |
| **代替案存在**  | INVALIDATED 仮説時に代替ソリューション存在   |  ⬜  |
| **UXパターン**  | 参考にすべき業界UXパターン存在               |  ⬜  |

### 判定

| 判定         | 条件                                            |
| ------------ | ----------------------------------------------- |
| **🟢 GO**    | Feasibility VALIDATED + Cost OK + 代替案不要    |
| **🟡 PIVOT** | 一部仮説 INVALIDATED → 代替ソリューションに転換 |
| **🔴 NO-GO** | 核心仮説 INVALIDATED + 代替案なし               |
| **⏸️ DEFER** | 技術は可能だが現在のコスト/複雑度が過大         |
```

---

### Phase 5: Decision & Handoff (最終決定 + ハンドオフ)

> **目的**: リサーチ結果を総合して最終決定を下し、feature-pilotに構造化された入力を伝達

#### 最終決定マトリクス

```
              Gate 1 GO    Gate 1 NO-GO
Gate 2 GO  │  BUILD       │  N/A (Gate 1が先)
Gate 2 PIVOT│  BUILD(代替) │  N/A
Gate 2 NO-GO│  SKIP/DEFER │  SKIP
Gate 2 N/A │  BUILD(Tier S/M) │  SKIP/DEFER
```

| 決定      | 意味                   | 次のアクション                                       |
| --------- | ---------------------- | ---------------------------------------------------- |
| **BUILD** | 自社開発実施           | feature-pilot 進入 (feature-architect → spec → impl) |
| **BUY**   | 外部ソリューション統合 | ライブラリ/SDK 選定 → 統合実装                       |
| **SKIP**  | 現時点で不要/不可      | RESEARCH.md 記録、今後再検討                         |
| **DEFER** | N ヶ月後再検討         | RESEARCH.mdに再検討時期を記録                        |

#### 成果物 1: RESEARCH.md

```markdown
# Research Summary: [機能名]

> 生成日: YYYY-MM-DD
> Tier: [S|M|L|XL]
> 最終決定: [BUILD|BUY|SKIP|DEFER]

## 1. Outcome (ビジネス目標)

[達成しようとするKPI/指標]

## 2. Problem Statement

"[誰]は[状況]で[問題]を抱える。これにより[結果]。"

## 3. Opportunity Map

|  ID   | 機会  | Evidence | Impact |
| :---: | ----- | -------- | :----: |
| OPP-1 | [...] | [...]    |  HIGH  |

**Target Opportunity**: OPP-X — [選定根拠]

## 4. Solution Candidates (Tier L/XLのみ)

|  ID   | ソリューション | メリット | デメリット | 選択 |
| :---: | -------------- | -------- | ---------- | :--: |
| SOL-1 | [...]          | [...]    | [...]      |  ✅  |
| SOL-2 | [...]          | [...]    | [...]      |  ❌  |

**選択根拠**: [...]
**却下根拠**: [...]

## 5. Assumption Test Results (Tier L/XLのみ)

|  ID   | 仮説  | タイプ      | テスト | 結果  | 判定 |
| :---: | ----- | ----------- | ------ | ----- | :--: |
| ASM-1 | [...] | Feasibility | [...]  | [...] |  ✅  |

## 6. Gate 判定

|  Gate  | 判定 | 根拠要約                 |
| :----: | :--: | ------------------------ |
| Gate 1 |  GO  | [Evidence 3件, RICE 7.2] |
| Gate 2 |  GO  | [PoC 通過, 月 $0 追加]   |

## 7. 最終決定

**決定**: BUILD
**根拠**: [総合判断]

## 8. feature-pilot ハンドオフデータ

- **BRIEF §0 原文**: [ユーザーシナリオ]
- **Hard Constraints**: [技術的制約, R4で発見]
- **参照リサーチ**: [docs/research/*.md リンク]
- **OSS Recipe**: [docs/oss/*/adoption.md リンク] (該当時)
- **PoC 結果**: [poc/ 結果要約] (該当時)
- **UX 参照**: [競合UXパターンリンク]

## 9. リサーチメタデータ

- **投資時間**: [実際所要時間]
- **Appetite**: [設定した時間予算]
- **Evidence 収集**: Deep Research N件, 競合 N社, OSS N件, PoC N件
- **再検討時期**: [DEFER 時 YYYY-MM-DD]
```

#### 成果物 2: CONTEXT.json `research` セクション

BUILD 決定時、feature-architectが CONTEXT.json を生成する際に `research` セクションを自動的に事前充填します。

```json
{
  "research": {
    "tier": "L",
    "appetite_hours": 4,
    "actual_hours": 3.5,
    "started_at": "2026-02-09T10:00:00+09:00",
    "completed_at": "2026-02-09T13:30:00+09:00",
    "research_md_path": "docs/features/<id>/RESEARCH.md",

    "outcome": "ユーザー復習完了率 30% → 60%",
    "problem_statement": "学習者は復習タイミングを逃し長期記憶への転換に失敗する。",

    "opportunity_map": {
      "total_opportunities": 3,
      "target_opportunity": {
        "id": "OPP-1",
        "description": "ユーザーが復習タイミングを逃す",
        "evidence_count": 3,
        "impact": "HIGH"
      }
    },

    "solution": {
      "selected": {
        "id": "SOL-1",
        "name": "SRS 基盤自動復習スケジューリング",
        "source": "oss-analyzer: Anki SM-2",
        "rationale": "業界標準 + 実装コスト低"
      },
      "rejected": [
        {
          "id": "SOL-2",
          "name": "AI 基盤パーソナライズ復習",
          "rejection_rationale": "MVP段階ではオーバーエンジニアリング"
        }
      ]
    },

    "assumptions": [
      {
        "id": "ASM-1",
        "statement": "SM-2が韓国語学習に効果的",
        "type": "desirability",
        "risk": "MEDIUM",
        "result": "VALIDATED",
        "evidence": "研究 3件確認"
      }
    ],

    "gates": {
      "gate_1": { "verdict": "GO", "evidence_summary": "..." },
      "gate_2": { "verdict": "GO", "evidence_summary": "..." }
    },

    "decision": "BUILD",
    "handoff": {
      "hard_constraints": ["SM-2 間隔: 1,3,7,14,30日", "オフライン計算必須"],
      "research_refs": ["docs/research/srs-algorithm-comparison.md"],
      "oss_recipes": ["docs/oss/anki/v4/adoption.md"],
      "ux_references": ["Anki 復習画面", "Quizlet 学習モード"],
      "poc_summary": "Edge Function SM-2 計算 平均 23ms"
    }
  }
}
```

---

## feature-pilot 統合プロトコル

### NEW_FEATURE パイプライン (research-pilot 統合後)

```
Phase -1: ★ research-pilot ★ (新規追加)
        ┌────────────────────────────────────┐
        │ Skill ツール使用:                    │
        │ - skill: "research-pilot"          │
        │ - args: "<機能説明>"              │
        │                                    │
        │ ★ 条件付き実行:                      │
        │   IF ユーザー要求に「リサーチ」,        │
        │      「妥当性」,「調査」,「ゼロベース」, │
        │      「フルスクラッチ」キーワード含む    │
        │   OR ユーザーが明示的に要求            │
        │   → research-pilot 実行            │
        │                                    │
        │   ELSE:                            │
        │   → 既存 feature-pilot フロー維持    │
        │                                    │
        │ ★ BUILD 決定時:                      │
        │   → RESEARCH.md + research セクション │
        │   → Phase 0 (既存 feature-pilot)    │
        │                                    │
        │ ★ SKIP/DEFER 決定時:                │
        │   → RESEARCH.md 記録後終了           │
        └────────────────────────────────────┘
        ↓ BUILD → feature-pilot Phase 0に進入

Phase 0: (既存) リクエスト受付・分類
        ↓

Phase 0.5: turbo-mode コンテキスト収集
        ↓ (research-pilotの結果もコンテキストに含む)

Step 1: feature-architect (CONTEXT.json 生成)
        ↓ research セクション自動事前充填

Step 2: feature-spec-generator
        ↓ ...以下既存パイプラインと同一
```

### 自動実行 vs 明示的実行

| 条件                                                       | 動作                                     |
| ---------------------------------------------------------- | ---------------------------------------- |
| ユーザーが「リサーチ」「妥当性」「調査」等のキーワード使用 | **自動実行**                             |
| ユーザーが `/research-pilot` を直接呼び出し                | **明示的実行**                           |
| feature-pilotが NEW_FEATURE を Tier XL と判定              | **ユーザーに research-pilot 実行を提案** |
| 既存 RESEARCH.md があり 30日以内                           | **キャッシュ使用** (再実行省略)          |
| 既存 RESEARCH.md があり 30日超過                           | **再実行を提案**                         |

---

## 例外処理

| 状況                   | 処理                                                |
| ---------------------- | --------------------------------------------------- |
| **Deep Research 失敗** | WebSearch フォールバックで代替、結果品質 Warning    |
| **競合データなし**     | competitive-tracker なしに deep-research で直接調査 |
| **PoC 失敗**           | 代替ソリューションに PIVOT、Gate 2 再評価           |
| **Appetite 超過**      | 現時点までの結果で Gate 判定、未完了部分を明示      |
| **ユーザー中断**       | 現在の Phase まで RESEARCH.md 保存、再開可能        |
| **Gate 1 NO-GO**       | Phase 5 に直行、SKIP/DEFER 決定                     |
| **Gate 2 NO-GO**       | 代替ソリューション検討後最終決定                    |

---

## AI 行動指針

### DO (すべきこと)

- ✅ Tier を先に判定し Appetite に合わせて Phase 範囲を決定
- ✅ 全ての判断に Evidence(根拠) 添付 — 根拠なき主張禁止
- ✅ 最低3つの代替案検討後1つ選択 (Phase 3)
- ✅ PoC 結果は定量的データで記録
- ✅ Gate 判定は明示的基準で (直感禁止)
- ✅ RESEARCH.md を常に生成 (SKIP/DEFER 決定でも)
- ✅ feature-pilot ハンドオフデータを構造化して伝達
- ✅ Teresa Torresの "crummy first draft" 原則遵守 — 完璧より速い初稿

### DON'T (してはいけないこと)

- ❌ 根拠なく「この機能は必要です」と結論
- ❌ 代替案検討なく単一ソリューションに直行
- ❌ PoC なしに「技術的に可能です」と仮定 (Tier XL)
- ❌ Appetite を超過して無限リサーチ
- ❌ Gate 基準を任意に緩和
- ❌ RESEARCH.md 生成なしに feature-pilot へ進行
- ❌ 既存 RESEARCH.md が有効なのに再実行 (キャッシュ浪費)

---

## 使用例

```bash
# フルスクラッチリサーチ (自動 Tier 判定)
/research-pilot "ディクテーション機能をゼロベースで調査したい"

# Tier 明示
/research-pilot --tier XL "AI 基盤文法校正機能"

# 特定 Phase から (以前の結果がある場合)
/research-pilot --phase 3 "033-vocabulary-notebook"

# PoC 強制実行
/research-pilot --poc "STT 基盤発音評価"

# Gate 1 スキップ (既に検証済みの問題)
/research-pilot --skip-gate1 "006-srs-review-system 再設計"
```

---

## 変更履歴

| 日付       | バージョン | 変更内容                                                              |
| ---------- | ---------- | --------------------------------------------------------------------- |
| 2026-02-09 | v1.0.0     | 初期作成 — OST + Double Diamond + Shape Up ハイブリッドフレームワーク |
