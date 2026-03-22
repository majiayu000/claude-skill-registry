---
name: report-format
description: 尚书省 report 模式回奏格式规范，定义回奏必备字段与结构
---

# Skill: 回奏格式

> **适用 Agent**：尚书省
> **加载时机**：尚书省 report 模式（汇总完毕准备回奏时）

## 回奏报告格式

```json
{
  "report": {
    "plan_id": "PLAN-20260312-001",
    "title": "用户登录模块开发",
    "status": "delivered",
    "summary": "简要执行结果描述",
    "subtask_results": [
      {
        "task_id": "TASK-001",
        "department": "gongbu",
        "status": "done",
        "output": "src/auth/login.ts"
      },
      {
        "task_id": "TASK-002",
        "department": "xingbu",
        "status": "done",
        "output": "tests/auth/login.test.ts"
      }
    ],
    "issues": [],
    "recommendations": ""
  }
}
```

## 回奏流程

尚书省编写回奏报告后，通过 SendMessage 发送至太子（Lead），由太子汇总呈报皇上。太子不得修改回奏内容，仅负责中转与格式化呈报。

## 必备字段

- `plan_id`：关联的方案编号
- `status`：delivered / partial / failed
- `summary`：一段话概括执行结果
- `subtask_results`：每个子任务的完成状态与产出物
- `issues`：执行过程中遇到的问题（即使已解决也需记录）
