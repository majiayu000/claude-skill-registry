---
name: game-networking
cluster: game-dev
description: "Implements networking for multiplayer games, handling protocols, latency, and synchronization."
tags: ["multiplayer","networking","protocols"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "multiplayer networking game protocols latency synchronization"
---

# game-networking

## Purpose
This skill allows the AI to implement multiplayer game networking, managing protocols (e.g., UDP, TCP), minimizing latency, and ensuring game state synchronization for seamless player interactions.

## When to Use
Use this skill when building multiplayer games that require real-time communication, such as online shooters, MMOs, or cooperative adventures. Apply it for scenarios involving player synchronization, server-client architectures, or handling network interruptions in game loops.

## Key Capabilities
- Handles UDP for low-latency, unreliable data transmission and TCP for reliable, ordered delivery.
- Implements latency compensation via interpolation and prediction algorithms to smooth gameplay.
- Synchronizes game states using techniques like delta encoding and authoritative servers.
- Supports NAT traversal and peer-to-peer connections for reduced server dependency.
- Manages bandwidth optimization through packet compression and prioritization.

## Usage Patterns
To use this skill, first initialize a network context, then establish connections, send/receive data, and handle disconnections. Always wrap network operations in try-catch blocks for robustness. For example, in a game loop, check for incoming packets every frame and update game state accordingly. Use asynchronous patterns to avoid blocking the main thread. If authentication is needed, set the environment variable `$GAME_NETWORKING_API_KEY` before invoking commands.

## Common Commands/API
Interact via OpenClaw CLI or REST API. CLI commands require the skill to be activated first with `openclaw activate game-networking`.

- **CLI Commands:**
  - Initialize a network session: `openclaw game-networking init --protocol udp --port 5000 --key $GAME_NETWORKING_API_KEY`
    - Example: Sets up a UDP server on port 5000, requiring an API key.
  - Send a packet: `openclaw game-networking send --host 192.168.1.1 --data '{"player_pos": [10, 20]}'`
    - Flags: `--host` for target IP, `--data` for JSON payload.
  - Receive packets: `openclaw game-networking listen --timeout 5`
    - Listens for incoming data with a 5-second timeout.

- **API Endpoints:**
  - POST /api/network/connect: Establishes a connection; body: `{"protocol": "udp", "host": "localhost", "port": 5000}`
    - Requires header: `Authorization: Bearer $GAME_NETWORKING_API_KEY`
  - GET /api/network/status: Retrieves current latency and connection stats; query param: `?sessionID=123`
  - PUT /api/network/sync: Sends game state updates; body: `{"state": {"players": [{"id": 1, "pos": [5, 10]}]}}`

- **Code Snippets:**
  - Initialize and connect in Python:
    ```python
    import openclaw
    api_key = os.environ.get('GAME_NETWORKING_API_KEY')
    session = openclaw.game_networking.init(protocol='udp', port=5000, key=api_key)
    session.connect(host='192.168.1.1')
    ```
  - Send data:
    ```python
    data = {'player_pos': [10, 20]}
    openclaw.game_networking.send(session, data)
    ```

- **Config Formats:**
  - Use JSON for configurations, e.g.:
    ```json
    {
      "protocol": "tcp",
      "maxLatency": 100,
      "syncInterval": 50
    }
    ```
    - Save as `network-config.json` and pass via CLI: `openclaw game-networking init --config network-config.json`

## Integration Notes
Integrate this skill into game engines like Unity or Godot by importing the OpenClaw SDK and calling functions from your scripts. For Unity, add the OpenClaw package via NuGet and reference it in C# scripts. Always verify dependencies: ensure the skill is compatible with your game's architecture (e.g., client-server vs. P2P). If using with other OpenClaw skills, chain them; for example, use `game-auth` first to handle user logins, then pass the token to network commands via `$GAME_NETWORKING_API_KEY`. Test integrations in a simulated environment to handle firewall issues.

## Error Handling
Anticipate common errors like connection timeouts, packet loss, or invalid API keys. Use try-except blocks for CLI/API calls; for example, catch `NetworkError` for failed connections. Specific patterns:
- If a command fails with "Timeout", retry up to 3 times with exponential backoff: `openclaw game-networking send --retry 3`.
- For API errors, check HTTP status codes (e.g., 401 for unauthorized; respond by prompting for `$GAME_NETWORKING_API_KEY`).
- In code, handle exceptions like this:
  ```python
  try:
      response = openclaw.game_networking.listen(timeout=5)
  except openclaw.NetworkTimeoutError as e:
      print(f"Timeout occurred: {e}. Retrying...")
      # Implement retry logic here
  ```
Log errors with timestamps and include debug flags in commands, e.g., `openclaw game-networking init --debug` to output detailed traces.

## Usage Examples
1. **Set up a multiplayer lobby:** Use this to create a simple server for player connections. First, run `openclaw game-networking init --protocol tcp --port 8080 --key $GAME_NETWORKING_API_KEY`. Then, in your game code, connect clients with: ```python
import openclaw
session = openclaw.game_networking.connect(host='localhost', port=8080)
session.send({'action': 'join_lobby', 'player_name': 'User1'})
``` This establishes a lobby where players can join and exchange messages.

2. **Synchronize player positions in a real-time game:** Initialize with `openclaw game-networking init --protocol udp`. In the game loop, send updates: ```python
while game_running:
    pos = get_player_position()
    openclaw.game_networking.send(session, {'player_pos': pos})
    incoming = openclaw.game_networking.receive()
    if incoming: update_game_state(incoming)
``` This ensures low-latency synchronization, compensating for delays by interpolating positions.

## Graph Relationships
- Depends on: authentication (for secure connections), game-physics (for synchronized simulations)
- Related to: game-dev cluster skills like game-ai (for intelligent network behaviors), data-storage (for persisting game states)
- Conflicts with: none directly, but avoid overlapping with low-level socket implementations
