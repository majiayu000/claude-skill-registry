---
name: capability-distill
description: 能力蒸馏工作流——从用户批准的强模型访谈或真实任务轨迹中提取非显然的判断规则，形成可审计的 judgment packet，再交给 skill-audit 和 skill-creator 决定是否落成可加载 skill。当用户说“蒸馏这个模型的判断力”“把这次任务的关键决策固化下来”“模型窗口要关了，保留它在某类场景的判断”时使用。普通流程文档、直接写 SKILL.md、泛化最佳实践或未授权的会话日志扫描不使用本 skill。
---

# Capability Distill

把“为什么在两个合理选项中选择其中一个”提取成证据支持的判断规则。不要把操作步骤、通用建议或原始会话内容换个格式包装成 skill。

## 与现有技能的边界

- `capability-distill`：选择获准证据、还原决策事件、提取判断规则、输出 judgment packet。
- `skill-audit`：判断这些规则是否值得成为 skill、归属哪个现有 skill、是否重复以及如何分层。
- `skill-creator`：创建或修改具体的 `SKILL.md`、设计 with-skill/baseline eval、迭代和验证触发描述。
- `skill-lifeguard`：当产物属于高影响工作流时补可靠性契约和漂移修复闭环。

不要在本 skill 中复制后三者的完整写作、注册或评测流程。目标是提供它们可消费的高信号输入。

## Operating Contract

- Direct actions: 使用当前对话和用户明确批准的本地材料；先读元数据再读内容；生成脱敏的 judgment packet；运行本地只读检查。
- Escalate before: 读取未获准的会话历史、memory、home 目录或其他仓库；把任何轨迹内容发送给外部模型；覆盖已有 skill；写入共享仓库；发布或安装产物。
- Evidence-backed pushback: 判断密度低、证据不足或已有 skill 完整覆盖时，给出具体重叠项并建议不蒸馏或只更新原 skill。
- Feedback loop: 把 eval 中的“未生效 / 机械化 / 误触发”连同对应 `rule_id` 回写到下一轮 judgment packet，而不是只改措辞。

## 0. 建立数据边界

在读取额外材料前记录以下字段：

```yaml
source_scope:
  approved_roots: []
  approved_artifact_types: []
  external_model_destination:
  raw_content_authorized: false
  output_path:
```

当前对话和用户本次明确附带的文件可直接使用。其他路径、历史日志和 memory 不因“可能有帮助”而自动进入范围；缺少批准时先询问并暂停对应读取。

执行以下数据纪律：

- 不假定 `~/.claude`、`~/.codex` 或任何固定运行时路径存在。使用用户给出的路径、当前工作区和当前运行时可用的搜索工具。
- 先查看文件名、时间、提交主题等元数据，只对候选决策事件读取最小必要片段。
- 不把 token、密钥、cookie、个人身份信息、客户数据、私有源码或完整 prompt/response 写入 packet 或 eval。
- 如需外部强模型，只发送经用户批准的脱敏场景摘要；没有目标模型和数据发送授权就标记阻塞，不假装完成窗口蒸馏。
- provenance 只写可验证的来源标签和日期。模型名、版本或作者未知时留空，不猜测。

## 1. 判断是否适合蒸馏

先区分对象：

- 可由固定命令或 checklist 完成的是流程，交给 `skill-audit` / `skill-creator`，不做判断蒸馏。
- 需要根据上下文在多个合理选项间权衡，并且存在切换、停止或上抛信号的，才是候选判断。
- 只包含“谨慎、验证充分、保持简洁”等通用态度时，直接判为低判断密度。

对候选场景记录 `judgment_density`、`evidence_strength` 和 `existing_coverage`（high / medium / low）。只保留判断密度高、证据至少中等且现有覆盖不完整的场景。

## 2. 还原决策事件

从获准证据中提取事件摘要，而不是复制原文。每个事件至少包含：

```yaml
decision_event:
  evidence_ref:
  context:
  viable_options: []
  chosen_option:
  observed_signal:
  outcome:
  counterfactual:
  redactions_applied: []
```

`evidence_ref` 使用本地、非敏感的定位信息，例如仓库相对路径和 commit SHA；不要把原始聊天文本塞进该字段。没有 outcome 的事件只能作为假设，不能升级为高置信规则。

## 3. 写作前重叠审计

在写任何 `judgment_rule` 前，先在 `source_scope` 获准的 roots 或已附 inventory 内搜索现有 rules、skills、registry 和相近 owner；先查索引和元数据，再读最可能相关的最小片段。没有获准的 owner 根目录或清单时，先请求范围并暂停规则起草，不能把“未提供”当作“无覆盖”。

每个候选场景记录 `searched_roots`、`queries`、`candidate_owners`、逐 owner 的 `coverage` / `evidence_ref`、`uncovered_gap` 和 `decision`：

- `covered`：停止起草，不生成新规则。
- `partial`：只允许为明确的 `uncovered_gap` 起草增量，默认更新现有 owner。
- `uncovered`：才可进入新规则候选；仍须在交付前完成逐规则归属复核。

该记录是进入下一步的硬 gate。后面的 `skill-audit` 复核不能替代这次写作前审计。

## 4. 提取隐性判断

窗口蒸馏时，对每个脱敏场景逐个询问强模型：

- 行为差异首先出现在哪个决策点？
- 哪个可观察信号会切换策略、停止或上抛？
- 最像成功的失败状态是什么，如何识别？
- 默认规则在哪些条件下应被违反？

轨迹蒸馏时，围绕已有事件回答相同问题，并比较成功与失败轨迹。不要让模型“一次写完整指令体系”；那会掩盖证据和规则之间的映射。

## 5. 生成 judgment packet

每条规则使用以下结构：

```yaml
judgment_rule:
  rule_id:
  scenario:
  observable_signal:
  default_action:
  exception:
  stop_or_escalate:
  evidence_refs: []
  confidence:
  open_questions: []
```

规则不得包含源材料中的秘密值或大段原文。`confidence` 由证据数量、结果可观察性和反例覆盖决定；单一无结果片段不能标 high。

## 6. 去除泛化废话

逐条运行三关，并记录被删除的 `rule_id` 与原因：

1. 反转测试：反过来说若明显荒谬，原句通常没有信息量。
2. 新手测试：无该领域经验的合格工程师也会自然做到，则不值得蒸馏。
3. 可违反测试：无法构造一个可观察的违反场景，则规则太抽象。

规则通过三关仍需具备 `observable_signal`、`exception` 和 `stop_or_escalate`；缺一项就返回提取阶段，不用“按情况判断”填空。

## 7. 逐规则归属复核与实现交接

把通过前置重叠审计和三关过滤的 packet 交给 `skill-audit`，要求它对每条规则复核：`existing_owner`、`coverage`、`recommended_home`。完整覆盖的规则删除；部分覆盖的规则优先更新原 skill；只有明确无归属的高信号规则才进入新 skill brief。

用户要求可加载 skill 时，再调用 `skill-creator`：

1. 以通过审计的 packet 为输入，不重新发明规则。
2. 用本 `SKILL.md` 所在目录下的 `evals/evals.json` 作为最低测试集（从 skill 根解析，不从当前仓库根解析），并为目标领域增加真实、脱敏场景。
3. 同时运行 with-skill 和 baseline/old-skill，对比可观察行为，不以“文字更好看”判定成功。
4. 高影响工作流再交给 `skill-lifeguard` 检查负例、checkpoint、done condition、replay hook 和 drift signal。

## 8. 模型升级后的重蒸馏

来源强模型或日常目标模型升级时，不直接覆盖旧 packet 或 skill。先复用原先获准的 `source_scope`、场景清单、`decision_event` 和 eval；新增证据仍需单独批准。把旧版和候选新版并列保存，并记录可验证的来源标签、模型版本和日期；未知字段留空。

按稳定的 `rule_id` 做逐条 diff；旧版没有稳定 ID 时，使用 `scenario` + `observable_signal` 对齐。每条差异标为 `unchanged`、`refined`、`added` 或 `removal_candidate`，并附证据、行为影响和未决问题。diff 只是审计产物，不自动证明新版更好，也不授权删除或覆盖。

- 来源强模型升级：用同一批脱敏场景重新逐场景 elicitation；新增或改变的规则仍需通过证据、三关过滤和重叠审计。
- 日常目标模型升级：在新目标模型上同时运行 baseline、旧 skill 和候选 skill。只有 baseline 已在真实场景和近边界负例中稳定具备某条行为时，才可把该规则标为 `removal_candidate`。
- 交付更新：把 diff 和 eval 结果交给 `skill-audit` / `skill-creator`；经用户确认后更新原 owner，不另建同场景 skill。保留旧版本或 commit 作为 rollback，不自动删除历史产物。

## Done When

`packet_only` 仅在以下条件全部满足时完成：

- `source_scope` 已记录，所有读取和外部发送均在批准范围内。
- 输出不含原始秘密、个人数据、客户数据或大段轨迹原文。
- 每条保留规则都能追溯到至少一个 `decision_event`，并具有信号、默认动作、例外和停止/上抛条件。
- 三关删除记录存在，未知信息留空或列入 `open_questions`。
- `skill-audit` 已给出保留、更新现有 skill 或不创建的归属结论。

`skill_delivery` 还必须满足：

- `skill-creator` 的真实 with-skill/baseline eval 已运行并保存结果。
- 至少一个近边界负例证明普通流程请求不会误用本 skill。
- 如由模型升级触发，旧版/候选版逐规则 diff 已保存；目标模型上的 baseline、旧 skill、候选 skill 结果支持每个删除或修改决定，并记录 rollback。
- registry/质量/测试命令按目标仓库要求 fresh 通过；无法运行的检查明确标记 blocker。

## Gotchas

- 扫描整个 home 目录不是“场景发现”，而是未经授权的数据扩大；改为批准范围内的元数据优先检索。
- “来自某强模型”不是证据。没有 decision event 和 outcome 的内容只能是待测假设。
- 新建文件比更新旧文件更容易，但 overlap high 时必须更新现有 owner。
- 构造任务常会迎合规则；eval 至少包含真实脱敏任务和一个容易误触发的近边界请求。
