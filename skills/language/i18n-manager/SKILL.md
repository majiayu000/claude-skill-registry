---
name: i18n-manager
description: 国际化管理器，获取翻译文件、添加新key、检查冲突、推荐命名
---

# 国际化管理器

## 功能

- 获取模块的 i18n 配置
- 添加新的翻译 key
- 检查 key 命名冲突
- 推荐 key 命名规范

## 使用方式

查看模块 i18n:
  cat apps/admin-app/src/modules/test/config.ts | grep -A 20 'i18n:'

查看应用 i18n:
  cat apps/admin-app/src/locales/zh-CN.json

## i18n 配置位置

模块级（推荐）:
  apps/{app}/src/modules/{module}/config.ts

应用级:
  apps/{app}/src/locales/{lang}.json

## 添加新翻译

在模块 config.ts 中:
  export default {
    i18n: {
      'zh-CN': {
        'test.pageA.title': '页面A',
        'test.pageA.desc': '描述'
      },
      'en-US': {
        'test.pageA.title': 'Page A',
        'test.pageA.desc': 'Description'
      }
    }
  }

## 命名规范

格式: {module}.{feature}.{item}

示例:
  - test.pageA.title（页面标题）
  - test.pageA.table.code（表格列）
  - test.pageA.button.print（按钮）
  - test.pageA.dialog.title（对话框标题）

## 常用前缀

common: 通用文本
menu: 菜单项
title: 标题
button: 按钮
field: 字段
message: 提示信息
dialog: 对话框
table: 表格

## 检查冲突

  grep -r \"test.pageA.title\" apps/admin-app/src/modules/*/config.ts

## 合并到应用 i18n

  pnpm locale:merge
  pnpm locale:merge:all
