---
name: excel-toolkit
description: Excel 数据处理工具包，针对 BTC ShopFlow 的库存、盘点、报表等 Excel 导入导出场景
---

# Excel 工具包

## 何时使用

当你需要：
- 处理库存 Excel 导入
- 生成盘点数据报表
- Excel 数据验证和清洗
- 批量数据处理

## 项目中的 Excel 场景

### 1. 库存数据导出

已实现的导出功能:
  - 财务库存导出: apps/finance-app/.../useFinanceInventoryExport.ts
  - 物流库存导出: apps/logistics-app/.../useLogisticsInventoryExport.ts
  - 错误监控导出: apps/operations-app/.../BtcErrorMonitorExport.vue

使用的工具:
  import { exportTableToExcel } from '@btc/shared-core'

### 2. 常见 Excel 操作

导出表格数据:
```typescript
import { exportTableToExcel } from '@btc/shared-core'

// 导出数据
exportTableToExcel({
  data: tableData,
  filename: '库存数据',
  sheetName: 'Sheet1'
})
```

读取上传的 Excel:
```typescript
// 使用 file-saver 和 xlsx 库
import * as XLSX from 'xlsx'

const handleFileUpload = (file: File) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    const data = e.target?.result
    const workbook = XLSX.read(data, { type: 'binary' })
    const sheetName = workbook.SheetNames[0]
    const worksheet = workbook.Sheets[sheetName]
    const jsonData = XLSX.utils.sheet_to_json(worksheet)
    // 处理 jsonData
  }
  reader.readAsBinaryString(file)
}
```

### 3. Excel 数据验证

验证库存导入数据:
```typescript
const validateExcelData = (data: any[]) => {
  const errors: string[] = []
  
  data.forEach((row, index) => {
    // 必填字段检查
    if (!row.stockCode) {
      errors.push(第 \ 行：缺少料号)
    }
    
    // 数据类型检查
    if (isNaN(Number(row.quantity))) {
      errors.push(第 \ 行：数量必须是数字)
    }
    
    // 业务规则验证
    if (row.quantity < 0) {
      errors.push(第 \ 行：数量不能为负数)
    }
  })
  
  return errors
}
```

### 4. 生成复杂报表

多 Sheet 报表:
```typescript
import * as XLSX from 'xlsx'

const generateMultiSheetReport = () => {
  const wb = XLSX.utils.book_new()
  
  // Sheet 1: 汇总数据
  const summaryData = [
    ['料号', '库存数量', '差异', '状态'],
    // ... 数据
  ]
  const ws1 = XLSX.utils.aoa_to_sheet(summaryData)
  XLSX.utils.book_append_sheet(wb, ws1, '汇总')
  
  // Sheet 2: 明细数据
  const detailData = [...]
  const ws2 = XLSX.utils.aoa_to_sheet(detailData)
  XLSX.utils.book_append_sheet(wb, ws2, '明细')
  
  // 导出
  XLSX.writeFile(wb, '库存盘点报表.xlsx')
}
```

### 5. 数据转换

Excel 转 JSON:
```typescript
import * as XLSX from 'xlsx'

const excelToJSON = (file: File): Promise<any[]> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = (e) => {
      try {
        const workbook = XLSX.read(e.target?.result, { type: 'array' })
        const firstSheet = workbook.Sheets[workbook.SheetNames[0]]
        const jsonData = XLSX.utils.sheet_to_json(firstSheet, {
          raw: false,  // 保持原始格式
          defval: ''   // 空值默认为空字符串
        })
        resolve(jsonData)
      } catch (error) {
        reject(error)
      }
    }
    reader.readAsArrayBuffer(file)
  })
}
```

JSON 转 Excel:
```typescript
const jsonToExcel = (data: any[], filename: string) => {
  const ws = XLSX.utils.json_to_sheet(data)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Data')
  XLSX.writeFile(wb, \\.xlsx\)
}
```

## 依赖库

项目推荐使用:
```bash
# 前端
pnpm add xlsx file-saver
pnpm add -D @types/file-saver

# 或脚本中（Node.js）
pnpm add xlsx
```

## 常见 Excel 任务

### 任务 1：库存数据批量导入

1. 用户上传 Excel 文件
2. 读取并解析数据
3. 验证数据格式和业务规则
4. 批量调用 API 导入
5. 返回导入结果（成功/失败）

### 任务 2：生成盘点报表

1. 从后端 API 获取盘点数据
2. 格式化数据（料号、名称、数量、差异等）
3. 生成多 Sheet Excel（汇总 + 明细）
4. 添加样式（表头、边框、颜色）
5. 下载到本地

### 任务 3：数据对比分析

1. 读取系统数据和 Excel 数据
2. 对比差异
3. 生成差异报告
4. 导出 Excel 文件

## 项目中使用 exportTableToExcel

当前项目已有封装好的导出函数:
```typescript
import { exportTableToExcel } from '@btc/shared-core'

// 简单导出
exportTableToExcel({
  data: tableData.value,
  filename: '库存数据'
})
```

查看源码: packages/shared-core/src/utils/export.ts

## Excel 最佳实践

1. **大数据处理**: 分批处理，避免内存溢出
2. **数据验证**: 导入前验证必填字段和格式
3. **错误处理**: 提供友好的错误提示
4. **进度反馈**: 大文件导入时显示进度条
5. **模板下载**: 提供标准的导入模板

## 常见问题

Q: Excel 文件太大导致浏览器卡顿?
A: 使用 Web Worker 处理，或分批处理

Q: 中文乱码?
A: 确保使用 UTF-8 编码，或使用 xlsx 库的 bookType: 'xlsx'

Q: 日期格式不对?
A: Excel 日期是数字，需要转换:
   const date = new Date((excelDate - 25569) * 86400 * 1000)

Q: 如何添加样式?
A: 使用 xlsx-style 库或 exceljs 库

## 下一步

需要处理 PDF? → 可以创建 pdf-toolkit 技能
需要数据导入? → 结合 quality-assurance 技能验证数据
