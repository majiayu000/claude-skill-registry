---
name: auto-vitepress
description: 自动为当前项目生成或更新 VitePress 文档网站。
---

# 自动生成 VitePress 文档

## 目标
为当前项目在 `/docs` 目录下创建或更新一个 VitePress 文档网站。此过程应具备智能化，能够处理依赖安装、目录扫描、配置生成和文件创建等任务。

## 指令

### 步骤 1: 环境准备

1.  **检查 `package.json`**: 读取项目根目录下的 `package.json` 文件。如果文件不存在，则新建一个满足 VitePress 需求的依赖配置文件，然后继续执行。
2.  **检查并安装依赖**:
    *   分析 `package.json` 的 `devDependencies` 字段。
    *   检查 `vitepress` 和 `vue` 是否已存在。
    *   如果任一依赖缺失，使用 `npm install -D vitepress vue` 命令进行安装。
3.  **创建目录结构**:
    *   检查项目根目录下是否存在 `/docs/.vitepress` 目录。
    *   如果不存在，请创建它。

### 步骤 2: 智能扫描与侧边栏生成

1.  **查找并读取 README.md**:
    *   在项目根目录查找 `README.md` 文件。
    *   如果存在，解析其内容作为文档基础结构参考。
    *   分析标题、章节结构和内容，用于构建侧边栏和首页。
2.  **分析项目结构和功能**:
    *   根据 README 的内容分析项目的主要功能模块。
    *   识别项目中的核心概念、组件、工具函数等。
    *   根据这些分析结果生成文档结构，而不是直接映射代码文件。
3.  **构建侧边栏对象**:
    *   基于 README 的章节结构和项目功能分析来生成侧边栏。
    *   将主要功能模块映射为可折叠的分组，格式为 `{ text: '功能模块名', collapsed: false, items: [...] }`。
    *   为每个功能模块创建对应的文档页面链接，格式为 `{ text: '功能说明', link: '/模块/说明' }`。
    *   如果 README 中有"快速开始"、"使用方法"、"API 参考"等章节，将它们映射为侧边栏项。
    *   将这个过程的产物构建成一个符合 VitePress `sidebar` 格式的 JavaScript 数组。

### 步骤 3: 生成或更新配置文件

1.  **检查 `config.js`**: 检查 `/docs/.vitepress/config.js` 文件是否存在。
2.  **如果 `config.js` 不存在**:
    *   读取 `package.json` 的 `name`、`description`、`author` 和 `repository` 字段。
    *   从 `package.json` 的 `repository` 字段提取 GitHub 仓库链接（如果存在）。
    *   从 `package.json` 的 `author` 字段提取作者信息（如果存在），用于版权信息。
    *   读取项目根目录的 `LICENSE` 文件确定许可证类型，如果不存在则默认使用 MIT。
    *   检查项目根目录是否存在 logo 图片或图标（如 `logo.png`、`logo.svg`、`icon.png`、`icon.svg` 等），如果存在则使用，否则使用 VitePress 官方默认 logo（VPLogo）。
    *   读取 `README.md` 的内容作为首页的基础内容（如果存在）。
    *   创建一个新的 `config.js` 文件，内容如下模板所示，并将上一步生成的 `sidebar` 对象填充进去。
      ```javascript
      import { defineConfig } from 'vitepress'

      export default defineConfig({
        title: '项目名称',
        description: '项目描述',
        themeConfig: {
          // Logo（如果找到图片则设置，否则使用 VitePress 官方默认 logo）
          logo: '/logo 路径.png', // 或不设置此属性使用默认 logo
          // 顶部导航
          nav: [
            { text: '首页', link: '/' },
            { text: '指南', link: '/guide/intro' },
            {
              text: 'GitHub',
              link: 'https://github.com/username/repo'
            }
          ],
          // 侧边栏
          sidebar: [/* 在这里填充侧边栏对象 */],
          // 底部信息
          footer: {
            message: '基于 许可证类型 许可发布',
            copyright: `版权所有 © ${new Date().getFullYear()} 作者名`
          },
          // 显示文档最后更新时间
          lastUpdated: {
            text: '最后更新于',
            formatOptions: {
              dateStyle: 'full',
              timeStyle: 'medium'
            }
          }
        }
      })
      ```
3.  **如果 `config.js` 已存在**:
    *   读取文件内容。
    *   使用正则表达式或字符串替换的方式，安全地更新 `themeConfig` 中的 `sidebar` 字段。**注意：只更新 `sidebar`，不要覆盖用户的其他配置。**
    *   如果 `themeConfig.nav` 不存在，则添加基础的顶部导航配置。
    *   如果 `themeConfig.footer` 不存在，则添加底部版权信息配置。
    *   如果 `themeConfig.lastUpdated` 不存在，则添加文档最后更新时间配置。
    *   如果 `themeConfig.logo` 不存在，则检查项目根目录是否存在 logo 图片或图标，如果存在则设置，否则使用 VitePress 官方默认 logo（VPLogo）。

### 步骤 4: 创建文档页面和 NPM 脚本

1.  **根据功能生成文档页面**:
    *   遍历 `sidebar` 对象中的所有链接。
    *   对于每一个功能模块链接，检查对应的文件（如 `/docs/模块/说明.md`）是否存在。
    *   如果不存在，根据 README 的相关内容和项目功能分析来生成文档内容。
    *   文档内容应包含该功能模块的详细说明、使用方法、示例代码等。
    *   而不是简单的占位标题，要生成有实际价值的使用文档。
2.  **创建首页**:
    *   检查 `/docs/index.md` 是否存在。
    *   如果不存在，优先使用 `README.md` 的内容作为首页内容。
    *   如果 `README.md` 不存在，则使用 `package.json` 的 `name` 和 `description` 生成一个简单的首页。
    *   首页模板如下（注意 hero 区域只包含 `name` 和 `tagline`，不包含 `text`）:
      ```markdown
      ---
      layout: home

      hero:
        name: 项目名称
        tagline: 项目描述
        actions:
          - theme: brand
            text: 快速开始
            link: /guide/how-to-use

      features:
        - title: 特性 1
          details: 特性 1 的描述
        - title: 特性 2
          details: 特性 2 的描述
      ---
      ```
3.  **添加 NPM 脚本**:
    *   读取 `package.json`。
    *   检查 `scripts` 字段中是否已存在 `docs:dev` 和 `docs:build`。
    *   如果不存在，则添加它们：
      ```json
      "scripts": {
        "docs:dev": "vitepress dev docs",
        "docs:build": "vitepress build docs"
      }
      ```
    *   将更新后的内容写回 `package.json`。

## 总结
完成以上所有步骤后，向用户报告任务完成，并提示他们可以通过运行 `npm run docs:dev` 来启动文档服务器。
