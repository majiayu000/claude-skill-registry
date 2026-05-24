---
name: vite-dep-check
description: Vite 项目依赖版本检查工具。检查依赖是否过时、显示版本对比、标记更新类型、提供 Vite 生态兼容性建议。当用户需要检查 Vite 项目依赖版本、查找过时依赖、获取升级建议时使用此技能。
---

# Vite Dependency Version Check

检查 Vite 项目的依赖版本状态，提供升级建议和兼容性提示。

## 检查流程

1. **读取 package.json** - 获取当前依赖列表
2. **查询最新版本** - 使用 npm outdated 或 npm-check-updates
3. **分析更新类型** - 标记 major/minor/patch
4. **兼容性检查** - Vite 生态特殊依赖提示
5. **生成报告** - 输出结构化结果和升级命令

## 快速检查命令

```bash
# 查看过时依赖
npm outdated

# 详细 JSON 格式
npm outdated --json

# 使用 ncu 检查（更详细）
npx npm-check-updates
```

## 更新类型说明

| 类型 | 示例 | 风险 | 说明 |
|------|------|------|------|
| 🔴 Major | 4.x → 5.x | 高 | 可能有breaking changes |
| 🟡 Minor | 4.1→ 4.2 | 中 | 新功能，通常兼容 |
| 🟢 Patch | 4.1.0 → 4.1.1 | 低 | Bug 修复 |

## Vite 生态核心依赖

| 依赖 | 说明 | 注意事项 |
|------|------|----------|
| vite | 构建工具核心 | 大版本升级需检查插件兼容性 |
| @vitejs/plugin-vue | Vue 插件 | 需匹配 Vue 版本 |
| @vitejs/plugin-react | React 插件 | 需匹配 React 版本 |
| vite-plugin-* | 社区插件 | 检查是否支持当前 Vite 版本 |

## 检查脚本

```bash
#!/bin/bash
# 完整依赖检查

echo "=== 当前依赖版本 ==="
cat package.json | grep -A 100 '"dependencies"' | head -50

echo ""
echo "=== 过时依赖检查 ==="
npm outdated

echo ""
echo "=== 安全漏洞检查 ==="
npm audit --summary
```

## 输出格式

```markdown
## 依赖版本检查报告

### 📊 概览
- 总依赖数：X
- 需更新：Y
- 安全问题：Z

### 🔴 Major更新（需谨慎）
| 包名 | 当前版本 | 最新版本 | 说明 |
|------|----------|----------|------|
| vite | 4.5.0 | 5.2.0 | [查看迁移指南] |

### 🟡 Minor 更新（建议更新）
| 包名 | 当前版本 | 最新版本 |
|------|----------|----------|
| vue | 3.3.0 | 3.4.0 |

### 🟢 Patch 更新（安全更新）
| 包名 | 当前版本 | 最新版本 |
|------|----------|----------|
| axios | 1.6.0 | 1.6.2 |

### 📦 升级命令
# 安全更新（仅 patch）
npm update

# 更新指定包
npm install vite@latest
```

## 兼容性提示

### Vite 5.x 要求
- Node.js >= 18
- 部分插件需更新到兼容版本

### 常见兼容问题
- `@vitejs/plugin-vue` 需要 `vue >= 3.2.25`
- `@vitejs/plugin-react` 需要 `react >= 17`
- `vite-plugin-pwa` 不同版本对应不同 Vite 版本

## 最佳实践

1. **先更新 patch** - 风险最低
2. **测试后再更新 minor** - 运行测试确认
3. **major 单独处理** - 阅读迁移指南，逐个升级
4. **锁定版本** - 生产环境使用 package-lock.json
5. **定期检查** - 建议每月检查一次