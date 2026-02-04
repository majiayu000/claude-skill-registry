---
name: render-deployment
description: Guide for deploying Spring Boot backend to Render cloud platform. Use this when deploying, troubleshooting, or managing Render deployments.
---

# Render Deployment Guide

Deploy Spring Boot applications to Render's free/starter tier.

## Render Configuration (render.yaml)

```yaml
services:
  - type: web
    name: salon-hub-api
    runtime: docker
    dockerfilePath: ./Dockerfile
    plan: free  # or starter for always-on
    buildCommand: ./gradlew bootJar
    healthCheckPath: /actuator/health
    envVars:
      - key: SPRING_PROFILES_ACTIVE
        value: prod
      - key: DB_PASSWORD
        sync: false  # Set manually in dashboard
      - key: JWT_SECRET
        sync: false

databases:
  - name: salon-hub-db
    databaseName: salon_hub
    user: salon_hub_api
    plan: free
```

## Dockerfile for Render

```dockerfile
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app
COPY . .
RUN ./gradlew bootJar --no-daemon

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /app/build/libs/*.jar app.jar

# Render uses PORT env variable
ENV PORT=8082
EXPOSE ${PORT}

ENTRYPOINT ["java", "-XX:+UseContainerSupport", "-XX:MaxRAMPercentage=75.0", "-jar", "app.jar"]
```

## Environment Variables on Render

Set these in Render Dashboard → Environment:

| Variable | Value |
|----------|-------|
| `SPRING_PROFILES_ACTIVE` | `prod` |
| `DATABASE_JDBC_URL` | JDBC URL from Render Dashboard |
| `DB_USERNAME` | Database username from Render |
| `DB_PASSWORD` | Database password from Render |
| `JWT_SECRET` | Secure random string (256+ bits) |

### ⚠️ CRITICAL: Getting Database Credentials from Render Dashboard

**The MCP API does NOT provide database passwords.** You MUST get the actual connection string from the Render Dashboard:

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click on your PostgreSQL database
3. Click **"Connect"** button (top-right)
4. Copy the **Internal Database URL** or **External Database URL**

The URL format is:
```
postgresql://USER:PASSWORD@HOST:PORT/DATABASE
```

**Convert to JDBC format:**
```
jdbc:postgresql://HOST:PORT/DATABASE
```

Then set environment variables:
- `DATABASE_JDBC_URL`: The JDBC URL
- `DB_USERNAME`: The username from the URL
- `DB_PASSWORD`: The password from the URL (this is what you can't get via API!)

### Why MCP Can Connect But Your App Can't

The Render MCP server has **internal API access** to database credentials that aren't exposed through the public API. When `EOFException at doAuthentication` occurs:

1. **The password is wrong** - Get the actual password from Dashboard
2. The MCP `query_render_postgres` tool works because it uses Render's internal credential management
3. Your app needs the credentials manually set in environment variables

## Deploy Methods

### 1. Auto-Deploy (Recommended)
Connect GitHub repo → Render auto-deploys on push to `main`

### 2. Manual Deploy via Dashboard
Render Dashboard → Manual Deploy → Deploy latest commit

### 3. Deploy Hook (CI/CD)
```bash
curl -X POST "https://api.render.com/deploy/srv-YOUR-SERVICE-ID?key=YOUR-DEPLOY-KEY"
```

### 4. Render CLI
```bash
render deploys create srv-YOUR-SERVICE-ID
```

## Keep Alive for Free Tier

Free tier spins down after 15 min of inactivity. Use GitHub Actions:

```yaml
# .github/workflows/keep-alive.yml
name: Keep Render Alive

on:
  schedule:
    - cron: '*/5 * * * *'  # Every 5 minutes

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Health Endpoint
        run: |
          curl -s https://YOUR-APP.onrender.com/actuator/health
```

## Health Check Configuration

Render pings your health endpoint to verify deployment success:

```yaml
# application-prod.yml
management:
  endpoints:
    web:
      exposure:
        include: health,info
  endpoint:
    health:
      show-details: never  # Don't expose internals
```

## Troubleshooting

### Deploy Fails - Check Logs
1. Render Dashboard → Logs
2. Look for startup errors
3. Common issues: missing env vars, DB connection, port binding

### App Not Starting
- Ensure `PORT` environment variable is used (Render sets this)
- Check memory limits (free tier: 512MB)
- Verify health endpoint responds within timeout

### Database Connection Issues - CRITICAL

**IMPORTANT: PostgreSQL connection requires specific URL formats!**

#### Internal vs External URLs

Render provides TWO database URLs:

| Type | Format | Use Case |
|------|--------|----------|
| **Internal** | `dpg-xxx-a:5432` | Services in same Render region (faster, no SSL) |
| **External** | `dpg-xxx-a.oregon-postgres.render.com:5432` | External access (requires SSL) |

#### ⚠️ PORT IS REQUIRED!

**The port `:5432` is ALWAYS required**, even for internal URLs:

```yaml
# ❌ WRONG - Missing port causes EOFException
spring:
  datasource:
    url: jdbc:postgresql://dpg-xxx-a/salon_hub_db

# ✅ CORRECT - Always include :5432
spring:
  datasource:
    url: jdbc:postgresql://dpg-xxx-a:5432/salon_hub_db
```

#### Internal URL Configuration (Recommended for Render-to-Render)

```yaml
# prod.yml - For services within Render's network
spring:
  datasource:
    url: ${DATABASE_JDBC_URL:jdbc:postgresql://dpg-xxx-a:5432/database_name}
    username: ${DB_USERNAME:db_user}
    password: ${DB_PASSWORD:password}
    driver-class-name: org.postgresql.Driver
```

Environment variables on Render:
```
DATABASE_JDBC_URL=jdbc:postgresql://dpg-xxx-a:5432/database_name
DB_HOST=dpg-xxx-a
DB_PORT=5432
DB_NAME=database_name
DB_USERNAME=db_user
DB_PASSWORD=password
```

#### External URL Configuration (For external access)

```yaml
# Requires SSL for external connections
spring:
  datasource:
    url: jdbc:postgresql://dpg-xxx-a.oregon-postgres.render.com:5432/database_name?sslmode=require
```

#### Common Database Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `EOFException: null` at `doAuthentication` | Missing port `:5432` | Add `:5432` to URL |
| `The connection attempt failed` | Wrong hostname or network issue | Use internal URL for Render services |
| `SSL required` | External URL without SSL | Add `?sslmode=require` to external URLs |
| `Connection refused` | Wrong host or DB not running | Verify DB status in Render dashboard |

#### Environment Variables Required for Database

| Variable | Example Value | Notes |
|----------|---------------|-------|
| `DATABASE_URL` | `postgresql://user:pass@host:5432/db` | Standard format |
| `DATABASE_JDBC_URL` | `jdbc:postgresql://host:5432/db` | For Spring Boot |
| `DB_HOST` | `dpg-xxx-a` | Internal hostname |
| `DB_PORT` | `5432` | Always 5432 for PostgreSQL |
| `DB_NAME` | `salon_hub_db` | Database name |
| `DB_USERNAME` | `salon_hub_db_user` | Database user |
| `DB_PASSWORD` | `secret` | Database password |

### Cold Start Slow
Free tier takes 30-60 seconds to spin up. Options:
- Use keep-alive cron job
- Upgrade to starter plan ($7/month)

### Production Configuration Best Practices

```yaml
# prod.yml
spring:
  jpa:
    hibernate:
      ddl-auto: update    # NEVER use create-drop in production!
    show-sql: false       # Disable SQL logging for performance
  flyway:
    enabled: true         # Use migrations for schema changes
    baseline-on-migrate: true
```

**WARNING**: `ddl-auto: create-drop` will **DELETE ALL DATA** on every restart!

## Using Render MCP Tools

You can manage Render from VS Code using the Render MCP server:

### Setup
Add to `.vscode/mcp.json`:
```json
{
  "servers": {
    "render": {
      "url": "https://mcp.render.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_RENDER_API_KEY"
      }
    }
  }
}
```

### Available MCP Tools

| Tool | Description |
|------|-------------|
| `mcp_render_list_services` | List all services in workspace |
| `mcp_render_list_deploys` | View deployment history |
| `mcp_render_list_logs` | Get application logs |
| `mcp_render_list_postgres_instances` | List databases |
| `mcp_render_update_environment_variables` | Update env vars (triggers deploy) |
| `mcp_render_get_metrics` | CPU/memory/bandwidth metrics |

### Common MCP Operations

```
# Check deployment status
Ask: "List recent deploys for salon-hub-api"

# View error logs
Ask: "Show error logs for srv-xxx service"

# Update environment variables
Ask: "Update DATABASE_JDBC_URL to jdbc:postgresql://host:5432/db"
```

## URLs

| Resource | URL |
|----------|-----|
| **API Base** | `https://salon-hub-api.onrender.com` |
| **Health** | `https://salon-hub-api.onrender.com/actuator/health` |
| **Swagger** | `https://salon-hub-api.onrender.com/swagger-ui.html` |
| **Dashboard** | `https://dashboard.render.com` |

## Deployment Checklist

- [ ] All tests pass locally: `./gradlew check`
- [ ] Dockerfile builds successfully
- [ ] Environment variables set in Render
- [ ] Database provisioned and connected
- [ ] Push to main branch
- [ ] Verify deployment in Render dashboard
- [ ] Test health endpoint responds
- [ ] Test critical API endpoints
