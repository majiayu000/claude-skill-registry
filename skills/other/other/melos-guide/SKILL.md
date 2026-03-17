---
name: melos-guide
description: Guide for Melos monorepo management in Flutter/Dart projects. Use when user asks about melos setup, melos commands, workspace scripts, or monorepo workflows. Triggers on "melos bootstrap", "run melos script", "setup melos", "workspace management".
---

# Melos Guide

Melos 是 Flutter/Dart 单仓库 (monorepo) 管理工具。

## 初始化

```bash
# 安装 melos CLI（如未安装）
dart pub global activate melos

# 确保 PATH 包含 pub-cache/bin
export PATH="$PATH:$HOME/.pub-cache/bin"

# 初始化工作区依赖
melos bootstrap
```

## 预定义脚本

| 命令 | 说明 |
|------|------|
| `melos outdated` | 检查过期依赖 |
| `melos upgrade` | 升级依赖 |
| `melos gen` | 代码生成（仅对依赖 build_runner 的包） |
| `melos analyze` | 静态分析 |
| `melos fix` | 自动修复 |
| `melos sort` | 排序 import |
| `melos precommit` | 提交前检查：fix + format + sort |
| `melos test` | 运行测试（仅对有 test/ 目录的包） |

## 常用命令

```bash
melos run --help              # 查看所有脚本
melos clean && melos bootstrap # 清理并重新初始化
melos list                    # 列出所有包
melos exec --scope="pkg" -- cmd # 对特定包执行命令
```

## 工作区配置

根目录 `pubspec.yaml`：
```yaml
workspace:
  - apps/*
  - packages/*
```

子包 `pubspec.yaml`：
```yaml
resolution: workspace
```
