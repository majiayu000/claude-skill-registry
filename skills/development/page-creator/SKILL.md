---
name: page-creator
description: 页面创建完整流程，从路由配置到组件使用、服务集成、功能实现的端到端指南
---

# 页面创建器

## 何时使用

当你需要：
- 在某个应用的某个模块中增加新页面
- 配置路由和菜单
- 集成后端 EPS 服务
- 使用 BTC 组件（Table、Form、Dialog等）
- 实现特定功能（打印、导入、导出等）

## 完整创建流程

### 示例场景

需求：在管理应用（admin-app）的测试模块（test）中增加页面A
- 路由名称：test-page-a
- 路径：/test/page-a
- 后端服务：eps.test.pageA
- 组件：BtcMasterTableGroup
- 功能：打印（参考 PDF 模板）

### 步骤 1：创建页面文件

位置：\pps/admin-app/src/modules/test/views/page-a/index.vue\

基础模板：
\\\ue
<template>
  <div class="page-a">
    <BtcMasterTableGroup
      ref="masterTableRef"
      :service="pageAService"
      title-key="test.pageA.title"
    >
      <template #toolbar>
        <el-button type="primary" @click="handlePrint">
          <BtcSvg name="print" />
          打印
        </el-button>
      </template>
    </BtcMasterTableGroup>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { BtcMasterTableGroup, BtcSvg } from '@btc/shared-components'
import { usePageAService } from './composables/usePageAService'
import { usePrint } from './composables/usePrint'

const masterTableRef = ref()
const pageAService = usePageAService()
const { handlePrint } = usePrint(masterTableRef)
</script>

<style scoped lang="scss">
.page-a {
  height: 100%;
}
</style>
\\\

### 步骤 2：创建服务文件

位置：\pps/admin-app/src/modules/test/views/page-a/composables/usePageAService.ts\

\\\	ypescript
import { getEpsService } from '@btc/shared-core'

export const usePageAService = () => {
  // 获取 EPS 服务节点
  const epsNode = getEpsService('eps.test.pageA')
  
  return {
    // CRUD 方法会自动从 EPS 生成
    query: epsNode?.query,
    save: epsNode?.save,
    update: epsNode?.update,
    delete: epsNode?.delete,
    // 自定义方法
    export: epsNode?.export,
  }
}
\\\

### 步骤 3：实现打印功能

位置：\pps/admin-app/src/modules/test/views/page-a/composables/usePrint.ts\

\\\	ypescript
import { ref } from 'vue'
import type { Ref } from 'vue'

export const usePrint = (tableRef: Ref) => {
  const printTemplate = \\\
  <div class="print-template">
    <div class="print-header">
      <h1>{{title}}</h1>
      <p class="print-date">打印日期: {{date}}</p>
    </div>
    
    <table class="print-table">
      <thead>
        <tr>
          <th>序号</th>
          <th>料号</th>
          <th>名称</th>
          <th>数量</th>
        </tr>
      </thead>
      <tbody>
        {{#each rows}}
        <tr>
          <td>{{@index}}</td>
          <td>{{code}}</td>
          <td>{{name}}</td>
          <td>{{qty}}</td>
        </tr>
        {{/each}}
      </tbody>
    </table>
  </div>
  
  <style>
  @media print {
    @page { size: A4; margin: 15mm; }
    body { margin: 0; }
  }
  
  .print-template {
    padding: 20px;
    font-family: 'Microsoft YaHei', sans-serif;
  }
  
  .print-header {
    text-align: center;
    margin-bottom: 30px;
    border-bottom: 2px solid #333;
    padding-bottom: 15px;
  }
  
  .print-table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .print-table th,
  .print-table td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  
  .print-table th {
    background-color: #f5f5f5;
    font-weight: bold;
  }
  </style>
  \\\
  
  const handlePrint = () => {
    // 获取表格数据
    const tableData = tableRef.value?.getTableData() || []
    
    // 渲染模板
    const printContent = renderTemplate(printTemplate, {
      title: '页面A打印',
      date: new Date().toLocaleDateString('zh-CN'),
      rows: tableData
    })
    
    // 打开打印窗口
    const printWindow = window.open('', '_blank')
    if (printWindow) {
      printWindow.document.write(printContent)
      printWindow.document.close()
      printWindow.print()
    }
  }
  
  return {
    handlePrint
  }
}

// 简单的模板渲染
const renderTemplate = (template: string, data: any): string => {
  let result = template
  result = result.replace(/{{title}}/g, data.title)
  result = result.replace(/{{date}}/g, data.date)
  
  // 处理循环
  const eachRegex = /{{#each rows}}([\\s\\S]*?){{\/each}}/g
  result = result.replace(eachRegex, (match, itemTemplate) => {
    return data.rows.map((row: any, index: number) => {
      return itemTemplate
        .replace(/{{@index}}/g, index + 1)
        .replace(/{{code}}/g, row.code)
        .replace(/{{name}}/g, row.name)
        .replace(/{{qty}}/g, row.qty)
    }).join('')
  })
  
  return result
}
\\\

### 步骤 4：配置路由

位置：\pps/admin-app/src/modules/test/config.ts\

添加路由配置：
\\\	ypescript
export default {
  routes: [
    // ... 其他路由
    {
      path: '/test/page-a',
      name: 'test-page-a',
      component: () => import('./views/page-a/index.vue'),
      meta: {
        labelKey: 'test.pageA.title',
        icon: 'document'
      }
    }
  ],
  
  i18n: {
    'zh-CN': {
      'test.pageA.title': '页面A',
      'test.pageA.desc': '页面A描述'
    },
    'en-US': {
      'test.pageA.title': 'Page A',
      'test.pageA.desc': 'Page A Description'
    }
  }
}
\\\

### 步骤 5：添加到菜单（可选）

在 config.ts 的 menus 中添加：
\\\	ypescript
export default {
  menus: [
    {
      labelKey: 'test.menu.title',
      children: [
        // ... 其他菜单项
        {
          labelKey: 'test.pageA.title',
          path: '/test/page-a',
          icon: 'document'
        }
      ]
    }
  ]
}
\\\

## 常用 BTC 组件选择

### 1. BtcMasterTableGroup（推荐用于列表页）

特点：左侧主数据选择 + 右侧明细表格

\\\ue
<BtcMasterTableGroup
  :left-service="leftService"
  left-title="title.left"
  @select="onMasterSelect"
>
  <!-- 明细表格会自动生成 -->
</BtcMasterTableGroup>
\\\

使用场景：
- 部门-用户
- 仓库-库位
- 客户-订单

### 2. BtcDoubleLeftGroup（双左侧布局）

特点：左侧主数据 + 左侧次数据 + 右侧明细

\\\ue
<BtcDoubleLeftGroup
  :left-service="leftService"
  :center-service="centerService"
  :show-center-search="true"
>
  <template #right>
    <!-- 自定义右侧内容 -->
  </template>
</BtcDoubleLeftGroup>
\\\

使用场景：
- 仓库-库区-库位
- 部门-小组-人员

### 3. BtcCrud（基础 CRUD）

特点：最简单的增删改查

\\\ue
<BtcCrud :service="crudService">
  <BtcTable>
    <BtcTableColumn prop="code" label="编号" />
    <BtcTableColumn prop="name" label="名称" />
  </BtcTable>
</BtcCrud>
\\\

使用场景：
- 简单的列表页
- 字典数据管理

### 4. BtcFilterTableGroup（筛选+表格）

特点：顶部筛选 + 表格 + 分页

\\\ue
<BtcFilterTableGroup
  :service="tableService"
  :filter-config="filterConfig"
>
  <!-- 表格列配置 -->
</BtcFilterTableGroup>
\\\

使用场景：
- 需要复杂筛选的列表
- 报表查询

## EPS 服务使用

### 获取 EPS 服务

\\\	ypescript
import { getEpsService } from '@btc/shared-core'

// 方式 1：直接获取（推荐）
const epsNode = getEpsService('eps.test.pageA')

// 方式 2：从 EPS 树中查找
import { eps } from '@/build/eps/eps'
const epsNode = eps.test?.pageA
\\\

### 使用 EPS 方法

\\\	ypescript
// CRUD 方法（EPS 自动生成）
const service = {
  query: epsNode?.query,      // 查询列表
  save: epsNode?.save,        // 新增
  update: epsNode?.update,    // 更新
  delete: epsNode?.delete,    // 删除
  
  // 自定义方法
  export: epsNode?.export,
  import: epsNode?.import,
  print: epsNode?.print,
}

// 调用示例
const data = await service.query({ page: 1, size: 20 })
await service.save({ code: 'A001', name: '测试' })
\\\

### EPS 路径规范

格式：\eps.{module}.{entity}.{method}\

示例：
- \eps.warehouse.location.query\ - 仓库库位查询
- \eps.inventory.result.export\ - 库存结果导出
- \eps.test.pageA.print\ - 测试页面A打印

## 完整示例：创建带打印功能的页面

### 需求分析

- 应用：admin-app
- 模块：test  
- 页面：page-a
- 路由：/test/page-a
- 服务：eps.test.pageA
- 组件：BtcMasterTableGroup
- 功能：打印（参考 PDF 模板）

### 1. 创建目录结构

\\\ash
apps/admin-app/src/modules/test/views/page-a/
├── index.vue                          # 主页面
├── composables/
│   ├── usePageAService.ts            # 服务
│   ├── usePageAPrint.ts              # 打印功能
│   └── usePageAData.ts               # 数据处理
└── components/                        # 页面私有组件（可选）
    └── PageAPrintTemplate.vue
\\\

### 2. 主页面实现

\\\ue
<!-- apps/admin-app/src/modules/test/views/page-a/index.vue -->
<template>
  <div class="page-a">
    <BtcMasterTableGroup
      ref="masterTableRef"
      :left-service="leftService"
      left-title-key="test.pageA.leftTitle"
      :right-service="rightService"
      @left-select="handleLeftSelect"
    >
      <template #toolbar>
        <el-button type="primary" @click="handlePrint">
          <BtcSvg name="print" class="mr-[5px]" />
          {{ t('common.print') }}
        </el-button>
        <el-button @click="handleExport">
          <BtcSvg name="export" class="mr-[5px]" />
          {{ t('common.export') }}
        </el-button>
      </template>
    </BtcMasterTableGroup>
    
    <!-- 打印内容（隐藏） -->
    <div ref="printContentRef" class="print-content">
      <PageAPrintTemplate :data="printData" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { BtcMasterTableGroup, BtcSvg } from '@btc/shared-components'
import { usePageAService } from './composables/usePageAService'
import { usePageAPrint } from './composables/usePageAPrint'
import PageAPrintTemplate from './components/PageAPrintTemplate.vue'

const { t } = useI18n()
const masterTableRef = ref()
const printContentRef = ref()

// 服务
const { leftService, rightService } = usePageAService()

// 打印
const printData = ref({})
const { handlePrint, handleExport } = usePageAPrint(
  masterTableRef, 
  printContentRef,
  printData
)

// 左侧选择事件
const handleLeftSelect = (selected: any) => {
  printData.value = {
    ...selected,
    details: masterTableRef.value?.getTableData() || []
  }
}
</script>

<style scoped lang="scss">
.page-a {
  height: 100%;
}

.print-content {
  display: none;
}

@media print {
  .page-a > :not(.print-content) {
    display: none !important;
  }
  
  .print-content {
    display: block !important;
  }
}
</style>
\\\

### 3. 服务实现

\\\	ypescript
// apps/admin-app/src/modules/test/views/page-a/composables/usePageAService.ts
import { getEpsService } from '@btc/shared-core'

export const usePageAService = () => {
  // 左侧主数据服务
  const leftEps = getEpsService('eps.test.pageA.master')
  const leftService = {
    query: leftEps?.query,
    save: leftEps?.save,
    update: leftEps?.update,
    delete: leftEps?.delete,
  }
  
  // 右侧明细服务
  const rightEps = getEpsService('eps.test.pageA.detail')
  const rightService = {
    query: rightEps?.query,
    save: rightEps?.save,
    update: rightEps?.update,
    delete: rightEps?.delete,
  }
  
  return {
    leftService,
    rightService
  }
}
\\\

### 4. 打印功能实现（基于 PDF 模板）

\\\	ypescript
// apps/admin-app/src/modules/test/views/page-a/composables/usePageAPrint.ts
import { ref } from 'vue'
import type { Ref } from 'vue'

export const usePageAPrint = (
  tableRef: Ref,
  printRef: Ref,
  printData: Ref
) => {
  // 打印
  const handlePrint = () => {
    // 更新打印数据
    printData.value = {
      title: '页面A打印',
      date: new Date().toLocaleDateString('zh-CN'),
      data: tableRef.value?.getTableData() || []
    }
    
    // 等待 Vue 更新 DOM
    setTimeout(() => {
      window.print()
    }, 100)
  }
  
  // 导出 Excel
  const handleExport = () => {
    const tableData = tableRef.value?.getTableData() || []
    // 使用 excel-toolkit 导出
    exportTableToExcel({
      data: tableData,
      filename: '页面A数据'
    })
  }
  
  return {
    handlePrint,
    handleExport
  }
}
\\\

### 5. 打印模板组件（根据 PDF 创建）

\\\ue
<!-- apps/admin-app/src/modules/test/views/page-a/components/PageAPrintTemplate.vue -->
<template>
  <div class="print-template">
    <!-- 页眉 -->
    <div class="print-header">
      <div class="header-logo">
        <img src="/logo.png" alt="Logo" />
      </div>
      <h1 class="header-title">{{ data.title || '页面A打印单' }}</h1>
      <div class="header-info">
        <span>单号: {{ data.orderNo }}</span>
        <span>日期: {{ data.date }}</span>
      </div>
    </div>
    
    <!-- 基本信息 -->
    <div class="print-section">
      <h2>基本信息</h2>
      <div class="info-grid">
        <div class="info-item">
          <label>部门:</label>
          <span>{{ data.department }}</span>
        </div>
        <div class="info-item">
          <label>负责人:</label>
          <span>{{ data.owner }}</span>
        </div>
      </div>
    </div>
    
    <!-- 明细表格 -->
    <div class="print-section">
      <h2>明细数据</h2>
      <table class="print-table">
        <thead>
          <tr>
            <th>序号</th>
            <th>料号</th>
            <th>名称</th>
            <th>规格</th>
            <th>数量</th>
            <th>单位</th>
            <th>备注</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in data.details" :key="index">
            <td>{{ index + 1 }}</td>
            <td>{{ item.code }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.spec }}</td>
            <td>{{ item.qty }}</td>
            <td>{{ item.unit }}</td>
            <td>{{ item.remark }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- 页脚签名区 -->
    <div class="print-footer">
      <div class="signature-area">
        <div class="signature-item">
          <label>制单人:</label>
          <span class="signature-line">__________</span>
        </div>
        <div class="signature-item">
          <label>审核人:</label>
          <span class="signature-line">__________</span>
        </div>
        <div class="signature-item">
          <label>批准人:</label>
          <span class="signature-line">__________</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  data: {
    title?: string
    orderNo?: string
    date?: string
    department?: string
    owner?: string
    details?: any[]
  }
}

defineProps<Props>()
</script>

<style scoped lang="scss">
.print-template {
  padding: 20mm;
  font-family: 'Microsoft YaHei', 'SimSun', sans-serif;
  font-size: 12pt;
}

.print-header {
  text-align: center;
  margin-bottom: 20px;
  border-bottom: 2px solid #000;
  padding-bottom: 15px;
}

.header-logo img {
  height: 40px;
  margin-bottom: 10px;
}

.header-title {
  font-size: 20pt;
  font-weight: bold;
  margin: 10px 0;
}

.header-info {
  display: flex;
  justify-content: space-between;
  font-size: 10pt;
  color: #666;
}

.print-section {
  margin-bottom: 20px;
}

.print-section h2 {
  font-size: 14pt;
  font-weight: bold;
  border-left: 4px solid #000;
  padding-left: 8px;
  margin-bottom: 10px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.info-item {
  display: flex;
  
  label {
    font-weight: bold;
    margin-right: 5px;
    min-width: 80px;
  }
}

.print-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  
  th, td {
    border: 1px solid #000;
    padding: 6px 8px;
    text-align: left;
  }
  
  th {
    background-color: #f5f5f5;
    font-weight: bold;
    text-align: center;
  }
  
  td {
    font-size: 10pt;
  }
}

.print-footer {
  margin-top: 30px;
  page-break-inside: avoid;
}

.signature-area {
  display: flex;
  justify-content: space-around;
  padding: 20px 0;
}

.signature-item {
  display: flex;
  align-items: center;
  
  label {
    font-weight: bold;
    margin-right: 10px;
  }
  
  .signature-line {
    display: inline-block;
    border-bottom: 1px solid #000;
    min-width: 100px;
    height: 20px;
  }
}

@media print {
  @page {
    size: A4;
    margin: 15mm;
  }
  
  .print-template {
    padding: 0;
  }
}
</style>
\\\

### 6. 配置路由和国际化

\\\	ypescript
// apps/admin-app/src/modules/test/config.ts
export default {
  routes: [
    {
      path: '/test/page-a',
      name: 'test-page-a',
      component: () => import('./views/page-a/index.vue'),
      meta: {
        labelKey: 'test.pageA.title'
      }
    }
  ],
  
  i18n: {
    'zh-CN': {
      'test.pageA.title': '页面A',
      'test.pageA.leftTitle': '主数据',
      'test.pageA.print': '打印单据'
    },
    'en-US': {
      'test.pageA.title': 'Page A',
      'test.pageA.leftTitle': 'Master Data',
      'test.pageA.print': 'Print Document'
    }
  }
}
\\\

## PDF 模板转换工作流

### 场景：根据 SOP PDF 创建打印模板

1. **上传 PDF 文件**
   - 用户提供 SOP PDF
   - AI 分析 PDF 结构和样式

2. **提取内容和布局**
   \\\
   使用 pdf-to-html 技能提取：
   - 标题、段落、表格
   - 字体大小、颜色
   - 布局位置
   \\\

3. **生成 Vue 组件**
   \\\
   AI 创建 PageAPrintTemplate.vue
   - 保持 PDF 的视觉效果
   - 使用响应式 CSS
   - 内嵌打印样式
   \\\

4. **集成到页面**
   \\\
   在 index.vue 中：
   - 引入打印模板组件
   - 绑定数据
   - 实现打印逻辑
   \\\

5. **测试和调整**
   \\\
   - 预览打印效果
   - 对比 PDF 原件
   - 微调样式
   \\\

## 快速创建模板

### 模板 1：主从表格页

\\\ash
# 提供以下信息
应用: admin-app
模块: test
页面名: customer-order
路由: /test/customer-order
左侧服务: eps.test.customer
右侧服务: eps.test.order
组件: BtcMasterTableGroup

# AI 会自动创建完整的页面文件
\\\

### 模板 2：简单列表页

\\\ash
应用: admin-app
模块: test  
页面名: product-list
路由: /test/product-list
服务: eps.test.product
组件: BtcCrud
\\\

### 模板 3：复杂筛选页

\\\ash
应用: admin-app
模块: test
页面名: report-query
路由: /test/report-query
服务: eps.test.report
组件: BtcFilterTableGroup
功能: 导出Excel、打印
\\\

## 组件推荐决策树

\\\
需要主从结构？
├─ 是 → 需要双层主数据？
│  ├─ 是 → BtcDoubleLeftGroup
│  └─ 否 → BtcMasterTableGroup
└─ 否 → 需要复杂筛选？
   ├─ 是 → BtcFilterTableGroup
   └─ 否 → BtcCrud
\\\

## 常见功能实现

### 打印功能
\\\	ypescript
const handlePrint = () => {
  window.print()
}
\\\

### 导出 Excel
\\\	ypescript
import { exportTableToExcel } from '@btc/shared-core'

const handleExport = () => {
  const data = tableRef.value?.getTableData()
  exportTableToExcel({ data, filename: '数据导出' })
}
\\\

### 导入 Excel  
\\\	ypescript
import * as XLSX from 'xlsx'

const handleImport = (file: File) => {
  // 使用 excel-toolkit 技能处理
}
\\\

### 批量操作
\\\	ypescript
const handleBatchDelete = async () => {
  const selected = tableRef.value?.getSelection()
  await service.batchDelete(selected.map(item => item.id))
  tableRef.value?.refresh()
}
\\\

## 完整开发检查清单

创建新页面时的检查项：

- [ ] 1. 创建页面文件 \iews/{page-name}/index.vue\
- [ ] 2. 创建服务文件 \composables/use{PageName}Service.ts\
- [ ] 3. 配置路由 \config.ts - routes\
- [ ] 4. 添加国际化 \config.ts - i18n\
- [ ] 5. 添加菜单项 \config.ts - menus\（可选）
- [ ] 6. 实现业务逻辑
- [ ] 7. 实现特殊功能（打印、导入、导出等）
- [ ] 8. 测试功能
- [ ] 9. 检查 i18n key
- [ ] 10. 提交代码

## 常见问题

Q: 如何快速找到合适的组件？
A: 查看 packages/shared-components/src/index.ts 或文档

Q: EPS 服务路径怎么确定？
A: 查看 build/eps/eps.json 或咨询后端

Q: 打印样式不对？
A: 检查 @media print CSS 规则

Q: 如何从 PDF 提取样式？
A: 使用 pdf-to-html 技能，手动对照调整

## 下一步

- 需要 PDF 转换？→ 使用 pdf-to-html 技能
- 需要 Excel 处理？→ 使用 excel-toolkit 技能
- 需要了解组件？→ 使用 component-development 技能（待创建）
