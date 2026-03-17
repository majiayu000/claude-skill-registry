---
name: handler-generator
description: Generates new Go HTTP handlers following Ishkul patterns. Creates handler with proper request/response types, error handling, validation, structured logging, and matching test file. Use when adding new API endpoints.
---

# Go Handler Generator

Creates new Go HTTP handlers following Ishkul's established patterns.

## What Gets Created

When generating a new handler, create:

1. **Handler file**: `backend/internal/handlers/resource_name.go`
2. **Test file**: `backend/internal/handlers/resource_name_test.go`
3. **Route registration**: Update `backend/cmd/server/main.go`
4. **Models** (if needed): `backend/internal/models/resource_name.go`

## Handler Template

```go
package handlers

import (
    "encoding/json"
    "net/http"
    "log/slog"

    "github.com/mesbahtanvir/ishkul/backend/internal/middleware"
    "github.com/mesbahtanvir/ishkul/backend/internal/models"
    "github.com/mesbahtanvir/ishkul/backend/pkg/firebase"
)

// =============================================================================
// Request/Response Types
// =============================================================================

// CreateResourceRequest represents the request body for creating a resource
type CreateResourceRequest struct {
    Title       string `json:"title"`
    Description string `json:"description,omitempty"`
}

// ResourceResponse represents a resource in API responses
type ResourceResponse struct {
    ID          string `json:"id"`
    Title       string `json:"title"`
    Description string `json:"description,omitempty"`
    UserID      string `json:"userId"`
    CreatedAt   string `json:"createdAt"`
    UpdatedAt   string `json:"updatedAt"`
}

// ListResourcesResponse represents the response for listing resources
type ListResourcesResponse struct {
    Resources []ResourceResponse `json:"resources"`
    Total     int                `json:"total"`
}

// =============================================================================
// Error Codes (use existing from auth.go or add new ones)
// =============================================================================

const (
    ErrCodeResourceNotFound = "RESOURCE_NOT_FOUND"
    ErrCodeResourceExists   = "RESOURCE_EXISTS"
)

// =============================================================================
// Main Handler (Router)
// =============================================================================

// ResourcesHandler routes requests to the appropriate handler based on path and method
// Handles:
//   - POST /api/resources - Create resource
//   - GET /api/resources - List user's resources
//   - GET /api/resources/{id} - Get single resource
//   - PUT /api/resources/{id} - Update resource
//   - DELETE /api/resources/{id} - Delete resource
func ResourcesHandler(w http.ResponseWriter, r *http.Request) {
    // Parse resource ID from path if present
    // Path: /api/resources or /api/resources/{id}
    resourceID := extractResourceID(r.URL.Path, "/api/resources/")

    if resourceID == "" {
        // Root path: /api/resources
        switch r.Method {
        case http.MethodPost:
            createResource(w, r)
        case http.MethodGet:
            listResources(w, r)
        default:
            http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        }
    } else {
        // Resource path: /api/resources/{id}
        switch r.Method {
        case http.MethodGet:
            getResource(w, r, resourceID)
        case http.MethodPut:
            updateResource(w, r, resourceID)
        case http.MethodDelete:
            deleteResource(w, r, resourceID)
        default:
            http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        }
    }
}

// =============================================================================
// Individual Handlers
// =============================================================================

// createResource handles POST /api/resources
func createResource(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()

    // 1. Get authenticated user from context (set by auth middleware)
    userID := middleware.GetUserID(ctx)
    if userID == "" {
        sendErrorResponse(w, http.StatusUnauthorized, ErrCodeUnauthorized, "User not authenticated")
        return
    }

    // 2. Parse request body
    var req CreateResourceRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        sendErrorResponse(w, http.StatusBadRequest, ErrCodeInvalidRequest, "Invalid request format")
        return
    }

    // 3. Validate input
    if req.Title == "" {
        sendErrorResponse(w, http.StatusBadRequest, ErrCodeInvalidRequest, "Title is required")
        return
    }

    if len(req.Title) > 200 {
        sendErrorResponse(w, http.StatusBadRequest, ErrCodeInvalidRequest, "Title must be 200 characters or less")
        return
    }

    // 4. Create resource in Firestore
    firestoreClient, err := firebase.GetFirestoreClient(ctx)
    if err != nil {
        appLogger.Error("firestore_client_error",
            slog.String("error", err.Error()),
            slog.String("user_id", userID),
        )
        sendErrorResponse(w, http.StatusInternalServerError, ErrCodeInternalError, "Database connection failed")
        return
    }

    resource := models.Resource{
        ID:          generateID(), // Use UUID or similar
        Title:       req.Title,
        Description: req.Description,
        UserID:      userID,
        CreatedAt:   time.Now(),
        UpdatedAt:   time.Now(),
    }

    _, err = firestoreClient.Collection("resources").Doc(resource.ID).Set(ctx, resource)
    if err != nil {
        appLogger.Error("resource_create_error",
            slog.String("error", err.Error()),
            slog.String("user_id", userID),
        )
        sendErrorResponse(w, http.StatusInternalServerError, ErrCodeInternalError, "Failed to create resource")
        return
    }

    // 5. Log success
    appLogger.Info("resource_created",
        slog.String("resource_id", resource.ID),
        slog.String("user_id", userID),
        slog.String("title", resource.Title),
    )

    // 6. Return response
    response := ResourceResponse{
        ID:          resource.ID,
        Title:       resource.Title,
        Description: resource.Description,
        UserID:      resource.UserID,
        CreatedAt:   resource.CreatedAt.Format(time.RFC3339),
        UpdatedAt:   resource.UpdatedAt.Format(time.RFC3339),
    }

    JSONCreated(w, response)
}

// listResources handles GET /api/resources
func listResources(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()

    userID := middleware.GetUserID(ctx)
    if userID == "" {
        sendErrorResponse(w, http.StatusUnauthorized, ErrCodeUnauthorized, "User not authenticated")
        return
    }

    firestoreClient, err := firebase.GetFirestoreClient(ctx)
    if err != nil {
        sendErrorResponse(w, http.StatusInternalServerError, ErrCodeInternalError, "Database connection failed")
        return
    }

    // Query user's resources
    docs, err := firestoreClient.Collection("resources").
        Where("userId", "==", userID).
        OrderBy("createdAt", firestore.Desc).
        Limit(100). // Always limit queries
        Documents(ctx).
        GetAll()

    if err != nil {
        appLogger.Error("resources_list_error",
            slog.String("error", err.Error()),
            slog.String("user_id", userID),
        )
        sendErrorResponse(w, http.StatusInternalServerError, ErrCodeInternalError, "Failed to fetch resources")
        return
    }

    resources := make([]ResourceResponse, 0, len(docs))
    for _, doc := range docs {
        var resource models.Resource
        if err := doc.DataTo(&resource); err != nil {
            continue // Skip invalid documents
        }

        resources = append(resources, ResourceResponse{
            ID:          resource.ID,
            Title:       resource.Title,
            Description: resource.Description,
            UserID:      resource.UserID,
            CreatedAt:   resource.CreatedAt.Format(time.RFC3339),
            UpdatedAt:   resource.UpdatedAt.Format(time.RFC3339),
        })
    }

    JSONSuccess(w, ListResourcesResponse{
        Resources: resources,
        Total:     len(resources),
    })
}

// getResource handles GET /api/resources/{id}
func getResource(w http.ResponseWriter, r *http.Request, resourceID string) {
    ctx := r.Context()

    userID := middleware.GetUserID(ctx)
    if userID == "" {
        sendErrorResponse(w, http.StatusUnauthorized, ErrCodeUnauthorized, "User not authenticated")
        return
    }

    firestoreClient, err := firebase.GetFirestoreClient(ctx)
    if err != nil {
        sendErrorResponse(w, http.StatusInternalServerError, ErrCodeInternalError, "Database connection failed")
        return
    }

    doc, err := firestoreClient.Collection("resources").Doc(resourceID).Get(ctx)
    if err != nil {
        if status.Code(err) == codes.NotFound {
            sendErrorResponse(w, http.StatusNotFound, ErrCodeResourceNotFound, "Resource not found")
            return
        }
        sendErrorResponse(w, http.StatusInternalServerError, ErrCodeInternalError, "Failed to fetch resource")
        return
    }

    var resource models.Resource
    if err := doc.DataTo(&resource); err != nil {
        sendErrorResponse(w, http.StatusInternalServerError, ErrCodeInternalError, "Failed to parse resource")
        return
    }

    // Check ownership
    if resource.UserID != userID {
        sendErrorResponse(w, http.StatusNotFound, ErrCodeResourceNotFound, "Resource not found")
        return
    }

    JSONSuccess(w, ResourceResponse{
        ID:          resource.ID,
        Title:       resource.Title,
        Description: resource.Description,
        UserID:      resource.UserID,
        CreatedAt:   resource.CreatedAt.Format(time.RFC3339),
        UpdatedAt:   resource.UpdatedAt.Format(time.RFC3339),
    })
}

// updateResource handles PUT /api/resources/{id}
func updateResource(w http.ResponseWriter, r *http.Request, resourceID string) {
    ctx := r.Context()

    userID := middleware.GetUserID(ctx)
    if userID == "" {
        sendErrorResponse(w, http.StatusUnauthorized, ErrCodeUnauthorized, "User not authenticated")
        return
    }

    var req CreateResourceRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        sendErrorResponse(w, http.StatusBadRequest, ErrCodeInvalidRequest, "Invalid request format")
        return
    }

    firestoreClient, err := firebase.GetFirestoreClient(ctx)
    if err != nil {
        sendErrorResponse(w, http.StatusInternalServerError, ErrCodeInternalError, "Database connection failed")
        return
    }

    // Get existing resource
    docRef := firestoreClient.Collection("resources").Doc(resourceID)
    doc, err := docRef.Get(ctx)
    if err != nil {
        if status.Code(err) == codes.NotFound {
            sendErrorResponse(w, http.StatusNotFound, ErrCodeResourceNotFound, "Resource not found")
            return
        }
        sendErrorResponse(w, http.StatusInternalServerError, ErrCodeInternalError, "Failed to fetch resource")
        return
    }

    var resource models.Resource
    if err := doc.DataTo(&resource); err != nil {
        sendErrorResponse(w, http.StatusInternalServerError, ErrCodeInternalError, "Failed to parse resource")
        return
    }

    // Check ownership
    if resource.UserID != userID {
        sendErrorResponse(w, http.StatusNotFound, ErrCodeResourceNotFound, "Resource not found")
        return
    }

    // Update fields
    updates := []firestore.Update{
        {Path: "updatedAt", Value: time.Now()},
    }

    if req.Title != "" {
        updates = append(updates, firestore.Update{Path: "title", Value: req.Title})
    }
    if req.Description != "" {
        updates = append(updates, firestore.Update{Path: "description", Value: req.Description})
    }

    _, err = docRef.Update(ctx, updates)
    if err != nil {
        sendErrorResponse(w, http.StatusInternalServerError, ErrCodeInternalError, "Failed to update resource")
        return
    }

    appLogger.Info("resource_updated",
        slog.String("resource_id", resourceID),
        slog.String("user_id", userID),
    )

    JSONSuccess(w, map[string]string{"message": "Resource updated"})
}

// deleteResource handles DELETE /api/resources/{id}
func deleteResource(w http.ResponseWriter, r *http.Request, resourceID string) {
    ctx := r.Context()

    userID := middleware.GetUserID(ctx)
    if userID == "" {
        sendErrorResponse(w, http.StatusUnauthorized, ErrCodeUnauthorized, "User not authenticated")
        return
    }

    firestoreClient, err := firebase.GetFirestoreClient(ctx)
    if err != nil {
        sendErrorResponse(w, http.StatusInternalServerError, ErrCodeInternalError, "Database connection failed")
        return
    }

    docRef := firestoreClient.Collection("resources").Doc(resourceID)
    doc, err := docRef.Get(ctx)
    if err != nil {
        if status.Code(err) == codes.NotFound {
            sendErrorResponse(w, http.StatusNotFound, ErrCodeResourceNotFound, "Resource not found")
            return
        }
        sendErrorResponse(w, http.StatusInternalServerError, ErrCodeInternalError, "Failed to fetch resource")
        return
    }

    var resource models.Resource
    if err := doc.DataTo(&resource); err != nil {
        sendErrorResponse(w, http.StatusInternalServerError, ErrCodeInternalError, "Failed to parse resource")
        return
    }

    // Check ownership
    if resource.UserID != userID {
        sendErrorResponse(w, http.StatusNotFound, ErrCodeResourceNotFound, "Resource not found")
        return
    }

    _, err = docRef.Delete(ctx)
    if err != nil {
        sendErrorResponse(w, http.StatusInternalServerError, ErrCodeInternalError, "Failed to delete resource")
        return
    }

    appLogger.Info("resource_deleted",
        slog.String("resource_id", resourceID),
        slog.String("user_id", userID),
    )

    w.WriteHeader(http.StatusNoContent)
}

// =============================================================================
// Helpers
// =============================================================================

func extractResourceID(path, prefix string) string {
    if !strings.HasPrefix(path, prefix) {
        return ""
    }
    id := strings.TrimPrefix(path, prefix)
    // Remove trailing slashes and any sub-paths
    if idx := strings.Index(id, "/"); idx != -1 {
        id = id[:idx]
    }
    return strings.TrimSpace(id)
}
```

## Model Template

If needed, create `backend/internal/models/resource.go`:

```go
package models

import "time"

// Resource represents a user-created resource
type Resource struct {
    ID          string    `json:"id" firestore:"id"`
    Title       string    `json:"title" firestore:"title"`
    Description string    `json:"description,omitempty" firestore:"description,omitempty"`
    UserID      string    `json:"userId" firestore:"userId"`
    CreatedAt   time.Time `json:"createdAt" firestore:"createdAt"`
    UpdatedAt   time.Time `json:"updatedAt" firestore:"updatedAt"`
}
```

## Route Registration

Add to `backend/cmd/server/main.go`:

```go
// In main() after other route registrations:
mux.Handle("/api/resources", middleware.Auth(http.HandlerFunc(handlers.ResourcesHandler)))
mux.Handle("/api/resources/", middleware.Auth(http.HandlerFunc(handlers.ResourcesHandler)))
```

## Test File Template

See test-generator skill for full Go test template. Key sections:

1. Method validation tests
2. Authentication tests
3. Input validation tests
4. Success cases
5. Edge cases
6. Authorization (ownership) tests

## Checklist Before Completing

- [ ] Handler file created with proper structure
- [ ] Request/response types defined
- [ ] Error codes defined/reused
- [ ] Input validation implemented
- [ ] Ownership checks for user resources
- [ ] Structured logging added
- [ ] Test file created
- [ ] Route registered in main.go
- [ ] Run verification:
  ```bash
  cd backend && gofmt -w . && go vet ./... && go test ./...
  ```

## When to Use

- When adding new API endpoints
- When creating CRUD operations for a resource
- When building authenticated endpoints
- When integrating with Firestore
