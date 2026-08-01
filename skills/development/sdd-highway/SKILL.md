---
name: sdd-highway
description: 要件定義書 (requirements.md) を基に、詳細設計書 (design.md) やタスクリスト (tasks.md) の作成手順を省略し、直接実装と記録を行う高速開発モード。小規模な機能追加、バグ修正、プロトタイピングに適している。
---

# sdd-highway

## Description
要件定義書 (`requirements.md`) を基に、詳細設計書 (`design.md`) やタスクリスト (`tasks.md`) の作成手順を省略し、直接実装と記録を行う高速開発モード。小規模な機能追加、バグ修正、プロトタイピングに適している。
Trigger examples: "一気に実装", "高速開発", "highway mode", "implement fast", "急ぎで実装", "サクッと修正", "fast track"

## ステップ1：前提確認
以下のファイルが揃っていることを確認する：
1. `.sdd/steering/` 配下のドキュメント（product.md, tech.md, structure.md）
2. `.sdd/target-spec.txt` （ターゲット指定済）
3. `.sdd/specs/[spec名]/requirements.md` （要件定義済）

## ステップ2：実装実行
要件定義書とステアリング情報を基に、以下の手順を一気に実行する。

1. **設計**: 思考プロセス内（Thinking Process）で簡易設計を行う（必要に応じてメモを残すが、`design.md` は必須ではない）。
2. **実装**: テスト先行開発（TDD）で実装を行う。
   - 既存コードの変更、新規ファイルの作成。
   - `npm test` による検証。

## ステップ3：記録 (Summary)
実装内容のサマリを `.sdd/specs/[spec名]/highway-summary.md` に記録する。

### 出力フォーマット
```markdown
# Highway 実装サマリ

## 設計方針
- <簡易設計メモ>

## 実装内容
- <変更点1>
- <変更点2>

## テスト結果
- <実施したテストコマンドと結果>
```

## 完了報告
「Highway実装完了。詳細は highway-summary.md を参照してください。
問題がなければ `/sdd-archive` でクローズしてください。」
