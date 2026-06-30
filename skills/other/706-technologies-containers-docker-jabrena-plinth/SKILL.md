---
name: 706-technologies-containers-docker
description: Use when you need framework-agnostic Docker and container image guidance for Java projects - Dockerfile design, multi-stage Maven builds, jlink custom runtimes, micro runtime distributions such as Alpaquita, JVM container ergonomics, non-root execution, image metadata, .dockerignore, reproducible builds, vulnerability scanning, SBOM awareness, and production-safe container defaults. This should trigger for requests such as Review Java Dockerfile; Improve Docker image security; Add jlink runtime to a Java container; Add containerization to a Java project; Optimize Java container image size; Review Docker build reproducibility. Part of cursor-rules-java project
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.16.0
---
# Java container image best practices with Docker

Help teams build secure, reproducible, and maintainable **Docker container images** for Java applications without coupling the guidance to Spring Boot, Quarkus, or Micronaut.

**What is covered in this Skill?**

- Dockerfile structure for Java applications: multi-stage builds, Maven dependency caching, deterministic artifact copies, `jlink` custom runtimes, and `.dockerignore`
- Runtime image selection: micro distributions such as Alpaquita, minimal JRE images, pinned versions or digests where appropriate, image labels, and explicit entrypoints
- JVM container ergonomics: memory percentage flags, startup behavior, graceful shutdown signals, time zones, and predictable runtime options
- Security defaults: non-root users, least privilege, no secrets in layers, reduced package managers, vulnerability scanning, SBOM awareness, and avoiding privileged containers
- Operational readiness: health checks when suitable, stdout/stderr logging, port declaration, image size control, build reproducibility, and CI verification

**Scope:** Framework-agnostic Docker and container-image quality for Java projects. For framework runtime wiring, defer to the matching Spring Boot, Quarkus, or Micronaut skill. For Testcontainers-based tests, defer to the relevant testing skill.

## Constraints

Keep recommendations at the Dockerfile, image-build, and runtime-container layer unless the user explicitly asks for framework-specific configuration. After editing this repository's XML sources, regenerate skills and verify the build.

- **MANDATORY**: Run `./mvnw compile` or `mvn compile` before proposing Java or Maven changes in the same change set
- **SECRETS**: Never bake credentials, tokens, private keys, Maven settings with secrets, or environment-specific secrets into image layers, labels, arguments, or logs
- **SECURITY**: Prefer non-root execution, least-privilege filesystem permissions, micro runtime images, and explicit container capabilities over privileged defaults
- **JLINK**: Prefer `jlink` custom runtimes for production images when the module graph is known, validated at runtime, and compatible with the application's dependencies
- **REPRODUCIBILITY**: Pin base image versions intentionally, document digest trade-offs, keep build inputs explicit, and avoid network-dependent runtime startup steps
- **JVM**: Account for container memory and CPU limits with JVM flags, graceful shutdown behavior, and observable startup failures before claiming production readiness
- **BOUNDARIES**: Defer Spring Boot runtime behavior to `@301-frameworks-spring-boot-core`, Quarkus runtime behavior to `@401-frameworks-quarkus-core`, Micronaut runtime behavior to `@501-frameworks-micronaut-core`, and Testcontainers setup to the matching testing skill
- **MANDATORY**: Regenerate skills with `./mvnw clean install -pl skills-generator` after editing skill or system-prompt XML in this repo
- **VERIFY**: Run `./mvnw clean verify` or `mvn clean verify` before promoting changes
- **EDGE CASE**: If the target Java version, build tool, deployment platform, base-image policy, registry policy, or security scanner is missing and affects the recommendation, ask a clarifying question before editing container artifacts
- **EDGE CASE**: If requested changes conflict with security policy, image provenance, air-gapped builds, or runtime platform constraints, explain the trade-off and ask for confirmation

## When to use this skill

- Review Java Dockerfile
- Improve Docker image security
- Add jlink runtime to a Java container
- Add containerization to a Java project
- Optimize Java container image size
- Review Docker build reproducibility

## Workflow

1. **Read reference and assess container context**

Read `references/706-technologies-containers-docker.md` and inspect current Dockerfiles, `.dockerignore`, Maven build inputs, image build scripts, CI jobs, registry policy, and deployment constraints before proposing changes.

2. **Identify runtime and supply-chain constraints**

Confirm Java version, build tool, `jlink` module requirements, micro distro compatibility, target platform, base-image policy, registry requirements, vulnerability scanner, SBOM expectations, memory limits, exposed ports, and operational readiness needs.

3. **Apply container-aligned changes**

Implement or refactor Docker and container build artifacts following the reference patterns and project conventions, keeping framework-specific runtime behavior out of scope unless explicitly requested.

4. **Run verification and report results**

Execute appropriate build, image build, scan, smoke-test, and generator checks; summarize what changed, what was verified, and any remaining container risks.

## Reference

For detailed guidance, examples, and constraints, see [references/706-technologies-containers-docker.md](references/706-technologies-containers-docker.md).
