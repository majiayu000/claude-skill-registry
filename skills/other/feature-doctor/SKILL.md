---
name: feature-doctor
description: |
  プロジェクト プロジェクトの CONTEXT.json/状態不整合/破損を診断し自動復旧(Self-Healing)するスキル。
  CONTEXT.json エラー、状態不整合、JSON 破損、欠落コンテキスト、related_code 不整合等を復旧する必要がある時に使用する。
  「context 壊れた」「CONTEXT.json エラー」「状態不整合」「self-heal」「doctor」リクエストでトリガーされる。
doc_contract:
  review_interval_days: 90
---

# Feature Doctor (Self-Healing)

> **目標**: CONTEXT.json 基盤パイプラインが壊れた時に **中断なく復旧** し、復旧不可項目は明確に表記する。

## 核心原則

1. **SSOT 維持**: CONTEXT.json が真実の源泉
2. **安全な復旧**: 破損時にバックアップ作成後テンプレート基盤復旧
3. **明示的警告**: 自動復旧された項目は必ず警告として報告
4. **非破壊的補正**: 既存内容を上書きせず欠落フィールドのみ補完

---

## 実行手順

### Step 1: 診断実行

```bash
python3 .quality/scripts/feature_doctor.py
```

### Step 2: 自動復旧 (必要時)

```bash
python3 .quality/scripts/feature_doctor.py --fix
```

### Step 3: 結果要約

- 修正された CONTEXT.json リスト
- バックアップ作成パス (`CONTEXT.json.bak.<timestamp>`) 確認
- 復旧不可項目はユーザーに手動介入を要求

---

## 自動復旧ルール

- **CONTEXT.json 欠落**: テンプレート基盤生成 + `AwaitingUser` 状態で表示
- **JSON 破損**: 既存ファイルバックアップ → 復旧版生成 → blocker にバックアップパスを記録
- **必須フィールド欠落**: テンプレートデフォルト値で補完
- **index/spec パス欠落**: 実ファイル存在時に自動マッピング
- **feature_id 不整合**: 自動修正せず警告のみ出力
- **brief_context 欠落/空**: `brief_regenerator.py` を実行して BRIEF.md から自動抽出
  ```bash
  python3 .quality/scripts/brief_regenerator.py --apply --feature <NNN>
  ```
- **schema_version 旧バージョン**: 段階的マイグレーション実行
  - v4→v5: `architecture` セクション追加 (null 初期化)
  - v5→v6: `completion_contract` セクション追加 (テンプレート初期値)
  - v6→v7: `completion_contract.version` + `brief_context` セクション追加
  - マイグレーション後 `schema_version` → 7 に更新
  - **非破壊原則**: 既存フィールドは上書きせず、欠落フィールドのみ追加

---

## DO / DON'T

### DO

- ✅ 復旧前にバックアップ作成有無を確認
- ✅ 復旧結果を要約してユーザーに報告
- ✅ 必要時 `/feature-architect` で再生成を誘導
- ✅ brief_context 欠落時に `brief_regenerator.py --apply` で自動補完
- ✅ schema_version が最新版 (7) 未満の場合は段階的マイグレーション実行

### DON'T

- ❌ ユーザー同意なく既存コンテンツを強制上書き
- ❌ feature_id 不整合を自動修正
- ❌ 復旧結果を非表示処理

---

## 使用例

```bash
# 全体復旧
/feature-doctor

# 特定機能のみ復旧
/feature-doctor 046
```

> 実際の実行は内部的に `python3 .quality/scripts/feature_doctor.py` を使用する。
