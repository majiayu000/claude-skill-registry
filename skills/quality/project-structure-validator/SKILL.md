---
name: project-structure-validator
description: 压力测试STRUCT文件，验证模块化分解的可行性。当项目结构确定后使用，确保模块边界清晰。
stage: IMPLEMENTATION_PLANNING
level_supported: [L1, L2, L3]
---

## project-structure-validator: 项目结构验证

### 描述
压力测试project_structure.md中定义的模块化分解方案，验证其在真实场景下的可行性和独立性。

### 适用场景
- **WORKFLOW_STEP_5 Task S5-1**: STRUCT验证时，评估分解方案的合理性
- **WORKFLOW_STEP_5 Task S5-3**: Self-Reflection中定期审视模块边界
- **复杂项目**: 模块众多且依赖复杂时

### 输入
- spec/implementation/project_structure.md（模块定义）
- design/architecture.md（组件依赖）
- goal_breakdown.md（GOAL与模块的映射）
- 当前级别（L1/L2/L3）

### 输出
- 项目结构验证报告（markdown）
- 模块分解评分（模块数/独立性/清晰度）
- 风险识别：
  - 模块间循环依赖
  - 模块职责重叠
  - 模块边界模糊
  - 模块规模不平衡
- 改进建议

### 执行策略
1. 从project_structure.md读取模块定义
2. 验证模块的独立性指标：
   - 模块数量适当（L1: 3-5, L2: 5-8, L3: 8-12）
   - 无循环依赖（依赖图为DAG）
   - 职责清晰（无大量协作职责）
   - 规模平衡（内部代码行数相近）
3. 对照goal_breakdown.md，检查GOAL分配到模块的合理性
4. 识别高风险模块（核心/复杂/关键路径）
5. 生成验证报告和改进建议

### 价值
- **Architecture**: 评估模块设计的质量，及早识别问题
- **Tech Lead**: 指导模块划分，减少后期大规模重构
- **Dev**: 清晰的模块边界，便于团队分工

### 验收标准
- 模块数量适当（不过多不过少）
- 无循环依赖
- 模块职责单一清晰
- 模块规模平衡
- 所有GOAL能清晰分配到模块
