---
name: xiaohongshu-skill
description: 小红书全功能工具。搜帖子、看详情、刷推荐流、发笔记（图文/视频/长文/Markdown）、二维码登录、评论点赞收藏、写模板、管策略、跑 SOP。兼容 Claude Code / OpenClaw / Codex / Hermes Agent 等支持 AgentSkills 规范的平台。提到 xiaohongshu、小红书、rednote、帮我搜下小红书、发到小红书、小红书上怎么说的、找 rednote 攻略、看看小红书上有没有、小红书上有个帖子就触发。
user-invokable: true
metadata: {"openclaw": {"emoji": "📕", "requires": {"bins": ["python3", "playwright"], "anyBins": ["python3", "python"]}, "os": ["win32", "linux", "darwin"], "install": [{"id": "pip", "kind": "node", "label": "Install dependencies (pip)", "bins": ["playwright"]}]}}
---

# 小红书 Skill

用 Python Playwright 驱动浏览器操作小红书。数据从 `window.__INITIAL_STATE__`（Vue SSR 状态对象）里取。搜索、发布、互动、运营全在这。

## 写操作安全规则

下面这些命令会真的改动账号数据。跑之前**必须**让用户确认：

1. **发布笔记** -- 先展示标题、正文、图片列表。用户说"发"才发。
2. **评论/回复** -- 先展示要发出去的内容。用户说"发"才发。
3. **点赞/收藏** -- 先展示目标帖子。用户说"行"才执行。

用 `AskUserQuestion` 弹确认框。别自己决定。

## 前置条件

在 `{baseDir}` 目录装依赖：

```bash
cd {baseDir}
pip install -r requirements.txt
playwright install chromium
```

Linux/WSL 还要跑：

```bash
playwright install-deps chromium
```

## 快速开始

所有命令从 `{baseDir}` 目录跑。

### 1. 登录（第一次必须做）

```bash
cd {baseDir}

# 弹出浏览器窗口，显示二维码，用微信或小红书 App 扫
python -m scripts qrcode --headless=false

# 检查登录还在不在
python -m scripts check-login
```

无头环境里二维码存到 `{baseDir}/data/qrcode.png`。传给别人扫也行。

### 2. 搜索

```bash
cd {baseDir}

# 基本搜索
python -m scripts search "关键词"

# 带条件
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

# 用搜索结果里的 id 和 xsec_token
python -m scripts feed <feed_id> <xsec_token>

# 同时加载评论
python -m scripts feed <feed_id> <xsec_token> --load-comments --max-comments=20
```

### 4. 用户主页

```bash
cd {baseDir}

# 看别人的主页
python -m scripts user <user_id> [xsec_token]

# 看自己的主页
python -m scripts me
```

### 5. 评论互动

**先确认再发。** 跑之前用 `AskUserQuestion` 把评论内容亮出来让用户确认。

```bash
cd {baseDir}

# 发评论
python -m scripts comment <feed_id> <xsec_token> --content="好棒的笔记！"

# 回复别人的评论
python -m scripts reply <feed_id> <xsec_token> --comment-id=<comment_id> --reply-user-id=<user_id> --content="感谢分享"

# 通过通知页回复（更安全）
python -m scripts reply-notification --content="谢谢关注" --index=0
```

### 6. 点赞 / 收藏

**先确认再操作。** 用 `AskUserQuestion` 把目标帖子亮出来让用户确认。

```bash
cd {baseDir}

# 点赞 / 取消
python -m scripts like <feed_id> <xsec_token>
python -m scripts unlike <feed_id> <xsec_token>

# 收藏 / 取消
python -m scripts collect <feed_id> <xsec_token>
python -m scripts uncollect <feed_id> <xsec_token>
```

### 7. 首页推荐流

```bash
cd {baseDir}
python -m scripts explore --limit=20
```

### 8. 发布笔记

**先确认再发。** 跑之前用 `AskUserQuestion` 把标题、正文、图片亮出来让用户确认。

```bash
cd {baseDir}

# 图文笔记（默认停在发布按钮，加 --auto-publish 自动发）
python -m scripts publish --title="标题" --content="正文" --images="img1.jpg,img2.jpg" --tags="旅行,美食"

# 视频笔记
python -m scripts publish-video --title="标题" --content="描述" --video="video.mp4" --tags="vlog"

# Markdown 渲染成图片再发
python -m scripts publish-md --title="标题" --file=article.md --tags="干货"
python -m scripts publish-md --title="标题" --text="# 正文\n内容..." --width=1080

# 长文笔记（创作者中心"写长文"）
python -m scripts publish-longform --title="长文标题" --content="长文正文内容..."

# 定时发布
python -m scripts publish --title="标题" --content="正文" --images="img.jpg" --schedule-time="2025-03-01 12:00"
```

### 9. 写作模板

```bash
cd {baseDir}

# 生成模板（标题建议 + 内容框架 + 标签推荐）
python -m scripts template --topic="旅行攻略"
python -m scripts template --topic="美食探店" --type=视频
python -m scripts template --topic="学习方法" --type=长文
```

### 10. 运营策略

```bash
cd {baseDir}

# 设账号定位
python -m scripts strategy-init --persona="旅行博主" --audience="18-35岁旅行爱好者" --direction="旅行攻略,小众目的地"

# 看当前策略
python -m scripts strategy-show

# 查今日互动配额
python -m scripts strategy-check-limit --limit-type=likes
python -m scripts strategy-check-limit --limit-type=comments

# 加内容日历
python -m scripts strategy-add-post --date="2025-03-01" --topic="春日出行攻略" --type=图文
```

### 11. SOP 编排

```bash
cd {baseDir}

# 发布 SOP（选题分析 -> 内容校验 -> 模板生成 -> 发布准备）
python -m scripts sop --type=publish --topic="旅行攻略" --note-type=图文

# 推荐流互动 SOP（模拟真人浏览行为）
python -m scripts sop --type=explore --feed-count=10 --like-prob=0.3 --collect-prob=0.1

# 评论互动 SOP（逐条回复，带配额控制）
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

**Vue Ref 解包：** 始终用 `.value` 或 `._value`：

```javascript
const data = obj.value !== undefined ? obj.value : obj._value;
```

## 反爬保护

内置多层防护，尽量避免触发验证码：

- **频率控制**：两次导航间自动等 3-6 秒。连续 5 次请求后冷却 10 秒。
- **真人化延迟**：点击前等 1-2.5s，点击后冷却 5-12s。每 3 次交互批次冷却 15-30s。
- **真人化发布**：标题填写延迟 0.5-1.5s。正文逐字输入，每字 20-60ms。步骤间隔随机。
- **频率检测**：自动识别 toast 提示（"频繁"、"操作太快"、"稍后再试"）。
- **失败重试**：评论提交失败自动重试一次（间隔 2-4s）。
- **验证码检测**：检测到安全验证重定向时抛出 `CaptchaError`。
- **每日配额**：策略模块追踪每天互动次数，防止超。

**触发验证码了怎么办：**

1. 等几分钟再试。
2. 跑 `cd {baseDir} && python -m scripts qrcode --headless=false` 手动过验证。
3. Cookie 失效了就重新扫码登录。

## 输出格式

所有命令输出 JSON。搜索结果长这样：

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
├── SKILL.md              # 本文件
├── README.md             # 项目文档
├── requirements.txt      # Python 依赖
├── LICENSE               # MIT
├── data/                 # 运行时数据（二维码、调试输出）
├── scripts/              # 核心模块
│   ├── __init__.py       # 模块导出（v1.3.0）
│   ├── __main__.py       # CLI 入口（22+ 子命令）
│   ├── client.py         # 浏览器客户端（频率控制 + 验证码检测）
│   ├── login.py          # 二维码登录流程
│   ├── search.py         # 搜索（多条件筛选）
│   ├── feed.py           # 帖子详情提取
│   ├── user.py           # 用户主页提取
│   ├── comment.py        # 评论（发表/回复/通知页 + 延迟 + 重试）
│   ├── interact.py       # 点赞收藏（延迟 + 频率检测 + 批次冷却）
│   ├── explore.py        # 推荐流提取
│   ├── publish.py        # 发布（图文/视频/Markdown/长文 + 延迟）
│   ├── templates.py      # 写作模板引擎
│   ├── strategy.py       # 运营策略（配额/日历/定位）
│   └── sop.py            # SOP 编排引擎
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

## 跨平台兼容

| 环境 | 无头模式 | 有头（扫码登录） | 备注 |
|------|----------|-----------------|------|
| Windows | OK | OK | 主力开发环境 |
| WSL2 (Win11) | OK | 用 WSLg | 需要 `playwright install-deps` |
| Linux 服务器 | OK | 不适用 | 二维码存图片文件 |

## 注意

1. **Cookie 过期**：定期会过期。`check-login` 返回 false 就重新登录。
2. **频率限制**：猛抓会出验证码。别关内置频率控制。
3. **xsec_token**：跟会话绑定的。始终用搜索结果里最新的。
4. **配额管理**：用 `strategy-check-limit` 查剩余配额，别超过。
5. **别滥用**：会封号。本工具仅供学习研究用。
