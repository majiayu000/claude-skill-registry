---
name: backend-javaee
description: (ePost) Use when working with Jakarta EE — JAX-RS endpoints, CDI/EJB services, JPA/Hibernate, WildFly deployment
user-invocable: false
metadata:
  keywords:
    - javaee
    - jakarta
    - jax-rs
    - hibernate
    - ejb
    - cdi
    - wildfly
    - jpa
  agent-affinity:
    - epost-fullstack-developer
    - epost-tester
    - epost-debugger
    - epost-code-reviewer
  platforms:
    - backend
---

# Jakarta EE Backend Patterns

## Critical: This is NOT Spring Boot

This backend uses **Jakarta EE conventions**:
- WAR packaging deployed to WildFly 26.1 application server
- Dependency injection via `@Inject` (CDI) and `@EJB`
- REST endpoints via `@Path`, `@GET`, `@POST` (JAX-RS / RESTEasy)
- Persistence via `persistence.xml` + `@Entity` (JPA/Hibernate 5.6)
- Transaction management via `@Transactional` (CDI) or container-managed (EJB)

Do NOT suggest Spring Boot patterns (no `@Autowired`, no `@SpringBootApplication`, no `application.properties`).

## Tech Stack
- **Language**: Java 8 | **Platform**: Jakarta EE 8 / WildFly 26.1
- **REST**: JAX-RS via RESTEasy | **ORM**: Hibernate 5.6
- **Databases**: PostgreSQL + MongoDB | **Build**: Maven
- **Microprofile**: Eclipse MicroProfile 4.1

## Conventions
- **Package structure**: `no.epost.<module>.<layer>` (rest, service, dao, model, dto)
- **REST**: JAX-RS `@Path` classes, return `Response` objects
- **Services**: CDI `@ApplicationScoped` beans or `@Stateless` EJBs
- **DAOs**: JPA EntityManager via `@PersistenceContext`
- **DTOs**: Separate from entities, manual mapping or MapStruct
- **Validation**: Bean Validation (`@NotNull`, `@Size`, etc.)
- **Error handling**: Exception mappers (`@Provider` + `ExceptionMapper<T>`)

## Build Commands
```bash
mvn clean package            # Build WAR
mvn test                     # Unit tests
mvn verify -Parquillian      # Integration tests
```

## Sub-Skill Routing

When this skill is active and user intent matches a sub-skill, delegate:

| Intent | Sub-Skill | When |
|--------|-----------|------|
| Database work | `backend-databases` | PostgreSQL, MongoDB, persistence |

## Aspects

| Aspect | File | Purpose |
|--------|------|---------|
| REST | references/rest-patterns.md | JAX-RS endpoint patterns |
| Services | references/service-patterns.md | CDI/EJB service layer |
| Persistence | references/persistence-patterns.md | JPA/Hibernate + MongoDB |
| Testing | references/testing-patterns.md | JUnit 4, Mockito, Arquillian |
