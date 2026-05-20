---
name: fastapi-error-handling
description: Provides a comprehensive, reusable skill for standardized API error handling in FastAPI. Includes custom exception classes, global exception handlers, structured JSON logging, and standardized Pydantic error schemas. Use this when you need to implement a robust error handling system in a FastAPI project.
---

# FastAPI Error Handling Skill

This skill provides a structured and reusable approach to handling exceptions in a FastAPI application. It includes custom exceptions, global handlers, structured logging, and standardized response schemas.

## Core Components

The implementation is split across four reference files for clarity and modularity. You should create a new module in your project (e.g., `my_app/error_handling/`) and place these files within it. Remember to add an empty `__init__.py` in that directory to make it a Python package.

1.  **`references/exceptions.py`**: Contains a hierarchy of custom exception classes that can be raised from your application logic.
2.  **`references/schemas.py`**: Defines the Pydantic models for standardized error responses.
3.  **`references/handlers.py`**: Provides global exception handler functions to catch custom and unhandled exceptions, format the response, and log the error.
4.  **`references/logging_config.py`**: Includes a configuration for structured JSON logging, which is crucial for monitoring and debugging in production.

## How to Use

### Step 1: Integrate the Components

1.  Create a new package in your FastAPI project (e.g., `my_project/error_handling`).
2.  Copy the content from the following files into the corresponding new files within your `error_handling` package:
    *   `references/exceptions.py` -> `my_project/error_handling/exceptions.py`
    *   `references/schemas.py` -> `my_project/error_handling/schemas.py`
    *   `references/handlers.py` -> `my_project/error_handling/handlers.py`
    *   `references/logging_config.py` -> `my_project/error_handling/logging_config.py`
3.  Create an empty `my_project/error_handling/__init__.py` file.
4.  The logging configuration in `logging_config.py` requires `python-json-logger`. Install it:
    ```bash
    pip install python-json-logger
    ```

### Step 2: Configure Your FastAPI App

In your main application file (e.g., `main.py`), import and apply the configurations.

```python
from fastapi import FastAPI
from my_project.error_handling.handlers import register_exception_handlers
from my_project.error_handling.logging_config import setup_logging

# Apply structured logging configuration
setup_logging()

app = FastAPI()

# Register the global exception handlers
register_exception_handlers(app)

# ... your routes and other application logic
```

### Step 3: Use in Your Application

Now you can raise the custom exceptions from your API endpoints. The global handlers will automatically catch them and return a standardized JSON response.

**Example:**

```python
from fastapi import APIRouter
from my_project.error_handling.exceptions import NotFound, Unauthorized

router = APIRouter()

@router.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 42:
        # This will be caught by the api_exception_handler
        raise NotFound(message=f"Item with id {item_id} does not exist.")
    if item_id == 13:
        # This will also be caught
        raise Unauthorized(user_message="You do not have permission to view this sacred item.")
    return {"item_id": item_id}

@router.get("/unhandled")
async def trigger_unhandled_error():
    # This will be caught by the unhandled_exception_handler
    result = 1 / 0
    return {"result": result}

app.include_router(router)
```

## Customization

-   **Environment:** The `handlers.py` file uses a simple `IS_DEV_ENVIRONMENT` flag. In a real application, you should replace this with a proper settings management system (e.g., Pydantic's `BaseSettings`) to control whether debug information is included in responses.
-   **Exceptions:** You can easily extend `exceptions.py` with more specific exception classes inheriting from `APIException`.
