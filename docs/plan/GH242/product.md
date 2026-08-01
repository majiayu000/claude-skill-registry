# GH242 产品规格：failure-aware plugin discovery 与 coverage ratchet

关联 issue: https://github.com/majiayu000/claude-skill-registry-core/issues/242
基线: `51b5acb069b41fceed343b4b04d42b2f0811f09f`
状态: `Approved for implementation by implx auth_mode:auto`

## 背景与问题

当前 plugin discovery 把 npm/GitHub 的 nonzero、timeout、malformed JSON 与 API failure 折叠
成 `[]`/`None`，最终会把“来源不可用”误报成“No plugin candidates”。plugin source/index loader
也会把 malformed file 当作空列表，使已发布 catalog 静默缺失。现有 CI 仅要求全局 line coverage
不低于 50%，无法证明这些关键 failure branches 被执行，也无法阻止 changed code 无测试。

## 目标

- 让每个 discovery source 的成功、缺失和失败可区分、可定位、可机器读取。
- 用稳定 `complete|partial|failed` 状态和退出码阻止故障结果覆盖可信输出。
- 允许维护者显式接受 partial，但在终端和 JSON report 中永久保留该事实。
- malformed plugin source/index fail closed，仅真正 optional 且缺失的输入允许 fallback。
- 对两个核心模块和所有关键失败分支建立可持续 coverage proof。
- 将全局 coverage 固定为不回退 baseline，并要求 changed-line coverage ≥80%。

## 非目标

- 不改变 plugin 候选评分、最低 skill 数、npm queries、top-30 registry 上限或排序。
- 不把网络/API 失败重试、缓存、GitHub App authentication 纳入本 issue。
- 不新增 discovery source，不自动修改 `sources/plugins.json`。
- 不触发真实 npm/GitHub discovery run，也不发布生成物。
- 不因 coverage 门禁而排除 production files、标记虚假 `pragma: no cover` 或弱化测试。

## 可观察行为不变量

1. `GH242-INV-01`：npm/GitHub 的 nonzero exit、timeout、malformed JSON、invalid response shape
   和 API failure 必须产生 typed、source-scoped error，至少包含稳定 `source`、`operation`、
   `kind` 与无 secret 的 `subject`；不得 broad-except 后返回空 list/string/structure。
2. `GH242-INV-02`：每次 CLI run 必须得到唯一稳定状态：所有 attempted source units 成功或
   documented optional-missing 为 `complete`；成功与错误并存为 `partial`；没有任何可信成功
   unit 或 authoritative input 无法读取为 `failed`。`complete` 可以有零候选，不能仅凭候选数
   推断状态。
3. `GH242-INV-03`：退出码固定为 `complete=0`、默认 `partial=2`、`failed=1`；
   `--allow-partial` 只把 `partial` 改为退出 0，不能允许 `failed`，也不能隐藏原状态。
4. `GH242-INV-04`：JSON output 是带 `schema_version`、`status`、`allow_partial`、`candidates`、
   per-source outcomes 与 typed `errors` 的 report；terminal summary 稳定输出 status/candidate/
   error counts。partial report 必须明确标记，不能输出成与 complete 相同的 bare candidate list。
5. `GH242-INV-05`：complete output 与显式允许的 partial output 必须经同目录临时文件原子替换。
   默认 partial、failed、serialization/write failure 均保持已有 output byte-for-byte 不变，且不
   留下会被后续读取的临时文件。
6. `GH242-INV-06`：存在但 JSON 损坏、top-level 非 object、`plugins` 非 list 或 plugin item
   shape 非法的 source/index 必须抛 typed error；禁止退化为空列表或 fallback 到较旧来源。
7. `GH242-INV-07`：optional-missing 只适用于文档明确列出的边界：尚不存在的 existing-plugin
   exclusion file、未提供/缺失的 optional registry enrichment，以及 source-first index chain 中
   缺失的 optional source。存在但为空的有效 source 是权威空集合，不能触发 stale fallback。
8. `GH242-INV-08`：npm query、npm view、repo metadata、repo tree、package content、registry
   parse 与 output write 的 complete/partial/failed 分支都有 deterministic tests；所有
   `GH242-INV-01` failure kinds 至少各有一个直接测试，关键 failure functions 达到 100% line
   与 branch coverage。
9. `GH242-INV-09`：`scripts/discover_plugins.py` 与 `scripts/plugin_index.py` 各自达到至少 80%
   line coverage；CI 读取机器生成 coverage report 验证，不能用合并后的平均值掩盖单模块不足。
10. `GH242-INV-10`：CI 的 global line coverage 不低于存档的 origin/main baseline，baseline
    在后续 PR 中只能持平或提高；相对 merge base 的 changed executable lines coverage ≥80%。
    任一 coverage gate 失败都阻止 PR，不得以 CLI `--cov-fail-under=50` 覆盖更严格配置。

## 验收场景

| 场景 | 预期结果 | 覆盖 |
| --- | --- | --- |
| 所有 sources 成功但没有候选 | `complete`, exit 0，可原子写空 candidates report | `INV-02`, `INV-05` |
| 一个 npm query timeout，其余 source 成功 | `partial`, 默认 exit 2，旧 output 不变 | `INV-01`–`INV-05` |
| 同一 partial run 加 `--allow-partial` | exit 0，report 仍标 `partial`/`allow_partial: true` | `INV-03`, `INV-04` |
| 所有远程 units 失败 | `failed`, exit 1，`--allow-partial` 无效 | `INV-02`, `INV-03` |
| `sources/plugins.json` 存在但 malformed | typed error，不能 fallback 到 registry | `INV-06`, `INV-07` |
| plugin source 合法且 `plugins: []` | 权威空集合，不读取 stale registry plugins | `INV-07` |
| changed discovery error branch 无测试 | module/critical/changed-line gate 至少一个失败 | `INV-08`–`INV-10` |

## 完成条件

`GH242-INV-01` 至 `GH242-INV-10` 全部有 fresh deterministic evidence；实现不得降低既有
global baseline 或通过排除文件伪造 coverage。合并仍须通过独立 reviewer、当前 CI、review
threads、merge state 与 PR gate；真实 discovery/publish 仍由 maintainer 受控执行。
