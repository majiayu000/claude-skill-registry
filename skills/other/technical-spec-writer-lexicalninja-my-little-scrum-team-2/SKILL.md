---
name: technical-spec-writer
description: Creates detailed technical specifications including architecture, data models, APIs, and technology choices. Use when you need to document technical implementation details, system design, or API contracts. Provides concrete technical guidance for implementation.
---

# Technical Specification Writer Skill

## Instructions

1. Analyze requirements and determine technical approach
2. Design system architecture and components
3. Define data models and schemas
4. Specify API contracts (endpoints, request/response formats)
5. Identify technology stack and libraries
6. Document integration points and interfaces
7. Define configuration and deployment requirements
8. Include code examples and patterns when helpful

## Examples

**Input:** "User authentication system"
**Output:**
```markdown
## Technical Specifications

### Architecture
- **Pattern**: RESTful API with JWT authentication
- **Framework**: Express.js (Node.js)
- **Database**: PostgreSQL with Prisma ORM
- **Authentication**: JWT tokens stored in HTTP-only cookies

### Data Models

#### User Model
```typescript
{
  id: string (UUID, primary key)
  email: string (unique, indexed)
  passwordHash: string (bcrypt, 60 chars)
  createdAt: DateTime
  updatedAt: DateTime
  emailVerified: boolean
}
```

#### PasswordResetToken Model
```typescript
{
  id: string (UUID, primary key)
  userId: string (foreign key -> User.id)
  token: string (random 32-char hex, indexed)
  expiresAt: DateTime
  used: boolean
  createdAt: DateTime
}
```

### API Endpoints

#### POST /api/auth/register
**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (201):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "emailVerified": false
  }
}
```

**Errors:**
- 400: Invalid email format or weak password
- 409: Email already exists

#### POST /api/auth/login
**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com"
  },
  "token": "jwt.token.here"
}
```

**Errors:**
- 401: Invalid credentials

### Technology Stack
- **Runtime**: Node.js 18+
- **Framework**: Express.js 4.x
- **Database**: PostgreSQL 14+
- **ORM**: Prisma 5.x
- **Authentication**: jsonwebtoken, bcrypt
- **Validation**: zod
- **Testing**: Jest, Supertest

### Security Considerations
- Passwords hashed with bcrypt (10+ rounds)
- JWT tokens expire after 24 hours
- Password reset tokens expire after 1 hour
- Rate limiting: 5 requests/minute for auth endpoints
- CORS configured for specific origins only
```

## Format Guidelines

- Use clear section headers
- Include code examples for data models and APIs
- Specify exact versions for libraries when important
- Document error responses and status codes
- Include security and performance considerations
- Use standard formats (OpenAPI for APIs, ERD for data models)
