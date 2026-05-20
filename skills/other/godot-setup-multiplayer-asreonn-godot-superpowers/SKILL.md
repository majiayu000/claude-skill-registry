---
name: godot-setup-multiplayer
version: 1.0.0
displayName: Setup Multiplayer Networking (Godot 4.x)
description: >
  Use when building multiplayer games in Godot 4.x that require networked gameplay,
  player synchronization, or RPC communication. Sets up the new High-Level Multiplayer API
  with MultiplayerSpawner, MultiplayerSynchronizer, and @rpc annotations.
author: Asreonn
license: MIT
category: game-development
type: tool
difficulty: advanced
audience: [developers]
keywords:
  - godot
  - multiplayer
  - networking
  - rpc
  - multiplayerpeer
  - authority
  - host
  - client
  - server
  - replication
  - enet
  - synchronizer
  - spawner
platforms: [macos, linux, windows]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme

permissions:
  filesystem:
    read: [".gd", ".tscn", ".tres"]
    write: [".gd", ".tscn", ".tres"]
  git: true

behavior:
  auto_rollback: true
  validation: true
  git_commits: true

outputs: "Multiplayer scenes with ENet setup, RPC annotations, synchronizers, spawners"
requirements: "Godot 4.x project, basic networking knowledge"
execution: "Assisted - provides templates and patterns"
integration: "Part of Godot 4.x Phase 2 skills"
---

# Setup Multiplayer Networking (Godot 4.x)

## Core Principle

**Godot 4.x replaces the old `remote func` system with the High-Level Multiplayer API using `MultiplayerSpawner`, `MultiplayerSynchronizer`, and `@rpc` annotations.** Authority determines who controls what—server authority is the default safe pattern.

## What Changed from Godot 3.x

| Godot 3.x | Godot 4.x |
|-----------|-----------|
| `remote func` | `@rpc` annotation |
| `remotesync` | `@rpc(any_peer, call_local)` |
| `master` | `@rpc(authority)` with `is_multiplayer_authority()` |
| `slave` | `@rpc` called from non-authority |
| `get_tree().network_peer` | `multiplayer.multiplayer_peer` |
| Custom sync | `MultiplayerSynchronizer` |
| Custom spawn | `MultiplayerSpawner` |

## Multiplayer API Setup

### MultiplayerPeer Configuration

The foundation of networking in Godot 4.x:

```gdscript
extends Node

@export var port: int = 7000
@export var max_players: int = 8

func create_host() -> void:
    var peer = ENetMultiplayerPeer.new()
    var error = peer.create_server(port, max_players)
    
    if error == OK:
        multiplayer.multiplayer_peer = peer
        print("Server started on port ", port)
        _setup_multiplayer_signals()
    else:
        push_error("Failed to create server: ", error)

func join_host(address: String) -> void:
    var peer = ENetMultiplayerPeer.new()
    var error = peer.create_client(address, port)
    
    if error == OK:
        multiplayer.multiplayer_peer = peer
        print("Connecting to ", address, ":", port)
        _setup_multiplayer_signals()
    else:
        push_error("Failed to create client: ", error)
```

### Connection Handling

```gdscript
func _setup_multiplayer_signals() -> void:
    multiplayer.peer_connected.connect(_on_peer_connected)
    multiplayer.peer_disconnected.connect(_on_peer_disconnected)
    multiplayer.connected_to_server.connect(_on_connected_to_server)
    multiplayer.connection_failed.connect(_on_connection_failed)
    multiplayer.server_disconnected.connect(_on_server_disconnected)

func _on_peer_connected(id: int) -> void:
    print("Player connected: ", id)
    if multiplayer.is_server():
        _spawn_player(id)

func _on_peer_disconnected(id: int) -> void:
    print("Player disconnected: ", id)
    if multiplayer.is_server():
        _despawn_player(id)

func _on_connected_to_server() -> void:
    print("Connected to server as ", multiplayer.get_unique_id())

func _on_connection_failed() -> void:
    push_error("Failed to connect to server")

func _on_server_disconnected() -> void:
    push_warning("Server disconnected")
    multiplayer.multiplayer_peer = null
```

## Node Synchronization

### MultiplayerSpawner Setup

Automatically spawn/despawn nodes across all clients:

```gdscript
# In your main game scene or world node
extends Node2D

@onready var spawner: MultiplayerSpawner = $MultiplayerSpawner

func _ready() -> void:
    # Set the spawn path (where spawned nodes will be added)
    spawner.spawn_path = "../Players"
    
    # Add the player scene to auto-spawn list
    var player_scene = preload("res://scenes/player.tscn")
    spawner.add_spawnable_scene(player_scene.resource_path)

func _spawn_player(id: int) -> void:
    # Only the server spawns players
    if not multiplayer.is_server():
        return
    
    var player = preload("res://scenes/player.tscn").instantiate()
    player.name = str(id)  # Name must match peer ID for authority
    player.set_multiplayer_authority(id)
    
    # Add to spawn path - spawner handles replication
    $Players.add_child(player, true)  # "true" makes it replicated
```

### MultiplayerSynchronizer Configuration

Synchronize properties automatically:

```gdscript
# player.gd
extends CharacterBody2D

@export var speed: float = 200.0
@export var health: int = 100

# Properties to sync (configured in editor)
@onready var synchronizer: MultiplayerSynchronizer = $MultiplayerSynchronizer

func _ready() -> void:
    # Configure what to sync (can also do this in editor)
    var config = synchronizer.get_replication_config()
    config.add_property(":position")
    config.add_property(":velocity")
    config.add_property(":health")
    
    # Sync interval (lower = more frequent, more bandwidth)
    synchronizer.replication_interval = 0.05  # 20 times per second
    
    # Only sync if value changed
    synchronizer.delta_interval = 0.0  # 0 = always sync

func _physics_process(delta: float) -> void:
    # Only process input if we have authority
    if not is_multiplayer_authority():
        return
    
    var input_dir = Input.get_vector("move_left", "move_right", "move_up", "move_down")
    velocity = input_dir * speed
    move_and_slide()
```

### Scene Replication Setup

In the Godot editor:

1. **Add MultiplayerSpawner** to your world/game scene
2. **Set Spawn Path** to a Node where players will be added (e.g., `../Players`)
3. **Add spawnable scenes** in the inspector (player.tscn, enemy.tscn, etc.)
4. **Add MultiplayerSynchronizer** as child of nodes that need sync
5. **Configure ReplicationConfig** in the synchronizer inspector

## RPC Patterns

### @rpc Annotation Usage

Replace `remote func` with `@rpc` decorator:

```gdscript
# Godot 3.x style (OLD - don't use)
remote func take_damage(amount: int) -> void:
    health -= amount

# Godot 4.x style (NEW)
@rpc
def take_damage(amount: int) -> void:
    health -= amount
```

### Call Modes

Control who can call and where it executes:

```gdscript
# Authority only (default) - only authority peer can call
@rpc
func server_only_function() -> void:
    pass  # Runs on all peers, but only authority can trigger

# Any peer can call
@rpc(any_peer)
func any_peer_can_call() -> void:
    pass

# Call on local peer too (replaces 'remotesync')
@rpc(any_peer, call_local)
func synced_function() -> void:
    pass  # Runs on caller AND all remote peers

# Authority with local call
@rpc(authority, call_local)
func authority_synced() -> void:
    pass

# Unreliable for fast updates (position, rotation)
@rpc(unreliable)
func fast_update(pos: Vector2) -> void:
    pass

# Unreliable + ordered (good for continuous position updates)
@rpc(unreliable, ordered)
func ordered_update(pos: Vector2) -> void:
    pass
```

### RPC Reliability and Channels

```gdscript
# Reliable (default) - guaranteed delivery, ordered
@rpc
func important_event(data: Dictionary) -> void:
    pass  # Use for: scoring, death, state changes

# Unreliable - faster, may be lost
@rpc(unreliable)
func position_update(pos: Vector2) -> void:
    pass  # Use for: frequent position/rotation updates

# Unreliable ordered - drops old packets, keeps order
@rpc(unreliable, ordered)
func continuous_stream(data: PackedByteArray) -> void:
    pass  # Use for: voice chat, streaming data

# Channel configuration (0-9, default 0)
@rpc(channel=1)
func chat_message(msg: String) -> void:
    pass  # Separate channel for chat, won't block game data

# Mode + reliability combinations
@rpc(authority, unreliable)
func server_position_update(pos: Vector2) -> void:
    pass

@rpc(any_peer, unreliable, ordered, channel=2)
func voice_data(data: PackedByteArray) -> void:
    pass
```

## Authority Patterns

### Server Authority (Recommended)

Server validates all actions:

```gdscript
# player.gd
extends CharacterBody2D

@export var speed: float = 200.0
var input_vector: Vector2 = Vector2.ZERO

func _physics_process(delta: float) -> void:
    if is_multiplayer_authority():
        # Authority (usually server) handles actual movement
        _process_authority(delta)
    else:
        # Non-authority (client) handles prediction/interpolation
        _process_remote(delta)

func _process_authority(delta: float) -> void:
    if multiplayer.is_server():
        # Server: apply actual inputs received from clients
        velocity = input_vector * speed
        move_and_slide()
    else:
        # Client: send inputs to server, predict locally
        input_vector = Input.get_vector("move_left", "move_right", "move_up", "move_down")
        rpc_id(1, "receive_input", input_vector)  # Send to server (peer 1)
        
        # Client-side prediction (optional)
        velocity = input_vector * speed
        move_and_slide()

@rpc(any_peer)
func receive_input(input: Vector2) -> void:
    # Only server processes inputs
    if not multiplayer.is_server():
        return
    
    # Validate input (anti-cheat)
    if input.length() > 1.0:
        input = input.normalized()
    
    input_vector = input

func _process_remote(delta: float) -> void:
    # Interpolate to sync position
    # MultiplayerSynchronizer handles this automatically
    pass
```

### Client-Side Prediction

Reduce perceived latency:

```gdscript
extends CharacterBody2D

var predicted_position: Vector2
var server_position: Vector2
var reconciliation_speed: float = 10.0

func _ready() -> void:
    if is_multiplayer_authority() and not multiplayer.is_server():
        # Client with authority over this player
        set_physics_process(true)

func _physics_process(delta: float) -> void:
    if is_multiplayer_authority() and not multiplayer.is_server():
        # Client prediction
        var input = Input.get_vector("move_left", "move_right", "move_up", "move_down")
        velocity = input * speed
        predicted_position = position + velocity * delta
        
        # Reconcile with server
        position = position.lerp(server_position, reconciliation_speed * delta)
        move_and_slide()
        
        # Send input to server
        rpc_id(1, "update_input", input)

@rpc
func update_state(pos: Vector2, vel: Vector2) -> void:
    # Received from server
    server_position = pos
    velocity = vel
```

### State Reconciliation

Handle server corrections:

```gdscript
var input_history: Array[Dictionary] = []
var last_processed_input: int = 0

func _physics_process(delta: float) -> void:
    if is_multiplayer_authority():
        var input = get_input()
        var input_id = Time.get_ticks_msec()
        
        input_history.append({"id": input_id, "input": input})
        
        # Apply input
        apply_input(input, delta)
        
        # Send to server with ID
        rpc_id(1, "process_input", input_id, input)

@rpc
func correction(server_state: Dictionary) -> void:
    # Server sends authoritative state + last processed input ID
    position = server_state.position
    velocity = server_state.velocity
    last_processed_input = server_state.last_input_id
    
    # Replay unprocessed inputs
    for hist in input_history:
        if hist.id > last_processed_input:
            apply_input(hist.input, get_physics_process_delta_time())
    
    # Clear old history
    input_history = input_history.filter(func(h): return h.id > last_processed_input)
```

## Scene Structure

### Lobby Scene

```gdscript
# lobby.gd
extends Control

@onready var host_button: Button = $HostButton
@onready var join_button: Button = $JoinButton
@onready var address_input: LineEdit = $AddressInput
@onready var status_label: Label = $StatusLabel

func _ready() -> void:
    host_button.pressed.connect(_on_host_pressed)
    join_button.pressed.connect(_on_join_pressed)
    
    multiplayer.connected_to_server.connect(_on_connection_success)
    multiplayer.connection_failed.connect(_on_connection_failed)

func _on_host_pressed() -> void:
    var peer = ENetMultiplayerPeer.new()
    var err = peer.create_server(7000, 4)
    
    if err == OK:
        multiplayer.multiplayer_peer = peer
        status_label.text = "Hosting on port 7000"
        _start_game()
    else:
        status_label.text = "Failed to host: " + str(err)

func _on_join_pressed() -> void:
    var address = address_input.text if address_input.text else "localhost"
    var peer = ENetMultiplayerPeer.new()
    var err = peer.create_client(address, 7000)
    
    if err == OK:
        multiplayer.multiplayer_peer = peer
        status_label.text = "Connecting..."
    else:
        status_label.text = "Failed to connect: " + str(err)

func _on_connection_success() -> void:
    status_label.text = "Connected!"
    _start_game()

func _on_connection_failed() -> void:
    status_label.text = "Connection failed"

func _start_game() -> void:
    get_tree().change_scene_to_file("res://scenes/game.tscn")
```

### Game Scene with Multiplayer

```gdscript
# game.gd
extends Node2D

@onready var spawner: MultiplayerSpawner = $MultiplayerSpawner
@onready var players_container: Node2D = $Players

func _ready() -> void:
    spawner.spawn_function = _spawn_player_custom
    
    if multiplayer.is_server():
        multiplayer.peer_connected.connect(_on_peer_connected)
        multiplayer.peer_disconnected.connect(_on_peer_disconnected)
        
        # Spawn host player
        _spawn_player(1)

func _on_peer_connected(id: int) -> void:
    _spawn_player(id)

func _on_peer_disconnected(id: int) -> void:
    var player = players_container.get_node_or_null(str(id))
    if player:
        player.queue_free()

func _spawn_player(id: int) -> void:
    var player_data = {
        "player_id": id,
        "spawn_position": get_random_spawn_point()
    }
    spawner.spawn(player_data)

func _spawn_player_custom(data: Dictionary) -> Node:
    var player = preload("res://scenes/player.tscn").instantiate()
    player.name = str(data.player_id)
    player.set_multiplayer_authority(data.player_id)
    player.position = data.spawn_position
    return player
```

### Player Scene

```gdscript
# player.gd
extends CharacterBody2D

@export var speed: float = 200.0
@export var health: int = 100

@onready var synchronizer: MultiplayerSynchronizer = $MultiplayerSynchronizer
@onready var label: Label = $Label

func _ready() -> void:
    label.text = str(get_multiplayer_authority())
    
    # Only process if we have authority
    set_physics_process(is_multiplayer_authority())
    set_process_input(is_multiplayer_authority())

func _physics_process(delta: float) -> void:
    var input_dir = Input.get_vector("move_left", "move_right", "move_up", "move_down")
    velocity = input_dir * speed
    move_and_slide()

@rpc(any_peer)
func take_damage(amount: int) -> void:
    # Only server processes damage
    if not multiplayer.is_server():
        return
    
    health -= amount
    
    if health <= 0:
        rpc("died")
        _respawn()

@rpc(call_local)
func died() -> void:
    visible = false
    set_physics_process(false)

func _respawn() -> void:
    health = 100
    position = Vector2.ZERO
    rpc("respawned")

@rpc(call_local)
func respawned() -> void:
    visible = true
    set_physics_process(is_multiplayer_authority())
```

### Disconnection Handling

```gdscript
func _setup_disconnection_handling() -> void:
    multiplayer.server_disconnected.connect(_on_server_disconnected)
    multiplayer.peer_disconnected.connect(_on_peer_disconnected)
    get_tree().auto_accept_quit = false

func _notification(what: int) -> void:
    if what == NOTIFICATION_WM_CLOSE_REQUEST:
        _cleanup_and_quit()

func _cleanup_and_quit() -> void:
    if multiplayer.multiplayer_peer:
        multiplayer.multiplayer_peer.close()
        multiplayer.multiplayer_peer = null
    get_tree().quit()

func _on_server_disconnected() -> void:
    push_warning("Server disconnected")
    multiplayer.multiplayer_peer = null
    get_tree().change_scene_to_file("res://scenes/lobby.tscn")

func _on_peer_disconnected(id: int) -> void:
    var player = get_node_or_null("Players/" + str(id))
    if player:
        player.queue_free()
```

## Examples

### Basic Host/Client Setup

```gdscript
# network_manager.gd - Autoload singleton
extends Node

signal player_connected(id: int)
signal player_disconnected(id: int)
signal server_started
signal connection_failed

@export var default_port: int = 7000
@export var max_players: int = 4

var peer: ENetMultiplayerPeer = null

func create_server(port: int = default_port) -> Error:
    peer = ENetMultiplayerPeer.new()
    var err = peer.create_server(port, max_players)
    
    if err == OK:
        multiplayer.multiplayer_peer = peer
        _setup_signals()
        server_started.emit()
    
    return err

func join_server(address: String, port: int = default_port) -> Error:
    peer = ENetMultiplayerPeer.new()
    var err = peer.create_client(address, port)
    
    if err == OK:
        multiplayer.multiplayer_peer = peer
        _setup_signals()
    else:
        connection_failed.emit()
    
    return err

func _setup_signals() -> void:
    multiplayer.peer_connected.connect(func(id): player_connected.emit(id))
    multiplayer.peer_disconnected.connect(func(id): player_disconnected.emit(id))

func close_connection() -> void:
    if peer:
        peer.close()
        multiplayer.multiplayer_peer = null
        peer = null
```

### Player Synchronization

```gdscript
# synced_player.gd
extends CharacterBody2D

@export var sync_position: Vector2:
    set(value):
        sync_position = value
        if not is_multiplayer_authority():
            position = sync_position

@export var sync_rotation: float:
    set(value):
        sync_rotation = value
        if not is_multiplayer_authority():
            rotation = sync_rotation

func _physics_process(delta: float) -> void:
    if is_multiplayer_authority():
        # Update sync variables (MultiplayerSynchronizer sends these)
        sync_position = position
        sync_rotation = rotation
        
        var input = Input.get_vector("move_left", "move_right", "move_up", "move_down")
        velocity = input * 200
        move_and_slide()
```

### State Replication

```gdscript
# game_state.gd - Server authoritative game state
extends Node

# Replicated to all clients
@export var game_time: float = 0.0
@export var scores: Dictionary = {}
@export var game_phase: String = "lobby"

func _physics_process(delta: float) -> void:
    if multiplayer.is_server():
        game_time += delta
        _check_win_conditions()

func add_score(player_id: int, points: int) -> void:
    # Only server modifies state
    if not multiplayer.is_server():
        return
    
    if not scores.has(player_id):
        scores[player_id] = 0
    
    scores[player_id] += points
    
    # State is automatically synced via MultiplayerSynchronizer
    rpc("score_updated", player_id, scores[player_id])

@rpc(call_local)
func score_updated(player_id: int, new_score: int) -> void:
    print("Player ", player_id, " score: ", new_score)

func _check_win_conditions() -> void:
    for player_id in scores:
        if scores[player_id] >= 100:
            end_game(player_id)

func end_game(winner_id: int) -> void:
    game_phase = "ended"
    rpc("game_ended", winner_id)

@rpc(call_local)
func game_ended(winner_id: int) -> void:
    print("Game over! Winner: ", winner_id)
    get_tree().change_scene_to_file("res://scenes/victory.tscn")
```

### Chat System

```gdscript
# chat_system.gd
extends Control

@onready var chat_display: RichTextLabel = $ChatDisplay
@onready var chat_input: LineEdit = $ChatInput
@onready var send_button: Button = $SendButton

func _ready() -> void:
    send_button.pressed.connect(_send_message)
    chat_input.text_submitted.connect(func(_t): _send_message())

func _send_message() -> void:
    var message = chat_input.text.strip_edges()
    if message.is_empty():
        return
    
    var sender_id = multiplayer.get_unique_id()
    var sender_name = "Player " + str(sender_id)
    
    # Send to all peers (including server)
    rpc("receive_message", sender_name, message)
    
    chat_input.clear()

@rpc(any_peer, call_local)
func receive_message(sender: String, message: String) -> void:
    var formatted = "[b]%s:[/b] %s\n" % [sender, message]
    chat_display.append_text(formatted)
    
    # Auto-scroll to bottom
    chat_display.scroll_to_line(chat_display.get_line_count())
```

## Migration from Godot 3.x

### Remote Functions

```gdscript
# Godot 3.x (OLD)
remote func attack(target_id: int, damage: int) -> void:
    var target = get_node("../Players/" + str(target_id))
    if target:
        target.health -= damage

remotesync func update_position(pos: Vector2) -> void:
    position = pos

master func validate_movement(pos: Vector2) -> bool:
    return is_valid_position(pos)

slave func receive_correction(pos: Vector2) -> void:
    position = pos

# Godot 4.x (NEW)
@rpc(any_peer)
func attack(target_id: int, damage: int) -> void:
    var target = get_node("../Players/" + str(target_id))
    if target:
        target.health -= damage

@rpc(any_peer, call_local)
func update_position(pos: Vector2) -> void:
    position = pos

@rpc(authority)
func validate_movement(pos: Vector2) -> bool:
    return is_valid_position(pos)

@rpc
func receive_correction(pos: Vector2) -> void:
    position = pos
```

### RPC Calls

```gdscript
# Godot 3.x (OLD)
rpc("function_name", arg1, arg2)
rpc_id(peer_id, "function_name", arg1, arg2)
rpc_unreliable("function_name", arg1)

# Godot 4.x (NEW)
rpc("function_name", arg1, arg2)           # Reliable, default
rpc_id(peer_id, "function_name", arg1, arg2)

# For unreliable, use annotation on function:
@rpc(unreliable)
func fast_update() -> void:
    pass
```

### Network Peer Access

```gdscript
# Godot 3.x (OLD)
var peer = get_tree().network_peer
var my_id = get_tree().get_network_unique_id()
var is_server = get_tree().is_network_server()

# Godot 4.x (NEW)
var peer = multiplayer.multiplayer_peer
var my_id = multiplayer.get_unique_id()
var is_server = multiplayer.is_server()
```

### Custom Multiplayer

```gdscript
# Godot 3.x (OLD) - custom MultiplayerAPI
var custom_multiplayer = MultiplayerAPI.new()
custom_multiplayer.set_root_node(self)
set_custom_multiplayer(custom_multiplayer)

# Godot 4.x (NEW) - SceneMultiplayer
var scene_multiplayer = SceneMultiplayer.new()
get_tree().set_multiplayer(scene_multiplayer, get_path())
```

## When to Use

### Build New Multiplayer Games
Setting up networking from scratch in Godot 4.x.

### Migrate Existing Games
Converting Godot 3.x multiplayer to 4.x syntax.

### Add Multiplayer to Single-Player
Retrofitting existing game with networking.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `remote func` syntax | Use `@rpc` annotation |
| Calling RPC before peer setup | Set `multiplayer.multiplayer_peer` first |
| Not setting authority | Use `set_multiplayer_authority(id)` |
| Server processing client input directly | Validate all client input |
| Synchronizing everything | Only sync what's necessary |
| Using reliable RPC for position | Use `@rpc(unreliable)` for frequent updates |
| Forgetting `call_local` | Add if function should run on caller too |
| Spawning without spawner | Use `MultiplayerSpawner` for replicated nodes |

## Integration

Works with:
- **godot-modernize-gdscript** - Use with modern GDScript features
- **godot-profile-performance** - Optimize network bandwidth
- **godot-setup-navigation** - Multiplayer AI pathfinding

## Safety

- Always validate client input on server
- Use server authority for critical game state
- Sanitize chat messages (prevent injection)
- Limit RPC call frequency (rate limiting)
- Use unreliable channels for non-critical data

## Resources

- Godot 4.x High-Level Multiplayer: https://docs.godotengine.org/en/stable/tutorials/networking/high_level_multiplayer.html
- RPC Tutorial: https://docs.godotengine.org/en/stable/tutorials/networking/rpc.html
- MultiplayerSynchronizer: https://docs.godotengine.org/en/stable/classes/class_multiplayersynchronizer.html
