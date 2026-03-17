---
name: dokploy-mcp
description: AI-driven deployment management using Dokploy MCP server for projects, applications, and databases
version: 1.0.0
category: devops-automation
complexity: complex
author: Claude Command and Control
created: 2025-12-27
status: active
---

# Dokploy MCP Skill

## Description

AI-powered deployment management skill that leverages the Dokploy MCP (Model Context Protocol) server to orchestrate complete deployment workflows. Provides intelligent automation for project lifecycle, application deployment, database provisioning, Git provider configuration, and build system management across 43 specialized tools.

## When to Use This Skill

**Explicit Triggers:**
- When user says "deploy to Dokploy" or "manage Dokploy deployment"
- When asked to "create a new Dokploy project" or "setup Dokploy application"
- When managing database instances: "provision PostgreSQL on Dokploy"
- When configuring Git providers: "connect GitHub/GitLab/Bitbucket to Dokploy app"
- When monitoring deployments: "check Dokploy application status"
- When troubleshooting: "debug Dokploy deployment failure"
- When scaling: "update Dokploy app replicas" or "configure resource limits"

**Context Patterns:**
- DevOps workflows requiring deployment automation
- CI/CD pipeline integration with Dokploy
- Multi-environment deployment management (dev/staging/prod)
- Database provisioning and configuration
- Application lifecycle management (deploy, monitor, rollback)

## When NOT to Use This Skill

- When deploying to other platforms (use platform-specific skills: aws-deploy, gcp-deploy, k8s-deploy)
- When managing Kubernetes directly (use k8s-management skill instead)
- When writing Dockerfiles (use dockerfile-builder skill instead)
- For local development (use local-dev-setup skill)
- When Dokploy server is not configured or unavailable

## Prerequisites

### Environment Setup
1. **Dokploy Server Access**:
   - `DOKPLOY_URL` environment variable set to API endpoint (e.g., `https://dokploy.example.com/api`)
   - `DOKPLOY_API_KEY` environment variable set to authentication token

2. **MCP Server Installation**:
   ```bash
   # Verify MCP server is available
   npx -y @ahdev/dokploy-mcp
   ```

3. **Network Connectivity**:
   - Access to Dokploy API endpoint
   - Outbound HTTPS access for Git provider integrations

### Knowledge Prerequisites
- Understanding of deployment concepts (projects, environments, services)
- Familiarity with Git workflows and providers
- Basic knowledge of Docker and containerization
- PostgreSQL database administration (for database management)

### Tool Dependencies
- **MCP Servers**: Dokploy MCP server (`@ahdev/dokploy-mcp`)
- **Git Providers**: GitHub, GitLab, Bitbucket, Gitea tokens (as needed)
- **Docker Registry**: Credentials for private image access (optional)

## Workflow

### Phase 1: Initial Assessment

**Step 1.1: Validate Environment**
```bash
# Check environment variables
echo "Dokploy URL: ${DOKPLOY_URL:-(not set)}"
echo "API Key: ${DOKPLOY_API_KEY:+(configured)}"

# Test API connectivity
curl -f "${DOKPLOY_URL}/health" -H "Authorization: Bearer ${DOKPLOY_API_KEY}"
```

**Decision Point**: If environment invalid → Guide user through setup

**Step 1.2: Understand User Intent**

Ask clarifying questions:
1. What are you trying to deploy? (web app, API, database, full stack)
2. What's the Git repository URL? (if applicable)
3. What environment? (development, staging, production)
4. Any special requirements? (custom domain, SSL, environment variables)

**Step 1.3: List Existing Resources**

Use MCP tool: `dokploy-mcp:project-all`
```javascript
// Get all projects with environments and services
const projects = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "project-all",
  arguments: {}
});
```

Display summary to user:
```
📊 Current Dokploy Resources:

Projects (3):
  • production-env (5 apps, 2 databases)
  • staging-env (3 apps, 1 database)
  • development-env (2 apps)
```

### Phase 2: Project & Environment Setup

**Step 2.1: Create or Select Project**

**If new project needed**:

Use MCP tool: `dokploy-mcp:project-create`
```javascript
const project = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "project-create",
  arguments: {
    name: "my-project",
    description: "Production environment for MyApp",
    env: "NODE_ENV=production\nLOG_LEVEL=info"
  }
});
```

**If using existing project**:

Use MCP tool: `dokploy-mcp:project-one`
```javascript
const project = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "project-one",
  arguments: {
    projectId: "proj_abc123"
  }
});
```

**Step 2.2: Duplicate Environment (Optional)**

For creating new environments from existing:

Use MCP tool: `dokploy-mcp:project-duplicate`
```javascript
const newEnv = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "project-duplicate",
  arguments: {
    sourceEnvironmentId: "env_prod_123",
    name: "staging-v2",
    duplicateInSameProject: false,
    includeServices: true,
    selectedServices: [
      { id: "app_api_456", type: "application" },
      { id: "db_postgres_789", type: "postgres" }
    ]
  }
});
```

### Phase 3: Application Deployment

**Step 3.1: Create Application**

Use MCP tool: `dokploy-mcp:application-create`
```javascript
const app = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-create",
  arguments: {
    name: "api-service",
    appName: "myapp-api",
    environmentId: project.environmentId,
    description: "REST API backend service"
  }
});
```

**Step 3.2: Configure Git Provider**

**Decision Tree**: Which Git provider?

| Provider | Use When | MCP Tool |
|----------|----------|----------|
| GitHub | Public/private GitHub repos | `application-saveGithubProvider` |
| GitLab | Self-hosted or GitLab.com | `application-saveGitlabProvider` |
| Bitbucket | Atlassian ecosystem | `application-saveBitbucketProvider` |
| Gitea | Self-hosted Gitea | `application-saveGiteaProvider` |
| Custom Git | Generic Git server | `application-saveGitProvider` |
| Docker Image | Pre-built images | `application-saveDockerProvider` |

**Example: GitHub Integration**
```javascript
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-saveGithubProvider",
  arguments: {
    applicationId: app.applicationId,
    repository: "https://github.com/org/repo",
    owner: "org",
    branch: "main",
    buildPath: "./",
    githubId: "github_integration_123",
    enableSubmodules: false,
    triggerType: "push",
    watchPaths: ["src/**", "package.json"]
  }
});
```

**Step 3.3: Configure Build System**

**Decision Tree**: Which build type?

| Build Type | Use When | Configuration |
|-----------|----------|---------------|
| `dockerfile` | Custom Dockerfile exists | Specify `dockerfile`, `dockerContextPath`, `dockerBuildStage` |
| `nixpacks` | Auto-detect framework (Next.js, React, etc.) | Minimal config needed |
| `heroku_buildpacks` | Heroku-compatible apps | Specify `herokuVersion` |
| `paketo_buildpacks` | Cloud-native buildpacks | Auto-detection |
| `static` | Static sites (React build, Vue, etc.) | Set `isStaticSpa`, `publishDirectory` |
| `railpack` | Rails applications | Specify `railpackVersion` |

**Example: Dockerfile Build**
```javascript
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-saveBuildType",
  arguments: {
    applicationId: app.applicationId,
    buildType: "dockerfile",
    dockerfile: "Dockerfile",
    dockerContextPath: "./",
    dockerBuildStage: "production"
  }
});
```

**Step 3.4: Configure Environment Variables**

Use MCP tool: `dokploy-mcp:application-saveEnvironment`
```javascript
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-saveEnvironment",
  arguments: {
    applicationId: app.applicationId,
    env: `NODE_ENV=production
DATABASE_URL=postgresql://user:pass@db:5432/mydb
API_KEY=\${SECRET_API_KEY}
REDIS_URL=redis://cache:6379`,
    buildArgs: `NPM_TOKEN=\${NPM_TOKEN}
BUILD_ENV=production`
  }
});
```

**Step 3.5: Deploy Application**

Use MCP tool: `dokploy-mcp:application-deploy`
```javascript
const deployment = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-deploy",
  arguments: {
    applicationId: app.applicationId,
    title: "Initial deployment v1.0.0",
    description: "First production deployment with new feature X"
  }
});
```

**Monitor Deployment Progress**:
```javascript
// Check application status
const status = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-one",
  arguments: { applicationId: app.applicationId }
});

console.log(`Status: ${status.applicationStatus}`); // idle | running | done | error
```

### Phase 4: Database Provisioning

**Step 4.1: Create PostgreSQL Database**

Use MCP tool: `dokploy-mcp:postgres-create`
```javascript
const db = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "postgres-create",
  arguments: {
    name: "production-db",
    appName: "myapp-postgres",
    environmentId: project.environmentId,
    databaseName: "myapp",
    databaseUser: "myapp_user",
    databasePassword: "secure_random_password_123",
    dockerImage: "postgres:16",
    description: "Production PostgreSQL database"
  }
});
```

**Step 4.2: Configure Database Environment**

Use MCP tool: `dokploy-mcp:postgres-saveEnvironment`
```javascript
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "postgres-saveEnvironment",
  arguments: {
    postgresId: db.postgresId,
    env: `POSTGRES_MAX_CONNECTIONS=200
POSTGRES_SHARED_BUFFERS=256MB
POSTGRES_WORK_MEM=16MB`
  }
});
```

**Step 4.3: Expose External Port (Optional)**

Use MCP tool: `dokploy-mcp:postgres-saveExternalPort`
```javascript
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "postgres-saveExternalPort",
  arguments: {
    postgresId: db.postgresId,
    externalPort: 5432
  }
});
```

**Step 4.4: Deploy Database**

Use MCP tool: `dokploy-mcp:postgres-deploy`
```javascript
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "postgres-deploy",
  arguments: {
    postgresId: db.postgresId
  }
});
```

### Phase 5: Domain & Networking Configuration

**Step 5.1: Create Domain**

Use MCP tool: `dokploy-mcp:domain-create`
```javascript
const domain = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "domain-create",
  arguments: {
    host: "api.example.com",
    https: true,
    certificateType: "letsencrypt",
    port: 3000,
    path: "/",
    stripPath: false,
    domainType: "application",
    applicationId: app.applicationId
  }
});
```

**Step 5.2: Validate Domain Configuration**

Use MCP tool: `dokploy-mcp:domain-validateDomain`
```javascript
const validation = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "domain-validateDomain",
  arguments: {
    domain: "api.example.com",
    serverIp: "203.0.113.42"
  }
});

if (!validation.valid) {
  console.warn(`⚠️ DNS not configured: ${validation.message}`);
}
```

### Phase 6: Monitoring & Management

**Step 6.1: Check Application Monitoring**

Use MCP tool: `dokploy-mcp:application-readAppMonitoring`
```javascript
const metrics = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-readAppMonitoring",
  arguments: {
    appName: "myapp-api"
  }
});

// Display metrics
console.log(`
📊 Application Metrics:
  CPU: ${metrics.cpu}%
  Memory: ${metrics.memory}MB
  Uptime: ${metrics.uptime}s
  Requests: ${metrics.requests}/min
`);
```

**Step 6.2: Manage Application Lifecycle**

| Action | MCP Tool | Use When |
|--------|----------|----------|
| Start | `application-start` | Application stopped, need to bring online |
| Stop | `application-stop` | Maintenance, scaling down |
| Restart | `application-reload` | Config changes, minor updates |
| Redeploy | `application-redeploy` | New code, force rebuild |
| Rollback | `application-deploy` (previous version) | Deployment failure |

**Example: Redeploy Application**
```javascript
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-redeploy",
  arguments: {
    applicationId: app.applicationId,
    title: "Hotfix deployment v1.0.1",
    description: "Critical bug fix for authentication issue"
  }
});
```

### Phase 7: Error Handling & Recovery

**Step 7.1: Detect Deployment Failures**

```javascript
const app = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-one",
  arguments: { applicationId: "app_123" }
});

if (app.applicationStatus === "error") {
  // Investigate failure
  console.error("❌ Deployment failed!");

  // Read Traefik logs for routing issues
  const traefikConfig = await use_mcp_tool({
    server_name: "dokploy-mcp",
    tool_name: "application-readTraefikConfig",
    arguments: { applicationId: app.applicationId }
  });

  // Check build logs, container logs, etc.
}
```

**Step 7.2: Common Failure Modes**

| Error | Symptom | Resolution |
|-------|---------|------------|
| Build Failure | Status stuck at "running" | Check build logs, verify Dockerfile, check dependencies |
| Start Failure | Container exits immediately | Check environment variables, validate entry point |
| Network Issues | App deploys but unreachable | Validate domain configuration, check port mappings |
| Database Connection | App fails health checks | Verify DATABASE_URL, check network connectivity |
| Resource Limits | OOM errors | Increase `memoryLimit`, optimize application |

**Step 7.3: Cancel Stuck Deployments**

Use MCP tool: `dokploy-mcp:application-cancelDeployment`
```javascript
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-cancelDeployment",
  arguments: {
    applicationId: app.applicationId
  }
});
```

**Step 7.4: Clean Deployment Queues**

Use MCP tool: `dokploy-mcp:application-cleanQueues`
```javascript
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-cleanQueues",
  arguments: {
    applicationId: app.applicationId
  }
});
```

## Examples

### Example 1: Deploy Node.js API from GitHub

**Scenario**: Deploy a production-ready Express.js API with PostgreSQL database

**Input**:
```
User: "Deploy my Express API from GitHub to Dokploy production environment"
Repo: https://github.com/myorg/express-api
Branch: main
Environment: production
Database: PostgreSQL 16
```

**Workflow Execution**:

```javascript
// 1. Create project
const project = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "project-create",
  arguments: {
    name: "production-api",
    description: "Production environment for Express API",
    env: "NODE_ENV=production"
  }
});

// 2. Create application
const app = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-create",
  arguments: {
    name: "express-api",
    appName: "myorg-express-api",
    environmentId: project.environmentId,
    description: "Express.js REST API"
  }
});

// 3. Configure GitHub
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-saveGithubProvider",
  arguments: {
    applicationId: app.applicationId,
    repository: "https://github.com/myorg/express-api",
    owner: "myorg",
    branch: "main",
    buildPath: "./",
    githubId: null, // Will use GitHub App integration
    enableSubmodules: false,
    triggerType: "push"
  }
});

// 4. Configure Dockerfile build
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-saveBuildType",
  arguments: {
    applicationId: app.applicationId,
    buildType: "dockerfile",
    dockerfile: "Dockerfile",
    dockerContextPath: "./",
    dockerBuildStage: "production"
  }
});

// 5. Create PostgreSQL database
const db = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "postgres-create",
  arguments: {
    name: "api-database",
    appName: "express-api-db",
    environmentId: project.environmentId,
    databaseName: "express_api",
    databaseUser: "api_user",
    databasePassword: "generated_secure_password_456",
    dockerImage: "postgres:16"
  }
});

// 6. Deploy database
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "postgres-deploy",
  arguments: { postgresId: db.postgresId }
});

// 7. Configure app environment with database URL
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-saveEnvironment",
  arguments: {
    applicationId: app.applicationId,
    env: `NODE_ENV=production
DATABASE_URL=postgresql://api_user:generated_secure_password_456@express-api-db:5432/express_api
PORT=3000
LOG_LEVEL=info`,
    buildArgs: ""
  }
});

// 8. Deploy application
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-deploy",
  arguments: {
    applicationId: app.applicationId,
    title: "Initial production deployment",
    description: "First deployment to production environment"
  }
});

// 9. Configure domain with SSL
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "domain-create",
  arguments: {
    host: "api.myorg.com",
    https: true,
    certificateType: "letsencrypt",
    port: 3000,
    path: "/",
    stripPath: false,
    domainType: "application",
    applicationId: app.applicationId
  }
});
```

**Expected Output**:
```
✅ Deployment Complete!

Project: production-api (proj_abc123)
Application: express-api (app_def456)
  Status: running ✓
  URL: https://api.myorg.com
  Build: Dockerfile (production stage)

Database: api-database (db_ghi789)
  Status: running ✓
  Engine: PostgreSQL 16
  Internal: express-api-db:5432

Next Steps:
  • Monitor: /check-deployment app_def456
  • Logs: /view-logs app_def456
  • Rollback: /rollback-deployment app_def456
```

**Rationale**: This example demonstrates a complete production deployment workflow including project creation, Git integration, database provisioning, environment configuration, and domain setup with SSL.

---

### Example 2: Deploy Static React App with Nixpacks

**Scenario**: Auto-detect and deploy a React SPA using Nixpacks buildpack

**Input**:
```
User: "Deploy my React app from GitLab to Dokploy staging"
Repo: https://gitlab.com/team/react-dashboard
Branch: develop
Build: Auto-detect (Nixpacks)
Environment: staging
```

**Workflow Execution**:

```javascript
// 1. Use existing staging project
const project = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "project-one",
  arguments: { projectId: "proj_staging_123" }
});

// 2. Create application
const app = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-create",
  arguments: {
    name: "react-dashboard",
    appName: "dashboard-staging",
    environmentId: project.environmentId
  }
});

// 3. Configure GitLab
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-saveGitlabProvider",
  arguments: {
    applicationId: app.applicationId,
    gitlabRepository: "https://gitlab.com/team/react-dashboard",
    gitlabOwner: "team",
    gitlabBranch: "develop",
    gitlabBuildPath: "./",
    gitlabId: "gitlab_integration_789",
    gitlabProjectId: 42,
    gitlabPathNamespace: "team/react-dashboard",
    enableSubmodules: false
  }
});

// 4. Configure Nixpacks build (auto-detect React)
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-saveBuildType",
  arguments: {
    applicationId: app.applicationId,
    buildType: "nixpacks",
    dockerContextPath: "./",
    dockerBuildStage: null, // Not needed for Nixpacks
    isStaticSpa: true,
    publishDirectory: "dist" // React build output
  }
});

// 5. Configure environment
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-saveEnvironment",
  arguments: {
    applicationId: app.applicationId,
    env: `VITE_API_URL=https://api-staging.example.com
VITE_ENV=staging`,
    buildArgs: `NODE_VERSION=20`
  }
});

// 6. Deploy
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-deploy",
  arguments: {
    applicationId: app.applicationId,
    title: "Staging deployment",
    description: "Auto-deploy from develop branch"
  }
});
```

**Expected Output**:
```
✅ React App Deployed!

Application: react-dashboard (app_xyz789)
  Status: running ✓
  Build: Nixpacks (auto-detected React + Vite)
  Environment: staging

Build Details:
  • Detected: React 18 + Vite
  • Node.js: 20.x
  • Output: dist/ directory
  • Type: Static SPA

URL: (domain not configured yet)

Tip: Add domain with:
  /add-domain app_xyz789 dashboard-staging.example.com
```

**Rationale**: Demonstrates auto-detection capabilities of Nixpacks for modern JavaScript frameworks and static site deployment workflow.

---

### Example 3: Troubleshoot Failed Deployment

**Scenario**: Application deployment stuck in "running" status, need to debug and fix

**Input**:
```
User: "My app deployment is stuck, can you help debug?"
Application ID: app_trouble_123
Expected: Should be "done"
Actual: Stuck at "running" for 15 minutes
```

**Workflow Execution**:

```javascript
// 1. Check current status
const app = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-one",
  arguments: { applicationId: "app_trouble_123" }
});

console.log(`Current Status: ${app.applicationStatus}`);
console.log(`Last Deployment: ${app.lastDeployment?.timestamp}`);

// 2. Check Traefik routing config
const traefikConfig = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-readTraefikConfig",
  arguments: { applicationId: "app_trouble_123" }
});

// 3. Check monitoring metrics
try {
  const metrics = await use_mcp_tool({
    server_name: "dokploy-mcp",
    tool_name: "application-readAppMonitoring",
    arguments: { appName: app.appName }
  });
  console.log("App Metrics:", metrics);
} catch (error) {
  console.warn("⚠️ Monitoring unavailable - app may not be running");
}

// 4. Cancel stuck deployment
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-cancelDeployment",
  arguments: { applicationId: "app_trouble_123" }
});

// 5. Clean deployment queues
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-cleanQueues",
  arguments: { applicationId: "app_trouble_123" }
});

// 6. Review configuration for issues
const buildConfig = {
  buildType: app.buildType,
  dockerfile: app.dockerfile,
  dockerImage: app.dockerImage,
  env: app.env
};

console.log("Build Configuration:", buildConfig);

// Identify issue: Missing required environment variable
const missingVars = [];
if (!app.env.includes("DATABASE_URL")) {
  missingVars.push("DATABASE_URL");
}

if (missingVars.length > 0) {
  console.warn(`❌ Missing environment variables: ${missingVars.join(", ")}`);

  // 7. Fix environment configuration
  await use_mcp_tool({
    server_name: "dokploy-mcp",
    tool_name: "application-saveEnvironment",
    arguments: {
      applicationId: "app_trouble_123",
      env: `${app.env}
DATABASE_URL=postgresql://user:pass@db:5432/mydb`,
      buildArgs: app.buildArgs
    }
  });
}

// 8. Redeploy with fix
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-redeploy",
  arguments: {
    applicationId: "app_trouble_123",
    title: "Fix: Added missing DATABASE_URL",
    description: "Resolved deployment failure by adding required environment variable"
  }
});
```

**Expected Output**:
```
🔍 Debugging Deployment...

Current Status: running (stuck for 15 min)

Issues Found:
  ❌ Missing environment variable: DATABASE_URL
  ⚠️ Container health check failing

Actions Taken:
  1. Cancelled stuck deployment
  2. Cleaned deployment queues
  3. Added missing DATABASE_URL
  4. Redeploying with fixes

New Deployment Status: running ⏳
  → Monitor with: /check-deployment app_trouble_123

Root Cause: Application couldn't connect to database due to missing DATABASE_URL
Resolution: Added connection string to environment configuration
```

**Rationale**: Shows systematic debugging approach using monitoring tools, configuration review, and deployment lifecycle management to identify and resolve common deployment failures.

---

### Example 4: Multi-Environment Duplication

**Scenario**: Clone production environment to create identical staging setup

**Input**:
```
User: "Clone my production setup to create a new staging-v2 environment"
Source: production-env (env_prod_123)
Target: staging-v2 (new)
Include: All services (3 apps, 2 databases)
```

**Workflow Execution**:

```javascript
// 1. Get source environment details
const prodProject = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "project-one",
  arguments: { projectId: "proj_prod_123" }
});

// Extract all services from production
const services = [
  // Applications
  { id: "app_api_456", type: "application" },
  { id: "app_web_457", type: "application" },
  { id: "app_worker_458", type: "application" },
  // Databases
  { id: "db_postgres_789", type: "postgres" },
  { id: "db_redis_790", type: "redis" }
];

// 2. Duplicate environment
const stagingV2 = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "project-duplicate",
  arguments: {
    sourceEnvironmentId: "env_prod_123",
    name: "staging-v2",
    description: "Staging environment v2 - cloned from production",
    duplicateInSameProject: false,
    includeServices: true,
    selectedServices: services
  }
});

// 3. Update environment variables for staging
for (const service of services) {
  if (service.type === "application") {
    await use_mcp_tool({
      server_name: "dokploy-mcp",
      tool_name: "application-saveEnvironment",
      arguments: {
        applicationId: service.id, // Maps to new duplicated ID
        env: `NODE_ENV=staging
API_URL=https://api-staging-v2.example.com
LOG_LEVEL=debug`, // More verbose for staging
        buildArgs: ""
      }
    });
  }
}

// 4. Update domains for staging
const domains = [
  { app: "app_api_456", host: "api-staging-v2.example.com" },
  { app: "app_web_457", host: "app-staging-v2.example.com" }
];

for (const { app, host } of domains) {
  await use_mcp_tool({
    server_name: "dokploy-mcp",
    tool_name: "domain-create",
    arguments: {
      host: host,
      https: true,
      certificateType: "letsencrypt",
      port: 3000,
      domainType: "application",
      applicationId: app,
      stripPath: false
    }
  });
}
```

**Expected Output**:
```
✅ Environment Duplicated!

Source: production-env (env_prod_123)
Target: staging-v2 (env_staging_v2_999)

Cloned Services (5):
  Applications (3):
    • api-service → api-service-staging-v2
    • web-frontend → web-frontend-staging-v2
    • background-worker → background-worker-staging-v2

  Databases (2):
    • production-db → staging-v2-db
    • redis-cache → redis-cache-staging-v2

Configuration Updates:
  ✓ Environment variables updated for staging
  ✓ Domains configured (.staging-v2.example.com)
  ✓ SSL certificates provisioned

Ready to Deploy:
  /deploy-all staging-v2
```

**Rationale**: Demonstrates environment duplication for testing, staging, or disaster recovery scenarios while maintaining configuration parity with modifications for environment-specific settings.

---

### Example 5: Database Migration and Scaling

**Scenario**: Provision new PostgreSQL database, migrate data, and configure high availability

**Input**:
```
User: "Create a new PostgreSQL 16 database with replication and external access"
Environment: production
Database: user-data-v2
Replicas: 3 (high availability)
External Port: 5432
```

**Workflow Execution**:

```javascript
// 1. Create primary database
const db = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "postgres-create",
  arguments: {
    name: "user-data-v2",
    appName: "userdata-v2-primary",
    environmentId: "env_prod_123",
    databaseName: "userdata",
    databaseUser: "userdata_admin",
    databasePassword: "super_secure_password_789",
    dockerImage: "postgres:16",
    description: "Production user data database with HA"
  }
});

// 2. Configure performance tuning
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "postgres-saveEnvironment",
  arguments: {
    postgresId: db.postgresId,
    env: `POSTGRES_MAX_CONNECTIONS=300
POSTGRES_SHARED_BUFFERS=512MB
POSTGRES_EFFECTIVE_CACHE_SIZE=2GB
POSTGRES_MAINTENANCE_WORK_MEM=128MB
POSTGRES_CHECKPOINT_COMPLETION_TARGET=0.9
POSTGRES_WAL_BUFFERS=16MB
POSTGRES_DEFAULT_STATISTICS_TARGET=100`
  }
});

// 3. Update resource limits for HA
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "postgres-update",
  arguments: {
    postgresId: db.postgresId,
    replicas: 3, // High availability with 3 replicas
    memoryLimit: "2048",
    memoryReservation: "1024",
    cpuLimit: "2.0",
    cpuReservation: "1.0",
    restartPolicySwarm: {
      Condition: "on-failure",
      Delay: 10000000000, // 10 seconds
      MaxAttempts: 5,
      Window: 120000000000 // 2 minutes
    },
    updateConfigSwarm: {
      Parallelism: 1,
      Delay: 30000000000, // 30 seconds between updates
      FailureAction: "rollback",
      Monitor: 60000000000, // 1 minute monitoring
      MaxFailureRatio: 0.3,
      Order: "stop-first"
    }
  }
});

// 4. Expose external port for client access
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "postgres-saveExternalPort",
  arguments: {
    postgresId: db.postgresId,
    externalPort: 5432
  }
});

// 5. Deploy database with HA configuration
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "postgres-deploy",
  arguments: {
    postgresId: db.postgresId
  }
});

// 6. Verify deployment and health
const deployed = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "postgres-one",
  arguments: {
    postgresId: db.postgresId
  }
});

console.log(`Database Status: ${deployed.applicationStatus}`);
console.log(`Replicas: ${deployed.replicas}`);
console.log(`External Access: ${deployed.externalPort ? 'Enabled on port ' + deployed.externalPort : 'Disabled'}`);
```

**Expected Output**:
```
✅ High-Availability Database Deployed!

Database: user-data-v2 (db_ha_999)
  Status: running ✓
  Engine: PostgreSQL 16
  Replicas: 3 (high availability)

Configuration:
  Memory: 2GB limit, 1GB reserved
  CPU: 2.0 limit, 1.0 reserved
  Max Connections: 300

Network:
  Internal: userdata-v2-primary:5432
  External: dokploy-server.com:5432

Connection String:
  postgresql://userdata_admin:***@dokploy-server.com:5432/userdata

Health Checks:
  ✓ All 3 replicas healthy
  ✓ Replication lag: <100ms
  ✓ Resource usage: 45% memory, 30% CPU

Next Steps:
  • Migrate data: pg_dump old_db | psql new_db
  • Update applications: Use new DATABASE_URL
  • Monitor: /check-database db_ha_999
```

**Rationale**: Demonstrates advanced database provisioning with high availability configuration, performance tuning, external access, and Docker Swarm orchestration features.

---

## Quality Standards

### Validation Checklist

**Before Deployment:**
- [ ] Environment variables validated (no missing required vars)
- [ ] Git provider authentication confirmed
- [ ] Build configuration matches project structure
- [ ] Database connection strings tested
- [ ] Domain DNS records verified
- [ ] SSL certificates can be provisioned
- [ ] Resource limits appropriate for workload

**After Deployment:**
- [ ] Application status = "done" (not stuck at "running")
- [ ] Health checks passing
- [ ] Domains resolving correctly
- [ ] SSL certificates active
- [ ] Monitoring metrics available
- [ ] Logs accessible and showing expected output
- [ ] Database connections working

### Performance Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Deployment Time | <5 min for simple apps | Time from deploy to "done" status |
| Build Success Rate | >95% | Successful builds / total attempts |
| Uptime | 99.9% | Application availability |
| Response Time | <500ms p95 | API response latency |
| Resource Efficiency | <80% utilization | CPU/memory usage under load |

### Security Standards

**Mandatory:**
- [ ] HTTPS enabled for all public domains
- [ ] Let's Encrypt certificates auto-renewed
- [ ] Database passwords generated (≥20 chars, random)
- [ ] Secrets stored as environment variables (never in code)
- [ ] External database ports restricted by firewall
- [ ] Git provider tokens scoped to minimum permissions

**Recommended:**
- [ ] Network isolation between environments
- [ ] Rate limiting on public endpoints
- [ ] Database backup schedule configured
- [ ] Audit logging enabled
- [ ] Resource quotas enforced

## Common Pitfalls

### ❌ Pitfall 1: Missing Environment Variables

**Problem**: Application deploys but crashes immediately due to missing `DATABASE_URL`

**Symptom**:
```
Application Status: error
Container exits with code 1
Logs: "Error: DATABASE_URL is not defined"
```

**Solution**:
```javascript
// Always validate required variables before deployment
const requiredVars = ["DATABASE_URL", "API_KEY", "SECRET_KEY"];
const currentEnv = app.env.split("\n");

for (const varName of requiredVars) {
  if (!currentEnv.some(line => line.startsWith(varName))) {
    console.error(`❌ Missing required variable: ${varName}`);
    // Add missing variable
  }
}
```

---

### ❌ Pitfall 2: Wrong Build Type Selection

**Problem**: Chose `dockerfile` but no Dockerfile exists in repository

**Symptom**:
```
Build fails with: "Dockerfile not found in context"
```

**Solution**:
Use build type detection logic:
```javascript
// Check repository structure first
const repoFiles = await fetchRepoFileList(repo);

let buildType;
if (repoFiles.includes("Dockerfile")) {
  buildType = "dockerfile";
} else if (repoFiles.includes("package.json")) {
  buildType = "nixpacks"; // Auto-detect Node.js
} else if (repoFiles.includes("requirements.txt")) {
  buildType = "nixpacks"; // Auto-detect Python
} else {
  buildType = "heroku_buildpacks"; // Fallback
}
```

---

### ❌ Pitfall 3: Port Mismatch

**Problem**: Application listens on port 8080 but domain configured for port 3000

**Symptom**:
```
Domain configured ✓
SSL certificate issued ✓
Application status: running ✓
But: 502 Bad Gateway error
```

**Solution**:
```javascript
// Always match application's PORT env var with domain configuration
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-saveEnvironment",
  arguments: {
    applicationId: app.applicationId,
    env: `PORT=3000` // Match this...
  }
});

await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "domain-create",
  arguments: {
    applicationId: app.applicationId,
    port: 3000 // ...with this
  }
});
```

---

### ❌ Pitfall 4: Database Not Ready Before App Deployment

**Problem**: Deploy application before database is fully running

**Symptom**:
```
Application fails health checks
Logs: "Connection refused to database"
Database status: running (but still initializing)
```

**Solution**:
```javascript
// Wait for database to be fully ready
const db = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "postgres-deploy",
  arguments: { postgresId: db.postgresId }
});

// Poll until status = "done"
let dbStatus;
do {
  await sleep(5000); // Wait 5 seconds
  const dbCheck = await use_mcp_tool({
    server_name: "dokploy-mcp",
    tool_name: "postgres-one",
    arguments: { postgresId: db.postgresId }
  });
  dbStatus = dbCheck.applicationStatus;
} while (dbStatus !== "done");

console.log("✅ Database ready, deploying application...");

// Now safe to deploy app
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "application-deploy",
  arguments: { applicationId: app.applicationId }
});
```

---

### ❌ Pitfall 5: Forgotten Domain Validation

**Problem**: Create domain but forget to configure DNS records

**Symptom**:
```
Domain created ✓
SSL certificate: PENDING (never completes)
```

**Solution**:
```javascript
// Always validate domain before SSL provisioning
const validation = await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "domain-validateDomain",
  arguments: {
    domain: "api.example.com",
    serverIp: "203.0.113.42"
  }
});

if (!validation.valid) {
  console.warn(`
⚠️ DNS Configuration Required:

Add this A record to your DNS provider:
  Type: A
  Name: api
  Value: 203.0.113.42
  TTL: 300

Then wait 5-10 minutes for propagation.
  `);

  // Don't proceed with SSL until DNS is ready
  return;
}

// DNS valid, proceed with domain creation
await use_mcp_tool({
  server_name: "dokploy-mcp",
  tool_name: "domain-create",
  arguments: { /* ... */ }
});
```

---

## Integration Notes

### Related Agents

**Builder Agent** (`agents/builder.md`):
- **Collaboration**: Builder prepares application code, Dokploy skill handles deployment
- **Handoff**: Builder commits code → triggers webhook → Dokploy auto-deploys
- **Use Together**: Complex features requiring code changes + deployment

**DevOps Agent** (`agents/devops.md`):
- **Collaboration**: DevOps manages infrastructure, Dokploy manages applications
- **Handoff**: DevOps provisions servers → Dokploy deploys services
- **Use Together**: Multi-server deployments, infrastructure scaling

**Validator Agent** (`agents/validator.md`):
- **Collaboration**: Validator runs tests → Dokploy deploys on success
- **Handoff**: CI/CD pipeline coordination
- **Use Together**: Quality-gated deployments

### Related Commands

**`/deploy`**: Quick deployment command (wraps this skill)
**`/rollback`**: Undoes deployment (uses redeploy with previous version)
**`/check-deployment`**: Status monitoring (uses application-one + monitoring tools)
**`/scale-app`**: Replica/resource management (uses application-update)

### MCP Server Dependencies

**Primary**: `dokploy-mcp` (@ahdev/dokploy-mcp)
- Required for all deployment operations
- Provides 43 tools across projects, applications, databases, domains

**Optional**:
- `github` - Enhanced GitHub integration (issue tracking, PR status)
- `gitlab` - Enhanced GitLab integration
- `monitoring` - Extended metrics and alerting

### Orchestration Patterns

**Sequential Deployment**:
```
1. Create Project → 2. Create App → 3. Deploy → 4. Configure Domain
```

**Parallel Database + App**:
```
┌─ Create DB → Deploy DB ─┐
│                          ├→ Configure App Env → Deploy App
└─ Create App ────────────┘
```

**Multi-Service Deployment**:
```
Orchestrator
  ├─ Worker 1: API deployment
  ├─ Worker 2: Web deployment
  ├─ Worker 3: Database provisioning
  └─ Coordinator: Domain configuration after all complete
```

## Troubleshooting

### Issue: "Dokploy MCP server not found"

**Symptom**:
```
Error: MCP server "dokploy-mcp" is not available
```

**Resolution**:
1. Verify MCP server installation:
   ```bash
   npx -y @ahdev/dokploy-mcp --version
   ```

2. Check MCP configuration in Claude settings:
   ```json
   {
     "mcpServers": {
       "dokploy-mcp": {
         "command": "npx",
         "args": ["-y", "@ahdev/dokploy-mcp"],
         "env": {
           "DOKPLOY_URL": "https://dokploy.example.com/api",
           "DOKPLOY_API_KEY": "your-api-key"
         }
       }
     }
   }
   ```

3. Restart Claude Code to reload MCP servers

---

### Issue: "API authentication failed"

**Symptom**:
```
Error 401: Unauthorized
Invalid or missing API key
```

**Resolution**:
1. Verify `DOKPLOY_API_KEY` is set correctly
2. Check API key hasn't expired (Dokploy UI → Settings → API Keys)
3. Regenerate API key if necessary:
   ```bash
   export DOKPLOY_API_KEY="new-key-here"
   ```

---

### Issue: "Deployment stuck at 'running' status"

**Symptom**:
```
Application Status: running (for >10 minutes)
Expected: Should transition to "done"
```

**Resolution**:
1. Cancel stuck deployment:
   ```javascript
   await use_mcp_tool({
     server_name: "dokploy-mcp",
     tool_name: "application-cancelDeployment",
     arguments: { applicationId: "app_123" }
   });
   ```

2. Clean queues:
   ```javascript
   await use_mcp_tool({
     server_name: "dokploy-mcp",
     tool_name: "application-cleanQueues",
     arguments: { applicationId: "app_123" }
   });
   ```

3. Check build logs in Dokploy UI
4. Fix configuration issues (missing env vars, wrong port, etc.)
5. Redeploy

---

### Issue: "Domain SSL certificate provisioning fails"

**Symptom**:
```
Domain: Created ✓
HTTPS: Enabled ✓
Certificate: PENDING (never completes)
```

**Resolution**:
1. Validate DNS configuration:
   ```javascript
   const validation = await use_mcp_tool({
     server_name: "dokploy-mcp",
     tool_name: "domain-validateDomain",
     arguments: {
       domain: "api.example.com",
       serverIp: "203.0.113.42"
     }
   });
   ```

2. If DNS invalid:
   - Add A record pointing to Dokploy server IP
   - Wait 5-10 minutes for propagation
   - Retry validation

3. If DNS valid but still failing:
   - Check Let's Encrypt rate limits (5/week per domain)
   - Verify port 80/443 accessible on server
   - Check Traefik logs in Dokploy

---

### Issue: "Database connection refused from application"

**Symptom**:
```
Application logs: "Error: connect ECONNREFUSED db:5432"
Database status: running ✓
```

**Resolution**:
1. Verify database is fully initialized (not just "running"):
   ```javascript
   const db = await use_mcp_tool({
     server_name: "dokploy-mcp",
     tool_name: "postgres-one",
     arguments: { postgresId: "db_123" }
   });
   // Check if status === "done"
   ```

2. Check DATABASE_URL format:
   ```
   Correct: postgresql://user:pass@db-appname:5432/dbname
   Wrong:   postgresql://user:pass@localhost:5432/dbname
   ```

3. Ensure app and database in same project/environment (network isolation)

4. Test connection manually:
   ```bash
   docker exec -it app-container psql $DATABASE_URL
   ```

---

## Version History

- **1.0.0** (2025-12-27): Initial comprehensive skill release
  - 43 Dokploy MCP tools integrated
  - Complete workflow coverage (projects, apps, databases, domains)
  - 5 detailed examples covering common scenarios
  - Error handling and troubleshooting guidance
  - Multi-Git provider support
  - Build system flexibility (Dockerfile, Nixpacks, etc.)

---

## Metadata

```json
{
  "name": "dokploy-mcp",
  "version": "1.0.0",
  "description": "AI-driven deployment management using Dokploy MCP server",
  "author": "Claude Command and Control",
  "created": "2025-12-27",
  "last_updated": "2025-12-27",
  "status": "active",
  "complexity": "complex",
  "category": "devops-automation",
  "tags": ["deployment", "dokploy", "mcp", "docker", "database", "devops", "automation"],
  "token_budget": "15000",
  "usage_frequency_target": "daily",
  "integrations": {
    "agents": ["builder", "devops", "validator"],
    "commands": ["/deploy", "/rollback", "/scale-app"],
    "mcp_servers": ["dokploy-mcp"]
  },
  "tools_count": 43,
  "categories": {
    "projects": 6,
    "applications": 24,
    "databases": 13
  }
}
```

---

**Repository Note**: This project has been moved to the official Dokploy organization at https://github.com/Dokploy/mcp. For the latest updates, issues, and contributions, please visit the official repository.
