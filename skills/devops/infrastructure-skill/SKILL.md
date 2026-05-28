---
document_name: "infrastructure.skill.md"
location: ".claude/skills/infrastructure.skill.md"
codebook_id: "CB-SKILL-INFRA-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for infrastructure as code and environment management"
skill_metadata:
  category: "devops"
  complexity: "advanced"
  estimated_time: "varies"
  prerequisites:
    - "Cloud provider access"
    - "IaC tool knowledge"
category: "skills"
status: "active"
tags:
  - "skill"
  - "infrastructure"
  - "devops"
  - "iac"
ai_parser_instructions: |
  This skill defines procedures for infrastructure management.
  Section markers: === SECTION ===
  Procedure markers: === PROCEDURE: NAME ===
---

# Infrastructure Skill

=== PURPOSE ===

This skill provides procedures for Infrastructure as Code and environment management. Used by the DevOps Engineer for all infrastructure work.

---

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(devops-engineer) @ref(CB-AGENT-DEVOPS-001) | Primary skill for infrastructure |

---

=== PREREQUISITES ===

Before using this skill:
- [ ] Cloud provider account configured
- [ ] IaC tool installed (Terraform, Pulumi, etc.)
- [ ] Security review from @agent(security-lead)

---

=== PROCEDURE: Environment Setup ===

**Environments:**
- **Development** - Local development, ephemeral
- **Staging** - Pre-production testing
- **Production** - Live environment

**Environment Parity Principle:**
Staging should mirror production as closely as possible.

---

=== PROCEDURE: Environment Variables ===

**Location:** `.env.example`

**Template:**
```bash
# Application
NODE_ENV=development
PORT=3000
LOG_LEVEL=debug

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/db

# External Services
API_KEY=your-api-key-here

# Feature Flags
FEATURE_NEW_UI=false
```

**Rules:**
- Never commit `.env` files
- Always provide `.env.example`
- Document all variables
- Use descriptive names

---

=== PROCEDURE: Docker Configuration ===

**Dockerfile Best Practices:**
```dockerfile
# Use specific version
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy dependency files first (caching)
COPY package*.json ./
RUN npm ci --only=production

# Copy application code
COPY . .

# Build application
RUN npm run build

# Non-root user
USER node

# Health check
HEALTHCHECK CMD curl -f http://localhost:3000/health || exit 1

# Start application
CMD ["npm", "start"]
```

---

=== PROCEDURE: Docker Compose ===

**Location:** `docker-compose.yml`

**Template:**
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    depends_on:
      - db
    volumes:
      - .:/app
      - /app/node_modules

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

=== PROCEDURE: Secret Management ===

**Purpose:** Handle sensitive configuration

**Options:**
- GitHub Secrets (for CI/CD)
- Cloud provider secret managers
- Vault (for complex setups)

**Rules:**
- Never store secrets in code
- Rotate secrets regularly
- Audit secret access
- Use least privilege

---

=== PROCEDURE: Infrastructure Documentation ===

**Location:** `infrastructure/README.md`

**Contents:**
- Architecture diagram
- Environment list
- Access instructions
- Runbooks for common operations
- Contact for issues

---

=== ANTI-PATTERNS ===

### Snowflake Servers
**Problem:** Manually configured servers
**Solution:** Use IaC for all infrastructure

### Secrets in Code
**Problem:** Credentials in repository
**Solution:** Use secret management

### No Environment Parity
**Problem:** Staging differs from production
**Solution:** Mirror configurations

### Missing Documentation
**Problem:** Undocumented infrastructure
**Solution:** Document everything

---

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(cicd-pipeline) | CI/CD uses infrastructure |
| @skill(deployment) | Deployment targets infrastructure |
| @skill(security-review) | Security reviews infrastructure |
