---
name: podcast-publish-xiaoyuzhou
description: |
  自动发布每日科技早报播客到小宇宙平台。
  触发场景：用户提到"发布播客"、"小宇宙播客"、"自动发布"、"播客上传"、"RSS发布"。
  适用于：将生成的播客音频自动发布到RSS.com，并通过RSS订阅同步到小宇宙，同时发送飞书通知。
---

# 播客发布到小宇宙 Skill

## 概述

此 Skill 实现了每日科技早报播客的全自动发布流程：播客生成 → RSS.com发布 → 小宇宙同步 → 飞书通知。

**项目路径**: `/Users/qitmac001395/workspace/QAL/ideas/apps/daily-podcast-ai`

## 核心能力

| 功能 | 状态 | 所需配置 |
|------|------|---------|
| 早报播客生成 | ✅ 可用 | ELEVENLABS_API_KEY |
| RSS.com自动发布 | ✅ 可用 | RSS_COM_API_KEY + RSS_COM_PODCAST_ID |
| 小宇宙RSS订阅 | ✅ 可用 | 一次性手动配置 |
| 飞书消息通知 | ✅ 可用 | FEISHU_APP_ID + FEISHU_APP_SECRET + FEISHU_RECEIVER_OPEN_ID |
| 定时自动执行 | ✅ 可用 | macOS launchd (每天7点) |

## 使用方法

### 方式1: 自动执行（推荐）

**无需操作**，每天早上7点自动运行：
```
07:00 - 从缓存读取新闻（0:00-6:00收集的30-50篇）
07:02 - AI优选Top 10新闻
07:05 - 生成对话脚本（双人播报模式）
07:10 - TTS语音合成（ElevenLabs）
07:15 - 合并音频 + 生成封面
07:17 - 发布到RSS.com
07:18 - 发送飞书通知
08:00 - 小宇宙自动同步
```

### 方式2: 手动发布指定日期

```bash
cd /Users/qitmac001395/workspace/QAL/ideas/apps/daily-podcast-ai

# 发布昨天的播客
python scripts/publish_to_rss.py --date 2026-01-14

# 生成今天的播客并发布
python scripts/daily_generate.py --from-cache && \
python scripts/publish_to_rss.py --date $(date +%Y-%m-%d)
```

### 方式3: 仅发送飞书通知

```bash
python scripts/notify_feishu.py \
  --date 2026-01-14 \
  --rss-url "https://rss.com/podcasts/xxx/feed.xml" \
  --episode-url "https://rss.com/podcasts/xxx/episodes/ep_xxx" \
  --article-count 10
```

---

## 首次配置指南

### 步骤1: RSS.com配置（5分钟）

1. **注册账号**: https://rss.com/ → Sign Up
2. **创建播客**: Dashboard → Create New Podcast
   ```
   名称: 今日科技早报
   分类: Technology / News
   语言: Chinese (Simplified)
   ```
3. **获取凭证**:
   - Settings → API Keys → Generate New API Key
   - 复制 API Key: `rss_com_sk_xxx`
   - 从播客URL获取 Podcast ID

4. **配置环境变量**:
   编辑 `apps/daily-podcast-ai/.env`：
   ```bash
   RSS_COM_API_KEY=rss_com_sk_your_actual_key
   RSS_COM_PODCAST_ID=your-podcast-uuid
   ```

### 步骤2: 小宇宙订阅配置（3分钟，仅需一次）

1. **登录创作者平台**: https://podcaster.xiaoyuzhoufm.com/podcasts/695e1e64e0970c835fb2e784/home
2. **添加RSS订阅**:
   - 设置 → RSS Feed设置
   - 输入: `https://rss.com/podcasts/{YOUR_ID}/feed.xml`
   - 点击「验证并导入」
3. **首次同步**: 点击「立即同步」

### 步骤3: 飞书通知配置（可选，5分钟）

1. **创建飞书应用**: https://open.feishu.cn/app
2. **添加权限**: `im:message` + `im:message:send_as_bot`
3. **配置环境变量**:
   ```bash
   FEISHU_APP_ID=cli_xxx
   FEISHU_APP_SECRET=xxx
   FEISHU_RECEIVER_OPEN_ID=ou_18b8063b232cbdec73ea1541dfb74890  # 王植萌
   ```

### 步骤4: 测试验证（2分钟）

```bash
# 测试发布
python scripts/publish_to_rss.py --date 2026-01-14

# 预期看到:
# ✅ Episode published successfully!
# 📱 发送飞书通知...
# ✅ 飞书消息发送成功
```

---

## 技术架构

### 集成流程图

```
┌─────────────┐
│ 早报生成     │  scripts/daily_generate.py
│ (每天7点)    │  - 从cache读取新闻
└──────┬──────┘  - AI优选Top 10
       │         - TTS语音合成
       ↓
┌─────────────┐
│ 输出文件     │  output/{date}/dailyReport/
│             │  - podcast-{date}-1.2x.mp3
│             │  - cover-{date}.png
└──────┬──────┘  - script-{date}.md
       │
       ↓
┌─────────────┐
│ RSS发布     │  scripts/publish_to_rss.py
│             │  - 上传音频到RSS.com
└──────┬──────┘  - 创建单集元数据
       │
       ├──────────────────┐
       ↓                  ↓
┌─────────────┐    ┌─────────────┐
│ RSS Feed    │    │ 飞书通知     │  scripts/notify_feishu.py
│ 更新        │    │             │  - 发送卡片消息
└──────┬──────┘    └─────────────┘  - 包含RSS链接
       │
       ↓ (每小时)
┌─────────────┐
│ 小宇宙同步   │  podcaster.xiaoyuzhoufm.com
│             │  - 自动抓取RSS
└─────────────┘  - 发布到App
```

### 关键文件

| 文件 | 行数 | 功能 |
|------|------|------|
| `scripts/publish_to_rss.py` | 376 | RSS.com发布主脚本 |
| `scripts/notify_feishu.py` | 191 | 飞书通知脚本 |
| `scripts/daily_generate.py` | 651 | 播客生成核心逻辑 |
| `scripts/daily_automated_run.sh` | 100 | 定时任务执行脚本 |
| `docs/XIAOYUZHOU_INTEGRATION.md` | - | 完整集成指南 |
| `QUICKSTART_XIAOYUZHOU.md` | - | 5分钟快速开始 |

### 环境变量清单

```bash
# 必需 - 播客生成
ELEVENLABS_API_KEY=sk_xxx          # TTS语音合成

# 可选 - AI增强
OPENAI_API_KEY=sk-xxx              # AI摘要和优选

# 必需 - RSS发布
RSS_COM_API_KEY=rss_com_sk_xxx    # RSS.com API
RSS_COM_PODCAST_ID=xxx-xxx-xxx     # 播客频道ID

# 可选 - 飞书通知
FEISHU_APP_ID=cli_xxx              # 飞书应用ID
FEISHU_APP_SECRET=xxx              # 飞书密钥
FEISHU_RECEIVER_OPEN_ID=ou_xxx     # 接收者Open ID
```

---

## 代码改进（已实现）

### 1. 智能文件名识别（publish_to_rss.py:258-269）

**问题**: 项目生成 `podcast-{date}-1.2x.mp3`，但脚本期望 `podcast-{date}.mp3`

**解决**: 自动查找并使用多速率版本
```python
audio_file = base_path / f"podcast-{args.date}.mp3"
if not audio_file.exists():
    audio_file_12x = base_path / f"podcast-{args.date}-1.2x.mp3"
    audio_file_15x = base_path / f"podcast-{args.date}-1.5x.mp3"

    if audio_file_12x.exists():
        audio_file = audio_file_12x
```

### 2. 多端点重试机制（publish_to_rss.py:106-159）

**问题**: RSS.com API端点可能变化

**解决**: 依次尝试3个可能的端点
```python
upload_endpoints = [
    f"{self.API_BASE_URL}/upload",
    f"{self.API_BASE_URL}/media",
    f"{self.API_BASE_URL}/podcasts/{self.podcast_id}/media"
]
```

### 3. 飞书通知集成（publish_to_rss.py:343-362）

**功能**: 发布成功后自动调用 `notify_feishu.py`

**特性**:
- 使用 `check=False` 避免通知失败中断主流程
- 自动提取文章数量
- 传递RSS URL和单集URL

---

## 飞书消息效果

发布成功后，接收者会收到蓝色卡片消息：

```
┌─────────────────────────────────────────┐
│ 🎙️ 今日科技早报已发布                    │
├─────────────────────────────────────────┤
│ 📅 日期: 2026-01-14                     │
│ 📰 内容: 精选 10 篇科技新闻              │
│                                         │
│ 📢 发布状态:                             │
│ - ✅ RSS.com 发布成功                    │
│ - ⏳ 小宇宙同步中（预计1小时内）          │
│                                         │
│ 🔗 单集链接: https://rss.com/...        │
│ 📡 RSS Feed: https://rss.com/...feed.xml│
│                                         │
│ ───────────────────────────────────────  │
│ 💡 小宇宙订阅步骤:                       │
│ 1. 打开小宇宙创作者平台                  │
│ 2. 点击「立即同步」查看最新单集          │
│ 3. 首次设置需添加RSS订阅（仅需一次）      │
└─────────────────────────────────────────┘
```

---

## 故障排查

### 常见问题

| 问题 | 症状 | 解决方案 |
|------|------|---------|
| RSS发布失败 | `401 Unauthorized` | 检查API Key是否正确/过期 |
| 文件找不到 | `Missing required files` | 确认播客已生成，检查output目录 |
| 小宇宙未同步 | RSS成功但App无单集 | 手动点击「立即同步」 |
| 飞书通知失败 | 发布成功但无消息 | 检查应用权限，验证open_id |
| API端点404 | `Endpoint not found` | 查看RSS.com最新API文档 |

### 调试命令

```bash
# 查看最近的生成日志
tail -50 logs/daily_run.log

# 检查错误日志
tail -50 logs/daily_error.log

# 验证RSS Feed可访问
curl -I "https://rss.com/podcasts/{YOUR_ID}/feed.xml"

# 验证环境变量
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); \
  print('RSS Key:', bool(os.getenv('RSS_COM_API_KEY'))); \
  print('Podcast ID:', bool(os.getenv('RSS_COM_PODCAST_ID')))"
```

---

## 使用场景

### 场景1: 每日自动发布（默认）

**触发**: 每天07:00自动执行
**流程**: 完整的生成 → 发布 → 通知
**无需操作**: 配置一次后永久生效

### 场景2: 补发昨天的播客

```bash
# 用户说: "帮我重新发布昨天的播客到小宇宙"
python scripts/publish_to_rss.py --date 2026-01-14
```

### 场景3: 仅通知不发布

```bash
# 用户说: "通知植萌播客已发布"
python scripts/notify_feishu.py \
  --date 2026-01-14 \
  --rss-url "https://rss.com/podcasts/xxx/feed.xml" \
  --article-count 10
```

### 场景4: 生成但不发布

```bash
# 用户说: "生成今天的播客但先不发布"
python scripts/daily_generate.py --from-cache
# 不运行 publish_to_rss.py
```

---

## 技术细节

### RSS.com API集成

**API版本**: v4
**Base URL**: https://api.rss.com/v4
**认证方式**: Bearer Token

**核心端点**:
```
POST /upload                           # 上传文件（主端点）
POST /media                            # 备选端点1
POST /podcasts/{id}/media              # 备选端点2
POST /podcasts/{id}/episodes           # 创建单集
GET  /podcasts/{id}/feed.xml           # RSS Feed
```

**文件上传**:
- 音频: 最大100MB，支持MP3/M4A
- 封面: 最大5MB，推荐3000x3000px PNG
- 超时: 120秒

### 小宇宙集成方式

**方式**: RSS订阅（非API上传）

**优势**:
- ✅ 一次配置，永久生效
- ✅ 无需逆向工程小宇宙API
- ✅ 官方支持，稳定可靠
- ✅ 支持多平台分发

**更新频率**:
- 默认: 每小时
- 可设置: 30分钟/2小时/4小时

### 飞书通知实现

**消息类型**: Interactive（卡片消息）

**卡片结构**:
```json
{
  "header": {"title": "🎙️ 今日科技早报已发布", "template": "blue"},
  "elements": [
    {"tag": "markdown", "content": "📅 日期: {date}\n📰 内容: 精选 {count} 篇..."}
  ]
}
```

**依赖库**: httpx>=0.27.0

---

## 监控与维护

### 日志位置

```
logs/
├── daily_run.log        # 主日志（生成+发布）
├── daily_error.log      # 错误日志
├── hourly-stdout.log    # 每小时收集日志
└── hourly-stderr.log    # 收集错误
```

### 关键日志搜索

```bash
# 查看最近5次发布状态
grep "Publication completed" logs/daily_run.log | tail -5

# 查看RSS发布错误
grep "RSS" logs/daily_error.log

# 查看飞书通知记录
grep "飞书通知" logs/daily_run.log | tail -5
```

### 数据清理

```bash
# 清理30天前的播客文件（节省空间）
find output/ -type d -mtime +30 -exec rm -rf {} +

# 清理缓存（保留最近7天）
find cache/ -name "*.json" -mtime +7 -delete
```

---

## 成本预估

### 每日成本

| 服务 | 用量 | 成本 |
|------|------|------|
| ElevenLabs TTS | 3-5分钟音频 | ¥1-2 |
| OpenAI GPT-4o-mini | 摘要+优选 | ¥0.5-1 |
| RSS.com | 3-5MB存储+流量 | 免费 |
| 小宇宙 | RSS订阅 | 免费 |
| 飞书API | 1条消息/天 | 免费 |

**月度总计**: ¥45-90（主要是ElevenLabs和OpenAI）

### 免费额度

- **ElevenLabs**: 10,000 credits/月（约10分钟）
- **OpenAI**: 需付费，但gpt-4o-mini成本极低
- **RSS.com**: 免费版支持5GB存储+流量
- **飞书**: 企业自建应用免费

---

## 扩展功能（可选）

### 1. 多平台分发

将同一个RSS Feed提交到：
- 小宇宙（已支持）
- 喜马拉雅
- 荔枝FM
- Apple Podcasts
- Spotify Podcasts

### 2. 数据分析

从RSS.com获取统计数据：
```bash
curl -H "Authorization: Bearer $RSS_COM_API_KEY" \
  "https://api.rss.com/v4/podcasts/$RSS_COM_PODCAST_ID/analytics"
```

### 3. 智能推送

根据播放数据优化：
- 调整发布时间（当前07:00）
- 优化新闻选择策略
- A/B测试不同播报风格

### 4. 批量操作

```bash
# 批量发布最近7天的播客
for date in $(seq -f "%Y-%m-%d" 7 -1 1); do
  python scripts/publish_to_rss.py --date $date
  sleep 10
done
```

---

## 注意事项

### 重要提醒

1. **API凭证安全**:
   - ✅ `.env` 已在 `.gitignore` 中
   - ❌ 不要将API Key提交到Git
   - ❌ 不要在日志中打印完整API Key

2. **文件命名规范**:
   - 项目生成带速率后缀的文件（`-1.2x.mp3`）
   - 发布脚本会自动识别
   - 优先使用1.2x版本（平衡时长和音质）

3. **错误处理策略**:
   - RSS发布失败 → 中断流程（需要人工介入）
   - 飞书通知失败 → 仅记录日志（不影响发布）
   - 小宇宙同步延迟 → 可手动触发

4. **RSS Feed更新频率**:
   - RSS.com: 实时更新
   - 小宇宙: 每小时抓取（可配置）
   - 加速同步: 手动点击「立即同步」

---

## 相关资源

### 官方文档
- **RSS.com API**: https://api.rss.com/v4/docs
- **小宇宙创作者指南**: https://podcaster.xiaoyuzhoufm.com/help
- **飞书开放平台**: https://open.feishu.cn/document/

### 项目文档
- **完整集成指南**: [docs/XIAOYUZHOU_INTEGRATION.md](../../apps/daily-podcast-ai/docs/XIAOYUZHOU_INTEGRATION.md)
- **快速开始**: [QUICKSTART_XIAOYUZHOU.md](../../apps/daily-podcast-ai/QUICKSTART_XIAOYUZHOU.md)
- **主项目README**: [apps/daily-podcast-ai/README.md](../../apps/daily-podcast-ai/README.md)

### 工具链接
- **Feed验证**: https://validator.w3.org/feed/
- **卡片消息构建**: https://open.feishu.cn/tool/cardbuilder
- **ElevenLabs管理**: https://elevenlabs.io/app/

---

## 更新记录

- **2026-01-15**: 初始版本，支持RSS.com自动发布和小宇宙订阅
- **2026-01-15**: 添加飞书通知功能（王植萌）
- **2026-01-15**: 修复多速率音频文件名识别问题
- **2026-01-15**: 增强API错误处理，支持多端点重试

---

## Skill维护者

- **创建者**: Claude Code
- **项目**: daily-podcast-ai
- **版本**: v1.0.0
- **最后更新**: 2026-01-15
