---
name: debug
description: Debug errors, bugs, and unexpected behavior systematically in Home Assistant integration. Use when investigating errors, analyzing stack traces, fixing bugs, or troubleshooting unexpected behavior.
---

# Debug Errors and Bugs Systematically

Debug errors, bugs, and unexpected behavior in the Linus Dashboard Home Assistant integration.

---

## Context Loading

Before debugging, load:
1. [.aidriven/memorybank.md](.aidriven/memorybank.md) - Project architecture
2. [.aidriven/rules/clean_code.md](.aidriven/rules/clean_code.md) - Code standards
3. [.aidriven/rules/homeassistant_integration.md](.aidriven/rules/homeassistant_integration.md) - HA patterns
4. [.aidriven/rules/async_patterns.md](.aidriven/rules/async_patterns.md) - Async best practices

---

## Debug Process

### Step 1: Understand the Error

**Collect Information:**
- Error message (full stack trace)
- When does it occur? (startup, service call, state change)
- Which file/function is involved?
- User actions that trigger it
- Home Assistant version and logs

**Questions to Ask:**
1. Is this a Python exception or HA-specific error?
2. Does the error occur consistently or randomly?
3. Are there related errors in `home-assistant.log`?
4. What changed recently (code, config, HA version)?

### Step 2: Analyze Root Cause

**Common Error Categories:**

#### 1. Async/Await Issues
```python
# Symptoms:
# - "coroutine was never awaited"
# - Event loop blocking
# - Timeouts

# Check for:
await missing_function()  # Missing await
blocking_io_call()  # Blocking I/O in async context
```

#### 2. Home Assistant Integration Errors
```python
# Symptoms:
# - Integration fails to load
# - Config flow errors
# - Entity not showing up

# Check for:
# - Missing async_setup_entry/async_unload_entry
# - Incorrect platform registration
# - Missing unique_id on entities
# - Data not stored in hass.data correctly
```

#### 3. API/Network Errors
```python
# Symptoms:
# - Connection refused
# - Timeouts
# - 4xx/5xx HTTP errors

# Check for:
# - Supabase URL/key configuration
# - Network connectivity
# - API rate limits
# - Timeout values
```

### Step 3: Investigate

**Review Code:**
- Read the file where error occurs
- Trace the execution path
- Check function signatures
- Review recent changes with `git log`

**Check Logs:**
```bash
# Home Assistant logs
tail -f /config/home-assistant.log | grep linus

# Check for warnings
grep -i "warning.*linus" /config/home-assistant.log
```

**Add Debug Logging:**
```python
import logging
_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("Variable value: %s", variable)
_LOGGER.info("Entering function with args: %s", args)
```

### Step 4: Fix the Issue

**Apply Fix:**
- Make minimal changes to fix root cause
- Follow code standards from [.aidriven/rules/clean_code.md](.aidriven/rules/clean_code.md)
- Add error handling if missing
- Update documentation if behavior changed

**Test the Fix:**
1. Restart Home Assistant
2. Reproduce the original error scenario
3. Verify error is gone
4. Check logs for new errors
5. Test related functionality

### Step 5: Verify and Document

**Verification:**
- [ ] Error no longer occurs
- [ ] No new errors introduced
- [ ] Related features still work
- [ ] Logs are clean

**Documentation:**
- Update inline comments if needed
- Note the fix in commit message
- Update CHANGELOG if user-facing

---

## Common Issues and Solutions

### Issue: "coroutine was never awaited"
**Solution:** Add `await` before async function calls
```python
# Before
result = async_function()

# After
result = await async_function()
```

### Issue: Integration doesn't load
**Solution:** Check entry setup and platform registration
```python
# Ensure proper setup
async def async_setup_entry(hass, entry):
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True
```

### Issue: Entity not updating
**Solution:** Verify state updates and coordinator refresh
```python
# Ensure coordinator updates
await self.coordinator.async_request_refresh()
```

### Issue: Timeout errors
**Solution:** Increase timeout or optimize slow operations
```python
# Add proper timeout
async with timeout(30):
    result = await slow_operation()
```

---

## Debug Tools

**Home Assistant Developer Tools:**
- Services tab - Test service calls
- States tab - Check entity states
- Events tab - Monitor events
- Template tab - Test templates

**Python Debugging:**
```python
# Add breakpoint (if debugging locally)
import pdb; pdb.set_trace()

# Add detailed logging
_LOGGER.debug("State: %s, Attrs: %s", self.state, self.extra_state_attributes)
```

**Git Tools:**
```bash
# Find when bug was introduced
git log --oneline -- path/to/file.py

# Check recent changes
git diff HEAD~5 -- path/to/file.py
```

---

## Checklist

Before completing debug:
- [ ] Root cause identified
- [ ] Fix implemented following code standards
- [ ] Error no longer reproduces
- [ ] Related functionality tested
- [ ] Logs reviewed for new issues
- [ ] Changes documented
