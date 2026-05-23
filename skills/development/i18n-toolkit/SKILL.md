---
name: i18n-toolkit
description: 国际化工具包，翻译检查、合并、新增、验证，基于扁平化i18n结构
---

# 国际化工具包

## 何时使用

当你需要：管理翻译文件、添加新翻译、检查缺失翻译、合并i18n文件

## 项目i18n架构

扁平化结构:
  - 所有翻译key使用点号分隔: 'module.page.field'
  - 每个模块在config.ts中定义i18n
  - 自动扫描和合并到locales/{lang}.json

示例:
  apps/admin-app/src/modules/access/config.ts:
    i18n: {
      'zh-CN': {
        'access.menu.title': '权限管理',
        'access.roles.title': '角色列表'
      },
      'en-US': {
        'access.menu.title': 'Access Control',
        'access.roles.title': 'Role List'
      }
    }

## 常用命令

检查翻译完整性:
  pnpm i18n:check:completeness
  # 检查所有应用的中英文翻译是否完整

查找重复翻译:
  pnpm i18n:check:duplicates
  # 检测重复的翻译key

检查所有:
  pnpm i18n:check:all

合并翻译文件:
  pnpm locale:merge
  # 合并当前应用的i18n到locales/*.json

合并所有应用:
  pnpm locale:merge:all

检查i18n key格式:
  pnpm check:i18n
  pnpm check:i18n:apps  # 只检查apps目录

## 添加新翻译

步骤:
1. 在模块的config.ts中添加i18n对象
2. 使用扁平化key命名: 'module.feature.item'
3. 同时提供中英文翻译
4. 运行 pnpm locale:merge 合并

示例:
  export default {
    i18n: {
      'zh-CN': {
        'warehouse.menu.title': '仓库管理',
        'warehouse.location.add': '新增库位'
      },
      'en-US': {
        'warehouse.menu.title': 'Warehouse',
        'warehouse.location.add': 'Add Location'
      }
    }
  }

## 翻译命名规范

格式: {module}.{feature}.{item}

示例:
  - access.menu.title（权限菜单标题）
  - access.roles.list（角色列表）
  - warehouse.location.name（库位名称）
  - common.button.save（通用保存按钮）

## 使用翻译

在Vue组件中:
  {{ \('access.menu.title') }}

在TypeScript中:
  import { t } from 'vue-i18n'
  const title = t('access.menu.title')

## ESLint规则

项目配置了i18n相关的ESLint规则:
  - no-chinese-in-template: 禁止模板中硬编码中文
  - require-i18n-key: 要求使用i18n key
  - i18n-key-format: key格式验证

## 常见问题

Q: 翻译key命名规范?
A: {module}.{feature}.{item}，全小写，点号分隔

Q: 如何检查缺失的英文翻译?
A: pnpm i18n:check:completeness

Q: 翻译不生效?
A: 运行 pnpm locale:merge 合并，然后重启开发服务器

Q: ESLint报错硬编码中文?
A: 使用 \('key') 替换硬编码文本

## 相关文档

- docs/guides/i18n/flat-structure.md
- docs/guides/i18n/best-practices.md
- docs/guides/i18n/eslint-rules.md
