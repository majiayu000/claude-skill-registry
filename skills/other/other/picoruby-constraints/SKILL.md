---
name: PicoRuby Development Constraints
description: Documents memory limits and stdlib constraints for PicoRuby on ESP32. Use this when writing code that will run on ESP32 hardware or designing features for PicoRuby applications.
---

# PicoRuby Development Constraints

Memory constraints and stdlib limitations for ESP32 PicoRuby development.

## Memory & Runtime Limits

- **Total heap**: 520KB (strict limit)
- **Nesting depth**: Avoid deep recursion; prefer iterative solutions
- **String handling**: Pre-allocate when possible; avoid repeated concatenation
- **Arrays**: Use fixed-size when known; minimize dynamic growth during tight loops

## PicoRuby vs CRuby

| Feature | PicoRuby | CRuby |
|---------|----------|-------|
| Gems | ❌ No bundler/gems | ✅ Full ecosystem |
| stdlib | Minimal (R2P2-ESP32 only) | Complete stdlib |
| Memory | ~520KB heap | GB+ available |
| GC | Simple mark-sweep | Complex generational |
| Float math | ⚠️ Limited precision | Full IEEE 754 |

## PicoRuby-safe stdlib

**Available**:
- `Array#each`, `#map`, `#select` (avoid `#each_with_index` in tight loops)
- `Hash` (simple key-value)
- `String` (basic methods, avoid regex for embedded)
- `Time` (limited; ESP32 time depends on system clock)
- `File` (via R2P2-ESP32 abstraction)

**Unavailable**:
- Regex (use string matching instead)
- Threads (single-threaded runtime)
- Fiber/Enumerator (complex control flow not needed)
