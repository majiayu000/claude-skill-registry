---
name: code-reviewer
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements - reviews implementation against plan or requirements with severity分级（Critical/Important/Minor）. NO MERGE WITHOUT CODE REVIEW FIRST.
metadata:
  short-description: 代码审查与质量保证
  keywords:
    - code-reviewer
    - 代码审查
    - Code Review
    - 代码质量
    - 安全检查
    - 性能优化
    - 最佳实践
    - code review
    - quality check
  category: 代码质量
  author: Bensz Conan
  platform: Claude Code | OpenAI Codex | ChatGPT
  iron-law: |
    NO MERGE WITHOUT CODE REVIEW FIRST
---

# Code Reviewer - 代码审查专家

铁律：`NO MERGE WITHOUT CODE REVIEW FIRST`。

目标：用最少的时间发现“最致命的问题”（安全/正确性/数据一致性/可维护性），并给出可落地的修复建议。

为满足社区推荐的 `SKILL.md` 500 行以内约束：大量代码示例与长模板已下沉到 `awesome-code/agents/code-reviewer/references/legacy-skill-full.md`。

## 何时使用

- 重大功能完成后、合并前、发布前
- 大重构/跨模块变更
- 引入新依赖、新权限、新数据流

## 审查输入

- 需求/计划：用户描述、PR 描述、`PLAN.md`
- 代码改动：diff、关键文件、测试结果
- 风险偏好：可接受的破坏性/性能回退范围

## 输出格式（必须结构化）

对每个问题输出：
- Severity：Critical / Important / Minor
- What：问题是什么（具体到文件/函数/行为）
- Why：为什么是问题（风险与影响）
- Fix：如何修（最小变更优先）
- Verify：如何验证（测试/复现步骤）

## 审查顺序（先 P0 再 P2）

1. Critical（P0）
   - 鉴权/授权缺陷、注入、路径遍历、敏感信息泄露
   - 数据一致性/事务边界错误、不可恢复的数据破坏

2. Important（P1）
   - 明显性能风险（N+1、O(n^2) 热路径、内存爆）
   - 测试覆盖不足（关键路径无回归验证）

3. Minor（P2）
   - 可维护性：命名、重复、复杂度、模块边界
   - 文档/注释/类型标注缺失

## 快速检查清单

- [ ] 输入验证与输出编码是否到位？
- [ ] 权限校验是否在服务端强制执行？
- [ ] 是否引入了新的敏感数据写入/日志输出？
- [ ] 是否有回归测试或至少可复现的验证步骤？
- [ ] 是否存在明显的性能/资源泄露风险？

