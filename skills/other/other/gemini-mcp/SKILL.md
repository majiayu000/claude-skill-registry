---
name: gemini-mcp
description: Manage MCP (Model Context Protocol) servers with Gemini CLI for extended tool capabilities, custom integrations, and enterprise workflows. Use when integrating external tools, databases, or APIs with Gemini.
---

# Gemini MCP Server Management

Comprehensive MCP (Model Context Protocol) server integration for extending Gemini CLI with custom tools and capabilities.

## What is MCP?

MCP (Model Context Protocol) allows Gemini to connect to external servers that provide additional tools and capabilities:
- Database connections
- API integrations  
- Custom business logic
- Enterprise systems
- Specialized tools

## Quick Start

### List MCP Servers

```bash
# View configured servers
gemini mcp list

# Check server status
gemini -i
/mcp

# Test server connection
gemini mcp test <server-name>
```

### Add MCP Server

```bash
# Interactive setup
gemini mcp add

# Manual configuration
gemini mcp add \
  --name "my-server" \
  --command "python" \
  --args "-m my_mcp_server" \
  --cwd "./mcp-servers/"
```

### Remove Server

```bash
gemini mcp remove <server-name>
```

## MCP Configuration

### Configuration File

```json
// ~/.gemini/mcp-servers.json or ./.gemini/mcp-servers.json
{
  "mcpServers": {
    "database-tools": {
      "command": "python",
      "args": ["-m", "database_mcp_server"],
      "cwd": "./mcp-tools/database",
      "env": {
        "DATABASE_URL": "postgresql://localhost/mydb",
        "DB_PASSWORD": "$DB_PASSWORD_FROM_ENV"
      },
      "timeout": 30000,
      "trust": false
    },
    "api-gateway": {
      "command": "node",
      "args": ["./api-mcp-server.js"],
      "cwd": "./mcp-tools/api",
      "env": {
        "API_KEY": "$API_KEY",
        "BASE_URL": "https://api.example.com"
      },
      "includeTools": ["getUser", "createOrder"],
      "excludeTools": ["deleteUser"]
    },
    "analytics": {
      "command": "docker",
      "args": ["run", "-p", "8080:8080", "analytics-mcp:latest"],
      "timeout": 60000,
      "trust": true
    }
  }
}
```

### Security Settings

```json
{
  "mcpServers": {
    "secure-server": {
      "command": "python",
      "args": ["secure_server.py"],
      "trust": false,  // Require confirmation for tool calls
      "includeTools": ["safe_read", "safe_write"],
      "excludeTools": ["dangerous_delete"],
      "allowedDomains": ["*.internal.com"],
      "maxConcurrent": 5,
      "rateLimit": {
        "requests": 100,
        "window": 60000  // per minute
      }
    }
  }
}
```

## Building MCP Servers

### Python MCP Server

```python
# database_mcp_server.py
import json
import sys
import psycopg2
from typing import Dict, Any

class DatabaseMCP:
    def __init__(self):
        self.conn = psycopg2.connect(
            os.environ.get('DATABASE_URL')
        )
    
    def handle_request(self, request: Dict[str, Any]):
        method = request.get('method')
        params = request.get('params', {})
        
        if method == 'query':
            return self.execute_query(params.get('sql'))
        elif method == 'insert':
            return self.insert_data(
                params.get('table'),
                params.get('data')
            )
        
    def execute_query(self, sql: str):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    
    def get_tools(self):
        return [
            {
                "name": "database_query",
                "description": "Execute SQL query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sql": {
                            "type": "string",
                            "description": "SQL query to execute"
                        }
                    },
                    "required": ["sql"]
                }
            },
            {
                "name": "database_insert",
                "description": "Insert data into table",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "table": {"type": "string"},
                        "data": {"type": "object"}
                    },
                    "required": ["table", "data"]
                }
            }
        ]

if __name__ == "__main__":
    server = DatabaseMCP()
    server.start()
```

### Node.js MCP Server

```javascript
// api-mcp-server.js
const { MCPServer } = require('@modelcontextprotocol/server');
const axios = require('axios');

class APIMCPServer extends MCPServer {
  constructor() {
    super();
    this.baseURL = process.env.BASE_URL;
    this.apiKey = process.env.API_KEY;
  }
  
  async getTools() {
    return [
      {
        name: 'api_get',
        description: 'Make GET request to API',
        parameters: {
          type: 'object',
          properties: {
            endpoint: {
              type: 'string',
              description: 'API endpoint path'
            },
            params: {
              type: 'object',
              description: 'Query parameters'
            }
          },
          required: ['endpoint']
        }
      },
      {
        name: 'api_post',
        description: 'Make POST request to API',
        parameters: {
          type: 'object',
          properties: {
            endpoint: { type: 'string' },
            body: { type: 'object' }
          },
          required: ['endpoint', 'body']
        }
      }
    ];
  }
  
  async handleToolCall(name, params) {
    const headers = {
      'Authorization': `Bearer ${this.apiKey}`,
      'Content-Type': 'application/json'
    };
    
    switch(name) {
      case 'api_get':
        const response = await axios.get(
          `${this.baseURL}${params.endpoint}`,
          { headers, params: params.params }
        );
        return response.data;
        
      case 'api_post':
        const postResponse = await axios.post(
          `${this.baseURL}${params.endpoint}`,
          params.body,
          { headers }
        );
        return postResponse.data;
        
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  }
}

const server = new APIMCPServer();
server.start();
```

### Docker MCP Server

```dockerfile
# Dockerfile for MCP server
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy server code
COPY mcp_server.py .

# MCP protocol port
EXPOSE 8080

# Start server
CMD ["python", "mcp_server.py"]
```

```bash
# Build and run
docker build -t my-mcp-server .
docker run -p 8080:8080 -e DATABASE_URL="$DATABASE_URL" my-mcp-server
```

## Usage Patterns

### Database Operations

```bash
# Configure database MCP
cat > ~/.gemini/mcp-servers.json << 'EOF'
{
  "mcpServers": {
    "postgres": {
      "command": "python",
      "args": ["-m", "postgres_mcp"],
      "env": {
        "DATABASE_URL": "postgresql://user:pass@localhost/db"
      }
    }
  }
}
EOF

# Use with YOLO for automated database operations
gemini --yolo -p "Query the users table and generate comprehensive report of active users from last week"
gemini --yolo -p "Create detailed sales analysis with charts from the orders table"
```

### API Integration

```bash
# Configure API MCP
gemini mcp add \
  --name "stripe" \
  --command "node" \
  --args "stripe-mcp.js" \
  --env "STRIPE_KEY=$STRIPE_SECRET_KEY"

# Use with YOLO for automated API operations
gemini --yolo -p "Create a new customer and subscription using Stripe with full setup"
gemini --yolo -p "Generate comprehensive transaction report with analytics for this month"
```

### Custom Business Logic

```bash
# Configure business logic MCP
gemini mcp add \
  --name "business-rules" \
  --command "java" \
  --args "-jar business-mcp.jar"

# Apply business rules with YOLO automation
gemini --yolo -p "Validate this order against all business rules and generate compliance report"
gemini --yolo -p "Calculate pricing using custom algorithm and create detailed breakdown"
```

## YOLO Mode with MCP Servers

**YOLO mode** with MCP servers enables powerful automation for trusted operations:

### Automated Data Operations

```bash
# Database automation with YOLO
gemini --yolo -p "Using the database MCP:
1. Query all user activity from last 30 days
2. Generate engagement analytics
3. Create user segmentation report
4. Export findings to CSV
5. Send summary email to stakeholders"

# Multi-database operations
gemini --yolo -p "Synchronize data between PostgreSQL and Redis:
1. Read user sessions from Redis
2. Update last_active in PostgreSQL
3. Clean expired sessions
4. Generate sync report"
```

### API Workflow Automation

```bash
# Automated API orchestration
gemini --yolo -p "Using Stripe and database MCP servers:
1. Fetch all subscription cancellations from Stripe
2. Update user status in our database
3. Send personalized retention offers
4. Log all actions for audit
5. Generate retention campaign report"

# Multi-service integration
gemini --yolo -p "Complete order processing workflow:
1. Validate order via business rules MCP
2. Process payment via Stripe MCP
3. Update inventory via database MCP
4. Send confirmation via email MCP
5. Log transaction and generate receipt"
```

### Enterprise Automation

```bash
# Automated compliance reporting
gemini --yolo -p "Generate quarterly compliance report:
1. Query all financial data via database MCP
2. Validate against regulations via compliance MCP
3. Generate charts and visualizations
4. Create executive summary
5. Export to PDF and store securely"

# Infrastructure monitoring
gemini --yolo -p "Complete infrastructure health check:
1. Query metrics from monitoring MCP
2. Check service status via K8s MCP
3. Analyze logs via logging MCP
4. Generate incident reports
5. Update status dashboard"
```

### Safe YOLO Practices for MCP

```bash
# ✅ SAFE with YOLO (read-only or low-risk)
gemini --yolo -p "Generate analytics dashboard from database MCP"
gemini --yolo -p "Sync read-only data between MCP services"
gemini --yolo -p "Create comprehensive status reports from all MCPs"

# ⚠️ USE CAUTION (write operations)
# Review first, then use YOLO if confident
gemini -p "Plan user data migration between databases"
# After review:
gemini --yolo -p "Execute the reviewed migration plan"

# 🔒 NEVER YOLO (critical operations)
# Always manual approval for:
# - Production data deletion
# - Security configuration changes
# - Financial transactions above thresholds
```

### MCP Server Management Automation

```bash
#!/bin/bash
# Automated MCP server lifecycle management

manage_mcp_servers() {
  local operation="$1"
  
  case $operation in
    health-check)
      gemini --yolo -p "Check health of all MCP servers and create status report"
      ;;
    
    restart-all)
      gemini --yolo -p "Safely restart all MCP servers in dependency order"
      ;;
    
    update-configs)
      gemini --yolo -p "Update all MCP server configurations and validate"
      ;;
    
    deploy-new)
      gemini --yolo -p "Deploy new MCP servers from configs and test connections"
      ;;
  esac
}

# Usage
manage_mcp_servers health-check
```

## Advanced Workflows

### Multi-Server Orchestration

```bash
#!/bin/bash
# Orchestrate multiple MCP servers

orchestrate_mcp() {
  # Start all servers
  gemini mcp start database
  gemini mcp start api
  gemini mcp start analytics
  
  # Execute workflow
  gemini --yolo -p "Using all available MCP tools:
  1. Query user data from database
  2. Enrich with API data
  3. Analyze with analytics tools
  4. Generate comprehensive report"
  
  # Stop servers
  gemini mcp stop --all
}
```

### Dynamic Server Management

```bash
#!/bin/bash
# Dynamically add servers based on project

setup_project_mcp() {
  local project_type="$1"
  
  case $project_type in
    ecommerce)
      gemini mcp add --name "payment" --command "payment-mcp"
      gemini mcp add --name "inventory" --command "inventory-mcp"
      gemini mcp add --name "shipping" --command "shipping-mcp"
      ;;
    
    analytics)
      gemini mcp add --name "bigquery" --command "bq-mcp"
      gemini mcp add --name "tableau" --command "tableau-mcp"
      ;;
    
    devops)
      gemini mcp add --name "kubernetes" --command "k8s-mcp"
      gemini mcp add --name "terraform" --command "tf-mcp"
      ;;
  esac
  
  echo "MCP servers configured for $project_type project"
}
```

### Health Monitoring

```bash
#!/bin/bash
# Monitor MCP server health

monitor_mcp_health() {
  while true; do
    echo "=== MCP Server Status ==="
    
    for server in $(gemini mcp list --json | jq -r '.servers[].name'); do
      if gemini mcp test "$server" > /dev/null 2>&1; then
        echo "✓ $server: Healthy"
      else
        echo "✗ $server: Unhealthy"
        
        # Attempt restart
        echo "  Attempting restart..."
        gemini mcp restart "$server"
      fi
    done
    
    sleep 30
  done
}
```

### Load Balancing

```json
// Load-balanced MCP configuration
{
  "mcpServers": {
    "api-pool": {
      "type": "pool",
      "strategy": "round-robin",  // or "random", "least-connections"
      "servers": [
        {
          "command": "node",
          "args": ["api-1.js"],
          "port": 8081
        },
        {
          "command": "node",
          "args": ["api-2.js"],
          "port": 8082
        },
        {
          "command": "node",
          "args": ["api-3.js"],
          "port": 8083
        }
      ],
      "healthCheck": {
        "interval": 10000,
        "timeout": 5000,
        "path": "/health"
      }
    }
  }
}
```

## Security Best Practices

### Authentication

```json
{
  "mcpServers": {
    "secure-server": {
      "command": "python",
      "args": ["server.py"],
      "auth": {
        "type": "bearer",
        "token": "$MCP_AUTH_TOKEN"
      },
      "tls": {
        "enabled": true,
        "cert": "/path/to/cert.pem",
        "key": "/path/to/key.pem",
        "ca": "/path/to/ca.pem"
      }
    }
  }
}
```

### Tool Restrictions

```bash
#!/bin/bash
# Restrict MCP tool access

restrict_mcp_tools() {
  local server="$1"
  local allowed_tools=("$@")
  
  # Generate config with restrictions
  cat > ~/.gemini/mcp-restrictions.json << EOF
{
  "$server": {
    "includeTools": [${allowed_tools[@]}],
    "requireConfirmation": true,
    "logAllCalls": true,
    "maxCallsPerMinute": 10
  }
}
EOF
  
  # Apply restrictions
  gemini mcp update "$server" --config ~/.gemini/mcp-restrictions.json
}

# Usage
restrict_mcp_tools "database" "read_only_query" "get_schema"
```

### Audit Logging

```python
# Auditing MCP server
import logging
import json
from datetime import datetime

class AuditedMCPServer:
    def __init__(self):
        self.audit_log = logging.getLogger('mcp.audit')
        self.audit_log.setLevel(logging.INFO)
        
        # Setup audit file
        handler = logging.FileHandler('/var/log/mcp-audit.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.audit_log.addHandler(handler)
    
    def handle_tool_call(self, tool, params, user_context):
        # Log before execution
        self.audit_log.info(json.dumps({
            'event': 'tool_call_start',
            'tool': tool,
            'params': params,
            'user': user_context,
            'timestamp': datetime.utcnow().isoformat()
        }))
        
        try:
            result = self.execute_tool(tool, params)
            
            # Log success
            self.audit_log.info(json.dumps({
                'event': 'tool_call_success',
                'tool': tool,
                'result_size': len(str(result))
            }))
            
            return result
            
        except Exception as e:
            # Log failure
            self.audit_log.error(json.dumps({
                'event': 'tool_call_failure',
                'tool': tool,
                'error': str(e)
            }))
            raise
```

## Troubleshooting

### Common Issues

1. **Server Won't Start**
```bash
# Check logs
gemini mcp logs <server-name>

# Test manually
python -m my_mcp_server --debug

# Check port conflicts
lsof -i :8080
```

2. **Connection Timeout**
```bash
# Increase timeout
gemini mcp update <server> --timeout 60000

# Check network
ping localhost
telnet localhost 8080
```

3. **Tool Not Available**
```bash
# List available tools
gemini -i
/tools

# Refresh tool list
gemini mcp refresh <server>

# Check server implementation
gemini mcp debug <server>
```

### Debug Mode

```bash
# Enable debug logging
export GEMINI_MCP_DEBUG=true

# Verbose output
gemini --verbose mcp test <server>

# Trace tool calls
gemini --trace -p "Use MCP tools to query database"
```

## Performance Optimization

### Connection Pooling

```json
{
  "mcpServers": {
    "database": {
      "command": "python",
      "args": ["db_mcp.py"],
      "pool": {
        "min": 2,
        "max": 10,
        "idle": 300000  // 5 minutes
      }
    }
  }
}
```

### Caching

```bash
# Enable MCP response caching
export GEMINI_MCP_CACHE=true
export GEMINI_MCP_CACHE_TTL=300  # seconds

# Clear cache
gemini mcp cache clear
```

## Related Skills

- `gemini-cli`: Main Gemini CLI integration
- `gemini-auth`: Authentication management
- `gemini-chat`: Interactive chat sessions
- `gemini-tools`: Tool execution workflows