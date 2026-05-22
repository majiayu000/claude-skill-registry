---
name: qa-engineer-integration
description: Write integration tests for CLI commands with Vitest
---

# QA Engineer for Integration Testing

## Responsibilities

- This skill ensures integration tests cover CLI behavior changes first.
- Tests remain readable, deterministic, and aligned with how users run commands.
- End-to-end side effects are emphasized: filesystem, API calls, logging, and reports.

## When to use

Integration tests are mandatory for every new feature or behavior change. Write these tests before the implementation. Use this skill whenever a change affects CLI command behavior, API interactions, filesystem reads and writes, logging, or reporting.

## Best practices

- Use `preconditions` helpers to set up MSW handlers, memfs state, and stubbed dependencies.
- Require MSW handlers to be registered inside preconditions so API behavior is explicit per test.
- Drive the CLI via `command.parseAsync([...args])` and assert side effects and outputs.
- Validate behavior through action spies, manifest files, reports, logs, and console output.
- Test titles must always start with `should`.

## Patterns to follow

- **Preconditions:** Group setup helpers in a `preconditions` object (e.g., `canLoadFiles`, `canLoadManifest`, `canCreateRemoteResources`, `failsToUpdateRemoteResources`). Each helper should be focused, deterministic, and reusable across tests.
- **MSW in preconditions:** Define MSW handlers inside those precondition helpers (e.g., `preconditions.canCreateRemoteResources` registers `http.post` and returns created items). This keeps request and response behavior close to the test intent.
- **Filesystem state:** Use `memfs` and `vol.fromJSON` to create local files and `vol.reset` in `afterEach` to clear state. When you need path resolution, use `resolveCommandPath` with the command constants.
- **Command execution:** Import the command module, register the CLI `index`, then run `command.parseAsync(['node', 'test', ...args])`.
- **Assertions:** Verify action calls with `expect(actions.method).toHaveBeenCalledWith(...)`, then check generated manifest entries, reports, log output, and console messages.

Example shape (simplified):

```ts
const server = setupServer();

const preconditions = {
  canLoadFiles(items: Item[]) {
    const dir = resolveCommandPath(directories.items, DEFAULT_SPACE);
    vol.fromJSON(Object.fromEntries(items.map(item => [path.join(dir, `${item.slug}.json`), JSON.stringify(item)])));
  },
  canCreateRemoteItems(items: Item[]) {
    const created = items.map(item => ({ ...item, id: getID() }));
    server.use(
      http.post(`https://mapi.storyblok.com/v1/spaces/${DEFAULT_SPACE}/items`, async ({ request }) => {
        const body = await request.json();
        const match = created.find(i => i.slug === body.item.slug);
        return HttpResponse.json({ item: match });
      }),
    );
    return created;
  },
};

describe('command push', () => {
  beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
  afterEach(() => {
    vi.resetAllMocks();
    vi.clearAllMocks();
    vol.reset();
    server.resetHandlers();
    resetReporter();
  });
  afterAll(() => server.close());

  it('should push items and write manifest/report', async () => {
    preconditions.canLoadFiles([makeMockItem()]);
    preconditions.canCreateRemoteItems([makeMockItem()]);

    await command.parseAsync(['node', 'test', 'push', '--space', DEFAULT_SPACE]);

    expect(actions.createItem).toHaveBeenCalled();
    expect(await parseManifest()).toEqual([expect.objectContaining({ old_id: expect.anything() })]);
    expect(getReport()).toEqual(expect.objectContaining({ status: 'SUCCESS' }));
  });
});
```
