---
name: cli-creator
description: 创建高质量 Node.js CLI 工具的完整指南。当用户需要构建命令行工具时使用:(1)创建新的 CLI 项目,(2)选择合适的框架和依赖,(3)实现 CLI 功能,(4)配置测试和打包,(5)应用 CLI 最佳实践
---

# CLI Creator

创建高质量、现代化的 Node.js CLI 工具。

## 概述

本技能提供从零开始创建专业级 CLI 工具的完整工作流,包括框架选择、项目初始化、功能实现、测试配置和打包分发。

## 快速开始 (5分钟创建最小化CLI)

```bash
# 使用本技能的初始化脚本
npx ts-node skills/cli-creator/scripts/init_cli.ts my-cli

# 进入项目目录
cd my-cli

# 运行 CLI
npx . --help
npx . --version
```

## 工作流程决策树

```
用户请求创建 CLI
│
├─ 步骤 1: 框架选择
│  ├─ 评估项目复杂度 (命令数量、交互需求、插件需求)
│  ├─ 参考 references/framework_comparison.md
│  └─ 推荐: Commander.js (默认) / oclif / Ink
│
├─ 步骤 2: 项目初始化
│  ├─ 运行 scripts/init_cli.ts 生成项目结构
│  ├─ 选择模板级别 (minimal/standard/advanced)
│  └─ 配置项目元数据 (名称、描述、版本)
│
├─ 步骤 3: 开发指导
│  ├─ 实现命令逻辑 (src/commands/)
│  ├─ 配置 UI 增强 (chalk, ora)
│  ├─ 添加配置管理 (cosmiconfig + zod)
│  └─ 参考 references/best_practices.md
│
├─ 步骤 4: 测试和打包
│  ├─ 配置测试 (vitest)
│  ├─ 运行 scripts/validate_cli.ts 验证
│  ├─ 参考 references/testing_strategies.md
│  └─ 参考 references/packaging_guide.md
│
└─ 步骤 5: 发布分发
   ├─ npm publish (推荐)
   ├─ npx 一键运行
   └─ 可选: Node.js SEA 单文件打包
```

## 核心脚本

### scripts/init_cli.ts

CLI 项目初始化主脚本。

**用法**:
```bash
npx ts-node skills/cli-creator/scripts/init_cli.ts <cli-name> [options]
```

**选项**:
- `--framework <name>`: 指定框架 (commander/oclif/yargs/ink/citty/cac)
- `--template <type>`: 模板级别 (minimal/standard/advanced)
- `--ui`: 包含 UI 库 (chalk + ora)
- `--config`: 包含配置管理 (cosmiconfig + zod)
- `--testing`: 包含测试配置 (vitest)

**示例**:
```bash
# 最小化 CLI (Commander.js)
npx ts-node skills/cli-creator/scripts/init_cli.ts my-tool

# 标准配置,包含 UI 和测试
npx ts-node skills/cli-creator/scripts/init_cli.ts my-tool --template standard --ui --testing

# 高级配置,oclif 框架
npx ts-node skills/cli-creator/scripts/init_cli.ts my-tool --framework oclif --template advanced

# React UI CLI (Ink)
npx ts-node skills/cli-creator/scripts/init_cli.ts my-tool --framework ink
```

### scripts/generate_project.ts

基于配置生成完整项目结构。

**自动调用**: 由 init_cli.ts 内部调用

### scripts/install_dependencies.ts

根据配置安装精确的依赖版本。

**自动调用**: 由 init_cli.ts 内部调用

### scripts/validate_cli.ts

验证生成的 CLI 项目完整性。

**用法**:
```bash
npx ts-node skills/cli-creator/scripts/validate_cli.ts <project-path>
```

**验证检查**:
- ✓ package.json 格式正确
- ✓ bin/run.js 可执行文件存在
- ✓ tsconfig.json 配置正确
- ✓ 依赖安装完整
- ✓ 可以运行 --help
- ✓ 可以运行 --version
- ✓ 测试可以运行

## 参考文档导航

### 框架选择

**何时读取**: 用户询问"哪个框架最好?"或需要框架对比时

```bash
# 搜索关键词
grep -r "framework comparison" skills/cli-creator/references/
grep -r "Commander.js vs oclif" skills/cli-creator/references/
```

**文件**: `references/framework_comparison.md`
- 框架选择决策树
- 详细对比表格 (学习曲线、包体积、TypeScript 支持)
- 推荐场景说明
- 每个框架的优缺点分析

### 最佳实践

**何时读取**: 实现 CLI 功能或改进用户体验时

```bash
# 搜索关键词
grep -r "UX principles" skills/cli-creator/references/
grep -r "POSIX" skills/cli-creator/references/
grep -r "error handling" skills/cli-creator/references/
```

**文件**: `references/best_practices.md`
- 用户体验原则 (渐进式披露、POSIX 兼容、彩色输出)
- 代码组织模式
- 命令设计模式
- 配置管理最佳实践
- 性能优化建议

### 依赖配置

**何时读取**: 选择和配置依赖时

```bash
# 搜索关键词
grep -r "chalk" skills/cli-creator/references/
grep -r "vitest" skills/cli-creator/references/
grep -r "dependencies" skills/cli-creator/references/
```

**文件**: `references/dependency_guide.md`
- 最小化依赖方案
- 完整功能方案
- 框架特定配置
- 依赖版本选择建议
- 安全性考虑

### 测试策略

**何时读取**: 配置测试或调试测试问题时

```bash
# 搜索关键词
grep -r "vitest" skills/cli-creator/references/
grep -r "test" skills/cli-creator/references/
grep -r "coverage" skills/cli-creator/references/
```

**文件**: `references/testing_strategies.md`
- 测试框架选择 (Vitest 推荐)
- 测试模式 (命令输出测试、单元测试、集成测试)
- 代码示例
- 覆盖率配置

### 打包分发

**何时读取**: 准备发布 CLI 时

```bash
# 搜索关键词
grep -r "npm publish" skills/cli-creator/references/
grep -r "SEA" skills/cli-creator/references/
grep -r "npx" skills/cli-creator/references/
```

**文件**: `references/packaging_guide.md`
- 分发方式对比 (npm、npx、Node.js SEA、nexe、Docker)
- 推荐方案: npm + npx
- package.json 配置
- 发布流程
- 高级: Node.js SEA 单文件

### 完整技术栈参考

**何时读取**: 需要深入技术细节或查阅完整库列表时

```bash
# 搜索关键词
grep -r "execa" skills/cli-creator/references/
grep -r "zod" skills/cli-creator/references/
grep -r "cosmiconfig" skills/cli-creator/references/
```

**文件**: `references/original_reference.md`
- 完整的 node-cli-skill.md 原始内容
- 所有技术栈和库的详细文档
- 优秀 CLI 项目参考
- 设计思路与最佳实践 (完整版)

## 框架支持策略

### 支持的框架

| 框架 | 默认 | 特点 | 推荐场景 |
|------|------|------|----------|
| **Commander.js** | ✅ | 简单、流行、社区成熟 | 中小型 CLI,快速开发 |
| **oclif** | - | 企业级、插件系统、自动文档 | 大型 CLI、插件化需求 |
| **Yargs** | - | 功能丰富、中间件支持 | 复杂参数验证 |
| **Ink** | - | React 组件化、富交互 | 现代 UI、交互式 CLI |
| **citty** | - | 轻量、现代 ESM | UnJS 生态 |
| **cac** | - | 极简、零依赖 | 超轻量级工具 |

### 框架选择决策树

```
项目复杂度评估:
├── 1-3 个简单命令 → Commander.js / cac
├── 3-10 个命令,中等复杂 → Commander.js / Yargs
├── 10+ 个命令,需要插件 → oclif
├── 富 UI/交互式 → Ink
└── 极简/零依赖追求 → cac / citty
```

## 模板级别

### Minimal

**特点**: ~5 文件,快速开始
**适用**: 学习、原型、简单脚本
**内容**:
- package.json (最小依赖)
- tsconfig.json
- src/index.ts (简单命令)
- bin/run.js

### Standard (推荐)

**特点**: ~15 文件,标准开发流程
**适用**: 大多数 CLI 项目
**内容**:
- package.json (包含测试、lint)
- tsconfig.json
- vitest.config.ts
- biome.json
- src/commands/init.ts
- src/lib/config.ts
- src/lib/logger.ts
- test/basic.test.ts
- bin/run.js

### Advanced

**特点**: ~25 文件,企业级质量
**适用**: 大型项目、团队协作
**内容**:
- 完整的配置系统 (cosmiconfig + zod)
- 错误处理体系
- 多命令组织
- 完整测试套件
- 构建和打包配置

## 常见使用场景

### 场景 1: 创建新的 CLI 工具

```
用户: "帮我创建一个 CLI 工具,叫 file-organizer"
Claude:
  1. 收集配置信息 (名称、描述、功能)
  2. 推荐框架 (默认 Commander.js)
  3. 运行 init_cli.ts
  4. 生成项目结构
  5. 安装依赖
  6. 提供使用指南
```

### 场景 2: 框架选择建议

```
用户: "Commander.js 和 oclif 哪个更好?"
Claude:
  1. 加载 framework_comparison.md
  2. 提供对比分析
  3. 根据用户需求推荐
```

### 场景 3: CLI 开发问题

```
用户: "我的 CLI 测试失败了"
Claude:
  1. 加载 testing_strategies.md
  2. 诊断问题
  3. 提供解决方案
```

### 场景 4: 添加功能到现有 CLI

```
用户: "我想在我的 CLI 中添加配置文件支持"
Claude:
  1. 加载 dependency_guide.md
  2. 推荐 cosmiconfig + zod
  3. 提供实现示例
```

## 技术栈默认值

### 核心依赖

```json
{
  "dependencies": {
    "commander": "^12.0.0",
    "chalk": "^5.3.0",
    "ora": "^8.0.0"
  },
  "devDependencies": {
    "typescript": "^5.6.0",
    "tsx": "^4.19.0",
    "vitest": "^2.1.0",
    "@biomejs/biome": "^1.9.0",
    "@types/node": "^22.0.0"
  }
}
```

### 可选依赖

```json
{
  "dependencies": {
    "cosmiconfig": "^9.0.0",
    "zod": "^3.23.0",
    "execa": "^9.5.0"
  }
}
```

## 目录结构示例

```
my-cli/
├── src/
│   ├── commands/         # 命令实现
│   │   ├── init.ts
│   │   └── build.ts
│   ├── lib/              # 共享库
│   │   ├── config.ts     # 配置管理
│   │   ├── logger.ts     # 日志工具
│   │   └── api.ts        # API客户端
│   ├── utils/            # 工具函数
│   └── index.ts          # 入口
├── test/                 # 测试文件
├── bin/
│   └── run.js            # 可执行文件
├── package.json
├── tsconfig.json
├── vitest.config.ts
└── README.md
```

## 开发命令

生成的 CLI 项目包含以下 npm scripts:

```json
{
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsdown src/index.ts --format cjs,esm",
    "test": "vitest",
    "test:coverage": "vitest run --coverage",
    "lint": "biome check .",
    "format": "biome format . --write",
    "typecheck": "tsc --noEmit"
  }
}
```

## 质量检查清单

在发布 CLI 前,确保:

- [ ] 可以运行 `--help` 显示帮助信息
- [ ] 可以运行 `--version` 显示版本号
- [ ] 支持 `NO_COLOR` 环境变量
- [ ] 错误信息清晰有用
- [ ] 测试覆盖率 > 80%
- [ ] TypeScript 编译无错误
- [ ] 通过 lint 检查
- [ ] README.md 包含使用示例
- [ ] package.json 包含正确的 bin 字段
