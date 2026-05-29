---
name: codex-hermes-playwright-ext-timeout-triage
description: 排查 Codex/Hermes 的 playwright-ext 从“可用”变为不可用（Extension connection timeout）时的最小闭环流程。先判定 bridge 层，再判定 token/同步链路，避免误把问题归因于“未安装 Playwright”。
---

# Codex/Hermes Playwright-ext Timeout Triage

## Trigger
当出现以下任一现象时使用：
- `mcp_playwright_ext_browser_tabs(list)` 返回 `Extension connection timeout`
- 用户反馈“昨天还好好的，今天 playwright-ext 不行了”
- 怀疑 all-my-ai-needs 同步脚本把 token 覆盖成占位符

## Core Principle
先区分三层问题，避免混淆：
1) Playwright CLI 是否安装（本地依赖层）
2) token 是否有效（配置层）
3) MCP Bridge 扩展是否在线（连接层）

`playwright --version` 正常 != bridge 一定可连。

## Steps
1. 快速确认本地依赖（只做事实核验，不做安装）
- `node -v`
- `npm -v`
- `npx playwright --version`

2. 双端复测同一个最小调用
- Hermes: `hermes mcp test playwright-ext` + `browser_tabs(list)`
- Codex: 用 `codex exec` 直接调用 `playwright-ext.browser_tabs(list)`
- 结果判读要区分三种：
  - 两端都 timeout：优先判定为 bridge/扩展未连通（系统性）
  - 仅 Codex timeout、Hermes 正常：优先查 Codex token/配置
  - 仅 Hermes timeout、Codex 正常：优先查 Hermes 侧会话/客户端连接状态（常见是当前 Hermes 会话未连上 Bridge，非 token 本身）

3. 读取配置中的 token 实值（不要猜）
- Hermes: `~/.hermes/config.yaml`
- Codex: `~/.codex/config.toml`
- 用结构化解析（如 Python `tomllib`）提取字段，确认是否为占位符 `<PLAYWRIGHT_EXT_TOKEN>`。

4. 检查“配置已修复但当前会话仍失败”的进程级漂移
- 现象：`~/.hermes/config.yaml` 已是实值 token，但当前 Hermes/Gateway 会话仍 timeout。
- 做法：检查正在运行的 `playwright-mcp --extension` 进程环境变量是否还是旧值/占位符。
- 示例（仅做核验，注意掩码输出）：
  - `ps -Ao pid,ppid,etime,command | grep '@playwright/mcp@latest --extension'`
  - `ps eww -p <node_pid> -o pid=,ppid=,command=` 并比对 `PLAYWRIGHT_MCP_EXTENSION_TOKEN`
- 判读：
  - 若网关长驻进程中的 token 仍是占位符，而新启动的临时进程 token 已是实值，则根因为“长驻进程未重载配置”（会话级/进程级问题），不是当前配置文件内容问题。
  - 修复优先级：重启对应长驻进程（如 `hermes gateway restart`）后复测。

5. 排查 all-my-ai-needs 同步链路是否会覆盖 token
- 读取：
  - `scripts/sync_to_codex.sh`
  - `platforms/codex/config.toml`
  - `scripts/bootstrap.sh`
- 关键判断：
  - 模板里是否是占位符（通常是）
  - `sync_to_codex.sh` 是否仅在 `--sync-config` 下触碰 `config.toml`
  - `bootstrap.sh` 默认是否传 `--sync-config`（通常不传）

6. 用 dry-run + 隔离黑盒实验验证真实行为
- Dry-run：
  - `./scripts/sync_to_codex.sh --root-only --sync-config --dry-run --yes`
  - 看 diff 是否显示 token 占位符来源于模板
- 隔离实验：
  - 使用临时 `CODEX_HOME`
  - 先写入真实 token，再执行同步脚本（带/不带 `--sync-config`）
  - 比较前后 token/哈希，验证脚本是否会“占位符倒灌”

7. 最终归因模板
- 若 Codex 是占位符、Hermes 是实值，且双端都timeout：
  - 结论 A：Codex 配置存在占位符问题
  - 结论 B：Bridge 连接层也有独立问题（即使 token 正确仍可能 timeout）
- 若“修正 token 后 Codex 成功、Hermes 仍 timeout”：
  - 结论 A：token 问题已被部分修复（至少一端可用）
  - 结论 B：剩余故障多为客户端会话级 bridge 状态（如当前 Hermes 会话未重新握手）
  - 建议动作：重启失败端客户端进程/会话后复测，不要再回退到“安装 Playwright 浏览器”路径
- 避免只给单因结论。

## Reusable Commands
- `hermes mcp test playwright-ext`
- `hermes mcp list`
- `codex mcp get playwright-ext`
- `codex exec --ephemeral --json "调用 playwright-ext browser_tabs(list) 并原样返回"`
- `./scripts/sync_to_codex.sh --root-only --sync-config --dry-run --yes`
- `python3 - <<'PY' ...` 结构化读取 `~/.codex/config.toml` 与 `~/.hermes/config.yaml` 的 token 后再比对（避免肉眼误判）

## Pitfalls
- 不要把“已安装 Playwright”当作 bridge 正常的证据。
- 不要把“某一端成功/浏览器 tab 显示已连接”直接等价为“另一端 token 一定错误”。先做双端最小调用复测再下结论。
- 不要在未获用户同意时直接改写本地 token。
- shell 历史未命中不代表“绝对没执行过”，只能作为弱证据。
- 先做复测再改配置，能避免无效改动。

## Done Criteria
- 双端最小调用复测结果明确
- token 状态（Hermes/Codex）明确
- 同步脚本是否会覆盖的证据完整（脚本阅读 + dry-run + 黑盒）
- 对用户给出“双层问题”结论与下一步最小修复建议（先修 Codex token，再复测 bridge）