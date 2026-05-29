---
name: component-catalog
description: 组件目录，列出所有BTC组件、使用示例、推荐组件选择
---

# 组件目录

## 功能

- 列出所有 BTC 组件
- 查看组件使用示例
- 推荐合适的组件
- 组件 API 速查

## 组件分类

### Data 数据组件（CRUD常用）⭐⭐⭐⭐⭐

BtcCrud: 基础增删改查
  用途: 简单列表页
  示例: apps/admin-app/src/modules/test/views/crud/

BtcMasterTableGroup: 主从表格
  用途: 主数据+明细（如部门-用户）
  示例: apps/system-app/src/modules/warehouse/

BtcFilterTableGroup: 筛选表格
  用途: 复杂筛选+列表
  示例: apps/admin-app/src/modules/test/views/filter-list-test/

BtcDoubleLeftGroup: 双左侧布局
  用途: 三级结构（如仓库-库区-库位）
  
BtcTable: 表格
BtcPagination: 分页

### Form 表单组件

BtcForm: 表单容器
BtcUpsert: 新增/编辑弹窗
BtcDialog: 对话框
BtcUpload: 文件上传
BtcSelectButton: 选择按钮
BtcColorPicker: 颜色选择器

### CRUD 工具组件

BtcCrudRow: CRUD 行容器
BtcAddBtn: 新增按钮
BtcEditBtn: 编辑按钮
BtcDeleteBtn: 删除按钮
BtcRefreshBtn: 刷新按钮
BtcExportBtn: 导出按钮
BtcImportBtn: 导入按钮
BtcSearchKey: 搜索框

### Basic 基础组件

BtcButton: 按钮
BtcSvg: SVG 图标
BtcEmpty: 空状态
BtcCard: 卡片
BtcTag: 标签
BtcAvatar: 头像

### Feedback 反馈组件

BtcMessage: 消息提示
BtcDialog: 对话框
BtcNotification: 通知

## 组件选择决策

需要 CRUD？
  简单列表 → BtcCrud
  主从结构 → BtcMasterTableGroup
  复杂筛选 → BtcFilterTableGroup
  三级结构 → BtcDoubleLeftGroup

需要表单？
  弹窗表单 → BtcUpsert
  独立表单 → BtcForm
  
需要上传？
  → BtcUpload, BtcImportBtn

需要导出？
  → BtcExportBtn

## 查看组件

完整导出:
  cat packages/shared-components/src/index.ts

组件文档:
  http://localhost:5113（启动 docs-app）

## 常用组合

列表页:
  BtcCrud + BtcTable + BtcPagination

主从页:
  BtcMasterTableGroup（自动包含左右表格）

筛选页:
  BtcFilterTableGroup（自动包含筛选+表格）
