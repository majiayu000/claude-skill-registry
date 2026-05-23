---
name: game-developer
description: Expert in interactive entertainment, creating immersive experiences with Unity, Unreal Engine, and Godot.
---

# Game Developer

## Purpose

Provides interactive entertainment development expertise specializing in Unity (C#) and Unreal Engine (C++). Builds 2D/3D games with gameplay programming, graphics optimization, multiplayer networking, and engine architecture for immersive gaming experiences.

## When to Use

- Prototyping game mechanics (Character controllers, combat systems)
- Optimizing graphics performance (Shaders, LODs, Occlusion Culling)
- Implementing multiplayer networking (Netcode for GameObjects, Mirror, Unreal Replication)
- Designing level architecture and streaming systems
- Developing VR/AR experiences (OpenXR, ARKit)
- Creating custom editor tools and pipelines

---
---

## 2. Decision Framework

### Engine Selection

```
Which engine fits the project?
│
├─ **Unity**
│  ├─ Mobile/2D/VR? → **Yes** (Best ecosystem, smaller build size)
│  ├─ Team knows C#? → **Yes**
│  └─ Stylized graphics? → **Yes** (URP is flexible)
│
├─ **Unreal Engine 5**
│  ├─ Photorealism? → **Yes** (Nanite + Lumen out of box)
│  ├─ Open World? → **Yes** (World Partition system)
│  └─ Team knows C++? → **Yes** (Or Blueprints visual scripting)
│
└─ **Godot**
   ├─ Open Source requirement? → **Yes** (MIT License)
   ├─ Lightweight 2D? → **Yes** (Dedicated 2D engine)
   └─ Linux native dev? → **Yes** (Excellent Linux support)
```

### Multiplayer Architecture

| Model | Description | Best For |
|-------|-------------|----------|
| **Client-Hosted (P2P)** | One player is host. | Co-op games, Fighting games (with rollback). Cheap. |
| **Dedicated Server** | Authoritative server in cloud. | Competitive Shooters, MMOs. Prevents cheating. |
| **Relay Server** | Relay service (e.g., Unity Relay). | Session-based games avoiding NAT issues. |

### Graphics Pipeline (Unity)

| Pipeline | Target | Pros |
|----------|--------|------|
| **URP (Universal)** | Mobile, VR, Switch, PC | High perf, customizable, large asset store support. |
| **HDRP (High Def)** | PC, PS5, Xbox Series X | Photorealism, Volumetric lighting, Compute shaders. |
| **Built-in** | Legacy | **Avoid for new projects.** |

**Red Flags → Escalate to `graphics-engineer` (Specialist):**
- Writing custom rendering backends (Vulkan/DirectX/Metal) from scratch
- Debugging driver-level GPU crashes
- Implementing novel GI (Global Illumination) algorithms

---
---

### Workflow 2: Unreal Engine Multiplayer Setup

**Goal:** Replicate a variable (Health) from Server to Clients.

**Steps:**

1.  **Header (`Character.h`)**
    ```cpp
    UPROPERTY(ReplicatedUsing=OnRep_Health)
    float Health;

    UFUNCTION()
    void OnRep_Health();

    void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;
    ```

2.  **Implementation (`Character.cpp`)**
    ```cpp
    void AMyCharacter::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const {
        Super::GetLifetimeReplicatedProps(OutLifetimeProps);
        DOREPLIFETIME(AMyCharacter, Health);
    }

    void AMyCharacter::TakeDamage(float DamageAmount) {
        if (HasAuthority()) {
            Health -= DamageAmount;
            // OnRep_Health() called automatically on clients
            // Must call manually on Server if needed
            OnRep_Health(); 
        }
    }
    ```

3.  **Blueprint Integration**
    -   Bind UI Progress Bar to `Health` variable.
    -   Test with "Play as Client" (NetMode).

---
---

### Workflow 4: VFX Graph & Shader Graph (Visual Effects)

**Goal:** Create a GPU-accelerated particle system for a magic spell.

**Steps:**

1.  **Shader Graph (The Look)**
    -   Create `Unlit Shader Graph`.
    -   Add `Voronoi Noise` node scrolling with `Time`.
    -   Multiply with `Color` property (HDR).
    -   Connect to `Base Color` and `Alpha`.
    -   Set Surface Type to `Transparent` / `Additive`.

2.  **VFX Graph (The Motion)**
    -   Create `Visual Effect Graph` asset.
    -   **Spawn Context:** Constant Rate (1000/sec).
    -   **Initialize:** Set Lifetime (0.5s - 1s), Set Velocity (Random Direction).
    -   **Update:** Add `Turbulence` (Noise Field) to simulate wind.
    -   **Output:** Set `Quad Output` to use the Shader Graph created above.

3.  **Optimization**
    -   Use `GPU Events` if particles need to trigger gameplay logic (e.g., damage).
    -   Set `Bounds` correctly to avoid culling issues.

---
---

## 5. Anti-Patterns & Gotchas

### ❌ Anti-Pattern 1: Heavy Logic in `Update()`

**What it looks like:**
-   Performing `FindObjectOfType`, `GetComponent`, or heavy math every frame.

**Why it fails:**
-   Kills CPU performance.
-   Drains battery on mobile.

**Correct approach:**
-   Cache references in `Start()` or `Awake()`.
-   Use Coroutines or InvokeRepeating for logic that doesn't need to run every frame (e.g., AI pathfinding updates every 0.5s).

### ❌ Anti-Pattern 2: Trusting the Client

**What it looks like:**
-   Client sends "I shot player X" to server.
-   Server applies damage immediately.

**Why it fails:**
-   Cheaters can send fake packets.

**Correct approach:**
-   **Authoritative Server:** Client sends "I fired". Server calculates hit. Server tells Client "You hit".
-   Use prediction/reconciliation to mask latency for the local player.

### ❌ Anti-Pattern 3: God Classes

**What it looks like:**
-   `PlayerController.cs` has 2000 lines handling Movement, Combat, Inventory, UI, and Audio.

**Why it fails:**
-   Spaghetti code.
-   Hard to debug.

**Correct approach:**
-   **Composition:** `PlayerMovement`, `PlayerCombat`, `PlayerInventory`.
-   Use components to split responsibility.

---
---

## 7. Quality Checklist

**Performance:**
-   [ ] **Frame Rate:** Stable 60fps on target hardware.
-   [ ] **GC Alloc:** 0 bytes allocated per frame in main gameplay loop.
-   [ ] **Draw Calls:** Batched appropriately (check Frame Debugger).
-   [ ] **Load Times:** Async loading used for scenes/assets.

**Code Architecture:**
-   [ ] **Decoupled:** Systems communicate via Events/Interfaces, not hard dependencies.
-   [ ] **Clean:** No "God Classes" > 500 lines.
-   [ ] **Version Control:** Large binaries (textures, audio) handled via Git LFS.

**UX/Polish:**
-   [ ] **Controls:** Input remapping supported.
-   [ ] **UI:** Scales correctly for different aspect ratios (16:9, 21:9, Mobile Notches).
-   [ ] **Feedback:** Audio/Visual cues for all player actions (Juice).

## Examples

### Example 1: 2D Platformer Game Development

**Scenario:** Building a commercial 2D platformer with physics-based gameplay.

**Implementation:**
1. **Physics**: Custom physics engine for responsive platforming
2. **Animation**: Sprite-based animation with state machines
3. **Level Design**: Tilemap-based levels with procedural elements
4. **Audio**: Spatial audio system with adaptive music

**Technical Approach:**
```python
# Character controller pattern
class PlayerCharacter:
    def update(self, dt):
        input = self.input_system.get_player_input()
        velocity = self.physics.apply_gravity(velocity, dt)
        velocity = self.handle_movement(input, velocity)
        displacement = self.physics.integrate(velocity, dt)
        self.handle_collisions(displacement)
        self.animation.update_state(velocity, input)
```

### Example 2: VR Experience Development

**Scenario:** Creating an immersive VR experience for Oculus/Meta Quest.

**VR Implementation:**
1. **Locomotion**: Teleportation and smooth movement options
2. **Interaction**: Hand tracking with gesture recognition
3. **Optimization**: Single-pass stereo rendering
4. **Comfort**: Comfort mode options for sensitive users

**Key Considerations:**
- 72Hz minimum frame rate for comfort
- Motion sickness avoidance in design
- Hand physics for realistic interaction
- Battery optimization for standalone headsets

### Example 3: Multiplayer Battle Royale

**Scenario:** Developing a competitive multiplayer game with 100 players.

**Multiplayer Architecture:**
1. **Networking**: Client-side prediction with server reconciliation
2. **Lag Compensation**: Interpolation and extrapolation techniques
3. **Anti-Cheat**: Server-side validation, cheat detection
4. **Matchmaking**: Skill-based matchmaking with queue optimization

## Best Practices

### Game Development

- **Core Loop First**: Prototype and refine the core gameplay loop
- **Modular Architecture**: Decouple systems for maintainability
- **Performance Budgeting**: Define and monitor performance targets
- **Data-Driven Design**: Use configuration files for game balance
- **Version Control**: Handle large binary assets appropriately

### Physics and Movement

- **Determinism**: Ensure consistent physics across networked games
- **Collision Detection**: Optimize for minimal false positives
- **Character Controllers**: Separate physics from character logic
- **Ragdoll Physics**: Use for death animations and interaction
- **Performance**: Profile physics update time, optimize as needed

### Graphics and Rendering

- **Batching**: Group draw calls for GPU efficiency
- **Level of Detail**: Implement LOD for models and textures
- **Shaders**: Optimize shader complexity, use shared materials
- **Lighting**: Balance quality and performance, use baked lighting
- **Post-Processing**: Apply selectively, profile GPU impact

### Audio Implementation

- **Spatial Audio**: 3D positioning for immersion
- **Adaptive Music**: Dynamic soundtrack based on gameplay
- **Performance**: Stream large audio files, pool sound effects
- **Compression**: Use appropriate audio compression formats
- **Accessibility**: Provide audio cues as alternatives to visual feedback

### Testing and Quality

- **Playtesting**: Regular playtesting sessions for feedback
- **Performance Profiling**: Monitor frame rate, memory, load times
- **Platform Testing**: Test on target hardware, not just dev machines
- **Accessibility**: Implement accessibility features from start
- **Localization**: Plan for international markets early
