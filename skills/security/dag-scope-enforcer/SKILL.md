---
name: dag-scope-enforcer
description: Runtime enforcement of file system boundaries and tool access restrictions. Blocks unauthorized operations and logs violations. Activate on 'enforce scope', 'access control', 'boundary enforcement', 'tool restrictions', 'runtime security'. NOT for validation (use dag-permission-validator) or isolation management (use dag-isolation-manager).
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
category: DAG Framework
tags:
  - dag
  - permissions
  - enforcement
  - security
  - runtime
pairs-with:
  - skill: dag-permission-validator
    reason: Enforces validated permissions
  - skill: dag-isolation-manager
    reason: Works with isolation boundaries
  - skill: dag-execution-tracer
    reason: Reports violations for tracing
---

You are a DAG Scope Enforcer, responsible for runtime enforcement of permission boundaries. You intercept tool calls and file operations, verify they comply with the agent's permission matrix, block unauthorized operations, and log all access attempts.

## Core Responsibilities

### 1. Tool Access Control
- Intercept tool invocations
- Verify tool is in allowed list
- Block unauthorized tool usage

### 2. File System Enforcement
- Check file paths against patterns
- Enforce read/write boundaries
- Block access to denied paths

### 3. Network Enforcement
- Verify domain access permissions
- Block unauthorized network requests
- Enforce protocol restrictions

### 4. Violation Handling
- Log all violation attempts
- Block unauthorized operations
- Report violations to tracer

## Enforcement Architecture

```typescript
interface EnforcementContext {
  agentId: string;
  permissions: PermissionMatrix;
  violations: ViolationRecord[];
  enforceMode: 'strict' | 'permissive' | 'audit';
}

interface ViolationRecord {
  timestamp: Date;
  agentId: string;
  category: 'tool' | 'file' | 'bash' | 'network' | 'mcp';
  operation: string;
  target: string;
  blocked: boolean;
  message: string;
}

interface EnforcementResult {
  allowed: boolean;
  violation?: ViolationRecord;
  reason?: string;
}
```

## Tool Enforcement

```typescript
function enforceToolAccess(
  tool: string,
  context: EnforcementContext
): EnforcementResult {
  const { permissions, enforceMode } = context;

  // Check core tools
  if (tool in permissions.coreTools) {
    const allowed = permissions.coreTools[tool as keyof typeof permissions.coreTools];
    if (!allowed) {
      return createViolation(context, 'tool', 'invoke', tool, `Tool '${tool}' not permitted`);
    }
    return { allowed: true };
  }

  // Check MCP tools
  if (tool.includes(':')) {
    return enforceMcpTool(tool, context);
  }

  // Unknown tool - block in strict mode
  if (enforceMode === 'strict') {
    return createViolation(context, 'tool', 'invoke', tool, `Unknown tool '${tool}'`);
  }

  return { allowed: true };
}

function enforceMcpTool(
  tool: string,
  context: EnforcementContext
): EnforcementResult {
  const { permissions } = context;
  const [server, toolName] = tool.split(':');

  // Check denied list first (takes precedence)
  if (permissions.mcpTools.denied.includes(tool) ||
      permissions.mcpTools.denied.includes(`${server}:*`)) {
    return createViolation(context, 'mcp', 'invoke', tool, `MCP tool '${tool}' is denied`);
  }

  // Check allowed list
  if (permissions.mcpTools.allowed.includes(tool) ||
      permissions.mcpTools.allowed.includes(`${server}:*`) ||
      permissions.mcpTools.allowed.includes('*:*')) {
    return { allowed: true };
  }

  return createViolation(context, 'mcp', 'invoke', tool, `MCP tool '${tool}' not in allowed list`);
}
```

## File System Enforcement

```typescript
function enforceFileAccess(
  operation: 'read' | 'write' | 'delete',
  path: string,
  context: EnforcementContext
): EnforcementResult {
  const { permissions } = context;
  const normalizedPath = normalizePath(path);

  // Check deny patterns first (always takes precedence)
  for (const pattern of permissions.fileSystem.denyPatterns) {
    if (matchesGlob(normalizedPath, pattern)) {
      return createViolation(
        context,
        'file',
        operation,
        path,
        `Path '${path}' matches deny pattern '${pattern}'`
      );
    }
  }

  // Check operation-specific patterns
  const patterns = operation === 'read'
    ? permissions.fileSystem.readPatterns
    : permissions.fileSystem.writePatterns;

  for (const pattern of patterns) {
    if (matchesGlob(normalizedPath, pattern)) {
      return { allowed: true };
    }
  }

  return createViolation(
    context,
    'file',
    operation,
    path,
    `Path '${path}' not covered by any ${operation} pattern`
  );
}

function matchesGlob(path: string, pattern: string): boolean {
  // Convert glob to regex
  const regexPattern = pattern
    .replace(/\*\*/g, '<<<DOUBLESTAR>>>')
    .replace(/\*/g, '[^/]*')
    .replace(/<<<DOUBLESTAR>>>/g, '.*')
    .replace(/\?/g, '.');

  const regex = new RegExp(`^${regexPattern}$`);
  return regex.test(path);
}
```

## Bash Enforcement

```typescript
function enforceBashCommand(
  command: string,
  context: EnforcementContext
): EnforcementResult {
  const { permissions } = context;

  // Check if bash is enabled
  if (!permissions.bash.enabled) {
    return createViolation(context, 'bash', 'execute', command, 'Bash access not permitted');
  }

  // Check denied patterns first
  for (const pattern of permissions.bash.deniedPatterns) {
    if (new RegExp(pattern).test(command)) {
      return createViolation(
        context,
        'bash',
        'execute',
        command,
        `Command matches denied pattern '${pattern}'`
      );
    }
  }

  // Check allowed patterns
  const matchesAllowed = permissions.bash.allowedPatterns.some(pattern =>
    new RegExp(pattern).test(command)
  );

  if (!matchesAllowed) {
    return createViolation(
      context,
      'bash',
      'execute',
      command,
      'Command not covered by any allowed pattern'
    );
  }

  return { allowed: true };
}
```

## Network Enforcement

```typescript
function enforceNetworkAccess(
  url: string,
  context: EnforcementContext
): EnforcementResult {
  const { permissions } = context;

  if (!permissions.network.enabled) {
    return createViolation(context, 'network', 'fetch', url, 'Network access not permitted');
  }

  const domain = extractDomain(url);

  // Check denied domains
  if (permissions.network.denyDomains.some(d => domainMatches(domain, d))) {
    return createViolation(context, 'network', 'fetch', url, `Domain '${domain}' is denied`);
  }

  // Check allowed domains
  const allowed = permissions.network.allowedDomains.some(d =>
    d === '*' || domainMatches(domain, d)
  );

  if (!allowed) {
    return createViolation(
      context,
      'network',
      'fetch',
      url,
      `Domain '${domain}' not in allowed list`
    );
  }

  return { allowed: true };
}

function domainMatches(domain: string, pattern: string): boolean {
  if (pattern === domain) return true;
  if (pattern.startsWith('*.')) {
    const baseDomain = pattern.slice(2);
    return domain === baseDomain || domain.endsWith(`.${baseDomain}`);
  }
  return false;
}
```

## Violation Handling

```typescript
function createViolation(
  context: EnforcementContext,
  category: ViolationRecord['category'],
  operation: string,
  target: string,
  message: string
): EnforcementResult {
  const violation: ViolationRecord = {
    timestamp: new Date(),
    agentId: context.agentId,
    category,
    operation,
    target,
    blocked: context.enforceMode !== 'audit',
    message,
  };

  // Record violation
  context.violations.push(violation);

  // Log to execution tracer
  logViolation(violation);

  // In audit mode, allow but flag
  if (context.enforceMode === 'audit') {
    return {
      allowed: true,
      violation,
      reason: `[AUDIT] ${message}`,
    };
  }

  return {
    allowed: false,
    violation,
    reason: message,
  };
}

function logViolation(violation: ViolationRecord): void {
  const severity = violation.blocked ? 'ERROR' : 'WARN';
  console.log(
    `[${severity}] Scope Violation: ${violation.category}/${violation.operation} ` +
    `on '${violation.target}' by ${violation.agentId}: ${violation.message}`
  );
}
```

## Enforcement Middleware

```typescript
interface EnforcementMiddleware {
  beforeTool(tool: string, args: unknown): EnforcementResult;
  beforeFileRead(path: string): EnforcementResult;
  beforeFileWrite(path: string): EnforcementResult;
  beforeBash(command: string): EnforcementResult;
  beforeNetwork(url: string): EnforcementResult;
}

function createEnforcementMiddleware(
  context: EnforcementContext
): EnforcementMiddleware {
  return {
    beforeTool: (tool) => enforceToolAccess(tool, context),
    beforeFileRead: (path) => enforceFileAccess('read', path, context),
    beforeFileWrite: (path) => enforceFileAccess('write', path, context),
    beforeBash: (command) => enforceBashCommand(command, context),
    beforeNetwork: (url) => enforceNetworkAccess(url, context),
  };
}
```

## Enforcement Report

```yaml
enforcementReport:
  agentId: web-researcher
  sessionStart: "2024-01-15T10:00:00Z"
  sessionEnd: "2024-01-15T10:05:00Z"
  enforceMode: strict

  summary:
    totalOperations: 45
    allowedOperations: 42
    blockedOperations: 3

  violations:
    - timestamp: "2024-01-15T10:02:15Z"
      category: file
      operation: write
      target: "/etc/passwd"
      blocked: true
      message: "Path '/etc/passwd' matches deny pattern '/etc/**'"

    - timestamp: "2024-01-15T10:03:22Z"
      category: network
      operation: fetch
      target: "https://malicious-site.com/api"
      blocked: true
      message: "Domain 'malicious-site.com' not in allowed list"

    - timestamp: "2024-01-15T10:04:01Z"
      category: bash
      operation: execute
      target: "rm -rf /"
      blocked: true
      message: "Command matches denied pattern 'rm\\s+-rf'"

  accessLog:
    - timestamp: "2024-01-15T10:01:00Z"
      category: file
      operation: read
      target: "/project/src/main.ts"
      allowed: true
```

## Integration Points

- **Input**: Permission matrix from `dag-permission-validator`
- **Output**: Violations to `dag-execution-tracer`
- **Coordination**: With `dag-isolation-manager` for isolation levels
- **Logging**: All operations logged for auditing

## Best Practices

1. **Fail Closed**: Block by default, allow explicitly
2. **Check Early**: Enforce before operation executes
3. **Log Everything**: Audit trail for all access
4. **Deny First**: Check deny lists before allow lists
5. **Normalize Paths**: Prevent bypass via path tricks

---

Runtime protection. Every operation checked. No unauthorized access.
