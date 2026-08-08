---
name: qa-testing-nunit
description: Design and refactor C# test suites with NUnit for API, component, and integration scenarios. Use when creating or fixing NUnit fixtures, structuring test projects, setting up WireMock and Testcontainers dependencies, and reducing flaky behavior in CI or local runs. For general backend service implementation use $software-csharp-backend, for pipeline target changes use $ops-nuke-cicd, and for logging-migration rewrites use $dev-structured-logs.
---

# C# Testing NUnit Fixtures

## Quick Reference
- Classify test scope first: API, component, or integration.
- Lock runtime constraints before execution: Docker availability, framework target, and explicitly excluded suites.
- Use this skill for test-suite architecture and fixture behavior, not for general service implementation or CI graph refactors.
- Default to two files per handler/use case: `<Feature>Fixture.cs` and `<Feature>Tests.cs`.
- For full-cycle API tests, use controller-focused structure: one fixture per controller/test family and one base `ApiTest.cs` + `ApiFixture.cs` (split by scenario family only when needed).
- Do not translate SpecFlow/Taffy step definitions into C# line-by-line; rewrite scenario intent into idiomatic API tests.
- For API migrations, avoid one global shared setup fixture; each controller/test family fixture owns its own dependencies.
- Fixture ownership for API tests should include DB launcher + migrators + WireMock + WebApplicationFactory + client.
- Reset mutable state in `[SetUp]`; dispose all owned infra in `[OneTimeTearDown]`.
- For DB bootstrapping, follow pricing-style `DatabaseLauncher + MigratorContainer` from `tests/utils/Sc.Fin.Pricing.Tests.Utils/Testcontainers`.
- Use canonical migrator command `dotnet Sc.Tool.FluentMigrator.dll migrateup -m /sql` and avoid custom ready-check arguments in tests.
- Keep migrator ordering explicit (dependency migrators first, domain migrator last) and support fixture-level optional migrator toggles when some suites do not need all DBs.
- Add explicit migrator verification tests that assert launcher startup, migrator completion/order, and required tables.
- Use iterative quality loop: `code -> build -> run tests -> fix -> repeat`.
- For health endpoints, use `[Test] + [TestCase] + [CancelAfter(...)]` with method signature `(string url, CancellationToken cancellationToken)`; keep `[Test]` together with `[TestCase]` to avoid NUnit analyzer issues.
- If user excludes infra-dependent suites (for example component tests requiring Docker), run feasible categories first and report exactly what remains unvalidated.
- If the task shifts into service design or backend refactoring, switch to `$software-csharp-backend`.
- If the task shifts into `nuke/Build.cs`, category target wiring, or CI artifact publication, switch to `$ops-nuke-cicd`.

## Workflow
1. Define boundary, dependencies, expected assertion depth, and environment constraints.
Load `references/nunit-structure.md`.
2. Select fixture composition and lifecycle.
Load `references/fixture-pattern.md` and `references/testing-templates.md`.
3. Implement scenario tests for the target layer.
Load `references/api-testing-nunit.md` or `references/component-testing-nunit.md`.
4. Choose double vs real dependency strategy.
Load `references/dependency-strategy-matrix.md`, then `references/wiremock-setup.md` or `references/testcontainers-setup.md`.
5. Add resilient async and eventual-consistency assertions.
Load `references/async-eventual-assertions.md`.
6. Harden suite against flaky behavior.
Load `references/anti-flakiness.md`.
7. Tune execution in CI.
Load `references/ci-parallelism-sharding.md` and `references/infrastructure-troubleshooting.md`.
8. Validate changed suites through build-test feedback targets.
For NUKE-based repositories, run `BuildAll`, `LocalUnitTest`, `ApiTest`/`DbTest` as needed, then `TestAll`; use `$ops-nuke-cicd` for pipeline-target changes.
9. If this is a migration from SpecFlow-style assets, produce migration trace artifacts.
Use `$docs-codebase` with migration matrix and feature trace templates.

## Resources
- [NUnit Structure](references/nunit-structure.md): project layout, naming, categories, and lifecycle conventions.
- [Fixture Pattern](references/fixture-pattern.md): fixture boundaries, shared setup, teardown, and composition.
- [Testing Templates](references/testing-templates.md): copy-ready fixture/Testcontainers/WireMock templates.
- [API Testing with NUnit](references/api-testing-nunit.md): endpoint-level tests with HTTP assertions and contract checks.
- [Component Testing with NUnit](references/component-testing-nunit.md): in-process integration tests across collaborating components.
- [Dependency Strategy Matrix](references/dependency-strategy-matrix.md): decide WireMock vs Testcontainers by scenario.
- [WireMock Setup](references/wiremock-setup.md): deterministic stubs, request verification, and failure simulation.
- [Testcontainers Setup](references/testcontainers-setup.md): container lifecycle, readiness, and test isolation.
- [Async Eventual Assertions](references/async-eventual-assertions.md): polling, timeouts, and message-driven verification.
- [Anti-Flakiness](references/anti-flakiness.md): reliability rules for stable execution.
- [CI Parallelism and Sharding](references/ci-parallelism-sharding.md): split test execution safely and efficiently.
- [Infrastructure Troubleshooting](references/infrastructure-troubleshooting.md): diagnose startup failures, port collisions, and readiness issues.
- [Skill Data](Data/data.json): curated Microsoft and .NET testing references for this skill.

## Templates
- [NUnit Handler Fixture Template](assets/nunit-handler-fixture-template.cs): base fixture for setup wiring and deterministic scenario configuration.
- [NUnit Handler Tests Template](assets/nunit-handler-tests-template.cs): base test class using fixture with Arrange/Act/Assert flow.
- [NUnit API Fixture Template](assets/nunit-api-fixture-template.cs): API fixture for controller-focused API-to-database full-cycle tests.
- [NUnit API Tests Template](assets/nunit-api-tests-template.cs): base API test class with fixture isolation and parallel-safe lifecycle.
- [NUnit API Request Builder Template](assets/nunit-api-request-builder-template.cs): deterministic request builder for scenario setup.
- [NUnit API TestCaseSources Template](assets/nunit-api-test-case-sources-template.cs): reusable `TestCaseData` source methods.
- [NUnit WireMock Template](assets/nunit-wiremock-template.cs): pricing-style `WireMockServerWrapper` and per-dependency `*WiremockServer` helper pattern.
- [NUnit Database Launcher Template](assets/nunit-database-launcher-template.cs): pricing-style `DatabaseLauncher`, ordered migrator chain, optional migrator toggles, and startup verification hooks.
