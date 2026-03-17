---
name: template-code-generator
description: "Generate boilerplate code and project templates/skeletons automatically. Use when: (1) Creating new projects from scratch (React app, FastAPI backend, Express API), (2) Generating repetitive code patterns (CRUD endpoints, models, controllers), (3) Scaffolding components, services, or modules, (4) Creating test boilerplate, (5) Setting up monorepo structures. Provides project templates and code generation patterns for common development tasks."
---

# Template Code Generator

Generate boilerplate code and complete project skeletons automatically, accelerating development with battle-tested templates.

## Quick Start

### Generate Complete Projects

**React Application**:
```bash
# Use assets/react-app as template base
# Includes: Vite, TypeScript, React Router, standard structure
```

**FastAPI Backend**:
```bash
# Complete API structure with:
# - Route organization
# - CRUD patterns
# - Database models
# - Pydantic schemas
```

**Express/TypeScript API**:
```bash
# Production-ready structure:
# - Controllers/Services pattern
# - Middleware setup
# - Error handling
# - Type safety
```

See **[template_patterns.md](references/template_patterns.md)** for complete project structures.

### Generate Code Patterns

**CRUD Endpoints**:
```typescript
// Generates complete REST endpoints with validation
router.get('/', controller.getAll);
router.post('/', validate(schema), controller.create);
router.put('/:id', validate(schema), controller.update);
router.delete('/:id', controller.delete);
```

**React Components**:
```typescript
// Functional component with TypeScript props
export const ComponentName: React.FC<Props> = ({ prop1, prop2 }) => {
  return <div>{/* content */}</div>;
};
```

See **[code_patterns.md](references/code_patterns.md)** for all code generation patterns.

## Project Templates

### Web Applications

**React/TypeScript SPA**
- Vite build system
- React Router setup
- Custom hooks (useFetch, useAuth)
- Component structure (common, layout, pages)
- Type-safe API client
- Environment configuration

**Full-Stack Monorepo**
- Turborepo setup
- Frontend (React) + Backend (Express/FastAPI)
- Shared packages (types, utils, UI components)
- Coordinated build pipeline

### Backend Services

**FastAPI Application**
- Modular API structure (v1 routing)
- CRUD base classes
- Pydantic schemas
- Database models (SQLAlchemy/Prisma)
- Dependency injection
- Authentication/Authorization setup

**Express/TypeScript API**
- MVC architecture
- Service layer pattern
- Middleware (auth, validation, error handling)
- TypeORM/Prisma integration
- Request/response typing

### CLI Tools

**Python CLI (Click)**
- Command structure
- Subcommands pattern
- Configuration management
- Progress indicators
- Installation via setuptools

## Code Generation Patterns

### Classes and Models

**TypeScript Interface + Class**:
```typescript
interface User {
  id: number;
  email: string;
  name: string;
}

class UserModel implements User {
  constructor(
    public id: number,
    public email: string,
    public name: string
  ) {}

  toJSON(): User {
    return { id: this.id, email: this.email, name: this.name };
  }
}
```

**Python Dataclass**:
```python
@dataclass
class User:
    id: int
    email: str
    name: str
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return asdict(self)
```

### API Endpoints

**REST CRUD (Express)**:
```typescript
class UserController {
  async getAll(req: Request, res: Response) {
    const users = await userService.findAll();
    res.json(users);
  }

  async create(req: Request, res: Response) {
    const user = await userService.create(req.body);
    res.status(201).json(user);
  }

  // ... getById, update, delete
}
```

**FastAPI Endpoints**:
```python
@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_user.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=User)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create(db, obj_in=user_in)
```

### Components

**React Functional Component**:
```typescript
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
}

export const Button: React.FC<ButtonProps> = ({ label, onClick, variant = 'primary' }) => {
  return (
    <button className={`btn btn-${variant}`} onClick={onClick}>
      {label}
    </button>
  );
};
```

**Custom Hook**:
```typescript
function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}
```

### Tests

**Jest Test Suite**:
```typescript
describe('UserService', () => {
  it('should create user', async () => {
    const userData = { email: 'test@example.com', name: 'Test' };
    const user = await userService.create(userData);
    expect(user.email).toBe(userData.email);
  });

  it('should throw on duplicate email', async () => {
    await expect(userService.create({ email: 'existing@test.com' }))
      .rejects.toThrow();
  });
});
```

**Pytest Suite**:
```python
class TestUserService:
    def test_create_user(self, db_session):
        user_data = UserCreate(email="test@example.com", name="Test")
        user = crud_user.create(db_session, obj_in=user_data)
        assert user.email == user_data.email

    def test_duplicate_email_raises_error(self, db_session):
        with pytest.raises(ValueError):
            crud_user.create(db_session, obj_in=duplicate_data)
```

## Generation Workflow

### 1. Identify Need

Determine what to generate:
- **Complete project**: Use project templates
- **Specific pattern**: Use code generators
- **Boilerplate**: Combine templates + patterns

### 2. Select Template/Pattern

Choose appropriate template:
- **Frontend**: React app template
- **Backend**: FastAPI or Express template
- **Full-stack**: Monorepo template
- **Code**: Specific pattern (CRUD, component, test)

### 3. Customize

Adapt template to requirements:
- Replace placeholder names
- Add/remove features
- Configure dependencies
- Update structure

### 4. Generate

Create the code:
- Copy template structure
- Generate code patterns
- Fill in details
- Add configurations

### 5. Verify

Check generated code:
- Syntax correctness
- Type safety
- Dependencies installed
- Tests passing

## Best Practices

### 1. Follow Project Conventions

Match existing code style:
```typescript
// Match naming: camelCase, PascalCase, snake_case
// Match structure: file organization, folder naming
// Match patterns: error handling, validation
```

### 2. Include Type Safety

Add type annotations:
```typescript
// TypeScript
interface Props { ... }
function component(props: Props): JSX.Element { ... }

// Python
def function(param: str) -> dict[str, Any]: ...
```

### 3. Generate Tests Alongside Code

Create test boilerplate with implementation:
```
src/
  services/userService.ts
tests/
  services/userService.test.ts
```

### 4. Use Consistent Patterns

Apply same patterns across codebase:
- Error handling approach
- Validation strategy
- Naming conventions
- File structure

### 5. Document Generated Code

Add comments explaining:
```typescript
/**
 * UserService handles all user-related operations.
 * Uses repository pattern for data access.
 */
export class UserService {
  // Implementation
}
```

## Common Scenarios

### Scenario 1: New React Component

**Request**: "Create a UserCard component that displays user info"

**Generate**:
```typescript
interface UserCardProps {
  user: {
    name: string;
    email: string;
    avatar?: string;
  };
  onEdit?: () => void;
}

export const UserCard: React.FC<UserCardProps> = ({ user, onEdit }) => {
  return (
    <div className="user-card">
      {user.avatar && <img src={user.avatar} alt={user.name} />}
      <h3>{user.name}</h3>
      <p>{user.email}</p>
      {onEdit && <button onClick={onEdit}>Edit</button>}
    </div>
  );
};
```

### Scenario 2: CRUD Endpoints

**Request**: "Generate CRUD endpoints for Product model"

**Generate**:
- Routes file with all endpoints
- Controller with CRUD methods
- Service layer implementation
- Validation schemas
- Test suite

### Scenario 3: New Project

**Request**: "Create a new FastAPI backend with PostgreSQL"

**Generate**:
- Complete project structure
- Database configuration
- Initial models and schemas
- CRUD base classes
- Authentication setup
- Docker configuration
- Tests setup

## Reference Documentation

### Project Templates
See **[template_patterns.md](references/template_patterns.md)** for:
- React/TypeScript Application
- FastAPI Backend
- Express/TypeScript API
- Python CLI Tool
- Full-Stack Monorepo
- Complete file structures and core files

### Code Patterns
See **[code_patterns.md](references/code_patterns.md)** for:
- Class generators (TypeScript, Python)
- API endpoint patterns (REST, GraphQL)
- Component generators (React, Vue)
- Test generators (Jest, pytest)
- Database models (TypeORM, SQLAlchemy)
- Service classes
- Middleware patterns
- Validation schemas (Zod, Pydantic)
