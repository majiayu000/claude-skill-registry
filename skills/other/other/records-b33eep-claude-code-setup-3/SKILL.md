# Record 032: Kotlin Standards Skill

## Status

Done

---

## Problem

**What problem are we solving?**

Kotlin developers using claude-code-setup have no language-specific coding standards and best practices. Currently, context skills exist for Python, TypeScript, JavaScript, Shell, and Java, but Kotlin is missing, even though it's increasingly used for Android development, backend (Spring Boot, Ktor), and Kotlin Multiplatform (KMP).

**Why does it need to be solved?**

1. **Consistency**: Kotlin projects need uniform conventions (naming, package structure, idioms)
2. **Quality**: Kotlin has specific best practices (coroutines, flows, sealed classes, data classes) that should be followed
3. **Ecosystem**: Kotlin tooling (Gradle, Maven, ktlint, detekt) must be understood and used correctly
4. **Parity**: Other major languages have context skills that auto-load based on tech stack
5. **Modern Features**: Kotlin 2.3.0 (LTS) brings new features (explicit backing fields, UUID API, K2 compiler) that should be utilized

**What happens if we do nothing?**

- Kotlin developers receive generic code without language-specific best practices
- Inconsistent code quality compared to projects using Python/TypeScript/Java skills
- Manual corrections required for convention violations
- Missed opportunities for modern Kotlin features (coroutines, flows, sealed classes)
- No standardized approach to common Kotlin challenges

**Concrete problems without Kotlin skill:**
- No guidance on Coroutines and Structured Concurrency
- No Flow patterns (StateFlow vs SharedFlow vs MutableStateFlow)
- No Sealed Classes/Interfaces for type-safe state modeling
- No Data Class best practices (copy, destructuring)
- No build tool guidance (Gradle Kotlin DSL vs Groovy DSL)
- No Multiplatform patterns

## Options Considered

### Option A: Core Kotlin Standards (Like standards-shell)
- **Approach:** Pure Kotlin language skill without framework-specific guidance
- **Pros:** Universal, framework-agnostic; lightweight; clear separation (language vs framework)
- **Cons:** Incomplete for Android/backend developers; framework patterns must be added manually; no multiplatform guidance

### Option B: Core Kotlin + Framework Extensions (Like standards-java)
- **Approach:** Base skill for Kotlin core (naming, coroutines, flows, data classes, testing), separate extension skills for Android/Spring/Ktor later
- **Pros:** Modular, lightweight for simple projects; extensible for enterprise needs; clear separation (core vs frameworks); users with simple projects don't load unnecessary Android/Spring context
- **Cons:** More files to maintain; extension skills must be created later

### Option C: Comprehensive Kotlin Skill with Frameworks
- **Approach:** One large skill with Android, Spring Boot, Ktor, Multiplatform
- **Pros:** Complete coverage for all Kotlin developers; all scenarios in one file
- **Cons:** Large skill file slows down context loading; too broad for simple Kotlin projects; hard to maintain

### Option D: Kotlin with MCP Server for Documentation
- **Approach:** Core skill + MCP Server for kotlinlang.org/Android Docs/Ktor Docs
- **Pros:** Live access to current documentation; always up-to-date
- **Cons:** Complex setup requirement; MCP Server necessary (additional dependency); not all users need live docs (standards usually sufficient)

### Decision

**Option B: Core Kotlin + Framework Extensions**

**Rationale:**
- Same approach as standards-java (proven, Record 031)
- Modular and lightweight for all Kotlin projects
- Kotlin core is universally applicable (Android, backend, multiplatform)
- Extension skills (standards-android, standards-spring-kotlin, standards-ktor) can be added later based on user needs
- Users with simple Kotlin projects don't load unnecessary framework context
- MCP Server is not necessary - Kotlin standards and best practices are stable enough
- Focus on Kotlin 2.3.0 LTS with modern features (K2 compiler, coroutines, flows)

## Solution

### Base Skill: standards-kotlin

Create a context skill following the established pattern of standards-python, standards-typescript, standards-shell, and standards-java.

**File Location:**
- `~/.claude/skills/standards-kotlin/SKILL.md`

**Auto-Loading:**
- Tech Stack contains: "kotlin"
- File extensions: `.kt`, `.kts`
- Applies to: `[kotlin, gradle, maven, junit, kotest, kotlinx-coroutines, ktor, spring]`

**Content Structure:**

1. **Core Principles** - Readability, Explicitness, Null Safety, Immutability
2. **Naming Conventions** - Classes, Functions, Properties, Constants, Packages
3. **Project Structure**
   - Gradle Kotlin DSL (build.gradle.kts) - preferred
   - Maven (pom.xml) - alternative
   - Source Sets (src/main/kotlin, src/test/kotlin)
4. **Modern Kotlin Features (2.0-2.3)**
   - K2 Compiler (stable since 2.0, performance improvements)
   - Data Classes (copy, destructuring, componentN)
   - Sealed Classes/Interfaces (exhaustive when expressions)
   - Inline Value Classes (zero-cost wrappers)
   - Context Receivers (experimental, 2.2+)
   - Explicit Backing Fields (experimental, 2.3)
   - UUID API (experimental, 2.3)
5. **Coroutines & Concurrency**
   - Structured Concurrency (coroutineScope, supervisorScope)
   - Dispatchers (Main, IO, Default, Unconfined)
   - launch vs async (fire-and-forget vs result)
   - Job lifecycle, cancellation, exception handling
6. **Flow API**
   - StateFlow vs SharedFlow vs MutableStateFlow
   - Cold vs Hot Flows
   - Flow operators (map, filter, flatMapConcat, collectLatest)
   - Flow best practices (single source of truth)
7. **Null Safety**
   - Safe calls (?.), Elvis operator (?:), !! operator
   - lateinit vs lazy initialization
   - Nullable types vs Java Optional
8. **Collections & Sequences**
   - List vs MutableList, immutability by default
   - Sequence for lazy evaluation on large collections
   - Collection operations (map, filter, fold, reduce)
9. **Testing Fundamentals**
   - JUnit 5 + kotlin.test annotations
   - Kotest (optional modern alternative)
   - Mockk for mocking (Kotlin-native)
   - Coroutines testing (runTest, TestDispatcher)
10. **Build Tool Awareness**
    - Gradle Kotlin DSL best practices (buildSrc, version catalogs)
    - Dependency management (implementation vs api vs compileOnly)
    - Maven for Kotlin projects (kotlin-maven-plugin)
11. **Recommended Tooling**
    - ktlint (code formatting, auto-fix)
    - detekt (static analysis, code smells)
    - kotlinx-serialization (JSON, protobuf)
    - Kotlin compiler plugins (all-open, no-arg, sam-with-receiver)

**Design Decisions:**

- **No MCP Server initially**: Standards skill provides guidance without external dependencies. If live documentation search becomes critical, consider adding MCP later.
- **No framework specifics**: Android, Spring Boot, Ktor patterns belong in separate extension skills
- **Focus on Kotlin 2.3.0 LTS**: Document modern features, mark experimental features clearly (explicit backing fields, context receivers)
- **Practical examples**: Include code snippets for each section (similar to standards-shell and standards-java)
- **Tool integration guidance**: Reference tools but don't require them
- **Gradle Kotlin DSL preference**: Recommend Kotlin DSL over Groovy DSL for type safety and IDE support

### Future Extension Skills

These will be created later based on user needs:

1. **standards-android** - Android-specific patterns (Jetpack Compose, ViewModels, Room, Hilt/Koin DI)
2. **standards-spring-kotlin** - Spring Boot with Kotlin (WebFlux, R2DBC, Kotlin DSL for beans)
3. **standards-ktor** - Ktor Server/Client patterns (routing, plugins, serialization)
4. **standards-kmp** - Kotlin Multiplatform (expect/actual, common code, platform-specific implementations)

### Installation Integration

**Install Script (`install.sh`):**
- Add standards-kotlin to available skills
- No new dependencies required (jq, git already checked)

**Skill Metadata (SKILL.md front matter):**
```yaml
---
name: standards-kotlin
description: Kotlin coding standards for modern applications. Includes naming conventions, coroutines, flows, and recommended tooling.
type: context
applies_to: [kotlin, gradle, maven, junit, kotest, kotlinx-coroutines, ktor, spring]
---
```

**Testing:**
- Add test scenario for standards-kotlin skill loading
- Verify auto-load on Tech Stack: "Kotlin"
- Verify task-based loading on `.kt` file edit

## User Stories

### Story 1: Create standards-kotlin Skill File
**As a** Kotlin developer
**I want** a standards-kotlin skill with coding standards and best practices
**So that** Claude generates consistent, high-quality Kotlin code

**Acceptance Criteria:**
- [ ] Create `~/.claude/skills/standards-kotlin/SKILL.md`
- [ ] Include YAML front matter: name, description, type: context, applies_to: [kotlin, gradle, maven, junit, kotest, kotlinx-coroutines, ktor, spring]
- [ ] Core Principles section (readability, explicitness, null safety, immutability)
- [ ] Naming Conventions section (classes, functions, properties, constants with examples)
- [ ] Project Structure section (Gradle Kotlin DSL, Maven, source sets)
- [ ] Modern Kotlin Features section organized by version (2.0-2.3):
  - K2 Compiler (stable since 2.0)
  - Data Classes (copy, destructuring, componentN)
  - Sealed Classes/Interfaces (exhaustive when)
  - Inline Value Classes (zero-cost wrappers)
  - Context Receivers (experimental, 2.2+)
  - Explicit Backing Fields (experimental, 2.3)
  - UUID API (experimental, 2.3)
- [ ] Coroutines & Concurrency section (structured concurrency, dispatchers, launch vs async, cancellation)
- [ ] Flow API section (StateFlow vs SharedFlow vs MutableStateFlow, cold vs hot flows, operators, best practices)
- [ ] Null Safety section (safe calls ?., Elvis ?:, !!, lateinit vs lazy)
- [ ] Collections & Sequences section (List vs MutableList, Sequence for lazy evaluation)
- [ ] Testing Fundamentals section (JUnit 5, kotlin.test, Mockk, coroutines testing with runTest)
- [ ] Build Tool Awareness section (Gradle Kotlin DSL, Maven, dependency management)
- [ ] Recommended Tooling section (ktlint, detekt, kotlinx-serialization, compiler plugins)
- [ ] Production Best Practices section (15+ rules)
- [ ] Follow same format/structure as standards-python, standards-typescript, standards-java

**Priority:** High
**Status:** Pending

### Story 2: Integrate standards-kotlin into Install Script
**As a** user
**I want** standards-kotlin available in the installer
**So that** I can install it like other skills

**Acceptance Criteria:**
- [ ] Add standards-kotlin to `skills/` directory structure
- [ ] Update install.sh to recognize standards-kotlin as available skill
- [ ] Skill appears in interactive toggle selection menu
- [ ] Skill installs to `~/.claude/skills/standards-kotlin/`
- [ ] installed.json tracks standards-kotlin installation
- [ ] /claude-code-setup command shows standards-kotlin as available/installed

**Priority:** High
**Status:** Pending

### Story 3: Add E2E Test for standards-kotlin
**As a** maintainer
**I want** automated tests for standards-kotlin skill
**So that** I can verify it installs and loads correctly

**Acceptance Criteria:**
- [ ] Create test scenario in `tests/scenarios/` for standards-kotlin (e.g., 19-standards-kotlin-skill.sh)
- [ ] Test: Install standards-kotlin via install.sh
- [ ] Test: Verify skill file exists in `~/.claude/skills/standards-kotlin/SKILL.md`
- [ ] Test: Verify installed.json contains standards-kotlin entry
- [ ] Test: Verify YAML front matter structure (name, type, applies_to fields)
- [ ] Test: Validate all required content sections present (11+ sections)
- [ ] Test: Check coverage of modern Kotlin features (data classes, sealed classes, coroutines, flows)
- [ ] Test: Verify applies_to field includes key keywords (kotlin, gradle, kotlinx-coroutines)
- [ ] Test: Verify no deps.json present (standards-kotlin has no external dependencies)
- [ ] Test: Run full test suite (`./tests/test.sh`) to ensure no regressions in existing tests
- [ ] Test passes in CI pipeline (GitHub Actions)

**Priority:** Medium
**Status:** Pending

**Note:** When developing tests, always run the full test suite (`./tests/test.sh`) to verify the build runs successfully and no existing tests are broken.

### Story 4: Update Documentation
**As a** user
**I want** documentation about standards-kotlin skill
**So that** I know it exists and how to use it

**Acceptance Criteria:**
- [ ] Add standards-kotlin to README.md skills table (sorted alphabetically)
- [ ] Create `website/pages/features/skills/standards-kotlin.mdx` documentation page
- [ ] Add to `website/pages/features/skills/_meta.js` navigation
- [ ] Document auto-loading behavior (Tech Stack: kotlin, file extensions: .kt, .kts)
- [ ] Include practical code examples (data classes, coroutines, flows, sealed classes)
- [ ] Mention future extension skills (standards-android, standards-spring-kotlin, standards-ktor, standards-kmp)
- [ ] Update CHANGELOG.md with new content version entry
- [ ] Update `templates/VERSION` (increment from 37 to 38)
- [ ] Update README.md content badge (v37 → v38)

**Priority:** Medium
**Status:** Pending
