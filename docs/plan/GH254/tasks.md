# GH254 任务计划

关联 issue: https://github.com/majiayu000/claude-skill-registry-core/issues/254
产品规格: `docs/plan/GH254/product.md`
技术规格: `docs/plan/GH254/tech.md`
状态: `Approved for implementation by implx auth_mode:auto`

## `SP254-T1`：闭合 taxonomy code 与两层 parent 契约

- Owner: `implementation_lane`
- Dependencies: none
- Covers: `B-001`, `B-002`, `B-003`
- Done when: 42 类双向唯一，恰有 12 个 root，非法 parent 图 fail closed。
- Verify: `python -m pytest -q tests/test_category_taxonomy.py`

## `SP254-T2`：生成 sidecar 并让 Pages 动态消费

- Owner: `implementation_lane`
- Dependencies: `SP254-T1`
- Covers: `B-001`, `B-002`, `B-003`, `B-004`, `B-008`
- Done when: sidecar exact-shape；42 类 slug/code 不丢失；unknown non-empty 可见；empty 用 default。
- Verify: `python -m pytest -q tests/test_build_search_index.py tests/test_pages_request_budget.py`

## `SP254-T3`：实现确定性分层样本与人工准确率门禁

- Owner: `implementation_lane`
- Dependencies: `SP254-T1`
- Covers: `B-005`, `B-006`, `B-007`, `B-008`
- Done when: 六层固定 quota/digest；证据缺失、过期、重复或低准确率均 fail closed。
- Verify: `python -m pytest -q tests/test_audit_category_quality.py tests/test_check_category_sample_review.py`

## `SP254-T4`：全量验证、独立审查与交付

- Owner: `verification_owner`
- Dependencies: `SP254-T1`, `SP254-T2`, `SP254-T3`
- Covers: `B-001` through `B-008`
- Done when: focused/full tests、lint、CI、review threads、独立 reviewer 和 PR gate 全绿。
- Verify:

```bash
python scripts/check_taxonomy_governance.py --strict-canonical
python -m pytest -q
ruff check scripts tests
git diff --check
```

## Coverage check

Product invariant set:
`{B-001,B-002,B-003,B-004,B-005,B-006,B-007,B-008}`.

Task coverage union:
`{B-001,B-002,B-003,B-004,B-005,B-006,B-007,B-008}`.
