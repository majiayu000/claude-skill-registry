---
name: python_env
description: USE WHEN you need to create, activate, or manage Python virtual environments (venv/virtualenv); install dependencies in isolation; run scripts or tests in controlled environments; or prepare reproducible runtime environments for CI/CD.
---

## 概要（精简）

本技能用于：
- 在本地或 CI 中创建、准备并使用 Python 虚拟环境（venv/virtualenv）。
- 以隔离环境安装依赖（requirements.txt / pyproject.toml / constraints.txt）。

## 何时使用本技能

- 需要为运行脚本或测试创建隔离环境
- 在项目中安装依赖且希望可复现安装
- 需要在无破坏主系统 Python 的情况下运行临时代码

## 快速操作（推荐使用 scripts 下的工具）

1. 创建虚拟环境（示例，会打印激活命令）：

```bash
python3 -m venv /path/to/venv
# 或使用脚本：
python skills/python_env/scripts/create_venv.py --path /path/to/venv
```

2. 激活（bash/zsh）：

```bash
source /path/to/venv/bin/activate
```

3. 在虚拟环境中安装依赖：

```bash
/path/to/venv/bin/pip install -r requirements.txt
# 或使用脚本：
python skills/python_env/scripts/install_requirements.py --venv /path/to/venv --requirements requirements.txt
```

4. 运行脚本或测试：

```bash
source /path/to/venv/bin/activate && python your_script.py
```

## 脚本（已包含）

- `scripts/create_venv.py` — 创建 venv，并打印适用于常见 shell 的激活命令
- `scripts/install_requirements.py` — 在指定 venv 中安装 requirements.txt 或单个包

## 额外说明

- 支持的替代方案：`conda`、`poetry`、`pipx`。当使用这些工具时，只需在 SKILL 触发时说明所用工具，脚本不会替换这些工作流。
- 建议项目维护 `requirements.txt` 或 `pyproject.toml` 并在 CI 中调用这些脚本以确保可复现性。
