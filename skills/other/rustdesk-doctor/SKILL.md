---
name: rustdesk-doctor
description: 诊断 RustDesk 连接问题。当用户说 RustDesk 连不上、无法远程、ID 不显示、注册失败时使用
allowed-tools: Bash, Read, Edit, Write
metadata:
  argument-hint: "[自建服务器IP，如 124.221.234.205]"
---

# RustDesk 连接诊断工具

诊断 RustDesk 客户端无法连接服务器的问题，覆盖 Clash/TUN 代理干扰、服务器端配置、云安全组等常见根因。

用户传入的参数（如有）：$ARGUMENTS

## 诊断流程

严格按以下步骤执行，每一步都要执行并记录结果，最后给出综合诊断。

### 第一步：采集客户端状态

**并行执行以下检查：**

1. **RustDesk 进程和网络连接**
```bash
ps aux | grep -i rustdesk | grep -v grep
echo "=== 网络连接 ==="
lsof -i -P -n 2>/dev/null | grep -i rustdesk
```

2. **RustDesk 配置文件**
```bash
CONFIG_DIR="$HOME/Library/Preferences/com.carriez.RustDesk"
echo "=== RustDesk2.toml ==="
cat "$CONFIG_DIR/RustDesk2.toml" 2>/dev/null || echo "文件不存在"
echo "=== RustDesk_local.toml ==="
cat "$CONFIG_DIR/RustDesk_local.toml" 2>/dev/null || echo "文件不存在"
```

3. **RustDesk 最新日志（关键行）**
```bash
LOG="$HOME/Library/Logs/RustDesk/RustDesk_rCURRENT.log"
cat "$LOG" 2>/dev/null || echo "日志不存在"
```

### 第二步：检查 Clash/代理干扰

**并行执行以下检查：**

1. **Mihomo 中 RustDesk 的连接和规则匹配**
```bash
SOCKET="/var/tmp/verge/verge-mihomo.sock"
if [ -S "$SOCKET" ]; then
  curl -s --unix-socket "$SOCKET" http://localhost/connections 2>/dev/null | python3 -c "
import sys,json
data=json.load(sys.stdin)
conns=data.get('connections',[])
found=False
for c in conns:
    meta=c.get('metadata',{})
    proc=meta.get('process','').lower()
    host=meta.get('host','').lower()
    dst=meta.get('destinationIP','')
    if 'rustdesk' in proc or 'rustdesk' in host or '21116' in meta.get('destinationPort','') or '21115' in meta.get('destinationPort',''):
        chains=c.get('chains',[])
        rule=c.get('rule','')
        rp=c.get('rulePayload','')
        net=meta.get('network','')
        dp=meta.get('destinationPort','')
        print(f'{meta.get(\"process\",\"\")} | {net} | {host or dst}:{dp} | rule={rule} {rp} | chains={chains}')
        found=True
if not found:
    print('Mihomo 中没有 RustDesk 相关连接')
"
else
  echo "Mihomo unix socket 不存在，Clash 可能未运行"
fi
```

2. **Mihomo 中 RustDesk 相关规则**
```bash
SOCKET="/var/tmp/verge/verge-mihomo.sock"
if [ -S "$SOCKET" ]; then
  curl -s --unix-socket "$SOCKET" http://localhost/rules 2>/dev/null | python3 -c "
import sys,json
rules=json.load(sys.stdin).get('rules',[])
for r in rules:
    p=str(r.get('payload','')).lower()
    if 'rustdesk' in p:
        print(f\"{r.get('type')},{r.get('payload')},{r.get('proxy')}\")
" || echo "无法获取规则"
  echo "=== TUN 配置 ==="
  curl -s --unix-socket "$SOCKET" http://localhost/configs 2>/dev/null | python3 -c "
import sys,json
c=json.load(sys.stdin)
tun=c.get('tun',{})
print('TUN enabled:', tun.get('enable'))
rea=tun.get('route-exclude-address',[])
if rea:
    print('route-exclude-address:', rea)
"
fi
```

3. **DNS 解析检查（fake-ip 检测）**

对 RustDesk 服务器域名进行 DNS 解析，检查是否返回 fake-ip (198.18.x.x)：
```bash
# 如果配置了自建服务器（IP 地址），跳过域名解析
# 如果使用默认公共服务器，检查 rs-ny.rustdesk.com
nslookup rs-ny.rustdesk.com 2>&1
nslookup rustdesk.com 2>&1
```

4. **路由检查**

检查 RustDesk 服务器 IP 的路由走向（是否经过 TUN utun1024）：
```bash
# 对配置中的服务器 IP 执行 route get
# 如果走 utun1024 → TUN 拦截
# 如果走 en0 → 直连
route -n get <服务器IP> 2>&1 | head -6
```

5. **Clash Verge profiles 中的 RustDesk 配置**
```bash
PROFILES_DIR="$HOME/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/profiles"
grep -ril "rustdesk" "$PROFILES_DIR/"*.yaml "$PROFILES_DIR/"*.js 2>/dev/null | while read f; do
  echo "=== $(basename $f) ==="
  grep -in "rustdesk" "$f"
done
```

### 第三步：网络连通性测试

**对配置中的服务器（自建或默认公共服务器）执行：**

```bash
SERVER="<服务器IP或域名>"
echo "=== TCP 21115 (NAT test) ==="
nc -z -w5 $SERVER 21115 2>&1 && echo "OK" || echo "FAIL"
echo "=== TCP 21116 (rendezvous) ==="
nc -z -w5 $SERVER 21116 2>&1 && echo "OK" || echo "FAIL"
echo "=== TCP 21117 (relay) ==="
nc -z -w5 $SERVER 21117 2>&1 && echo "OK" || echo "FAIL"
echo "=== UDP 21116 ==="
nc -z -w5 -u $SERVER 21116 2>&1 && echo "OK" || echo "FAIL（UDP 结果可能不准确）"
echo "=== 路由走向 ==="
route -n get $SERVER 2>&1 | head -6
```

### 第四步：服务器端检查（如可 SSH）

如果用户提供了自建服务器 IP 且可以 SSH，执行以下检查：

```bash
SERVER="<服务器IP>"
ssh -o ConnectTimeout=10 root@$SERVER "
echo '=== Docker 容器状态 ==='
docker ps | grep -i rust
echo '=== hbbs 日志（最后 20 行）==='
docker logs hbbs --tail 20 2>&1
echo '=== hbbr 日志（最后 10 行）==='
docker logs hbbr --tail 10 2>&1
echo '=== 端口监听 ==='
ss -ulnp | grep 21116
ss -tlnp | grep -E '2111[5-9]'
echo '=== 公钥 ==='
cat /root/id_ed25519.pub 2>/dev/null || find / -name 'id_ed25519.pub' 2>/dev/null | head -1 | xargs cat 2>/dev/null
echo '=== UFW 状态 ==='
ufw status 2>/dev/null | head -15
echo '=== 云安全组防火墙链 ==='
iptables -L INPUT -n 2>/dev/null | head -5
echo '=== 抓包测试（10秒）==='
timeout 10 tcpdump -i eth0 -c 5 udp port 21116 2>&1
"
```

### 第五步：local-ip-addr 检查

检查 RustDesk 是否把 TUN 网关 IP 当成了本机 IP：

```bash
CONFIG="$HOME/Library/Preferences/com.carriez.RustDesk/RustDesk2.toml"
LOCAL_IP=$(grep 'local-ip-addr' "$CONFIG" 2>/dev/null | awk -F"'" '{print $2}')
if [ "$LOCAL_IP" = "198.18.0.1" ]; then
  echo "WARNING: local-ip-addr = 198.18.0.1 (TUN 网关假 IP)"
  echo "RustDesk 启动时检测到 TUN 虚拟网卡 IP，需要在 TUN 关闭时启动 RustDesk"
  REAL_IP=$(ifconfig en0 2>/dev/null | grep 'inet ' | awk '{print $2}')
  echo "真实 IP 应该是: $REAL_IP"
elif [ -n "$LOCAL_IP" ]; then
  echo "local-ip-addr = $LOCAL_IP"
else
  echo "local-ip-addr 未设置（自动检测）"
fi
```

## 综合诊断

根据采集到的所有信息，按以下判断矩阵分析：

### 常见问题判断矩阵

| 日志关键行 | 网络状态 | Clash 状态 | 诊断 |
|-----------|---------|-----------|------|
| `register_pk ... key not confirmed` 持续重试 | 端口不通 | 走 DIRECT | **TUN DIRECT UDP 转发异常或服务器不可达** |
| `register_pk ... key not confirmed` 持续重试 | 端口通 | 走 Proxies | **代理节点不支持 RustDesk UDP 协议** |
| `register_pk ... key not confirmed` + 服务器 tcpdump 零包 | SSH 通，其他端口不通 | - | **云安全组未放行 21115-21117/tcp 和 21116/udp** |
| `Got nat response` 有回复但 `register_pk` 失败 | UDP 通，TCP 21115 不通 | 走 Proxies | **代理对裸 TCP 转发不完整，需加 IP-CIDR 规则** |
| `Failed to connect to ...:21115` | TCP 不通 | - | **TCP 21115 被阻断（代理/防火墙/安全组）** |
| `local-ip-addr = 198.18.0.1` | - | TUN 开启 | **TUN 假 IP 污染，关 TUN 重启 RustDesk 或清空该字段** |
| `error sending request for url (https://api.rustdesk.com/...)` | HTTPS 不通 | 走 DIRECT | **RustDesk 官方 API 被墙，需走代理** |
| DNS 解析返回 198.18.x.x | - | fake-ip 模式 | **rustdesk.com 需加入 fake-ip-filter 或改用 +.rustdesk.com** |

### 常见解决方案

#### 方案 A：TUN 模式下 DIRECT UDP 不通

TUN 的 DIRECT 出口可能无法正确转发 UDP。解决：

1. 在 Merge.yaml 中加 `route-exclude-address` 让服务器 IP 完全绕过 TUN：
```yaml
tun:
  route-exclude-address:
    - <服务器IP>/32
```

2. 或让 RustDesk 流量走代理（删除订阅中的 DIRECT 规则）

#### 方案 B：订阅配置自带 rustdesk.com DIRECT 规则

订阅可能包含 `DOMAIN-SUFFIX,rustdesk.com,DIRECT`。如需走代理：

在规则 profile 的 `delete` 区加：
```yaml
delete:
  - DOMAIN-SUFFIX,rustdesk.com,DIRECT
```

#### 方案 C：云安全组未开端口

腾讯云/阿里云等安全组在云平台层面过滤，iptables 和 UFW 看不到。需在云控制台添加：

| 协议 | 端口 | 来源 |
|------|------|------|
| TCP | 21115-21117 | 0.0.0.0/0 |
| UDP | 21116 | 0.0.0.0/0 |

#### 方案 D：local-ip-addr 被 TUN 假 IP 污染

RustDesk 启动时检测网卡 IP，TUN 模式下会拿到 198.18.0.1。解决：

1. 关闭 TUN → 启动 RustDesk（让它检测真实 IP）→ 再开 TUN
2. 或手动清空 `RustDesk2.toml` 中的 `local-ip-addr`：
```toml
[options]
local-ip-addr = ''
```

#### 方案 E：代理节点不支持 RustDesk 协议

RustDesk 使用 UDP + 裸 TCP（非 HTTP/TLS），部分代理节点不支持。解决：

1. 切换支持 UDP 的代理节点
2. 对裸 TCP 端口（21115），需加 IP-CIDR 规则让 Mihomo 能路由：
```yaml
prepend:
  - IP-CIDR,<服务器IP>/32,Proxies,no-resolve
```

## RustDesk 端口说明

| 端口 | 协议 | 用途 |
|------|------|------|
| 21114 | TCP | API / Web 控制台（新版） |
| 21115 | TCP | NAT 类型检测 |
| 21116 | TCP+UDP | 会合服务器（注册、信令） |
| 21117 | TCP | 中继转发 |
| 21118 | TCP | WebSocket |
| 21119 | TCP | WebSocket 中继 |

## 注意事项

- 诊断操作全部只读，不修改任何配置
- 修改配置前告知用户并确认
- SSH 到服务器前确认用户授权
- 优先排查：云安全组 > 代理/TUN 干扰 > 服务器端 > 客户端配置
- 用中文输出所有诊断信息
