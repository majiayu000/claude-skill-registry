---
name: midea-recall-diagnose-playwright
description: 用于排查 sit/uat/prod 环境下 `/rag-recall/api/search/keyword` 未召回目标 doc/faq 的问题。支持两种输入：1) 完整请求（headers+body；若 `headers.appId` 缺失但 `body.appId` 存在，可回填）；2) requestId+targetId。统一走“回放 -> ELK -> ES -> 代码最小核对”，禁止 broad search 和冲突口径。
---

# Recall 排查（索引路由版）

## 0. 优先级与硬规则（必须遵守）

- **规则优先级**：`SKILL.md` > `references/*.md`。冲突时只按本文件执行。
- **接口约束**：`keyword` 回放只能用终端 `curl -X POST`，禁止浏览器地址栏访问。
- **取证范围**：本技能只用 `ELK + ES`，禁止调用 `/rag-recall/api/search/trace/recordInfo`。
- **执行通道约束（强制）**：除 `keyword` 回放外，ELK/ES 取证一律使用 Playwright 页面操作；禁止 `curl`/脚本直连 ELK。
- **完整请求强制回放**：拿到 `headers + body` 后，必须先回放并获取 fresh `requestId`，再查 ELK/ES。
- **回放后 requestId-first**：第一条 ELK 查询必须包含 `requestId + TRACE_TARGET_ES + targetId`。
- **首条 KQL 精确匹配（强制）**：首条查询中 `requestId/targetId/TRACE_TARGET_ES` 必须完整精确匹配，禁止 `*` 通配（如 `replay_*`）。
- **禁止 broad search**：回放成功后，禁止先用 `targetId` 单独扫 3 天日志再逐步收敛。
- **ELK 门禁（强制）**：任何 ELK 查询执行前，必须先通过 `python3 scripts/elk_guard.py ... --kql '<KQL>'` 校验；校验失败禁止继续查 ELK。
- **时间窗规则**：回放后先查 `回放时间点 ±15 分钟`；无结果再扩到 `now-3d~now`。
- **TRACE 触发条件（已核对）**：`TRACE_TARGET_ES` 只会在 `traceTargetIds` 非空时打印；若原始请求 `traceTargetIds=[]`，原 `requestId` 很可能查不到该类日志，必须回放并注入 `targetIds`。
- **TRACE 日志格式（已核对）**：真实生产日志中，`phase=request` 会携带 `requestDsl=...`，`phase=response` 会携带 `isError/tookMs/returnedHitCount/totalHitCount`；`targetUrl` 形如 `GET /<index或逗号分隔索引> [cluster=N] (<desc>)`。样例见 `references/trace-target-es-format.md`。
- **回放头回填规则（已核对）**：若 `headers.appId` 缺失但 `request.body.appId` 存在，可回填为回放请求头；`appChannel` 同理。除这两个已核对字段外，其他关键鉴权头不得猜。
- **字段规则**：优先以 ELK `requestDsl` 实际字段为准；字段不明确再查 ES `_mapping`。
- **ES 路由规则（强制）**：进入 ES 前优先从 ELK `targetUrl` 中的 `[cluster=...]` 直接解析集群；若没有集群标识，再从 `requestDsl` / `targetUrl` 提取实际索引名做路由；禁止固定地址直查。
- **ES 路由消歧规则（强制）**：若日志已带 `[cluster=...]`，不得再要求用户补 `sourceSystem`；只有在无集群标识且 `requestDsl` 命中共享索引导致多集群歧义时，才可用 `sourceSystem` 辅助消歧；若仍不能唯一定位，必须中止，禁止 fallback。
- **阶段顺序来源（强制）**：优先用运行时 `CHAIN_NAME` 提取真实阶段顺序；拿不到则动态读取关键链路代码（`SearchLiteFlowService + LiteFlowConstants`）；都失败才回退默认顺序。
- **阶段顺序门禁（强制）**：首次丢失阶段必须按当前链路顺序判定，未验证前序文本召回证据时，禁止直接判定向量阶段丢失。
- **首次丢失口径（强制）**：first-loss 只能由 `phase=response hit=false` 判定；仅凭下游 `phase=request` 缺失不得判该下游阶段丢失。
- **下游 request 缺失口径（强制）**：若已确认上游阶段 `response hit=false`，下游无 `phase=request` 只允许表述为“下游未触发/未发起 request（由上游丢失导致）”，禁止表述为“下游阶段丢失”。
- **描述禁令（强制）**：若向量阶段没有 `phase=response hit=false` 证据，禁止输出“向量召回没了/丢了”；必要时只能写“向量阶段 request 未触发（上游 first-loss 在 XXX）”。
- **首次丢失校验（强制）**：输出结论前必须通过 `python3 scripts/first_loss_guard.py` 校验。
- **代码后置**：默认先完成回放/ELK/ES 定位，输出前再做最小代码核对。
- **最小代码集**：只读与“首次丢失阶段”直接相关的 `2~4` 个文件，禁止全量扫代码。
- **targetIds 上限**：最多 10 个，超出直接拒绝。
- **缺参处理**：缺少可复用 `appId`（优先 `headers.appId`，其次 `body.appId`）或其他关键鉴权头时，不得猜测，必须要求补齐。

## 1. 输入模式

### A. 完整请求模式（优先）

- 输入：`env + targetType + targetIds + request.headers + request.body`
- 行为：必须先回放，再进入 ELK/ES。

### B. requestId 模式

- 输入：`env + targetType + targetIds + requestId`
- 行为：直接 ELK-first；证据不足时要求补全完整请求并执行回放。

## 2. 30 秒流程卡（固定顺序）

1. 规范化输入并校验 JSON。
2. 回放请求（fresh `requestId` + 注入 `traceTargetIds`）。
3. 先用 `scripts/elk_guard.py` 生成并校验 KQL，再用 `requestId + TRACE_TARGET_ES + targetId` 查 ELK。
4. 仅当首次丢失在召回阶段时进入 ES 做三步快检。
5. 输出前做最小代码核对，给出代码证据。

## 3. 标准流程（可执行）

### 3.1 完整请求模式

1. 规范化输入：

```bash
cat >/tmp/diag_input.json <<'JSON'
<input-json>
JSON
jq -e . /tmp/diag_input.json >/dev/null
python3 scripts/prepare_diagnosis.py --input /tmp/diag_input.json
```

2. 回放前处理：
- 将 `body.requestId` 替换为 fresh 值（`原ID_replay_<ts>` 或 `uuidgen`）。
- 将 `targetIds` 合并到 `body.traceTargetIds`。
- 若 `headers.appId` 缺失但 `body.appId` 存在，可用 `body.appId` 回填请求头；`appChannel` 同理。

3. 执行回放：

```bash
curl -X POST '<base_url>/rag-recall/api/search/keyword' \
  -H 'Content-Type: application/json' \
  -H 'appId: <appId>' \
  -H 'appChannel: <appChannel>' \
  -d '<body-with-fresh-requestId-and-traceTargetIds>'
```

4. 回放成功判定：
- 响应中拿到 replay `requestId`。
- 记录最小摘要：`requestId`、总命中数、错误信息。

5. ELK 阶段定位：
- 查询必须包含：`requestId + targetId + TRACE_TARGET_ES`（可加 `link_id=requestId`）。
- 查询前必须执行门禁：

```bash
# 生成推荐 KQL
python3 scripts/elk_guard.py \
  --request-id '<replayRequestId>' \
  --target-id '<targetId>' \
  --mode first \
  --emit-template

# 校验你将要执行的 KQL；失败则停止，不得继续
python3 scripts/elk_guard.py \
  --request-id '<replayRequestId>' \
  --target-id '<targetId>' \
  --mode first \
  --kql '<your-kql>'
```

- 首条 KQL 必须直接采用 `--emit-template` 输出，不允许“因为太长”而删减到 requestId-only / targetId-only。
- 时间窗先用 15 分钟，再扩 3 天。
- 执行方式：只允许 Playwright（如 `browser_navigate/browser_type/browser_press_key`）；禁止 `curl` ELK API。
- 先从 ELK 提取该次请求的 `CHAIN_NAME` 阶段顺序，再按顺序找首个 `phase=response hit=false` 的 `cmpId`。
- 对每个下游阶段，`phase=request` 仅用于说明“是否触发”，不可替代 `phase=response` 作为 first-loss 证据。
- 首次丢失结论前必须跑阶段门禁（示例）：

```bash
python3 scripts/first_loss_guard.py \
  --target-type DOC \
  --chain-line 'CHAIN_NAME[_FULL_RANGE_SEARCH_WITH_LLM_] full_range_meta_filter[...]==>full_range_docTxtRecall[...]==>doc_item_vector_retrieval_batch_es[...]==>full_range_rerank[...]' \
  --events '[{"cmpId":"full_range_docTxtRecall","phase":"response","hit":true},{"cmpId":"doc_item_vector_retrieval_batch_es","phase":"response","hit":false}]' \
  --assert-first-loss doc_item_vector_retrieval_batch_es
```

- 若没有 `CHAIN_NAME`，直接让脚本从代码提取链路顺序：

```bash
python3 scripts/first_loss_guard.py \
  --target-type DOC \
  --repo-root '<rag-recall-root>' \
  --chain-id '_FULL_RANGE_SEARCH_WITH_LLM_' \
  --events '<events-json>'
```

- `--chain-order` 仅用于调试覆盖，不作为常规输入。
- 若 `first_loss_guard.py` 返回 `BLOCKED/FAIL`，禁止输出“向量阶段首次丢失”。

6. ES 验证（仅召回阶段进入）：
- 先解析 ES 控制台路由（示例）：

```bash
python3 scripts/prepare_diagnosis.py \
  --input /tmp/diag_input.json \
  --config references/env-config.local.yaml \
  --request-dsl '<requestDsl-or-raw-elk-line>' \
  --source-system '<sourceSystem-if-needed>' | jq '.esConsoleRoute'
```

- 若脚本报 `requestDsl index route is ambiguous`：先检查是否命中了共享 FAQ 索引；必要时补一个 `sourceSystem` 做消歧。
- 若脚本报 `unable to resolve ES console route` 或 `sourceSystem ... has no ES cluster mapping`：立即中止并补齐有效的 `requestDsl/sourceSystem` 证据。
- `Q1` 原始 `requestDsl` 复跑。
- `Q2` 目标存在性（DOC 用 `doc_id`；FAQ 用 `knowledge_base_id`）。
- `Q3` 保留 filter + 去掉 text must（仅文本阶段需要）。
- 执行方式：只允许 Playwright 控制台页面操作；禁止 `curl` 直连 ES。

### 3.2 requestId 模式

1. 直接按 `requestId + targetId + TRACE_TARGET_ES` 查 ELK。
2. 若 15 分钟无结果，扩到 `now-3d~now`。
3. 若原始请求 `traceTargetIds=[]` 或扩窗后仍无有效证据，判定“未完成带 trace 的复现”，要求补全完整请求并回放。
4. 首次丢失在召回阶段时，再进入 ES 三步快检。

## 4. 代码核对（按需触发，输出前必须）

触发条件（任一满足）：
- 已定位首次丢失阶段，准备输出根因。
- ELK/ES 证据冲突或无法解释。
- 用户明确要求查看实现细节。

最小必读文件（按场景选 2~4 个）：
- 入口与参数约束：
  - `api/src/main/java/com/midea/jr/robot/rag/recall/api/web/controller/SearchController.java`
- TRACE 语义：
  - `infrastructure/src/main/java/com/midea/jr/robot/rag/recall/infrastructure/aspect/EsQueryTraceAspect.java`
  - `common/src/main/java/com/midea/jr/robot/rag/recall/common/utils/TraceTargetScanUtils.java`
- cmpId 映射：
  - `common/src/main/java/com/midea/jr/robot/rag/recall/common/constant/LiteFlowConstants.java`
- 召回实现：
  - DOC：`domain/src/main/java/com/midea/jr/robot/rag/recall/domain/search/cmp/fullrange/FullRangeDocTxtRecallCmp.java`
  - DOC 向量：`domain/src/main/java/com/midea/jr/robot/rag/recall/domain/search/cmp/fullrange/RecallDocItemVectorBatchEsCmp.java`
  - FAQ：`domain/src/main/java/com/midea/jr/robot/rag/recall/domain/search/cmp/fullrange/FullRangeFaqTxtRecallCmp.java`

## 5. 根因判定最小集

- `phase=response hit=false`：该阶段未命中目标的最高优先级证据。
- `下游 phase=request 缺失`：只表示该阶段可能未触发，必须依附上游 first-loss 解释，不能单独当作“该阶段丢失”。
- `目标存在性=0`：索引缺数据/发布未生效/索引路由不覆盖。
- `目标存在性>0 且 原DSL=0`：文本匹配或过滤条件问题。
- `原DSL>0 但最终未返回`：排序/阈值/TopN 问题。
- 若已确认丢在 `full_range_rerank` 或之后：停止 ES 深挖，按 rerank/准出问题交付。

## 6. 输出模板（固定）

1. 目标首次丢失阶段（`cmpId`）
2. 简要原因
3. ELK 关键证据
4. 阶段审计（文本/向量/重排各阶段 `response hit=true|false|unknown`；可补充 `request triggered|not_triggered`，但不得用其判 first-loss）
5. 代码证据（至少 2 条，`文件:行号`）
6. 若在召回阶段：ES 证据（`total/returned/rank/score`）
7. 下一步动作（仅当前阶段相关）

## 7. 违规恢复协议（必须）

- 若出现任一违规（如 `targetId-only`、`requestId-only`、缺 `TRACE_TARGET_ES`、先 broad search），必须立即中止当前路径。
- 若出现 `requestId` 通配/截断（如 `replay_*`）或首条 KQL 被降级，按违规处理并立即中止。
- 若出现 `curl` 查询 ELK/ES（非 `keyword` 回放），按违规处理并立即中止。
- 若出现“未验证文本阶段就判向量阶段”的情况，按违规处理。
- 先输出一行：`BLOCKED_BY_GUARD: <违规原因>`。
- 然后从“ELK 阶段定位”重跑：先 `elk_guard.py` 校验通过，再继续。

## 8. 资源

- `scripts/prepare_diagnosis.py`
- `scripts/elk_guard.py`
- `scripts/first_loss_guard.py`
- `references/quick-runbook.md`
- `references/trace-target-es-format.md`
- `references/env-config.example.yaml`
- `references/env-config.local.yaml`
