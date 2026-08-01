# GH241 任务计划

关联 issue: https://github.com/majiayu000/claude-skill-registry-core/issues/241
产品规格: `docs/plan/GH241/product.md`
技术规格: `docs/plan/GH241/tech.md`
状态: `Approved for implementation by implx auth_mode:auto`

## 执行边界

- 共享 generator/validator/test 文件采用单一顺序 `implementation_lane`，不并行写同一文件。
- 本次授权允许实施 `SP241-T1` 至 `SP241-T4` 并形成 PR；不允许修改 generated outputs、
  data/main repo、触发真实 publish/deploy 或绕过现有安全/尺寸/分类门禁。
- 每个任务完成后先运行 focused checks；最终必须经过独立只读 reviewer 和当前 PR gate。

## `SP241-T1`：锁定 V1 契约与统一 writers

- Owner: `implementation_lane`
- Dependencies: none
- Covers: `GH241-INV-01`, `GH241-INV-02`, `GH241-INV-03`, `GH241-INV-10`
- Files: `docs/artifact-api-contract.md`, `scripts/index_artifacts.py`,
  `scripts/rebuild_registry.py`, `scripts/build_search_index.py`
- 工作内容:
  1. 写清 payload/count/alias/window matrix，以 `total_count` 为 canonical。
  2. 集中构造 Pages pointers，并让 registry pointer 输出同一组必填字段。
  3. 保留公开 path 与 record shape；search shard 明确使用 `s`。
- Done when:
  - 六类 pointer 均满足 V1 required fields，不含完整 payload。
  - manifest/pointer 用 `total_count`；保留 alias 时值一致且 contract 有窗口。
  - writer 单元测试覆盖空集合与多 shard/part 集合。
- Verify:

```bash
python -m pytest -q tests/test_check_artifact_api.py -k 'writer or pointer'
ruff check scripts/index_artifacts.py scripts/rebuild_registry.py scripts/build_search_index.py
git diff --check
```

## `SP241-T2`：实现全链路 validator 与生成 fixture

- Owner: `implementation_lane`
- Dependencies: `SP241-T1`
- Covers: `GH241-INV-04`, `GH241-INV-05`, `GH241-INV-06`, `GH241-INV-07`,
  `GH241-INV-08`
- Files: `scripts/check_artifact_api.py`, `tests/test_check_artifact_api.py`
- 工作内容:
  1. 实现严格 JSON/schema、safe relative path、entry/shard、bytes/hash/gzip 校验。
  2. 按 registry dedup、search/category scan、signal/lite stable-id dedup 分组比较 totals。
  3. 用 production writers 在 `tmp_path` 生成完整 fixture，再参数化单点 mutation。
  4. 提供稳定 error code、简短 CLI summary 与 `--output-json`。
- Done when:
  - 合法 generated fixture 通过；schema/count/path/bytes/hash/gzip/total 漂移分别失败。
  - path escape、symlink、duplicate ref、未知 payload shape 失败且不读取 root 外内容。
  - 多个独立错误可在一个 report 中呈现，CLI 返回非零且不泄露内容。
- Verify:

```bash
python -m pytest -q tests/test_check_artifact_api.py
ruff check scripts/check_artifact_api.py tests/test_check_artifact_api.py
git diff --check
```

## `SP241-T3`：让 Web reader 与发布入口 fail closed

- Owner: `implementation_lane`
- Dependencies: `SP241-T1`, `SP241-T2`
- Covers: `GH241-INV-03`, `GH241-INV-07`, `GH241-INV-09`, `GH241-INV-10`
- Files: `docs/js/app.js`, `.github/workflows/build-index.yml`,
  `scripts/sync_main_repo.sh`, `tests/test_pipeline_contracts.py`
- 工作内容:
  1. 为 lite/pointer/manifest/entry/search shard 添加 exact shape/type/count 校验。
  2. 删除 manifest/shard 的 `|| []`、length/count guessing，未知 shape 抛可见错误。
  3. 在 Pages upload 与 merged main publish 前执行 validator，并补齐 workflow triggers。
  4. 添加 reader behavior 与 gate-order tests，保留现有 guards 的相对顺序。
- Done when:
  - reader 对有效 lite/V1 shard 返回相同用户数据，对未知/损坏 shape 明确抛错。
  - 两条 publish 路径都在最终 upload/publish 前 fail closed，现有 gates 未删除或弱化。
  - tests 证明调用顺序，而非只证明 validator 字符串存在。
- Verify:

```bash
python -m pytest -q tests/test_pipeline_contracts.py
python -m pytest -q tests/test_check_artifact_api.py
git diff --check
```

## `SP241-T4`：全量验证、性能证据与 PR handoff

- Owner: `implementation_lane`
- Dependencies: `SP241-T1`, `SP241-T2`, `SP241-T3`
- Covers: `GH241-INV-01` through `GH241-INV-10`
- Files: 无计划 production edit；仅测试/PR evidence
- 工作内容:
  1. 对 generated fixture 和当前 checkout artifacts 各运行一次 validator，记录数量与耗时。
  2. 运行 focused/full pytest、Ruff、diff/status 检查，确认无 generated output 被纳入 diff。
  3. 在 PR 映射 invariant → test，并交给独立只读 reviewer；不触发 live dispatch。
- Done when:
  - fresh checks 全部通过，validator runtime 适合 CI 且无跳过 shard/hash。
  - diff 仅含授权 core 文件；没有 data/main 直接变更、测试弱化或 warning fallback。
  - 当前 CI、review threads、merge state 与 PR gate 完整，live publish 留给 maintainer。
- Verify:

```bash
python scripts/check_artifact_api.py --root . --docs-dir docs
python -m pytest -q tests/test_check_artifact_api.py tests/test_pipeline_contracts.py
python -m pytest -q
ruff check scripts/check_artifact_api.py scripts/index_artifacts.py \
  scripts/rebuild_registry.py scripts/build_search_index.py tests/test_check_artifact_api.py
git diff --check
git status --short
```

## 追踪矩阵与 human gates

| 不变量 | Primary task | Final gate |
| --- | --- | --- |
| `INV-01`–`INV-03`, `INV-10` | `SP241-T1`, `SP241-T3` | `SP241-T4` |
| `INV-04`–`INV-08` | `SP241-T2` | `SP241-T4` |
| `INV-09` | `SP241-T3` | `SP241-T4` |

1. 实施授权已由 `implx auth_mode:auto` 满足。
2. 合并前必须有独立 reviewer 与当前 CI/review threads/merge state/PR gate evidence。
3. 真实 Pages deploy/main publish 由 maintainer 受控执行；本计划不授权 implementation agent
   dispatch，也不以本地 fixture 替代上线后验证。
