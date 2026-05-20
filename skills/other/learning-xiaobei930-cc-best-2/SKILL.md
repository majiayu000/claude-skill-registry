---
name: learning
description: "Extracts reusable patterns from sessions. Use at session end to capture debugging insights and project-specific knowledge."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
parent: session
---

# 持续学习技能

本技能用于从开发会话中提取可复用的模式和知识，实现持续学习和改进。

## 子文件

- [extraction-guide.md](extraction-guide.md) - 会话学习方法论（知识分类、置信度系统）

## 触发条件

- 会话结束时评估
- 发现新的调试技巧
- 解决了复杂问题
- 创建了可复用的解决方案
- 学到了项目特定知识

## 学习模式类型

### 1. 错误解决模式

当解决了一个错误，记录：

- 错误信息
- 根本原因
- 解决方案
- 预防措施

````markdown
## 错误: Cannot read property 'xxx' of undefined

### 场景

访问嵌套对象属性时

### 根本原因

异步数据未加载完成就访问

### 解决方案

```typescript
// 使用可选链
const value = obj?.nested?.property;

// 或提供默认值
const value = obj?.nested?.property ?? defaultValue;
```
````

### 预防

- 始终使用可选链访问可能为空的属性
- 在组件中添加加载状态检查

````

### 2. 调试技巧

```markdown
## 技巧: 调试 Next.js API 路由

### 场景
API 路由返回意外结果

### 技巧
1. 在 route.ts 开头添加日志
```typescript
export async function GET(request: NextRequest) {
  console.log('[API] GET /api/xxx', {
    url: request.url,
    headers: Object.fromEntries(request.headers)
  })
  // ...
}
````

2. 使用 Postman/curl 直接测试
3. 检查中间件是否拦截

````

### 3. 变通方案

```markdown
## 变通: Prisma 不支持的复杂查询

### 场景
需要执行 Prisma 不原生支持的 SQL

### 变通方案
```typescript
// 使用 $queryRaw 执行原生 SQL
const result = await prisma.$queryRaw`
  SELECT * FROM users
  WHERE LOWER(name) LIKE ${`%${search.toLowerCase()}%`}
`

// 或使用 $executeRaw 执行命令
await prisma.$executeRaw`
  UPDATE users SET updated_at = NOW()
  WHERE id = ${userId}
`
````

### 注意

- 需要手动处理 SQL 注入防护
- 返回类型需要手动指定

````

### 4. 项目特定知识

```markdown
## 项目: 用户认证流程

### 流程
1. 用户提交凭证 → POST /api/auth/login
2. 验证凭证 → 检查数据库
3. 生成 JWT → 设置 httpOnly cookie
4. 返回用户信息

### 关键文件
- `src/app/api/auth/login/route.ts` - 登录接口
- `src/lib/auth.ts` - 认证工具函数
- `src/middleware.ts` - 路由保护

### 注意事项
- Token 有效期 7 天
- 刷新 Token 在 /api/auth/refresh
- 受保护路由在 middleware.ts 配置
````

## 评估清单

会话结束时，检查以下内容：

### 值得记录的模式

```markdown
- [ ] 解决了一个复杂的 Bug？
- [ ] 发现了一个调试技巧？
- [ ] 创建了一个可复用的代码片段？
- [ ] 学到了框架/库的新用法？
- [ ] 遇到并解决了性能问题？
- [ ] 找到了一个变通方案？
- [ ] 了解了项目特定的知识？
```

### 不值得记录的模式

```markdown
- [ ] 简单的拼写错误
- [ ] 一次性的配置问题
- [ ] 外部 API 临时故障
- [ ] 已知的简单问题
```

## 知识库结构

```
.claude/
└── learned/
    ├── errors/
    │   ├── prisma-connection-issues.md
    │   └── react-hydration-mismatch.md
    ├── debugging/
    │   ├── next-api-routes.md
    │   └── database-query-slow.md
    ├── workarounds/
    │   ├── prisma-raw-queries.md
    │   └── nextauth-custom-session.md
    ├── patterns/
    │   ├── error-handling.md
    │   └── api-response-format.md
    └── project/
        ├── auth-flow.md
        └── data-models.md
```

## 知识文档模板

```markdown
---
title: [标题]
category: [errors|debugging|workarounds|patterns|project]
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# [标题]

## 场景

[描述遇到这个问题/使用这个模式的场景]

## 问题/需求

[具体的问题描述或需求说明]

## 解决方案

[详细的解决方案，包括代码示例]

## 相关文件

- `path/to/file.ts` - [说明]

## 参考

- [链接1](url)
- [链接2](url)

## 注意事项

[使用时需要注意的点]
```

## 自动化集成

### 会话评估 Hook

会话评估已通过 Node.js Hook 自动化，无需手动触发：

- **脚本**: `scripts/node/hooks/evaluate-session.js`（运行 `--help` 查看详情）
- **触发时机**: Stop 事件（会话结束时）
- **功能**: 自动评估会话长度，提示提取可复用模式

### 配置文件

```json
{
  "min_session_length": 10,
  "extraction_threshold": "medium",
  "auto_approve": false,
  "learned_skills_path": "~/.claude/learned/",
  "patterns_to_detect": [
    "error_resolution",
    "debugging_techniques",
    "workarounds",
    "project_specific"
  ],
  "ignore_patterns": ["simple_typos", "one_time_fixes", "external_api_issues"]
}
```

## 本能系统（进阶）

本能是介于"观察"和"正式技能"之间的中间状态，用于捕捉重复出现的模式。

### 本能的生命周期

```
观察 ──→ 记录 ──→ 本能 ──→ 演化
 │        │        │        │
 │        │        │        └─→ 技能/命令/智能体
 │        │        └─→ 置信度评估
 │        └─→ observations.jsonl
 └─→ Hook 自动捕获
```

### 置信度评分

| 置信度 | 含义     | 动作                |
| ------ | -------- | ------------------- |
| 0.3    | 首次观察 | 记录但不采取行动    |
| 0.5    | 重复出现 | 形成初步本能        |
| 0.7    | 多次验证 | 考虑演化为技能      |
| 0.9    | 高度可靠 | 正式演化为技能/命令 |

### 本能记录格式

```markdown
## 本能: [名称]

### 触发模式

[什么情况下触发]

### 推荐行为

[应该如何响应]

### 置信度: 0.X

[基于多少次观察]

### 观察记录

- 2025-01-20: [场景1]
- 2025-01-22: [场景2]

### 演化候选

- [ ] 升级为技能
- [ ] 升级为命令
- [ ] 写入 CLAUDE.md
```

### 自动观察 Hook

通过 PostToolUse hook 自动捕获工具调用模式，无需手动触发。

- **脚本**: `scripts/node/hooks/observe-patterns.js`（运行 `--help` 查看详情）
- **输出**: `memory-bank/observations.jsonl`（JSONL 格式，自动轮转）
- **触发**: Write、Edit、Bash 操作后自动运行
- **检测模式**: error_fix、repeated_search、multi_file_edit、test_after_edit
- **与 /learn 配合**: `/learn` 命令在 Step 0 自动读取观察数据作为分析输入

---

## 最佳实践

1. **及时记录** - 解决问题后立即记录，不要等
2. **结构化** - 使用统一的模板格式
3. **具体示例** - 包含代码示例和文件路径
4. **定期回顾** - 定期整理和更新知识库
5. **团队共享** - 有价值的知识分享给团队
6. **版本控制** - 将知识库纳入版本控制
7. **标签分类** - 使用标签便于搜索
8. **保持简洁** - 只记录有价值的内容
9. **更新过时** - 及时更新过时的信息
10. **关联项目** - 记录项目特定的上下文
11. **本能演化** - 重复模式升级为正式技能

---

> **记住**: 每次调试都是学习机会。记录下来，下次就能更快解决类似问题。本能系统让学习更系统化，从观察到技能的演化让知识沉淀更有效。
