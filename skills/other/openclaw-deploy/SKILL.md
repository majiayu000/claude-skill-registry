---
name: openclaw-deploy
description: 在远程服务器上一键部署 OpenClaw。当用户需要安装 OpenClaw、部署 OpenClaw、配置 OpenClaw 到服务器时使用
allowed-tools: Bash, Read, Write, AskUserQuestion, WebSearch, WebFetch, Task, Glob, Grep, Edit
metadata:
  argument-hint: "[SSH连接信息，如 root@host -p port]"
---

# OpenClaw 远程一键部署

在远程 Linux 服务器上自动部署 OpenClaw + AI 模型 + 聊天频道。

---

## 第零步：输出傻瓜教程

**skill 启动后，必须先输出以下准备清单**，让用户知道需要什么，然后再用 AskUserQuestion 收集信息：

```markdown
# OpenClaw 一键部署

欢迎！部署前你需要准备以下东西：

| 序号 | 准备什么 | 说明 | 必需？ |
|------|----------|------|--------|
| 1 | 一台 Linux 服务器 | 最低 1GB 内存 + 500MB 磁盘，支持 SSH 登录 | 必需 |
| 2 | SSH 免密登录 | 确保本机能 `ssh user@host` 直接连上 | 必需 |
| 3 | AI 模型 API Key | 智谱GLM / DeepSeek / OpenAI / Claude / Kimi / 通义 任选 | 必需 |
| 4 | 聊天频道 Bot Token | Telegram(@BotFather) 或 Discord 或 飞书，也可以暂不配 | 可选 |
| 5 | 代理地址 | 中国大陆服务器 + 海外频道(Telegram/Discord)时需要 | 视情况 |
| 6 | 浏览器控制 | 让 Bot 能操控浏览器搜索/截图/填表，需额外安装 Playwright | 可选 |
```

---

## 第一步：收集信息

用 AskUserQuestion 收集（$ARGUMENTS 已提供的跳过）。分两轮问：

### 第一轮（必填 3 项）：

用 AskUserQuestion 同时问以下 3 个问题：

1. **SSH 连接信息**（header: "SSH 连接"）
   - 选项根据上下文动态生成（如之前用过的服务器），兜底选项"其他服务器"
2. **AI 模型**（header: "AI 模型"）
   - 智谱 GLM-5（国产，无需代理）
   - DeepSeek（国产，无需代理）
   - OpenAI GPT-4o（需代理或海外服务器）
   - Anthropic Claude（需代理或海外服务器）
3. **聊天频道**（header: "聊天频道"）
   - Telegram（需 Bot Token，中国大陆需代理）
   - Discord（需 Bot Token）
   - 飞书（需 Bot Token）
   - 暂不配置
4. **浏览器控制**（header: "浏览器"）
   - 启用（Bot 可操控浏览器搜索/截图/填表）
   - 暂不配置

### 第二轮（根据第一轮结果追问）：

- 如果用户没提供 API Key → 问 API Key
- 如果选了聊天频道 → 问 Bot Token
  - 如果用户没有 Bot Token → 给出创建教程：
    - Telegram：找 @BotFather，发 `/newbot`
    - Discord：去 discord.com/developers 创建 Application → Bot
    - 飞书：去 open.feishu.cn 创建自建应用
- 如果选了 Telegram/Discord 且服务器在中国大陆 → 问代理地址
  - 自动判断：如果 SSH 到服务器后 `curl -s --connect-timeout 3 https://api.telegram.org` 失败，则判定需要代理

---

## 第二步：环境检查

SSH 连接到服务器，**单条命令**获取全部信息：

```bash
ssh <SSH_ARGS> "echo '=== CPU ===' && nproc && echo '=== 内存 ===' && free -h && echo '=== 磁盘 ===' && df -h / && echo '=== 系统 ===' && uname -a && echo '=== Node.js ===' && node -v 2>/dev/null || echo '未安装' && echo '=== npm ===' && npm -v 2>/dev/null || echo '未安装' && echo '=== 包管理器 ===' && which pacman apt yum dnf 2>/dev/null && echo '=== OpenClaw ===' && openclaw --version 2>/dev/null || echo '未安装'"
```

**最低要求**：1GB RAM + 500MB 磁盘。不满足则告知用户并停止。

---

## 第三步：安装 Node.js（如未安装）

根据检测到的包管理器：

| 包管理器 | 命令 |
|----------|------|
| pacman (Arch) | `pacman -S --noconfirm nodejs npm` |
| apt (Debian/Ubuntu) | `curl -fsSL https://deb.nodesource.com/setup_22.x \| bash - && apt install -y nodejs` |
| dnf (RHEL/Fedora) | `dnf install -y nodejs npm` |
| yum (CentOS) | `curl -fsSL https://rpm.nodesource.com/setup_22.x \| bash - && yum install -y nodejs` |

安装后验证：`node -v && npm -v`，确认 Node.js >= 22。

---

## 第四步：安装 OpenClaw

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

> **重要**：安装脚本会尝试启动交互式 onboarding wizard，在非 TTY 环境会报 `/dev/tty: No such device or address` 错误。**这是正常的**，OpenClaw 本体已安装成功。

验证：`openclaw --version`

---

## 第五步：写入配置文件

**直接写 `~/.openclaw/openclaw.json`**，不用交互式 wizard。

### 模型配置模板

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "<PROVIDER_NAME>": {
        "baseUrl": "<BASE_URL>",
        "apiKey": "<API_KEY>",
        "api": "openai-completions",
        "models": [
          {
            "id": "<MODEL_ID>",
            "name": "<DISPLAY_NAME>",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 128000,
            "maxTokens": 32000
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "<PROVIDER_NAME>/<MODEL_ID>"
      },
      "memorySearch": {
        "enabled": false
      }
    }
  },
  "gateway": {
    "mode": "local"
  }
}
```

### 常见模型参考

| Provider 名 | MODEL_ID | baseUrl |
|-------------|----------|---------|
| zhipu | glm-5 | `https://open.bigmodel.cn/api/paas/v4` |
| openai | gpt-4o | `https://api.openai.com/v1` |
| deepseek | deepseek-chat | `https://api.deepseek.com/v1` |
| kimi | moonshot-v1-128k | `https://api.moonshot.cn/v1` |
| qwen | qwen-max | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| anthropic | claude-sonnet-4-5-20250929 | `https://api.anthropic.com/v1` |

> **注意**：Anthropic 模型的 `api` 字段应为 `"anthropic-messages"` 而非 `"openai-completions"`。

写入后立即修复权限：

```bash
mkdir -p ~/.openclaw/agents/main/sessions ~/.openclaw/credentials
chmod 700 ~/.openclaw
chmod 600 ~/.openclaw/openclaw.json
```

---

## 第六步：启动网关（systemd）

按顺序执行：

```bash
# 安装 systemd 服务
openclaw gateway install

# 启用 linger（退出 SSH 后服务不会停）
loginctl enable-linger $(whoami)

# 启动
export XDG_RUNTIME_DIR=/run/user/$(id -u)
systemctl --user start openclaw-gateway.service
```

等待 3 秒后验证：

```bash
systemctl --user status openclaw-gateway.service | head -10
```

确认 `Active: active (running)`。

### 轮换 device token

网关首次启动后，轮换 operator token 修复可能的认证问题：

```bash
# 先获取 device ID
DEVICE_ID=$(openclaw devices list 2>&1 | grep -oP '[a-f0-9]{40,}')
# 轮换 token
openclaw devices rotate --role operator --device "$DEVICE_ID"
```

---

## 第七步：配置聊天频道（如需要）

根据用户选择的频道执行对应配置。

### 7a. 设置频道

**Telegram：**
```bash
openclaw config set channels.telegram.enabled true
openclaw config set channels.telegram.botToken '<BOT_TOKEN>'
openclaw config set channels.telegram.dmPolicy pairing
```

**Discord：**
```bash
openclaw config set channels.discord.enabled true
openclaw config set channels.discord.botToken '<BOT_TOKEN>'
openclaw config set channels.discord.dmPolicy pairing
```

**飞书：**
```bash
openclaw config set channels.feishu.enabled true
openclaw config set channels.feishu.token '<BOT_TOKEN>'
openclaw config set channels.feishu.dmPolicy pairing
```

### 7b. 配置代理（中国大陆服务器 + 海外频道时必须）

> **适用场景**：服务器在中国大陆，且频道是 Telegram 或 Discord（需访问海外 API）。
> 飞书是国内服务，不需要代理。

先测试是否需要代理（自动判断）：

```bash
# Telegram
curl -s --connect-timeout 3 https://api.telegram.org/bot<BOT_TOKEN>/getMe
# Discord
curl -s --connect-timeout 3 https://discord.com/api/v10/users/@me -H "Authorization: Bot <BOT_TOKEN>"
```

如果超时/失败，说明需要代理。用用户提供的代理测试：

```bash
export http_proxy='<PROXY_URL>' && export https_proxy='<PROXY_URL>'
curl -s --connect-timeout 5 https://api.telegram.org/bot<BOT_TOKEN>/getMe
```

确认返回成功后，写入 systemd override。

> **重要**：proxy.conf 必须**一次性写完所有环境变量**（代理 + no_proxy + DISPLAY），
> 不要分多次追加，后续浏览器步骤也不需要再改这个文件。

```bash
mkdir -p ~/.config/systemd/user/openclaw-gateway.service.d
cat > ~/.config/systemd/user/openclaw-gateway.service.d/proxy.conf << EOF
[Service]
Environment="http_proxy=<PROXY_URL>"
Environment="https_proxy=<PROXY_URL>"
Environment="no_proxy=127.0.0.1,localhost,::1"
Environment="NO_PROXY=127.0.0.1,localhost,::1"
Environment="DISPLAY=:99"
EOF
```

> **为什么要 `no_proxy`**：没有它，OpenClaw 连本地 Chrome CDP 端口也会走代理，
> 导致浏览器启动成功但 OpenClaw 检测不到，报 `Failed to start Chrome CDP`。
> 即使当前不配浏览器，也要加上 `no_proxy`，防止后续开启浏览器时踩坑。

> **为什么要 `DISPLAY=:99`**：浏览器需要显示服务器，即使 headless 模式也需要。
> 如果不配浏览器，这个变量无害。

### 7c. 重启网关（必须通过 systemd！）

> **关键坑点**：`openclaw config set` 会触发内部热重启，但热重启**不会**加载 systemd 的环境变量（代理）。
> 所有涉及频道/代理的配置改完后，必须用 `systemctl --user restart` 来重启。

```bash
export XDG_RUNTIME_DIR=/run/user/$(id -u)
systemctl --user daemon-reload
systemctl --user restart openclaw-gateway.service
```

### 7d. 验证频道连接

等待 5 秒后：

```bash
openclaw channels status
```

确认输出包含 `enabled, configured, running`。

**如果看到 `fetch failed` 或 `Network request failed`**：代理没生效，检查 proxy.conf 并确认是通过 systemctl 重启的。

### 7e. 配对用户

让用户在对应频道给 Bot 发一条消息。Bot 会回复配对码。

> **关键坑点**：配对命令是 `openclaw pairing approve <channel> <CODE>`，
> **不是** `openclaw devices approve <CODE>`（那个会报 `unknown requestId`）。

```bash
# 查看待配对列表（必须指定频道名）
openclaw pairing list <channel>
# 例如：openclaw pairing list telegram

# 批准配对
openclaw pairing approve <channel> <PAIRING_CODE>
# 例如：openclaw pairing approve telegram BAEWET79
```

配对码有效期约 1 小时。如果过期，让用户重新发消息即可生成新码。

---


## Extended Reference

Detailed material starting at `## 第八步：配置浏览器控制（可选）` has been moved to [`reference/extended.md`](reference/extended.md) to keep this skill concise. Load that reference when the task requires the moved examples, command catalogs, checklists, platform details, or implementation templates.
