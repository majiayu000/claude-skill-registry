---
name: db-test
description: Generate database integration tests with Testcontainers
argument-hint: "<repository-name> [--provider=cosmosdb|postgres]"
tags: [testing, database, testcontainers, integration]
user-invocable: true
---

# Database Integration Tests

Generate integration tests using Testcontainers for real database validation.

## For .NET (Testcontainers)
```bash
dotnet add package Testcontainers.CosmosDb
```
```csharp
public class CandidateRepositoryTests : IAsyncLifetime
{
    private readonly CosmosDbContainer _container = new CosmosDbBuilder().Build();

    public async Task InitializeAsync() => await _container.StartAsync();
    public async Task DisposeAsync() => await _container.DisposeAsync();

    [Fact]
    public async Task Create_ValidCandidate_Persists()
    {
        var client = new CosmosClient(_container.GetConnectionString());
        var repo = new CandidateRepository(client, Options.Create(settings));
        var candidate = CreateTestCandidate();
        await repo.CreateAsync(candidate);
        var result = await repo.GetByIdAsync(candidate.Id);
        result.Should().BeEquivalentTo(candidate);
    }
}
```

## Arguments
- `<repository-name>`: Repository class to test
- `--provider=<cosmosdb|postgres|mongodb>`: Database provider