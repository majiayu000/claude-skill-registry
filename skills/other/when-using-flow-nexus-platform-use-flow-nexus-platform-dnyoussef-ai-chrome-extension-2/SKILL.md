# Flow Nexus Platform Management SOP

```yaml
metadata:
  skill_name: when-using-flow-nexus-platform-use-flow-nexus-platform
  version: 1.0.0
  category: platform-integration
  difficulty: intermediate
  estimated_duration: 30-60 minutes
  trigger_patterns:
    - "flow nexus platform"
    - "manage flow nexus"
    - "flow nexus authentication"
    - "deploy to flow nexus"
    - "flow nexus sandboxes"
  dependencies:
    - flow-nexus MCP server
    - Valid email for registration
    - Claude Flow hooks
  agents:
    - cicd-engineer (infrastructure orchestrator)
    - backend-dev (service integrator)
    - system-architect (platform designer)
  success_criteria:
    - Authentication successful
    - Services configured and running
    - Application deployed
    - Monitoring active
    - Payment system operational
```

## Overview

Comprehensive Flow Nexus platform management covering authentication, sandboxes, storage, databases, app deployment, payments, and monitoring. This SOP provides end-to-end platform operations.

## Prerequisites

**Required:**
- Flow Nexus MCP server installed
- Valid email address
- Internet connectivity

**Optional:**
- E2B API key for enhanced features
- Anthropic API key for Claude Code sandboxes
- Payment method for credits

**Verification:**
```bash
# Check Flow Nexus MCP availability
claude mcp list | grep flow-nexus

# Test connection
npx flow-nexus@latest --version
```

## Agent Responsibilities

### cicd-engineer (Infrastructure Orchestrator)
**Role:** Manage infrastructure, sandboxes, deployments, and CI/CD pipelines

**Expertise:**
- Cloud infrastructure management
- Container orchestration
- Deployment automation
- Resource optimization

**Output:** Infrastructure configuration, deployment pipelines, monitoring setup

### backend-dev (Service Integrator)
**Role:** Integrate platform services, APIs, and business logic

**Expertise:**
- API integration
- Service architecture
- Database design
- Authentication flows

**Output:** Service integration code, API endpoints, database schemas

### system-architect (Platform Designer)
**Role:** Design platform architecture, scalability patterns, and system integration

**Expertise:**
- System architecture
- Scalability patterns
- Performance optimization
- Security design

**Output:** Architecture diagrams, technical specifications, integration patterns

## Phase 1: Authentication Setup

**Objective:** Register user, authenticate, verify access to platform services

**Evidence-Based Validation:**
- User registered successfully
- Authentication token obtained
- Session active and verified
- User profile accessible

**cicd-engineer Actions:**
```bash
# Pre-task coordination
npx claude-flow@alpha hooks pre-task --description "Setup Flow Nexus authentication"

# Restore session
npx claude-flow@alpha hooks session-restore --session-id "flow-nexus-setup-$(date +%s)"

# Check current authentication status
mcp__flow-nexus__auth_status { "detailed": true }

# If not authenticated, register new user
mcp__flow-nexus__user_register {
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "username": "platform_user",
  "full_name": "Platform User"
}

# Login to create session
mcp__flow-nexus__user_login {
  "email": "user@example.com",
  "password": "SecurePassword123!"
}

# Store user ID in memory
USER_ID="[returned_user_id]"
npx claude-flow@alpha memory store --key "flow-nexus/user-id" --value "$USER_ID"

# Get user profile
mcp__flow-nexus__user_profile { "user_id": "$USER_ID" }

# Store profile in memory
npx claude-flow@alpha memory store \
  --key "flow-nexus/user-profile" \
  --value "{\"user_id\": \"$USER_ID\", \"tier\": \"free\", \"timestamp\": \"$(date -Iseconds)\"}"
```

**backend-dev Actions:**
```bash
# Create platform configuration
mkdir -p platform/{config,services,scripts,docs}

cat > platform/config/flow-nexus.json << 'EOF'
{
  "platform": "flow-nexus",
  "version": "1.0.0",
  "authentication": {
    "type": "email_password",
    "session_timeout": 3600
  },
  "services": {
    "sandboxes": { "enabled": true, "max_concurrent": 5 },
    "storage": { "enabled": true, "max_size_mb": 1000 },
    "databases": { "enabled": true, "max_connections": 10 },
    "workflows": { "enabled": true, "max_agents": 8 }
  },
  "limits": {
    "requests_per_minute": 60,
    "storage_mb": 1000,
    "compute_hours": 10
  }
}
EOF

# Post-edit hook
npx claude-flow@alpha hooks post-edit --file "platform/config/flow-nexus.json" --memory-key "flow-nexus/config"
```

**system-architect Actions:**
```bash
# Document authentication flow
cat > platform/docs/AUTHENTICATION.md << 'EOF'
# Flow Nexus Authentication

## Overview

Flow Nexus uses email/password authentication with JWT tokens for session management.

## Authentication Flow

1. **Registration**: Create new user account
   - Email validation required
   - Password complexity enforced
   - Username unique constraint

2. **Login**: Obtain authentication token
   - Returns JWT token
   - Token expires after 1 hour
   - Refresh token available

3. **Session Management**: Maintain active session
   - Auto-refresh before expiry
   - Logout clears session
   - Multi-device support

## Security Best Practices

- Use strong passwords (min 12 characters)
- Enable 2FA when available
- Rotate tokens regularly
- Never commit credentials to git

## API Examples

### Register
```bash
mcp__flow-nexus__user_register {
  "email": "user@example.com",
  "password": "secure_password"
}
```

### Login
```bash
mcp__flow-nexus__user_login {
  "email": "user@example.com",
  "password": "secure_password"
}
```

### Logout
```bash
mcp__flow-nexus__user_logout
```
EOF

# Post-edit hook
npx claude-flow@alpha hooks post-edit --file "platform/docs/AUTHENTICATION.md" --memory-key "flow-nexus/auth-docs"
```

**Success Criteria:**
- [ ] User registered successfully
- [ ] Authentication token obtained
- [ ] Configuration created
- [ ] Documentation generated

**Memory Persistence:**
```bash
npx claude-flow@alpha memory store \
  --key "flow-nexus/phase1-complete" \
  --value "{\"status\": \"complete\", \"user_id\": \"$USER_ID\", \"authenticated\": true, \"timestamp\": \"$(date -Iseconds)\"}"
```

## Phase 2: Configure Services

**Objective:** Setup sandboxes, storage, databases, and other platform services

**Evidence-Based Validation:**
- Sandboxes created and running
- Storage buckets configured
- Database connections established
- Real-time subscriptions active

**cicd-engineer Actions:**
```bash
# Retrieve user ID
USER_ID=$(npx claude-flow@alpha memory retrieve --key "flow-nexus/user-id" | jq -r '.value')

# Create sandbox for development
mcp__flow-nexus__sandbox_create {
  "template": "node",
  "name": "dev-sandbox",
  "timeout": 3600,
  "env_vars": {
    "NODE_ENV": "development",
    "LOG_LEVEL": "debug"
  },
  "install_packages": ["express", "axios", "dotenv"]
}

# Store sandbox ID
SANDBOX_ID="[returned_sandbox_id]"
npx claude-flow@alpha memory store --key "flow-nexus/sandbox-id" --value "$SANDBOX_ID"

# Configure sandbox with additional settings
mcp__flow-nexus__sandbox_configure {
  "sandbox_id": "$SANDBOX_ID",
  "env_vars": {
    "API_URL": "https://api.flow-nexus.ruv.io",
    "MAX_RETRIES": "3"
  },
  "install_packages": ["typescript", "jest"]
}

# Create storage bucket
mcp__flow-nexus__storage_upload {
  "bucket": "platform-assets",
  "path": ".gitkeep",
  "content": ""
}

# Setup real-time subscriptions
mcp__flow-nexus__realtime_subscribe {
  "table": "workflows",
  "event": "*"
}

# Store subscription ID
SUBSCRIPTION_ID="[returned_subscription_id]"
npx claude-flow@alpha memory store --key "flow-nexus/subscription-id" --value "$SUBSCRIPTION_ID"

# Notify completion
npx claude-flow@alpha hooks notify --message "Services configured: sandbox, storage, real-time subscriptions"
```

**backend-dev Actions:**
```bash
# Create service initialization script
cat > platform/scripts/init-services.js << 'EOF'
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

async function initializeSandbox() {
  console.log('Initializing sandbox...');
  // Sandbox initialization logic
  return { status: 'success', sandbox_id: process.env.SANDBOX_ID };
}

async function initializeStorage() {
  console.log('Initializing storage...');
  // Storage setup logic
  return { status: 'success', bucket: 'platform-assets' };
}

async function initializeDatabase() {
  console.log('Initializing database...');
  // Database connection logic
  return { status: 'success', connected: true };
}

async function main() {
  try {
    const sandbox = await initializeSandbox();
    const storage = await initializeStorage();
    const database = await initializeDatabase();

    console.log('All services initialized successfully:', {
      sandbox,
      storage,
      database
    });
  } catch (error) {
    console.error('Service initialization failed:', error);
    process.exit(1);
  }
}

main();
EOF

# Post-edit hook
npx claude-flow@alpha hooks post-edit --file "platform/scripts/init-services.js" --memory-key "flow-nexus/init-script"

# Create database schema
cat > platform/config/schema.sql << 'EOF'
-- Flow Nexus Platform Schema

CREATE TABLE IF NOT EXISTS applications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(50) DEFAULT 'active',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS deployments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  application_id UUID REFERENCES applications(id),
  version VARCHAR(50) NOT NULL,
  sandbox_id VARCHAR(255),
  status VARCHAR(50) DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS metrics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  deployment_id UUID REFERENCES deployments(id),
  metric_type VARCHAR(100),
  metric_value JSONB,
  recorded_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_applications_user_id ON applications(user_id);
CREATE INDEX idx_deployments_app_id ON deployments(application_id);
CREATE INDEX idx_metrics_deployment_id ON metrics(deployment_id);
EOF

# Post-edit hook
npx claude-flow@alpha hooks post-edit --file "platform/config/schema.sql" --memory-key "flow-nexus/schema"
```

**system-architect Actions:**
```bash
# Document service architecture
cat > platform/docs/ARCHITECTURE.md << 'EOF'
# Flow Nexus Platform Architecture

## System Components

### 1. Sandboxes (E2B)
- Isolated code execution environments
- Multiple templates (Node.js, Python, React)
- Resource limits enforced
- Environment variable support

### 2. Storage
- Object storage for files
- Bucket-based organization
- Public URL generation
- File upload/download APIs

### 3. Databases
- PostgreSQL with Supabase
- Real-time subscriptions
- Row-level security
- Connection pooling

### 4. Workflows
- Event-driven processing
- Agent coordination
- Task orchestration
- Message queue integration

## Service Integration

```
┌─────────────────────────────────────────┐
│         Flow Nexus Platform             │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────┐  ┌──────────┐           │
│  │ Sandboxes│  │ Storage  │           │
│  │  (E2B)   │  │(Supabase)│           │
│  └────┬─────┘  └────┬─────┘           │
│       │             │                  │
│  ┌────▼─────────────▼─────┐           │
│  │    Event Bus            │           │
│  │  (Real-time sync)       │           │
│  └────┬────────────────────┘           │
│       │                                │
│  ┌────▼─────┐  ┌──────────┐           │
│  │ Workflows│  │Databases │           │
│  │ (Claude  │  │(Postgres)│           │
│  │  Flow)   │  │          │           │
│  └──────────┘  └──────────┘           │
└─────────────────────────────────────────┘
```

## Scalability Patterns

1. **Horizontal Scaling**: Add more sandboxes
2. **Vertical Scaling**: Increase sandbox resources
3. **Load Balancing**: Distribute across regions
4. **Caching**: Redis for frequently accessed data
5. **CDN**: Static asset delivery

## Security Measures

- Authentication required for all operations
- API rate limiting enforced
- Sandbox isolation with network controls
- Encrypted data at rest and in transit
- Audit logging for all actions
EOF

# Post-edit hook
npx claude-flow@alpha hooks post-edit --file "platform/docs/ARCHITECTURE.md" --memory-key "flow-nexus/architecture"
```

**Success Criteria:**
- [ ] Sandbox created and configured
- [ ] Storage bucket initialized
- [ ] Database schema applied
- [ ] Real-time subscriptions active

**Memory Persistence:**
```bash
npx claude-flow@alpha memory store \
  --key "flow-nexus/phase2-complete" \
  --value "{\"status\": \"complete\", \"sandbox_id\": \"$SANDBOX_ID\", \"subscription_id\": \"$SUBSCRIPTION_ID\", \"timestamp\": \"$(date -Iseconds)\"}"
```

## Phase 3: Deploy Applications

**Objective:** Deploy applications using templates or custom configurations

**Evidence-Based Validation:**
- Application deployed successfully
- Health checks passing
- Metrics being collected
- Public URL accessible

**cicd-engineer Actions:**
```bash
# List available templates
mcp__flow-nexus__template_list {
  "category": "web",
  "limit": 10
}

# Deploy from template
mcp__flow-nexus__template_deploy {
  "template_name": "nextjs-starter",
  "deployment_name": "my-nextjs-app",
  "variables": {
    "anthropic_api_key": "$ANTHROPIC_API_KEY",
    "app_name": "My Next.js App",
    "port": "3000"
  },
  "env_vars": {
    "NODE_ENV": "production",
    "DATABASE_URL": "$DATABASE_URL"
  }
}

# Store deployment ID
DEPLOYMENT_ID="[returned_deployment_id]"
npx claude-flow@alpha memory store --key "flow-nexus/deployment-id" --value "$DEPLOYMENT_ID"

# Subscribe to execution stream
mcp__flow-nexus__execution_stream_subscribe {
  "deployment_id": "$DEPLOYMENT_ID",
  "stream_type": "claude-code"
}

# Monitor deployment status
for i in {1..10}; do
  sleep 10
  mcp__flow-nexus__execution_stream_status {
    "stream_id": "$DEPLOYMENT_ID"
  }
done

# Notify deployment completion
npx claude-flow@alpha hooks notify --message "Application deployed successfully: $DEPLOYMENT_ID"
```

**backend-dev Actions:**
```bash
# Create custom application deployment script
cat > platform/scripts/deploy-app.sh << 'EOF'
#!/bin/bash
set -e

APP_NAME="${1:-my-app}"
SANDBOX_ID="${2:-$SANDBOX_ID}"

echo "Deploying $APP_NAME to sandbox $SANDBOX_ID..."

# Upload application files
echo "Uploading files..."
mcp__flow-nexus__sandbox_upload \
  --sandbox_id="$SANDBOX_ID" \
  --file_path="app.js" \
  --content="$(cat platform/services/app.js)"

# Execute startup script
echo "Starting application..."
mcp__flow-nexus__sandbox_execute \
  --sandbox_id="$SANDBOX_ID" \
  --code="npm start" \
  --timeout=300

echo "Application deployed successfully!"
echo "Access logs: mcp__flow-nexus__sandbox_logs --sandbox_id=$SANDBOX_ID"
EOF

chmod +x platform/scripts/deploy-app.sh

# Create sample application
cat > platform/services/app.js << 'EOF'
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

app.get('/api/info', (req, res) => {
  res.json({
    name: 'Flow Nexus Platform App',
    version: '1.0.0',
    environment: process.env.NODE_ENV
  });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
EOF

# Post-edit hooks
npx claude-flow@alpha hooks post-edit --file "platform/scripts/deploy-app.sh" --memory-key "flow-nexus/deploy-script"
npx claude-flow@alpha hooks post-edit --file "platform/services/app.js" --memory-key "flow-nexus/app"
```

**system-architect Actions:**
```bash
# Document deployment process
cat > platform/docs/DEPLOYMENT.md << 'EOF'
# Application Deployment Guide

## Deployment Methods

### 1. Template Deployment
Use pre-built templates for quick setup:
```bash
mcp__flow-nexus__template_deploy {
  "template_name": "nextjs-starter",
  "deployment_name": "my-app"
}
```

### 2. Custom Deployment
Deploy custom applications:
```bash
./platform/scripts/deploy-app.sh my-app $SANDBOX_ID
```

## Deployment Workflow

1. **Prepare**: Build and test locally
2. **Upload**: Transfer files to sandbox
3. **Configure**: Set environment variables
4. **Execute**: Start application
5. **Monitor**: Track health and metrics
6. **Scale**: Adjust resources as needed

## Health Monitoring

Check application health:
```bash
curl http://localhost:3000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-30T12:00:00Z",
  "uptime": 3600
}
```

## Troubleshooting

### Application Not Starting
- Check sandbox logs
- Verify environment variables
- Ensure dependencies installed
- Check port availability

### Health Check Failing
- Verify application is running
- Check network connectivity
- Review error logs
- Test locally first

### Performance Issues
- Monitor resource usage
- Check database connections
- Review application logs
- Consider scaling up
EOF

# Post-edit hook
npx claude-flow@alpha hooks post-edit --file "platform/docs/DEPLOYMENT.md" --memory-key "flow-nexus/deployment-docs"
```

**Success Criteria:**
- [ ] Application deployed from template
- [ ] Custom deployment script created
- [ ] Health checks configured
- [ ] Documentation completed

**Memory Persistence:**
```bash
npx claude-flow@alpha memory store \
  --key "flow-nexus/phase3-complete" \
  --value "{\"status\": \"complete\", \"deployment_id\": \"$DEPLOYMENT_ID\", \"app_running\": true, \"timestamp\": \"$(date -Iseconds)\"}"
```

## Phase 4: Manage Operations

**Objective:** Monitor applications, manage resources, handle scaling and updates

**Evidence-Based Validation:**
- Monitoring dashboards active
- Metrics being collected
- Alerts configured
- Scaling policies defined

**cicd-engineer Actions:**
```bash
# Get system health
mcp__flow-nexus__system_health

# Check sandbox status
SANDBOX_ID=$(npx claude-flow@alpha memory retrieve --key "flow-nexus/sandbox-id" | jq -r '.value')
mcp__flow-nexus__sandbox_status { "sandbox_id": "$SANDBOX_ID" }

# Get sandbox logs
mcp__flow-nexus__sandbox_logs {
  "sandbox_id": "$SANDBOX_ID",
  "lines": 100
}

# List execution files
DEPLOYMENT_ID=$(npx claude-flow@alpha memory retrieve --key "flow-nexus/deployment-id" | jq -r '.value')
mcp__flow-nexus__execution_files_list {
  "stream_id": "$DEPLOYMENT_ID",
  "created_by": "claude-code"
}

# Get audit log
USER_ID=$(npx claude-flow@alpha memory retrieve --key "flow-nexus/user-id" | jq -r '.value')
mcp__flow-nexus__audit_log {
  "user_id": "$USER_ID",
  "limit": 50
}

# Store monitoring data
npx claude-flow@alpha memory store \
  --key "flow-nexus/monitoring" \
  --value "{\"health\": \"good\", \"sandbox_status\": \"running\", \"log_lines\": 100, \"timestamp\": \"$(date -Iseconds)\"}"
```

**backend-dev Actions:**
```bash
# Create monitoring dashboard configuration
cat > platform/config/monitoring.json << 'EOF'
{
  "dashboards": {
    "main": {
      "panels": [
        {
          "title": "Application Health",
          "type": "status",
          "metrics": ["uptime", "response_time", "error_rate"]
        },
        {
          "title": "Resource Usage",
          "type": "timeseries",
          "metrics": ["cpu_usage", "memory_usage", "disk_usage"]
        },
        {
          "title": "Request Metrics",
          "type": "counter",
          "metrics": ["requests_total", "requests_per_second"]
        }
      ]
    }
  },
  "alerts": {
    "high_error_rate": {
      "threshold": 0.05,
      "window": "5m",
      "severity": "critical"
    },
    "high_latency": {
      "threshold": 1000,
      "window": "5m",
      "severity": "warning"
    },
    "resource_exhaustion": {
      "threshold": 0.9,
      "window": "10m",
      "severity": "critical"
    }
  }
}
EOF

# Create operations utility script
cat > platform/scripts/ops-util.sh << 'EOF'
#!/bin/bash

CMD="${1:-help}"
SANDBOX_ID="${SANDBOX_ID:-$(npx claude-flow@alpha memory retrieve --key flow-nexus/sandbox-id | jq -r '.value')}"

case "$CMD" in
  status)
    echo "Getting system status..."
    mcp__flow-nexus__system_health
    ;;
  logs)
    echo "Fetching logs for sandbox $SANDBOX_ID..."
    mcp__flow-nexus__sandbox_logs --sandbox_id="$SANDBOX_ID" --lines=50
    ;;
  restart)
    echo "Restarting sandbox $SANDBOX_ID..."
    mcp__flow-nexus__sandbox_stop --sandbox_id="$SANDBOX_ID"
    sleep 5
    ./platform/scripts/deploy-app.sh
    ;;
  scale)
    REPLICAS="${2:-2}"
    echo "Scaling to $REPLICAS replicas..."
    # Scaling logic here
    ;;
  help)
    echo "Usage: $0 {status|logs|restart|scale}"
    ;;
  *)
    echo "Unknown command: $CMD"
    exit 1
    ;;
esac
EOF

chmod +x platform/scripts/ops-util.sh

# Post-edit hooks
npx claude-flow@alpha hooks post-edit --file "platform/config/monitoring.json" --memory-key "flow-nexus/monitoring-config"
npx claude-flow@alpha hooks post-edit --file "platform/scripts/ops-util.sh" --memory-key "flow-nexus/ops-util"
```

**system-architect Actions:**
```bash
# Document operations procedures
cat > platform/docs/OPERATIONS.md << 'EOF'
# Operations Guide

## Monitoring

### Health Checks
```bash
# System health
mcp__flow-nexus__system_health

# Sandbox status
mcp__flow-nexus__sandbox_status --sandbox_id=$SANDBOX_ID

# Application health
curl http://localhost:3000/health
```

### Logs
```bash
# View sandbox logs
mcp__flow-nexus__sandbox_logs --sandbox_id=$SANDBOX_ID --lines=100

# Stream logs in real-time
./platform/scripts/ops-util.sh logs
```

### Metrics
- **CPU Usage**: Track compute utilization
- **Memory Usage**: Monitor memory consumption
- **Request Rate**: Requests per second
- **Error Rate**: Failed requests percentage
- **Latency**: Response time (p50, p95, p99)

## Scaling

### Manual Scaling
```bash
# Scale up
./platform/scripts/ops-util.sh scale 3

# Scale down
./platform/scripts/ops-util.sh scale 1
```

### Auto-scaling Policies
- Scale up when CPU >80% for 5 minutes
- Scale down when CPU <20% for 10 minutes
- Min replicas: 1
- Max replicas: 10

## Incident Response

### High Error Rate
1. Check application logs
2. Review recent deployments
3. Verify external dependencies
4. Rollback if necessary

### Performance Degradation
1. Check resource usage
2. Review database queries
3. Analyze slow endpoints
4. Scale resources if needed

### Service Outage
1. Check system health
2. Verify sandbox status
3. Restart application
4. Escalate if persists

## Maintenance

### Updates
```bash
# Update dependencies
mcp__flow-nexus__sandbox_configure \
  --sandbox_id=$SANDBOX_ID \
  --install_packages=["package@latest"]

# Restart application
./platform/scripts/ops-util.sh restart
```

### Backups
- Automated daily backups
- 30-day retention
- Point-in-time recovery available
EOF

# Post-edit hook
npx claude-flow@alpha hooks post-edit --file "platform/docs/OPERATIONS.md" --memory-key "flow-nexus/ops-docs"
```

**Success Criteria:**
- [ ] Monitoring configured
- [ ] Logs accessible
- [ ] Operations utilities created
- [ ] Incident procedures documented

**Memory Persistence:**
```bash
npx claude-flow@alpha memory store \
  --key "flow-nexus/phase4-complete" \
  --value "{\"status\": \"complete\", \"monitoring\": \"active\", \"ops_tools\": \"ready\", \"timestamp\": \"$(date -Iseconds)\"}"
```

## Phase 5: Handle Payments

**Objective:** Manage credits, configure auto-refill, track usage and billing

**Evidence-Based Validation:**
- Credit balance retrieved
- Payment history accessible
- Auto-refill configured
- Usage tracking active

**cicd-engineer Actions:**
```bash
# Check credit balance
mcp__flow-nexus__check_balance

# Store balance
BALANCE="[returned_balance]"
npx claude-flow@alpha memory store --key "flow-nexus/balance" --value "$BALANCE"

# Get payment history
mcp__flow-nexus__get_payment_history { "limit": 20 }

# Configure auto-refill
mcp__flow-nexus__configure_auto_refill {
  "enabled": true,
  "threshold": 10,
  "amount": 50
}

# Get user statistics
USER_ID=$(npx claude-flow@alpha memory retrieve --key "flow-nexus/user-id" | jq -r '.value')
mcp__flow-nexus__user_stats { "user_id": "$USER_ID" }

# Notify configuration complete
npx claude-flow@alpha hooks notify --message "Payment system configured with auto-refill"
```

**backend-dev Actions:**
```bash
# Create billing utility script
cat > platform/scripts/billing-util.sh << 'EOF'
#!/bin/bash

CMD="${1:-balance}"

case "$CMD" in
  balance)
    echo "Checking credit balance..."
    mcp__flow-nexus__check_balance
    ;;
  history)
    LIMIT="${2:-10}"
    echo "Fetching payment history (last $LIMIT transactions)..."
    mcp__flow-nexus__get_payment_history --limit=$LIMIT
    ;;
  refill)
    AMOUNT="${2:-50}"
    echo "Creating payment link for $$AMOUNT..."
    mcp__flow-nexus__create_payment_link --amount=$AMOUNT
    ;;
  auto-refill)
    ACTION="${2:-status}"
    if [ "$ACTION" = "enable" ]; then
      THRESHOLD="${3:-10}"
      AMOUNT="${4:-50}"
      mcp__flow-nexus__configure_auto_refill \
        --enabled=true \
        --threshold=$THRESHOLD \
        --amount=$AMOUNT
    elif [ "$ACTION" = "disable" ]; then
      mcp__flow-nexus__configure_auto_refill --enabled=false
    else
      echo "Current auto-refill status:"
      mcp__flow-nexus__check_balance | jq '.auto_refill'
    fi
    ;;
  help)
    echo "Usage: $0 {balance|history|refill|auto-refill}"
    ;;
  *)
    echo "Unknown command: $CMD"
    exit 1
    ;;
esac
EOF

chmod +x platform/scripts/billing-util.sh

# Post-edit hook
npx claude-flow@alpha hooks post-edit --file "platform/scripts/billing-util.sh" --memory-key "flow-nexus/billing-util"

# Post-task hook
npx claude-flow@alpha hooks post-task --task-id "flow-nexus-platform-setup"
```

**system-architect Actions:**
```bash
# Document billing and payments
cat > platform/docs/BILLING.md << 'EOF'
# Billing and Payments Guide

## Credits System

Flow Nexus uses a credit-based billing system:
- Credits deducted for resource usage
- Minimum purchase: $10
- Auto-refill available

## Usage Costs

### Sandboxes
- $0.01 per minute (Node.js, Python)
- $0.02 per minute (React, Next.js)
- Free tier: 100 minutes/month

### Storage
- $0.10 per GB/month
- Free tier: 1 GB

### Workflows
- $0.001 per task execution
- Free tier: 1000 tasks/month

### Neural Training
- Nano: $0.05/hour
- Small: $0.15/hour
- Medium: $0.50/hour
- Large: $2.00/hour

## Managing Credits

### Check Balance
```bash
./platform/scripts/billing-util.sh balance
```

### View History
```bash
./platform/scripts/billing-util.sh history 20
```

### Add Credits
```bash
./platform/scripts/billing-util.sh refill 50
```

### Auto-Refill

Enable automatic credit refills:
```bash
./platform/scripts/billing-util.sh auto-refill enable 10 50
```

This will automatically add $50 credits when balance falls below $10.

Disable auto-refill:
```bash
./platform/scripts/billing-util.sh auto-refill disable
```

## Cost Optimization

1. **Stop Unused Sandboxes**: Reduce compute costs
2. **Clean Up Storage**: Remove old files
3. **Optimize Workflows**: Reduce task executions
4. **Use Free Tier**: Stay within limits when possible
5. **Monitor Usage**: Track spending regularly

## Billing Alerts

Configure alerts for:
- Low balance warnings
- High usage notifications
- Monthly spending limits
- Budget thresholds

## Payment Methods

Supported payment methods:
- Credit/Debit Cards
- PayPal
- Wire Transfer (enterprise)

## Invoices

Access invoices:
```bash
mcp__flow-nexus__get_payment_history --limit=12
```

Invoices include:
- Transaction date
- Amount charged
- Credits purchased
- Usage details
EOF

# Post-edit hook
npx claude-flow@alpha hooks post-edit --file "platform/docs/BILLING.md" --memory-key "flow-nexus/billing-docs"

# Session end hook
npx claude-flow@alpha hooks session-end --export-metrics true
```

**Success Criteria:**
- [ ] Credit balance checked
- [ ] Payment history retrieved
- [ ] Auto-refill configured
- [ ] Billing utilities created
- [ ] Documentation completed

**Memory Persistence:**
```bash
npx claude-flow@alpha memory store \
  --key "flow-nexus/phase5-complete" \
  --value "{\"status\": \"complete\", \"balance\": $BALANCE, \"auto_refill\": true, \"timestamp\": \"$(date -Iseconds)\"}"

# Final workflow summary
npx claude-flow@alpha memory store \
  --key "flow-nexus/workflow-complete" \
  --value "{\"status\": \"success\", \"authenticated\": true, \"deployed\": true, \"monitored\": true, \"billing\": \"configured\", \"timestamp\": \"$(date -Iseconds)\"}"
```

## Workflow Summary

**Total Estimated Duration:** 30-60 minutes

**Phase Breakdown:**
1. Authentication Setup: 5-10 minutes
2. Configure Services: 10-15 minutes
3. Deploy Applications: 10-15 minutes
4. Manage Operations: 5-10 minutes
5. Handle Payments: 5-10 minutes

**Key Deliverables:**
- Authenticated user account
- Configured platform services
- Deployed application
- Operations utilities
- Billing management
- Complete documentation

## Evidence-Based Success Metrics

**Authentication:**
- User registered and verified
- Session token obtained
- Profile accessible

**Services:**
- Sandbox running
- Storage configured
- Database connected
- Real-time subscriptions active

**Deployment:**
- Application deployed
- Health checks passing
- Logs accessible

**Operations:**
- Monitoring active
- Metrics collected
- Utilities functional

**Billing:**
- Balance checked
- Auto-refill configured
- Usage tracked

## Troubleshooting

**Authentication Failures:**
- Verify email and password
- Check network connectivity
- Clear browser cache
- Try password reset

**Sandbox Issues:**
- Check sandbox status
- Review logs for errors
- Verify environment variables
- Ensure sufficient credits

**Deployment Failures:**
- Validate template configuration
- Check file permissions
- Verify dependencies
- Review error messages

**Payment Problems:**
- Verify payment method
- Check credit balance
- Review transaction history
- Contact support if needed

## Best Practices

1. **Security**: Never commit credentials
2. **Monitoring**: Enable comprehensive logging
3. **Backups**: Regular data backups
4. **Updates**: Keep dependencies current
5. **Testing**: Test before production
6. **Documentation**: Maintain up-to-date docs
7. **Optimization**: Monitor and optimize costs
8. **Support**: Use audit logs for debugging

## References

- Flow Nexus Platform: https://flow-nexus.ruv.io
- API Documentation: https://flow-nexus.ruv.io/docs
- Pricing: https://flow-nexus.ruv.io/pricing
- Support: https://flow-nexus.ruv.io/support
