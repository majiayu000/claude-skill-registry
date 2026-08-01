---
name: api-provider-status
description: '| 供应商 | 查询方式 | 登录状态存储 |'
---

# API Provider Status Skill

API 供应商状态查询与余额监控。

## 功能

- 查询各 API 供应商的余额/用量
- 生成统计报告
- 支持定时自动查询

## 支持的供应商

| 供应商 | 查询方式 | 登录状态存储 |
|--------|----------|--------------|
| Anapi (Claude) | API 直接查询 | 不需要登录 |
| GitHub Copilot | Playwright 抓取 | `~/.playwright-data/github` |
| 性价比 API | Playwright 抓取 | `~/.playwright-data/xingjiabiapi` |
| OpenRouter VIP | 暂不支持 | - |
| ZAI (智谱) | 暂不支持 | - |

## 查询方法详解

### 1. Anapi (Claude)

**方式**: 直接 API 调用（无需登录）

```bash
curl -s -H "User-Agent: Mozilla/5.0" \
  "https://anapi.9w7.cn/api/apikeys/query?key=<YOUR_KEY>"
```

**返回数据**:
- `status`: 状态 (normal/expired/exhausted)
- `daily_success_count`: 今日请求数
- `global_daily_limit`: 每日限额
- `expires_at`: 到期时间
- `success_rate`: 成功率

### 2. GitHub Copilot Pro

**方式**: Playwright 抓取（需要先登录）

**查询页面**: `https://github.com/settings/copilot`

**登录流程**:
```python
from playwright.sync_api import sync_playwright
import os

user_data_dir = os.path.expanduser('~/.playwright-data/github')
os.makedirs(user_data_dir, exist_ok=True)

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir,
        headless=False,  # 显示浏览器让用户登录
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.goto('https://github.com/settings/copilot')
    # 用户手动登录后，登录状态会保存到 user_data_dir
```

**抓取数据**:
- Premium requests 用量百分比
- 订阅状态 (Active/Inactive)

**正则匹配**:
```python
import re
usage_match = re.search(r'Premium requests\s*([\d.]+)%', text)
is_active = 'Copilot Pro is active' in text
```

### 3. 性价比 API (xingjiabiapi)

**方式**: Playwright 抓取（需要先登录）

**查询页面**: `https://xingjiabiapi.com/console`

**登录流程**:
```python
user_data_dir = os.path.expanduser('~/.playwright-data/xingjiabiapi')
# 同上，使用 launch_persistent_context
```

**抓取数据**:
- 当前余额
- 历史消耗
- 请求次数
- 总 Tokens

**正则匹配**:
```python
balance_match = re.search(r'当前余额💰([\d.]+)', text)
consumed_match = re.search(r'历史消耗💰([\d.]+)', text)
requests_match = re.search(r'请求次数(\d+)', text)
tokens_match = re.search(r'总Tokens(\d+)', text)
```

## 使用方法

### 命令行

```bash
# 生成完整报告
python3 ~/clawd/skills/api-provider-status/balance_checker.py report

# 查询指定供应商
python3 ~/clawd/skills/api-provider-status/balance_checker.py query anapi
python3 ~/clawd/skills/api-provider-status/balance_checker.py query github-copilot
python3 ~/clawd/skills/api-provider-status/balance_checker.py query xingjiabiapi

# JSON 格式查询所有
python3 ~/clawd/skills/api-provider-status/balance_checker.py all
```

### 用量统计

```bash
# 最近 12 小时用量
python3 ~/clawd/skills/api-provider-status/usage_tracker.py report 12

# 最近 24 小时用量
python3 ~/clawd/skills/api-provider-status/usage_tracker.py report 24

# JSON 格式
python3 ~/clawd/skills/api-provider-status/usage_tracker.py stats 12
```

## 首次登录设置

如果 Playwright 登录状态过期，需要重新登录：

```python
# GitHub 登录
cd ~/clawd/skills/playwright-automation
python3 << 'EOF'
from playwright.sync_api import sync_playwright
import os

user_data_dir = os.path.expanduser('~/.playwright-data/github')
os.makedirs(user_data_dir, exist_ok=True)

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir, headless=False
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.goto('https://github.com/login')
    input('登录完成后按 Enter...')
    context.close()
EOF

# 性价比登录
python3 << 'EOF'
from playwright.sync_api import sync_playwright
import os

user_data_dir = os.path.expanduser('~/.playwright-data/xingjiabiapi')
os.makedirs(user_data_dir, exist_ok=True)

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir, headless=False
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.goto('https://xingjiabiapi.com/')
    input('登录完成后按 Enter...')
    context.close()
EOF
```

## 定时任务

已配置 cron 任务每 12 小时自动查询并推送到 NewsRobot 群。

## 文件结构

```
skills/api-provider-status/
├── SKILL.md              # 本文档
├── balance_checker.py    # 余额查询脚本
└── usage_tracker.py      # 用量统计脚本（从 OpenClaw 日志读取）
```

## 登录状态存储

```
~/.playwright-data/
├── github/               # GitHub 登录状态
└── xingjiabiapi/         # 性价比登录状态
```
