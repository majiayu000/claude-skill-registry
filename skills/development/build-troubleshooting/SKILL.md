---
name: build-troubleshooting
description: FAQ for diagnosing and resolving build and test failures
---

# Build & Test Troubleshooting FAQ

**Purpose**: Reference guide for diagnosing and resolving build failures, test failures, and other development environment issues.

**When to use**: When encountering unexpected build or test failures, especially those that seem environment-related rather than code-related.

---

## FAQ

### Q1: NeoForge GameTest fails with "Illegal version number specified version (main)"

**Symptoms**:
```
File /path/to/neoforge-1.21.2/build/resources/main is not a valid mod file
Caused by: java.lang.IllegalArgumentException: Illegal version number specified version (main)
```

**Cause**: IDE (IntelliJ IDEA, Eclipse) generated `bin/` directories containing unprocessed resource files. The `neoforge.mods.toml` in `bin/main/META-INF/` has `version="${version}"` instead of the actual version number.

**Solution**:
1. Delete IDE-generated bin directories:
   ```bash
   rm -rf neoforge-1.21.2/bin common-1.21.2/bin
   ```
2. Or run the cleanAll task which now includes bin/ cleanup:
   ```bash
   ./gradlew cleanAll
   ```

**Prevention**:
- Configure IDE to use Gradle for builds instead of built-in compiler
- Add `bin/` to `.gitignore` (already done in this project)

**Reference**: Discovered 2026-01-25 during portal GameTest implementation.

---

### Q2: GameTest structure template not found or too small

**Symptoms**:
- Tests fail with "structure not found" errors
- Portal/structure tests fail because test area is too small

**Cause**:
- Fabric uses `FabricGameTest.EMPTY_STRUCTURE` constant (built-in)
- NeoForge requires explicit structure template files

**Solution**:
For NeoForge, create a proper NBT structure file:
1. Create `empty_test.nbt` in `common-{version}/src/main/resources/data/chronodawn/structure/`
2. Reference it as `"chronodawn:empty_test"` in test configuration

**Note**: The structure must be large enough for the test content (e.g., 10x10x10 for portal frame tests).

---

### Q3: Gradle daemon conflicts during parallel builds

**Symptoms**:
- Build fails with lock file errors
- "Could not create service of type" errors
- Tests hang or fail intermittently

**Solution**:
```bash
./gradlew --stop
./gradlew cleanAll
```

---

### Q4: Test passes on Fabric but fails on NeoForge (or vice versa)

**Checklist**:
1. **Mixin configurations**: Check both loader-specific mixin JSON files
2. **Structure templates**: NeoForge needs explicit templates, Fabric has EMPTY_STRUCTURE
3. **API differences**: Some APIs behave differently between loaders
4. **IDE artifacts**: Run `./gradlew cleanAll` to remove stale bin/ directories

---

### Q5: "session.lock" errors during GameTest

**Symptoms**:
```
Failed to lock the level ... session.lock
```

**Cause**: Previous test run left a lock file.

**Solution**:
The `gameTestAll` task already handles this by cleaning stale world directories. If it persists:
```bash
rm -rf fabric-*/run/gametestworld
rm -rf neoforge-*/run/gametestworld
```

---

## Adding New FAQ Entries

When encountering a new build/test issue:
1. Document symptoms (exact error message)
2. Identify root cause
3. Document solution
4. Add prevention tips if applicable
5. Add reference date for tracking
