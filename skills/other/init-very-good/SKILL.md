---
name: init-very-good
description: Install Very Good CLI for Flutter project tooling. Use when user needs very_good_cli, wants to use Very Good templates, or gets "very_good: command not found". Triggers on "install very_good", "init very good", "very good cli", "setup very_good".
---

# 安装 Very Good CLI

确保 very_good_cli 已安装并可用。

## 安装步骤

```bash
# 1. 检查是否已安装
command -v very_good

# 2. 如果未安装，执行安装
dart pub global activate very_good_cli

# 3. 确保 PATH 包含 pub-cache/bin
export PATH="$PATH:$HOME/.pub-cache/bin"
```

## 验证

```bash
very_good --version
```
