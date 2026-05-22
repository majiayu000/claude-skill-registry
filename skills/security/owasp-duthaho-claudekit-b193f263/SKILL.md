# OWASP Security

## Description

OWASP Top 10 security practices and secure coding patterns.

## When to Use

- Security code reviews
- Implementing authentication
- Handling user input

---

## Core Patterns

### Input Validation

```python
# Always validate and sanitize
from pydantic import BaseModel, EmailStr

class UserInput(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
```

### SQL Injection Prevention

```python
# Never concatenate user input
# Bad
query = f"SELECT * FROM users WHERE id = {user_id}"

# Good - parameterized
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### XSS Prevention

```typescript
// Never use innerHTML with user data
// Bad
element.innerHTML = userInput;

// Good
element.textContent = userInput;
```

### Authentication

```python
# Hash passwords properly
from passlib.hash import argon2

hashed = argon2.hash(password)
verified = argon2.verify(password, hashed)
```

## Security Checklist

- [ ] Input validation on all user data
- [ ] Parameterized queries
- [ ] Output encoding
- [ ] Strong password hashing
- [ ] Secure session management
- [ ] HTTPS everywhere
- [ ] Security headers configured

## Common Pitfalls

- **Trusting user input**: Always validate
- **SQL concatenation**: Use parameters
- **Storing plain passwords**: Use argon2/bcrypt
