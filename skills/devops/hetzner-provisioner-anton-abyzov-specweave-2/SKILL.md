---
name: hetzner-provisioner
description: Provisions infrastructure on Hetzner Cloud with Terraform/Pulumi. Generates IaC code for CX11/CX21/CX31 instances, managed Postgres, SSL configuration, Docker deployment. Activates for deploy on Hetzner, Hetzner Cloud, budget deployment, cheap hosting, $10/month hosting.
---

# Hetzner Cloud Provisioner

Automated infrastructure provisioning for Hetzner Cloud - the budget-friendly alternative to Vercel and AWS.

## Purpose

Generate and deploy infrastructure-as-code (Terraform/Pulumi) for Hetzner Cloud, enabling $10-15/month SaaS deployments instead of $50-100/month on other platforms.

## When to Use

Activates when user mentions:
- "deploy on Hetzner"
- "Hetzner Cloud"
- "budget deployment"
- "cheap hosting"
- "deploy for $10/month"
- "cost-effective infrastructure"

## What It Does

1. **Analyzes requirements**:
   - Application type (NextJS, Node.js, Python, etc.)
   - Database needs (Postgres, MySQL, Redis)
   - Expected traffic/users
   - Budget constraints

2. **Generates Infrastructure-as-Code**:
   - Terraform configuration for Hetzner Cloud
   - Alternative: Pulumi for TypeScript-native IaC
   - Server instances (CX11, CX21, CX31)
   - Managed databases (Postgres, MySQL)
   - Object storage (if needed)
   - Networking (firewall rules, floating IPs)

3. **Configures Production Setup**:
   - Docker containerization
   - SSL certificates (Let's Encrypt)
   - DNS configuration (Cloudflare or Hetzner DNS)
   - GitHub Actions CI/CD pipeline
   - Monitoring (Uptime Kuma, self-hosted)
   - Automated backups

4. **Outputs Deployment Guide**:
   - Step-by-step deployment instructions
   - Cost breakdown
   - Monitoring URLs
   - Troubleshooting guide

---

## ⚠️ CRITICAL: Secrets Required (MANDATORY CHECK)

**BEFORE generating Terraform/Pulumi code, CHECK for Hetzner API token.**

### Step 1: Check If Token Exists

```bash
# Check .env file
if [ -f .env ] && grep -q "HETZNER_API_TOKEN" .env; then
  echo "✅ Hetzner API token found"
else
  # Token NOT found - STOP and prompt user
fi
```

### Step 2: If Token Missing, STOP and Show This Message

```
🔐 **Hetzner API Token Required**

I need your Hetzner API token to provision infrastructure.

**How to get it**:
1. Go to: https://console.hetzner.cloud/
2. Click on your project (or create one)
3. Navigate to: Security → API Tokens
4. Click "Generate API Token"
5. Give it a name (e.g., "specweave-deployment")
6. Permissions: **Read & Write**
7. Click "Generate"
8. **Copy the token immediately** (you can't see it again!)

**Where I'll save it**:
- File: `.env` (gitignored, secure)
- Format: `HETZNER_API_TOKEN=your-token-here`

**Security**:
✅ .env is in .gitignore (never committed to git)
✅ Token is 64 characters, alphanumeric
✅ Stored locally only (not in source code)

Please paste your Hetzner API token:
```

### Step 3: Validate Token Format

```bash
# Hetzner tokens are 64 alphanumeric characters
if [[ ! "$HETZNER_API_TOKEN" =~ ^[a-zA-Z0-9]{64}$ ]]; then
  echo "⚠️  Warning: Token format unexpected"
  echo "Expected: 64 alphanumeric characters"
  echo "Got: ${#HETZNER_API_TOKEN} characters"
  echo ""
  echo "This might not be a valid Hetzner API token."
  echo "Continue anyway? (yes/no)"
fi
```

### Step 4: Save Token Securely

```bash
# Save to .env
echo "HETZNER_API_TOKEN=$HETZNER_API_TOKEN" >> .env

# Ensure .env is gitignored
if ! grep -q "^\.env$" .gitignore; then
  echo ".env" >> .gitignore
fi

# Create .env.example for team
cat > .env.example << 'EOF'
# Hetzner Cloud API Token
# Get from: https://console.hetzner.cloud/ → Security → API Tokens
HETZNER_API_TOKEN=your-hetzner-token-here
EOF

echo "✅ Token saved to .env (gitignored)"
echo "✅ Created .env.example for team (commit this)"
```

### Step 5: Use Token in Terraform

```hcl
# terraform/variables.tf
variable "hetzner_token" {
  description = "Hetzner Cloud API Token"
  type        = string
  sensitive   = true
}

# terraform/provider.tf
provider "hcloud" {
  token = var.hetzner_token
}

# Run Terraform
# export TF_VAR_hetzner_token=$HETZNER_API_TOKEN
# terraform apply
```

---

## Example Usage

**User**: "Deploy my NextJS app on Hetzner with Postgres, as cheaply as possible"

**hetzner-provisioner**:
```markdown
I'll provision your NextJS app on Hetzner Cloud for ~$12/month.

Infrastructure:
- CX11 instance (2 vCPU, 2GB RAM): $5.83/month
- Managed Postgres (2GB): $5.00/month
- 20GB storage: $0.50/month
- SSL (Let's Encrypt): Free
- Total: ~$11.33/month

Creating Terraform configuration...

✅ Generated files:
- terraform/main.tf
- terraform/variables.tf
- terraform/outputs.tf
- .github/workflows/deploy.yml

Next steps:
1. Set HETZNER_API_TOKEN in GitHub secrets
2. Push to GitHub
3. GitHub Actions will deploy automatically

Deployment URL: https://your-app.yourdomain.com (after DNS configured)
```

## Configuration

Supports multiple instance types:
- **CX11** (1 vCPU, 2GB RAM): $5.83/month - Small apps, 100-1000 users
- **CX21** (2 vCPU, 4GB RAM): $6.90/month - Medium apps, 1000-10000 users
- **CX31** (2 vCPU, 8GB RAM): $14.28/month - Larger apps, 10000+ users

Database options:
- Managed Postgres (2GB): $5/month
- Managed MySQL (2GB): $5/month
- Self-hosted (included in instance cost)

## Cost Comparison

| Platform | Small App | Medium App | Large App |
|----------|-----------|------------|-----------|
| **Hetzner** | $12/mo | $15/mo | $25/mo |
| Vercel | $60/mo | $120/mo | $240/mo |
| AWS | $25/mo | $80/mo | $200/mo |
| Railway | $20/mo | $50/mo | $100/mo |

**Savings**: 50-80% vs alternatives

## Technical Details

**Terraform Provider**: `hetznercloud/hcloud`
**API**: Hetzner Cloud API v1
**Regions**: Nuremberg, Falkenstein, Helsinki (Germany/Finland)
**Deployment**: Docker + GitHub Actions
**Monitoring**: Uptime Kuma (self-hosted, free)

## Integration

Works with:
- `cost-optimizer` - Recommends Hetzner when budget-conscious
- `devops-agent` - Strategic infrastructure planning
- `nextjs-agent` - NextJS-specific deployment
- Any backend framework (Node.js, Python, Go, etc.)

## Limitations

- EU-only data centers (GDPR-friendly)
- Requires Hetzner Cloud account
- Manual DNS configuration needed
- Not suitable for multi-region deployments (use AWS/GCP for that)

## Future Enhancements

- Kubernetes support (k3s on Hetzner)
- Load balancer configuration
- Multi-region deployment
- Disaster recovery setup

