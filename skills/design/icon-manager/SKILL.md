---
name: icon-manager
description: 图标管理器，列出所有SVG图标、推荐图标、添加新图标
---

# 图标管理器

## 功能

- 列出所有可用 SVG 图标
- 按分类查找图标
- 推荐合适的图标
- 添加新图标

## 图标位置

packages/shared-components/src/assets/icons/

分类:
  - actions/: 操作类（add, delete, edit, search, export, import等）
  - navigation/: 导航类（home, menu, arrow等）
  - status/: 状态类（success, fail, warn, info等）
  - people/: 人员类（user, team, dept等）
  - data/: 数据类（chart, table, file等）
  - business/: 业务类（warehouse, product等）
  - system/: 系统类（settings, theme, lock等）
  - misc/: 其他

## 列出所有图标

  Get-ChildItem packages/shared-components/src/assets/icons -Recurse -Filter *.svg | Select-Object Name

## 使用图标

在 Vue 中:
  <BtcSvg name=\"add\" />
  <BtcSvg name=\"delete\" class=\"text-red-500\" />

在配置中:
  meta: { icon: 'document' }
  menu: { icon: 'warehouse' }

## 常用图标列表

操作: add, delete, edit, search, refresh, export, import, print, download, upload
导航: home, menu, back, arrow-left, arrow-right
状态: success, fail, warn, info, question
业务: warehouse, product, order, inventory, customer

完整列表（133个）:
  packages/shared-components/src/assets/icons/

## 添加新图标

1. 准备 SVG 文件（单色，去除 fill 属性）
2. 放入对应分类目录: packages/shared-components/src/assets/icons/{category}/
3. 命名规范: kebab-case（如 new-icon.svg）
4. 使用: <BtcSvg name=\"new-icon\" />

## SVG 优化

- 移除 fill 属性（改用 currentColor）
- 设置 viewBox=\"0 0 24 24\"
- 移除不必要的属性
- 压缩 SVG（使用 SVGO）

## 图标推荐

根据功能推荐:
  - 打印 → print
  - 导出 → export
  - 导入 → import
  - 仓库 → warehouse
  - 库位 → location
  - 盘点 → inventory
  - 报表 → chart, table
  - 文档 → document, file
