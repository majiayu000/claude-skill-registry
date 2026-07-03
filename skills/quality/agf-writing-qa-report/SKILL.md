---
name: agf-writing-qa-report
description: Use when qa-engineer (or miniapp-qa-engineer) is about to publish an E2E or UAT report. Provides the report skeleton, evidence-quality bar, verdict criteria, and hand-off rules. SIT is now dev-owned and lives in progress/<role>.md (see agf-running-sit-tests skill) — this skill does NOT cover SIT reports.
---

# Writing a QA Report (E2E / UAT)

Use this skill when:

- E2E execution is complete and a report needs publishing
- UAT business sign-off needs to be captured
- A bug-fix E2E re-verification needs recording (always **appended** as `## Re-run [N] — [date]` to the existing `[feature]-e2e-[YYYY-MM-DD].md`; never a new file — see "File path & naming" below)

**Pair with**:
- `agf-running-sit-tests` skill — SIT 由 dev 自跑，本 skill 不覆盖 SIT 报告（SIT 证据已在 `progress/<role>.md` 的 `**SIT 证据**` 段，归档随 `docs/qa/<feature>-process-log.md` 走）
- **UAT 用例文档** `docs/qa/[feature]-uat-cases-[date].md`（模板 `docs/qa/uat-cases-_TEMPLATE.md`，gate SSOT 见 `testing.md`「UAT 用例文档」节）— UAT 执行前生成 + 用户审核 `status: Approved`；执行证据回填用例文档（证据 SSOT），**UAT 报告引用用例 ID，不重复粘贴证据**
- This skill — covers the **E2E / UAT artifact** (report file) format

## File path & naming

`docs/qa/[feature-kebab-case]-[stage]-[YYYY-MM-DD].md` — Stage ∈ `{e2e, uat}`. Examples:
- `docs/qa/oauth-login-e2e-2026-05-13.md`
- `docs/qa/oauth-login-uat-2026-05-15.md`

**One report per stage per feature.** Re-runs after defect fix → append a new `## Re-run [N] — [date]` section to the same file, do not create a new file.

## Required sections (in order)

```markdown
---
# frontmatter 是 verdict 数据的唯一 SSOT（agf-verdict.py 解析；validate-verdict hook 校客观底线、agf-matrix.sh fan-in 都读这里）
feature: [feature-slug]
date: YYYY-MM-DD
tester: qa-engineer
stage: E2E                     # E2E | UAT
report_verdict: Promote        # Promote | Conditional promote | Block
critical_defect_count: 0       # 客观底线事实（>0 时 report_verdict 必须为 Block）
p0_pass2_total: 0              # P0 用例数（需 pass²）
p0_pass2_ok: 0                # 连续 2 次都过的 P0 数
uat_signoff_verdict: N/A       # approve | request changes | N/A（仅 UAT 阶段有值；不推导）
---

# QA Report — [Feature] — [E2E|UAT]

- **Date**: YYYY-MM-DD
- **Stage**: E2E / UAT
- **Tester**: qa-engineer ([model name]) / 业务方姓名（UAT）
- **Branch**: [branch + commit hash]
- **Environment**: local docker-compose / staging / pre-prod
- **PRD**: docs/prd/[feature]-[date].md
- **Code review (含 SIT Audit)**: docs/reviews/[feature]-[date].md

## Summary

- Total AC: N
- Passed: M
- Failed: K
- Blocked: J
- 界面渲染核查（仅 UAT 且含界面 feature）: N/N 界面真渲染 + 截图 + 读图四查通过（矩阵 SSOT 在用例文档）
- **Verdict**: ✅ Promote to next stage / ❌ Block / ⚠️ Conditional promote

## Pre-conditions Checked

- [ ] 单元测试 + lint + typecheck 全绿
- [ ] code-reviewer 报告已存在且 verdict ≠ Block（含 SIT Audit = ✅ / ⚠️）
- [ ] PRD AC 可访问
- [ ] 环境就绪（DB 起来 / 迁移已 apply / 服务已启动）
- [ ] **（仅 UAT）用例文档已审核**：`docs/qa/[feature]-uat-cases-[date].md` 存在且 frontmatter `status: Approved`（MAJOR / MINOR 强制；PATCH 级 hotfix 由 PL 豁免时在报告注明理由）

任何一条没勾 → 不该开始测；先 SendMessage product-lead 解决先决条件。

## AC Results

### AC-1 (P0): [verbatim AC text from PRD]

- **Priority**: P0 / P1 / P2（来自 PRD §4 Priority；P0 必须跑 2 次，P1/P2 跑 1 次即可）
- **Setup**: [起始状态]
- **Action**: [触发步骤]
- **Expected**: [复制 PRD AC 原文]
- **Actual (run 1)**:
  ```
  HTTP/1.1 200 OK
  Content-Type: application/json
  {"id": 42, "status": "created"}
  ```
- **Actual (run 2)** [P0 必填；P1/P2 可空]:
  ```
  HTTP/1.1 200 OK
  ...
  ```
- **Reliability**: `pass^1 = 1/1` 或 `pass^2 = 2/2`（P0）— 两次不一致 = `⚠️ Flaky`，按 fail 处理
- **Verdict**: ✅ Pass / ❌ Fail / ⚠️ Blocked / ⚠️ Flaky

(每个 AC 都要单独一节，**禁止合并写 'all passed'**。**为什么 P0 要跑 2 次**：业界实证（τ-bench）pass@1 高 ≠ pass^k 高，单次过的 P0 case 偶发问题会逃逸到生产。)

## Defects Found

| ID | Severity | Title | Repro steps | Suspected file |
|---|---|---|---|---|
| DEF-1 | High | ... | 1. ... 2. ... | backend/app/foo |

Severity 标准:
- **Critical**: 阻断核心流程，无 workaround
- **High**: 阻断核心流程但有 workaround；或非核心流程的数据/安全问题
- **Medium**: 边缘场景失败，不阻断核心流程
- **Low**: 体验/文案/兼容性

## Cross-stage Notes

- E2E → UAT: 给业务方的操作手册 / 数据准备说明 / 已知 P2 defect 列表

## Cost (this QA session)

- Tokens consumed: [from `/usage`]
- Estimated cost: [CNY]
- 同 feature 累计（E2E + UAT 总和）：[CNY]

## Hand-off

✅ Promote → SendMessage product-lead 进下一阶段
❌ Block → SendMessage product-lead 列 critical defect，重新派回 dev
⚠️ Conditional → 列 P2 defect 单独建 issue，allow 进下一阶段
```

## Verdict 决策树（不能凭感觉）

```
任一 P0 AC = Fail              → ❌ Block
所有 P0 + P1 AC = Pass         → ✅ Promote
P0 全 Pass，P1 部分 Fail        → ⚠️ Conditional（P1 失败必须建跟踪 issue）
有 P0 = Blocked（环境问题）     → ⚠️ Block + 升级 product-lead
```

### 客观底线硬校验（frontmatter，退出时 hook 拦）

`report_verdict` 的定性选择（Promote vs Conditional）**不**套公式，但两条**客观底线**由 `validate-verdict.sh`（委托 `agf-verdict.py`，ADR-010）退出时重算、违反即 exit 2 打回——填 frontmatter 前自查：

- `critical_defect_count > 0` → `report_verdict` **必须为 Block**（有 critical defect 却 Promote/Conditional = 不可能组合）。
- `p0_pass2_ok < p0_pass2_total`（P0 未全部 pass²）→ `report_verdict` **不得为 Promote**（P0 没连过 2 次不准晋级）。

> 这两条只拦"客观不可能组合"，不强定 Promote/Conditional 档；极保守 fail-open（缺字段 / 坏 yaml 一律放行 + WARN）。`uat_signoff_verdict` 仅结构化记录、不推导。

## Evidence 质量条

每条 Pass 的 Actual 段**必须**有可验证产物之一：

- HTTP 调用：`curl -i` 完整响应头 + body（敏感字段可遮）
- DB 状态：`SELECT` 前后对比
- UI：截图（命名规则：`evidence/AC-N-[step].png`）
- 日志：相关行（带时间戳）
- 文件落盘：`ls -la` + 内容 head

**禁止**只写"Passed, looks correct"——这种 Pass 不可信，等同没测。

**UAT 含用户可见界面的用例额外强制**（SSOT：`testing.md`「UAT 界面渲染核查」节）：

- 截图**必选**且必须来自 chrome-devtools 真渲染（小程序 / Apple 轨用对应模拟器；命名 `evidence/UAT-[case]-[界面slug].png`），**落盘后必须用 Read 读回做视觉分析**（对照 design spec + `index.html` 原型），在用例文档「界面渲染核查矩阵」回填四查结论（导航 / 裁切 / 控件可点 / 视觉达标）
- curl / `SELECT` 输出只能作**补充**——**纯 API / DB 断言不构成 Pass**；矩阵任一行缺截图或缺读图结论（"已截图" ≠ "已核查"）= 该界面未测，本报告不得发布

## 反模式

（"合并写 all passed" / "无 evidence 的 Pass" / "Defect 不写 Repro" 已由下文「完成前的验证」checklist 反向守门，此处不重列。）

- ❌ 跑 E2E 时同时改代码（移动靶）— 必须 freeze 分支再跑
- ❌ 用生产 API key 跑 E2E — 必须用专用测试 key + 每日花费上限
- ❌ 用本 skill 写 SIT 报告 — SIT 已 dev 自跑，证据落 `progress/<role>.md`，不再有独立 SIT 报告
- ❌ UAT 用 API 断言代替界面渲染 — 接口 200 ≠ 界面可用（导航缺失 / 裁切 / 控件点不动全漏检）；含界面用例必须真渲染 + 截图 + 读图四查，"时间紧 / E2E 已截过图 / 后端数据对了"都不是豁免理由
- ❌ 截图存档但不读图 — 截图必须用 Read 读回、以视觉能力对照 design spec 给"视觉达标"结论；**UIUX 是用户对产品最直接的感受**，"功能对了但界面糙"不是可交付状态，"已截图"不等于"已核查"

## 完成前的验证

- [ ] 每条 AC 都有 Setup / Action / Expected / Actual / Verdict 五段？
- [ ] 每个 Pass 都有可验证 evidence？
- [ ] Defects 表每行都有 Repro steps + Suspected file？
- [ ] Cost 一节填了实际数字（不是 TBD）？
- [ ] Verdict 由决策树推出（不是凭感觉）？
- [ ] **交互控件全覆盖**（含前端的 feature）：页面每个可交互控件都点击/输入过 + 断言了可观测后果（DOM/网络/路由/状态），非"截图看着有按钮"（见 `testing.md` 前后端对接强制覆盖项 ③）？
- [ ] **（仅 UAT）界面渲染核查矩阵**：每个用户可见界面已真渲染 + 截图 + 读图四查（导航 / 裁切 / 控件可点 / 视觉达标），每张截图都被 Read 读回分析过，无"待执行"残留、无以纯 API 断言代替（见 `testing.md`「UAT 界面渲染核查」节）？
- [ ] Hand-off SendMessage 已发出？

任一不行 → 不要 publish，回去补。

## Hand-off 触发

报告落盘后立即（**不等用户问**）：

1. SendMessage product-lead，附 verdict + report path + 1 句话总结
2. 如 verdict = Block：列 top-3 critical defect 在消息正文
3. 如 verdict = ⚠️ Conditional：把 P2 defect 通过 `TaskCreate` 单独开 follow-up task（由 product-lead 派发）
