---
name: evaluate-skill
description: 评价 Skill 执行结果的 Skill。当需要评价产出质量、判断是否需要迭代时触发。触发词：评价、evaluate、打分、怎么样、效果如何。
---

# 评价

根据预定义的评价标准，评价 Skill 的执行结果。

## 前置条件

- `criteria.md` 存在（评价标准）
- 执行结果存在（要评价的产出）

## 流程

1. **读取评价标准** - 读取 criteria.md
2. **读取执行结果** - 读取要评价的产出
3. **逐维度评分** - 按核心维度和补充维度评分
4. **计算总分** - 加权计算总分
5. **判断是否通过** - 与通过条件对比
6. **输出评价** - 写入 evaluation.json 和 evaluation.md

## 评分规则

每个维度 1-10 分：
- 1-3：不合格，严重问题
- 4-5：勉强，有明显问题
- 6-7：合格，基本达标
- 8-9：良好，超出预期
- 10：优秀，完美

## 权重计算

- 高权重：x3
- 中权重：x2
- 低权重：x1

总分 = Σ(维度分数 × 权重) / Σ(权重) × 10 / 10

## 输出

### evaluation.json（严格格式，Hook 读取）

```json
{
  "score": 7.5,
  "pass": true,
  "needs_iteration": false,
  "reason": "产出完整，质量良好，达成目标",
  "dimensions": {
    "completeness": {"score": 8, "weight": "high"},
    "quality": {"score": 7, "weight": "high"},
    "goal_achievement": {"score": 8, "weight": "high"}
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### evaluation.md（人类可读）

```markdown
# 评价报告

## 总分：7.5 / 10 ✓ 通过

## 各维度评分

| 维度 | 分数 | 权重 | 说明 |
|-----|------|-----|------|
| 产出完整性 | 8 | 高 | [说明] |
| 产出质量 | 7 | 高 | [说明] |
| 目标达成 | 8 | 高 | [说明] |

## 结论

[是否通过，是否需要迭代]

## 改进建议

[如果需要迭代，给出具体建议]
```

## 输出位置

- evaluation.json → `.sop-engine/skills/<skill-name>/.meta/evaluation.json`
- evaluation.md → `.sop-engine/skills/<skill-name>/workspace/evaluation.md`

## 原则

- 评价要基于标准，不主观臆断
- 分数要有依据，给出说明
- 改进建议要具体可操作
- 允许补充临时维度
