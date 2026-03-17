# 🐛 Auto Debug Skill

---
name: auto-debug
description: Automatically detect bugs from terminal output and suggest/apply fixes without manual intervention
---

## 🎯 Purpose

ตรวจจับ errors จาก terminal output อัตโนมัติ และแนะนำหรือแก้ไขปัญหาทันที ลดเวลา debug ลงอย่างมาก

## 📋 When to Use

- เมื่อ terminal แสดง error messages
- เมื่อ build/compile fail
- เมื่อ tests fail
- เมื่อ runtime errors occur
- เมื่อ linting errors เกิดขึ้น

## 🔧 Capabilities

### 1. Error Detection
| Error Type | Detection Pattern |
|------------|-------------------|
| TypeScript | `TS\d+:`, `Type error:` |
| ESLint | `error:`, `warning:` |
| Runtime | `Error:`, `Exception:` |
| Build | `ENOENT`, `Cannot find module` |
| Test | `FAIL`, `Expected.*but received` |

### 2. Common Error Fixes

#### TypeScript Errors
```typescript
// TS2322: Type 'string' is not assignable to type 'number'
// Fix: Change variable type or value

// TS2339: Property does not exist
// Fix: Add property to interface or use optional chaining

// TS7006: Parameter implicitly has 'any' type
// Fix: Add explicit type annotation
```

#### Module Errors
```bash
# Cannot find module 'xyz'
# Fix 1: npm install xyz
# Fix 2: Check import path spelling
# Fix 3: Add to tsconfig paths

# Module not found: Can't resolve './component'
# Fix: Check file exists, check extension, check case sensitivity
```

#### Runtime Errors
```javascript
// TypeError: Cannot read property 'x' of undefined
// Fix: Add null check or optional chaining

// ReferenceError: variable is not defined
// Fix: Declare variable or check scope

// SyntaxError: Unexpected token
// Fix: Check JSON format, missing brackets
```

## 📝 Auto-Debug Process

```
┌─────────────────┐
│  Error Occurs   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Parse Error Msg │ ← Extract error type, location, message
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Identify Cause  │ ← Match patterns, analyze context
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Generate Fix    │ ← Create solution based on error type
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Apply & Verify  │ ← Apply fix, re-run to verify
└────────┬────────┘
         │
         ▼
   Fixed? ────No────▶ Try alternative fix
         │
        Yes
         │
         ▼
      Done! ✅
```

## 🔄 Auto-Fix Loop

```python
MAX_ATTEMPTS = 5
attempt = 0

while error_exists and attempt < MAX_ATTEMPTS:
    error = parse_error(terminal_output)
    fix = generate_fix(error)
    apply_fix(fix)
    result = run_command_again()
    
    if result.success:
        log_solution(error, fix)  # Save for future
        break
    else:
        attempt += 1
        try_alternative_fix()
```

## 📚 Error Pattern Database

### Build Errors
| Pattern | Cause | Auto-Fix |
|---------|-------|----------|
| `ENOENT` | File not found | Check path, create file |
| `EACCES` | Permission denied | Check permissions |
| `EADDRINUSE` | Port in use | Kill process or change port |

### Dependency Errors
| Pattern | Cause | Auto-Fix |
|---------|-------|----------|
| `peer dep` | Version mismatch | Update package |
| `ERESOLVE` | Conflict | Use --legacy-peer-deps |
| `not found` | Missing package | npm install |

### Syntax Errors
| Pattern | Cause | Auto-Fix |
|---------|-------|----------|
| `Unexpected token` | Typo, missing bracket | Add missing syntax |
| `Unterminated string` | Missing quote | Add closing quote |
| `Invalid JSON` | Malformed JSON | Fix JSON syntax |

## ✅ Self-Check

- [ ] Error correctly identified
- [ ] Root cause understood
- [ ] Fix is safe (won't break other code)
- [ ] Fix verified by re-running
- [ ] Solution logged for future reference

## 📢 Announcement Format

```
[🐛 Auto-Debug] Detected: {error type}
[🐛 Auto-Debug] Cause: {root cause}
[🐛 Auto-Debug] Fixing: {applying fix}
[🐛 Auto-Debug] ✅ Fixed: {summary}
```

## 🔗 Related Skills

- `debugging` - Manual debugging
- `error-recovery` - Graceful error handling
- `testing` - Prevent errors with tests
