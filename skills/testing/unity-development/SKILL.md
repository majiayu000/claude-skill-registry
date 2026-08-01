---
name: unity-development
description: Comprehensive guide for Unity development. Provides architecture patterns,
  MCP tool selection, and composite task workflows. Parent skill always referenced
  for Unity-related tasks. See child skills fo
---

---
name: unity-development
description: Comprehensive guide for Unity development. Provides architecture patterns, MCP tool selection, and composite task workflows. Parent skill always referenced for Unity-related tasks. See child skills for detailed implementation. Use when: Unity development in general, C# editing, scene operations, UI implementation, asset management, PlayMode testing
allowed-tools: Read, Grep, Glob
---

# Unity Development Guide

A comprehensive guide for Unity development. This skill serves as **always-referenced parent skill**, providing common patterns and tool selection guidance.

## Architecture Patterns

### Fail-Fast Principle

**Do not write null checks. Use objects directly when their existence is assumed.**

```csharp
// NG: Forbidden pattern
if (component != null) { component.DoSomething(); }
if (gameObject != null) { gameObject.SetActive(false); }
if (service != null) { service.Execute(); }

// OK: Correct pattern - direct usage
GetComponent<Rigidbody>().velocity = Vector3.zero;
GameService.Initialize();
target.position = Vector3.zero;
```

**Applies to**:
- Null check after `GetComponent<T>()`
- Null check after `Find*()`
- Null check after `[Inject]`

### No GetComponent in Update

**GetComponent every frame causes GC allocation and performance degradation. Cache in Awake.**

```csharp
// NG: GC allocation every frame
void Update()
{
    GetComponent<Rigidbody>().velocity = input;
}

// OK: Cache in Awake
private Rigidbody _rb;

void Awake()
{
    _rb = GetComponent<Rigidbody>();
}

void Update()
{
    _rb.velocity = input;
}
```

### UniTask Patterns

**Use UniTask instead of coroutines. async void is forbidden.**

```csharp
using Cysharp.Threading.Tasks;

// NG: async void
async void Start()
{
    await DoWorkAsync();
}

// OK: UniTaskVoid + destroyCancellationToken
async UniTaskVoid Start()
{
    await DoWorkAsync(destroyCancellationToken);
}

// OK: When return value is needed
async UniTask<int> CalculateAsync(CancellationToken ct)
{
    await UniTask.Delay(1000, cancellationToken: ct);
    return 42;
}
```

**Best Practices**:
- Use `destroyCancellationToken` for auto-cancel on GameObject destruction
- `UniTask.Delay` > `Task.Delay` (zero allocation)
- `UniTask.WhenAll` for parallel execution

### VContainer DI

**Use VContainer for dependency injection. Constructor injection recommended.**

```csharp
// Interface definition
public interface IPlayerService
{
    void Initialize();
}

// Implementation class
public class PlayerService : IPlayerService
{
    public void Initialize() { /* ... */ }
}

// Consumer (MonoBehaviour)
public class GameManager : MonoBehaviour
{
    [Inject] private readonly IPlayerService _playerService;

    void Start()
    {
        _playerService.Initialize();
    }
}

// LifetimeScope configuration
public class GameLifetimeScope : LifetimeScope
{
    protected override void Configure(IContainerBuilder builder)
    {
        builder.Register<IPlayerService, PlayerService>(Lifetime.Singleton);
        builder.RegisterComponentInHierarchy<GameManager>();
    }
}
```

**Lifetime Selection**:
- `Lifetime.Singleton` - One instance for entire app
- `Lifetime.Scoped` - One instance per scene
- `Lifetime.Transient` - New instance each time

---

## MCP Tool Categories

### C# Code Editing

| Tool | Purpose | Usage Condition |
|------|---------|-----------------|
| `edit_snippet` | Lightweight edit | Diff within 80 characters |
| `edit_structured` | Structured edit | Method body replacement, member addition |
| `get_symbols` | Symbol list | Required before editing |
| `find_symbol` | Symbol search | Find symbol by name |
| `find_refs` | Reference search | Before refactoring |
| `read` | Read code | Check file contents |
| `search` | Pattern search | Regex search |
| `create_class` | Create class | New file |
| `rename_symbol` | Rename | Project-wide |
| `remove_symbol` | Remove symbol | Delete unused code |

### Scene & GameObject

| Tool | Purpose |
|------|---------|
| `get_hierarchy` | Get hierarchy |
| `create_gameobject` | Create GameObject |
| `modify_gameobject` | Modify GameObject |
| `delete_gameobject` | Delete GameObject |
| `find_gameobject` | Find GameObject |
| `add_component` | Add component |
| `modify_component` | Modify component |
| `remove_component` | Remove component |
| `list_components` | List components |

### Asset Management

| Tool | Purpose |
|------|---------|
| `create_prefab` | Create prefab |
| `modify_prefab` | Modify prefab |
| `instantiate_prefab` | Instantiate prefab |
| `create_material` | Create material |
| `modify_material` | Modify material |
| `manage_asset_database` | Asset operations |
| `addressables_manage` | Addressables management |

### PlayMode & Testing

| Tool | Purpose |
|------|---------|
| `play_game` | Start PlayMode |
| `stop_game` | Stop PlayMode |
| `pause_game` | Pause |
| `input_keyboard` | Keyboard input |
| `input_mouse` | Mouse input |
| `input_gamepad` | Gamepad input |
| `capture_screenshot` | Screenshot |
| `run_tests` | Run tests |

### UI Systems

| System | Purpose | Detail Skill |
|--------|---------|--------------|
| uGUI | Game UI (Canvas/EventSystem) | `unity-game-ugui-design` |
| UI Toolkit | Modern UI (Runtime/Editor) | `unity-game-ui-toolkit-design` |
| IMGUI | Editor extensions only | `unity-editor-imgui-design` |

---

## Composite Workflow Examples

### Example 1: Scene Transition with UI Button

**Required operations**: UI creation + Scene management + C# script

```javascript
// 1. Create button GameObject
mcp__unity-mcp-server__create_gameobject({
  name: "StartButton",
  parentPath: "/Canvas"
})

// 2. Add Button component
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Canvas/StartButton",
  componentType: "Button"
})

// 3. Create click handler script
mcp__unity-mcp-server__create_class({
  path: "Assets/Scripts/UI/StartButtonHandler.cs",
  className: "StartButtonHandler",
  baseType: "MonoBehaviour",
  namespace: "Game.UI"
})

// 4. Add OnClick implementation
mcp__unity-mcp-server__edit_structured({
  path: "Assets/Scripts/UI/StartButtonHandler.cs",
  symbolName: "StartButtonHandler",
  operation: "insert_after",
  newText: `
    public void OnStartClicked()
    {
        SceneManager.LoadScene("GameScene");
    }
`
})
```

### Example 2: Create Enemy Character

**Required operations**: GameObject + Components + C# script + Prefab

```javascript
// 1. Create enemy GameObject
mcp__unity-mcp-server__create_gameobject({
  name: "Enemy",
  primitiveType: "capsule",
  position: { x: 0, y: 1, z: 0 }
})

// 2. Add components
mcp__unity-mcp-server__add_component({
  gameObjectPath: "/Enemy",
  componentType: "Rigidbody"
})

// 3. Create enemy script
mcp__unity-mcp-server__create_class({
  path: "Assets/Scripts/Enemies/EnemyController.cs",
  className: "EnemyController",
  baseType: "MonoBehaviour"
})

// 4. Add AI implementation
mcp__unity-mcp-server__edit_structured({
  path: "Assets/Scripts/Enemies/EnemyController.cs",
  symbolName: "EnemyController",
  operation: "insert_after",
  newText: `
    [SerializeField] private float _speed = 3f;
    private Transform _target;

    void Update()
    {
        if (_target != null)
            transform.position = Vector3.MoveTowards(
                transform.position,
                _target.position,
                _speed * Time.deltaTime
            );
    }
`
})

// 5. Convert to prefab
mcp__unity-mcp-server__create_prefab({
  gameObjectPath: "/Enemy",
  prefabPath: "Assets/Prefabs/Enemies/Enemy.prefab"
})
```

### Example 3: PlayMode Testing

**Required operations**: Test creation + PlayMode control + Input simulation

```javascript
// 1. Create test class
mcp__unity-mcp-server__create_class({
  path: "Assets/Tests/PlayMode/PlayerMovementTests.cs",
  className: "PlayerMovementTests",
  namespace: "Tests.PlayMode",
  usings: "NUnit.Framework,UnityEngine.TestTools,System.Collections"
})

// 2. Add PlayMode test implementation
mcp__unity-mcp-server__edit_structured({
  path: "Assets/Tests/PlayMode/PlayerMovementTests.cs",
  symbolName: "PlayerMovementTests",
  operation: "insert_after",
  newText: `
    [UnityTest]
    public IEnumerator Player_MovesForward_WhenWPressed()
    {
        var player = Object.FindObjectOfType<PlayerController>();
        var startPos = player.transform.position;

        yield return null;

        // Simulate W key input
        // Use input_keyboard tool during test execution

        yield return new WaitForSeconds(0.5f);

        Assert.Greater(player.transform.position.z, startPos.z);
    }
`
})

// 3. Run tests
mcp__unity-mcp-server__run_tests({
  testMode: "PlayMode",
  filter: "PlayerMovementTests"
})
```

---

## Child Skill Reference

Refer to the following child skills when detailed implementation patterns are needed:

| Skill | Purpose | When to Reference |
|-------|---------|-------------------|
| `unity-csharp-editing` | C# editing, TDD, refactoring | During code editing |
| `unity-scene-management` | Scene & GameObject operations | During scene construction |
| `unity-asset-management` | Prefabs, materials, Addressables | During asset management |
| `unity-playmode-testing` | PlayMode, input simulation | During test execution |
| `unity-game-ugui-design` | uGUI (Canvas/EventSystem) | During game UI implementation |
| `unity-game-ui-toolkit-design` | UI Toolkit (Runtime) | During modern UI implementation |
| `unity-editor-imgui-design` | IMGUI (EditorWindow/Inspector) | During editor extension |

---

## Quick Decision Tree

```
Unity Development Task
├─ Need code editing?
│   ├─ YES → edit_snippet / edit_structured
│   │         Details: unity-csharp-editing
│   └─ NO → Next
├─ Need scene/GameObject operations?
│   ├─ YES → create_gameobject / add_component
│   │         Details: unity-scene-management
│   └─ NO → Next
├─ Need asset operations?
│   ├─ YES → create_prefab / addressables_manage
│   │         Details: unity-asset-management
│   └─ NO → Next
├─ Need UI implementation?
│   ├─ Game UI → unity-game-ugui-design or unity-game-ui-toolkit-design
│   └─ Editor UI → unity-editor-imgui-design
└─ Need testing/verification?
    └─ YES → play_game / run_tests
              Details: unity-playmode-testing
```
