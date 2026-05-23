---
name: mock-contract-advisor
description: 生成Mock/Stub契约检查清单，enforcing test_suites.md的Mock策略规则。当TS中Mock策略确定后使用。
stage: IMPLEMENTATION_PLANNING
level_supported: [L2, L3]
---

## mock-contract-advisor: Mock/契约设计

### 描述
基于test_suites.md的Mock/Stub策略，生成契约定义清单和检查规则。避免过度Mock、递归Mock等反模式。

### 适用场景
- **WORKFLOW_STEP_5 Task S5-2**: 创建test_suites.md中的Mock策略章节时
- **WORKFLOW_STEP_5 Task S5-3**: Self-Reflection中审视Mock设计
- **L2/L3项目**: 需要Complex Mock/契约设计的系统

### 输入
- test_suites.md（Mock策略章节）
- design/（组件间接口）
- goals_breakdown.md（需要Mock的依赖项）
- 当前级别（L2/L3）

### 输出
- Mock/契约设计报告（markdown）
- 契约清单（哪些外部服务需要Mock）
- Mock复杂度分析（简单/中等/复杂）
- 检查清单：
  - Mock粒度是否合理
  - 是否存在递归Mock
  - 是否使用全局Mock
  - 是否定义了契约验证
- 风险识别和建议

### Mock契约格式

**标准Mock契约定义**：
```yaml
Mock: [service_name]
  Purpose: [为什么需要Mock]
  Contract:
    Input:
      - Parameter: [name]
        Type: [type]
        Example: [example]
    Output:
      - Field: [name]
        Type: [type]
        Example: [example]
    Exceptions:
      - Error: [error_type]
        Condition: [when]
        Response: [response]
  Complexity: [Simple/Medium/Complex]
  Verification: [如何验证Mock被正确调用]
  Integration: [集成测试覆盖]
```

### 执行策略

**第1步: 依赖识别**
从design/列举所有外部依赖：
- 外部API（支付/短信/邮件等）
- 数据库（主库/缓存/队列等）
- 第三方服务（认证/分析等）
- 内部服务（其他微服务）

**第2步: Mock决策**
对每个依赖决定是否Mock：
| 依赖类型 | Mock | 集成测试 | 理由 |
|---------|------|--------|------|
| 外部API | ✅ | ✅ | 不可控，需Mock |
| 数据库 | ❌ | ✅ | 使用测试库 |
| 缓存 | ✅ | ✅ | 可Mock，也需集成 |
| 内部服务 | ✅ | ✅ | 可Mock，也需集成 |

**第3步: 契约定义**
为每个Mock定义清晰的契约：
- 输入参数及类型
- 输出数据及格式
- 异常情况及处理
- 验证方式

**第4步: 复杂度评估**
- **Simple**: 单一输入/输出，无异常处理
- **Medium**: 多参数/多返回值，有基本异常
- **Complex**: 复杂状态机、异步回调、多异常

**第5步: 反模式检查**
- ❌ 递归Mock: Mock的Mock（应该简化设计）
- ❌ 全局Mock: 全局状态Mock（应该用依赖注入）
- ❌ 过度Mock: Mock过多细节（应该集成测试）
- ❌ 无验证Mock: Mock未被验证调用（应该添加验证）

**第6步: L2/L3分级**
- **L2**: 关键依赖Mock + 基础集成测试
- **L3**: 完整Mock + 全面集成测试 + 异常场景覆盖

**第7步: 修复建议**
- 简化过度Mock的设计
- 添加缺失的集成测试
- 消除反模式
- 定义清晰的验证机制

### 价值
- **Dev**: 清晰的Mock契约定义，减少集成问题
- **QA**: Mock设计评审，确保测试真实性
- **Architecture**: 识别不合理的依赖设计

### 验收标准（L2/L3）
- 每个Mock都有清晰的契约定义
- 无递归Mock（Mock的Mock）
- 无全局Mock
- Mock粒度合理（不Mock过多细节）
- 存在对Mock的验证机制
- 集成测试覆盖关键依赖
