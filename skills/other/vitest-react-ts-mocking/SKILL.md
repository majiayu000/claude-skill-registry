---
name: vitest-react-ts-mocking
description: Implement mocking in Vitest for React-TS (modules, timers, fetch) and write tests that still achieve 100% coverage. Includes best-practice patterns to avoid brittle mocks.
argument-hint: "[what to mock: module|fetch|timers] [path] [behavior]"
allowed-tools: Read, Write, Grep, Glob
---

# Vitest Mocking (React-TS) + 100% coverage

You are adding mocks in Vitest while keeping tests robust and achieving 100% coverage.

## Non-negotiables

1) Tests remain deterministic and cover 100% of the code under test.
2) Prefer mocking at the boundary:
   - module boundary via vi.mock
   - network boundary by stubbing fetch (or the project’s API client)
3) Reset/restore mocks appropriately (clearMocks/mockReset/restoreMocks are enabled in config).

Use template.md as the default structure.
