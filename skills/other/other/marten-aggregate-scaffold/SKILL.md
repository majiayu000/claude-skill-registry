---
name: marten__aggregate_scaffold
description: Create a new event-sourced aggregate with proper Apply methods, event handling, and Marten configuration. Use this when adding a new domain entity that needs event sourcing.
---

Follow this guide to create a new **event-sourced aggregate** in the ApiService following strict Event Sourcing patterns.

1. **Define the Initial Event**
   - Create a `record` in `src/BookStore.ApiService/Events/`
   - **Naming**: Past tense (e.g., `AuthorCreated`, not `CreateAuthor`)
   - **Properties**: Include all initial state properties
   - **IDs**: Use `Guid` for aggregate ID
   - **Timestamp**: Use `DateTimeOffset`
   - **Example**:
     ```csharp
     namespace BookStore.ApiService.Events;

     public record AuthorCreated(
         Guid Id,
         string Name,
         string Biography,
         DateTimeOffset CreatedAt
     );
     ```

2. **Create the Aggregate**
   - Create a `record` in `src/BookStore.ApiService/Aggregates/`
   - **Template**:
     ```csharp
     namespace BookStore.ApiService.Aggregates;

     public record Author
     {
         public Guid Id { get; init; }
         public string Name { get; init; } = string.Empty;
         public string Biography { get; init; } = string.Empty;
         public bool Deleted { get; init; }
         public int Version { get; init; }

         // Factory method for new aggregates
         public static Author Create(AuthorCreated @event)
         {
             return new Author
             {
                 Id = @event.Id,
                 Name = @event.Name,
                 Biography = @event.Biography
             };
         }

         // Apply method for Marten (MUST be void, single parameter)
         public void Apply(AuthorCreated @event)
         {
             // Marten uses this for event replay - do not return anything
         }

         // Apply method for subsequent events
         public void Apply(AuthorUpdated @event)
         {
             // Handle state changes
         }
     }
     ```

3. **Add Behavior Methods**
   - Add methods to aggregate that **return events**
   - **Pattern**: Validate → Return Event
   - **Example**:
     ```csharp
     public AuthorUpdated Update(string name, string biography)
     {
         if (Deleted)
             throw new InvalidOperationException("Cannot update deleted author");

         if (string.IsNullOrWhiteSpace(name))
             throw new ArgumentException("Name is required", nameof(name));

         return new AuthorUpdated(Id, name, biography, DateTimeOffset.UtcNow);
     }
     ```

4. **Configure Marten**
   - Open `src/BookStore.ApiService/Program.cs`
   - Add aggregate to Marten's event store:
     ```csharp
     builder.Services.AddMarten(options =>
     {
         // Existing configuration...

         // Add your aggregate
         options.Events.StreamIdentity = StreamIdentity.AsGuid;
     });
     ```

5. **Create Unit Tests**
   - Create test file in `tests/BookStore.ApiService.UnitTests/Aggregates/`
   - **Test Pattern**:
     ```csharp
     using TUnit.Core;
     using TUnit.Assertions.Extensions;

     public class AuthorTests
     {
         [Test]
         public async Task Create_ReturnsValidAggregate()
         {
             // Arrange
             var created = new AuthorCreated(
                 Guid.CreateVersion7(),
                 "Martin Fowler",
                 "Author and speaker",
                 DateTimeOffset.UtcNow
             );

             // Act
             var author = Author.Create(created);

             // Assert
             await Assert.That(author.Id).IsEqualTo(created.Id);
             await Assert.That(author.Name).IsEqualTo("Martin Fowler");
         }

         [Test]
         public async Task Update_DeletedAuthor_ThrowsException()
         {
             // Arrange
             var author = new Author { Deleted = true };

             // Act & Assert
             await Assert.That(() => author.Update("New Name", "Bio"))
                 .Throws<InvalidOperationException>();
         }
     }
     ```

6. **Verify Analyzer Compliance**
   - Run `dotnet build` to check for BS1xxx-BS4xxx warnings
   - Ensure:
     - ✅ Events are `record` types (BS1001)
     - ✅ Apply methods are `void` with single parameter (BS1002)
     - ✅ Aggregates use proper patterns (BS2xxx)

7. **Next Steps**
    - Use `/marten__single_stream_projection` or `/marten__multi_stream_projection` to create read models from your aggregate's events
    - Use `/wolverine__create_operation` (and `/wolverine__update_operation` when needed) to create complete command/handler/endpoint flows
    - Use `/test__integration_scaffold` to create integration tests
    - Use `/test__verify_feature` to ensure everything works

## Related Skills

**Prerequisites**:
- None - this is a foundational skill for event sourcing

**Next Steps**:
- `/marten__single_stream_projection` - Create read models from aggregate events
- `/marten__multi_stream_projection` - Aggregate multiple streams if needed
- `/wolverine__create_operation` - Add commands, handlers, and endpoints for this aggregate
- `/test__integration_scaffold` - Create integration tests
- `/test__verify_feature` - Run all verification checks

**See Also**:
- [wolverine__create_operation](../wolverine__create_operation/SKILL.md) - Complete write operation workflow
- [event-sourcing-guide](../../../docs/guides/event-sourcing-guide.md) - Event Sourcing patterns
- [marten-guide](../../../docs/guides/marten-guide.md) - Marten event store integration
- [analyzer-rules](../../../docs/guides/analyzer-rules.md) - Code analyzer rules (BS1xxx-BS4xxx)
- ApiService AGENTS.md - Backend patterns and conventions

## Key Rules to Remember

- **Apply Methods**: MUST be `void` with single event parameter (Marten convention)
- **Behavior Methods**: Return events, don't mutate state directly
- **IDs**: Use `Guid.CreateVersion7()` for new aggregates
- **Immutability**: Use `record` types with `init` properties
- **Validation**: Validate in behavior methods, throw exceptions for invalid operations
