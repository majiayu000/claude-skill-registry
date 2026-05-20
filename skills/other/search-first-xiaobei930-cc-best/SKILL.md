---
name: search-first
description: "Research-before-coding workflow: systematically search existing solutions before custom implementation. Use when introducing new libraries, tools, or solving unfamiliar problems."
allowed-tools: Read, Bash, Grep, Glob, WebSearch, WebFetch
---

# 研究优先工作流

编码前系统化搜索现有方案，做出 Adopt/Extend/Compose/Build 决策。

**核心原则：不重复造轮子，但也不盲目引入依赖。**

## 触发条件 | Trigger Conditions

- `/cc-best:lead` 技术方案设计阶段
- 需要引入新库/工具/框架时
- 遇到"需要 X 功能"的需求时
- 解决不熟悉的技术问题时

## 搜索流程 | Search Process

```
1. 并行搜索（限时 5-10 分钟）
   ├─ 包管理器（npm/PyPI/Maven 等，根据项目技术栈）
   ├─ MCP 服务器（如适用）
   ├─ GitHub/社区方案
   └─ 官方文档/API 参考

2. 方案评估
   ├─ 功能匹配度
   ├─ 维护活跃度（最近提交、issue 响应）
   ├─ 许可证兼容性
   └─ 依赖复杂度

3. 决策 + 记录
   ├─ 输出 Adopt/Extend/Compose/Build 决策
   ├─ 记录到 progress.md 决策表
   └─ 标注置信度
```

## 评估矩阵 | Decision Matrix

| 条件                           | 决策           | 行动                 |
| ------------------------------ | -------------- | -------------------- |
| 精确匹配 + 活跃维护 + 兼容许可 | 采用 (Adopt)   | 直接安装使用         |
| 部分匹配 + 良好基础            | 扩展 (Extend)  | 安装 + 薄包装器适配  |
| 多个弱匹配                     | 组合 (Compose) | 组合 2-3 个小包      |
| 无合适方案                     | 构建 (Build)   | 自研，但带着搜索知识 |

### 评估检查清单

```markdown
- [ ] 功能是否满足核心需求（≥80%）
- [ ] 最近 6 个月内有提交
- [ ] 许可证与项目兼容（MIT/Apache/ISC 优先）
- [ ] 依赖数量合理（<20 direct deps）
- [ ] 有测试覆盖和文档
- [ ] 无已知安全漏洞
```

## 与角色工作流的集成 | Pipeline Integration

在 `/cc-best:lead` 工作流中，技术栈选型前自动触发：

```
PM(需求) → Lead(search-first → 方案设计) → Dev(实现)
```

### 集成方式

1. **Lead 角色**：技术方案设计时，对每个新依赖执行 search-first
2. **Dev 角色**：遇到"需要引入新工具"时，暂停编码执行 search-first
3. **Architect agent**：架构决策中自动引用 search-first 结果

## 搜索策略 | Search Strategy

### 按场景选择搜索深度

| 场景          | 搜索深度 | 时间上限 |
| ------------- | -------- | -------- |
| 已知成熟方案  | 浅搜索   | 2 分钟   |
| 常见功能需求  | 标准搜索 | 5 分钟   |
| 创新/罕见需求 | 深度搜索 | 10 分钟  |

### 搜索来源优先级

1. 项目已有依赖（检查 package.json/go.mod 等）
2. 项目技术栈生态的官方推荐
3. 包管理器搜索（npm search / pip search 等）
4. GitHub trending + awesome-xxx 列表
5. WebSearch 通用搜索

## 决策记录模板 | Decision Template

```markdown
### 搜索决策: [功能描述]

**搜索范围**: [npm/GitHub/WebSearch]
**候选方案**:

1. [方案A] - [优劣概述]
2. [方案B] - [优劣概述]

**决策**: [Adopt/Extend/Compose/Build] [方案名]
**理由**: [1-2 句]
**置信度**: [高/中/低]
```

## 最佳实践 | Best Practices

1. **搜索有时间上限** — 超时用 MVP 方案，标记 TBD
2. **不是每个工具都要搜索** — 区分"已知成熟方案"和"新需求"
3. **检查维护状态** — star 多但 3 年未更新的比新库风险更高
4. **考虑退出成本** — 深度耦合的依赖要慎重选择
5. **记录搜索过程** — 即使决定 Build，也记录为什么不 Adopt

---

> **记住**: 搜索不是目的，做出有依据的决策才是目的。5 分钟的搜索可以避免 5 天的重复造轮子。
