---
name: interactive-page-creator
description: 交互式页面创建向导，通过连续对话收集需求，自动创建完整页面
---

# 交互式页面创建向导

## 工作流程

这是一个主技能，会编排其他工具技能完成复杂任务。

## 创建流程

### 阶段 1：需求收集

AI 会询问以下信息（如果用户未提供）:

1. **应用和模块**
   - 在哪个应用？（如 admin-app）
   - 在哪个模块？（如 test）
   - 使用 route-analyzer 列出可选模块

2. **页面基本信息**
   - 页面名称？（如 page-a）
   - 路由路径？（推荐：/{module}/{page-name}）
   - 路由名称？（推荐：{module}-{page-name}）
   - 使用 route-analyzer 检查冲突

3. **后端服务**
   - EPS 服务路径？（如 eps.test.pageA）
   - 使用 eps-analyzer 验证服务是否存在
   - 如果不存在，生成服务桩代码

4. **组件选择**
   - 页面类型？（列表/主从/筛选）
   - 使用 component-catalog 推荐组件
   - 确定使用哪个 BTC 组件

5. **图标选择**
   - 页面图标？（用于菜单和路由 meta）
   - 使用 icon-manager 列出可选图标
   - 推荐相关图标

6. **国际化**
   - 页面中文名称？
   - 页面英文名称？
   - 使用 i18n-manager 生成标准 key

7. **功能需求**
   - 需要打印？→ 加载 pdf-toolkit
   - 需要导入 Excel？→ 加载 excel-toolkit
   - 需要导出 PDF？→ 加载 pdf-toolkit
   - 参考 PDF 模板？→ 加载 pdf-to-html

### 阶段 2：文件创建

使用 file-navigator 创建:

1. **创建目录结构**
   \\\
   apps/{app}/src/modules/{module}/views/{page}/
   ├── index.vue
   ├── composables/
   │   ├── use{Page}Service.ts
   │   ├── use{Page}Print.ts（如果需要）
   │   └── use{Page}Data.ts
   └── components/（如果需要）
   \\\

2. **生成主页面**
   - 根据选择的组件生成模板
   - 集成选择的功能
   - 应用统一样式

3. **生成服务文件**
   - 使用 eps-analyzer 生成 EPS 调用代码
   - 包含所有 CRUD 方法

4. **生成功能文件**
   - 打印功能（如果需要）
   - 导入导出功能（如果需要）

### 阶段 3：配置更新

1. **更新路由配置**
   - 在 config.ts 的 views 中添加路由
   - 使用 route-analyzer 验证

2. **更新国际化**
   - 在 config.ts 的 i18n 中添加翻译
   - 使用 i18n-manager 生成标准 key

3. **更新菜单（可选）**
   - 在 config.ts 的 menus 中添加菜单项
   - 使用选择的图标

### 阶段 4：功能实现

根据需求实现特定功能：

**打印功能**:
1. 如果提供 PDF 模板：
   - 使用 pdf-to-html 提取 PDF 结构
   - 生成 PrintTemplate.vue 组件
   - 实现打印逻辑

2. 如果无 PDF：
   - 使用标准打印模板
   - 生成基础打印样式

**导入功能**:
- 使用 excel-toolkit 生成导入代码
- 包含数据验证逻辑

**导出功能**:
- 使用 excel-toolkit 生成导出代码
- 支持自定义列配置

### 阶段 5：验证和完善

1. **代码检查**
   - 使用 quality-assurance 检查代码质量
   - 检查 i18n key 是否完整
   - 检查导入路径

2. **功能测试**
   - 提供测试步骤
   - 常见问题排查

3. **文档更新**
   - 添加页面说明注释
   - 更新模块 README（如果有）

## 交互示例

用户: \"在 admin-app 的 test 模块创建页面A\"

AI: \"好的，让我帮你创建。请提供以下信息：\"
  
  1. 路由路径？（推荐：/test/page-a）
     [AI 使用 route-analyzer 列出现有路由]
  
  2. 后端 EPS 服务？（如 eps.test.pageA）
     [AI 使用 eps-analyzer 验证服务]
  
  3. 页面类型？
     a) 简单列表（BtcCrud）
     b) 主从结构（BtcMasterTableGroup）
     c) 复杂筛选（BtcFilterTableGroup）
     [AI 使用 component-catalog 展示组件]
  
  4. 需要什么功能？
     □ 打印
     □ 导入 Excel
     □ 导出 Excel
     □ 导出 PDF
  
  5. 页面图标？
     [AI 使用 icon-manager 推荐图标]
  
  6. 页面中文名/英文名？
     [AI 使用 i18n-manager 生成 key]

用户: \"路由用 /test/page-a，服务是 eps.test.pageA，用主从结构，需要打印功能，图标用 document\"

AI: \"收到！开始创建...\"
  [使用 file-navigator 创建文件]
  [使用 page-creator 生成代码]
  [使用 pdf-toolkit 添加打印]
  [使用 route-analyzer 更新路由]
  [使用 i18n-manager 添加翻译]
  
AI: \"✅ 页面创建完成！文件已创建在：
  - apps/admin-app/src/modules/test/views/page-a/index.vue
  - apps/admin-app/src/modules/test/views/page-a/composables/usePageAService.ts
  - apps/admin-app/src/modules/test/views/page-a/composables/usePageAPrint.ts
  
  路由已配置：/test/page-a
  国际化已添加：test.pageA.title
  
  下一步：
  1. 启动开发服务器验证
  2. 如果需要打印模板，可以上传 PDF 参考\"

## 连续技能调用

创建页面 → 添加功能 → 优化样式 → 测试 → 部署

每个阶段都可以调用相应的工具技能。

## 使用此技能

直接说：\"在 {app} 的 {module} 模块创建 {page}\"

AI 会自动启动交互式向导，逐步收集信息并创建页面。
