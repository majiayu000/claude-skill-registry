---
name: unity
description: |
  Unity game engine guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Unity projects, or when the user mentions Unity game development.
  Provides MonoBehaviour patterns, component architecture, physics, UI, and scripting guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: csharp
  extensions: ".cs"
---

# Unity Guide

> Applies to: Unity 2022 LTS+, C#, Games, VR/AR, Simulations, Interactive Media

## Core Principles

1. **Component-Based Architecture**: One MonoBehaviour = one responsibility
2. **Composition Over Inheritance**: Combine components on GameObjects; avoid deep class hierarchies
3. **Data-Driven Design**: Use ScriptableObjects for configuration and shared data
4. **Event-Driven Communication**: Decouple systems with C# events, UnityEvents, or ScriptableObject events
5. **Cache Everything**: Never call `Find`, `GetComponent`, or allocate in `Update`

## Guardrails

### MonoBehaviour Rules

- Keep `Update()` bodies under 20 lines; delegate to focused methods
- Cache all `GetComponent` results in `Awake()` (never call in `Update`)
- Subscribe to events in `OnEnable`, unsubscribe in `OnDisable`
- Use `[SerializeField] private` instead of `public` for inspector fields
- Apply `[RequireComponent]` attribute when a script depends on another component
- Never use `GameObject.Find` or `FindObjectOfType` at runtime (cache in `Start`/`Awake`)
- Use `CompareTag("Tag")` instead of `gameObject.tag == "Tag"` (avoids GC allocation)

### Project Organization

- Prefix project folder with `_Project/` to keep it at top of Assets
- Group assets by feature, not by type (e.g., `Player/` contains scripts, prefabs, materials)
- Keep `Resources/` minimal; prefer Addressables for runtime asset loading
- Store all runtime configuration in ScriptableObjects under `_Project/ScriptableObjects/`
- Place editor-only scripts inside `Editor/` folders

### Performance

- Object pool frequently spawned objects (bullets, particles, enemies)
- Avoid allocations in hot paths (`Update`, `FixedUpdate`, physics callbacks)
- Reuse collections instead of creating new ones each frame
- Use `StringBuilder` for string operations; never concatenate in loops
- Prefer value types (`struct`) for small, short-lived data
- Set physics layers properly; disable unnecessary collision pairs in Physics settings
- Use `Time.deltaTime` for frame-independent movement, `Time.fixedDeltaTime` in `FixedUpdate`

### Naming Conventions

- Scripts: `PascalCase.cs` matching the class name (e.g., `PlayerController.cs`)
- Private fields: `camelCase` (e.g., `moveSpeed`, `jumpHeight`)
- Serialized fields: prefix with `[Header("Section")]` for inspector grouping
- Interfaces: `IPrefixed` (e.g., `IDamageable`, `IInteractable`)
- ScriptableObjects: `PascalCase` with descriptive asset menu name
- Scenes: `PascalCase` (e.g., `MainMenu.unity`, `Level01.unity`)
- Prefabs: `PascalCase` matching the primary component (e.g., `EnemyGoblin.prefab`)

## Project Structure

```
MyGame/
├── Assets/
│   ├── _Project/
│   │   ├── Art/                    # Materials, Models, Sprites, Textures
│   │   ├── Audio/                  # Music, SFX
│   │   ├── Prefabs/                # Characters, Environment, UI
│   │   ├── Scenes/
│   │   ├── Scripts/
│   │   │   ├── Core/              # GameManager, SceneLoader, ServiceLocator
│   │   │   ├── Player/            # PlayerController, PlayerHealth, PlayerInput
│   │   │   ├── Enemies/           # AI, spawning, enemy types
│   │   │   ├── UI/                # HUD, menus, dialogs
│   │   │   ├── Systems/           # Audio, save, pooling, events
│   │   │   └── Data/              # ScriptableObjects, serializable structs
│   │   ├── ScriptableObjects/     # Items, Enemies, Settings assets
│   │   └── Settings/              # InputActions.inputactions
│   ├── Plugins/
│   └── Resources/                  # Keep minimal; prefer Addressables
├── Packages/manifest.json
├── ProjectSettings/
├── Tests/                          # EditMode/ and PlayMode/
└── .gitignore
```

## MonoBehaviour Lifecycle

Understanding execution order is critical for correct initialization.

```csharp
public class LifecycleExample : MonoBehaviour
{
    // INITIALIZATION (called once)
    private void Awake()    { /* Cache components, init self. Runs even if disabled. */ }
    private void OnEnable() { /* Subscribe to events. Runs when enabled. */ }
    private void Start()    { /* Cross-object setup. Runs before first Update, only if enabled. */ }

    // UPDATE LOOP (called every frame/tick)
    private void Update()      { /* Game logic, input. Use Time.deltaTime. */ }
    private void FixedUpdate() { /* Physics. Constant timestep. Rigidbody movement here. */ }
    private void LateUpdate()  { /* Camera follow, post-processing. After all Updates. */ }

    // CLEANUP
    private void OnDisable()  { /* Unsubscribe events. */ }
    private void OnDestroy()  { /* Final cleanup. */ }
}
```

**Key rules**: `Awake` initializes self-references. `Start` accesses other objects. `OnEnable`/`OnDisable` always pair event subscriptions. Physics in `FixedUpdate` only.

## Component Patterns

### Singleton (DontDestroyOnLoad)

```csharp
public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }

    public GameState CurrentState { get; private set; }
    public event System.Action<GameState> OnStateChanged;

    private void Awake()
    {
        if (Instance != null && Instance != this) { Destroy(gameObject); return; }
        Instance = this;
        DontDestroyOnLoad(gameObject);
    }

    public void SetState(GameState state)
    {
        if (CurrentState == state) return;
        CurrentState = state;
        OnStateChanged?.Invoke(state);
    }
}
```

Use singletons sparingly. Prefer Service Locator or dependency injection for testability.

### Service Locator

```csharp
public static class ServiceLocator
{
    private static readonly Dictionary<Type, object> Services = new();

    public static void Register<T>(T service) where T : class
        => Services[typeof(T)] = service;

    public static T Get<T>() where T : class
        => Services.TryGetValue(typeof(T), out var s) ? s as T : null;

    public static void Clear() => Services.Clear();
}

// Register in bootstrapper Awake(), resolve anywhere
```

### Health / Damageable Interface

```csharp
public interface IDamageable
{
    void TakeDamage(int amount);
    bool IsAlive { get; }
}

public class Health : MonoBehaviour, IDamageable
{
    [SerializeField] private int maxHealth = 100;
    public int Current { get; private set; }
    public bool IsAlive => Current > 0;

    public UnityEvent<int, int> OnHealthChanged; // current, max
    public UnityEvent OnDeath;

    private void Start() { Current = maxHealth; OnHealthChanged?.Invoke(Current, maxHealth); }

    public void TakeDamage(int amount)
    {
        if (!IsAlive) return;
        Current = Mathf.Max(0, Current - amount);
        OnHealthChanged?.Invoke(Current, maxHealth);
        if (Current <= 0) OnDeath?.Invoke();
    }

    public void Heal(int amount)
    {
        if (!IsAlive) return;
        Current = Mathf.Min(maxHealth, Current + amount);
        OnHealthChanged?.Invoke(Current, maxHealth);
    }
}
```

## Input Handling (New Input System)

```csharp
[RequireComponent(typeof(CharacterController))]
public class PlayerController : MonoBehaviour
{
    [Header("Movement")]
    [SerializeField] private float moveSpeed = 5f;
    [SerializeField] private float jumpHeight = 2f;
    [SerializeField] private float gravity = -15f;

    private CharacterController controller;
    private PlayerInput playerInput;
    private Vector2 moveInput;
    private Vector3 velocity;

    private void Awake()
    {
        controller = GetComponent<CharacterController>();
        playerInput = GetComponent<PlayerInput>();
    }

    private void OnEnable()
    {
        playerInput.actions["Move"].performed += ctx => moveInput = ctx.ReadValue<Vector2>();
        playerInput.actions["Move"].canceled += ctx => moveInput = Vector2.zero;
        playerInput.actions["Jump"].performed += _ => TryJump();
    }

    private void Update() => HandleMovement();

    private void HandleMovement()
    {
        if (controller.isGrounded && velocity.y < 0) velocity.y = -2f;

        var move = (transform.forward * moveInput.y + transform.right * moveInput.x) * moveSpeed;
        velocity.y += gravity * Time.deltaTime;
        controller.Move((move + velocity) * Time.deltaTime);
    }

    private void TryJump()
    {
        if (controller.isGrounded)
            velocity.y = Mathf.Sqrt(jumpHeight * -2f * gravity);
    }
}
```

Always use the new Input System package. Define actions in `.inputactions` asset, not hardcoded `KeyCode` checks.

## Physics Basics

```csharp
// Move Rigidbody in FixedUpdate only
private void FixedUpdate()
{
    rb.MovePosition(rb.position + moveDirection * speed * Time.fixedDeltaTime);
}

// Collision detection (requires Collider + Rigidbody on at least one)
private void OnCollisionEnter(Collision collision)
{
    if (collision.gameObject.CompareTag("Enemy"))
    {
        var damageable = collision.gameObject.GetComponent<IDamageable>();
        damageable?.TakeDamage(10);
    }
}

// Trigger detection (Collider with isTrigger = true)
private void OnTriggerEnter(Collider other)
{
    if (other.CompareTag("Pickup"))
        CollectItem(other.gameObject);
}
```

**Rules**: Rigidbody movement in `FixedUpdate`. Use layers to filter collisions. Prefer `CompareTag` over string comparison. Set Rigidbody interpolation for smooth rendering.

## UI / Canvas

```csharp
public class HUDController : MonoBehaviour
{
    [Header("Health")]
    [SerializeField] private Slider healthBar;
    [SerializeField] private TextMeshProUGUI healthText;

    [Header("Score")]
    [SerializeField] private TextMeshProUGUI scoreText;

    public void UpdateHealth(int current, int max)
    {
        healthBar.value = (float)current / max;
        healthText.text = $"{current}/{max}";
    }

    public void UpdateScore(int score) => scoreText.text = score.ToString("N0");
}
```

**UI guidelines**: Use TextMeshPro for all text (never legacy UI.Text). Anchor UI elements properly for responsive layouts. Use Canvas Groups for fade effects. Keep UI logic in dedicated controllers, not game logic scripts.

## ScriptableObjects

```csharp
[CreateAssetMenu(fileName = "New Item", menuName = "Game/Items/Item Data")]
public class ItemData : ScriptableObject
{
    [Header("Basic Info")]
    public string itemName;
    [TextArea(3, 5)] public string description;
    public Sprite icon;
    public ItemType itemType;
    public Rarity rarity;

    [Header("Properties")]
    public int maxStack = 99;
    public int buyPrice;
    public int sellPrice;
}
```

Use ScriptableObjects for: item definitions, enemy configs, game settings, event channels, audio libraries. They live as `.asset` files, are editable in the Inspector, and shared across scenes without singletons.

### ScriptableObject Event Channel

```csharp
[CreateAssetMenu(menuName = "Game/Events/Game Event")]
public class GameEvent : ScriptableObject
{
    private readonly List<System.Action> listeners = new();

    public void Raise() { for (int i = listeners.Count - 1; i >= 0; i--) listeners[i](); }
    public void Register(System.Action listener) => listeners.Add(listener);
    public void Unregister(System.Action listener) => listeners.Remove(listener);
}
```

Wire listeners in `OnEnable`/`OnDisable`. This decouples systems completely -- the publisher does not know about subscribers.

## Object Pooling

```csharp
public class ObjectPool<T> where T : Component
{
    private readonly T prefab;
    private readonly Transform parent;
    private readonly Queue<T> pool = new();

    public ObjectPool(T prefab, Transform parent, int initialSize)
    {
        this.prefab = prefab;
        this.parent = parent;
        for (int i = 0; i < initialSize; i++) pool.Enqueue(CreateInstance());
    }

    public T Get(Vector3 pos, Quaternion rot)
    {
        var obj = pool.Count > 0 ? pool.Dequeue() : CreateInstance();
        obj.transform.SetPositionAndRotation(pos, rot);
        obj.gameObject.SetActive(true);
        return obj;
    }

    public void Return(T obj) { obj.gameObject.SetActive(false); pool.Enqueue(obj); }

    private T CreateInstance()
    {
        var obj = Object.Instantiate(prefab, parent);
        obj.gameObject.SetActive(false);
        return obj;
    }
}
```

Pool bullets, particles, enemies -- anything spawned frequently. Never call `Instantiate`/`Destroy` in tight loops.

## Testing

### Edit Mode Tests (Pure Logic)

```csharp
using NUnit.Framework;

[TestFixture]
public class InventoryTests
{
    [Test]
    public void AddItem_WhenSlotAvailable_ReturnsTrue()
    {
        var inventory = new Inventory(maxSlots: 10);
        Assert.IsTrue(inventory.AddItem(itemData, quantity: 1));
    }

    [Test]
    public void AddItem_WhenFull_ReturnsFalse()
    {
        var inventory = new Inventory(maxSlots: 0);
        Assert.IsFalse(inventory.AddItem(itemData, quantity: 1));
    }
}
```

### Play Mode Tests (MonoBehaviour)

```csharp
using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

[TestFixture]
public class HealthTests
{
    [UnityTest]
    public IEnumerator TakeDamage_ReducesCurrentHealth()
    {
        var go = new GameObject();
        var health = go.AddComponent<Health>();
        yield return null; // Wait for Start()

        health.TakeDamage(25);
        Assert.AreEqual(75, health.Current);

        Object.Destroy(go);
    }
}
```

**Testing rules**: Edit Mode for pure logic (no MonoBehaviour dependency). Play Mode for component behavior that requires the Unity lifecycle. Always `Destroy` test GameObjects in `TearDown` or inline.

## Commands

```bash
# Command-line build (macOS)
/Applications/Unity/Hub/Editor/2022.3.0f1/Unity.app/Contents/MacOS/Unity \
  -quit -batchmode -projectPath ~/Projects/MyGame \
  -buildTarget StandaloneOSX -buildPath Builds/macOS/MyGame.app

# Run Edit Mode tests
Unity -runTests -projectPath /path/to/project \
  -testResults results.xml -testPlatform EditMode

# Run Play Mode tests
Unity -runTests -projectPath /path/to/project \
  -testResults results.xml -testPlatform PlayMode

# Export package
Unity -exportPackage Assets/MyPlugin MyPlugin.unitypackage
```

## Common Mistakes

```csharp
// BAD: Finding objects every frame
void Update() { var player = GameObject.Find("Player"); }
// GOOD: Cache in Awake/Start
private Transform player;
void Awake() => player = GameObject.Find("Player").transform;

// BAD: String tag comparison (GC alloc)
if (gameObject.tag == "Player") { }
// GOOD: CompareTag (no allocation)
if (gameObject.CompareTag("Player")) { }

// BAD: Allocating in Update
void Update() { var list = new List<Enemy>(); }
// GOOD: Reuse collections
private readonly List<Enemy> enemies = new();
void Update() { enemies.Clear(); /* reuse */ }

// BAD: Moving Rigidbody in Update
void Update() { rb.MovePosition(target); }
// GOOD: Physics in FixedUpdate
void FixedUpdate() { rb.MovePosition(target); }
```

## Advanced Topics

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Animation, networking, editor scripting, performance profiling, state machines, save systems, advanced pooling

## External References

- [Unity Documentation](https://docs.unity3d.com/)
- [Unity Learn](https://learn.unity.com/)
- [Unity Scripting API](https://docs.unity3d.com/ScriptReference/)
- [Game Programming Patterns](https://gameprogrammingpatterns.com/)
- [Unity Best Practices](https://unity.com/how-to)
