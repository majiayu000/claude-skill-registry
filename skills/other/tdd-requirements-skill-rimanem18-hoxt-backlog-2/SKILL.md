---
description: 明示的に @agent-tdd-requiement-analyst が呼び出すことで使用します。メインエージェントが使用する必要はありません。
---

## 事前準備

開発コンテキストの準備を行います：

1. **関連ファイルを直接読み込み**
   - `docs/implements/{要件名}/{{task_id}}/{feature_name}-requirements.md` - 既存の要件定義を確認
   - 関連する設計文書やタスクファイルも必要に応じて読み込み

読み込み完了後、準備されたコンテキスト情報を基にTDD要件定義の作業を開始します。

フォーマットは以下を参考にします:

[TDD用要件整理フォーマット](./references/TDD_REQUIREMENTS_TEMPLATE.md)

整理後、以下を実行してください：

1. 要件定義書を `docs/implements/{要件名}/{{task_id}}/{feature_name}-requirements.md` に保存（既存ファイルがある場合は追記）
2. TODOステータスを更新（要件定義完了をマーク）
3. **品質判定**: 要件の品質を以下の基準で判定
   - 要件が明確で曖昧さがない
   - 入出力仕様が具体的に定義されている
   - 制約条件が明確
   - 実装可能性が確実

## 品質判定基準

```
✅ 高品質:
- 要件の曖昧さ: なし
- 入出力定義: 完全
- 制約条件: 明確
- 実装可能性: 確実

⚠️ 要改善:
- 要件に曖昧な部分がある
- 入出力の詳細が不明確
- 技術的制約が不明
- ユーザー意図の確認が必要
```

## TODO更新パターン

```
- 現在のTODOを「completed」にマーク
- 要件定義フェーズの完了をTODO内容に反映
- 次のフェーズ「テストケース洗い出し」をTODOに追加
- 品質判定結果をTODO内容に記録
```

## 参考情報
必要な内容を取捨選択し Read して参考にしてください。

- [バックエンド開発ガイドライン](../common/references/backend.md)
- [フロントエンド開発ガイドライン](../common/references/frontend.md)
- [ドキュメント作成ガイドライン](../common/references/documents.md)
- [スキーマ駆動開発ガイドライン](../common/references/schema-db.md)
- [E2Eテストガイドライン](../common/references/e2e.md)
