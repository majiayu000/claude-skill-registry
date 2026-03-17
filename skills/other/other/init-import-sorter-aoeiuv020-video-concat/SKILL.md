---
name: init-import-sorter
description: Install import_sorter for Dart import sorting. Use when user needs import sorting, wants to sort imports, or gets "import_sorter not found". Triggers on "install import_sorter", "init import sorter", "sort imports", "setup import_sorter".
---

# 安装 Import Sorter

确保 import_sorter 已安装并可用。使用支持 pub workspaces 的修复版本。

## 安装步骤

```bash
# 1. 检查是否已安装
dart pub global list | grep import_sorter

# 2. 如果未安装，从修复分支安装（支持 monorepo pub workspaces）
dart pub global activate --source git https://github.com/myConsciousness/import_sorter.git --git-ref fix/monorepo-pub-workspaces
```

## 使用

```bash
# 对单个文件排序
dart pub global run import_sorter --no-comments

# 通过 melos 对所有包排序
melos sort
```
