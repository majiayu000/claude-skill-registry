---
name: node-red
description: Edit, analyze, and create Node-RED flows by working with flows.json files, understanding node types, and applying Node-RED best practices. Use when the user mentions Node-RED, flows.json, flow development, or needs to modify Node-RED configurations.
---

# Node-RED Flow Development

This skill provides comprehensive support for Node-RED development, including flow creation, modification, validation, and deployment through the Admin API.

## When to Use This Skill

Use this skill when:
- Creating or modifying Node-RED flows (flows.json files)
- Building MQTT, HTTP API, or data pipeline integrations
- Debugging or validating flow configurations
- Working with function nodes and context storage
- Deploying flows via the Node-RED Admin API
- Converting requirements into Node-RED flow implementations

## Available Resources

### Scripts (scripts/)

Execute these Python scripts for common Node-RED operations:

- **generate_uuid.py** - Generate valid Node-RED node IDs
  ```bash
  python scripts/generate_uuid.py [count]
  ```

- **validate_flow.py** - Validate flow JSON structure and wire connections
  ```bash
  python scripts/validate_flow.py <flow.json>
  ```

- **wire_nodes.py** - Connect nodes programmatically
  ```bash
  python scripts/wire_nodes.py <flow.json> <source_id> <target_id> [output_port]
  ```

- **create_flow_template.py** - Generate boilerplate flows
  ```bash
  python scripts/create_flow_template.py <mqtt|http-api|data-pipeline|error-handler> [output.json]
  ```

### References (references/)

Consult these detailed references as needed:

- **node_schemas.md** - Complete schemas for all Node-RED node types
- **api_reference.md** - Node-RED Admin API documentation with examples
- **function_snippets.md** - Reusable function node code patterns

### Assets (assets/)

Use these templates and boilerplate files:

- **templates/mqtt_flow.json** - Complete MQTT pub/sub flow with error handling
- **templates/http_api_flow.json** - REST API with CRUD operations and authentication
- **boilerplate/function_async.js** - Async function node patterns
- **boilerplate/function_context.js** - Context storage examples

## Core Workflow

### Creating a New Flow

1. Determine the flow type needed (MQTT, HTTP API, data processing, etc.)
2. Generate a template using `scripts/create_flow_template.py`
3. Modify the template to match requirements
4. Validate the flow using `scripts/validate_flow.py`
5. Deploy via Admin API or save as flows.json

### Modifying Existing Flows

1. Read and parse the flows.json file
2. Identify nodes by type and ID
3. Make modifications while preserving:
   - Wire connections (arrays of node IDs)
   - Tab references (`z` property)
   - Node coordinates (`x`, `y`)
4. Validate changes before saving
5. Use `scripts/wire_nodes.py` to connect nodes if needed

### Working with Function Nodes

For function nodes, reference:
- `assets/boilerplate/function_async.js` for async operations
- `assets/boilerplate/function_context.js` for context storage
- `references/function_snippets.md` for specific patterns

Available objects in function nodes:
- `msg` - Message object
- `node` - Node API (send, done, error, warn, log, status)
- `context` - Node-scoped storage
- `flow` - Flow-scoped storage
- `global` - Global storage
- `RED` - Runtime API
- `env` - Environment variables

### Deploying Flows

To deploy flows via the Admin API:

1. Retrieve current configuration:
   ```bash
   GET /flows
   ```

2. Modify the configuration as needed

3. Deploy with appropriate deployment type:
   ```bash
   POST /flows
   Headers: Node-RED-Deployment-Type: full|nodes|flows|reload
   ```

4. Verify deployment success

## Common Patterns

### Message Flow Structure

Every Node-RED message follows this pattern:
- Primary data in `msg.payload`
- Topic/category in `msg.topic`
- Unique ID in `msg._msgid`
- Additional properties as needed

### Error Handling

Implement error handling using:
1. Try-catch blocks in function nodes
2. Catch nodes to intercept errors
3. Status nodes to monitor node states
4. Dedicated error output wires

### Environment Variables

Use environment variables for configuration:
- In node properties: `$(ENV_VAR_NAME)`
- In function nodes: `env.get("ENV_VAR_NAME")`
- Via Docker: `-e KEY=value`

### Context Storage Levels

Choose appropriate context level:
- **Node context**: Local to single node
- **Flow context**: Shared within flow/tab
- **Global context**: System-wide sharing
- **Persistent**: Survives restarts (configure in settings.js)

## Validation Checklist

Before deploying flows, verify:
- [ ] JSON syntax is valid
- [ ] All wire connections reference existing node IDs
- [ ] Tab references (`z` property) are correct
- [ ] Function node JavaScript is syntactically valid
- [ ] Required configuration nodes exist (MQTT brokers, etc.)
- [ ] Environment variables are properly referenced
- [ ] Error handling is implemented

## Quick Commands

Generate five Node-RED UUIDs:
```bash
python scripts/generate_uuid.py 5
```

Create an MQTT flow template:
```bash
python scripts/create_flow_template.py mqtt my-mqtt-flow.json
```

Validate a flow file:
```bash
python scripts/validate_flow.py flows.json
```

Wire two nodes together:
```bash
python scripts/wire_nodes.py flows.json inject-node-id debug-node-id
```

## Node-RED Configuration

### Default File Locations
- Flows: `~/.node-red/flows_<hostname>.json`
- Settings: `~/.node-red/settings.js`
- Custom nodes: `~/.node-red/node_modules/`

### Running Node-RED
- Normal mode: `node-red`
- Safe mode (no flow execution): `node-red --safe`
- Custom flow file: `node-red myflows.json`

## Best Practices

1. **Use appropriate node types**: Prefer change nodes over function nodes for simple transformations
2. **Implement error handling**: Always include catch nodes for critical paths
3. **Document flows**: Use comment nodes and node descriptions
4. **Organize with tabs**: Separate flows by logical function or system
5. **Version control**: Store flows.json in git with meaningful commit messages
6. **Test incrementally**: Deploy and test small changes frequently
7. **Monitor performance**: Use status nodes and debug output wisely

## Troubleshooting

For common issues:
- **Invalid JSON**: Use `scripts/validate_flow.py` to find syntax errors
- **Broken wires**: Check that all wired node IDs exist
- **Missing configurations**: Ensure broker/server configs are included
- **Function errors**: Test JavaScript in isolation first
- **API deployment fails**: Verify authentication and check revision conflicts

## Additional Resources

For detailed specifications and examples:
- Consult `references/node_schemas.md` for node property details
- Review `references/api_reference.md` for API operations
- Use `references/function_snippets.md` for tested code patterns
- Copy templates from `assets/templates/` as starting points