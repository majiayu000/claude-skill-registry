---
name: cliproxy-newapi-stack
description: 在 Linux VPS 上部署 CLIProxyAPI + NewAPI 组合栈，把 Codex/Claude/Gemini/Qwen 等订阅账号包装成可计费的 OpenAI 兼容 API。负责 NewAPI Docker 部署、容器→宿主桥接、模型计费倍率（ModelRatio/CacheRatio/CompletionRatio）、SQLite 直写额度、CLIProxyAPI 408 冷却补丁、多账号 OAuth 凭据热加载、双路径验证。当用户说"部署 cliproxy + newapi"、"加 OpenAI 计费层"、"配置 newapi 渠道接 cliproxy"、"newapi 价格不对"、"加新的 codex/claude 账号到现有部署"、"172.17.0.1 容器网络"、"408 冷却放大故障"时触发。
allowed-tools: Bash, Read, Write, Edit
metadata:
  argument-hint: '[ssh-目标，例如 root@1.2.3.4]'
---

# CLIProxyAPI + NewAPI Metering Stack

把 OAuth 订阅账号 (`codex`/`claude`/`gemini`/`qwen`/`iflow`) 通过 **CLIProxyAPI** 暴露为
OpenAI 兼容 API，再用 **NewAPI** (`calciumion/new-api`) 在前面套一层计费/限流/多用户 token。
姊妹 skill `cliproxy-deploy` 只负责裸 CLIProxyAPI；本 skill 在其上加 metering 层并补全踩过的坑。

所有"完成"结论必须基于**本会话**命令输出（W-16）。价格和额度变更后必须真发一次请求并查
`logs.quota` 不为 0。

---

## 0. 前置确认（必问）

- **SSH 目标**：`root@HOST` 是否能免密
- **端口分配**：`CLIPROXY_PORT`（默认 `8317`）、`NEWAPI_PORT`（默认 `8200`）
- **裸部署是否就绪**：CLIProxyAPI 已经在 `<HOST>:<CLIPROXY_PORT>` 跑通？没就先跑
  `cliproxy-deploy` skill
- **登录账号供应商**：`codex` / `claude` / `qwen` / `iflow` / `gemini`
- **价格输入格式**：每个虚拟模型给我 input / cached / output 三个 USD per 1M 数字
- **客户端机器**：要在哪些机器上落 `BASE_URL` 环境变量

降级路径：默认走"本地 OAuth + scp 同步 + UFW 开 NewAPI 端口 + SQLite 直写价格"。

---

## Phase 1 — CLIProxyAPI（委托给姊妹 skill）

裸部署已在 `cliproxy-deploy` skill 完成；本 skill 不重复其内容，只补丁两个点：

1. **加稳定性开关**到 `/root/CLIProxyAPI/config.yaml`：
   ```yaml
   disable-cooling: true
   ```
   原因见 `references/troubleshooting.md` "CLIProxyAPI cooldown 原理"。
   若漏改，30 并发 5KB payload 会出现混合 ~50% 503。

2. **不要把 CLIProxyAPI 端口暴露到公网**（与裸部署不同）：
   - `host: ""` 仍可，但仅给容器访问，外部公网走 NewAPI 入口即可
   - 如果之前已经 `ufw allow <CLIPROXY_PORT>` 想保留作为 admin 后门也行，但要换强 key

---

## Phase 2 — 部署 NewAPI 容器

```bash
SSH_TARGET=root@<HOST> SSH_KEY=~/.ssh/id_ed25519 NEWAPI_PORT=8200 \
  scripts/deploy_newapi.sh
```

脚本完成后 UFW 放行：
```bash
ssh -i <KEY> <SSH_TARGET> "ufw allow <NEWAPI_PORT>/tcp && ufw status | grep <NEWAPI_PORT>"
```

首次访问 `http://<HOST>:<NEWAPI_PORT>` 完成 root 账号注册（NewAPI 不预置默认密码）。
保存账号密码到密码管理器（不要写进 skill / 日志 / 提交）。

---

## Phase 3 — 渠道 + Token

### 3a. 创建渠道（CLIProxyAPI as upstream）

NewAPI 后台 → "渠道" → 新建 → OpenAI 类型：

- **base_url**：`http://172.17.0.1:<CLIPROXY_PORT>`
  ⚠️ **不能写 `127.0.0.1`** — 容器里的 127.0.0.1 是容器自己。详见
  `references/troubleshooting.md` "容器网络速记"。
- **密钥**：CLIProxyAPI 的 `cpa_xxx` key
- **模型**：以逗号分隔填 CLIProxyAPI 暴露的虚拟模型名，例如：
  `gpt-5.4,gpt-5.3-codex,gpt-5.3-codex-spark,gpt-5.4-mini,gpt-5.2`
- 测试按钮应当 200 OK；失败先查 `references/troubleshooting.md`。

### 3b. 创建 Token（客户端用）

NewAPI 后台 → "令牌" → 新建：
- **名称**：`client-default` 之类标识
- **额度**：先放 `unlimited` 或一个大数（实际计费由 user.quota 控制）
- **可用模型**：勾上你给客户端开放的模型
- 复制生成的 `sk-xxx`（这是客户端的 BASE_API_KEY）

---

## Phase 4 — 写价格 + 充额度

### 4a. 写价格

用 `scripts/set_pricing.py`（基于实测 USD/1M 自动算出三个倍率）：

```bash
SSH_TARGET=root@<HOST> SSH_KEY=~/.ssh/id_ed25519 \
  scripts/set_pricing.py \
    --model gpt-5.4       --input 2.5  --cached 0.25  --output 15 \
    --model gpt-5.3-codex --input 1.75 --cached 0.175 --output 14
```

脚本会：合并写入 `options` 表的 `ModelRatio` / `CacheRatio` / `CompletionRatio`，重启容器。

⚠️ 倍率语义见 `references/newapi-pricing.md` —— `CacheRatio` / `CompletionRatio` 是**相对
输入价的倍数**，不是绝对单价。`ModelRatio` 在不同 fork 里可能除以 2，第一次配置务必发请求
看 `logs.quota` 实际值匹配预期。

### 4b. 充额度

NewAPI 在线充值通常未配，最快走 SQLite 直写：
```bash
SSH_TARGET=root@<HOST> SSH_KEY=~/.ssh/id_ed25519 \
  scripts/topup.sh <user_id> <quota>
# 例：1 1000000000  → 1B quota ≈ USD 2000 (默认 QuotaPerUnit=500000)
```

### 4c. 配置在线充值（可选）

如果要让用户自助充值，NewAPI 后台 → 系统 → 支付：
- Stripe / 易支付 / 自定义 → 填 `TopUpLink` 等字段
- 不配也行，管理员手动加额度 (`scripts/topup.sh`) 是合法主路径

---

## Phase 5 — 客户端环境变量

把以下三行追加到客户端的 `~/.zshrc` 或 `~/.bashrc`：

```bash
export BASE_URL="http://<HOST>:<NEWAPI_PORT>/v1"
export BASE_API_KEY="<NEWAPI_TOKEN>"   # sk-xxx
export BASE_MODEL="<虚拟模型名>"       # 如 gpt-5.4
```

`source` 一下生效。

跨多台机器同步时（W-14 文件归属）：单台单台手动 SSH 改各自的 rc 文件，避免并行写覆盖。

---

## Phase 6 — 加新账号（OpenAI/Anthropic/etc）

不需要重启服务，CLIProxyAPI 有 file watcher。

最简单：
```bash
PROVIDER=codex \
  SSH_TARGET=root@<HOST> SSH_KEY=~/.ssh/id_ed25519 \
  CLIPROXY_LOCAL=<本地 CLIProxyAPI 仓库路径> \
  scripts/add_codex_account.sh
```

脚本流程：
1. 本地启 `go run ./cmd/server -<provider>-login -config config.yaml`
2. 浏览器**用新账号**登录（先在浏览器登出旧账号或用无痕窗口 — 否则会复用旧 session 把旧凭据
   覆盖回去）
3. 自动 diff `~/.cli-proxy-api/<provider>-*.json`，把新文件 `scp` 到 VPS
4. tail VPS 日志确认 `auth file changed (CREATE)`

详见 `references/multi-account.md`（含订阅条件、轮询语义、删除账号、验证方法）。

---

## 验证（Phase 4/5/6 之后必跑）

```bash
HOST=<HOST> SSH_TARGET=root@<HOST> SSH_KEY=~/.ssh/id_ed25519 \
  CLIPROXY_PORT=<CLIPROXY_PORT> NEWAPI_PORT=<NEWAPI_PORT> \
  CLIPROXY_KEY=<cpa_xxx> NEWAPI_TOKEN=<sk-xxx> MODEL=<虚拟模型> \
  scripts/verify_stack.sh
```

通过判定：
- 直连 CLIProxyAPI HTTP 200
- 经 NewAPI HTTP 200
- 最近 `logs` 里对应 `request_id` 行 `quota > 0`

任一不满足都不得声称"部署完成"。

---

## 资源索引

| 文件 | 用途 |
|---|---|
| `scripts/deploy_newapi.sh` | NewAPI 容器一键部署 + 健康自检 |
| `scripts/set_pricing.py` | 用 USD/1M 三参数自动写 NewAPI ratios |
| `scripts/topup.sh` | 直接 SQLite 改 `users.quota` |
| `scripts/verify_stack.sh` | 双路径 + 计费日志验证 |
| `scripts/add_codex_account.sh` | OAuth 登录 + 同步凭据 + watcher 校验 |
| `references/newapi-pricing.md` | ModelRatio / CacheRatio / CompletionRatio / QuotaPerUnit 完整语义 + 计算示例 |
| `references/troubleshooting.md` | 容器网络、cooldown、PUT 不生效、UFW 等踩坑表 |
| `references/multi-account.md` | 多账号轮询语义 + 加号 / 删号 / 订阅条件 |

---

## 不要做的事

- ❌ NewAPI 渠道 base_url 写 `http://127.0.0.1:<port>`（容器内自指）
- ❌ 把 `CacheRatio` 当绝对单价（实际是相对输入的倍数）
- ❌ 价格只走 `/api/option/` PUT 不验证（已知该接口可能静默失败）
- ❌ 远端 OAuth 隧道折腾（5 分钟窗口 + 隧道配合，已踩过坑，统一用本地登录 + scp）
- ❌ 把 CLIProxyAPI 公网端口的 `cpa_` key 和 NewAPI 的 `sk-` token 共享给同一类客户端
- ❌ 跨会话声称"价格生效"——必须本会话发请求 + 看 `logs.quota`
- ❌ 在没有 `disable-cooling: true` 的情况下做高并发压测
