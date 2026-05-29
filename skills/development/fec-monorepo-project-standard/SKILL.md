---
name: fec-monorepo-project-standard
description: Use when creating, reviewing, or restructuring frontend monorepos with pnpm workspace, Turborepo, Nx, multi-package dependency boundaries, task orchestration, package naming, or package publishing; Chinese triggers include monorepo, workspace, 多包.
---

# Monorepo 项目规范

适用于使用 pnpm workspace、Turborepo 或 Nx 的多包前端仓库。

## Purpose

规范 Monorepo 项目的目录结构、依赖管理、任务编排和包发布流程，确保多包协作的构建效率和版本一致性。

## Procedure

1. 先确认仓库是否已使用 pnpm workspace、Turborepo 或 Nx，并沿用现有包命名与任务约定。
2. 将应用放在 `apps/`，共享库、配置和工具放在 `packages/` 或既有等价目录。
3. 内部依赖使用 `workspace:*`，通过依赖图驱动构建顺序。
4. 为 build、lint、test 配置可缓存、可并行的根任务。
5. 发布包前检查包边界、循环依赖、exports、peer dependencies 和版本策略。

## 工具选择

| 工具               | 适用 | 特点                       |
| ------------------ | ---- | -------------------------- |
| **pnpm workspace** | 基础 | 依赖提升、链接、脚本聚合   |
| **Turborepo**      | 推荐 | 缓存、并行、依赖图         |
| **Nx**             | 大型 | 增量构建、云缓存、插件生态 |

## 目录结构

### pnpm + Turborepo

```
├── package.json                # 根 package，workspace 配置
├── pnpm-workspace.yaml         # workspace 包列表
├── turbo.json                  # Turborepo 配置
│
├── apps/
│   ├── web/                    # 主应用
│   │   ├── package.json
│   │   └── ...
│   ├── admin/                  # 管理后台
│   └── docs/                   # 文档站
│
├── packages/
│   ├── ui/                     # 共享 UI 组件
│   │   ├── package.json
│   │   └── src/
│   ├── utils/                  # 工具函数
│   ├── config-eslint/         # 共享 ESLint 配置
│   └── config-typescript/     # 共享 TS 配置
│
└── tooling/                    # 构建/测试工具（可选）
    └── scripts/
```

### pnpm-workspace.yaml

```yaml
packages:
  - "apps/*"
  - "packages/*"
```

## 依赖管理

- 内部包使用 `workspace:*` 协议
- 根 `package.json` 统一部分依赖版本，子包可覆盖
- 禁止循环依赖，通过 `pnpm why` 检查

```json
{
  "dependencies": {
    "@repo/ui": "workspace:*",
    "@repo/utils": "workspace:*"
  }
}
```

## Turborepo 任务编排

```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "lint": {
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["^build"]
    }
  }
}
```

- `^build` 表示先执行依赖包的 build
- `outputs` 用于缓存命中判断

## Nx 任务编排

```json
{
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["{projectRoot}/dist"],
      "cache": true
    }
  }
}
```

## 包命名

- 内部包：`@org/package-name` 或 `@repo/package-name`
- 发布到 npm：遵循 `@scope/name` 规范

## Constraints

- 子包之间通过 `workspace:*` 引用，不发布到 npm 再安装
- 共享配置（ESLint、TS）放在 `packages/config-*`，子包 extends
- 构建顺序由依赖图决定，不手动指定无关依赖
- 根目录执行 `pnpm -r build` 或 `turbo run build` 时，所有包按序构建
- 禁止循环依赖，新增包时通过 `pnpm why` 检查依赖链

## Expected Output

- Monorepo 目录结构清晰（`apps/` 应用、`packages/` 共享包、`tooling/` 工具）
- `pnpm-workspace.yaml` 和 `turbo.json` / `nx.json` 配置正确
- 内部包使用 `workspace:*` 协议，无循环依赖
- 构建、lint、test 任务可通过根命令一键执行，缓存命中率高
