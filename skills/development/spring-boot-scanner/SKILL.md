---
name: spring-boot-scanner
description: Smart code scanner that detects Spring Boot patterns and routes to appropriate skills. Auto-invokes when editing Java or Kotlin files in Spring Boot projects, working with pom.xml/build.gradle containing spring-boot-starter, or when context suggests Spring Boot development. Detects annotations (@RestController, @Entity, @EnableWebSecurity, @SpringBootTest) to determine relevant skills and provides contextual guidance. Uses progressive automation - auto-invokes for low-risk patterns (web-api, data, DDD), confirms before loading high-risk skills (security, testing, verify).
---

# Spring Boot Scanner

Smart pattern detection and skill routing for Spring Boot projects.

## Core Behavior

**Trigger Conditions**:
- Editing `*.java` or `*.kt` files in a project with `spring-boot-starter` dependencies
- Working with `pom.xml` or `build.gradle*` containing Spring Boot
- User mentions "Spring Boot", "Spring Security", "Spring Data", etc.

**Action**: Scan code → Detect patterns → Route to appropriate skill

## Detection Algorithm

### Phase 1: Project Detection

```
1. Check for Spring Boot indicators:
   - Glob: **/pom.xml → grep spring-boot-starter
   - Glob: **/build.gradle* → grep org.springframework.boot

2. If Spring Boot detected → Continue to Phase 2
   If not → Exit (not a Spring Boot project)
```

### Phase 2: Annotation Scanning

Scan current file or changed files for these annotation patterns:

| Annotation Pattern | Detected Skill | Risk Level |
|-------------------|----------------|------------|
| `@RestController`, `@GetMapping`, `@PostMapping`, `@RequestMapping` | spring-boot-web-api | LOW |
| `@Entity`, `@Repository`, `@Aggregate`, `@MappedSuperclass` | spring-boot-data-ddd | LOW |
| `@Service` in `**/domain/**` or `**/service/**` | domain-driven-design | LOW |
| `@ApplicationModule`, `@ApplicationModuleListener` | spring-boot-modulith | LOW |
| `@Timed`, `@Counted`, `HealthIndicator`, `MeterRegistry` | spring-boot-observability | LOW |
| `@EnableWebSecurity`, `@PreAuthorize`, `@Secured`, `SecurityFilterChain` | spring-boot-security | HIGH |
| `@SpringBootTest`, `@WebMvcTest`, `@DataJpaTest`, `@MockitoBean` | spring-boot-testing | HIGH |
| `@MockBean` (deprecated) | spring-boot-testing | HIGH + WARNING |
| Build file with version < 4.0 | spring-boot-verify | HIGH |

### Phase 3: Risk-Based Routing

**LOW RISK (Auto-Invoke)**:
- Provide skill guidance immediately
- No confirmation required
- Skills: web-api, data-ddd, domain-driven-design, modulith, observability

**HIGH RISK (Suggest + Confirm)**:
- Present recommendation to user
- Wait for confirmation before loading full skill
- Skills: security, testing, verify

## Routing Workflow

```
ON detecting patterns:

1. LOW RISK patterns detected:
   → "I notice you're working with [pattern]. Here's guidance from spring-boot-[skill]:"
   → Load skill's Quick Reference section
   → Provide contextual tips

2. HIGH RISK patterns detected:
   → Use AskUserQuestion:
     "I detected [security/testing/migration] patterns. Would you like me to:
     - Load spring-boot-[skill] for detailed guidance
     - Run a verification scan
     - Continue without skill guidance"
   → Wait for user choice
   → Route accordingly

3. Multiple patterns detected:
   → Prioritize HIGH RISK (always ask)
   → Batch LOW RISK (summarize all)
   → Example: "Detected REST controller and security config. Loading web-api guidance. For security patterns, would you like detailed review?"
```

## Quick Reference: Annotation → Skill Map

Use this script to detect patterns:

```bash
# Run from project root
python3 scripts/detect_patterns.py /path/to/file.java
```

Or use Grep directly:

```bash
# Web API detection
grep -l "@RestController\|@GetMapping\|@PostMapping" **/*.java

# Security detection
grep -l "@EnableWebSecurity\|@PreAuthorize\|SecurityFilterChain" **/*.java

# Testing detection
grep -l "@SpringBootTest\|@WebMvcTest\|@MockitoBean\|@MockBean" **/*.java
```

## Escalation Triggers

Always confirm before proceeding when detecting:

| Pattern | Reason | Action |
|---------|--------|--------|
| `@EnableGlobalMethodSecurity` | Deprecated in Security 6+ | Confirm + Migration guidance |
| `@MockBean` | Deprecated in Boot 3.4+ | Confirm + Show @MockitoBean |
| `spring-boot-starter-parent` < 3.0 | Major migration needed | Confirm + Suggest verify-upgrade |
| `.and()` in security config | Removed in Security 7 | Confirm + Lambda DSL guidance |
| `com.fasterxml.jackson` | Jackson 3 migration | Confirm + Namespace change |

## Integration with Existing Components

**Delegates to Skills**:
- `spring-boot-web-api` → REST patterns
- `spring-boot-data-ddd` → Repository/Entity patterns
- `spring-boot-security` → Security configuration
- `spring-boot-testing` → Test patterns
- `spring-boot-modulith` → Module structure
- `spring-boot-observability` → Metrics/Health
- `spring-boot-verify` → Dependencies/Config
- `domain-driven-design` → DDD architecture

**Delegates to Agents** (for comprehensive review):
- `spring-boot-reviewer` → Full codebase review
- `spring-boot-upgrade-verifier` → Migration analysis

**When to delegate to agents**:
- User asks for "review" or "scan" of entire project
- Multiple HIGH RISK patterns across many files
- Explicit `/spring-review` or `/verify-upgrade` command

## Known Limitations

- **Annotation-based only**: Detects standard Spring annotations, not custom/meta-annotations or XML configuration
- **Java and Kotlin only**: Scans `*.java` and `*.kt` files; no Groovy/Scala support
- **Spring Boot 3.x+ optimized**: Escalation patterns focus on Boot 3.x → 4.x migration; older versions may have gaps
- **No AST parsing**: Uses regex matching, so patterns in comments/strings may cause false positives

## Model Tier Performance

The scanner is designed for reliability across all model tiers:

| Aspect | Behavior |
|--------|----------|
| **Haiku/Sonnet/Opus** | All fully supported |
| **Determinism** | Python script ensures consistent results regardless of model |
| **Single file scan** | <100ms typical |
| **Project scan** | 1-2s for typical projects (recursive) |

The Python detection script handles heavy lifting, making results model-independent.

## Escape Hatch

If scanner guidance isn't helpful for the current context:

| Scenario | Action |
|----------|--------|
| Skip LOW RISK guidance | Ignore suggestions and continue working |
| Skip HIGH RISK confirmation | Select "Continue without guidance" option |
| Need comprehensive review | Use `/spring-review` command instead |
| Disable temporarily | Remove `spring-boot-scanner` from active skills |

The scanner is advisory—it suggests skills but never blocks your workflow.

## Detailed References

- **Workflow**: See [WORKFLOW.md](WORKFLOW.md) for step-by-step detection flow
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for trigger scenarios
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- **Detection Script**: See [scripts/detect_patterns.py](scripts/detect_patterns.py) for programmatic detection

## Critical Reminders

1. **Always check project type first** — Only activate for Spring Boot projects
2. **Respect risk levels** — Never auto-invoke security/testing/verify without confirmation
3. **Batch notifications** — Don't spam user with multiple skill suggestions
4. **Delegate to agents for scale** — Use reviewer agent for multi-file analysis
5. **Preserve user flow** — Guidance should assist, not interrupt
