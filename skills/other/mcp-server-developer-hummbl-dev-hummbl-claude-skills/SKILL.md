---
name: mcp-server-developer
description: Model Context Protocol (MCP) server implementation specialist for Claude Desktop integration. Handles TypeScript/Node.js server scaffolding, endpoint creation, telemetry setup, npx distribution, and comprehensive documentation. Follows MCP specification and best practices for production-grade server deployment.
---

# MCP Server Developer

Expert implementation of Model Context Protocol (MCP) servers for Claude Desktop integration. This skill provides comprehensive guidance for building production-ready MCP servers with TypeScript, including architecture design, endpoint implementation, database integration, telemetry tracking, and distribution via npx.

## Core Competencies

### 1. MCP Server Architecture
- **Scaffold Generation**: TypeScript project setup with proper MCP protocol structure
- **Server Configuration**: MCP protocol compliance, JSON-RPC handling, stdio transport
- **Endpoint Design**: RESTful-style resource and tool endpoints following MCP spec
- **Type Safety**: Strict TypeScript types for requests, responses, and schemas
- **Error Handling**: Comprehensive error catching with proper MCP error responses

### 2. Database Integration
- **D1 SQLite Setup**: Schema design optimized for edge deployment
- **Query Optimization**: <500ms latency targets for all database operations
- **FTS5 Search**: Full-text search implementation for model discovery
- **Data Modeling**: Efficient table structures with proper indexing
- **Migration Scripts**: Version-controlled schema evolution

### 3. Telemetry & Analytics
- **Event Tracking**: Structured logging for install, usage, and performance metrics
- **Latency Monitoring**: Request timing with percentile tracking (p50, p95, p99)
- **User Analytics**: Privacy-respecting usage patterns without PII
- **Error Reporting**: Structured error logging for debugging
- **Success Metrics**: WAU (Weekly Active Users) and engagement tracking

### 4. NPX Distribution
- **Package Configuration**: package.json with proper bin entries for npx execution
- **Version Management**: Semantic versioning with changelog automation
- **Publishing Workflow**: npm registry deployment with CI/CD integration
- **Update Strategy**: Non-breaking updates with deprecation notices
- **Installation Testing**: Cross-platform verification (macOS, Windows, Linux)

## Implementation Guidelines

### Phase 0: Server Scaffold (Week 1)
1. **Initialize TypeScript Project**
   ```bash
   npm init -y
   npm install --save-dev typescript @types/node
   npx tsc --init
   ```

2. **MCP Server Setup**
   - Install MCP SDK: `npm install @modelcontextprotocol/sdk`
   - Create server entry point (`src/index.ts`)
   - Implement stdio transport handler
   - Add basic resource/tool endpoints

3. **Type Definitions**
   ```typescript
   interface MCPServer {
     name: string;
     version: string;
     resources: Resource[];
     tools: Tool[];
   }
   
   interface Resource {
     uri: string;
     name: string;
     description: string;
     mimeType?: string;
   }
   
   interface Tool {
     name: string;
     description: string;
     inputSchema: JSONSchema;
   }
   ```

### Phase 1: Core Functionality (Week 2)
1. **Database Schema**
   ```sql
   CREATE TABLE mental_models (
     id TEXT PRIMARY KEY,
     code TEXT UNIQUE NOT NULL,
     transformation_class TEXT NOT NULL,
     name TEXT NOT NULL,
     description TEXT,
     use_cases JSON,
     difficulty_tier INTEGER,
     prerequisites JSON,
     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   
   CREATE VIRTUAL TABLE models_fts USING fts5(
     code, name, description, use_cases
   );
   ```

2. **Endpoint Implementation**
   - GET resource endpoints (models list, transformations)
   - POST tool endpoints (analyze, decompose, synthesize)
   - Error handling with MCP-compliant responses
   - Input validation with Zod or similar

3. **Transformation Logic**
   - Perspective (P): Multi-viewpoint analysis
   - Inversion (IN): Reverse assumption mapping
   - Composition (CO): Integration synthesis
   - Decomposition (DE): Component breakdown
   - Recursion (RE): Feedback loop identification
   - Meta-Systems (SY): Systems-of-systems coordination

### Phase 2: Documentation & Examples (Week 3)
1. **Quick Start Guide** (5-minute setup)
   ```markdown
   # Quick Start
   
   1. Install via npx:
      ```bash
      npx @hummbl/mcp-server
      ```
   
   2. Configure Claude Desktop:
      Add to `claude_desktop_config.json`:
      ```json
      {
        "mcpServers": {
          "hummbl": {
            "command": "npx",
            "args": ["@hummbl/mcp-server"]
          }
        }
      }
      ```
   
   3. Test in Claude:
      "Use the perspective transformation on this problem: [your problem]"
   ```

2. **Runnable Examples**
   - **Example 1**: Code analysis with decomposition
   - **Example 2**: Strategy synthesis with composition
   - **Example 3**: Decision making with perspective + inversion

3. **Troubleshooting Guide**
   - Installation failures (permissions, npm config)
   - Claude Desktop connection issues
   - Latency/performance problems
   - Error message reference

### Phase 3: Distribution & Testing (Week 4)
1. **NPX Setup**
   ```json
   {
     "name": "@hummbl/mcp-server",
     "version": "1.0.0",
     "bin": {
       "hummbl-mcp": "./dist/index.js"
     },
     "files": ["dist", "README.md", "LICENSE"],
     "publishConfig": {
       "access": "public"
     }
   }
   ```

2. **CI/CD Pipeline**
   - GitHub Actions for automated testing
   - Automated npm publishing on release tags
   - Cross-platform binary testing
   - Documentation deployment

3. **Beta Testing**
   - 3-5 beta testers minimum
   - Structured feedback collection
   - Performance benchmarking
   - Edge case identification

## Quality Gates

### Functional Requirements ✅
- [ ] All MCP endpoints respond correctly to spec
- [ ] Database queries complete <500ms (p95)
- [ ] Zero crashes during 24-hour stability test
- [ ] Error handling covers all edge cases
- [ ] Type safety: 100% TypeScript strict mode

### Documentation Requirements ✅
- [ ] Quick start achieves first run in <5 minutes
- [ ] All examples run without modification
- [ ] Troubleshooting covers 90%+ of common issues
- [ ] API reference is complete and accurate
- [ ] Inline code comments for complex logic

### Adoption Requirements ✅
- [ ] 10+ Weekly Active Users (WAU) by target date
- [ ] 3+ beta testers provide positive feedback
- [ ] Zero P0 bugs in production after Week 2
- [ ] Average user rating ≥4.0/5.0
- [ ] MCP directory listing approved

## MCP Protocol Compliance

### Required Capabilities
1. **Resources**: Read-only data access (models, transformations)
2. **Tools**: Interactive operations (analyze, decompose, synthesize)
3. **Prompts**: Pre-defined workflows (optional in Phase 0)

### Transport Layer
- **stdio**: Standard input/output for Claude Desktop
- **JSON-RPC 2.0**: All requests/responses follow spec
- **Error Codes**: Proper HTTP-style error codes

### Security Best Practices
- Input sanitization for all user-provided data
- Rate limiting to prevent abuse
- No external network calls without explicit permission
- Minimal permissions model
- Audit logging for all operations

## Performance Optimization

### Latency Targets
- **p50**: <100ms for all endpoints
- **p95**: <500ms for database queries
- **p99**: <1000ms for complex transformations

### Optimization Strategies
1. **Database**: Index all frequently queried columns
2. **Caching**: In-memory LRU cache for hot data
3. **Lazy Loading**: Load resources only when needed
4. **Batch Operations**: Group similar queries
5. **Connection Pooling**: Reuse database connections

## Telemetry Schema

```typescript
interface TelemetryEvent {
  event_name: 'mcp_install' | 'mcp_success_run' | 'api_call' | 'doc_view';
  user_id: string; // Anonymized hash
  ts: string; // ISO 8601
  meta: {
    client?: string; // Claude Desktop version
    version?: string; // MCP server version
    model?: string; // e.g., "CO4"
    lat_ms?: number; // Latency in milliseconds
    endpoint?: string; // Endpoint called
    status?: number; // HTTP-style status code
  };
}
```

## Distribution Checklist

### Pre-Publication ✅
- [ ] Version number updated (semantic versioning)
- [ ] CHANGELOG.md updated with release notes
- [ ] README.md reviewed and accurate
- [ ] LICENSE file present (MIT recommended)
- [ ] package.json metadata complete
- [ ] Dependencies audit clean (`npm audit`)
- [ ] Bundle size acceptable (<5MB)

### MCP Directory Submission ✅
- [ ] Clear description (160 characters max)
- [ ] Category selection appropriate
- [ ] Screenshots/demos prepared
- [ ] Usage examples documented
- [ ] Support contact provided

### Post-Publication ✅
- [ ] NPM package downloadable via npx
- [ ] GitHub release created with notes
- [ ] Documentation site updated
- [ ] Community announcement posted
- [ ] Beta testers notified

## Common Pitfalls & Solutions

### Issue: Claude Desktop doesn't detect server
**Solution**: Verify stdio transport is properly initialized and JSON-RPC responses are formatted correctly.

### Issue: High latency (>1s)
**Solution**: Add database indexes, implement caching, or optimize query complexity.

### Issue: Installation fails on Windows
**Solution**: Test with cross-platform paths, avoid shell-specific commands, use `cross-env` for environment variables.

### Issue: Breaking changes between versions
**Solution**: Follow semantic versioning strictly, maintain backwards compatibility, provide migration guides.

## Examples

### Example 1: Minimal MCP Server

```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

const server = new Server({
  name: 'hummbl-mcp-server',
  version: '1.0.0',
}, {
  capabilities: {
    resources: {},
    tools: {},
  },
});

// Register resource: List mental models
server.setRequestHandler('resources/list', async () => ({
  resources: [
    {
      uri: 'hummbl://models',
      name: 'Mental Models',
      description: 'BASE120 mental model collection',
      mimeType: 'application/json',
    },
  ],
}));

// Register tool: Analyze with perspective transformation
server.setRequestHandler('tools/call', async (request) => {
  if (request.params.name === 'analyze-perspective') {
    const { text } = request.params.arguments;
    // Transformation logic here
    return {
      content: [{
        type: 'text',
        text: `Perspective analysis: ${text}`,
      }],
    };
  }
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Example 2: Database Integration

```typescript
import Database from 'better-sqlite3';

const db = new Database('hummbl.db');

// Initialize schema
db.exec(`
  CREATE TABLE IF NOT EXISTS mental_models (
    id TEXT PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    transformation_class TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT
  );
  
  CREATE INDEX IF NOT EXISTS idx_transformation 
  ON mental_models(transformation_class);
`);

// Query with prepared statement
const getModelsByTransformation = db.prepare(`
  SELECT * FROM mental_models 
  WHERE transformation_class = ? 
  ORDER BY code
`);

const perspectiveModels = getModelsByTransformation.all('P');
```

### Example 3: Telemetry Logging

```typescript
function logTelemetry(event: TelemetryEvent) {
  const logEntry = {
    ...event,
    ts: new Date().toISOString(),
  };
  
  // Log to console (development)
  if (process.env.NODE_ENV === 'development') {
    console.log(JSON.stringify(logEntry));
  }
  
  // Send to analytics service (production)
  if (process.env.NODE_ENV === 'production') {
    // TODO: Send to analytics endpoint
  }
}

// Usage
logTelemetry({
  event_name: 'api_call',
  user_id: hashUserId(userId),
  ts: new Date().toISOString(),
  meta: {
    endpoint: '/tools/analyze-perspective',
    lat_ms: 245,
    status: 200,
  },
});
```

## Resources

- **MCP Specification**: https://spec.modelcontextprotocol.io/
- **MCP SDK**: https://github.com/modelcontextprotocol/typescript-sdk
- **Claude Desktop Config**: https://docs.claude.com/en/docs/agents-and-tools/agent-skills
- **TypeScript Best Practices**: https://typescript-lang.org/docs/handbook/intro.html
- **NPM Publishing Guide**: https://docs.npmjs.com/packages-and-modules/contributing-packages-to-the-registry

## Success Criteria

**Phase 0 is successful when:**
1. ✅ `npx @hummbl/mcp-server` runs cleanly on any machine
2. ✅ 10+ developers using it weekly by target date
3. ✅ 3 compelling examples work out-of-the-box
4. ✅ Zero P0 bugs after Week 2
5. ✅ Clear path to Phase 1 identified

**Phase 0 fails if:**
1. ❌ <10 users after 60 days → Pivot to consulting focus
2. ❌ >5 P0 bugs in first 30 days → Architecture review needed
3. ❌ >1000ms latency sustained → Tech stack reassessment required
