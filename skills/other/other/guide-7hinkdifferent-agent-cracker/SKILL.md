---
name: guide
description: 学习引导：根据用户的学习意图，在 docs/demos/projects 中定位最相关的内容，生成结构化的学习路径
---

# Guide

根据用户的学习意图，在 docs/demos/projects 中定位最相关的内容，生成结构化的学习路径，包含到原始源码的对应。

## Trigger

`/guide <query>`

- `<query>` 可以是机制名称、问题、或学习目标

## 使用场景

| 场景 | 示例 query | 输出重点 |
|------|-----------|---------|
| 学习特定机制 | `/guide repomap` | 定位 docs 中该机制的分析、demo 复现、原始源码路径 |
| 跨 agent 对比 | `/guide how do agents handle context window` | 从多个 docs 的同一维度提取对比，列出各 agent 的策略 |
| 设计自己的 agent | `/guide I want to build a CLI agent with tool calling` | 推荐参考哪些 agent 的哪些维度、MVP 组件列表、demo 学习顺序 |
| 理解整体 | `/guide overview` | 项目结构导览、推荐阅读顺序 |

## Workflow

### Step 1: 意图分类

根据 `<query>` 判断用户意图类别：

- **学习特定机制** — query 是某个具体机制名（如 repomap、search-replace、event-stream）
  → 定位到具体 agent + dimension/demo
- **跨 agent 对比** — query 涉及某个通用概念/维度（如 context management、tool system、error handling）
  → 汇总多个 docs 的同一维度
- **设计参考** — query 描述想构建的东西（如 "build a CLI agent"、"design a tool system"）
  → 基于需求匹配 agent 特征 + MVP 组件
- **整体概览** — query 是 "overview"、"入门"、"怎么用" 等
  → 输出项目导航地图

### Step 2: 检索相关内容

1. 读 `agents.yaml` 获取 agent 列表和状态（只关注 `in-progress` 或 `done` 的 agent）
2. 根据意图类别读取对应资源：
   - 读 `docs/<agent>.md` 的相关维度（D1-D8, D7.5）
   - 读 `demos/<agent>/README.md` 查看已有 demo 列表
   - 如果涉及原始源码，从 docs 中提取 "核心文件" 列
3. 跨 agent 搜索时，对每个已分析的 agent 都检查相关维度

### Step 3: 生成学习路径

根据意图类别生成不同结构的输出：

#### A. 学习特定机制

```markdown
## 学习路径: <mechanism>

### 推荐阅读
| 资源 | 路径 | 说明 |
|------|------|------|
| <agent> D<N> 分析 | docs/<agent>.md → "<section>" | <brief> |
| <mechanism> demo | demos/<agent>/<mechanism>/ | 最简复现 |

### 原始源码对照
| 机制 | Agent | 原始文件 | Demo 文件 | 说明 |
|------|-------|----------|-----------|------|
| <mechanism> | <agent> | <original-path> | demos/<agent>/<mechanism>/main.py | <brief> |

### 推荐学习顺序
1. 先看 docs/<agent>.md D<N> 理解设计
2. 跑 demos/<agent>/<mechanism>/ 体验实现
3. 对比原始源码 projects/<agent>/<path>

### 延伸资源
- 相关 demo: ...
- 相关维度: ...
```

#### B. 跨 agent 对比

```markdown
## 跨 Agent 对比: <topic>

### 各 Agent 策略
| 维度 | <agent1> | <agent2> | <agent3> |
|------|----------|----------|----------|
| ... | ... | ... | ... |

### 详细分析
（从各 docs 的对应维度提取关键段落）

### 相关 Demo
| Agent | Demo | 路径 |
|-------|------|------|
| ... | ... | ... |

### 推荐学习顺序
1. ...
```

#### C. 设计参考

```markdown
## 设计参考: <goal>

### 推荐参考 Agent
| Agent | 匹配原因 | 重点维度 |
|-------|----------|----------|
| ... | ... | ... |

### MVP 组件清单
（从推荐 agent 的 D7.5 提取，合并为通用清单）

| 组件 | 参考实现 | Demo |
|------|----------|------|
| ... | ... | ... |

### 推荐学习顺序
1. 先看 <agent> D1-D2 理解主循环
2. 按 MVP 组件顺序逐个跑 demo
3. 参考 mini-<agent> 串联
```

#### D. 整体概览

```markdown
## Agent Cracker 导览

### 项目定位
系统性研究开源 Coding Agent 的实现原理，提取关键机制并用最简代码复现。

### 已分析 Agent
（从 agents.yaml 列出 in-progress/done 的 agent 及其特点）

### 资源地图
| 资源类型 | 路径 | 说明 |
|----------|------|------|
| 分析文档 | docs/<agent>.md | 8 维度深度分析 |
| 机制 demo | demos/<agent>/<mechanism>/ | 独立可运行的最简复现 |
| 原始源码 | projects/<agent>/ | git submodule |

### 推荐阅读顺序
1. 挑一个你熟悉的 agent，读 docs 的 D1（概览）和 D2（主循环）
2. 跑对应的 demo，对照 README 中的原始源码路径
3. 读第二个 agent 的 docs，体会不同设计选择
4. 按 D7.5 MVP 组件清单，逐个跑 demo
5. 参考 mini-<agent> 串联 demo，尝试组装自己的 mini agent

### 维度速查
| 维度 | 内容 | 关键问题 |
|------|------|----------|
| D1 | Overview & Architecture | 这个 agent 是什么？ |
| D2 | Agent Loop | 主循环怎么跑的？ |
| D3 | Tool/Action 系统 | Tool 怎么注册和调用？ |
| D4 | Prompt 工程 | Prompt 怎么组装的？ |
| D5 | 上下文管理 | Context window 怎么控制？ |
| D6 | 错误处理与恢复 | 出错了怎么办？ |
| D7 | 关键创新点 | 有什么独特设计？ |
| D7.5 | MVP 组件 | 最小可运行版本需要什么？ |
| D8 | 跨 Agent 对比 | 不同 agent 怎么对比？ |
```

## Output Requirements

1. 输出必须包含具体的文件路径，让用户可以直接跳转
2. 只推荐已分析（in-progress/done）的 agent 内容，pending 的 agent 不推荐
3. 如果 query 涉及的机制没有对应 demo，明确说明并建议用 `/create-demo` 创建
4. 中文输出，代码/路径/标识符用英文
5. 学习路径应有明确的先后顺序，不是简单罗列
