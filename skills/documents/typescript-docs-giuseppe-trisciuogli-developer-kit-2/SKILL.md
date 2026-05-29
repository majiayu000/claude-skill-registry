---
name: typescript-docs
version: 1.0.0
description: Create comprehensive TypeScript documentation using JSDoc, TypeDoc, and multi-layered documentation patterns for different audiences. Includes API documentation, architectural decision records (ADRs), code examples, and framework-specific patterns for NestJS, Express, React, Angular, and Vue.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
category: frontend
tags: [typescript, documentation, jsdoc, typedoc, api-docs, adr, react, angular, vue, nestjs, express]
---

# TypeScript Documentation Skill

## Overview
Deliver production-ready TypeScript documentation that serves multiple audiences through layered documentation architecture. Generate API docs with TypeDoc, create architectural decision records, and maintain comprehensive code examples.

## When to Use
- "generate TypeScript API docs" - Create TypeDoc configuration and generate documentation
- "document this TypeScript module" - Add comprehensive JSDoc to a module
- "create ADR for TypeScript decision" - Document architectural decisions
- "setup documentation pipeline" - Configure automated documentation generation
- "document React component" - Create component documentation with examples
- "create API reference" - Generate comprehensive API documentation

## Quick Start

1. Install TypeDoc and related tools:
```bash
npm install --save-dev typedoc typedoc-plugin-markdown
npm install --save-dev @compodoc/compodoc # For Angular
```

2. Create basic TypeDoc configuration:
```json
{
  "entryPoints": ["src/index.ts"],
  "out": "docs/api",
  "theme": "markdown",
  "excludePrivate": true,
  "readme": "README.md"
}
```

3. Generate documentation:
```bash
npx typedoc
```

## Core Documentation Patterns

### 1. JSDoc Best Practices

#### Interface Documentation
```typescript
/**
 * Represents a user in the authentication system
 * @interface User
 *
 * @property id - Unique identifier (UUID v4)
 * @property email - User's email address (validated format)
 * @property roles - Array of user roles for RBAC
 * @property metadata - Additional user data (preferences, settings)
 *
 * @example
 * ```typescript
 * const user: User = {
 *   id: "550e8400-e29b-41d4-a716-446655440000",
 *   email: "user@example.com",
 *   roles: ["user", "admin"],
 *   metadata: {
 *     theme: "dark",
 *     language: "en"
 *   }
 * };
 * ```
 *
 * @see {@link UserRole} for role definitions
 * @see {@link UserService} for user operations
 */
export interface User {
  id: string;
  email: string;
  roles: UserRole[];
  metadata: Record<string, unknown>;
}
```

#### Function Documentation
```typescript
/**
 * Authenticates a user with email and password
 * @param email - User's email address
 * @param password - User's password (min 8 characters)
 * @param options - Additional authentication options
 * @returns Promise resolving to authentication result
 *
 * @throws {InvalidCredentialsError} If email/password don't match
 * @throws {AccountLockedError} If account is locked after failed attempts
 * @throws {RateLimitExceededError} If too many attempts made
 *
 * @remarks
 * Implements secure authentication with:
 * - Bcrypt password hashing (cost factor 12)
 * - Rate limiting (5 attempts per 15 minutes)
 * - Account lockout after 3 consecutive failures
 * - JWT token generation with 15-minute expiry
 *
 * @example
 * ```typescript
 * try {
 *   const result = await authenticateUser("user@example.com", "password123");
 *   console.log(`Authenticated: ${result.user.email}`);
 * } catch (error) {
 *   if (error instanceof InvalidCredentialsError) {
 *     // Handle invalid credentials
 *   }
 * }
 * ```
 *
 * @security
 * - Passwords are never logged or stored in plain text
 * - Uses timing-attack safe comparison
 * - Implements CSRF protection for web requests
 *
 * @performance
 * - Average response time: ~200ms
 * - Uses connection pooling for database queries
 * - Caches user permissions for 5 minutes
 */
export async function authenticateUser(
  email: string,
  password: string,
  options?: AuthOptions
): Promise<AuthResult> {
  // Implementation
}
```

#### Class Documentation
```typescript
/**
 * Service for managing user authentication and authorization
 *
 * @remarks
 * This service handles:
 * - User authentication with JWT tokens
 * - Password reset flows
 * - Multi-factor authentication
 * - Session management
 * - Role-based access control
 *
 * @example
 * ```typescript
 * const authService = new AuthService(config);
 *
 * // Authenticate user
 * const token = await authService.login(email, password);
 *
 * // Verify token
 * const user = await authService.verifyToken(token);
 * ```
 *
 * @security
 * - All passwords hashed with bcrypt
 * - JWT tokens signed with RS256
 * - Rate limiting on authentication endpoints
 * - Secure session management
 *
 * @performance
 * - Uses Redis for session storage
 * - Implements connection pooling
 * - Caches user permissions
 */
export class AuthService {
  /**
   * Creates an instance of AuthService
   * @param config - Service configuration
   * @param config.jwtSecret - Secret key for JWT signing
   * @param config.tokenExpiry - Token expiry duration
   * @param config.refreshTokenExpiry - Refresh token expiry
   */
  constructor(private readonly config: AuthConfig) {}

  /**
   * Authenticates a user and returns access tokens
   * @param credentials - User credentials
   * @returns Authentication result with tokens
   */
  async login(credentials: LoginCredentials): Promise<AuthResult> {
    // Implementation
  }
}
```

### 2. Advanced TypeScript Documentation

#### Generic Constraints
```typescript
/**
 * Repository base class for TypeScript entities
 * @template T - Entity type (must extend BaseEntity)
 * @template K - Primary key type (string | number)
 *
 * @remarks
 * Provides CRUD operations with type safety.
 * All methods return Result types for explicit error handling.
 *
 * @example
 * ```typescript
 * class UserRepository extends BaseRepository<User, string> {
 *   async findByEmail(email: string): Promise<Result<User, RepositoryError>> {
 *     // Implementation
 *   }
 * }
 * ```
 */
export abstract class BaseRepository<T extends BaseEntity, K extends string | number> {
  /**
   * Finds an entity by its primary key
   * @param id - Primary key value
   * @returns Result containing entity or error
   */
  abstract findById(id: K): Promise<Result<T, RepositoryError>>;
}
```

#### Union Types and Discriminated Unions
```typescript
/**
 * Represents different types of API responses
 * @variant success - Successful response with data
 * @variant error - Error response with error details
 * @variant pending - Pending response for async operations
 *
 * @example
 * ```typescript
 * type ApiResponse<T> = SuccessResponse<T> | ErrorResponse | PendingResponse;
 *
 * function handleResponse<T>(response: ApiResponse<T>) {
 *   switch (response.status) {
 *     case 'success':
 *       console.log(response.data);
 *       break;
 *     case 'error':
 *       console.error(response.error);
 *       break;
 *     case 'pending':
 *       console.log('Loading...');
 *       break;
 *   }
 * }
 * ```
 */
export type ApiResponse<T> =
  | { status: 'success'; data: T }
  | { status: 'error'; error: ApiError }
  | { status: 'pending'; progress?: number };
```

### 3. Framework-Specific Documentation

#### NestJS Documentation
```typescript
/**
 * Guard for protecting routes with JWT authentication
 *
 * @guard
 * @remarks
 * Validates JWT tokens from Authorization header.
 * Attaches user data to request object.
 *
 * @usageNotes
 * Apply to controllers or methods:
 * ```typescript
 * @Controller('users')
 * @UseGuards(JwtAuthGuard)
 * export class UserController {
 *   @Get('profile')
 *   getProfile(@Request() req) {
 *     return req.user;
 *   }
 * }
 * ```
 *
 * @security
 * - Validates token signature
 * - Checks token expiration
 * - Prevents token replay attacks
 *
 * @performance
 * - Caches validation results for 5 minutes
 * - Uses Redis for distributed caching
 */
@Injectable()
export class JwtAuthGuard implements CanActivate {
  constructor(private jwtService: JwtService) {}

  /**
   * Validates JWT token and extracts user data
   * @param context - Execution context
   * @returns True if authentication successful
   */
  async canActivate(context: ExecutionContext): Promise<boolean> {
    // Implementation
  }
}
```

#### React Component Documentation
```typescript
/**
 * User profile card component
 * @component
 * @param {UserProfileProps} props - Component props
 * @param {User} props.user - User data to display
 * @param {boolean} props.editable - Whether profile is editable
 * @param {function} props.onEdit - Edit button click handler
 *
 * @example
 * ```tsx
 * export default function Dashboard() {
 *   const { user } = useAuth();
 *
 *   return (
 *     <div>
 *       <h1>User Profile</h1>
 *       <UserProfile
 *         user={user}
 *         editable={true}
 *         onEdit={() => console.log('Edit clicked')}
 *       />
 *     </div>
 *   );
 * }
 * ```
 *
 * @performance
 * - Memoized with React.memo
 * - Lazy loads avatar images
 * - Optimistic UI updates
 *
 * @accessibility
 * - Full keyboard navigation
 * - ARIA labels for screen readers
 * - High contrast support
 */
export const UserProfile = React.memo<UserProfileProps>(
  ({ user, editable, onEdit }) => {
    // Implementation
  }
);
```

#### Express Middleware Documentation
```typescript
/**
 * Rate limiting middleware with Redis backend
 * @middleware
 * @param options - Rate limiting options
 * @param options.windowMs - Time window in milliseconds
 * @param options.max - Maximum requests per window
 * @param options.keyGenerator - Function to generate rate limit key
 *
 * @example
 * ```typescript
 * app.use('/api', rateLimit({
 *   windowMs: 15 * 60 * 1000, // 15 minutes
 *   max: 100, // limit each IP to 100 requests per windowMs
 *   keyGenerator: (req) => req.ip
 * }));
 * ```
 *
 * @errorResponses
 * - `429` - Too many requests
 * - `500` - Redis connection error
 *
 * @security
 * - Prevents DoS attacks
 * - Implements sliding window algorithm
 * - Distributed across multiple servers
 */
export function rateLimit(options: RateLimitOptions): RequestHandler {
  // Implementation
}
```

## Architectural Decision Records (ADRs)

### ADR Template
```markdown
# ADR-001: TypeScript Strict Mode Configuration

## Status
Proposed | Accepted | Rejected | Deprecated | Superseded

## Context
What is the issue that we're seeing that is motivating this decision?

## Decision
What is the change that we're proposing and/or doing?

## Consequences
What becomes easier or more difficult to do because of this change?

## Compliance
- Links to standards or regulations
- Impact on compliance requirements

## References
- [TypeScript Strict Mode Documentation](https://www.typescriptlang.org/tsconfig#strict)
- [Related ADRs](#)
```

### Sample ADR
```markdown
# ADR-003: NestJS Framework Selection for Backend API

## Status
Accepted

## Context
Our Express.js monolith has grown to 50k+ lines with:
- Inconsistent error handling patterns
- No standardized validation
- Difficult testing due to tight coupling
- Poor TypeScript integration

We need a framework that provides:
- Strong TypeScript support
- Opinionated structure
- Built-in validation and error handling
- Excellent testing support
- Microservices readiness

## Decision
Adopt NestJS for all new backend services with:
- Full TypeScript strict mode
- Class-based DI container
- Modular architecture
- Built-in validation pipes
- Exception filters
- Swagger/OpenAPI integration

## Consequences
### Positive
- 40% reduction in boilerplate code
- Consistent patterns across services
- Improved testability with dependency injection
- Better developer experience with decorators
- Built-in support for microservices

### Negative
- Learning curve for team (2-3 weeks)
- More complex for simple APIs
- Requires understanding of decorators
- Additional build step needed

## Implementation
1. Create NestJS starter template
2. Migrate new services to NestJS
3. Gradually refactor critical Express services
4. Establish NestJS best practices guide

## Compliance
- Aligns with architecture standards v2.1
- Supports SOC2 through better error handling
- Enables GDPR compliance with structured logging
```

## Documentation Generation Pipeline

### TypeDoc Configuration
```json
{
  "entryPoints": ["src/index.ts"],
  "out": "docs/api",
  "theme": "markdown",
  "readme": "README.md",
  "excludePrivate": true,
  "excludeProtected": false,
  "excludeExternals": true,
  "includeVersion": true,
  "sort": ["source-order"],
  "kindSortOrder": [
    "Document",
    "Project",
    "Module",
    "Namespace",
    "Enum",
    "Class",
    "Interface",
    "TypeAlias",
    "Constructor",
    "Property",
    "Method"
  ],
  "categorizeByGroup": true,
  "categoryOrder": [
    "Authentication",
    "Authorization",
    "*",
    "Other"
  ],
  "navigation": {
    "includeCategories": true,
    "includeGroups": true
  }
}
```

### Documentation Scripts
```json
{
  "scripts": {
    "docs:generate": "typedoc",
    "docs:serve": "cd docs && python -m http.server 8080",
    "docs:validate": "node scripts/validate-docs.js",
    "docs:deploy": "npm run docs:generate && ./scripts/deploy-docs.sh",
    "adr:new": "node scripts/create-adr.js",
    "adr:generate-index": "node scripts/generate-adr-index.js"
  }
}
```

### GitHub Actions Workflow
```yaml
name: Documentation

on:
  push:
    branches: [main, develop]
    paths:
      - 'src/**'
      - 'docs/**'
      - '.github/workflows/docs.yml'

jobs:
  generate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Generate TypeDoc
        run: npm run docs:generate

      - name: Validate documentation
        run: npm run docs:validate

      - name: Check for documentation changes
        id: changes
        run: |
          if git diff --quiet HEAD~1 docs/; then
            echo "changed=false" >> $GITHUB_OUTPUT
          else
            echo "changed=true" >> $GITHUB_OUTPUT
          fi

      - name: Commit documentation
        if: steps.changes.outputs.changed == 'true'
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add docs/
          git commit -m "docs: update generated documentation [skip ci]"
          git push

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

## Framework-Specific Documentation

### NestJS Documentation Patterns
```typescript
/**
 * Decorator for rate limiting endpoints
 * @decorator
 * @param options - Rate limiting options
 *
 * @usageNotes
 * Apply to controller methods:
 * ```typescript
 * @Controller('users')
 * export class UserController {
 *   @Get()
 *   @RateLimit({ points: 100, duration: 60 })
 *   async findAll() {
 *     // Implementation
 *   }
 * }
 * ```
 *
 * @see {@link RateLimitInterceptor}
 * @see {@link RateLimitOptions}
 */
export const RateLimit = (options: RateLimitOptions) =>
  applyDecorators(
    UseInterceptors(RateLimitInterceptor),
    SetMetadata('rateLimit', options)
  );
```

### React Documentation Patterns
```typescript
/**
 * Custom hook for managing form state with validation
 * @hook
 * @param schema - Yup validation schema
 * @param initialValues - Initial form values
 * @returns Form state and handlers
 *
 * @example
 * ```tsx
 * function LoginForm() {
 *   const { values, errors, handleSubmit, handleChange } = useForm({
 *     schema: loginSchema,
 *     initialValues: { email: '', password: '' }
 *   });
 *
 *   return (
 *     <form onSubmit={handleSubmit}>
 *       <input
 *         name="email"
 *         value={values.email}
 *         onChange={handleChange}
 *       />
 *       {errors.email && <span>{errors.email}</span>}
 *     </form>
 *   );
 * }
 * ```
 *
 * @performance
 * - Memoized validation to prevent unnecessary re-renders
 * - Debounced validation for better UX
 * - Optimistic updates for better perceived performance
 */
export function useForm<T>({
  schema,
  initialValues
}: UseFormOptions<T>): UseFormReturn<T> {
  // Implementation
}
```

### Angular Documentation Patterns
```typescript
/**
 * Service for managing user sessions
 * @injectable
 * @providedIn root
 *
 * @remarks
 * Handles user authentication state across the application.
 * Automatically refreshes tokens before expiry.
 *
 * @example
 * ```typescript
 * export class AppComponent {
 *   constructor(private authService: AuthService) {}
 *
 *   async login() {
 *     await this.authService.login(credentials);
 *   }
 * }
 * ```
 *
 * @security
 * - Stores tokens in secure storage
 * - Implements token refresh logic
 * - Handles logout on all tabs (broadcast channel)
 */
@Injectable({
  providedIn: 'root'
})
export class AuthService {
  // Implementation
}
```

## Documentation Validation

### TypeDoc Plugin for Validation
```typescript
// typedoc-plugin-validation.js
export function load(app) {
  app.converter.on(
    Converter.EVENT_CREATE_SIGNATURE,
    (context, reflection, node?) => {
      // Check if method has JSDoc
      if (reflection.kind === ReflectionKind.Method) {
        const comment = reflection.comment;
        if (!comment) {
          app.logger.warn(
            `Method ${reflection.name} lacks documentation in ${reflection.parent.name}`
          );
        }
      }
    }
  );
}
```

### ESLint Rules for Documentation
```json
{
  "rules": {
    "jsdoc/require-description": "error",
    "jsdoc/require-param-description": "error",
    "jsdoc/require-returns-description": "error",
    "jsdoc/require-example": "warn",
    "jsdoc/check-alignment": "error",
    "jsdoc/check-indentation": "error",
    "jsdoc/tag-lines": ["error", "any", { "startLines": 1 }]
  }
}
```

## Best Practices

1. **Document Public APIs**: All public methods, classes, and interfaces
2. **Use @example**: Provide runnable examples for complex functions
3. **Include @throws**: Document all possible errors
4. **Add @see**: Cross-reference related functions/types
5. **Use @remarks**: Add implementation details and notes
6. **Document Generics**: Explain generic constraints and usage
7. **Include Performance Notes**: Document time/space complexity
8. **Add Security Warnings**: Highlight security considerations
9. **Use Categories**: Group related documentation
10. **Keep Updated**: Update docs when code changes

## Common Pitfalls to Avoid

1. **Don't document obvious code**: Focus on why, not what
2. **Avoid outdated examples**: Keep examples current
3. **Don't skip error cases**: Document all @throws scenarios
4. **Avoid generic descriptions**: Be specific to your implementation
5. **Don't ignore edge cases**: Document special conditions
6. **Avoid broken links**: Keep @see references valid
7. **Don't use unclear language**: Write for your audience
8. **Avoid duplication**: Link to related docs instead of repeating