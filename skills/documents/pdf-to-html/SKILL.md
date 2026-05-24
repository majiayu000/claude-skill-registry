---
name: pdf-to-html
description: PDF 转 HTML 工具，用于提取 PDF 内容和布局，转换为可编辑的 HTML/Vue 模板
---

# PDF 转 HTML 工具

## 何时使用

当你需要：
- 将 PDF 文档转换为 HTML 模板
- 提取 PDF 中的内容和布局信息
- 根据 PDF 创建打印模板
- 分析 PDF 结构和样式
- 将 SOP PDF 转换为可编辑的页面模板

## 主要功能

### 1. PDF 内容提取

提取 PDF 中的结构化内容：
- 标题和段落文本
- 表格数据
- 列表信息
- 图片和图表位置

### 2. 布局分析

分析 PDF 的视觉布局：
- 字体大小和样式
- 颜色信息
- 布局位置和间距
- 页面结构（页眉、页脚、内容区）

### 3. HTML 模板生成

将 PDF 转换为可编辑的 HTML/Vue 模板：
- 保持 PDF 的视觉效果
- 生成响应式 CSS
- 内嵌打印样式（@media print）
- 创建可复用的组件结构

## 使用场景

### 场景 1：根据 SOP PDF 创建打印模板

**工作流程**：

1. **上传 PDF 文件**
   - 用户提供 SOP PDF 文档
   - AI 分析 PDF 结构和样式

2. **提取内容和布局**
   ```
   使用 pdf-to-html 技能提取：
   - 标题、段落、表格
   - 字体大小、颜色
   - 布局位置
   ```

3. **生成 Vue 组件**
   - AI 创建打印模板组件（如 `PageAPrintTemplate.vue`）
   - 保持 PDF 的视觉效果
   - 使用响应式 CSS
   - 内嵌打印样式

4. **集成到页面**
   - 在页面组件中引入打印模板
   - 绑定动态数据
   - 实现打印逻辑

5. **测试和调整**
   - 预览打印效果
   - 对比 PDF 原件
   - 微调样式以匹配原 PDF

### 场景 2：批量转换 PDF 模板

当有多个 PDF 模板需要转换时：
- 逐个分析每个 PDF
- 提取共同的结构模式
- 创建可复用的模板组件
- 统一样式规范

## 技术实现

### PDF 解析库

**前端方案**（浏览器环境）：
```bash
pnpm add pdfjs-dist
```

```typescript
import * as pdfjsLib from 'pdfjs-dist'

const extractPDFContent = async (pdfUrl: string) => {
  const loadingTask = pdfjsLib.getDocument(pdfUrl)
  const pdf = await loadingTask.promise
  
  const content = []
  for (let i = 1; i <= pdf.numPages; i++) {
    const page = await pdf.getPage(i)
    const textContent = await page.getTextContent()
    
    content.push({
      page: i,
      items: textContent.items.map(item => ({
        text: item.str,
        x: item.transform[4],
        y: item.transform[5],
        fontSize: item.transform[0],
        fontName: item.fontName
      }))
    })
  }
  
  return content
}
```

**后端方案**（Node.js）：
```bash
pnpm add pdf-parse pdfjs-dist
```

```typescript
import pdf from 'pdf-parse'
import fs from 'fs'

const extractPDFContent = async (pdfPath: string) => {
  const dataBuffer = fs.readFileSync(pdfPath)
  const data = await pdf(dataBuffer)
  
  return {
    numPages: data.numpages,
    text: data.text,
    info: data.info,
    metadata: data.metadata
  }
}
```

### HTML 模板生成

根据提取的内容生成 Vue 组件：

```vue
<template>
  <div class="print-template">
    <!-- 页眉 -->
    <div class="print-header">
      <h1>{{ title }}</h1>
    </div>
    
    <!-- 内容区 -->
    <div class="print-content">
      <!-- 从 PDF 提取的内容 -->
      <div v-for="section in sections" :key="section.id">
        <h2>{{ section.title }}</h2>
        <p>{{ section.content }}</p>
      </div>
      
      <!-- 表格 -->
      <table class="print-table">
        <thead>
          <tr>
            <th v-for="col in tableColumns" :key="col">{{ col }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in tableData" :key="row.id">
            <td v-for="col in tableColumns" :key="col">{{ row[col] }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- 页脚 -->
    <div class="print-footer">
      <p>{{ footerText }}</p>
    </div>
  </div>
</template>

<style scoped>
.print-template {
  /* 从 PDF 提取的样式 */
  font-family: 'SimSun', serif;
  font-size: 12pt;
  line-height: 1.6;
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
```

## 提取的信息类型

### 1. 文本内容
- 标题层级（H1, H2, H3...）
- 段落文本
- 列表项
- 页眉页脚文本

### 2. 表格数据
- 表头信息
- 表格行数据
- 单元格样式
- 表格布局

### 3. 样式信息
- 字体大小和类型
- 颜色（文字、背景）
- 对齐方式
- 间距和边距
- 边框样式

### 4. 布局结构
- 页面尺寸
- 内容区域位置
- 分栏布局
- 图片位置和尺寸

## 与 page-creator 集成

`pdf-to-html` 通常与 `page-creator` 配合使用：

1. **使用 pdf-to-html 提取 PDF 内容**
2. **使用 page-creator 生成页面组件**
3. **将提取的内容填充到组件中**
4. **调整样式以匹配原 PDF**

## 常见任务

### 任务 1：提取单个 PDF 模板

1. 读取 PDF 文件
2. 解析 PDF 结构
3. 提取文本和样式
4. 生成 HTML/Vue 模板
5. 保存为组件文件

### 任务 2：批量转换 PDF

1. 扫描 PDF 目录
2. 逐个处理 PDF 文件
3. 提取共同模式
4. 生成统一模板结构
5. 创建模板库

### 任务 3：PDF 样式分析

1. 分析 PDF 的视觉样式
2. 提取 CSS 属性
3. 生成样式映射
4. 创建样式变量文件
5. 应用到 Vue 组件

## 最佳实践

1. **保持视觉一致性**：生成的 HTML 应尽可能接近原 PDF 的视觉效果
2. **响应式设计**：确保模板在不同尺寸下正常显示
3. **打印优化**：使用 `@media print` 优化打印样式
4. **可维护性**：生成的代码应清晰、可编辑
5. **数据绑定**：将静态内容替换为动态数据绑定

## 相关技能

- **page-creator**：创建页面组件，使用 pdf-to-html 提取的内容
- **pdf-toolkit**：生成 PDF 文档，与 pdf-to-html 形成完整闭环
- **interactive-page-creator**：交互式创建页面，可调用 pdf-to-html 处理 PDF 模板

## 注意事项

- PDF 解析可能不完美，需要人工检查和调整
- 复杂布局的 PDF 可能需要手动重构
- 图片和图表需要单独处理
- 中文字体需要确保正确显示
- 表格结构复杂的 PDF 可能需要手动调整

## 下一步

需要创建页面？→ 使用 page-creator 技能
需要生成 PDF？→ 使用 pdf-toolkit 技能
需要交互式创建？→ 使用 interactive-page-creator 技能
