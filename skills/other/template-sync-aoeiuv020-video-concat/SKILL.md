---
name: template-sync
description: 将模板仓库的更新同步到基于模板创建的项目中。当用户要求同步/合并模板更新、升级模板、或拉取模板最新改动时使用。
---

# Template Sync

将 `flutter_melos_template` 的更新同步到派生项目中。

## 使用方法

在派生项目目录下执行：

```bash
dart run <skill_path>/scripts/sync_template.dart --template <template_repo_path> [--template-commit <sha>]
```

## 参数

| 参数 | 说明 |
|------|------|
| `--template` / `-t` | 模板仓库路径或 URL（可选，默认从 `.env` 的 `TEMPLATE_REPO` 读取） |
| `--template-commit` / `-c` | 派生时对应的模板 commit SHA（可选，不填则按时间自动匹配） |
| `--dry-run` | 只显示操作计划，不执行 |

## 工作原理

1. 自动获取当前项目的初始 commit
2. 确定模板基准版本（用户指定或按时间匹配）
3. 添加模板为 git remote
4. 通过 `git replace --graft` 建立祖先关系
5. 正常 `git merge` 合并模板更新
6. 遇到冲突时列出冲突文件，尝试自动解决后提交；无法解决的告知用户
