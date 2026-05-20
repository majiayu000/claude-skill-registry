---
name: gathering-feature
description: The drum sounds. Bloodhound, Elephant, Turtle, Beaver, Raccoon, Deer, Fox, and Owl gather for complete feature development. Use when building a full feature from exploration to documentation — secure by design.
---

# Gathering Feature 🌲🐾

The drum echoes through the forest. One by one, they come. The Bloodhound scouts the territory. The Elephant builds with unstoppable momentum. The Turtle hardens what was built — bone-deep security, not bolted on afterward. The Beaver tests the hardened code. The Raccoon audits for secrets and cleanup. The Deer ensures all can travel the paths. The Fox optimizes for speed. The Owl documents what was learned. When the gathering completes, a feature stands where before there was only forest — secure from birth.

## When to Summon

- Building a complete feature from scratch
- Major functionality spanning frontend, backend, and database
- Features requiring exploration, implementation, testing, and documentation
- When you want the full lifecycle handled automatically

---

## Grove Tools for This Gathering

Use `gw` and `gf` throughout. Quick reference for feature work:

```bash
# Orientation — start every gathering here
gw context

# Exploration phase (Bloodhound)
gf --agent search "pattern"         # Find relevant code
gf --agent func "functionName"      # Find function definitions
gf --agent usage "ComponentName"    # Find where things are used
gf --agent impact "module"          # Understand change blast radius

# Testing phase (Beaver)
gw ci --affected --diagnose         # Run CI on affected packages

# Shipping phase (after all animals complete)
gw git pr-prep                      # Preflight check before PR
gw git ship --write -a -m "feat: description"  # Commit + push
```

---

## The Gathering

```
SUMMON → ORGANIZE → EXECUTE → VALIDATE → COMPLETE
   ↓         ↲          ↲          ↲          ↓
Receive  Dispatch   Animals    Verify   Feature
Request  Animals    Work       All      Ready
```

### Animals Mobilized

1. **🐕 Bloodhound** — Scout the codebase, understand patterns
2. **🐘 Elephant** — Build the multi-file feature
3. **🐢 Turtle** — Harden what was built (secure by design, not bolted on)
4. **🦫 Beaver** — Write comprehensive tests (including hardened code)
5. **🦝 Raccoon** — Security audit and cleanup
6. **🦌 Deer** — Accessibility audit
7. **🦊 Fox** — Performance optimization
8. **🦉 Owl** — Document the feature

---

### Phase 1: SUMMON

_The drum sounds. The forest listens..._

Receive and parse the request:

**Clarify the Feature:**

- What does this feature do?
- Which users benefit?
- What's in scope? What's out?
- Any existing issues or specs?

**Confirm:**

> "I'll mobilize a gathering for: **[feature description]**
>
> This will involve:
>
> - 🐕 Bloodhound scouting the codebase
> - 🐘 Elephant building across **[estimated files]** files
> - 🐢 Turtle hardening security by design
> - 🦫 Beaver writing tests
> - 🦝 Raccoon auditing for secrets and cleanup
> - 🦌 Deer checking accessibility
> - 🦊 Fox optimizing performance
> - 🦉 Owl writing documentation
>
> Proceed with the gathering?"

---

### Phase 2: ORGANIZE

_The animals assemble, knowing their roles..._

Dispatch in sequence:

**Dispatch Order:**

```
Bloodhound ──→ Elephant ──→ Turtle ──→ Beaver ──→ Raccoon ──→ Deer ──→ Fox ──→ Owl
   │              │            │          │           │          │        │       │
   │              │            │          │           │          │        │       │
Scout          Build       Harden      Test       Secrets    a11y    Speed   Docs
Patterns      Feature     Security    Coverage    Cleanup    Check   Opt     Write
```

**Cross-Cutting Standard — Signpost Error Codes:**
All animals MUST use Signpost error codes (from `@autumnsgrove/groveengine/errors`). This is not optional:

- **Elephant** uses them when building (buildErrorJson in API routes, throwGroveError in page loads)
- **Turtle** verifies all errors use Signpost codes during hardening (Phase 2E checklist)
- **Beaver** tests that API routes return proper `error_code` fields
- **Raccoon** audits for bare `throw error()` and `console.error` without `logGroveError()`
- Client-side feedback uses `toast` from `@autumnsgrove/groveengine/ui`

See `AgentUsage/error_handling.md` for the full reference.

**Dependencies:**

- Bloodhound must complete before Elephant (needs context)
- Elephant must complete before Turtle (hardens what was built)
- Turtle must complete before Beaver (tests the hardened code)
- Beaver must complete before Raccoon (tests catch remaining issues)
- Raccoon, Deer, Fox can run in parallel after Beaver
- Owl last (documents everything)

**Why Turtle before Beaver:**
Security is not a phase you bolt on after testing — it shapes _what_ you build. The Turtle reviews Elephant's work and hardens it: adds input validation schemas, output encoding, parameterized queries, security headers. Then Beaver tests the hardened code, catching both functional and security regressions. This is secure by design.

---

### Phase 3: EXECUTE

_The animals work. The forest transforms..._

Execute each phase:

**🐕 BLOODHOUND — SCOUT**

```
"Scouting the codebase for [feature]..."

Output:
- Files that will need changes
- Patterns to follow
- Integration points identified
- Potential obstacles found
```

**🐘 ELEPHANT — BUILD**

```
"Building [feature] with momentum..."

Output:
- All required files created/modified
- Frontend components
- Backend API endpoints
- Database schema changes
- Integration wired
```

**🐢 TURTLE — HARDEN**

```
"Withdrawing to study what was built..."

Output:
- Input validation added (Zod schemas on all endpoints)
- Output encoding verified (context-aware)
- Parameterized queries enforced (zero concatenation)
- Security headers configured (CSP, HSTS, etc.)
- Error handling hardened (generic messages, no leaks)
- Defense-in-depth layers applied
```

**🦫 BEAVER — TEST**

```
"Building test dams for confidence..."

Output:
- Integration tests for user flows
- Unit tests for complex logic
- Security regression tests (from Turtle's hardening)
- Edge case coverage
- All tests passing
```

**🦝 RACCOON — AUDIT**

```
"Rummaging for security risks..."

Output:
- Secrets scan (none found)
- Vulnerability check (clean)
- Input validation verified
- Auth checks confirmed
```

**🦌 DEER — SENSE**

```
"Sensing accessibility barriers..."

Output:
- Keyboard navigation works
- Screen reader compatible
- Color contrast passes
- Reduced motion respected
```

**🦊 FOX — OPTIMIZE**

```
"Hunting for performance gains..."

Output:
- Bundle size optimized
- Database queries fast
- Images optimized
- Caching implemented
```

**🦉 OWL — ARCHIVE**

```
"Archiving knowledge for the forest..."

Output:
- Help documentation written
- API documentation updated
- Code comments added
- README updated
```

---

### Phase 4: VALIDATE

_The work is done. Each animal verifies their contribution..._

**MANDATORY: Run full affected-package verification before the gathering concludes.**

This is the final quality gate — the moment the entire gathering's work is proven sound:

```bash
# Step 1: Sync all dependencies
pnpm install

# Step 2: Run affected-only CI — lint, check, test, build on ONLY packages the gathering touched
gw ci --affected --fail-fast --diagnose
```

**If verification fails:** Identify which animal's work caused the failure. Return to that phase, fix the issue, and re-run verification. The gathering does not conclude on broken code.

**Validation Checklist (after CI passes):**

- [ ] CI: `gw ci --affected` passes clean (lint, check, test, build)
- [ ] Bloodhound: All integration points mapped
- [ ] Elephant: Feature functional end-to-end
- [ ] Turtle: Input validation on all entry points
- [ ] Turtle: Output encoding on all exit points
- [ ] Turtle: Security headers configured
- [ ] Turtle: Defense-in-depth layers verified
- [ ] Beaver: All tests passing, coverage adequate
- [ ] Raccoon: No secrets or dead code found
- [ ] Deer: WCAG AA compliance verified
- [ ] Fox: Performance targets met
- [ ] Owl: Documentation complete

**Quality Gates:**

```
If CI fails:
  → Read diagnostics (--diagnose output)
  → Identify the responsible animal phase
  → Fix the issue
  → Re-run: gw ci --affected --fail-fast --diagnose
  → Repeat until clean

If any animal finds critical issues:
  → Return to that phase
  → Fix the issue
  → Re-run CI verification
  → Continue validation

If all gates pass:
  → Proceed to COMPLETE
```

---

### Phase 5: COMPLETE

_The gathering ends. A feature stands complete..._

**Completion Report:**

```markdown
## 🌲 GATHERING FEATURE COMPLETE

### Feature: [Name]

### Animals Mobilized

🐕 Bloodhound → 🐘 Elephant → 🐢 Turtle → 🦫 Beaver → 🦝 Raccoon → 🦌 Deer → 🦊 Fox → 🦉 Owl

### What Was Built

- **Files Changed:** [count]
- **New Components:** [list]
- **API Endpoints:** [list]
- **Database Changes:** [summary]

### Quality Verification

- ✅ Tests: [X] passing, [Y]% coverage
- ✅ Hardened: Input validation, output encoding, security headers
- ✅ Security: No secrets or vulnerabilities found
- ✅ Accessibility: WCAG AA compliant
- ✅ Performance: [metrics]
- ✅ Documentation: Complete

### Artifacts Created

- Source code (committed)
- Tests ([location])
- Documentation ([location])
- Migration scripts (if applicable)

### Time Elapsed

[Duration]

_The forest grows. The feature lives._
```

---

## Example Gathering

**User:** "/gathering-feature Add a bookmarking system for posts"

**Gathering execution:**

1. 🌲 **SUMMON** — "Mobilizing for: Bookmarking system. Allow users to save posts for later."

2. 🌲 **ORGANIZE** — "Dispatch sequence: Bloodhound → Elephant → Turtle → Beaver → Raccoon + Deer + Fox → Owl"

3. 🌲 **EXECUTE** —
   - 🐕 Scout: "Found post components, user service patterns, database conventions"
   - 🐘 Build: "Created bookmark service, API endpoints, UI components, database schema"
   - 🐢 Harden: "Added Zod validation on bookmark endpoints, parameterized all queries, output encoding on bookmark titles, CSP headers configured"
   - 🦫 Test: "Added 18 tests covering CRUD operations, auth checks, security regressions, edge cases"
   - 🦝 Audit: "No secrets, clean dependencies, dead code removed"
   - 🦌 Sense: "Keyboard nav works, screen reader announces, contrast passes"
   - 🦊 Optimize: "Lazy loaded bookmarks, indexed queries, compressed images"
   - 🦉 Archive: "Help doc written, API documented, code commented"

4. 🌲 **VALIDATE** — "All quality gates pass"

5. 🌲 **COMPLETE** — "Feature deployed, hardened, tested, audited, documented — secure from birth"

---

_When the drum sounds, the forest answers._ 🌲
