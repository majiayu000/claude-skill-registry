---
name: turbo-mode
description: |
  プロジェクト プロジェクトの **実際の並列実行エンジン**。
  ultrawork + ecomode + Crystal の TaskQueue コンセプトを統合。

  **v3.0 核心変化**: Enforced Skill Pattern 適用
  - Pre-flight/Post-flight Checklist 強制
  - Model Routing Policy 強制
  - Evidence Caching 自動化
  - 違反時即座に中断

  「ターボ」、「turbo」、「速く」、「並列で」、「同時に」等のリクエストでトリガーされる。

  <example>
  user: "ターボモードでコンテキスト収集して"
  assistant: "turbo-modeを使用して並列でコンテキストを収集します"
  </example>

  <example>
  user: "速く分析して"
  assistant: "turbo-modeを有効化して並列分析を開始します"
  </example>
doc_contract:
  review_interval_days: 30
---

# Turbo Mode v3.0 (Enforced Parallel Execution Engine)

> **核心コンセプト**: 「分析 → バッチ → 実行 → 検証」 (Analyze → Batch → Execute → Verify)

v2.0 が「ガイドライン文書」だったとすれば、v3.0 は **強制実行プロトコル**が内蔵された実際のエンジンです。

## 核心変化 (v2.0 → v3.0)

| 領域              | v2.0 (文書) | v3.0 (強制)                |
| ----------------- | ----------- | -------------------------- |
| Pre-flight Check  | なし        | **MANDATORY**              |
| Model Routing     | 推奨        | **MANDATORY** (違反時中断) |
| Evidence Cache    | 言及のみ    | **自動キャッシング**       |
| Post-flight Check | なし        | **MANDATORY**              |
| 違反処理          | なし        | **即座に中断 + 再開始**    |

---

## 🚨 EXECUTION PROTOCOL (MANDATORY)

> **CRITICAL**: このセクションは **省略不可**です。AI は turbo-mode 実行時に必ず下記チェックリストを **出力して確認**すべきです。

### Pre-flight Checklist (実行前必須)

turbo-mode 実行前必ず下記チェックリストを **出力**して各項目を確認:

```markdown
## ✈️ Turbo Mode Pre-flight Checklist

|   #    | 項目                            | 状態 | 備考         |
| :----: | ------------------------------- | :--: | ------------ |
| PF-001 | 作業リスト生成完了              |  ⬜  |              |
| PF-002 | 各作業にタイプ(Read/Write) 指定 |  ⬜  |              |
| PF-003 | 依存性グラフ分析完了            |  ⬜  |              |
| PF-004 | バッチ構成出力完了              |  ⬜  |              |
| PF-005 | 各 Task に model パラメータ明示 |  ⬜  |              |
| PF-006 | 作業 ID 確定                    |  ⬜  | 命名規則遵守 |

→ 全ての項目 ✅ 確認後実行進行
→ 一つでも ❌ 時即座に中断 + 事由報告
```

### Model Routing Policy (モデルポリシー) - MANDATORY

> **CRITICAL**: Task ツール呼び出し時必ず `model` パラメータ明示。欠落時該当 Task 無効。

| 作業タイプ                 |   モデル   | 根拠                           |
| -------------------------- | :--------: | ------------------------------ |
| ファイル検索、パターン検索 | **haiku**  | Glob/Grep ラッピング、推論不要 |
| package.json 読取          | **haiku**  | 単純パース                     |
| Hook/Service 検索          | **haiku**  | パターンマッチング             |
| DB スキーマ確認            | **haiku**  | メタデータ照会                 |
| Model/Schema 生成          | **sonnet** | テンプレート基準               |
| Custom Hook 実装           | **sonnet** | パターン理解必要               |
| Component 実装             | **sonnet** | React パターン                 |
| テスト作成                 | **sonnet** | テストパターン理解             |
| アーキテクチャ決定         |  **opus**  | トレードオフ分析               |
| バグ根本原因               |  **opus**  | 深い推論                       |
| セキュリティ検討           |  **opus**  | 脆弱性分析                     |

**フォールバック戦略**:

- haiku 失敗 → sonnet 自動昇格
- sonnet 失敗 → opus 自動昇格

**Task 呼び出し例示**:

```
✅ 正しい呼び出し:
Task(
  description: "ViewModel パターン検索",
  prompt: "lib/features/で ViewModel パターン検索",
  subagent_type: "Explore",
  model: "haiku"  ← MANDATORY
)

❌ 誤った呼び出し (model 欠落):
Task(
  description: "ViewModel パターン検索",
  prompt: "...",
  subagent_type: "Explore"
  // model 欠落 → この Task は無効、再実行必要
)
```

### Evidence Policy (キャッシュポリシー)

| 検証タイプ       | 有効時間 | 無効化条件           | キャッシュキー                   |
| ---------------- | :------: | -------------------- | -------------------------------- |
| npm run lint     |   30分   | src/\*_/_.ts 変更    | `analyze_${timestamp}`           |
| npm test         |   30分   | test/\*_/_.ts 変更   | `test_${timestamp}`              |
| パターン検索結果 |   60分   | 検索対象ファイル変更 | `search_${pattern}_${timestamp}` |

**動作**:

1. 検証/検索要求時 `CONTEXT.json > evidence_cache` 確認
2. 有効なキャッシュ存在 → スキップ + "**[CACHE HIT]** キャッシュ使用" メッセージ出力
3. キャッシュなし/満了 → 実行 + 結果キャッシング

### Post-flight Checklist (実行後必須)

turbo-mode 完了前必ず下記チェックリストを **出力**して検証:

```markdown
## 🛬 Turbo Mode Post-flight Checklist

|    #    | 項目                               | 状態 | 備考 |
| :-----: | ---------------------------------- | :--: | ---- |
| POF-001 | 全てのバッチ実行完了               |  ⬜  |      |
| POF-002 | 各 Task model パラメータ含有確認   |  ⬜  |      |
| POF-003 | 衝突/失敗なし確認                  |  ⬜  |      |
| POF-004 | 結果マージ完了                     |  ⬜  |      |
| POF-005 | Evidence キャッシング完了 (該当時) |  ⬜  |      |

→ 全ての項目 ✅ 時完了報告
→ 一つでも ❌ 時修正後再検証
```

### Violation Protocol (違反時処理)

| 違反タイプ              |    深刻度    | 処理                          |
| ----------------------- | :----------: | ----------------------------- |
| Pre-flight 未出力       | **CRITICAL** | 即座に中断、最初から再開始    |
| Model パラメータ欠落    |   **HIGH**   | 該当 Task 再実行 (model 追加) |
| 依存性無視並列実行      |   **HIGH**   | 結果廃棄、再実行              |
| Post-flight 未検証      |   **HIGH**   | 完了報告前検証実行            |
| Evidence キャッシュ無視 |  **MEDIUM**  | 警告後進行                    |

---

## 核心原則

1. **分析優先**: 作業リストと依存性分析なしに並列実行禁止
2. **モデル最適化**: 簡単な作業に Opus 使用禁止
3. **衝突防止**: 同じファイルを複数 Task で同時修正禁止
4. **検証キャッシング**: 同一検証繰り返し防止

---

## 🚀 実行プロトコル

### Phase 1: 作業リスト収集

turbo-mode 活性化時、まず実行すべき **全ての作業を明示的に羅列**します。

```markdown
## 📋 作業リスト (Turbo Mode)

| ID  | 作業                            | タイプ | 予想ティア |
| --- | ------------------------------- | ------ | ---------- |
| T1  | src/features/で類似パターン検索 | Read   | Haiku      |
| T2  | DB スキーマで関連テーブル確認   | Read   | Haiku      |
| T3  | 既存テストパターン調査          | Read   | Haiku      |
| T4  | CONTEXT.json 生成               | Write  | Sonnet     |
| T5  | SPEC.md 生成                    | Write  | Sonnet     |
| T6  | Model/Type 実装                 | Write  | Sonnet     |
| T7  | API Route 実装                  | Write  | Sonnet     |
| T8  | Custom Hook 実装                | Write  | Sonnet     |
| T9  | Component 実装                  | Write  | Sonnet     |
| T10 | テスト作成                      | Write  | Sonnet     |
```

---

### Phase 2: 依存性グラフ分析

**自動分析規則**:

| 規則                    | 説明                     | 例示                                 |
| ----------------------- | ------------------------ | ------------------------------------ |
| **Read → 独立**         | 読取専用作業はすべて独立 | T1, T2, T3 並列可能                  |
| **Write → 順序確認**    | 書き込みは入力依存性確認 | T5 は T4 必要 (CONTEXT → SPEC)       |
| **同じファイル → 順次** | 同一ファイル修正は順次   | package.json 修正は直列化            |
| **レイヤー依存性**      | Types → API → Hooks → UI | Types → API Route → Hook → Component |

**依存性グラフ出力**:

```
## 🔗 依存性グラフ

T1 ──┐
T2 ──┼──→ T4 ──→ T5 ──→ T6 ──┐
T3 ──┘                       │
                             ├──→ T8 ──→ T9 ──→ T10
                     T7 ─────┘

**依存性説明**:
- T1, T2, T3: 独立 (並列可能)
- T4: T1,T2,T3 完了後実行
- T5: T4 完了後実行
- T6, T7: T5 完了後並列可能
- T8: T6 必要 (Model import)
- T9: T8 必要 (ViewModel import)
- T10: T9 必要 (Component テスト)
```

---

### Phase 3: バッチ自動構成

依存性グラフを基に **トポロジー整列**してバッチを構成します。

**バッチ構成アルゴリズム**:

1. 依存性がない作業 → バッチ 1
2. バッチ 1 完了後依存性解消された作業 → バッチ 2
3. 繰り返し

```markdown
## 📦 バッチ構成

### バッチ 1 (並列 - 読取専用)

| ID  | 作業               |  モデル   | エージェント |
| --- | ------------------ | :-------: | ------------ |
| T1  | 類似パターン検索   | **haiku** | Explore      |
| T2  | DB スキーマ確認    | **haiku** | Explore      |
| T3  | テストパターン調査 | **haiku** | Explore      |

### バッチ 2 (順次 - 文書生成)

| ID  | 作業              |   モデル   | エージェント    |
| --- | ----------------- | :--------: | --------------- |
| T4  | CONTEXT.json 生成 | **sonnet** | general-purpose |
| T5  | SPEC.md 生成      | **sonnet** | general-purpose |

### バッチ 3 (並列 - 独立実装)

| ID  | 作業            |   モデル   | エージェント    |
| --- | --------------- | :--------: | --------------- |
| T6  | Model 実装      | **sonnet** | general-purpose |
| T7  | Repository 実装 | **sonnet** | general-purpose |

### バッチ 4 (順次 - レイヤー統合)

| ID  | 作業           |   モデル   | エージェント    |
| --- | -------------- | :--------: | --------------- |
| T8  | ViewModel 実装 | **sonnet** | general-purpose |
| T9  | Component 実装    | **sonnet** | general-purpose |
| T10 | テスト作成     | **sonnet** | general-purpose |
```

---

### Phase 4: 実際の並列実行 ⭐

**核心**: Claude Code の Task Tool は **単一応答で複数個呼び出し可能**です。

#### 並列バッチ実行方法

**CRITICAL**: 並列バッチ内全ての Task を **一つの応答**で同時に呼び出します。

```
## ▶️ バッチ 1 実行 (並列)

次の 3個 Task を **単一応答で同時呼び出し**:

Task 1:
  - description: "類似パターン検索"
  - prompt: "src/features/で Hook パターン検索"
  - subagent_type: "Explore"
  - model: "haiku"  ← MANDATORY

Task 2:
  - description: "DB スキーマ確認"
  - prompt: "Supabase スキーマで関連テーブル確認"
  - subagent_type: "Explore"
  - model: "haiku"  ← MANDATORY

Task 3:
  - description: "テストパターン調査"
  - prompt: "test/ フォルダで類似テストパターン調査"
  - subagent_type: "Explore"
  - model: "haiku"  ← MANDATORY

→ 全ての結果同時返却 (待機時間 1/3 に短縮)
```

---

### Phase 5: 結果収集および衝突検出

**結果収集フォーマット**:

```markdown
## 📊 バッチ 1 結果

| ID  | 状態    | Model | 結果要約                     | 生成/修正ファイル |
| --- | ------- | :---: | ---------------------------- | ----------------- |
| T1  | ✅ 成功 | haiku | 3個 ViewModel パターン発見   | -                 |
| T2  | ✅ 成功 | haiku | users, progress テーブル関連 | -                 |
| T3  | ✅ 成功 | haiku | mocktail 基盤テストパターン  | -                 |

**Model 使用確認**: ✅ 全ての Task に model 明示
**衝突検出**: なし (すべて Read 作業)
```

**衝突検出規則**:

| 衝突タイプ   | 検出条件                            | 解決方法                   |
| ------------ | ----------------------------------- | -------------------------- |
| ファイル衝突 | 2個以上 Task が同じファイル修正試行 | 最初の結果維持、残り再実行 |
| Import 衝突  | まだないファイル import 試行        | 依存性順序再検討           |
| 状態不一致   | CONTEXT.json 同時修正               | Lock 獲得後順次処理        |

---

## ⚠️ 制約事項

### 並列不可作業

| 作業タイプ        | 理由             | 処理方法              |
| ----------------- | ---------------- | --------------------- |
| CONTEXT.json 修正 | 単一状態ファイル | Lock 獲得後順次       |
| package.json 修正 | 依存性衝突危険   | 順次処理              |
| 同じファイル修正  | 内容衝突         | 1ファイル = 1ワーカー |
| レイヤー依存性    | import 順序      | Hook → Component 順次 |

### バックグラウンド実行

長い作業はバックグラウンドに分離:

```
# バックグラウンド (run_in_background: true)
- npm run build
- npm test
- npm run lint

# 同期 (既定)
- npm run lint -- --quiet
- npm install
```

---

## 📈 予想効果

| 指標             | 既存 (順次) | Turbo Mode v3.0  |     改善     |
| ---------------- | :---------: | :--------------: | :----------: |
| コンテキスト収集 |    100%     |      30-40%      | **60-70% ↓** |
| 実装段階         |    100%     |      50-60%      | **40-50% ↓** |
| トークンコスト   |    100%     |      40-60%      | **40-60% ↓** |
| 繰り返し検証     |    100%     | 20% (キャッシュ) |  **80% ↓**   |

**根拠**:

- 3個 Haiku 並列 → 1/3 待機時間
- 2個 Sonnet 並列 → 1/2 待機時間
- Haiku コスト = Sonnet の ~5%, Opus の ~3%
- Evidence Cache → 同一検証スキップ

---

## 📊 出力形式

### 成功時

```markdown
# Turbo Mode 実行完了

> **実行時間**: 2026-02-01T10:30:00+09:00
> **モデル使用**: Haiku 3回、Sonnet 7回、Opus 0回
> **キャッシュ活用率**: 40% (4/10 キャッシュヒット)

## Summary

| 項目     | 結果 |
| -------- | :--: |
| 総作業   | 10個 |
| バッチ数 | 4個  |
| 並列効率 | 60%  |
| 成功     | 10個 |
| 失敗     | 0個  |

## バッチ別結果

| バッチ | 作業数 | モデル | 所要時間 | 状態 |
| :----: | :----: | :----: | :------: | :--: |
|   B1   |   3    | haiku  |   45秒   |  ✅  |
|   B2   |   2    | sonnet |   2分    |  ✅  |
|   B3   |   2    | sonnet |   2分    |  ✅  |
|   B4   |   3    | sonnet |   3分    |  ✅  |

**総所要時間**: 7分 45秒
**順次実行予想時間**: 20分
**節減**: **60%** ⚡

## Evidence キャッシング

| 検証               | キャッシュキー                | 満了時間 |
| ------------------ | ----------------------------- | -------- |
| ViewModel パターン | `search_viewmodel_1706755800` | +60分    |
| DB スキーマ        | `search_schema_1706755800`    | +60分    |
```

### 失敗時

```markdown
# Turbo Mode 実行失敗

> **失敗時点**: バッチ 3, Task T6
> **失敗事由**: Model パラメータ欠落

## 推奨措置

1. T6 再実行 (model: "sonnet" 追加)
2. バッチ 3 から再開始
```

---

## 使用例示

```bash
# 自然語呼び出し
"ターボモードでコンテキスト収集して"
"速く既存パターン分析して"
"並列で Model と Repository 実装して"

# 明示的呼び出し
/turbo-mode

# キャッシュ無視 (強制再実行)
/turbo-mode --force
```

---

## 変更履歴

| 日付       | バージョン | 変更内容                                                                                                                                             |
| ---------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-02-01 | v1.0       | 新規生成 - ultrawork + ecomode 統合、Web特化                                                                                                    |
| 2026-02-01 | v2.0       | 大幅強化 - ガイドライン → 実行エンジン、依存性分析/バッチ構成/並列実行プロトコル追加                                                                 |
| 2026-02-01 | **v3.0**   | **Enforced Skill Pattern 適用** - Pre-flight/Post-flight Checklist 強制、Model Routing Policy 強制、Evidence Caching 自動化、Violation Protocol 追加 |
