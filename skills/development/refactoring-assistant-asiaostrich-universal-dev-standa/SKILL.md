---
source: skills/claude-code/refactoring-assistant/SKILL.md
source_version: 2.0.0
translation_version: 2.0.0
last_synced: 2026-01-21
status: current
name: refactoring-assistant
description: |
  引导重构决策和大规模代码改进。
  使用时机：重构代码、遗留系统现代化、技术债、重写决策。
  关键字：refactor, rewrite, legacy, strangler, technical debt, 重构, 重写, 技术债.
---

# 重构助手

> **语言**: [English](../../../../../skills/claude-code/refactoring-assistant/SKILL.md) | 简体中文

**版本**: 2.0.0
**最后更新**: 2026-01-21
**适用范围**: Claude Code Skills

---

## 目的

本技能提供重构与重写的决策框架、大规模重构模式，以及技术债管理。策略分为三个层级：战术性（日常）、战略性（架构）、安全防护（遗留代码）。

---

## 快速参考（YAML 压缩格式）

```yaml
# === 决策：重构 vs 重写 ===
decision_tree:
  - q: "代码在生产环境运行？"
    n: "→ 考虑重写（风险较低）"
    y: next
  - q: "了解代码的功能？"
    n: "→ 先写特征测试"
    y: next
  - q: "测试覆盖率 >60%？"
    n: "→ 先补测试"
    y: next
  - q: "核心架构可修复？"
    n: "→ Strangler Fig 模式"
    y: "→ 增量重构 ✓"

comparison_matrix:
  favor_refactor: [大型代码库, 良好测试, 业务关键, 团队熟悉, 架构健全, 时间紧迫, 低风险]
  favor_rewrite: [小型独立, 无测试, 可容忍停机, 无人熟悉, 架构有缺陷, 时间充裕, 较高风险]

# === 警告：第二系统效应 ===
rewrite_antipatterns:
  - "加入原本没有的功能"
  - "为未来弹性过度抽象"
  - "忽略现有系统的经验教训"
quote: "第二个系统是一个人设计过最危险的系统。— Fred Brooks"

# === 战术性策略：日常重构 ===
tactical:
  preparatory_refactoring:
    definition: "在新增功能前调整结构，让改变更容易"
    quote: "先把改变变容易（这可能很难），然后再做那个容易的改变。— Kent Beck"
    when: [功能被阻挡, 降低阻力, 即将变更]
    workflow:
      1: "识别要做的改变"
      2: "识别是什么让改变困难"
      3: "重构以让改变变容易"
      4: "做那个（现在变容易的）改变"
    principles:
      - "预备性重构与功能分开提交"
      - "每一步都维持测试通过"
      - "不要混合重构与功能工作"

  boy_scout_rule:
    definition: "离开时让代码比来时更干净（机会主义重构）"
    quote: "离开营地时，让它比你来的时候更干净。— Robert C. Martin"
    when: [任何维护, Bug修复, 功能新增, 对抗熵]
    guidelines:
      - "只做小改进（分钟，不是小时）"
      - "不改变行为"
      - "不破坏现有测试"
      - "保持范围在当前任务内"
    examples:
      - "重新命名令人困惑的变量"
      - "将几行代码提取为命名良好的方法"
      - "移除死代码"
      - "加入澄清注释"
    antipatterns:
      - "把 Bug 修复变成大重构"
      - "重构不相关的代码"
      - "没有测试覆盖就修改"
      - "范围蔓延超出原始任务"

  red_green_refactor:
    definition: "TDD 重构阶段"
    duration: "每循环 5-15 分钟"
    scope: "单一方法/类"
    techniques: [提取方法, 重新命名, 内联变量, 替换魔术数字]
    reference: "→ 见 TDD 标准"

# === 战略性策略：架构重构 ===
strategic:
  strangler_fig:
    definition: "逐步将功能路由到新系统，渐进替换旧系统"
    origin: "命名自绞杀榕树"
    phases:
      1_拦截: "请求 → 门面 → 旧系统(100%)"
      2_迁移: "请求 → 门面 → [新系统(功能), 旧系统(其余)]"
      3_完成: "请求 → 新系统(100%) [旧系统下线]"
    checklist:
      - "识别拦截点"
      - "建立事件捕获层"
      - "在新系统实现第一个功能"
      - "渐进式路由流量"
      - "监控并比较"
      - "下线旧系统"

  anti_corruption_layer:
    definition: "防止遗留模型污染新系统的翻译层"
    origin: "Eric Evans, 领域驱动设计 (2003)"
    when:
      - "新旧系统必须共存并互动"
      - "遗留系统有混乱的领域模型"
      - "保护新系统的限界上下文"
    components:
      facade: "简化复杂的遗留接口"
      adapter: "将遗留数据转换为新领域模型"
      translator: "映射遗留术语到通用语言"
    checklist:
      - "定义清晰的 ACL 接口"
      - "映射遗留实体到新模型"
      - "处理数据格式转换"
      - "实现错误翻译"
      - "加入日志以便调试"
      - "彻底测试 ACL 隔离性"
    vs_strangler:
      strangler: "目标是取代遗留"
      acl: "目标是与遗留共存"

  branch_by_abstraction:
    steps:
      1: "客户端 → 抽象(接口) → 旧实现"
      2: "客户端 → 抽象 → [旧实现, 新实现(切换)]"
      3: "客户端 → 新实现 [旧实现已移除]"
    principles: [所有变更在主干, 功能开关, 过渡期共存]

  parallel_change:
    aka: "Expand-Migrate-Contract"
    phases:
      expand: "新增新的在旧的旁边，新代码用新的，旧的仍运作"
      migrate: "更新所有客户端用新的，验证，数据迁移"
      contract: "移除旧的，清理，更新文档"

# === 安全策略：遗留代码 ===
safety:
  legacy:
    definition: "没有测试的代码（不论年龄）"
    dilemma: "安全修改需要测试 → 加测试需要修改代码"
    solution: "使用安全技术先加测试"

  characterization_tests:
    purpose: "捕捉现有行为（非验证正确性）"
    process:
      1: "调用要理解的代码"
      2: "写预期会失败的断言"
      3: "执行，观察实际结果"
      4: "更新断言以匹配实际行为"
      5: "重复直到涵盖需要修改的行为"
    principle: "记录代码做什么，而非应该做什么"

  scratch_refactoring:
    definition: "为了理解而重构，舍弃所有变更"
    workflow:
      1: "建立探针分支（或 git stash）"
      2: "大胆重构以理解"
      3: "记录学到的内容"
      4: "舍弃变更（git reset --hard）"
      5: "应用学习编写特征测试"
    when: [代码太复杂, 无文档, 需要快速建立心智模型]
    principle: "目标是理解，不是整洁代码"

  seams:
    definition: "可以在不编辑代码的情况下改变行为的地方"
    object: "通过多态覆写（注入测试替身）"
    preprocessing: "编译时替换（宏）"
    link: "链接时替换（DI，模块替换）"

  sprout_wrap:
    sprout_method: "新逻辑 → 建立新方法，从旧的调用"
    sprout_class: "新逻辑独立演进 → 新类"
    wrap_method: "加入前后行为 → 重命名原方法，建立包装器"
    wrap_class: "装饰现有 → 装饰者模式"
    principle: "新代码用 TDD；遗留代码在测试前保持不动"

# === 数据库：重构 ===
db_expand_contract:
  expand: "新增新列/表，应用程序同时写入，可安全回滚"
  migrate: "复制数据，验证一致性，应用程序从新的读取"
  contract: "确认旧的未使用，移除旧的，清理双写"

db_scenarios:
  rename_column: {strategy: "新增→迁移→删除", risk: 中}
  split_table: {strategy: "新表+外键→迁移→调整", risk: 高}
  merge_tables: {strategy: "新表→合并→切换", risk: 高}
  change_datatype: {strategy: "新列→转换→切换", risk: 中}
  add_not_null: {strategy: "填默认→加约束", risk: 低}

# === 工作流程：安全重构 ===
before: [定义成功标准, "覆盖率>80%", 干净工作目录, 建立分支, 与团队沟通]
during: [一次一个小变更, 每次变更后测试, 失败就恢复, 频繁提交, 不加新功能]
after: [所有测试通过, 可衡量地更好, 文档已更新, 团队已审查, 没有新功能]

# === 指标 ===
code_quality:
  cyclomatic_complexity: "每函数<10"
  cognitive_complexity: "越低越好"
  coupling: "降低"
  cohesion: "提高"
  duplication: "<3%"

test_quality:
  coverage: "≥80%，不降低"
  speed: "重构后更快"
  flaky_count: "降低"

# === 技术债管理 ===
quadrant: # Martin Fowler
  prudent_deliberate: "我们知道这是债务"
  reckless_deliberate: "没时间做设计"
  prudent_inadvertent: "现在知道应该怎么做了"
  reckless_inadvertent: "什么是分层？"

priority:
  high: {criteria: "阻塞开发，频繁出错", action: "立即处理"}
  medium: {criteria: "拖慢开发，增加复杂度", action: "规划到下个迭代"}
  low: {criteria: "小麻烦，影响局部", action: "有机会就处理"}

tracking:
  fields: [描述, 影响, 估计工作量, 忽视风险, 相关代码]

# === 决策矩阵摘要 ===
decision_matrix:
  - {strategy: "预备性重构", scale: "小", risk: "低", use: "降低功能开发阻力"}
  - {strategy: "童子军规则", scale: "极小", risk: "低", use: "持续偿债"}
  - {strategy: "红-绿-重构", scale: "小", risk: "低", use: "TDD 开发循环"}
  - {strategy: "绞杀榕", scale: "大", risk: "中", use: "系统汰换"}
  - {strategy: "防腐层", scale: "中", risk: "低", use: "新旧共存"}
  - {strategy: "抽象分支", scale: "大", risk: "中", use: "主干重构"}
  - {strategy: "平行变更", scale: "中", risk: "低", use: "接口/Schema 迁移"}
  - {strategy: "特征测试", scale: "—", risk: "—", use: "遗留重构的前置条件"}
  - {strategy: "探针式重构", scale: "小", risk: "低", use: "理解黑盒代码"}

# === 策略选择 ===
selection_guide:
  功能被混乱代码阻挡: "预备性重构"
  在Bug修复中接触代码: "童子军规则"
  用TDD写新代码: "红-绿-重构"
  取代整个遗留系统: "绞杀榕"
  整合遗留不被污染: "防腐层"
  在主干重构共享代码: "抽象分支"
  变更广泛使用的接口: "平行变更"
  处理未测试的遗留: "特征测试 + 探针式重构 先做"
```

---

## 配置侦测

### 侦测顺序

1. 检查 `CONTRIBUTING.md` 中的「停用技能」区段
2. 检查 `CONTRIBUTING.md` 中的「重构标准」区段
3. 如果未找到，**默认使用标准重构实践**

---

## 详细指南

完整标准请参阅：
- [重构标准](../../../core/refactoring-standards.md)

---

## 相关标准

- [重构标准](../../../core/refactoring-standards.md) - 核心标准
- [测试驱动开发](../../../core/test-driven-development.md) - TDD 重构阶段
- [代码审查检查清单](../../../core/code-review-checklist.md) - 重构 PR 审查
- [签入标准](../../../core/checkin-standards.md) - 提交前要求
- [TDD 助手](../tdd-assistant/SKILL.md) - TDD 工作流程

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 2.0.0 | 2026-01-21 | 新增战术性策略（预备性重构、童子军规则）、防腐层、决策矩阵摘要。重组为战术性/战略性/安全防护三层。 |
| 1.0.0 | 2026-01-12 | 初始发布 |

---

## 授权

本技能以 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授权发布。

**来源**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
