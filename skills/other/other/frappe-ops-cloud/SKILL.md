---
name: frappe-ops-cloud
description: >
  Use when working with Frappe Cloud, Press API, provisioning sites, or managing benches on Frappe Cloud infrastructure.
  Prevents failed deployments from misconfigured cloud settings and API misuse.
  Covers Frappe Cloud dashboard, Press API, site provisioning, bench management, environment variables, cloud-specific limitations.
  Keywords: Frappe Cloud, Press, cloud API, site provisioning, bench management, FC, frappecloud.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Cloud & Press

Complete reference for Frappe Cloud managed hosting and Press self-hosted alternative.

---

## Quick Reference — Frappe Cloud Concepts

| Concept | Description |
|---------|-------------|
| **Site** | A single Frappe instance with its own database, domain, and apps |
| **Bench** | A shared runtime environment hosting one or more sites with the same app versions |
| **Server** | The underlying infrastructure (VM) running one or more benches |
| **Private Bench** | A dedicated bench for a single customer with full control |
| **Shared Bench** | A Frappe-managed bench shared across multiple sites |
| **Press** | The open-source platform (AGPL-3.0) that powers Frappe Cloud |
| **Agent** | Flask application on each server enabling Press-to-site communication |

---

## Decision Tree: Frappe Cloud vs Self-Hosted

```
Choosing hosting strategy:
├── Small team, want zero ops overhead?
│   └── Frappe Cloud (Shared Bench) — fastest time to production
├── Need custom server configuration?
│   ├── Budget for managed infra? → Frappe Cloud (Private Bench)
│   └── Want full control? → Self-hosted with bench
├── Need to host Frappe for multiple clients?
│   ├── Want managed platform? → Frappe Cloud
│   └── Want own platform? → Self-hosted Press
├── Regulatory/compliance — data must stay on-premises?
│   └── Self-hosted (bench or Press)
└── Development/testing environment?
    ├── Quick prototype → Frappe Cloud (free trial)
    └── Long-term dev → Local bench installation
```

---

## Frappe Cloud Overview

Frappe Cloud is a fully managed hosting platform for the Frappe stack. It handles server provisioning, backups, updates, monitoring, and scaling.

### Core Features

| Feature | Details |
|---------|---------|
| **Automated backups** | Scheduled daily backups with retention policies |
| **Automatic updates** | Managed update cycles for Frappe apps |
| **Scaling** | Horizontal and vertical scaling without downtime |
| **Multi-tenancy** | Multiple independent sites per bench |
| **SSL/TLS** | Automatic certificate provisioning and renewal |
| **Monitoring** | Real-time server and site monitoring |
| **Role-based access** | Granular permissions for team members |
| **Billing** | Daily/monthly subscriptions, wallet credits, multiple payment methods |

### Infrastructure Options

| Option | Use Case |
|--------|----------|
| **Shared Bench** | Cost-effective for small sites; Frappe manages the bench |
| **Private Bench** | Dedicated environment; custom app versions and update schedules |
| **Dedicated Server** | Full server for high-traffic or compliance requirements |

---

## Frappe Cloud Dashboard

### Site Management

The dashboard provides centralized control for all site operations:

- **Create sites** — Provision new sites on shared or private benches
- **Install/remove apps** — Add or remove Frappe apps from sites
- **Backups** — Manual and scheduled backups, restore from backup
- **Domain management** — Add custom domains with automatic SSL
- **Site config** — Edit `site_config.json` via the dashboard
- **Monitoring** — View CPU, memory, disk usage, and request logs
- **Site actions** — Migrate, update, suspend, archive, or transfer sites

### Bench Management

- **Create benches** — Set up shared or private benches
- **App management** — Select apps and their versions/branches
- **Update scheduling** — Control when benches receive updates
- **Environment variables** — Set custom environment variables
- **SSH access** — Connect to bench via SSH for debugging
- **Log browser** — View application and error logs
- **Database access** — Query the database via the dashboard

### Server Management

- **Provision servers** — Create servers across multiple cloud providers
- **Scale resources** — Upgrade CPU, memory, and storage
- **Storage add-ons** — Attach additional storage volumes
- **Server snapshots** — Create and restore server snapshots

---

## Deploying Apps on Frappe Cloud

### Adding a Custom App

1. Navigate to **Apps** in the Frappe Cloud dashboard
2. Click **Add App** and provide the GitHub repository URL
3. Select the branch to deploy
4. Configure build settings if needed
5. The app becomes available for installation on sites within compatible benches

### App Marketplace

Frappe Cloud includes a marketplace where developers can:

- List apps with descriptions and pricing
- Set compatibility requirements (Frappe version, dependencies)
- Configure pricing models (free, one-time, subscription)
- Manage payouts for commercial apps
- Track installations and usage analytics

### Deployment Workflow

```
Developer pushes code → Frappe Cloud detects update →
  Bench rebuild triggered → Assets compiled →
    Sites migrated → New version live
```

**For Private Benches**: Updates are controlled by the bench owner — NEVER auto-deployed without approval.

**For Shared Benches**: Frappe manages the update schedule.

---

## Site Provisioning Workflow

### Creating a New Site

1. **Select bench** — Choose shared or private bench
2. **Choose plan** — Select resource allocation (CPU, memory, storage)
3. **Configure apps** — Select which apps to install
4. **Set domain** — Use `*.frappe.cloud` subdomain or custom domain
5. **Create** — Frappe Cloud provisions the site (typically under 5 minutes)

### Custom Domain Setup

1. Navigate to site **Domains** in the dashboard
2. Add your custom domain (e.g., `erp.example.com`)
3. Configure DNS: Add a **CNAME** record pointing to the Frappe Cloud proxy
4. Frappe Cloud verifies DNS and provisions SSL certificate automatically
5. **ALWAYS** wait for DNS propagation before expecting SSL to work (up to 48 hours)

### Critical Rules

- **ALWAYS** use CNAME records for custom domains (not A records)
- **NEVER** transfer DNS to Frappe Cloud — only add CNAME records
- **ALWAYS** verify SSL is active before switching production traffic
- Custom domain SSL uses Let's Encrypt — auto-renews before expiry

---

## Frappe Cloud vs Self-Hosted Comparison

| Aspect | Frappe Cloud | Self-Hosted (bench) | Self-Hosted (Press) |
|--------|:------------:|:-------------------:|:-------------------:|
| **Setup time** | Minutes | Hours | Days |
| **Server management** | Managed | You manage | You manage |
| **Backups** | Automatic | Manual/cron | Automatic |
| **Updates** | Managed schedule | `bench update` | Managed via Press |
| **SSL certificates** | Automatic | Manual/certbot | Automatic |
| **Scaling** | Dashboard button | Manual | Dashboard |
| **Multi-tenancy** | Built-in | DNS multi-tenant | Built-in |
| **Cost** | Subscription | Infrastructure only | Infrastructure only |
| **Custom server config** | Limited | Full control | Full control |
| **Data sovereignty** | Frappe's infra | Your infra | Your infra |
| **SSH access** | Private bench only | Full | Full |
| **Monitoring** | Built-in | Set up yourself | Built-in |
| **Support** | Included | Community only | Community only |

---

## Press: Self-Hosted Frappe Cloud

### What Is Press?

Press is the open-source platform (AGPL-3.0) that powers Frappe Cloud. Organizations can self-host Press to create their own managed hosting platform for Frappe applications.

**GitHub**: `https://github.com/frappe/press`

### Architecture

| Component | Technology | Role |
|-----------|-----------|------|
| Press | Frappe Framework | Platform management, billing, dashboard |
| Agent | Flask | Server-to-site communication |
| Docker | Container runtime | App packaging and deployment |
| Ansible | Automation | Server provisioning and configuration |
| Frappe UI | Vue.js | Dashboard frontend |

### Key Capabilities

- **Multi-server management** — Provision and manage multiple servers
- **Site lifecycle** — Create, update, migrate, backup, restore, archive sites
- **Bench management** — Deploy benches with specific app versions
- **Billing system** — Subscriptions, invoicing, wallet credits, ERP integration
- **Marketplace** — App listing, pricing, payouts
- **Role-based access** — Granular permissions per team and resource
- **Monitoring** — Real-time metrics and alerting

### When to Self-Host Press

- You need to host Frappe for multiple clients/tenants
- You want a managed platform but on your own infrastructure
- You need full data sovereignty and regulatory compliance
- You want to offer Frappe hosting as a service

### When NOT to Self-Host Press

- **NEVER** self-host Press for a single site — use bench directly
- **NEVER** self-host Press without dedicated DevOps capacity
- **NEVER** underestimate the operational overhead — Press itself requires maintenance

### Self-Hosting Requirements

- Dedicated servers (bare metal or VMs) with Ubuntu
- DNS management for wildcard domains
- Object storage for backups (S3-compatible)
- SMTP service for transactional email
- Familiarity with Ansible, Docker, and Frappe Framework

---

## Frappe Cloud Limitations

### What You CANNOT Do on Frappe Cloud

- Install system-level packages (no root access on shared benches)
- Modify Nginx/Supervisor configuration directly
- Access raw database files (only SQL access via dashboard)
- Run long-running background processes outside Frappe's job queue
- Use non-standard ports or protocols

### Shared Bench Limitations

- No SSH access
- No custom environment variables (use site_config.json instead)
- Shared resources with other sites — performance may vary
- Update schedule controlled by Frappe (not the site owner)

### Private Bench Advantages Over Shared

- SSH access for debugging
- Custom environment variables
- Controlled update schedule
- Dedicated resources
- Custom app versions and branches

---

## Frappe Cloud Best Practices

### Site Configuration

- **ALWAYS** set `maintenance_mode` before large data imports
- **ALWAYS** use the dashboard for site config changes (not direct file edits)
- **NEVER** disable scheduler on Frappe Cloud — use `pause_scheduler` instead
- **ALWAYS** test app updates on a staging site before production

### Backup Strategy

- Frappe Cloud creates automatic daily backups
- **ALWAYS** create a manual backup before major changes
- **ALWAYS** download and store backups off-platform periodically
- **NEVER** rely solely on Frappe Cloud backups — maintain your own copies

### Performance

- Monitor site usage via the dashboard — upgrade plan before hitting limits
- Use background jobs for heavy operations (not synchronous API calls)
- Enable Redis caching for frequently accessed data
- Review slow query logs via the database analyzer tool

---

## Frappe Cloud DevOps Tools

| Tool | Purpose |
|------|---------|
| **Log Browser** | View application logs, error logs, scheduler logs |
| **Database Analyzer** | Run SQL queries, view slow queries, analyze indexes |
| **Binlog Browser** | View database change logs (binary log events) |
| **SSH Access** | Terminal access to private benches for debugging |
| **Process Status** | View running workers, scheduler status, job queue |

### Analytics Integrations

Frappe Cloud sites can connect to external analytics tools:
- Frappe Insights (native)
- Power BI (via API)
- Metabase (via database connection)
- Custom dashboards (via Frappe API)

---

## Reference Files

| File | Contents |
|------|----------|
| [examples.md](references/examples.md) | Cloud deployment workflow examples |
| [anti-patterns.md](references/anti-patterns.md) | Common Frappe Cloud mistakes and fixes |
