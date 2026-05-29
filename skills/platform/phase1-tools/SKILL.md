# Phase 1 Execution Foundation Tools

Document processing and development tools for TAISUN v2.

## When to Use

- ドキュメント変換（Markdown → PDF/DOCX）
- PDF操作・編集
- 開発環境の検証・診断

## Enabled Capabilities (Mandatory)

### Core Tools

| Tool | Status | Description |
|------|--------|-------------|
| **Git** | ✅ Enabled | Version control |
| **Docker/Compose** | ✅ Enabled | Container orchestration |
| **Node.js** | ✅ Enabled | Runtime environment |
| **npm** | ✅ Enabled | Package management |

### Document Export Tools

| Tool | Status | Description |
|------|--------|-------------|
| **Pandoc** | ✅ Enabled | Universal document converter |
| **Marp** | ✅ Enabled | Markdown to slides |
| **Gotenberg** | ✅ Enabled | HTML/Office to PDF (Docker) |
| **Stirling-PDF** | ✅ Enabled | PDF manipulation toolkit |

## Disabled Capabilities (Optional)

These tools are disabled by default for security and resource optimization.
Enable only when explicitly needed with human approval.

### Observability

| Tool | Status | Description | Enable With |
|------|--------|-------------|-------------|
| **Sentry** | ❌ Disabled | Error tracking | `SENTRY_DSN` in .env |

### Database

| Tool | Status | Description | Enable With |
|------|--------|-------------|-------------|
| **PostgreSQL** | ❌ Disabled | Relational database | `POSTGRES_MCP_DSN` in .env |
| **Redis** | ❌ Disabled | Cache/Queue | `REDIS_URL` in .env |

### Project Management

| Tool | Status | Description | Enable With |
|------|--------|-------------|-------------|
| **Linear** | ❌ Disabled | Issue tracking | `LINEAR_API_KEY` in .env |
| **Notion** | ❌ Disabled | Knowledge base | `NOTION_API_KEY` in .env |

### Cloud Infrastructure

| Tool | Status | Description | Enable With |
|------|--------|-------------|-------------|
| **AWS** | ❌ Disabled | Cloud services | AWS credentials in .env |
| **Cloudflare** | ❌ Disabled | CDN/DNS | `CLOUDFLARE_API_TOKEN` in .env |
| **Kubernetes** | ❌ Disabled | Container orchestration | kubeconfig |

## Governance Principles

### 1. Minimal Permissions
- Tools run with least privilege
- Destructive operations require human approval
- No automatic resource provisioning

### 2. Secret Management
- All secrets in `.env` files
- Never commit secrets to git
- Use environment variables only

### 3. Idempotent Operations
- Scripts safe for re-execution
- No side effects on repeated runs
- Self-healing error recovery

### 4. Audit Trail
- All operations logged
- Changes tracked in git
- Metrics collected for analysis

## Usage

```bash
# Setup environment
make setup

# Verify installation
make verify

# Run diagnostics
make doctor

# Start document tools
make tools-up

# Export documents
make docs-export

# Stop document tools
make tools-down
```

## File Structure

```
scripts/phase1/
├── verify.sh      # Installation verification
├── doctor.sh      # System diagnostics
└── docs-export.sh # Document export

docker-compose.tools.yml  # Gotenberg + Stirling-PDF
.env.tools.example        # Tool configuration template
```

## Related Skills

- `pdf-automation-gotenberg` - Advanced PDF automation
- `doc-convert-pandoc` - Document conversion workflows
