---
name: k8s-ndots-search-domain-nxdomain-flood
description: |
  Fix for massive NxDomain query floods to external DNS servers caused by Kubernetes
  ndots:5 search domain expansion. Use when: (1) DNS server shows low cache hit rate
  with 60%+ NxDomain responses, (2) DNS logs show queries like
  "service.namespace.svc.cluster.local.yourdomain.lan", (3) external DNS receives
  thousands of junk queries per hour for non-existent names ending in your search
  domain, (4) DNS cache hit ratio is unexpectedly low despite stable workloads.
  Applies to any Kubernetes cluster using CoreDNS with a custom DNS search domain.
author: Claude Code
version: 1.1.0
date: 2026-02-17
---

# Kubernetes ndots:5 Search Domain NxDomain Flood

## Problem
Kubernetes pods have `ndots:5` and a custom search domain (e.g., `viktorbarzin.lan`)
in their `/etc/resolv.conf`. When resolving internal service names like
`redis.redis.svc.cluster.local` (4 dots < ndots:5), glibc tries all search domain
suffixes before the absolute name. This generates queries like:

1. `redis.redis.svc.cluster.local.namespace.svc.cluster.local` (CoreDNS handles, NxDomain)
2. `redis.redis.svc.cluster.local.svc.cluster.local` (CoreDNS handles, NxDomain)
3. `redis.redis.svc.cluster.local.cluster.local` (CoreDNS handles, NxDomain)
4. `redis.redis.svc.cluster.local.yourdomain.lan` (CoreDNS **forwards to external DNS**, NxDomain)
5. `redis.redis.svc.cluster.local` (finally resolves)

Step 4 is the problem: CoreDNS forwards `*.yourdomain.lan` queries to the external DNS
server, flooding it with junk NxDomain requests. With hundreds of pods making DNS lookups,
this generates tens of thousands of useless queries per day.

## Context / Trigger Conditions
- DNS server (e.g., Technitium, Pi-hole, BIND) shows high NxDomain percentage (50%+)
- DNS cache hit rate is unexpectedly low
- DNS logs show queries ending in `*.svc.cluster.local.yourdomain.lan`
- CoreDNS Corefile has a server block forwarding `yourdomain.lan` to an external DNS
- Node resolv.conf has `search yourdomain.lan` (set by DHCP)
- Top DNS clients by query volume are Kubernetes node IPs (not pod IPs), because
  CoreDNS forwards via NodePort and the source IP becomes the node IP

## Solution

### Step 1: Confirm the problem
Check DNS query logs for the pattern:
```bash
# Enable Technitium query logging temporarily
# API: /api/settings/set?token=TOKEN&enableLogging=true&logQueries=true&loggingType=File

# Check for junk queries
kubectl exec -n technitium PODNAME -- grep "cluster.local.yourdomain" /etc/dns/logs/*.log
```

### Step 2: Add generic CoreDNS template regex (RECOMMENDED)

Instead of creating specific catch-all blocks for each junk suffix pattern, add a single
`template` directive with a regex inside the `yourdomain.lan` server block. This catches
ALL multi-label junk queries (e.g., `*.cluster.local.yourdomain.lan`,
`*.yourdomain.lan.yourdomain.lan`, `www.cloudflare.com.yourdomain.lan`) in one rule:

```
yourdomain.lan:53 {
  errors
  template ANY ANY yourdomain.lan {
    match ".*\..*\.yourdomain\.lan\.$"
    rcode NXDOMAIN
    fallthrough
  }
  forward . <your-dns-server-ip>
  cache {
    success 10000 300 6
    denial 10000 300 60
  }
}
```

**How it works**: The regex `.*\..*\.yourdomain\.lan\.$` matches any query with 2+ labels
before `.yourdomain.lan` — meaning only single-label queries like `idrac.yourdomain.lan`
fall through to the real DNS server. All junk multi-label queries get instant NXDOMAIN.

**Important**: The `fallthrough` directive is required so that legitimate single-label
queries (which don't match the regex) continue to the `forward` plugin.

#### Alternative: Specific catch-all blocks (DEPRECATED)

The older approach used separate server blocks per junk suffix pattern:

```
cluster.local.yourdomain.lan:53 {
  errors
  template ANY ANY {
    rcode NXDOMAIN
  }
  cache {
    denial 10000 3600
  }
}
```

This requires adding a new block for each pattern and doesn't catch arbitrary junk queries
like `www.cloudflare.com.yourdomain.lan`. The generic regex approach above is preferred.

### Step 3: Apply the CoreDNS ConfigMap
```bash
kubectl apply -f coredns-configmap.yaml
# CoreDNS auto-reloads via the `reload` plugin (default 30s)
```

### Step 4: Manage in Terraform (this cluster)
The CoreDNS ConfigMap is managed in `modules/kubernetes/technitium/main.tf` as
`kubernetes_config_map.coredns`. To import an existing ConfigMap:
```bash
terraform import 'module.kubernetes_cluster.module.technitium["technitium"].kubernetes_config_map.coredns' 'kube-system/coredns'
```

## Verification
1. Test that the template returns NXDOMAIN instantly:
```bash
kubectl run dns-test --rm -i --restart=Never --image=busybox -- \
  nslookup redis.redis.svc.cluster.local.yourdomain.lan 10.96.0.10
# Should return NXDOMAIN immediately
```

2. Check DNS logs - no more `*.cluster.local.yourdomain.lan` queries to external DNS
3. NxDomain percentage on external DNS should drop significantly within an hour

## Additional Fix: Enable DNS Cache Persistence
If the DNS server (Technitium) loses its cache on pod restart, enable `saveCache`:
```
/api/settings/set?token=TOKEN&saveCache=true
```
This prevents the cache hit rate from resetting to zero after every restart.

## Notes
- The same `ndots:5` issue also causes `*.yourdomain.lan.yourdomain.lan` (double suffix)
  and `*.yourdomain.me.yourdomain.lan` patterns — the generic regex catches all of these
- The top DNS client IPs will be the **node IPs** (not pod IPs) because CoreDNS forwards
  via NodePort, and the source becomes the node's IP
- `ndots:5` is the Kubernetes default and shouldn't be changed cluster-wide as it breaks
  short-name service resolution
- Individual pods can set `dnsConfig.options: [{name: ndots, value: "2"}]` to reduce
  search domain lookups, but this is a per-pod opt-in
- Prometheus scrape targets using `.yourdomain.lan` hostnames should add a trailing dot
  (e.g., `idrac.yourdomain.lan.:161`) to bypass ndots expansion entirely
- ExternalName services don't need trailing dots — the generic template regex handles them

## See also
- `pfsense-dnsmasq-interface-binding` — Related: preserve client IPs for DNS port forwarding
- `crowdsec-agent-registration-failure` — another common K8s DNS-adjacent issue
- `loki-helm-deployment-pitfalls` — Loki deployment patterns
