---
name: qa-check
description: QAチェックリストに対して現在のコードの修正状況を自動検証し、レポートを出力する
user-invocable: true
argument-hint: "[BUG-ID|all] (例: BUG-004 or all)"
allowed-tools: Read, Grep, Glob
---

# QA検証スキル

QAチェックリスト（`docs/qa_checklist.md`）に対して、現在のコードベースの修正状況を自動検証する。

## 処理フロー

1. `docs/qa_checklist.md` を読み込み、バグ一覧を解析
2. 引数で指定されたバグID（またはall）を対象に
3. 各バグの対応ファイルをGrep/Readで検査
4. 修正済み / 未解決 / 一部対応 のステータスを判定
5. レポートをマークダウンテーブルで出力

## 判定基準

- **修正済み**: バグの原因コードが修正されていることを確認
- **未解決**: バグの原因コードがそのまま残っている
- **一部対応**: 部分的に修正されているが完全ではない

## 出力フォーマット

```markdown
## QA検証レポート

| BUG-ID | 重要度 | ステータス | 対象ファイル | 詳細 |
|--------|--------|-----------|-------------|------|
| BUG-001 | High | 修正済み | MainTabView.swift | タブ構成が設計書通りに修正 |
| BUG-004 | High | 未解決 | DetailView.swift | リアクションボタンのクロージャが空 |

### サマリー
- 修正済み: X件
- 未解決: Y件
- 一部対応: Z件
```

## ルール違反チェック（追加検査）

以下のパターンもGrepで検出し、ルール違反として報告:

- `NavigationView` → `.claude/rules/ios-swift.md` 違反
- `@StateObject` (KMP VM用) → `.claude/rules/ios-swift.md` 違反
- `.onChange(of:.*\{.*newValue in` → 旧シンタックス
