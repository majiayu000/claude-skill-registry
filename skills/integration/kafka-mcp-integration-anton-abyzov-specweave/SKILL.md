---
name: kafka-mcp-integration
description: MCP server integration for Kafka operations. Auto-activates on keywords kafka mcp, mcp server, mcp configure, mcp setup, kanapuli, tuannvm, confluent mcp, kafka integration. Provides configuration examples and connection guidance for all 4 MCP servers.
---

# Kafka MCP Server Integration

Expert knowledge for integrating SpecWeave with Kafka MCP (Model Context Protocol) servers. Supports 4 MCP server implementations with auto-detection and configuration guidance.

---

> **Code-First Recommendation**: For most Kafka automation tasks, [writing code is better than MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) (98% token reduction). Use **kafkajs** or **kafka-node** directly:
>
> ```typescript
> import { Kafka } from 'kafkajs';
> const kafka = new Kafka({ brokers: ['localhost:9092'] });
> const producer = kafka.producer();
> await producer.send({ topic: 'events', messages: [{ value: 'Hello' }] });
> ```
>
> **When MCP IS useful**: Quick interactive debugging, topic exploration, Claude Desktop integration.
>
> **When to use code instead**: CI/CD pipelines, test automation, production scripts, anything that should be committed and reusable.

---

## Supported MCP Servers

### 1. kanapuli/mcp-kafka (Node.js)

**Installation**:
```bash
npm install -g mcp-kafka
```

**Capabilities**:
- Authentication: SASL_PLAINTEXT, PLAINTEXT
- Operations: produce, consume, list-topics, describe-topic, get-offsets
- Best for: Basic Kafka operations, quick prototyping

**Configuration Example**:
```json
{
  "mcpServers": {
    "kafka": {
      "command": "npx",
      "args": ["mcp-kafka"],
      "env": {
        "KAFKA_BROKERS": "localhost:9092",
        "KAFKA_SASL_MECHANISM": "plain",
        "KAFKA_SASL_USERNAME": "user",
        "KAFKA_SASL_PASSWORD": "password"
      }
    }
  }
}
```

### 2. tuannvm/kafka-mcp-server (Go)

**Installation**:
```bash
go install github.com/tuannvm/kafka-mcp-server@latest
```

**Capabilities**:
- Authentication: SASL_SCRAM_SHA_256, SASL_SCRAM_SHA_512, SASL_SSL, PLAINTEXT
- Operations: All CRUD operations, consumer group management, offset management
- Best for: Production use, advanced SASL authentication

**Configuration Example**:
```json
{
  "mcpServers": {
    "kafka": {
      "command": "kafka-mcp-server",
      "args": [
        "--brokers", "localhost:9092",
        "--sasl-mechanism", "SCRAM-SHA-256",
        "--sasl-username", "admin",
        "--sasl-password", "admin-secret"
      ]
    }
  }
}
```

### 3. Joel-hanson/kafka-mcp-server (Python)

**Installation**:
```bash
pip install kafka-mcp-server
```

**Capabilities**:
- Authentication: SASL_PLAINTEXT, PLAINTEXT, SSL
- Operations: produce, consume, list-topics, describe-topic
- Best for: Claude Desktop integration, Python ecosystem

**Configuration Example**:
```json
{
  "mcpServers": {
    "kafka": {
      "command": "python",
      "args": ["-m", "kafka_mcp_server"],
      "env": {
        "KAFKA_BOOTSTRAP_SERVERS": "localhost:9092"
      }
    }
  }
}
```

### 4. Confluent Official MCP (Enterprise)

**Installation**:
```bash
confluent plugin install mcp-server
```

**Capabilities**:
- Authentication: OAuth, SASL_SCRAM, API Keys
- Operations: All Kafka operations, Schema Registry, ksqlDB, Flink SQL
- Advanced: Natural language interface, AI-powered query generation
- Best for: Confluent Cloud, enterprise deployments

**Configuration Example**:
```json
{
  "mcpServers": {
    "kafka": {
      "command": "confluent",
      "args": ["mcp", "start"],
      "env": {
        "CONFLUENT_CLOUD_API_KEY": "your-api-key",
        "CONFLUENT_CLOUD_API_SECRET": "your-api-secret"
      }
    }
  }
}
```

## Auto-Detection

SpecWeave can auto-detect installed MCP servers:

```bash
/sw-kafka:mcp-configure
```

This command:
1. Scans for installed MCP servers (npm, go, pip, confluent CLI)
2. Checks which servers are currently running
3. Ranks servers by capabilities (Confluent > tuannvm > kanapuli > Joel-hanson)
4. Generates recommended configuration
5. Tests connection

## Quick Start

### Option 1: Auto-Configure (Recommended)

```bash
/sw-kafka:mcp-configure
```

Interactive wizard guides you through:
- MCP server selection (or auto-detect)
- Broker URL configuration
- Authentication setup
- Connection testing

### Option 2: Manual Configuration

1. **Install preferred MCP server** (see installation commands above)

2. **Create `.mcp.json` configuration**:

```json
{
  "serverType": "tuannvm",
  "brokerUrls": ["localhost:9092"],
  "authentication": {
    "mechanism": "SASL/SCRAM-SHA-256",
    "username": "admin",
    "password": "admin-secret"
  }
}
```

3. **Test connection**:

```bash
# Via MCP server CLI
kafka-mcp-server test-connection

# Or via SpecWeave
node -e "import('./dist/lib/mcp/detector.js').then(async ({ MCPServerDetector }) => {
  const detector = new MCPServerDetector();
  const result = await detector.detectAll();
  console.log(JSON.stringify(result, null, 2));
});"
```

## MCP Server Comparison

| Feature | kanapuli | tuannvm | Joel-hanson | Confluent |
|---------|----------|---------|-------------|-----------|
| **Language** | Node.js | Go | Python | Official CLI |
| **SASL_PLAINTEXT** | ✅ | ✅ | ✅ | ✅ |
| **SCRAM-SHA-256** | ❌ | ✅ | ❌ | ✅ |
| **SCRAM-SHA-512** | ❌ | ✅ | ❌ | ✅ |
| **mTLS/SSL** | ❌ | ✅ | ✅ | ✅ |
| **OAuth** | ❌ | ❌ | ❌ | ✅ |
| **Consumer Groups** | ❌ | ✅ | ❌ | ✅ |
| **Offset Mgmt** | ❌ | ✅ | ❌ | ✅ |
| **Schema Registry** | ❌ | ❌ | ❌ | ✅ |
| **ksqlDB** | ❌ | ❌ | ❌ | ✅ |
| **Flink SQL** | ❌ | ❌ | ❌ | ✅ |
| **AI/NL Interface** | ❌ | ❌ | ❌ | ✅ |
| **Best For** | Prototyping | Production | Desktop | Enterprise |

## Troubleshooting

### MCP Server Not Detected

```bash
# Check if MCP server installed
npm list -g mcp-kafka         # kanapuli
which kafka-mcp-server        # tuannvm
pip show kafka-mcp-server     # Joel-hanson
confluent version             # Confluent
```

### Connection Refused

- Verify Kafka broker is running: `kcat -L -b localhost:9092`
- Check firewall rules
- Validate broker URL (correct host:port)

### Authentication Failed

- Double-check credentials (username, password, API keys)
- Verify SASL mechanism matches broker configuration
- Check broker logs for authentication errors

### Operations Not Working

- Ensure MCP server supports the operation (see comparison table)
- Check broker ACLs (permissions for the authenticated user)
- Verify topic exists: `/sw-kafka:mcp-configure list-topics`

## Operations via MCP

Once configured, you can perform Kafka operations via MCP:

```typescript
import { MCPServerDetector } from './lib/mcp/detector';

const detector = new MCPServerDetector();
const result = await detector.detectAll();

// Use recommended server
if (result.recommended) {
  console.log(`Using ${result.recommended} MCP server`);
  console.log(`Reason: ${result.rankingReason}`);
}
```

## Security Best Practices

1. **Never commit credentials** - Use environment variables or secrets manager
2. **Use strongest auth** - Prefer SCRAM-SHA-512 > SCRAM-SHA-256 > PLAINTEXT
3. **Enable TLS/SSL** - Encrypt communication with broker
4. **Rotate credentials** - Regularly update passwords and API keys
5. **Least privilege** - Grant only necessary ACLs to MCP server user

## Related Commands

- `/sw-kafka:mcp-configure` - Interactive MCP server setup
- `/sw-kafka:dev-env start` - Start local Kafka for testing
- `/sw-kafka:deploy` - Deploy production Kafka cluster

## External Links

- [kanapuli/mcp-kafka](https://github.com/kanapuli/mcp-kafka)
- [tuannvm/kafka-mcp-server](https://github.com/tuannvm/kafka-mcp-server)
- [Joel-hanson/kafka-mcp-server](https://github.com/Joel-hanson/kafka-mcp-server)
- [Confluent MCP Documentation](https://docs.confluent.io/platform/current/mcp/)
- [MCP Protocol Specification](https://modelcontextprotocol.org/)
