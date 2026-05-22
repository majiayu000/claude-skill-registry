---
name: when-bridging-web-cli-use-web-cli-teleport
description: Bridge web interfaces with CLI workflows for seamless bidirectional integration
version: 1.0.0
tags:
  - web
  - cli
  - integration
  - bridge
  - teleport
category: workflow
agents:
  - backend-dev
  - system-architect
complexity: advanced
estimated_duration: 45-90 minutes
prerequisites:
  - Claude Flow installed
  - Web development experience
  - CLI knowledge
outputs:
  - Web-CLI bridge
  - API endpoints
  - CLI integration
  - Bidirectional communication
---

# Web-CLI Teleport SOP

## Overview

Bridge web interfaces with CLI workflows for seamless integration, enabling web applications to trigger CLI commands and CLI tools to display web interfaces.

## Agents & Responsibilities

### backend-dev
**Role:** Implement bridge API and integration logic
**Responsibilities:**
- Build REST API for CLI integration
- Implement WebSocket for real-time communication
- Handle authentication and security
- Manage state synchronization

### system-architect
**Role:** Design bridge architecture and patterns
**Responsibilities:**
- Design integration architecture
- Define communication protocols
- Plan security model
- Ensure scalability

## Phase 1: Design Bridge Architecture

### Objective
Design architecture for bidirectional web-CLI communication.

### Scripts

```bash
# Generate architecture diagram
npx claude-flow@alpha architect design \
  --type "web-cli-bridge" \
  --output bridge-architecture.json

# Define API specification
cat > api-spec.yaml <<EOF
openapi: 3.0.0
info:
  title: Web-CLI Bridge API
  version: 1.0.0
paths:
  /cli/execute:
    post:
      summary: Execute CLI command from web
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                command: { type: string }
                args: { type: array }
      responses:
        '200':
          description: Command output
  /web/render:
    post:
      summary: Render web UI from CLI
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                component: { type: string }
                data: { type: object }
EOF

# Store architecture
npx claude-flow@alpha memory store \
  --key "bridge/architecture" \
  --file bridge-architecture.json
```

### Architecture Patterns

**Web → CLI:**
```
Web UI → REST API → CLI Executor → Command → Output → API → Web UI
```

**CLI → Web:**
```
CLI Tool → WebSocket → Web Server → Browser → UI Render
```

**Bidirectional:**
```
Web UI ←→ WebSocket ←→ Bridge Server ←→ CLI Tools
```

## Phase 2: Implement Web Interface

### Objective
Build web interface that can trigger and monitor CLI commands.

### Scripts

```bash
# Create web application
npx create-react-app web-cli-bridge
cd web-cli-bridge

# Install dependencies
npm install axios socket.io-client

# Generate web components
npx claude-flow@alpha generate component \
  --name "CLIExecutor" \
  --type "react" \
  --output src/components/CLIExecutor.jsx

# Build web interface
npm run build

# Deploy web app
npx claude-flow@alpha deploy web \
  --source ./build \
  --target ./deploy/web
```

### Web Component Example

```javascript
// src/components/CLIExecutor.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import io from 'socket.io-client';

function CLIExecutor() {
  const [command, setCommand] = useState('');
  const [output, setOutput] = useState('');
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const newSocket = io('http://localhost:3001');
    setSocket(newSocket);

    newSocket.on('cli-output', (data) => {
      setOutput(prev => prev + data + '\n');
    });

    return () => newSocket.close();
  }, []);

  const executeCommand = async () => {
    try {
      const response = await axios.post('/api/cli/execute', {
        command,
        args: command.split(' ').slice(1)
      });
      setOutput(response.data.output);
    } catch (error) {
      setOutput(`Error: ${error.message}`);
    }
  };

  return (
    <div className="cli-executor">
      <input
        type="text"
        value={command}
        onChange={(e) => setCommand(e.target.value)}
        placeholder="Enter CLI command..."
      />
      <button onClick={executeCommand}>Execute</button>
      <pre className="output">{output}</pre>
    </div>
  );
}

export default CLIExecutor;
```

## Phase 3: Implement CLI Bridge

### Objective
Build CLI-side bridge that connects to web interface.

### Scripts

```bash
# Create bridge server
mkdir cli-bridge
cd cli-bridge
npm init -y
npm install express socket.io cors child_process

# Generate bridge server
npx claude-flow@alpha generate server \
  --type "bridge" \
  --output server.js

# Start bridge server
node server.js &

# Test connection
curl -X POST http://localhost:3001/api/cli/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "ls", "args": ["-la"]}'
```

### Bridge Server Implementation

```javascript
// server.js
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const { exec } = require('child_process');
const cors = require('cors');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, { cors: { origin: '*' } });

app.use(cors());
app.use(express.json());

// Execute CLI command from web
app.post('/api/cli/execute', (req, res) => {
  const { command, args = [] } = req.body;
  const fullCommand = `${command} ${args.join(' ')}`;

  exec(fullCommand, (error, stdout, stderr) => {
    if (error) {
      return res.status(500).json({
        error: error.message,
        stderr
      });
    }

    res.json({
      output: stdout,
      stderr
    });

    // Broadcast to all connected clients
    io.emit('cli-output', stdout);
  });
});

// Render web UI from CLI
app.post('/api/web/render', (req, res) => {
  const { component, data } = req.body;

  io.emit('render-component', {
    component,
    data
  });

  res.json({ success: true });
});

// WebSocket connection
io.on('connection', (socket) => {
  console.log('Client connected');

  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });
});

server.listen(3001, () => {
  console.log('Bridge server running on port 3001');
});
```

### CLI Tool Integration

```bash
#!/bin/bash
# cli-tool-with-web.sh

# Function to render web UI from CLI
render_web_ui() {
  local component=$1
  local data=$2

  curl -X POST http://localhost:3001/api/web/render \
    -H "Content-Type: application/json" \
    -d "{\"component\": \"$component\", \"data\": $data}"
}

# Example: Show analysis results in web UI
analyze_code() {
  local path=$1
  local results=$(npx claude-flow@alpha analyze "$path" --format json)

  # Send results to web interface
  render_web_ui "AnalysisResults" "$results"

  echo "Results sent to web interface"
}

analyze_code ./src
```

## Phase 4: Test Integration

### Objective
Validate bidirectional communication and error handling.

### Scripts

```bash
# Test web → CLI
curl -X POST http://localhost:3001/api/cli/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "npx", "args": ["claude-flow@alpha", "swarm", "status"]}'

# Test CLI → web
bash cli-tool-with-web.sh

# Test WebSocket connection
node test-websocket.js

# Run integration tests
npm test -- --testPathPattern=integration

# Load testing
npx artillery quick --count 10 -n 20 http://localhost:3001/api/cli/execute
```

### Integration Tests

```javascript
// tests/integration.test.js
const request = require('supertest');
const io = require('socket.io-client');
const app = require('../server');

describe('Web-CLI Bridge Integration', () => {
  let socket;

  beforeAll((done) => {
    socket = io('http://localhost:3001');
    socket.on('connect', done);
  });

  afterAll(() => {
    socket.close();
  });

  it('should execute CLI command from web', async () => {
    const response = await request(app)
      .post('/api/cli/execute')
      .send({ command: 'echo', args: ['test'] });

    expect(response.status).toBe(200);
    expect(response.body.output).toContain('test');
  });

  it('should broadcast CLI output via WebSocket', (done) => {
    socket.on('cli-output', (data) => {
      expect(data).toBeDefined();
      done();
    });

    request(app)
      .post('/api/cli/execute')
      .send({ command: 'echo', args: ['websocket test'] });
  });

  it('should render web UI from CLI', async () => {
    const response = await request(app)
      .post('/api/web/render')
      .send({
        component: 'TestComponent',
        data: { test: true }
      });

    expect(response.status).toBe(200);
    expect(response.body.success).toBe(true);
  });
});
```

## Phase 5: Deploy and Monitor

### Objective
Deploy bridge to production and monitor performance.

### Scripts

```bash
# Build for production
npm run build:web
npm run build:server

# Deploy with Docker
cat > Dockerfile <<EOF
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
EXPOSE 3001
CMD ["node", "server.js"]
EOF

docker build -t web-cli-bridge .
docker run -d -p 3001:3001 web-cli-bridge

# Monitor with Prometheus
cat > prometheus.yml <<EOF
scrape_configs:
  - job_name: 'bridge'
    static_configs:
      - targets: ['localhost:3001']
EOF

# Setup logging
mkdir logs
node server.js > logs/bridge.log 2>&1 &

# Monitor logs
tail -f logs/bridge.log

# Health check
curl http://localhost:3001/health
```

## Success Criteria

- [ ] Bridge architecture designed
- [ ] Web interface functional
- [ ] CLI bridge operational
- [ ] Integration tested
- [ ] Deployed and monitored

### Performance Targets
- API response time: <200ms
- WebSocket latency: <50ms
- Command execution: <5s
- Uptime: >99.9%

## Best Practices

1. **Security:** Implement authentication and authorization
2. **Error Handling:** Graceful error handling on both sides
3. **Logging:** Comprehensive logging for debugging
4. **Rate Limiting:** Prevent abuse
5. **Validation:** Validate all inputs
6. **Monitoring:** Track performance metrics
7. **Documentation:** Document API and protocols
8. **Testing:** Comprehensive integration tests

## Common Issues & Solutions

### Issue: Command Execution Timeout
**Symptoms:** Long-running commands hang
**Solution:** Implement timeout mechanism, use async execution

### Issue: WebSocket Disconnections
**Symptoms:** Frequent disconnections
**Solution:** Implement reconnection logic, use heartbeat

### Issue: Security Vulnerabilities
**Symptoms:** Unauthorized command execution
**Solution:** Implement authentication, whitelist commands

## Integration Points

- **swarm-orchestration:** Execute orchestration from web
- **performance-analysis:** Display metrics in web UI
- **slash-commands:** Expose commands via web

## References

- WebSocket Protocol
- REST API Design
- CLI Integration Patterns
- Security Best Practices
