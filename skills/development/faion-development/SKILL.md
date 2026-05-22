---
name: faion-development
description: "Development orchestrator: Python, JS/TS, backend languages, DevOps, documentation. Merges dev-django + dev-ui-design + dev-docs. 68 methodologies."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---

# Development Domain Skill

**Communication: User's language. Code: English.**

## Purpose

Orchestrates all development activities from coding to deployment. Covers Python ecosystem, JavaScript/TypeScript, backend languages, DevOps/Infrastructure, and documentation.

## Merged From

| Original Skill | Content |
|----------------|---------|
| faion-dev-django-skill | Django coding standards, patterns |
| faion-dev-frontend-skill | UI brainstorming, Storybook, components |
| faion-dev-docs-skill | CLAUDE.md documentation creation |

---

## Agents

| Agent | Purpose | Skills Used |
|-------|---------|-------------|
| faion-code-agent | Code generation & review | faion-python-skill, faion-javascript-skill, faion-backend-skill |
| faion-test-agent | Test generation & execution | faion-testing-skill |
| faion-devops-agent | CI/CD, infrastructure | faion-aws-cli-skill, faion-k8s-cli-skill, faion-terraform-skill, faion-docker-skill |
| faion-frontend-brainstormer-agent | Generate 3-5 design variants | - |
| faion-storybook-agent | Setup/maintain Storybook | - |
| faion-frontend-component-agent | Develop components with stories | - |

---

## Workflows

### Workflow 1: Backend Development

```
Requirements → Design → Code → Test → Review → Deploy
```

### Workflow 2: UI Development

```
Requirements → Brainstorm (3-5 variants) → User selects → Refine → Storybook → Components
```

### Workflow 3: Documentation

```
Analyze Folder → Identify Type → Write CLAUDE.md → Verify
```

---

## Methodologies (68)

### Python Ecosystem (8)

#### M-DEV-001: Django Coding Standards

**Problem:** Inconsistent Django code across projects.

**Framework:**

1. **Import Style:**
```python
# Cross-app imports - ALWAYS with alias
from apps.orders import models as order_models
from apps.users import services as user_services

# Own modules (relative)
from .models import User
from . import constants
```

2. **Services = Functions:**
```python
# services/activation.py
def activate_user_item(
    user: User,
    item_code: str,
    *,
    activated_by: Admin,
) -> Item:
    """Activate item for user."""
    item = Item.objects.get(code=item_code)
    item.user = user
    item.is_active = True
    item.save(update_fields=['user', 'is_active', 'updated_at'])
    return item
```

3. **Multi-line Parameters:**
```python
def create_order(
    user: User,
    amount: Decimal,
    order_type: str,
    *,  # Keyword-only after
    item: Item | None = None,
    notify: bool = True,
) -> Order:
    ...
```

4. **Thin Views:**
```python
class ItemActivationView(APIView):
    def post(self, request):
        serializer = ItemActivationRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = services.activate_user_item(
            user=request.user,
            item_code=serializer.validated_data['item_code'],
        )
        return Response(ItemResponse(item).data)
```

**Agent:** faion-code-agent

#### M-DEV-002: Django Code Decision Tree

**Problem:** Unclear where to put code.

**Framework:**
```
What does the function do?
│
├─ Changes DB (CREATE/UPDATE/DELETE)?
│  └─ services/
├─ Makes external API calls?
│  └─ services/ or integrations/
├─ Pure function (validation, calculation)?
│  └─ utils/
└─ Data transformation?
   └─ utils/
```

**Agent:** faion-code-agent

#### M-DEV-003: Django Base Model Pattern

**Problem:** Missing standard fields on models.

**Framework:**
```python
class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

**Agent:** faion-code-agent

#### M-DEV-004: Django Testing with pytest

**Problem:** Inconsistent test patterns.

**Framework:**
```python
@pytest.mark.django_db
def test_activate_item_success(user, item):
    result = services.activate_user_item(
        user=user,
        item_code=item.code,
    )
    assert result.is_active is True
    assert result.user == user
```

**Agent:** faion-test-agent

#### M-DEV-005: FastAPI Standards

**Problem:** Inconsistent FastAPI patterns.

**Framework:**
```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ItemCreate(BaseModel):
    name: str
    price: float

@app.post("/items/", response_model=ItemResponse)
async def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await services.create_item(db, item, current_user)
```

**Agent:** faion-code-agent

#### M-DEV-006: Python Project Structure

**Problem:** No standard project layout.

**Framework:**
```
project/
├── pyproject.toml
├── src/
│   └── package/
│       ├── __init__.py
│       ├── main.py
│       └── models/
├── tests/
│   ├── conftest.py
│   └── test_*.py
├── .env.example
└── README.md
```

**Agent:** faion-code-agent

#### M-DEV-007: Python Type Hints

**Problem:** Unclear function signatures.

**Framework:**
```python
from typing import Optional, List, Dict

def process_users(
    users: List[User],
    options: Optional[Dict[str, str]] = None,
) -> List[ProcessedUser]:
    ...
```

**Agent:** faion-code-agent

#### M-DEV-008: Python Dependency Management

**Problem:** Dependency conflicts, no lockfile.

**Framework:**
- Use `pyproject.toml` for project config
- Use `poetry` or `uv` for dependency management
- Lock dependencies: `poetry.lock` or `uv.lock`
- Separate dev dependencies

**Agent:** faion-code-agent

### JavaScript/TypeScript Ecosystem (8)

#### M-DEV-009: React Component Pattern

**Problem:** Inconsistent component structure.

**Framework:**
```typescript
// src/components/Button/Button.tsx
interface ButtonProps {
  variant: 'primary' | 'secondary';
  children: React.ReactNode;
  onClick?: () => void;
}

export const Button: React.FC<ButtonProps> = ({
  variant,
  children,
  onClick,
}) => {
  return (
    <button className={styles[variant]} onClick={onClick}>
      {children}
    </button>
  );
};
```

**Agent:** faion-code-agent

#### M-DEV-010: React Hooks Pattern

**Problem:** Logic duplicated across components.

**Framework:**
```typescript
// hooks/useUser.ts
export function useUser(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetchUser(userId)
      .then(setUser)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [userId]);

  return { user, loading, error };
}
```

**Agent:** faion-code-agent

#### M-DEV-011: TypeScript Strict Mode

**Problem:** Type errors caught too late.

**Framework:**
```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

**Agent:** faion-code-agent

#### M-DEV-012: Node.js Project Structure

**Problem:** No standard layout for Node.js.

**Framework:**
```
project/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts
│   ├── routes/
│   ├── services/
│   └── models/
├── tests/
│   └── *.test.ts
└── .env.example
```

**Agent:** faion-code-agent

#### M-DEV-013: Next.js App Router Pattern

**Problem:** Unclear Next.js 13+ patterns.

**Framework:**
```
app/
├── layout.tsx       # Root layout
├── page.tsx         # Home page
├── (auth)/
│   ├── login/
│   │   └── page.tsx
│   └── register/
│       └── page.tsx
├── dashboard/
│   ├── layout.tsx   # Dashboard layout
│   └── page.tsx
└── api/
    └── users/
        └── route.ts
```

**Agent:** faion-code-agent

#### M-DEV-014: Frontend State Management

**Problem:** State scattered across components.

**Framework:**
| Solution | Use Case |
|----------|----------|
| useState | Local component state |
| useContext | Shared state (theme, auth) |
| Zustand | Medium complexity |
| Redux Toolkit | Large apps, time-travel debugging |
| TanStack Query | Server state caching |

**Agent:** faion-code-agent

#### M-DEV-015: CSS Architecture

**Problem:** Unorganized styles.

**Framework:**
| Approach | Use Case |
|----------|----------|
| CSS Modules | Component isolation |
| Tailwind CSS | Rapid prototyping |
| styled-components | CSS-in-JS, dynamic styles |
| SCSS + BEM | Large traditional projects |

**Agent:** faion-code-agent

#### M-DEV-016: Frontend Testing

**Problem:** No test strategy.

**Framework:**
```typescript
// Component test with Testing Library
import { render, screen } from '@testing-library/react';
import { Button } from './Button';

test('renders button with text', () => {
  render(<Button variant="primary">Click me</Button>);
  expect(screen.getByText('Click me')).toBeInTheDocument();
});
```

**Agent:** faion-test-agent

### Backend Languages (24)

#### M-DEV-017: Go Project Structure

**Problem:** No standard Go layout.

**Framework:**
```
project/
├── cmd/
│   └── server/
│       └── main.go
├── internal/
│   ├── handlers/
│   ├── services/
│   └── models/
├── pkg/           # Reusable packages
├── go.mod
└── go.sum
```

**Agent:** faion-code-agent

#### M-DEV-018: Go Error Handling

**Problem:** Inconsistent error handling.

**Framework:**
```go
func GetUser(id string) (*User, error) {
    user, err := db.FindUser(id)
    if err != nil {
        return nil, fmt.Errorf("get user %s: %w", id, err)
    }
    return user, nil
}
```

**Agent:** faion-code-agent

#### M-DEV-019: Go Interface Pattern

**Problem:** Tight coupling between components.

**Framework:**
```go
// Define interface where it's used
type UserRepository interface {
    Find(id string) (*User, error)
    Save(user *User) error
}

// Implementation
type PostgresUserRepo struct {
    db *sql.DB
}

func (r *PostgresUserRepo) Find(id string) (*User, error) {
    // implementation
}
```

**Agent:** faion-code-agent

#### M-DEV-020: Go Concurrency Patterns

**Problem:** Race conditions, goroutine leaks.

**Framework:**
```go
// Worker pool pattern
func worker(jobs <-chan Job, results chan<- Result) {
    for job := range jobs {
        results <- process(job)
    }
}

func main() {
    jobs := make(chan Job, 100)
    results := make(chan Result, 100)

    for w := 1; w <= 3; w++ {
        go worker(jobs, results)
    }
}
```

**Agent:** faion-code-agent

#### M-DEV-021: Ruby on Rails Patterns

**Problem:** Fat controllers, thin models.

**Framework:**
- **Thin Controllers:** Only HTTP handling
- **Service Objects:** Business logic
- **Form Objects:** Complex validations
- **Query Objects:** Complex queries
- **Presenters:** View logic

**Agent:** faion-code-agent

#### M-DEV-022: Ruby on Rails Testing

**Problem:** Slow, flaky tests.

**Framework:**
```ruby
RSpec.describe UserService do
  describe '#create' do
    let(:params) { { name: 'John', email: 'john@example.com' } }

    it 'creates user with valid params' do
      result = described_class.create(params)
      expect(result).to be_success
    end
  end
end
```

**Agent:** faion-test-agent

#### M-DEV-023: PHP Laravel Patterns

**Problem:** Inconsistent Laravel code.

**Framework:**
```php
// Service Pattern
class UserService
{
    public function create(array $data): User
    {
        return User::create($data);
    }
}

// Controller
class UserController extends Controller
{
    public function store(CreateUserRequest $request, UserService $service)
    {
        $user = $service->create($request->validated());
        return new UserResource($user);
    }
}
```

**Agent:** faion-code-agent

#### M-DEV-024: PHP Laravel Testing

**Problem:** No test coverage.

**Framework:**
```php
class UserTest extends TestCase
{
    public function test_user_can_be_created(): void
    {
        $response = $this->postJson('/api/users', [
            'name' => 'John',
            'email' => 'john@example.com',
        ]);

        $response->assertStatus(201);
    }
}
```

**Agent:** faion-test-agent

#### M-DEV-025: Java Spring Boot Patterns

**Problem:** Inconsistent Spring code.

**Framework:**
```java
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;

    public User createUser(CreateUserDto dto) {
        User user = User.builder()
            .name(dto.getName())
            .email(dto.getEmail())
            .build();
        return userRepository.save(user);
    }
}
```

**Agent:** faion-code-agent

#### M-DEV-026: Java Spring Boot Testing

**Problem:** Complex test setup.

**Framework:**
```java
@SpringBootTest
class UserServiceTest {
    @Autowired
    private UserService userService;

    @Test
    void shouldCreateUser() {
        CreateUserDto dto = new CreateUserDto("John", "john@example.com");
        User result = userService.createUser(dto);
        assertThat(result.getName()).isEqualTo("John");
    }
}
```

**Agent:** faion-test-agent

#### M-DEV-027: C# .NET Patterns

**Problem:** Inconsistent .NET code.

**Framework:**
```csharp
public class UserService : IUserService
{
    private readonly IUserRepository _repository;

    public UserService(IUserRepository repository)
    {
        _repository = repository;
    }

    public async Task<User> CreateAsync(CreateUserDto dto)
    {
        var user = new User { Name = dto.Name, Email = dto.Email };
        return await _repository.AddAsync(user);
    }
}
```

**Agent:** faion-code-agent

#### M-DEV-028: C# .NET Testing

**Problem:** Hard to test dependencies.

**Framework:**
```csharp
public class UserServiceTests
{
    [Fact]
    public async Task CreateAsync_ShouldReturnUser()
    {
        var mockRepo = new Mock<IUserRepository>();
        var service = new UserService(mockRepo.Object);

        var result = await service.CreateAsync(new CreateUserDto("John", "john@example.com"));

        Assert.Equal("John", result.Name);
    }
}
```

**Agent:** faion-test-agent

#### M-DEV-029: Rust Project Structure

**Problem:** No standard Rust layout.

**Framework:**
```
project/
├── Cargo.toml
├── src/
│   ├── main.rs
│   ├── lib.rs
│   └── modules/
│       ├── mod.rs
│       └── user.rs
├── tests/
│   └── integration_test.rs
└── examples/
```

**Agent:** faion-code-agent

#### M-DEV-030: Rust Error Handling

**Problem:** Panic vs Result confusion.

**Framework:**
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum UserError {
    #[error("user not found: {0}")]
    NotFound(String),
    #[error("database error")]
    Database(#[from] sqlx::Error),
}

pub fn get_user(id: &str) -> Result<User, UserError> {
    db.find_user(id)
        .map_err(|e| UserError::Database(e))?
        .ok_or(UserError::NotFound(id.to_string()))
}
```

**Agent:** faion-code-agent

#### M-DEV-031: Rust Async Patterns

**Problem:** Async complexity.

**Framework:**
```rust
use tokio;

#[tokio::main]
async fn main() {
    let result = fetch_data().await;
    println!("{:?}", result);
}

async fn fetch_data() -> Result<Data, Error> {
    let response = reqwest::get("https://api.example.com/data").await?;
    response.json().await
}
```

**Agent:** faion-code-agent

#### M-DEV-032: Rust Testing

**Problem:** No test organization.

**Framework:**
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_create_user() {
        let user = User::new("John", "john@example.com");
        assert_eq!(user.name, "John");
    }

    #[tokio::test]
    async fn test_async_fetch() {
        let result = fetch_data().await;
        assert!(result.is_ok());
    }
}
```

**Agent:** faion-test-agent

#### M-DEV-033: Database Migration Patterns

**Problem:** Manual database changes.

**Framework:**
```sql
-- Up migration
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Down migration
DROP TABLE users;
```

**Agent:** faion-code-agent

#### M-DEV-034: SQL Query Optimization

**Problem:** Slow database queries.

**Framework:**
1. Add appropriate indexes
2. Use EXPLAIN ANALYZE
3. Avoid SELECT *
4. Use query pagination
5. Consider read replicas

**Agent:** faion-code-agent

#### M-DEV-035: ORM Best Practices

**Problem:** N+1 queries, memory issues.

**Framework:**
```python
# Bad: N+1 queries
users = User.objects.all()
for user in users:
    print(user.orders.count())  # New query each iteration

# Good: Prefetch
users = User.objects.prefetch_related('orders').all()
for user in users:
    print(len(user.orders.all()))  # Uses prefetched data
```

**Agent:** faion-code-agent

#### M-DEV-036: API Response Patterns

**Problem:** Inconsistent API responses.

**Framework:**
```json
// Success
{
  "data": { ... },
  "meta": { "page": 1, "total": 100 }
}

// Error
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [{ "field": "email", "error": "invalid_format" }]
  }
}
```

**Agent:** faion-code-agent

#### M-DEV-037: Authentication Patterns

**Problem:** Insecure auth implementation.

**Framework:**
| Pattern | Use Case |
|---------|----------|
| JWT | Stateless API auth |
| Session | Server-side state |
| OAuth2 | Third-party login |
| API Keys | Server-to-server |

**Agent:** faion-code-agent

#### M-DEV-038: Caching Strategies

**Problem:** High database load.

**Framework:**
| Strategy | Use Case |
|----------|----------|
| Cache-aside | Read-heavy workloads |
| Write-through | Write consistency |
| Write-behind | Write performance |
| Read-through | Automatic cache population |

**Agent:** faion-code-agent

#### M-DEV-039: Queue/Background Jobs

**Problem:** Blocking operations in requests.

**Framework:**
```python
# Celery example
@celery_app.task
def send_welcome_email(user_id: int):
    user = User.objects.get(id=user_id)
    email_service.send(user.email, "Welcome!")

# Usage
send_welcome_email.delay(user.id)
```

**Agent:** faion-code-agent

#### M-DEV-040: Logging Best Practices

**Problem:** No structured logging.

**Framework:**
```python
import structlog

logger = structlog.get_logger()

logger.info(
    "user_created",
    user_id=user.id,
    email=user.email,
    source="api"
)
```

**Agent:** faion-code-agent

### DevOps & Infrastructure (28)

#### M-DEV-041: Docker Best Practices

**Problem:** Large, insecure images.

**Framework:**
```dockerfile
# Multi-stage build
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "main.py"]
```

**Agent:** faion-devops-agent

#### M-DEV-042: Docker Compose Patterns

**Problem:** Complex local environments.

**Framework:**
```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgres://postgres:postgres@db:5432/app

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

**Agent:** faion-devops-agent

#### M-DEV-043: Kubernetes Deployment

**Problem:** No standard K8s patterns.

**Framework:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      containers:
      - name: app
        image: app:latest
        ports:
        - containerPort: 8000
        resources:
          limits:
            memory: "256Mi"
            cpu: "500m"
```

**Agent:** faion-devops-agent

#### M-DEV-044: Kubernetes Service

**Problem:** Pod networking complexity.

**Framework:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: app
spec:
  selector:
    app: app
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

**Agent:** faion-devops-agent

#### M-DEV-045: Kubernetes ConfigMap/Secret

**Problem:** Hardcoded configuration.

**Framework:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  DATABASE_PASSWORD: base64encoded

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: "info"
```

**Agent:** faion-devops-agent

#### M-DEV-046: Terraform Module Structure

**Problem:** Unorganized infrastructure code.

**Framework:**
```
terraform/
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── rds/
├── environments/
│   ├── dev/
│   │   └── main.tf
│   └── prod/
│       └── main.tf
└── backend.tf
```

**Agent:** faion-devops-agent

#### M-DEV-047: Terraform State Management

**Problem:** State conflicts, lost state.

**Framework:**
```hcl
terraform {
  backend "s3" {
    bucket         = "terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

**Agent:** faion-devops-agent

#### M-DEV-048: AWS VPC Design

**Problem:** Insecure network architecture.

**Framework:**
```
VPC (10.0.0.0/16)
├── Public Subnets (10.0.1.0/24, 10.0.2.0/24)
│   └── NAT Gateway, ALB
├── Private Subnets (10.0.10.0/24, 10.0.11.0/24)
│   └── Application servers
└── Database Subnets (10.0.20.0/24, 10.0.21.0/24)
    └── RDS, ElastiCache
```

**Agent:** faion-devops-agent

#### M-DEV-049: AWS IAM Best Practices

**Problem:** Over-permissive IAM policies.

**Framework:**
1. Least privilege principle
2. Use IAM roles, not users
3. Enable MFA
4. Use service-linked roles
5. Regular access review

**Agent:** faion-devops-agent

#### M-DEV-050: CI/CD Pipeline Design

**Problem:** Manual deployments.

**Framework:**
```yaml
# GitHub Actions example
name: CI/CD
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: ./deploy.sh
```

**Agent:** faion-devops-agent

#### M-DEV-051: GitOps Pattern

**Problem:** Configuration drift.

**Framework:**
1. Git as single source of truth
2. Declarative configuration
3. Automated sync (ArgoCD, Flux)
4. Pull-based deployments

**Agent:** faion-devops-agent

#### M-DEV-052: Blue-Green Deployment

**Problem:** Downtime during deployments.

**Framework:**
```
                    ┌─────────────┐
                    │    ALB      │
                    └──────┬──────┘
                           │
              ┌────────────┴────────────┐
              │                         │
        ┌─────▼─────┐            ┌──────▼─────┐
        │   Blue    │            │   Green    │
        │  (live)   │            │   (new)    │
        └───────────┘            └────────────┘

1. Deploy to Green
2. Test Green
3. Switch ALB to Green
4. Blue becomes staging
```

**Agent:** faion-devops-agent

#### M-DEV-053: Canary Deployment

**Problem:** Risky full rollouts.

**Framework:**
```
Traffic Split:
1. 5% → New version (canary)
   95% → Old version
2. Monitor metrics
3. If OK: 25% → 50% → 100%
4. If error: rollback to 0%
```

**Agent:** faion-devops-agent

#### M-DEV-054: Infrastructure Monitoring

**Problem:** No visibility into issues.

**Framework:**
| Layer | Tools |
|-------|-------|
| Infrastructure | CloudWatch, Datadog |
| Application | APM (New Relic, Datadog) |
| Logs | ELK, Loki, CloudWatch Logs |
| Traces | Jaeger, X-Ray |

**Agent:** faion-devops-agent

#### M-DEV-055: Alerting Strategy

**Problem:** Alert fatigue or missing alerts.

**Framework:**
| Severity | Response | Example |
|----------|----------|---------|
| P1 | Immediate | Service down |
| P2 | < 1 hour | Error rate > 5% |
| P3 | < 8 hours | Disk > 80% |
| P4 | Next day | Warning conditions |

**Agent:** faion-devops-agent

#### M-DEV-056: Backup Strategy

**Problem:** Data loss risk.

**Framework:**
| Type | Frequency | Retention |
|------|-----------|-----------|
| Full | Weekly | 30 days |
| Incremental | Daily | 14 days |
| Transaction logs | Hourly | 7 days |

**Agent:** faion-devops-agent

#### M-DEV-057: Disaster Recovery

**Problem:** No recovery plan.

**Framework:**
| Metric | Target |
|--------|--------|
| RPO (Recovery Point) | < 1 hour |
| RTO (Recovery Time) | < 4 hours |

**Steps:**
1. Multi-AZ deployment
2. Cross-region backups
3. Regular DR drills
4. Runbook documentation

**Agent:** faion-devops-agent

#### M-DEV-058: Security Scanning

**Problem:** Vulnerabilities in code/deps.

**Framework:**
| Type | Tool | Frequency |
|------|------|-----------|
| SAST | SonarQube, Semgrep | Every commit |
| DAST | OWASP ZAP | Weekly |
| Dependencies | Snyk, Dependabot | Daily |
| Container | Trivy, Clair | Every build |

**Agent:** faion-devops-agent

#### M-DEV-059: Secret Management

**Problem:** Secrets in code/env files.

**Framework:**
| Tool | Use Case |
|------|----------|
| HashiCorp Vault | Enterprise |
| AWS Secrets Manager | AWS native |
| 1Password | Team credentials |
| SOPS | Git-encrypted secrets |

**Agent:** faion-devops-agent

#### M-DEV-060: Load Testing

**Problem:** Unknown capacity limits.

**Framework:**
```yaml
# k6 example
import http from 'k6/http';

export const options = {
  stages: [
    { duration: '5m', target: 100 },  // Ramp up
    { duration: '10m', target: 100 }, // Stay
    { duration: '5m', target: 0 },    // Ramp down
  ],
};

export default function () {
  http.get('https://api.example.com/');
}
```

**Agent:** faion-devops-agent

#### M-DEV-061: Nginx Configuration

**Problem:** Suboptimal web server config.

**Framework:**
```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /var/www/static/;
        expires 30d;
    }

    gzip on;
    gzip_types text/plain application/json;
}
```

**Agent:** faion-devops-agent

#### M-DEV-062: SSL/TLS Configuration

**Problem:** Insecure HTTPS setup.

**Framework:**
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;

add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

**Agent:** faion-devops-agent

#### M-DEV-063: CDN Configuration

**Problem:** Slow global content delivery.

**Framework:**
| Setting | Value |
|---------|-------|
| Cache TTL (static) | 30 days |
| Cache TTL (API) | No cache |
| Compression | Brotli, Gzip |
| HTTP/2 | Enabled |

**Agent:** faion-devops-agent

#### M-DEV-064: Database HA Setup

**Problem:** Single point of failure.

**Framework:**
```
Primary (write)
    │
    ├─► Replica 1 (read)
    └─► Replica 2 (read)

Auto-failover: Primary fails → Replica promoted
```

**Agent:** faion-devops-agent

#### M-DEV-065: CLAUDE.md Documentation

**Problem:** No AI-readable context.

**Framework:**
```markdown
# {Folder Name}

{One-sentence description}

## Overview
{2-3 sentences explaining what this folder contains}

## Structure
| Path | Purpose |
|------|---------|
| `file.py` | Description |

## Key Concepts
- **Concept1**: Explanation

## Entry Points
- `main_file.py` — Primary entry point

## Common Operations
### Operation 1
```bash
command example
```

## Dependencies
- dep1: purpose
```

**Size Guidelines:**
- Target: 100-150 lines
- Maximum: 200 lines

**Agent:** faion-code-agent

#### M-DEV-066: Storybook Setup

**Problem:** No component documentation.

**Framework:**
```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Click me',
  },
};
```

**Agent:** faion-storybook-agent

#### M-DEV-067: Design Tokens

**Problem:** Inconsistent design values.

**Framework:**
```typescript
// tokens/
export const colors = {
  primary: {
    50: '#f0f9ff',
    500: '#3b82f6',
    900: '#1e3a8a',
  },
  semantic: {
    success: '#22c55e',
    error: '#ef4444',
    warning: '#f59e0b',
  },
};

export const spacing = {
  0: '0',
  1: '0.25rem',
  2: '0.5rem',
  4: '1rem',
  8: '2rem',
};
```

**Agent:** faion-frontend-component-agent

#### M-DEV-068: Component File Structure

**Problem:** Scattered component files.

**Framework:**
```
src/components/{Name}/
├── {Name}.tsx           # Component
├── {Name}.stories.tsx   # Storybook
├── {Name}.test.tsx      # Tests
├── {Name}.module.css    # Styles
└── index.ts             # Export
```

**Agent:** faion-frontend-component-agent

---

## Execution

### Backend Development

```python
Task(subagent_type="faion-code-agent",
     prompt=f"Implement {feature} using {framework}")

Task(subagent_type="faion-test-agent",
     prompt=f"Write tests for {feature}")
```

### UI Development

```python
# Phase 1: Brainstorming
Task(subagent_type="faion-frontend-brainstormer-agent",
     prompt=f"Create 3-5 DISTINCT design variants for: {requirements}")

# Phase 2: Storybook
Task(subagent_type="faion-storybook-agent",
     prompt=f"Setup Storybook for {project}")

# Phase 3: Components
Task(subagent_type="faion-frontend-component-agent",
     prompt=f"Develop {component_name} with story file")
```

### Infrastructure

```python
Task(subagent_type="faion-devops-agent",
     prompt=f"Setup {infra_component} for {project}")
```

---

## Technical Skills Used

| Skill | Purpose |
|-------|---------|
| faion-python-skill | Python ecosystem patterns |
| faion-javascript-skill | JS/TS patterns |
| faion-backend-skill | Go, Ruby, PHP, Java, C#, Rust |
| faion-aws-cli-skill | AWS operations |
| faion-k8s-cli-skill | Kubernetes operations |
| faion-terraform-skill | Infrastructure as code |
| faion-docker-skill | Container operations |
| faion-testing-skill | Test frameworks |

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| faion-api-skill | API design patterns |
| faion-sdd-domain-skill | Specs and design docs |
| faion-product-domain-skill | Requirements for development |

---

*Domain Skill v1.0 - Development*
*68 Methodologies | 6 Agents*
*Merged from: faion-dev-django-skill, faion-dev-frontend-skill, faion-dev-docs-skill*
