---
name: background-process-stop-process
description: "To stop a managed background task, terminate a running process by ID to shut it down cleanly."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"backgroundProcess","tool_name":"stop_process","arguments":{}}
```

## Tool Description
Stops a running background process.

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object",
  "properties": {
    "processId": {
      "type": "string",
      "format": "uuid"
    }
  },
  "required": [
    "processId"
  ],
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"backgroundProcess","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
