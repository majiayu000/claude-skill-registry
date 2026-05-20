---
name: node-ops
cluster: distributed-comms
description: "Node pairing: approve/reject, nodes run/invoke, screen_record, camera_snap, location, System76 mgmt"
tags: ["nodes","pairing","system76","screen","camera"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "node pairing approve run invoke screen camera location system76"
---

# node-ops

## Purpose
This skill handles node operations in a distributed communications setup, focusing on pairing nodes (approve/reject), executing commands, and managing hardware like screen recording, camera snapshots, location tracking, and System76 device management. It's designed for secure, cluster-based interactions in environments like distributed-comms.

## When to Use
Use this skill when setting up or managing node pairs in a cluster, such as approving new nodes for communication, invoking remote commands, or accessing device features. Apply it in scenarios involving IoT devices, remote monitoring, or System76 hardware integration, like fleet management or real-time data capture.

## Key Capabilities
- Approve or reject node pairings via authenticated requests.
- Invoke or run commands on paired nodes, supporting asynchronous execution.
- Record screen sessions or take camera snapshots on target nodes.
- Retrieve location data from nodes, using GPS or network-based methods.
- Manage System76 devices, including firmware updates and hardware diagnostics.
- Handle secure communications within the distributed-comms cluster, with encryption for all operations.

## Usage Patterns
Always authenticate using the `$NODE_OPS_API_KEY` environment variable before operations. Start with pairing nodes, then proceed to commands or hardware access. Use CLI for quick tasks or API for programmatic integration. For example, check node status first, then execute actions. In code, import the skill as a module and call methods with required parameters; in scripts, pipe outputs for chaining commands.

## Common Commands/API
Use the CLI tool `node-ops` or the REST API at `https://api.distributed-comms.com/v1/node-ops`. Authentication requires setting `$NODE_OPS_API_KEY` in your environment.

- CLI for pairing: `node-ops pair approve --node-id 123 --reason "Verified"`. Reject with: `node-ops pair reject --node-id 123 --reason "Unauthorized"`.
- CLI for running commands: `node-ops run --node-id 123 --command "ls -la" --async`. Example output: JSON with command status.
- API endpoint for screen recording: POST /api/screen_record with body: `{"node_id": "123", "duration": 30}`. Response: 200 OK with recording URL.
- API for camera snapshot: GET /api/camera_snap?node_id=123. Requires headers: `Authorization: Bearer $NODE_OPS_API_KEY`.
- Code snippet for invoking a command:
  ```javascript
  const nodeOps = require('node-ops-sdk');
  nodeOps.invoke({ nodeId: '123', command: 'echo Hello' })
    .then(result => console.log(result));
  ```
- Code snippet for location retrieval:
  ```python
  import node_ops
  location = node_ops.get_location(node_id='123')
  print(location)  # Returns dict: {'lat': 37.7749, 'lon': -122.4194}
  ```
- Config format: Use JSON files for node profiles, e.g., `{"node_id": "123", "pair_status": "approved", "api_key": "$NODE_OPS_API_KEY"}`.

## Integration Notes
Integrate by setting `$NODE_OPS_API_KEY` as an environment variable in your application. For cluster interactions, ensure your code references the distributed-comms endpoint. Use SDKs like `node-ops-sdk` for Node.js or Python wrappers. When combining with other skills, handle cross-cluster calls by prefixing with the cluster ID, e.g., `distributed-comms:node-ops run ...`. Avoid hardcoding keys; use secure vaults or env files.

## Error Handling
Common errors include authentication failures (HTTP 401), node not found (404), or command timeouts. Check response codes and handle with try-catch blocks. For CLI, parse errors with `--verbose` flag. Example: If pairing fails, retry after checking `$NODE_OPS_API_KEY`. In code:
  ```javascript
  try {
    await nodeOps.pairApprove({ nodeId: '123' });
  } catch (error) {
    if (error.code === 'AUTH_ERROR') console.error('Invalid API key');
  }
  ```
Log detailed errors using the skill's built-in logging, enabled via `--debug` flag.

## Graph Relationships
This skill relates to: distributed-comms cluster (parent), skills with tags: nodes (peers), pairing (related), system76 (dependent), screen and camera (integrated hardware features). Connections: Uses distributed-comms for node discovery; shares data with system76 management skills.
