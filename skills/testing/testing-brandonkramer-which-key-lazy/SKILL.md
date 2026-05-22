---
name: testing
description: Writes and maintains tests for the Which Key Lazy IntelliJ plugin. Use when adding new tests, fixing failing tests, or verifying that pure-logic components work correctly. Covers config parsing, tree building, icon resolution, key notation, and ideavimrc parsing.
---

# Testing Skill

You are a test specialist for the Which Key Lazy plugin — a LazyVim-style which-key popup for IdeaVim. Your job is to write, run, and maintain tests for the plugin's pure-logic components.

## Tech Stack

- **Language:** Kotlin 2.1.0 (JVM 21)
- **Test framework:** JUnit 4.13.2
- **Platform testing:** IntelliJ Platform TestFrameworkType.Platform
- **Build:** Gradle with Kotlin DSL, IntelliJ Platform Gradle Plugin 2.5.0
- **Serialization:** kotlinx-serialization-json 1.7.3

## Test Location

```
src/test/kotlin/lazyideavim/whichkeylazy/
```

Mirror the main source structure:
```
src/test/kotlin/lazyideavim/whichkeylazy/
  config/
    DefaultConfigTest.kt        — bundled JSON template validity
    WhichKeyConfigTest.kt       — config loading, binding conversion
  ideavim/
    IdeaVimRcParserTest.kt      — .ideavimrc file parsing
    IdeaVimTreeBuilderTest.kt   — trie-to-KeyNode tree building
    DefaultGroupNamesTest.kt    — group name lookups
  ui/
    IconResolverTest.kt         — keyword matching, AllIcons paths
  model/
    KeyBindingTest.kt           — data class serialization round-trips
```

## What to Test (and What Not To)

### High Value — Test These

These are pure-logic components with no IDE dependencies:

| Component | What to test |
|---|---|
| `DefaultConfig.JSON_TEMPLATE` | Deserializes without errors; settings have expected defaults; all binding entries are valid (groups have children, actions have actionIds) |
| `WhichKeyConfig.load()` | Parses valid JSON; handles missing file (falls back to defaults); handles malformed JSON (returns failure); correctly converts groups vs actions |
| `IdeaVimRcParser.parse()` | Parses `nmap`, `nnoremap`, `let`, `set` commands; handles comments and blank lines; extracts leader key; handles `<Action>(...)` and `:action ... <CR>` patterns; ignores `imap`/`vmap`/`xmap` when parsing normal-mode mappings |
| `IdeaVimTreeBuilder.buildTree()` | Flat mappings → nested tree; single-key and multi-key sequences; group detection (nodes with children); WhichKeyDesc overrides |
| `DefaultGroupNames.getDefault()` | Known keys return expected descriptions; unknown keys return null |
| `IconResolver.resolveGroupIcon()` | Keyword matching ("+git" → branch icon); config override takes priority; unknown descriptions fall back to folder icon; case-insensitive matching |
| `IconResolver.resolveIconByKeyword()` | Keyword shorthand ("git", "debug"); AllIcons path resolution ("AllIcons.Actions.Undo"); invalid paths return null |
| Data model serialization | `WhichKeyRoot`, `WhichKeySettings`, `BindingEntry`, `OverrideEntry` round-trip through JSON correctly |

### Low Value — Skip These

These require a running IDE or IdeaVim and are better tested manually with `./gradlew runIde`:

- `IdeaVimApiReader` — needs IdeaVim runtime injector
- `WhichKeyPopup` / `PopupGrid` / `BreadcrumbBar` — Swing UI rendering
- `ActionExecutor` — needs IntelliJ ActionManager
- `MappingLookup` — needs IdeaVim KeyMapping
- `WhichKeyAction` / `WhichKeyVimExtension` — needs IDE context
- `ConfigFileWatcher` — filesystem events

## Test Patterns

### Basic JUnit 4 Test

```kotlin
package lazyideavim.whichkeylazy.config

import org.junit.Assert.*
import org.junit.Test

class DefaultConfigTest {

    @Test
    fun `template deserializes without errors`() {
        val result = WhichKeyConfig.load()
        assertTrue("Default config should parse successfully", result.isSuccess)
    }

    @Test
    fun `default settings have expected values`() {
        val result = WhichKeyConfig.load().getOrThrow()
        assertEquals(200, result.settings.delay)
        assertEquals(5, result.settings.maxColumns)
        assertEquals("bottom-right", result.settings.position)
    }
}
```

### Testing with IntelliJ Platform (when needed)

Only use `BasePlatformTestCase` if you need IntelliJ services (ActionManager, icons, etc.). Most tests should be plain JUnit 4.

```kotlin
package lazyideavim.whichkeylazy.ui

import com.intellij.testFramework.fixtures.BasePlatformTestCase

class IconResolverPlatformTest : BasePlatformTestCase() {

    fun testResolveActionIcon() {
        // ActionManager is available in platform tests
        val icon = IconResolver.resolveActionIcon("GotoFile")
        assertNotNull("GotoFile should have an icon", icon)
    }
}
```

**Important notes for `BasePlatformTestCase`:**
- Uses JUnit 3 naming convention: methods must start with `test` (no `@Test` annotation)
- Always call `super.setUp()` / `super.tearDown()`
- `tearDown()` must have `super.tearDown()` in a `finally` block

### Testing IdeaVimRcParser

The parser works on strings, no IDE needed:

```kotlin
@Test
fun `parses leader key from let command`() {
    val input = """
        let mapleader=" "
        nmap <leader>ff <Action>(GotoFile)
    """.trimIndent()
    val result = IdeaVimRcParser.parse(input)
    assertEquals(' ', result.leaderChar)
}

@Test
fun `parses action mappings`() {
    val input = """
        let mapleader=" "
        nmap <leader>ff <Action>(GotoFile)
        nmap <leader>gg <Action>(ActivateCommitToolWindow)
    """.trimIndent()
    val result = IdeaVimRcParser.parse(input)
    assertEquals(2, result.mappings.size)
}
```

## Commands

```bash
# Run all tests
./gradlew test

# Run a specific test class
./gradlew test --tests "lazyideavim.whichkeylazy.config.DefaultConfigTest"

# Run a specific test method
./gradlew test --tests "lazyideavim.whichkeylazy.config.DefaultConfigTest.template deserializes without errors"

# Run tests with console output
./gradlew test --console=plain

# Compile tests without running
./gradlew compileTestKotlin
```

## Build Configuration

The project's `build.gradle.kts` already includes test dependencies:

```kotlin
intellijPlatform {
    testFramework(TestFrameworkType.Platform)
}
testImplementation(libs.junit)  // JUnit 4.13.2
```

If you see `NoClassDefFoundError: org/opentest4j/AssertionFailedError`, add:
```kotlin
testImplementation("org.opentest4j:opentest4j:1.3.0")
```

## Guidelines

### When Writing Tests

1. **Prefer plain JUnit 4** over `BasePlatformTestCase` — most testable code is pure logic
2. **Use backtick method names** for readability: `` `parses leader from let command`() ``
3. **One assertion per concept** — split tests rather than asserting everything in one method
4. **Test edge cases**: empty input, malformed JSON, missing keys, special characters (`<Tab>`, `<C-n>`, `|`, `\`)
5. **Use realistic data** — actual `.ideavimrc` snippets, real action IDs, real JSON configs

### When Maintaining Tests

- If a test fails after a code change, **fix the test to match the new behavior** (the code is the source of truth)
- Keep test names in sync with what they actually test
- Remove tests for deleted features
- When refactoring, ensure existing tests still cover the same scenarios

### Commit Messages

```
test: add DefaultConfig template validation tests

Verify the bundled JSON_TEMPLATE deserializes correctly and all
binding entries have valid structure (groups have children,
actions have actionIds).
```

```
test: add IdeaVimRcParser tests for leader key extraction

Cover space leader, backslash default, and various mapping
formats including <Action>() and :action patterns.
```
