---
name: poka-yoke-patterns
description: "Master Poka-Yoke error-proofing from Toyota Production System. Design systems that prevent mistakes through structure, not vigilance. Covers: path protection, FMEA analysis, quality gates, andon signals, timeout enforcement, type-safe designs. When designing systems, preventing defects, implementing safety mechanisms, or analyzing failure modes."
allowed_tools: "Read, Write, Edit, Glob, Grep, Bash(cargo make:*)"
---

# Poka-Yoke Patterns Skill

## What is Poka-Yoke?

**Poka-Yoke** (ポカ・ヨケ): Japanese for "mistake-proofing"

**Core Idea**: Design systems so mistakes become impossible or immediately obvious

Don't rely on:
- ❌ Vigilance (staying alert)
- ❌ Discipline (following rules)
- ❌ Memory (remembering procedures)

Instead, use:
- ✓ System design (mistakes impossible)
- ✓ Automatic detection (mistakes caught immediately)
- ✓ Physical/logical constraints (mistakes prevented)

## Three Types of Poka-Yoke

### 1. Prevent Mistakes (Yokuten: Prevention)

Make the mistake physically or logically impossible

**Example**: USB-C connector only fits one way
- Before: Users bent pins trying to insert upside down
- After: Design prevents upside-down insertion

**In ggen**:
```rust
// Prevent: Can't create invalid path using NewType
#[derive(Clone)]
pub struct ProtectedPath(String);

impl ProtectedPath {
    pub fn new(path: &str) -> Result<Self, Error> {
        // Validation happens here - can't bypass
        validate_path_safety(path)?;
        Ok(ProtectedPath(path.to_string()))
    }
}

// Now path must be validated:
let path = ProtectedPath::new(user_input)?;  // Validation enforced
let unsafe_path = String::from(user_input);   // Bypasses validation!
```

### 2. Detect Mistakes (Shakokugel: Detection)

Make mistakes visible immediately

**Example**: Gas pump nozzles differ by fuel type
- Before: Drivers pumped wrong fuel, destroying engines
- After: Nozzles physically differ - wrong one won't fit

**In ggen**:
```bash
# Detect: Immediate feedback on errors
cargo make check     # Errors visible instantly (<5s)

# Detect: Warnings-as-errors (no silent issues)
RUSTFLAGS="-D warnings"  # Warnings caught immediately

# Detect: Type system catches mistakes
let num: i32 = "string";  // Compiler error ✓ (caught immediately)
```

### 3. React to Mistakes (Kakunin: Confirmation)

Stop the line when mistakes detected

**Example**: Factory line stops on defect detection
- Before: Defective parts moved to next station
- After: Line halts - defect must be fixed before continuing

**In ggen**:
```
Andon Signal Protocol
│
├─ RED (Error) → STOP immediately, fix now
├─ YELLOW (Warning) → Investigate, review before release
└─ GREEN (Success) → Continue to next step
```

## Poka-Yoke Mechanisms in ggen

### 1. Type-Safety (Prevent)

Use types to make misuse impossible:

```rust
// ❌ Without type safety
pub fn process(path: &str) {
    if is_protected(path) {
        // Handle protected
    }
    // Caller can forget to check!
}

// ✓ With type safety (enforced at compile-time)
pub fn process(path: ProtectedPath) {
    // Can't construct ProtectedPath without validation
    // Mistake impossible - compiler enforces
}
```

### 2. Path Protection (Prevent)

Glob-based whitelisting prevents path traversal:

```rust
pub struct PathProtector {
    protected: Vec<GlobPattern>,    // NEVER overwrite
    regenerate: Vec<GlobPattern>,   // ALWAYS regenerate
}

impl PathProtector {
    pub fn can_write(&self, path: &Path) -> Result<()> {
        // Reject protected paths
        for pattern in &self.protected {
            if pattern.matches(path) {
                return Err(Error::ProtectedPathViolation);
            }
        }
        Ok(())
    }
}

// Usage:
let protector = PathProtector::new()?;
protector.can_write("src/domain/core.rs")?;  // ✓ Can write
protector.can_write(".env")?;                 // ✗ BLOCKED
```

### 3. Timeout Enforcement (Detect)

Prevents hangs, detects deadlocks:

```bash
# Timeout mechanism:
cargo make check    # Quick timeout (5s) - catches hangs
                    # If no timeout: escalation timeout (120s)

# On timeout:
# 1. Quick timeout expires
# 2. Check if lock contention
# 3. If yes: allow escalation timeout
# 4. If no: hard error (deadlock detected)
```

**Effect**: Hangs detected within seconds, never indefinite waits

### 4. Quality Gates (Detect)

Mandatory checks before proceeding:

```
Pre-Commit Gate:
  cargo make check    ✓ Must pass (RED: blocks commit)
  cargo make lint     ✓ Must pass (RED: blocks commit)
  cargo make test-unit ✓ Must pass (RED: blocks commit)

Pre-Push Gate:
  cargo make test     ✓ Must pass (RED: blocks push)
  cargo make lint     ✓ Must pass (RED: blocks push)
  Security audit      ✓ Must pass (RED: blocks push)

Without these gates: Broken code gets committed/pushed
With gates: Mistakes caught before damage
```

### 5. Andon Signals (React)

Stop-the-line protocol on defects:

```
RED Signal (Stop)
├─ Compilation error
├─ Test failure
├─ Timeout occurred
└─ Security issue
→ Action: STOP immediately, fix before proceeding

YELLOW Signal (Warn)
├─ Clippy warning
├─ Performance regression
└─ Deprecation notice
→ Action: Investigate before release

GREEN Signal (Go)
├─ All tests passing
├─ Clippy clean
├─ SLOs met
└─ Security audit clean
→ Action: PROCEED safely
```

## FMEA (Failure Mode & Effects Analysis)

**FMEA**: Proactively identify and mitigate failure modes

### FMEA Process

1. **Identify failure modes**
   - What could go wrong?
   - How could system break?
   - What are edge cases?

2. **Assess severity (1-10)**
   - 10: System crashes, data loss
   - 5: Feature broken, workaround exists
   - 1: Minor inconvenience

3. **Assess occurrence (1-10)**
   - 10: Happens daily
   - 5: Happens monthly
   - 1: Rare (once per year)

4. **Assess detection (1-10)**
   - 10: Almost never detected until customer hit
   - 5: Detected during testing
   - 1: Impossible to miss (immediate feedback)

5. **Calculate RPN = Severity × Occurrence × Detection**
   - High RPN (> 150): High priority mitigation
   - Medium (50-150): Plan mitigation
   - Low (< 50): Monitor

6. **Design mitigations**
   - Prevent (best)
   - Detect (second best)
   - React (last resort)

### Example FMEA: Path Protection

```
Failure Mode: User path overwrites protected file

Severity: 10 (data loss)
Occurrence: 3 (rare, but would happen)
Detection: 10 (not detected by current system)
RPN = 10 × 3 × 10 = 300 (CRITICAL!)

Mitigations:
1. PREVENT: Use type system (ProtectedPath)
   - Validation enforced at type level
   - Severity: 10, Occurrence: 3, Detection: 1
   - RPN = 10 × 3 × 1 = 30 (ACCEPTABLE)

2. DETECT: Glob pattern checking
   - Additional validation layer
   - Catches mistakes type system missed

3. REACT: Permission hooks
   - Final gate before write
   - User must approve risky operations
```

## Timeout Patterns

### Mechanism: Quick + Escalation Timeouts

```
Operation Starts
        ↓
Quick Timeout (5s)
        ↓
    [Timeout?] ──→ YES → Check lock status
        │                    ↓
        NO               Contention?
        │                    ↓
    Continue          [YES] Escalate
                      [NO]  Fail (deadlock)
```

### Benefits

- **Fast feedback**: Issues detected within seconds
- **Handle contention**: Allows legitimate slowness
- **Prevent hangs**: No indefinite waits
- **Automatic**: No user action needed

### Implementation

```bash
# Example from Makefile.toml:
[tasks.check]
command = "cargo"
args = ["check"]
timeout = 5    # Quick timeout (5s)
timeout_escalation = 120  # Escalation (120s)
```

## Type-Safe Design Patterns

### NewType Pattern (Prevent)

```rust
// Strong type prevents misuse
#[derive(Clone)]
pub struct CrateName(String);

pub struct Crate {
    name: CrateName,  // Must be CrateName, not String
    // ...
}

impl CrateName {
    pub fn new(s: &str) -> Result<Self> {
        // Validation here
        if !is_valid_crate_name(s) {
            return Err(Error::InvalidCrateName);
        }
        Ok(CrateName(s.to_string()))
    }
}

// Usage:
let name = CrateName::new("my-crate")?;  // Validation enforced
let crate = Crate { name, };              // Safe construction

// Can't bypass:
let invalid = Crate {
    name: CrateName::new("invalid!!!")?,  // Would fail validation
    // ...
};
```

### Builder Pattern (Prevent)

```rust
pub struct ConfigBuilder {
    path: Option<PathBuf>,
    timeout: Option<Duration>,
    retries: Option<u32>,
}

impl ConfigBuilder {
    pub fn path(mut self, p: PathBuf) -> Result<Self> {
        validate_path(&p)?;  // Validate during build
        self.path = Some(p);
        Ok(self)
    }

    pub fn build(self) -> Result<Config> {
        // Ensure required fields present
        Ok(Config {
            path: self.path.ok_or(Error::PathRequired)?,
            timeout: self.timeout.unwrap_or_default(),
            retries: self.retries.unwrap_or(3),
        })
    }
}

// Usage:
let config = ConfigBuilder::new()
    .path(path)?
    .build()?;  // Validation enforced at each step
```

## Quality Gate Pattern

```rust
pub struct QualityGate {
    checks: Vec<Box<dyn Check>>,
}

impl QualityGate {
    pub fn verify(&self) -> Result<()> {
        for check in &self.checks {
            check.run()?;  // All must pass (RED stops)
        }
        Ok(())  // All checks GREEN
    }
}

pub trait Check {
    fn run(&self) -> Result<()>;
}

struct CompilationCheck;
impl Check for CompilationCheck {
    fn run(&self) -> Result<()> {
        // cargo make check
        // RED: Compilation error
    }
}

struct LintCheck;
impl Check for LintCheck {
    fn run(&self) -> Result<()> {
        // cargo make lint
        // RED: Clippy warning
    }
}

struct TestCheck;
impl Check for TestCheck {
    fn run(&self) -> Result<()> {
        // cargo make test-unit
        // RED: Test failure
    }
}

// Usage:
let gate = QualityGate {
    checks: vec![
        Box::new(CompilationCheck),
        Box::new(LintCheck),
        Box::new(TestCheck),
    ],
};

gate.verify()?;  // All must pass before proceeding
```

## Key Principles

1. **Prevent > Detect > React**
   - Prevention: Best (mistakes impossible)
   - Detection: Second best (mistakes caught early)
   - Reaction: Last resort (stop when detected)

2. **Shift Left**
   - Catch issues early (compilation, not runtime)
   - Type system (compile-time, not test-time)
   - Gates (before commit, not after push)

3. **Stop the Line**
   - RED signals: Must fix immediately
   - Don't ignore or bypass
   - Prevents defect propagation

4. **Automate Everything**
   - No manual checks (easy to forget)
   - Cargo make (automatic verification)
   - Type system (compile-time enforcement)

5. **Zero-Tolerance**
   - Warnings treated as errors
   - No accumulated tech debt
   - Prevents small issues becoming big problems

## Success Criteria

✓ Mistakes prevented at type level
✓ Errors detected within 5 seconds
✓ Quality gates block broken code
✓ Andon signals followed
✓ FMEA completed for major features
✓ Timeout enforcement active
✓ Zero escaped defects to production

## See Also

- `reference.md` - Detailed Poka-Yoke patterns
- `examples.md` - Real-world implementations
- `fmea-template.md` - FMEA analysis template
- Toyota Production System documentation
- Type-Safe Design Patterns in Rust
