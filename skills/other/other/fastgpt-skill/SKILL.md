---
description: 上海财经大学 FastGPT 平台接口，接入「匡时财经教育大模型」和「博弈与社会课程智能体」。当用户需要使用上财校内 AI 助教或教育大模型时使用。
---

# fastgpt-skill

上财 FastGPT 平台 OpenAPI 封装。

## 核心能力

- 匡时财经教育大模型问答
- 博弈与社会课程智能体
- 多 agent 配置支持

## 接口

- 上财 FastGPT：llm.sufe.edu.cn OpenAPI

## 使用

```bash
node "$SKILLS_ROOT/fastgpt-skill/index.js" --query "什么是纳什均衡"
```

## 注意

- 需要上财校内网络或 VPN
- agent 配置在 index.js 中预设
