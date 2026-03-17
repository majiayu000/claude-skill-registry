---
name: marten__event_projection
description: Create a Marten Event Projection for 1:1 event transformation or side-effects (creating separate documents per event).
---

Follow this guide to create a **Event Projection** in Marten. This is best for flattening events into queryable documents (1 event -> 1 document) or copying data to other tables.

1.  **Define the Projection Class**
    -   Create a `class` in `src/BookStore.ApiService/Projections/`
    -   **Base Class**: `EventProjection`
    -   **Template**: `templates/Projection.cs`

2.  **Configure in Marten**
    -   Open `src/BookStore.ApiService/Infrastructure/Extensions/MartenConfigurationExtensions.cs`
    -   Register:
        ```csharp
        options.Projections.Add<AuditLogProjection>(ProjectionLifecycle.Async);
        ```

3.  **Use Cases**
    -   History tables
    -   Audit logs
    -   Flattening stream data for reporting/analytics (without aggregation)

## Related Skills
- `/marten__multi_stream_projection`: For aggregating data.
