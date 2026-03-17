# Record 031: Java Developer Skill

## Status

Done

---

## Problem

Java developers using claude-code-setup lack language-specific coding standards and best practices. Currently, context skills exist for Python, TypeScript, JavaScript, and Shell, but Java is notably absent despite being widely used in enterprise applications.

**What problem are we solving?**

When Claude generates or modifies Java code without Java-specific standards:
- Code lacks consistency with enterprise Java conventions (naming, package structure, error handling)
- No guidance on build tools (Maven vs Gradle) and dependency management
- Missing patterns for common frameworks (Spring Boot, Jakarta EE, Quarkus)
- No integration guidance for Java ecosystem tools (JUnit, Mockito, checkstyle, spotbugs, SonarQube)
- Inconsistent approach to logging, exception handling, and resource management

**Why does it need to be solved?**

1. **Consistency**: Java projects require strict adherence to conventions (especially in enterprise environments)
2. **Quality**: Java has specific best practices (try-with-resources, Optional, Stream API) that should be followed
3. **Ecosystem**: Java tooling (Maven/Gradle, testing, static analysis) needs to be understood and properly used
4. **Parity**: Other major languages have context skills that auto-load based on tech stack

**What happens if we do nothing?**

- Java developers get generic code without language-specific best practices
- Inconsistent code quality compared to projects using Python/TypeScript skills
- Manual corrections needed for convention violations
- Missed opportunities for modern Java features (records, sealed classes, pattern matching)
- No standardized approach to common Java challenges (dependency injection, transaction management, etc.)

## Options Considered

### Option A: Comprehensive Enterprise Java Skill
- **Approach:** Single skill covering everything from Spring Boot to Jakarta EE, Maven/Gradle, testing, security, performance
- **Pros:** Complete coverage for enterprise Java developers, addresses all common scenarios
- **Cons:** Large skill file may slow down context loading, too broad for simple Java projects

### Option B: Core Java Standards + Framework Extensions
- **Approach:** Base skill covers core Java language (naming conventions, patterns, modern Java features, basic tooling), with separate optional extension skills for Spring/Jakarta EE/Quarkus created later as needed
- **Pros:** Modular design, lightweight for simple projects, extensible for enterprise needs, clear separation of concerns
- **Cons:** More files to maintain, requires creating additional skills for full enterprise coverage

### Option C: Spring-Focused Java Skill
- **Approach:** Focus primarily on Spring Boot/Spring Framework as the dominant Java framework
- **Pros:** Matches most modern Java development, clear focus, complete coverage of Spring ecosystem
- **Cons:** Excludes Jakarta EE, Quarkus, and non-framework Java users, not universal

### Option D: Core Java Only (Like standards-shell)
- **Approach:** Pure Java language standards without framework-specific guidance
- **Pros:** Universal, framework-agnostic, clean separation of concerns, lightweight
- **Cons:** Incomplete for enterprise developers, framework patterns need to be added manually

### Decision

**Option B: Core Java Standards + Framework Extensions**

Create a focused `standards-java` skill covering core Java language conventions and best practices. Framework-specific patterns (Spring, Jakarta EE, Quarkus) and potentially build tool specifics (Maven, Gradle) will be separate extension skills created later as needed.

**Reasoning:**
- Modular approach allows lightweight base for all Java projects
- Extension skills can be added based on actual user needs
- Follows single-responsibility principle - base skill handles language, extensions handle frameworks
- Users working on simple Java projects don't load unnecessary Spring/Jakarta EE context
- Enterprise developers can combine base + framework skills for complete coverage

## Solution

### Base Skill: standards-java

Create a context skill following the established pattern of standards-python, standards-typescript, and standards-shell.

**File Location:**
- `~/.claude/skills/standards-java/SKILL.md`

**Auto-Loading:**
- Tech Stack contains: "java"
- File extensions: `.java`
- Applies to: [java, maven, gradle, junit, spring, jakarta, quarkus]

**Content Structure:**

1. **Core Principles** - Readability, maintainability, SOLID, DRY
2. **Naming Conventions** - Classes, methods, packages, constants, variables
3. **Modern Java Features** (Java 17+)
   - Records for immutable data
   - Sealed classes for restricted hierarchies
   - Pattern matching (instanceof, switch)
   - Text blocks for multi-line strings
   - Switch expressions
4. **Code Organization**
   - Package structure
   - Visibility modifiers (public, protected, package-private, private)
   - SOLID principles application
5. **Exception Handling**
   - Checked vs unchecked exceptions
   - Try-with-resources
   - Custom exception hierarchies
6. **Collections & Streams API**
   - When to use List, Set, Map
   - Stream operations and best practices
   - Collectors usage
7. **Optional & Null Handling**
   - Prefer Optional for return values
   - Null-safety patterns
8. **Testing Fundamentals**
   - JUnit 5 basics
   - Mockito for mocking
   - Test naming conventions
9. **Build Tool Awareness**
   - Maven project structure (pom.xml, src/main/java, src/test/java)
   - Gradle project structure (build.gradle, settings.gradle)
   - Dependency declaration patterns
10. **Recommended Tooling**
    - checkstyle for style checking
    - spotbugs for bug detection
    - JaCoCo for code coverage
    - Maven Enforcer / Gradle verification

**Design Decisions:**

- **No MCP Server initially**: Standards skill provides guidance without external dependencies. If documentation search or dependency analysis becomes critical, consider adding MCP later.
- **No framework specifics**: Spring, Jakarta EE, Quarkus patterns belong in separate extension skills
- **Focus on modern Java**: Recommend latest LTS (Java 21/25), document features available since Java 17+
- **Practical examples**: Include code snippets for each section (similar to standards-shell)
- **Tool integration guidance**: Reference tools but don't require them

### Future Extension Skills

These will be created later based on user needs:

1. **standards-spring** - Spring Boot, dependency injection, REST controllers, Spring Data
2. **standards-jakartaee** - CDI, JAX-RS, JPA, Jakarta EE patterns
3. **standards-quarkus** - Quarkus-specific reactive patterns, native compilation
4. **maven-expert** / **gradle-expert** - Deep build tool guidance (if needed)

### Installation Integration

**Install Script (`install.sh`):**
- Add standards-java to available skills
- No new dependencies required (jq, git already checked)

**Skill Metadata (SKILL.md front matter):**
```yaml
---
name: standards-java
description: Java coding standards for enterprise applications. Includes naming conventions, modern Java features, and recommended tooling.
type: context
applies_to: [java, maven, gradle, junit, spring, jakarta, quarkus]
---
```

**Testing:**
- Add test scenario for standards-java skill loading
- Verify auto-load on Tech Stack: "Java"
- Verify task-based loading on `.java` file edit

## User Stories

### Story 1: Create standards-java Skill File
**As a** Java developer
**I want** a standards-java skill with coding standards and best practices
**So that** Claude generates consistent, high-quality Java code

**Acceptance Criteria:**
- [x] Create `~/.claude/skills/standards-java/SKILL.md`
- [x] Include YAML front matter: name, description, type: context, applies_to: [java, maven, gradle, junit, spring, jakarta, quarkus]
- [x] Core Principles section (readability, maintainability, SOLID, DRY)
- [x] Naming Conventions section (classes, methods, packages, constants, variables with examples)
- [x] Modern Java Features section organized by version:
  - Java 17: records, sealed classes, pattern matching, text blocks, switch expressions
  - Java 21: virtual threads, sequenced collections, record patterns, pattern matching for switch
  - Java 25: flexible main methods, scoped values, gatherers, primitive pattern matching (preview)
- [x] Note recommending latest LTS (Java 21/25) for new projects
- [x] Code Organization section (package structure, visibility, SOLID principles)
- [x] Exception Handling section (checked vs unchecked, try-with-resources, custom exceptions)
- [x] Collections & Streams API section (List/Set/Map usage, Stream best practices)
- [x] Optional & Null Handling section
- [x] Testing Fundamentals section (JUnit 5, Mockito basics)
- [x] Build Tool Awareness section (Maven and Gradle project structure)
- [x] Recommended Tooling section (checkstyle, spotbugs, JaCoCo)
- [x] Follow same format/structure as standards-python, standards-typescript, standards-shell

**Priority:** High
**Status:** Done

**Implementation Notes:**
- Created comprehensive 630-line skill file following standards-python/typescript/shell pattern
- Added YAML front matter with extended applies_to list (included mockito, testcontainers, hibernate, jpa)
- Structured with clear sections: Core Principles, Naming, Project Structure (Maven/Gradle), Modern Java Features
- Modern Java Features section organized by Java version (17, 21, 25):
  - Java 17: records, sealed classes, pattern matching, text blocks, switch expressions
  - Java 21: virtual threads, sequenced collections, record patterns, pattern matching for switch (finalized)
  - Java 25: flexible main methods, scoped values, gatherers, primitive pattern matching (preview)
- Added recommendation to use latest LTS (Java 21/25) for new projects
- All features include practical code examples
- Code Organization includes SOLID principles with concrete examples (SRP, DIP)
- Exception handling: checked vs unchecked guidance, try-with-resources, custom exception hierarchies
- Collections & Streams: when to use List/Set/Map, stream best practices, immutable collections with List.of/Set.of/Map.of
- Optional usage: return types vs parameters, chaining operations, null-safety with Objects utilities
- Testing: JUnit 5 with @BeforeEach/@Test/@ParameterizedTest, Mockito with @Mock/@InjectMocks, test naming conventions
- Build tools: Maven and Gradle project structures, dependency examples in both pom.xml and build.gradle.kts
- Recommended tooling: maven/gradle, junit-jupiter, mockito, checkstyle, spotbugs, jacoco, testcontainers
- Production best practices: 15 rules including immutability, DI, fail fast, explicit code, resource management
- Comments guidance: less is more, explain WHY not WHAT
- References: Java Language Spec, Effective Java, Clean Code

### Story 2: Integrate standards-java into Install Script
**As a** user
**I want** standards-java available in the installer
**So that** I can install it like other skills

**Acceptance Criteria:**
- [x] Add standards-java to `skills/` directory structure
- [x] Update install.sh to recognize standards-java as an available skill
- [x] Skill appears in interactive toggle selection menu
- [x] Skill installs to `~/.claude/skills/standards-java/`
- [x] installed.json tracks standards-java installation
- [x] /claude-code-setup command shows standards-java as available/installed

**Priority:** High
**Status:** Done

**Implementation Notes:**
- No code changes to install.sh required - automatic discovery via directory scanning
- Install script discovers skills by scanning `$SCRIPT_DIR/skills/` for subdirectories (lib/modules.sh:706)
- Verified with `./install.sh --list`: standards-java appears in available skills
- Skill installation handled by existing `install_skill()` function (lib/skills.sh:100-126)
- Copies skill directory from `skills/standards-java/` to `~/.claude/skills/standards-java/`
- Tracking in installed.json handled by existing infrastructure (lib/helpers.sh:89-96)
- /claude-code-setup command discovers modules via `ls -1 "$temp_dir/skills/"` (commands/claude-code-setup.md:26)
- Interactive toggle selection includes standards-java automatically (lib/modules.sh:691-711)

### Story 3: Add E2E Test for standards-java
**As a** maintainer
**I want** automated tests for standards-java skill
**So that** I can verify it installs and loads correctly

**Acceptance Criteria:**
- [x] Create test scenario in `tests/scenarios/` for standards-java
- [x] Test: Install standards-java via install.sh
- [x] Test: Verify skill file exists in `~/.claude/skills/standards-java/SKILL.md`
- [x] Test: Verify installed.json contains standards-java entry
- [x] Test: Simulate Tech Stack "Java" and verify skill would load (check applies_to)
- [x] Test passes in CI pipeline

**Priority:** Medium
**Status:** Done

**Implementation Notes:**
- Created `tests/scenarios/18-standards-java-skill.sh` with comprehensive test coverage
- Test structure: 6 scenarios covering file structure, content sections, installation, tracking, auto-loading, and dependencies
- Verified YAML front matter structure (name, type, applies_to fields)
- Validated all 11 required content sections present: Core Principles, Naming Conventions, Modern Java Features, Code Organization, Exception Handling, Collections & Streams API, Optional & Null Handling, Testing Fundamentals, Build Tool Awareness, Recommended Tooling, Production Best Practices
- Checked coverage of 5 modern Java features: records, sealed classes, pattern matching, text blocks, switch expressions
- Installation test uses default skill selection (all pre-selected) for consistency with other skill tests
- Verified SHA256 hash match between source and installed SKILL.md
- Confirmed tracking in installed.json via jq query: `.skills | index("standards-java")`
- Validated applies_to field includes 5 key keywords: java, maven, gradle, junit, spring
- Verified no deps.json present (standards-java has no external dependencies)
- All 31 test assertions pass successfully

### Story 4: Update Documentation
**As a** user
**I want** documentation about standards-java skill
**So that** I know it exists and how to use it

**Acceptance Criteria:**
- [x] Add standards-java to README.md skills table
- [x] Create `website/pages/features/skills/standards-java.mdx` documentation page
- [x] Add to `website/pages/features/skills/_meta.js` navigation
- [x] Document auto-loading behavior (Tech Stack: java, file extensions: .java)
- [x] Mention future extension skills (standards-spring, standards-jakartaee, etc.)
- [x] Update CHANGELOG.md with new content version

**Priority:** Medium
**Status:** Done

**Implementation Notes:**
- Updated README.md skills table: Added Java row (sorted alphabetically) with tech stack "java, maven, gradle, spring, junit"
- Created `website/pages/features/skills/standards-java.mdx` (230 lines) following standards-python/typescript pattern
- Documentation sections: Metadata, Core Principles, Naming Conventions, Modern Java Features (records, sealed classes, pattern matching, text blocks), Code Organization, Exception Handling, Collections & Streams, Optional & Null Handling, Testing, Build Tools, Recommended Tooling, Production Checklist
- Included practical code examples for each section (10+ code blocks demonstrating modern Java patterns)
- Auto-loading metadata documented: applies_to includes java, maven, gradle, junit, spring, jakarta, quarkus, mockito, testcontainers, hibernate, jpa
- Future Extensions section: Explicitly mentions standards-spring, standards-jakartaee, standards-quarkus as planned separate skills
- Updated `website/pages/features/skills/_meta.js`: Added 'standards-java': 'Java' entry (alphabetically after index, before python)
- Updated CHANGELOG.md with Content v37 entry under [Unreleased] section
- Content v37 description: "Add `standards-java` skill for Java enterprise applications" with bullet points for core features, modern Java, testing, build tools, production practices, future extensions
- Updated `templates/VERSION` from 36 to 37
- Updated README.md badge from "Content v36" to "Content v37"
