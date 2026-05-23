---
name: build-hs
description: Start a ghcid session to monitor the build. Use when working with Haskell projects, starting ghcid, checking build errors, or searching Haskell documentation with hoogle.
user-invocable: true
---

# Haskell Build Monitoring with ghcid

Start a ghcid session to monitor the build.

**Before starting**: Verify which command is actually allowed in `.claude/settings.local.json` for ghcid and ensure you use it to avoid prompting for permission.

First, check `package.yaml` to identify the test components:
- `tests:` section → use the test name with `-test` suffix (e.g., `dota-sage-test`)

Then run ghcid with the `all` target (which includes all libraries and executables, including internal libraries) PLUS all test components using the Bash tool with `run_in_background: true`:

```
ghcid \
  -c 'cabal repl --enable-multi-repl all <test-name>' \
  --restart=<project>.cabal \
  --test ':!cabal test' \
  --outputfile=build.log \
  --clear
```

**Note**: The `all` target ensures internal libraries are included in the build. Tests must be specified explicitly since `all` doesn't include them. The `--restart` flag causes ghcid to automatically restart when the cabal file changes (e.g., after hpack regeneration). The `--test` flag runs the test suite automatically after a successful build.

To keep context usage reasonable, only the output file `build.log` should be used to monitor the build status, ideally reading only the first few lines and then more if needed using the Read tool.

**Monitoring build status**:
- Check for errors: Use Read tool with `file_path: "build.log"` and `limit: 20`
- Check if ghcid is running: View background processes in Claude Code UI, or `ps aux | grep ghcid`
- Kill ghcid: Use KillShell tool with the shell ID, or `pkill ghcid`

**When to restart ghcid**:
- If ghcid appears stuck or unresponsive
- When adding a new component (library, executable, test) to `package.yaml` that needs to be included in the repl command

**Note**: With the `--restart` flag, ghcid will automatically restart when the cabal file changes, so manual restarts are not needed after running `hpack --force`. Always use `hpack --force` to avoid version mismatch errors when regenerating cabal files.

**Important**: If you add a new component (library, executable, or test suite) to `package.yaml`, you must also remind me to update the permission in `.claude/settings.local.json` to include the new component name in the ghcid command.

**Note**: Avoid building the project directly with cabal or stack. Let ghcid monitor compilation continuously.

**Incremental Compilation Performance**:
- The initial ghcid build takes a few seconds to compile all modules
- After that, incremental recompilation is essentially instant (typically <1 second)
- **IMPORTANT**: Do not add `sleep` delays between making code changes and checking build.log
- ghcid detects file changes and recompiles immediately, so you can check build.log right after making edits
- If you need to verify compilation completed, just read build.log directly - if ghcid is still compiling, you'll see the status

## Common Build Issues

**HasField instance errors with OverloadedRecordDot**:
- These errors are almost always due to missing imports of the data constructor
- Fix: Import the data constructor explicitly using `import Module (Type(..))` rather than just `import Module (Type)`
- Example: If you see `No instance for (GHC.Records.HasField "field" Type ...)`, check that you're importing `Type(..)` not just `Type`

## Documentation Search with Hoogle

Use hoogle CLI to search for documentation of project dependencies.

**Basic search commands**:

1. **Search for a function by name**:
   ```
   hoogle search "mapMaybe"
   ```
   Example output: Shows functions from Data.Maybe and other modules

2. **Search by type signature**:
   ```
   hoogle search "(a -> Bool) -> [a] -> [a]"
   ```
   Finds functions like `filter`, `takeWhile`, etc.

3. **Search for specific package documentation**:
   ```
   hoogle search "aeson" --count=10
   ```
   Lists top 10 results from the aeson package

4. **Get detailed information about a function**:
   ```
   hoogle search "traverse" --info
   ```
   Shows full documentation with examples

5. **Search in specific modules**:
   ```
   hoogle search "module:Data.List take"
   ```
   Searches only within Data.List module

**Advanced usage**:

- **Limit results**: Add `--count=N` to show only N results
- **JSON output**: Add `--json` for machine-readable output
- **Exact match**: Use quotes for exact function name matching
- **Type class search**: Search for `"Monad m => ..."` to find typeclass instances

**Common search patterns**:

- Find JSON parsing: `hoogle search "ByteString -> Maybe Value"`
- Find list functions: `hoogle search "module:Data.List"`
- Find monad operations: `hoogle search "Monad m =>"`
- Find lens operations: `hoogle search "Lens'"`

**Integration with development**:
- When encountering unfamiliar functions in build.log errors, use hoogle to understand their usage
- Use type signature search to discover appropriate functions for your use case
- Explore package APIs by searching the package name to understand available modules and functions before implementing features
