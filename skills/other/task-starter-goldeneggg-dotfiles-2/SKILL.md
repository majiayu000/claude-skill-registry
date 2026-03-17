---
name: task-starter
description: |
  Web開発プロジェクト・タスクの開始時に必要なドキュメント群を作成するスキル。
  以下の状況で使用:
    (1) ユーザーが「新しいプロジェクトを始めたい」「タスクを開始したい」「プロジェクトをセットアップして」と依頼した時
    (2) ユーザーが明示的に「/task-starter」を実行した時
    (3) 新機能開発、リファクタリング、バグ修正などのタスクで計画・ドキュメント整備が必要な時
    (4) 「ドキュメント構造を作って」「プロジェクトの骨組みを用意して」と依頼された時
    (5) 「タスク管理用のフォルダを作成して」「開発の準備をして」と依頼された時
    (6) 「TODOリストを整理したい」「作業計画を立てたい」と相談された時
    (7) 「仕様書のテンプレートが欲しい」「タスク分割を手伝って」と依頼された時
---

# Task Starter

Web開発プロジェクト・タスクの標準ドキュメント構造を生成し、計画を支援する。

## ワークフロー

### Phase 1: 情報収集

1. **プロジェクト基本情報を収集**
   ```
   AskUserQuestionツールで確認:
   - プロジェクト/タスク名
   - 出力先ディレクトリ
   - 概要と目的
   - 新規開発 or 既存コード改修
   ```

2. **既存コード改修の場合、現状を分析**
   - 関連ファイルをGlob/Grep/Readで調査
   - アーキテクチャと処理フローを把握
   - 課題・改善点を特定

### Phase 2: 構造生成

1. **プロジェクトフォルダを作成**
   スキルディレクトリ内のスクリプトを実行:
   ```bash
   python3 ~/.claude/skills/task-starter/scripts/init_project.py "{プロジェクト名}" --path "{出力先}" --description "{概要}"
   ```

   生成される構造:
   ```
   YYYYMMDD-{kebab-case-name}/
   ├── README.md           # 概要と目的
   ├── references/         # 現状分析資料
   ├── files/              # 参考データ・ファイル
   ├── specs/              # 要件・仕様書
   ├── todos/              # タスクドキュメント
   │   └── 001-{task-name}/
   └── logs/               # タスク作業ログ置き場
       └── 001-{task-name}/
   ```

2. **参考ファイルの有無を確認**
   - ユーザーに参考データ・ファイルがあるか質問
   - あれば `files/` にコピーまたはリンク

### Phase 3: ドキュメント生成

1. **references/ - 現状分析（既存コード改修時のみ）**
   - `{このSKILL.mdのDIR}/references/templates/reference-template.md` をベースに作成
   - 現状のアーキテクチャ、主要コンポーネント、処理フローを記載

2. **specs/ - 仕様書**
   - `{このSKILL.mdのDIR}/references/templates/spec-template.md` をベースに作成
   - 要件、技術仕様、UI/UX、依存関係を記載

3. **todos/ - タスク分割**
   - `{このSKILL.mdのDIR}/references/templates/todo-template.md` をベースに作成
   - 1-2時間で完了する粒度に分割
   - 各タスクに連番フォルダ: `001-setup/`, `002-implement-xxx/`, ...
   - 依存関係を考慮した順序で配置
   - 各タスクファイル内には references/ , specs/ への参照パスを記載

### Phase 4: レビューと確定

1. **生成結果を一覧表示**
   ```
   📁 YYYYMMDD-project-name/
   ├── 📄 README.md
   ├── 📁 references/
   │   └── 📄 current-state.md
   ├── 📁 files/
   ├── 📁 specs/
   │   └── 📄 feature-spec.md
   ├── 📁 todos/
   │   ├── 📁 001-setup/
   │   │   └── 📄 README.md
   │   └── 📁 002-implement/
   │       └── 📄 README.md
   └── 📁 logs/
       ├── 📁 001-setup/
       └── 📁 002-implement/
   ```

2. **ユーザーレビューを依頼**
   - 構造と内容を確認してもらう
   - フィードバックに基づき修正

3. **承認後、完了メッセージを表示**

## TODOタスク分割ガイドライン

### 粒度の基準
- **目安**: 1-2時間で完了
- **明確なゴール**: 完了条件が明確
- **独立性**: 他タスクへの依存を最小化しつつ、同時対応すべき内容は1つのタスクに内包

### Web開発での典型的な分割パターン

**フロントエンド機能追加**:
1. 001-design-component - コンポーネント設計
2. 002-implement-ui - UI実装
3. 003-add-state-management - 状態管理追加
4. 004-integrate-api - API連携
5. 005-add-tests - テスト追加

**API開発**:
1. 001-design-api - API設計
2. 002-implement-endpoint - エンドポイント実装
3. 003-add-validation - バリデーション追加
4. 004-add-error-handling - エラーハンドリング
5. 005-add-tests - テスト追加

**リファクタリング**:
1. 001-analyze-current - 現状分析
2. 002-design-new-structure - 新構造設計
3. 003-extract-xxx - 抽出・分離
4. 004-update-references - 参照更新
5. 005-verify-behavior - 動作確認

## 実装スタイル

### 自由度: Medium

- テンプレートは固定だが、内容はプロジェクトに応じてカスタマイズ
- フォルダ構造は標準化、ドキュメント内容は柔軟に対応

### ユーザーインタラクション

- **Phase 1**: 必須（プロジェクト情報収集）
- **Phase 4**: 必須（レビューと承認）
- **途中キャンセル**: 生成途中のファイルは削除またはユーザーに確認

## エラーハンドリング

| エラー                       | 対応                                           |
| ---------------------------- | ---------------------------------------------- |
| フォルダが既に存在           | エラーメッセージを表示し、別名を提案           |
| 権限不足でファイル作成不可   | エラーを報告し、別の出力先を提案               |
| 情報収集中にキャンセル       | 確認後、生成済みファイルを削除するか選択させる |
| Python 3が未インストール     | 手動でフォルダ構造を作成する代替手順を案内     |

## 前提条件

- Python 3.x（`{このSKILL.mdのDIR}/scripts/init_project.py`の実行に必要）
- 出力先ディレクトリへの書き込み権限

## リソース

### scripts/

- `{このSKILL.mdのDIR}/scripts/init_project.py` - プロジェクトフォルダ構造を生成（Python 3必須）

### references/templates/

- `{このSKILL.mdのDIR}/references/templates/spec-template.md` - 仕様書テンプレート
- `{このSKILL.mdのDIR}/references/templates/todo-template.md` - TODOタスクテンプレート
- `{このSKILL.mdのDIR}/references/templates/reference-template.md` - 現状分析テンプレート
