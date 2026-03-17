---
name: excel-processor
description: Process Excel files with data manipulation, formula generation, and chart creation. Use when working with spreadsheets or Excel data.
---

# Excel Processor Skill

Excelファイルの作成、編集、解析を行うスキルです。

## 概要

Excelの読み書き、数式、グラフ、スタイル設定を自動化します。

## 主な機能

- **データ読み書き**: セル、行、列の操作
- **数式**: SUM、VLOOKUP等の自動生成
- **グラフ**: 折れ線、棒、円グラフ
- **スタイル**: 色、フォント、罫線
- **条件付き書式**: ルールベースの書式
- **ピボットテーブル**: 集計表作成
- **CSV/JSON変換**: データ変換

## 使用方法

### Python (openpyxl)

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.chart import BarChart, Reference

# 新規作成
wb = Workbook()
ws = wb.active
ws.title = "Sales Data"

# データ入力
ws['A1'] = "Product"
ws['B1'] = "Sales"
ws.append(["iPhone", 1000])
ws.append(["MacBook", 800])

# スタイル設定
ws['A1'].font = Font(bold=True)
ws['A1'].fill = PatternFill(start_color="FFFF00", fill_type="solid")

# グラフ作成
chart = BarChart()
data = Reference(ws, min_col=2, min_row=1, max_row=3)
cats = Reference(ws, min_col=1, min_row=2, max_row=3)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
ws.add_chart(chart, "D1")

wb.save("sales.xlsx")

# 読み込み
wb = load_workbook("sales.xlsx")
ws = wb.active
for row in ws.iter_rows(values_only=True):
    print(row)
```

### JavaScript (ExcelJS)

```javascript
const ExcelJS = require('exceljs');

async function createExcel() {
  const workbook = new ExcelJS.Workbook();
  const worksheet = workbook.addWorksheet('Sales');

  // ヘッダー
  worksheet.columns = [
    { header: 'Product', key: 'product', width: 15 },
    { header: 'Sales', key: 'sales', width: 10 }
  ];

  // データ
  worksheet.addRow({ product: 'iPhone', sales: 1000 });
  worksheet.addRow({ product: 'MacBook', sales: 800 });

  // スタイル
  worksheet.getRow(1).font = { bold: true };
  worksheet.getRow(1).fill = {
    type: 'pattern',
    pattern: 'solid',
    fgColor: { argb: 'FFFFFF00' }
  };

  // 数式
  worksheet.getCell('B4').value = { formula: 'SUM(B2:B3)' };

  await workbook.xlsx.writeFile('sales.xlsx');
}
```

### データ分析 (pandas)

```python
import pandas as pd

# 読み込み
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# 分析
summary = df.groupby('Category')['Sales'].sum()

# 書き込み
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Data', index=False)
    summary.to_excel(writer, sheet_name='Summary')
```

### 高度な機能

```python
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.chart import LineChart, Reference

# データフレームから
import pandas as pd
df = pd.DataFrame({
    'Month': ['Jan', 'Feb', 'Mar'],
    'Sales': [100, 150, 120]
})

wb = Workbook()
ws = wb.active
for r in dataframe_to_rows(df, index=False, header=True):
    ws.append(r)

# 条件付き書式
from openpyxl.formatting.rule import ColorScaleRule
ws.conditional_formatting.add('B2:B4',
    ColorScaleRule(start_type='min', start_color='AA0000',
                   end_type='max', end_color='00AA00'))

# 数式
ws['B5'] = '=AVERAGE(B2:B4)'
ws['B6'] = '=MAX(B2:B4)'

wb.save('advanced.xlsx')
```

## ライブラリ

### Python
- **openpyxl**: .xlsx読み書き
- **xlrd/xlwt**: .xls (旧形式)
- **pandas**: データ分析
- **xlsxwriter**: 高速書き込み

### JavaScript
- **ExcelJS**: 完全機能
- **xlsx**: SheetJS、読み込み特化
- **node-xlsx**: シンプル

### Go
- **excelize**: 高性能

### Java
- **Apache POI**: 標準ライブラリ

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-01-22
