---
name: managing-dns
description: Manage DNS records, TTL strategies, and DNS-as-code automation for infrastructure. Use when configuring domain resolution, automating DNS from Kubernetes with external-dns, setting up DNS-based load balancing, or troubleshooting propagation issues across cloud providers (Route53, Cloud DNS, Azure DNS, Cloudflare).
---

# DNS Management

Configure and automate DNS records with proper TTL strategies, DNS-as-code patterns, and troubleshooting techniques.

## Purpose

Guide DNS configuration for applications, infrastructure, and services with focus on:
- Record type selection (A, AAAA, CNAME, MX, TXT, SRV, CAA)
- TTL strategies for propagation and caching
- DNS-as-code automation (external-dns, OctoDNS, DNSControl)
- Cloud DNS services comparison and selection
- DNS-based load balancing patterns
- Troubleshooting tools and techniques

## When to Use This Skill

Apply DNS management patterns when:
- Setting up DNS for new applications or services
- Automating DNS updates from Kubernetes workloads
- Configuring DNS-based failover or load balancing
- Troubleshooting DNS propagation or resolution issues
- Migrating DNS between providers
- Planning DNS changes with minimal downtime
- Implementing GeoDNS for global users

## Record Type Selection

### Quick Reference

**Address Resolution:**
- **A Record**: Map hostname to IPv4 address (example.com → 192.0.2.1)
- **AAAA Record**: Map hostname to IPv6 address (example.com → 2001:db8::1)
- **CNAME Record**: Alias to another domain (www.example.com → example.com)
  - Cannot use at zone apex (@)
  - Cannot coexist with other records at same name

**Email Configuration:**
- **MX Record**: Direct email to mail servers with priority
- **TXT Record**: Email authentication (SPF, DKIM, DMARC) and verification

**Service Discovery:**
- **SRV Record**: Specify service location (protocol, priority, weight, port, target)

**Delegation and Security:**
- **NS Record**: Delegate subdomain to different nameservers
- **CAA Record**: Restrict which Certificate Authorities can issue certificates

**Cloud-Specific:**
- **ALIAS Record**: Like CNAME but works at zone apex (Route53, Cloudflare)

### Decision Tree

```
Need to point domain to:
├─ IPv4 Address? → A record
├─ IPv6 Address? → AAAA record
├─ Another Domain?
│  ├─ Zone apex (@) → ALIAS/ANAME or A record
│  └─ Subdomain → CNAME
├─ Mail Server? → MX record (with priority)
├─ Email Authentication? → TXT record (SPF/DKIM/DMARC)
├─ Service Discovery? → SRV record
├─ Domain Verification? → TXT record
├─ Certificate Control? → CAA record
└─ Subdomain Delegation? → NS record
```

For detailed record type examples and patterns, see `references/record-types.md`.

## TTL Strategy

### Standard TTL Values

**By Change Frequency:**
- **Stable records**: 3600-86400s (1-24 hours) - NS, stable A/AAAA
- **Normal operation**: 3600s (1 hour) - Standard websites, MX
- **Moderate changes**: 300-1800s (5-30 min) - Development, A/B testing
- **Failover scenarios**: 60-300s (1-5 min) - Critical records needing fast updates

**Key Principle:** Lower TTL = faster propagation but higher DNS query load

### Pre-Change Process

When planning DNS changes:

```
T-48h: Lower TTL to 300s
T-24h: Verify TTL propagated globally
T-0h:  Make DNS change
T+1h:  Verify new records propagating
T+6h:  Confirm global propagation
T+24h: Raise TTL back to normal (3600s)
```

**Propagation Formula:** `Max Time = Old TTL + New TTL + Query Time`

Example: Changing a record with 3600s TTL takes up to 2 hours to fully propagate.

### TTL by Use Case

| Use Case | TTL | Rationale |
|----------|-----|-----------|
| Production (stable) | 3600s | Balance speed and load |
| Before planned change | 300s | Fast propagation |
| Development/staging | 300-600s | Frequent changes |
| DNS-based failover | 60-300s | Fast recovery |
| Mail servers | 3600s | Rarely change |
| NS records | 86400s | Very stable |

For detailed TTL scenarios and calculations, see `references/ttl-strategies.md`.

## DNS-as-Code Tools

### Tool Selection by Use Case

**Kubernetes DNS Automation → external-dns**
- Annotation-based configuration on Services/Ingresses
- Automatic sync to DNS providers (20+ supported)
- No manual DNS updates required
- See `examples/external-dns/`

**Multi-Provider DNS Management → OctoDNS or DNSControl**
- Version control for DNS records
- Sync configuration across multiple providers
- Preview changes before applying
- OctoDNS (Python/YAML) - See `examples/octodns/`
- DNSControl (JavaScript) - See `examples/dnscontrol/`

**Infrastructure-as-Code → Terraform**
- Manage DNS alongside cloud resources
- Provider-specific resources (aws_route53_record, etc.)
- See `examples/terraform/`

### Tool Comparison

| Tool | Language | Best For | Kubernetes | Multi-Provider |
|------|----------|----------|------------|----------------|
| external-dns | Go | K8s automation | ★★★★★ | ★★★★ |
| OctoDNS | Python/YAML | Version control | ★★★ | ★★★★★ |
| DNSControl | JavaScript | Complex logic | ★★ | ★★★★★ |
| Terraform | HCL | IaC integration | ★★★ | ★★★★ |

### Quick Start: external-dns

```yaml
# Kubernetes Service with DNS annotation
apiVersion: v1
kind: Service
metadata:
  name: app
  annotations:
    external-dns.alpha.kubernetes.io/hostname: app.example.com
    external-dns.alpha.kubernetes.io/ttl: "300"
spec:
  type: LoadBalancer
  ports:
    - port: 80
```

Deploy external-dns controller once, then all annotated Services/Ingresses automatically create DNS records.

For complete examples, see `examples/external-dns/` and `references/dns-as-code-comparison.md`.

## Cloud DNS Provider Selection

### Provider Characteristics

**AWS Route53**
- Best for AWS-heavy infrastructure
- Advanced routing policies (weighted, latency, geolocation, failover)
- Health checks with automatic failover
- ALIAS records for AWS resources (ELB, CloudFront, S3)
- Pricing: $0.50/month per zone + $0.40 per million queries

**Google Cloud DNS**
- Best for GCP-native applications
- Strong DNSSEC support with automatic key rotation
- Private zones for VPC internal DNS
- Split-horizon DNS (different internal/external records)
- Pricing: $0.20/month per zone + $0.40 per million queries

**Azure DNS**
- Best for Azure-native applications
- Integration with Azure Traffic Manager
- Azure Private DNS zones
- Azure RBAC for access control
- Pricing: $0.50/month per zone + $0.40 per million queries

**Cloudflare**
- Best for multi-cloud or cloud-agnostic
- Fastest DNS query times globally
- Built-in DDoS protection
- Free tier with unlimited queries
- CDN integration
- Pricing: Free tier, $20/month Pro, $200/month Business

### Selection Decision Tree

```
Choose based on:
├─ AWS-heavy? → Route53
├─ GCP-native? → Cloud DNS
├─ Azure-native? → Azure DNS
├─ Multi-cloud? → Cloudflare or OctoDNS/DNSControl
├─ Need fastest global DNS? → Cloudflare
├─ Need DDoS protection? → Cloudflare
└─ Budget-conscious? → Cloudflare (free tier) or Cloud DNS (lowest zone cost)
```

For detailed provider comparisons and examples, see `references/cloud-providers.md`.

## DNS-Based Load Balancing

### GeoDNS (Geographic Routing)

Return different IP addresses based on client location to:
- Reduce latency (route to nearest data center)
- Comply with data residency requirements
- Distribute load across regions

**Example Pattern:**
```
Client Location → DNS Response
├─ North America → 192.0.2.1 (US data center)
├─ Europe → 192.0.2.10 (EU data center)
└─ Default → CloudFront edge (global CDN)
```

### Weighted Routing

Distribute traffic by percentage for:
- Blue-green deployments
- Canary releases (10% to new version)
- A/B testing

**Example Pattern:**
```
DNS Responses:
├─ 90% → 192.0.2.1 (stable version)
└─ 10% → 192.0.2.2 (canary version)
```

### Health Check-Based Failover

Automatically route traffic away from unhealthy endpoints.

**Pattern:**
```
Primary: 192.0.2.1 (health checked every 30s)
├─ Healthy → Return primary IP
└─ Unhealthy → Return secondary IP (192.0.2.2)

Failover time: ~2-3 minutes
= Health check failures (90s) + TTL expiration (60s)
```

For complete load balancing examples, see `examples/load-balancing/`.

## Troubleshooting

### Essential Commands

**Check DNS Resolution:**
```bash
# Basic query
dig example.com

# Clean output (just IP)
dig example.com +short

# Query specific DNS server
dig @8.8.8.8 example.com
dig @1.1.1.1 example.com

# Trace resolution path
dig +trace example.com
```

**Check TTL:**
```bash
dig example.com | grep -A1 "ANSWER SECTION"
# Look for TTL value (number before IN A)
```

**Check Propagation:**
```bash
# Multiple resolvers
dig @8.8.8.8 example.com +short       # Google
dig @1.1.1.1 example.com +short       # Cloudflare
dig @208.67.222.222 example.com +short # OpenDNS
```

**Flush Local DNS Cache:**
```bash
# macOS
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder

# Windows
ipconfig /flushdns

# Linux
sudo systemd-resolve --flush-caches
```

### Common Problems

**Slow Propagation:**
- Check current TTL (old TTL must expire first)
- Lower TTL 24-48 hours before changes
- Use propagation checkers: whatsmydns.net, dnschecker.org

**CNAME at Zone Apex:**
- Error: Cannot use CNAME at @ (zone apex)
- Solution: Use ALIAS record (Route53, Cloudflare) or A record

**external-dns Not Creating Records:**
- Verify annotation spelling: `external-dns.alpha.kubernetes.io/hostname`
- Check domain filter matches: `--domain-filter=example.com`
- Review external-dns logs for errors
- Confirm provider credentials configured

For detailed troubleshooting, see `references/troubleshooting.md`.

## Common Patterns

### Pattern 1: Kubernetes DNS Automation

```yaml
# Deploy external-dns (once per cluster)
helm install external-dns external-dns/external-dns \
  --set provider=aws \
  --set domainFilters[0]=example.com \
  --set policy=sync

# Then annotate Services
apiVersion: v1
kind: Service
metadata:
  annotations:
    external-dns.alpha.kubernetes.io/hostname: api.example.com
    external-dns.alpha.kubernetes.io/ttl: "300"
spec:
  type: LoadBalancer
```

### Pattern 2: Multi-Provider Sync with OctoDNS

```yaml
# octodns-config.yaml
providers:
  config:
    class: octodns.provider.yaml.YamlProvider
    directory: ./config
  route53:
    class: octodns_route53.Route53Provider
  cloudflare:
    class: octodns_cloudflare.CloudflareProvider

zones:
  example.com.:
    sources: [config]
    targets: [route53, cloudflare]
```

### Pattern 3: DNS-Based Failover

```hcl
# Route53 with health checks
resource "aws_route53_health_check" "primary" {
  fqdn              = "primary.example.com"
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = 3
  request_interval  = 30
}

resource "aws_route53_record" "primary" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "api.example.com"
  type           = "A"
  ttl            = 60
  set_identifier = "primary"

  failover_routing_policy {
    type = "PRIMARY"
  }

  health_check_id = aws_route53_health_check.primary.id
  records         = ["192.0.2.1"]
}

resource "aws_route53_record" "secondary" {
  zone_id        = aws_route53_zone.main.zone_id
  name           = "api.example.com"
  type           = "A"
  ttl            = 60
  set_identifier = "secondary"

  failover_routing_policy {
    type = "SECONDARY"
  }

  records = ["192.0.2.2"]
}
```

## Integration with Other Skills

**infrastructure-as-code:**
- Manage DNS via Terraform/Pulumi alongside other resources
- Zone configuration in IaC repositories

**kubernetes-operations:**
- external-dns automates DNS for Kubernetes workloads
- Ingress controller integration for automatic DNS

**load-balancing-patterns:**
- DNS-based load balancing (GeoDNS, weighted routing)
- Health checks and failover configurations

**security-hardening:**
- DNSSEC for DNS integrity
- CAA records for certificate authority control
- DNS-based DDoS mitigation

**secret-management:**
- Store DNS provider API credentials in vaults
- Secure DDNS update mechanisms

## Additional Resources

**Reference Documentation:**
- `references/record-types.md` - Detailed record type guide with examples
- `references/ttl-strategies.md` - TTL scenarios and propagation calculations
- `references/cloud-providers.md` - Provider comparison and detailed features
- `references/troubleshooting.md` - Common problems and solutions
- `references/dns-as-code-comparison.md` - Tool comparison matrix

**Examples:**
- `examples/external-dns/` - Kubernetes DNS automation
- `examples/octodns/` - Multi-provider sync with YAML
- `examples/dnscontrol/` - Multi-provider with JavaScript DSL
- `examples/terraform/` - Cloud provider configurations
- `examples/load-balancing/` - GeoDNS and failover patterns

**Scripts:**
- `scripts/check-dns-propagation.sh` - Verify propagation across resolvers
- `scripts/validate-dns-config.py` - Validate DNS configuration
- `scripts/export-dns-records.sh` - Export existing DNS records
- `scripts/calculate-ttl-propagation.py` - Calculate propagation time

## Quick Reference

### Record Types Cheat Sheet

| Record | Purpose | Example |
|--------|---------|---------|
| A | IPv4 address | example.com → 192.0.2.1 |
| AAAA | IPv6 address | example.com → 2001:db8::1 |
| CNAME | Alias to domain | www → example.com |
| MX | Mail server | 10 mail.example.com |
| TXT | Text/verification | "v=spf1 include:_spf.google.com ~all" |
| SRV | Service location | 10 60 5060 sip.example.com |
| NS | Nameserver delegation | ns1.provider.com |
| CAA | CA authorization | 0 issue "letsencrypt.org" |

### TTL Cheat Sheet

| Scenario | TTL | Why |
|----------|-----|-----|
| Stable production | 3600s | Balance speed/load |
| Before change | 300s | Fast propagation |
| Failover | 60-300s | Fast recovery |
| NS records | 86400s | Very stable |

### Provider Cheat Sheet

| Provider | Best For | Key Feature |
|----------|----------|-------------|
| Route53 | AWS | Advanced routing, health checks |
| Cloud DNS | GCP | DNSSEC, private zones |
| Azure DNS | Azure | Traffic Manager integration |
| Cloudflare | Multi-cloud | Fastest, DDoS protection, free tier |

### Tool Cheat Sheet

| Tool | Use When |
|------|----------|
| external-dns | Kubernetes DNS automation |
| OctoDNS | Multi-provider, Python shop |
| DNSControl | Multi-provider, JavaScript preference |
| Terraform | Managing DNS with other infrastructure |
