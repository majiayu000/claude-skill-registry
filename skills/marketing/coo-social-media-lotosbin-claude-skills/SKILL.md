---
name: coo-social-media
description: COO 社交媒体运营技能，使用 Playwright MCP 实现小红书、抖音、微信公众号、视频号的自动化运营
version: 1.0.0
---

# COO 社交媒体运营技能

## 触发条件
当用户提到以下内容时自动触发:
- "小红书运营"
- "抖音运营"
- "公众号运营"
- "视频号运营"
- "社交媒体发布"
- "社交媒体数据"

## 核心能力

### Playwright MCP 集成

使用 `playwright` MCP 进行社交媒体自动化操作:

```bash
# 导航到指定页面
mcp__playwright__playwright_navigate --url "https://www.xiaohongshu.com/..."

# 页面截图
mcp__playwright__playwright_screenshot --name "screenshot" --savePng true

# 获取页面内容
mcp__playwright__playwright_get_visible_text

# 获取页面HTML
mcp__playwright__playwright_get_visible_html

# 点击元素
mcp__playwright__playwright_click --selector "CSS选择器"

# 输入内容
mcp__playwright__playwright_fill --selector "CSS选择器" --value "内容"

# 滚动页面
mcp__playwright__playwright_evaluate --script "window.scrollTo(0, document.body.scrollHeight)"
```

### 小红书运营

#### 发布笔记

```
1. 导航到小红书创作者中心
2. 点击"发布笔记"
3. 填写标题 (建议格式: 【分类】内容描述)
4. 上传封面图
5. 填写正文内容
6. 添加话题标签
7. 点击发布

mcp__playwright__playwright_navigate --url "https://creator.xiaohongshu.com/"
```

#### 数据分析

```
1. 导航到数据中心
2. 查看笔记数据
   - 浏览量
   - 点赞数
   - 收藏数
   - 评论数
3. 截图保存数据
4. 获取页面文本进行分析
```

### 抖音运营

#### 发布视频

```
1. 导航到抖音创作者平台
2. 点击"发布视频"
3. 上传视频文件
4. 填写视频文案 (不超过50字)
5. 添加话题标签
6. 点击发布

mcp__playwright__playwright_navigate --url "https://creator.douyin.com/"
```

#### 数据分析

```
1. 导航到数据中心
2. 查看视频数据
   - 播放量
   - 点赞数
   - 评论数
   - 分享数
3. 获取互动数据
```

### 微信公众号运营

#### 发布文章

```
1. 登录微信公众号后台
2. 点击"写新文章"
3. 填写标题
4. 编写正文 (支持HTML格式)
5. 设置封面图
6. 填写摘要
7. 点击发布

mcp__playwright__playwright_navigate --url "https://mp.weixin.qq.com/"
```

#### 数据分析

```
1. 导航到数据统计
2. 查看文章数据
   - 阅读量
   - 在看数
   - 点赞数
   - 分享数
3. 获取用户数据
```

### 视频号运营

#### 发布视频

```
1. 登录视频号管理后台
2. 点击"发布视频"
3. 上传视频
4. 填写视频文案
5. 添加话题
6. 点击发布
```

#### 数据分析

```
1. 查看视频数据
   - 播放量
   - 点赞数
   - 评论数
   - 分享数
2. 获取用户画像
```

## 运营流程

### 每日运营

```
每日流程:
├── 08:00 - 检查各平台消息和评论
├── 09:00 - 回复用户问题和反馈
├── 10:00 - 发布当日内容 (如计划中)
├── 14:00 - 数据监控和互动
├── 17:00 - 数据汇总和报告
└── 18:00 - 次日内容准备
```

### 内容发布流程

```
1. 内容策划
   ├── 确定发布平台
   ├── 准备素材 (图片/视频/文案)
   └── 设定发布时间

2. 内容创作
   ├── 撰写文案
   ├── 制作素材
   └── 预览确认

3. 发布执行
   ├── 登录各平台
   ├── 上传内容
   └── 发布确认

4. 数据追踪
   ├── 监控发布状态
   ├── 记录初始数据
   └── 跟进互动
```

## 内容模板

### 小红书笔记模板

```
标题: 【分类】内容描述
封面: 吸引眼球的图片
正文:
1. 开场吸引 (痛点/解决方案)
2. 产品介绍
3. 使用场景
4. 行动号召 (下载/关注)
标签: #效率工具 #AI #产品名
```

### 抖音视频模板

```
视频时长: 15-60秒
文案: 不超过50字
话题: 相关话题标签
```

### 微信公众号模板

```
标题: 文章标题 (不超过64字)
摘要: 文章摘要
正文: HTML格式内容 (2000-5000字)
封面: 封面图片URL
作者: 作者名
```

## 数据采集

### 使用 Playwright 采集数据

```bash
# 采集小红书数据
mcp__playwright__playwright_navigate \
  --url "https://creator.xiaohongshu.com/"

# 截图保存
mcp__playwright__playwright_screenshot \
  --name "xiaohongshu_data_$(date +%Y%m%d)" \
  --savePng true

# 获取文本
mcp__playwright__playwright_get_visible_text

# 获取HTML
mcp__playwright__playwright_get_visible_html \
  --selector ".data-section"
```

### 数据汇总模板

```
# [日期] 社交媒体数据报告

## 小红书
| 指标 | 数值 | 变化 |
|------|------|------|
| 粉丝数 | XXX | +XX |
| 笔记数 | XX | +X |
| 平均点赞 | XXX | +XX% |

## 抖音
| 指标 | 数值 | 变化 |
|------|------|------|
| 粉丝数 | XXX | +XX |
| 视频数 | XX | +X |
| 平均播放 | XXXX | +XX% |

## 微信公众号
| 指标 | 数值 | 变化 |
|------|------|------|
| 粉丝数 | XXX | +XX |
| 文章数 | XX | +X |
| 平均阅读 | XXX | +XX% |
```

## 最佳实践

### 内容优化
- 标题要吸引眼球
- 封面图要清晰美观
- 内容要有价值
- 保持更新频率

### 互动策略
- 及时回复评论
- 积极与用户互动
- 关注热点话题
- 参与平台活动

### 数据分析
- 定期分析数据
- 找出爆款规律
- 优化内容策略
- 跟踪竞品动态