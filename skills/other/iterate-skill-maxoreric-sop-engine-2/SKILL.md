---
name: iterate-skill
description: 迭代改进 Skill 的 Skill。当评价不通过或需要优化时触发。触发词：迭代、改进、优化、iterate、improve。
---

# 迭代改进

根据评价结果，改进 Skill。

## 前置条件

- `evaluation.json` 存在（评价结果）
- `evaluation.md` 存在（改进建议）
- `SKILL.md` 存在（当前版本）

## 流程

1. **读取评价** - 读取 evaluation.json 和 evaluation.md
2. **分析问题** - 找出低分维度和改进建议
3. **备份当前版本** - 复制到 versions/
4. **修改 Skill** - 根据建议改进 SKILL.md
5. **更新 criteria.md** - 如需调整评价标准
6. **更新状态** - 更新 status.json 的 iteration 计数

## 改进策略

### 产出完整性低
- 检查是否遗漏了必要内容
- 补充缺失的部分
- 增加检查清单

### 产出质量低
- 分析质量问题的原因
- 增加质量要求的描述
- 添加示例和反例

### 目标达成低
- 重新审视目标定义
- 调整 Skill 的流程
- 增加验证步骤

## 版本管理

备份到 `versions/` 目录：
- `SKILL.v1.md`
- `SKILL.v2.md`
- ...

命名规则：`SKILL.v{iteration}.md`

## 输出

更新后的文件：
- `.sop-engine/skills/<skill-name>/SKILL.md`（新版本）
- `.sop-engine/skills/<skill-name>/versions/SKILL.v{n}.md`（旧版本备份）
- `.sop-engine/skills/<skill-name>/.meta/status.json`（iteration +1）

## 原则

- 每次迭代只改一个主要问题
- 保留历史版本，支持回滚
- 改进要有针对性，不要大改
- 检查是否会引入新问题
