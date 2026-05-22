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
  "type": "object",
  "properties": {
    "time": {
      "type": "number",
      "description": "The time to wait in seconds"
    },
    "text": {
      "type": "string",
      "description": "The text to wait for"
    },
    "textGone": {
      "type": "string",
      "description": "The text to wait for to disappear"
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
