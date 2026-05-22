# Backend Error Handling Skill

**Purpose**: Guidance for consistent error handling, error response format, and HTTPException usage.

## Overview

All errors MUST use consistent JSON format with error code, message, and optional details. Use HTTPException with appropriate status codes. Handle validation errors, authentication errors, and database errors appropriately.

## Key Patterns

### 1. Standardized Error Response Format

**Pattern**: All error responses follow consistent format

```python
from fastapi import HTTPException, status

# Error response format (from HTTPException)
{
    "detail": "Error message"
}

# For validation errors with details
{
    "detail": [
        {
            "loc": ["body", "title"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```

**Pattern Rules**:
- Use HTTPException for all errors
- FastAPI automatically formats errors as JSON
- Use `detail` field for error message
- Pydantic validation errors include field locations

### 2. HTTP Status Codes

**Pattern**: Use appropriate HTTP status codes

```python
from fastapi import HTTPException, status

# 400 Bad Request - Validation errors
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid input data"
)

# 401 Unauthorized - Authentication errors
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or missing JWT token"
)

# 403 Forbidden - Authorization errors
raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User ID mismatch: You can only access your own data"
)

# 404 Not Found - Resource not found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Task not found"
)

# 409 Conflict - Resource conflict (e.g., duplicate email)
raise HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Email already registered"
)

# 500 Internal Server Error - Unexpected errors
raise HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal server error"
)
```

**Status Code Guidelines**:
- **400**: Client errors (validation, malformed request)
- **401**: Authentication required or failed
- **403**: Authorization failed (user mismatch, insufficient permissions)
- **404**: Resource not found
- **409**: Resource conflict (duplicate, constraint violation)
- **500**: Server errors (unexpected, database errors)

### 3. Validation Error Handling

**Pattern**: Handle Pydantic validation errors

```python
from fastapi import HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors"""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid input data",
                "details": exc.errors()
            }
        }
    )
```

**Pattern Rules**:
- Pydantic automatically validates request bodies
- Validation errors return 400 with field details
- Use exception handler for custom validation error format
- Include field locations in error details

### 4. Custom Validation Errors

**Pattern**: Raise validation errors from service layer

```python
from fastapi import HTTPException, status

def create_task(db: Session, user_id: str, task_data: TaskCreateRequest):
    # Validate title length
    if len(task_data.title) > 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title must be 200 characters or less"
        )
    
    # Validate description length
    if task_data.description and len(task_data.description) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Description must be 1000 characters or less"
        )
    
    # Validate priority enum
    if task_data.priority not in ["low", "medium", "high", None]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Priority must be low, medium, or high"
        )
```

**Pattern Rules**:
- Validate in service layer or route handler
- Return 400 for validation errors
- Provide clear, actionable error messages
- Validate enum values explicitly

### 5. Authentication Error Handling

**Pattern**: Handle JWT authentication errors

```python
from fastapi import HTTPException, status
from jose import ExpiredSignatureError, JWTError

def verify_jwt_token(credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])
        # ... extract user info
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please sign in again."
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing JWT token"
        )
```

**Pattern Rules**:
- Return 401 for authentication failures
- Distinguish between expired and invalid tokens
- Provide clear error messages
- Client should redirect to login on 401

### 6. Authorization Error Handling

**Pattern**: Handle user isolation violations

```python
from fastapi import HTTPException, status

@router.get("/{user_id}/tasks/{task_id}")
async def get_task(
    user_id: str,
    task_id: int,
    current_user: dict = Depends(verify_jwt_token)
):
    # Verify user_id matches JWT token
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID mismatch: You can only access your own data"
        )
    
    # Verify task belongs to user
    task = task_service.get_task_by_id(db, user_id, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
```

**Pattern Rules**:
- Return 403 for user_id mismatch (authorization failure)
- Return 404 if resource doesn't exist
- Always verify user_id before accessing resources
- Provide clear error messages

### 7. Database Error Handling

**Pattern**: Handle database errors gracefully

```python
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status

@router.post("/{user_id}/tasks")
async def create_task(
    user_id: str,
    task_data: TaskCreateRequest,
    db: Session = Depends(get_db)
):
    try:
        task = task_service.create_task(db, user_id, task_data)
        return {"success": True, "data": task}
    
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database constraint violation"
        )
    except SQLAlchemyError as e:
        db.rollback()
        # Log error for debugging
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
```

**Pattern Rules**:
- Catch `IntegrityError` for constraint violations (400)
- Catch `SQLAlchemyError` for database errors (500)
- Always rollback on errors
- Log errors for debugging
- Don't expose internal error details to clients

### 8. Global Error Handler

**Pattern**: Create global exception handler

```python
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors"""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid input data",
                "details": exc.errors()
            }
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "message": exc.detail
            }
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Internal server error"
            }
        }
    )
```

**Pattern Rules**:
- Register exception handlers in main.py
- Handle validation errors with field details
- Handle HTTPException with consistent format
- Handle unexpected errors with logging
- Don't expose internal error details

### 9. Error Response with Code

**Pattern**: Include error code in response

```python
from fastapi import HTTPException, status

class ErrorResponse:
    """Standard error response format"""
    
    @staticmethod
    def validation_error(message: str, details: dict = None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "VALIDATION_ERROR",
                "message": message,
                "details": details
            }
        )
    
    @staticmethod
    def authentication_error(message: str = "Invalid or missing JWT token"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "AUTHENTICATION_ERROR",
                "message": message
            }
        )
    
    @staticmethod
    def authorization_error(message: str = "User ID mismatch"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "AUTHORIZATION_ERROR",
                "message": message
            }
        )
    
    @staticmethod
    def not_found(resource: str = "Resource"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "NOT_FOUND",
                "message": f"{resource} not found"
            }
        )
```

**Pattern Rules**:
- Include error code for programmatic handling
- Use consistent error code names
- Include human-readable message
- Include optional details for validation errors

### 10. Query Parameter Validation Errors

**Pattern**: Handle invalid query parameters

```python
from fastapi import Query, HTTPException, status

@router.get("/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    status: Optional[str] = Query(None, regex="^(all|pending|completed)$"),
    sort: Optional[str] = Query(None, regex="^(created|title|updated|priority|due_date)$"),
    page: Optional[int] = Query(1, ge=1),
    limit: Optional[int] = Query(20, ge=1, le=100)
):
    # FastAPI automatically validates query parameters
    # Invalid values return 422 Unprocessable Entity
    pass
```

**Pattern Rules**:
- Use Query() with validation (regex, ge, le)
- FastAPI automatically returns 422 for invalid query params
- Provide default values for optional parameters
- Validate enum values with regex

## Steps for Error Handling in New Endpoint

1. **Validate Inputs**
   - Use Pydantic models for request validation
   - Add custom validation in service layer
   - Return 400 for validation errors

2. **Verify Authentication**
   - Use JWT verification dependency
   - Return 401 for authentication failures

3. **Verify Authorization**
   - Check user_id matches JWT token
   - Return 403 for authorization failures

4. **Handle Database Operations**
   - Wrap in try/except
   - Rollback on errors
   - Return appropriate status codes

5. **Handle Resource Not Found**
   - Check if resource exists
   - Return 404 if not found

6. **Handle Unexpected Errors**
   - Log errors for debugging
   - Return 500 with generic message
   - Don't expose internal details

## Common Patterns Summary

- ✅ Use HTTPException for all errors
- ✅ Use appropriate HTTP status codes
- ✅ Return consistent error format
- ✅ Include error code and message
- ✅ Provide clear, actionable error messages
- ✅ Handle validation errors with field details
- ✅ Handle database errors with rollback
- ✅ Log errors for debugging
- ✅ Don't expose internal error details
- ✅ Use global exception handlers

