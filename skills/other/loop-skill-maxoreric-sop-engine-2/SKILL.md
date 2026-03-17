---
name: loop-skill
description: 循环执行的 Skill。当需要重复执行直到满足条件时触发。触发词：循环、loop、重复、直到、until、持续。
---

# 循环执行

重复执行某个操作，直到满足完成条件。

## 机制

基于 Claude Code 的 Stop hook 实现：
1. 执行任务
2. Claude 尝试停止
3. Stop hook 检查完成条件
4. 未完成 → exit code 2 → 继续执行
5. 已完成 → exit code 0 → 允许停止

## 参数

- **任务描述**：要重复执行的任务
- **完成条件**：什么情况算完成
- **最大次数**：防止无限循环

## 使用方式

在对话中说明：
```
请循环执行 [任务描述]，直到 [完成条件]，最多 [N] 次
```

或使用 slash command：
```
/loop "任务描述" --until "完成条件" --max 10
```

## 完成条件类型

### 1. 文件存在
```
直到 output.md 存在
```

### 2. 内容匹配
```
直到输出包含 "DONE"
```

### 3. 评价通过
```
直到评价分数 >= 7
```

### 4. 人工确认
```
直到用户确认满意
```

## 状态追踪

在 `.meta/loop-status.json` 中记录：

```json
{
  "task": "任务描述",
  "completion_condition": "完成条件",
  "max_iterations": 10,
  "current_iteration": 3,
  "status": "running",
  "history": [
    {"iteration": 1, "result": "..."},
    {"iteration": 2, "result": "..."}
  ]
}
```

## 原则

- 必须设置最大次数，防止无限循环
- 每次迭代要有进展，不要原地踏步
- 卡住时要能跳出并报告
- 记录每次迭代的结果
