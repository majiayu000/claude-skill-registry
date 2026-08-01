---
name: backend-data-processor
description: Process vehicle insurance Excel data using Pandas - file handling, data
  cleaning, merging, validation. Use when processing Excel/CSV files, handling data
  imports, implementing business rules (negative
---

---
name: backend-data-processor
description: Process vehicle insurance Excel data using Pandas - file handling, data cleaning, merging, validation. Use when processing Excel/CSV files, handling data imports, implementing business rules (negative premiums, zero commissions), debugging data pipelines, or optimizing Pandas performance. Keywords: data_processor.py, Excel, CSV, Pandas, merge, deduplication, date normalization.
allowed-tools: Read, Edit, Grep, Glob
---

# Backend Data Processor - 车险数据处理后端实现指南

**版本**: v1.0
**最后更新**: 2025-11-08
**适用场景**: Excel 数据处理、数据清洗、文件合并、数据验证

---

## 📌 Skill 概述

本 Skill 提供车险签单数据处理后端的完整实现指南,作为 `analyzing-auto-insurance-data` Skill 的后端补充。涵盖数据流转、核心处理逻辑、业务规则实现、性能优化和错误处理。

**核心价值**:
- ✅ **数据流转架构**: Excel → CSV → 合并 → 存储全流程
- ✅ **核心处理函数**: 4个关键方法详解(文件处理/清洗/合并/批量扫描)
- ✅ **业务规则实现**: 负保费/零手续费/日期标准化/缺失值填充
- ✅ **性能优化技巧**: Pandas 最佳实践、内存管理、大文件处理
- ✅ **错误处理与日志**: 异常捕获机制、日志标准、用户友好提示

**关键文件位置**:
- [backend/data_processor.py](../../backend/data_processor.py) - 数据处理核心
- [backend/api_server.py](../../backend/api_server.py) - Flask API 服务

---

## 📊 一、数据流转架构

### 1.1 整体流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                       Excel 文件上传到 data/ 目录                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  scan_and_process_new_files()                                   │
│  - 扫描 data/*.xlsx, data/*.xls                                  │
│  - 批量处理所有新文件                                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
         ┌───────────────────────────────────────┐
         │  process_new_excel(excel_path)        │
         │  - 读取 Excel 文件 (pd.read_excel)     │
         │  - 返回原始 DataFrame                  │
         └───────────────┬───────────────────────┘
                         │
                         ▼
         ┌───────────────────────────────────────┐
         │  _clean_data(df)                      │
         │  - 删除空行                            │
         │  - 日期格式标准化                       │
         │  - 数值类型转换                         │
         │  - 缺失值填充为空字符串                  │
         └───────────────┬───────────────────────┘
                         │
                         ▼
         ┌───────────────────────────────────────┐
         │  merge_with_existing(new_df)          │
         │  - 读取现有 CSV (如存在)                │
         │  - pd.concat() 合并新旧数据             │
         │  - 根据保单号+投保确认时间去重           │
         └───────────────┬───────────────────────┘
                         │
                         ▼
         ┌───────────────────────────────────────┐
         │  save_merged_data(df)                 │
         │  - 保存为 车险清单_2025年10-11月_合并.csv │
         │  - 编码: utf-8-sig (支持Excel打开)     │
         └───────────────┬───────────────────────┘
                         │
                         ▼
         ┌───────────────────────────────────────┐
         │  移动到 data/processed/ 目录            │
         │  - 重命名: 原文件名_processed_时间戳.xlsx │
         │  - 避免重复处理                         │
         └───────────────────────────────────────┘
```

### 1.2 文件命名与版本管理

**输入文件命名规范**:
- 格式: `data/*.xlsx` 或 `data/*.xls`
- 示例: `车险清单_2025年10月.xlsx`

**处理后文件命名**:
- 格式: `data/processed/{原文件名}_processed_{YYYYMMDD_HHMMSS}.xlsx`
- 示例: `data/processed/车险清单_2025年10月_processed_20251108_143025.xlsx`

**合并文件命名**:
- 固定文件名: `车险清单_2025年10-11月_合并.csv`
- 位置: 项目根目录
- 编码: `utf-8-sig` (带 BOM,Excel 可直接打开)

### 1.3 增量更新策略

**去重逻辑** ([data_processor.py:172-177](../../backend/data_processor.py#L172-L177)):
```python
# 根据保单号和投保确认时间去重,保留最新记录
merged_df = merged_df.drop_duplicates(
    subset=['保单号', '投保确认时间'],
    keep='last'
)
```

**为什么选择这两个字段**:
- `保单号`: 业务唯一标识
- `投保确认时间`: 同一保单可能有批改记录,需要保留时间维度

**`keep='last'` 的原因**:
- 批改操作会更新保单信息,最新记录更准确
- 合并时新数据在后,`keep='last'` 优先保留新数据

---

## 🔧 二、核心处理函数详解

### 2.1 `process_new_excel(excel_path)` - Excel 文件处理

**位置**: [data_processor.py:107-127](../../backend/data_processor.py#L107-L127)

**功能**: 读取 Excel 文件并返回清洗后的 DataFrame

**实现细节**:
```python
def process_new_excel(self, excel_path):
    print(f"正在处理Excel文件: {excel_path}")

    # 读取 Excel 文件
    df = pd.read_excel(excel_path)

    print(f"  读取成功: {len(df)} 行, {len(df.columns)} 列")

    # 数据清洗
    df = self._clean_data(df)

    return df
```

**注意事项**:
- ❌ **不要使用** `pd.read_excel(excel_path, dtype=str)` - 会导致数值计算失败
- ✅ **推荐**: 让 Pandas 自动推断类型,后续在 `_clean_data()` 中转换
- ✅ **异常处理**: 调用方 `scan_and_process_new_files()` 已处理异常

**常见问题**:
1. **Excel 文件损坏**: 会抛出 `xlrd.biffh.XLRDError`
2. **文件被占用**: Windows 下可能抛出 `PermissionError`
3. **内存不足**: 大文件(>100MB)可能触发 `MemoryError`

---

### 2.2 `_clean_data(df)` - 数据清洗

**位置**: [data_processor.py:129-153](../../backend/data_processor.py#L129-L153)

**功能**: 标准化数据格式,确保符合 CSV 规范

**清洗步骤**:

#### 步骤 1: 删除完全为空的行
```python
df = df.dropna(how='all')
```
- 移除 Excel 中的空白行
- 避免后续计算时出现 NaN 值污染

#### 步骤 2: 日期格式标准化
```python
date_columns = ['刷新时间', '投保确认时间', '保险起期']
for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
```
- `errors='coerce'`: 无法解析的日期转为 `NaT` (Not a Time)
- 支持多种日期格式: `2025-11-08`, `2025/11/08`, `20251108` 等

**常见日期问题**:
- Excel 日期序列号: `44500` → 自动转换为 `2021-10-15`
- 文本日期: `"2025年11月8日"` → `errors='coerce'` 会转为 `NaT`
- 空值: 保留为 `NaT`,后续填充为空字符串

#### 步骤 3: 数值类型转换
```python
numeric_columns = ['签单/批改保费', '签单数量', '手续费', '手续费含税', '增值税']
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
```
- `errors='coerce'`: 无法解析的数值转为 `NaN`
- 自动处理: `"1,234.56"` → `1234.56` (移除千分位逗号)

**常见数值问题**:
- 负保费: `-5000.00` (退保/批改) → 保留负数,不做修改
- 零手续费: `0.00` → 合法值,不做修改
- 文本数值: `"五万"` → 转为 `NaN`

#### 步骤 4: 缺失值填充
```python
df = df.fillna('')
```
- 将所有 `NaN` / `NaT` 填充为空字符串 `''`
- 避免 JSON 序列化时出现 `null` 值
- 前端可统一判断 `value === ''` 来识别缺失

**⚠️ 重要**: 日期列在此步骤会被转为空字符串,需要在后续查询时重新转换:
```python
df['投保确认时间'] = pd.to_datetime(df['投保确认时间'], errors='coerce')
```

---

### 2.3 `merge_with_existing(new_df)` - 数据合并

**位置**: [data_processor.py:155-184](../../backend/data_processor.py#L155-L184)

**功能**: 将新数据与现有 CSV 合并,去重并统计

**实现细节**:
```python
def merge_with_existing(self, new_df):
    if self.merged_csv.exists():
        print(f"读取现有数据: {self.merged_csv}")
        existing_df = pd.read_csv(self.merged_csv, encoding='utf-8-sig')

        # 合并数据
        merged_df = pd.concat([existing_df, new_df], ignore_index=True)

        # 去重 - 根据保单号和投保确认时间
        if '保单号' in merged_df.columns and '投保确认时间' in merged_df.columns:
            merged_df = merged_df.drop_duplicates(
                subset=['保单号', '投保确认时间'],
                keep='last'
            )

        print(f"  合并完成: {len(existing_df)} + {len(new_df)} = {len(merged_df)} 行")
    else:
        print(f"  未找到现有数据,创建新文件")
        merged_df = new_df

    return merged_df
```

**关键参数解析**:
- `encoding='utf-8-sig'`: 读取带 BOM 的 UTF-8 文件
- `ignore_index=True`: 重新生成 0-N 的连续索引
- `keep='last'`: 保留重复记录中的最后一条

**性能优化建议**:
```python
# ❌ 不推荐: 逐行追加(O(n²) 复杂度)
for _, row in new_df.iterrows():
    existing_df = existing_df.append(row)

# ✅ 推荐: 一次性合并(O(n) 复杂度)
merged_df = pd.concat([existing_df, new_df], ignore_index=True)
```

**内存优化**:
- 大文件(>1GB)可使用 `pd.read_csv(chunksize=10000)` 分块读取
- 合并后立即删除中间变量: `del existing_df, new_df`

---

### 2.4 `scan_and_process_new_files()` - 批量处理

**位置**: [data_processor.py:191-237](../../backend/data_processor.py#L191-L237)

**功能**: 扫描 data 目录,批量处理所有新 Excel 文件

**实现流程**:

#### 步骤 1: 扫描目录
```python
excel_files = list(self.data_dir.glob('*.xlsx')) + list(self.data_dir.glob('*.xls'))
```
- 使用 `pathlib.Path.glob()` 查找文件
- 支持 `.xlsx` 和 `.xls` 两种格式

#### 步骤 2: 批量处理
```python
all_new_data = []
for excel_file in excel_files:
    try:
        # 处理单个文件
        df = self.process_new_excel(excel_file)
        all_new_data.append(df)

        # 处理完成后移动到已处理目录
        processed_dir = self.data_dir / 'processed'
        processed_dir.mkdir(exist_ok=True)

        new_path = processed_dir / f"{excel_file.stem}_processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}{excel_file.suffix}"
        excel_file.rename(new_path)
        print(f"  文件已移动: {new_path}")

    except Exception as e:
        print(f"  处理失败: {e}")
```

**异常处理策略**:
- ✅ **单文件失败不中断**: 使用 `try-except` 捕获单文件异常
- ✅ **记录错误信息**: `print(f"处理失败: {e}")`
- ✅ **继续处理下一个**: 不抛出异常,保证其他文件正常处理

#### 步骤 3: 合并与保存
```python
if all_new_data:
    # 合并所有新数据
    combined_new = pd.concat(all_new_data, ignore_index=True)

    # 与现有数据合并
    final_df = self.merge_with_existing(combined_new)

    # 保存
    self.save_merged_data(final_df)

    print(f"数据更新完成!")
```

**触发方式**:
1. **手动触发**: `python backend/data_processor.py`
2. **API 触发**: `POST /api/refresh` (见 [api_server.py:21-37](../../backend/api_server.py#L21-L37))
3. **定时任务**: 可配置 cron 定时执行

---

## 🎯 三、业务规则实现

### 3.1 负保费处理(退保/批改)

**业务场景**:
- 退保: `签单/批改保费 < 0` (例如: `-5000.00`)
- 批改减保: 部分退保导致保费为负

**处理策略**:
```python
# ✅ 保留负数,不做修改
df[col] = pd.to_numeric(df[col], errors='coerce')
```

**查询时的处理**:
- **保费统计**: 直接 `sum()`,负数会自动抵消正数
- **保单件数**: 需要过滤 `>= 50` 的记录(见 [data_processor.py:507-509](../../backend/data_processor.py#L507-L509))

```python
# 保单件数: 过滤小额/负保费
period_data = period_data[period_data['签单/批改保费'] >= 50]
daily_stats = period_data.groupby('weekday_index').size()
```

**注意事项**:
- ❌ 不要用 `abs()` 取绝对值 - 会导致退保也计入正保费
- ✅ 前端展示时可用红色标注负数

---

### 3.2 零手续费场景

**业务场景**:
- 新能源车险: 部分地区手续费为 0
- 活动期间: 免手续费促销

**处理策略**:
```python
# ✅ 保留 0 值,不做修改
commission_day = sum_float(day_df['手续费含税'])  # 0 也会被累加
```

**验证逻辑**:
- ❌ 不要判断 `if commission > 0:` - 会忽略合法的 0 值
- ✅ 允许 0 值存在,前端可特殊展示

---

### 3.3 日期格式标准化

**支持的日期格式**:
1. **ISO 8601**: `2025-11-08` (推荐)
2. **斜杠分隔**: `2025/11/08`
3. **无分隔符**: `20251108`
4. **Excel 序列号**: `44500` (自动转换)

**标准化代码**:
```python
df['投保确认时间'] = pd.to_datetime(df['投保确认时间'], errors='coerce')
```

**API 返回格式**:
```python
# 统一转换为 YYYY-MM-DD 格式
latest_date.strftime('%Y-%m-%d')  # '2025-11-08'
```

**时区处理**:
- 当前不涉及时区转换(所有数据均为本地时间)
- 如需支持时区: `pd.to_datetime(..., utc=True)`

---

### 3.4 缺失值填充策略

**填充规则**:
```python
df = df.fillna('')  # 统一填充为空字符串
```

**各字段缺失值处理**:

| 字段类型 | 缺失值处理 | 查询时处理 |
|---------|-----------|-----------|
| 日期字段 | `NaT` → `''` | `pd.to_datetime(..., errors='coerce')` 重新转换 |
| 数值字段 | `NaN` → `''` | `pd.to_numeric(..., errors='coerce')` 重新转换 |
| 文本字段 | `None` → `''` | 直接使用空字符串 |

**查询时的重新转换** (必需):
```python
# 读取 CSV 后必须重新转换日期
df = pd.read_csv(self.merged_csv, encoding='utf-8-sig')
df['投保确认时间'] = pd.to_datetime(df['投保确认时间'], errors='coerce')
```

**为什么需要重新转换**:
- CSV 文件不保留数据类型信息
- `pd.read_csv()` 默认将日期读为字符串
- 必须显式转换才能进行日期运算

---

## ⚡ 四、性能优化技巧

### 4.1 Pandas 优化模式

#### 优化 1: 使用向量化操作

❌ **低效**: 逐行迭代
```python
for _, row in df.iterrows():
    if row['签单/批改保费'] >= 50:
        count += 1
```

✅ **高效**: 向量化过滤
```python
count = len(df[df['签单/批改保费'] >= 50])
```

**性能提升**: 100x - 1000x

---

#### 优化 2: 避免多次 DataFrame 复制

❌ **低效**: 链式过滤(每次创建新 DataFrame)
```python
df = df[df['签单/批改保费'] >= 50]
df = df[df['是否续保'] == '是']
df = df[df['三级机构'] == '达州']
```

✅ **高效**: 合并条件
```python
mask = (df['签单/批改保费'] >= 50) & \
       (df['是否续保'] == '是') & \
       (df['三级机构'] == '达州')
df = df[mask]
```

**内存节省**: 避免创建 3 个中间 DataFrame

---

#### 优化 3: 使用 `low_memory=False` 处理大文件

```python
# ✅ 推荐: 大文件读取时指定
df = pd.read_csv(self.merged_csv, encoding='utf-8-sig', low_memory=False)
```

**说明**:
- `low_memory=True` (默认): 分块读取,可能导致数据类型推断不一致
- `low_memory=False`: 一次性读取,确保类型一致(适用于 <1GB 文件)

---

### 4.2 内存管理

#### 技巧 1: 显式删除中间变量

```python
existing_df = pd.read_csv(...)
new_df = pd.read_excel(...)
merged_df = pd.concat([existing_df, new_df])

# ✅ 立即释放内存
del existing_df, new_df
```

#### 技巧 2: 使用 `dtype` 指定数据类型(适用于已知列)

```python
# ✅ 指定类型可减少内存占用
dtype_dict = {
    '保单号': 'string',
    '签单/批改保费': 'float32',  # 而非 float64
    '签单数量': 'int32'           # 而非 int64
}
df = pd.read_csv(..., dtype=dtype_dict)
```

**内存节省**: `float64` → `float32` 减少 50% 内存

#### 技巧 3: 分块处理大文件

```python
# ✅ 超大文件(>1GB)使用分块
chunk_size = 10000
chunks = []
for chunk in pd.read_csv(..., chunksize=chunk_size):
    # 处理每个分块
    chunk = chunk[chunk['签单/批改保费'] >= 50]
    chunks.append(chunk)

df = pd.concat(chunks, ignore_index=True)
```

---

### 4.3 大文件处理策略

**文件大小分级**:
- **小文件** (<10MB): 直接 `pd.read_csv()` / `pd.read_excel()`
- **中文件** (10MB - 100MB): 使用 `low_memory=False`
- **大文件** (100MB - 1GB): 使用 `dtype` 指定类型
- **超大文件** (>1GB): 使用 `chunksize` 分块处理

**当前项目实践**:
- 车险清单合并 CSV: 约 20MB (中文件)
- 使用 `low_memory=False` 确保类型一致

---

### 4.4 并发处理考虑

**当前架构**: 单进程顺序处理

**可优化方向**:
```python
from concurrent.futures import ProcessPoolExecutor

def process_file(excel_file):
    df = pd.read_excel(excel_file)
    df = _clean_data(df)
    return df

# ✅ 多进程并行处理
with ProcessPoolExecutor(max_workers=4) as executor:
    results = executor.map(process_file, excel_files)
    all_new_data = list(results)
```

**注意事项**:
- ⚠️ 多进程会增加内存占用(每个进程独立内存)
- ⚠️ Windows 下需要 `if __name__ == '__main__':` 保护
- ✅ 适用于文件数量多(>10)且单文件小(<10MB)的场景

---

## 🔍 五、错误处理与日志

### 5.1 异常捕获机制

#### 文件处理异常

```python
try:
    df = self.process_new_excel(excel_file)
    all_new_data.append(df)
except Exception as e:
    print(f"  处理失败: {e}")
    # ✅ 不中断,继续处理下一个文件
```

**捕获的异常类型**:
- `FileNotFoundError`: 文件不存在
- `PermissionError`: 文件被占用(Windows)
- `xlrd.biffh.XLRDError`: Excel 文件损坏
- `MemoryError`: 内存不足
- `pd.errors.ParserError`: CSV 解析失败

---

#### API 异常处理 ([api_server.py:26-37](../../backend/api_server.py#L26-L37))

```python
@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    try:
        processor.scan_and_process_new_files()
        return jsonify({
            'success': True,
            'message': '数据刷新成功',
            'latest_date': processor.get_latest_date()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'数据刷新失败: {str(e)}'
        }), 500
```

**统一响应格式**:
- 成功: `{ success: true, data: {...} }`
- 失败: `{ success: false, message: "错误信息" }`, HTTP 500

---

### 5.2 日志记录标准

**当前日志级别**:
- `print()`: 输出到 stdout (终端/日志文件)
- 无结构化日志(未使用 `logging` 模块)

**日志内容**:
```python
print(f"正在处理Excel文件: {excel_path}")               # INFO
print(f"  读取成功: {len(df)} 行, {len(df.columns)} 列")  # INFO
print(f"  数据清洗完成")                                # INFO
print(f"  处理失败: {e}")                                # ERROR
```

**改进建议** (使用 `logging` 模块):
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('backend/backend.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 使用
logger.info(f"正在处理Excel文件: {excel_path}")
logger.error(f"处理失败: {e}", exc_info=True)  # 记录完整堆栈
```

---

### 5.3 用户友好的错误提示

**API 错误提示设计**:

| 错误场景 | HTTP 状态码 | 错误消息 | 用户操作建议 |
|---------|-----------|---------|------------|
| 未找到数据 | 404 | "未找到数据" | 请先上传 Excel 文件 |
| 文件格式错误 | 500 | "Excel 文件格式不正确" | 请检查文件格式是否为 .xlsx/.xls |
| 必填列缺失 | 500 | "缺少必填列: 保单号" | 请确保 Excel 包含所有必填列 |
| 日期格式错误 | 500 | "投保确认时间格式不正确" | 请使用 YYYY-MM-DD 格式 |
| 内存不足 | 500 | "文件过大,内存不足" | 请分批上传较小的文件 |

**前端展示建议**:
```javascript
if (!response.success) {
  // ✅ 用户友好的提示
  toast.error(response.message)

  // ❌ 不友好的提示
  console.error(response.message)
}
```

---

## 📖 六、实际代码示例与最佳实践

### 6.1 完整的文件处理流程

```python
from pathlib import Path
from data_processor import DataProcessor

# 初始化处理器
processor = DataProcessor(
    data_dir='data',
    staff_mapping_file='业务员机构团队归属.json'
)

# 批量处理新文件
processor.scan_and_process_new_files()

# 输出示例:
# ==========================================
# 找到 2 个Excel文件
# 正在处理Excel文件: data/车险清单_2025年10月.xlsx
#   读取成功: 1234 行, 45 列
#   数据清洗完成
#   合并完成: 5678 + 1234 = 6912 行
#   文件已移动: data/processed/车险清单_2025年10月_processed_20251108_143025.xlsx
# 正在处理Excel文件: data/车险清单_2025年11月.xlsx
#   读取成功: 890 行, 45 列
#   数据清洗完成
#   合并完成: 6912 + 890 = 7802 行
#   文件已移动: data/processed/车险清单_2025年11月_processed_20251108_143030.xlsx
# 数据更新完成!
```

---

### 6.2 单文件处理(手动控制)

```python
from pathlib import Path
import pandas as pd
from data_processor import DataProcessor

processor = DataProcessor()

# 步骤 1: 处理单个 Excel
excel_path = Path('data/车险清单_2025年10月.xlsx')
df = processor.process_new_excel(excel_path)

# 步骤 2: 检查数据
print(f"处理后数据: {len(df)} 行")
print(f"列名: {df.columns.tolist()}")

# 步骤 3: 合并到现有数据
merged_df = processor.merge_with_existing(df)

# 步骤 4: 保存
processor.save_merged_data(merged_df)

print("单文件处理完成!")
```

---

### 6.3 数据验证与质量检查

```python
import pandas as pd

# 读取合并后的数据
df = pd.read_csv('车险清单_2025年10-11月_合并.csv', encoding='utf-8-sig', low_memory=False)

# ===== 数据质量检查 =====

# 1. 检查必填列是否存在
required_cols = ['保单号', '业务员', '投保确认时间', '签单/批改保费']
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    print(f"❌ 缺少必填列: {missing_cols}")
else:
    print(f"✅ 必填列完整")

# 2. 检查保单号唯一性
df['投保确认时间'] = pd.to_datetime(df['投保确认时间'], errors='coerce')
duplicates = df[df.duplicated(subset=['保单号', '投保确认时间'], keep=False)]
if len(duplicates) > 0:
    print(f"⚠️  发现 {len(duplicates)} 条重复记录")
else:
    print(f"✅ 无重复记录")

# 3. 检查日期范围
latest_date = df['投保确认时间'].max()
earliest_date = df['投保确认时间'].min()
print(f"📅 日期范围: {earliest_date.date()} ~ {latest_date.date()}")

# 4. 检查保费分布
print(f"💰 保费统计:")
print(f"  - 最小值: {df['签单/批改保费'].min():.2f}")
print(f"  - 最大值: {df['签单/批改保费'].max():.2f}")
print(f"  - 平均值: {df['签单/批改保费'].mean():.2f}")
print(f"  - 负保费记录数: {len(df[df['签单/批改保费'] < 0])}")

# 5. 检查业务员映射覆盖率
staff_in_data = set(df['业务员'].dropna().unique())
staff_in_mapping = set()  # 从映射文件中提取
coverage = len(staff_in_mapping & staff_in_data) / len(staff_in_data) * 100
print(f"👥 业务员映射覆盖率: {coverage:.1f}%")
```

---

### 6.4 最佳实践总结

#### ✅ 推荐做法

1. **使用 pathlib 处理路径**
   ```python
   # ✅ 推荐
   from pathlib import Path
   project_root = Path(__file__).parent.parent
   csv_path = project_root / '车险清单_2025年10-11月_合并.csv'

   # ❌ 不推荐
   import os
   csv_path = os.path.join(os.getcwd(), '车险清单_2025年10-11月_合并.csv')
   ```

2. **读取 CSV 时始终指定 encoding**
   ```python
   # ✅ 推荐
   df = pd.read_csv(csv_path, encoding='utf-8-sig')

   # ❌ 不推荐(可能乱码)
   df = pd.read_csv(csv_path)
   ```

3. **查询前重新转换日期类型**
   ```python
   # ✅ 推荐
   df = pd.read_csv(csv_path, encoding='utf-8-sig')
   df['投保确认时间'] = pd.to_datetime(df['投保确认时间'], errors='coerce')

   # ❌ 不推荐(日期运算会报错)
   df = pd.read_csv(csv_path, encoding='utf-8-sig')
   df['投保确认时间'].max()  # TypeError: '>' not supported
   ```

4. **使用向量化操作**
   ```python
   # ✅ 推荐
   count = len(df[df['签单/批改保费'] >= 50])

   # ❌ 不推荐
   count = 0
   for _, row in df.iterrows():
       if row['签单/批改保费'] >= 50:
           count += 1
   ```

5. **异常捕获不中断批量处理**
   ```python
   # ✅ 推荐
   for file in files:
       try:
           process(file)
       except Exception as e:
           logger.error(f"处理失败: {e}")
           continue  # 继续处理下一个

   # ❌ 不推荐(一个文件失败导致全部中断)
   for file in files:
       process(file)  # 未捕获异常
   ```

#### ❌ 常见陷阱

1. **链式赋值警告**
   ```python
   # ❌ 会触发 SettingWithCopyWarning
   df[df['签单/批改保费'] >= 50]['是否续保'] = '是'

   # ✅ 使用 .loc
   df.loc[df['签单/批改保费'] >= 50, '是否续保'] = '是'
   ```

2. **日期比较前未转换**
   ```python
   # ❌ 日期是字符串,比较结果错误
   df = pd.read_csv(csv_path)
   df = df[df['投保确认时间'] > '2025-11-01']  # 字符串比较

   # ✅ 先转换为日期
   df['投保确认时间'] = pd.to_datetime(df['投保确认时间'], errors='coerce')
   df = df[df['投保确认时间'] > pd.to_datetime('2025-11-01')]
   ```

3. **忽略 errors='coerce'**
   ```python
   # ❌ 无效日期会抛出异常
   df['投保确认时间'] = pd.to_datetime(df['投保确认时间'])

   # ✅ 无效日期转为 NaT
   df['投保确认时间'] = pd.to_datetime(df['投保确认时间'], errors='coerce')
   ```

4. **使用 append() 追加行** (Pandas 1.4+ 已弃用)
   ```python
   # ❌ 已弃用,且性能差
   for _, row in df.iterrows():
       new_df = new_df.append(row)

   # ✅ 使用 concat
   new_df = pd.concat([new_df, df], ignore_index=True)
   ```

---

## 🔗 七、相关资源

### 关键代码位置
- [backend/data_processor.py](../../backend/data_processor.py) - 数据处理核心逻辑
  - [L107-236](../../backend/data_processor.py#L107-L236): 文件处理、清洗、合并
  - [L129-153](../../backend/data_processor.py#L129-L153): 数据清洗规则
  - [L155-184](../../backend/data_processor.py#L155-L184): 数据合并与去重
- [backend/api_server.py](../../backend/api_server.py) - Flask API 服务
  - [L21-37](../../backend/api_server.py#L21-L37): 数据刷新接口

### 相关 Skills
- [analyzing-auto-insurance-data](../analyzing-auto-insurance-data/SKILL.md) - 数据分析核心方法
- [api-endpoint-design](../SKILLS_ROADMAP.md#4-api-endpoint-design) (待开发) - API 规范文档

### 文档资源
- [ARCHITECTURE.md](../../docs/ARCHITECTURE.md) - 系统架构文档
- [PRODUCT_SPEC.md](../../docs/PRODUCT_SPEC.md) - 产品需求文档

---

## ✅ 总结

### 核心要点

1. **数据流转**: Excel → 清洗 → 合并 → 去重 → CSV
2. **去重策略**: 保单号 + 投保确认时间, `keep='last'`
3. **清洗步骤**: 删除空行 → 日期转换 → 数值转换 → 填充空值
4. **性能优化**: 向量化操作、避免链式过滤、显式删除中间变量
5. **异常处理**: 单文件失败不中断、记录错误信息、用户友好提示

### Token 节省估算

- **每次对话节省**: 3000-5000 tokens
- **年使用次数**: 约 30 次(数据处理问题)
- **年总节省**: 90,000 - 150,000 tokens

### 适用场景

✅ 适用:
- Excel 文件上传与处理
- 数据清洗规则修改
- 合并逻辑调整
- 性能优化
- 异常排查

❌ 不适用:
- 业务逻辑查询(使用 `analyzing-auto-insurance-data`)
- API 接口设计(使用 `api-endpoint-design`)
- 前端组件开发(使用 `vue-component-dev`)

---

**文档维护者**: Claude Code AI Assistant
**创建日期**: 2025-11-08
**下次审查**: 2025-11-22
