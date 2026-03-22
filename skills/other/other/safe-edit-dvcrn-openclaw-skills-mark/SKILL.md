---
name: safe-edit
description: 安全配置修改辅助技能 - 在修改重要配置文件前自动设置回滚，支持多平台（Linux/macOS/FreeBSD/Windows）
metadata: {"openclaw":{"emoji":"🛡️","requires":{},"permissions":[]}}
---

# 🛡️ safe-edit 安全配置修改技能

> 在修改重要配置文件前自动设置回滚机制，**防止 OpenClaw 自己把自己改崩溃**。

## 🎯 解决什么问题

日常操作中，我们经常需要修改系统或应用的配置文件，但有时可能会出现：

- ❌ 改错配置导致服务崩溃
- ❌ 忘记原来配置是什么，无法恢复
- ❌ 手抖按错键，配置被覆盖
- ❌ 改完后不记得改了什么

**safe-edit 就是为了解决这些问题！**

## 🔥 什么时候该用

> ⚠️ **这是防止 OpenClaw 自己把自己改崩溃的核心技能！** 每次修改关键配置文件前都必须使用。

当你要做以下操作时，**必须使用 safe-edit**：

| 场景 | 示例 |
|------|------|
| 修改 OpenClaw 核心配置 | `openclaw.json` |
| 修改系统级配置 | crontab、nginx.conf、docker-compose.yml |
| 修改定时任务 | 添加/删除 cron 任务 |
| 修改用户数据 | 用户画像、权限配置 |
| 任何可能让服务崩溃的操作 | 修改端口、认证信息 |

**简单判断**：只要是**修改配置文件**，且**不确定后果**，就用 safe-edit。

## ✅ 使用方法

### 1. 开始修改（必做！）

用户说"我要修改 xxx 配置"时：

```
请使用 safe-edit 开始修改配置文件: /path/to/config.json
```

或直接执行：
```bash
safe-edit start /root/.openclaw/openclaw.json
```

AI 会自动：
1. ✅ 备份当前配置文件
2. ✅ 设置 15 分钟后自动回滚
3. ✅ 提示用户确认操作

### 2. 执行修改

现在可以安全地进行配置修改了！

### 3. 确认成功（修改完成后必做！）

告诉 AI：
```
safe-edit 确认成功
```

这会**立即取消** 15 分钟后的自动回滚。

### 4. 取消回滚（可选）

如果发现改错了，想立即回滚：
```
safe-edit 取消回滚
```

### 5. 查看状态

```
safe-edit 状态
```

## 🔄 工作流程

```
用户: 我想修改 openclaw.json

AI: 好的，使用 safe-edit 开始修改

  1. safe-edit start /root/.openclaw/openclaw.json
     ↓
  2. [自动] 备份文件 + 设置 15 分钟回滚
     ↓
  3. AI 执行配置修改
     ↓
用户: 改完了，没问题

AI: 确认成功
  4. safe-edit confirm
     ↓
  5. 取消回滚任务 ✅ 完成！

如果出问题：
  - 15 分钟后自动恢复备份
  - 或手动执行 safe-edit 取消回滚
```

## 🎯 触发关键词

当用户说以下话时，AI 应该**自动推荐使用 safe-edit**：

- "我想修改配置"
- "我要改一下 xxx.json"
- "帮我改一下 crontab"
- "改一下定时任务"
- "修改系统配置"
- 任何涉及配置文件修改的操作

## 🔧 底层脚本

脚本位置：`/root/.openclaw/scripts/safe-edit.sh`

### 支持的平台

| 平台 | 回滚方式 |
|------|----------|
| Linux (Debian/Ubuntu/RHEL) | at 命令 |
| Linux (WSL) | at 命令 |
| macOS | at / sleep 后台 |
| FreeBSD | at 命令 |
| Windows (Git Bash/MSYS) | schtasks / sleep 后台 |

### 命令行用法

```bash
# 开始修改并设置回滚
safe-edit start <文件路径>

# 确认成功，取消回滚
safe-edit confirm

# 取消回滚
safe-edit cancel

# 查看状态
safe-edit status
```

## 📝 示例对话

**用户**: 我想把 crontab 里的某个定时任务删掉

**AI**: 好的，这个操作有风险，我先使用 safe-edit 设置回滚机制：
```
safe-edit start /var/spool/cron/crontabs/root
```

已设置 15 分钟自动回滚。确认完成后请告诉我"safe-edit 确认成功"。

---

**用户**: 帮我改一下 openclaw.json 的某个配置

**AI**: 好的，我来使用 safe-edit：
```
safe-edit start /root/.openclaw/openclaw.json
```

备份完成，回滚已设置。请问要改什么配置？

（修改完成后）

**用户**: 改完了，一切正常

**AI**: 确认成功，取消回滚：
```
safe-edit confirm
```

✅ 完成！

---

*⚠️ 重要：每次修改配置文件前务必使用此技能！这是避免生产事故的最后一道防线。*
