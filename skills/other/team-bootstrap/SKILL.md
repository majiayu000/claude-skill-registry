---
name: team-bootstrap
description: 首次创建 Teammate 的引导流程——太子首次协作或尚书首次派发六部时加载，完成 Team 创建与分层启动
---

# Skill: 会话引导（Team Bootstrap）

> **适用 Agent**：太子（Lead）、尚书省
> **加载时机**：会话中首次需要与 Teammate 通信前（收到旨意、执行早朝等）

## 术语约定

本项目中 **Agent** 与 **Teammate** 含义不同，不可混用：

| 术语 | 含义 | 示例 |
|------|------|------|
| **Agent** | 逻辑角色身份——governance-core 与 architecture-overview 中定义的十个角色 | "中书省 Agent 负责规划" |
| **Teammate** | Claude Code 运行时实例——通过 `Agent tool + team_name` 创建的进程 | "创建中书省 Teammate" |
| **Lead** | 团队领导的运行时实例——太子即 Lead | "太子（Lead）创建团队" |

**核心原则**：Agent 是设计图纸上的角色，Teammate 是实际上工的人。**SendMessage 只能送达已创建的 Teammate，不能凭空唤醒一个不存在的实例。**

## 引导流程

```
会话启动 → 太子就位
  ├─ 闲聊 → 太子直答，不创建 Teammate
  └─ 旨意/早朝/需协作
       ├─ 步骤1：TeamCreate（仅首次，team_name: "sansheng-liubu"）
       ├─ 步骤2：创建三省（中书·门下·尚书，治理必备）
       ├─ 步骤3：太子 SendMessage 传旨中书省
       └─ 步骤4：按需创建六部（尚书省请求，太子代建）
```

## 三省职责原则

三省（中书、门下、尚书）是**决策与协调层**，不直接执行代码编写、测试、部署等具体操作。具体执行由尚书省派发至六部完成。三省职责边界：
- **中书省**：规划方案，不写代码
- **门下省**：审议与覆奏，不执行任务
- **尚书省**：派发协调汇总，不亲自动手

## Teammate 命名约束

> ⚠️ **Claude Code 已知 Bug**：Teammate `name` 含中文字符时，Agent 间通信（SendMessage）会静默失败。
>
> **规则：所有 Teammate 的 `name` 参数必须使用英文或拼音（ASCII），禁止使用中文。**
> - ✅ 合法：`zhongshu` `menxia` `shangshu` `gongbu` `worker-1`
> - ❌ 禁止：`中书省` `工部` `员外郎1`

## 防重检查流程

创建任何 Teammate 前，**必须**执行以下检查：

1. **读取团队配置**：`Read ~/.claude/teams/sansheng-liubu/config.json`
2. **检查 members 数组**：是否已有同名成员（`name` 字段匹配）
3. **若已存在**：发送探活 SendMessage，等待 30 秒判定存活
4. **若不存在** → 正常创建

> 📎 详细规则见 `bootstrap-timeout-policy.md`

## 分层创建策略

三层创建体系：第一层三省（太子直接创建）、第二层六部（尚书省请求，太子代建）、第三层员外郎（堂官申请→尚书省批准→太子代创建）。

> 📎 详细规则见 `bootstrap-prompts.md`

## 创建前检查清单

> 📎 详细规则见 `bootstrap-checklist.md`

## 释放策略

| Teammate | 释放时机 | 释放方式 |
|----------|---------|---------|
| 三省 | 当前旨意全部完成且无后续任务 | 太子发送 shutdown_request |
| 六部 | 尚书省确认无后续任务，或皇上明确要求清理 | 尚书省请求太子发送 shutdown_request（可选保留供后续复用） |
| 员外郎 | 子任务完成、堂官确认产出 | 堂官请求尚书省，尚书省转请太子 shutdown |

## 早朝场景特殊处理

早朝（`/morning-court`）：第一阶段太子自查（无需 Teammate）；第二阶段须确保三省已创建；第三阶段仅联络有活跃任务且已有 Teammate 的部门，否则太子代为汇总。

## Shutdown 超时处理

> 📎 详细规则见 `bootstrap-timeout-policy.md`
