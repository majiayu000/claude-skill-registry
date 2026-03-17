---
name: marten__get_by_id
description: Adds a new GET operation to fetch a single resource by ID. Handles 404s, caching, and localization.
---

Follow this guide to implement a **Get By ID** endpoint in the ApiService.

1.  **Prerequisites**
    -   Ensure the Projection exists (`/marten__single_stream_projection` or similar).

2.  **Create Endpoint**
    -   Create/Update `src/BookStore.ApiService/Endpoints/{Resource}Endpoints.cs`
    -   **Method**: `MapGet`
    -   **Logic**: `GetOrCreateLocalizedAsync` -> `LoadAsync` -> Map to DTO
    -   **Template**: `templates/GetByIdEndpoint.cs`

3.  **Client Integration**
    -   Create `IGet{Resource}Endpoint.cs` in Client project.

## Related Skills
- `/marten__list_query`: For fetching lists of resources.
