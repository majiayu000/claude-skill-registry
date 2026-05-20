---
name: doc-coauthoring
description: |
  Guide users through a structured workflow for co-authoring documentation.
  Triggers: 「ドキュメントを書いて」「仕様書を作成」「READMEを更新」「提案書を作って」「PRD」「設計ドキュメント」
  Use when: Writing documentation, proposals, technical specs, decision docs, or similar structured content.
  Workflow: Context Gathering → Refinement & Structure → Reader Testing
---

# Doc Co-Authoring Workflow

構造化されたドキュメント共同作成ワークフロー。3つのステージを通じてユーザーをガイドする。

## Stage 1: Context Gathering
（ステージ1：コンテキスト収集）

**目標**: ユーザーの知識とエージェントの知識のギャップを埋める。

### 初期質問

1. ドキュメントの種類は？（技術仕様、提案書、決定文書等）
2. 主な読者は？
3. 読者に期待する反応は？
4. テンプレートや特定のフォーマットはある？
5. その他の制約やコンテキストは？

### 情報収集

- プロジェクト/問題の背景
- 関連するチーム議論やドキュメント
- 代替案が採用されない理由
- タイムライン制約
- 技術アーキテクチャや依存関係

### 終了条件

エッジケースやトレードオフについて質問できるようになったら、次のステージへ。

## Stage 2: Refinement & Structure
（ステージ2：構造化と改善）

**目標**: セクションごとにブレインストーミング・キュレーション・反復的改善で構築。

### 各セクションの作業フロー

1. **Clarifying Questions**: セクションに含める内容について5-10の質問
2. **Brainstorming**: 5-20のアイデアを生成
3. **Curation**: ユーザーが保持/削除/結合を判断
4. **Gap Check**: 不足している重要な情報がないか確認
5. **Drafting**: セクションを起草
6. **Iterative Refinement**: フィードバックに基づく改善

### 品質チェック（80%完了時）

- セクション間の流れと一貫性
- 冗長性や矛盾
- 「スロップ」がないか（英語の "slop"：汎用的な埋め文・内容のない定型表現）
- 全ての文が意味を持つか

## Stage 3: Reader Testing
（ステージ3：読者視点でのテスト）

**目標**: 新鮮な視点でドキュメントをテストし、盲点を発見する。

1. **Reader Questions**: 読者が質問しそうな5-10の質問を予測
2. **Testing**: 予測した質問をドキュメントに対してチェック
3. **Additional Checks**: 曖昧さ、前提知識、矛盾を確認
4. **Fix**: 見つかった問題を修正し、Stage 2に戻る

### 最終レビュー

Reader Testingが通ったら:
1. ユーザー自身の最終読み通しを推奨
2. 事実、リンク、技術詳細のダブルチェック
3. 望んだインパクトが達成されているか確認

## Resources

- `resources/implementation-playbook.md` - 詳細なワークフロー手順、サブエージェント活用、アーティファクト管理方針
