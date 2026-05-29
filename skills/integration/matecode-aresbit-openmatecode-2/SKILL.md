---
name: matecode
description: MateCode - Claude Code Telegram Bridge 管理工具。用于启动、停止、监控 Telegram 远程控制服务
---

# MateCode - Claude Code Telegram Bridge

通过 Telegram 远程控制 Claude Code。

## 快速命令

```bash
# 启动服务
./matecode.sh start

# 停止服务
./matecode.sh stop

# 重启服务
./matecode.sh restart

# 查看状态
./matecode.sh status

# 查看日志
./matecode.sh logs
```

## 配置步骤

### 1. 安装依赖

```bash
# macOS
brew install tmux

# Ubuntu/Debian
sudo apt-get install tmux
```

### 2. 设置 Telegram Bot Token

从 @BotFather 获取 bot token，然后设置环境变量：

```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
# 添加到 ~/.zshrc 或 ~/.bashrc 使其永久生效
echo 'export TELEGRAM_BOT_TOKEN="your_token_here"' >> ~/.zshrc
```

### 3. 配置 Claude Stop Hook

```bash
cp hooks/send-to-telegram.sh ~/.claude/hooks/
nano ~/.claude/hooks/send-to-telegram.sh  # 编辑设置 bot token
chmod +x ~/.claude/hooks/send-to-telegram.sh
```

添加到 `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [{"hooks": [{"type": "command", "command": "~/.claude/hooks/send-to-telegram.sh"}]}]
  }
}
```

## 文件结构

| 文件 | 用途 |
|------|------|
| `matecode.sh` | 主启动脚本 |
| `bridge.py` | Telegram 桥接服务 |
| `hooks/send-to-telegram.sh` | Claude 响应钩子 |
| `start_bridge.sh` / `stop_bridge.sh` | 单独控制 bridge |

## Telegram Bot 命令

| 命令 | 功能 |
|------|------|
| `/status` | 检查 tmux 状态 |
| `/clear` | 清空对话 |
| `/continue_` | 继续最近会话 |
| `/resume` | 选择会话恢复 |
| `/stop` | 中断 Claude |

## 故障排查

### Bridge 无法启动

```bash
# 检查环境变量
echo $TELEGRAM_BOT_TOKEN

# 检查端口占用
lsof -i :8081

# 查看详细日志
cat bridge.log
tail -f bridge.log
```

### tmux 会话问题

```bash
# 手动连接到会话
tmux attach -t claude

# 强制关闭所有相关进程
pkill -f "bridge\.py"
tmux kill-session -t claude
```

### 无法收到回复

1. 检查 `~/.claude/hooks/send-to-telegram.sh` 是否正确配置
2. 确认 `TELEGRAM_BOT_TOKEN` 已设置
3. 查看 `~/.claude/telegram_chat_id` 是否存在
4. 检查 `~/.claude/settings.json` 的 hooks 配置

## 技术特点

- **纯标准库**: bridge.py 使用 Python 标准库，无外部依赖
- **长轮询**: 30 秒超时，低延迟响应
- **实时推送**: 通过 transcript 监控即时推送回复
- **安全**: 只向外连接 Telegram API，不接收入站请求
