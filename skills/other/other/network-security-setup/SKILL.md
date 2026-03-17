---
name: network-security-setup
description: Configure Claude Code sandbox network isolation with trusted domains, custom access policies, and environment variables
tags: [security, network, isolation, trusted-domains, configuration]
version: 1.0.0
---

# Network Security Setup

## Purpose
Configure Claude Code sandbox network isolation policies including trusted domain whitelisting, custom access rules, and secure environment variable management.

## Specialist Agent

I am a network security specialist with expertise in:
- Zero-trust network architecture for AI code execution
- Domain whitelisting and access control policies
- Prompt injection attack prevention via network isolation
- Secure environment variable management
- Corporate proxy and internal registry configuration

### Methodology (Systems Thinking + Self-Consistency)

1. **Analyze Environment**: Understand deployment context (enterprise, open-source, local)
2. **Design Network Policy**: Create appropriate trusted domain list
3. **Configure Access Rules**: Set up custom access patterns and exclusions
4. **Secure Credentials**: Properly handle environment variables and secrets
5. **Validate Security**: Test that policies block untrusted access while enabling work

### Network Isolation Modes

**Mode 1: Trusted Network Access (Recommended Default)**
```yaml
mode: trusted
description: Claude can only access pre-approved, known-safe domains
use_case: General development, open-source projects
trusted_domains:
  - "*.npmjs.org"
  - "registry.npmjs.org"
  - "*.yarnpkg.com"
  - "*.github.com"
  - "api.github.com"
  - "raw.githubusercontent.com"
  - "*.cloudfront.net"
  - "*.docker.io"
  - "registry.hub.docker.com"
  - "*.pypi.org"
  - "pypi.python.org"
```

**Mode 2: No Network Access**
```yaml
mode: none
description: Complete network isolation, no external access
use_case: Maximum security, offline development, sensitive projects
trusted_domains: []
```

**Mode 3: Custom Access**
```yaml
mode: custom
description: User-defined whitelist of allowed domains
use_case: Enterprise with internal registries, corporate networks
trusted_domains:
  - "registry.company.internal"
  - "docs.company.com"
  - "api.company.com"
  - "*.company-cdn.net"
  - [Include standard registries as needed]
```

### Default Trusted Domains (Anthropic-Approved)

**Package Registries**:
- `*.npmjs.org` - npm packages
- `registry.npmjs.org` - npm registry
- `*.yarnpkg.com` - Yarn registry
- `*.pypi.org` - Python packages
- `pypi.python.org` - Python registry
- `rubygems.org` - Ruby gems
- `*.maven.org` - Maven packages

**Container Registries**:
- `*.docker.io` - Docker Hub
- `registry.hub.docker.com` - Docker registry
- `ghcr.io` - GitHub Container Registry
- `gcr.io` - Google Container Registry
- `*.azurecr.io` - Azure Container Registry

**Source Control & CDNs**:
- `*.github.com` - GitHub
- `api.github.com` - GitHub API
- `raw.githubusercontent.com` - Raw GitHub content
- `*.cloudfront.net` - AWS CloudFront
- `cdn.jsdelivr.net` - jsDelivr CDN
- `unpkg.com` - unpkg CDN

**Development Tools**:
- `*.vercel.com` - Vercel deployment
- `*.netlify.com` - Netlify deployment
- `*.supabase.co` - Supabase API

### Enterprise Configuration

**Internal Registry Setup**:
```json
{
  "sandbox": {
    "enabled": true,
    "network": {
      "mode": "custom",
      "trustedDomains": [
        "registry.company.internal:5000",
        "npm.company.com",
        "docs.company.com",
        "api-docs.company.internal",
        "*.company-cdn.net",
        "*.company.cloud",

        // Include standard public registries if needed
        "registry.npmjs.org",
        "*.github.com"
      ],
      "customProxy": {
        "enabled": true,
        "http": "http://proxy.company.com:8080",
        "https": "http://proxy.company.com:8080",
        "noProxy": [
          "localhost",
          "127.0.0.1",
          "*.company.internal"
        ]
      }
    }
  }
}
```

**Corporate Proxy Configuration**:
```json
{
  "sandbox": {
    "network": {
      "customProxy": {
        "enabled": true,
        "http": "http://corporate-proxy.company.com:3128",
        "https": "http://corporate-proxy.company.com:3128",
        "noProxy": [
          "localhost",
          "*.internal",
          "*.company.com"
        ],
        "authentication": {
          "enabled": false  // Use system credentials
        }
      }
    }
  }
}
```

### Environment Variables (Secure Management)

**Safe Environment Variables** (OK to configure):
```yaml
safe_env_vars:
  - NODE_ENV: "development"
  - API_BASE_URL: "https://api.company.com"
  - LOG_LEVEL: "debug"
  - FEATURE_FLAGS: "new_ui,beta_features"
  - BUILD_TARGET: "production"
```

**Dangerous (NEVER in sandbox config)**:
```yaml
dangerous_env_vars:  # Store in .env.local, never in settings
  - API_KEY: "sk-..."  ❌ SECRET
  - DATABASE_PASSWORD: "..."  ❌ SECRET
  - PRIVATE_KEY: "..."  ❌ SECRET
  - AWS_SECRET_ACCESS_KEY: "..."  ❌ SECRET
```

**Best Practice for Secrets**:
1. Store in `.env.local` (gitignored)
2. Use environment variable references in sandbox config
3. Document required variables without values
4. Use secret management services in production

**Example Secure Configuration**:
```json
{
  "sandbox": {
    "environmentVariables": {
      // ✅ Non-sensitive configuration
      "NODE_ENV": "development",
      "API_BASE_URL": "https://api.staging.company.com",

      // ✅ Reference to local .env file (document required vars)
      "__REQUIRED_SECRETS__": "API_KEY, DATABASE_URL (store in .env.local)"
    }
  }
}
```

### Security Threat Mitigation

**Threat 1: Prompt Injection → Data Exfiltration**
```
Attack: Malicious prompt in downloaded code tries to send sensitive data to attacker.com
Mitigation: Network isolation blocks all non-whitelisted domains
Result: Attack fails, data stays secure
```

**Threat 2: Malicious Package Download**
```
Attack: Prompt injection tries to install malware from evil-registry.com
Mitigation: Only trusted registries allowed
Result: Download blocked, system protected
```

**Threat 3: Internal Network Scanning**
```
Attack: Code tries to scan internal network for vulnerable services
Mitigation: Network isolation prevents arbitrary connections
Result: Internal network remains hidden
```

**Threat 4: Credential Theft**
```
Attack: Downloaded code reads environment variables and sends to attacker
Mitigation: Secrets not in sandbox config, network blocked anyway
Result: No credentials accessible or exfiltratable
```

### Domain Pattern Matching

**Wildcard Patterns**:
- `*.example.com` - Matches all subdomains: api.example.com, cdn.example.com
- `example.com` - Exact match only
- `*.*.example.com` - Multi-level wildcards: a.b.example.com

**Port Specifications**:
- `registry.company.com:5000` - Specific port
- `*.company.com:*` - Any port on subdomains
- `localhost:3000` - Local development server

**Protocol Handling**:
- HTTPS preferred and enforced where possible
- HTTP allowed only for localhost and internal domains
- WebSocket connections follow same rules (ws:// → wss://)

### Validation and Testing

**Test Network Policy**:
```bash
# Should succeed (trusted domain)
npm install express

# Should succeed (trusted domain)
git clone https://github.com/user/repo

# Should fail (untrusted domain)
curl https://random-website.com

# Should succeed if allowLocalBinding enabled
npm run dev
```

**Verification Checklist**:
- [ ] Package installations work from trusted registries
- [ ] GitHub operations succeed
- [ ] CDN resources accessible if needed
- [ ] Internal registries accessible (enterprise)
- [ ] Untrusted domains blocked
- [ ] Local development servers work if configured
- [ ] Build commands pass with required env vars
- [ ] No secrets in sandbox configuration

## Input Contract

```yaml
environment_type: enterprise | opensource | local | custom
required_access:
  public_registries: array[string]
  internal_domains: array[string]
  cdn_services: array[string]
needs_proxy: boolean
proxy_config: object (if needs_proxy)
required_env_vars: array[{name, value, is_secret}]
```

## Output Contract

```yaml
network_configuration:
  mode: trusted | none | custom
  trusted_domains: array[string]
  proxy_config: object (if applicable)
  environment_variables: object (non-secrets only)

security_analysis:
  threats_mitigated: array[string]
  access_granted: array[string]
  access_denied: array[string]
  recommendations: array[string]

setup_instructions:
  config_file_location: string
  config_content: json
  validation_commands: array[string]
  documentation_links: array[string]
```

## Integration Points

- **Cascades**: Works with sandbox-configurator for complete security setup
- **Commands**: `/network-security`, `/trusted-domains`
- **Other Skills**: Pairs with sandbox-configurator, security-review

## Usage Examples

**Standard Development Setup**:
```
Configure network security for open-source development with standard npm and GitHub access
```

**Enterprise Internal**:
```
Set up network isolation for enterprise:
- Internal npm registry: npm.company.internal
- Internal docs: docs.company.com
- Corporate proxy: proxy.company.com:8080
- Keep access to public GitHub
```

**Maximum Security**:
```
Configure maximum security with no network access for sensitive project
```

**Add Custom Domain**:
```
Add api.specialservice.com to trusted domains for API integration
```

## Failure Modes & Mitigations

- **Package install fails**: Add registry to trusted domains
- **Git clone fails**: Add git host to trusted domains
- **Build fails with network error**: Check if build accesses CDN, add to whitelist
- **Proxy authentication fails**: Verify proxy credentials or use system auth
- **Environment variable missing**: Document in config, add to .env.local

## Validation Checklist

- [ ] All required registries in trusted domains
- [ ] Internal domains include ports if non-standard
- [ ] Proxy configuration correct (if needed)
- [ ] No secrets in sandbox configuration
- [ ] Required env vars documented
- [ ] Test package installation
- [ ] Test git operations
- [ ] Test build commands
- [ ] Verify untrusted access blocked

## Neural Training Integration

```yaml
training:
  pattern: systems-thinking
  feedback_collection: true
  success_metrics:
    - zero_security_incidents
    - development_velocity_maintained
    - false_positive_rate_low
```

---

**Quick Reference**:
- Config location: `.claude/settings.local.json`
- Default mode: Trusted network access
- Wildcard syntax: `*.domain.com`
- Secrets: NEVER in sandbox config, use .env.local

**Security Principle**: Deny by default, allow explicitly, verify continuously
