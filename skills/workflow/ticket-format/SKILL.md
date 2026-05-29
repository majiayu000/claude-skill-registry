---
name: ticket-format
description: 任务工单格式规范，定义标准工单结构与子任务状态流转
---

# Skill: 工单格式

> **适用 Agent**：尚书省、六部
> **加载时机**：尚书省派发任务时；六部接收任务时

## 任务工单

```json
{
  "task": {
    "id": "TASK-20260312-001",
    "title": "实现用户登录接口",
    "priority": "P1",
    "source": "旨意原文摘要",
    "plan_id": "PLAN-20260312-001",
    "assigned_to": "gongbu",
    "depends_on": [],
    "tags": [],
    "acceptance_criteria": [
      "JWT Token 正确签发",
      "错误返回统一格式",
      "单元测试覆盖率 > 80%"
    ],
    "status": "assigned",
    "deliverables": [],
    "notes": ""
  }
}
```

## 子任务状态

| 状态 | 含义 | 负责方 |
|------|------|--------|
| `pending` | 待派发 | 尚书省 |
| `assigned` | 已派发至某部 | 尚书省 → 六部 |
| `in_progress` | 执行中 | 六部 |
| `blocked` | 被阻塞，需协调 | 六部 → 尚书省 |
| `done` | 部门完成，待汇总 | 六部 → 尚书省 |
| `auditing` | 门下覆奏审查中 | 尚书省 → 门下省 |
| `rejected` | 产出不合格，打回 | 尚书省 / 刑部 → 六部 |
| `partial_done` | 部分子任务完成，其余超时/失败 | 堂官 → 尚书省（附缺失说明） |
