---
name: dnsdist
description: DNS load balancer with DoS protection, multi-protocol support (DoH, DoT, DoQ), and dynamic traffic management
version: 1.0.0
tags: [dns, load-balancer, powerdns, doh, dot, doq, security, lua, performance]
---

# dnsdist

High-performance DNS load balancer from PowerDNS that distributes queries across backend servers while providing DoS protection, caching, and support for encrypted DNS protocols (DoH, DoT, DoQ, DNSCrypt).

## Overview

dnsdist is a DNS-aware, DoS-aware load balancer that receives DNS queries and intelligently routes them to backend servers based on configurable policies. It operates at the DNS protocol level, enabling sophisticated traffic management, abuse prevention, and protocol translation.

### Key Capabilities

- **Load Balancing**: Distribute queries across multiple DNS backends
- **DoS Protection**: Dynamic blocking, rate limiting, eBPF filtering
- **Multi-Protocol**: Do53, DNS-over-TLS, DNS-over-HTTPS, DNS-over-QUIC, DNSCrypt
- **Response Caching**: Built-in packet cache with stale serving
- **Dynamic Configuration**: Runtime changes via Lua console
- **Monitoring**: Prometheus metrics, REST API, Carbon export

## Installation

### Package Managers

**Debian/Ubuntu:**
```bash
apt-get install -y dnsdist
```

**RHEL/CentOS:**
```bash
yum install -y epel-release
yum install -y dnsdist
```

**FreeBSD:**
```bash
pkg install dns/dnsdist
```

### From Source

```bash
# Dependencies: C++17 compiler, Boost, Lua 5.1+, libedit

# From tarball
wget https://downloads.powerdns.com/releases/dnsdist-X.Y.Z.tar.bz2
tar xf dnsdist-X.Y.Z.tar.bz2
cd dnsdist-X.Y.Z
./configure
make
sudo make install

# From Git
git clone https://github.com/PowerDNS/pdns.git
cd pdns/pdns/dnsdistdist
autoreconf -i
./configure
make
```

### Verify Installation

```bash
dnsdist --version
# Check for: dns-over-tls(DOT) dns-over-https(DOH) dnscrypt
```

## Quick Start

### Basic Command Line

```bash
# Listen on port 5300, forward to Quad9 servers
dnsdist -l 127.0.0.1:5300 9.9.9.9 2620:fe::fe 2620:fe::9
```

### Minimal Configuration

Create `dnsdist.conf`:

```lua
-- Listen on standard DNS port
setLocal("0.0.0.0:53")

-- Add backend servers
newServer({address="9.9.9.9", name="quad9-primary"})
newServer({address="1.1.1.1", name="cloudflare"})

-- Set load balancing policy
setServerPolicy(firstAvailable)

-- Access control (default: RFC1918 ranges)
setACL({"0.0.0.0/0", "::/0"})  -- Allow all (be careful!)
```

Run with configuration:

```bash
dnsdist -C dnsdist.conf
```

## Backend Server Configuration

### Adding Servers

```lua
-- Basic server
newServer("192.168.1.10")

-- Server with options
newServer({
  address = "192.168.1.10:53",
  name = "dns-primary",
  qps = 100,                    -- Max queries per second
  order = 1,                    -- Selection order
  weight = 100,                 -- Load balancing weight
  retries = 2,                  -- Retry attempts
  tcpConnectTimeout = 5,        -- TCP connect timeout (seconds)
  tcpSendTimeout = 30,          -- TCP send timeout
  tcpRecvTimeout = 30,          -- TCP receive timeout
  checkInterval = 1,            -- Health check interval
  checkTimeout = 1000,          -- Health check timeout (ms)
  maxCheckFailures = 3,         -- Failures before marking down
  mustResolve = true,           -- Must resolve check name
  checkName = "health.example.com",
  rise = 2,                     -- Successes before marking up
  useClientSubnet = true,       -- Forward EDNS Client Subnet
  pool = "primary"              -- Assign to pool
})

-- Server with DNS-over-TLS backend
newServer({
  address = "1.1.1.1:853",
  tls = "openssl",              -- or "gnutls"
  subjectName = "cloudflare-dns.com",
  validateCertificates = true
})

-- Server with DNS-over-HTTPS backend
newServer({
  address = "1.1.1.1:443",
  tls = "openssl",
  dohPath = "/dns-query",
  subjectName = "cloudflare-dns.com"
})
```

### Server Pools

```lua
-- Create pools for different purposes
newServer({address="192.168.1.10", pool="recursive"})
newServer({address="192.168.1.11", pool="recursive"})
newServer({address="10.0.0.50", pool="authoritative"})

-- Route queries to specific pools
addAction(QNameSuffixRule("internal.example.com"), PoolAction("authoritative"))
addAction(AllRule(), PoolAction("recursive"))
```

### Server Management

```lua
-- Console commands
showServers()                   -- Display all servers
getServer(0):setUp()            -- Force server up
getServer(0):setDown()          -- Force server down
getServer(0):setQPS(50)         -- Change QPS limit
getServer(0):addPool("backup")  -- Add to pool
rmServer(0)                     -- Remove server
```

## Load Balancing Policies

### Built-in Policies

```lua
-- First available (default)
setServerPolicy(firstAvailable)

-- Round robin
setServerPolicy(roundrobin)

-- Least outstanding queries
setServerPolicy(leastOutstanding)

-- Weighted random
setServerPolicy(wrandom)

-- Weighted round robin
setServerPolicy(whashed)

-- Random
setServerPolicy(random)

-- Consistent hashing (sticky by client IP)
setServerPolicy(chashed)
```

### Custom Policy

```lua
-- Custom Lua policy function
function myPolicy(servers, dq)
  -- Route .internal queries to first server
  if dq.qname:isPartOf(newDNSName("internal.")) then
    return servers[1]
  end
  -- Round robin for everything else
  return leastOutstanding.policy(servers, dq)
end

setServerPolicyLua("myPolicy", myPolicy)
```

### Per-Pool Policies

```lua
getPool("recursive"):setPolicy(leastOutstanding)
getPool("authoritative"):setPolicy(roundrobin)
```

## Rules and Actions

### Rule Selectors

```lua
-- Match by query name
QNameRule("example.com")              -- Exact match
QNameSuffixRule("example.com")        -- Suffix match
QNameSetRule(newSuffixMatchNode())    -- Set-based match
RegexRule(".*\\.example\\.com$")      -- Regex match

-- Match by query type
QTypeRule(DNSQType.ANY)
QTypeRule(DNSQType.AXFR)

-- Match by source
NetmaskGroupRule(nmg)                 -- IP ranges
MaxQPSIPRule(10, 32, 48)             -- Rate per IP (IPv4/32, IPv6/48)
MaxQPSRule(1000)                      -- Global rate

-- Match by protocol
TCPRule(true)                         -- TCP queries
DNSSECRule()                          -- DNSSEC queries

-- Match by response code
RCodeRule(DNSRCode.NXDOMAIN)
RCodeRule(DNSRCode.SERVFAIL)

-- Compound rules
AndRule({QTypeRule(DNSQType.ANY), MaxQPSIPRule(1)})
OrRule({QNameRule("blocked1.com"), QNameRule("blocked2.com")})
NotRule(NetmaskGroupRule(allowedNmg))
```

### Actions

```lua
-- Routing actions
PoolAction("poolname")                -- Route to pool
newServer({...})                      -- Direct to server

-- Response actions
DropAction()                          -- Drop query silently
RefusedAction()                       -- Return REFUSED
NXDomainAction()                      -- Return NXDOMAIN
SpoofAction("192.168.1.1")           -- Spoof A record
SpoofCNAMEAction("cname.example.com") -- Spoof CNAME

-- Modification actions
SetNoRecurseAction()                  -- Clear RD flag
DelayAction(100)                      -- Delay response (ms)
TCAction()                            -- Force TCP (set TC bit)
LogAction("/var/log/queries.log")     -- Log query

-- Rate limiting
DelayAction(500)                      -- Slow down client
SetEDNSOptionAction(8, "value")       -- Add EDNS option
```

### Adding Rules

```lua
-- Add rule with action
addAction(MaxQPSIPRule(10), DelayAction(200))
addAction(QTypeRule(DNSQType.ANY), DropAction())
addAction(QNameSuffixRule("blocked.com"), RefusedAction())

-- Rule with logging
addAction(MaxQPSIPRule(50), LogAction("/var/log/ratelimit.log", false, true))

-- Rule ordering (insert at position)
addAction(QNameRule("priority.com"), PoolAction("fast"), 0)

-- Response rules
addResponseAction(RCodeRule(DNSRCode.SERVFAIL), LogAction())

-- Cache hit rules
addCacheHitResponseAction(...)
```

### Rule Management

```lua
showRules()                           -- List all rules
rmRule(0)                             -- Remove rule by index
mvRule(0, 5)                          -- Move rule position
clearRules()                          -- Remove all rules
topRules()                            -- Show rule hit stats
```

## DNS-over-TLS (DoT)

### Incoming DoT

```lua
-- Basic DoT listener
addTLSLocal("0.0.0.0:853",
  "/etc/ssl/certs/dns.example.com.pem",
  "/etc/ssl/private/dns.example.com.key"
)

-- With options
addTLSLocal("0.0.0.0:853",
  "/etc/ssl/certs/dns.pem",
  "/etc/ssl/private/dns.key",
  {
    minTLSVersion = "tls1.2",
    ciphers = "ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384",
    numberOfTicketsKeys = 5,
    ticketKeyFile = "/etc/dnsdist/ticket.key",
    sessionTickets = true,
    numberOfStoredSessions = 20000
  }
)

-- Multiple certificates (ECDSA + RSA)
addTLSLocal("0.0.0.0:853",
  {"/etc/ssl/certs/dns.ecdsa.pem", "/etc/ssl/certs/dns.rsa.pem"},
  {"/etc/ssl/private/dns.ecdsa.key", "/etc/ssl/private/dns.rsa.key"}
)
```

### Outgoing DoT

```lua
-- Forward to DoT backend
newServer({
  address = "1.1.1.1:853",
  tls = "openssl",
  subjectName = "cloudflare-dns.com",
  validateCertificates = true
})

-- With certificate pinning
newServer({
  address = "9.9.9.9:853",
  tls = "openssl",
  subjectName = "dns.quad9.net",
  validateCertificates = true,
  caStore = "/etc/ssl/certs/quad9.pem"
})
```

## DNS-over-HTTPS (DoH)

### Incoming DoH

```lua
-- Basic DoH listener
addDOHLocal("0.0.0.0:443",
  "/etc/ssl/certs/dns.pem",
  "/etc/ssl/private/dns.key",
  "/dns-query"
)

-- With options
addDOHLocal("0.0.0.0:443",
  "/etc/ssl/certs/dns.pem",
  "/etc/ssl/private/dns.key",
  "/dns-query",
  {
    minTLSVersion = "tls1.2",
    customResponseHeaders = {["X-Custom"] = "value"},
    serverTokens = "dnsdist",
    trustForwardedForHeader = false
  }
)

-- Behind reverse proxy (HTTP only)
addDOHLocal("127.0.0.1:8053")
```

### Outgoing DoH

```lua
newServer({
  address = "1.1.1.1:443",
  tls = "openssl",
  dohPath = "/dns-query",
  subjectName = "cloudflare-dns.com",
  validateCertificates = true
})
```

## DNS-over-QUIC (DoQ)

```lua
-- DoQ listener (port 853 UDP)
addDOQLocal("0.0.0.0:853",
  "/etc/ssl/certs/dns.pem",
  "/etc/ssl/private/dns.key"
)

-- DNS-over-HTTP/3
addDOH3Local("0.0.0.0:443",
  "/etc/ssl/certs/dns.pem",
  "/etc/ssl/private/dns.key",
  "/dns-query"
)
```

## Response Caching

### Basic Cache Setup

```lua
-- Create cache with 100,000 entries
pc = newPacketCache(100000, {
  maxTTL = 86400,              -- Max TTL (1 day)
  minTTL = 60,                 -- Min TTL (1 minute)
  temporaryFailureTTL = 60,    -- SERVFAIL cache time
  staleTTL = 3600,             -- Stale serving window
  dontAge = false,             -- Age cached responses
  numberOfShards = 1,          -- Parallelism
  deferrableInsertLock = true, -- Performance optimization
  maxNegativeTTL = 3600,       -- NXDOMAIN cache time
  parseECS = true              -- ECS-aware caching
})

-- Attach to default pool
getPool(""):setCache(pc)

-- Pool-specific cache
recursiveCache = newPacketCache(50000)
getPool("recursive"):setCache(recursiveCache)
```

### Cache Management

```lua
-- View statistics
getPool(""):getCache():printStats()

-- Purge entries
getPool(""):getCache():purgeExpired(0)
getPool(""):getCache():expunge(1000)  -- Remove oldest 1000

-- Remove specific entries
getPool(""):getCache():expungeByName(newDNSName("example.com"))
getPool(""):getCache():expungeByName(newDNSName("example.com"), DNSQType.A)

-- Remove cache from pool
getPool(""):unsetCache()
```

## DoS Protection

### Dynamic Blocking Rules

```lua
-- Create dynamic blocking rules group
local dbr = dynBlockRulesGroup()

-- Rate limiting rules
dbr:setQueryRate(100, 10, "Query rate exceeded", 60)
-- Block if >100 qps over 10 seconds, for 60 seconds

dbr:setRCodeRate(DNSRCode.NXDOMAIN, 50, 10, "NXDOMAIN rate exceeded", 300)
dbr:setRCodeRate(DNSRCode.SERVFAIL, 20, 10, "SERVFAIL rate exceeded", 300)

-- Query type rate limiting
dbr:setQTypeRate(DNSQType.ANY, 5, 10, "ANY query rate exceeded", 60)

-- Response bandwidth rate
dbr:setResponseByteRate(10000000, 10, "Bandwidth exceeded", 60)
-- Block if >10MB/s over 10 seconds

-- Exclude trusted ranges
dbr:excludeRange(newNMG({"10.0.0.0/8", "192.168.0.0/16"}))

-- Apply in maintenance function (called every second)
function maintenance()
  dbr:apply()
end
```

### Manual Blocking

```lua
-- Block specific address
addDynamicBlock(newCA("192.0.2.1"), "Manual block", 3600)

-- Block with action
addDynamicBlock(newCA("192.0.2.0/24"), "Subnet block", 3600, DNSAction.Refused)

-- View active blocks
showDynBlocks()

-- Clear all blocks
clearDynBlocks()

-- Clear specific block
rmDynBlocks(newCA("192.0.2.1"))
```

### eBPF Filtering (High Performance)

```lua
-- Create eBPF filter
bpf = newBPFFilter({
  ipv4MaxItems = 100000,
  ipv6MaxItems = 100000,
  qnamesMaxItems = 10000,
  mapDir = "/sys/fs/bpf/dnsdist"  -- Persistent maps
})

-- Attach to frontend
bpf:attachToAllBinds()

-- Create dynamic eBPF filter
dynbpf = newDynBPFFilter(bpf)

-- Use with dynamic blocking
dbr:setQueryRate(100, 10, "Rate exceeded", 60, DNSAction.Drop, 0, 0, dynbpf)

-- Manual eBPF blocking
bpf:block(newCA("192.0.2.1"))
bpf:blockQName(newDNSName("blocked.com"), DNSQType.ANY)

-- Unblock
bpf:unblock(newCA("192.0.2.1"))

-- Statistics
bpf:getStats()
```

## Access Control

```lua
-- Set ACL (replaces existing)
setACL({"10.0.0.0/8", "192.168.0.0/16", "172.16.0.0/12"})

-- Add to ACL
addACL("203.0.113.0/24")

-- View ACL
showACL()

-- Require proxy protocol from load balancers
setProxyProtocolACL({"10.0.0.1/32", "10.0.0.2/32"})
```

## Webserver and API

### Enable Webserver

```lua
-- Basic webserver
webserver("127.0.0.1:8083")

-- With authentication
webserver("127.0.0.1:8083")
setWebserverConfig({
  password = hashPassword("supersecret"),
  apiKey = hashPassword("apikey123"),
  acl = "127.0.0.1/8, ::1/128",
  dashboardRequiresAuthentication = true,
  statsRequireAuthentication = false
})

-- Enable API write access
setAPIWritable(true, "/etc/dnsdist/acl-updates/")
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard HTML |
| `/jsonstat?command=stats` | GET | Statistics JSON |
| `/jsonstat?command=dynblocklist` | GET | Dynamic blocks |
| `/metrics` | GET | Prometheus metrics |
| `/api/v1/servers/localhost` | GET | Server overview |
| `/api/v1/servers/localhost/config/allow-from` | PUT | Update ACL |
| `/api/v1/cache` | DELETE | Purge cache entries |

### Example API Usage

```bash
# Get statistics
curl -H "X-API-Key: apikey123" http://127.0.0.1:8083/jsonstat?command=stats

# Prometheus metrics
curl http://127.0.0.1:8083/metrics

# Purge cache
curl -X DELETE -H "X-API-Key: apikey123" \
  "http://127.0.0.1:8083/api/v1/cache?pool=&name=example.com"
```

## Console Management

### Enable Console

```lua
-- Local console socket
controlSocket("127.0.0.1:5199")

-- With authentication
setKey("base64encodedkey==")
```

### Connect to Console

```bash
dnsdist -c 127.0.0.1:5199
# Or with key
dnsdist -c 127.0.0.1:5199 -k "base64encodedkey=="
```

### Console Commands

```lua
-- Server management
showServers()
showPools()
getServer(0):isUp()

-- Rule management
showRules()
showResponseRules()
topRules()

-- Statistics
showBinds()
showTCPStats()
showTLSErrorCounters()
showDOHFrontends()
showDOHResponseCodes()

-- Cache
getPool(""):getCache():printStats()

-- Traffic analysis
grepq("example.com")
topQueries(20)
topResponses(20, DNSRCode.NXDOMAIN)
topClients(20)

-- Dynamic blocks
showDynBlocks()
clearDynBlocks()

-- Maintenance
dumpStats()
delta()              -- Changes since last call
quit() / exit()
```

## Logging and Metrics

### Query Logging

```lua
-- Log all queries
addAction(AllRule(), LogAction("/var/log/dnsdist/queries.log", false, true))

-- Log rate-limited queries
addAction(MaxQPSIPRule(10), LogAction("/var/log/ratelimit.log"))

-- Remote logging (dnstap)
dnstapLog = newFrameStreamUnixLogger("/var/run/dnstap.sock")
addAction(AllRule(), DnstapLogAction("dnsdist", dnstapLog))
addResponseAction(AllRule(), DnstapLogResponseAction("dnsdist", dnstapLog))
```

### Carbon/Graphite Export

```lua
carbonServer("graphite.example.com:2003", "dnsdist.node1", 10)
-- Host, prefix, interval (seconds)
```

### Prometheus Metrics

Access at `http://server:8083/metrics`:

```
# HELP dnsdist_queries Number of queries
# TYPE dnsdist_queries counter
dnsdist_queries 12345678

# HELP dnsdist_responses Number of responses
# TYPE dnsdist_responses counter
dnsdist_responses 12345670

# HELP dnsdist_servfail_responses ServFail responses
# TYPE dnsdist_servfail_responses counter
dnsdist_servfail_responses 100

# HELP dnsdist_latency_avg Average latency (usec)
# TYPE dnsdist_latency_avg gauge
dnsdist_latency_avg 1234.5
```

## Configuration Examples

### High-Availability DNS Load Balancer

```lua
-- dnsdist.conf - HA DNS Load Balancer

-- Frontend listeners
setLocal("0.0.0.0:53")
addTLSLocal("0.0.0.0:853", "/etc/ssl/dns.pem", "/etc/ssl/dns.key")
addDOHLocal("0.0.0.0:443", "/etc/ssl/dns.pem", "/etc/ssl/dns.key", "/dns-query")

-- Backend servers with health checks
newServer({
  address = "192.168.1.10:53",
  name = "dns1",
  checkName = "health.internal.",
  checkInterval = 1,
  maxCheckFailures = 3,
  rise = 2,
  pool = "recursive"
})
newServer({
  address = "192.168.1.11:53",
  name = "dns2",
  checkName = "health.internal.",
  checkInterval = 1,
  maxCheckFailures = 3,
  rise = 2,
  pool = "recursive"
})

-- Load balancing
setServerPolicy(leastOutstanding)

-- Response cache
pc = newPacketCache(500000, {
  maxTTL = 86400,
  minTTL = 60,
  staleTTL = 3600
})
getPool("recursive"):setCache(pc)

-- DoS protection
local dbr = dynBlockRulesGroup()
dbr:setQueryRate(100, 10, "Query flood", 60)
dbr:setRCodeRate(DNSRCode.NXDOMAIN, 50, 10, "NXDOMAIN flood", 300)

function maintenance()
  dbr:apply()
end

-- Access control
setACL({"0.0.0.0/0", "::/0"})

-- Monitoring
webserver("127.0.0.1:8083")
setWebserverConfig({password = hashPassword("monitor123")})
controlSocket("127.0.0.1:5199")
```

### Split-Horizon DNS

```lua
-- Route internal queries to internal servers
newServer({address = "10.0.0.53", pool = "internal"})
newServer({address = "10.0.0.54", pool = "internal"})

-- External recursive resolvers
newServer({address = "9.9.9.9", pool = "external"})
newServer({address = "1.1.1.1", pool = "external"})

-- Routing rules
addAction(QNameSuffixRule("internal.example.com"), PoolAction("internal"))
addAction(QNameSuffixRule("corp.example.com"), PoolAction("internal"))
addAction(AllRule(), PoolAction("external"))

-- Different policies per pool
getPool("internal"):setPolicy(roundrobin)
getPool("external"):setPolicy(leastOutstanding)
```

### DNS Firewall with Blocklist

```lua
-- Load blocklist
blockedDomains = newSuffixMatchNode()
for line in io.lines("/etc/dnsdist/blocklist.txt") do
  blockedDomains:add(newDNSName(line))
end

-- Block malicious domains
addAction(SuffixMatchNodeRule(blockedDomains), SetTagAction("blocked", "malware"))
addAction(TagRule("blocked"), NXDomainAction())

-- Rate limit ANY queries
addAction(QTypeRule(DNSQType.ANY), DropAction())

-- Limit AXFR attempts
addAction(QTypeRule(DNSQType.AXFR), RefusedAction())

-- Log blocked queries
addAction(TagRule("blocked"), LogAction("/var/log/blocked.log"))
```

## Troubleshooting

### Debug Commands

```lua
-- Enable verbose logging
setVerbose(true)
setVerboseHealthChecks(true)

-- Check server status
showServers()
getServer(0):getDrops()
getServer(0):getLatencyAvg()

-- Check cache performance
getPool(""):getCache():printStats()

-- View TLS errors
showTLSErrorCounters()

-- Traffic analysis
grepq("problem.domain.com", 100)
topQueries(20)
topSlowResponses(20)
```

### Common Issues

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| Server marked down | `showServers()` - check healthcheck | Verify backend reachable, check `checkName` |
| High latency | `getServer(N):getLatencyAvg()` | Add more backends, enable caching |
| Cache misses | `getCache():printStats()` | Increase cache size, check minTTL |
| DoH not working | `showTLSErrorCounters()` | Verify certificates, check SNI |
| Rate limiting | `showDynBlocks()` | Adjust thresholds, add exclusions |

## Resources

- [dnsdist Documentation](https://dnsdist.org/)
- [PowerDNS GitHub](https://github.com/PowerDNS/pdns)
- [dnsdist Configuration Reference](https://dnsdist.org/reference/config.html)
- [PowerDNS Community](https://www.powerdns.com/community.html)
