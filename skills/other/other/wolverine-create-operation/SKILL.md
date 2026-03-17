---
name: wolverine__create_operation
description: Adds a new CREATE operation (starting a stream) to the Backend. Use this when implementing POST endpoints to create new resources.
---

Follow this guide to implement a **Create Operation** (Start Stream) in the ApiService.

1.  **Define the Domain Event**
    -   Create a `record` in `src/BookStore.ApiService/Events/`
    -   **Naming**: `{Resource}Created`
    -   **Template**: `templates/Event.cs`

2.  **Define the Command**
    -   Create a `record` in `src/BookStore.ApiService/Commands/{Resource}/`
    -   **Naming**: `Create{Resource}`
    -   **Template**: `templates/Command.cs`

3.  **Implement the Endpoint**
    -   Create/Update `src/BookStore.ApiService/Endpoints/{Resource}Endpoints.cs`
    -   **Pattern**: [Wolverine.HTTP](https://wolverinefx.net/guide/http/)
    -   **Logic**: Pure function returning `(IResult, StartStream<T>)`
    -   **Template**: `templates/Endpoint.cs`

4.  **Update Read Models**
    -   Ensure your projections handle the `{Resource}Created` event.

## Related Skills
- `/wolverine__update_operation`: For updating existing resources.
- `/wolverine__delete_operation`: For deleting resources.
