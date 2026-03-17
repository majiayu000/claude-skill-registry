---
name: fix-bug
description: バグIDを指定してQAチェックリストに基づくコード修正を自動実行する
user-invocable: true
argument-hint: "<BUG-ID> (例: BUG-004)"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# バグ修正スキル

QAチェックリストのバグIDを指定して、コード修正を自動実行する。

## 処理フロー

1. `docs/qa_checklist.md` から指定バグIDの詳細情報を取得
2. バグに関連するファイルを特定し読み込み
3. `.claude/rules/` のルールを参照して修正方針を決定
4. コード修正を実行
5. 関連テストがあれば実行して検証
6. 修正サマリーを報告

## ルール参照

修正時は以下のルールを必ず遵守:

- `.claude/rules/ios-swift.md` — iOS開発ルール
- `.claude/rules/kotlin-kmp.md` — Kotlin KMP開発ルール

## 修正方針

- 最小限の変更で修正する（不要なリファクタリングをしない）
- 既存のコードパターンに従う
- 修正対象がKotlin shared層の場合: `./gradlew :shared:testDebugUnitTest` で検証
- 修正対象がiOS層の場合: ビルドエラーがないことを確認

## 出力フォーマット

```markdown
## BUG-XXX 修正レポート

### 修正内容
- 修正ファイル: `path/to/file.swift`
- 変更概要: ...

### 検証結果
- テスト: PASS / FAIL
- ビルド: SUCCESS / FAILURE

### 残存リスク
（該当する場合のみ）
```
