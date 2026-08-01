---
name: mql5-x-compile
description: 'Compile MQL5 indicators via CLI using X: drive mapping to bypass ''Program
  Files'' path spaces issue. Use when compiling MQL5, MetaEditor, indicators, scripts,
  or when user mentions compilation errors r'
---

---
name: mql5-x-compile
description: Compile MQL5 indicators via CLI using X: drive mapping to bypass 'Program Files' path spaces issue. Use PROACTIVELY after editing ANY .mq5 or .mqh file. Triggers - after editing MQL5 code, compile, build, MetaEditor, .mq5, .mqh, indicator, script, EA, expert advisor, "test it", "try it", "run it", path space errors. (project)
allowed-tools: Bash, Read
---

# MQL5 X-Drive CLI Compilation

Compile MQL5 indicators/scripts via command line using X: drive mapping to avoid "Program Files" path spaces that cause silent compilation failures.

## When to Use (Proactive Triggers)

**ALWAYS use this skill after:**
- Editing any `.mq5` file (indicator, script, EA)
- Editing any `.mqh` file (library/include)
- User says "compile", "build", "test it", "try it", "run it"
- User asks to verify changes work
- Making code changes that need validation

**Also use when:**
- User mentions MetaEditor, compilation errors, or path issues
- Exit code 1 appears (reminder: exit 1 is normal, check .ex5 file)
- Need to verify .ex5 file was created

## Prerequisites

**X: drive must be mapped** (one-time setup):

```bash
BOTTLE="$HOME/Library/Application Support/CrossOver/Bottles/MetaTrader 5"
cd "$BOTTLE/dosdevices"
ln -s "../drive_c/Program Files/MetaTrader 5/MQL5" "x:"
```

Verify mapping exists:

```bash
ls -la "$BOTTLE/dosdevices/" | grep "x:"
```

## Compilation Instructions

### Step 1: Construct X: Drive Path

Convert standard path to X: drive format:

- Standard: `C:\Program Files\MetaTrader 5\MQL5\Indicators\Custom\MyIndicator.mq5`
- X: drive: `X:\Indicators\Custom\MyIndicator.mq5`

**Pattern**: Remove `Program Files/MetaTrader 5/MQL5/` prefix, replace with `X:\`

### Step 2: Execute Compilation

```bash
CX="$HOME/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/wine"
BOTTLE="MetaTrader 5"
ME="C:/Program Files/MetaTrader 5/MetaEditor64.exe"

# Compile using X: drive path
"$CX" --bottle "$BOTTLE" --cx-app "$ME" \
  /log \
  /compile:"X:\\Indicators\\Custom\\YourFile.mq5" \
  /inc:"X:"
```

**Critical flags**:

- `/log`: Enable compilation logging
- `/compile:"X:\\..."`: Source file (X: drive path with escaped backslashes)
- `/inc:"X:"`: Include directory (X: drive root = MQL5 folder)

### Step 3: Verify Compilation

**CRITICAL**: Wine/CrossOver returns exit code 1 even on successful compilation. **Ignore the exit code** - always verify by checking the .ex5 file and per-file log.

Check if .ex5 file was created:

```bash
BOTTLE="$HOME/Library/Application Support/CrossOver/Bottles/MetaTrader 5"
EX5_FILE="$BOTTLE/drive_c/Program Files/MetaTrader 5/MQL5/Indicators/Custom/YourFile.ex5"
LOG_FILE="$BOTTLE/drive_c/Program Files/MetaTrader 5/MQL5/Indicators/Custom/YourFile.log"

# Check .ex5 exists with recent timestamp
if [ -f "$EX5_FILE" ]; then
  ls -lh "$EX5_FILE"
  echo "✅ Compilation successful"
else
  echo "❌ Compilation failed"
fi

# Check per-file log (UTF-16LE, but often readable with cat)
cat "$LOG_FILE" | grep -i "error\|warning\|Result"
```

**Per-file log location**: The `.log` file is created in the same directory as the `.mq5` file (e.g., `Fvg.mq5` → `Fvg.log`). This is more reliable than `logs/metaeditor.log`.

## Common Patterns

### Example 1: Compile CCI Neutrality Indicator

```bash
CX="$HOME/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/wine"
"$CX" --bottle "MetaTrader 5" \
  --cx-app "C:/Program Files/MetaTrader 5/MetaEditor64.exe" \
  /log \
  /compile:"X:\\Indicators\\Custom\\Development\\CCINeutrality\\CCI_Neutrality_RoC_DEBUG.mq5" \
  /inc:"X:"

# Result: CCI_Neutrality_RoC_DEBUG.ex5 created (23KB)
```

### Example 2: Compile Script

```bash
"$CX" --bottle "MetaTrader 5" \
  --cx-app "C:/Program Files/MetaTrader 5/MetaEditor64.exe" \
  /log \
  /compile:"X:\\Scripts\\DataExport\\ExportAligned.mq5" \
  /inc:"X:"
```

### Example 3: Verify X: Drive Mapping

```bash
CX="$HOME/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/wine"
"$CX" --bottle "MetaTrader 5" cmd /c "dir X:\" | head -10
# Should list: Indicators, Scripts, Include, Experts, etc.
```

## Troubleshooting

### Issue: Exit code 1 but compilation succeeded

**Cause**: Wine/CrossOver always returns exit code 1, even on success
**Solution**: **Ignore exit code.** Always verify by:
1. Check `.ex5` file exists with recent timestamp: `ls -la YourFile.ex5`
2. Check per-file log for "0 errors, 0 warnings": `cat YourFile.log`

### Issue: 42 errors, include file not found

**Cause**: Compiling from simple path (e.g., `C:/file.mq5`) without X: drive
**Solution**: Use X: drive path with `/inc:"X:"` flag

### Issue: Exit code 0 but no .ex5 file

**Cause**: Path contains spaces or special characters
**Solution**: Use X: drive path exclusively (no spaces)

### Issue: X: drive not found

**Cause**: Symlink not created
**Solution**: Run prerequisite setup to create `x:` symlink in dosdevices

### Issue: Wrong CrossOver path

**Cause**: Using `/Applications/CrossOver.app` instead of `~/Applications/`
**Solution**: Verify CrossOver location with `ls ~/Applications/CrossOver.app`

### Issue: Can't find metaeditor.log

**Cause**: Looking in wrong location
**Solution**: Use per-file log instead - it's in the same directory as your `.mq5` file (e.g., `Fvg.mq5` creates `Fvg.log`)

## Benefits of X: Drive Method

✅ **Eliminates path spaces**: No "Program Files" in path
✅ **Faster compilation**: ~1 second compile time
✅ **Reliable**: Works consistently unlike direct path compilation
✅ **Includes resolved**: `/inc:"X:"` finds all MQL5 libraries
✅ **Simple paths**: `X:\Indicators\...` instead of long absolute paths

## Comparison: X: Drive vs Manual GUI

| Method | Speed | Automation | Reliability |
| --- | --- | --- | --- |
| X: drive CLI | ~1s | ✅ Yes | ✅ High |
| Manual MetaEditor | ~3s | ❌ No | ✅ High |
| Direct CLI path | N/A | ⚠️ Unreliable | ❌ Fails silently |

## Integration with Git Workflow

X: drive mapping is persistent and git-safe:

- Symlink stored in bottle's `dosdevices/` folder
- Doesn't affect MQL5 source files
- Works across git branches
- No configuration files to commit

## Security Notes

- X: drive is READ-ONLY for compilation purposes
- No execution of compiled files during compilation
- MetaEditor runs in sandboxed Wine environment
- No network access during compilation

## Quick Reference

**Compilation command template**:

```bash
wine --bottle "MetaTrader 5" \
  --cx-app "C:/Program Files/MetaTrader 5/MetaEditor64.exe" \
  /log /compile:"X:\\Path\\To\\File.mq5" /inc:"X:"
```

**Bottle location**: `~/Library/Application Support/CrossOver/Bottles/MetaTrader 5/`

**X: drive maps to**: `MQL5/` folder inside bottle

**Verification**: Check for `.ex5` file and review per-file `.log` (ignore exit code - it's always 1)
