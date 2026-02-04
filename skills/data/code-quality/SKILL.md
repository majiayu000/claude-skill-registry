---
name: code-quality
description: 执行代码质量门禁检查（测试通过→覆盖率→Lint→GOAL追溯→可提交），验证单元测试覆盖率≥80%、集成测试通过率≥95%、代码规范零错误。当完成代码实现、准备提交代码、需要质量验证、进行提交前自检时使用。确保代码可合并。
stage: EXECSPEC_FULFILL
level_supported: [L1-STREAMLINED]
---

# Code Quality Skill

> **Scope**: EXECSPEC_FULFILL — Fulfill ExecSpec（落实 ExecSpec）
>
> **版本**: 0.1.0（占位）| **创建日期**: 2025-11-27

---

## 概述

Code Quality 是代码提交前的质量门禁：

```
┌─────────────────────────────────────────────────────┐
│              ✅ Code Quality Gates                  │
├─────────────────────────────────────────────────────┤
│  测试通过 → 覆盖率 → Lint → GOAL追溯 → 可提交     │
│  (Tests)   (Coverage) (Style) (Trace)  (Commit)   │
└─────────────────────────────────────────────────────┘
```

**核心职责**：
- 质量门禁检查（覆盖率、集成测试）
- 代码规范验证（lint、format）
- GOAL 追溯完整性
- 提交前自检

---

## L1-STREAMLINED

### 质量门禁阈值

| 指标 | L1 阈值 |
|------|---------|
| 单元测试覆盖率 | ≥ 80% |
| 集成测试通过率 | ≥ 95% |
| Lint 错误 | 0 |
| GOAL 覆盖 | 100% |

### 检查清单

- [ ] 所有测试通过（无红色）
- [ ] 覆盖率达标（≥80%）
- [ ] 无 lint 错误
- [ ] GOAL 注释完整

### 通过标准

- 4 项全部通过（100%）

---

## >> 命令

```
>>quality_gate_l1      # 执行质量门禁检查
>>pre_commit_l1        # 提交前自检
```

---

## Commit Message 规范

```
<type>(<scope>): <subject>

<body>

GOAL: GOAL-XXX-001
```

**Type 类型**：
- `feat`: 新功能
- `fix`: Bug 修复
- `refactor`: 重构
- `test`: 测试
- `docs`: 文档

**示例**：
```
feat(auth): 实现用户登录功能

- 添加登录表单验证
- 集成 JWT token 生成
- 添加单元测试

GOAL: GOAL-AUTH-001
```

---

## 相关 Skills

- **前置**: tdd-cycle（TDD 循环中）
- **原则**: principle-solid, principle-dry
- **后续**: progress-tracking（更新进度）

---

**TODO**: 待细化质量门禁脚本和自动化检查流程
