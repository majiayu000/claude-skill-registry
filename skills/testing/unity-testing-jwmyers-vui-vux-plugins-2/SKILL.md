---
name: unity-testing
description: This skill should be used when the user asks about "tests", "unit tests", "EditMode tests", "PlayMode tests", "Test Runner", "test coverage", "NUnit", "Assert", "test fixtures", "writing tests", "running tests", or discusses Unity testing patterns and practices.
version: 0.3.0
---

# Unity Testing

Expert knowledge of Unity testing patterns, EditMode/PlayMode tests, and test-driven development for the Zero-Day Attack project.

## Test Types

### EditMode Tests

Run without entering Play mode - fast iteration:

| Property | Value                                     |
| -------- | ----------------------------------------- |
| Location | `Assets/Tests/Editor/`                    |
| Assembly | `*.Tests.Editor.asmdef`                   |
| Speed    | Fast (no scene loading)                   |
| Use For  | Pure logic, data validation, calculations |

### PlayMode Tests

Run in simulated Play mode - test runtime behavior:

| Property | Value                                          |
| -------- | ---------------------------------------------- |
| Location | `Assets/Tests/Runtime/`                        |
| Assembly | `*.Tests.Runtime.asmdef`                       |
| Speed    | Slower (scene setup required)                  |
| Use For  | MonoBehaviour, scene interactions, integration |

## Project Test Structure

```text
Assets/Tests/
├── Editor/
│   ├── BoardLayoutConfigTests.cs    # LayoutConfig validation
│   └── TileDatabaseTests.cs         # Database integrity
└── Runtime/
    ├── CoordinateConversionTests.cs # Grid-to-world conversion
    └── GameInitializationTests.cs   # Startup and state
```

## Writing EditMode Tests

### EditMode Test Basic Structure

```csharp
using NUnit.Framework;
using ZeroDayAttack.Config;

namespace ZeroDayAttack.Tests.Editor
{
    [TestFixture]
    public class LayoutConfigTests
    {
        [Test]
        public void GridSize_ShouldBeFive()
        {
            Assert.AreEqual(5, LayoutConfig.GridSize);
        }

        [Test]
        public void ScreenDimensions_ShouldMatch1920x1080()
        {
            // At 100 PPU: 1920/100 = 19.2, 1080/100 = 10.8
            Assert.AreEqual(19.2f, LayoutConfig.ScreenWidth, 0.001f);
            Assert.AreEqual(10.8f, LayoutConfig.ScreenHeight, 0.001f);
        }

        [Test]
        public void CameraOrthoSize_ShouldBeHalfHeight()
        {
            float expectedOrtho = LayoutConfig.ScreenHeight / 2f;
            Assert.AreEqual(expectedOrtho, LayoutConfig.CameraOrthoSize, 0.001f);
        }
    }
}
```

### Testing ScriptableObjects

```csharp
using NUnit.Framework;
using UnityEngine;
using ZeroDayAttack.Core.Data;

namespace ZeroDayAttack.Tests.Editor
{
    [TestFixture]
    public class TileDatabaseTests
    {
        private TileDatabase database;

        [OneTimeSetUp]
        public void LoadDatabase()
        {
            database = Resources.Load<TileDatabase>("TileDatabase");
        }

        [Test]
        public void Database_ShouldLoad()
        {
            Assert.IsNotNull(database, "TileDatabase not found in Resources");
        }

        [Test]
        public void Database_ShouldHave25Tiles()
        {
            Assert.AreEqual(25, database.Tiles.Count);
        }

        [Test]
        public void AllTiles_ShouldHaveSprites()
        {
            foreach (var tile in database.Tiles)
            {
                Assert.IsNotNull(tile.TileSprite,
                    $"Tile {tile.TileId} missing sprite");
            }
        }
    }
}
```

## Writing PlayMode Tests

### PlayMode Test Basic Structure

```csharp
using System.Collections;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;
using ZeroDayAttack.View;

namespace ZeroDayAttack.Tests.Runtime
{
    [TestFixture]
    public class TileManagerTests
    {
        private TileManager tileManager;

        [UnitySetUp]
        public IEnumerator SetUp()
        {
            // Create test object
            var go = new GameObject("TileManager");
            tileManager = go.AddComponent<TileManager>();
            yield return null;  // Wait one frame
        }

        [UnityTearDown]
        public IEnumerator TearDown()
        {
            if (tileManager != null)
            {
                Object.Destroy(tileManager.gameObject);
            }
            yield return null;
        }

        [UnityTest]
        public IEnumerator Instance_ShouldBeSet()
        {
            yield return null;
            Assert.IsNotNull(TileManager.Instance);
        }

        [UnityTest]
        public IEnumerator GridToWorld_CenterTile_ShouldBeAtOrigin()
        {
            yield return null;
            var worldPos = tileManager.GetWorldPosition(2, 2);
            Assert.AreEqual(0f, worldPos.x, 0.001f);
            Assert.AreEqual(0f, worldPos.y, 0.001f);
        }
    }
}
```

### Testing with Scenes

```csharp
using UnityEngine.SceneManagement;

[UnityTest]
public IEnumerator GameplayScene_ShouldLoad()
{
    SceneManager.LoadScene("GameplayScene");
    yield return null;  // Wait for load

    var gameManager = GameObject.FindObjectOfType<GameManager>();
    Assert.IsNotNull(gameManager);
}
```

## Common Assertions

### Value Assertions

```csharp
Assert.AreEqual(expected, actual);
Assert.AreEqual(expected, actual, delta);  // For floats
Assert.AreNotEqual(notExpected, actual);
Assert.IsTrue(condition);
Assert.IsFalse(condition);
```

### Null Assertions

```csharp
Assert.IsNull(obj);
Assert.IsNotNull(obj);
```

### Collection Assertions

```csharp
Assert.Contains(item, collection);
Assert.IsEmpty(collection);
Assert.IsNotEmpty(collection);
CollectionAssert.AreEqual(expected, actual);
CollectionAssert.AreEquivalent(expected, actual);  // Order-independent
```

### Exception Assertions

```csharp
Assert.Throws<ArgumentException>(() => {
    SomeMethod(invalidArg);
});

Assert.DoesNotThrow(() => {
    SomeMethod(validArg);
});
```

## Running Tests via MCP

### Run All EditMode Tests

```json
{
  "testMode": "EditMode"
}
```

### Run Specific Test Class

```json
{
  "testMode": "EditMode",
  "testClass": "LayoutConfigTests"
}
```

### Run Specific Test Method

```json
{
  "testMode": "EditMode",
  "testMethod": "ZeroDayAttack.Tests.Editor.LayoutConfigTests.GridSize_ShouldBeFive"
}
```

### Useful Options

```json
{
  "testMode": "EditMode",
  "includePassingTests": false, // Only show failures
  "includeMessages": true, // Include assertion messages
  "includeStacktrace": true, // Include stack traces
  "includeLogs": true // Include console logs
}
```

## Test Naming Conventions

### Pattern: `Method_Scenario_ExpectedResult`

```csharp
[Test] public void GridToWorld_CenterTile_ReturnsOrigin() { }
[Test] public void PlaceTile_InvalidPosition_ThrowsException() { }
[Test] public void MoveToken_ValidPath_UpdatesPosition() { }
```

### Test Class Naming

```csharp
public class GameManagerTests { }      // Tests for GameManager
public class TileValidationTests { }   // Tests for tile validation logic
public class PathFindingTests { }      // Tests for path algorithms
```

## Test Categories

Organize tests with categories:

```csharp
[Test]
[Category("FastTests")]
public void QuickCalculation_Test() { }

[Test]
[Category("Integration")]
public void SceneSetup_Test() { }
```

Run by category:

```json
{
  "testMode": "EditMode",
  "testCategory": "FastTests"
}
```

## Testing Best Practices

### Arrange-Act-Assert Pattern

```csharp
[Test]
public void PathSegment_RotateBy90_UpdatesNodes()
{
    // Arrange
    var segment = new PathSegment(EdgeNode.Left, EdgeNode.Top, PathColor.Blue);

    // Act
    var rotated = segment.Rotate(90);

    // Assert
    Assert.AreEqual(EdgeNode.Top, rotated.From);
    Assert.AreEqual(EdgeNode.Right, rotated.To);
}
```

### One Assertion Per Test (When Practical)

```csharp
// Good: Focused tests
[Test] public void Tile_HasCorrectWidth() { }
[Test] public void Tile_HasCorrectHeight() { }

// OK for related properties
[Test]
public void Tile_HasCorrectDimensions()
{
    Assert.AreEqual(2.0f, tile.Width);
    Assert.AreEqual(2.0f, tile.Height);
}
```

### Test Independence

Each test should be independent:

- Use `[SetUp]` for common initialization
- Use `[TearDown]` for cleanup
- Don't rely on test execution order

### Fast Tests

Prefer EditMode tests when possible:

- No scene loading overhead
- Pure logic tests run instantly
- Use PlayMode only when necessary

## Existing Tests

### BoardLayoutConfigTests

Tests `LayoutConfig` constants:

- Grid dimensions
- Screen dimensions
- Camera settings
- Zone coordinates

### TileDatabaseTests

Tests `TileDatabase` integrity:

- Database loads from Resources
- Correct tile count (25)
- All tiles have sprites
- All tiles have valid path data

### CoordinateConversionTests

Tests `TileManager` coordinate conversion:

- Grid-to-world mapping
- Center tile at origin
- Corner positions correct

### GameInitializationTests

Tests game startup:

- Managers initialize correctly
- Scene hierarchy valid
- Initial state correct

## Mocking & Isolation

For Unity testing without external dependencies:

| Technique            | Use Case                        |
| -------------------- | ------------------------------- |
| Interface extraction | Mock complex dependencies       |
| ScriptableObjects    | Test data without scene loading |
| Prefab instantiation | Isolated component testing      |
| `Resources.Load()`   | Load test assets in EditMode    |

## Common Mistakes

| Mistake                         | Solution                                   |
| ------------------------------- | ------------------------------------------ |
| Tests depend on execution order | Use `[SetUp]`/`[TearDown]` for state reset |
| Missing scene for PlayMode      | Load required scene in `[UnitySetUp]`      |
| Shared mutable state            | Create fresh objects in each test          |
| Not cleaning up GameObjects     | Destroy test objects in `[UnityTearDown]`  |
| Using PlayMode for pure logic   | Move to EditMode for faster iteration      |

## When to Use EditMode vs PlayMode

| Use EditMode When...             | Use PlayMode When...                 |
| -------------------------------- | ------------------------------------ |
| Testing pure C# logic            | Testing MonoBehaviour lifecycle      |
| Validating ScriptableObject data | Testing scene interactions           |
| Testing static calculations      | Testing coroutines or async behavior |
| Fast iteration is important      | Need Update/FixedUpdate behavior     |

## Reference Files

This skill's `references/` folder contains:

| File                | Contains                                     | Read When                            |
| ------------------- | -------------------------------------------- | ------------------------------------ |
| `editmode-tests.md` | EditMode test examples, `[Test]` attribute   | Writing editor/data validation tests |
| `playmode-tests.md` | PlayMode patterns, `[UnityTest]`, coroutines | Writing runtime/scene tests          |
| `test-patterns.md`  | AAA pattern, naming, isolation, mocking      | Need test architecture guidance      |
| `existing-tests.md` | Current project tests and what they cover    | Understanding test coverage          |

## Running Tests

### In Unity Editor

Window > General > Test Runner

- EditMode tab for editor tests
- PlayMode tab for runtime tests

### Via MCP

Enable testing group: `/unity-mcp-enable testing`

Then use `tests-run` tool with filter options.
