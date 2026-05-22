---
name: mcp-server-evaluations
description: Evaluate MCP servers for quality and reliability. Verify tool functionality, test error handling, generate tests, and assess response quality with no dependencies other than curl. Use this when validating MCP server implementations, testing OpenAPI-to-MCP conversions, or assessing API tool quality.
license: MIT
compatibility: Requires curl, jq, bun or node v22+
metadata:
  author: mcp.com.ai agent-skills
  version: "0.1.0"
allowed-tools: Bash(curl:*) Bash(jq:*) Read Node(bun:*) Node(node:*)
---

# MCP Server Evaluations Skill

Systematically evaluate MCP servers to ensure they function correctly, handle errors gracefully, and meet quality standards.

## Workflow

### Phase 1: Environment Verification

1. **Verify MCP server is running**
   ```bash
   curl -s http://localhost:3030/health
   # Expected: 200 OK
   
   curl -s -X POST http://localhost:3030/mcp \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","id":1,"method":"ping"}'
   # Expected: {"jsonrpc":"2.0","id":1,"result":{}}
   ```

### Phase 2: Tool Discovery

1. **List all available tools**
   ```bash
   curl -X POST http://localhost:3030/mcp \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
   ```

2. **Verify tool completeness**
   - [ ] All OpenAPI operations exposed as tools
   - [ ] Tool names follow consistent convention (e.g., `getUsers`, `createOrder`)
   - [ ] Descriptions are clear and actionable
   - [ ] Required vs optional parameters clearly marked
   - [ ] Parameter types match OpenAPI schema

3. **Document discovered tools** — Create inventory of tools for systematic testing.

### Phase 3: Functional Testing

For each discovered tool:

1. **Basic functionality test**
   ```bash
   curl -X POST http://localhost:3030/mcp \
     -H "Content-Type: application/json" \
     -d '{
       "jsonrpc": "2.0",
       "method": "tools/call",
       "params": {
         "name": "<tool_name>",
         "arguments": { <valid_arguments> }
       },
       "id": 2
     }'
   ```

2. **Verify response structure**
   - [ ] Response contains expected data
   - [ ] Data types match schema
   - [ ] No unexpected null values
   - [ ] Pagination works (if applicable)

3. **Error handling test** — Call with invalid/missing arguments:
   ```bash
   curl -X POST http://localhost:3030/mcp \
     -H "Content-Type: application/json" \
     -d '{
       "jsonrpc": "2.0",
       "method": "tools/call",
       "params": {
         "name": "<tool_name>",
         "arguments": {}
       },
       "id": 3
     }'
   ```

4. **Verify error response quality**
   - [ ] Error message is actionable
   - [ ] Missing required parameters identified
   - [ ] HTTP status codes propagated correctly

### Phase 4: Question-Based Evaluation

Generate and test with realistic user questions:

1. **Generate 10+ test questions** covering:
   - Simple single-tool queries
   - Multi-step workflows requiring multiple tools
   - Edge cases (empty results, large datasets)
   - Error scenarios (invalid IDs, unauthorized access)

2. **Execute each question** through MCP client or Inspector

3. **Score responses** using evaluation criteria:
   - **Correctness**: Does the answer match expected result?
   - **Completeness**: Is all relevant information included?
   - **Clarity**: Is the response well-structured?
   - **Performance**: Response time within acceptable limits?

### Phase 5: Quality Scoring

Calculate overall quality score:

| Category | Weight | Criteria |
|----------|--------|----------|
| Tool Discovery | 20% | All operations exposed, proper naming |
| Basic Functionality | 30% | Valid inputs return correct responses |
| Error Handling | 20% | Graceful errors with actionable messages |
| Question Accuracy | 20% | Test questions answered correctly |
| Performance | 10% | Response times < 5s for standard ops |

**Pass threshold**: 80% overall score

## Quick Evaluation Checklist

Run this minimal check for fast validation:

```bash
# 1. Health check
curl -s http://localhost:3030/health | grep -q "" && echo "✓ Health OK" || echo "✗ Health FAILED"

# 2. MCP ping
curl -s -X POST http://localhost:3030/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"ping"}' | jq -e '.jsonrpc == "2.0" and .result' > /dev/null && echo "✓ Ping OK" || echo "✗ Ping FAILED"

# 3. Tools list
curl -s -X POST http://localhost:3030/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' | jq '.result.tools | length' | xargs -I {} echo "✓ {} tools discovered"

# 4. Sample tool call (adjust tool name and args)
curl -s -X POST http://localhost:3030/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"listPets","arguments":{}},"id":2}' | jq '.result' > /dev/null && echo "✓ Tool call OK" || echo "✗ Tool call FAILED"
```

## Test Question Templates

Use these patterns to generate effective test questions:

1. **List/Query**: "Show me all [resources] that match [criteria]"
2. **Get Details**: "What are the details of [resource] with ID [id]?"
3. **Create**: "Create a new [resource] with [properties]"
4. **Update**: "Update [resource] [id] to change [field] to [value]"
5. **Delete**: "Remove [resource] with ID [id]"
6. **Aggregate**: "How many [resources] exist with [status]?"
7. **Search**: "Find [resources] where [field] contains [term]"
8. **Workflow**: "Create a [resource], then update it, then list all"

## References

For detailed documentation:
- [references/mcp-inspector-guide.md](references/mcp-inspector-guide.md) — Inspector setup & usage
- [references/evaluation-criteria.md](references/evaluation-criteria.md) — Quality metrics & scoring
- [references/question-templates.md](references/question-templates.md) — Test question generation

## Example: Petstore API Evaluation

```bash
# 1. Run health checks
curl -s http://localhost:3030/health
curl -s -X POST http://localhost:3030/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"ping"}' | jq -e '.jsonrpc == "2.0" and .result' > /dev/null && echo "✓ Ping OK" || echo "✗ Ping FAILED"

# 2. Tool discovery
curl -s -X POST http://localhost:3030/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' | jq '.result.tools'

# 3. Test questions:
# - "List all available pets"
# - "Show details of pet with ID 1"
# - "Find pets with status 'available'"
# - "Create a new pet named 'Fluffy'"
```
