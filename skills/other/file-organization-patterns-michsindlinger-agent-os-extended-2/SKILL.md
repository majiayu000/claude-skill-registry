---
name: [PROJECT]-file-organization
description: [PROJECT] file and directory structure conventions and enforcement
globs: ["**/*"]
---

# File Organization Patterns

> **Template for project-specific file organization skill**
> Define WHERE every type of file belongs in your codebase

**Project**: [PROJECT NAME]
**Structure Type**: [CUSTOMIZE: Monorepo / Multi-repo / Monolith / Microservices]
**Last Updated**: [DATE]

---

## Project Root Structure

**[CUSTOMIZE WITH YOUR PROJECT LAYOUT]**

```
[PROJECT-ROOT]/
├── [CUSTOMIZE: backend/ or src/main/ or app/]
├── [CUSTOMIZE: frontend/ or client/ or web/]
├── [CUSTOMIZE: shared/ or common/ or libs/]
├── [CUSTOMIZE: tests/ or test/]
├── [CUSTOMIZE: docs/]
├── [CUSTOMIZE: scripts/]
├── [CUSTOMIZE: .github/ or .gitlab/]
└── [CUSTOMIZE: docker/]

Example (Monorepo):
project-root/
├── backend/          # Spring Boot backend
├── frontend/         # React frontend
├── shared/           # Shared types, utils
├── docs/             # Documentation
├── scripts/          # Build scripts
└── .github/          # CI/CD workflows

Example (Backend-only):
project-root/
├── src/
│   ├── main/
│   └── test/
├── docs/
└── .github/
```

---

## Backend File Structure

**[CUSTOMIZE WITH YOUR BACKEND ORGANIZATION]**

### Package/Module Structure

**Base Path**: [CUSTOMIZE: src/main/java/com/company/ or src/ or app/]

**Directory Layout**:
```
[CUSTOMIZE: Show your backend structure]

Example (Java Spring Boot):
src/main/java/com/company/projectname/
├── controller/       # REST controllers ONLY
│   ├── UserController.java
│   └── OrderController.java
├── service/          # Business logic ONLY
│   ├── UserService.java
│   └── OrderService.java
├── repository/       # Data access ONLY
│   ├── UserRepository.java
│   └── OrderRepository.java
├── entity/           # JPA entities ONLY
│   ├── User.java
│   └── Order.java
├── dto/              # Data transfer objects ONLY
│   ├── UserDTO.java
│   ├── UserCreateRequest.java
│   └── UserUpdateRequest.java
├── exception/        # Custom exceptions ONLY
│   ├── UserNotFoundException.java
│   └── DuplicateEmailException.java
├── config/           # Configuration classes
│   └── SecurityConfig.java
└── util/             # Utility classes
    └── DateUtil.java

Example (Node.js/Express):
src/
├── controllers/      # Route handlers
├── services/         # Business logic
├── repositories/     # Database access
├── models/           # Mongoose/Sequelize models
├── dto/              # Request/response types
├── middleware/       # Express middleware
├── config/           # Configuration
└── utils/            # Utilities

Example (Python/Django):
app/
├── views/            # ViewSets
├── serializers/      # DRF serializers
├── models.py         # Django models
├── services/         # Business logic
├── exceptions.py     # Custom exceptions
└── utils/            # Utilities
```

### File Placement Rules

**Controllers/Routes**:
- MUST go in: [CUSTOMIZE: controller/ or controllers/ or routes/ or views/]
- NEVER in: root, service/, random folders
- Naming: [CUSTOMIZE: UserController.java or users.controller.ts or user_controller.py]

**Services/Business Logic**:
- MUST go in: [CUSTOMIZE: service/ or services/]
- NEVER in: controller/, util/, root
- Naming: [CUSTOMIZE: UserService.java or user.service.ts or user_service.py]

**Repositories/Data Access**:
- MUST go in: [CUSTOMIZE: repository/ or repositories/ or models/ or dao/]
- NEVER in: service/, controller/, root
- Naming: [CUSTOMIZE: UserRepository.java or user.repository.ts]

**Entities/Models**:
- MUST go in: [CUSTOMIZE: entity/ or entities/ or models/]
- NEVER in: dto/, service/, root
- Naming: [CUSTOMIZE: User.java or user.entity.ts or user.model.ts]

**DTOs/Request-Response**:
- MUST go in: [CUSTOMIZE: dto/ or dtos/ or serializers/]
- NEVER in: entity/, model/, root
- Naming: [CUSTOMIZE: UserDTO.java or user.dto.ts or UserSerializer]

**Exceptions/Errors**:
- MUST go in: [CUSTOMIZE: exception/ or exceptions/ or errors/]
- NEVER in: service/, root
- Naming: [CUSTOMIZE: UserNotFoundException.java or NotFoundError.ts]

**Configuration**:
- MUST go in: [CUSTOMIZE: config/ or configuration/]
- NEVER in: service/, util/, root
- Naming: [CUSTOMIZE: SecurityConfig.java or database.config.ts]

**Utilities/Helpers**:
- MUST go in: [CUSTOMIZE: util/ or utils/ or helpers/]
- NEVER in: service/, controller/
- Naming: [CUSTOMIZE: DateUtil.java or date.util.ts or date_util.py]

---

## Frontend File Structure

**[CUSTOMIZE WITH YOUR FRONTEND ORGANIZATION]**

### Directory Layout

**Base Path**: [CUSTOMIZE: src/ or app/]

**Organization Pattern**: [CUSTOMIZE: By-feature / By-type / Atomic design / Hybrid]

**Example - By-Type** (Traditional):
```
[CUSTOMIZE: Show your frontend structure]

Example (React):
src/
├── components/       # Reusable components ONLY
│   ├── common/       # Shared (Button, Card, Badge)
│   ├── layout/       # Layout components (Header, Sidebar)
│   └── features/     # Feature-specific (UserList, ProductCard)
├── pages/            # Page components ONLY
│   ├── Dashboard.tsx
│   ├── Users.tsx
│   └── Settings.tsx
├── services/         # API clients ONLY
│   ├── UserService.ts
│   └── api.ts
├── hooks/            # Custom hooks ONLY (React)
│   ├── useUsers.ts
│   └── useAuth.ts
├── contexts/         # React Context providers ONLY
│   └── AuthContext.tsx
├── types/            # TypeScript types/interfaces ONLY
│   ├── User.ts
│   └── api.types.ts
├── utils/            # Utility functions ONLY
│   ├── format.ts
│   └── validation.ts
├── assets/           # Static assets ONLY
│   ├── images/
│   ├── fonts/
│   └── styles/
└── config/           # Configuration ONLY
    └── constants.ts

Example (Angular):
src/app/
├── components/       # Standalone components
├── pages/            # Page components
├── services/         # Injectable services
├── guards/           # Route guards
├── interceptors/     # HTTP interceptors
├── models/           # TypeScript interfaces
├── pipes/            # Custom pipes
└── directives/       # Custom directives

Example (Vue):
src/
├── components/       # Vue components
├── views/            # Page views
├── composables/      # Composition functions
├── stores/           # Pinia stores
├── router/           # Vue Router
├── types/            # TypeScript types
└── assets/           # Static assets
```

**Example - By-Feature** (Modern):
```
src/
├── features/
│   ├── users/
│   │   ├── components/  # UserList, UserCard
│   │   ├── services/    # UserService
│   │   ├── hooks/       # useUsers
│   │   ├── types/       # User types
│   │   └── tests/       # Feature tests
│   └── products/
│       ├── components/
│       ├── services/
│       └── ...
├── shared/              # Shared across features
│   ├── components/      # Button, Card
│   ├── hooks/           # useApi
│   └── utils/
└── core/                # App-level
    ├── layout/
    ├── routing/
    └── config/
```

### File Placement Rules

**Components**:
- MUST go in: [CUSTOMIZE: components/ or features/[feature]/components/]
- NEVER in: root, services/, pages/ (unless page component)
- Naming: [CUSTOMIZE: UserList.tsx or user-list.component.ts or UserList.vue]
- Co-location: [CUSTOMIZE: CSS next to component? Tests next to component?]

**Pages/Views**:
- MUST go in: [CUSTOMIZE: pages/ or views/ or features/[feature]/pages/]
- NEVER in: components/ (unless also reusable), root
- Naming: [CUSTOMIZE: Dashboard.tsx or dashboard.page.ts or Dashboard.vue]

**Services/API Clients**:
- MUST go in: [CUSTOMIZE: services/ or api/ or features/[feature]/services/]
- NEVER in: components/, pages/, root
- Naming: [CUSTOMIZE: UserService.ts or user.service.ts or userService.ts]

**Hooks/Composables** (if applicable):
- MUST go in: [CUSTOMIZE: hooks/ or composables/ or features/[feature]/hooks/]
- NEVER in: components/, root
- Naming: [CUSTOMIZE: useUsers.ts or use-users.ts or useUsers.tsx]

**Types/Interfaces**:
- MUST go in: [CUSTOMIZE: types/ or models/ or features/[feature]/types/]
- NEVER in: components/, services/, root
- Naming: [CUSTOMIZE: User.ts or user.types.ts or IUser.ts]

**Utilities**:
- MUST go in: [CUSTOMIZE: utils/ or helpers/ or lib/]
- NEVER in: components/, services/, root
- Naming: [CUSTOMIZE: format.ts or formatUtils.ts or format_utils.ts]

**Assets** (Images, Fonts, Global CSS):
- MUST go in: [CUSTOMIZE: assets/ or public/ or static/]
- NEVER in: components/, src/, root
- Subfolders: [CUSTOMIZE: assets/images/, assets/fonts/, assets/styles/]

---

## Test File Structure

**[CUSTOMIZE WITH YOUR TEST ORGANIZATION]**

### Test Location Strategy

**Co-located** (next to source):
```
[CUSTOMIZE if using co-located tests]

Example:
src/services/
├── UserService.ts
├── UserService.test.ts  <- Next to source
```

**Separate Test Directory**:
```
[CUSTOMIZE if using separate test dirs]

Example:
src/services/UserService.ts
test/services/UserService.test.ts  <- Mirrors structure
```

### Test File Naming

**Convention**: [CUSTOMIZE: .test.ts / .spec.ts / Test.java / _test.py / _spec.rb]

**Examples**:
- UserService -> [UserService.test.ts or UserServiceTest.java or user_service_test.py]

---

## Configuration Files

**[CUSTOMIZE WITH YOUR CONFIG ORGANIZATION]**

**Where Config Files Go**:

| File Type | Location | Example |
|-----------|----------|---------|
| Environment vars | [CUSTOMIZE: .env / config/ / env/] | .env.development |
| App config | [CUSTOMIZE: config/ / src/config/] | database.config.ts |
| CI/CD | [CUSTOMIZE: .github/workflows/ / .gitlab-ci.yml] | ci.yml |
| Docker | [CUSTOMIZE: root / docker/] | Dockerfile, docker-compose.yml |
| Package manager | [CUSTOMIZE: root] | package.json, pom.xml |
| Linting | [CUSTOMIZE: root] | .eslintrc.json, .prettierrc |
| TypeScript | [CUSTOMIZE: root] | tsconfig.json |

---

## Build Output

**[CUSTOMIZE WHERE BUILD ARTIFACTS GO]**

**Backend**:
- Build output: [CUSTOMIZE: target/ or dist/ or build/]
- NEVER commit build artifacts

**Frontend**:
- Build output: [CUSTOMIZE: dist/ or build/ or out/]
- NEVER commit build artifacts

**Rules**:
- Always in .gitignore
- Clean before rebuild

---

## Common Anti-Patterns to Avoid

**[CUSTOMIZE WITH PROJECT-SPECIFIC VIOLATIONS]**

**NEVER DO**:
- Controllers in root directory
- Services mixed with controllers in same folder
- DTOs in entity folder (or vice versa)
- Test files in src/ (if using separate test directory)
- Business logic in controllers
- Database queries in services (should be in repository)
- [CUSTOMIZE: Project-specific violation]

**ALWAYS DO**:
- One file type per directory (controllers in controller/, services in service/)
- Mirror test structure to source structure
- Keep related files together (feature-based if that's your pattern)
- Consistent naming conventions
- [CUSTOMIZE: Project-specific rule]

---

## File Naming Conventions

**[CUSTOMIZE WITH PROJECT STANDARDS]**

### Backend

**Controllers**: [CUSTOMIZE: UserController.java / users.controller.ts / user_controller.py]
**Services**: [CUSTOMIZE: UserService.java / user.service.ts / user_service.py]
**Repositories**: [CUSTOMIZE: UserRepository.java / user.repository.ts]
**Entities**: [CUSTOMIZE: User.java / user.entity.ts / user.model.ts]
**DTOs**: [CUSTOMIZE: UserDTO.java / user.dto.ts / UserCreateRequest.java]
**Tests**: [CUSTOMIZE: UserServiceTest.java / user.service.test.ts]

### Frontend

**Components**: [CUSTOMIZE: UserList.tsx / user-list.component.ts / UserList.vue]
**Pages**: [CUSTOMIZE: Dashboard.tsx / dashboard.page.ts]
**Services**: [CUSTOMIZE: UserService.ts / user.service.ts]
**Hooks**: [CUSTOMIZE: useUsers.ts / use-users.ts]
**Types**: [CUSTOMIZE: User.ts / user.types.ts / IUser.ts]
**Styles**: [CUSTOMIZE: UserList.module.css / user-list.component.css / UserList.styles.ts]

---

## Validation Rules

**[CUSTOMIZE WITH ENFORCEMENT RULES]**

### Mandatory Rules

**Rule 1: One Concern Per Directory**
- Controllers ONLY in controller/
- Services ONLY in service/
- No mixing

**Rule 2: Consistent Depth**
- All controllers at same depth: [CUSTOMIZE: src/controller/*.java or src/main/java/com/company/controller/*.java]
- No random nesting

**Rule 3: Test Mirror Source**
- If source: `src/service/UserService.java`
- Then test: [CUSTOMIZE: src/test/java/.../service/UserServiceTest.java or test/service/UserService.test.ts]

**Rule 4: No Code in Root**
- NEVER: `project-root/UserController.java`
- ALWAYS: Proper directory structure

**[CUSTOMIZE: Add more rules]**

---

## Reorganization Patterns

### Moving Misplaced Files

**If file in wrong location**:

```bash
[CUSTOMIZE: Show how to reorganize]

Example:
# Found: src/UserController.java (WRONG - in root of src/)
# Should: src/controller/UserController.java

# Action:
mkdir -p src/controller
mv src/UserController.java src/controller/
# Update imports in other files
```

### Bulk Reorganization

**Pattern**:
```bash
[CUSTOMIZE: Show bulk move commands]

Example:
# Find all controllers in wrong places
find src -name "*Controller.java" -not -path "*/controller/*"
# Move to correct location
```

---

## Package/Import Structure

**[CUSTOMIZE WITH IMPORT RULES]**

### Import Order

**Convention**:
```
[CUSTOMIZE: Show import organization]

Examples:
1. Standard library imports
2. Third-party imports
3. Internal imports (relative)

OR:

1. Framework imports (React, Angular, Django)
2. Third-party libraries
3. Internal absolute imports
4. Internal relative imports
5. Type imports (TypeScript)
```

### Path Aliases

**Configured Aliases**:
```
[CUSTOMIZE: List path aliases if used]

Examples:
- @/components -> src/components
- @/services -> src/services
- ~/utils -> src/utils
```

---

## Special Directories

**[CUSTOMIZE WITH SPECIAL FOLDERS]**

### Generated Code

**Location**: [CUSTOMIZE: generated/ or .generated/ or codegen/]
**Rule**: Never edit manually, always in .gitignore

### Migrations

**Location**: [CUSTOMIZE: db/migrations/ or migrations/ or alembic/versions/]
**Naming**: [CUSTOMIZE: V1__create_users.sql or 001_create_users.py]

### Fixtures/Seeds

**Location**: [CUSTOMIZE: db/seeds/ or fixtures/ or test/fixtures/]

---

## File Size Limits

**[CUSTOMIZE WITH PROJECT STANDARDS]**

**Recommended Limits**:
- Controller: [<=200 lines / <=300 lines]
- Service: [<=300 lines / <=500 lines]
- Component: [<=250 lines / <=300 lines]

**When to Split**:
- If file >limit -> Split into multiple files
- Extract to separate concerns

---

## Examples: Common File Types

**[CUSTOMIZE - COMPLETE MAPPING]**

| File Type | Exact Location | Naming Pattern | Example |
|-----------|----------------|----------------|---------|
| REST Controller | [CUSTOMIZE] | [CUSTOMIZE] | UserController.java |
| Service Class | [CUSTOMIZE] | [CUSTOMIZE] | UserService.java |
| Repository | [CUSTOMIZE] | [CUSTOMIZE] | UserRepository.java |
| Entity | [CUSTOMIZE] | [CUSTOMIZE] | User.java |
| DTO (Request) | [CUSTOMIZE] | [CUSTOMIZE] | UserCreateRequest.java |
| DTO (Response) | [CUSTOMIZE] | [CUSTOMIZE] | UserDTO.java |
| Custom Exception | [CUSTOMIZE] | [CUSTOMIZE] | UserNotFoundException.java |
| React Component | [CUSTOMIZE] | [CUSTOMIZE] | UserList.tsx |
| React Page | [CUSTOMIZE] | [CUSTOMIZE] | Dashboard.tsx |
| API Service | [CUSTOMIZE] | [CUSTOMIZE] | UserService.ts |
| Custom Hook | [CUSTOMIZE] | [CUSTOMIZE] | useUsers.ts |
| Type Definition | [CUSTOMIZE] | [CUSTOMIZE] | User.ts |
| Utility Function | [CUSTOMIZE] | [CUSTOMIZE] | formatDate.ts |
| Test File | [CUSTOMIZE] | [CUSTOMIZE] | UserService.test.ts |
| Config File | [CUSTOMIZE] | [CUSTOMIZE] | database.config.ts |

---

## Structure Validation Checklist

**[CUSTOMIZE WITH VALIDATION STEPS]**

Run before committing:

- [ ] All controllers in correct directory
- [ ] All services in correct directory
- [ ] No code files in root (except config)
- [ ] Test files mirror source structure
- [ ] No orphaned files (imports broken)
- [ ] Consistent naming throughout
- [ ] No duplicate directories (controller/ AND controllers/)
- [ ] [PROJECT-SPECIFIC CHECK]

---

## Project-Specific Patterns

**[CUSTOMIZE - ADD YOUR CONVENTIONS]**

### Feature Modules (if applicable)
- [How features are organized]
- [What goes in each feature]
- [How features communicate]

### Shared/Common Code
- [Where shared code lives]
- [When to extract to shared]

### Monorepo Workspace Rules (if applicable)
- [How workspaces are organized]
- [Inter-workspace dependencies]

---

## Quick Reference

**Backend Quick Lookup**:
- Controller? -> [PATH]
- Service? -> [PATH]
- Repository? -> [PATH]
- Entity? -> [PATH]
- DTO? -> [PATH]
- Exception? -> [PATH]
- Test? -> [PATH]

**Frontend Quick Lookup**:
- Component? -> [PATH]
- Page? -> [PATH]
- Service? -> [PATH]
- Hook? -> [PATH]
- Type? -> [PATH]
- Util? -> [PATH]
- Test? -> [PATH]

---

**Customization Complete**: Replace all [CUSTOMIZE] sections with project structure.

**Auto-generated by**: `/add-skill file-organization` command (via codebase analysis)

**Used by**: project-structure-manager agent (consulted before file creation)
