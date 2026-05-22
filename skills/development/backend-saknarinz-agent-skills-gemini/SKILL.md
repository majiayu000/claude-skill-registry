---
name: Backend Development
description: พัฒนา Backend ด้วย Spring Boot, Node.js, Python อย่างมืออาชีพ
---

# Backend Development Skill

## Overview

Skill สำหรับพัฒนา Backend applications ครอบคลุม 3 tech stacks หลัก พร้อม best practices

---

## Spring Boot (Java/Kotlin)

### Project Structure

```
src/main/java/com/example/myapp/
├── config/              # Configuration classes
│   ├── SecurityConfig.java
│   └── WebConfig.java
├── controller/          # REST Controllers
│   └── UserController.java
├── service/             # Business logic
│   ├── UserService.java
│   └── impl/
│       └── UserServiceImpl.java
├── repository/          # Data access
│   └── UserRepository.java
├── model/               # JPA Entities
│   └── User.java
├── dto/                 # Data Transfer Objects
│   ├── request/
│   └── response/
├── exception/           # Custom exceptions
│   └── GlobalExceptionHandler.java
└── MyApplication.java
```

### Best Practices

#### Controller

```java
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    @GetMapping
    public ResponseEntity<List<UserResponse>> getUsers() {
        return ResponseEntity.ok(userService.findAll());
    }

    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
        return ResponseEntity.ok(userService.findById(id));
    }

    @PostMapping
    public ResponseEntity<UserResponse> createUser(
            @Valid @RequestBody CreateUserRequest request) {
        return ResponseEntity
            .status(HttpStatus.CREATED)
            .body(userService.create(request));
    }
}
```

#### Service

```java
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final UserMapper userMapper;

    @Override
    public UserResponse findById(Long id) {
        return userRepository.findById(id)
            .map(userMapper::toResponse)
            .orElseThrow(() -> new ResourceNotFoundException("User", id));
    }

    @Override
    @Transactional
    public UserResponse create(CreateUserRequest request) {
        User user = userMapper.toEntity(request);
        return userMapper.toResponse(userRepository.save(user));
    }
}
```

#### Exception Handling

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex) {
        return ResponseEntity
            .status(HttpStatus.NOT_FOUND)
            .body(new ErrorResponse(ex.getMessage()));
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex) {
        List<String> errors = ex.getBindingResult()
            .getFieldErrors()
            .stream()
            .map(e -> e.getField() + ": " + e.getDefaultMessage())
            .toList();
        return ResponseEntity
            .badRequest()
            .body(new ErrorResponse("Validation failed", errors));
    }
}
```

---

## Node.js (Express/NestJS)

### Express + TypeScript Structure

```
src/
├── config/
│   └── index.ts
├── controllers/
│   └── user.controller.ts
├── services/
│   └── user.service.ts
├── repositories/
│   └── user.repository.ts
├── models/
│   └── user.model.ts
├── middlewares/
│   ├── auth.middleware.ts
│   └── error.middleware.ts
├── routes/
│   ├── user.routes.ts
│   └── index.ts
├── utils/
│   └── errors.ts
└── index.ts
```

### Best Practices

#### Controller

```typescript
// user.controller.ts
export class UserController {
  constructor(private userService: UserService) {}

  getUsers = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const users = await this.userService.findAll();
      res.json(users);
    } catch (error) {
      next(error);
    }
  };

  createUser = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const user = await this.userService.create(req.body);
      res.status(201).json(user);
    } catch (error) {
      next(error);
    }
  };
}
```

#### Error Middleware

```typescript
// error.middleware.ts
export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction,
) {
  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      message: error.message,
      errors: error.errors,
    });
  }

  console.error(error);
  res.status(500).json({ message: "Internal server error" });
}
```

### NestJS Structure

```
src/
├── modules/
│   ├── users/
│   │   ├── users.controller.ts
│   │   ├── users.service.ts
│   │   ├── users.module.ts
│   │   ├── dto/
│   │   └── entities/
│   └── auth/
├── common/
│   ├── filters/
│   ├── guards/
│   └── interceptors/
└── main.ts
```

---

## Python (FastAPI/Django)

### FastAPI Structure

```
app/
├── api/
│   ├── v1/
│   │   ├── endpoints/
│   │   │   └── users.py
│   │   └── router.py
│   └── deps.py          # Dependencies
├── core/
│   ├── config.py
│   └── security.py
├── models/
│   └── user.py
├── schemas/
│   └── user.py
├── services/
│   └── user.py
├── db/
│   ├── base.py
│   └── session.py
└── main.py
```

### Best Practices

#### Router

```python
# api/v1/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return user_service.get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = user_service.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    return user_service.create_user(db, user_in)
```

#### Schema (Pydantic)

```python
# schemas/user.py
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
```

---

## API Design Best Practices

### RESTful Conventions

| Action | HTTP Method | Endpoint       | Status Code |
| ------ | ----------- | -------------- | ----------- |
| List   | GET         | /api/users     | 200         |
| Get    | GET         | /api/users/:id | 200         |
| Create | POST        | /api/users     | 201         |
| Update | PUT         | /api/users/:id | 200         |
| Patch  | PATCH       | /api/users/:id | 200         |
| Delete | DELETE      | /api/users/:id | 204         |

### Response Format

```json
// Success
{
  "data": { ... },
  "meta": {
    "page": 1,
    "limit": 10,
    "total": 100
  }
}

// Error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      { "field": "email", "message": "Invalid email format" }
    ]
  }
}
```

---

## Backend Checklist

- [ ] Clear project structure
- [ ] Input validation
- [ ] Proper error handling
- [ ] Authentication/Authorization
- [ ] Database transactions
- [ ] Logging
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Rate limiting
- [ ] CORS configuration
- [ ] Environment configuration
- [ ] Unit tests
- [ ] Integration tests
