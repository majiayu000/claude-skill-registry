---
name: playwright-browser-resize
description: "To resize the browser window, change viewport size to test responsive layouts."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"playwright","tool_name":"browser_resize","arguments":{}}
```

## Tool Description
Resize the browser window

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "width": {
      "type": "number",
      "description": "Width of the browser window"
    },
    "height": {
      "type": "number",
      "description": "Height of the browser window"
    }
  },
  "required": [
    "width",
    "height"
  ],
  "additionalProperties": false
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"playwright","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
