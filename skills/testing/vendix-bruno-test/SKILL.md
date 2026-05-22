---
name: vendix-bruno-test
description: >
  Patterns for Bruno API testing in Vendix.
  Trigger: When creating API tests, editing .bru files, or verifying endpoints.
license: Apache-2.0
metadata:
  author: vendix-bot
  version: "1.1"
  scope: [root]
  auto_invoke: "Creating API tests (Bruno)"
---

## When to Use

Use this skill when:

- Creating new API endpoints that need testing.
- Debugging existing API flows.
- Adding integration tests in Bruno.
- Structuring new Bruno collections or folders.

## Critical Patterns

### Pattern 1: File Structure & Naming

Organize tests hierarchically matching the API domain structure:
`bruno/Vendix/<Domain>/<Resource>/<Action Name>.bru`

- **Domain**: Broad area (e.g., `SuperAdmin`, `Organization`, `Store`).
- **Resource**: Entity being manipulated (e.g., `Users`, `Products`).
- **Action**: Human-readable name (e.g., `Create User`, `Get All Products`).

### Pattern 2: Authentication

- **Default**: Use `auth: inherit` for most endpoints.
- **Config**: The collection (`collection.bru`) handles Bearer auth using `{{token}}`.
- **Login**: Only login endpoints should set `auth: none` and capture the token.

### Pattern 3: Standard Assertions

Every test MUST include these standard assertions in the `tests` block:

```javascript
test("Operation successful", function () {
  expect(res.status).to.equal(200); // or 201
  expect(res.body.success).to.be.true;
});

test("Data structure is valid", function () {
  expect(res.body).to.have.property("data");
  // Check specific fields
  expect(res.body.data).to.have.property("id");
});
```

### Pattern 4: Variable Chaining

Capture created IDs to use in subsequent requests (e.g., Delete or Update).

```bru
vars:post-response {
  created_user_id: res.body.data.id
}
```

### Pattern 5: DTO Alignment (CRITICAL)

When creating tests, **ALWAYS** inspect the backend DTO (`*.dto.ts`) to ensure the request body matches exactly:

- Field names (snake_case vs camelCase).
- Required fields (vs optional).
- Data types (string, number, boolean).
- Validation rules (min/max length, regex).

**Example Check:**
If DTO has `@IsString() @IsNotEmpty() organization_name: string;`, the Bruno body MUST include `"organization_name": "Value"`.

## Code Examples

### Example 1: Standard Create Request (`Create User.bru`)

```bru
meta {
  name: Create User
  type: http
  seq: 1
}

post {
  url: http://{{url}}/admin/users
  body: json
  auth: inherit
}

body:json {
  {
    "email": "test@example.com",
    "password": "Password123!",
    "name": "Test User"
  }
}

vars:post-response {
  user_id: res.body.data.id
}

tests {
  test("Create successful", function() {
    expect(res.status).to.equal(201);
    expect(res.body.success).to.be.true;
  });

  test("No sensitive data", function() {
    expect(res.body.data).to.not.have.property('password');
  });
}
```

### Example 2: Login & Token Capture (`Login.bru`)

```bru
script:post-response {
  // Set global token for next requests
  bru.setVar("token", res.body.data.access_token);
}
```

## Commands

```bash
# Run collection from CLI (if bruno-cli is installed)
bru run bruno/Vendix

# Run specific folder
bru run bruno/Vendix/SuperAdmin/Users
```
