---
name: iot-protocols
cluster: iot
description: "IoT protocols: Zigbee (mesh), Z-Wave (home), LoRaWAN (long-range), CoAP (lightweight), Matter (interoperable), Thread (I"
tags: ["iot","iot-protocols"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "iot-protocols iot"
---

# iot-protocols

## Purpose
This skill provides tools for interacting with IoT protocols like Zigbee, Z-Wave, LoRaWAN, CoAP, Matter, and Thread, enabling device connectivity, data exchange, and network management in IoT applications.

## When to Use
Use this skill when building IoT systems requiring low-power, mesh networking (e.g., Zigbee for smart homes), long-range communication (e.g., LoRaWAN for sensors in remote areas), or lightweight protocols (e.g., CoAP for constrained devices). Apply it in scenarios like smart home automation, industrial IoT monitoring, or interoperable ecosystems with Matter.

## Key Capabilities
- Establish connections to devices using specific protocols: e.g., Zigbee for mesh networks or Thread for IPv6-based low-power wireless.
- Send/receive data payloads: e.g., query sensor data via CoAP or control Z-Wave devices.
- Configure network settings: e.g., set up LoRaWAN gateways or Matter fabric bridges.
- Handle protocol-specific features: e.g., Zigbee's binding for device pairing or LoRaWAN's adaptive data rate.
- Interoperate across protocols: e.g., bridge Matter devices with Thread networks for seamless integration.

## Usage Patterns
To accomplish tasks, always authenticate first by setting the environment variable `export IOT_API_KEY=your_api_key`. Start with the `openclaw iot init` command to initialize the session, then use subcommands for protocol-specific actions. For example, to connect to a device, specify the protocol and device ID; for data operations, use query flags. Always include error checking in scripts. Pattern: `openclaw iot <subcommand> --protocol <protocol> --device-id <id>`. Use JSON config files for complex setups, e.g., create a file named `config.json` with `{ "protocol": "zigbee", "networkKey": "hex_key" }` and pass it via `--config config.json`.

## Common Commands/API
Use the OpenClaw CLI for quick interactions or REST APIs for programmatic access. Authentication requires the `$IOT_API_KEY` header.

- CLI Command: List protocols  
  `openclaw iot list --protocol zigbee`  
  This outputs available Zigbee devices; add `--verbose` for detailed network info.

- CLI Command: Connect to a device  
  `openclaw iot connect --protocol lorawan --device-id 456 --region EU868`  
  Use this to establish a LoRaWAN connection; specify region flag for frequency bands.

- API Endpoint: Send data via CoAP  
  POST /api/iot/send  
  Body: `{ "protocol": "coap", "endpoint": "/sensors/temp", "payload": "{\"temp\": 25}" }`  
  Include header: `Authorization: Bearer $IOT_API_KEY`

- API Endpoint: Query Z-Wave status  
  GET /api/iot/status?protocol=z-wave&device-id=789  
  Response: JSON object like `{ "status": "online", "nodes": 5 }`; handle with a simple fetch in code:  
  `fetch('/api/iot/status', { headers: { 'Authorization': process.env.IOT_API_KEY } }) .then(response => response.json())`

- Config Format: For Matter integration, use a YAML file:  
  `matter-config.yaml: protocol: matter, fabricId: 12345, nodeId: 678`  
  Load it with: `openclaw iot load-config --file matter-config.yaml`

## Integration Notes
Integrate this skill with other OpenClaw tools by referencing the `iot` cluster in your workflow. For external systems, export `$IOT_API_KEY` and use it in API calls. To combine with a database skill, pipe output: e.g., `openclaw iot get --protocol coap | openclaw db insert`. For Thread integration, ensure IPv6 compatibility in your network stack. Example: In a Node.js app, import OpenClaw SDK and call:  
`const openclaw = require('openclaw-sdk'); openclaw.iot.connect({ protocol: 'thread', deviceId: '101' });`  
Always validate inputs; for Zigbee, check mesh topology before connecting.

## Error Handling
Handle errors by checking CLI exit codes or API response status. Common errors include authentication failures (HTTP 401) or protocol mismatches (e.g., invalid Zigbee network key). Use try-catch in code:  
`try { await openclaw.iot.connect({ protocol: 'z-wave', deviceId: '202' }); } catch (error) { console.error(error.message); // e.g., "Device not found" }`  
For CLI, parse output: if `openclaw iot connect` returns non-zero, check stderr for messages like "Protocol not supported". Retry transient errors (e.g., LoRaWAN signal loss) with exponential backoff.

## Concrete Usage Examples
1. **Set up a Zigbee mesh network:** First, export your key: `export IOT_API_KEY=abc123`. Then, initialize: `openclaw iot init --protocol zigbee`. Connect devices: `openclaw iot connect --protocol zigbee --device-id 303 --pan-id 0x1a62`. Send a command to toggle a light: `openclaw iot send --protocol zigbee --endpoint /lights/1 --payload '{"state": "on"}'`. This establishes a mesh for home automation.

2. **Query data from a LoRaWAN sensor:** Authenticate via env var, then: `openclaw iot connect --protocol lorawan --device-id 404 --app-eui 70B3D57EF0000000`. Retrieve data: `openclaw iot get --protocol lorawan --payload-type temp`. In code:  
  `openclaw.iot.get({ protocol: 'lorawan', deviceId: '404' }).then(data => console.log(data));`  
  This is useful for monitoring remote environmental sensors.

## Graph Relationships
- Related to: iot-cluster (for broader IoT management), networking-skills (for protocol-agnostic networking).
- Depends on: security-skills (for encryption in protocols like Zigbee).
- Connected via: iot tag, allowing cross-skill queries in OpenClaw's graph.
