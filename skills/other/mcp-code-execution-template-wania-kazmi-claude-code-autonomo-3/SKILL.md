---
name: mcp-code-execution-template
description: |
  Template skill demonstrating the MCP Code Execution pattern for 98%+ token efficiency.
  Use this as a reference when creating skills that interact with MCP servers.
  Triggers: mcp, code execution, token efficient, tool wrapper, external api
author: Claude Code
version: 1.0.0
mcp-pattern: code-execution
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# MCP Code Execution Template

This skill demonstrates how to build token-efficient skills that interact with MCP servers using the Code Execution pattern instead of direct tool calls.

## Why This Pattern?

| Approach | Token Usage | Problem |
|----------|-------------|---------|
| Direct Tool Calls | 50,000+ per operation | All data flows through model context |
| Code Execution | ~100 per operation | Data processed outside context |

**Savings: 98%+**

## Directory Structure

```
mcp-code-execution-template/
├── SKILL.md              # This file (~100 tokens loaded)
├── servers/              # MCP tool wrappers (loaded on-demand)
│   ├── mcp-client.ts     # Base MCP client
│   └── example-server/   # Example server wrapper
│       ├── index.ts
│       └── exampleTool.ts
├── scripts/
│   └── execute.ts        # Execution helper
└── workspace/            # Intermediate files (not in context)
```

## How to Use This Template

### Step 1: Create Tool Wrappers

For each MCP server you need, create a directory in `./servers/`:

```typescript
// ./servers/{server-name}/{tool}.ts
import { callMCPTool } from '../mcp-client';

interface ToolInput {
  param1: string;
  param2?: number;
}

interface ToolOutput {
  result: any;
}

export async function toolName(input: ToolInput): Promise<ToolOutput> {
  return callMCPTool<ToolOutput>('{server}__{tool}', input);
}
```

### Step 2: Discover Tools Progressively

Don't load all tools upfront. Explore the filesystem:

```bash
# List available servers
ls ./servers/

# List tools in a server
ls ./servers/{server-name}/

# Read only the tool you need
cat ./servers/{server-name}/{tool}.ts
```

### Step 3: Write Execution Code

Write code that runs in the execution environment:

```typescript
import * as server from './servers/{server-name}';

async function main() {
  // 1. Call MCP tools (data stays in execution env)
  const rawData = await server.fetchLargeData({ id: 'abc' });

  // 2. Process/filter in execution environment
  const filtered = rawData.items.filter(item => item.active);
  const summary = {
    total: rawData.items.length,
    active: filtered.length,
    sample: filtered.slice(0, 3)
  };

  // 3. Return ONLY summary to model
  console.log(JSON.stringify(summary, null, 2));
}

main();
```

### Step 4: Execute Outside Context

Run the code so data never enters model context:

```bash
npx ts-node ./workspace/task.ts
# OR
python ./scripts/execute.py ./workspace/task.ts
```

## Example: Processing Large Spreadsheet

**Task**: Find all overdue invoices in a 10,000 row spreadsheet

**Wrong Way (Direct Tool Calls):**
```
TOOL: sheets.getSpreadsheet(id: 'abc')
→ Returns 10,000 rows = 100,000 tokens
Model processes all rows manually = expensive
```

**Right Way (Code Execution):**
```typescript
// ./workspace/find-overdue.ts
import * as sheets from './servers/google-sheets';

async function main() {
  const data = await sheets.getSpreadsheet({ id: 'abc' });

  const today = new Date();
  const overdue = data.rows.filter(row => {
    const dueDate = new Date(row.dueDate);
    return dueDate < today && row.status !== 'paid';
  });

  console.log(`Found ${overdue.length} overdue invoices`);
  console.log('Top 5 by amount:');
  overdue
    .sort((a, b) => b.amount - a.amount)
    .slice(0, 5)
    .forEach(inv => {
      console.log(`  ${inv.invoiceId}: $${inv.amount} (due: ${inv.dueDate})`);
    });
}

main();
```

**Result**: Model sees ~20 lines of output instead of 10,000 rows.

## Validation Checklist

When creating MCP-enabled skills, verify:

- [ ] Tool definitions are in separate files (progressive disclosure)
- [ ] Code runs in execution environment, not model context
- [ ] Large data is filtered/aggregated before returning
- [ ] Only summaries and samples are logged/returned
- [ ] Workspace directory used for intermediate files
- [ ] Token usage < 500 for typical operations

## When NOT to Use Code Execution

Use direct tool calls when:
- Fetching a single small value (< 100 tokens)
- Interactive debugging where you need to see intermediate steps
- The overhead of writing code exceeds the token savings
