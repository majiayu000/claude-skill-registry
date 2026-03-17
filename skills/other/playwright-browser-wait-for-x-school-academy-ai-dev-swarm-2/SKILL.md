---
name: playwright-browser-wait-for
description: "To wait for page state changes, wait for text to appear or disappear or for a timeout."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"playwright","tool_name":"browser_wait_for","arguments":{}}
```

## Tool Description
Wait for text to appear or disappear or a specified time to pass

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "time": {
      "description": "The time to wait in seconds",
      "type": "number"
    },
    "text": {
      "description": "The text to wait for",
      "type": "string"
    },
    "textGone": {
      "description": "The text to wait for to disappear",
      "type": "string"
    }
  },
  "additionalProperties": false
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"playwright","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
