---
name: workflow-json-architect
description: n8n workflow JSON structure management for Vigil Guard v2.0.0 (24-node 3-branch parallel pipeline). Use for node manipulation, connections, Code node JavaScript, 3-Branch Executor logic, Arbiter v2 integration, and critical reminder to import workflow to n8n GUI.
version: 2.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# n8n Workflow JSON Architecture Management (v2.0.0)

## Overview

Expert guidance for managing n8n workflow JSON files (24 nodes, 3-branch parallel detection) in Vigil Guard v2.0.0. This skill focuses **exclusively** on the JSON structure, node manipulation, connections, and workflow lifecycle - NOT on detection patterns or business logic (see `n8n-vigil-workflow` for patterns).

## When to Use This Skill

- Modifying workflow JSON structure (`Vigil Guard v2.0.0.json`)
- Adding/removing/reordering nodes
- Editing Code node embedded JavaScript
- Managing node connections and data flow
- Working with 3-Branch Executor node
- Configuring Arbiter v2 weighted fusion
- Migrating workflows between versions
- Debugging workflow execution errors
- Understanding n8n JSON schema
- **Explaining to user: "Import workflow to n8n GUI NOW!"**

## v2.0.0 Architecture Change

### From 40-node Sequential → 24-node 3-Branch Parallel

```
OLD (v1.x): 40+ nodes, sequential processing, rules.config.json

NEW (v2.0.0): 24 nodes, 3-branch parallel detection
  - 3-Branch Executor (parallel HTTP calls)
  - Arbiter v2 (weighted fusion)
  - No rules.config.json (patterns in heuristics-service)
```

## CRITICAL: Workflow Lifecycle Understanding

### The #1 Most Important Concept

**n8n workflows are stored in SQLite database, NOT in JSON files!**

```yaml
TRUTH:
  - Workflow execution reads from: SQLite database (/home/node/.n8n/database.sqlite)
  - JSON file in repo is: Backup/version control ONLY
  - Changes to JSON have NO EFFECT until user imports to n8n GUI

WORKFLOW:
  1. Edit JSON file in repo
  2. IMMEDIATELY tell user: " IMPORT THIS FILE TO n8n GUI NOW!"
  3. User imports via: n8n GUI → Import from File
  4. n8n copies JSON → SQLite database
  5. Workflow executes from SQLite (NOT from file)
```

### CROWN RULE: WORKFLOW IMPORT STATUS - OPERATOR TRUST AXIOM

**ABSOLUTELY FORBIDDEN DEBUGGING HYPOTHESES:**

```yaml
NEVER CHECK:
  - "Was the workflow imported?"
  - "Is the workflow in n8n SQL database?"
  - "Is the workflow active?"
  - "Did you activate the workflow after import?"

INDISPUTABLE FACT:
  - If operator confirmed import: workflow IS imported
  - Workflow IS in SQLite database
  - Workflow IS active
  - All Code nodes have LATEST JavaScript from JSON file
  - This is 100% TRUTH without verification

CORRECT DEBUGGING APPROACH:
  - Operator confirms import → END OF STORY
  - Problem is NOT in import
  - Problem IS in workflow logic
  - Debug: analyze node code, tests, configuration
  - DO NOT waste tokens verifying import
```

### User Communication Template

```markdown
Workflow JSON updated successfully!

**CRITICAL NEXT STEP - DO THIS NOW:**

1. Open n8n GUI: http://localhost:5678
2. Click menu (≡) → **Import from File**
3. Select: `services/workflow/workflows/Vigil Guard v2.0.0.json`
4. Confirm import
5. Activate workflow (toggle switch)

**Your changes will NOT work until you complete this import!**

After importing, test with: n8n GUI → Test workflow → Chat tab
```

## Workflow JSON Structure (v2.0.0)

### Top-Level Schema

```json
{
  "name": "Vigil Guard v2.0.0",
  "nodes": [
    {
      "parameters": {},
      "id": "unique-uuid",
      "name": "Node_Name",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [x, y]
    }
  ],
  "connections": {
    "Source_Node": {
      "main": [
        [
          {
            "node": "Target_Node",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "settings": {
    "executionOrder": "v1"
  },
  "updatedAt": "2025-01-30T10:00:00.000Z",
  "versionId": "uuid"
}
```

### 24-Node Architecture (v2.0.0)

```
1. When chat message received    # Chat trigger
2. Webhook v2                    # HTTP webhook trigger
3. Extract Input                 # Normalize input format
4. Load allowlist.schema.json    # Load allowlist config
5. Load pii.conf                 # Load PII patterns (361 lines)
6. Load unified_config.json      # Load main config (303 lines, v5.0.0)
7. Extract allowlist             # Parse allowlist
8. Extract pii.conf              # Parse PII config
9. Extract unified_config        # Parse main config
10. Merge Config                 # Combine all configs
11. Config Loader v2             # Final config object
12. Input Validator v2           # Validate input (length, format)
13. Validation Check             # Route based on validation
14. 3-Branch Executor            # PARALLEL branch execution (CRITICAL)
15. Arbiter v2                   # Weighted score fusion (CRITICAL)
16. Arbiter Decision             # Route based on score
17. PII_Redactor_v2              # Dual-language PII detection
18. Block Response v2            # Generate block response
19. Merge Final                  # Merge all paths
20. Build NDJSON v2              # Format for logging
21. Log to ClickHouse v2         # Send to analytics DB
22. Clean Output v2              # User-facing result
23. Early Block v2               # Fast-path for validation failures
24. output to plugin             # Browser extension response
```

### Node Types

**Core Processing Nodes:**
1. **Code** - Custom JavaScript logic (most common)
2. **HTTP Request** - API calls (3-branch services, Presidio, ClickHouse)
3. **Merge** - Combine data streams (config merge, path merge)
4. **Switch** - Conditional routing (thresholds)
5. **Set** - Variable assignment
6. **Webhook** - Trigger endpoint

### Data Flow (3-Branch Parallel)

```
Webhook Trigger
  → Extract Input
  → Config Loader v2 (merge configs)
  → Input Validator v2
  → 3-Branch Executor (PARALLEL):
      ├─ HTTP: heuristics-service:5005 (Branch A)
      ├─ HTTP: semantic-service:5006 (Branch B)
      └─ HTTP: prompt-guard-api:8000 (Branch C)
  → Arbiter v2 (weighted fusion: A*0.30 + B*0.35 + C*0.35)
  → Arbiter Decision (Switch)
      ├─ ALLOW → Clean Output
      ├─ SANITIZE → PII_Redactor_v2 → Clean Output
      └─ BLOCK → Block Response
  → Build NDJSON v2
  → Log to ClickHouse v2
  → Clean Output v2
```

## Common Tasks

### Task 1: Modify 3-Branch Executor

**Example: Add timeout to branch calls**

```javascript
// Find 3-Branch Executor node
const branchNode = workflow.nodes.find(n => n.name === "3-Branch Executor");

// Modify HTTP parameters for each branch
branchNode.parameters = {
  jsCode: `
    const items = $input.all();
    const text = items[0].json.sanitized_input || items[0].json.chatInput;
    const requestId = items[0].json.request_id || 'default';

    // Branch timeouts (v2.0.0)
    const TIMEOUTS = {
      A: 1000,  // Heuristics: 1 second
      B: 2000,  // Semantic: 2 seconds
      C: 3000   // LLM Guard: 3 seconds
    };

    // Parallel branch execution
    const [branchA, branchB, branchC] = await Promise.allSettled([
      // Branch A: Heuristics Service
      fetch('http://heuristics-service:5005/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, request_id: requestId }),
        signal: AbortSignal.timeout(TIMEOUTS.A)
      }).then(r => r.json()),

      // Branch B: Semantic Service
      fetch('http://semantic-service:5006/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, request_id: requestId }),
        signal: AbortSignal.timeout(TIMEOUTS.B)
      }).then(r => r.json()),

      // Branch C: LLM Guard
      fetch('http://prompt-guard-api:8000/detect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
        signal: AbortSignal.timeout(TIMEOUTS.C)
      }).then(r => r.json())
    ]);

    return [{
      json: {
        ...items[0].json,
        branch_results: {
          A: branchA.status === 'fulfilled' ? branchA.value : { score: 0, degraded: true },
          B: branchB.status === 'fulfilled' ? branchB.value : { score: 0, degraded: true },
          C: branchC.status === 'fulfilled' ? branchC.value : { score: 0, degraded: true }
        }
      }
    }];
  `
};
```

### Task 2: Modify Arbiter v2 Weights

**Example: Change branch weights**

```javascript
// Find Arbiter v2 node
const arbiterNode = workflow.nodes.find(n => n.name === "Arbiter v2");

// Modify weighted fusion logic
arbiterNode.parameters.jsCode = `
  const items = $input.all();
  const branches = items[0].json.branch_results;

  // v2.0.0 Weighted fusion
  const WEIGHTS = {
    A: 0.30,  // Heuristics
    B: 0.35,  // Semantic
    C: 0.35   // LLM Guard
  };

  // Calculate weighted score
  const weightedScore =
    (branches.A.score || 0) * WEIGHTS.A +
    (branches.B.score || 0) * WEIGHTS.B +
    (branches.C.score || 0) * WEIGHTS.C;

  // Critical signal override
  const criticalOverride =
    branches.A.critical_signals?.obfuscation_heavy ||
    branches.C.critical_signals?.llm_attack;

  // Decision matrix
  let decision;
  if (criticalOverride || weightedScore >= 85) {
    decision = 'BLOCK';
  } else if (weightedScore >= 30) {
    decision = 'SANITIZE';
  } else {
    decision = 'ALLOW';
  }

  return [{
    json: {
      ...items[0].json,
      threat_score: weightedScore,
      arbiter_decision: decision,
      critical_override: criticalOverride
    }
  }];
`;
```

### Task 3: Add New Node

**Example: Add post-processing step**

```javascript
// 1. Create new node
const newNode = {
  "parameters": {
    "jsCode": `
      const items = $input.all();
      // Your processing logic
      return items.map((item, index) => ({
        json: {
          ...item.json,
          processed: true
        },
        pairedItem: { item: index }
      }));
    `
  },
  "id": crypto.randomUUID(),
  "name": "Post_Processing",
  "type": "n8n-nodes-base.code",
  "typeVersion": 2,
  "position": [1500, 300]
};

// 2. Insert into nodes array
workflow.nodes.push(newNode);

// 3. Update connections
// Find where to insert (after Arbiter Decision, before Clean Output)
workflow.connections["Arbiter Decision"].main[0][0].node = "Post_Processing";
workflow.connections["Post_Processing"] = {
  "main": [[{ "node": "Clean Output v2", "type": "main", "index": 0 }]]
};

// 4. Save and tell user to import
```

### Task 4: Migrate from v1.x to v2.0.0

**Migration Checklist:**

```javascript
// 1. Update workflow name
workflow.name = "Vigil Guard v2.0.0";

// 2. Replace 40-node sequential with 24-node parallel
// - Remove all sequential pattern matching nodes
// - Add 3-Branch Executor
// - Add Arbiter v2

// 3. Remove rules.config.json references
// - Pattern matching now in heuristics-service
// - Categories in unified_config.json

// 4. Update ClickHouse logging
const loggingNode = workflow.nodes.find(n => n.name.includes("NDJSON"));
loggingNode.parameters.jsCode = loggingNode.parameters.jsCode
  .replace(/"pipeline_version": "1\.\d+\.\d+"/, '"pipeline_version": "2.0.0"')
  + `
  // v2.0.0: Add branch columns
  result.branch_a_score = items[0].json.branch_results?.A?.score || 0;
  result.branch_b_score = items[0].json.branch_results?.B?.score || 0;
  result.branch_c_score = items[0].json.branch_results?.C?.score || 0;
  result.arbiter_decision = items[0].json.arbiter_decision;
  result.branch_a_timing_ms = items[0].json.timing?.branch_a_ms || 0;
  result.branch_b_timing_ms = items[0].json.timing?.branch_b_ms || 0;
  result.branch_c_timing_ms = items[0].json.timing?.branch_c_ms || 0;
`;

// 5. Update workflow metadata
workflow.updatedAt = new Date().toISOString();
workflow.versionId = crypto.randomUUID();
```

## Code Node Patterns (v2.0.0)

### Pattern 1: Data Access

```javascript
// Get all input items
const items = $input.all();

// Access first item's JSON
const data = items[0].json;

// Access branch results (v2.0.0)
const branchA = data.branch_results?.A;
const branchB = data.branch_results?.B;
const branchC = data.branch_results?.C;
```

### Pattern 2: Returning Modified Data

```javascript
// Return modified items (preserves pairedItem for tracing)
return items.map((item, index) => ({
  json: {
    ...item.json,
    new_field: "value"
  },
  pairedItem: {
    item: index
  }
}));
```

### Pattern 3: Accessing Config Data

```javascript
// Config loaded via Merge node, available in all downstream Code nodes
const items = $input.all();
const contextItem = items[0];

// Access config sections (v2.0.0: unified_config.json)
const unified = contextItem.json.config;        // unified_config.json (303 lines)
const piiConfig = contextItem.json.pii;         // pii.conf (361 lines)

// Use config values
const allowMax = unified.thresholds?.allow_max || 29;
const sanitizeLight = unified.thresholds?.sanitize_light || 64;
```

### Pattern 4: Branch Result Handling

```javascript
// Handle degraded branches (timeout/error)
const branches = items[0].json.branch_results;

for (const [id, result] of Object.entries(branches)) {
  if (result.degraded) {
    console.log(`Branch ${id} degraded, using score 0`);
    result.score = 0;
  }
}

// Calculate weighted score
const score =
  branches.A.score * 0.30 +
  branches.B.score * 0.35 +
  branches.C.score * 0.35;
```

### Pattern 5: HTTP Request Error Handling

```javascript
try {
  const response = await fetch('http://heuristics-service:5005/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, request_id: requestId }),
    signal: AbortSignal.timeout(1000)  // 1 second timeout
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  return await response.json();
} catch (error) {
  console.error('Branch A error:', error.message);
  return { score: 0, degraded: true, error: error.message };
}
```

## Node Positioning (Visual Layout)

### Grid System
- **X-axis:** 0 (left) → 2000+ (right)
- **Y-axis:** 0 (top) → 1200+ (bottom)
- **Spacing:** 220 pixels between nodes horizontally
- **Vertical offset:** 100-150 pixels for parallel branches

### Example Layout (v2.0.0)

```javascript
// Sequential flow (left to right)
nodes[0].position = [240, 300];   // Webhook Trigger
nodes[1].position = [460, 300];   // Extract Input
nodes[2].position = [680, 300];   // Config Loader
nodes[3].position = [900, 300];   // Input Validator

// 3-Branch Executor (single node, handles parallel internally)
nodes[4].position = [1120, 300];  // 3-Branch Executor

// Post-branch processing
nodes[5].position = [1340, 300];  // Arbiter v2
nodes[6].position = [1560, 300];  // Arbiter Decision
```

## Connection Syntax

### Simple Connection (A → B)

```json
{
  "connections": {
    "Node_A": {
      "main": [
        [{ "node": "Node_B", "type": "main", "index": 0 }]
      ]
    }
  }
}
```

### Switch Node (Conditional - Arbiter Decision)

```json
{
  "connections": {
    "Arbiter Decision": {
      "main": [
        [{ "node": "Clean Output v2", "type": "main", "index": 0 }],
        [{ "node": "PII_Redactor_v2", "type": "main", "index": 0 }],
        [{ "node": "Block Response v2", "type": "main", "index": 0 }]
      ]
    }
  }
}
```

## Debugging Workflow Execution

### Common Error Patterns

**Error: Branch timeout**
```javascript
// Problem: Branch service takes too long
// Solution: Increase timeout or check service health

// Check service health
curl http://localhost:5005/health  // Heuristics
curl http://localhost:5006/health  // Semantic
curl http://localhost:8000/health  // LLM Guard
```

**Error: "Cannot read property 'branch_results' of undefined"**
```javascript
// Problem: 3-Branch Executor didn't return results
// Solution: Check branch node output and add fallback

const branches = items[0].json.branch_results || {
  A: { score: 0, degraded: true },
  B: { score: 0, degraded: true },
  C: { score: 0, degraded: true }
};
```

### Enable Debug Logging

```javascript
// Add to Code nodes for debugging
console.log('=== Node Name Debug ===');
console.log('Input:', JSON.stringify($input.all(), null, 2));
console.log('Branch Results:', JSON.stringify(items[0].json.branch_results, null, 2));
console.log('Arbiter Decision:', items[0].json.arbiter_decision);
```

**View Logs:**
```bash
docker logs vigil-n8n | grep "Debug"
```

## Performance Optimization

### Parallel Branch Execution

```javascript
// 3-Branch Executor uses Promise.allSettled for parallel execution
// Each branch runs independently, no blocking

const [branchA, branchB, branchC] = await Promise.allSettled([
  fetchBranchA(text),
  fetchBranchB(text),
  fetchBranchC(text)
]);

// All branches complete in max(timeoutA, timeoutB, timeoutC)
// Not sequential: timeoutA + timeoutB + timeoutC
```

### Cache Config Data

```javascript
// Config loaded once at start, reused in all nodes
const config = $('Config_Loader_v2').all()[0].json.config;
// Don't reload in every node
```

## Integration with Other Skills

### When to Use Other Skills

**`n8n-vigil-workflow`:**
- Understanding 3-branch detection logic
- Modifying decision thresholds
- PII detection configuration
- Business logic changes

**`pattern-library-manager`:**
- Adding detection patterns (heuristics-service)
- ReDoS validation

**`vigil-testing-e2e`:**
- Writing tests for modified workflow
- Validating arbiter decisions
- Testing branch behavior

**`clickhouse-grafana-monitoring`:**
- Verifying workflow logs branch columns correctly
- Analyzing branch metrics

## Reference Files

### Workflow
- **Current**: `services/workflow/workflows/Vigil Guard v2.0.0.json`
- **Backups**: `services/workflow/workflows/backups/`

### Configuration
- `services/workflow/config/unified_config.json` (303 lines, v5.0.0)
- `services/workflow/config/pii.conf` (361 lines)

### Documentation
- Architecture: `docs/ARCHITECTURE.md`
- n8n docs: https://docs.n8n.io/

## Quick Reference

### Essential Commands

```bash
# View workflow structure
cat services/workflow/workflows/Vigil*.json | jq .

# Count nodes (expected: 24)
jq '.nodes | length' services/workflow/workflows/Vigil*.json

# List node names
jq -r '.nodes[].name' services/workflow/workflows/Vigil*.json

# Find 3-Branch Executor
jq '.nodes[] | select(.name | contains("Branch"))' services/workflow/workflows/Vigil*.json

# Extract Arbiter v2 code
jq -r '.nodes[] | select(.name == "Arbiter v2") | .parameters.jsCode' services/workflow/workflows/Vigil*.json
```

### Node Checklist (Before Commit)

- [ ] Node has unique `id` (UUID)
- [ ] Node has valid `type` (n8n-nodes-base.*)
- [ ] Node has `position` [x, y]
- [ ] Node has incoming connection (or is trigger)
- [ ] Node has outgoing connection (or is terminal)
- [ ] Code node JavaScript is syntactically valid
- [ ] pairedItem preserved in return statements
- [ ] Error handling implemented (try/catch)
- [ ] Branch degradation handled (score=0 on timeout)
- [ ] Workflow `updatedAt` timestamp updated
- [ ] User instructed: "Import to n8n NOW!"

---

**Last Updated:** 2025-12-09
**Workflow Version:** v2.0.0 (24 nodes, 3-branch parallel)
**Maintained By:** Vigil Guard Development Team

## Version History

- **v2.0.0** (Current): 24 nodes, 3-branch parallel, Arbiter v2
- **v1.7.0**: 41 nodes, sequential pipeline
- **v1.6.11**: 40 nodes, rules.config.json (DEPRECATED)
