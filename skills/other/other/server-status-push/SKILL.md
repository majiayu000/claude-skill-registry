---
name: server-status-push
description: "检查 Linux 服务器健康状态并汇总发送给用户（支持一键文本报告）"
license: MIT
---

# server-status-push Skill

用于快速收集并汇报服务器运行状态（CPU/内存/磁盘/负载/网络/Docker）。

## 何时使用

当用户说：
- “看下服务器状态”
- “汇报机器健康情况”
- “发我当前服务器资源占用”

## 执行步骤

1. 运行状态采集脚本：

```bash
bash /root/.pi/agent/skills/server-status-push/collect-status.sh
```

2. 将结果直接回复用户。
3. 如果当前环境可用 `send_message` 工具，可额外调用 `send_message` 主动推送一次摘要。

## 输出要求

- 先给结论：正常/告警
- 再给关键指标：
  - load average
  - CPU 核心数
  - 内存使用率
  - 根分区使用率
  - Docker 容器状态（如可用）
- 如发现异常（例如磁盘 > 85%、内存 > 90%），明确标注并给出建议。

## 快速诊断阈值（默认）

- 磁盘使用率 > 85%：告警
- 内存使用率 > 90%：告警
- 1 分钟 load > CPU 核心数 × 1.5：告警

## 示例

```bash
bash /root/.pi/agent/skills/server-status-push/collect-status.sh
```
