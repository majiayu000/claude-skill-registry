---
name: glossary-updater
description: プロジェクト プロジェクトの glossary.md 用語集を更新するスキル。PRD/FRD 文書変更、新機能追加、コードベース変更後に用語集同期が必要なときにこのスキルを使用する。「用語集更新」、「glossary 同期」、「新用語追加」などの要求でトリガーされる。
doc_contract:
  review_interval_days: 90
---

# Glossary Updater

## Overview

プロジェクト プロジェクトのドメイン用語集（`docs/glossary.md`）を最新状態に保つスキル。PRD/FRD 文書、コードベース（enum、型定義）から新用語を発見して用語集に追加する。

## トリガー条件

次の状況でこのスキル使用を提案する:

1. **PRD/FRD 文書変更後**: `docs/features/` フォルダの文書が修正されたとき
2. **明示的要求**: 「用語集更新」、「glossary 同期」、「新用語追加」
3. **新機能実装完了後**: 新 enum、モデル、サービスが追加されたとき

## ワークフロー

### 1. 現在の用語集分析

```
Read docs/glossary.md
```

用語集の現在のセクション構造と既存用語リストを把握する。セクション構造は `references/glossary-structure.md` を参照。

### 2. ソース分析（変更タイプに応じて選択）

#### A. 文書ベース分析（PRD/FRD 変更時）

```
# 変更された PRD/FRD 文書を読む
Read docs/features/{feature-number}/PRD-*.md
Read docs/features/{feature-number}/FRD-*.md

# 新用語抽出: 太字(**term**)、テーブル定義、新概念
```

#### B. コードベース分析（コード変更時） - Feature-First 構造

```
# 新しく追加された enum/型定義確認（Feature-First）
Glob src/features/**/types/*.ts
Grep "enum " src/features/**/types/
Grep "interface " src/features/**/types/
Grep "type " src/features/**/types/

# 新 API / コンポーネント確認（Feature-First）
Glob src/features/**/api/*.ts
Glob src/features/**/components/*.tsx
```

### 3. 欠落用語識別

既存用語集とソースを比較して欠落した用語を識別する:

- 新 enum 値（例: `GamePhase`, `BattleMode`）
- 新型定義（例: `BattleResult`, `PlayerState`）
- PRD/FRD で定義された新概念

### 4. 用語追加

#### 用語追加形式

各セクションに適したテーブル形式で追加:

**ビジネス/ゲームシステム用語:**

```markdown
| **Term** | 日本語 | 説明 | 実装例 |
```

**技術用語:**

```markdown
| **Term** | 説明 | 実装 |
```

#### セクション選択基準

`references/glossary-structure.md` のセクション分類基準に従う。

### 5. 検証および完了

1. 目次と本文のセクション番号一致確認
2. マークダウンテーブル形式検証
3. 改訂履歴更新（バージョン番号増加）

## 注意事項

- **重複防止**: 既に存在する用語は追加しない
- **一貫した形式**: 既存テーブル形式と同じように維持
- **日本語説明**: すべての説明は日本語で作成
- **実装例**: 可能であれば実際のファイル名/型名を明示

## Resources

### references/

- `glossary-structure.md`: 用語集セクション構造および分類基準
