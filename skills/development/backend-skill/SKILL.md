---
name: backend-skill
description: Build backend application logic including route generation, request/response handling, and database connectivity. Use for server-side development.
---

# Backend Skill – API Routes & Data Handling

## Instructions

1. **Route Generation**
   - Define clear and consistent API routes
   - Follow RESTful conventions
   - Organize routes by domain or feature

2. **Request & Response Handling**
   - Validate incoming requests
   - Structure consistent response formats
   - Handle errors and edge cases safely

3. **Database Connection**
   - Connect to databases using reliable drivers or ORMs
   - Manage transactions properly
   - Handle connection lifecycle and pooling

4. **Business Logic**
   - Separate business logic from routing
   - Keep handlers small and readable
   - Reuse shared services and utilities

## Best Practices
- Use clear naming conventions
- Validate all inputs and outputs
- Keep routes thin and logic modular
- Handle errors consistently
- Follow backend framework best practices

## Example Structure
```ts
app.post("/users", async (req, res) => {
  const user = await db.user.create(req.body);
  res.status(201).json(user);
});
