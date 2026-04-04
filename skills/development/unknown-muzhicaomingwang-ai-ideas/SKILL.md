# zhimeng-agent 自动化任务技能

> 个人自动化任务集合，通过 macOS launchd 定时调度，自动执行日常任务并同步到多个平台。

## 概览

```
zhimeng-agent/
├── tasks/
│   ├── config.py              # 统一配置
│   ├── sync_utils.py          # 多平台同步工具
│   ├── daily_report/          # 日报生成（0:00）
│   ├── email_organizer/       # 邮箱整理（2:00）
│   ├── desktop_organizer/     # 桌面整理（4:00）
│   ├── tech_news/             # 科技新闻（7:00）
│   └── launchd/               # macOS 定时任务配置
├── logs/                      # 运行日志
└── SKILL.md                   # 本文档
```

## 任务列表

| 任务 | 调度时间 | 功能 | 输出目标 |
|------|----------|------|----------|
| daily-report | 每天 00:00 | 生成每日工作报告 | Git, Notion, Feishu, Obsidian |
| email-organizer | 每天 02:00 | 自动归档邮件 | Obsidian |
| desktop-organizer | 每天 04:00 | 整理桌面和下载目录 | Obsidian |
| tech-news | 每天 07:00 | 聚合科技新闻 | Obsidian, Feishu |

---

## 1. 日报生成 (daily-report)

### 功能
- 从 Git 仓库提取当日提交记录
- 整合 Claude Code 会话摘要
- 生成结构化的工作日报

### 数据源
- Git commits（指定仓库目录）
- Claude Code sessions（`~/.claude/projects/`）

### 输出
```markdown
# 2026-01-07 工作日报

## 代码提交
- feat(plan): 实现方案生成核心流程

## Claude Code 会话
- 4 个会话，总交互 23 轮

## 统计
- 提交数: 5
- 会话数: 4
```

### 手动运行
```bash
cd /Users/qitmac001395/workspace/QAL/ideas/apps/zhimeng-agent
poetry run python -m tasks.daily_report.main --dry-run  # 仅生成不同步
poetry run python -m tasks.daily_report.main            # 生成并同步
```

---

## 2. 邮箱整理 (email-organizer)

### 功能
- 使用 himalaya CLI 连接 Gmail
- 自动归档通知类邮件
- 按发件人分类统计

### 归档规则
优先归档以下类型：
- 社交平台通知（LinkedIn, Twitter, Reddit 等）
- 技术平台通知（GitHub, Stack Overflow 等）
- 新闻简报（newsletter, digest 等）
- 自动邮件（noreply, mailer 等）

### 前置条件
1. 安装 himalaya CLI：`brew install himalaya`
2. 配置 Gmail App Password
3. 创建配置文件 `~/.himalaya-config/himalaya/config.toml`

### 手动运行
```bash
poetry run python -m tasks.email_organizer.main --dry-run  # 仅分析
poetry run python -m tasks.email_organizer.main            # 执行归档
```

---

## 3. 桌面整理 (desktop-organizer)

### 功能
- 扫描桌面和下载目录
- 按文件类型分类移动
- 清理超过30天的旧文件

### 整理规则

| 文件类型 | 目标目录 |
|----------|----------|
| 图片 (.png, .jpg, .gif) | ~/Pictures/Desktop-Archive/ |
| 文档 (.pdf, .doc, .md) | ~/Documents/Desktop-Archive/ |
| 压缩包 (.zip, .tar) | ~/Downloads/Archives/ |
| 代码 (.py, .js, .java) | ~/Documents/Code-Archive/ |
| 其他 | ~/Documents/Desktop-Other/ |

### 安全特性
- 不删除任何文件，仅移动
- 保留最近7天的文件在原位
- 生成详细的移动日志

### 手动运行
```bash
poetry run python -m tasks.desktop_organizer.main --dry-run  # 仅预览
poetry run python -m tasks.desktop_organizer.main            # 执行整理
```

---

## 4. 科技新闻 (tech-news)

### 功能
- 抓取 Hacker News 热门文章
- 获取 GitHub 24小时热门仓库
- 生成每日科技早报

### 数据源
- Hacker News Top Stories（默认15条）
- GitHub Trending（默认10个仓库）

### 输出格式
```markdown
# 2026-01-07 (周二) 科技早报

## Hacker News 热门
1. [Article Title](url) (320分, 45评论)

## GitHub 热门仓库
- **[owner/repo](url)** ⭐ 1234 `Python` `AI`
  > Repository description
```

### 手动运行
```bash
poetry run python -m tasks.tech_news.main --dry-run           # 仅生成
poetry run python -m tasks.tech_news.main --hn-count 20       # 自定义数量
poetry run python -m tasks.tech_news.main                     # 生成并同步
```

---

## 安装与管理

### 安装定时任务
```bash
cd /Users/qitmac001395/workspace/QAL/ideas/apps/zhimeng-agent/tasks/launchd
./install.sh install
```

### 查看任务状态
```bash
./install.sh status
```

### 立即执行任务
```bash
./install.sh run daily-report
./install.sh run tech-news
```

### 卸载定时任务
```bash
./install.sh uninstall
```

### 查看运行日志
```bash
# 标准输出
tail -f logs/daily-report.log
tail -f logs/tech-news.log

# 错误日志
tail -f logs/daily-report.error.log
```

---

## 配置

### 环境变量

在 `.env` 文件中配置：

```bash
# 飞书配置
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret

# OpenAI（用于摘要生成，可选）
OPENAI_API_KEY=your_api_key

# Notion（可选）
NOTION_TOKEN=your_token
```

### 核心配置文件

`tasks/config.py` 包含所有可调整参数：

```python
@dataclass
class TaskConfig:
    # 调度时间（小时）
    DAILY_REPORT_HOUR: int = 0
    EMAIL_ORGANIZE_HOUR: int = 2
    DESKTOP_ORGANIZE_HOUR: int = 4
    TECH_NEWS_HOUR: int = 7

    # 路径配置
    IDEAS_ROOT: Path = Path("/Users/qitmac001395/workspace/QAL/ideas")
    OBSIDIAN_VAULT: Path = Path("/Users/qitmac001395/Documents/Obsidian Vault")

    # 飞书接收者
    FEISHU_RECIPIENT_OPEN_ID: str = "ou_18b8063b232cbdec73ea1541dfb74890"
```

---

## 同步平台

### Obsidian
- 直接写入 Markdown 文件到 Obsidian Vault
- 按任务类型分目录：`Journal/`, `News/`, `Reports/`

### 飞书
- 通过飞书 API 发送消息
- 支持富文本和 Markdown 格式

### Notion
- 通过 Notion API 创建页面
- 支持父页面指定

### Git
- 自动提交日报到指定仓库
- Commit message 包含日期和摘要

---

## 故障排查

### 任务未执行
```bash
# 检查任务是否加载
launchctl list | grep zhimeng

# 手动触发测试
launchctl start com.zhimeng.tech-news

# 查看系统日志
log show --predicate 'subsystem == "com.apple.launchd"' --last 1h | grep zhimeng
```

### Python 环境问题
```bash
# 确认 Poetry virtualenv 路径正确
poetry env info --path

# 测试模块导入
poetry run python -c "from tasks.config import config; print(config)"
```

### 权限问题
```bash
# 确保脚本可执行
chmod +x tasks/launchd/install.sh

# 确保 Python 可执行
ls -la /Users/qitmac001395/Library/Caches/pypoetry/virtualenvs/zhimeng-agent-ORFMGT-6-py3.12/bin/python
```

---

## 开发指南

### 添加新任务

1. 创建任务目录：
```bash
mkdir -p tasks/new_task
touch tasks/new_task/__init__.py
touch tasks/new_task/main.py
```

2. 实现主逻辑（参考现有任务结构）：
```python
# tasks/new_task/main.py
from tasks.config import config
from tasks.sync_utils import create_syncer

class NewTaskRunner:
    def run(self):
        # 执行任务逻辑
        content = self.generate_content()

        # 同步到平台
        syncer = create_syncer()
        syncer.sync_content(
            title="report-title",
            content=content,
            targets=["obsidian", "feishu"],
        )

def main():
    runner = NewTaskRunner()
    runner.run()

if __name__ == "__main__":
    main()
```

3. 创建 launchd plist 文件并安装

### 测试同步
```python
from tasks.sync_utils import create_syncer

syncer = create_syncer()
syncer.sync_content(
    title="test-sync",
    content="# Test\nThis is a test.",
    targets=["obsidian"],
    obsidian_folder="Test",
)
```

---

## 版本历史

- **v1.0.0** (2026-01-07): 初始版本
  - 4个定时任务：日报、邮箱、桌面、新闻
  - 多平台同步支持
  - macOS launchd 调度
