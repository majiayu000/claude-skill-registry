---
name: clash-routes
description: 查看指定进程的代理线路。通过 Mihomo API 查询当前活跃连接，显示进程匹配的规则和代理链路。用于确认某个进程（如 claude、chrome）走的是哪条订阅线路
allowed-tools: Bash
metadata:
  argument-hint: "[进程名，默认显示全部]"
---

# Clash 线路查看工具

查看当前活跃连接的代理线路信息，确认指定进程走的是哪条订阅/代理链。

用户传入的参数：$ARGUMENTS
如果用户没有传入参数，显示所有活跃连接（按进程分组）。

## 执行流程

### 第一步：获取 Mihomo API 凭证

读取 Clash Verge 配置获取 API secret：

```bash
SECRET=$(grep '^secret:' "/Users/lifcc/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/clash-verge.yaml" 2>/dev/null | awk '{print $2}')
[ -z "$SECRET" ] && SECRET=$(grep '^secret:' "/Users/lifcc/.config/clash/config.yaml" 2>/dev/null | awk '{print $2}')
echo "Secret: ${SECRET:-(未找到)}"
```

### 第二步：查询连接信息

优先使用 Unix socket，fallback 到 HTTP：

```bash
# Unix socket 方式（Clash Verge Rev）
SOCKET="/var/tmp/verge/verge-mihomo.sock"
if [ -S "$SOCKET" ]; then
  CONNECTIONS=$(curl -s --unix-socket "$SOCKET" "http://localhost/connections" -H "Authorization: Bearer $SECRET" 2>/dev/null)
else
  # HTTP fallback
  CONTROLLER=$(grep '^external-controller:' "/Users/lifcc/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/clash-verge.yaml" 2>/dev/null | awk '{print $2}' | tr -d "'\"")
  [ -z "$CONTROLLER" ] && CONTROLLER="127.0.0.1:9090"
  CONNECTIONS=$(curl -s "http://$CONTROLLER/connections" -H "Authorization: Bearer $SECRET" 2>/dev/null)
fi
```

### 第三步：解析并展示线路

用 Python 解析 JSON，按进程分组显示：

```python
import json, sys

data = json.loads(sys.stdin.read())
connections = data.get("connections", [])

# 过滤进程名（如果指定了参数）
process_filter = "参数中的进程名" # 从 $ARGUMENTS 获取

results = []
for conn in connections:
  meta = conn.get("metadata", {})
  process = meta.get("process", "unknown")
  host = meta.get("host", "") or meta.get("destinationIP", "")
  port = meta.get("destinationPort", "")
  rule = conn.get("rule", "") + ("/" + conn.get("rulePayload", "") if conn.get("rulePayload") else "")
  chains = conn.get("chains", [])
  network = meta.get("network", "")

  if process_filter and process_filter.lower() not in process.lower():
    continue

  results.append({
    "process": process,
    "host": f"{host}:{port}" if port else host,
    "rule": rule,
    "chains": " → ".join(reversed(chains)) if chains else "DIRECT",
    "network": network.upper(),
  })

# 按进程分组
from collections import defaultdict
grouped = defaultdict(list)
for r in results:
  grouped[r["process"]].append(r)

for process, conns in sorted(grouped.items()):
  print(f"\n{'='*60}")
  print(f"进程: {process} ({len(conns)} 个连接)")
  print(f"{'='*60}")

  # 按链路去重统计
  chain_stats = defaultdict(lambda: {"count": 0, "hosts": set()})
  for c in conns:
    key = f"{c['rule']} → {c['chains']}"
    chain_stats[key]["count"] += 1
    chain_stats[key]["hosts"].add(c["host"])

  for route, info in sorted(chain_stats.items(), key=lambda x: -x[1]["count"]):
    print(f"  线路: {route}")
    print(f"  连接数: {info['count']}")
    hosts = sorted(info["hosts"])
    if len(hosts) <= 5:
      print(f"  目标: {', '.join(hosts)}")
    else:
      print(f"  目标: {', '.join(hosts[:5])} ... (+{len(hosts)-5})")
    print()
```

### 完整的一键执行命令

将上面的步骤组合成一个完整的 bash 命令执行：

```bash
SECRET=$(grep '^secret:' "/Users/lifcc/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/clash-verge.yaml" 2>/dev/null | awk '{print $2}')
SOCKET="/var/tmp/verge/verge-mihomo.sock"
FILTER="$ARGUMENTS"

if [ -S "$SOCKET" ]; then
  DATA=$(curl -s --unix-socket "$SOCKET" "http://localhost/connections" -H "Authorization: Bearer $SECRET" 2>/dev/null)
else
  CONTROLLER=$(grep '^external-controller:' "/Users/lifcc/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/clash-verge.yaml" 2>/dev/null | awk '{print $2}' | tr -d "'\"")
  [ -z "$CONTROLLER" ] && CONTROLLER="127.0.0.1:9090"
  DATA=$(curl -s "http://$CONTROLLER/connections" -H "Authorization: Bearer $SECRET" 2>/dev/null)
fi

if [ -z "$DATA" ] || echo "$DATA" | python3 -c "import sys,json; json.load(sys.stdin)" 2>/dev/null; [ $? -ne 0 ]; then
  # 验证 JSON 有效性
  :
fi

echo "$DATA" | python3 -c "
import json, sys
from collections import defaultdict

data = json.loads(sys.stdin.read())
conns = data.get('connections', [])
filt = '$FILTER'.strip().lower()

results = []
for c in conns:
    m = c.get('metadata', {})
    proc = m.get('process', 'unknown')
    if filt and filt not in proc.lower():
        continue
    host = m.get('host', '') or m.get('destinationIP', '')
    port = m.get('destinationPort', '')
    rule = c.get('rule', '')
    rp = c.get('rulePayload', '')
    if rp:
        rule += '/' + rp
    chains = c.get('chains', [])
    chain_str = ' → '.join(reversed(chains)) if chains else 'DIRECT'
    results.append({'process': proc, 'host': f'{host}:{port}' if port else host, 'rule': rule, 'chains': chain_str})

grouped = defaultdict(list)
for r in results:
    grouped[r['process']].append(r)

if not grouped:
    target = filt if filt else '任何进程'
    print(f'未找到 {target} 的活跃连接')
    sys.exit(0)

total = sum(len(v) for v in grouped.values())
print(f'共 {total} 个活跃连接，涉及 {len(grouped)} 个进程')

for proc, pconns in sorted(grouped.items()):
    print(f'\n{\"=\"*60}')
    print(f'进程: {proc} ({len(pconns)} 个连接)')
    print(f'{\"=\"*60}')
    chain_stats = defaultdict(lambda: {'count': 0, 'hosts': set()})
    for c in pconns:
        key = f'{c[\"rule\"]} → {c[\"chains\"]}'
        chain_stats[key]['count'] += 1
        chain_stats[key]['hosts'].add(c['host'])
    for route, info in sorted(chain_stats.items(), key=lambda x: -x[1]['count']):
        print(f'  线路: {route}')
        print(f'  连接数: {info[\"count\"]}')
        hosts = sorted(info['hosts'])
        if len(hosts) <= 5:
            print(f'  目标: {\", \".join(hosts)}')
        else:
            print(f'  目标: {\", \".join(hosts[:5])} ... (+{len(hosts)-5})')
        print()
"
```

## 输出格式

按进程分组，每个进程显示：
- **线路**：匹配规则 → 代理链路（如 `ProcessName/claude → 🤖 AI → 🇯🇵 日本 东京`）
- **连接数**：该线路上的活跃连接数量
- **目标**：连接的目标域名/IP

## 使用示例

- `/clash-routes` - 查看所有进程的线路
- `/clash-routes claude` - 只看 claude 进程
- `/clash-routes chrome` - 只看 chrome 进程
- `/clash-routes telegram` - 只看 telegram 进程

## 注意事项

- 只读操作，不修改任何配置
- 需要 Clash Verge Rev 或 mihomo 正在运行
- 通过 Unix socket 访问比 HTTP 更可靠（不受 external-controller 配置影响）
- 用中文输出所有信息
