---
name: add-device
description: Add a new implementation of the primary protocol/interface (Alex Rivera's workflow)
disable-model-invocation: true
---

Add a new implementation of the primary protocol/interface: $ARGUMENTS

Follow Alex Rivera's hardware integration standards:

1. **Study the protocol**: Read the primary protocol/interface definition in the core layer (see Key Abstractions and Protocol Methods in project config)

2. **Implement the class** in the core layer file:
   - MUST satisfy the primary protocol/interface
   - Follow the future annotations pattern (see stack concepts in project config)
   - All methods MUST have return type annotations
   - Document protocol-specific commands with clear comments
   - Raise the discovery error exception if resource not detected on `open()`
   - Raise the connection error exception on communication failures
   - Track `is_open` state accurately
   - `close()` MUST be idempotent — safe to call multiple times

3. **Update config** if new settings are needed:
   - Add to the config file's Settings class with the project's env prefix
   - Document in the env example file with defaults and description

4. **Update the mock implementation** to mirror any new behavior:
   - Same exceptions for same error conditions
   - Same state transitions

5. **Wire into lifespan** in the app factory:
   - Add selection logic in the lifespan function
   - Ensure the fail-safe operation runs on both startup and shutdown for the new implementation

6. **Write tests** in the core layer test file (see test file mapping in project config):
   - Test `open()` / `close()` lifecycle
   - Test state-changing operations for valid and invalid inputs
   - Test `get_info()` returns expected structure
   - Test error conditions raise typed exceptions
   - Test `is_open` property accuracy

7. **Verify**: Run the test command and the type-check command (see project config)