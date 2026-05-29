---
name: marten__multi_stream_projection
description: Create a Marten Multi-Stream Projection to aggregate events from *multiple* streams into a single view (e.g., summaries, dashboards).
---

Follow this guide to create a **Multi-Stream Projection** (View Projection) in Marten. This allows you to aggregate data across many different streams into a single document (or multiple documents based on grouping).

1.  **Define the Projection Class**
    -   Create a `class` in `src/BookStore.ApiService/Projections/`
    -   **Naming**: `{Summary}Projection` (e.g., `AuthorDashboardProjection` or `MonthlySalesProjection`)
    -   **Base Class**: `MultiStreamProjection<T, TId>`
    -   **Template**: `templates/Projection.cs`

2.  **Configure in Marten**
    -   Open `src/BookStore.ApiService/Infrastructure/Extensions/MartenConfigurationExtensions.cs`
    -   Register:
        ```csharp
        options.Projections.Add<AuthorDashboardProjection>(ProjectionLifecycle.Async);
        ```

3.  **Indexing**
    -   Add indexes in `ConfigureIndexes` if you need to query by fields other than Id.

## Related Skills
- `/marten__single_stream_projection`: If you only need data from one stream.
- `/marten__event_projection`: If you need 1:1 transformation without aggregation.
