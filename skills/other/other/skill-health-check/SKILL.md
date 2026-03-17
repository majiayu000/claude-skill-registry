---
name: skill-health-check
description: |
  プロジェクト プロジェクトのスキルシステムガバナンスを自動検証するスキル。
  GOVERNANCE.md 規則遵守状況をチェックし、ヘルスレポートを生成する。

  **自動化された監査項目**:
  - MANIFEST.json 保有有無
  - 依存関係一貫性 (calls ↔ called_by マッチング)
  - Deprecated スキル経過時間
  - バージョンスキーマ遵守
  - 状態遷移規則検証

  「スキルヘルスチェック」、「ガバナンス検査」、「スキル監査」、「health check」などのリクエストでトリガーされる。

  <example>
  user: "スキルヘルスチェックして"
  assistant: "skill-health-checkを使用してスキルシステム全体を監査します"
  </example>

  <example>
  user: "ガバナンス規則違反ある?"
  assistant: "skill-health-checkを実行して規則違反事項を検査します"
  </example>
doc_contract:
  review_interval_days: 30
---

# Skill Health Check (スキルガバナンス自動監査)

> **核心コンセプト**: "自動化された規則遵守検証" (Automated Governance Compliance)

スキルシステムの長期運用のため GOVERNANCE.md 規則を自動検証するメタスキル。

## 核心原則

1. **自動化優先**: 手動監査依存を最小化
2. **規則ベース**: GOVERNANCE.md 規則を機械的に検証
3. **早期警報**: 問題発生前の予防的検出
4. **実行可能な推奨**: 発見事項に対する具体的措置案内

---

## 🚨 EXECUTION PROTOCOL (MANDATORY) - v2.0

> **ESP v2.0 適用**: このスキルは Enforced Skill Pattern に従います。

### Pre-flight Checklist (スキル開始前必須出力)

```markdown
## ✈️ Pre-flight Checklist - skill-health-check

|   ID   | 項目                           | 状態 | 備考 |
| :----: | ------------------------------ | :--: | ---- |
| PF-001 | GOVERNANCE.md アクセス可能     |  ⬜  |      |
| PF-002 | スキルディレクトリアクセス可能 |  ⬜  |      |
| PF-003 | 監査範囲確定 (全体/単一スキル) |  ⬜  |      |

→ 全ての項目 ✅ 確認後監査進行
→ PF-001, PF-002 ❌ 時即座に中断
```

### Post-flight Checklist (スキル完了前必須出力)

```markdown
## 🛬 Post-flight Checklist - skill-health-check

|   ID    | 項目                   | 状態 | 備考 |
| :-----: | ---------------------- | :--: | ---- |
| POF-001 | ヘルスレポート出力完了 |  ⬜  |      |
| POF-002 | ヘルススコア計算完了   |  ⬜  |      |
| POF-003 | 推奨措置リスト提示     |  ⬜  |      |

→ POF-001, POF-002 ❌ 時監査未完了処理
```

### Model Routing Policy

| 作業              | 推奨モデル | 備考               |
| ----------------- | :--------: | ------------------ |
| MANIFEST スキャン |   haiku    | ファイル存在確認   |
| 依存性分析        |   haiku    | 相互参照確認       |
| ESP 検証          |   sonnet   | プロトコル理解必要 |
| レポート生成      |   haiku    | フォーマッティング |

### Violation Protocol

| 違反類型             |  深刻度  | 処理                       |
| -------------------- | :------: | -------------------------- |
| Pre-flight 未出力    | CRITICAL | 即座に中断、最初から再開始 |
| Post-flight 未検証   |   HIGH   | 完了報告前検証実行         |
| Model パラメータ欠落 |  MEDIUM  | 該当 Task 再実行           |
| ヘルススコア未計算   |   HIGH   | レポート不完全処理         |

---

## 🔍 監査項目 (Audit Checklist)

### 1. MANIFEST 保有検査

**規則**: 全てのスキルは MANIFEST.json を保有すべきである。

```
検査ロジック:
1. .claude/skills/*/SKILL.md リスト収集
2. 各スキルディレクトリに MANIFEST.json 存在確認
3. 未保有スキルリスト生成
```

**出力**:

```markdown
### MANIFEST 保有現況

|   状態    | 数量 | 比率 |
| :-------: | :--: | :--: |
|  ✅ 保有  |  14  | 38%  |
| ❌ 未保有 |  23  | 62%  |

#### 未保有スキルリスト (優先順位順)

| 優先順位 | スキル        | Tier | 事由                     |
| :------: | ------------- | :--: | ------------------------ |
|    P1    | pre-quality-gate |  3   | 核心 QA インフラ         |
|    P1    | security-scan |  3   | セキュリティ核心インフラ |
|   ...    | ...           | ...  | ...                      |
```

### 2. 依存性一貫性検査

**規則**: `calls` 配列のスキルは該当スキルの `called_by`に逆参照されるべきである。

```
検査ロジック:
1. 全ての MANIFEST.json ロード
2. A.calls に B があれば → B.called_by に A があるべき
3. 不一致ペア識別
```

**出力**:

```markdown
### 依存性一貫性

| 検査項目                     |     状態     |
| ---------------------------- | :----------: |
| calls → called_by マッチング | ⚠️ 2件不一致 |
| 循環依存性                   |   ✅ なし    |

#### 不一致詳細

| スキル A      | calls      | スキル B   | called_by 欠落 |
| ------------- | ---------- | ---------- | :------------: |
| feature-pilot | turbo-mode | turbo-mode |       ❌       |
```

### 3. Deprecated スキル経過検査

**規則**: Deprecated 後 6ヶ月経過時 Archive 必要。

```
検査ロジック:
1. SKILL.md で "DEPRECATED" マーカー検索
2. deprecated 日付抽出 (GOVERNANCE.md 参照)
3. 現在日付と比較して経過時間計算
```

**出力**:

```markdown
### Deprecated スキル現況

| スキル                    | Deprecated 日付 | 経過 | Archive 予定 |   状態    |
| ------------------------- | :-------------: | :--: | :----------: | :-------: |
| feature-data-wiring       |   2026-01-25    | 7日  |  2026-07-25  | ✅ 猶予中 |
| feature-navigation-wiring |   2026-01-25    | 7日  |  2026-07-25  | ✅ 猶予中 |
```

### 4. バージョンスキーマ検査

**規則**: バージョンは `vMAJOR.MINOR.PATCH` 形式に従うべきである。

```
検査ロジック:
1. MANIFEST.json の skill_version フィールド検査
2. 正規表現マッチング: /^\\d+\\.\\d+\\.\\d+$/
3. SKILL.md 変更履歴のバージョン表記検査
```

### 5. Tier 分類検査

**規則**: tier は 1, 2, 3 の中の一つであるべきである。

```
検査ロジック:
1. MANIFEST.json の tier フィールド検査
2. 有効値: 1 (Orchestrator), 2 (Pipeline), 3 (Utility)
```

### 6. ESP (Enforced Skill Pattern) 検証 ⭐ v2.1

> **核心目的**: "文書構造検証"を通じた ESP 強制力確認
>
> ⚠️ **設計原則**: ESP は **静的文書検証**で強制される。
> ランタイムログは強制不可能なので使用しない。

**規則**: ESP 適用スキルは MANIFEST.json と SKILL.md 全てに ESP 構造があるべきである。

### 7. Documentation Contract 検査 ⭐ v2.2

> `node .claude/scripts/doc-contract.mjs --json` 実行結果基準

**規則**: 全てのスキル/エージェントは最新マニュアルを保有すべきである。

```
検査ロジック:
1. node .claude/scripts/doc-contract.mjs --json 実行
2. 結果 JSON の summary で状態別カウント抽出
3. CURRENT 比率でスコア計算 (加重値 10%)
4. STALE/MISSING → Critical 推奨措置提示
5. REVIEW_NEEDED → Warning 推奨措置提示
```

**出力**:

```markdown
### Documentation Contract 現況

|       状態       | 数量 | 比率 |
| :--------------: | :--: | :--: |
|    ✅ CURRENT    |  42  | 74%  |
|     🔴 STALE     |  3   |  5%  |
|    ⚠️ MISSING    |  8   | 14%  |
| 🟡 REVIEW_NEEDED |  4   |  7%  |

#### 推奨措置

| 優先順位 | ツール        |  状態   | 措置                            |
| :------: | ------------- | :-----: | ------------------------------- |
|    P1    | feature-pilot |  STALE  | /manual-generator feature-pilot |
|    P2    | new-skill     | MISSING | /manual-generator new-skill     |
```

#### 6.1 MANIFEST.json ESP 設定検査

```
検査ロジック:
1. MANIFEST.json 存在確認
2. schema_version >= 2 確認
3. enforced_protocol フィールド存在確認
4. preflight_required, postflight_required = true 確認
5. model_routing セクション存在確認
```

#### 6.2 SKILL.md EXECUTION PROTOCOL 検査

```
検査ロジック:
1. SKILL.md で "EXECUTION PROTOCOL" セクション存在確認
2. Pre-flight Checklist テーブル存在確認
3. Post-flight Checklist テーブル存在確認
4. Model Routing Policy テーブル存在確認
5. Violation Protocol テーブル存在確認
```

#### 6.3 文書-実際一貫性検査

```
検査ロジック:
1. MANIFEST.json の preflight_checks 個数 == SKILL.md Pre-flight 項目数
2. MANIFEST.json の postflight_checks 個数 == SKILL.md Post-flight 項目数
3. MANIFEST.json の model_routing.task_specific キー == SKILL.md Model Routing 作業リスト
```

**出力**:

```markdown
### ESP 遵守現況 (静的文書検証)

#### ESP 適用スキルリスト

| スキル             | Schema | MANIFEST ESP | SKILL.md PROTOCOL | 一貫性 | 状態 |
| ------------------ | :----: | :----------: | :---------------: | :----: | :--: |
| feature-pilot      |   2    |      ✅      |        ✅         |   ✅   | 完了 |
| turbo-mode         |   2    |      ✅      |        ✅         |   ✅   | 完了 |
| persistent-mode    |   2    |      ✅      |        ✅         |   ✅   | 完了 |
| pre-quality-gate   |   2    |      ✅      |        ✅         |   ✅   | 完了 |
| security-scan      |   2    |      ✅      |        ✅         |   ✅   | 完了 |
| skill-health-check |   2    |      ✅      |        ✅         |   ✅   | 完了 |

#### ESP 文書構造スコア

| 指標                     |  値  | 目標 | 状態 |
| ------------------------ | :--: | :--: | :--: |
| ESP 適用スキル数         |  6   |  ≥4  |  ✅  |
| MANIFEST-SKILL.md 一貫性 | 100% | 100% |  ✅  |
| Pre-flight 定義率        | 100% | 100% |  ✅  |
| Post-flight 定義率       | 100% | 100% |  ✅  |

#### 不一致発見時

| スキル            | 問題類型              | 詳細                  | 推奨措置        |
| ----------------- | --------------------- | --------------------- | --------------- |
| (例示) some-skill | MANIFEST-SKILL 不一致 | Pre-flight 3個 vs 2個 | SKILL.md 同期化 |
```

#### 6.4 ESP 未適用核心スキル識別

```
検査ロジック:
1. Tier 1/2 スキル中 ESP 未適用識別
2. 核心インフラスキル中 ESP 未適用識別
3. 優先マイグレーション対象リスト生成
```

**出力**:

```markdown
#### ESP マイグレーション優先順位

| 優先順位 | スキル              | Tier | 現在 Schema | 推奨措置          |
| :------: | ------------------- | :--: | :---------: | ----------------- |
|    P1    | feature-architect   |  2   |      1      | ESP v2.0 検討推奨 |
|    P1    | feature-implementer |  2   |      1      | ESP v2.0 検討推奨 |
|    P2    | bug-fix             |  2   |      1      | ESP v2.0 検討推奨 |
```

---

## 📊 レポート出力フォーマット

### 全体ヘルス要約

```markdown
# スキルシステムヘルスレポート

> **監査日**: 2026-02-01
> **総スキル数**: 37個

## Executive Summary

| 検査項目             | 状態 |   スコア   |
| -------------------- | :--: | :--------: |
| MANIFEST 保有率      |  🔴  |    38%     |
| 依存性一貫性         |  🟡  | 2件不一致  |
| Deprecated 管理      |  ✅  |    正常    |
| バージョンスキーマ   |  ✅  | 100% 遵守  |
| **全体ヘルススコア** |  🟡  | **65/100** |

## 推奨措置 (優先順位順)

### 🔴 Critical (即座)

1. turbo-mode called_by 更新必要

### 🟡 Warning (1週以内)

1. pre-quality-gate MANIFEST 生成
2. security-scan MANIFEST 生成
3. persistent-mode MANIFEST 生成

### ℹ️ Info

- Deprecated スキル 2個は 2026-07-25 Archive 予定
```

---

## 🚀 実行プロトコル

### Phase 1: データ収集

```
1. Glob: .claude/skills/*/SKILL.md → 全体スキルリスト
2. Glob: .claude/skills/*/MANIFEST.json → MANIFEST 保有リスト
3. Read: 各 MANIFEST.json 内容パース
4. Read: GOVERNANCE.md 規則参照
```

### Phase 2: 規則検証

```
for each skill in skills:
    1. MANIFEST 存在確認
    2. MANIFEST スキーマ検証
    3. 依存性相互検証
    4. Deprecated 状態確認
    5. バージョンフォーマット検証
```

### Phase 3: レポート生成

```
1. 検査結果集計
2. ヘルススコア計算
3. 優先順位別推奨措置整列
4. Markdown レポート出力
```

---

## 📈 ヘルススコア計算

| 項目                          | 加重値  |   満点   | 計算方式                                                  |
| ----------------------------- | :-----: | :------: | --------------------------------------------------------- |
| MANIFEST 保有率               |   25%   |   25点   | (保有数 / 総数) × 25                                      |
| **ESP 文書遵守率** ⭐         | **20%** | **20点** | (MANIFEST ESP 設定 + SKILL.md PROTOCOL + 一貫性) / 3 × 20 |
| 依存性一貫性                  |   15%   |   15点   | 不一致 0 = 15点、1件当たり -3点                           |
| Deprecated 管理               |   10%   |   10点   | 違反 0 = 10点、1件当たり -3点                             |
| バージョンスキーマ            |   10%   |   10点   | (遵守数 / 総数) × 10                                      |
| Tier 分類                     |   10%   |   10点   | (有効数 / 総数) × 10                                      |
| **Documentation Contract** ⭐ | **10%** | **10点** | (CURRENT 数 / 総数) × 10                                  |

**ESP スコア細部**:

- MANIFEST ESP 設定: (ESP 設定完了スキル / ESP 対象スキル) × 100%
- SKILL.md PROTOCOL: (PROTOCOL セクションあるスキル / ESP 対象スキル) × 100%
- 文書一貫性: (MANIFEST-SKILL.md 一致スキル / ESP 対象スキル) × 100%

**ボーナススコア**:

- ESP 適用スキル 6個以上: +5点
- 全ての ESP スキル文書一貫性 100%: +5点

**等級**:

- 🟢 Good: 80-100点
- 🟡 Warning: 60-79点
- 🔴 Critical: 0-59点

---

## 🔄 自動実行時点

| 時点                | トリガー               | 範囲                 |
| ------------------- | ---------------------- | -------------------- |
| **月間** (毎月 1日) | 手動またはスケジュール | 全体監査             |
| **スキル変更後**    | 推奨                   | 変更されたスキルのみ |
| **PR 生成前**       | 推奨                   | 全体監査             |

---

## ⚠️ 制約事項

1. **読取専用**: このスキルは監査のみ実行し、自動修正しない
2. **MANIFEST 依存**: MANIFEST ないスキルは一部検査不可
3. **手動措置必要**: 推奨措置は人間が実行すべき

---

## 使用例示

```bash
# 全体ヘルスチェック
/skill-health-check

# 特定項目のみ検査
/skill-health-check --manifest-only
/skill-health-check --dependencies-only

# レポート保存
/skill-health-check --save docs/metrics/health-2026-02.md
```

---

## 変更履歴

| 日付       | バージョン | 変更内容                                                                                                                                                               |
| ---------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-02-09 | v2.2       | **Documentation Contract 検査追加**: doc-contract.mjs 基準 7番目監査項目。CURRENT 比率でスコア計算 (加重値 10%)。既存加重値再調整 (manifest 30→25, dependency 20→15)。 |
| 2026-02-01 | v2.1       | **ESP 検証方式根本再設計**: ランタイムログ(esp_execution_log) → 静的文書検証に転換。MANIFEST.json + SKILL.md 構造一貫性検査。強制不可能なメトリック削除。              |
| 2026-02-01 | v2.0       | **ESP 検証機能追加**: ESP 適用有無検査、EXECUTION PROTOCOL セクション追加、ヘルススコアに ESP 項目追加 (加重値 20%)                                                    |
| 2026-02-01 | v1.0       | 新規生成 - 自動化されたガバナンス監査スキル                                                                                                                            |
