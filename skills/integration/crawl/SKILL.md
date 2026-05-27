---
name: crawl
description: 根据用户需求，使用已经登录的浏览器，基于chrome-devtools 工具的方式来从浏览器中获取用户需要的内容，支持文章内容提取和批量处理。仅用来获取那些需要登录后才能完整访问的网站。
allowed-tools: Read, Grep, Glob, Write, Search, mcp__chrome-devtools__navigate_page, mcp__chrome-devtools__evaluate_script, mcp__chrome-devtools__take_snapshot, mcp__chrome-devtools__list_pages, mcp__chrome-devtools__new_page, mcp__chrome-devtools__click, mcp__chrome-devtools__fill, mcp__chrome-devtools__wait_for, Bash, Task
---

# crawl

## Reference
请先参考学习[how-to-crawl-with-chrome-dev-mcp.md](how-to-crawl-with-chrome-dev-mcp.md)

## Instructions
这个程序仅用来处理那些需要登陆后才能完整登录的网站，在处理过程中不要尝试生成采用其他框架或者程序来获取内容，这样获取的内容是不完整的。

1. 使用python脚本程序，先判断当前是在macos还是windows环境
2. 根据当前的操作系统环境，开启新浏览器实例
3. 检查mcp工具chrome-devtools是否就绪，如果还未就绪请重新连接mcp工具
4. 你只能使用chrome-devtols来获取浏览器中的信息，请调用mcp工具完成用户给出的任务
5. **重要**: 所有输出文件和程序都必须保存在项目根目录下的 `output` 文件夹中

### MCP 配置要求
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--browser-url=http://127.0.0.1:9222"
      ],
      "env": {}
    }
  }
}
```

## 🚀 核心功能

### 1. 智能浏览器管理
- **自动环境检测**: 智能识别 Windows/macOS/Linux 环境
- **自动浏览器启动**: 根据系统自动启动Chrome实例
- **MCP连接检查**: 自动验证Chrome DevTools MCP连接状态
- **代理配置支持**: 支持自动代理配置

### 2. 统一API集成
- **API服务管理**: 自动启动和管理API服务
- **数据格式验证**: 确保数据符合API要求
- **批量数据写入**: 支持批量数据高效写入
- **错误重试机制**: 自动重试失败的数据写入

### 3. 文章内容提取
使用集成的文章内容提取器，支持以下网站：
- **X/Twitter** (x.com) - 推文内容提取
- **The Atlantic** (theatlantic.com)
- **Medium** (medium.com)

## 📁 输出目录结构
```
output/
├── logs/              # 执行日志
├── data/              # 数据文件
├── snapshots/         # 页面快照
└── reports/           # 执行报告
```

## 📚 相关文档

| 文档 | 描述 | 用途 |
|------|------|------|
| [QUICK_START.md](QUICK_START.md) | 快速启动指南 | 新手入门 |
| [EXAMPLES.md](EXAMPLES.md) | 详细使用示例 | 参考代码 |
| [BEST_PRACTICES.md](BEST_PRACTICES.md) | 最佳实践指南 | 进阶优化 |
| [crawl_manager.py](crawl_manager.py) | 核心管理器 | 直接使用 |

## 🎯 快速开始

### 方法一：使用核心管理器（推荐）
```python
from .crawl_manager import extract_x_tweets

# 提取Elon Musk的最新5篇推文
result = extract_x_tweets("elonmusk", 5)
print(result)
```

### 方法二：使用标准模板
```python
# 参考 EXAMPLES.md 中的完整示例
```

## ⚡ 性能特点

- ✅ **一键式启动** - 自动环境配置
- ✅ **智能重试** - 自动错误恢复
- ✅ **数据验证** - 确保数据质量
- ✅ **日志追踪** - 完整执行记录
- ✅ **批量处理** - 高效数据处理

## 🚨 重要提醒

1. **Output目录**: 所有输出文件必须保存在 `output/` 目录下
2. **URL要求**: 数据必须有有效的URL字段
3. **依赖检查**: 使用前确保Chrome和相关依赖已安装
4. **网络环境**: 根据需要配置代理设置

## 📖 详细文档

- **完整示例**: 查看 [EXAMPLES.md](EXAMPLES.md)
- **最佳实践**: 查看 [BEST_PRACTICES.md]
- **快速上手**: 查看 [QUICK_START.md](QUICK_START.md)
- **核心代码**: 查看 [crawl_manager.py](crawl_manager.py)