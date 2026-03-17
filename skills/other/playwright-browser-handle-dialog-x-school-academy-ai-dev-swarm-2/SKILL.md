---
name: playwright-browser-handle-dialog
description: "To accept or dismiss browser dialogs like alert/confirm/prompt, handle the dialog so automation can continue."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"playwright","tool_name":"browser_handle_dialog","arguments":{}}
```

## Tool Description
Handle a dialog

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "accept": {
      "type": "boolean",
      "description": "Whether to accept the dialog."
    },
    "promptText": {
      "description": "The text of the prompt in case of a prompt dialog.",
      "type": "string"
    }
  },
  "required": [
    "accept"
  ],
  "additionalProperties": false
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"playwright","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
