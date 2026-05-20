---
name: create-docker-container
description: Add a Docker container to a Datagrok package with Dockerfile, config, and HTTP/WebSocket access
---

# Create Docker Container

Help the user add a Docker container to their Datagrok package so it can be built, deployed, and accessed via the platform.

## Usage
```
/create-docker-container [package-name]
```

## Instructions

Follow these steps to create a Docker container for a Datagrok package:

### 1. Create the Dockerfile

Create a `dockerfiles/` folder inside the package root and add a `Dockerfile` there.

- The container MUST expose exactly one port using `EXPOSE $PORT` (only one EXPOSE is allowed).
- The application inside the container MUST embed an HTTP server listening on that port.
- Follow Docker best practices: minimal base images, multi-stage builds, small layers.

Example structure:
```
packages/MyPackage/
  dockerfiles/
    Dockerfile
    container.json   (optional)
  src/
  package.json
```

### 2. Create container.json (optional)

Place `container.json` in the same directory as the `Dockerfile`. If omitted, defaults are used.

```json
{
  "cpu": 1.5,
  "gpu": 1,
  "memory": 2048,
  "on_demand": true,
  "shutdown_timeout": 60,
  "storage": 25,
  "env": {
    "CONN": "#{x.Package:Entity}",
    "LOGIN": "login"
  }
}
```

Configuration properties and defaults:

| Property           | Type    | Default | Description                                              |
|--------------------|---------|---------|----------------------------------------------------------|
| cpu                | Double  | 0.25    | CPU cores allocated                                      |
| gpu                | Integer | 0       | GPU devices reserved                                     |
| memory             | Integer | 512     | RAM in megabytes                                         |
| on_demand          | Boolean | false   | Start container only on first request                    |
| shutdown_timeout   | Integer | null    | Idle minutes before auto-shutdown                        |
| storage            | Integer | 21      | Disk storage in gigabytes                                |
| shm_size           | Integer | 64      | Shared memory in megabytes                               |
| env                | Object  |         | Environment variables passed to the container            |

For env values, use `#{x.Package:Entity}` to pass a JSON-serialized entity from a package namespace. Credentials are only passed for connections within the same package.

### 3. Implement HTTP request access

Get the container ID and use `fetchProxy` to call the container's HTTP server:

```typescript
const containerId = (await grok.dapi.docker.dockerContainers.filter('my-container').first()).id;

const params = {
  method: 'POST',
  headers: {'Accept': 'application/json', 'Content-Type': 'application/json'},
  body: JSON.stringify(payload),
};
const response: Response = await grok.dapi.docker.dockerContainers.fetchProxy(containerId, '/endpoint', params);
const result = await response.json();
```

The `params` object follows the standard [RequestInit](https://developer.mozilla.org/en-US/docs/Web/API/RequestInit) interface.

### 4. Implement WebSocket access (if needed)

```typescript
const ws: WebSocket = await grok.dapi.docker.dockerContainers.webSocketProxy(container.id, '/ws');
ws.send('Hello');

ws.addEventListener('message', (event: MessageEvent) => {
  console.log(event.data);
});

setTimeout(() => ws.close(), 3000);
```

### 5. Build and publish

```shell
webpack
grok publish dev
```

A return code of 0 indicates successful deployment. After publishing, Datagrok queues the image for building automatically.

### 6. Monitor status

In Datagrok, go to Platform -> Dockers to view containers and images. Status indicators:
- Green dot: running/ready
- Red dot: error
- Blinking grey dot: pending (starting, stopping, or rebuilding)
- No dot: stopped

Right-click a card to start/stop containers or rebuild images. Check logs via the Property pane.

## Behavior

- Ask the user for the package name and what service the container will run.
- Create the `dockerfiles/` directory, `Dockerfile`, and optionally `container.json`.
- If the user needs HTTP access, generate a TypeScript helper function using `fetchProxy`.
- If the user needs WebSocket access, generate a helper using `webSocketProxy`.
- Remind the user that only one `EXPOSE` port is allowed in the Dockerfile.
- Remind the user that `grok-spawner` must be running in the same environment.
- Follow project coding conventions: no excessive comments, prefer for-in loops, catch/else if on new lines.
