---
name: xiaohongshu-skill
description: 当用户想要与小红书（xiaohongshu/rednote）交互时使用此 Skill。包括搜索笔记、获取帖子详情、查看用户主页、二维码扫码登录、发布笔记（图文/视频/长文/Markdown）、评论互动（发表/回复/通知页回复）、点赞收藏、浏览推荐流、写作模板生成、运营策略管理、SOP 编排等。当用户提到 xiaohongshu、小红书、rednote，或需要浏览/抓取/发布/互动中国社交媒体内容时激活此 Skill。
user-invokable: true
metadata: {"openclaw": {"emoji": "📕", "requires": {"bins": ["python3", "playwright"], "anyBins": ["python3", "python"]}, "os": ["win32", "linux", "darwin"], "install": [{"id": "pip", "kind": "node", "label": "Install dependencies (pip)", "bins": ["playwright"]}]}}
---

# 小红书 Skill

基于 Python Playwright 的小红书（rednote）全功能交互工具，通过浏览器自动化从 `window.__INITIAL_STATE__`（Vue SSR 状态）中提取结构化数据，并支持发布、互动、运营管理等操作。

## 前置条件

在 `{baseDir}` 目录下安装依赖：

```bash
cd {baseDir}
pip install -r requirements.txt
playwright install chromium
```

Linux/WSL 环境还需运行：
```bash
playwright install-deps chromium
```

## 快速开始

所有命令从 `{baseDir}` 目录运行。

### 1. 登录（首次必须）

```bash
cd {baseDir}

# 打开浏览器窗口，显示二维码供微信/小红书扫描
python -m scripts qrcode --headless=false

# 检查登录是否仍然有效
python -m scripts check-login
```

在无头环境下，二维码图片保存到 `{baseDir}/data/qrcode.png`，可通过其他渠道发送扫码。

### 2. 搜索

```bash
cd {baseDir}

# 基础搜索
python -m scripts search "关键词"

# 带筛选条件
python -m scripts search "美食" --sort-by=最新 --note-type=图文 --limit=10
```

**筛选选项：**
- `--sort-by`：综合、最新、最多点赞、最多评论、最多收藏
- `--note-type`：不限、视频、图文
- `--publish-time`：不限、一天内、一周内、半年内
- `--search-scope`：不限、已看过、未看过、已关注
- `--location`：不限、同城、附近

### 3. 帖子详情

```bash
cd {baseDir}

# 使用搜索结果中的 id 和 xsec_token
python -m scripts feed <feed_id> <xsec_token>

# 加载评论
python -m scripts feed <feed_id> <xsec_token> --load-comments --max-comments=20
```

### 4. 用户主页

```bash
cd {baseDir}

# 查看指定用户主页
python -m scripts user <user_id> [xsec_token]

# 查看自己的主页
python -m scripts me
```

### 5. 评论互动

```bash
cd {baseDir}

# 发表评论
python -m scripts comment <feed_id> <xsec_token> --content="好棒的笔记！"

# 回复评论
python -m scripts reply <feed_id> <xsec_token> --comment-id=<comment_id> --reply-user-id=<user_id> --content="感谢分享"

# 通过通知页回复（更安全的回复方式）
python -m scripts reply-notification --content="谢谢关注" --index=0
```

### 6. 点赞 / 收藏

```bash
cd {baseDir}

# 点赞 / 取消点赞
python -m scripts like <feed_id> <xsec_token>
python -m scripts unlike <feed_id> <xsec_token>

# 收藏 / 取消收藏
python -m scripts collect <feed_id> <xsec_token>
python -m scripts uncollect <feed_id> <xsec_token>
```

### 7. 首页推荐流

```bash
cd {baseDir}
python -m scripts explore --limit=20
```

### 8. 发布笔记

```bash
cd {baseDir}

# 发布图文笔记（默认停在发布按钮处，加 --auto-publish 自动发布）
python -m scripts publish --title="标题" --content="正文" --images="img1.jpg,img2.jpg" --tags="旅行,美食"

# 发布视频笔记
python -m scripts publish-video --title="标题" --content="描述" --video="video.mp4" --tags="vlog"

# Markdown 渲染为图片后发布
python -m scripts publish-md --title="标题" --file=article.md --tags="干货"
python -m scripts publish-md --title="标题" --text="# 正文\n内容..." --width=1080

# 发布长文笔记（创作者中心"写长文"功能）
python -m scripts publish-longform --title="长文标题" --content="长文正文内容..."

# 定时发布
python -m scripts publish --title="标题" --content="正文" --images="img.jpg" --schedule-time="2025-03-01 12:00"
```

### 9. 写作模板

```bash
cd {baseDir}

# 生成写作模板（含标题建议、内容框架、标签推荐）
python -m scripts template --topic="旅行攻略"
python -m scripts template --topic="美食探店" --type=视频
python -m scripts template --topic="学习方法" --type=长文
```

### 10. 运营策略

```bash
cd {baseDir}

# 初始化账号定位
python -m scripts strategy-init --persona="旅行博主" --audience="18-35岁旅行爱好者" --direction="旅行攻略,小众目的地"

# 查看当前策略
python -m scripts strategy-show

# 检查每日互动配额
python -m scripts strategy-check-limit --limit-type=likes
python -m scripts strategy-check-limit --limit-type=comments

# 添加内容日历
python -m scripts strategy-add-post --date="2025-03-01" --topic="春日出行攻略" --type=图文
```

### 11. SOP 编排

```bash
cd {baseDir}

# 发布 SOP（选题分析 → 内容校验 → 模板生成 → 发布准备）
python -m scripts sop --type=publish --topic="旅行攻略" --note-type=图文

# 推荐流互动 SOP（模拟自然浏览行为）
python -m scripts sop --type=explore --feed-count=10 --like-prob=0.3 --collect-prob=0.1

# 评论互动 SOP（逐条回复，配额控制）
python -m scripts sop --type=comment --replies='[{"feed_id":"abc","xsec_token":"xyz","content":"好棒"}]'
```

## 数据提取路径

| 数据类型 | JavaScript 路径 |
|----------|----------------|
| 搜索结果 | `window.__INITIAL_STATE__.search.feeds` |
| 帖子详情 | `window.__INITIAL_STATE__.note.noteDetailMap` |
| 互动状态 | `window.__INITIAL_STATE__.note.noteDetailMap[id].note.interactInfo` |
| 用户信息 | `window.__INITIAL_STATE__.user.userPageData` |
| 用户笔记 | `window.__INITIAL_STATE__.user.notes` |
| 推荐流   | `window.__INITIAL_STATE__.feed.feeds` |

**Vue Ref 处理：** 始终通过 `.value` 或 `._value` 解包：
```javascript
const data = obj.value !== undefined ? obj.value : obj._value;
```

## 反爬保护与防封体系

本 Skill 内置了完善的防封措施（基于 xiaohongshu-ops 安全理念）：

- **频率控制**：两次导航间自动延迟 3-6 秒，每 5 次连续请求后冷却 10 秒
- **人性化互动**：点击前随机延迟 1-2.5s，点击后冷却 5-12s，每 3 次交互批次冷却 15-30s
- **人性化发布**：标题填写延迟 0.5-1.5s，正文逐字输入延迟 20-60ms/字，步骤间随机等待
- **频率限制检测**：自动检测 toast 提示（"频繁"、"操作太快"、"稍后再试"）
- **失败重试**：评论提交失败后自动重试一次（间隔 2-4s）
- **验证码检测**：自动检测安全验证页面重定向，触发时抛出 `CaptchaError`
- **每日配额管理**：策略模块追踪每日互动次数，防止超限

**触发验证码时的处理：**
1. 等待几分钟后重试
2. 运行 `cd {baseDir} && python -m scripts qrcode --headless=false` 手动通过验证
3. 如 Cookie 失效，重新扫码登录

## 输出格式

所有命令输出 JSON 到标准输出。搜索结果示例：
```json
{
  "id": "abc123",
  "xsec_token": "ABxyz...",
  "title": "帖子标题",
  "type": "normal",
  "user": "用户名",
  "user_id": "user123",
  "liked_count": "1234",
  "collected_count": "567",
  "comment_count": "89"
}
```

## 文件结构

```
{baseDir}/
├── SKILL.md              # 本文件（Skill 规范）
├── README.md             # 项目文档
├── requirements.txt      # Python 依赖
├── LICENSE               # MIT 许可证
├── data/                 # 运行时数据（二维码、调试输出）
├── scripts/              # 核心模块
│   ├── __init__.py       # 模块导出（v1.2.0）
│   ├── __main__.py       # CLI 入口（22+ 子命令）
│   ├── client.py         # 浏览器客户端封装（频率控制 + 验证码检测）
│   ├── login.py          # 二维码扫码登录流程
│   ├── search.py         # 搜索（支持多种筛选）
│   ├── feed.py           # 帖子详情提取
│   ├── user.py           # 用户主页提取
│   ├── comment.py        # 评论互动（发表/回复/通知页回复 + 人性化延迟 + 重试）
│   ├── interact.py       # 点赞收藏（人性化延迟 + 频率检测 + 批次冷却）
│   ├── explore.py        # 首页推荐流提取
│   ├── publish.py        # 发布（图文/视频/Markdown/长文 + 人性化延迟）
│   ├── templates.py      # 写作模板引擎（标题生成/内容模板/标签推荐/校验）
│   ├── strategy.py       # 运营策略管理（配额追踪/内容日历/账号定位）
│   └── sop.py            # SOP 编排引擎（发布/评论/推荐流互动 SOP）
└── tests/                # 单元测试
    ├── test_client.py
    ├── test_login.py
    ├── test_search.py
    ├── test_feed.py
    ├── test_user.py
    ├── test_comment.py
    ├── test_interact.py
    ├── test_publish.py
    ├── test_templates.py
    ├── test_strategy.py
    └── test_sop.py
```

## 跨平台兼容性

| 环境 | 无头模式 | 有头模式（扫码登录） | 备注 |
|------|----------|----------------------|------|
| Windows | 支持 | 支持 | 主要开发环境 |
| WSL2 (Win11) | 支持 | 通过 WSLg 支持 | 需要 `playwright install-deps` |
| Linux 服务器 | 支持 | 不适用 | 二维码保存为图片文件 |

## 注意事项

1. **Cookie 过期**：Cookie 会定期过期，`check-login` 返回 false 时需重新登录
2. **频率限制**：过度抓取会触发验证码，请依赖内置的频率控制
3. **xsec_token**：Token 与会话绑定，始终使用搜索/用户结果中的最新 Token
4. **配额管理**：使用 `strategy-check-limit` 查看当日剩余配额，避免超限
5. **仅供学习**：请遵守小红书的使用条款，本工具仅用于学习研究
