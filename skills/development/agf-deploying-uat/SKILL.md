---
name: agf-deploying-uat
description: Use when deploy-engineer is about to deploy the merged-to-main code to the isolated local UAT stack (after code review + SIT Audit pass and merge, before qa-engineer runs E2E/UAT). Provides the applicability gate, pre-flight checks, isolated compose bring-up (independent project name + port offset +900), in-container migration, real-output smoke test, hand-off, and the deploy-report skeleton. Pairs with deployment.md "UAT 环境部署" contract and slash /agf-deploy-uat.
---

# Deploying to the isolated UAT stack

把**合并到 main 后的干净代码**部署到与所有 dev worktree 物理隔离的本地 UAT 栈，冒烟自检通过后交接 qa-engineer。本 skill 是 deploy-engineer 的分步 runbook；隔离契约的单一来源是 [`deployment.md`](../../standards/deployment.md) "UAT 环境部署" 节。

## 适用门

满足以下**全部**才进入部署：

- 角色 = `deploy-engineer`（review-only / deploy-only，不修源码）。
- 目标是 **Web 全栈链路**（docker-compose 化的 frontend + backend + postgres 等）。小程序"部署"= 上传体验版 → **不适用**，归 miniapp-dev / miniapp-qa-engineer。
- code review（含 SIT Audit）已通过**且已合并到 main**，product-lead 已确认"部署 UAT"（对话内询问通过或 `/agf-deploy-uat` 手动触发）。

任一不满足 → 不部署，SendMessage product-lead 说明缺什么。

## 前置检查（部署前必须逐项确认）

- [ ] **main 干净且最新**：在合并后的 main 上，`git status` 无未提交改动，记录待部署 commit SHA（`git rev-parse --short HEAD`）。绝不部署任何未合并的 dev worktree 分支。
- [ ] **docker 可用**：`docker compose version` 正常返回（daemon 在跑）。
- [ ] **`.env.uat` 存在**：UAT 专用环境变量文件（含密钥）已就位且 **gitignore**（不入库）。缺失 → 阻断，请 product-lead 协调补齐。
- [ ] **端口未被占**：+900 带（6332 / 8900 / 8980）当前空闲（`lsof -i:8900` 等快速核对），确认不与 dev（base）/ QA pool（base+100..+700）/ 既有 UAT 栈撞车。

任一不勾 → 不起栈，先 SendMessage product-lead 解决先决条件。

## 隔离起栈（独立 project name + 端口偏移 +900）

```bash
export COMPOSE_PROJECT_NAME=${APP_NAME}-uat   # 独立 project → 容器/网络/卷全独立于 dev / QA
export UAT_PORT_OFFSET=900                     # → POSTGRES 6332 / BACKEND 8900 / FRONTEND(caddy) 8980
docker compose -p "$COMPOSE_PROJECT_NAME" --env-file .env.uat up -d --build
```

- `-p "$COMPOSE_PROJECT_NAME"`：让容器 / 网络 / 卷全部带 `<app>-uat` 前缀，与 dev worktree 物理隔离。
- `--env-file .env.uat`：注入 UAT 专用变量（DB 连接、LLM key、端口偏移消费等）。
- `--build`：必须重建 image（**禁止**仅 `restart`——restart 不重建 image，合并后的新代码不会进容器，正是 deployment.md "P0/P1 修复 Close 前的强制门" 节 Step 1「容器重建」记录的失败模式）。
- 起栈后 `docker compose -p "$COMPOSE_PROJECT_NAME" ps` 确认各服务 `Up`（healthy）。

## 容器内迁移

DB schema 迁移必须**在容器内**对 UAT 库跑，不在宿主机：

```bash
docker compose -p "$COMPOSE_PROJECT_NAME" exec backend alembic upgrade head
```

- 捕获真实输出（迁移版本号 / `Running upgrade ...` 行），贴进部署报告"迁移结果"段。
- 迁移报错 → 按 systematic-debugging 定位：若是 `.env.uat` / 连接配置问题 → 自修重跑；若是 migration 脚本本身错（代码问题）→ 退回 product-lead → dev。

## 冒烟（真实输出，非 dry-run）

复用 [`deployment.md`](../../standards/deployment.md) "P0/P1 修复 Close 前的强制门" 节 Step 2「curl 实证 AC 边界（真实输出，非 dry-run）」的实证原则——**只接受真实响应**，拒绝 "dry-run pass" / "本地 unit 已过" / "代码看着对"。

- **backend 健康/核心端点**：
  ```bash
  curl -sS -w "\nHTTP %{http_code}\n" http://localhost:8900/health
  curl -sS -w "\nHTTP %{http_code}\n" http://localhost:8900/api/<核心只读端点>
  ```
- **frontend 可达**：
  ```bash
  curl -sS -I http://localhost:8980    # 期望 200 / index.html 可达
  ```
- **DB 连通**（迁移后表存在）：
  ```bash
  docker compose -p "$COMPOSE_PROJECT_NAME" exec postgres psql -U <user> -d <db> -c "\dt"
  ```
- 至少覆盖：**前端可达 + 后端健康 + 一个核心 API 真实 200 + DB 连通**。任一非预期 → gate = `❌ 部署失败`。

**冒烟范围说明**：冒烟只证明"环境立起来、链路通"，**不是** E2E——不替业务流程 / AC 验收做判断（那是 qa-engineer 的事）。冒烟若暴露**代码层**缺陷（如核心 API 500），采集证据后退回 product-lead，不自己改源码。

## 二元 gate

部署门只有两态，**不发明**新 verdict 词表：

- `✅ 部署成功（冒烟通过）` —— 前置全过 + 起栈 healthy + 迁移成功 + 冒烟真实 200/连通。
- `❌ 部署失败` —— 任一环节失败；报告里标明是**环境/配置问题**（deploy-engineer 自修重部）还是**代码问题**（退回 PL → dev）。

## 交接

报告落盘后立即（**不等用户问**）SendMessage product-lead：

- ✅ 成功：附报告路径 + UAT 栈各服务 URL（`http://localhost:8980` / `http://localhost:8900`）+ 部署 commit SHA，供 PL 触发 qa-engineer 对**共享 UAT 栈**跑 E2E。
- ❌ 失败：附报告路径 + 失败定位（环境 vs 代码）+ 建议（重部 / 退回 dev）。

```
SendMessage({to: "product-lead", message: "UAT 部署完成: [功能名]\n报告: docs/deploy/[feature]-uat-[YYYY-MM-DD].md\nUAT 栈: FRONTEND http://localhost:8980 / BACKEND http://localhost:8900\n部署 commit: [SHA]\n结果: ✅ 部署成功（冒烟通过） / ❌ 部署失败", summary: "UAT 部署: [功能名]"})
```

## 部署报告骨架

落到 `docs/deploy/<feature>-uat-<YYYY-MM-DD>.md`（与 `docs/reviews` / `docs/qa` 对称；pool=1，**无** `agf-matrix.sh` 用的 YAML frontmatter）：

````markdown
# UAT 部署报告 — [Feature]

- **Date**: YYYY-MM-DD
- **Deployer**: deploy-engineer ([model name])
- **部署 commit (merged main)**: [short SHA]
- **Compose project**: ${APP_NAME}-uat
- **端口偏移**: UAT_PORT_OFFSET=900

## UAT 栈服务地址（交给 qa-engineer 作测试目标）

| 服务 | URL / 端口 |
|---|---|
| Frontend (caddy) | http://localhost:8980 |
| Backend (API)    | http://localhost:8900 |
| Postgres         | localhost:6332 |

## 前置检查

- [x] main 干净且最新（commit [SHA]）
- [x] docker 可用（`docker compose version`）
- [x] `.env.uat` 存在（gitignore，未入库）
- [x] +900 端口带空闲，不与 dev / QA pool 撞车

## 隔离起栈

```
docker compose -p ${APP_NAME}-uat --env-file .env.uat up -d --build
```
（贴 `docker compose ps` 各服务 Up/healthy 输出）

## 迁移结果（容器内）

```
docker compose -p ${APP_NAME}-uat exec backend alembic upgrade head
（贴真实迁移输出：Running upgrade ... → <revision>）
```

## 冒烟证据（真实输出，非 dry-run）

- **Frontend 可达**：`curl -I http://localhost:8980` → （贴 HTTP 200 头）
- **Backend 健康**：`curl -w "HTTP %{http_code}" http://localhost:8900/health` → （贴状态码 + body）
- **核心 API**：`curl ... http://localhost:8900/api/<端点>` → （贴真实响应）
- **DB 连通**：`... psql -c "\dt"` → （贴表清单）

## Deploy Gate

**Verdict**: ✅ 部署成功（冒烟通过） / ❌ 部署失败
（失败时：问题归类 = 环境/配置（自修重部） / 代码（退回 product-lead → dev）+ 证据）

## Hand-off

✅ → SendMessage product-lead（附 UAT URL）→ PL 触发 qa-engineer E2E
❌ → SendMessage product-lead（附失败定位）→ PL 决策重部 / 退回 dev
````

## 完成前的验证

- [ ] 部署源确为合并后的 main（记了 commit SHA），不是 dev worktree 分支？
- [ ] 用了独立 `-p ${APP_NAME}-uat` + 端口偏移 +900（未复用 dev / QA 栈）？
- [ ] 迁移在容器内对 UAT 库跑且有真实输出？
- [ ] 冒烟每条都有真实 curl/psql 输出（无 dry-run、无"看着对"）？
- [ ] gate 是二元（✅/❌），失败时标了环境 vs 代码归类？
- [ ] 报告落盘 + SendMessage product-lead 已发（附 UAT URL）？

任一不行 → 不要声明部署成功，回去补。

## 反模式

- ❌ 部署 dev worktree 未合并分支 —— 必须从合并后的 main 拉。
- ❌ 仅 `docker compose restart` 不 `--build` —— 新代码不进容器（deployment.md "P0/P1 修复 Close 前的强制门" 节 Step 1「容器重建」失败模式）。
- ❌ 复用 dev / QA 栈"省事" —— 破坏隔离，污染测试基线。
- ❌ 冒烟用 dry-run / "本地看着对" 当证据 —— 等同没冒烟。
- ❌ 冒烟暴露代码 bug 时自己改 `backend/` / `frontend/` —— 越界；采证退回 PL → dev。
- ❌ 给部署门发明多档 verdict 词表 —— 二元 gate（✅/❌）即可，保 CLAUDE.md「Verdict 词表 4 套」硬事实。
