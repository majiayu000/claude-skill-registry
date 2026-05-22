---
name: tech-stack-analyzer
description: Automatically detects project tech stack and generates framework-specific standards. PROACTIVELY activates on: (1) New project initialization, (2) package.json changes, (3) SessionStart in new repositories. Analyzes dependencies, frameworks, languages, and tools to create customized CLAUDE.md standards files.
---

# Tech Stack Analyzer Skill

You are the Tech Stack Analyzer. Your mission is to automatically detect the project's technology stack and generate comprehensive, framework-specific development standards.

## When to Activate

Auto-activate when:
- **New project detected** (first session in a repository)
- **package.json modified** (dependencies added/removed)
- **Explicit request** (`/analyze-tech-stack` command)
- **Missing standards** (.factory/standards/ directory empty)

## Analysis Process

### Step 1: Detect Package Manager

Check for lock files in this order:
1. `bun.lockb` → Bun
2. `pnpm-lock.yaml` → pnpm
3. `yarn.lock` → Yarn
4. `package-lock.json` → npm
5. `requirements.txt` → pip (Python)
6. `Cargo.toml` → Cargo (Rust)
7. `go.mod` → Go modules

**Output:** Detected package manager

### Step 2: Analyze package.json (JavaScript/TypeScript)

```javascript
// Read and parse package.json
const pkg = JSON.parse(await Read('package.json'));
const allDeps = { ...pkg.dependencies, ...pkg.devDependencies };

// Detect frameworks
const frameworks = [];
if (allDeps['react']) frameworks.push('react');
if (allDeps['next']) frameworks.push('nextjs');
if (allDeps['vue']) frameworks.push('vue');
if (allDeps['nuxt']) frameworks.push('nuxt');
if (allDeps['@angular/core']) frameworks.push('angular');
if (allDeps['svelte']) frameworks.push('svelte');
if (allDeps['express']) frameworks.push('express');
if (allDeps['fastify']) frameworks.push('fastify');
if (allDeps['@nestjs/core']) frameworks.push('nestjs');
if (allDeps['koa']) frameworks.push('koa');

// Detect testing framework
let testFramework = 'none';
if (allDeps['jest']) testFramework = 'jest';
else if (allDeps['vitest']) testFramework = 'vitest';
else if (allDeps['@playwright/test']) testFramework = 'playwright';
else if (allDeps['cypress']) testFramework = 'cypress';

// Detect build tool
let buildTool = 'none';
if (allDeps['vite']) buildTool = 'vite';
else if (allDeps['webpack']) buildTool = 'webpack';
else if (allDeps['rollup']) buildTool = 'rollup';
else if (allDeps['esbuild']) buildTool = 'esbuild';
else if (pkg.name?.includes('bun')) buildTool = 'bun';

// Detect state management
let stateManager = 'none';
if (allDeps['redux']) stateManager = 'redux';
else if (allDeps['zustand']) stateManager = 'zustand';
else if (allDeps['jotai']) stateManager = 'jotai';
else if (allDeps['recoil']) stateManager = 'recoil';
else if (allDeps['mobx']) stateManager = 'mobx';
else if (allDeps['pinia']) stateManager = 'pinia (Vue)';
else if (allDeps['@ngrx/store']) stateManager = 'ngrx (Angular)';

// Detect linter/formatter
const linters = [];
if (allDeps['eslint']) linters.push('eslint');
if (allDeps['prettier']) linters.push('prettier');
if (allDeps['@biomejs/biome']) linters.push('biome');

// Detect TypeScript
const isTypeScript = allDeps['typescript'] || 
                     pkg.scripts?.some(s => s.includes('tsc'));
```

**Output:** Framework inventory with versions

### Step 3: Detect Languages

Check for config files:
- `tsconfig.json` → TypeScript
- `*.py` files → Python
- `Cargo.toml` → Rust
- `go.mod` → Go
- `*.java` files → Java
- `*.kt` files → Kotlin
- `*.swift` files → Swift

**Output:** Primary and secondary languages

### Step 4: Generate Standards Files

For each detected framework/language, create a standards file in `.factory/standards/`:

#### React Standards (if React detected)

```markdown
# React Development Standards

## Component Patterns

### Functional Components (Required)
- Use functional components with hooks
- Avoid class components unless maintaining legacy code
- Co-locate component logic with UI

### Hooks Best Practices
\`\`\`typescript
// ✅ Good: Custom hooks for reusable logic
function useUserData(userId: string) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    setLoading(true);
    fetchUser(userId)
      .then(setUser)
      .finally(() => setLoading(false));
  }, [userId]);
  
  return { user, loading };
}

// ❌ Bad: Logic directly in component
function UserProfile({ userId }: Props) {
  const [user, setUser] = useState<User | null>(null);
  
  useEffect(() => {
    fetch(\`/api/users/\${userId}\`).then(r => r.json()).then(setUser);
  }, [userId]);
  
  return <div>{user?.name}</div>;
}
\`\`\`

### State Management
- **Local State:** useState/useReducer for component-specific state
- **Global State:** ${stateManager || 'Context API for simple cases'}
- **Server State:** React Query or SWR for API data

### Performance Optimization
- Memoize expensive computations with `useMemo`
- Memoize callbacks with `useCallback` when passed to memoized children
- Use `React.memo` for pure components that re-render frequently
- Lazy load routes and heavy components: `React.lazy(() => import('./Heavy'))`

## File Structure
\`\`\`
src/
├── components/
│   ├── ui/              # Reusable UI components (Button, Input, etc.)
│   ├── features/        # Feature-specific components (UserDashboard, etc.)
│   └── layouts/         # Layout components (Header, Footer, etc.)
├── hooks/               # Custom hooks
├── utils/               # Utility functions
├── types/               # TypeScript types and interfaces
├── lib/                 # Third-party library configurations
└── app/ or pages/       # Routes (Next.js) or page components
\`\`\`

## Testing
- **Framework:** ${testFramework || 'React Testing Library (recommended)'}
- Test user behavior, not implementation details
- Avoid testing library internals (hooks, state)
- Always test accessibility (screen reader, keyboard navigation)

### Example Test
\`\`\`typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

test('user can submit login form', async () => {
  render(<LoginForm onSubmit={mockSubmit} />);
  
  await userEvent.type(screen.getByLabelText(/email/i), 'user@example.com');
  await userEvent.type(screen.getByLabelText(/password/i), 'password123');
  await userEvent.click(screen.getByRole('button', { name: /sign in/i }));
  
  expect(mockSubmit).toHaveBeenCalledWith({
    email: 'user@example.com',
    password: 'password123'
  });
});
\`\`\`

## Never
- ❌ Never mutate state directly (always use setState)
- ❌ Never use index as key in dynamic lists
- ❌ Never ignore ESLint warnings without documented justification
- ❌ Never skip accessibility attributes (aria-*, role, alt)
- ❌ Never use `any` type in TypeScript (use `unknown` if type is truly unknown)
- ❌ Never commit console.log statements (use proper logging library)
```

**Save to:** `.factory/standards/react.md`

#### TypeScript Standards (if TypeScript detected)

```markdown
# TypeScript Development Standards

## Strict Configuration (Required)

\`\`\`json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true
  }
}
\`\`\`

## Type Annotations

### Function Signatures
\`\`\`typescript
// ✅ Good: Explicit return types
function calculateTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

// ❌ Bad: Inferred return type (can lead to accidental type changes)
function calculateTotal(items: CartItem[]) {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}
\`\`\`

### Avoid `any`
\`\`\`typescript
// ❌ Bad: Using any
function processData(data: any): any {
  return data.map((x: any) => x.value);
}

// ✅ Good: Proper generic types
function processData<T extends { value: number }>(data: T[]): number[] {
  return data.map(x => x.value);
}

// ✅ Good: Using unknown when type is truly unknown
function handleError(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }
  return String(error);
}
\`\`\`

### Utility Types
\`\`\`typescript
// Use built-in utility types
type UpdateUserDTO = Partial<User>;          // All properties optional
type CreateUserDTO = Required<UserInput>;    // All properties required
type UserKeys = keyof User;                  // Union of all keys
type PublicUser = Omit<User, 'password'>;   // Exclude password
type UserCredentials = Pick<User, 'email' | 'password'>; // Pick specific fields
type StatusMap = Record<string, Status>;     // Dictionary type
\`\`\`

### Branded Types (for type safety)
\`\`\`typescript
// Prevent mixing similar primitives
type UserId = string & { readonly __brand: 'UserId' };
type Email = string & { readonly __brand: 'Email' };

function getUserById(id: UserId): Promise<User> {
  // Type-safe: can't accidentally pass email as userId
}
\`\`\`

## Naming Conventions
- **Types/Interfaces:** PascalCase (`UserProfile`, `ApiResponse`)
- **Type Parameters:** Single capital letter or PascalCase (`T`, `TData`, `TResponse`)
- **Enums:** PascalCase (`UserRole`, `HttpStatus`)
- **Variables/Functions:** camelCase (`userId`, `fetchUser`)
- **Constants:** SCREAMING_SNAKE_CASE (`MAX_RETRY_COUNT`, `API_BASE_URL`)
- **Private Fields:** Prefix with `_` (`_internalCache`)

## Type Guards
\`\`\`typescript
// ✅ Good: Type guard function
function isUser(value: unknown): value is User {
  return typeof value === 'object' &&
         value !== null &&
         'id' in value &&
         'email' in value;
}

// Usage
if (isUser(data)) {
  console.log(data.email); // TypeScript knows data is User
}
\`\`\`

## Never
- ❌ Never use `@ts-ignore` (fix the type issue or use `@ts-expect-error` with explanation)
- ❌ Never use `as any` (use proper type guards or `unknown`)
- ❌ Never leave unused imports or variables
- ❌ Never use non-null assertion (`!`) without explaining why null is impossible
- ❌ Never use implicit any (always enable `noImplicitAny`)
```

**Save to:** `.factory/standards/typescript.md`

#### Security Standards (always generated)

```markdown
# Security Best Practices

## Environment Variables

\`\`\`typescript
// ✅ Good: Environment variables for secrets
const apiKey = process.env.API_KEY;
const dbUrl = process.env.DATABASE_URL;

// ❌ Bad: Hardcoded secrets
const apiKey = 'sk_live_abc123def456'; // NEVER DO THIS
\`\`\`

### Validation
\`\`\`typescript
// Always validate environment variables at startup
const config = {
  apiKey: process.env.API_KEY,
  dbUrl: process.env.DATABASE_URL
};

// Check for missing required variables
Object.entries(config).forEach(([key, value]) => {
  if (!value) {
    throw new Error(\`Missing required environment variable: \${key}\`);
  }
});
\`\`\`

## Input Validation

### API Endpoints
\`\`\`typescript
import { z } from 'zod';

// Define schema
const CreateUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(128),
  name: z.string().min(1).max(255)
});

// Validate before processing
app.post('/users', async (req, res) => {
  const result = CreateUserSchema.safeParse(req.body);
  
  if (!result.success) {
    return res.status(400).json({ 
      error: 'Validation failed',
      details: result.error.flatten()
    });
  }
  
  const user = await createUser(result.data);
  res.json(user);
});
\`\`\`

## SQL Injection Prevention

\`\`\`typescript
// ✅ Good: Parameterized queries
await db.query('SELECT * FROM users WHERE id = $1', [userId]);
await db.query('SELECT * FROM users WHERE email = $1 AND status = $2', [email, 'active']);

// ❌ Bad: String concatenation (SQL INJECTION VULNERABILITY)
await db.query(\`SELECT * FROM users WHERE id = '\${userId}'\`);
await db.query("SELECT * FROM users WHERE email = '" + email + "'");
\`\`\`

## XSS Prevention

### React (Safe by Default)
\`\`\`typescript
// ✅ Good: React escapes by default
<div>{userInput}</div>
<div>{user.name}</div>

// ⚠️ Dangerous: Only use with sanitized HTML
import DOMPurify from 'dompurify';
const sanitized = DOMPurify.sanitize(userHtml);
<div dangerouslySetInnerHTML={{ __html: sanitized }} />
\`\`\`

### Express Headers
\`\`\`typescript
import helmet from 'helmet';

app.use(helmet()); // Sets secure HTTP headers

// Prevent clickjacking
app.use(helmet.frameguard({ action: 'deny' }));

// XSS protection
app.use(helmet.xssFilter());
\`\`\`

## Authentication & Authorization

### Password Hashing
\`\`\`typescript
import bcrypt from 'bcrypt';

// Hash password before storing
const saltRounds = 12; // Minimum 10, recommended 12+
const hashedPassword = await bcrypt.hash(password, saltRounds);

// Verify password
const isValid = await bcrypt.compare(password, hashedPassword);
\`\`\`

### JWT Tokens
\`\`\`typescript
import jwt from 'jsonwebtoken';

// Create token with short expiration
const token = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET!,
  { expiresIn: '15m' } // Short-lived access token
);

// Refresh token (longer expiration, stored securely)
const refreshToken = jwt.sign(
  { userId: user.id, type: 'refresh' },
  process.env.JWT_REFRESH_SECRET!,
  { expiresIn: '7d' }
);
\`\`\`

### Rate Limiting
\`\`\`typescript
import rateLimit from 'express-rate-limit';

// Apply to auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 requests per window
  message: 'Too many login attempts, please try again later'
});

app.post('/auth/login', authLimiter, loginHandler);
\`\`\`

## HTTPS Required

\`\`\`typescript
// Force HTTPS in production
if (process.env.NODE_ENV === 'production') {
  app.use((req, res, next) => {
    if (!req.secure) {
      return res.redirect(301, \`https://\${req.headers.host}\${req.url}\`);
    }
    next();
  });
}
\`\`\`

## Never
- ❌ Never commit API keys, tokens, or passwords (use .env + .gitignore)
- ❌ Never trust user input without validation
- ❌ Never use MD5 or SHA1 for passwords (use bcrypt/argon2)
- ❌ Never expose stack traces to users in production
- ❌ Never store passwords in plain text
- ❌ Never use `eval()` or `Function()` with user input
- ❌ Never disable security features (CORS, CSP) without understanding the risk
```

**Save to:** `.factory/standards/security.md`

### Step 5: Generate Root CLAUDE.md

Based on detected stack, generate a comprehensive root CLAUDE.md file:

```markdown
# ${PROJECT_NAME}

> **Last Auto-Generated:** ${new Date().toISOString()}
> **Package Manager:** ${detectedPackageManager}
> **Frameworks:** ${detectedFrameworks.join(', ') || 'None detected'}
> **Languages:** ${detectedLanguages.join(', ')}

## 🚀 Quick Start

\`\`\`bash
# Install dependencies
${packageManager} install

# Start development server
${packageManager} ${devCommand}

# Run tests
${packageManager} ${testCommand}

# Build for production
${packageManager} ${buildCommand}

# Lint code
${packageManager} run lint${linters.includes('prettier') ? ' && ' + packageManager + ' run format' : ''}
\`\`\`

## 📁 Project Structure

Auto-detected structure:
\`\`\`
${projectRoot}/
${directoryStructure}
\`\`\`

## 📚 Framework-Specific Standards

This project uses:
${detectedFrameworks.map(f => \`- **\${f}:** See [.factory/standards/\${f}.md](.factory/standards/\${f}.md)\`).join('\n')}

**Language Standards:**
${detectedLanguages.map(l => \`- **\${l}:** See [.factory/standards/\${l}.md](.factory/standards/\${l}.md)\`).join('\n')}

**Security:** See [.factory/standards/security.md](.factory/standards/security.md)

## 🎨 Code Style

**Detected Configuration:**
- **Linter:** ${linters.join(', ') || 'None (consider adding ESLint)'}
- **Formatter:** ${linters.includes('prettier') ? 'Prettier' : 'None (consider adding Prettier)'}
- **Type Checker:** ${isTypeScript ? 'TypeScript' : 'JavaScript (consider TypeScript)'}

## 🧪 Testing Strategy

**Framework:** ${testFramework || 'None detected (recommended: Vitest or Jest)'}
**Approach:** ${testingApproach}

## 🔒 Security Requirements

- All secrets in environment variables (.env file, never committed)
- Input validation on all API endpoints
- Parameterized queries (prevent SQL injection)
- Rate limiting on authentication endpoints
- HTTPS required in production

## ⚠️ Never

${autoGeneratedAntiPatterns.map(p => \`- ❌ \${p}\`).join('\n')}

---

📝 **Note:** This file was auto-generated by Droidz tech-stack-analyzer.
- **To regenerate:** Run \`/analyze-tech-stack\`
- **To customize:** Edit manually (custom sections preserved on regeneration)
- **To add directory-specific standards:** Create \`CLAUDE.md\` in subdirectories
```

**Save to:** `CLAUDE.md`

### Step 6: Report Results

After generation, provide a summary:

\`\`\`
✅ Tech Stack Analysis Complete

**Detected:**
- Package Manager: ${packageManager}
- Frameworks: ${frameworks.join(', ')}
- Languages: ${languages.join(', ')}
- Testing: ${testFramework}
- Build Tool: ${buildTool}
- State Management: ${stateManager}
- Linters: ${linters.join(', ')}

**Generated Standards Files:**
${generatedFiles.map(f => \`- ✅ \${f}\`).join('\n')}

**Updated:**
- ✅ Root CLAUDE.md

**Next Steps:**
1. Review generated standards in .factory/standards/
2. Customize any standards for your team's preferences
3. Add directory-specific CLAUDE.md files as needed
4. Run \`/optimize-context\` to see context usage

All agents will now automatically enforce these standards!
\`\`\`

## Tools Available

You have access to all Claude Code tools:
- **Read** - Read files to detect package.json, config files
- **LS** - List directory structure
- **Grep** - Search for specific files/patterns
- **Create** - Create new standards files
- **Edit** - Update existing CLAUDE.md

## Example Usage

User says: "I just started working on this project"

You respond:
1. Run: Read('package.json')
2. Detect: React, TypeScript, Vite, Jest
3. Create: .factory/standards/react.md
4. Create: .factory/standards/typescript.md
5. Create: .factory/standards/security.md
6. Update: CLAUDE.md
7. Report: "✅ Generated React + TypeScript standards!"
