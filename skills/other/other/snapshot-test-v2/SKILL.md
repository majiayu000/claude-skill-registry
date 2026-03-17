---
name: snapshot-test-v2
description: Generate snapshot tests with Verify (.NET) or Jest snapshots
argument-hint: "<target> [--framework=verify|jest]"
tags: [testing, snapshot, verify, regression]
user-invocable: true
---

# Snapshot Testing

Generate snapshot tests for API responses and component rendering.

## For .NET (Verify)
```bash
dotnet add package Verify.Xunit
```
```csharp
[Fact]
public Task GetCandidate_ReturnsExpectedShape()
{
    var result = service.GetById("test-id");
    return Verify(result);
}
```

## For React (Jest)
```typescript
test('CandidateCard renders correctly', () => {
  const { container } = render(<CandidateCard candidate={mockCandidate} />);
  expect(container).toMatchSnapshot();
});
```

## Arguments
- `<target>`: Class or component to snapshot
- `--framework=<verify|jest>`: Testing framework