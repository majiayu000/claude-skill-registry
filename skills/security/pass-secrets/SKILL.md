# Pass 密钥管理 Skill

## 概述

使用 Pass (Password Store) 统一管理所有 API 密钥和敏感凭证。Pass 基于 GPG 加密，支持 Git 同步，安全可靠。

## 快速开始

### 查看所有密钥
```bash
pass
# 或
pass ls
```

### 获取密钥
```bash
pass api/openai           # 显示密钥
pass -c api/openai        # 复制到剪贴板
```

### 添加密钥
```bash
pass insert api/new-service
# 或多行
pass insert -m api/new-service
```

### 编辑密钥
```bash
pass edit api/openai
```

### 删除密钥
```bash
pass rm api/old-service
```

### 生成随机密钥
```bash
pass generate api/new-token 32
```

---

## 目录结构

```
~/.password-store/
├── api/                    # API 密钥
│   ├── openrouter-vip.gpg
│   ├── zai.gpg
│   ├── anapi.gpg
│   └── github-copilot.gpg
├── tokens/                 # 访问令牌
│   ├── telegram-bot.gpg
│   └── github.gpg
├── cloud/                  # 云服务凭证
│   ├── aws.gpg
│   └── gcp.gpg
└── services/               # 其他服务
    └── docker.gpg
```

---

## Git 同步

### 初始化同步
```bash
pass git init
pass git remote add origin git@github.com:用户名/password-store.git
pass git push -u origin master
```

### 日常同步
```bash
pass git pull    # 拉取
pass git push    # 推送
```

### 新设备克隆
```bash
# 1. 导入 GPG 密钥
gpg --import private-key.asc

# 2. 克隆仓库
git clone git@github.com:用户名/password-store.git ~/.password-store
```

---

## 与 OpenClaw 集成

### 方式 1: 启动脚本

创建 `~/.openclaw/scripts/start-with-pass.sh`:

```bash
#!/bin/bash
# 从 Pass 加载密钥并启动 OpenClaw

export ZAI_API_KEY=$(pass api/zai)
export OPENROUTER_VIP_API_KEY=$(pass api/openrouter-vip)

exec openclaw gateway "$@"
```

### 方式 2: 环境变量文件

```bash
# 生成 .env 文件（临时使用）
pass api/zai | xargs -I {} echo "ZAI_API_KEY={}" > /tmp/openclaw.env
pass api/openrouter-vip | xargs -I {} echo "OPENROUTER_VIP_API_KEY={}" >> /tmp/openclaw.env

# 使用
source /tmp/openclaw.env && openclaw gateway
```

### 方式 3: 直接引用（推荐）

在 `~/.bashrc` 或 `~/.zshrc` 中添加:

```bash
# OpenClaw 密钥
alias openclaw-start='ZAI_API_KEY=$(pass api/zai) OPENROUTER_VIP_API_KEY=$(pass api/openrouter-vip) openclaw gateway'
```

---

## 常用命令速查

| 命令 | 说明 |
|------|------|
| `pass` | 列出所有密钥 |
| `pass api/xxx` | 显示密钥 |
| `pass -c api/xxx` | 复制到剪贴板 |
| `pass insert api/xxx` | 添加密钥 |
| `pass edit api/xxx` | 编辑密钥 |
| `pass rm api/xxx` | 删除密钥 |
| `pass mv api/old api/new` | 重命名 |
| `pass cp api/xxx api/backup` | 复制 |
| `pass find xxx` | 搜索 |
| `pass generate api/xxx 32` | 生成随机密钥 |
| `pass git pull` | 同步拉取 |
| `pass git push` | 同步推送 |

---

## 安全最佳实践

### 1. GPG 密钥备份
```bash
# 导出私钥（安全保存！）
gpg --export-secret-keys --armor 你的邮箱 > gpg-private.asc

# 导出公钥
gpg --export --armor 你的邮箱 > gpg-public.asc
```

### 2. 使用私有仓库
- GitHub/GitLab 私有仓库
- 即使泄露，没有 GPG 私钥也无法解密

### 3. 定期轮换密钥
```bash
# 更新密钥
pass edit api/openai

# 查看修改历史
pass git log --oneline
```

### 4. 多设备同步注意
- 每台设备需要导入 GPG 私钥
- 使用 SSH 密钥访问 Git 仓库

---

## 故障排查

### GPG 解密失败
```bash
# 检查密钥
gpg --list-secret-keys

# 重新导入
gpg --import private-key.asc
```

### Git 同步冲突
```bash
pass git status
pass git stash
pass git pull
pass git stash pop
```

### 权限问题
```bash
chmod 700 ~/.password-store
chmod 600 ~/.password-store/**/*.gpg
```

---

## 相关资源

- [Pass 官网](https://www.passwordstore.org/)
- [Pass GitHub](https://github.com/zx2c4/pass)
- [GPG 教程](https://gnupg.org/documentation/)

---

## 当前配置

**GPG 密钥**: `5F845B8E1B6C5C52` (DL <2067089451@qq.com>)

**已存储的密钥**:
- `api/openrouter-vip` - OpenRouter VIP API
- `api/zai` - 智谱 AI API
- `api/anapi` - Anapi Claude API
- `tokens/telegram-bot` - Telegram Bot Token
- `tokens/github-copilot` - GitHub Copilot Token

---

*由小a创建和维护*
