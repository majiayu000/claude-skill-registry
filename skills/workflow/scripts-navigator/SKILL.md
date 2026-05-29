---
name: scripts-navigator
description: Scripts 架构导航器（v1.0.10重构后），脚本分类、位置、常用脚本速查
---

# Scripts 导航器

## 何时使用

当你需要：查找脚本、运行脚本、理解scripts架构、了解脚本功能

## Scripts 新架构（v1.0.10）

scripts/
├── bin/                # 统一命令入口
│   ├── build.js        # node scripts/bin/build.js cdn system
│   └── dev.js
├── commands/           # 具体命令实现
│   ├── build/          # 构建脚本
│   ├── dev/            # 开发脚本
│   ├── test/           # 测试脚本
│   ├── check/          # 检查脚本
│   ├── tools/          # 工具脚本
│   ├── release/        # 发布脚本
│   └── handlers/       # 命令处理器
├── utils/              # 公共工具
│   ├── logger.mjs      # 日志工具
│   ├── path-helper.mjs # 路径工具
│   ├── monorepo-helper.mjs  # monorepo工具
│   ├── turbo-helper.mjs     # turbo封装
│   └── shell-helper.mjs     # shell执行
├── config/             # 配置文件
│   ├── apps.config.js
│   ├── build.config.js
│   └── deploy.config.js
├── shell/              # Shell脚本
│   ├── deploy/
│   └── utils/
└── archive/            # 归档的过时脚本

## 常用脚本速查

构建脚本:
  scripts/commands/build/cdn-build.mjs      # CDN构建
  scripts/commands/build/dist-build.mjs     # Dist构建
  scripts/commands/build/preview-build.mjs  # 预览构建

开发脚本:
  scripts/commands/dev/dev-all.mjs          # 启动多应用
  scripts/commands/dev/dev-with-check.mjs   # 带检查启动

测试脚本:
  scripts/commands/test/deployment-test.mjs # 部署测试

检查脚本:
  scripts/commands/check/check-circular-deps.mjs  # 循环依赖
  scripts/commands/check/check-i18n-keys.js       # i18n检查

发布脚本:
  scripts/commands/release/push.mjs         # 发布推送（支持--auto）
  scripts/commands/release/version.mjs      # 版本管理

工具脚本:
  scripts/commands/tools/turbo.js           # Turbo封装
  scripts/commands/tools/clean-vite-cache.mjs    # 清理Vite缓存
  scripts/commands/tools/clean-cache.mjs         # 清理所有缓存
  scripts/commands/tools/locale-merge.mjs        # 合并i18n
  scripts/commands/tools/create-app-cli.mjs      # 创建应用
  scripts/commands/tools/update-changelog.mjs    # 更新CHANGELOG
  scripts/commands/tools/upload-app-to-cdn.mjs   # 上传到CDN

部署Shell脚本:
  scripts/shell/utils/build-and-push-local.sh      # 构建推送
  scripts/shell/utils/deploy-static.sh             # 静态部署
  scripts/shell/utils/build-deploy-incremental-k8s.sh  # K8s增量部署

## 公共工具使用

logger.mjs:
  import { logger } from '../../utils/logger.mjs'
  logger.info('消息')

path-helper.mjs:
  import { getRootDir } from '../../utils/path-helper.mjs'
  const rootDir = getRootDir()

monorepo-helper.mjs:
  import { getAllApps, getAppConfig } from '../../utils/monorepo-helper.mjs'

turbo-helper.mjs:
  import { runTurbo } from '../../utils/turbo-helper.mjs'
  await runTurbo(['run', 'build', '--filter=admin-app'])

## 运行脚本

直接运行:
  node scripts/commands/build/cdn-build.mjs system
  node scripts/commands/release/push.mjs --auto --version=1.0.11

通过package.json:
  pnpm build-cdn:system
  pnpm release:push

## 常见问题

Q: 脚本在哪个目录?
A: 新架构下都在 scripts/commands/{category}/

Q: 如何运行类型检查?
A: pnpm type-check:all 或 node scripts/commands/type-check.mjs

Q: 清理缓存脚本在哪?
A: scripts/commands/tools/clean-vite-cache.mjs

Q: 发布脚本怎么用?
A: node scripts/commands/release/push.mjs --auto --version=1.0.11
