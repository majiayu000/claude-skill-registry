---
name: render-mermaid
description: Mermaidレンダリングエージェント - Mermaid図をPNG/SVG/PDF画像に変換。/render-mermaid [対象パス] で呼び出し。
user_invocable: true
---

# Mermaid Renderer Agent

Mermaid CLI（mmdc）を使用してMermaid図を画像ファイルに変換するエージェントです。

## 目的

このエージェントは以下の機能を提供します：

1. **単一ファイル変換** - `.mmd` ファイルを PNG/SVG/PDF に変換
2. **Markdown内図変換** - Markdown内のMermaid図を画像に抽出・変換
3. **一括変換** - ディレクトリ内の全Mermaid図を一括変換
4. **エラー検出** - シンタックスエラーの検出と報告

## 前提条件

### Mermaid CLI のインストール

```bash
# npm でインストール
npm install -g @mermaid-js/mermaid-cli

# 確認
mmdc --version
```

## 実行プロンプト

あなたはMermaid図を画像に変換する専門家エージェントです。以下の手順で変換を実行してください。

### Step 1: 環境確認

```bash
# mermaid-cli がインストールされているか確認
which mmdc && mmdc --version
```

インストールされていない場合は、ユーザーにインストール方法を案内してください。

### Step 2: 対象ファイルの特定

変換対象を特定します：

```bash
# .mmd ファイルを検索
find [対象パス] -name "*.mmd" -type f

# Markdown内のMermaid図を検索
grep -l "```mermaid" [対象パス]/**/*.md
```

または Serena/Glob ツールを使用：

```
Glob: "**/*.mmd"
Grep: "```mermaid" --glob="*.md"
```

### Step 3: 変換の実行

#### 単一の .mmd ファイルを変換

```bash
# 推奨: PNG と SVG の両方を生成
mmdc -i diagram.mmd -o diagram.png
mmdc -i diagram.mmd -o diagram.svg

# PNG のみ
mmdc -i diagram.mmd -o diagram.png

# SVG のみ
mmdc -i diagram.mmd -o diagram.svg

# PDF に変換
mmdc -i diagram.mmd -o diagram.pdf

# 背景色を指定
mmdc -i diagram.mmd -o diagram.png -b transparent

# テーマを指定（default, forest, dark, neutral）
mmdc -i diagram.mmd -o diagram.png -t dark

# 幅を指定
mmdc -i diagram.mmd -o diagram.png -w 1200

# スケールを指定
mmdc -i diagram.mmd -o diagram.png -s 2
```

#### Markdown ファイル内の Mermaid を変換

```bash
# Markdown内の全Mermaid図を画像に変換し、Markdownを更新
mmdc -i document.md -o document-with-images.md

# 画像の出力ディレクトリを指定
mmdc -i document.md -o document-with-images.md -O ./images/
```

### Step 4: 一括変換

複数ファイルを一括変換する場合：

```bash
# 全 .mmd ファイルを PNG と SVG の両方に変換
for f in $(find . -name "*.mmd"); do
  mmdc -i "$f" -o "${f%.mmd}.png"
  mmdc -i "$f" -o "${f%.mmd}.svg"
done

# 全 Markdown 内の Mermaid を変換（PNG と SVG 両方生成、PNG をリンク）
for f in $(find . -name "*.md" -exec grep -l "mermaid" {} \;); do
  output_dir="$(dirname "$f")/images"
  mkdir -p "$output_dir"
  # PNG を生成してMarkdownにリンク
  mmdc -i "$f" -o "$f" -O "$output_dir/" -e png
  # SVG も同じディレクトリに生成（リンクはPNGのまま）
  for mmd in "$output_dir"/*.png; do
    base="${mmd%.png}"
    mmdc -i "${base}.mmd" -o "${base}.svg" 2>/dev/null || true
  done
done
```

**注意:** デフォルトでPNGとSVGの両方を出力します。Markdown内にはPNGがリンクされます。

### Step 5: 設定ファイルの活用

高度なカスタマイズには設定ファイルを使用：

```bash
# 設定ファイルを指定
mmdc -i diagram.mmd -o diagram.png -c mermaid-config.json
```

**mermaid-config.json の例：**

```json
{
  "theme": "default",
  "themeVariables": {
    "primaryColor": "#5D8AA8",
    "primaryTextColor": "#fff",
    "primaryBorderColor": "#3D6A88",
    "lineColor": "#333",
    "secondaryColor": "#A0C4E4",
    "tertiaryColor": "#E8F4FD"
  },
  "flowchart": {
    "curve": "basis",
    "padding": 20
  },
  "sequence": {
    "diagramMarginX": 50,
    "diagramMarginY": 10,
    "actorMargin": 50,
    "width": 150
  }
}
```

**Puppeteer設定ファイル（puppeteer-config.json）：**

```json
{
  "headless": true,
  "args": ["--no-sandbox", "--disable-setuid-sandbox"]
}
```

```bash
mmdc -i diagram.mmd -o diagram.png -p puppeteer-config.json
```

### Step 6: エラーハンドリング

変換エラーが発生した場合：

1. **シンタックスエラー**
   - `/fix-mermaid` スキルを呼び出してエラーを修正
   - よくあるエラー：引用符の欠落、不正なノードID

2. **Puppeteerエラー**
   - `--no-sandbox` オプションを追加
   - Chromiumがインストールされているか確認

3. **タイムアウトエラー**
   - 大きな図は分割を検討
   - タイムアウト値を増加: `--puppeteerConfigFile` で設定

## コマンドオプション一覧

| オプション | 説明 | デフォルト |
|-----------|------|----------|
| `-i, --input` | 入力ファイル | 必須 |
| `-o, --output` | 出力ファイル | 必須 |
| `-t, --theme` | テーマ（default, forest, dark, neutral） | default |
| `-b, --backgroundColor` | 背景色 | white |
| `-w, --width` | 幅（ピクセル） | 800 |
| `-H, --height` | 高さ（ピクセル） | 自動 |
| `-s, --scale` | スケール倍率 | 1 |
| `-c, --configFile` | Mermaid設定ファイル | - |
| `-p, --puppeteerConfigFile` | Puppeteer設定ファイル | - |
| `-O, --outputDir` | 画像出力ディレクトリ | 入力と同じ |
| `-q, --quiet` | 出力を抑制 | false |

## 使用例

### 例1: リファクタリング成果物の図を変換

```bash
# reports 内の全Markdown図を PNG と SVG で画像化
cd reports
for f in $(find . -name "*.md"); do
  if grep -q "mermaid" "$f"; then
    dir=$(dirname "$f")
    mkdir -p "$dir/images"
    # PNG を生成してMarkdownにリンク
    mmdc -i "$f" -o "$f" -O "$dir/images/" -e png -t default -b transparent
    # SVG も生成（同じディレクトリに出力）
    for mmd in "$dir/images"/*.png; do
      [ -f "$mmd" ] && mmdc -i "${mmd%.png}.mmd" -o "${mmd%.png}.svg" -t default -b transparent 2>/dev/null || true
    done
  fi
done
```

**ポイント:** PNG と SVG の両方を生成し、Markdown には PNG がリンクされます。SVG は同じディレクトリに保存されるため、必要に応じて利用できます。

### 例2: ドメインストーリーを高品質PDFに

```bash
mmdc -i domain-story.mmd -o domain-story.pdf -s 2 -t forest
```

### 例3: ダークモード用の図を生成

```bash
mmdc -i architecture.mmd -o architecture-dark.svg -t dark -b "#1a1a2e"
```

## 出力

変換完了後、以下を報告：

- 変換したファイル数
- 出力形式と保存先（PNG と SVG の両方）
- Markdown内のリンク形式（PNG がリンクされる）
- エラーがあった場合はその内容
- 次のステップの提案（必要に応じて `/fix-mermaid` を推奨）

**出力形式のデフォルト動作:**
- `.mmd` ファイル → PNG と SVG の両方を生成
- Markdown 内の図 → PNG をリンク、SVG も同ディレクトリに生成

## 関連スキル

- `/fix-mermaid` - Mermaid図のシンタックスエラーを修正
- `/create-domain-story` - ドメインストーリーをMermaid形式で作成
