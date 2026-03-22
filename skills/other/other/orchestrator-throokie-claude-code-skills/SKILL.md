---
name: orchestrator
description: 多代理协作编排器，基于 Anthropic 工程团队架构，支持 Lead-Worker 模式、API Key 轮换、并行执行。触发词：创建团队、多代理协作、长任务、复杂任务、并行搜索。
version: 2.0
---

# Orchestrator Pro - 多代理协作增强版

> 版本：v2.0 - 2026-03-17
> 基于 Anthropic 工程团队的多代理研究系统架构

---

## 📋 概述

Orchestrator Pro 是 Anthropic 工程师团队使用的工作模式的实现：
- **1 个 Lead Agent** (Opus 4) - 负责决策和协调
- **3-5 个 Worker Agents** (Sonnet 4) - 并行执行子任务
- **多 API Key 轮换** - 避免单个 Key 频率限制

---

## 🚀 快速开始

### 基础用法

```bash
# 启动 Orchestrator Pro 模式
node ~/src/user-scripts/skills/agents/orchestrator/scripts/route-intent.mjs "研究 Rust 异步编程"

# 并行模式（实验性）
node ~/src/user-scripts/skills/agents/orchestrator/scripts/route-intent.mjs "研究 Rust 异步编程" --parallel

# 只生成计划，不执行
node ~/src/user-scripts/skills/agents/orchestrator/scripts/route-intent.mjs "开发登录系统" --plan-only
```

### Claude Code 自动触发

当用户输入包含以下触发词时，自动调用 Orchestrator：

| 用户输入 | 自动调用 |
|----------|----------|
| "创建团队研究 X" | orchestrator |
| "多代理协作开发" | orchestrator |
| "长任务" | orchestrator |
| "复杂任务" | orchestrator |
| "并行搜索" | orchestrator (parallel 模式) |

---

## 🏗️ 架构设计

### Orchestrator-Workers 模式

```
                ┌─ Worker 1 (Sonnet) ─ 研究者 ─┐
                ├─ Worker 2 (Sonnet) ─ 开发者 ─┤
用户 → Opus (Lead) ─┼─ Worker 3 (Sonnet) ─ 审查者 ─┼→ 综合结果
                ├─ Worker 4 (Sonnet) ─ 文档员 ─┤
                └─ Worker 5 (Sonnet) ─ 测试者 ─┘
```

### 多 API Key 轮换

```
API Key 池:
├─ key-1 (active)    → Lead Agent + Worker 1
├─ key-2 (backup)    → Worker 2 + Worker 3
└─ key-3 (backup)    → Worker 4 + Worker 5

轮询策略：round-robin
切换条件：
  - 当前 Key 达到速率限制
  - 并发请求数超过阈值
```

---

## 📁 目录结构

```
orchestrator/
├── SKILL.md              # 主入口文档（本文件）
├── scripts/
│   ├── spawn-agent.mjs   # 生成子代理
│   ├── collect-results.mjs # 收集结果
│   ├── route-intent.mjs  # 意图路由
│   └── api-rotator.mjs   # API Key 轮换器（新增）
├── prompts/
│   ├── researcher.md     # Research Agent 提示词
│   ├── builder.md        # Builder Agent 提示词
│   ├── reviewer.md       # Reviewer Agent 提示词
│   └── archiver.md       # Archiver Agent 提示词
└── config/
    ├── api-keys.json     # API Key 配置（~/.claude/api-keys.json）
    └── agent-roles.json  # 代理角色配置
```

---

## 🔧 核心功能

### 1. API Key 轮换器

**用法**：
```javascript
import { getAvailableKey } from '~/src/user-scripts/skills/agents/orchestrator/scripts/api-rotator.mjs';

const key = getAvailableKey('anthropic', 'worker-2');
// 返回可用的 API Key，自动跳过达到限流的 Key
```

**轮换策略**：
| 策略 | 说明 |
|------|------|
| round-robin | 按顺序轮询，每次使用下一个 Key |
| least-used | 使用今日用量最少的 Key |
| priority | 按优先级顺序，主 Key 故障时切备用 |

### 2. 并行执行引擎

**用法**：
```bash
# 串行执行（默认）
node route-intent.mjs "任务"

# 并行执行（需要多个 API Key）
node route-intent.mjs "任务" --parallel
```

**并行限制**：
- 单个 API Key：最多 2 个并发请求
- 2 个 API Keys：最多 4 个并发请求
- 3+ API Keys：最多 6 个并发请求

### 3. 子代理类型

| 代理类型 | 用途 | 推荐模型 | 触发词 |
|----------|------|----------|--------|
| `researcher` | 研究搜索 | Sonnet 4 | "搜索"、"研究"、"对比" |
| `builder` | 开发建设 | Sonnet 4 | "开发"、"实现"、"构建" |
| `reviewer` | 代码审查 | Opus 4 | "review"、"审查"、"优化" |
| `archiver` | 文档归档 | Sonnet 4 | "总结"、"归档"、"记录" |
| `tester` | 测试验证 | Sonnet 4 | "测试"、"验证" |
| `general` | 通用任务 | Sonnet 4 | 其他 |

---

## 📊 使用示例

### 示例 1：多代理研究（并行模式）

```bash
# 用户输入
"创建团队研究 Rust 异步编程的最佳实践"

# Orchestrator 执行
1. Lead Agent (Opus) 分析任务，分解为 3 个子任务：
   - 子任务 1: 搜索 Rust 异步基础教程
   - 子任务 2: 对比 tokio 和 async-std 生态
   - 子任务 3: 整理 GitHub 实战案例

2. 启动 3 个 Worker Agents 并行执行：
   - Worker 1 (Sonnet, key-1) → 搜索基础教程
   - Worker 2 (Sonnet, key-2) → 对比生态
   - Worker 3 (Sonnet, key-3) → 整理案例

3. 等待所有 Worker 完成

4. Lead Agent 综合所有结果，输出综合报告
```

**预期输出**：
```markdown
## 研究报告：Rust 异步编程最佳实践

### 核心发现
（Lead Agent 综合 3 个 Worker 的结果）

### 基础教程（Worker 1）
- The Rust Programming Language - Chapter 16
- Tokio documentation
- ...

### 生态对比（Worker 2）
| 特性 | Tokio | async-std |
|------|-------|-----------|
| 性能 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 生态 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| ...

### 实战案例（Worker 3）
1. [项目 A](github.com/xxx) - 高并发服务器
2. [项目 B](github.com/yyy) - Web 框架
...

### 来源统计
- 技术文档：5 个
- GitHub 项目：8 个
- 论坛讨论：3 个
```

### 示例 2：协作开发（串行模式）

```bash
# 用户输入
"开发一个用户登录系统"

# Orchestrator 执行（单 API Key 模式）
1. Lead Agent 分解任务：
   - 子任务 1: 前端登录页面 UI
   - 子任务 2: 后端认证 API
   - 子任务 3: 单元测试
   - 子任务 4: 代码审查

2. 串行执行（避免触发限流）：
   - Worker 1 → 前端页面
   - Worker 2 → 后端 API
   - Worker 3 → 测试代码
   - Worker 4 → 代码审查

3. 每个子任务完成后，更新进度文件

4. 所有任务完成后，输出综合报告
```

---

## ⚙️ 配置说明

### API Key 配置

编辑 `~/.claude/api-keys.json`：

```json
{
  "providers": {
    "anthropic": {
      "keys": [
        {
          "id": "key-1",
          "api_key": "sk-ant-api03-你的实际 Key",
          "_status": "active"
        },
        {
          "id": "key-2",
          "api_key": "sk-ant-api03-placeholder",
          "_status": "placeholder"
        }
      ]
    }
  }
}
```

### 环境变量方式

也可以使用环境变量：

```bash
# ~/.bashrc 或 ~/.config/fish/config.fish
export ANTHROPIC_API_KEY_1="sk-ant-api03-xxx"
export ANTHROPIC_API_KEY_2="sk-ant-api03-yyy"
export ANTHROPIC_API_KEY_3="sk-ant-api03-zzz"
```

---

## 📈 性能优化

### 单 Key 模式优化

当只有一个 API Key 时：

```javascript
// route-intent.mjs 中添加请求间隔
const SINGLE_KEY_DELAY = 2000; // 2 秒间隔

if (activeKeys === 1) {
  await sleep(SINGLE_KEY_DELAY);
}
```

### 多 Key 模式优化

当有多个 API Key 时：

```javascript
// 并行执行，最大化吞吐量
const concurrentLimit = Math.min(agentCount, activeKeys * 2);
await Promise.all(agents.map(a => execute(a)));
```

---

## ⚠️ 注意事项

### 1. API Key 安全

```bash
# 设置文件权限
chmod 600 ~/.claude/api-keys.json

# 不要提交到 git
echo "api-keys.json" >> ~/.claude/.gitignore
```

### 2. 速率限制

| 模型 | Requests/min | Tokens/min |
|------|--------------|------------|
| Opus 4 | 160 | 80,000 |
| Sonnet 4 | 240 | 120,000 |
| Haiku 4 | 320 | 160,000 |

### 3. 错误处理

当 API Key 达到限流时：

```
1. 自动切换到下一个可用 Key
2. 记录当前 Key 的冷却时间（默认 60 秒）
3. 如果所有 Key 都限流，等待后重试
```

---

## 🔗 参考资源

- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Anthropic: Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

---

*最后更新：2026-03-17 | 版本：v2.0*
