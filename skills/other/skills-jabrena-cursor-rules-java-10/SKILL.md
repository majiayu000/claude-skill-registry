---
name: 132-java-testing-integration-testing
description: Use when you need to set up, review, or improve Java integration tests — including generating a BaseIntegrationTest.java with WireMock for HTTP stubs, detecting HTTP client infrastructure from import signals, injecting service coordinates dynamically via System.setProperty(), creating WireMock JSON mapping files with bodyFileName, isolating stubs per test method, verifying HTTP interactions, or eliminating anti-patterns such as Mockito-mocked HTTP clients or globally registered WireMock stubs.
metadata:
  author: Juan Antonio Breña Moral
  version: 0.12.0-SNAPSHOT
---
# Java Integration testing guidelines

Set up robust integration-test infrastructure for Java services using WireMock to stub outbound HTTP dependencies.

**Core areas:** Infrastructure topology detection (scanning imports for `HttpClient`, `feign.*`, `retrofit2.*`, `RestTemplate`, etc.), abstract `BaseIntegrationTest` base class, `WireMockExtension` with `@RegisterExtension`, dynamic port allocation (`dynamicPort()`), `usingFilesUnderClasspath("wiremock")`, `@BeforeAll` + `System.setProperty()` for coordinate propagation, concrete test classes extending the base class, WireMock JSON mapping files (`bodyFileName` referencing `wiremock/files/`), programmatic stub registration via WireMock DSL, per-test stub isolation (register stubs inside each test method), fault injection (503 service unavailable, network latency with `withFixedDelay`), request verification (`WIREMOCK.verify`), `wiremock-standalone` Maven dependency (test scope), and anti-patterns (global `@BeforeAll` stubs causing order-dependent failures, Mockito-mocked HTTP clients bypassing the real HTTP pipeline, hardcoded ports or URLs in property files).

**Prerequisites:** Run `./mvnw compile` or `mvn compile` before applying any change. If compilation fails, **stop immediately** and do not proceed — compilation failure is a blocking condition.

**Multi-step scope:** Step 1 scans class imports for HTTP client signals and confirms the integration topology with the user (REST → WireMock). Step 2 generates a tailored `BaseIntegrationTest.java` under `src/test/java/{root-package}/` with `WireMockExtension` and `@BeforeAll` coordinate propagation, then lists required Maven dependencies. Step 3 generates starter WireMock JSON mapping files (one per confirmed external service) under `src/test/resources/wiremock/mappings/{service-name}/`.

**Before applying changes:** Read the reference for detailed examples, good/bad patterns, and constraints.

## Reference

For detailed guidance, examples, and constraints, see [references/132-java-integration-testing.md](references/132-java-integration-testing.md).
