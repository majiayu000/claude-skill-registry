---
name: healthcare-monitor
description: 医疗行业企业融资监控系统。实时监控医疗健康企业的工商变更，识别融资信号，自动推送告警。支持天眼查/企查查数据采集、AI融资判断、多渠道推送。
allowed-tools: Bash, Read, Write, Edit, Exec, Browser, Message, Cron
---

# 医疗行业企业融资监控系统

## 概述

本技能实现医疗健康行业企业的融资信号实时监控，通过工商变更数据识别未披露的融资事件，为媒体、投资机构提供情报服务。

## 核心功能

### 1. 企业监控列表管理
- 添加/删除监控企业
- 按行业、地区、规模分类
- 设置监控优先级

### 2. 工商变更检测
- 定时爬取天眼查/企查查
- 增量对比检测变更
- 识别关键变更类型

### 3. 融资信号识别
- AI 判断是否为融资
- 融资轮次推断
- 投资方识别

### 4. 多渠道推送
- Telegram 实时告警
- 飞书群组推送
- 日报/周报生成

## 文件结构

```
skills/healthcare-monitor/
├── SKILL.md                 # 技能说明
├── config/
│   ├── companies.json       # 监控企业列表
│   └── settings.json        # 配置参数
├── scripts/
│   ├── monitor.py           # 主监控脚本
│   ├── scraper.py           # 数据采集
│   ├── analyzer.py          # 融资分析
│   └── notifier.py          # 推送通知
├── data/
│   ├── snapshots/           # 企业快照
│   ├── changes/             # 变更记录
│   └── reports/             # 生成的报告
└── templates/
    ├── alert.md             # 告警模板
    └── daily_report.md      # 日报模板
```

## 快速开始

### 1. 添加监控企业

```bash
# 添加单个企业
python3 ~/clawd/skills/healthcare-monitor/scripts/monitor.py add "北京某某医疗科技有限公司"

# 批量导入
python3 ~/clawd/skills/healthcare-monitor/scripts/monitor.py import companies.csv
```

### 2. 手动检查

```bash
# 检查所有企业
python3 ~/clawd/skills/healthcare-monitor/scripts/monitor.py check

# 检查单个企业
python3 ~/clawd/skills/healthcare-monitor/scripts/monitor.py check "公司名称"
```

### 3. 设置定时任务

```bash
# 每小时检查重点企业
# 使用 OpenClaw cron 工具设置
```

## 融资信号识别规则

### 强信号 (置信度 >80%)

| 信号 | 描述 | 权重 |
|------|------|------|
| 新增机构股东 | 股东名称包含"投资/资本/基金/创投" | +40 |
| 注册资本增加 | 增幅 >10% | +30 |
| 股权稀释 | 创始人持股比例下降 | +20 |

### 中信号 (置信度 50-80%)

| 信号 | 描述 | 权重 |
|------|------|------|
| 新增自然人股东 | 可能是投资人代持 | +15 |
| 经营范围扩大 | 业务扩张信号 | +10 |
| 办公地址变更 | 搬迁到更好区域 | +10 |

### 弱信号 (置信度 <50%)

| 信号 | 描述 | 权重 |
|------|------|------|
| 仅注册资本增加 | 可能是内部增资 | +10 |
| 法人变更 | 可能是内部调整 | +5 |

### 融资轮次判断

```yaml
种子/天使轮:
  - 公司成立 <2 年
  - 注册资本 <500 万
  - 新股东为天使投资人

A轮:
  - 公司成立 2-4 年
  - 注册资本增幅 20-50%
  - 新股东为知名 VC

B轮+:
  - 公司成立 >3 年
  - 注册资本增幅 10-30%
  - 新股东为大型 PE/战略投资者
```

## 数据采集

### 天眼查采集

```python
# 采集字段
fields = {
    "basic": ["公司名称", "法人", "注册资本", "成立日期", "经营状态"],
    "shareholders": ["股东名称", "持股比例", "认缴出资", "出资日期"],
    "changes": ["变更时间", "变更项目", "变更前", "变更后"],
    "investments": ["被投企业", "投资金额", "投资时间"],
}
```

### 反爬策略

```yaml
策略:
  - 使用 Playwright 无头浏览器
  - 随机延迟 3-10 秒
  - 轮换 User-Agent
  - 代理 IP 池 (可选)
  - 模拟人类行为 (滚动、点击)

限制:
  - 每小时最多 100 次请求
  - 单企业每天最多查询 3 次
  - 遇到验证码暂停并告警
```

## 推送配置

### Telegram 推送

```json
{
  "telegram": {
    "enabled": true,
    "bot_token": "从 config 读取",
    "chat_id": "8518085684",
    "alert_level": "high"
  }
}
```

### 飞书推送

```json
{
  "feishu": {
    "enabled": true,
    "webhook": "从 config 读取",
    "alert_level": "all"
  }
}
```

## 告警模板

### 融资告警

```markdown
🚨 **融资信号告警**

**企业**: {{company_name}}
**变更时间**: {{change_date}}
**置信度**: {{confidence}}%

**变更详情**:
- 注册资本: {{old_capital}} → {{new_capital}}
- 新增股东: {{new_shareholders}}
- 股权变化: {{equity_changes}}

**AI 分析**:
- 融资轮次: {{round_estimate}}
- 融资金额: {{amount_estimate}}
- 投资方: {{investors}}

**数据来源**: 天眼查
**监控时间**: {{monitor_time}}
```

## API 接口

### 查询企业状态

```bash
GET /api/company/{company_name}

Response:
{
  "name": "公司名称",
  "last_check": "2026-02-03 22:00:00",
  "status": "normal",
  "recent_changes": [...],
  "funding_signals": [...]
}
```

### 添加监控

```bash
POST /api/monitor
{
  "company_name": "公司名称",
  "priority": "high",
  "check_interval": "hourly"
}
```

## 使用场景

### 场景一: 媒体情报

动脉网等医疗媒体使用，第一时间获取融资新闻线索。

```yaml
工作流:
  1. 系统检测到融资信号
  2. 推送到编辑 Telegram
  3. 编辑核实后发布新闻
  4. 比竞争对手快 24-48 小时
```

### 场景二: 投资机构

VC/PE 使用，发现潜在投资标的或跟投机会。

```yaml
工作流:
  1. 系统检测到 A 轮融资
  2. 推送到投资经理
  3. 评估是否跟进
  4. 主动联系企业
```

### 场景三: 大药企 BD

药企商务拓展部门使用，寻找合作/收购标的。

```yaml
工作流:
  1. 系统检测到目标领域企业融资
  2. 推送到 BD 团队
  3. 评估合作可能性
  4. 发起商务接触
```

## 监控企业列表 (初始)

### 医疗器械

- 迈瑞医疗
- 联影医疗
- 微创医疗
- 先瑞达医疗
- 心脉医疗

### 创新药

- 百济神州
- 信达生物
- 君实生物
- 再鼎医药
- 和黄医药

### 医疗AI

- 推想科技
- 数坤科技
- 深睿医疗
- 汇医慧影
- 医渡云

### 互联网医疗

- 微医集团
- 丁香园
- 春雨医生
- 好大夫在线
- 平安好医生

### 基因检测

- 华大基因
- 贝瑞基因
- 燃石医学
- 泛生子
- 诺禾致源

## 配置参数

```json
{
  "check_interval": {
    "high_priority": "1h",
    "normal": "6h",
    "low": "24h"
  },
  "alert_threshold": {
    "confidence": 60,
    "capital_change_percent": 10
  },
  "scraper": {
    "delay_min": 3,
    "delay_max": 10,
    "max_requests_per_hour": 100
  },
  "notification": {
    "telegram": true,
    "feishu": true,
    "email": false
  }
}
```

## 故障排查

### 问题: 爬取失败

```bash
# 检查日志
tail -f ~/clawd/skills/healthcare-monitor/data/logs/scraper.log

# 常见原因
- IP 被封: 更换代理
- 验证码: 人工处理或接入打码平台
- 页面结构变化: 更新选择器
```

### 问题: 误报过多

```bash
# 调整置信度阈值
# 编辑 config/settings.json
{
  "alert_threshold": {
    "confidence": 70  # 提高阈值
  }
}
```

## 相关文件

- `~/clawd/docs/solutions/healthcare-data-intelligence.md` - 完整解决方案
- `~/.openclaw/agents/healthcare-monitor/` - Agent 配置
- `~/clawd/skills/healthcare-monitor/data/` - 数据存储

## TODO

- [ ] 实现天眼查爬虫
- [ ] 实现融资信号 AI 分析
- [ ] 设置定时任务
- [ ] 对接飞书推送
- [ ] 添加 Web 管理界面
- [ ] 支持更多数据源 (企查查、启信宝)
- [ ] 实现日报/周报自动生成
