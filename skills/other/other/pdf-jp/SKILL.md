---
name: pdf-jp
description: Generate Japanese PDFs using reportlab or fpdf2 with CJK font embedding, vertical text, business document templates, and inkan image placement. Triggers on requests to create 日本語PDF, 請求書PDF, 領収書PDF, PDF帳票, 縦書きPDF.
---

# 日本語 PDF 生成スキル

## 概要

reportlab または fpdf2 を使用して、日本語のビジネス文書を `.pdf` ファイルとして生成するスキルです。CJK フォントの埋め込み、縦書き対応、印鑑画像の配置、帳票レイアウトなど、日本語 PDF に必要な機能をカバーします。

## 前提条件

```bash
# reportlab を使用する場合
pip install reportlab

# fpdf2 を使用する場合（軽量版）
pip install fpdf2

# 日本語フォント（いずれかをインストール）
# IPAex フォント: https://moji.or.jp/ipafont/
# Noto Sans JP: https://fonts.google.com/noto/specimen/Noto+Sans+JP
```

## 対応フォント

### CJK フォント一覧

| フォント名 | ファイル名 | 特徴 | ライセンス |
|---|---|---|---|
| IPAex明朝 | ipaexm.ttf | 明朝体、ビジネス文書向き | IPA フォントライセンス |
| IPAexゴシック | ipaexg.ttf | ゴシック体、見出し向き | IPA フォントライセンス |
| Noto Sans JP | NotoSansJP-Regular.ttf | ゴシック体、多ウェイト対応 | SIL Open Font License |
| Noto Serif JP | NotoSerifJP-Regular.ttf | 明朝体、多ウェイト対応 | SIL Open Font License |

### reportlab でのフォント登録

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

# フォント登録
pdfmetrics.registerFont(TTFont('IPAexMincho', 'ipaexm.ttf'))
pdfmetrics.registerFont(TTFont('IPAexGothic', 'ipaexg.ttf'))

# Noto Sans JP（複数ウェイト）
pdfmetrics.registerFont(TTFont('NotoSansJP', 'NotoSansJP-Regular.ttf'))
pdfmetrics.registerFont(TTFont('NotoSansJP-Bold', 'NotoSansJP-Bold.ttf'))
```

### fpdf2 でのフォント登録

```python
from fpdf import FPDF

pdf = FPDF()
pdf.add_font('IPAexMincho', '', 'ipaexm.ttf', uni=True)
pdf.add_font('IPAexGothic', '', 'ipaexg.ttf', uni=True)
pdf.set_font('IPAexMincho', size=10)
```

## 用紙サイズと余白

### A4 デフォルト設定

| 項目 | 値 | ポイント |
|---|---|---|
| 用紙幅 | 210mm | 595.28pt |
| 用紙高さ | 297mm | 841.89pt |
| 上余白 | 25mm | 70.87pt |
| 下余白 | 25mm | 70.87pt |
| 左余白 | 25mm | 70.87pt |
| 右余白 | 25mm | 70.87pt |

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

PAGE_WIDTH, PAGE_HEIGHT = A4  # 595.28, 841.89
MARGIN_TOP = 25 * mm
MARGIN_BOTTOM = 25 * mm
MARGIN_LEFT = 25 * mm
MARGIN_RIGHT = 25 * mm

# 印刷可能領域
CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
CONTENT_HEIGHT = PAGE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
```

## reportlab による日本語 PDF 生成

### 基本的な文書作成

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# フォント登録
pdfmetrics.registerFont(TTFont('IPAexMincho', 'ipaexm.ttf'))
pdfmetrics.registerFont(TTFont('IPAexGothic', 'ipaexg.ttf'))

c = canvas.Canvas('output.pdf', pagesize=A4)
width, height = A4

# タイトル
c.setFont('IPAexGothic', 24)
c.drawCentredString(width / 2, height - 40 * mm, '請 求 書')

# 本文
c.setFont('IPAexMincho', 10)
c.drawString(25 * mm, height - 60 * mm, '下記の通りご請求申し上げます。')

c.save()
```

### Platypus（高レベル API）の使用

```python
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

# ドキュメント作成
doc = SimpleDocTemplate(
    'output.pdf',
    pagesize=A4,
    topMargin=25 * mm,
    bottomMargin=25 * mm,
    leftMargin=25 * mm,
    rightMargin=25 * mm,
)

# 日本語スタイル定義
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name='JapaneseTitle',
    fontName='IPAexGothic',
    fontSize=24,
    alignment=1,  # CENTER
    spaceAfter=10 * mm,
))
styles.add(ParagraphStyle(
    name='JapaneseBody',
    fontName='IPAexMincho',
    fontSize=10,
    leading=16,  # 行間
    spaceAfter=3 * mm,
))
styles.add(ParagraphStyle(
    name='JapaneseHeading',
    fontName='IPAexGothic',
    fontSize=14,
    spaceAfter=5 * mm,
    spaceBefore=8 * mm,
))

# コンテンツ構築
elements = []
elements.append(Paragraph('請 求 書', styles['JapaneseTitle']))
elements.append(Spacer(1, 10 * mm))
elements.append(Paragraph('下記の通りご請求申し上げます。', styles['JapaneseBody']))

doc.build(elements)
```

## テーブルの作成

### 明細テーブル

```python
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import mm

# テーブルデータ
data = [
    ['品名', '数量', '単位', '単価', '金額'],
    ['コンサルティング費用', '1', '式', '¥500,000', '¥500,000'],
    ['システム開発費', '1', '式', '¥1,200,000', '¥1,200,000'],
    ['', '', '', '小計', '¥1,700,000'],
    ['', '', '', '消費税（10%）', '¥170,000'],
    ['', '', '', '合計', '¥1,870,000'],
]

# 列幅
col_widths = [60 * mm, 15 * mm, 15 * mm, 25 * mm, 30 * mm]

table = Table(data, colWidths=col_widths)
table.setStyle(TableStyle([
    # フォント
    ('FONTNAME', (0, 0), (-1, -1), 'IPAexMincho'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),

    # ヘッダー行
    ('FONTNAME', (0, 0), (-1, 0), 'IPAexGothic'),
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

    # データ行
    ('ALIGN', (1, 1), (1, -1), 'RIGHT'),  # 数量
    ('ALIGN', (3, 1), (4, -1), 'RIGHT'),  # 単価・金額

    # 罫線
    ('GRID', (0, 0), (-1, -4), 0.5, colors.black),
    ('LINEBELOW', (3, -2), (-1, -2), 0.5, colors.black),
    ('LINEBELOW', (3, -1), (-1, -1), 1.5, colors.black),

    # 合計行を太字に
    ('FONTNAME', (3, -1), (-1, -1), 'IPAexGothic'),
    ('FONTSIZE', (3, -1), (-1, -1), 12),

    # パディング
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))

elements.append(table)
```

## 縦書き PDF

reportlab で縦書きを実現する方法：

```python
def draw_vertical_text(c, text, x, y, font_name='IPAexMincho', font_size=12):
    """縦書きテキストを描画する"""
    c.setFont(font_name, font_size)
    line_height = font_size * 1.5

    for i, char in enumerate(text):
        # 句読点の位置調整
        if char in '、。，．':
            # 縦書き時は右上に移動
            c.drawString(x + font_size * 0.5, y - i * line_height + font_size * 0.3, char)
        elif char in 'ー—':
            # 長音記号は縦向きに
            c.saveState()
            c.translate(x + font_size * 0.5, y - i * line_height - font_size * 0.5)
            c.rotate(90)
            c.drawString(0, 0, char)
            c.restoreState()
        else:
            c.drawString(x, y - i * line_height, char)
```

### 縦書きページ設定

```python
# 縦書きでは横向き用紙を使用することが多い
from reportlab.lib.pagesizes import A4, landscape

c = canvas.Canvas('tategaki.pdf', pagesize=landscape(A4))
width, height = landscape(A4)

# 右から左へ列を配置
col_spacing = 20 * mm
start_x = width - 30 * mm  # 右端から開始
start_y = height - 30 * mm  # 上端から開始

lines = ['吾輩は猫である。', '名前はまだ無い。', 'どこで生れたかとんと見当がつかぬ。']
for i, line in enumerate(lines):
    x = start_x - i * col_spacing
    draw_vertical_text(c, line, x, start_y)
```

## 印鑑画像の配置

```python
from reportlab.lib.units import mm

def add_inkan_image(c, image_path, x, y, size=20*mm):
    """印鑑画像を PDF に配置する"""
    c.drawImage(
        image_path,
        x, y,
        width=size,
        height=size,
        preserveAspectRatio=True,
        mask='auto',  # 透過対応
    )

# 印鑑欄の枠線と画像を描画
def draw_inkan_area(c, x, y, labels=None):
    """印鑑欄（枠線+ラベル+画像スペース）を描画する"""
    if labels is None:
        labels = ['承認', '確認', '担当']

    box_width = 25 * mm
    label_height = 8 * mm
    stamp_height = 25 * mm

    c.setFont('IPAexGothic', 8)

    for i, label in enumerate(labels):
        bx = x + i * box_width

        # ラベル枠
        c.rect(bx, y, box_width, label_height)
        c.drawCentredString(bx + box_width / 2, y + 2 * mm, label)

        # 印鑑スペース枠
        c.rect(bx, y - stamp_height, box_width, stamp_height)
```

## fpdf2 による生成（軽量版）

reportlab の代替として fpdf2 を使用する場合：

```python
from fpdf import FPDF

class JapanesePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('IPAexMincho', '', 'ipaexm.ttf', uni=True)
        self.add_font('IPAexGothic', '', 'ipaexg.ttf', uni=True)

    def header(self):
        self.set_font('IPAexGothic', size=8)
        self.cell(0, 10, '【会社名】', align='R', new_x='LMARGIN', new_y='NEXT')

    def footer(self):
        self.set_y(-15)
        self.set_font('IPAexMincho', size=8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

pdf = JapanesePDF()
pdf.alias_nb_pages()
pdf.add_page()
pdf.set_font('IPAexGothic', size=24)
pdf.cell(0, 20, '請 求 書', align='C', new_x='LMARGIN', new_y='NEXT')
pdf.output('output.pdf')
```

## ビジネス文書テンプレート

### 請求書 PDF

日本のビジネスで使用する請求書を PDF として出力します。

- 参照: [templates/invoice.md](templates/invoice.md)

## 日本語 OCR との連携

生成した PDF を OCR で読み取る場合のヒント：

```bash
# Tesseract OCR で日本語テキストを抽出
tesseract input.pdf output -l jpn pdf

# 日本語 + 英語の混在文書
tesseract input.pdf output -l jpn+eng pdf
```

### OCR 精度を高めるための PDF 生成のコツ

| 項目 | 推奨 | 理由 |
|---|---|---|
| フォントサイズ | 10pt 以上 | 小さい文字は認識率が低下する |
| フォント種別 | ゴシック体 | 明朝体より認識精度が高い |
| 文字間隔 | 標準以上 | 文字が詰まると誤認識が増える |
| 背景 | 白地に黒文字 | コントラストが高いほど精度が上がる |
| 解像度 | 300dpi 以上 | スキャン時の推奨解像度 |

## 生成時の確認事項

PDF を生成する前に、以下をユーザーに確認してください：

1. **文書の種類**: 請求書 / 領収書 / 報告書 / その他
2. **使用ライブラリ**: reportlab（デフォルト）/ fpdf2（軽量版）
3. **フォント**: IPAex明朝（デフォルト）/ IPAexゴシック / Noto Sans JP
4. **文字方向**: 横書き（デフォルト）/ 縦書き
5. **用紙サイズ**: A4（デフォルト）/ B5 / A3
6. **印鑑**: 画像ファイルのパス（ある場合）
7. **パスワード保護**: 必要 / 不要

不明な項目はデフォルト値を使用し、プレースホルダーには `【〇〇】` を使用してください。

## セキュリティ設定

```python
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

c = canvas.Canvas('secure.pdf', pagesize=A4)
c.setEncrypt('user_password', 'owner_password')
# ユーザーパスワード: 閲覧時に要求
# オーナーパスワード: 編集・印刷の制限解除に要求
```

## 出力時の注意事項

- フォントファイル（.ttf）が実行環境に存在することを事前に確認する
- フォントが見つからない場合のフォールバック処理を実装する
- ファイル名: `invoice_20260304.pdf` のように英数字を推奨する
- 大量ページの生成時はメモリ使用量に注意する
