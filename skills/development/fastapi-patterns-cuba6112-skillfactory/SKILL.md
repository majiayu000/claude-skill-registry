---
name: fastapi-patterns
description: Advanced FastAPI patterns including hierarchical dependency injection, background task management, and type-safe dependency annotation. Triggers: fastapi, dependency-injection, background-tasks, annotated-dependency, permission-chain.
---

# FastAPI Advanced Patterns

## Overview
FastAPI leverages Python's type hints and async capabilities to provide a robust framework for building APIs. Its core strength lies in its Dependency Injection system, which allows for clean, reusable, and hierarchical code structure.

## When to Use
- **Shared Logic**: When multiple endpoints need the same authentication, database session, or pagination logic.
- **Offloading I/O**: When a request triggers a slow operation (like sending an email) that shouldn't block the user response.
- **Complex Security**: When you need multi-level permission checks (e.g., User -> Active User -> Admin).

## Decision Tree
1. Do you need the same logic in 3+ endpoints? 
   - YES: Create a reusable Dependency.
2. Does an operation take more than 50ms and doesn't return data to the user? 
   - YES: Use `BackgroundTasks`.
3. Do you want full IDE autocompletion for injected values? 
   - YES: Use `Annotated[Type, Depends(func)]` syntax.

## Workflows

### 1. Implementing Reusable Shared Logic
1. Define a dependency function that extracts common parameters (e.g., pagination or auth).
2. Create a type alias using `Annotated[Type, Depends(dependency_function)]`.
3. Inject this alias into multiple path operation functions to access the shared logic results.

### 2. Offloading Tasks to the Background
1. Define a standard Python function for the slow task (e.g., sending an email).
2. Include `background_tasks: BackgroundTasks` as a parameter in the API endpoint.
3. Call `background_tasks.add_task(task_function, *args)` inside the endpoint.
4. Return a response immediately to the user while the task runs in the background.

### 3. Hierarchical Permission Checks
1. Create a base dependency for `get_current_user`.
2. Create a sub-dependency `get_active_user` that depends on `get_current_user`.
3. Create a final `get_admin_user` that depends on `get_active_user`.
4. FastAPI will execute the chain in order and stop if any dependency raises an HTTPException.

## Non-Obvious Insights
- **Dependency Tree Resolution**: FastAPI resolves a full tree of dependencies automatically; if three different dependencies all require the same database session, FastAPI can be configured to call the session creator only once per request.
- **Annotated is Best Practice**: Using `Annotated` keeps your code DRY (Don't Repeat Yourself) and ensures that static analysis tools understand exactly what type is being injected.
- **Flexible Background Tasks**: `BackgroundTasks` can be declared anywhere in the dependency chain, not just in the final endpoint function.

## Evidence
- "Dependency Injection means... that there is a way for your code to declare things that it requires to work and use." - [FastAPI Docs](https://fastapi.tiangolo.com/tutorial/dependencies/)
- "BackgroundTasks is useful for operations that need to happen after a request... client doesn't really have to be waiting." - [FastAPI Docs](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- "Annotated dependencies... type information will be preserved, which means your editor will keep providing autocompletion." - [FastAPI Docs](https://fastapi.tiangolo.com/tutorial/dependencies/)

## Scripts
- `scripts/fastapi-patterns_tool.py`: Example of Dependency Injection and Background Tasks.
- `scripts/fastapi-patterns_tool.js`: (Simulated) Pattern comparison for Node.js middleware.

## Dependencies
- `fastapi`
- `pydantic`

## References
- [references/README.md](references/README.md)