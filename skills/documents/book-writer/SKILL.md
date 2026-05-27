---
name: book-writer
description: |
  books リポジトリ用の技術文書作成ワークフロー。
  論文・技術文書などを .qmd 形式の構造化ドキュメントに変換する。
  サブエージェントで補足文書を並列生成し、Quarto callout で補足情報を追加。
  使用タイミング: (1) 論文まとめの作成、(2) 技術文書のドキュメント化、
  (3) 複雑な概念を含む文書の解説作成、(4) 「〜についてまとめて」という依頼
---

# Book Writer

books リポジトリ用の技術文書作成ワークフロー。論文・技術文書などを効率的に `.qmd` 形式の構造化ドキュメントへ変換する。

## ワークフロー概要

```
Phase 0: 執筆準備（言語・本確認・ディレクトリ作成）
    ↓
Phase 1: メイン文書作成 (00-overview.qmd)
    ↓
Phase 2: 補足文書の並列生成（サブエージェント）
    ↓
Phase 3: Callout 補足の追加
    ↓
Phase 4: index.qmd と _quarto.yml の設定
    ↓
Phase 5: 最終確認・リンク整備
```

## リファレンス

### 書式ルール（サブエージェント向け）

**重要**: サブエージェントに補足文書を作成させる際は、必ず `assets/formatting-rules.md` を読ませてください。

- **assets/formatting-rules.md**: 書式ルール完全版（Box drawings、Quarto 記法、ファイル命名、リンク等）
  - Box drawings 内は半角英数字のみ使用（日本語禁止）
  - 実在するファイルへのリンクのみ
  - Callout の適切な使用方法

### Quarto 機能リファレンス

詳細な Quarto 機能については、`references/` ディレクトリのリファレンスファイルを参照してください：

- **callouts.md**: Callout の詳細オプション（appearance, icon, collapse, cross-reference 等）
- **cross-references.md**: 図表・セクション・数式等への相互参照システム（`@fig-`, `@tbl-`, `@sec-` 等）
- **figures.md**: 図の挿入・サイズ調整・サブフィギュア・lightbox 等
- **tables.md**: 表の作成（pipe tables, list tables, 計算表）・スタイリング・サブテーブル等
- **diagrams.md**: Mermaid・Graphviz によるダイアグラム作成

これらは技術文書作成時に頻繁に参照することになります。特に **cross-references.md** は、図表参照を多用する技術文書では必須です。

---

## Phase 0: 執筆準備

### 目的

執筆開始前に必要な情報を確認し、ディレクトリ構造を準備する。

### 手順

1. **執筆言語の確認**: 日本語（`ja/`）か英語（`en/`）か
   - ユーザーに確認: 「日本語で執筆しますか？それとも英語ですか？」
   - 回答に応じてディレクトリを決定: `ja/{book}/` または `en/{book}/`

2. **本の名前の確認**: ディレクトリ名となる本（ケバブケース）
   - 例: `olmo-3`, `deepseek-r1`, `molmo2`, `qwen-3`

3. **元文書の確認**: 論文 URL、PDF パス、テキストファイルなど

4. **ディレクトリ作成**: `{lang}/{book}/` と `{lang}/{book}/images/` を作成

5. **_metadata.yml を作成**:
   ```yaml
   sidebar: book-name
   ```
   - `sidebar` には本の名前（ケバブケース）を指定
   - この値は `_quarto.yml` の `id` と一致させる

**注意**: `index.qmd` は Phase 4（補足文書が確定した後）に作成します。

---

## ディレクトリ構成

基本構成:

```
{lang}/{book}/
├── _metadata.yml           # サイドバーID指定
├── index.qmd               # 本のランディングページ（Phase 4で作成）
├── 00-overview.qmd         # メイン文書（概要・全体像）
├── 01-concept-a.qmd        # 補足文書1
├── 02-concept-b.qmd        # 補足文書2
├── 03-concept-c.qmd        # 補足文書3
├── ...
└── images/                 # 画像ディレクトリ
    └── figure.png
```

### ファイル命名規則

- **00-overview.qmd**: メイン文書（概要・全体の流れ）
- **01-xx.qmd, 02-xx.qmd...**: 補足文書（連番、トピック名をケバブケース）
- **images/**: 画像は専用ディレクトリに配置
- **拡張子**: `.qmd` を使用（Quarto の機能をフル活用）

### 参考例: ja/olmo-3/

```
ja/olmo-3/
├── _metadata.yml
├── index.qmd
├── 00-overview.qmd
├── 01-sliding-window-attention.qmd
├── 02-deduplication.qmd
├── 03-data-mixing.qmd
├── 04-midtraining.qmd
├── 05-long-context.qmd
├── 06-grpo-olmorl.qmd
└── images/
    └── olmo-3.png
```

---

## Phase 1: メイン文書作成 (00-overview.qmd)

### 目的

全体の流れを把握できるメイン文書を作成する。詳細は後で補足文書に分離。

### 手順

1. **構造分析**: 元テキストの章立て・主要トピックを把握
2. **骨格作成**: 見出し構成を決定（`## セクション` → `### サブセクション`）
3. **本文執筆**: 各セクションの要点を簡潔に記述
4. **補足候補マーク**: 詳細解説が必要な概念・用語に `> 詳細: [補足文書名](path.qmd)` を仮置き

### 出力例

```markdown
# {本の名前} Technical Report まとめ

## 概要

このモデルは...

## アーキテクチャ

### 特徴的な機構

効率的な Attention 機構を採用し...

> 詳細: [Sliding Window Attention](01-sliding-window-attention.qmd)

### その他の特徴

...
```

### リンク記法

メイン文書から補足文書へのリンクは相対パス:

```markdown
> 詳細: [補足文書タイトル](01-concept-name.qmd)
```

### 図表・ダイアグラム・クロスリファレンス

技術文書では図表やダイアグラムが頻繁に登場します。Quarto の強力な機能を活用しましょう：

- **図の挿入**: `![Caption](image.png){#fig-name}` で図を挿入し、`@fig-name` で参照
- **表の作成**: Pipe tables や List tables で複雑な表を作成し、`@tbl-name` で参照
- **ダイアグラム**: Mermaid や Graphviz でフローチャート・シーケンス図を作成
- **クロスリファレンス**: `@fig-`, `@tbl-`, `@sec-`, `@eq-` による統一的な参照システム
- **数式**: KaTeX（LaTeX 記法）を使用（`$x^2$` でインライン、`$$\sum_{i=1}^{n}$$` でディスプレイ）

> **詳細**: `references/cross-references.md`, `references/figures.md`, `references/tables.md`, `references/diagrams.md` を参照してください。

---

## Phase 2: 補足文書の並列生成

### 目的

メイン文書でマークした概念・用語について、サブエージェント（Task tool）で補足文書を並列生成。

### 手順

1. **補足候補の抽出**: メイン文書から `> 詳細:` でマークした箇所をリストアップ
2. **サブエージェント起動**: 各補足文書を並列で生成

```
Task tool を複数同時に呼び出し:
- Agent 1: 01-sliding-window-attention.qmd を作成
- Agent 2: 02-deduplication.qmd を作成
- Agent 3: 03-data-mixing.qmd を作成
```

3. **結果確認**: 各サブエージェントの出力を確認し、必要に応じて修正

### サブエージェントへのプロンプト例

**重要**: サブエージェントには必ず書式ルールを読ませてから作業させること。

```
あなたは book-writer スキルのサブエージェントです。

まず、以下の書式ルールを確認してください:
{.claude/skills/book-writer/assets/formatting-rules.md の内容を読み込む}

**CRITICAL ルール**（厳守）:
- 日本語（`ja/`）の場合は**である調**で記述（ですます調禁止）
- Box drawings 内は半角英数字のみ使用（日本語禁止）
- **リスト前に必ず空行を挿入**（箇条書き、順序付きリスト、チェックリスト全て）
- **blockquote（`>`で始まる引用ブロック）の前にも空行を挿入**
- リンクは実在するファイルのみ（存在しないファイルへのリンク禁止）
- 拡張子は必ず `.qmd`
- Callout は適切に開閉（`:::` の対応確認）

---

以下の概念について補足文書を作成してください:

- ファイル: {lang}/{book}/01-sliding-window-attention.qmd
- 対象概念: Sliding Window Attention
- 元文書の該当箇所: [引用]
- 含めるべき内容:
  - 概念の定義と動機
  - 仕組みの解説（図解があれば言及）
  - 他手法との比較（Quarto callout で記載）

**記法**:
- タイトル: `# Sliding Window Attention`
- 表・図があれば Quarto 記法で記述
- 他手法との比較は `.callout-note collapse="true"` で記載
```

### 補足文書の構成

- **タイトル**: `# 概念名`
- **内容**: 概念の定義、動機、仕組み、比較など
- **Callout**: 発展的内容や比較は Quarto callout で追加

---

## Phase 3: Callout 補足の追加

### 目的

本筋から逸れるが知っておきたい補足情報を Quarto callout で追加。

### Callout の使いどころ

- 他モデル・他手法との比較
- 発展的な内容（論文では触れられていない応用など）
- 参考情報（本文を読む上で必須ではないもの）
- 出典・参考文献への言及

### 記法

```markdown
::: {.callout-note collapse="true"}
## 他モデルとの比較: Qwen3, DeepSeek

Qwen3 は SWA を採用せず Full Attention を使用...

**参考**: [Qwen3 Technical Report](https://arxiv.org/abs/...)
:::
```

**Callout の種類**:
- `.callout-note`: 補足情報（デフォルト、青色）
- `.callout-tip`: ヒント・Tips（緑色）
- `.callout-important`: 重要な情報（赤色）
- `.callout-warning`: 警告（オレンジ色）
- `.callout-caution`: 注意（赤色）

**オプション**:
- `collapse="true"`: 折りたたみ可能にする
- `collapse="false"`: デフォルトで展開（省略時はこれ）

> **詳細**: より高度な Callout の使い方（appearance, icon, cross-reference 等）は `references/callouts.md` を参照してください。

### 手順

1. **メイン文書を走査**: 比較・発展内容を追加できる箇所を特定
2. **補足文書を走査**: 同様に callout 追加箇所を特定
3. **Callout 追加**: 各文書に callout を挿入

---

## Phase 4: index.qmd と _quarto.yml の設定

### 目的

補足文書が確定したので、本のランディングページ（index.qmd）を作成し、サイト全体のナビゲーションに統合する。

### 4.1: index.qmd の作成

Phase 2 で確定した補足文書をもとに、`index.qmd` を作成します。

#### テンプレート

```yaml
---
title: "本のタイトル"
description: "本の説明（1行）"
date: "YYYY-MM-DD"
author: "Naoto Iwase"
categories: [カテゴリ1, カテゴリ2, カテゴリ3]
image: "images/cover-image.png"
---

モデル/技術の簡単な説明（1-2段落）

**論文**: [arXiv:XXXX.XXXXX](https://arxiv.org/abs/XXXX.XXXXX)

**Tech Report**: URL（もしあれば）

## 目次

- [全体像](00-overview.qmd)
- [補足文書1のタイトル](01-xxx.qmd)
- [補足文書2のタイトル](02-xxx.qmd)
- ...
```

#### フィールド説明

- **title**: 本のタイトル（モデル名など）
- **description**: 1行の説明文（簡潔なひと言で）
- **date**: 作成日または論文の公開日（YYYY-MM-DD形式）
  - **重要**: 現在の日付は Bash ツールで `date +%Y-%m-%d` を実行して確認すること
  - タイポを防ぐため、手動で年を書かずに必ずコマンド結果を使用する
- **author**: "Naoto Iwase"（固定）
- **categories**: 適切なカテゴリを**最大2つまで**リスト形式で指定
  - **重要**: まず既存カテゴリを確認して表記揺れを防ぐ：
    ```bash
    python .claude/skills/book-writer/scripts/list_categories.py .
    ```
  - 既存カテゴリがあれば優先的に使用し、新規カテゴリは必要な場合のみ追加
  - 例: `[LLM, Reasoning]`
  - 例: `[VLM, Multimodal]`
  - 例: `[Deep Learning, Statistical Physics]`
- **image**: カバー画像のパス（`images/` ディレクトリ内）

#### 本文

- モデル/技術の簡単な紹介（1-2段落）
- 論文へのリンク（arXiv URLなど）
- Tech ReportやブログのURL（あれば）
- **目次**: 00-overview.qmd と Phase 2 で作成した全ての補足文書へのリンク

### 4.2: _quarto.yml のサイドバー設定

新しい本を `_quarto.yml` の `sidebar` セクションに追加します。`index.qmd` の目次と一致させます。

```yaml
sidebar:
  - id: new-book
    title: "New Book Title"
    style: "docked"
    contents:
      - section: "New Book Title"
        href: ja/new-book/index.qmd
        contents:
          - text: "全体像"
            href: ja/new-book/00-overview.qmd
          - text: "概念A"
            href: ja/new-book/01-concept-a.qmd
          - text: "概念B"
            href: ja/new-book/02-concept-b.qmd
          # ... 他の補足文書も同様に追加
```

**注意点**:
- `id` は一意の識別子（本の名前、`_metadata.yml` の `sidebar` と同じ）
- `title` はサイドバーに表示されるタイトル
- `href` は必ず相対パスで記述
- 補足文書の `text` は日本語の場合は日本語、英語の場合は英語で記述
- `index.qmd` の目次とサイドバーの内容を一致させること
- 既存のサイドバーエントリ（例: `olmo-3`, `molmo2`）を参考にすること

---

## Phase 5: 最終確認・リンク整備

### 目的

すべての文書とリンクが正しく整備されているか最終確認を行う。

### 手順

#### 5.1: Box Drawings の自動修正

**最初に必ず実行**: LLMは文字幅を正確に認識できないため、Box drawingsの修正は自動化ツールに任せます。

```bash
python .claude/skills/book-writer/scripts/fix_box_drawings.py {lang}/{book}
```

このスクリプトは:
- 全角文字と半角文字の表示幅を正しく計算（ASCII=1, 全角=2）
- Box drawingsの右端を自動で揃える
- 修正が必要なファイルのみ上書き

#### 5.2: リストとblockquote前の空行の自動修正

**次に必ず実行**: LLMは箇条書きやblockquote前の空行を見落としやすいため、自動化ツールで修正します。

```bash
python3 .claude/skills/book-writer/scripts/fix_spacing.py {lang}/{book}
```

このスクリプトは:
- 箇条書き（`-`, `*`, `+`）と順序付きリスト（`1.`, `2.`など）の直前に空行がない箇所を検出
- blockquote（`>`で始まる引用ブロック）の直前に空行がない箇所を検出
- 自動的に空行を挿入
- 修正が必要なファイルのみ上書き

#### 5.3: チェックリスト

自動修正ツールの実行後、以下を確認:

- [ ] 日本語（`ja/`）の場合は**である調**で記述されているか
- [ ] `_metadata.yml` が作成されているか（`sidebar: book-name` 形式）
- [ ] `index.qmd` が作成されているか（目次が全章を網羅しているか）
- [ ] `_quarto.yml` のサイドバーに追加されているか
- [ ] `index.qmd` の目次と `_quarto.yml` のサイドバーが一致しているか
- [ ] メイン文書から補足文書へのリンクが正しいか（`.qmd` 拡張子）
- [ ] 補足文書の番号が連番になっているか（01, 02, 03...）
- [ ] リスト前に空行が挿入されているか（箇条書き、順序付きリスト、チェックリスト全て）
- [ ] リスト項目内の引用（blockquote）の前にも空行が挿入されているか
- [ ] Quarto callout が正しく閉じているか（`:::` の対応）
- [ ] 画像は `images/` ディレクトリに配置されているか

### リンク形式の確認

メイン文書から補足文書:

```markdown
> 詳細: [Sliding Window Attention](01-sliding-window-attention.qmd)
```

画像の参照:

```markdown
![図のキャプション](images/figure.png)
```

### ローカルプレビュー（オプション）

Quarto でローカルプレビューして確認:

```bash
quarto preview
```

---

## Tips

### コンテキスト管理

- 元テキストが長い場合、Phase 1 では要点のみ抽出し、詳細は Phase 2 で各サブエージェントに分担
- サブエージェントには必要な部分のみ渡す（元テキスト全体を渡さない）

### 並列度の調整

- 補足文書が多い場合は 3-5 個ずつバッチで生成
- 依存関係がある場合は順次生成（例: 用語 A の説明に用語 B が必要）

### 一貫性の確保

- 用語の統一（メイン文書で定義した表記を補足文書でも使用）
- ファイル命名の連番は 00, 01, 02... のように2桁にする

### Box drawings の使用

図表やフロー図を Box drawings（罫線文字）で表現する際の注意点:

- **半角文字のみを使用**: Box drawings 内に日本語などの全角文字を入れると、文字幅が揃わずレイアウトが崩れるため、Box drawings 内は英数字・記号のみで記述
- **.qmd でも同じ**: Quarto でも ASCII box drawings は同様に機能する
- **サブエージェントへの注意**: サブエージェントに Box drawings を含む文書を作成させる際は、必ず `assets/formatting-rules.md` の該当セクションを読ませること
- **自動修正**: Phase 5で `scripts/fix_box_drawings.py` を必ず実行（LLMは文字幅を認識できないため）
- **例**:

```
Good (半角のみ):
┌─────────────────────────────────────────────────────────────┐
│  Stage 1: Pretraining                                       │
│  - Data: Dolma 3 Mix (6T tokens)                            │
│  - Goal: General language understanding & generation        │
└─────────────────────────────────────────────────────────────┘

Bad (全角文字混在):
┌─────────────────────────────────────────────────────────────┐
│  ステージ 1: 事前学習                                        │  ← 崩れる
│  - データ: Dolma 3 Mix (6T tokens)                          │  ← 崩れる
└─────────────────────────────────────────────────────────────┘
```

### 言語別の注意点

### 日本語 (ja/) の場合

- **文体**: である調（断定調）を使用
  - 例: 「〜である」「〜する」「〜となる」
  - ですます調は使用しない
- 専門用語は初出時に英語を併記: 「強化学習（Reinforcement Learning, RL）」
- 論文タイトルや固有名詞は原語表記を優先
- Callout 内も日本語で記述

### 英語 (en/) の場合

- 明確で簡潔な表現を心がける
- 専門用語は略語の初出時に展開: "Reinforcement Learning (RL)"
- Callout 内も英語で記述
