---
name: context-updater
description: 项目上下文自动更新器。当新增功能、重构代码、修改架构时触发，确保 project_context.md 保持最新。触发词：新功能, 重构, 架构变更, 新模块, 新系统, 完成实现。
---

# 项目上下文更新器

当项目发生重大变更时，自动提醒更新 `.claude/context/project_context.md`。

## 触发判断

### ✅ 需要更新
- 新增 AutoLoad / 核心系统 / 重要组件
- 架构重构（状态机、依赖关系、数据流）
- 修改输入映射 / 物理层配置
- 完成重要功能实现

### ❌ 不需要更新
- bug修复、参数调整、性能优化（不涉及架构）
- UI样式调整、添加注释

## 更新原则

**文件**: `.claude/context/project_context.md`

1. **简洁优先** - 每个模块 ≤ 3 行描述
2. **结构化** - 使用列表/表格，避免段落
3. **架构级别** - 只记录架构信息，不含实现细节
4. **控制总量** - 保持 < 4000 tokens

## 更新示例

**变更**: 新增 SkillManager AutoLoad

**更新内容**:
```markdown
### AutoLoad 系统
- **SkillManager**: 技能管理，处理释放和冷却
```

**变更**: 实现连招系统

**更新内容**:
```markdown
### 连招系统
- **功能**: 检测输入序列，触发特殊技能
- **关键类**: ComboDetector, ComboData (Resource)
- **信号**: combo_triggered(combo_name: String)
```

## 自动检查清单

完成以下任务时，检查是否需要更新 context：

- [ ] 新增 AutoLoad 脚本
- [ ] 创建核心系统
- [ ] 重构状态机框架
- [ ] 修改输入/物理层配置
- [ ] 完成重要功能

## 更新流程

1. 检测变更范围（AutoLoad/核心模块/配置）
2. 读取 project_context.md，识别需要更新的章节
3. 生成简洁内容（≤3行/模块）
4. 验证 token 数量 < 4000，删除过时信息
5. 保存文件

## 提醒机制

**触发条件**:
- 检测到 `Util/AutoLoad/` 新增脚本
- 对话中出现 "完成"、"重构" 关键词
- 修改了状态机、伤害系统等框架代码

**提醒用户**: 列出变更内容，询问是否更新 context
