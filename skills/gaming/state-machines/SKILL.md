---
name: state-machines
description: Implements state machine patterns for game logic, AI, and animations including hierarchical state machines and pushdown automata. Use when building complex game behaviors.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Godot State Machines

When implementing complex behaviors, use these state machine patterns for clean and maintainable code.

## Basic State Machine

### Enum-Based State Machine
```gdscript
extends CharacterBody2D

enum State { IDLE, RUN, JUMP, FALL, ATTACK }

var current_state: State = State.IDLE

func _physics_process(delta: float) -> void:
    match current_state:
        State.IDLE:
            state_idle(delta)
        State.RUN:
            state_run(delta)
        State.JUMP:
            state_jump(delta)
        State.FALL:
            state_fall(delta)
        State.ATTACK:
            state_attack(delta)

    move_and_slide()

func change_state(new_state: State) -> void:
    if current_state == new_state:
        return

    # Exit current state
    exit_state(current_state)

    var old_state := current_state
    current_state = new_state

    # Enter new state
    enter_state(new_state, old_state)

func enter_state(state: State, _previous: State) -> void:
    match state:
        State.JUMP:
            velocity.y = jump_velocity
            $AnimationPlayer.play("jump")
        State.ATTACK:
            $AnimationPlayer.play("attack")

func exit_state(state: State) -> void:
    match state:
        State.ATTACK:
            # Reset attack hitbox
            $Hitbox.monitoring = false

func state_idle(delta: float) -> void:
    apply_gravity(delta)
    velocity.x = move_toward(velocity.x, 0, friction * delta)

    if not is_on_floor():
        change_state(State.FALL)
    elif Input.is_action_just_pressed("jump"):
        change_state(State.JUMP)
    elif Input.is_action_just_pressed("attack"):
        change_state(State.ATTACK)
    elif Input.get_axis("move_left", "move_right") != 0:
        change_state(State.RUN)
```

## Node-Based State Machine

### State Base Class
```gdscript
# state.gd
class_name State
extends Node

# Reference to the state machine
var state_machine: StateMachine

# Called when entering this state
func enter(_previous_state: State) -> void:
    pass

# Called when exiting this state
func exit() -> void:
    pass

# Called every frame
func update(_delta: float) -> void:
    pass

# Called every physics frame
func physics_update(_delta: float) -> void:
    pass

# Handle input events
func handle_input(_event: InputEvent) -> void:
    pass
```

### State Machine Controller
```gdscript
# state_machine.gd
class_name StateMachine
extends Node

@export var initial_state: State

var current_state: State
var states: Dictionary = {}

func _ready() -> void:
    # Register all child states
    for child in get_children():
        if child is State:
            states[child.name.to_lower()] = child
            child.state_machine = self

    # Start with initial state
    if initial_state:
        current_state = initial_state
        current_state.enter(null)

func _unhandled_input(event: InputEvent) -> void:
    if current_state:
        current_state.handle_input(event)

func _process(delta: float) -> void:
    if current_state:
        current_state.update(delta)

func _physics_process(delta: float) -> void:
    if current_state:
        current_state.physics_update(delta)

func transition_to(state_name: String) -> void:
    if not states.has(state_name):
        push_error("State '%s' does not exist" % state_name)
        return

    var new_state: State = states[state_name]

    if current_state:
        current_state.exit()

    var previous_state := current_state
    current_state = new_state
    current_state.enter(previous_state)
```

### Concrete State Example
```gdscript
# idle_state.gd
class_name IdleState
extends State

@onready var player: CharacterBody2D = owner

func enter(_previous_state: State) -> void:
    player.animation_player.play("idle")

func physics_update(delta: float) -> void:
    player.apply_gravity(delta)
    player.velocity.x = move_toward(player.velocity.x, 0, player.friction * delta)
    player.move_and_slide()

    # Check transitions
    if not player.is_on_floor():
        state_machine.transition_to("fall")
    elif Input.get_axis("move_left", "move_right") != 0:
        state_machine.transition_to("run")

func handle_input(event: InputEvent) -> void:
    if event.is_action_pressed("jump") and player.is_on_floor():
        state_machine.transition_to("jump")
    elif event.is_action_pressed("attack"):
        state_machine.transition_to("attack")
```

## Hierarchical State Machine

### State with Sub-States
```gdscript
# hierarchical_state.gd
class_name HierarchicalState
extends State

@export var initial_substate: State

var current_substate: State
var substates: Dictionary = {}

func _ready() -> void:
    for child in get_children():
        if child is State:
            substates[child.name.to_lower()] = child
            child.state_machine = state_machine

func enter(previous_state: State) -> void:
    if initial_substate:
        current_substate = initial_substate
        current_substate.enter(previous_state)

func exit() -> void:
    if current_substate:
        current_substate.exit()

func update(delta: float) -> void:
    if current_substate:
        current_substate.update(delta)

func physics_update(delta: float) -> void:
    if current_substate:
        current_substate.physics_update(delta)

func handle_input(event: InputEvent) -> void:
    if current_substate:
        current_substate.handle_input(event)

func transition_to_substate(substate_name: String) -> void:
    if not substates.has(substate_name):
        return

    var new_substate: State = substates[substate_name]

    if current_substate:
        current_substate.exit()

    current_substate = new_substate
    current_substate.enter(current_substate)
```

### Example: Combat State with Sub-States
```gdscript
# Scene Tree:
# StateMachine
#   - Idle
#   - Move
#   - Combat (HierarchicalState)
#       - AttackLight
#       - AttackHeavy
#       - Block
#       - Dodge

# combat_state.gd
class_name CombatState
extends HierarchicalState

@onready var player: CharacterBody2D = owner

func enter(previous_state: State) -> void:
    super.enter(previous_state)
    player.in_combat = true

func exit() -> void:
    super.exit()
    player.in_combat = false

func handle_input(event: InputEvent) -> void:
    # Combat-specific transitions
    if event.is_action_pressed("light_attack"):
        transition_to_substate("attacklight")
    elif event.is_action_pressed("heavy_attack"):
        transition_to_substate("attackheavy")
    elif event.is_action_pressed("block"):
        transition_to_substate("block")
    elif event.is_action_pressed("dodge"):
        transition_to_substate("dodge")
    else:
        super.handle_input(event)
```

## Pushdown Automaton

### State Stack
```gdscript
# pushdown_state_machine.gd
class_name PushdownStateMachine
extends Node

var state_stack: Array[State] = []
var states: Dictionary = {}

func _ready() -> void:
    for child in get_children():
        if child is State:
            states[child.name.to_lower()] = child
            child.state_machine = self

func current_state() -> State:
    if state_stack.is_empty():
        return null
    return state_stack.back()

func _process(delta: float) -> void:
    var state := current_state()
    if state:
        state.update(delta)

func _physics_process(delta: float) -> void:
    var state := current_state()
    if state:
        state.physics_update(delta)

# Push a new state onto the stack
func push_state(state_name: String) -> void:
    var new_state: State = states.get(state_name)
    if not new_state:
        return

    var previous := current_state()
    if previous:
        previous.pause()  # Pause but don't exit

    state_stack.append(new_state)
    new_state.enter(previous)

# Pop the current state and resume previous
func pop_state() -> void:
    if state_stack.is_empty():
        return

    var popped := state_stack.pop_back()
    popped.exit()

    var resumed := current_state()
    if resumed:
        resumed.resume()

# Replace current state
func change_state(state_name: String) -> void:
    pop_state()
    push_state(state_name)
```

### Pausable State Base
```gdscript
# pausable_state.gd
class_name PausableState
extends State

var is_paused := false

func pause() -> void:
    is_paused = true

func resume() -> void:
    is_paused = false

func update(delta: float) -> void:
    if is_paused:
        return
    # Normal update
```

### Example: Dialogue System with Pushdown
```gdscript
# Use pushdown for menus/dialogue that pause gameplay

# gameplay_state.gd
extends PausableState

func physics_update(delta: float) -> void:
    if is_paused:
        return
    # Normal gameplay

func handle_input(event: InputEvent) -> void:
    if event.is_action_pressed("interact"):
        # Push dialogue state, pausing gameplay
        state_machine.push_state("dialogue")
    elif event.is_action_pressed("pause"):
        state_machine.push_state("pause_menu")

# dialogue_state.gd
extends State

func enter(_previous: State) -> void:
    $DialogueUI.show()
    get_tree().paused = true

func exit() -> void:
    $DialogueUI.hide()
    get_tree().paused = false

func handle_input(event: InputEvent) -> void:
    if event.is_action_pressed("ui_accept"):
        if dialogue_complete():
            state_machine.pop_state()
        else:
            advance_dialogue()
```

## Animation State Machine Integration

### Linking to AnimationTree
```gdscript
extends CharacterBody2D

@onready var animation_tree: AnimationTree = $AnimationTree
@onready var state_machine_playback: AnimationNodeStateMachinePlayback = \
    animation_tree.get("parameters/playback")

enum State { IDLE, RUN, JUMP, FALL, ATTACK }
var current_state: State = State.IDLE

func change_state(new_state: State) -> void:
    current_state = new_state

    # Sync animation state machine
    match new_state:
        State.IDLE:
            state_machine_playback.travel("Idle")
        State.RUN:
            state_machine_playback.travel("Run")
        State.JUMP:
            state_machine_playback.travel("Jump")
        State.FALL:
            state_machine_playback.travel("Fall")
        State.ATTACK:
            state_machine_playback.travel("Attack")

func _physics_process(delta: float) -> void:
    # Update blend parameters
    animation_tree.set("parameters/Run/blend_position", velocity.x / max_speed)
```

### Animation Callbacks for State Transitions
```gdscript
extends State

@onready var player: CharacterBody2D = owner
@onready var anim_player: AnimationPlayer = owner.get_node("AnimationPlayer")

func enter(_previous: State) -> void:
    anim_player.animation_finished.connect(_on_animation_finished)
    anim_player.play("attack")

func exit() -> void:
    anim_player.animation_finished.disconnect(_on_animation_finished)

func _on_animation_finished(anim_name: String) -> void:
    if anim_name == "attack":
        state_machine.transition_to("idle")
```

## Behavior Trees Alternative

### Simple Behavior Tree
```gdscript
# behavior_tree.gd
class_name BehaviorTree
extends Node

enum Status { SUCCESS, FAILURE, RUNNING }

var root: BTNode
var blackboard: Dictionary = {}

func _ready() -> void:
    root = get_child(0) as BTNode
    if root:
        root.tree = self

func _process(delta: float) -> void:
    if root:
        root.tick(delta)

# bt_node.gd
class_name BTNode
extends Node

var tree: BehaviorTree

func tick(_delta: float) -> BehaviorTree.Status:
    return BehaviorTree.Status.SUCCESS

# bt_selector.gd (OR node - succeeds if any child succeeds)
class_name BTSelector
extends BTNode

func tick(delta: float) -> BehaviorTree.Status:
    for child in get_children():
        var status := (child as BTNode).tick(delta)
        if status != BehaviorTree.Status.FAILURE:
            return status
    return BehaviorTree.Status.FAILURE

# bt_sequence.gd (AND node - succeeds if all children succeed)
class_name BTSequence
extends BTNode

func tick(delta: float) -> BehaviorTree.Status:
    for child in get_children():
        var status := (child as BTNode).tick(delta)
        if status != BehaviorTree.Status.SUCCESS:
            return status
    return BehaviorTree.Status.SUCCESS
```

## State Machine Debugging

### Debug Visualization
```gdscript
extends StateMachine

@export var debug_enabled := true

func transition_to(state_name: String) -> void:
    if debug_enabled:
        print("[StateMachine] %s -> %s" % [
            current_state.name if current_state else "null",
            state_name
        ])

    super.transition_to(state_name)

func _process(delta: float) -> void:
    super._process(delta)

    if debug_enabled and OS.is_debug_build():
        # Draw debug info
        var label := owner.get_node_or_null("DebugLabel")
        if label:
            label.text = "State: %s" % current_state.name
```

### State History
```gdscript
extends StateMachine

var state_history: Array[String] = []
var max_history := 10

func transition_to(state_name: String) -> void:
    if current_state:
        state_history.append(current_state.name)
        if state_history.size() > max_history:
            state_history.pop_front()

    super.transition_to(state_name)

func get_previous_state() -> String:
    if state_history.is_empty():
        return ""
    return state_history.back()

func return_to_previous() -> void:
    var previous := get_previous_state()
    if previous:
        state_history.pop_back()
        transition_to(previous)
```
