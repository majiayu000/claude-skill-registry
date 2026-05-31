---
name: cliproxy-deploy
description: 在 Linux VPS 上部署 CLIProxyAPI（router-for-me/CLIProxyAPI）并暴露 OpenAI 兼容 API。覆盖 Go 环境、源码拉取、最小配置、OAuth 登录（远端 / 本地同步两种路径）、UFW 放行、密钥轮换、健康校验、环境变量落盘。当用户说“部署 cliproxy / 把 codex/claude/gemini 账号暴露成 API / router-for-me 上线 VPS”时触发。
allowed-tools: Bash, Read, Write, Edit
metadata:
  argument-hint: '[ssh-目标，例如 root@1.2.3.4] [端口，默认 8317]'
---

# CLIProxyAPI VPS 部署

把 `https://github.com/router-for-me/CLIProxyAPI` 部署到远程 Linux 服务器，并暴露 OpenAI 兼容接口（`/v1/chat/completions`、`/v1/models`）。适配 Codex / Claude / Gemini / Qwen / iFlow / Antigravity 的 OAuth 订阅账号。

所有“必须 X”条款都附带降级路径；所有“完成”结论必须基于**本会话**命令输出（W-16）。

---

## 0. 前置确认（必问）

必须在动手前确认：

1. **SSH 目标**：`root@HOST`，是否能免密登录
2. **部署范围**：允许落盘目录（默认 `/root/CLIProxyAPI` + `/root/.cli-proxy-api`）
3. **服务端口**：默认 `8317`
4. **访问策略**：
   - `localhost only`（host=127.0.0.1，走 SSH 隧道）
   - `公网直连`（需要 UFW 放行 + 必须换随机 key）
5. **登录路径**：
   - A. 远端 OAuth（需 SSH 端口转发 + 本机浏览器配合，5 分钟超时窗口）
   - B. 本地登录后同步 `~/.cli-proxy-api/*.json` 到 VPS（更稳，推荐）

降级路径：若用户不指定，默认使用 `公网直连 + 本地登录同步`，并在启动后立即轮换随机 key。

---

## 1. 远端环境检查（只读）

```bash
ssh -i <KEY> <SSH_TARGET> "uname -a && . /etc/os-release 2>/dev/null; \
  command -v go && go version || echo 'NO_GO'; \
  command -v git || echo 'NO_GIT'; \
  command -v ufw && ufw status | head -n 20 || echo 'NO_UFW'; \
  ss -ltn | grep ':<PORT>' || echo 'PORT_FREE'"
```

判定：
- 没有 Go → 第 2 步安装
- 端口占用 → 确认是否旧进程，不要盲杀
- UFW active → 记录当前规则（避免在放行后改动其他端口）

## 2. 安装 Go + Git（Ubuntu/Debian）

```bash
ssh -i <KEY> <SSH_TARGET> "apt-get update && apt-get install -y golang-go git"
```

注意：
- 项目 `go.mod` 可能要求 Go 1.26+，系统 apt 的 Go 版本偏旧**没关系** —— `go run` 会自动下载 toolchain。
- 若不希望 GOTOOLCHAIN 自动下载，改装官方 tarball 到 `/usr/local/go`，并 `export PATH=/usr/local/go/bin:$PATH`。

## 3. 克隆仓库

```bash
ssh -i <KEY> <SSH_TARGET> "rm -rf /root/CLIProxyAPI && \
  git clone https://github.com/router-for-me/CLIProxyAPI.git /root/CLIProxyAPI && \
  cd /root/CLIProxyAPI && git rev-parse --short HEAD"
```

## 4. 最小配置

复制 `config.example.yaml` → `config.yaml`，只调这几项：

```yaml
host: ""                          # 公网直连；仅 localhost 改 "127.0.0.1"
port: 8317
auth-dir: "~/.cli-proxy-api"
api-keys:
  - "PLACEHOLDER_WILL_ROTATE"     # 启动前后立即用第 8 步轮换
debug: false
proxy-url: ""
```

远端执行：

```bash
ssh -i <KEY> <SSH_TARGET> "cd /root/CLIProxyAPI && \
  test -f config.yaml || cp config.example.yaml config.yaml"
```

## 5. 获取认证凭据（二选一）

### 5A：本地登录 → 同步凭据（推荐）

本机执行（需本机有源码或已编译好的 `cli-proxy-api`）：

```bash
go run ./cmd/server -codex-login -config config.yaml
# 或 -claude-login / -login(Gemini) / -qwen-login / -iflow-login / -antigravity-login
```

成功后凭据落在 `~/.cli-proxy-api/<provider>-<email>.json`。

同步到 VPS：

```bash
ssh -i <KEY> <SSH_TARGET> 'mkdir -p /root/.cli-proxy-api'
scp -i <KEY> ~/.cli-proxy-api/<provider>-*.json <SSH_TARGET>:/root/.cli-proxy-api/
ssh -i <KEY> <SSH_TARGET> 'ls -l /root/.cli-proxy-api/'
```

### 5B：远端 OAuth（无本地可用时的备选）

远端发起：

```bash
ssh -tt -i <KEY> <SSH_TARGET> \
  "cd /root/CLIProxyAPI && /usr/bin/go run ./cmd/server -<provider>-login -no-browser -config config.yaml"
```

关键点：
- **回调端口固定**：Codex=1455，Claude=54545，iFlow=11451，Gemini=8085
- 本机新终端开隧道（同一端口）：
  ```bash
  ssh -i <KEY> -L <CALLBACK_PORT>:127.0.0.1:<CALLBACK_PORT> <SSH_TARGET>
  ```
- 本机浏览器打开远端打印的授权 URL，完成授权 → 自动回调到远端
- 程序有 **5 分钟超时**，开始前先把隧道和浏览器都准备好
- 若自动回调失败：把浏览器最终跳转到的 `http://localhost:<PORT>/...` 整个 URL 粘回远端交互提示

降级路径：5B 失败两次就切到 5A，不再继续试。

## 6. 启动服务（后台）

```bash
ssh -i <KEY> <SSH_TARGET> "cd /root/CLIProxyAPI && \
  nohup /usr/bin/go run ./cmd/server -config config.yaml \
    >/root/CLIProxyAPI/cli-proxy-api.log 2>&1 </dev/null & \
  echo \$! > /root/CLIProxyAPI/cli-proxy-api.pid"
```

验证监听与日志：

```bash
ssh -i <KEY> <SSH_TARGET> "lsof -i:<PORT>; tail -n 40 /root/CLIProxyAPI/cli-proxy-api.log"
```

必须看到：`API server started successfully on: :<PORT>` + `N auth files` ≥ 1。

## 7. 放行防火墙（公网直连时）

UFW 默认 `deny incoming`，即使端口监听了，公网依然会 `Empty reply from server`。**这是公网直连失败的最常见根因**。

```bash
ssh -i <KEY> <SSH_TARGET> "ufw allow <PORT>/tcp && ufw status | grep <PORT>"
```

仅 localhost 模式则**跳过**本步，并保持 `host: "127.0.0.1"`。

## 8. 轮换访问密钥（强烈建议）

绝不保留 `your-api-key-1` 默认值。生成随机 key：

```bash
python3 -c "import secrets; print('cpa_' + secrets.token_urlsafe(24))"
```

远端用 Python 原位替换 `api-keys:` 段（避免 sed 多行坑）：

```bash
ssh -i <KEY> <SSH_TARGET> "python3 - <<'PY'
from pathlib import Path
cfg = Path('/root/CLIProxyAPI/config.yaml')
new_key = '<NEW_KEY>'
lines = cfg.read_text().splitlines()
out, in_api = [], False
for line in lines:
    s = line.strip()
    if s.startswith('api-keys:'):
        out += ['api-keys:', f'  - \"{new_key}\"']
        in_api = True
        continue
    if in_api:
        if line.startswith('  - ') or not s or line.startswith('    '):
            continue
        in_api = False
    out.append(line)
cfg.write_text('\n'.join(out) + '\n')
PY"
```

CLIProxyAPI 支持配置热重载（见 `service.go` 的 file watcher），日志里会出现 `config file changed, reloading`，**不必重启**。若未热重载成功，再手动 `pkill -f 'cmd/server -config'` 并按第 6 步重启。

## 9. 健康校验（必须本会话命令证据）

### 9a. 内网（不受 UFW 影响）
```bash
ssh -i <KEY> <SSH_TARGET> "curl -fsS -H 'Authorization: Bearer <NEW_KEY>' \
  http://127.0.0.1:<PORT>/v1/models | head -c 400"
```

### 9b. 公网直连
```bash
curl -sS -i --max-time 30 http://<HOST>:<PORT>/v1/chat/completions \
  -H 'Authorization: Bearer <NEW_KEY>' -H 'Content-Type: application/json' \
  --data '{"model":"<MODEL>","messages":[{"role":"user","content":"请只回复 OK"}],"stream":false}'
```

必须满足：
- HTTP 200
- `choices[0].message.content` 含可读字符（非空、非 error）

任一不满足都不得声称“部署完成”。

## 10. 客户端环境变量

追加到 `~/.zshrc`（或 `~/.bashrc`）：

```bash
# CLIProxyAPI
export BASE_URL="http://<HOST>:<PORT>/v1"      # localhost 模式改 http://127.0.0.1:<PORT>/v1
export BASE_API_KEY="<NEW_KEY>"
export BASE_MODEL="<MODEL>"                    # 如 gpt-5.4 / claude-sonnet-4-5-...
```

随后：`source ~/.zshrc`。

---

## 排障速查

| 症状 | 最可能根因 | 验证 / 修复 |
|------|-----------|-----------|
| 公网 `Empty reply from server`，但远端 `127.0.0.1` 能通 | UFW 默认 deny，未放行端口 | `ufw status` → `ufw allow <PORT>/tcp` |
| 公网 `Connection refused` | 服务 host 绑 `127.0.0.1`，或进程没起 | 看 `lsof -i:<PORT>` 是否为 `*:<PORT>`，或改 host 后重启 |
| OAuth `Authentication timed out` | 5 分钟内未完成浏览器授权 + 隧道 | 改走 5A 本地登录同步 |
| OAuth 卡在 `exchanging for tokens` | 本机到 `auth.openai.com` / `claude.ai` 被代理或拦截 | 清 `proxy-url`，`curl -I https://auth.openai.com/oauth/token` 验证 |
| 启动日志 `0 auth files` | `auth-dir` 路径错 or 文件权限不足 | 核对 `~/.cli-proxy-api` 实际解析路径与文件属主 |
| `/v1/models` 401 | key 没用上当前 `config.yaml` 或热重载没生效 | `grep -nA2 '^api-keys:' config.yaml`，必要时重启 |
| 端口已被占用 | 旧进程未退出 | `lsof -i:<PORT>` → 针对性 kill，不要 `pkill -9 go` |

---

## 不要做的事

- ❌ 保留默认示例 key（`your-api-key-1`）上线
- ❌ 在没放行 UFW 的前提下宣布“公网可用”
- ❌ 直接 `pkill -9 go`（会误杀其他 Go 进程）
- ❌ 用 `sed -i` 改 `api-keys:` 多行段，容易残留旧行
- ❌ 将完整 key 贴回聊天（除非用户明确要求“直接给我完整值”一次）
- ❌ 跨会话声称“已部署”——必须重新跑第 9 步拿当次证据

---

## 参考事实（代码锚点，2026-04）

- 启动入口：`cmd/server/main.go:53` `main()`；登录参数 `-login/-codex-login/-claude-login/-qwen-login/-iflow-login/-antigravity-login/-no-browser/-config`
- 默认认证目录：`config.example.yaml` `auth-dir: "~/.cli-proxy-api"`
- 默认端口：`config.example.yaml` `port: 8317`
- 回调端口：Codex `sdk/auth/codex.go:27` = 1455；Claude `sdk/auth/claude.go:27` = 54545；iFlow `internal/auth/iflow/iflow_auth.go:42` = 11451；Gemini `internal/auth/gemini/gemini_auth.go:280` = 8085
- 凭据文件名：`codex-<email>.json` / `claude-<email>.json` / `qwen-<email>.json` / `iflow-<email>-<ts>.json`
- 热重载：`internal/watcher/*`（修改 `config.yaml` 或 auth-dir 下 JSON 触发）
- 路由：`internal/api/server.go:321` `setupRoutes()`（`/v1/*` 需 `AuthMiddleware`）
