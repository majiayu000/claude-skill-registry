# GH241 产品规格：以生成物强制执行 static artifact API v1

关联 issue: https://github.com/majiayu000/claude-skill-registry-core/issues/241
契约: `static-artifact-api-v1`
基线: `51b5acb069b41fceed343b4b04d42b2f0811f09f`
状态: `Approved for implementation by implx auth_mode:auto`

## 背景与问题

当前 `docs/artifact-api-contract.md` 描述了 pointer、manifest、shard/part，但实际生成物的
字段并不统一：部分 pointer 缺少 `schema_version`、`replacement`、`compat_since`，count
同时使用 `t`、`count`、`total_count`；search shard 实际 payload 是 `s`，文档却写为
`skills`。现有门禁主要检查文档关键词和文件大小，无法阻止 schema、引用、count、bytes 或
hash 漂移进入 Pages 或 merged main。

## 目标

- 让 `static-artifact-api-v1` 成为可被机器校验的发布契约，而非说明性文本。
- 统一 compatibility pointer 与 canonical count，保留兼容别名时给出明确窗口。
- 对 pointer → manifest → shard/part 的结构、引用和内容完整性 fail closed。
- 让 Web reader 对已声明 shape 明确解析，对未知或损坏 shape 明确失败。
- 在 Core Pages 与 merged main 两条发布路径上传前阻止不一致生成物。

## 非目标

- 不改变分片策略、排序、尺寸上限、stable skill id 或公开 URL。
- 不重新设计 skill、quality、security、ranking record 的业务字段。
- 不直接修改 `claude-skill-registry` 的 generated outputs，也不修改 data archive。
- 不在本次实施中触发真实 Pages deploy 或 main publish。
- 不要求历史消费者立刻停止读取已文档化的兼容别名。

## 可观察行为不变量

1. `GH241-INV-01`：每个 compatibility pointer 必须是 JSON object，且包含有效的
   `schema_version`、`deprecated_full_payload: true`、非空 `message`、`manifest`、
   `replacement`、`compat_since` 和非负整数 `total_count`；需要公布终止窗口时支持
   `compat_until`，pointer 不得包含完整 `skills`、`records` 或 `s` payload。
2. `GH241-INV-02`：`total_count` 是 pointer 与 manifest 的 canonical count。`t`、`count`、
   `registry_skill_count_dedup` 等兼容别名只可出现在契约明确列出的 artifact/window 中，且值
   必须与 `total_count` 相等；未知 count alias 或冲突值必须失败。
3. `GH241-INV-03`：V1 full-search shard 的唯一 payload key 是 `s`；lite search 的 payload
   key 是 `skills`。Web reader 遇到未知 top-level、manifest、entry 或 shard payload shape，
   以及缺失必填字段时必须抛出可见错误，不能猜测字段、替换为空数组或继续部分展示。
4. `GH241-INV-04`：每个 manifest 的 `total_count` 等于其 entry `count` 之和；
   `shard_count`/`part_count` 等于 entry 数量；每个 shard/part 自报 `count` 等于实际 payload
   长度，identity、payload key 与所属 artifact 类型一致。
5. `GH241-INV-05`：manifest/pointer 中的每个相对 path 必须规范化后仍位于 publish root、
   指向存在的常规文件且没有重复引用；entry 的 `bytes`、`gzip_bytes`、`sha256` 必须与磁盘
   内容一致，gzip 必须可解压且 JSON 内容与对应 plain artifact 等价。
6. `GH241-INV-06`：任何明确声明代表同一集合的 artifacts 必须报告相同 canonical count。
   至少 `registry_summary.json`、`registry-manifest.json`、`registry.json` pointer 与
   `stats.json.registry_skill_count_dedup` 的 deduplicated registry count 必须一致；search/category
   scan set、signal/lite dedup set 分别做组内一致性校验，不得把不同集合强行比较。featured
   subset、archive raw counts 和 plugin count 不参与 registry dedup 相等约束。
7. `GH241-INV-07`：validator 必须收集并报告所有可安全继续检查的错误，最终以非零退出；
   缺失、无效 JSON、类型错误、未知 schema/version/shape、path escape、count/size/hash 不一致
   都是 blocking error，不允许 warning + fallback。
8. `GH241-INV-08`：deterministic tests 必须用 production generator/writer 在临时目录生成
   fixture，证明合法最小集合通过，并分别篡改 schema、pointer、payload key、count、path、
   bytes、hash 与 gzip 内容证明失败；只检查源码关键词不算生成物契约证据。
9. `GH241-INV-09`：Core `build-index` 必须在 Pages artifact upload 前运行 validator；merged
   main rebuild 必须在同步结束前、任何发布提交之前运行同一 validator。任一失败都阻止后续
   upload/publish，且不得删除或弱化现有 security、canonical-category 与 size gates。
10. `GH241-INV-10`：公开文档必须准确区分 pointer、manifest、search `s`、lite `skills`、
    signal `records`、category/registry `skills`，并列出 count alias 的 artifact、canonical
    对应关系和兼容窗口；generator、reader、validator 与文档必须在同一 PR 保持一致。

## 验收场景

| 场景 | 预期结果 | 覆盖 |
| --- | --- | --- |
| production writers 生成最小完整 fixture | validator 退出 0，所有引用和 totals 一致 | `INV-01`–`INV-06`, `INV-08` |
| shard 把 `s` 改为 `skills` 或未知字段 | validator 与 Web reader 均 fail closed | `INV-03`, `INV-07` |
| entry count/hash/path 任一漂移 | 明确列出 artifact/path/error code，退出非零 | `INV-04`, `INV-05`, `INV-07` |
| stats 与 registry/search totals 不同 | 上传前失败，不发布部分一致的数据 | `INV-06`, `INV-09` |
| 兼容 alias 与 `total_count` 冲突或已超出窗口 | 失败，不猜测哪个 count 正确 | `INV-02`, `INV-10` |

## 完成条件

`GH241-INV-01` 至 `GH241-INV-10` 全部有 fresh deterministic evidence；实施 diff 只修改
core authority 范围，且不包含 generated archive/main 数据。合并仍须通过独立 reviewer、当前
CI、review threads、merge state 与 PR gate。真实 publish/deploy 仍是 maintainer gate。
