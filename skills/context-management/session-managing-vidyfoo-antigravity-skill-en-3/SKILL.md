---
name: session-managing
description: 自动触发的会话生命周期管理 - INHERIT (继承知识) + DEPOSIT (沉淀精华)
auto_trigger: true
---

# Session Lifecycle Skill

> **核心理念**: 会话生命周期 = 继承 → 工作 → 沉淀 → 闭环升级

---

## 自动触发协议

本 Skill 无需手动调用，AI 会在适当时机自动激活。

### INHERIT 模式 (继承)

**触发时机**:
- 新对话开始 (对话历史为空)
- 用户发出首个任务型请求
- 用户明确说 "开始"、"入职"、"onboarding"

**执行动作**:
```
1. view_file doc/memory.md (读取 TL;DR 10 条核心认知)
2. view_file .agent/rules/rule-one.md
3. (复杂任务) view_file doc/explanation/architecture.md
4. 静默继承，不打断用户工作流
```

**输出**: 无 (静默执行) 或简短确认

---

### DEPOSIT 模式 (沉淀)

**触发时机** (满足任一条):
- [ ] 产生了新的设计决策或架构选择
- [ ] 发现并解决了隐藏的技术问题
- [ ] 形成了可复用的编程模式或最佳实践
- [ ] 产生了"这个想法太妙了"的闪光洞察
- [ ] 对话即将结束且有沉淀价值

**执行动作**:
```
1. 提炼本次对话精华 (CORE/PATTERN/DECISION/TIP)
2. view_file doc/memory.md
3. 融合更新 doc/memory.md (去重升维)
4. 如为技术规范 → 写入 doc/specs/
5. 通知用户完成
```

**输出**:
```markdown
## 📦 沉淀完成

**本次新增**:
- `[PATTERN]` {模式名}
- `[DECISION]` {决策名}

✅ memory.md 已更新 (累计 N 条)
```

---

## 手动覆盖

用户可随时说:
- "跳过 onboarding" → 禁用 INHERIT
- "沉淀本次对话" → 强制 DEPOSIT
- "不需要沉淀" → 禁用 DEPOSIT

---

## Doc 系统集成 (Diátaxis)

### INHERIT 读取链 (优先级从高到低)

| 层级 | 文件 | 策略 | 说明 |
|------|------|------|------|
| **L1 必读** | `doc/memory.md` (TL;DR) | 始终 | 核心认知与原则 |
| **L1 必读** | `.agent/rules/rule-one.md` | 始终 | 项目宪章与禁忌 |
| **L2 按需** | `doc/explanation/README.md` | 架构与全貌 | 系统索引 |
| **L3 上下文** | `doc/explanation/subsystems/{xxx}.md` | 特定 Feature | 深度理解子系统 |
| **L3 上下文** | `doc/specs/{xxx}.md` | 特定 Feature | 查阅具体规范 |
| **L4 入门** | `doc/tutorials/quick-start.md` | 新手/重置 | 环境搭建与启动 |

### DEPOSIT 写入链

根据知识类型选择写入位置：

| 知识类型 (Diátaxis) | 写入目标 | 示例 |
|---------------------|----------|------|
| **Core Wisdom** (智慧/决策) | `doc/memory.md` | 设计哲学、架构决策、踩坑教训 |
| **Understanding** (原理/架构) | `doc/explanation/subsystems/` | 模块架构图、核心机制解析 |
| **Reference** (规范/规则) | `doc/specs/` | API 定义、业务规则、边界情况 |
| **How-To** (指南/测试) | `doc/how-to/` | 测试策略、调试指南、操作手册 |
| **Archive** (历史/草稿) | `doc/archive/` | 过时的设计文档、被取代的方案 |

---

## 记忆格式规范

详见 [memory-schema.md](resources/memory-schema.md)

### 类型标签

| 标签 | 含义 |
|------|------|
| `[CORE]` | 核心原则，永恒不变 |
| `[PATTERN]` | 可复用模式 |
| `[DECISION]` | 时间点决策 |
| `[TIP]` | 实用技巧 |

### 禁止事项

- ❌ 在 memory.md 中放置代码块
- ❌ 添加废话或显而易见的内容
- ❌ TL;DR 超过 10 条

---

## 质量门禁

### INHERIT

- [ ] 读取了 memory.md TL;DR
- [ ] 读取了 rule-one.md
- [ ] 理解项目核心规则

### DEPOSIT

- [ ] 新增内容真正有价值
- [ ] 表述足够精炼
- [ ] 已标注类型标签
- [ ] 已移除代码示例
