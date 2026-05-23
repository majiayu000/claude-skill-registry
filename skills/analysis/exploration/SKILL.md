---
name: exploration
description: "Code exploration strategies for understanding unfamiliar codebases. Use when exploring unknown code, debugging, or analyzing architecture."
allowed-tools: Read, Grep, Glob, Task
context: fork
agent: Explore
---

# 代码库探索

本技能提供代码库探索的通用方法论，包含两种策略模式。

## 子文件

- [isolated-research.md](isolated-research.md) - 隔离研究（快速一次性探索）
- [iterative-retrieval.md](iterative-retrieval.md) - 渐进式检索（多轮迭代探索）

## 策略选择

| 场景                 | 推荐策略            | 原因                     |
| -------------------- | ------------------- | ------------------------ |
| 快速了解某个模块     | isolated-research   | 一次性探索，不污染上下文 |
| 理解复杂的跨模块流程 | iterative-retrieval | 需要多轮精炼             |
| 简单的文件/函数定位  | 直接 Grep/Glob      | 无需完整探索流程         |
| 新项目初始理解       | iterative-retrieval | 需要建立全局认知         |
| 调试特定 Bug         | isolated-research   | 聚焦单一问题             |
| 架构分析和文档化     | iterative-retrieval | 需要完整依赖图           |

---

## 通用探索方法

### 搜索工具选择

| 目标               | 工具 | 示例                      |
| ------------------ | ---- | ------------------------- |
| 按文件名/路径查找  | Glob | `**/auth/**/*.ts`         |
| 按代码内容查找     | Grep | `"function authenticate"` |
| 读取完整文件       | Read | 直接读取已知路径文件      |
| 深度子任务（隔离） | Task | 派发子代理执行            |

### 搜索策略模式

```markdown
## 入口点搜索

- 路由/API 端点
- 中间件
- main/index 文件
- 配置文件

## 定义搜索

- class/function 定义
- type/interface 定义
- 常量/枚举定义

## 使用搜索

- import/require 语句
- 函数调用点
- 类实例化

## 依赖搜索

- package.json
- import 图谱
- 模块边界
```

---

## 输出格式（通用）

所有探索结果应遵循统一格式：

```markdown
## 探索报告

### 问题/目标

[描述探索的目标]

### 关键发现

| 文件                | 行号 | 功能说明       |
| ------------------- | ---- | -------------- |
| `src/auth/login.ts` | 42   | 登录验证入口   |
| `src/lib/jwt.ts`    | 15   | Token 生成逻辑 |

### 依赖关系

[可选：模块依赖图、调用链]

### 结论

[对问题的回答]

### 后续建议

[可选：建议的下一步动作]
```

---

## 子策略

### 1. isolated-research（隔离研究）

**特点**：

- 在子代理中执行，不污染主上下文
- 一次性任务，快速返回
- 适合聚焦的单一问题

详细指南参阅 `isolated-research.md`

### 2. iterative-retrieval（迭代检索）

**特点**：

- 多轮迭代，逐步精炼
- 置信度评估驱动
- 适合复杂跨模块问题

详细指南参阅 `iterative-retrieval.md`

---

## 与角色系统配合

| 角色     | 探索场景           | 推荐策略            |
| -------- | ------------------ | ------------------- |
| `/pm`    | 理解现有功能       | isolated-research   |
| `/lead`  | 架构分析、技术设计 | iterative-retrieval |
| `/dev`   | 实现前了解相关代码 | isolated-research   |
| `/qa`    | 理解测试范围       | isolated-research   |
| `/debug` | 追踪 Bug 根因      | iterative-retrieval |

---

## 最佳实践

1. **先评估再选择** - 根据问题复杂度选择策略
2. **记录路径** - 始终包含文件路径和行号
3. **限制范围** - 明确探索边界，避免发散
4. **输出结构化** - 使用统一格式便于后续使用
5. **复用结果** - 探索结果可保存到 memory-bank

---

**核心理念**：探索是理解的基础，好的探索策略能显著提升开发效率。
