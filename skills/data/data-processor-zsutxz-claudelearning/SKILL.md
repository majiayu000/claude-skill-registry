---
name： 爬虫数据处理
description： 清洗爬虫数据并生成Excel报表。处理JSON/CSV格式的爬虫数据，去重、格式化、生成统计报表时使用。
---

# 爬虫数据处理

## 处理流程

1. 读取JSON/CSV格式的原始数据
2. 数据清洗：去重、填充缺失值、格式标准化
3. 统计分析：计数、去重率、异常检测
4. 生成Excel报表(包含数据和图表)

## 脚本功能

### scripts/process.py

主处理脚本：
```python
import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart

def clean_data(df):
    # 去重
    df = df.drop_duplicates()
    # 填充缺失值
    df = df.fillna('')
    # 标准化格式
    df['price'] = df['price'].astype(float)
    return df

def generate_report(df， output_file):
    # 生成Excel
    with pd.ExcelWriter(output_file， engine='openpyxl') as writer:
        df.to_excel(writer， sheet_name='数据'， index=False)
        
        # 添加统计
        stats = df.describe()
        stats.to_excel(writer， sheet_name='统计')
        
        # 添加图表
        wb = writer.book
        ws = wb['统计']
        chart = BarChart()
        # ...图表配置
```

### scripts/dedupe.py

快速去重工具：
```python
import json

def dedupe_json(file_path， key_field):
    with open(file_path) as f:
        data = json.load(f)
    
    seen = set()
    unique_data = []
    
    for item in data:
        key = item.get(key_field)
        if key and key not in seen:
            seen.add(key)
            unique_data.append(item)
    
    return unique_data
```

## 使用示例

处理JSON数据：
运行 python scripts/process.py data.json --output report.xlsx

快速去重：
运行 python scripts/dedupe.py data.json --key url

## 输出说明

生成的Excel包含：
- 数据sheet：清洗后的完整数据
- 统计sheet：数量、去重率、价格分布等
- 图表sheet：可视化统计结果