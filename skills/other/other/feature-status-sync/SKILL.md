---
name: feature-status-sync
description: |
  プロジェクト プロジェクトの CONTEXT.json(SSOT) と index.md を同期するスキル。
  CONTEXT.json の progress 情報を基にコード存在有無を検証し、index.md を生成/更新する。
  feature-pilot の実装完了後の状態更新ステップで呼び出される。
  "機能状態同期", "ドキュメント・コード同期", "index.md 更新", "feature status sync" 等のリクエストでもトリガーされる。
doc_contract:
  review_interval_days: 90
---

# Feature Status Synchronizer

## Overview

プロジェクト プロジェクトにおける **CONTEXT.json(SSOT) とコード/ドキュメント間の同期** を実行するスキル。

### SSOT 構造

```
CONTEXT.json (SSOT) ← 唯一の真実のソース
    |
    +--→ コード検証 (ファイル存在有無)
    |
    +--→ index.md 生成 (個別 feature ビュー)
    |
    +--→ feature-registry.json 整合性検証 (Phase 7)
    |
    +--→ top-level index.md 同期 (Phase 7)
```

> **重要**: `index.md` は SSOT ではありません。`CONTEXT.json` から **生成されるビュー** です。

### 問題定義

- CONTEXT.json の progress と実際のコード状態の不一致
- index.md が outdated になり他のスキルが誤った情報を参照
- スキル間の SSOT 不一致による混乱

### 解決方法

1. `CONTEXT.json` から **FR別コードパス** を読み込み
2. 該当 **ファイルが実際に存在するか** 検証
3. **テストファイル存在有無** も確認
4. `CONTEXT.json` progress 更新
5. `index.md` 再生成

## トリガー条件

- `feature-pilot` 実装完了後の自動呼び出し (Step 5)
- "機能状態同期", "feature status sync"
- "index.md 更新", "ドキュメント・コード同期"
- PR 作成前の品質検査 (`/pre-quality-gate` 拡張)
- `priority-analyzer` 実行前の自動呼び出し推奨

## ワークフロー

### Phase 1: 対象 Feature 識別

```bash
# すべての feature CONTEXT.json 一覧を収集
Glob docs/features/*/CONTEXT.json
```

### Phase 2: 各 Feature 別分析

各 `CONTEXT.json` から:

1. **progress.details 読み込み** (FR別ファイルリスト)
2. **references.related_code 読み込み** (関連コードパス)
3. **priority.last_updated 確認** (Staleness 検査)

#### Priority Staleness 検査

> **自動化トリガー**: priority 更新の必要性を能動的に案内

```python
STALE_THRESHOLD_DAYS = 14

priority = context.get("priority", {})
last_updated = priority.get("last_updated")

if last_updated:
    days_old = (now - parse_datetime(last_updated)).days
    if days_old >= STALE_THRESHOLD_DAYS:
        print(f"Warning: {feature_id}: priority が {days_old} 日間更新されていません。")
        print(f"   /priority-analyzer {feature_id} --apply の実行を推奨します。")
```

**出力例**:

```
Warning: 008-monetization-system: priority が 21 日間更新されていません。
   /priority-analyzer 008-monetization-system --apply の実行を推奨します。
```

```json
{
  "progress": {
    "percentage": 100,
    "fr_total": 6,
    "fr_completed": 6,
    "details": {
      "FR-501": {
        "status": "completed",
        "files": ["src/features/lesson/components/LessonListPage.tsx"]
      }
    }
  }
}
```

### Phase 3: コード存在有無検証

```bash
# 各パスに対してファイル存在確認
Glob src/features/<feature>/components/<file>.tsx
Glob src/features/<feature>/hooks/<file>.ts

# テストファイル存在確認 (ルール: src/features/ → tests/unit/features/ 変換)
Glob tests/unit/features/<feature>/components/<file>.test.tsx
Glob tests/unit/features/<feature>/hooks/<file>.test.ts
```

### Phase 4: 状態判定ロジック

| コード存在 | テスト存在 | テスト通過 |  実装状態   |
| :--------: | :--------: | :--------: | :---------: |
|     OK     |     OK     |     OK     |  completed  |
|     OK     |     OK     |     NG     | in_progress |
|     OK     |     NG     |     --     | in_progress |
|     NG     |     --     |     --     |   pending   |

### Phase 4.5: テスト実行検証

> **目的**: ファイル存在だけでなく、テスト通過を Done 判定条件に含める

```bash
# 各 feature のテストを実行し結果を取得
npx vitest run tests/unit/features/${feature_name}/ --reporter=json
```

**結果を CONTEXT.json に記録**:

```json
{
  "progress": {
    "details": {
      "FR-XXX": {
        "status": "completed",
        "files": ["src/features/xxx/components/Yyy.tsx"],
        "test_passed": true,
        "last_verified_at": "2026-02-13T12:00:00+09:00"
      }
    }
  }
}
```

**判定フロー**:

1. テストファイルが存在しない → `in_progress`（テスト未作成）
2. テスト実行失敗 → `in_progress`（テスト不通過）
3. テスト実行成功 → `completed`（検証済み Done）

### Phase 5: CONTEXT.json 更新

```markdown
## CONTEXT.json 更新内容

1. Read `docs/features/<id>/CONTEXT.json`
2. Edit:
   - progress.percentage → 再計算
   - progress.fr_completed → 再計算
   - progress.details[FR-XXX].status → 検証結果反映
   - quick_resume.current_state → "SyncingStatus"
   - quick_resume.last_updated_at → 現在時刻
   - history[] += 同期記録
```

### Phase 6: index.md 生成

CONTEXT.json ベースで index.md を生成/再生成:

```markdown
# {feature_id}: {title}

> **状態**: {状態} ({progress.percentage}%)

## 進捗状況

| FR     | 名前         | コード | テスト |
| ------ | ------------ | :----: | :----: |
| FR-501 | レッスン一覧 |   OK   |   OK   |
| FR-502 | 対話学習     |   OK   |   --   |

## 関連ファイル

### Components

- src/features/lesson/components/LessonListPage.tsx

### Hooks

- src/features/lesson/hooks/useLessonSession.ts

...
```

### Phase 7: feature-registry.json 整合性検証 + top-level index.md 同期

> **目的**: 個別 feature の index.md 生成後、プロジェクト全体の整合性を保証

1. **feature-registry.json 整合性チェック**:
   - `docs/features/feature-registry.json` を読み込む
   - 対象 feature が registry に登録されているか確認
   - 未登録の場合は自動登録（feature-architect 未経由の手動作成ケース対応）

2. **top-level index.md 同期**:
   - `docs/features/index.md` に対象 feature のエントリが存在するか確認
   - 存在しない場合は「基盤モジュール」テーブルにエントリを追加
   - 統計セクションの数値を再計算

3. **validate_docs_consistency.py 実行（オプション）**:
   - `--json` モードで実行し、結果をチェック
   - D1-D5 のいずれかが FAIL の場合、警告メッセージを出力

## 不一致レポート

```markdown
## Feature Status Sync Report

### 不一致発見

| Feature                 | CONTEXT 状態 | 実際の状態 | 措置         |
| ----------------------- | :----------: | :--------: | ------------ |
| 015-gamification-system |      0%      |    95%     | CONTEXT 更新 |

### 詳細内容

#### 015-gamification-system

| FR      | CONTEXT | コード | テスト | 実際の状態 |
| ------- | :-----: | :----: | :----: | :--------: |
| FR-1501 | pending |   OK   |   OK   | completed  |
| FR-1502 | pending |   OK   |   OK   | completed  |
```

## コードパスマッピングルール

### ソース → テスト変換 (Feature-First 構造)

| ソースパス                            | テストパス                                        |
| ------------------------------------- | ------------------------------------------------- |
| `src/features/xxx/components/Yyy.tsx` | `tests/unit/features/xxx/components/Yyy.test.tsx` |
| `src/features/xxx/hooks/useYyy.ts`    | `tests/unit/features/xxx/hooks/useYyy.test.ts`    |
| `src/features/xxx/types/index.ts`     | `tests/unit/features/xxx/types/index.test.ts`     |
| `src/features/xxx/api/yyy.ts`         | `tests/unit/features/xxx/api/yyy.test.ts`         |
| `src/shared/components/Xxx.tsx`       | `tests/unit/shared/components/Xxx.test.tsx`       |

## 進捗率計算

```
全体進捗率 = (completed FR 数 / 全体 FR 数) x 100%

状態ラベル:
- 100%: 完了
- 80~99%: まとめ (~XX%)
- 50~79%: 進行中 (~XX%)
- 1~49%: 初期 (~XX%)
- 0%: 未実装
```

## 使用例

### 単一 Feature 同期

```
ユーザー: "015-gamification-system 状態同期して"

1. Read docs/features/015-gamification-system/CONTEXT.json
2. コードパス抽出・検証
3. CONTEXT.json progress 更新
4. index.md 再生成
5. ユーザーに結果報告
```

### 全体 Feature スキャン

```
ユーザー: "全体 feature 状態同期チェック"

1. Glob docs/features/*/CONTEXT.json
2. 各 feature に対して検証ループ
3. 不一致リスト生成
4. バッチ更新提案
```

## feature-pilot 連携

`feature-pilot` の実装完了段階で自動的に呼び出され、CONTEXT.json と index.md を同期:

```
feature-pilot パイプライン (NEW_FEATURE/MODIFY_FEATURE)
    ...
    Step 4: 実装完了
        ↓
    Step 5: feature-status-sync 呼び出し
        → Phase 1-6: CONTEXT.json + 個別 index.md 同期
        → Phase 7: registry 整合性 + top-level index.md 同期
        ↓
    Step 6: pre-quality-gate 呼び出し → 最終品質検証
```

## priority-analyzer 連携

`priority-analyzer` 実行時に **このスキルを先に呼び出し** て CONTEXT.json 状態を最新化した後に分析するよう推奨。

```markdown
## priority-analyzer 改善フロー

1. feature-status-sync 呼び出し → CONTEXT.json 同期
2. 同期された CONTEXT.json をベースに分析実行
3. 正確な優先順位結果の導出
```

### 双方向連携

| 方向                       | トリガー                  | 動作                            |
| -------------------------- | ------------------------- | ------------------------------- |
| **status-sync → priority** | Phase 2 で staleness 検知 | priority 更新案内メッセージ出力 |
| **priority → status-sync** | priority-analyzer 実行前  | progress 最新化推奨             |

**Staleness 閾値**: 14日 (STALE_THRESHOLD_DAYS)

---

## CONTEXT.json 直接更新

> **状態遷移**: `Implementing` / `BugFixing` → `SyncingStatus`

**更新例**:

```json
{
  "quick_resume": {
    "current_state": "SyncingStatus",
    "current_task": "015-gamification-system CONTEXT.json + index.md 同期完了",
    "next_actions": ["Reviewing ステップへ移行", "pre-quality-gate 実行"],
    "last_updated_at": "2026-02-11T16:00:00+09:00"
  },
  "progress": {
    "percentage": 95,
    "fr_total": 10,
    "fr_completed": 9,
    "fr_in_progress": 1
  },
  "history": [
    {
      "at": "2026-02-11T16:00:00+09:00",
      "from_state": "Implementing",
      "to_state": "SyncingStatus",
      "triggered_by": "feature-status-sync",
      "note": "FR 9/10 完了、CONTEXT.json + index.md 同期"
    }
  ]
}
```

---

## 注意事項

- **CONTEXT.json が SSOT**: index.md は生成物、直接編集禁止
- **自動更新はユーザー承認が必要**: 無断ドキュメント修正防止
- **Git 状態確認**: 修正前に `git status` で衝突可能性チェック
- **SPEC 文書は修正しない**: CONTEXT.json と index.md のみ対象

## CONTEXT.json 未存在時

```markdown
CONTEXT.json 未存在

`docs/features/029-vocabulary-book/CONTEXT.json` がありません。

次のいずれかを選択してください:

1. feature-architect で新規生成: `/feature-architect 029`
2. 手動で CONTEXT.json を作成
```

## Resources

このスキルは別途の実行スクリプトは不要です。ファイル検索と編集ツールで同期を実行します。

---

## 変更履歴

| 日付       | バージョン | 変更内容                                                     |
| ---------- | ---------- | ------------------------------------------------------------ |
| 2026-02-11 | v1.0       | プロジェクト 向けに移植 - Next.js/TypeScript 適応 |
