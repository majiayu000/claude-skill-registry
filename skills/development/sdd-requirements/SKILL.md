---
name: sdd-requirements
description: 実装したい機能の要件と受け入れ基準を定義し、要件定義書（requirements.md）を作成する。
---

# sdd-requirements

## Description
実装したい機能の要件と受け入れ基準を定義し、要件定義書（requirements.md）を作成する。
Trigger examples: "要件定義", "要件定義書作成", "仕様作りたい", "define requirements", "create spec", "仕様策定"

## ステップ1：前提確認
1. `.sdd/description.md` (機能説明) が存在することを確認する。
2. `.sdd/steering/` 配下のステアリング文書3点が揃っていることを確認する。
   - 不足している場合は適切なエラーメッセージを表示して停止する。

## ステップ2：spec作成または特定
1. `.sdd/description.md` を読み込み、機能内容を理解する。
2. `.sdd/target-spec.txt` を確認・更新する：
   - **新規の場合**: description から適切なspec名（例: `feature-name`）を生成し、`.sdd/specs/[spec名]/` ディレクトリを作成し、`target-spec.txt` に記録する。
   - **既存の場合**: ディレクトリが存在することを確認する。

## ステップ3：ステアリング情報の読み込み
`.sdd/steering/product.md`, `.sdd/steering/tech.md`, `.sdd/steering/structure.md` を読み込む。

## ステップ4：要件定義書の作成
`.sdd/specs/[spec名]/requirements.md` を以下の構成で作成する：

```markdown
# 要件定義書

## 機能概要
[description.mdの内容を基に機能の目的を記載]

## ユーザーストーリー
- ユーザーとして、[何を]したい。なぜなら[理由]だから。

## 機能要件
### 要件1：[主要機能名]
- 詳細説明
- 受入基準：
  - [ ] 条件1が満たされること
  - [ ] 条件2が満たされること

### 要件2：[次の機能]
- 詳細説明
- 受入基準：
  - [ ] 条件1が満たされること

## 非機能要件
- パフォーマンス/セキュリティなど：[必要に応じて]
```

## 完了確認
「要件定義完了。内容を確認したら `/sdd-design` へ進むか、小規模な修正で設計から実装まで一気に進めたい場合は `/sdd-highway` を実行してください。」
