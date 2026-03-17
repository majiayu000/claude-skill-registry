---
name: auth-manager
description: "网页登录态管理。定期检查各平台 Playwright 登录状态，过期自动告警。支持动态添加/删除平台。"
license: MIT
metadata:
  version: 1.0.0
  domains: [auth, playwright, session-management]
  type: automation
---

# Auth Manager - 网页登录态管理

## 当使用此技能

- 检查网页登录状态是否过期
- 添加新的平台到登录态监控
- 删除不再需要的平台
- 查看当前监控的平台列表
- 手动触发登录态检查

## 触发词

- "检查登录状态"
- "添加平台监控"
- "auth check"
- "登录过期"
- "session 管理"

## 架构

```
~/.playwright-data/<platform>/     # Playwright 浏览器 profile
~/.openclaw/auth-platforms.json    # 平台配置（动态）
~/.openclaw/auth-session-state.json # 检查结果状态
~/clawd/scripts/auth_session_manager.py  # 检查脚本
```

## 平台配置格式

`~/.openclaw/auth-platforms.json`:
```json
{
  "platforms": {
    "platform_id": {
      "name": "显示名称",
      "profile_dir": "~/.playwright-data/platform_id",
      "check_url": "https://example.com/dashboard",
      "login_url": "https://example.com/login",
      "logged_in_indicators": [".user-info", ".dashboard", "[class*='avatar']"],
      "login_page_indicators": ["input[type='password']", ".login-form"],
      "enabled": true
    }
  }
}
```

## 操作指南

### 添加新平台

1. 确认平台信息：名称、登录URL、登录后特征元素、登录页特征元素
2. 运行：`python3 ~/clawd/scripts/auth_session_manager.py --add <id> --name "名称" --check-url "URL" --login-url "URL"`
3. 首次登录：`python3 ~/clawd/scripts/auth_session_manager.py --login <id>`（会打开浏览器让用户手动登录）
4. 验证：`python3 ~/clawd/scripts/auth_session_manager.py --check --platform <id>`

### 删除平台

```bash
python3 ~/clawd/scripts/auth_session_manager.py --remove <id>
```

### 检查所有平台

```bash
python3 ~/clawd/scripts/auth_session_manager.py --check
```

### 列出平台

```bash
python3 ~/clawd/scripts/auth_session_manager.py --list
```

## Cron 任务

已配置每 6 小时自动检查（cron id: `1f2eb5a5-5c2e-4556-b006-e29325f41609`），过期则推送告警。

## 退出码

- 0: 全部正常
- 1: 有错误（非过期）
- 2: 有平台登录过期
