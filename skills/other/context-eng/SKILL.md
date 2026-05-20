---
name: Context Engineering Framework
description: Autonomous context extraction and structuring for converting unstructured information from multiple sources into AI-interpretable structured formats.
allowed-tools: Read, Write, Grep, Glob, WebFetch
---

## 汎用情報構造化フレームワーク

このフレームワークは、ウェブサイト、ドキュメント、テキストデータなど、様々な形式の非構造化情報を、AIが解釈・活用可能な形式に自律的に変換・整理するための汎用的な設計思想と仕様を定義します。

### I. 自律型エージェント汎用仕様 (Generic Autonomous Agent Specification)

あらゆる情報ソースを処理し、構造化データを生成するエージェントの設計テンプレートです。

```yaml
agent_specification:
  name: "汎用コンテキストエンジニアリング・エージェント"
  version: "1.0.0"
  description: |
    様々な形式の入力ソースから、階層的かつ構造化されたコンテキスト情報を抽出し、
    指定された形式（YAML, JSON等）のドキュメントとして自動的に整理・永続化する自律型エージェント。
    情報収集、テキスト解析、構造化、永続化を統合的に実行する。

  core_capabilities:
    - "多様な入力ソース（URL、テキスト、ファイル）の処理"
    - "コンテンツの論理構造の解析と階層化"
    - "関連性に基づく情報のグルーピングと要約"
    - "新規の関連情報ソースの自律的発見と追跡（クロール）"
    - "指定された形式での構造化データの永続化"

  input_schema:
    type: object
    properties:
      source_specification:
        type: object
        description: "処理対象となる情報ソースの定義"
        properties:
          source_type:
            type: string
            enum: ["url_list", "raw_text", "file_path", "mixed"]
          sources:
            type: array
            description: "処理するソースのリスト（URL、テキスト、ファイルパスなど）"
      
      processing_options:
        type: object
        description: "処理方法に関する設定"
        properties:
          output_base_directory:
            type: string
            description: "生成ファイルの保存先ディレクトリ"
          crawling_config:
            type: object
            description: "ウェブクロールに関する設定（最大深度、対象ドメインなど）"
          content_extraction_config:
            type: object
            description: "コンテンツ抽出に関する設定（階層深度、要約レベルなど）"
          output_format_config:
            type: object
            description: "出力形式に関する設定（ファイル形式、インデックス生成の有無など）"

  autonomous_workflow:
    - "1. 初期化: 入力検証と環境設定"
    - "2. メインループ: 情報ソースが尽きるまで以下の処理を繰り返す"
    - "  a. コンテンツ取得: ソースから情報を取得"
    - "  b. 構造抽出: コンテンツを解析し、階層構造を抽出"
    - "  c. 新規ソース発見: コンテンツ内から新たな関連情報ソースを発見し、処理キューに追加"
    - "3. 最終化: 全収集データを整理し、指定された形式でファイルシステムに保存"

  tool_definitions:
    # エージェントが利用する仮想的なツール群
    - web_content_fetcher: "URLからウェブコンテンツを取得"
    - llm_structure_extractor: "テキストから階層構造を抽出"
    - url_discovery_engine: "コンテンツから関連URLを発見"
    - file_system_manager: "ファイルとディレクトリを管理"

  error_handling_strategy:
    # エラー発生時の再試行、処理継続、ロギングに関する戦略
    - retry_mechanisms: "一時的なエラーに対する再試行戦略"
    - graceful_degradation: "部分的な失敗時も成功した処理結果は保持"

  success_criteria:
    # エージェントの成功を定義する基準
    - functional_requirements: "入力が仕様通りに処理され、出力が整合していること"
    - performance_requirements: "指定された時間やリソース内で処理が完了すること"
```

### II. 情報ソース分析テンプレート (Information Source Analysis Template)

エージェントによる自動処理の前に、対象となる情報ソース（特にウェブサイト）の構造を手動で分析・理解するためのテンプレートです。

---

**件名: [対象サイト名] 構造分析レポート**

1.  **概要 (Overview)**
    *   **対象サイト名:**
    *   **URL:**
    *   **目的:** (例: 製品ドキュメント、企業ブログ、サポートポータル)

2.  **ナビゲーション構造 (Navigation Structure)**
    *   **主要カテゴリ:** (トップレベルのメニュー項目をリストアップ)
    *   **階層:** (例: カテゴリ → サブカテゴリ → 記事)

3.  **コンテンツ組織の特徴 (Content Organization Features)**
    *   **主要セクション:** (例: ガイド、チュートリアル、APIリファレンス、更新履歴)
    *   **情報アーキテクチャ:** (階層型、トピックベース、時系列など)

4.  **URL構造 (URL Structure)**
    *   **ベースURL:**
    *   **カテゴリページのパターン:**
    *   **個別記事のパターン:**

5.  **メタデータ (Metadata Organization)**
    *   各ページや記事に含まれるメタデータ (例: 更新日、作成者、タグ)

6.  **コンテンツ抽出のための推奨事項 (Recommendations for Content Extraction)**
    *   処理を開始すべきエントリーポイントURL
    *   クロール対象とすべきURLパターン
    *   抽出の際に注意すべき点

---

### III. 専門家プロファイル・テンプレート (Expert Profile Template)

特定のドメイン知識を持つ担当者や専門家の能力、アプローチ、利用ツールを定義するためのテンプレートです。これにより、情報構造化の背後にあるコンテキストを明確にします。

---

**件名: [専門家名/チーム名] プロファイル**

1.  **目的と背景 (Purpose & Context)**
    *   専門分野、ミッション、および活動の全体像を記述します。

2.  **現在の状況 (Current State)**
    *   現在注力しているプロジェクトやタスク、開発中のシステムについて記述します。

3.  **主要な学びと原則 (Key Learnings & Principles)**
    *   活動を通じて得られた核心的な知見や、常に従うべき基本原則をリストアップします。
    *   (例: 「構造化されたコンテキストがAIの精度を向上させる」「自動化には明確な成功基準が必要」)

4.  **アプローチとパターン (Approach & Patterns)**
    *   問題解決やタスク遂行における一貫した方法論や思考パターンを記述します。
    *   (例: 情報収集 → 体系的な分析 → 詳細な実装計画の策定)

5.  **ツールとリソース (Tools & Resources)**
    *   使用する主要な技術スタック、ソフトウェア、データソースなどをリストアップします。

---

### IV. 実行例：汎用テンプレートの適用 (Implementation Example)

上記フレームワークを使用して、特定のタスクを実行する際の具体的な設定例です。

```yaml
# 実行例: [対象サイト]のドキュメントを構造化する

example_usage:
  task_definition:
    source_specification:
      source_type: "url_list"
      sources:
        - "[対象サイトのトップページのURL]"
        - "[対象サイトの主要カテゴリページのURL]"
    
    processing_options:
      output_base_directory: "[出力先ディレクトリ名]"
      crawling_config:
        max_crawl_depth: 2
        target_domain_patterns:
          - "[クロールを許可するドメインの正規表現]"
        max_pages_per_domain: 50
      
      content_extraction_config:
        context_granularity: "L1_L2" # 見出しレベル1と2までを抽出
        content_summarization: "detailed"
      
      output_format_config:
        file_format: "yaml_frontmatter" # Markdown形式（メタデータ付き）
        generate_index: true

  expected_output_structure:
    # 期待される出力のディレクトリ構造とファイル内容のサンプル
    directory_tree: |
      [出力先ディレクトリ名]/
      ├── index.md
      ├── [カテゴリ1]/
      │   ├── [記事A].md
      │   └── [記事B].md
      └── [カテゴリ2]/
          ├── [記事C].md
          └── ...
    
    file_content_sample: |
      ---
      title: "[記事のタイトル]"
      source_url: "[元の記事のURL]"
      last_updated: "[最終更新日時]"
      ---
      
      # コンテンツの要約
      
      ここに、AIによって生成された記事の要約が記述されます。
      
      ## [サブタイトル]
      
      - サブタイトルに対応するコンテンツの要点