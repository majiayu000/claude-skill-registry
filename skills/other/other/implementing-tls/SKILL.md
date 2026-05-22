---
name: implementing-tls
description: Configure TLS certificates and encryption for secure communications. Use when setting up HTTPS, securing service-to-service connections, implementing mutual TLS (mTLS), or debugging certificate issues.
---

# Implementing TLS

## Purpose

Implement Transport Layer Security (TLS) for encrypting network communications and authenticating services. Generate certificates, automate certificate lifecycle management with Let's Encrypt or internal CAs, configure TLS 1.3, implement mutual TLS for service authentication, and debug common certificate issues.

## When to Use This Skill

Trigger this skill when:
- Setting up HTTPS for web applications or APIs
- Securing service-to-service communication in microservices
- Implementing mutual TLS (mTLS) for zero-trust networks
- Generating certificates for development or production
- Automating certificate renewal and rotation
- Debugging certificate validation errors
- Configuring TLS termination at load balancers
- Setting up internal PKI for corporate networks

## Quick Start

### For Development (Local HTTPS)

Use mkcert for trusted local certificates:

```bash
# Install mkcert
brew install mkcert  # macOS
# sudo apt install mkcert  # Linux

# Install local CA
mkcert -install

# Generate certificate
mkcert example.com localhost 127.0.0.1
# Creates: example.com+2.pem and example.com+2-key.pem
```

### For Production (Public HTTPS)

**Kubernetes with cert-manager:**
```bash
# Install cert-manager
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace \
  --set installCRDs=true

# Create Let's Encrypt issuer
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod-key
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
```

**Traditional servers with Certbot:**
```bash
# Install certbot
sudo apt install certbot

# Obtain certificate
sudo certbot certonly --standalone -d example.com -d www.example.com
# Certificates saved to /etc/letsencrypt/live/example.com/
```

### For Internal Services (Internal PKI)

Generate internal CA with CFSSL:

```bash
# Install CFSSL
brew install cfssl  # macOS

# Create CA
cfssl genkey -initca ca-csr.json | cfssljson -bare ca

# Generate server certificate
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem \
  -config=ca-config.json -profile=server \
  server-csr.json | cfssljson -bare server
```

See `examples/cfssl-ca/` for complete configuration files.

## TLS 1.3 Configuration Best Practices

### Protocol Versions

Enable TLS 1.3 and 1.2 only:
```nginx
# Nginx
ssl_protocols TLSv1.3 TLSv1.2;
ssl_prefer_server_ciphers off;  # Let client choose
```

Disable obsolete protocols: SSLv3, TLS 1.0, TLS 1.1.

### Cipher Suites

**TLS 1.3 (5 cipher suites):**
```
TLS_AES_256_GCM_SHA384           # Recommended
TLS_CHACHA20_POLY1305_SHA256     # Mobile-optimized
TLS_AES_128_GCM_SHA256           # Performance
```

**TLS 1.2 fallback:**
```nginx
ssl_ciphers 'ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-CHACHA20-POLY1305';
```

### Security Features

- **Perfect Forward Secrecy (PFS)**: Use ephemeral key exchanges (ECDHE)
- **OCSP Stapling**: Enable for performance and privacy
- **HSTS**: Force HTTPS with `Strict-Transport-Security` header
- **Disable compression**: Prevent CRIME attacks

For detailed TLS 1.3 configuration, see `references/tls13-best-practices.md`.

## Decision Framework

### Certificate Type Selection

```
Need TLS certificate?
│
├─ Public-facing (internet users)?
│  │
│  ├─ Single domain → Let's Encrypt with HTTP-01
│  │  Tools: certbot, cert-manager
│  │  Challenge: HTTP verification
│  │
│  └─ Multiple subdomains → Let's Encrypt with DNS-01
│     Tools: certbot with DNS plugin, cert-manager
│     Challenge: DNS TXT records
│     Supports: Wildcard certificates (*.example.com)
│
└─ Internal (corporate network)?
   │
   ├─ Development → mkcert or self-signed
   │  Tools: mkcert (trusted), openssl (basic)
   │  No automation needed
   │
   └─ Production → Internal CA
      │
      ├─ Small scale (<10 services) → CFSSL
      │  Manual management acceptable
      │
      └─ Large scale (100+ services) → Vault PKI or cert-manager
         Dynamic secrets, automatic rotation
```

### Automation Tool Selection

```
Environment?
│
├─ Kubernetes → cert-manager
│  Native CRDs, Ingress integration
│  Supports: Let's Encrypt, Vault, CA, self-signed
│
├─ Traditional servers (VMs) → Certbot (public) or CFSSL (internal)
│  Plugins: nginx, apache, DNS providers
│  Automated renewal via cron/systemd
│
├─ Microservices (any platform) → HashiCorp Vault PKI
│  Dynamic secrets, short-lived certs
│  API-driven, service mesh integration
│
└─ Developer workstation → mkcert
   Trusted by browser automatically
```

### Standard TLS vs Mutual TLS (mTLS)

**Use Standard TLS (server-only authentication) when:**
- Public websites (users trust server)
- APIs with bearer tokens (separate auth layer)
- Services behind API gateway
- Simple architectures (<5 services)

**Use Mutual TLS (both authenticate) when:**
- Service-to-service in microservices
- High security requirements (financial, healthcare)
- Machine-to-machine APIs
- Zero-trust networks
- No shared network trust

See `references/mtls-guide.md` for mTLS implementation patterns.

## Common Workflows

### Generate Self-Signed Certificate

**Quick generation with SANs:**
```bash
# Create OpenSSL config
cat > san.cnf <<EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = v3_req

[dn]
CN = example.com

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = example.com
DNS.2 = www.example.com
DNS.3 = api.example.com
IP.1 = 192.168.1.100
EOF

# Generate key and certificate
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout server-key.pem -out server-cert.pem \
  -days 365 -config san.cnf -extensions v3_req

# Verify SANs
openssl x509 -in server-cert.pem -noout -text | grep -A 3 "Subject Alternative Name"
```

For detailed examples including CFSSL and mkcert, see `references/certificate-generation.md` and `examples/self-signed/`.

### Setup Let's Encrypt Automation

**With Certbot (traditional servers):**
```bash
# Standalone mode (port 80 must be free)
sudo certbot certonly --standalone -d example.com -d www.example.com

# Webroot mode (no service interruption)
sudo certbot certonly --webroot -w /var/www/html -d example.com

# DNS challenge (wildcard support)
sudo certbot certonly --manual --preferred-challenges dns \
  -d example.com -d "*.example.com"

# Test renewal
sudo certbot renew --dry-run
```

**With cert-manager (Kubernetes):**
```yaml
# Ingress with automatic certificate
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - example.com
    secretName: example-com-tls
  rules:
  - host: example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
```

See `references/automation-patterns.md` for complete automation guides.

### Configure Mutual TLS (mTLS)

**Server configuration (Nginx):**
```nginx
server {
    listen 443 ssl;
    server_name api.example.com;

    # Server certificate
    ssl_certificate /etc/ssl/certs/server.crt;
    ssl_certificate_key /etc/ssl/private/server.key;

    # CA to verify client certificates
    ssl_client_certificate /etc/ssl/certs/ca.crt;
    ssl_verify_client on;
    ssl_verify_depth 2;

    # TLS 1.3
    ssl_protocols TLSv1.3;

    location / {
        proxy_pass http://backend;
        # Pass client cert info to backend
        proxy_set_header X-SSL-Client-Cert $ssl_client_cert;
        proxy_set_header X-SSL-Client-S-DN $ssl_client_s_dn;
    }
}
```

**Client request with certificate:**
```bash
curl https://api.example.com/endpoint \
  --cert client.crt \
  --key client.key \
  --cacert ca.crt
```

See `references/mtls-guide.md` and `examples/mtls-nginx/` for complete mTLS implementations.

### Debug TLS Issues

**Test TLS connection:**
```bash
# Basic connection test
openssl s_client -connect example.com:443

# Show certificate chain
openssl s_client -connect example.com:443 -showcerts

# Test specific TLS version
openssl s_client -connect example.com:443 -tls1_3

# Test with client certificate (mTLS)
openssl s_client -connect api.example.com:443 \
  -cert client.crt -key client.key -CAfile ca.crt
```

**Examine certificate:**
```bash
# View certificate details
openssl x509 -in cert.pem -noout -text

# Check expiration
openssl x509 -in cert.pem -noout -dates

# Check Subject Alternative Names
openssl x509 -in cert.pem -noout -text | grep -A 1 "Subject Alternative Name"

# Verify certificate chain
openssl verify -CAfile ca.crt cert.pem
```

**Verify key and certificate match:**
```bash
# Certificate modulus
openssl x509 -in cert.pem -noout -modulus | md5sum

# Key modulus (must match)
openssl rsa -in key.pem -noout -modulus | md5sum
```

**Common errors and solutions:**

| Error | Cause | Solution |
|-------|-------|----------|
| `certificate has expired` | Certificate validity passed | Renew certificate, check system clock |
| `unable to get local issuer certificate` | CA not in trust store | Add CA cert to system trust store |
| `Hostname mismatch` | CN/SAN doesn't match hostname | Regenerate cert with correct SANs |
| `handshake failure` | TLS version/cipher mismatch | Enable TLS 1.2+, check cipher suites |
| `certificate signed by unknown authority` | Missing intermediate certs | Include full chain in server config |

See `references/debugging-tls.md` for comprehensive troubleshooting guide.

## Tool Selection Guide

| Use Case | Environment | Recommended Tool | Alternative |
|----------|-------------|------------------|-------------|
| Public HTTPS | Kubernetes | cert-manager | External Secrets Operator |
| Public HTTPS | VMs/Bare Metal | Certbot | acme.sh |
| Internal PKI | Any | HashiCorp Vault | CFSSL, Smallstep |
| mTLS (K8s) | Kubernetes | cert-manager + Istio | Linkerd, Consul |
| mTLS (VMs) | Traditional | Vault PKI | CFSSL |
| Local Dev | Workstation | mkcert | Self-signed (OpenSSL) |
| Debugging | Any | OpenSSL s_client | curl -v |
| Automation | CI/CD | CFSSL API | Vault API |

## Certificate Lifecycle

```
1. Generate
   ├─ Development: mkcert, self-signed (OpenSSL)
   ├─ Production: Let's Encrypt, commercial CA
   └─ Internal: CFSSL, Vault PKI

2. Deploy
   ├─ Kubernetes: Mount as Secret volume
   ├─ VMs: Copy to /etc/ssl/ or application directory
   └─ Containers: Mount via Docker volumes

3. Monitor
   ├─ Check expiry: openssl x509 -noout -dates
   ├─ Prometheus: blackbox_exporter (probe_ssl_earliest_cert_expiry)
   └─ Alert: < 7 days before expiry

4. Renew
   ├─ Automated: certbot renew, cert-manager, Vault Agent
   ├─ Manual: Generate new CSR, reissue from CA
   └─ Timing: Renew 30 days before expiry

5. Rotate
   ├─ Zero-downtime: Load new cert, graceful reload
   ├─ Kubernetes: Update Secret, rolling restart
   └─ Service mesh: Automatic rotation (Istio, Linkerd)
```

## Certificate Formats

**PEM (most common):**
- Extensions: .pem, .crt, .cer, .key
- Base64 encoded, ASCII text
- Used by: Apache, Nginx, OpenSSL

**DER (binary):**
- Extensions: .der, .cer
- Binary format
- Used by: Java, Windows

**PKCS#12 / PFX (container):**
- Extensions: .p12, .pfx
- Contains certificate + private key (password protected)
- Used by: Windows, Java keystores, browsers

**Convert formats:**
```bash
# PEM to DER
openssl x509 -in cert.pem -outform DER -out cert.der

# PEM to PKCS#12
openssl pkcs12 -export -out cert.p12 -inkey key.pem -in cert.pem

# PKCS#12 to PEM
openssl pkcs12 -in cert.p12 -out cert.pem -nodes
```

See `scripts/convert-formats.sh` for automated conversion.

## References

### Detailed Guides
- **references/certificate-generation.md** - Comprehensive generation examples (OpenSSL, CFSSL, mkcert)
- **references/automation-patterns.md** - Automation deep-dive (Certbot, cert-manager, Vault PKI)
- **references/mtls-guide.md** - mTLS implementation patterns and architecture
- **references/debugging-tls.md** - Troubleshooting guide with common errors and solutions
- **references/tls13-best-practices.md** - TLS 1.3 configuration and security features

## Examples

### Working Code
- **examples/self-signed/** - Self-signed certificate generation scripts
- **examples/cfssl-ca/** - Internal CA setup with CFSSL (complete configuration)
- **examples/certbot/** - Let's Encrypt automation (standalone, webroot, DNS challenges)
- **examples/cert-manager/** - Kubernetes certificate management (ClusterIssuer, Ingress)
- **examples/mtls-nginx/** - Mutual TLS with Nginx (server + client configuration)
- **examples/vault-pki/** - Vault PKI integration and dynamic certificates

## Scripts

### Utility Tools
- **scripts/check-cert-expiry.sh** - Monitor certificate expiration across multiple domains
- **scripts/validate-chain.sh** - Verify certificate chain integrity
- **scripts/test-tls-connection.sh** - Test TLS connections with various options
- **scripts/convert-formats.sh** - Convert between PEM, DER, and PKCS#12 formats

## Related Skills

**Security and Authentication:**
- **secret-management** - Store private keys securely (Vault, Kubernetes Secrets, HSM)
- **auth-security** - Application-level authentication (OAuth, OIDC, JWT)
- **security-hardening** - System security configuration
- **security-architecture** - Holistic security design and threat modeling

**Infrastructure:**
- **kubernetes-operations** - Kubernetes cluster TLS configuration
- **load-balancing-patterns** - TLS termination at load balancers
- **network-architecture** - Network security design

**Operations:**
- **deploying-applications** - Inject certificates at runtime
- **observability** - Monitor certificate health and expiry
- **building-ci-pipelines** - Automate certificate generation in CI/CD
