---
name: turborepo
description: "Turborepo monorepo 构建系统指导。触发词：turbo.json、task pipelines、dependsOn、caching、remote cache、turbo CLI、--filter、--affected、CI optimization、environment variables、internal packages、monorepo structure/best practices、boundaries。"
license: MIT
---

# Turborepo 技能

JavaScript/TypeScript monorepo 的构建系统。Turborepo 缓存任务输出并根据依赖图并行运行任务。

## 重要：包任务，非根任务

**不要创建根任务。始终创建包任务。**

创建任务/脚本/管道时，必须：
1. 将脚本添加到每个相关包的 `package.json`
2. 在根 `turbo.json` 中注册任务
3. 根 `package.json` 仅通过 `turbo run ` 委托

**不要**将任务逻辑放在根 `package.json` 中。这会破坏 Turborepo 的并行化。

## 次要规则：`turbo run` vs `turbo`

**当命令写入代码时始终使用 `turbo run`**：
```json
// package.json - 始终 "turbo run"
{ "scripts": { "build": "turbo run build" } }
```

**简写 `turbo ` 仅用于一次性终端命令**，由人类或代理直接输入。绝不将 `turbo build` 写入 package.json、CI 或脚本。

## 快速决策树

**「我需要配置任务」**：定义任务依赖、Lint/检查类型（并行+缓存）→ 使用 Transit Nodes 模式、指定构建输出、处理环境变量、设置 dev/watch 任务、包特定配置、全局设置（cacheDir、daemon）。  
**「我的缓存不工作」**：任务运行但输出未恢复 → 缺少 `outputs` 键、缓存意外未命中 → 参考 gotchas、需要调试哈希输入 → 使用 --summarize 或 --dry、想完全跳过缓存 → 使用 --force 或 cache: false、远程缓存不工作 → 参考 remote-cache、环境导致未命中 → 参考环境 gotchas。  
**「我想仅运行更改的包」**：更改的包+依赖（推荐）→ `turbo run build --affected`、自定义基础分支 → `--affected --affected-base=origin/develop`、手动 git 比较 → `--filter=...[origin/main]`。  
**「我想过滤包」**：仅更改的包 → `--affected`、按包名 → `--filter=web`、按目录 → `--filter=./apps/*`、包+依赖 → `--filter=web...`、包+被依赖 → `--filter=...web`。  
**「环境变量不工作」**：运行时变量不可用 → 严格模式过滤（默认）、缓存命中但环境错误 → 变量不在 `env` 键中、.env 更改不导致重建 → .env 不在 `inputs` 中、CI 变量缺失 → 参考环境 gotchas、框架变量（NEXT_PUBLIC_*）→ 通过推断自动包含。  
**「我需要设置 CI」**：GitHub Actions → 参考 github-actions、Vercel 部署 → 参考 vercel、CI 中的远程缓存 → 参考 remote-cache、仅构建更改的包 → `--affected` 标志、跳过不必要构建 → turbo-ignore。  
**「我想在开发期间监视更改」**：更改时重新运行任务 → `turbo watch`、带依赖的 dev 服务器 → 使用 `with` 键、依赖更改时重启 dev 服务器 → 使用 `interruptible: true`、持久 dev 任务 → 使用 `persistent: true`。

## 关键反模式

**在代码中使用 `turbo` 简写**：`turbo run` 在 package.json 脚本与 CI 管道中推荐。简写 `turbo ` 用于交互式终端使用。  
**根脚本绕过 Turbo**：根 `package.json` 脚本必须委托给 `turbo run`，不直接运行任务。  
**使用 `&&` 链接 Turbo 任务**：不要用 `&&` 链接 turbo 任务。让 turbo 编排。  
**`prebuild` 脚本手动构建依赖**：如 `prebuild` 手动构建其他包，绕过 Turborepo 依赖图。修复：如果依赖已声明，移除 `prebuild` 脚本，Turbo 的 `dependsOn: ["^build"]` 自动处理；如果依赖未声明，添加依赖到 package.json，然后移除 `prebuild` 脚本。  
**过度宽泛的 `globalDependencies`**：`globalDependencies` 影响所有包中的所有任务。要具体。  
**重复任务配置**：查找跨任务重复的配置，可折叠。Turborepo 支持共享配置模式。使用 `globalEnv` 与 `globalDependencies` 用于共享配置。  
**使用 `--parallel` 标志**：`--parallel` 标志绕过 Turborepo 依赖图。如果任务需要并行执行，正确配置 `dependsOn`。  
**根 turbo.json 中的包特定任务覆盖**：当多个包需要不同任务配置时，使用**包配置**（每个包中的 `turbo.json`）而非用 `package#task` 覆盖使根 `turbo.json` 混乱。  
**在 `inputs` 中使用 `../` 遍历出包**：不要使用相对路径如 `../` 引用包外文件。使用 `$TURBO_ROOT$` 代替。  
**缺少文件产生任务的 `outputs`**：在标记缺少 `outputs` 前，检查任务实际产生什么。仅当任务产生应被缓存的文件时标记。  
**`^build` vs `build` 混淆**：`^build` = 在依赖中先运行构建（此包导入的其他包），`build`（无 ^）= 在同一包中先运行构建，`pkg#task` = 特定包的任务。  
**环境变量未哈希**：如果 `API_URL` 更改不会导致重建，在 `env` 中添加它。  
**`.env` 文件不在 Inputs 中**：Turbo 不加载 `.env` 文件—你的框架加载。但 Turbo 需要知道更改：在 `inputs` 中包含 `.env` 文件。  
**Monorepo 中的根 `.env` 文件**：根 `.env` 文件是反模式—即使对于小 monorepo 或启动模板。它创建包之间的隐式耦合。正确：`.env` 文件在需要它们的包中。

## 常见任务配置

**标准构建管道**：`build` 有 `dependsOn: ["^build"]` 与 `outputs`，`dev` 有 `cache: false` 与 `persistent: true`。  
**带 `^dev` 模式的 Dev 任务**（用于 `turbo watch`）：根 `turbo.json` 中 `dev` 有 `dependsOn: ["^dev"]` 与 `persistent: false`，包 `turbo.json` 覆盖为 `persistent: true`。  
**用于并行任务与缓存失效的 Transit Nodes**：某些任务可并行运行（不需要依赖的构建输出）但必须在依赖源代码更改时失效缓存。Transit Nodes 解决两者：创建 `transit` 任务有 `dependsOn: ["^transit"]`，`my-task` 有 `dependsOn: ["transit"]`。  
**带环境变量**：使用 `globalEnv`、`globalDependencies`、任务级 `env`。

## 参考索引

配置（turbo.json 概览、包配置、任务配置、全局选项、gotchas）、缓存（缓存工作原理、远程缓存、gotchas）、环境变量（env、globalEnv、passThroughEnv、模式、gotchas）、过滤（--filter 语法概览、常见过滤模式）、CI/CD（一般 CI 原则、GitHub Actions 完整设置、Vercel 部署、模式）、CLI（turbo run 基础、命令与标志）、最佳实践（monorepo 最佳实践概览、仓库结构、创建内部包、依赖管理）、Watch 模式（turbo watch、可中断任务、dev 工作流）、边界（实验性：强制执行包隔离、基于标签的依赖规则）。

## 来源文档

基于 Turborepo 官方文档：https://turborepo.dev/docs
