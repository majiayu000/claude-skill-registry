---
name: langsmith-fetch
description: 通过从 LangSmith Studio 获取执行追踪来调试 LangChain 和 LangGraph 代理。用于调试代理行为、调查错误、分析工具调用、检查内存操作或检查代理性能时。自动获取最近的追踪并分析执行模式。需要安装 langsmith-fetch CLI。
---

# LangSmith 获取 - 代理调试技能

直接在终端中从 LangSmith Studio 获取执行追踪来调试 LangChain 和 LangGraph 代理。

## 何时使用此技能

当用户提到以下内容时自动激活：
- 🐛 "调试我的代理" 或 "哪里出问题了？"
- 🔍 "显示最近的追踪" 或 "发生了什么？"
- ❌ "检查错误" 或 "为什么失败了？"
- 💾 "分析内存操作" 或 "检查长期记忆"
- 📊 "审查代理性能" 或 "检查令牌使用情况"
- 🔧 "调用了哪些工具？" 或 "显示执行流程"

## 前提条件

### 1. 安装 langsmith-fetch
```bash
pip install langsmith-fetch
```

### 2. 设置环境变量
```bash
export LANGSMITH_API_KEY="your_langsmith_api_key"
export LANGSMITH_PROJECT="your_project_name"
```

## 使用流程

### 第 1 步：获取最近的追踪
首先运行以下命令获取最近的追踪记录：
```bash
langsmith-fetch recent
```

### 第 2 步：分析执行模式
分析获取的追踪数据，识别执行模式、错误和性能问题。

## 预期输出

详细的代理执行追踪信息，包括：
- 工具调用序列
- 错误和异常
- 内存操作
- 性能指标
- 执行时间线
