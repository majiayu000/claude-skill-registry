---
name: init-melos
description: Install and initialize Melos CLI for monorepo management. Use when user needs melos, wants to run melos bootstrap, or gets "melos: command not found". Triggers on "install melos", "init melos", "melos not found", "setup melos".
---

# 安装 Melos CLI

确保 Melos CLI 已安装并可用。

## 安装步骤

```bash
# 1. 检查是否已安装
command -v melos

# 2. 如果未安装，执行安装
dart pub global activate melos

# 3. 确保 PATH 包含 pub-cache/bin
export PATH="$PATH:$HOME/.pub-cache/bin"
```

## 验证

```bash
melos --version
```

## 初始化工作区

安装完成后，在工作区根目录执行：

```bash
melos bootstrap
```
