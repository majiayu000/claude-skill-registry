---
name: compile-report
description: レポートコンパイルエージェント - 分析結果のMarkdownファイルを統合HTMLレポートに変換。/compile-report [出力パス] で呼び出し。
user_invocable: true
---

# Report Compiler Agent

分析結果のMarkdownファイルを統合HTMLレポートに変換するエージェントです。

## 目的

このエージェントは以下の機能を提供します：

1. **Markdownの自動検出・統合** - 各ディレクトリ内のすべてのMarkdownファイルを動的に検出し統合
2. **Mermaid図のレンダリング** - Mermaid図をインライン埋め込み
3. **GraphDB可視化** - D3.jsインタラクティブグラフを埋め込み
4. **目次生成** - 自動的にサイドバー目次を生成
5. **スタイリング** - プロフェッショナルなスタイルを適用（ライト/ダークテーマ）
6. **レスポンシブ** - モバイル/印刷対応
7. **重複除去** - ファイル名の命名規則が異なる重複ファイルを自動的に除去

## 前提条件

- Python 3.9+
- markdown パッケージ
- pymdown-extensions パッケージ
- （オプション）mermaid-cli（Mermaid図の検証用）

## 実行プロンプト

あなたはレポートをコンパイルする専門家エージェントです。以下の手順でHTMLレポートを生成してください。

### Step 1: 環境確認

```bash
# 必要なパッケージの確認
source .venv/bin/activate
pip install markdown pymdown-extensions
```

### Step 2: Mermaid図の検証（推奨）

レポート生成前にMermaid図の構文エラーをチェックします。

```bash
# mmdc がインストールされている場合
/fix-mermaid ./reports
```

**注意: Mermaidの予約語問題**

以下の単語はMermaidのsequenceDiagramで予約語として解釈されるため、participant名として使用しないでください：

| 予約語 | 代替案 |
|-------|-------|
| `BOX` | `BoxAPI`, `BoxPlatform`, `BoxWebhook` |
| `box` | 同上 |

**例:**
```mermaid
# NG
participant BOX as BOX Platform

# OK
participant BoxPlatform as BOX Platform
```

### Step 3: レポートコンパイルスクリプトの実行

```bash
source .venv/bin/activate && python scripts/compile_report.py \
  --input-dir ./reports \
  --output ./reports/00_summary/full-report.html \
  --title "リファクタリング分析レポート"
```

### Step 4: 出力形式

#### 統合HTMLレポート

```html
<!DOCTYPE html>
<html>
<head>
    <title>リファクタリング分析レポート</title>
    <script src="mermaid.min.js"></script>
    <script src="d3.v7.min.js"></script>
    <style>/* プロフェッショナルスタイル */</style>
</head>
<body>
    <nav class="sidebar"><!-- サイドバー目次 --></nav>
    <main class="main-content">
        <section id="summary"><!-- エグゼクティブサマリー --></section>
        <section id="analysis"><!-- 分析結果 --></section>
        <section id="evaluation"><!-- MMI評価 --></section>
        <section id="design"><!-- 設計書 --></section>
        <section id="stories"><!-- ドメインストーリー --></section>
        <section id="graph">
            <!-- ナレッジグラフ -->
            <!-- D3.jsインタラクティブビューア -->
        </section>
    </main>
</body>
</html>
```

### Step 5: コマンドオプション

| オプション | 説明 | デフォルト |
|-----------|------|----------|
| `--input-dir` | 入力ディレクトリ | ./reports |
| `--output` | 出力HTMLファイル | ./reports/00_summary/full-report.html |
| `--title` | レポートタイトル | リファクタリング分析レポート |
| `--theme` | テーマ (light/dark) | light |

## 機能詳細

### Markdownファイルの自動検出

スクリプトは各レポートディレクトリ（`00_summary`, `01_analysis`, `02_evaluation`, など）から自動的にすべてのMarkdownファイルを検出します。

**動作:**
1. 優先ファイルリストに従って順序を決定
2. ディレクトリ内の他のMarkdownファイルを自動検出
3. ファイル名の命名規則の違い（`target-architecture.md` vs `target_architecture.md`）による重複を自動除去
4. サブディレクトリ（`visualizations/`など）も検索対象

**対応するファイル構造:**
```
reports/
├── 00_summary/          # エグゼクティブサマリー
├── 01_analysis/         # システム分析（全ファイル自動検出）
├── 02_evaluation/       # MMI評価
├── 03_design/           # 設計（API、ScalarDB含む全ファイル）
├── 04_stories/          # ドメインストーリー（個別ストーリー含む）
├── 05_estimate/         # コスト試算
└── graph/               # ナレッジグラフ（サブディレクトリ含む）
```

### GraphDB可視化の統合

`reports/graph/visualizations/graph.html`が存在する場合、自動的にインタラクティブグラフをレポートに埋め込みます。

**機能:**
- ノードのドラッグ移動
- マウスホイールでズーム
- ノードホバーで詳細表示（名前、タイプ、グループ）
- ノード検索
- 凡例表示（Domain/Entity/Term）

**前提:**
- `/build-graph` でGraphDBが構築済み
- `/visualize-graph` で可視化ファイルが生成済み

### Mermaid図のレンダリング

Markdownファイル内の```mermaid```ブロックを自動的に`<div class="mermaid">`に変換し、Mermaid.jsでレンダリングします。

**対応図:**
- flowchart / graph
- sequenceDiagram
- classDiagram
- stateDiagram
- erDiagram
- gantt
- xychart-beta

**非対応:**
- radarChart（xychart-betaで代替）

## 出力ファイル

```
reports/
└── 00_summary/
    └── full-report.html   # 統合HTMLレポート (約450KB)
```

## 使用例

### 例1: 基本的なコンパイル

```bash
/compile-report
```

### 例2: カスタムタイトルとダークテーマ

```bash
/compile-report --title "My Project Report" --theme dark
```

### 例3: ブラウザで開く

```bash
open reports/00_summary/full-report.html
```

## トラブルシューティング

### Mermaid図が表示されない

1. ブラウザのコンソールでエラーを確認
2. `/fix-mermaid`で構文エラーをチェック
3. 予約語（BOX等）を使用していないか確認

### GraphDBビューアが表示されない

1. `reports/graph/visualizations/graph.html`の存在を確認
2. `/visualize-graph`を実行してファイルを生成

### 日本語が文字化けする

1. HTMLファイルがUTF-8で保存されているか確認
2. ブラウザのエンコーディング設定を確認

## 関連スキル

- `/render-mermaid` - Mermaid図を画像に変換
- `/fix-mermaid` - Mermaid図のシンタックスエラーを修正
- `/visualize-graph` - GraphDBを可視化
- `/build-graph` - GraphDBを構築
