---
name: ip-check
description: 检测一个 IP 或住宅/机房代理节点的质量——注册库、地理库一致性、ASN/org、风控信誉、黑名单、住宅真实性、BGP 宣告、目标服务(Grok/Claude/ChatGPT)解锁与延迟三角测量。判定该 IP 能否安全用于 AI 服务(避免被地理库误判到别国导致区域锁)。当用户说"查这个 IP"、"这个节点在哪"、"这个代理能用吗"、"IP 质量检测"、"验收住宅 IP"、"为什么被判定在 X 国"、"check ip"、给出 socks5 代理凭证问归属或解锁时使用。
---

# IP 质量检测

判定一个 IP(或带凭证的 socks5 代理)是否适合用于 AI 服务(Grok/Claude/ChatGPT),核心是识破"物理在美国、纸面在别国"的租赁 IP 段——这类 IP 会被 ipinfo/MaxMind 等商业地理库判到欧盟,导致 Grok/Claude 区域锁,而风控只看地理库不看物理延迟。

## Operating Contract

只读检测,不改任何系统配置。脚本只发出站 HTTP/DNS 查询和(带凭证时)通过代理的探测,不写文件、不改代理设置、不动网络配置。

Direct actions:
- 对用户给出的 IP 或代理凭证跑 `ipcheck.py`,读 JSON,按 4 条硬标准出记分卡。
- 区分事实(JSON 字段)与推断(如"物理大概率在美东,依据延迟排名")。

Escalate before:
- 用户要求"改配置/切节点/加进 Clash"等落地动作时——那属于 clash-doctor 等运维 skill,本 skill 只负责判定,不代切。
- DNSBL 层报 `unreliable`(DNS 劫持)时,必须提示用户换网络重跑,不得把未测准当"干净"。
- 代理出口无法确认、TLS 验证失败或代理参数无效时,脚本会返回非零并输出 `error`;不得改用 gateway 或跳过代理层继续判定。

Evidence-backed pushback:
- 用户坚称某 IP 是美国、但 rdap 显示 RIPE 注册 + country 非 US 时,以 whois/geo 字段反驳,不附和主观判断。
- 单库判 US 不等于合格;三库分歧(split)本身就是"纸面搬家"信号,要指出而非取信最乐观的那一家。

Feedback loop:
- 换节点/换代理后重跑,用记分卡逐条对比(如西班牙段=退货、纽约段=合格),确认问题项确实消除。
- 有 IPQS_KEY/ABUSEIPDB_KEY 时补跑风控源;缺 key 显式标 skipped,不把"未检测"当"通过"。

## 何时用

- 用户给一个 IP 问"在哪/能用吗/为什么被判定在某国"
- 用户给 socks5 代理凭证(`socks5://user:pass@host:port`)问归属或某服务解不解锁
- 买了住宅/机房代理要验收
- 排查 AI 服务的区域锁

## 运行

脚本随 skill 安装位置运行。优先使用当前 runtime 的安装路径:Codex 通常是 `~/.agents/skills/ip-check/scripts/ipcheck.py`,Claude Code 通常是 `~/.claude/skills/ip-check/scripts/ipcheck.py`,仓库开发时也可用 `skills/ip-check/scripts/ipcheck.py`。

```bash
python3 <script> <IP>                                          # 只查 IP
python3 <script> socks5://user:pass@host:port                 # 带凭证多跑代理实测层
python3 <script> <IP> --proxy socks5://user:pass@host:port     # IP 与代理分开给
```

脚本输出结构化 JSON(9 层),你的工作是**读 JSON 做判定**,不要只转述字段。可选环境变量 `IPQS_KEY`(IPQualityScore 免费 5000/月)、`ABUSEIPDB_KEY`(免费 1000/天)存在时自动多跑两个风控源,没有则该项标 skipped。

## 检测层说明

| 层 | 数据源 | 看什么 |
|---|---|---|
| rdap | rdap.org → RIR | 注册库(ARIN=北美好 / RIPE=欧洲需警惕)、org、lease_flag、country |
| geo | ipinfo + ip-api + ipwho | 三库判定国家是否一致(consensus)还是分歧(split) |
| asn | ipinfo org + rdap | ASN 是否真 ISP、org 是否与 ASN 主体一致 |
| reputation | proxycheck + ipapi.is (+IPQS +AbuseIPDB) | proxy/vpn/datacenter 标记、risk 分、欺诈分 |
| dnsbl | Spamhaus/Barracuda/SORBS/SpamCop | 垃圾邮件黑名单(自带 DNS 劫持检测) |
| ptr | dig -x | 反向 DNS 是否有真住宅域名格式(hsd1/cable/dsl) |
| bgp | RIPEstat | 实际由哪个 ASN 宣告该前缀 |
| services | 代理直连各服务 | Grok/ChatGPT/Anthropic 是否可达、cf_loc、是否区域锁(需代理) |
| exit | 代理查出口 3 次 | 单跳还是轮换池、出口 IP 是否等于服务器 IP(需代理) |
| latency | 代理→各洲 AWS TLS 建连 ×3 | 物理最近的大洲(需代理) |

## 判定协议(读完 JSON 按此裁决)

输出一张**记分卡**,4 条硬标准逐项 ✅/⚠️/❌,再给总判定。

**硬标准(4 条,全过才算合格):**

1. **注册库 = ARIN** — `rdap.rir == "ARIN"` 且 `rdap.country == "US"`。RIPE/APNIC + 非美 country = ❌(这是西班牙段的死因)。`lease_flag=true`(mnt 出现 interlir/lease)= ❌ 直接退货。
2. **三库一致判 US** — `geo.consensus == true` 且国家都是 US。`geo.split == true`(库之间打架)= ⚠️ 强警告,这就是"纸面搬家"信号,分歧本身比任何单库结论更重要。
3. **ASN/org 一致且真 ISP** — 分三种情况:
   - `asn.is_real_isp == true` 且 `asn.org_matches_asn == true` → ✅。
   - `asn.is_real_isp == true` 但 `asn.org_matches_asn == false`(org 是陌生第三方名,如 Treochoy9/AviationAI)→ ⚠️ 租赁段特征,可用但有漂移风险,不是直接挂。
   - `asn.is_real_isp == false`(ASN 不在真 ISP 白名单)→ **不单独否决**,白名单只覆盖北美主流 ISP,合法的欧洲/亚洲/中小 ISP 会漏判。结合 reputation 综合看:若同时命中 datacenter/hosting → 退货;否则归 ⚠️ 慎用,提示"ASN 非主流 ISP,人工确认是否真住宅"。
4. **风控分干净** — proxycheck `risk==0`、`proxy/vpn=no`、`type` 非 hosting;ipapi.is 各 is_* 全 false;有 IPQS 时 `fraud_score` 低。任一命中 datacenter 或 abuser = ❌。

**辅助信号(加权,不单独否决):**

- `dnsbl.status=="unreliable"` → **必须提示用户**:当前网络有 DNS 劫持(多半是 Clash TUN fake-ip),黑名单这项没测准,要在非 TUN 网络重跑才有效。不要把 unreliable 当"干净"。
- `ptr.has_ptr==false` → 挂靠段常见特征,弱负面信号(纽约段也没 PTR 但仍合格,所以不单独否决)。
- `bgp.announced_by` 与 rdap org 不同主体 → IP 段近期可能易主,记录但不否决。

**代理实测层(有凭证时,价值最高——直接问风控本人):**

- `services.results.grok.com.region_blocked==true`(且是精确短语命中)→ Grok 确实锁了这个出口,**最强负面证据**。注意 `region_blocked` 是弱启发信号(首页是 SPA 空壳),`http_status` 和 `cf_loc` 才是硬信号——`cf_loc != "US"` 说明 Cloudflare 也判非美。
- `exit.stable==false` → 买静态却拿到轮换池,另一种坑,报告出来。
- `exit.exit_ip != 服务器IP` → 多跳,记录。
- `latency.closest` 是欧洲/亚洲但地理库判 US,或反之 → **物理/纸面分裂**,明确指出"物理在 X,纸面在 Y,风控信纸面"。

**总判定三档:**

- **合格** — 4 条硬标准全 ✅,可放心用于 AI 服务。
- **租赁段慎用** — 硬标准过但有 ⚠️(org 不匹配 / 无 PTR / BGP 易主),能用但说明风险,建议定期复查。
- **退货** — 任一 ❌(RIPE 注册 / 非美 country / lease_flag / 三库判非美 / datacenter / abuser / is_real_isp=false 且命中 hosting / 服务区域锁)。给出具体死因和"找代理商换 ARIN 注册 + ipinfo 显示 US 的 IP"话术。

## 输出格式

给用户一张中文记分卡:先一句话总判定,再逐层列关键证据(标注 ✅/⚠️/❌),最后给行动建议。区分事实(来自 JSON 字段)和推断(如"物理大概率在美东,依据延迟排名")。不要罗列所有原始字段,只挑支撑判定的关键证据。

## 已知边界

- scamalytics 全面封自动化访问(实测 403),协议已排除,用 proxycheck + ipapi.is + IPQS 替代。
- DNSBL 在 Clash TUN 环境不可信,脚本会自动检测并标 unreliable,据此提示用户。
- DNSBL 解析器故障和 Spamhaus `127.255.255.0/24` 查询错误码同样标 `unreliable`,不计作"未列入"或命中。
- SOCKS HTTPS 探测使用系统 CA 和 hostname 验证;证书失败属于探测失败,不得关闭 TLS 校验重试。
- `services` 层首页多为 SPA 空壳,`region_blocked` 是弱信号,以 http_status/cf_loc 为准。
- ip-api.com 限 45 次/分钟、proxycheck 免费 100 次/天,批量查多个 IP 时注意配额。
