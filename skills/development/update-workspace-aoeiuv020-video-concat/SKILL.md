---
name: update-workspace
description: Update Dart/Flutter workspace configuration in pubspec.yaml. Use when user wants to add a module to workspace, fix workspace config, add resolution:workspace, or manage monorepo pubspec.yaml entries. Triggers on "update workspace", "add to workspace", "fix pubspec workspace", "resolution workspace".
---

# Update Workspace

更新 Dart/Flutter 单仓库 workspace 配置。

## 功能

1. 向子模块 `pubspec.yaml` 添加 `resolution: workspace`
2. 更新根目录 `pubspec.yaml` 的 `workspace:` 列表（自动排序、去重）

## Usage

```bash
dart run <skill_path>/scripts/update_workspace.dart <root_path> [module_path]
```

## 参数

- `root_path`（必填）：工作区根目录路径
- `module_path`（可选）：要添加的模块路径（绝对路径或相对于根目录的路径）

## Examples

```bash
# 仅整理根目录 workspace 配置
dart run <skill_path>/scripts/update_workspace.dart /path/to/workspace

# 添加新模块到 workspace
dart run <skill_path>/scripts/update_workspace.dart /path/to/workspace /path/to/workspace/packages/my_pkg
```

## What It Does

1. 验证目录存在性
2. 如果提供了模块路径，在 `environment:` 后添加 `resolution: workspace`
3. 解析根目录 `pubspec.yaml` 现有的 `workspace:` 条目
4. 添加新模块（如果提供），路径自动规范化为正斜杠
5. 排序后重建 `workspace:` 节
