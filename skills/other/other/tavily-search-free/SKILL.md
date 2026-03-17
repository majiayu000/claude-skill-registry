---
name: tavily-search-free
description: Use Tavily Search API for optimized, real-time web search results for RAG. A pre-configured, cost-effective search tool.
---

# Tavily Search Skill

This skill utilizes the Tavily Search API, providing clean, real-time web search results optimized for LLMs and RAG pipelines.

## 执行环境

| 路径类型 | 路径 | 基准目录 |
|---------|------|---------|
| **技能目录** | `~/.pi/agent/skills/tavily-search-free/` | 固定位置 |
| **主脚本** | `~/.pi/agent/skills/tavily-search-free/scripts/tavily_search.py` | 技能目录 |
| **使用方式** | `pi` 自动调用或手动执行 | 无需手动执行 |

## 安装

```bash
cd ~/.pi/agent/skills/tavily-search-free
pip install tavily-python python-dotenv
```

## API Key 配置

需要 `TAVILY_API_KEY`。密钥已在 `.env` 中预配置。

## 使用方式

### 方式 1：通过 pi 自动调用（推荐）

`pi` 会自动调用此技能进行网络搜索，无需手动执行命令。

### 方式 2：手动执行

```bash
# 从技能目录执行
cd ~/.pi/agent/skills/tavily-search-free
python3 scripts/tavily_search.py --query "<query>" [--max-results <N>] [--search-depth <basic|advanced>]

# 或使用完整路径
cd /path/to/your/project
python3 ~/.pi/agent/skily-search-free/scripts/tavily_search.py --query "<query>"
```

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|-----|------|--------|------|
| `--query` | 是 | - | 搜索查询内容 |
| `--search-depth` | 否 | basic | 搜索深度：`basic` 或 `advanced`（更高质量但更慢） |
| `--max-results` | 否 | 10 | 最大返回结果数量 |

## 示例

```bash
# 基本搜索
python3 ~/.pi/agent/skilly-search-free/scripts/tavily_search.py --query "latest AI trends"

# 深度搜索（高级）
python3 ~/.pi/agent/skilly-search-free/scripts/tavily_search.py --query "autonomous research agents comparison" --search-depth advanced
```

## 输出格式

脚本输出 JSON 格式，包含 `results` 数组，每个结果包含：
- `url`: 结果链接
- `title`: 标题
- `content`: 内容摘要

## 路径说明

- **脚本位置**：`~/.pi/agent/skills/tavily-search-free/scripts/tavily_search.py`
- **配置位置**：`~/.pi/agent/skills/tavily-search-free/.env`
- **依赖安装**：需在技能目录中执行 `pip install`
- **项目上下文**：搜索结果基于查询内容，与本地项目无关
