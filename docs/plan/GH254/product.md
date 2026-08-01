# GH254 产品规格：canonical taxonomy 展示层与分类准确率证据

关联 issue: https://github.com/majiayu000/claude-skill-registry-core/issues/254
基线: `1d307fd932e210e3d6066888c87d1761a557885b`
状态: `Approved for implementation by implx auth_mode:auto`
复杂度: `medium`

## 背景与问题

canonical taxonomy 已闭合为 42 个 active 类别，但 Pages 仍把 12 个旧类别码作为显示权威，
导致 full-record 与 mini-record 对新类别的归一化结果不一致。taxonomy 已声明可选 `parent`
报告关系，却没有任何实际 parent；现有分类抽样又是单一全局池，不能保证覆盖无关键词大类。

## 目标

- 让 42 类的 slug、code、display name 和 parent 由 taxonomy 单一来源驱动 Pages。
- 建立两层 reporting hierarchy，不移动 skill、不改变叶子分类和过滤语义。
- 为六个重点类别建立确定性分层样本及 fail-closed 人工准确率复核门禁。

## 非目标

- 不批量重分类 archive skill，不修改 data/main 仓库。
- 不给无关键词类别补虚假关键词，不把抽样建议自动应用为迁移。
- 不改变 category shard、search shard、安装路径或稳定去重键。
- 不把 `other` 比例当作准确率。

## 可观察行为不变量

1. `B-001`：发布侧必须输出完整 42 类 taxonomy sidecar；每项包含唯一 `slug`、唯一
   `code`、非空 `display_name` 和可选 `parent`，且 slug 与 code 可双向无损解析。
2. `B-002`：taxonomy sidecar 缺失、字段不闭合、计数不符、重复 slug/code、未知 parent、
   自 parent 或超过两层时，构建/Pages 必须显式失败，禁止静默回退为 `other`。
3. `B-003`：taxonomy 必须形成 12 个顶层类别和一层子类别；`parent` 只影响报告与显示，
   不继承计数、不移动 archive、不改变叶子过滤结果。
4. `B-004`：Pages 对 canonical slug 或 code 输入返回同一个 canonical code；非空未知输入
   必须保留为可见原值，只有空输入才使用 taxonomy default。
5. `B-005`：分类质量样本必须按固定 seed、固定 quota 分层覆盖
   `integration`、`domains`、`skills`、`context-management`、`data`、`development`；
   输入遍历顺序变化不得改变成员、分层 digest 或总 digest。
6. `B-006`：每条样本必须记录路径、当前类别、bounded 语义摘录、语义来源、SKILL.md
   SHA-256 和 metadata SHA-256；源文件变化后旧复核证据必须失效。
7. `B-007`：任一目标类别人口不足、样本缺失、重复复核、digest/hash 不匹配、expected
   category 非 canonical 或准确率低于阈值时，复核门禁必须失败；不得静默缩减 quota。
8. `B-008`：抽样和复核均为审计证据，不得自动修改 taxonomy、metadata 或 skill 路径；
   既有 canonical publish/security/intake 行为保持兼容。

## Boundary checklist

| 边界 | 结论 |
| --- | --- |
| Empty / missing input | covered: `B-002`, `B-004`, `B-007` |
| Error and failure paths | covered: `B-002`, `B-007` |
| Authorization / permission | N/A：本变更只生成和验证本地/Pages 数据，不新增权限路径 |
| Concurrency / ordering | covered: `B-005` |
| Retry / idempotency | covered: `B-005`, `B-006` |
| Illegal state transitions | covered: `B-002`, `B-007` |
| Compatibility / migration | covered: `B-003`, `B-008` |
| Degradation / fallback | covered: `B-002`, `B-004` |
| Evidence and audit integrity | covered: `B-005`, `B-006`, `B-007` |
| Cancellation / partial completion | N/A：命令是可重复执行的离线确定性检查 |

## 完成条件

`B-001` 至 `B-008` 均有 fresh deterministic tests；完整 pytest、lint、独立 reviewer、
当前 CI、review threads、merge state 与 PR gate 全绿后才可合并。
