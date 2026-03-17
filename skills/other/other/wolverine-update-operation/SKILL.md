---
name: wolverine__update_operation
description: Adds a new UPDATE operation (appending to stream) to the Backend. Use this when implementing PUT or PATCH endpoints to modify existing resources.
---

Follow this guide to implement an **Update Operation** in the ApiService.

1.  **Define the Domain Event**
    -   Create a `record` in `src/BookStore.ApiService/Events/`
    -   **Naming**: `{Resource}Updated` or specific action (e.g., `BookPublished`)
    -   **Template**: `templates/Event.cs`

2.  **Define the Command**
    -   Create a `record` in `src/BookStore.ApiService/Commands/{Resource}/`
    -   **Naming**: `{Verb}{Resource}` (e.g., `UpdateAuthor`, `PublishBook`)
    -   **Template**: `templates/Command.cs`

3.  **Implement the Endpoint**
    -   Create/Update `src/BookStore.ApiService/Endpoints/{Resource}Endpoints.cs`
    -   **Pattern**: [Wolverine.HTTP](https://wolverinefx.net/guide/http/)
    -   **Features**: Use `[Aggregate]` attribute to auto-load state.
    -   **Logic**: Pure function receiving `aggregate` and returning `(IResult, IEvent)`.
    -   **Template**: `templates/Endpoint.cs`

4.  **Update Read Models**
    -   Ensure your projections handle the events.

## Related Skills
- `/wolverine__create_operation`: For creating new resources.
- `/wolverine__delete_operation`: For deleting resources.
