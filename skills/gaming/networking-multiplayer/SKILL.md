---
name: networking-multiplayer
description: Implements multiplayer networking using Godot's high-level multiplayer API, including RPCs, synchronization, client-server architecture, and lag compensation. Use when building online multiplayer games.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Godot Multiplayer Networking

When implementing multiplayer, follow these patterns for robust and responsive networked gameplay.

## High-Level Multiplayer API

### Setting Up Server and Client
```gdscript
extends Node

const PORT := 7777
const MAX_CLIENTS := 10

var peer: ENetMultiplayerPeer

func _ready() -> void:
    multiplayer.peer_connected.connect(_on_peer_connected)
    multiplayer.peer_disconnected.connect(_on_peer_disconnected)
    multiplayer.connected_to_server.connect(_on_connected_to_server)
    multiplayer.connection_failed.connect(_on_connection_failed)
    multiplayer.server_disconnected.connect(_on_server_disconnected)

func host_game() -> void:
    peer = ENetMultiplayerPeer.new()
    var error := peer.create_server(PORT, MAX_CLIENTS)
    if error != OK:
        push_error("Failed to create server: %s" % error)
        return

    multiplayer.multiplayer_peer = peer
    print("Server started on port %d" % PORT)

func join_game(address: String) -> void:
    peer = ENetMultiplayerPeer.new()
    var error := peer.create_client(address, PORT)
    if error != OK:
        push_error("Failed to create client: %s" % error)
        return

    multiplayer.multiplayer_peer = peer
    print("Connecting to %s:%d" % [address, PORT])

func _on_peer_connected(id: int) -> void:
    print("Peer connected: %d" % id)

func _on_peer_disconnected(id: int) -> void:
    print("Peer disconnected: %d" % id)

func _on_connected_to_server() -> void:
    print("Connected to server!")

func _on_connection_failed() -> void:
    print("Connection failed!")

func _on_server_disconnected() -> void:
    print("Server disconnected!")
```

### RPC (Remote Procedure Calls)
```gdscript
extends Node

# Call on all peers (including caller)
@rpc("any_peer", "call_local", "reliable")
func send_chat_message(message: String) -> void:
    var sender_id := multiplayer.get_remote_sender_id()
    print("[%d]: %s" % [sender_id, message])

# Call only on server
@rpc("any_peer", "call_remote", "reliable")
func request_spawn_player() -> void:
    if not multiplayer.is_server():
        return

    var sender_id := multiplayer.get_remote_sender_id()
    spawn_player.rpc(sender_id)

# Server calls on all clients
@rpc("authority", "call_local", "reliable")
func spawn_player(player_id: int) -> void:
    var player := preload("res://player.tscn").instantiate()
    player.name = str(player_id)
    player.set_multiplayer_authority(player_id)
    $Players.add_child(player)

# Unreliable for frequent updates (position, etc.)
@rpc("any_peer", "call_remote", "unreliable")
func update_position(pos: Vector3) -> void:
    position = pos

# Unreliable ordered (maintains order, but may drop)
@rpc("any_peer", "call_remote", "unreliable_ordered")
func update_input(input_vector: Vector2, timestamp: int) -> void:
    process_remote_input(input_vector, timestamp)
```

### RPC Modes Reference
```gdscript
# Authority modes:
# "authority" - Only multiplayer authority can call (default: server)
# "any_peer" - Any peer can call

# Call modes:
# "call_remote" - Call on remote peers only (not caller)
# "call_local" - Call on remote peers AND caller

# Transfer modes:
# "reliable" - Guaranteed delivery, ordered (TCP-like)
# "unreliable" - May be lost, unordered (UDP-like)
# "unreliable_ordered" - May be lost, but ordered
```

## MultiplayerSpawner and MultiplayerSynchronizer

### Automatic Spawning
```gdscript
# Scene tree setup:
# - GameManager
#   - MultiplayerSpawner (spawn_path: "../Players")
#   - Players

extends Node

@onready var spawner: MultiplayerSpawner = $MultiplayerSpawner

func _ready() -> void:
    # Add spawnable scenes
    spawner.add_spawnable_scene("res://player.tscn")
    spawner.add_spawnable_scene("res://enemy.tscn")
    spawner.add_spawnable_scene("res://projectile.tscn")

func spawn_player(player_id: int) -> void:
    if not multiplayer.is_server():
        return

    var player := preload("res://player.tscn").instantiate()
    player.name = str(player_id)
    player.set_multiplayer_authority(player_id)
    $Players.add_child(player)  # Automatically replicated by spawner
```

### Automatic State Synchronization
```gdscript
# Player scene tree:
# - Player (CharacterBody3D)
#   - MultiplayerSynchronizer
#   - CollisionShape3D
#   - MeshInstance3D

extends CharacterBody3D

# These properties are synced automatically via MultiplayerSynchronizer
# Configure in the inspector which properties to sync

@export var health := 100
var sync_position: Vector3
var sync_rotation: Vector3

func _physics_process(delta: float) -> void:
    if is_multiplayer_authority():
        # Local player - process input
        process_input(delta)
        move_and_slide()

        # Update sync properties
        sync_position = global_position
        sync_rotation = rotation
    else:
        # Remote player - interpolate to synced position
        global_position = global_position.lerp(sync_position, 10 * delta)
        rotation = rotation.lerp(sync_rotation, 10 * delta)
```

### MultiplayerSynchronizer Configuration
```gdscript
extends Node

func setup_synchronizer(sync: MultiplayerSynchronizer) -> void:
    # Replication interval (seconds)
    sync.replication_interval = 0.05  # 20 updates per second

    # Delta synchronization (only send changes)
    sync.delta_interval = 0.1

    # Visibility (who receives updates)
    sync.public_visibility = true

    # Or use visibility filters
    sync.set_visibility_for(peer_id, true)
```

## Client-Server Architecture

### Server Authority Pattern
```gdscript
extends CharacterBody3D

# Client sends input to server, server validates and moves
@rpc("any_peer", "call_remote", "unreliable_ordered")
func send_input(input: Dictionary, timestamp: int) -> void:
    if not multiplayer.is_server():
        return

    var sender_id := multiplayer.get_remote_sender_id()
    if sender_id != get_multiplayer_authority():
        return  # Ignore input from non-authority

    # Validate input
    if not validate_input(input):
        return

    # Apply input on server
    apply_input(input)

    # Send authoritative state back to all clients
    sync_state.rpc(global_position, velocity, timestamp)

@rpc("authority", "call_remote", "unreliable_ordered")
func sync_state(pos: Vector3, vel: Vector3, timestamp: int) -> void:
    # Client receives authoritative state
    server_position = pos
    server_velocity = vel
    last_server_timestamp = timestamp

func validate_input(input: Dictionary) -> bool:
    # Check for impossible values
    var move_dir: Vector2 = input.get("direction", Vector2.ZERO)
    if move_dir.length() > 1.1:  # Allow small margin
        return false
    return true
```

### Client-Side Prediction
```gdscript
extends CharacterBody3D

var input_history: Array[Dictionary] = []
var server_position: Vector3
var last_server_timestamp := 0

func _physics_process(delta: float) -> void:
    if not is_multiplayer_authority():
        return

    # Gather input
    var input := {
        "direction": Input.get_vector("left", "right", "forward", "back"),
        "jump": Input.is_action_just_pressed("jump"),
        "timestamp": Time.get_ticks_msec()
    }

    # Save to history for reconciliation
    input_history.append(input)

    # Apply locally (prediction)
    apply_input(input)
    move_and_slide()

    # Send to server
    send_input.rpc_id(1, input, input["timestamp"])

    # Reconcile with server state
    reconcile_with_server()

func reconcile_with_server() -> void:
    # Remove old inputs
    while input_history.size() > 0 and input_history[0]["timestamp"] <= last_server_timestamp:
        input_history.pop_front()

    # Check if position matches
    var error := global_position.distance_to(server_position)
    if error > 0.5:  # Threshold
        # Snap to server position and replay inputs
        global_position = server_position
        for input in input_history:
            apply_input(input)
            move_and_slide()

func apply_input(input: Dictionary) -> void:
    var direction: Vector2 = input["direction"]
    velocity.x = direction.x * speed
    velocity.z = direction.y * speed

    if input["jump"] and is_on_floor():
        velocity.y = jump_velocity
```

### Lag Compensation
```gdscript
extends Node

# Server-side lag compensation for hit detection
var position_history: Dictionary = {}  # peer_id -> Array of {position, timestamp}
const HISTORY_DURATION := 1.0  # Keep 1 second of history

func _physics_process(delta: float) -> void:
    if not multiplayer.is_server():
        return

    # Record positions for all players
    var current_time := Time.get_ticks_msec()
    for player in $Players.get_children():
        var peer_id := player.get_multiplayer_authority()
        if not position_history.has(peer_id):
            position_history[peer_id] = []

        position_history[peer_id].append({
            "position": player.global_position,
            "timestamp": current_time
        })

        # Clean old history
        while position_history[peer_id].size() > 0:
            if current_time - position_history[peer_id][0]["timestamp"] > HISTORY_DURATION * 1000:
                position_history[peer_id].pop_front()
            else:
                break

func get_position_at_time(peer_id: int, timestamp: int) -> Vector3:
    if not position_history.has(peer_id):
        return Vector3.ZERO

    var history: Array = position_history[peer_id]

    # Find surrounding timestamps
    for i in range(history.size() - 1):
        if history[i]["timestamp"] <= timestamp and history[i + 1]["timestamp"] >= timestamp:
            # Interpolate
            var t := float(timestamp - history[i]["timestamp"]) / float(history[i + 1]["timestamp"] - history[i]["timestamp"])
            return history[i]["position"].lerp(history[i + 1]["position"], t)

    # Return latest if timestamp is newer than history
    if history.size() > 0:
        return history[-1]["position"]

    return Vector3.ZERO

@rpc("any_peer", "call_remote", "reliable")
func process_shot(target_peer_id: int, client_timestamp: int) -> void:
    if not multiplayer.is_server():
        return

    var shooter_id := multiplayer.get_remote_sender_id()
    var shooter: Node3D = $Players.get_node(str(shooter_id))

    # Get target position at the time the shot was fired (from client's perspective)
    # Account for network latency
    var latency := get_peer_latency(shooter_id)
    var server_timestamp := client_timestamp + latency
    var target_position := get_position_at_time(target_peer_id, server_timestamp)

    # Validate hit
    var distance := shooter.global_position.distance_to(target_position)
    if distance < weapon_range:
        apply_damage.rpc(target_peer_id, damage)
```

## Interpolation and Extrapolation

### Network Interpolation
```gdscript
extends CharacterBody3D

var state_buffer: Array[Dictionary] = []
const INTERPOLATION_OFFSET := 0.1  # 100ms behind

func receive_state(pos: Vector3, vel: Vector3, timestamp: float) -> void:
    state_buffer.append({
        "position": pos,
        "velocity": vel,
        "timestamp": timestamp
    })

    # Keep buffer sorted and limited
    state_buffer.sort_custom(func(a, b): return a["timestamp"] < b["timestamp"])
    while state_buffer.size() > 20:
        state_buffer.pop_front()

func _physics_process(delta: float) -> void:
    if is_multiplayer_authority():
        return  # Local player doesn't interpolate

    var render_time := Time.get_unix_time_from_system() - INTERPOLATION_OFFSET

    # Find surrounding states
    var before: Dictionary
    var after: Dictionary

    for i in range(state_buffer.size() - 1):
        if state_buffer[i]["timestamp"] <= render_time and state_buffer[i + 1]["timestamp"] >= render_time:
            before = state_buffer[i]
            after = state_buffer[i + 1]
            break

    if before.is_empty() or after.is_empty():
        # Extrapolate if no valid states
        if state_buffer.size() > 0:
            extrapolate(state_buffer[-1], delta)
        return

    # Interpolate
    var t := (render_time - before["timestamp"]) / (after["timestamp"] - before["timestamp"])
    global_position = before["position"].lerp(after["position"], t)
```

### Snapshot Interpolation
```gdscript
extends Node

class_name SnapshotInterpolator

var snapshots: Array[Dictionary] = []
var interpolation_delay := 0.1

func add_snapshot(snapshot: Dictionary) -> void:
    snapshot["received_time"] = Time.get_unix_time_from_system()
    snapshots.append(snapshot)

    # Limit buffer size
    while snapshots.size() > 30:
        snapshots.pop_front()

func get_interpolated_state(entity_id: int) -> Dictionary:
    var render_time := Time.get_unix_time_from_system() - interpolation_delay

    var before: Dictionary
    var after: Dictionary

    for i in range(snapshots.size() - 1):
        var snap_time: float = snapshots[i]["received_time"]
        var next_time: float = snapshots[i + 1]["received_time"]

        if snap_time <= render_time and next_time >= render_time:
            before = snapshots[i]
            after = snapshots[i + 1]
            break

    if before.is_empty():
        return {}

    var t := (render_time - before["received_time"]) / (after["received_time"] - before["received_time"])

    var before_entity: Dictionary = before["entities"].get(entity_id, {})
    var after_entity: Dictionary = after["entities"].get(entity_id, {})

    if before_entity.is_empty() or after_entity.is_empty():
        return {}

    return {
        "position": before_entity["position"].lerp(after_entity["position"], t),
        "rotation": before_entity["rotation"].slerp(after_entity["rotation"], t)
    }
```

## WebSocket and WebRTC

### WebSocket Server
```gdscript
extends Node

var server: WebSocketMultiplayerPeer

func start_server(port: int) -> void:
    server = WebSocketMultiplayerPeer.new()
    var error := server.create_server(port)
    if error != OK:
        push_error("Failed to start WebSocket server")
        return

    multiplayer.multiplayer_peer = server

func _process(_delta: float) -> void:
    if server:
        server.poll()
```

### WebRTC for P2P
```gdscript
extends Node

var rtc_peer: WebRTCMultiplayerPeer

func initialize_webrtc() -> void:
    rtc_peer = WebRTCMultiplayerPeer.new()
    rtc_peer.create_mesh(generate_unique_id())
    multiplayer.multiplayer_peer = rtc_peer

func add_peer(peer_id: int) -> void:
    var connection := WebRTCPeerConnection.new()

    # Configure ICE servers (STUN/TURN)
    connection.initialize({
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]}
        ]
    })

    rtc_peer.add_peer(connection, peer_id)
```

## Common Networking Gotchas

### Authority Checks
```gdscript
# Always verify authority before processing sensitive operations
func _physics_process(delta: float) -> void:
    # Only process input for local player
    if not is_multiplayer_authority():
        return

    process_input(delta)

# Server should validate RPC sender
@rpc("any_peer", "call_remote", "reliable")
func deal_damage(target_id: int, amount: int) -> void:
    if not multiplayer.is_server():
        return

    var sender := multiplayer.get_remote_sender_id()

    # Validate sender can deal this damage
    if not can_player_attack(sender, target_id):
        return

    # Validate amount
    amount = clamp(amount, 0, MAX_DAMAGE)

    apply_damage(target_id, amount)
```

### Handling Disconnections
```gdscript
func _on_peer_disconnected(id: int) -> void:
    # Clean up player
    var player := $Players.get_node_or_null(str(id))
    if player:
        player.queue_free()

    # Notify other players
    if multiplayer.is_server():
        player_disconnected.rpc(id)

@rpc("authority", "call_local", "reliable")
func player_disconnected(id: int) -> void:
    print("Player %d left the game" % id)
```
