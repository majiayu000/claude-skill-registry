---
name: handoff-skill
description: Agent 间任务交接的 Skill。当需要把任务交给另一个 Agent 时触发。触发词：交接、handoff、交给、让 xxx 来处理。
---

# 任务交接

在 Agent 之间传递任务，参考邮件协议设计。

## 概念

| 邮件概念 | handoff 对应 |
|---------|-------------|
| From / To | 发送方 / 接收方 Agent |
| Subject | 任务主题 |
| Date | 时间戳 |
| Message-ID | task-id（唯一标识） |
| References | 上游任务（链式追溯） |
| Body | 任务描述 |
| Attachments | inputs/ 目录 |

## 流程

### 发送方

1. **创建 task-id** - 格式：`{timestamp}-{random}`
2. **准备输入文件** - 复制到 inputs/
3. **写 context.md** - 填写 Header 和 Body
4. **设置状态** - Status: pending
5. **通知接收方** - 告知 task-id

### 接收方

1. **读取 context.md** - 理解任务
2. **更新状态** - Status: in_progress
3. **执行任务** - 根据 Body 描述执行
4. **写入产出** - 放到 outputs/
5. **更新状态** - Status: completed / failed

## 目录结构

```
agents/<agent-name>/handoff/<task-id>/
├── context.md       # 任务上下文（严格格式）
├── inputs/          # 输入文件
└── outputs/         # 输出文件
```

## context.md 格式

```markdown
# Handoff

## Header
- Message-ID: 20240101-abc123
- From: researcher-agent
- To: writer-agent
- Date: 2024-01-01T12:00:00Z
- Subject: 撰写调研报告
- References: 20231231-xyz789

## Body

请根据调研结果撰写一份报告，要求：
1. 结构清晰
2. 重点突出
3. 包含结论和建议

## Attachments

- inputs/research.md
- inputs/data.json

## Status

pending
```

## Status 状态

- `pending` - 等待接收方处理
- `in_progress` - 接收方正在处理
- `completed` - 已完成
- `failed` - 失败

## 原则

- context.md 格式严格，Hook 要读取
- inputs/ 和 outputs/ 内容自由
- References 形成任务链，支持追溯
- 状态变更要及时更新
