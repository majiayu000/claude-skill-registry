---
name: marten__list_query
description: Adds a new Query operation to fetch a paged list of resources with filtering. Handles caching and pagination.
---

Follow this guide to implement a **List Query** endpoint in the ApiService.

1.  **Prerequisites**
    -   Ensure the Projection exists.
    -   Ensure indexes are configured for filtered fields.

2.  **Create Endpoint**
    -   Create/Update `src/BookStore.ApiService/Endpoints/{Resource}Endpoints.cs`
    -   **Method**: `MapGet`
    -   **Logic**: `GetOrCreateLocalizedAsync` -> `Query` -> `Where` -> `ToPagedListAsync`
    -   **Template**: `templates/ListEndpoint.cs`

3.  **Client Integration**
    -   Create `IGet{Resource}sEndpoint.cs` in Client project.

## Related Skills
- `/marten__get_by_id`: For fetching a single resource.
