---
name: repo-create
description: |
  GitHubリポジトリを新規作成・初期化。ghコマンド使用。
  トリガー例: 「リポジトリを作成」「GitHubリポジトリ」「repo-create」「gh repo create」
allowed-tools: Bash, Write, Glob, Grep
arguments: auto-detect
user-invocable: true
---

# GitHub Repository Creator

GitHubリポジトリを新規作成・初期化します。

## 前提条件

- GitHub CLI (`gh`) がインストール済み
- `gh auth login` で認証済み

## ワークフロー

### 1. 引数解析
`$ARGUMENTS` からリポジトリ名とオプションを特定:

- `repo-create [name]` → リポジトリ名
- `--public` / `--private` → 可視性（デフォルト: public）
- `--description` / `-d` → 説明
- `--clone` → カレントディレクトリにclone

### 2. 作成手順

1. **リポジトリ名の決定**
   - 引数指定 → 使用
   - 未指定 → カレントディレクトリ名を使用

2. **GitHubリポジトリ作成**
   ```bash
   gh repo create [name] --[public|private] --description "[description]"
   ```

3. **初期ファイル生成**（--clone 指定時）

   詳細は [references/](references/) を参照:
   - `README-template.md` - README.md テンプレート
   - `LICENSE-options.md` - ライセンス選択ガイド
   - `badges.md` - バッジ一覧
   - `EXAMPLES.md` - 使用例
   - `header-svg-template.md` - ヘッダーSVGテンプレート（変数プレースホルダー付き）

   **生成するファイル:**
   - `README.md` - テンプレートをベースに作成
   - `.gitignore` - 言語自動検出（`gh repo create` のデフォルト）
   - `LICENSE` - 選択プロンプト（MIT/Apache-2.0/GPL-3.0等）→ See [LICENSE-options.md](references/LICENSE-options.md)
   - `assets/header.svg` - ヘッダー画像（自動生成）→ See [header-svg-template.md](references/header-svg-template.md)

   **ヘッダー画像生成手順:**
   1. リポジトリの内容を分析して適切なカラーマップを選択（AI/ML、Web、バックエンド等）
   2. プロジェクト名の長さに応じてフォントサイズを計算
   3. `header-svg-template.md` のテンプレートの変数を置換して `assets/header.svg` に出力

4. **initial commit**
   ```bash
   git init
   git branch -M main
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```

5. **完了メッセージ**
   - リポジトリURL
   - 次のステップ

## 使用例

詳細な使用例は [references/EXAMPLES.md](references/EXAMPLES.md) を参照。

```bash
/repo-create my-awesome-project
/repo-create my-app --private --description "My awesome app"
/repo-create my-lib --clone
```
