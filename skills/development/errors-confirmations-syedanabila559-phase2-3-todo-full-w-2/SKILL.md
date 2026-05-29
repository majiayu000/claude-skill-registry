---
name: errors-confirmations
description: This skill should be used when implementing graceful error handling and user confirmations in both backend and frontend, including friendly tool not found messages, action confirmations, error toasts, and loading indicators.
---

# Errors & Confirmations Skill

This skill provides guidance for implementing graceful error handling and user confirmations.

## Purpose

Implement graceful errors in backend/frontend:
- Tool not found → "Task not found, try again"
- Always confirm actions in response (e.g., "Task added!")
- Frontend: Show error toasts, loading indicators

## When to Use

Use this skill when:
- Building error handling for chat API
- Creating user feedback mechanisms
- Implementing loading states
- Adding confirmation messages

## Capabilities

- **Backend Errors**: Structured error responses with user-friendly messages
- **Frontend Feedback**: Toast notifications, loading states
- **Action Confirmations**: Clear success messages for user actions
- **Error Recovery**: Graceful degradation and retry suggestions

## Backend Error Handling

### Error Response Models

```python
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class ErrorSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    message: str  # User-friendly message
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    retryable: bool = True
    suggestion: Optional[str] = None

class ToolError(Exception):
    def __init__(
        self,
        message: str,
        user_message: str,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        retryable: bool = True,
        suggestion: Optional[str] = None
    ):
        self.message = message
        self.user_message = user_message
        self.severity = severity
        self.retryable = retryable
        self.suggestion = suggestion
        super().__init__(message)
```

### Error Handlers

```python
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(ToolError)
async def tool_error_handler(request: Request, exc: ToolError):
    return JSONResponse(
        status_code=400 if exc.severity == ErrorSeverity.LOW else 500,
        content={
            "success": False,
            "error": exc.message,
            "message": exc.user_message,
            "severity": exc.severity.value,
            "retryable": exc.retryable,
            "suggestion": exc.suggestion
        }
    )

@app.exception_handler(HTTPException)
async def http_error_handler(request: Request, exc: HTTPException):
    user_messages = {
        400: "There was an issue with your request. Please check and try again.",
        401: "Please sign in to continue.",
        403: "You don't have permission for this action.",
        404: "The requested item was not found.",
        500: "Something went wrong on our end. Please try again."
    }

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "message": user_messages.get(exc.status_code, "An error occurred"),
            "retryable": exc.status_code >= 500
        }
    )
```

### Tool-Specific Errors

```python
async def get_task_by_id(user_id: str, task_id: str) -> Task:
    """Get task with proper error handling."""
    result = await session.execute(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
    )
    task = result.scalar_one_or_none()

    if not task:
        raise ToolError(
            message=f"Task {task_id} not found",
            user_message="I couldn't find that task. It may have been deleted already.",
            severity=ErrorSeverity.LOW,
            retryable=False,
            suggestion="Try listing your tasks to see what's available."
        )

    return task

async def add_task(user_id: str, title: str, **kwargs) -> dict:
    """Add task with confirmation."""
    try:
        task = Task(user_id=user_id, title=title, **kwargs)
        session.add(task)
        await session.commit()
        await session.refresh(task)

        return {
            "success": True,
            "message": f"Task added successfully!",
            "task": task_to_dict(task)
        }

    except Exception as e:
        raise ToolError(
            message=f"Failed to add task: {str(e)}",
            user_message="I wasn't able to add that task. Please try again.",
            severity=ErrorSeverity.MEDIUM,
            retryable=True,
            suggestion="Check that the title isn't too long and try once more."
        )
```

## Frontend Error Handling

### Toast Notifications

```tsx
// components/Toast.tsx
interface ToastProps {
  message: string;
  type: "success" | "error" | "info" | "warning";
  onClose: () => void;
}

export function Toast({ message, type, onClose }: ToastProps) {
  const styles = {
    success: "bg-green-500",
    error: "bg-red-500",
    info: "bg-blue-500",
    warning: "bg-yellow-500"
  };

  return (
    <div className={`toast ${styles[type]} fixed bottom-4 right-4 text-white px-4 py-3 rounded-lg shadow-lg flex items-center gap-2 animate-fade-in`}>
      <span>{type === "success" ? "✓" : type === "error" ? "✕" : "ℹ"}</span>
      <span>{message}</span>
      <button onClick={onClose} className="ml-2 hover:opacity-80">×</button>
    </div>
  );
}
```

### Toast Container

```tsx
// contexts/ToastContext.tsx
"use client";

import { createContext, useContext, useState, ReactNode } from "react";
import { Toast } from "@/components/Toast";

interface ToastItem {
  id: string;
  message: string;
  type: "success" | "error" | "info" | "warning";
}

interface ToastContextType {
  showToast: (message: string, type: ToastItem["type"]) => void;
}

const ToastContext = createContext<ToastContextType | null>(null);

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<ToastItem[]>([]);

  const showToast = (message: string, type: ToastItem["type"]) => {
    const id = Date.now().toString();
    setToasts(prev => [...prev, { id, message, type }]);

    // Auto-remove after 5 seconds
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, 5000);
  };

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      <div className="fixed bottom-4 right-4 z-50 space-y-2">
        {toasts.map(toast => (
          <Toast
            key={toast.id}
            message={toast.message}
            type={toast.type}
            onClose={() => setToasts(prev => prev.filter(t => t.id !== toast.id))}
          />
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error("useToast must be used within ToastProvider");
  }
  return context;
}
```

### Loading Indicator

```tsx
// components/LoadingIndicator.tsx
export function LoadingIndicator() {
  return (
    <div className="flex items-center gap-2 text-gray-500 p-2">
      <div className="typing-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
      <span className="text-sm">Thinking...</span>
    </div>
  );
}

export function LoadingButton({
  children,
  loading,
  disabled,
  onClick,
  className = ""
}: {
  children: React.ReactNode;
  loading: boolean;
  disabled?: boolean;
  onClick?: () => void;
  className?: string;
}) {
  return (
    <button
      onClick={onClick}
      disabled={loading || disabled}
      className={`relative ${className}`}
    >
      {loading && (
        <span className="absolute inset-0 flex items-center justify-center">
          <Spinner />
        </span>
      )}
      <span className={loading ? "invisible" : ""}>{children}</span>
    </button>
  );
}

function Spinner() {
  return (
    <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
        fill="none"
      />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>
  );
}
```

### Error Boundary

```tsx
// components/ErrorBoundary.tsx
"use client";

import { Component, ReactNode } from "react";
import { useToast } from "@/contexts/ToastContext";

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: any) {
    console.error("Error caught by boundary:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <h3 className="font-bold text-red-800">Something went wrong</h3>
          <p className="text-red-600 mt-1">Please refresh the page and try again.</p>
          <button
            onClick={() => this.setState({ hasError: false })}
            className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Try Again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

## Confirmation Messages

```python
# Backend confirmation templates
CONFIRMATIONS = {
    "add_task": "✓ Task added! I've created '{title}' for you.",
    "complete_task": "✓ Done! '{title}' is marked as complete.",
    "delete_task": "✓ Removed '{title}' from your tasks.",
    "update_task": "✓ Updated '{title}' with your changes.",
    "list_tasks": "Here are your {count} {status} tasks:"
}

def format_confirmation(action: str, **kwargs) -> str:
    """Format a confirmation message."""
    template = CONFIRMATIONS.get(action, "✓ Action completed!")
    return template.format(**kwargs)
```

## API Response Wrapper

```python
def success_response(
    message: str,
    data: Optional[dict] = None,
    confirmation: bool = True
) -> dict:
    """Create a success response with optional confirmation."""
    response = {
        "success": True,
        "message": message,
        "confirmation": confirmation
    }
    if data:
        response["data"] = data
    return response

def error_response(
    user_message: str,
    error: Optional[str] = None,
    suggestion: Optional[str] = None
) -> dict:
    """Create an error response."""
    return {
        "success": False,
        "message": user_message,
        "error": error,
        "suggestion": suggestion
    }
```

## Verification Checklist

- [ ] Tool errors return user-friendly messages
- [ ] Backend confirms actions ("Task added!")
- [ ] Frontend shows toast notifications
- [ ] Loading indicators during API calls
- [ ] Error boundary catches React errors
- [ ] Suggestions provided for recovery
- [ ] Graceful degradation on failures
