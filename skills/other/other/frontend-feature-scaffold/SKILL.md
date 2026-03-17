---
name: frontend__feature_scaffold
description: Adds a new feature to the Web Frontend (Blazor) with Reactive State, Optimistic Updates, and Cache Invalidation. Use this when implementing user-facing features that need real-time updates.
---

Follow this guide to implement a responsive frontend feature in `src/Web/BookStore.Web`.

1. **Prerequisites**
   - Ensure the API Client exists: `src/Client/BookStore.Client/I{Resource}Client.cs`.
   - Ensure the Shared/Response DTOs exist in `BookStore.Shared`.
   - if NOT, run `/marten__list_query` (for queries) or `/wolverine__create_operation` (for mutations) first.

1. **Create the Component**
   - Create/Update `src/Web/BookStore.Web/Components/Pages/{Feature}.razor`.
   - **Template**: `templates/Page.razor`
   - **Lifecycle**: Use `OnInitializedAsync` to start listening: `EventsService.StartListening();`.

2. **Implement Data Fetching**
   - **Pattern**: Use `ReactiveQuery<T>`.
   - **Setup (Template)**: `templates/ReactiveQueryInit.cs`

3. **Implement Optimistic Updates (Properties)**
   - **Use Case**: Toggling a boolean, changing a number (e.g., Favorites).
   - **Pattern**: `Mutate -> Call -> Rollback`.
     ```csharp
     query.MutateData(s => s with { IsFavorite = true }); // 1. Instant UI update
     try {
         await Client.UpdateAsync(); // 2. API Call
     } catch {
         query.MutateData(s => s with { IsFavorite = false }); // 3. Revert on error
     }
     ```

4. **Implement Optimistic Updates (Lists)**
   - **Use Case**: Adding a new item to a list instantly.
   - **Pattern**:
     ```csharp
     OptimisticService.AddOptimisticBook(id, title); // 1. Add to separate list
     await Client.CreateAsync(); // 2. API Call (Event will confirm/remove it)
     ```
   - **UI**: Merge `query.Data` with `OptimisticService.GetOptimisticBooks()` when rendering lists.

5. **Configure Invalidation**
   - Open `src/Web/BookStore.Web/Services/QueryInvalidationService.cs`.
   - Add cases to `GetInvalidationKeys(IDomainEventNotification notification)`.
   - **Rule**: Map the Domain Event (e.g., `BookCreated`) to the Query Keys you defined in Step 2 (e.g., `"Books"`).

6. **Verify**
   - Run the app and verify:
     1. Data loads.
     2. Mutations update UI instantly.
     3. SSE events (from other tabs/users) trigger auto-refetch.
   - Run `/test__verify_feature` for complete verification.

## Related Skills

**Prerequisites**:
- Backend endpoints must exist first:
   - `/wolverine__create_operation` - For mutation endpoints
   - `/marten__list_query` - For query endpoints
- Client SDK must be configured (usually done by the backend scaffolding skills)

**Next Steps**:
- `/test__integration_scaffold` - Create integration tests for the feature
- `/test__verify_feature` - Complete verification

**Debugging**:
- `/frontend__debug_sse` - If real-time updates don't work
- `/cache__debug_cache` - If query data is stale

**See Also**:
- [real-time-notifications](../../../docs/guides/real-time-notifications.md) - SSE architecture
- [wolverine__create_operation](../wolverine__create_operation/SKILL.md) - Backend mutations
- [marten__list_query](../marten__list_query/SKILL.md) - Backend queries
- Web AGENTS.md - ReactiveQuery patterns and SSE integration
