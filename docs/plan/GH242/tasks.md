# GH242 任务计划

关联 issue: https://github.com/majiayu000/claude-skill-registry-core/issues/242
产品规格: `docs/plan/GH242/product.md`
技术规格: `docs/plan/GH242/tech.md`
状态: `Approved for implementation by implx auth_mode:auto`

## 执行边界

- 共享 discovery/index/coverage 文件采用单一顺序 `implementation_lane`，不得并行写同一文件。
- 授权实施 `SP242-T1` 至 `SP242-T4` 并形成 PR；不调用真实 npm/GitHub discovery、不修改
  `sources/plugins.json` 或 generated outputs、不发布。
- 禁止降低 baseline、排除 production code、添加虚假 `pragma: no cover` 或弱化既有测试。

## `SP242-T1`：建立 typed source outcomes 与稳定状态机

- Owner: `implementation_lane`
- Dependencies: none
- Covers: `GH242-INV-01`, `GH242-INV-02`, `GH242-INV-03`, `GH242-INV-04`
- Files: `scripts/discover_plugins.py`, `tests/test_discover_plugins.py`
- 工作内容:
  1. 实现 `DiscoveryError`、`SourceOutcome`、`DiscoveryReport` 和 status reducer。
  2. npm/GitHub adapters 对 nonzero/timeout/JSON/shape/API failure 抛 source-scoped error。
  3. 实现稳定 exit code、terminal summary 与 `--allow-partial` 边界。
- Done when:
  - zero-candidate success 是 complete；mixed 是 partial；all-error/authoritative error 是 failed。
  - 所有 failure kinds 有直接测试且 error 不含 token/env/raw response。
  - partial 默认非零，allow-partial 不改变 status，failed 永不被允许。
- Verify:

```bash
python -m pytest -q tests/test_discover_plugins.py -k 'error or status or exit'
ruff check scripts/discover_plugins.py tests/test_discover_plugins.py
git diff --check
```

## `SP242-T2`：实现 atomic output 与 strict plugin index

- Owner: `implementation_lane`
- Dependencies: `SP242-T1`
- Covers: `GH242-INV-04`, `GH242-INV-05`, `GH242-INV-06`, `GH242-INV-07`
- Files: `scripts/discover_plugins.py`, `scripts/plugin_index.py`,
  `scripts/rebuild_registry.py`, `scripts/build_search_index.py`,
  `tests/test_discover_plugins.py`, `tests/test_plugin_index.py`
- 工作内容:
  1. complete/allowed-partial 用 same-directory temp + fsync + replace 写 report。
  2. strict loaders 区分 missing、present-empty、present-valid、malformed。
  3. 移除 rebuild duplicate loader，并让 search index 只在 missing 时 fallback。
  4. valid empty 原子写 `plugins.json`，失败保持旧文件 bytes 不变。
- Done when:
  - partial/failed/write failure preservation 与 temp cleanup 有测试。
  - malformed source/index 均抛 typed error；只有 documented missing 可 fallback。
  - present-empty 不加载 stale registry，也不遗留旧 generated plugins。
- Verify:

```bash
python -m pytest -q tests/test_discover_plugins.py tests/test_plugin_index.py \
  tests/test_plugin_contract.py
ruff check scripts/discover_plugins.py scripts/plugin_index.py \
  scripts/rebuild_registry.py scripts/build_search_index.py
git diff --check
```

## `SP242-T3`：建立 global/module/critical/changed-line coverage ratchet

- Owner: `implementation_lane`
- Dependencies: `SP242-T1`, `SP242-T2`
- Covers: `GH242-INV-08`, `GH242-INV-09`, `GH242-INV-10`
- Files: `scripts/check_coverage_ratchet.py`, `coverage-baseline.json`, `pyproject.toml`,
  `.github/workflows/python-tests.yml`, `tests/test_check_coverage_ratchet.py`,
  `tests/test_pipeline_contracts.py`
- 工作内容:
  1. 在 clean origin/main/CI Python 3.11 测量并保存不可降低 global baseline。
  2. checker 强制两个模块各 ≥80%，critical functions 无 missing lines/branch arcs。
  3. CI 生成 XML/JSON coverage，验证 baseline/module/critical，并用 diff-cover 强制 changed ≥80%。
  4. checkout 提供正确 merge base，移除 workflow 的全局 50 override。
- Done when:
  - synthetic coverage tests 覆盖 pass、global regression、module low、critical miss、baseline lowering。
  - CI contract 证明 `origin/main` 可用、所有 gates 顺序执行且没有 omit/override 绕过。
  - 初始 baseline 有 commit/runtime/evidence，数值来自 fresh origin/main 而非估算。
- Verify:

```bash
python -m pytest -q tests/test_check_coverage_ratchet.py tests/test_pipeline_contracts.py
python -m pytest -q --cov-report=xml:coverage.xml --cov-report=json:coverage.json
python scripts/check_coverage_ratchet.py --coverage coverage.json \
  --baseline coverage-baseline.json --compare-ref origin/main
diff-cover coverage.xml --compare-branch=origin/main --fail-under=80
git diff --check
```

## `SP242-T4`：全量验证与 PR handoff

- Owner: `implementation_lane`
- Dependencies: `SP242-T1`, `SP242-T2`, `SP242-T3`
- Covers: `GH242-INV-01` through `GH242-INV-10`
- Files: 无计划 production edit；仅 verification/PR evidence
- 工作内容:
  1. 运行 focused/full tests、coverage gates、Ruff 与 diff/status 检查。
  2. 审查 report/output 不含 secrets，diff 无 source/generated data 和 coverage artifact。
  3. PR 提供 invariant → test/coverage evidence，并交独立只读 reviewer。
- Done when:
  - fresh tests/coverage/Ruff 全部通过，failure branches 与两个 module target 有机器证据。
  - `coverage.xml`、`coverage.json`、htmlcov/temp files 未纳入 commit。
  - 当前 CI、review threads、merge state、独立 review 与 PR gate 完整；未触发 live discovery。
- Verify:

```bash
python -m pytest -q
python -m pytest -q --cov-report=xml:coverage.xml --cov-report=json:coverage.json
python scripts/check_coverage_ratchet.py --coverage coverage.json \
  --baseline coverage-baseline.json --compare-ref origin/main
diff-cover coverage.xml --compare-branch=origin/main --fail-under=80
ruff check scripts tests
git diff --check
git status --short
```

## 追踪矩阵与 human gates

| 不变量 | Primary task | Final gate |
| --- | --- | --- |
| `INV-01`–`INV-04` | `SP242-T1` | `SP242-T4` |
| `INV-05`–`INV-07` | `SP242-T2` | `SP242-T4` |
| `INV-08`–`INV-10` | `SP242-T3` | `SP242-T4` |

1. 实施授权已由 `implx auth_mode:auto` 满足。
2. 合并前必须有独立 reviewer、当前 CI/review threads/merge state 与 PR gate evidence。
3. 真实 npm/GitHub discovery 和 publish 由 maintainer 受控执行，本计划不授权 live run。
