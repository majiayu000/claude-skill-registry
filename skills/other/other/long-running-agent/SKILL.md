---
name: long-running-agent
description: 长周期任务管理框架，基于 Anthropic 官方最佳实践，支持多代理协作、进度追踪、强制闭环。触发词：长任务、复杂项目、多会话、团队协作、子代理。
version: 4.0
---

# Long-Running Agent 长周期任务管理 v4.0

> **重要：** 所有 Agent 必须遵守 `behavior-guidelines.md` 中的行为准则！
> 该文件定义了说话风格、工作流程、安全协议等核心规范。
>
> **基于 Anthropic 官方研究构建：**
> - [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
> - [How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)
> - [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
> - [Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)

---

## 一、核心理念：简单优先，渐进复杂

### 黄金法则

```
❌ 不要一开始就构建复杂的代理系统
✅ 从简单的 Prompt 开始，优化评估后再增加复杂度
✅ 只有在简单方案不够时才添加多步骤代理系统
```

### 成功的三个核心原则

1. **保持简单**：不需要时不要增加复杂度
2. **透明化**：明确展示 Agent 的推理过程
3. **精心设计工具接口**：通过良好的工具文档实现控制

---

## 二、Token 使用量决定性能（核心原理）

### 关键数据

```
在 BrowseComp 评估中，三个因素解释了 95% 的性能方差：
- Token 使用量（80%）← 最重要！
- 工具调用次数
- 模型选择

结论：多代理架构通过分配工作到独立上下文窗口，
有效扩展 Token 使用量，突破单代理限制。
```

### 多代理系统性能数据

| 指标 | 数值 |
|------|------|
| 单代理 → 多代理性能提升 | 90.2% |
| 代理 Token 消耗 | 约 4× 聊天 |
| 多代理 Token 消耗 | 约 15× 聊天 |

### 适用场景判断

```
✅ 适合多代理：
- 任务可并行化
- 信息超过单上下文窗口
- 需要多种工具/视角

❌ 不适合多代理：
- 所有代理需共享相同上下文
- 代理间有大量依赖关系
- 大多数编码任务（并行化任务较少）
```

---

## 三、五大工作流模式详解

### 模式总览

| 模式 | 适用场景 | 复杂度 | 本框架使用 |
|------|----------|--------|-----------|
| Prompt Chaining | 固定步骤任务 | ⭐ | 辅助 |
| Routing | 分类导向处理 | ⭐⭐ | 辅助 |
| Parallelization | 可并行子任务 | ⭐⭐ | 辅助 |
| **Orchestrator-Workers** | 复杂不可预测任务 | ⭐⭐⭐ | **核心** |
| **Evaluator-Optimizer** | 需要迭代改进 | ⭐⭐⭐ | **核心** |

### 1. Prompt Chaining（提示链）

```
任务分解为固定步骤，每步处理上一步输出

适用场景：
- 任务可清晰分解为固定子任务
- 愿意用延迟换取更高准确性

示例：
输入 → LLM调用1 → 检查点 → LLM调用2 → 检查点 → 输出
```

### 2. Routing（路由）

```
分类输入，导向专门的处理流程

适用场景：
- 复杂任务有明确分类
- 不同类别需要不同处理

示例：
输入 → 分类器 → 路由到专门Prompt → 输出
```

### 3. Parallelization（并行化）

```
多个 LLM 同时工作，结果聚合

两种变体：
- 分段：任务分成独立部分并行处理
- 投票：多个 LLM 尝试同一任务，取多数

适用场景：
- 子任务可并行化
- 需要多视角或多次尝试提高置信度
```

### 4. Orchestrator-Workers（编排者-工作者）⭐ 核心

```
中央 LLM 动态分解任务，委托给 Worker LLM，综合结果

适用场景：
- 复杂任务无法预测子任务（如编程，文件数量和改动类型不确定）
- 需要灵活性而非预定义子任务

架构图：
┌─────────────────────────────────────────────────────┐
│                    Lead Agent                        │
│  (分析查询，制定策略，分配任务，综合结果)              │
└─────────────────┬───────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
┌────────┐   ┌────────┐   ┌────────┐
│Subagent│   │Subagent│   │Subagent│
│ (搜索) │   │ (编码) │   │ (测试) │
└────────┘   └────────┘   └────────┘
     │             │             │
     └─────────────┴─────────────┘
                   │
                   ▼
           Lead Agent 综合
                   │
                   ▼
             Reviewer 审查
                   │
                   ▼
               完成 ✓
```

**多代理系统的优势：**

1. **并行压缩**：Subagent 独立探索，只返回最重要的 Token 给 Lead Agent
2. **关注分离**：不同的工具、提示和探索路径
3. **性能提升**：Claude Opus 4 Lead + Sonnet 4 Subagents 比单代理 Opus 4 性能提升 90.2%

**多代理系统的代价：**

```
- 代理使用约 4× Token（相比聊天）
- 多代理系统使用约 15× Token（相比聊天）
- 经济可行性要求任务价值足够高
```

### 5. Evaluator-Optimizer（评估者-优化者）⭐ 核心

```
一个 LLM 生成响应，另一个提供评估和反馈，循环迭代

这是 Claude Code 最推荐的模式！

适用场景：
- 有明确的评估标准
- 迭代改进有可衡量的价值
- LLM 响应可通过人类反馈改进
```

---

## 四、Token 效率原则

### 核心数据

```
Token 使用量解释 80% 的性能方差

关键限制：
- 单次输出限制：25,000 tokens
- 评估最小样本：~20 个测试用例
- 中位数代理运行时间：~45 秒
```

### 效率优化实践

```markdown
## 输出优化

❌ 错误：返回全部数据
```json
{"data": [/* 1000 条记录 */]}
```

✅ 正确：返回摘要 + 分页
```json
{
  "summary": "找到 1000 条记录",
  "page": 1,
  "per_page": 20,
  "items": [/* 20 条记录 */],
  "has_more": true
}
```

## 搜索优化

❌ 错误：单次大搜索
"搜索所有 Hyprland 配置问题"

✅ 正确：多次精准搜索
1. "Hyprland keybind conflict" (小)
2. "Hyprland config syntax error" (小)
3. "Hyprland window rules" (小)

## 工具返回优化

优先返回：
✅ name, image_url, file_type（直接信息）
❌ uuid, 256px_image_url, mime_type（技术标识符）

自然语言标识符比 UUID 更有效：
- UUID: "a1b2c3d4" → 容易幻觉
- 语义 ID: "user_jane" → 精确检索
```

### 效率优化原则

```markdown
1. 分页获取大数据
2. 压缩输出返回摘要
3. 多次小搜索优于单次大搜索
4. 单次输出限制 25,000 tokens
5. 错误提示要明确具体
```

---

## 五、核心问题：Agent 容易"假装完成"

```
❌ 写了几行代码就标记完成
❌ 没有运行测试验证
❌ 没有人 review
❌ 遇到问题就跳过
❌ 会话结束进度丢失
```

---

## 六、六大强制机制

### 1. 任务必须定义"完成标准"

```javascript
TaskCreate 时必须包含：

TaskCreate(
  subject: "实现登录 API",
  description: `
    开发 POST /login 接口

    ## 完成标准（必须全部满足）
    - [ ] API 能响应 POST /login
    - [ ] 正确用户返回 JWT token
    - [ ] 错误密码返回 401
    - [ ] 单元测试通过

    ## 验证命令
    npm test
  `
)
```

### 2. Reviewer 角色必须存在

每个团队必须有 **reviewer**，负责：
- 检查任务是否真正完成
- 运行测试
- 代码审查

```
团队成员:
- project-lead: 协调
- researcher: 调研
- coder: 编码
- reviewer: 审查 ← 必须！
- tester: 测试
```

### 3. 强制闭环流程

```
Agent 完成工作
    ↓
不能直接标记 completed！
    ↓
必须发送消息给 reviewer 审查：
    SendMessage(
      type: "message",
      recipient: "reviewer",
      content: "任务 #X 请求审查..."
    )
    ↓
Reviewer 验证后回复：
    SendMessage(
      type: "message",
      recipient: "coder",
      content: "审查通过 ✅ / 不通过 ❌"
    )
    ↓
只有审查通过时才能 TaskUpdate(status: "completed")
```

### 4. Agent 自查清单（强制执行）

在标记完成前，Agent **必须**自查：

```markdown
## 自查清单

1. 我是否运行了相关测试？
2. 我是否验证了"完成标准"的每一项？
3. 我是否更新了相关文档？
4. 代码是否能正常编译/运行？
5. 是否有遗留的 TODO 或 FIXME？

**如果任何一项是"否"，不能标记完成！**
```

### 5. 进度持久化（强制）

每个会话结束时必须写入：

```json
// .agent/progress.json
{
  "last_session": "2024-03-13T15:00:00",
  "completed": ["task-1", "task-2"],
  "in_progress": "task-3",
  "next_steps": ["完成 API 测试"],
  "notes": "登录逻辑已实现"
}
```

### 6. 会话恢复协议

新会话开始时必须：

```
1. 读取 progress.json
2. 检查 TaskList
3. 找到 in_progress 的任务
4. 发送消息唤醒相关 Agent
5. 如果 Agent 已关闭，重新 spawn
```

---

## 七、角色配置标准

### 角色定义

| 角色 | subagent_type | 职责 | 必须性 |
|------|---------------|------|--------|
| **project-lead** | general-purpose | 协调、综合、决策 | 必须 |
| **researcher** | Explore | 搜索、分析、调研 | 按需 |
| **coder** | general-purpose | 编码、实现 | 按需 |
| **reviewer** | general-purpose | 审查、验证 | **必须！** |
| **tester** | general-purpose | 测试、验证 | 按需 |

### 项目类型配置

**软件开发项目：**

```
团队成员:
- project-lead (team-lead): 协调进度、审阅代码
- researcher: 技术调研、方案设计
- coder-1: 前端开发
- coder-2: 后端开发
- reviewer: 代码审查 ← 必须
- tester: 测试验证
```

**文档/写作项目：**

```
团队成员:
- project-lead: 统筹进度
- researcher: 资料收集、深度调研
- writer-1: 主要撰写
- writer-2: 辅助撰写
- editor: 审阅修订 ← 必须（相当于 reviewer）
```

**研究/分析项目：**

```
团队成员:
- project-lead: 统筹方向
- researcher-1: 主要研究
- researcher-2: 辅助研究
- analyst: 数据分析
- reviewer: 结果验证 ← 必须
```

---

## 八、创建团队的标准流程

### 完整初始化示例

```javascript
// 1. 创建团队
TeamCreate(
  team_name: "auth-system",
  description: "开发用户认证系统"
)

// 2. 创建任务（带完成标准）
TaskCreate(
  subject: "实现登录 API",
  description: `
    开发 POST /login 接口

    ## 完成标准
    - [ ] 返回 JWT token
    - [ ] 密码错误返回 401
    - [ ] 测试覆盖率 > 80%

    ## 验证命令
    npm test
    curl -X POST localhost:3000/login -d '{"user":"test","pass":"wrong"}'
  `,
  activeForm: "开发登录 API"
)

// 3. Spawn 团队成员
Agent(subagent_type: "general-purpose", name: "coder", team_name: "auth-system")
Agent(subagent_type: "general-purpose", name: "reviewer", team_name: "auth-system")
Agent(subagent_type: "general-purpose", name: "tester", team_name: "auth-system")

// 4. 分配任务
TaskUpdate(taskId: "1", owner: "coder")
```

---

## 九、Evaluator-Optimizer 模式实现

### 核心流程图

```
┌─────────┐     ┌──────────┐     ┌─────────┐
│ Worker  │ ──→ │ Reviewer │ ──→ │ approve │ ──→ 完成
└─────────┘     └──────────┘     │ = true? │
     ↑               │           └─────────┘
     └───────────────┘
         approve = false (返回修改)
```

### 强制执行规则

```markdown
**禁止行为**：
- ❌ Worker 直接标记 completed
- ❌ 没有 Reviewer 就标记完成
- ❌ Reviewer 未通过就继续

**必须行为**：
- ✅ Worker 完成后发送 review 请求
- ✅ Reviewer 运行测试验证
- ✅ 只有 approve=true 才能 TaskUpdate(status: "completed")
```

### Reviewer 验证清单

```markdown
## 审查清单

1. **功能验证**
   - [ ] 代码能否正常编译/运行？
   - [ ] 测试是否通过？
   - [ ] 完成标准是否全部满足？

2. **质量检查**
   - [ ] 代码风格是否一致？
   - [ ] 是否有 TODO/FIXME 遗留？
   - [ ] 是否遵循最佳实践？

3. **安全审查**
   - [ ] 是否有安全风险？
   - [ ] 敏感信息是否泄露？
```

---

## 十、Agent 行为规范

### Coder 角色规范

```
当我认为任务完成时：

1. 先运行测试：npm test
2. 检查完成标准的每一项
3. 如果测试失败 → 修复 → 重新测试
4. 如果测试通过 → 发送 review 请求：

SendMessage(
  type: "message",
  recipient: "reviewer",
  content: """
  任务 #1 请求审查

  完成标准检查：
  - [x] 返回 JWT token
  - [x] 密码错误返回 401
  - [x] 测试覆盖率 85%

  验证命令：
  - npm test
  - npm run coverage

  文件变更：
  - src/auth/login.ts
  - tests/auth.test.ts
  """
)

5. 等待 reviewer 回复
6. 如果被拒绝 → 修复 → 重新请求审查
7. 如果通过 → TaskUpdate(status: "completed")
```

### Reviewer 角色规范

```
收到 review 请求后：

1. 读取相关文件
2. 运行测试：npm test
3. 检查代码质量
4. 回复：

如果通过：
SendMessage(
  type: "message",
  recipient: "coder",
  content: "审查通过 ✅\n\n所有测试通过，代码质量良好。\n\n你可以标记任务完成了。"
)

如果不通过：
SendMessage(
  type: "message",
  recipient: "coder",
  content: "审查不通过 ❌\n\n问题：\n1. 测试用例缺少边界情况\n2. 缺少错误处理\n\n请修复后重新提交审查。"
)
```

---

## 十一、项目文件结构

初始化时自动创建：

```
project/
├── .agent/
│   ├── progress.json        # 进度追踪
│   ├── feature_list.json    # 功能列表
│   └── session.log          # 会话日志
├── research/                # 研究资料
├── drafts/                  # 草稿/开发中
├── review/                  # 审阅中
└── completed/               # 已完成
```

### 进度文件位置

**进程唯一**（推荐）：绑定到项目路径

```
{项目目录}/.agent/progress.json
{项目目录}/.agent/feature_list.json
```

团队配置仍然放在全局：

```
~/.claude/teams/{project-hash}/config.json
```

---

## 十二、会话恢复流程

每个新会话开始时执行：

```bash
# 1. 读取进度
cat .agent/progress.json

# 2. 读取任务列表
TaskList

# 3. 检查团队状态
Read ~/.claude/teams/{team-name}/config.json

# 4. 选择下一个任务
# 优先选择：pending + 无 owner + 无 blockedBy
```

### 会话恢复示例

```
# 新会话开始

1. 读取 ~/.claude/teams/auth-system/progress.json
   → in_progress: "task-3"
   → next_steps: ["完成 API 测试"]

2. 检查 TaskList
   → task-3 status: in_progress, owner: coder

3. 检查 team config
   → coder: 已关闭

4. 重新 spawn coder
   Agent(subagent_type: "general-purpose", name: "coder", team_name: "auth-system")

5. 发送恢复消息
   SendMessage(
     recipient: "coder",
     content: "继续工作：task-3\n\n下一步：完成 API 测试\n\n上次进度：登录逻辑已实现"
   )
```

---

## 十三、Git 自动化

### 自动初始化

如果项目没有 git，自动初始化：

```bash
cd {项目目录}
git init
git add .
git commit -m "初始化项目"
```

### 进度变更自动提交

每次任务状态变化时，自动提交：

```
任务开始 → git commit -m "开始: {任务名}"
任务完成 → git commit -m "完成: {任务名}"
重要修改 → git commit -m "更新: {修改描述}"
会话结束 → git commit -m "进度: 保存会话进度"
```

---

## 十四、五不原则

| 原则 | 含义 |
|------|------|
| **不做完不结束** | 每个任务必须有明确完成标准 |
| **不验证不完成** | 必须有人审查 |
| **不记录不结束** | 必须写入进度 |
| **不恢复不开始** | 新会话必须检查上次进度 |
| **不提交不结束** | 每次变更必须 git commit |

---

## 十五、评估与迭代

### 1. 立即开始小样本评估

```
早期代理开发中，变化有巨大影响：
- 一个提示调整可能从 30% 提升到 80%
- 只需要约 20 个测试用例
- 不要等到有几百个测试用例才开始

最佳实践：小规模测试立即开始，而非延迟
```

### 2. LLM-as-Judge

```
使用 LLM 评估输出的标准：
- 事实准确性（声明是否匹配来源？）
- 引用准确性（引用来源是否匹配声明？）
- 完整性（是否覆盖所有请求方面？）
- 来源质量（是否使用主要来源？）
- 工具效率（工具使用是否合理？）

推荐：单个 LLM 调用输出 0.0-1.0 分数和通过/失败
```

---

## 十六、生产可靠性

### 1. 代理是有状态的，错误会复合

```
- 代理可能运行很长时间
- 小错误可能导致代理探索完全不同的轨迹
- 需要能够从错误发生点恢复
- 让代理知道工具失败并让其适应
```

### 2. 调试需要新方法

```
代理是非确定性的，相同提示可能产生不同结果

解决方案：
- 完整的生产追踪
- 监控代理决策模式
- 不监控对话内容（保护隐私）
```

---

## 十七、触发条件

当检测到以下情况时，**自动启动此 skill**：

1. 用户说"帮我开发/创建/实现一个..."
2. 任务涉及多个模块或文件
3. 预估工作量超过一个会话
4. 用户明确提到"团队"、"分工"、"协作"
5. 任务可以分解为 3+ 个子任务

---

## 关键数字速查

| 指标 | 数值 |
|------|------|
| 代理 Token 消耗 | 约 4× 聊天 |
| 多代理 Token 消耗 | 约 15× 聊天 |
| 多代理性能提升 | 90.2% (vs 单代理) |
| Token 使用解释方差 | 80% |
| 工具响应限制 | 25,000 tokens |
| 评估最小样本 | ~20 个测试用例 |
| 中位数代理运行时间 | ~45 秒 |

---

## 参考资源

- [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [How We Built Our Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Measuring AI Agent Autonomy in Practice](https://www.anthropic.com/research/measuring-agent-autonomy)
- [How AI Is Transforming Work at Anthropic](https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic)
- [2026 Agentic Coding Trends Report](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf)

---

*v4.0 - 更新于 2026-03-13*
*整合 Anthropic 官方最佳实践*