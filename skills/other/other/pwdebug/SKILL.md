---
name: pwdebug
description: 用于需要通过命令行操作真实浏览器实例进行前端调试（如导航、执行 JS、截图、元素拾取、控制台日志）且希望跨多次命令复用同一浏览器会话的场景。
---

# Playwright 浏览器调试 CLI

## 概览

该技能提供一个基于 Playwright 的命令行工具，用于启动浏览器服务并执行导航、评估 JS、截图、元素拾取与日志监听等调试操作。当前仅支持 Chromium（通过 CDP 连接）。

## 快速开始

> 工作目录应为本文件所在目录，示例命令默认从该目录执行。

1. 启动浏览器服务（常驻进程）：

```bash
scripts/pwdebug.py start
```

2. 在新标签页打开页面：

```bash
scripts/pwdebug.py nav https://example.com --new
```

3. 执行 JS 表达式：

```bash
scripts/pwdebug.py evaluate "document.title"
```

4. 截图：

```bash
scripts/pwdebug.py screenshot --full
```

5. 交互式拾取元素：

```bash
scripts/pwdebug.py pick "点击登录按钮"
```

6. 监听控制台日志：

```bash
scripts/pwdebug.py watch-logs
```

7. 查看最近日志：

```bash
scripts/pwdebug.py logs 100
```

## 说明

- CLI 入口：`scripts/pwdebug.py`
- 日志路径：`~/.cache/pwdebug/console.log.jsonl`
- 状态路径：`~/.cache/pwdebug/server.json`

## 依赖与安装

- 脚本依赖通过 `uv --script` 管理。
