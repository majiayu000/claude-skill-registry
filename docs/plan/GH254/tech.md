# GH254 技术规格：taxonomy sidecar、两层报告关系与分层复核门禁

关联 issue: https://github.com/majiayu000/claude-skill-registry-core/issues/254
产品规格: `docs/plan/GH254/product.md`
基线: `1d307fd932e210e3d6066888c87d1761a557885b`
状态: `Approved for implementation by implx auth_mode:auto`

```json
{
  "specrail-planned-changes": {
    "issue": 254,
    "complete": true,
    "paths": [
      "taxonomy/categories.yaml",
      "scripts/category_taxonomy.py",
      "scripts/build_search_index.py",
      "scripts/audit_category_quality.py",
      "scripts/check_category_sample_review.py",
      "docs/js/artifact-api.js",
      "docs/js/app.js",
      "docs/js/app-render.js",
      "docs/plan/canonical-taxonomy-governance-spec.md",
      "docs/plan/GH254/product.md",
      "docs/plan/GH254/tech.md",
      "docs/plan/GH254/tasks.md",
      "tests/test_category_taxonomy.py",
      "tests/test_build_search_index.py",
      "tests/test_audit_category_quality.py",
      "tests/test_check_category_sample_review.py",
      "tests/test_pages_request_budget.py"
    ],
    "spec_refs": ["B-001", "B-002", "B-003", "B-004", "B-005", "B-006", "B-007", "B-008"]
  }
}
```

## 当前根因与代码锚点

| 锚点 | 当前行为 |
| --- | --- |
| `scripts/category_taxonomy.py:47-123` | 只有 slug→code；未保留 code→slug 索引 |
| `scripts/category_taxonomy.py:234-246` | parent 仅检查存在和 deprecated，不拒绝自环、环或深链 |
| `docs/js/app.js:31-48` | Pages 手写 12 个旧 code/display name |
| `docs/js/app.js:144-165` | 未知非空类别被转换为 `oth` |
| `scripts/audit_category_quality.py:89-258` | 全量启发式报告，无 per-category quota 样本 |

## 技术设计

### 1. Canonical taxonomy contract

`CategoryTaxonomy` 保存唯一 `codes` 反向索引、审计 sampling policy，并提供：

- `slug_for_code()`：code→slug，未知默认拒绝；
- `public_contract(updated_at)`：生成 versioned sidecar；
- parent graph 验证：parent 必须 active、不得等于自身、parent 自身不得再有 parent。

taxonomy 使用 12 个既有 canonical 类别作为报告根；其他类别至多声明一个 root parent。
这是 reporting-only 元数据，`resolve()`、publishability、directory routing 和类别计数不继承。

### 2. Pages sidecar 与 fail-closed 初始化

`build_search_index.py` 生成 `docs/category-taxonomy.json`。Pages 启动时与 lite index 并行读取，
先由 `artifact-api.js` 做 exact-shape、唯一性、default 与 parent 深度检查，再建立运行时映射，
之后才归一化搜索记录。

`normalizeCategoryCode()` 接受 slug 或 code；unknown non-empty 原样返回，empty 使用 sidecar
default code。卡片、modal、filter、leaderboard 与 chart 使用动态 display name；子类别显示为
`Parent › Child`，计数仍是叶子直接计数。

### 3. 分层样本与准确率门禁

`taxonomy/categories.yaml` 声明固定 seed、quota 和六个 strata。`audit_category_quality.py`
先按路径 hash 在每层选择最小 N 项，只读取入选项的 bounded 内容，输出：

- policy、population/sample count；
- path、current category、description/excerpt、semantic sources；
- source/metadata SHA-256、sample key；
- per-stratum digest 和 overall digest。

人口小于 quota 时 sample report 为 failed。`check_category_sample_review.py` 读取人工 review
文件，要求 sample digest、路径集合和 source hashes 完全匹配，expected category 是 active
canonical，并计算 overall/per-category accuracy；低于阈值或证据不完整均非零退出。

### 4. 兼容与回滚

sidecar 是新增小型只读产物，不改变 static artifact API v1 的既有 pointer/shard shape。
回滚可整体 revert sidecar、动态映射、parent 与 sample gate；不需要 archive/data migration。

## Product-to-test mapping

| Behavior invariant | Implementation area | Verification |
| --- | --- | --- |
| `B-001`, `B-002` | taxonomy loader + sidecar validator | taxonomy/build/Pages invalid-shape tests |
| `B-003` | YAML parents + parent graph validator + labels | 12 roots、单层、计数不变 tests |
| `B-004` | Pages runtime maps | 42 类 slug/code round-trip + unknown/empty tests |
| `B-005`, `B-006` | stratified sample builder | reversed input、hash/digest、bounded evidence tests |
| `B-007` | sample review checker | missing/duplicate/stale/noncanonical/threshold negative fixtures |
| `B-008` | audit-only interfaces | no write/migration contract tests and existing suite |

## Deterministic checks

```bash
python -m pytest -q tests/test_category_taxonomy.py tests/test_build_search_index.py \
  tests/test_audit_category_quality.py tests/test_check_category_sample_review.py \
  tests/test_pages_request_budget.py
python scripts/check_taxonomy_governance.py --strict-canonical
python -m pytest -q
ruff check scripts tests
git diff --check
```
