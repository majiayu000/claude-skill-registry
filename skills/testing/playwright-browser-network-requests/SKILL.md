---
name: playwright-browser-network-requests
description: "To inspect network activity since page load, list network requests to review API calls and resources."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"playwright","tool_name":"browser_network_requests","arguments":{}}
```

## Tool Description
Returns all network requests since loading the page

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object",
  "properties": {
    "includeStatic": {
      "type": "boolean",
      "default": false,
      "description": "Whether to include successful static resources like images, fonts, scripts, etc. Defaults to false."
    }
  },
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"playwright","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
