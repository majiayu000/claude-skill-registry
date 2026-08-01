# GH242 技术规格：typed discovery outcomes 与 coverage proof

关联 issue: https://github.com/majiayu000/claude-skill-registry-core/issues/242
产品规格: `docs/plan/GH242/product.md`
基线: `51b5acb069b41fceed343b4b04d42b2f0811f09f`
状态: `Approved for implementation by implx auth_mode:auto`

## 当前根因与证据

1. `scripts/discover_plugins.py::npm_search()`、`npm_view()` 和 `gh_api()` 捕获任意 exception，
   将 subprocess nonzero、timeout、JSON error 统一变成 `[]`/`None`。
2. `inspect_repo_structure()` 对 metadata/tree 缺失或 malformed 返回预填空 structure，后续被
   `score_candidate()` 当作“repo 没有 plugin signals”，丢失 source failure。
3. `discover_from_npm()`/`discover_from_registry()` 只返回 candidates，没有 source outcomes；
   `main()` 以 candidates 为空决定“No plugin candidates”并以成功返回。
4. CLI output 直接写目标文件，不是 atomic；partial/failed 没有状态，也无法保护上次有效输出。
5. `scripts/plugin_index.py` 两个 loader broad-except 返回 `[]`；valid empty 与 missing/malformed
   无法区分。`scripts/rebuild_registry.py::load_plugins()` 复制了同一 silent fallback。
6. `.github/workflows/python-tests.yml` 安装 pytest-cov 后只运行
   `python -m pytest -q --cov-fail-under=50`；`pyproject.toml` 未记录 baseline、module target 或
   changed-line gate。现有 `tests/test_plugin_contract.py` 不覆盖 discovery/failure loaders。

## 技术设计

### 1. Typed source outcomes

在 `scripts/discover_plugins.py` 增加小型 typed model：

- `DiscoveryError`: `source`, `operation`, `kind`, `subject`, `message`；`kind` 固定为
  `nonzero_exit|timeout|malformed_json|invalid_shape|api_failure|read_error|write_error`。
- `SourceOutcome`: source unit id、`success|optional_missing|error`、candidate count 与 errors。
- `DiscoveryReport`: `schema_version: 1`、`status`、`allow_partial`、sorted candidates、outcomes、
  errors。只保存 bounded/sanitized stderr 摘要，不保存 command environment、token/header 或响应体。

subprocess 始终使用 argument list。`npm_search()`、`npm_view()`、`gh_api()` 在 failure 上抛
`DiscoveryError`，只在成功且 schema 合法时返回 typed payload。`inspect_repo_structure()` 不再
预填空结构掩盖 metadata/tree error；真实成功的空 tree 才返回空 signals。

### 2. 聚合状态与 CLI 语义

- 每个 npm query、package view、GitHub metadata/tree/content 与 registry parse 都记录 outcome；
  expected filtering（无 repo、无 bin、score 低）是成功 unit 的业务结果，不是 error。
- status reducer 只看 outcomes：零 error 为 `complete`；至少一 success 且至少一 error 为
  `partial`；无 success 或 authoritative exclusion input error 为 `failed`。`optional_missing`
  不计 success，也不计 error。
- exit code：`complete=0`、`partial=2`、`failed=1`；`--allow-partial` 仅令 partial 返回 0。
- terminal 最后一行稳定输出 `status=<...> candidates=<n> errors=<n> allow_partial=<bool>`；
  typed errors 写 stderr，candidate detail 保留现有可读输出。

### 3. Atomic report 与 optional-missing 边界

`--output` 改写 `DiscoveryReport` envelope。先在目标同目录创建唯一临时文件，serialize、flush、
`fsync` 后 `Path.replace()`；异常清理 temp 并抛 `write_error`。规则：

- complete：原子发布 report；零 candidates 也发布。
- partial：默认不写；仅 `--allow-partial` 原子发布并保留 `status: partial`。
- failed：永不写，即使带 `--allow-partial`。
- 任一不写路径都断言原 target bytes/hash 未变化。

明确 optional boundary：

1. discovery 的 existing-plugin exclusion file 尚不存在时是 documented optional empty set；
   文件存在但 malformed/invalid shape 是 authoritative failure。
2. `--npm-only` 不 attempt registry；普通模式下缺失 registry enrichment 是
   `optional_missing`，存在但 malformed 为 source error。
3. index build 的 `sources/plugins.json` 缺失时可尝试 registry fallback；source 合法且
   `plugins: []` 时返回 present-empty，不 fallback。registry 缺失则表示没有 optional plugin
   data；存在但 malformed 必须失败。

### 4. Strict plugin index API

在 `scripts/plugin_index.py` 增加 `PluginIndexError(source, kind, path, message)` 与能区分
`missing`/`present` 的 load result。loader 校验 top-level object、`plugins` list 和每个 item 至少
具有非空 string `name`、`repo`；I/O/JSON/shape error 均抛错。

`build_plugins_index()` 先验证并序列化到同目录 temp，再 atomic replace；valid empty list 也写
`count: 0, plugins: []`，避免旧 `plugins.json` 残留。`scripts/rebuild_registry.py` 删除重复 loader，
复用 strict source loader；`scripts/build_search_index.py` 仅在 result 为 missing 时 fallback，
不会用 truthiness 把 present-empty 当 missing。

### 5. Coverage ratchet

- 新增 `coverage-baseline.json`，记录从 clean `origin/main` fresh full suite 得到的 exact
  `global_line_percent`、采样 commit 和 schema。实施 PR 首次创建 baseline 时使用基线 commit，
  不用 PR 新增测试抬高后反推旧 baseline。
- 新增 `scripts/check_coverage_ratchet.py`：读取 `coverage.json`，要求当前 global ≥ stored
  baseline、`discover_plugins.py` ≥80%、`plugin_index.py` ≥80%；读取 coverage.py branch arcs 与
  AST function ranges，要求列入 `critical_functions` 的 failure functions无 missing lines/arcs。
- checker 用 `git show origin/main:coverage-baseline.json`（文件存在时）证明 baseline 未降低；
  初次引入时验证 recorded commit 是 merge base/ancestor 且 measurement evidence 由 CI 生成。
- `pyproject.toml` 保持 `branch = true`，生成 term、XML、JSON reports；不通过新增 omit/exclude 或
  `pragma: no cover` 达标。
- changed-line 使用 `diff-cover coverage.xml --compare-branch=origin/main --fail-under=80`；CI
  checkout `fetch-depth: 0`，安装固定 major 的 `diff-cover`，保证 merge base 可解析。
- 全局 gate 不再由 workflow 的 `--cov-fail-under=50` 覆盖；baseline checker 是唯一 global
  ratchet authority。`tests/test_pipeline_contracts.py` 锁定 checkout、reports、module/critical、
  baseline 与 diff-cover gates。

## 测试设计

新增 `tests/test_discover_plugins.py`：以 fake subprocess/result 覆盖 npm/GitHub success、nonzero、
timeout、malformed JSON、invalid shape；覆盖 mixed/all-failed reducer、zero-candidate complete、
`--allow-partial`、exit codes、sanitized errors 与 output preservation/atomic replace。

新增 `tests/test_plugin_index.py`：覆盖 source/registry missing、valid empty、valid plugins、malformed
JSON、wrong top-level/list/item shape、read error、atomic empty/nonempty write 与 serialization/write
failure preservation。新增 `tests/test_check_coverage_ratchet.py` 验证 baseline/module/critical/current
coverage pass/fail 和 baseline-lowering rejection。测试不得调用真实 npm/GitHub。

## 影响文件

| 文件 | 计划变更 |
| --- | --- |
| `scripts/discover_plugins.py` | typed errors/outcomes、status、CLI、atomic report |
| `scripts/plugin_index.py` | strict loaders、missing/present boundary、atomic writer |
| `scripts/rebuild_registry.py` | 复用 strict plugin source loader |
| `scripts/build_search_index.py` | source missing 与 present-empty 分流 |
| `scripts/check_coverage_ratchet.py` | global/module/critical coverage checker |
| `coverage-baseline.json` | origin/main global coverage baseline |
| `pyproject.toml` | coverage reports 与 dev dependency |
| `.github/workflows/python-tests.yml` | full history、coverage/ratchet/diff-cover gates |
| `tests/test_discover_plugins.py` | discovery failure/status/output tests |
| `tests/test_plugin_index.py` | strict loader/writer tests |
| `tests/test_check_coverage_ratchet.py` | ratchet checker tests |
| `tests/test_pipeline_contracts.py` | CI coverage contract tests |

## 不变量映射

| 产品不变量 | 实现区域 | Deterministic evidence |
| --- | --- | --- |
| `INV-01` | typed adapters | subprocess/API error matrix |
| `INV-02`, `INV-03` | reducer/CLI | complete/partial/failed + exit tests |
| `INV-04`, `INV-05` | report/atomic writer | schema + byte-preservation tests |
| `INV-06`, `INV-07` | strict index/load results | malformed/missing/present-empty tests |
| `INV-08`, `INV-09` | direct tests + critical checker | module/branch coverage report |
| `INV-10` | baseline checker + diff-cover | CI contract and synthetic report tests |

## 兼容、迁移、风险与回滚

- `--output` 从 bare list 变为 versioned report 是有意契约修正；仓库内无已声明 consumer。若发现
  consumer，实施时新增显式 `--output-format legacy-list` 仅限 `complete`，不得让 partial 伪装。
- strict item shape 可能暴露历史 malformed plugin；应修 source，不加 broad fallback。
- full git history/diff-cover 增加 CI 时间；可优化 fetch/filter，不能用不准确 base 替代。
- coverage baseline 可能因 Python patch 差异轻微波动；使用同一 CI Python 3.11 测量并保存精确值。
- 回滚应整体 revert status/report/index/coverage changes；不得只移除 gates或降低 baseline。已有
  valid output 不需迁移；任何临时文件均不得提交或发布。

## Deterministic checks

```bash
python -m pytest -q tests/test_discover_plugins.py tests/test_plugin_index.py \
  tests/test_check_coverage_ratchet.py tests/test_pipeline_contracts.py
python -m pytest -q --cov-report=xml:coverage.xml --cov-report=json:coverage.json
python scripts/check_coverage_ratchet.py --coverage coverage.json \
  --baseline coverage-baseline.json --compare-ref origin/main
diff-cover coverage.xml --compare-branch=origin/main --fail-under=80
python -m pytest -q
ruff check scripts/discover_plugins.py scripts/plugin_index.py \
  scripts/check_coverage_ratchet.py tests/test_discover_plugins.py tests/test_plugin_index.py
git diff --check
```

本次 `implx auth_mode:auto` invocation 已授权实施；合并仍须有独立 reviewer、当前 CI、review
threads、merge state 与 PR gate。真实 discovery/publish 不在实施授权内。
