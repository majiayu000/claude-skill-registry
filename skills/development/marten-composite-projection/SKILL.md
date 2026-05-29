---
name: marten__composite_projection
description: Create a Marten Composite Projection to chain multiple projections or group them for performance. Use this when you need to use the output of one projection as the input for another, or to optimize daemon throughput.
---

Follow this guide to create a **Composite Projection** in Marten (v8.18+).

1.  **Define the Projection Class**
    -   Create a `class` in `src/BookStore.ApiService/Projections/`
    -   **Naming**: `{Summary}Projection` (typically a View Projection)
    -   **Base Class**: `MultiStreamProjection<T, TId>` (usually) or custom.
    -   **Template**: `templates/Projection.cs`

2.  **Configure in Marten**
    -   Open `src/BookStore.ApiService/Infrastructure/Extensions/MartenConfigurationExtensions.cs`
    -   Register using `CompositeProjectionFor`:
        ```csharp
        options.Projections.CompositeProjectionFor("GroupDetails", projection =>
        {
            // Stage 1: Basic Projections
            projection.Add<UserProjection>();
            projection.Add<OrderProjection>();

            // Stage 2: Dependent Projections (inputs from Stage 1)
            projection.Add<UserDashboardProjection>(2);
        });
        ```

3.  **Indexing**
    -   Configure indexes as usual in `ConfigureIndexes`.

## Related Skills
- `/marten__multi_stream_projection`: For standard multi-stream aggregates.
- `/marten__single_stream_projection`: For standard single-stream aggregates.
