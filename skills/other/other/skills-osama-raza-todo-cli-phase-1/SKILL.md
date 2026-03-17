---
name: error-handling-skill
description: Standardized error handling functions for formatting, logging, and returning user-friendly error messages across the application.
functions:
  - name: handle_error
    description: Format an error message, log it with context, and return a user-friendly message
    parameters:
      type: object
      properties:
        error:
          type: Exception
          description: The exception or error to handle
        context:
          type: str
          description: Context information about where/why the error occurred
      required:
        - error
        - context
    returns:
      type: str
      description: A user-friendly error message

  - name: format_error_message
    description: Format an error message with consistent styling and optional error code
    parameters:
      type: object
      properties:
        message:
          type: str
          description: The error message to format
        error_code:
          type: str
          description: Optional error code to include
          default: ""
      required:
        - message
    returns:
      type: str
      description: Formatted error message in "✗ Error: [message]" format

  - name: log_error
    description: Log an error to stderr or file with timestamp and context
    parameters:
      type: object
      properties:
        error:
          type: Exception
          description: The exception to log
        context:
          type: str
          description: Context information about where the error occurred
      required:
        - error
        - context
    returns:
      type: None
      description: None
---

# Error Handling Skill

## Purpose
Provides standardized error handling across the application with consistent formatting, logging, and user-friendly messages.

## Functions

### 1. handle_error(error: Exception, context: str) -> str

Handles an exception by formatting the error message, logging it with context, and returning a user-friendly message.

**Parameters:**
- `error` (Exception): The exception or error object to handle
- `context` (str): Context information about where/why the error occurred

**Returns:**
- A user-friendly error message string

**Behavior:**
1. Format the error message using `format_error_message()`
2. Log the error using `log_error()`
3. Return a user-friendly message for display

### 2. format_error_message(message: str, error_code: str = "") -> str

Formats an error message with consistent styling and optional error code.

**Parameters:**
- `message` (str): The error message to format
- `error_code` (str, optional): Error code to include. Defaults to "".

**Returns:**
- Formatted error message in the format: "✗ Error: [message]"
- If error_code is provided: "✗ Error: [message] [error_code]"

**Examples:**
```python
format_error_message("File not found")  # "✗ Error: File not found"
format_error_message("Connection failed", "ERR_001")  # "✗ Error: Connection failed [ERR_001]"
```

### 3. log_error(error: Exception, context: str) -> None

Logs an error to stderr or file with timestamp and context information.

**Parameters:**
- `error` (Exception): The exception or error object to log
- `context` (str): Context information about where the error occurred

**Returns:**
- None

**Log Format:**
```
[TIMESTAMP] ERROR | Context: [context] | Message: [error_message] | Type: [error_type]
```

## Error Message Format

All error messages follow the format:
```
✗ Error: [message]
```

## Logging Setup

The skill uses Python's standard `logging` module with the following configuration:
- Format: `[%(asctime)s] %(levelname)s | %(message)s`
- Timestamp: ISO 8601 format
- Output: stderr by default
- Can be configured to log to file by setting up a file handler

## Usage Example

```python
from error_handling_skill import handle_error, format_error_message, log_error

try:
    risky_operation()
except Exception as e:
    user_message = handle_error(e, "user_authentication")
    print(user_message)
    # Output: "✗ Error: Authentication failed - Invalid credentials"
```

## Implementation Notes

- All functions include proper type hints
- All functions have docstrings documenting parameters, returns, and behavior
- Logging is configurable for different output destinations
- Error codes are optional but recommended for traceability
