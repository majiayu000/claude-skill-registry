---
name: xlsx
description: "全面的电子表格创建、编辑和分析功能，支持公式、格式、数据分析和可视化。当 Claude 需要处理电子表格（.xlsx、.xlsm、.csv、.tsv 等）时使用，包括：(1) 创建带有公式和格式的新电子表格，(2) 读取或分析数据，(3) 修改现有电子表格同时保留公式，(4) 电子表格中的数据分析和可视化，或 (5) 重新计算公式"
license: Proprietary. LICENSE.txt has complete terms
---

# 输出要求

## 所有 Excel 文件

### 零公式错误
- 每个 Excel 模型必须以零公式错误交付（#REF!、#DIV/0!、#VALUE!、#N/A、#NAME?）

### 保留现有模板（更新模板时）
- 修改文件时研究并完全匹配现有格式、样式和约定
- 绝不对具有既定模式的文件强加标准化格式
- 现有模板约定始终覆盖这些指南

## 财务模型

### 颜色编码标准
除非用户或现有模板另有说明

#### 行业标准颜色约定
- **蓝色文本 (RGB: 0,0,255)**：硬编码输入，以及用户将为场景更改的数字
- **黑色文本 (RGB: 0,0,0)**：所有公式和计算
- **绿色文本 (RGB: 0,128,0)**：从同一工作簿中的其他工作表提取的链接
- **红色文本 (RGB: 255,0,0)**：到其他文件的外部链接
- **黄色背景 (RGB: 255,255,0)**：需要注意的关键假设或需要更新的单元格

### 数字格式标准

#### 必需的格式规则
- **年份**：格式化为文本字符串（例如，"2024" 而不是 "2,024"）
- **货币**：使用 $#,##0 格式；始终在标题中指定单位（"收入（百万美元）"）
- **零**：使用数字格式使所有零为 "-"，包括百分比（例如，"$#,##0;($#,##0);-"）
- **百分比**：默认为 0.0% 格式（一位小数）
- **倍数**：格式化为 0.0x 用于估值倍数（EV/EBITDA、P/E）
- **负数**：使用括号 (123) 而不是减号 -123

### 公式构建规则

#### 假设放置
- 将所有假设（增长率、利润率、倍数等）放在单独的假设单元格中
- 在公式中使用单元格引用而不是硬编码值
- 示例：使用 =B5*(1+$B$6) 而不是 =B5*1.05

#### 公式错误预防
- 验证所有单元格引用是否正确
- 检查范围中的偏移一个错误
- 确保所有预测期间的公式一致
- 使用边缘案例测试（零值、负数）
- 验证没有意外的循环引用

#### 硬编码的文档要求
- 在单元格旁边（如果是表格末尾）注释或说明。格式："来源：[系统/文档]、[日期]、[具体参考]、[URL（如果适用）]"
- 示例：
  - "来源：公司 10-K，2024 财年，第 45 页，收入说明，[SEC EDGAR URL]"
  - "来源：公司 10-Q，2025 年第二季度，附件 99.1，[SEC EDGAR URL]"
  - "来源：彭博终端，2025/8/15，AAPL US Equity"
  - "来源：FactSet，2025/8/20，共识估计屏幕"

# XLSX 创建、编辑和分析

## 概述

用户可能会要求您创建、编辑或分析 .xlsx 文件的内容。您有不同的工具和工作流程可用于不同的任务。

## 重要要求

**LibreOffice 用于公式重新计算是必需的**：您可以假设已安装 LibreOffice，以使用 `recalc.py` 脚本重新计算公式值。脚本在首次运行时自动配置 LibreOffice

## 读取和分析数据

### 使用 pandas 进行数据分析
对于数据分析、可视化和基本操作，使用 **pandas**，它提供强大的数据操作功能：

```python
import pandas as pd

# 读取 Excel
df = pd.read_excel('file.xlsx')  # 默认：第一个工作表
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # 所有工作表作为字典

# 分析
df.head()      # 预览数据
df.info()      # 列信息
df.describe()  # 统计

# 写入 Excel
df.to_excel('output.xlsx', index=False)
```

## Excel 文件工作流程

## 关键：使用公式，而非硬编码值

**始终使用 Excel 公式而不是在 Python 中计算值并硬编码它们。** 这确保电子表格保持动态和可更新。

### ❌ 错误 - 硬编码计算值
```python
# 不好：在 Python 中计算并硬编码结果
total = df['Sales'].sum()
sheet['B10'] = total  # 硬编码 5000

# 不好：在 Python 中计算增长率
growth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']
sheet['C5'] = growth  # 硬编码 0.15

# 不好：Python 计算平均值
avg = sum(values) / len(values)
sheet['D20'] = avg  # 硬编码 42.5
```

### ✅ 正确 - 使用 Excel 公式
```python
# 好：让 Excel 计算总和
sheet['B10'] = '=SUM(B2:B9)'

# 好：增长率作为 Excel 公式
sheet['C5'] = '=(C4-C2)/C2'

# 好：使用 Excel 函数的平均值
sheet['D20'] = '=AVERAGE(D2:D19)'
```

这适用于所有计算 - 总计、百分比、比率、差值等。电子表格应该能够在源数据更改时重新计算。

## 常见工作流程
1. **选择工具**：pandas 用于数据，openpyxl 用于公式/格式
2. **创建/加载**：创建新工作簿或加载现有文件
3. **修改**：添加/编辑数据、公式和格式
4. **保存**：写入文件
5. **重新计算公式（如果使用公式则必需）**：使用 recalc.py 脚本
   ```bash
   python recalc.py output.xlsx
   ```
6. **验证并修复任何错误**：
   - 脚本返回带有错误详细信息的 JSON
   - 如果 `status` 为 `errors_found`，检查 `error_summary` 以获取特定错误类型和位置
   - 修复识别的错误并再次重新计算
   - 要修复的常见错误：
     - `#REF!`：无效的单元格引用
     - `#DIV/0!`：除以零
     - `#VALUE!`：公式中的错误数据类型
     - `#NAME?`：无法识别的公式名称

### 创建新 Excel 文件

```python
# 使用 openpyxl 处理公式和格式
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# 添加数据
sheet['A1'] = 'Hello'
sheet['B1'] = 'World'
sheet.append(['Row', 'of', 'data'])

# 添加公式
sheet['B2'] = '=SUM(A1:A10)'

# 格式
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

# 列宽
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

### 编辑现有 Excel 文件

```python
# 使用 openpyxl 保留公式和格式
from openpyxl import load_workbook

# 加载现有文件
wb = load_workbook('existing.xlsx')
sheet = wb.active  # 或 wb['SheetName'] 用于特定工作表

# 使用多个工作表
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"工作表：{sheet_name}")

# 修改单元格
sheet['A1'] = '新值'
sheet.insert_rows(2)  # 在位置 2 插入行
sheet.delete_cols(3)  # 删除列 3

# 添加新工作表
new_sheet = wb.create_sheet('NewSheet')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
```

## 重新计算公式

由 openpyxl 创建或修改的 Excel 文件包含字符串形式的公式，但不包含计算值。使用提供的 `recalc.py` 脚本重新计算公式：

```bash
python recalc.py <excel_file> [timeout_seconds]
```

示例：
```bash
python recalc.py output.xlsx 30
```

脚本：
- 首次运行时自动设置 LibreOffice 宏
- 重新计算所有工作表中的所有公式
- 扫描所有单元格以查找 Excel 错误（#REF!、#DIV/0! 等）
- 返回带有详细错误位置和计数的 JSON
- 在 Linux 和 macOS 上均可工作

## 公式验证检查清单

快速检查以确保公式正常工作：

### 基本验证
- [ ] **测试 2-3 个示例引用**：在构建完整模型之前验证它们提取正确的值
- [ ] **列映射**：确认 Excel 列匹配（例如，列 64 = BL，不是 BK）
- [ ] **行偏移**：记住 Excel 行是 1 索引的（DataFrame 行 5 = Excel 行 6）

### 常见陷阱
- [ ] **NaN 处理**：使用 `pd.notna()` 检查空值
- [ ] **最右侧列**：FY 数据通常在 50+ 列
- [ ] **多个匹配**：搜索所有出现，而不仅仅是第一个
- [ ] **除以零**：在公式中使用 `/` 之前检查分母（#DIV/0!）
- [ ] **错误引用**：验证所有单元格引用指向预期的单元格（#REF!）
- [ ] **跨工作表引用**：使用正确格式（Sheet1!A1）链接工作表

### 公式测试策略
- [ ] **从小处开始**：在广泛应用之前在 2-3 个单元格上测试公式
- [ ] **验证依赖项**：检查公式中引用的所有单元格是否存在
- [ ] **测试边缘案例**：包括零、负数和非常大的值

### 解释 recalc.py 输出
脚本返回带有错误详细信息的 JSON：
```json
{
  "status": "success",           // 或 "errors_found"
  "total_errors": 0,              // 总错误计数
  "total_formulas": 42,           // 文件中的公式数量
  "error_summary": {              // 仅在发现错误时出现
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

## 最佳实践

### 库选择
- **pandas**：最适合数据分析、批量操作和简单数据导出
- **openpyxl**：最适合复杂格式、公式和 Excel 特定功能

### 使用 openpyxl
- 单元格索引是 1 基的（row=1，column=1 指单元格 A1）
- 使用 `data_only=True` 读取计算值：`load_workbook('file.xlsx', data_only=True)`
- **警告**：如果使用 `data_only=True` 打开并保存，公式将被值替换并永久丢失
- 对于大文件：使用 `read_only=True` 进行读取或 `write_only=True` 进行写入
- 公式被保留但不被评估 - 使用 recalc.py 更新值

### 使用 pandas
- 指定数据类型以避免推断问题：`pd.read_excel('file.xlsx', dtype={'id': str})`
- 对于大文件，读取特定列：`pd.read_excel('file.xlsx', usecols=['A', 'C', 'E'])`
- 正确处理日期：`pd.read_excel('file.xlsx', parse_dates=['date_column'])`

## 代码风格指南
**重要**：为 Excel 操作生成 Python 代码时：
- 编写最少、简洁的 Python 代码，无不必要的注释
- 避免冗长的变量名和冗余操作
- 避免不必要的 print 语句

**对于 Excel 文件本身**：
- 为具有复杂公式或重要假设的单元格添加注释
- 记录硬编码值的数据源
- 包含关键计算和模型部分的说明
