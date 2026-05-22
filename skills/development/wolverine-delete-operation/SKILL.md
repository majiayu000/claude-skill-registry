---
name: wolverine__delete_operation
description: Adds a new DELETE operation (soft delete / tombstone) to the Backend. Use this when implementing DELETE endpoints to remove resources.
---

Follow this guide to implement a **Delete Operation** (Soft Delete) in the ApiService.

1.  **Define the Domain Event**
    -   Create a `record` in `src/BookStore.ApiService/Events/`
    -   **Naming**: `{Resource}Deleted`
    -   **Template**: `templates/Event.cs`

2.  **Define the Command**
    -   Create a `record` in `src/BookStore.ApiService/Commands/{Resource}/`
    -   **Naming**: `Delete{Resource}`
    -   **Template**: `templates/Command.cs`

3.  **Implement the Endpoint**
    -   Create/Update `src/BookStore.ApiService/Endpoints/{Resource}Endpoints.cs`
    -   **Pattern**: [Wolverine.HTTP](https://wolverinefx.net/guide/http/)
    -   **Features**: Use `[Aggregate]` attribute to auto-load state.
    -   **Logic**: Pure function receiving `aggregate` and returning `(IResult, IEvent)`.
    -   **Template**: `templates/Endpoint.cs`

4.  **Update Read Models**
    -   Ensure your projections handle the `{Resource}Deleted` event (e.g., set `Deleted = true` or remove document).

## Related Skills
- `/wolverine__create_operation`: For creating new resources.
- `/wolverine__update_operation`: For updating existing resources.
