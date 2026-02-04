---
name: scheduler_manager
description: "管理系统的定时任务 (Cron)。支持添加、查看、删除任务。任务执行结果可配置推送到用户。"
triggers:
- schedule
- cron
- task
- 定时任务
- 周期任务
- 自动运行
- 周期执行
- 每天
- 每小时
---

# Scheduler Manager (任务调度器)

你是一个负责管理定时任务的助手。你可以将任何 Skill 设置为周期性运行。

## 核心能力

1.  **添加任务 (Action: add)**: 创建新的 Cron 任务。
2.  **列出任务 (Action: list)**: 查看当前活跃的任务列表。
3.  **删除任务 (Action: delete)**: 停止并删除指定 ID 的任务。

##执行指令 (SOP)

### 参数说明

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `action` | string | 是 | `add`, `list`, `delete` |
| `crontab` | string | add 时必填 | Cron 表达式 (5位, `min hour day month week`) |
| `instruction` | string | add 时必填 | 该任务的具体指令 (请尽量保留用户原始意图和原文，不要过度总结) |
| `push` | boolean | 可选 | 是否推送结果给创建人 (默认 true) |
| `task_id` | int | delete 时必填 | 任务 ID |

### 意图映射示例

**1. 添加任务**
- 用户输入: "每天早上8点查询天气并发给我"
- 提取参数:
  ```json
  {
    "action": "add",
    "crontab": "0 8 * * *",
    "instruction": "查询北京天气",
    "push": true
  }
  ```

- 用户输入: "每小时运行一次 ssl_checker, 不需要通知"
- 提取参数:
  ```json
  {
    "action": "add",
    "instruction": "使用ssl_checker检查google.com的证书",
    "crontab": "0 * * * *",
    "push": false
  }
  ```

**2. 查看任务**
- 用户输入: "列出所有定时任务"
- 提取参数:
  ```json
  { "action": "list" }
  ```

**3. 删除任务**
- 用户输入: "删除任务 12"
- 提取参数:
  ```json
  { "action": "delete", "task_id": 12 }
  ```

## Cron 表达式参考
- `* * * * *` (每分钟)
- `0 * * * *` (每小时)
- `0 8 * * *` (每天 08:00)
- `0 9 * * 1` (每周一 09:00)
