---
name: spring-boot-scanner
description: Smart code scanner that detects Spring Boot patterns and routes to appropriate skills. Use when editing Java or Kotlin files in Spring Boot projects, working with pom.xml/build.gradle containing spring-boot-starter, or when context suggests Spring Boot development. Detects annotations (@RestController, @Entity, @EnableWebSecurity, @SpringBootTest) to determine relevant skills and provides contextual guidance. Uses progressive automation - auto-invokes for low-risk patterns (web-api, data, DDD), confirms before loading high-risk skills (security, testing, verify).
spring-boot-version: "4.0"
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

Scans in 3 phases: (1) detect Spring Boot project via build files, (2) scan annotations against the map below, (3) route by risk level — LOW auto-invokes, HIGH confirms first. See [WORKFLOW.md](WORKFLOW.md) for the full step-by-step detection flow.

## Annotation → Skill Map

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

## Escape Hatch

If scanner guidance isn't helpful for the current context:

| Scenario | Action |
|----------|--------|
| Skip LOW RISK guidance | Ignore suggestions and continue working |
| Skip HIGH RISK confirmation | Select "Continue without guidance" option |
| Need comprehensive review | Use `/spring-review` command instead |
| Disable temporarily | Remove `spring-boot-scanner` from active skills |

The scanner is advisory—it suggests skills but never blocks the workflow.

## Related Skills

| Need | Skill |
|------|-------|
| DDD concepts | `domain-driven-design` |
| Data layer | `spring-boot-data-ddd` |
| REST APIs | `spring-boot-web-api` |
| Security config | `spring-boot-security` |
| Full codebase review | Use `/spring-review` command |

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
