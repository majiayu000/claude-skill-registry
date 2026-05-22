---
name: drawio
description: Create and edit draw.io diagrams in XML format. Use when the user wants to create flowcharts, architecture diagrams, sequence diagrams, or any visual diagrams. Handles XML structure, styling, fonts (Noto Sans JP), arrows, connectors, and PNG export.
---

# Draw.io Diagram Skill

draw.ioファイル（.drawio）をXML形式で直接作成・編集するためのスキル。

## XML基本構造

```xml
<mxfile host="app.diagrams.net" modified="2024-01-01T00:00:00.000Z" agent="Claude" version="21.0.0">
  <diagram name="Page-1" id="page-1">
    <mxGraphModel dx="1000" dy="600" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0" defaultFontFamily="Noto Sans JP">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- 図形要素をここに追加 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## mxCell要素

### 矩形（Rectangle）

```xml
<mxCell id="rect-1" value="ラベル" style="rounded=0;whiteSpace=wrap;html=1;fontFamily=Noto Sans JP;fontSize=18;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry" />
</mxCell>
```

### 角丸矩形（Rounded Rectangle）

```xml
<mxCell id="rounded-1" value="ラベル" style="rounded=1;whiteSpace=wrap;html=1;fontFamily=Noto Sans JP;fontSize=18;arcSize=20;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="60" as="geometry" />
</mxCell>
```

### 楕円（Ellipse）

```xml
<mxCell id="ellipse-1" value="ラベル" style="ellipse;whiteSpace=wrap;html=1;fontFamily=Noto Sans JP;fontSize=18;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="80" as="geometry" />
</mxCell>
```

### ひし形（Diamond）

```xml
<mxCell id="diamond-1" value="条件" style="rhombus;whiteSpace=wrap;html=1;fontFamily=Noto Sans JP;fontSize=18;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="100" height="100" as="geometry" />
</mxCell>
```

### テキスト（Text Only）

```xml
<mxCell id="text-1" value="テキスト" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontFamily=Noto Sans JP;fontSize=18;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="30" as="geometry" />
</mxCell>
```

## 矢印・コネクタ

### 基本の矢印

```xml
<mxCell id="arrow-1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;fontFamily=Noto Sans JP;fontSize=14;" edge="1" parent="1" source="rect-1" target="rect-2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### ラベル付き矢印

```xml
<mxCell id="arrow-2" value="ラベル" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;fontFamily=Noto Sans JP;fontSize=14;" edge="1" parent="1" source="rect-1" target="rect-2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

### 点線矢印

```xml
<mxCell id="arrow-3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;dashed=1;fontFamily=Noto Sans JP;fontSize=14;" edge="1" parent="1" source="rect-1" target="rect-2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

## スタイル設定ガイド

### フォント設定（必須）

1. `mxGraphModel`に`defaultFontFamily="Noto Sans JP"`を設定
2. **すべてのテキスト要素**に`fontFamily=Noto Sans JP;`を明示的に追加

### 推奨設定

| 項目 | 推奨値 | 説明 |
|------|--------|------|
| fontSize | 18 | 標準の1.5倍、視認性向上 |
| 日本語テキスト幅 | 30-40px/文字 | レイアウト計算用 |
| 矢印とラベル間隔 | 20px以上 | 重なり防止 |

### 色設定

```
fillColor=#ffffff;      # 塗りつぶし色
strokeColor=#000000;    # 枠線色
fontColor=#333333;      # 文字色
```

### よく使う色

| 用途 | 色コード |
|------|----------|
| 白背景 | #ffffff |
| 薄い青 | #dae8fc |
| 薄い緑 | #d5e8d4 |
| 薄い黄 | #fff2cc |
| 薄い赤 | #f8cecc |
| 薄いグレー | #f5f5f5 |

## 配置ルール

### XMLの記述順 = 描画順

- **先に書いたものが背面**に配置される
- 矢印は図形より先（XMLの先頭側）に記述して最背面に配置

### 推奨構造

```xml
<root>
  <mxCell id="0" />
  <mxCell id="1" parent="0" />

  <!-- 1. 矢印・コネクタ（最背面） -->
  <mxCell id="arrow-1" ... edge="1" ... />
  <mxCell id="arrow-2" ... edge="1" ... />

  <!-- 2. 図形（中間） -->
  <mxCell id="rect-1" ... vertex="1" ... />
  <mxCell id="rect-2" ... vertex="1" ... />

  <!-- 3. テキストラベル（最前面） -->
  <mxCell id="text-1" ... vertex="1" ... />
</root>
```

## PNG変換

### drawio CLIコマンド

```bash
drawio -x -f png -s 2 -t -o output.png input.drawio
```

| オプション | 説明 |
|------------|------|
| -x | エクスポートモード |
| -f png | PNG形式 |
| -s 2 | 2倍スケール（高解像度） |
| -t | 透明背景 |
| -o | 出力ファイル指定 |

## 検証チェックリスト

作成後、以下を確認：

- [ ] mxGraphModelにdefaultFontFamilyが設定されているか
- [ ] 全テキスト要素にfontFamilyが明示的に設定されているか
- [ ] fontSizeは18px程度か（視認性）
- [ ] 矢印がXMLの先頭側に配置されているか（最背面）
- [ ] 矢印とラベルの間隔は20px以上か
- [ ] 日本語テキストの幅は十分か（30-40px/文字）
- [ ] PNG出力で視覚確認したか

## テンプレート

基本テンプレートは `templates/basic.drawio` を参照。
