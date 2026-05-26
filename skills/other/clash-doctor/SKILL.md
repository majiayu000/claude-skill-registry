---
name: clash-doctor
description: Clash Verge 诊断与配置管理。网络诊断、配置 AI 工具路由规则（Claude/Codex/Cursor/Warp）、查看/克隆订阅配置、切换配置文件。当用户遇到网络问题、要配置代理规则、切换订阅、查看 Clash 配置时使用
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
metadata:
  argument-hint: '[诊断域名 | profiles | clone <源> <目标> | setup-ai <订阅名> | switch <订阅名>]'
---

# Clash Verge 诊断与配置管理

你是一个 Clash Verge（mihomo 内核）的诊断和配置管理专家。

用户传入的参数：$ARGUMENTS

## 路径常量

```
VERGE_DIR=~/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev
PROFILES_INDEX=$VERGE_DIR/profiles.yaml
PROFILES_DIR=$VERGE_DIR/profiles
VERGE_YAML=$VERGE_DIR/verge.yaml
MIHOMO_API=http://127.0.0.1:9097
```

## 命令路由

根据 $ARGUMENTS 判断执行哪个模式：

| 参数模式 | 执行模式 |
|----------|----------|
| 无参数 或 域名（如 `github.com`） | **诊断模式** |
| `profiles` 或 `list` 或 `ls` | **配置文件列表** |
| `clone <源订阅名> <目标订阅名>` | **克隆覆盖配置** |
| `setup-ai <订阅名>` | **配置 AI 工具路由** |
| `switch <订阅名>` | **切换激活配置** |
| `status` | **当前状态概览** |

---

## 模式一：配置文件列表（profiles）

读取 `$PROFILES_INDEX`，列出所有 remote 类型的订阅，展示：

```
订阅名称 | UID | 流量使用 | 到期时间 | 覆盖文件状态 | 是否激活
```

**覆盖文件状态**判断：读取每个订阅的 option 中关联的 merge/rules/proxies/groups 文件，检查内容是否为空模板。

空模板判断标准（以下均视为"未配置"）：
- merge：只有注释行 + 空行
- rules：`prepend: []` 且 `append: []`
- proxies：`prepend: []` 且 `append: []`
- groups：`prepend: []` 且 `append: []`
- script：只有 `return config;`

输出格式示例：
```
📋 Clash Verge 订阅列表

  订阅名              流量          到期        覆盖状态        激活
─────────────────────────────────────────────────────────────────
★ Nexitally         179/500 GB    2026-03-01  ✅ 全配置       ← 当前
  灰狐云互联         57/200 GB     2027-03-04  ✅ 全配置
  YToo_SS            0/15 GB       2027-03-25  ✅ 全配置

覆盖详情：
  merge=DNS/TUN  rules=AI路由  proxies=住宅代理  groups=AI组
```

---

## 模式二：克隆覆盖配置（clone）

将源订阅的 5 个覆盖文件（merge/script/rules/proxies/groups）内容复制到目标订阅的对应覆盖文件。

**步骤**：
1. 读取 `$PROFILES_INDEX`，通过订阅名（name 字段模糊匹配）找到源和目标的 UID
2. 从源订阅的 option 中找到 merge/script/rules/proxies/groups 的 UID
3. 从目标订阅的 option 中找到对应的 UID
4. 逐个读取源文件内容，写入目标文件
5. **写入前确认**：列出将要覆盖的文件和内容摘要，等用户确认

**注意事项**：
- rules 中的 `delete` 部分可能需要适配（源订阅的原始规则和目标可能不同）
- merge 中的 TUN route-exclude-address 应保留（住宅代理 IP 防回环）
- 如果目标覆盖文件已有非空内容，警告用户将被覆盖

---

## 模式三：配置 AI 工具路由（setup-ai）

为指定订阅配置完整的 AI 开发工具代理路由。这是最常用的配置操作。

**步骤**：
1. 读取 `$PROFILES_INDEX`，通过订阅名找到目标 UID 和关联的覆盖文件 UID
2. 读取当前激活订阅的覆盖文件作为模板（如果有已配置的）
3. 如果没有现成模板，使用内置的 AI 路由规则集（见下方）
4. 写入 4 个覆盖文件（merge/rules/proxies/groups）
5. 提示用户在 Clash Verge 中 reload 配置

### 内置 AI 路由规则集

#### Rules（prepend 最高优先级）

```yaml
prepend:
  # --- Claude Code CLI ---
  - PROCESS-NAME,claude,AI
  - PROCESS-NAME,Claude,AI
  - PROCESS-NAME,Claude Helper,AI
  - PROCESS-NAME,Claude Helper (GPU),AI
  - PROCESS-NAME,Claude Helper (Renderer),AI
  - PROCESS-NAME,Claude Helper (Plugin),AI
  # --- Codex CLI ---
  - PROCESS-NAME,codex,Proxies
  - PROCESS-NAME,Codex,Proxies
  - PROCESS-NAME,Codex Helper,Proxies
  # --- Cursor ---
  - DOMAIN,marketplace.cursorapi.com,AI
  - DOMAIN,api2.cursor.sh,AI
  # --- Warp Terminal ---
  - PROCESS-NAME,stable,AI
  - PROCESS-NAME,Warp,AI
  - DOMAIN-SUFFIX,warp.dev,AI
  - DOMAIN-SUFFIX,app.warp.dev,AI
  - DOMAIN,rtc.app.warp.dev,AI
  # --- Anthropic 全域名 ---
  - DOMAIN-SUFFIX,anthropic.com,AI
  - DOMAIN-SUFFIX,claude.ai,AI
  - DOMAIN-SUFFIX,claudeusercontent.com,AI
  - DOMAIN-SUFFIX,claude.com,AI
  - DOMAIN,api.anthropic.com,AI
  - DOMAIN,console.anthropic.com,AI
  - DOMAIN,platform.claude.com,AI
  - DOMAIN,status.anthropic.com,AI
  - DOMAIN,anthropic.statuspage.io,AI
  - DOMAIN-SUFFIX,support.claude.com,AI
  - DOMAIN-SUFFIX,support.anthropic.com,AI
  - DOMAIN-SUFFIX,docs.claude.com,AI
  - DOMAIN-SUFFIX,anthropic.mintlify.app,AI
  - DOMAIN,cloudcode-pa.googleapis.com,AI
  - DOMAIN,daily-cloudcode-pa.googleapis.com,AI
  - DOMAIN,clau.de,AI
  - DOMAIN-KEYWORD,anthropic,AI
  - DOMAIN-KEYWORD,claude,AI
  # --- GitHub Education ---
  - DOMAIN,education.github.com,AI
  # --- Tailscale DIRECT ---
  - IP-CIDR,100.64.0.0/10,DIRECT,no-resolve
  - IP-CIDR6,fd7a:115c:a1e0::/48,DIRECT,no-resolve
  # --- Supabase DIRECT ---
  - DOMAIN-SUFFIX,supabase.co,DIRECT
  - DOMAIN-SUFFIX,supabase.com,DIRECT
```

#### Rules delete（清理原始订阅中可能存在的冲突规则）

```yaml
delete:
  - DOMAIN-SUFFIX,anthropic.com,Proxies
  - DOMAIN-SUFFIX,claude.ai,Proxies
  - DOMAIN-SUFFIX,claude.com,Proxies
  - DOMAIN,api.anthropic.com,Proxies
  - DOMAIN,console.anthropic.com,Proxies
  - DOMAIN,platform.claude.com,Proxies
  - DOMAIN,daily-cloudcode-pa.googleapis.com,Proxies
  - DOMAIN-SUFFIX,support.claude.com,Proxies
  - DOMAIN-SUFFIX,support.anthropic.com,Proxies
  - DOMAIN-SUFFIX,docs.claude.com,Proxies
  - DOMAIN-SUFFIX,anthropic.mintlify.app,Proxies
  - PROCESS-PATH-KEYWORD,Claude.app,AI
  - PROCESS-PATH-KEYWORD,Codex.app,Proxies
```

#### Proxies（住宅代理节点配置）

**优先级**：
1. 读取当前激活订阅的 proxies 覆盖文件，如有住宅代理节点则直接复制
2. 如无已配置的住宅代理，进入**交互式配置流程**：

**交互式配置流程**：
向用户询问以下信息（逐项或一次性提供均可）：

```
需要你提供住宅代理信息：
1. 代理类型（socks5/http，默认 socks5）
2. 服务器地址（IP 或域名）
3. 端口
4. 用户名（如有）
5. 密码（如有）
6. 节点显示名（默认 🏠 Residential US (AI)）

示例：socks5 / 1.2.3.4 / 44539 / myuser / mypass
```

用户提供后生成 Proxies 覆盖：

```yaml
prepend: []

append:
  - name: <节点显示名>
    type: <代理类型>
    server: <服务器地址>
    port: <端口>
    username: <用户名>
    password: <密码>
    udp: true

delete: []
```

**注意**：同时自动将代理服务器 IP 写入 Merge 的 `route-exclude-address`（TUN 防回环）。

#### Groups

```yaml
append:
  - name: AI
    type: select
    url: http://www.gstatic.com/generate_204
    proxies:
      # 从 proxies 覆盖中提取住宅代理名称填入
      - <住宅代理节点名>

delete:
  - AI  # 删除原始订阅中可能存在的同名组，确保使用自定义版本
```

#### Merge

```yaml
tun:
  route-exclude-address:
    # 住宅代理服务器 IP，防止 TUN 回环
    - <住宅代理IP>/32
```

---

## 模式四：切换激活配置（switch）

1. 读取 `$PROFILES_INDEX`，通过订阅名找到目标 UID
2. **确认**：告知用户将从当前订阅切换到目标订阅，列出目标订阅的覆盖配置状态
3. 如果目标订阅覆盖文件为空，警告用户可能缺少 AI 路由规则
4. 修改 `$PROFILES_INDEX` 的 `current` 字段为目标 UID
5. 提示用户在 Clash Verge 中 reload 或重启

---

## 模式五：当前状态概览（status）

并行采集：
1. 读取 `$PROFILES_INDEX` → 当前激活的订阅名和流量
2. 读取 `$VERGE_YAML` → TUN/系统代理/端口配置
3. `curl -s $MIHOMO_API/version` → mihomo 版本
4. `curl -s $MIHOMO_API/proxies` → 当前选中的节点

输出格式：
```
🔍 Clash Verge 状态

内核: mihomo v1.x.x
激活订阅: Nexitally (179/500 GB, 到期 2026-03-01)
模式: rule
端口: mixed=7897 socks=7898 http=7899
TUN: ✅ 开启 (stack=mixed)
系统代理: ✅ 开启

当前节点:
  Proxies → 🇭🇰 Hong Kong 02
  Google  → 🇺🇸 USA Seattle 03
  AI      → 🏠 Residential US (AI)
```

---

## 模式六：诊断模式（默认）

当参数为空或为域名时，执行网络诊断。默认目标为 `github.com`。

### 第一步：采集环境信息

**并行执行以下所有检查命令：**

1. **Shell 代理环境变量**
```bash
env | grep -i -E '(proxy|PROXY|http_proxy|https_proxy|all_proxy|no_proxy|ALL_PROXY|HTTP_PROXY|HTTPS_PROXY|NO_PROXY)' || echo "[结果] 无代理环境变量"
```

2. **macOS 系统代理设置**（检测当前活跃的网络接口）
```bash
ACTIVE_IF=$(route -n get default 2>/dev/null | awk '/interface:/{print $2}')
ACTIVE_SERVICE=$(networksetup -listallhardwareports | awk -v dev="$ACTIVE_IF" '/Hardware Port/{port=$0} /Device:/{if($2==dev) print port}' | sed 's/Hardware Port: //')
echo "活跃接口: $ACTIVE_IF ($ACTIVE_SERVICE)"
echo "=== Web Proxy ==="
networksetup -getwebproxy "$ACTIVE_SERVICE" 2>/dev/null
echo "=== Secure Web Proxy ==="
networksetup -getsecurewebproxy "$ACTIVE_SERVICE" 2>/dev/null
echo "=== SOCKS Proxy ==="
networksetup -getsocksfirewallproxy "$ACTIVE_SERVICE" 2>/dev/null
```

3. **DNS 解析对比**
```bash
TARGET="目标域名"
echo "=== 本地 DNS ==="
nslookup $TARGET 2>&1
echo "=== 外部 DNS (8.8.8.8) ==="
nslookup $TARGET 8.8.8.8 2>&1
echo "=== 外部 DNS (1.1.1.1) ==="
nslookup $TARGET 1.1.1.1 2>&1
```

4. **Git 代理配置**
```bash
echo "=== git http.proxy ==="
git config --global --get http.proxy 2>/dev/null || echo "未设置"
echo "=== git https.proxy ==="
git config --global --get https.proxy 2>/dev/null || echo "未设置"
```

5. **常见代理端口扫描**
```bash
for port in 7890 7891 7897 7898 7899 1080 1087 9090 9097 2080; do
  result=$(lsof -i :$port -sTCP:LISTEN 2>/dev/null | head -3)
  if [ -n "$result" ]; then
    echo "[端口 $port] 在监听:"
    echo "$result"
  fi
done
echo "=== 扫描完成 ==="
```

### 第二步：连通性测试

**并行执行以下测试：**

1. **直连测试**（不走代理）
```bash
TARGET="目标域名"
curl --noproxy '*' --connect-timeout 5 -s -o /dev/null -w "直连: HTTP=%{http_code} 耗时=%{time_total}s IP=%{remote_ip}\n" https://$TARGET 2>&1 || echo "直连: 失败(超时或拒绝)"
```

2. **通过代理测试**（对每个发现的监听端口测试）
```bash
TARGET="目标域名"
curl -x http://127.0.0.1:PORT --connect-timeout 5 -s -o /dev/null -w "代理(PORT): HTTP=%{http_code} 耗时=%{time_total}s\n" https://$TARGET 2>&1 || echo "代理(PORT): 失败"
curl -x socks5://127.0.0.1:PORT --connect-timeout 5 -s -o /dev/null -w "SOCKS5(PORT): HTTP=%{http_code} 耗时=%{time_total}s\n" https://$TARGET 2>&1 || echo "SOCKS5(PORT): 失败"
```

3. **Ping 测试**
```bash
TARGET="目标域名"
ping -c 3 -W 3 $TARGET 2>&1
```

4. **Clash API 状态检查**
```bash
curl -s $MIHOMO_API/version 2>/dev/null && echo ""
curl -s $MIHOMO_API/proxies 2>/dev/null | head -c 500
```

### 第三步：综合诊断

#### 判断矩阵

| DNS 结果 | 直连 | 代理 | 系统代理 | 诊断 |
|----------|------|------|----------|------|
| 198.18.x.x (fake-ip) | 超时 | 正常 | 关闭 | **TUN 模式 DNS 劫持生效但流量拦截失败，且系统代理未开启** |
| 198.18.x.x (fake-ip) | 超时 | 超时 | 关闭 | **代理软件整体异常，需要重启** |
| 198.18.x.x (fake-ip) | 正常 | 正常 | 任意 | **TUN 模式正常工作** |
| 正常 IP | 超时 | 正常 | 关闭 | **需要开启系统代理或设置环境变量** |
| 正常 IP | 超时 | 超时 | 开启 | **代理节点本身有问题，需要切换节点** |
| 正常 IP | 正常 | - | - | **网络正常，问题可能在浏览器/应用层** |

#### fake-ip 识别规则

- `198.18.0.0/15`（最常见）
- `28.0.0.0/8`
- `10.0.0.0/8`（需要结合延迟判断，ping < 1ms 基本是 fake-ip）

#### 诊断输出格式

1. **问题概述**：一句话总结当前网络状态
2. **详细分析**：逐项说明每个检查结果的含义
3. **根因**：指出问题的根本原因
4. **解决方案**：按优先级列出解决方法，包含具体操作步骤

---

## 常见问题的解决方案模板

### TUN 模式异常（DNS 劫持生效但流量不通）
```
根因：Clash TUN 模式的 DNS 劫持仍在工作（域名被解析为 fake-ip），
      但 TUN 虚拟网卡未正确拦截流量，导致连接直接发往 fake-ip 后超时。

解决方案（按优先级）：
1. 重启代理软件（Clash Verge / mihomo）
2. 如果重启无效，关闭 TUN 模式，改用系统代理模式
3. 开启 System Proxy（系统代理）开关
4. 如果是 macOS，检查是否需要重新授权网络扩展：
   系统设置 → 隐私与安全性 → 网络扩展
```

### 系统代理未开启
```
解决方案：
1. 在代理客户端中开启「System Proxy / 系统代理」
2. 或手动设置：
   networksetup -setwebproxy "Wi-Fi" 127.0.0.1 PORT
   networksetup -setsecurewebproxy "Wi-Fi" 127.0.0.1 PORT
```

### 代理节点不可用
```
解决方案：
1. 在 Clash 控制面板中切换到其他节点
2. 测试延迟：在 Clash 中点击「测速」
3. 如果所有节点都不行，检查订阅是否过期
```

### Shell/Git 代理环境变量缺失
```
解决方案：
在 ~/.zshrc 中添加：
  export http_proxy=http://127.0.0.1:7897
  export https_proxy=http://127.0.0.1:7897
  export all_proxy=socks5://127.0.0.1:7898
```

---

## 已知流量模式

### Chrome QUIC/HTTP3 (UDP 443) 产生无法匹配的连接

**现象**：连接表中出现随机域名（如 `8dc9ef6261.n2hlutbws.sbs:443`），类型为 `Tun(udp)`，下载量为 0。

**原因**：Chrome QUIC 协议使用 UDP 443，sniffer 嗅探到 Google QUIC 代理域名（随机字符串），不匹配任何规则。

**解决**（仅在需要时）：Chrome `chrome://flags/#enable-quic` → Disabled → 重启。

### parse-pure-ip 导致所有连接无域名

**现象**：连接表中 `host` 和 `sniffHost` 全部为空。

**修复**：在 merge 覆盖文件中设置：
```yaml
sniffer:
  parse-pure-ip: true
```
修改后**重启 Clash Verge 应用**（不是 reload）。

---

## 注意事项

- **诊断操作是只读的**，不修改任何配置
- **配置操作需要确认**：写入覆盖文件前必须展示将要写入的内容摘要，等用户确认
- **切换订阅需要确认**：展示目标订阅的覆盖状态，警告可能缺失的配置
- **不要修改原始订阅文件**（`RxQXGGBzmzSb.yaml` 等），只修改覆盖文件（merge/rules/proxies/groups/script）
- **住宅代理凭证敏感**：克隆时提醒用户覆盖文件包含代理凭证
- 用中文输出所有信息
- 端口以 `$VERGE_YAML` 中的实际配置为准（mixed=7897, socks=7898, http=7899, API=9097）
