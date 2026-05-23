---
name: "Unity"
description: >
  Comprehensive Unity game development best practices guide covering architecture, C# patterns,
  performance, rendering (URP/HDRP), DOTS/ECS, multiplayer, project structure, animation,
  2D development, Shader Graph, VFX Graph, debugging, localization, accessibility, UI Toolkit, and Cinemachine.
  Use whenever the user works on Unity, writes C# for Unity, asks about MonoBehaviour,
  ScriptableObject, prefabs, Addressables, Netcode, or any Unity-related question.
  Trigger on: "Unity", "game dev", "MonoBehaviour", "prefab", "URP", "HDRP", "DOTS",
  "ECS", "SerializeField", "GameObject", "Rigidbody", "Collider", "coroutine",
  "Unity 6", "Cinemachine", "Animator", "Tilemap", "UI Toolkit", "Addressable",
  "Shader Graph", "VFX Graph", "NavMesh", "Input System", "Sprite Atlas",
  "localization", "2D platformer", or context clues suggesting Unity development.
  Also use for Unity code review, refactoring, debugging, or architecture planning.
---

# Unity Development Guide

Battle-tested best practices for Unity, from project setup to shipping. This is the entry point — for deep dives, follow the pointers to the reference files.

## Reference Files — When to Read What

| You're doing… | Read this |
|---|---|
| Organizing folders, naming assets, import settings | `references/project-structure.md` |
| Writing or reviewing C# scripts | `references/csharp-patterns.md` |
| Hunting a performance issue or optimizing | `references/performance.md` |
| Designing game architecture, patterns, systems | `references/architecture.md` |
| Setting up Git, testing, CI/CD, or building | `references/workflow.md` |
| Animation, 2D, Shader/VFX Graph | `references/specialized.md` |
| Debugging, localization, accessibility, AI/Inference Engine | `references/systems.md` |
| UI Toolkit or Cinemachine setup | `references/architecture-advanced.md` |

Read the relevant reference *before* writing code — the patterns there will save you significant rework.

---

## 1. Project Structure

Feature-based folders scale better than type-based ones because related code stays together as the project grows:

```
Assets/
├── _Project/
│   ├── Scripts/
│   │   ├── Core/          # Game loop, managers, bootstrap
│   │   ├── Player/        # Controller, input, camera
│   │   ├── Enemies/       # AI, spawners, enemy types
│   │   ├── UI/            # Views, presenters, screens
│   │   ├── Data/          # ScriptableObject definitions
│   │   └── Utils/         # Extensions, helpers
│   ├── Prefabs/
│   ├── Scenes/
│   ├── ScriptableObjects/ # Data asset instances
│   ├── Art/               # Models, Textures, Materials, Animations, Shaders
│   └── Audio/             # SFX, Music
├── Plugins/               # Third-party SDKs
└── Settings/              # Render pipeline, input, quality
```

Why `_Project/`? The underscore prefix pins it to the top of the Assets folder, keeping your code separate from imported packages and third-party assets.

Why not `Resources/`? Unity loads everything in `Resources/` into memory at startup. For anything beyond a few small assets, prefer the Addressables system instead — it loads on demand and supports remote content delivery.

For the full deep dive on folder organization, asset naming conventions, import settings, prefab/scene conventions, and how to scale from a game jam to a large project, see `references/project-structure.md`.

### Assembly Definitions

Splitting code into assemblies (`.asmdef`) is one of the highest-leverage things you can do for iteration speed. Without them, changing *any* script recompiles *everything*. With them, Unity only recompiles the affected assembly:

```
Scripts/Core/    → Game.Core.asmdef
Scripts/Player/  → Game.Player.asmdef  (refs: Game.Core)
Scripts/UI/      → Game.UI.asmdef      (refs: Game.Core)
Scripts/Utils/   → Game.Utils.asmdef   (no dependencies)
```

### Naming Conventions

| Element | Convention | Example |
|---|---|---|
| Classes / Structs | PascalCase | `PlayerController` |
| Public methods | PascalCase | `TakeDamage()` |
| Private fields | _camelCase | `_currentHealth` |
| Serialized fields | `[SerializeField]` + _camelCase | `[SerializeField] private float _speed;` |
| Interfaces | I-prefix | `IDamageable` |
| ScriptableObjects | SO suffix | `WeaponDataSO` |
| Enums | PascalCase, singular | `WeaponType { Sword, Bow }` |

---

## 2. Core C# Patterns

These are the patterns that come up in virtually every Unity project. For the full catalog (lifecycle order, async patterns, extensions, editor scripting), see `references/csharp-patterns.md`.

### The Clean MonoBehaviour

A well-structured MonoBehaviour follows a consistent layout: serialized config at the top, events, private state, then lifecycle methods. This makes the class scannable at a glance.

```csharp
public class PlayerHealth : MonoBehaviour, IDamageable
{
    [Header("Config")]
    [SerializeField] private int _maxHealth = 100;
    [SerializeField] private float _invincibilityTime = 0.5f;

    [Header("Refs")]
    [SerializeField] private HealthBarUI _healthBar;

    public event Action<int, int> OnHealthChanged;  // current, max
    public event Action OnDeath;

    private int _currentHealth;
    private bool _isInvincible;

    private void Awake() => _currentHealth = _maxHealth;

    private void Start() => _healthBar?.SetMaxHealth(_maxHealth);

    public void TakeDamage(int damage)
    {
        if (_isInvincible || _currentHealth <= 0) return;
        _currentHealth = Mathf.Max(0, _currentHealth - damage);
        OnHealthChanged?.Invoke(_currentHealth, _maxHealth);
        if (_currentHealth <= 0) { OnDeath?.Invoke(); return; }
        StartCoroutine(InvincibilityCo());
    }

    private IEnumerator InvincibilityCo()
    {
        _isInvincible = true;
        yield return new WaitForSeconds(_invincibilityTime);
        _isInvincible = false;
    }
}
```

### Key Principles

**`[SerializeField] private` over `public` fields.** Public fields break encapsulation — other scripts can write to them freely, making bugs hard to trace. `[SerializeField]` exposes the field in the Inspector while keeping it private to other code.

**One responsibility per component.** Separate `PlayerMovement`, `PlayerHealth`, `PlayerCombat` rather than a monolithic `Player`. This lets you iterate on one system without risking others, and makes components reusable.

**Cache references in `Awake()`.** `GetComponent`, `Find`, and `FindObjectOfType` are all search operations. Calling them at runtime (especially in `Update`) wastes CPU cycles. Cache them once during initialization.

**Prefer `TryGetComponent<T>()` over `GetComponent<T>()`** — it returns a bool and avoids null reference exceptions while being slightly faster.

**Events for communication, not direct coupling.** When System A needs to tell System B something happened, use a C# event or a ScriptableObject event channel. This keeps systems independent and testable.

### ScriptableObject Architecture

ScriptableObjects (SOs) are assets that live in your project and persist across scenes. They're the backbone of a well-decoupled Unity project.

**Data containers** — weapon stats, enemy configs, level settings:
```csharp
[CreateAssetMenu(menuName = "Game/Weapon Data")]
public class WeaponDataSO : ScriptableObject
{
    public string weaponName;
    [Range(1, 100)] public int damage = 10;
    [Range(0.1f, 5f)] public float attackSpeed = 1f;
    public AudioClip[] attackSounds;
}
```

**Event channels** — fully decoupled pub/sub between systems:
```csharp
[CreateAssetMenu(menuName = "Events/Void Event")]
public class VoidEventChannelSO : ScriptableObject
{
    private Action _onRaised;
    public void Raise() => _onRaised?.Invoke();
    public void Subscribe(Action fn) => _onRaised += fn;
    public void Unsubscribe(Action fn) => _onRaised -= fn;
}
```

The beauty: the publisher just calls `Raise()` on a SO asset. The subscriber references the same asset and listens. Neither knows the other exists. You wire them via the Inspector. For the full pattern set (runtime sets, shared variables), see `references/architecture.md`.

---

## 3. Performance — The Essentials

Performance problems fall into three buckets: **CPU** (too much logic per frame), **GPU** (too much to render), and **Memory** (GC pauses from allocations). The number one rule is *profile first, optimize second* — open Window > Analysis > Profiler before guessing.

**Frame budget:** 16.6ms at 60fps, 33.3ms at 30fps. Every millisecond over budget means a dropped frame.

### Zero Allocations in Hot Paths

The garbage collector (GC) pauses the game when it runs. Allocations inside `Update()`, `FixedUpdate()`, or any per-frame code are the primary cause.

```csharp
// Problematic — allocates every frame
void Update() {
    var enemies = FindObjectsOfType<Enemy>();      // array allocation
    string s = "HP: " + _health;                    // string concat
    var list = new List<int>();                      // list allocation
}

// Better — pre-allocate, reuse
private readonly StringBuilder _sb = new();
private readonly List<int> _reusable = new();

void Update() {
    _sb.Clear().Append("HP: ").Append(_health);
    _reusable.Clear();
    // ... fill _reusable as needed
}
```

### Object Pooling

Frequent `Instantiate()` / `Destroy()` causes GC spikes and memory fragmentation. Pool objects instead. Unity 6+ provides `UnityEngine.Pool.ObjectPool<T>` out of the box, or build your own with a `Queue<GameObject>`.

### Rendering Quick Wins

- **Static Batching** for non-moving objects (check "Static" in Inspector)
- **GPU Instancing** for repeated meshes (enable on Material)
- **LOD Groups** on complex 3D models
- **Baked lighting** where possible — real-time lights are expensive, especially on mobile
- **Occlusion Culling** for indoor / complex scenes

For the complete performance playbook (physics, mobile targets, texture budgets, profiling workflow, Jobs/Burst), see `references/performance.md`.

---

## 4. Architecture Decisions

### Choose by Project Scale

| Scale | Team | Recommended Approach |
|---|---|---|
| Game jam / prototype | 1-2 | Singletons + direct references |
| Small indie | 1-3 | ScriptableObject Architecture |
| Medium | 3-10 | SO Architecture + Service Locator |
| Large / Live service | 10+ | DI framework (VContainer) + ECS where needed |

Don't over-engineer for the project's scale. A game jam doesn't need dependency injection. A 2-year live-service game does.

### Key Patterns Summary

| Pattern | Use Case |
|---|---|
| **SO Event Channels** | Decoupled communication across scenes |
| **State Machine** | Player states, AI, game flow, UI screens |
| **Service Locator** | Global system access without singletons |
| **Command** | Input handling, undo/redo, replays |
| **MVP (Model-View-Presenter)** | UI systems |
| **Object Pool** | Frequently spawned/destroyed objects |

Full implementations of each pattern are in `references/architecture.md`.

---

## 5. Modern Unity (Unity 6+)

Unity 6 is the current generation. The latest LTS is **Unity 6.3** (December 2025), which is the recommended baseline for new projects. Unity follows a quarterly update cadence (6.1 → 6.2 → 6.3 LTS → 6.4+).

### Pipeline Choice

Start with **URP** unless you need specific HDRP features (ray tracing, volumetric fog, high-end console fidelity). URP covers mobile, VR, 2D, and mid-range PC. Unity is moving toward a **unified renderer** (shared Render Graph backend) to bridge URP and HDRP — but for now, switching pipelines mid-project is still painful. Decide early.

### Addressables

Replace `Resources.Load()` in production. Addressables load assets on demand, support async loading, and enable remote content delivery. The key thing to remember: always release handles when you're done, or you'll leak memory.

### New Input System

Use the new Input System package for any project that targets multiple platforms or input devices. It handles keyboard, gamepad, touch, and XR inputs through a single abstraction layer (Input Actions asset).

### API Changes in Unity 6

Several APIs were renamed for clarity:
- `Rigidbody.velocity` → **`Rigidbody.linearVelocity`** (same for Rigidbody2D)
- `Rigidbody.angularVelocity` remains but check for deprecation warnings
- Cinemachine 2.x → **Cinemachine 3.x** (`CinemachineVirtualCamera` → `CinemachineCamera`, component names changed significantly — see architecture.md §10)

### Unity 6.3 LTS Highlights

- **Box2D v3** low-level 2D physics API (multi-threaded, deterministic, visual debugging) — runs alongside existing API, will eventually replace it
- **Platform Toolkit** — unified API for accounts, achievements, save data across PS5/Xbox/Switch/Steam/Android/iOS
- **Mesh LOD** — automated LOD generation in-editor for static and skinned meshes
- **Shader Graph** — terrain shader support, 8 texture coordinate sets, template browser
- **Scriptable Audio Pipeline** — extend the audio chain with Burst-compiled C# processors
- **UI Toolkit** gains custom shaders, filters, SVG (now a core module), and improved world-space support
- **2D Renderer** can now render Mesh Renderer and Skinned Mesh Renderer alongside sprites in 2D URP
- **Sprite Atlas Analyser** tool to find packing inefficiencies

### DOTS / ECS

ECS shines when you have thousands of similar entities to process (large-scale simulation, AI for crowds, server-side multiplayer). For most indie and mid-size projects with fewer than a few hundred active entities, the traditional MonoBehaviour approach is simpler and sufficient. If you do use DOTS, keep `Unity.Mathematics` types, use `EntityCommandBuffer` for structural changes, and combine ECS (logic) with GameObjects (authoring/rendering). Unity's roadmap includes deeper ECS unification in future versions.

### Netcode for GameObjects

For multiplayer: think server-authoritative from day one. Validate all inputs on the server, use `NetworkVariable<T>` for synchronized state, and apply client-side prediction for responsive feel. Minimize bandwidth by syncing only deltas.

---

## 6. Common Anti-Patterns

| Anti-Pattern | Why it hurts | Better approach |
|---|---|---|
| God `GameManager` class | Unmaintainable, everything coupled | Split into focused systems |
| `Find*()` in Update | Linear search every frame | Cache in Awake, use events |
| Public fields everywhere | No encapsulation, hard to trace bugs | `[SerializeField] private` |
| String-based anim params | Typos cause silent failures | `Animator.StringToHash()` cached |
| Deep inheritance | Rigid, hard to refactor | Composition + interfaces |
| Hardcoded magic numbers | Can't tweak without recompiling | ScriptableObjects or `const` |

---

## 7. Quick Decision Cheat Sheet

| Decision | Default Choice | Consider Alternative When… |
|---|---|---|
| Render pipeline | URP | You need ray tracing, volumetric fog → HDRP |
| Asset loading | Addressables | Tiny project with < 20 assets → Resources |
| Input | New Input System | Editor-only tool, no gamepad needed → old Input |
| Async | `Awaitable` (Unity 6+) | Pre-Unity 6 → UniTask or Coroutines |
| Multiplayer | Netcode for GameObjects | MMO/large scale → dedicated server + ECS |
| UI (menus, HUD) | UI Toolkit | In-world UI or legacy project → uGUI Canvas |
| Camera | Cinemachine | Very simple fixed camera → manual script |
| Physics | Built-in 3D/2D Physics | 10K+ bodies → DOTS Physics |
| Particles (< 100) | Shuriken (Particle System) | 1000+ particles or GPU effects → VFX Graph |
| Particles (1000+) | VFX Graph | Mobile without compute shaders → Shuriken |
| Localization | Unity Localization package | Tiny jam project → hardcoded strings |
| Version control | Git + LFS | Large team, binary-heavy → Perforce / Plastic |
| Animation blending | Blend Trees | Discrete states with no blending → simple transitions |
| 2D Physics | Built-in Physics2D | High-perf/deterministic needs → Box2D v3 low-level API (6.3+) |
| Cross-platform services | Platform Toolkit (6.3+) | Older Unity → manual per-platform SDKs |

---

## Skills connexes

| Besoin | Skill |
|--------|-------|
| Generer du code C# production | `/unity-code-gen` (Unity Code Gen) |
| Tester le code | `/unity-test` (Unity Test) |
| Debugger un probleme | `/unity-debug` (Unity Debug) |
| Prototyper rapidement | `/proto` (Unity Rapid Proto) |
| Audit de performance | `/perf-audit` (Unity Perf Audit) |
| Refactorer du code existant | `/unity-refactor` (Unity Refactor) |
| Custom editor tools | `/editor` (Unity Editor Tools) |
| Shaders HLSL | `/shader` (Unity Shader Generator) |
| UI avec UI Toolkit | `/uitk` (Unity UI Toolkit) |
| Multiplayer NGO | `/netcode` (Unity Multiplayer) |
| Asset loading async | `/addressables` (Unity Addressables) |
| Animation avancee | `/anim` (Unity Animation) |
| ECS et Jobs | `/dots` (Unity DOTS) |
| Build et CI/CD | `/build-config` (Unity Build & CI/CD) |
| Systeme audio | `/unity-audio` (Unity Audio) |
| Developpement 2D | `/2d` (Unity 2D) |
| Sauvegarde et persistence | `/unity-save` (Unity Save System) |
