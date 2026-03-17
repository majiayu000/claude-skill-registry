---
name: git-commit
description: Gitコミット時に変更内容を分析し、コミットprefix（add/fix/docs/refactor/test/chore/perf/build/ci/revert/style）を適切に選定して、明確で追跡可能なコミットメッセージを作成・実行するためのスキル。コミットメッセージ作成、prefix選定、複数変更の分割判断、コミット実行時に使用する。
allowed-tools: Read, Write, Bash
---

# Git Commit スキル

変更差分を根拠に、適切な `prefix` を決定して高品質なコミットを作るためのスキルです。

## このスキルで採用するprefix

- `add`: ユーザー価値が増える機能追加・仕様追加
- `fix`: バグ修正・不具合是正
- `docs`: ドキュメントのみ変更
- `refactor`: 振る舞いを変えない内部改善
- `test`: テスト追加・修正
- `chore`: 雑務的変更（設定、依存更新、軽微保守）
- `perf`: パフォーマンス改善
- `build`: ビルドシステムや依存解決の変更
- `ci`: CI/CD設定の変更
- `revert`: 既存コミットの取り消し
- `style`: フォーマットやlintのみ（意味的変更なし）

## 基本方針

- 1コミット1目的を守る
- コミット前に差分を確認する
- コミットメッセージは日本語で記述する
- `prefix` は「変更の主目的」で決める
- 迷う場合の優先順位は `fix > add > refactor > chore`

## メッセージ形式

```text
<prefix>: <summary>

<detail>
- <file path 1>
- <file path 2>
```

- `summary` は 30〜60 文字目安
- `detail` は 1〜3 行で要点のみ記載
- 修正ファイル名は本文に含めてよい（簡潔に列挙）

例:

```text
add: 記事選定ロジックに重複除外ルールを追加

候補記事の重複判定を導入し、配信品質を安定化。
- src/newsletter/selector.py
- tests/test_selector.py
```

```text
fix: タイムアウト時に再試行回数が増えない不具合を修正

リトライカウンタ更新条件の分岐漏れを修正。
- src/lambda/handler.py
```

```text`
docs: ローカル実行手順と環境変数の説明を更新

READMEの手順を最新構成に合わせて整理。
- README.md
```

## 実行フロー

1. 変更確認

```bash
git status --short
git diff --staged
git diff
```

2. 変更の主目的を1文で定義
- 「何を直した/追加したか」ではなく「なぜ必要か」を明確化

3. prefix判定
- 判定表に従い最も影響の大きい変更を採用
- 複数目的が混在する場合はコミット分割を優先

4. ステージング整理

```bash
git add <file>
# または

git add -p
```

5. コミット実行

```bash
git commit -m "<prefix>: <summary>" -m "<detail>\n- <file path>"
```

## prefix判定ルール（実務用）

- バグを直しているなら `fix`（新規機能を含んでも原則 `fix`）
- 新しい振る舞いを導入するなら `add`
- 外部仕様に影響せず内部構造のみ整理なら `refactor`
- テストだけなら `test`
- ドキュメントだけなら `docs`
- CI定義だけなら `ci`
- 依存解決・ビルド定義中心なら `build`
- 速度改善が主目的なら `perf`
- どれにも当てはまらない保守作業は `chore`

## NG例

- `update`, `misc`, `changes` のような曖昧なsummary
- 無関係な変更を1コミットに混在
- `fix` なのに本文が「機能追加」中心
- 巨大コミットを分割せずにそのまま記録
- 詳細が長すぎて差分を読まないと要点が分からない本文

## 実行前チェックリスト

- 差分を確認した
- prefixの根拠を説明できる
- 1コミット1目的になっている
- summary と detail が重複せず簡潔
- 本文に主要な修正ファイル名を記載した
- テストまたは最低限の動作確認を実施した

## クイックコマンド

このスキルを呼び出すコマンドprefixは以下を推奨:

```text
/git-commit
```

実行例:

```text
/git-commit 「変更差分を見て適切なprefixでコミットして」
```
