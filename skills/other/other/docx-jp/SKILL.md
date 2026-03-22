---
name: docx-jp
description: Generate Japanese Word documents (.docx) using python-docx with proper Japanese fonts, vertical writing (縦書き), ruby text (ふりがな), and business templates. Triggers on requests to create Word文書, 見積書docx, 請求書docx, 日本語Word, 縦書き文書, ビジネス文書Word.
---

# 日本語 Word 文書生成スキル

## 概要

python-docx を使用して、日本語のビジネス文書を正しいフォーマットで `.docx` ファイルとして生成するスキルです。日本語フォント設定、縦書き対応、ルビ（ふりがな）、禁則処理、印鑑欄など、日本のビジネス文書に必要な要素をすべてカバーします。

## 前提条件

```bash
pip install python-docx lxml
```

## 用紙・余白のデフォルト設定

すべての文書は以下のデフォルト設定で生成してください：

| 項目 | 値 |
|---|---|
| 用紙サイズ | A4（210mm x 297mm） |
| 上余白 | 25.4mm（1インチ） |
| 下余白 | 25.4mm（1インチ） |
| 左余白 | 31.75mm（1.25インチ） |
| 右余白 | 31.75mm（1.25インチ） |
| 文字方向 | 横書き（デフォルト） |

```python
from docx.shared import Mm

section = document.sections[0]
section.page_width = Mm(210)
section.page_height = Mm(297)
section.top_margin = Mm(25.4)
section.bottom_margin = Mm(25.4)
section.left_margin = Mm(31.75)
section.right_margin = Mm(31.75)
```

## 日本語フォント設定

### 推奨フォント一覧

| 用途 | フォント名 | 分類 |
|---|---|---|
| 本文（ゴシック体） | 游ゴシック / Yu Gothic | ゴシック |
| 本文（明朝体） | 游明朝 / Yu Mincho | 明朝 |
| 互換用（明朝体） | MS 明朝 / MS Mincho | 明朝 |
| 互換用（ゴシック体） | MS ゴシック / MS Gothic | ゴシック |
| ビジネス文書推奨 | 游明朝 | 明朝 |

### フォント設定の実装

```python
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn

document = Document()

# デフォルトフォントの設定
style = document.styles['Normal']
font = style.font
font.name = 'Yu Mincho'  # 英数字用
font.size = Pt(10.5)     # 日本語文書の標準サイズ

# 日本語フォントの設定（rFonts の eastAsia 属性）
rPr = style.element.rPr
if rPr is None:
    rPr = style.element.makeelement(qn('w:rPr'), {})
    style.element.append(rPr)
rFonts = rPr.makeelement(qn('w:rFonts'), {})
rFonts.set(qn('w:eastAsia'), '游明朝')
rPr.append(rFonts)
```

### フォントサイズの基準

| 要素 | サイズ |
|---|---|
| 表題（タイトル） | 18pt〜24pt |
| 見出し1 | 14pt〜16pt |
| 見出し2 | 12pt〜14pt |
| 本文 | 10.5pt（標準） |
| 注釈・補足 | 9pt |
| フッター | 8pt〜9pt |

## 縦書き（縦書き文書）対応

縦書き文書を生成する場合、セクションのテキスト方向を変更します：

```python
from docx.oxml.ns import qn
from lxml import etree

section = document.sections[0]
sectPr = section._sectPr

# テキスト方向を縦書きに設定
textDirection = sectPr.makeelement(qn('w:textDirection'), {})
textDirection.set(qn('w:val'), 'tbRl')  # Top-to-Bottom, Right-to-Left
sectPr.append(textDirection)
```

**注意事項**:
- 縦書き時は用紙を横向き（landscape）に設定することが多い
- 数字やアルファベットは縦中横（tatenakayoko）を検討する
- 句読点の位置が変わるため、禁則処理が重要になる

## ルビ（ふりがな）の設定

python-docx には直接ルビを設定する API がないため、XML を直接操作します：

```python
from docx.oxml.ns import qn
from lxml import etree

def add_ruby(paragraph, base_text, ruby_text, font_name='游明朝', base_size=21, ruby_size=10):
    """ルビ付きテキストを段落に追加する"""
    ruby_elem = paragraph._element.makeelement(qn('w:r'), {})

    ruby_xml = f'''
    <w:ruby xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
        <w:rubyPr>
            <w:rubyAlign w:val="distributeSpace"/>
            <w:hps w:val="{ruby_size}"/>
            <w:hpsRaise w:val="{base_size + 2}"/>
            <w:hpsBaseText w:val="{base_size}"/>
            <w:lid w:val="ja-JP"/>
        </w:rubyPr>
        <w:rt>
            <w:r>
                <w:rPr>
                    <w:rFonts w:eastAsia="{font_name}"/>
                    <w:sz w:val="{ruby_size}"/>
                </w:rPr>
                <w:t>{ruby_text}</w:t>
            </w:r>
        </w:rt>
        <w:rubyBase>
            <w:r>
                <w:rPr>
                    <w:rFonts w:eastAsia="{font_name}"/>
                    <w:sz w:val="{base_size}"/>
                </w:rPr>
                <w:t>{base_text}</w:t>
            </w:r>
        </w:rubyBase>
    </w:ruby>
    '''
    ruby_element = etree.fromstring(ruby_xml)
    ruby_elem.append(ruby_element)
    paragraph._element.append(ruby_elem)
```

## 禁則処理

Word 文書での日本語禁則処理を適切に設定します：

```python
# 段落に禁則処理を設定
pPr = paragraph._element.get_or_add_pPr()
kinsoku = pPr.makeelement(qn('w:kinsoku'), {})
kinsoku.set(qn('w:val'), '1')  # 禁則処理を有効化
pPr.append(kinsoku)

# ワードラップ設定
wordWrap = pPr.makeelement(qn('w:wordWrap'), {})
wordWrap.set(qn('w:val'), '0')  # 日本語の文字単位で折り返す
pPr.append(wordWrap)
```

### 禁則文字

| 種別 | 文字 |
|---|---|
| 行頭禁則 | 、。，．・：；？！）」』】〉》〕｝ー |
| 行末禁則 | （「『【〈《〔｛ |

## 印鑑欄（ハンコ欄）の作成

ビジネス文書に必要な印鑑欄をテーブルで作成します：

```python
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def add_inkan_table(document, labels=None):
    """印鑑欄を追加する（右寄せの3マス表）"""
    if labels is None:
        labels = ['承認', '確認', '担当']

    table = document.add_table(rows=2, cols=len(labels))
    table.alignment = WD_TABLE_ALIGNMENT.RIGHT

    for i, label in enumerate(labels):
        # ラベル行
        cell = table.cell(0, i)
        cell.text = label
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        cell.width = Cm(2.5)

        # 印鑑スペース行（空白、高さで印鑑サイズを表現）
        cell = table.cell(1, i)
        cell.text = ''
        cell.height = Cm(2.5)

    return table
```

## ビジネス文書テンプレート

### 見積書

日本のビジネスで使用する標準的な見積書フォーマットです。

- 参照: [templates/mitsumori.md](templates/mitsumori.md)

### 請求書

支払いを依頼するための請求書フォーマットです。

- 参照: [templates/seikyusho.md](templates/seikyusho.md)

## テーブルスタイル設定

日本語ビジネス文書のテーブルには以下のスタイルを適用してください：

```python
from docx.shared import Pt, Cm, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT

def style_business_table(table):
    """ビジネス文書用テーブルスタイルを適用"""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                paragraph.style.font.size = Pt(10)
                paragraph.style.font.name = 'Yu Mincho'

    # ヘッダー行の背景色を設定
    for cell in table.rows[0].cells:
        shading = cell._element.makeelement(qn('w:shd'), {
            qn('w:fill'): 'D9E2F3',
            qn('w:val'): 'clear'
        })
        cell._element.get_or_add_tcPr().append(shading)
```

## 生成時の確認事項

文書を生成する前に、以下をユーザーに確認してください：

1. **文書の種類**: 見積書 / 請求書 / 報告書 / その他
2. **文字方向**: 横書き（デフォルト）/ 縦書き
3. **フォント**: 游明朝（デフォルト）/ 游ゴシック / MS 明朝
4. **フォントサイズ**: 10.5pt（デフォルト）
5. **印鑑欄**: 必要（承認・確認・担当）/ 不要 / カスタム
6. **ルビ**: 必要な箇所があるか
7. **用紙サイズ**: A4（デフォルト）/ B5 / その他

不明な項目はデフォルト値を使用し、プレースホルダーには `【〇〇】` を使用してください。

## 出力時の注意事項

- ファイル名には日本語を使用可能だが、互換性のため英数字を推奨する
- 例: `mitsumori_20260304.docx`（`見積書_20260304.docx` も可）
- 生成後に `document.save('filename.docx')` で保存する
- python-docx はテンプレート `.docx` からの読み込みにも対応している
