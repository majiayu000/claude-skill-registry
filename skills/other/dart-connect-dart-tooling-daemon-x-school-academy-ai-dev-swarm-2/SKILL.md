---
name: dart-connect-dart-tooling-daemon
description: "To connect to the Dart Tooling Daemon for editor/runtime data, connect using a user-provided DTD URI before using related Dart tools."
---

## Usage
Use the MCP tool `dev-swarm.request` to send the payload as a JSON string:

```json
{"server_id":"dart","tool_name":"connect_dart_tooling_daemon","arguments":{}}
```

## Tool Description
Connects to the Dart Tooling Daemon. You should get the uri either from available tools or the user, do not just make up a random URI to pass. When asking the user for the uri, you should suggest the "Copy DTD Uri to clipboard" action. When reconnecting after losing a connection, always request a new uri first.

## Arguments Schema
The schema below describes the `arguments` object in the request payload.
```json
{
  "type": "object",
  "properties": {
    "uri": {
      "type": "string"
    }
  },
  "required": [
    "uri"
  ]
}
```

## Background Tasks
If the tool returns a task id, poll the task status via the MCP request tool:

```json
{"server_id":"dart","method":"tasks/status","params":{"task_id":"<task_id>"}}
```
