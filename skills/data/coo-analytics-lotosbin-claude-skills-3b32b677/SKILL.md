---
name: coo-analytics
description: COO 产品运营数据分析技能，使用 Playwright MCP 从 App Store Connect、小程序后台、小红书创作者中心等平台获取运营数据
version: 1.0.0
---

# COO 产品运营数据分析技能

## 触发条件
当用户提到以下内容时自动触发:
- "运营数据"
- "数据分析"
- "App Store 数据"
- "小程序数据"
- "创作者数据"
- "数据采集"
- "数据报告"

## 核心能力

### 数据源支持

| 平台 | 数据类型 | 采集方式 |
|------|----------|----------|
| App Store Connect | 下载量、收入、评分、评论 | Playwright MCP |
| 微信小程序后台 | 访问量、用户数、留存 | Playwright MCP |
| 小红书创作者中心 | 粉丝、笔记、互动数据 | Playwright MCP |
| 抖音创作者中心 | 播放量、粉丝、互动 | Playwright MCP |
| 微信公众号后台 | 阅读量、粉丝、互动 | Playwright MCP |

### Playwright MCP 集成

```bash
# 页面导航
mcp__playwright__playwright_navigate --url "URL"

# 页面截图
mcp__playwright__playwright_screenshot \
  --name "screenshot_name" \
  --savePng true \
  --fullPage true

# 获取页面文本
mcp__playwright__playwright_get_visible_text

# 获取页面HTML
mcp__playwright__playwright_get_visible_html

# 获取特定元素
mcp__playwright__playwright_get_visible_html --selector ".data-card"

# 等待页面加载
mcp__playwright__playwright_navigate \
  --url "URL" \
  --waitUntil "networkidle"

# 执行滚动
mcp__playwright__playwright_evaluate \
  --script "window.scrollTo(0, document.body.scrollHeight)"
```

### App Store Connect 数据采集

```
目标URL: https://appstoreconnect.apple.com/

采集数据:
├── 销售数据
│   ├── 单位销量
│   ├── 销售额
│   └── 订阅收入
├── 用户数据
│   ├── 新增用户
│   ├── 活跃用户
│   └── 留存率
├── 评价数据
│   ├── 评分分布
│   ├── 评论数量
│   └── 评论内容
└── 版本数据
    ├── 下载趋势
    └── 崩溃报告
```

**采集流程:**

```bash
# 1. 导航到 App Store Connect
mcp__playwright__playwright_navigate \
  --url "https://appstoreconnect.apple.com/" \
  --waitUntil "networkidle"

# 2. 登录状态检查
mcp__playwright__playwright_get_visible_text

# 3. 导航到销售报告
mcp__playwright__playwright_click \
  --selector "a[href*='sales']"

# 4. 截图保存数据
mcp__playwright__playwright_screenshot \
  --name "appstore_sales_$(date +%Y%m%d)" \
  --savePng true

# 5. 获取数据表格
mcp__playwright__playwright_get_visible_html \
  --selector ".sales-table"
```

### 小程序后台数据采集

```
目标URL: https://mp.weixin.qq.com/

采集数据:
├── 访问数据
│   ├── 页面浏览量
│   ├── 访问人数
│   └── 访问次数
├── 用户数据
│   ├── 新增用户
│   ├── 活跃用户
│   └── 用户画像
├── 来源分析
│   ├── 搜索来源
│   ├── 分享来源
│   └── 广告来源
└── 留存数据
    ├── 次日留存
    ├── 7日留存
    └── 30日留存
```

### 小红书创作者中心数据采集

```
目标URL: https://creator.xiaohongshu.com/

采集数据:
├── 粉丝数据
│   ├── 粉丝总数
│   ├── 新增粉丝
│   └── 粉丝画像
├── 内容数据
│   ├── 发布笔记数
│   ├── 笔记曝光
│   └── 互动数据
├── 互动数据
│   ├── 点赞数
│   ├── 收藏数
│   └── 评论数
└── 收益数据 (如有)
    ├── 品牌合作
    └── 直播收益
```

### 抖音创作者中心数据采集

```
目标URL: https://creator.douyin.com/

采集数据:
├── 视频数据
│   ├── 发布视频数
│   ├── 总播放量
│   └── 平均播放
├── 粉丝数据
│   ├── 粉丝总数
│   ├── 新增粉丝
│   └── 粉丝画像
├── 互动数据
│   ├── 点赞数
│   ├── 评论数
│   └── 分享数
└── 收益数据 (如有)
    ├── 直播收益
    └── 商品带货
```

## 数据采集流程

### 自动化采集脚本

```bash
#!/bin/bash
# daily_data_collect.sh

DATE=$(date +%Y%m%d)

# App Store 数据
collect_appstore() {
  echo "采集 App Store 数据..."
  mcp__playwright__playwright_navigate \
    --url "https://appstoreconnect.apple.com/"
  mcp__playwright__playwright_screenshot \
    --name "appstore_${DATE}" \
    --savePng true
}

# 小程序数据
collect_miniapp() {
  echo "采集小程序数据..."
  mcp__playwright__playwright_navigate \
    --url "https://mp.weixin.qq.com/"
  mcp__playwright__playwright_screenshot \
    --name "miniapp_${DATE}" \
    --savePng true
}

# 小红书数据
collect_xiaohongshu() {
  echo "采集小红书数据..."
  mcp__playwright__playwright_navigate \
    --url "https://creator.xiaohongshu.com/"
  mcp__playwright__playwright_screenshot \
    --name "xiaohongshu_${DATE}" \
    --savePng true
}

# 执行采集
collect_appstore
collect_miniapp
collect_xiaohongshu
```

## 数据报告模板

### 日报模板

```
# [日期] 运营数据日报

## App Store
| 指标 | 今日 | 昨日 | 变化 |
|------|------|------|------|
| 下载量 | XXX | XXX | +X% |
| 收入 | ¥XXX | ¥XXX | +X% |
| 评分 | X.X | X.X | - |
| 活跃用户 | XXX | XXX | +X% |

## 小程序
| 指标 | 今日 | 昨日 | 变化 |
|------|------|------|------|
| 访问量 | XXX | XXX | +X% |
| 新增用户 | XX | XX | +X% |
| 页面浏览 | XXX | XXX | +X% |

## 小红书
| 指标 | 今日 | 昨日 | 变化 |
|------|------|------|------|
| 粉丝 | XXX | XXX | +X |
| 点赞 | XXX | XXX | +X |
| 收藏 | XX | XX | +X |

## 问题与机会
- 问题: ...
- 机会: ...

## 明日计划
- [ ] 计划1
- [ ] 计划2
```

### 周报模板

```
# [周期] 运营数据周报

## 本周总结
- 完成事项
- 关键成果

## 数据概览
| 平台 | 周下载/访问 | 周收入 | 周互动 |
|------|------------|--------|--------|
| App Store | XXXX | ¥XXXX | XXX |
| 小程序 | XXXX | - | XXX |
| 小红书 | - | - | XXXX |

## 数据趋势
- 图表: 下载/访问趋势
- 图表: 收入趋势
- 图表: 互动趋势

## 对比分析
- 与上周对比
- 与目标对比

## 下周计划
- [ ] 计划1
- [ ] 计划2
```

## 数据分析方法

### 关键指标定义

| 指标 | 计算方式 | 监控频率 |
|------|----------|----------|
| 日活 (DAU) | 每日活跃用户数 | 每日 |
| 月活 (MAU) | 每月活跃用户数 | 每月 |
| 留存率 | (第N日回访用户/当日新增) | 每日 |
| 转化率 | 完成目标用户/总访问 | 每周 |
| ARPU | 收入/活跃用户 | 每月 |

### 异常检测

```
数据异常判断:
├── 指标变化超过 ±20%
├── 连续3天同向变化
└── 单日极值 (历史最高/最低)

异常处理流程:
1. 发现异常数据
2. 排查原因 (活动/Bug/外部因素)
3. 记录异常
4. 调整分析口径 (如需要)
5. 恢复正常监控
```

## 最佳实践

### 数据采集
- 固定采集时间，确保数据可比
- 保存原始截图，作为凭证
- 建立数据字典，统一口径

### 数据分析
- 多维度交叉分析
- 关注趋势变化
- 关联业务事件
- 及时发现问题

### 数据报告
- 突出关键指标
- 量化而非定性
- 对比基准数据
- 提出行动建议