---
name: mesh-security
description: Analyze Istio, Consul, and Linkerd service mesh configurations for security vulnerabilities with NIST 800-53 control mappings. Use when users need to audit mesh security, identify misconfigurations, check mTLS settings, review ACL policies, or prepare for FedRAMP assessments. Triggers on keywords like "mesh config", "istio security", "consul ACL", "linkerd policy", "service mesh audit", or "NIST compliance".
license: MIT
metadata:
  author: mesh-config-analyzer
  version: "1.0.0"
---

# Service Mesh Security Analyzer

Comprehensive security analysis for Istio, Consul, and Linkerd service mesh configurations with NIST 800-53 Rev 5 control mappings.

## Quick Start

### Analyze a Configuration File

```bash
# Run the analyzer wrapper directly
node ~/.claude/skills/mesh-security/lib/analyzer-wrapper.js <config-file>

# Examples
node ~/.claude/skills/mesh-security/lib/analyzer-wrapper.js ./istio-meshconfig.yaml
node ~/.claude/skills/mesh-security/lib/analyzer-wrapper.js ./consul-config.json
node ~/.claude/skills/mesh-security/lib/analyzer-wrapper.js ./linkerd-config.yaml --json
```

### Sample Configurations

Test configs are available in the `samples/` directory:
- Istio: `samples/sample-meshconfig.yaml`
- Consul: `samples/sample-consul-config.json`
- Linkerd: `samples/sample-linkerd-config.yaml`

## Supported Mesh Types

### Istio

**Auto-detection:** Files with `kind: MeshConfig` and `apiVersion` containing `istio.io`

**Security Checks:**
| Category | What It Checks |
|----------|----------------|
| mTLS | Enabled status, STRICT mode enforcement |
| Certificates | CA provider, validity duration (optimal 90 days) |
| Peer Authentication | Default peer auth, STRICT mode |
| Proxy Config | Privileged mode, image versioning, holdApplicationUntilProxyStarts |
| Secret Discovery | SDS enabled for certificate management |
| Trust Domain | Explicitly configured, not using default |
| Authorization | Default deny policies |
| Telemetry | Enabled collection, access logging |
| RBAC | Role-based access control enforcement |
| Traffic Policy | Outbound traffic restricted to REGISTRY_ONLY |

### Consul

**Auto-detection:** Files with `mesh_type: "consul"` or containing `connect`, `tls`, and `acl` fields

**Security Checks:**
| Category | What It Checks |
|----------|----------------|
| Service Mesh | Connect enabled |
| Proxy Security | No privileged mode |
| TLS Security | verify_incoming, verify_outgoing, hostname verification |
| Access Control | ACL enabled, default deny policy, agent tokens |
| Telemetry | Service metrics enabled |
| Auto-Encryption | TLS auto-encrypt feature |
| Gossip Encryption | Key configured, proper length, verification |
| FedRAMP Compliance | TLS 1.2+, FIPS ciphers, strong encryption |

### Linkerd

**Auto-detection:** Files with `mesh_type: "linkerd"` or containing `identity`, `proxy`, and `policy` fields

**Security Checks:**
| Category | What It Checks |
|----------|----------------|
| TLS Security | Enabled, enforced, cipher suites, min version 1.2 |
| Service Identity | Enabled, certificate issuer, validity period |
| Proxy Config | Non-privileged, versioning, timeouts, resource limits |
| Authorization | Policy enforcement, default deny, specific rules |
| Authentication | Strict mode enforcement |
| Observability | Tracing enabled, sampling, collector config |
| Metrics | Enabled, Prometheus integration, retention |
| Traffic Rules | TLS in destination rules, system namespace protection |

## Severity Levels

| Level | Meaning | Example Issues |
|-------|---------|----------------|
| **Critical** | Immediate security risk | RBAC/ACL disabled, mTLS not enforced, gossip encryption missing |
| **High** | Significant vulnerability | Permissive auth modes, privileged containers, missing hostname verification |
| **Medium** | Security weakness | Default trust domains, long certificate validity, missing telemetry |
| **Low** | Best practice violation | Non-pinned images, missing timeouts, default CA providers |

## NIST 800-53 Control Mappings

Findings are mapped to these NIST 800-53 Rev 5 controls:

| Control | Title | Relevant Checks |
|---------|-------|-----------------|
| AC-3 | Access Enforcement | RBAC, ACL, Authorization policies |
| AC-4 | Information Flow Enforcement | Outbound traffic policy, Policy enforcement |
| AC-17 | Remote Access | mTLS, TLS configuration |
| AU-2 | Audit Events | Telemetry, Access logging |
| AU-3 | Content of Audit Records | Logging configuration |
| AU-12 | Audit Generation | Metrics, Tracing |
| CA-3 | System Interconnections | Trust domain, Peer authentication |
| CM-2 | Baseline Configuration | Proxy config, Default settings |
| CM-6 | Configuration Settings | Security hardening |
| CM-7 | Least Functionality | Privileged mode, Outbound restrictions |
| IA-2 | Identification and Authentication | Service identity, Authentication |
| IA-5 | Authenticator Management | Certificate management, SDS |
| SC-7 | Boundary Protection | Traffic policy, Network segmentation |
| SC-8 | Transmission Confidentiality | mTLS, TLS settings |
| SC-12 | Cryptographic Key Management | Certificate validity, CA settings |
| SC-13 | Cryptographic Protection | Cipher suites, TLS versions |
| SC-23 | Session Authenticity | Peer authentication, Trust chain |
| SI-4 | System Monitoring | Telemetry, Metrics, Tracing |

## Workflow: Analyze a Mesh Configuration

1. **Read the configuration file** to understand its structure
2. **Run the analyzer** using the wrapper script
3. **Review findings** by severity (Critical first)
4. **Check NIST mappings** for compliance requirements
5. **Generate remediation** recommendations if needed

### Example Analysis Session

```
User: Analyze my Istio mesh configuration at ./istio-config.yaml

Steps:
1. Read the file to understand the mesh configuration
2. Run: node ~/.claude/skills/mesh-security/lib/analyzer-wrapper.js ./istio-config.yaml
3. Present findings grouped by severity
4. Highlight critical/high severity issues first
5. Include NIST control mappings for compliance context
6. Offer to generate fixes or compliance report
```

## Output Format

### Markdown (Default)

```markdown
## Security Analysis Results

**Mesh Type:** Istio
**File:** ./istio-config.yaml
**Total Findings:** 5

| Severity | Count |
|----------|-------|
| Critical | 1     |
| High     | 2     |
| Medium   | 2     |
| Low      | 0     |

### Critical Findings

#### 1. mTLS Configuration
**Issue:** mTLS is not set to STRICT mode
**Location:** `spec.mtls.mode`
**Recommendation:** Set mTLS mode to STRICT to enforce mutual TLS
**NIST Controls:** SC-8, SC-13
```

### JSON (--json flag)

```json
{
  "success": true,
  "meshType": "istio",
  "findings": [...],
  "summary": { "critical": 1, "high": 2, "medium": 2, "low": 0, "total": 5 }
}
```

## Related Skills

- **mesh-remediation** - Generate and apply security fixes
- **mesh-compliance-reporter** - Generate FedRAMP/NIST compliance reports

## Programmatic Usage

```javascript
const { analyzeConfig, formatFindings } = require('~/.claude/skills/mesh-security/lib/analyzer-wrapper.js');

// Analyze a config file
const results = analyzeConfig('./istio-config.yaml');
console.log(formatFindings(results));

// Or specify mesh type explicitly
const consulResults = analyzeConfig('./config.json', 'consul');
```
