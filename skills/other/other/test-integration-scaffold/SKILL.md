---
name: test__integration_scaffold
description: Create integration tests for API endpoints with SSE event verification and TUnit patterns. Use this when you need to test a new endpoint.
---

Follow this guide to create **integration tests** for API endpoints in `tests/BookStore.AppHost.Tests`.

1. **Create Test Class**
   - Create file in `tests/BookStore.AppHost.Tests/`
   - **Naming**: `{Feature}Tests.cs` (e.g., `AuthorCrudTests.cs`)
   - **Template**:
     ```csharp
     using BookStore.AppHost.Tests.Helpers;
     using BookStore.Client;
     using BookStore.Shared.Models;
     using Refit;
     using System.Net;

     namespace BookStore.AppHost.Tests;

     public class AuthorCrudTests
     {
         // Test methods here
     }
     ```

2. **Write Create Test (with SSE)**
   - Test endpoint that creates a resource
   - **Use Resource Helpers** for SSE event verification and creation
   - **Example**:
     ```csharp
     [Test]
     public async Task CreateAuthor_EndToEndFlow_ShouldReturnOk()
     {
         // Arrange
         var client = await HttpClientHelpers.GetAuthenticatedClientAsync<IAuthorsClient>();
         var createRequest = FakeDataGenerators.GenerateFakeAuthorRequest();

         // Act - Helper handles:
         // 1. Making the HTTP request
         // 2. Waiting for SSE notification
         // 3. Fetching and returning the created resource
         var author = await AuthorHelpers.CreateAuthorAsync(client, createRequest);

         // Assert
         await Assert.That(author).IsNotNull();
         await Assert.That(author!.Id).IsNotEqualTo(Guid.Empty);
     }
     ```

3. **Write Update Test**
   - Test endpoint that updates a resource
   - **Pattern**: Create → Update → Verify
     ```csharp
     [Test]
     public async Task UpdateAuthor_ShouldReturnOk()
     {
         // Arrange
         var client = await HttpClientHelpers.GetAuthenticatedClientAsync<IAuthorsClient>();
         var createRequest = FakeDataGenerators.GenerateFakeAuthorRequest();

         // Create author first
         var author = await AuthorHelpers.CreateAuthorAsync(client, createRequest);

         var updateRequest = FakeDataGenerators.GenerateFakeUpdateAuthorRequest();

         // Act - Helper handles ETag retrieval and SSE wait
         author = await AuthorHelpers.UpdateAuthorAsync(client, author!, updateRequest);

         // Assert - Verify update by fetching
         var updatedAuthor = await client.GetAuthorAsync(author!.Id);
         await Assert.That(updatedAuthor.Name).IsEqualTo(updateRequest.Name);
     }
     ```

4. **Write Delete Test (Soft Delete)**
   - Test soft deletion with restore capability
     ```csharp
     [Test]
     public async Task DeleteAuthor_ShouldReturnNoContent()
     {
         // Arrange
         var client = await HttpClientHelpers.GetAuthenticatedClientAsync<IAuthorsClient>();
         var createRequest = FakeDataGenerators.GenerateFakeAuthorRequest();
         var author = await AuthorHelpers.CreateAuthorAsync(client, createRequest);

         // Act - Delete
         author = await AuthorHelpers.DeleteAuthorAsync(client, author!);

         // Verify - Should return 404 from public API
         var publicClient = HttpClientHelpers.GetUnauthenticatedClient<IAuthorsClient>();
         try
         {
             await publicClient.GetAuthorAsync(author!.Id);
             Assert.Fail("Author should have been deleted");
         }
         catch (ApiException ex)
         {
             await Assert.That(ex.StatusCode).IsEqualTo(HttpStatusCode.NotFound);
         }
     }
     ```

5. **Write Query Tests**
   - Test GET endpoints without SSE
     ```csharp
     [Test]
     public async Task GetAuthors_ReturnsPagedList()
     {
         // Arrange
         var client = HttpClientHelpers.GetUnauthenticatedClient<IAuthorsClient>();

         // Act
         var response = await client.GetAuthorsAsync(page: 1, pageSize: 20);

         // Assert
         await Assert.That(response).IsNotNull();
         await Assert.That(response!.Items).IsNotNull();
         await Assert.That(response.TotalCount).IsGreaterThanOrEqualTo(0);
     }

     [Test]
     public async Task GetAuthorById_ExistingId_ReturnsAuthor()
     {
         // Arrange - Create an author first
         var adminClient = await HttpClientHelpers.GetAuthenticatedClientAsync<IAuthorsClient>();
         var createRequest = FakeDataGenerators.GenerateFakeAuthorRequest();
         var created = await AuthorHelpers.CreateAuthorAsync(adminClient, createRequest);

         // Act - Get by ID (public endpoint)
         var publicClient = HttpClientHelpers.GetUnauthenticatedClient<IAuthorsClient>();
         var author = await publicClient.GetAuthorAsync(created!.Id);

         // Assert
         await Assert.That(author).IsNotNull();
         await Assert.That(author!.Id).IsEqualTo(created.Id);
         await Assert.That(author.Name).IsEqualTo(createRequest.Name);
     }
     ```

6. **Add Custom Test Helper (if needed)**
   - For resource-specific operations, create separate helper files:
   - **AuthorHelpers.cs** (example):
     ```csharp
     using BookStore.Client;
     using BookStore.Shared.Models;

     namespace BookStore.AppHost.Tests.Helpers;

     public static class AuthorHelpers
     {
         public static async Task<AuthorDto> CreateAuthorAsync(
             IAuthorsClient client,
             CreateAuthorRequest createRequest)
         {
             var received = await SseEventHelpers.ExecuteAndWaitForEventAsync(
                 createRequest.Id,
                 ["AuthorCreated", "AuthorUpdated"],
                 async () =>
                 {
                     var response = await client.CreateAuthorWithResponseAsync(createRequest);
                     if (response.Error != null)
                         throw response.Error;
                 },
                 TestConstants.DefaultEventTimeout);

             if (!received)
                 throw new Exception("Failed to receive AuthorCreated event.");

             return await client.GetAuthorAsync(createRequest.Id);
         }

         public static async Task<AuthorDto> UpdateAuthorAsync(
             IAuthorsClient client,
             AuthorDto author,
             UpdateAuthorRequest updateRequest)
         {
             var version = ETagHelper.ParseETag(author.ETag) ?? 0;
             var received = await SseEventHelpers.ExecuteAndWaitForEventWithVersionAsync(
                 author.Id,
                 "AuthorUpdated",
                 async () => await client.UpdateAuthorAsync(author.Id, updateRequest, author.ETag),
                 TestConstants.DefaultEventTimeout,
                 minVersion: version + 1,
                 minTimestamp: DateTimeOffset.UtcNow);

             if (!received.Success)
                 throw new Exception("Failed to receive AuthorUpdated event.");

             return await client.GetAuthorAsync(author.Id);
         }

         public static async Task<AuthorDto> DeleteAuthorAsync(
             IAuthorsClient client,
             AuthorDto author)
         {
             var received = await SseEventHelpers.ExecuteAndWaitForEventAsync(
                 author.Id,
                 "AuthorDeleted",
                 async () =>
                 {
                     var etag = author.ETag;
                     if (string.IsNullOrEmpty(etag))
                     {
                         var latest = await client.GetAuthorAdminAsync(author.Id);
                         etag = latest?.ETag;
                     }
                     await client.SoftDeleteAuthorAsync(author.Id, etag);
                 },
                 TestConstants.DefaultEventTimeout);

             if (!received)
                 throw new Exception("Failed to receive AuthorDeleted event.");

             return await client.GetAuthorAsync(author.Id);
         }
     }
     ```
   - **FakeDataGenerators.cs** (add fake data generators):
     ```csharp
     using Bogus;
     using BookStore.Client;
     using BookStore.Shared.Models;

     namespace BookStore.AppHost.Tests.Helpers;

     public static class FakeDataGenerators
     {
         static readonly Faker _faker = new();

         public static CreateAuthorRequest GenerateFakeAuthorRequest() => new()
         {
             Id = Guid.CreateVersion7(),
             Name = _faker.Name.FullName(),
             Translations = new Dictionary<string, AuthorTranslationDto>
             {
                 ["en"] = new(_faker.Lorem.Paragraphs(2)),
                 ["es"] = new(_faker.Lorem.Paragraphs(2))
             }
         };

         public static UpdateAuthorRequest GenerateFakeUpdateAuthorRequest() => new()
         {
             Name = _faker.Name.FullName(),
             Translations = new Dictionary<string, AuthorTranslationDto>
             {
                 ["en"] = new(_faker.Lorem.Paragraphs(2)),
                 ["es"] = new(_faker.Lorem.Paragraphs(2))
             }
         };
     }
     ```

7. **Test Error Cases**
   - Test validation failures and edge cases
     ```csharp
     [Test]
     [Arguments("")]
     [Arguments(null)]
     public async Task CreateAuthor_WithInvalidName_ShouldReturnBadRequest(string? invalidName)
     {
         // Arrange
         var client = await HttpClientHelpers.GetAuthenticatedClientAsync<IAuthorsClient>();
         var request = new CreateAuthorRequest
         {
             Id = Guid.CreateVersion7(),
             Name = invalidName,
             Translations = new Dictionary<string, AuthorTranslationDto> { ["en"] = new("Biography") }
         };

         // Act & Assert - Refit throws ApiException on error
         try
         {
             await client.CreateAuthorAsync(request);
             Assert.Fail("Expected ApiException was not thrown");
         }
         catch (ApiException ex)
         {
             await Assert.That(ex.StatusCode).IsEqualTo(HttpStatusCode.BadRequest);
         }
     }

     [Test]
     public async Task DeleteAuthor_Unauthenticated_ReturnsUnauthorized()
     {
         // Arrange
         var client = HttpClientHelpers.GetUnauthenticatedClient<IAuthorsClient>();
         var authorId = Guid.CreateVersion7();

         // Act & Assert
         try
         {
             await client.SoftDeleteAuthorAsync(authorId);
             Assert.Fail("Expected ApiException was not thrown");
         }
         catch (ApiException ex)
         {
             await Assert.That(ex.StatusCode).IsEqualTo(HttpStatusCode.Unauthorized);
         }
     }

     // Validation with error codes (ProblemDetails pattern)
     [Test]
     [Arguments("", ErrorCodes.Books.TitleRequired)]
     [Arguments(null, ErrorCodes.Books.TitleRequired)]
     public async Task CreateBook_WithInvalidTitle_ReturnsExpectedErrorCode(
         string? title,
         string expectedErrorCode)
     {
         // Arrange
         var client = await HttpClientHelpers.GetAuthenticatedClientAsync<IBooksClient>();
         var request = FakeDataGenerators.GenerateFakeBookRequest();
         request.Title = title;

         // Act & Assert
         try
         {
             await client.CreateBookAsync(request);
             Assert.Fail("Expected ApiException was not thrown");
         }
         catch (ApiException ex)
         {
             await Assert.That(ex.StatusCode).IsEqualTo(HttpStatusCode.BadRequest);
             await Assert.That(ex.Content).Contains(expectedErrorCode);
         }
     }
     ```

## Key Testing Patterns

### Use Authenticated Refit Client for Admin Endpoints
```csharp
var client = await HttpClientHelpers.GetAuthenticatedClientAsync<IAuthorsClient>();
```

### Use Unauthenticated Refit Client for Public Endpoints
```csharp
var client = HttpClientHelpers.GetUnauthenticatedClient<IAuthorsClient>();
```

### Multi-Tenancy Testing
```csharp
// Use specific tenant
var httpClient = HttpClientHelpers.GetUnauthenticatedClient("tenant-id");
var client = RestService.For<IAuthorsClient>(httpClient);

// Or for authenticated requests
var httpClient = await HttpClientHelpers.GetTenantClientAsync("tenant-id", accessToken);
var client = RestService.For<IAuthorsClient>(httpClient);
```

### Wait for SSE Events After Mutations
```csharp
// Simple event wait
var received = await SseEventHelpers.ExecuteAndWaitForEventAsync(
    entityId,
    "EventName",
    async () => /* HTTP call */,
    TestConstants.DefaultEventTimeout
);

// Wait for multiple event types
var received = await SseEventHelpers.ExecuteAndWaitForEventAsync(
    entityId,
    ["EventName1", "EventName2"],
    async () => /* HTTP call */,
    TestConstants.DefaultEventTimeout
);

// Wait with version check (for updates)
var result = await SseEventHelpers.ExecuteAndWaitForEventWithVersionAsync(
    entityId,
    "EventName",
    async () => /* HTTP call */,
    TestConstants.DefaultEventTimeout,
    minVersion: currentVersion + 1,
    minTimestamp: DateTimeOffset.UtcNow
);
```

### Use FakeDataGenerators for Test Data
```csharp
var createRequest = FakeDataGenerators.GenerateFakeAuthorRequest();
var updateRequest = FakeDataGenerators.GenerateFakeUpdateAuthorRequest();
var email = FakeDataGenerators.GenerateFakeEmail();
var password = FakeDataGenerators.GenerateFakePassword();
```

### Use TestConstants for Timeouts
```csharp
TestConstants.DefaultTimeout           // 30 seconds
TestConstants.DefaultEventTimeout      // 30 seconds
TestConstants.DefaultProjectionDelay   // 500 ms
TestConstants.DefaultRetryDelay        // 100 ms
TestConstants.DefaultPollingInterval   // 50 ms
TestConstants.DefaultStreamTimeout     // 5 minutes
TestConstants.DefaultMaxRetries        // 10
```

### Handle ETags for Concurrency
```csharp
// Get resource with ETag
var response = await client.GetAuthorWithResponseAsync(authorId);
var etag = response.Headers.ETag?.Tag;

// Use ETag in update/delete
await client.UpdateAuthorAsync(authorId, updateRequest, etag);
await client.SoftDeleteAuthorAsync(authorId, etag);

// Parse ETag for version comparison
var version = ETagHelper.ParseETag(author.ETag) ?? 0;
```

## TUnit Assertion Patterns

```csharp
// Equality
await Assert.That(actual).IsEqualTo(expected);

// Null checks
await Assert.That(value).IsNotNull();
await Assert.That(value).IsNull();

// Boolean
await Assert.That(condition).IsTrue();
await Assert.That(condition).IsFalse();

// Collections
await Assert.That(collection).Contains(item);
await Assert.That(collection).DoesNotContain(item);

// Numeric comparisons
await Assert.That(count).IsGreaterThan(0);
await Assert.That(count).IsGreaterThanOrEqualTo(0);

// Refit Exception handling (use try/catch with Assert.Fail)
try
{
    await client.SomeMethodAsync();
    Assert.Fail("Expected ApiException was not thrown");
}
catch (ApiException ex)
{
    await Assert.That(ex.StatusCode).IsEqualTo(HttpStatusCode.BadRequest);
}
```

## Running Tests

Once tests are created, use the dedicated test runner skills:

- **`/test__integration_suite`** - Execute all integration tests with Aspire
- **`/test__unit_suite`** - Execute unit tests for API and analyzers
- **`/test__verify_feature`** - Complete verification (build + format + all tests)

For specific test filtering or manual commands, see:
- [run-integration-tests](../test__integration_suite/SKILL.md) - Integration test details
- [run-unit-tests](../test__unit_suite/SKILL.md) - Unit test details

### Quick Reference

```bash
# All integration tests
/test__integration_suite

# Specific test class
dotnet test --filter "FullyQualifiedName~AuthorCrudTests"

# Complete verification
/test__verify_feature
```

## Troubleshooting

**Test Hangs on SSE Wait**
- Check event name matches exactly (case-sensitive)
- Verify `MartenCommitListener` sends the notification
- Increase timeout if needed using `TestConstants`
- Check that the entity ID matches (use `Guid.Empty` to match any entity)

**Port Already in Use**
- Stop any running Aspire instances
- Check for orphaned `dotnet` processes
- Use `pkill -f dotnet` on macOS/Linux to clean up

**"Zero tests ran"**
- Ensure test class is public
- Ensure methods are decorated with `[Test]`
- Check `GlobalHooks` setup completed successfully
- Verify test assembly references TUnit

**Refit Exceptions Not Caught**
- Use try/catch blocks with `ApiException` for error testing
- Call `Assert.Fail()` if no exception was thrown
- Check status code on caught exception

**ETag Missing or Null**
- Use `*WithResponseAsync()` variants to access response headers
- Access ETag via `response.Headers.ETag?.Tag`
- Use `ETagHelper.ParseETag()` to get version number

## Related Skills

**Prerequisites**:
- Feature must be implemented first - see scaffolding skills:
    - `/wolverine__create_operation` - Backend create mutations
    - `/wolverine__update_operation` - Backend update mutations
    - `/marten__get_by_id` - Backend single-resource queries
    - `/marten__list_query` - Backend list queries
    - `/frontend__feature_scaffold` - UI components

**Next Steps**:
- `/test__integration_suite` - Execute the tests you created
- `/test__verify_feature` - Complete verification workflow
- Check coverage and add edge cases for boundary conditions

**See Also**:
- [verify-feature](../test__verify_feature/SKILL.md) - Definition of Done verification
- [run-integration-tests](../test__integration_suite/SKILL.md) - Integration test execution
- [run-unit-tests](../test__unit_suite/SKILL.md) - Unit test execution
- [integration-testing-guide](../../../docs/guides/integration-testing-guide.md) - Aspire integration testing
- [testing-guide](../../../docs/guides/testing-guide.md) - TUnit unit testing
- AppHost.Tests AGENTS.md - Test project patterns
