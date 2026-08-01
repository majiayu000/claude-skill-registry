# GH241 技术规格：artifact API v1 generator/reader/validator 一致性

关联 issue: https://github.com/majiayu000/claude-skill-registry-core/issues/241
产品规格: `docs/plan/GH241/product.md`
基线: `51b5acb069b41fceed343b4b04d42b2f0811f09f`
状态: `Approved for implementation by implx auth_mode:auto`

## 当前根因与证据

1. `scripts/index_artifacts.py` 的 search pointer 缺 `schema_version`、`replacement`、
   `compat_since`、`total_count`；signal/category pointer 仍以 `count` 为主且同样缺契约字段。
2. `scripts/rebuild_registry.py::build_compatibility_registry()` 没有统一 pointer schema，且
   `manifest` 取决于调用 flag；merged publish 虽传 `--compat-manifest-pointer`，契约并未由
   validator 证明。
3. `docs/artifact-api-contract.md` 声称 search shard payload 是 `skills`，实际
   `write_search_artifacts()` 写 `s`。
4. `docs/js/app.js::loadShardedSearchIndex()` 对缺失 `shards`/`s` 使用 `|| []`，会把未知或
   损坏 shape 静默解释成空结果；`normalizeSearchIndex()` 还会基于字段存在猜测 shape。
5. `scripts/check_category_artifacts.py` 只验证 category pointer 标记、manifest 存在和尺寸；
   `tests/test_pipeline_contracts.py` 只搜索文档关键词/step 顺序，未读取生成 fixture。
6. `.github/workflows/build-index.yml` 与 `scripts/sync_main_repo.sh` 在 upload/publish 前均没有
   pointer/manifest/shard 的 schema/count/path/hash 全链路校验。

## 技术设计

### 1. 统一 V1 writer schema

- 在 `scripts/index_artifacts.py` 中集中构造 compatibility pointer，避免 search、signal、
  category 各自复制字段。所有 pointer 写：`schema_version: 1`、`total_count`、
  `deprecated_full_payload`、`message`、`manifest`、`replacement`、`compat_since`；仅契约表
  允许的旧 alias 可保留，且必须等于 `total_count`。
- search manifest/shard 保留已发布的 `s`；signal 使用 `records`；category/registry 使用
  `skills`。manifest 全部以 `total_count` 为 canonical，category 原 `count` 作为窗口内 alias。
- `scripts/rebuild_registry.py` 使用相同 pointer contract；merged rebuild 必须提供 manifest。
  Core-only 不能同树发布 manifest 的模式仍可生成 summary，但不得作为完整 V1 publish set
  通过 validator。
- `scripts/build_search_index.py` 继续写 raw/archive diagnostics；对 dedup set 的统计字段以
  `total_count` 为来源，禁止通过 `len(...)` 掩盖上游 count 冲突。

### 2. Reader 显式判别并 fail closed

- `docs/js/app.js` 为 lite document、V1 pointer、V1 search manifest、entry 和 search shard
  分别做 exact required-field/type 检查。
- 仅 `schema_version == 1` 且 payload key 与声明类型匹配时读取。`manifest.shards`、entry
  `path`、shard `s`、各层 count 不得用 `|| []`、`|| skills.length` fallback。
- 允许的 legacy full-search document 必须匹配文档明确列出的 legacy shape；其它 object、
  array、未知 schema/version 或混合 shape 抛出 `Unsupported ... schema`，由现有 init error UI
  显示。startup 从 lite 到 legacy URL 的网络 fallback 保留，但 schema 错误不得在同一 artifact
  内降级成空数据。

### 3. 新增独立 validator

新增 `scripts/check_artifact_api.py`，CLI 以 `--root` 定位 merged/core artifact root，并以
`--docs-dir`（默认 `<root>/docs`）定位 Pages artifacts。validator 不导入 generator 的 shape
常量，避免 writer 与 checker 同错；V1 schema/allowed aliases 在 checker 中显式定义。

校验分层：

1. 安全加载 JSON，验证 object/required keys/exact schema、integer 范围与未知 payload key。
2. 从固定 public entrypoints 遍历 pointer → manifest → entries；引用必须是 POSIX 相对路径，
   `resolve()` 后仍在 root，且不允许 symlink、absolute path、`..` escape 或重复 path。
3. 对每个 plain/gzip artifact 校验 existence、regular file、bytes/gzip_bytes、SHA-256；解压
   gzip 后解析 JSON，并与 plain JSON 做结构等价比较。
4. 依据 artifact 类型验证 `s`/`records`/`skills`、identity、payload length、entry count、
   entry 数量与 manifest count；错误使用稳定 code 并尽可能继续收集。
5. 按集合语义分组汇总 totals：registry pointer/summary/manifest 与
   `stats.registry_skill_count_dedup` 为 registry dedup group；search/category 为 scan group；
   signal/lite 为 stable-id dedup group。只比较同组 totals，任一缺失、类型错误或组内不相等
   都失败。optional artifact 不以“缺失即跳过”处理：V1 public entrypoint 集合必须完整；只有
   明确的 execution profile 可缩小范围，本 issue 不新增 profile。

CLI 输出简短 summary；可选 `--output-json` 保存包含 `schema_version`、checked counts 与 errors
的报告。错误不得包含文件内容或 secret，仅包含稳定 code、相对 path 和说明。

### 4. Production-generated fixture tests

新增 `tests/test_check_artifact_api.py`：

- 调用 `write_search_artifacts()`、`write_signal_artifacts()`、
  `write_category_artifacts()`、`write_registry_shards()`、`build_registry_manifest()` 与
  `build_compatibility_registry()` 在 `tmp_path` 生成最小完整 V1 tree；补充 lite/stats/summary
  使用 production serialization helper，不复制 hand-authored pointer/manifest golden files。
- happy path 断言 validator 退出 0；参数化 mutation 在生成后只篡改一个事实，覆盖 unknown
  schema/shape、alias conflict、manifest/shard/actual count、path escape/missing/duplicate、
  bytes/hash、gzip mismatch 和 cross-artifact total。
- 单独的 JS contract test 证明 reader 不再包含 manifest/shard 的 `|| []` 猜测路径，并通过
  Node harness（若仓库现有 CI runtime 可用）或导出 pure normalizer fixtures 验证未知 shape
  抛错；不可仅依赖字符串存在断言。

### 5. 发布门禁接入

- `.github/workflows/build-index.yml`：在生成、size/category/canonical checks 后、
  `actions/upload-pages-artifact` 前执行 validator；workflow path trigger 包含 validator 及其
  直接契约依赖。
- `scripts/sync_main_repo.sh`：registry summary、search/signal、canonical、size/category checks
  完成后执行同一 validator，再进入 notices/外层 commit。validator 失败沿 `set -e` 阻止发布。
- 保留现有 security、canonical category、size、category guards；新 validator 不替代其政策。
- `tests/test_pipeline_contracts.py` 验证两个入口中的顺序与 fail-closed invocation，但核心
  schema 证据来自真实 fixture tests。

## 影响文件与所有权

| 文件 | 计划变更 |
| --- | --- |
| `docs/artifact-api-contract.md` | 修正文档 shape、canonical count 与 alias/window 表 |
| `scripts/index_artifacts.py` | 统一 Pages pointer/manifest writer |
| `scripts/rebuild_registry.py` | 统一 registry pointer 与 manifest contract |
| `scripts/build_search_index.py` | 对齐 dedup count/stats 输出 |
| `docs/js/app.js` | V1 reader 显式校验、未知 shape fail closed |
| `scripts/check_artifact_api.py` | 新增全链路 validator CLI |
| `tests/test_check_artifact_api.py` | production-generated fixture 与 mutation tests |
| `tests/test_pipeline_contracts.py` | reader/workflow 门禁顺序 contract tests |
| `.github/workflows/build-index.yml` | Pages upload 前执行 validator |
| `scripts/sync_main_repo.sh` | merged main rebuild 后执行 validator |

不修改 generated `docs/*.json`、`registry*.json`、`registry-shards/**`、data repo 或 main repo。

## 不变量映射

| 产品不变量 | 实现区域 | Deterministic evidence |
| --- | --- | --- |
| `INV-01`, `INV-02` | writer、contract、validator | pointer fixture + alias mutations |
| `INV-03` | contract、`docs/js/app.js`、validator | valid/unknown search shape tests |
| `INV-04`, `INV-05` | validator traversal | count/path/bytes/hash/gzip mutations |
| `INV-06` | validator total aggregator | one-at-a-time cross-total mutations |
| `INV-07` | validator report/CLI | multi-error report + nonzero exit tests |
| `INV-08` | production writer fixture | test asserts writers created fixture before mutation |
| `INV-09` | workflow/sync script | gate ordering contract tests |
| `INV-10` | contract + all above | field/payload/alias matrix test |

## 兼容、迁移与回滚

- Public paths 与 record payload 不变；`total_count` 是 additive canonical field。旧 `t`、
  `count`、`registry_skill_count_dedup` 仅按 contract alias table 保留到
  `compat_until: static-artifact-api-v2`，V1 validator 要求其与 canonical 值相等。
- reader 仍接受明确文档化的 lite/legacy full shape，但停止接受损坏 manifest/shard；这会把
  过去的空结果变成显式错误，是预期修复。
- 首次启用 gate 若暴露现存生成器漂移，应修 writer/contract 后重新生成；不得 allowlist
  当前坏 fixture 或将 error 降为 warning。
- 回滚应整体 revert writer/reader/validator/gate commit；不得只移除 gate 而保留新 schema，
  也不得手改 main generated outputs。已发布旧 V1 URL 不变，无数据迁移或 force push。

## 风险

- 全量 hash/gzip 校验增加 publish 时间；fixture benchmark 与 CI timing 需记录，必要时优化流式
  I/O，不能跳过文件。
- Core 与 merged root 的引用基准不同容易造成误判；测试必须覆盖 `docs/**` 与 root-level
  registry 两种 namespace。
- cross-total 只适用于明确定义的同一 set；scan、stable-id dedup、registry dedup、raw archive、
  featured subset 与 plugin count 必须分组或显式排除，不能靠数值偶然相等推断语义。
- JS 测试环境若不能导入 browser script，应先最小拆分 pure validator，不引入新 bundler。

## Deterministic checks

```bash
python -m pytest -q tests/test_check_artifact_api.py
python -m pytest -q tests/test_pipeline_contracts.py
python -m pytest -q
ruff check scripts/check_artifact_api.py scripts/index_artifacts.py \
  scripts/rebuild_registry.py scripts/build_search_index.py tests/test_check_artifact_api.py
git diff --check
```

本次 `implx auth_mode:auto` invocation 已授权实施；合并仍须满足独立 reviewer、当前 CI、
review threads、merge state 与 PR gate。真实 Pages/main publish dispatch 不在实施授权内。
