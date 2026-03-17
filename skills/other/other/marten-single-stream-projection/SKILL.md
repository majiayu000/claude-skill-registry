---
name: marten__single_stream_projection
description: Create a Marten Single Stream Projection to aggregate events from a single stream into a view (e.g., entity details).
---

Follow this guide to create a **Single Stream Projection** in Marten. This projection creates a single document for a single event stream (aggregate instance).

1.  **Define the Projection Class**
    -   Create a `class` in `src/BookStore.ApiService/Projections/`
    -   **Naming**: `{Resource}Projection` (e.g., `AuthorDetailsProjection`)
    -   **Base Class**: `SingleStreamProjection<T>` matches the standard pattern for explicit single stream aggregation.
    -   **Template**: `templates/Projection.cs`

2.  **Configure in Marten**
    -   Open `src/BookStore.ApiService/Infrastructure/Extensions/MartenConfigurationExtensions.cs`
    -   Register the projection in `RegisterProjections`:
        ```csharp
        options.Projections.Add<AuthorDetailsProjection>(ProjectionLifecycle.Async);
        ```
    -   *Note*: `Async` is recommended for performance. `Inline` handles consistency but impacts write performance.

3.  **Indexing (Optional)**
    -   In `ConfigureIndexes`:
        ```csharp
        options.Schema.For<AuthorDetailsProjection>().Index(x => x.Name);
        ```

4.  **Querying**
    -   Query this projection by ID (matching the stream ID) or other fields.
    -   Example: `session.LoadAsync<AuthorDetailsProjection>(streamId)`

## Related Skills
- `/marten__aggregate_scaffold`: Create the events first.
- `/marten__get_by_id`: Create an endpoint to query this projection.
- `/marten__list_query`: Create list endpoints if the projection supports browsing.
