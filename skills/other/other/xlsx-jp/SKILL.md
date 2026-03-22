---
name: xlsx-jp
description: Generate Japanese Excel files (.xlsx) using openpyxl with Japanese fonts, currency formatting (¥), Japanese era calendar (和暦), tax calculation, and business templates. Triggers on requests to create Excel帳票, 見積書Excel, 請求書xlsx, 勤怠管理表, 日本語スプレッドシート.
---

# 日本語 Excel ファイル生成スキル

## 概要

openpyxl を使用して、日本語のビジネス帳票を正しいフォーマットで `.xlsx` ファイルとして生成するスキルです。通貨表示（¥）、和暦、消費税計算、印鑑欄など、日本のビジネス帳票に必要な要素をカバーします。

## 前提条件

```bash
pip install openpyxl
```

## 基本設定

### ワークブック作成と日本語フォント

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill, numbers
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active

# デフォルトフォント設定
default_font = Font(name='游ゴシック', size=10)
ws.sheet_properties.defaultRowHeight = 18
```

### 推奨フォント一覧

| 用途 | フォント名 | 特徴 |
|---|---|---|
| 帳票全般 | 游ゴシック（Yu Gothic） | 視認性が高く帳票向き |
| フォーマルな文書 | 游明朝（Yu Mincho） | 正式な印象 |
| 互換性重視 | MS ゴシック（MS Gothic） | 等幅、古い環境でも表示可 |
| 互換性重視 | MS 明朝（MS Mincho） | 等幅明朝体 |

### フォントサイズの基準

| 要素 | サイズ |
|---|---|
| 帳票タイトル | 18pt〜24pt |
| セクション見出し | 12pt〜14pt |
| データセル | 10pt〜11pt |
| 注釈・備考 | 9pt |

## 通貨フォーマット（¥）

日本円の表示形式を設定します：

```python
from openpyxl.styles.numbers import FORMAT_NUMBER_COMMA_SEPARATED1

# 方法1: ¥記号付き桁区切り
yen_format = '¥#,##0'

# 方法2: マイナス値の表示（赤字）
yen_format_with_negative = '¥#,##0;[Red]-¥#,##0'

# 方法3: 税込・税抜表示用
yen_format_tax_included = '¥#,##0"(税込)"'

# 適用例
cell = ws['E5']
cell.value = 1500000
cell.number_format = yen_format
```

### 数値フォーマット一覧

| フォーマット | 表示例 | 用途 |
|---|---|---|
| `¥#,##0` | ¥1,500,000 | 基本的な金額表示 |
| `¥#,##0;[Red]-¥#,##0` | -¥500 （赤字） | 赤字表示付き |
| `#,##0` | 1,500,000 | 金額（¥なし） |
| `0.0%` | 10.0% | 税率表示 |
| `#,##0.0"時間"` | 160.0時間 | 労働時間 |

## 和暦（日本の年号）対応

```python
from datetime import date

def to_wareki(d):
    """西暦から和暦に変換する"""
    wareki_eras = [
        (date(2019, 5, 1), '令和'),
        (date(1989, 1, 8), '平成'),
        (date(1926, 12, 25), '昭和'),
        (date(1912, 7, 30), '大正'),
    ]
    for start_date, era_name in wareki_eras:
        if d >= start_date:
            year = d.year - start_date.year + 1
            year_str = '元' if year == 1 else str(year)
            return f'{era_name}{year_str}年{d.month}月{d.day}日'
    return f'{d.year}年{d.month}月{d.day}日'

# 使用例
today = date.today()
ws['B3'] = to_wareki(today)  # 例: 令和8年3月4日
```

### Excel セルでの和暦表示

```python
from openpyxl.styles import numbers

cell = ws['B3']
cell.value = date(2026, 3, 4)
cell.number_format = '[$-ja-JP-x-gannen]ggge"年"m"月"d"日"'
# 表示: 令和8年3月4日
```

## 消費税計算

### 標準税率（10%）と軽減税率（8%）

```python
TAX_RATE_STANDARD = 0.10   # 標準税率 10%
TAX_RATE_REDUCED = 0.08    # 軽減税率 8%（食品・新聞等）

def calculate_tax(amount, rate=TAX_RATE_STANDARD):
    """消費税を計算する（端数切り捨て）"""
    import math
    return math.floor(amount * rate)

# Excel数式での計算
ws['F10'] = '=FLOOR(F9*0.1, 1)'   # 標準税率（10%）
ws['F11'] = '=FLOOR(F9*0.08, 1)'  # 軽減税率（8%）
ws['F12'] = '=F9+F10'              # 合計（10%対象）
```

### インボイス制度対応

適格請求書（インボイス）に必要な項目：

| 項目 | 内容 |
|---|---|
| 登録番号 | T + 13桁の数字（例: T1234567890123） |
| 税率ごとの区分 | 10%対象 / 8%対象（軽減税率）を分けて記載 |
| 税率ごとの消費税額 | それぞれの税率に対する消費税額を明記 |

## 印鑑欄の作成

```python
def add_inkan_area(ws, start_row, start_col, labels=None):
    """印鑑欄を作成する"""
    if labels is None:
        labels = ['承認', '確認', '担当']

    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin'),
    )
    center_align = Alignment(horizontal='center', vertical='center')

    for i, label in enumerate(labels):
        col = start_col + i
        # ラベルセル
        cell = ws.cell(row=start_row, column=col, value=label)
        cell.font = Font(name='游ゴシック', size=8)
        cell.alignment = center_align
        cell.border = thin_border

        # 印鑑スペース（下の行を結合して高さを確保）
        stamp_cell = ws.cell(row=start_row + 1, column=col)
        stamp_cell.border = thin_border
        stamp_cell.alignment = center_align

    # 印鑑スペースの行の高さを設定
    ws.row_dimensions[start_row + 1].height = 60
```

## セルスタイルのユーティリティ

### ヘッダー行のスタイル

```python
header_font = Font(name='游ゴシック', size=10, bold=True, color='FFFFFF')
header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
header_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
header_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin'),
)

def apply_header_style(ws, row, start_col, end_col):
    """ヘッダー行にスタイルを適用する"""
    for col in range(start_col, end_col + 1):
        cell = ws.cell(row=row, column=col)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align
        cell.border = header_border
```

### 罫線パターン

```python
# 細い実線（帳票データ行）
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin'),
)

# 太い外枠線（合計行など）
thick_bottom = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thick'),
)

# 二重線（最終合計行の下）
double_bottom = Border(
    bottom=Side(style='double'),
)
```

## ビジネステンプレート

### 見積書

日本のビジネスで使用する標準的な見積書を Excel で作成します。

- 参照: [templates/mitsumori.md](templates/mitsumori.md)

### 勤怠管理表

月次の勤怠管理表（出退勤、休憩、残業時間を管理）を作成します。

- 参照: [templates/kintai.md](templates/kintai.md)

## 印刷設定

```python
from openpyxl.worksheet.page import PageMargins

# 用紙サイズ（A4）
ws.page_setup.paperSize = ws.PAPERSIZE_A4

# 印刷方向（縦）
ws.page_setup.orientation = 'portrait'

# 余白設定（インチ単位）
ws.page_margins = PageMargins(
    left=0.75, right=0.75,
    top=1.0, bottom=1.0,
    header=0.5, footer=0.5,
)

# 1ページに収める
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 1
ws.sheet_properties.pageSetUpPr.fitToPage = True

# ヘッダー・フッター
ws.oddHeader.center.text = '【会社名】'
ws.oddFooter.center.text = 'Page &P of &N'
```

## 生成時の確認事項

帳票を生成する前に、以下をユーザーに確認してください：

1. **帳票の種類**: 見積書 / 請求書 / 勤怠管理表 / その他
2. **フォント**: 游ゴシック（デフォルト）/ 游明朝 / MS ゴシック
3. **日付形式**: 和暦（デフォルト）/ 西暦
4. **消費税率**: 10%（デフォルト）/ 8%（軽減税率）/ 混合
5. **印鑑欄**: 必要（承認・確認・担当）/ 不要 / カスタム
6. **印刷設定**: A4 縦（デフォルト）/ A4 横 / B4 / A3
7. **シート名**: 日本語で指定（例: 「見積書」「勤怠管理」）

不明な項目はデフォルト値を使用し、プレースホルダーには `【〇〇】` を使用してください。

## 出力時の注意事項

- ファイル名は英数字を推奨: `mitsumori_20260304.xlsx`
- シート名は日本語可: `ws.title = '見積書'`
- 列幅は内容に応じて適切に調整する
- 数式を使用する場合、保存後に Excel で再計算が必要な場合がある
- `wb.save('filename.xlsx')` で保存する
