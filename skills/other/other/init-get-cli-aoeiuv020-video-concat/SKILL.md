---
name: init-get-cli
description: Install GetX CLI for Flutter GetX framework scaffolding. Use when user needs get_cli, wants to generate GetX pages/controllers, or gets "get_cli: command not found". Triggers on "install get_cli", "init get", "getx cli", "setup get_cli".
---

# 安装 GetX CLI

确保 get_cli 已安装并可用。

## 安装步骤

```bash
# 1. 检查是否已安装
command -v get_cli

# 2. 如果未安装，从 git 源安装
dart pub global activate -s git https://github.com/jonataslaw/get_cli

# 3. 确保 PATH 包含 pub-cache/bin
export PATH="$PATH:$HOME/.pub-cache/bin"
```

## 验证

```bash
get_cli --version
```
