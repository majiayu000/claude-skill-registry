---
name: background-process-get-process-output
description: "To read logs from a managed background process, fetch recent output (head or tail) for a process so you can inspect its stdout/stderr."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"backgroundProcess","tool_name":"get_process_output","arguments":{}}
```

## Tool Description
Gets the recent output for a background process. Can specify `head` or `tail`.

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object",
  "properties": {
    "processId": {
      "type": "string",
      "format": "uuid"
    },
    "head": {
      "type": "number"
    },
    "tail": {
      "type": "number"
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
