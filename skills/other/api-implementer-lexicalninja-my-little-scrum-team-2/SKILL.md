---
name: api-implementer
description: Implements API endpoints, routes, controllers, and request/response handling. Use when implementing REST APIs, GraphQL APIs, or other API endpoints. Handles routing, validation, error handling, and response formatting.
---

# API Implementer Skill

## Instructions

1. Analyze API requirements from task
2. Review API specifications (endpoints, request/response formats)
3. Implement API endpoints with proper routing
4. Add request validation
5. Implement error handling
6. Format responses correctly
7. Return implementation with:
   - Route definitions
   - Controller/handler functions
   - Validation logic
   - Error handling
   - Response formatting

## Examples

**Input:** "Implement POST /api/tasks endpoint"
**Output:**
```javascript
// routes/tasks.js
router.post('/api/tasks', authenticate, validateTaskInput, async (req, res) => {
    try {
        const task = await createTask({
            title: req.body.title,
            description: req.body.description,
            userId: req.user.id
        });
        res.status(201).json(task);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});

// middleware/validation.js
function validateTaskInput(req, res, next) {
    if (!req.body.title || req.body.title.trim().length === 0) {
        return res.status(400).json({ error: 'Title is required' });
    }
    if (req.body.title.length > 255) {
        return res.status(400).json({ error: 'Title must be 255 characters or less' });
    }
    next();
}
```

## API Implementation Areas

- **Route Definition**: HTTP method, path, middleware
- **Request Handling**: Parse request body, query params, headers
- **Validation**: Input validation, data sanitization
- **Business Logic**: Core functionality implementation
- **Error Handling**: Proper error responses, status codes
- **Response Formatting**: Consistent response structure
- **Authentication**: Auth middleware, token validation
- **Authorization**: Permission checks, role-based access

## Best Practices

- **RESTful Design**: Follow REST conventions
- **Consistent Responses**: Standard response format
- **Proper Status Codes**: Use appropriate HTTP status codes
- **Error Handling**: Comprehensive error handling
- **Validation**: Validate all inputs
- **Documentation**: Document endpoints and parameters
