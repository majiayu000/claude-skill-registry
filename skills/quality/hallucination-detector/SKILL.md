---
name: hallucination-detector
description: Detect and prevent hallucinated technical decisions during feature work. Auto-trigger when suggesting technologies, frameworks, APIs, database schemas, or external services. Validates all tech decisions against docs/project/tech-stack.md (single source of truth). Blocks suggestions that violate documented architecture. Requires evidence/citation for all technical choices. Prevents wrong tech stack, duplicate entities, fake APIs, incompatible versions.
---

<objective>
The hallucination-detector skill prevents hallucinated technical decisions by validating all technology choices, API suggestions, database schemas, and architectural patterns against the project's documented tech stack and existing codebase.

Hallucinated technical decisions destroy projects:
- Suggesting React when project uses Vue (wrong framework)
- Creating duplicate User entity when one already exists (duplicate schema)
- Recommending fake npm packages that don't exist (non-existent dependencies)
- Proposing PostgreSQL functions not available in project's version (incompatible APIs)
- Suggesting AWS services when project uses Google Cloud (wrong cloud provider)
- Inventing API endpoints that don't exist in external service (fake APIs)

This skill acts as a reality checker that:
1. **Loads** project's tech stack from docs/project/tech-stack.md (single source of truth)
2. **Validates** all technical suggestions against documented choices
3. **Verifies** entities, APIs, packages exist in codebase or documentation
4. **Requires** evidence/citations for all technical claims
5. **Blocks** suggestions that violate documented architecture
6. **Corrects** hallucinations with actual project technology

The result: Zero hallucinated tech decisions, implementation matches architecture, code that actually works.
</objective>

<quick_start>
<trigger_pattern>
Auto-trigger when detecting these suggestion patterns:

**Technology suggestions**:
- "Use [framework/library]" → Validate against tech-stack.md
- "Install [npm package]" → Verify package exists, check compatibility
- "Import from [module]" → Verify module exists in dependencies

**API/Service suggestions**:
- "Call [API endpoint]" → Verify endpoint exists in API docs
- "Use [external service]" → Confirm service in tech-stack.md
- "Query [database function]" → Check function exists in DB version

**Schema suggestions**:
- "Create [Entity] model" → Check if entity already exists
- "Add [column] to [table]" → Verify table exists, column doesn't
- "Define [interface]" → Check for existing similar types

**Pattern suggestions**:
- "Follow [architecture pattern]" → Validate against system-architecture.md
- "Use [design pattern]" → Check if pattern aligns with project conventions
</trigger_pattern>

<basic_workflow>
**Step 1**: Detect technical suggestion
- AI: "Let's use Redux for state management"
- Detected: Framework suggestion (Redux)

**Step 2**: Load tech stack from docs/project/tech-stack.md
```markdown
# State Management
- **Library**: Zustand
- **Rationale**: Simpler than Redux, less boilerplate
```

**Step 3**: Validate suggestion against tech stack
- Suggested: Redux
- Documented: Zustand
- **Mismatch detected**: HALLUCINATION

**Step 4**: Block hallucinated suggestion
```
🚨 HALLUCINATION DETECTED

Suggested: Redux for state management
Reality: Project uses Zustand (documented in tech-stack.md)

Reason for Zustand (from tech-stack.md):
- Simpler than Redux
- Less boilerplate
- Already integrated in project

Corrected suggestion:
Use Zustand for state management (as documented)

Evidence: docs/project/tech-stack.md, line 23
```

**Step 5**: Provide correct suggestion
- AI: "I'll use Zustand for state management (project's documented choice)"
</basic_workflow>

<immediate_value>
**Without hallucination-detector**:
```
AI: "Let's use Redux for state management and Axios for HTTP"
Developer: *Implements Redux + Axios*
Code review: "Why Redux? We use Zustand. Why Axios? We use fetch wrapper."
Result: Wasted 3 hours, need to refactor entire implementation
```

**With hallucination-detector**:
```
AI: "Let's use Redux for state management"
Detector: "🚨 HALLUCINATION: Project uses Zustand, not Redux (tech-stack.md)"
AI: "Corrected: I'll use Zustand for state management"
Developer: *Implements with Zustand correctly*
Result: Correct implementation on first try, zero refactoring
```
</immediate_value>
</quick_start>

<workflow>
<step number="1">
**Load project's tech stack** (single source of truth)

Read and parse docs/project/tech-stack.md:

```markdown
# Technology Stack

## Frontend
- **Framework**: React 18.2
- **State Management**: Zustand 4.4
- **Routing**: React Router 6.x
- **HTTP Client**: Native fetch with custom wrapper
- **UI Library**: Tailwind CSS 3.x
- **Form Handling**: React Hook Form 7.x

## Backend
- **Runtime**: Node.js 20.x
- **Framework**: Express 4.18
- **Database**: PostgreSQL 15.2
- **ORM**: Prisma 5.x
- **Authentication**: JWT (jsonwebtoken)
- **Validation**: Zod 3.x

## Infrastructure
- **Cloud**: AWS
- **Hosting**: Vercel (frontend), Railway (backend)
- **Storage**: AWS S3
- **Database**: Supabase (managed PostgreSQL)
```

Parse into structured data:
```typescript
const techStack = {
  frontend: {
    framework: { name: 'React', version: '18.2' },
    stateManagement: { name: 'Zustand', version: '4.4' },
    routing: { name: 'React Router', version: '6.x' },
    // ...
  },
  backend: {
    runtime: { name: 'Node.js', version: '20.x' },
    framework: { name: 'Express', version: '4.18' },
    database: { name: 'PostgreSQL', version: '15.2' },
    // ...
  },
  infrastructure: {
    cloud: 'AWS',
    hosting: { frontend: 'Vercel', backend: 'Railway' },
    // ...
  }
};
```
</step>

<step number="2">
**Detect technical suggestion in conversation**

Pattern matching for technical claims:

**Framework/library suggestions**:
```
- "use React" → Extract: { type: 'framework', name: 'React' }
- "install redux" → Extract: { type: 'library', name: 'redux', category: 'state-management' }
- "import axios" → Extract: { type: 'library', name: 'axios', category: 'http-client' }
```

**API endpoint suggestions**:
```
- "call GET /api/users" → Extract: { type: 'api-endpoint', method: 'GET', path: '/api/users' }
- "Stripe API: createPaymentIntent" → Extract: { type: 'external-api', service: 'Stripe', method: 'createPaymentIntent' }
```

**Database schema suggestions**:
```
- "create User model" → Extract: { type: 'model', name: 'User' }
- "add email column to users" → Extract: { type: 'column', table: 'users', column: 'email' }
- "use ARRAY_AGG function" → Extract: { type: 'db-function', name: 'ARRAY_AGG' }
```

**Cloud service suggestions**:
```
- "use Google Cloud Storage" → Extract: { type: 'cloud-service', provider: 'Google Cloud', service: 'Storage' }
- "deploy to AWS Lambda" → Extract: { type: 'cloud-service', provider: 'AWS', service: 'Lambda' }
```

See [references/detection-patterns.md](references/detection-patterns.md) for complete patterns.
</step>

<step number="3">
**Validate suggestion against tech stack**

Compare suggestion with documented choices:

**Framework validation**:
```typescript
function validateFramework(suggested: string): ValidationResult {
  const documented = techStack.frontend.framework.name;

  if (suggested.toLowerCase() !== documented.toLowerCase()) {
    return {
      valid: false,
      severity: 'CRITICAL',
      message: `Suggested ${suggested}, but project uses ${documented}`,
      evidence: 'docs/project/tech-stack.md, line 5'
    };
  }

  return { valid: true };
}
```

**Library validation**:
```typescript
function validateLibrary(category: string, suggested: string): ValidationResult {
  const documented = techStack.frontend[category]?.name;

  if (!documented) {
    return {
      valid: false,
      severity: 'HIGH',
      message: `No documented choice for ${category}. Verify before proceeding.`,
      action: 'CHECK_PACKAGE_JSON'
    };
  }

  if (suggested.toLowerCase() !== documented.toLowerCase()) {
    return {
      valid: false,
      severity: 'CRITICAL',
      message: `Suggested ${suggested}, but project uses ${documented} for ${category}`,
      evidence: 'docs/project/tech-stack.md'
    };
  }

  return { valid: true };
}
```

**Version validation**:
```typescript
function validateVersion(lib: string, suggestedVersion: string): ValidationResult {
  const documented = findLibraryVersion(lib);

  if (documented && !isCompatible(suggestedVersion, documented)) {
    return {
      valid: false,
      severity: 'HIGH',
      message: `Suggested ${lib}@${suggestedVersion}, but project uses ${lib}@${documented}`,
      action: 'USE_DOCUMENTED_VERSION'
    };
  }

  return { valid: true };
}
```
</step>

<step number="4">
**Verify entity/API existence in codebase**

Check if suggested entities already exist:

**Model existence check**:
```typescript
async function doesModelExist(modelName: string): Promise<boolean> {
  // Check Prisma schema
  const schemaContent = await readFile('prisma/schema.prisma');
  const modelRegex = new RegExp(`model ${modelName}\\s*{`, 'i');
  if (schemaContent.match(modelRegex)) {
    return true;
  }

  // Check TypeScript interfaces
  const results = await grep(`interface ${modelName}`, '**/*.ts');
  return results.length > 0;
}

// Usage
if (await doesModelExist('User')) {
  return {
    valid: false,
    severity: 'CRITICAL',
    message: 'User model already exists in prisma/schema.prisma',
    action: 'REUSE_EXISTING_MODEL'
  };
}
```

**API endpoint verification**:
```typescript
async function doesEndpointExist(method: string, path: string): Promise<boolean> {
  const pattern = `router\\.${method.toLowerCase()}\\(['"\`]${path}`;
  const results = await grep(pattern, '**/routes/**/*.ts');
  return results.length > 0;
}
```

**External service verification**:
```typescript
async function isExternalServiceConfigured(service: string): Promise<boolean> {
  // Check environment variables
  const envContent = await readFile('.env.example');
  const serviceEnvVars = {
    'Stripe': 'STRIPE_',
    'SendGrid': 'SENDGRID_',
    'AWS S3': 'AWS_'
  };

  const prefix = serviceEnvVars[service];
  if (prefix) {
    return envContent.includes(prefix);
  }

  // Check package.json
  const pkg = await readJSON('package.json');
  const servicePkg = {
    'Stripe': 'stripe',
    'SendGrid': '@sendgrid/mail'
  };

  return pkg.dependencies?.[servicePkg[service]] !== undefined;
}
```
</step>

<step number="5">
**Require evidence for technical claims**

Every technical suggestion must be backed by evidence:

**Package existence**:
```typescript
async function verifyPackageExists(packageName: string): Promise<Evidence> {
  try {
    // Query npm registry
    const response = await fetch(`https://registry.npmjs.org/${packageName}`);

    if (response.status === 404) {
      return {
        exists: false,
        message: `Package '${packageName}' does not exist on npm`,
        severity: 'CRITICAL'
      };
    }

    const data = await response.json();
    return {
      exists: true,
      latestVersion: data['dist-tags'].latest,
      description: data.description,
      url: `https://www.npmjs.com/package/${packageName}`
    };
  } catch (error) {
    return {
      exists: false,
      message: `Could not verify package '${packageName}'`,
      severity: 'HIGH',
      action: 'VERIFY_MANUALLY'
    };
  }
}
```

**API documentation verification**:
```typescript
async function verifyAPIEndpoint(service: string, endpoint: string): Promise<Evidence> {
  const apiDocs = {
    'Stripe': 'https://stripe.com/docs/api',
    'GitHub': 'https://docs.github.com/rest'
  };

  const docsUrl = apiDocs[service];
  if (!docsUrl) {
    return {
      verified: false,
      message: `No API docs configured for ${service}`,
      action: 'PROVIDE_DOCUMENTATION_LINK'
    };
  }

  // For now, require manual verification
  return {
    verified: 'MANUAL_REQUIRED',
    message: `Verify ${endpoint} exists in ${service} API docs`,
    docsUrl: docsUrl
  };
}
```

**Database function verification**:
```typescript
function verifyDatabaseFunction(dbType: string, functionName: string, version: string): Evidence {
  const postgresqlFunctions = {
    '15.2': ['ARRAY_AGG', 'STRING_AGG', 'JSON_BUILD_OBJECT', 'COALESCE'],
    '14.0': ['ARRAY_AGG', 'STRING_AGG', 'JSON_BUILD_OBJECT'],
    '13.0': ['ARRAY_AGG', 'STRING_AGG']
  };

  if (dbType === 'PostgreSQL') {
    const availableFunctions = postgresqlFunctions[version] || [];

    if (!availableFunctions.includes(functionName)) {
      return {
        exists: false,
        message: `Function '${functionName}' not available in PostgreSQL ${version}`,
        severity: 'HIGH',
        alternatives: availableFunctions
      };
    }
  }

  return { exists: true };
}
```
</step>

<step number="6">
**Block or correct hallucinated suggestions**

Based on validation results, take action:

**CRITICAL hallucination** (wrong tech stack):
```
🚨 HALLUCINATION BLOCKED

Suggested: Redux for state management
Reality: Project uses Zustand (tech-stack.md, line 7)

Why this is wrong:
- Redux is NOT in project dependencies (package.json)
- Zustand is already configured and used throughout codebase
- Mixing state management libraries creates inconsistency

Corrected implementation:
Use Zustand as documented:

import { create } from 'zustand';

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 }))
}));

Evidence:
- Tech stack: docs/project/tech-stack.md, line 7
- Example usage: src/stores/userStore.ts
- Dependencies: package.json (zustand@4.4.0)
```

**HIGH hallucination** (duplicate entity):
```
⚠️ HALLUCINATION DETECTED

Suggested: Create User model
Reality: User model already exists

Existing model: prisma/schema.prisma, lines 15-25

model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String
  createdAt DateTime @default(now())
}

Action: REUSE existing User model instead of creating duplicate

If you need additional fields, extend existing model:
- Add fields to existing User model
- Or create related model (UserProfile, UserSettings)
```

**MEDIUM hallucination** (undocumented choice):
```
ℹ️ VERIFICATION REQUIRED

Suggested: Axios for HTTP requests
Status: Not documented in tech-stack.md

Checking codebase...
- Found: Custom fetch wrapper in src/lib/api.ts
- Not found: Axios in package.json

Recommendation: Use existing fetch wrapper (project convention)

If Axios is needed:
1. Update tech-stack.md to document choice
2. Add rationale for using Axios over fetch
3. Get team approval
4. Then proceed with implementation
```
</step>
</workflow>

<detection_rules>
<framework_hallucinations>
**Common patterns**:
```
Hallucinated → Actual (from tech-stack.md)
----------------------------------------------
Vue → React
Redux → Zustand
Axios → fetch wrapper
Styled Components → Tailwind CSS
Jest → Vitest
Angular → React
MobX → Zustand
```

**Detection**:
```
Suggestion: "use Vue for the frontend"
Tech stack: "Framework: React 18.2"
Severity: CRITICAL (different framework)
```

**Correction**:
```
Use React (project's documented framework):

import React from 'react';

function MyComponent() {
  return <div>Hello</div>;
}
```
</framework_hallucinations>

<dependency_hallucinations>
**Non-existent packages**:
```
Hallucinated packages (don't exist on npm):
- react-hooks-library (meant: react-use)
- express-middleware (meant: specific middleware)
- database-orm (meant: Prisma/TypeORM)
```

**Detection**:
```typescript
const packageVerification = await npmRegistry.get('react-hooks-library');
// 404 Not Found

return {
  exists: false,
  severity: 'CRITICAL',
  message: 'Package does not exist on npm',
  suggestion: 'Did you mean "react-use"?'
};
```

**Version incompatibilities**:
```
Suggested: React 17.x
Project uses: React 18.2 (tech-stack.md)
Issue: Hooks API differences, breaking changes

Corrected: Use React 18.2 (project version)
```
</dependency_hallucinations>

<api_hallucinations>
**Fake API endpoints**:
```
Hallucinated → Reality
----------------------------------------------
GET /api/user/profile → GET /api/user/:id (check routes)
POST /api/auth/register → POST /api/auth/signup (check routes)
Stripe.charges.create → Stripe.paymentIntents.create (check Stripe docs)
```

**Detection**:
```typescript
const endpointExists = await doesEndpointExist('GET', '/api/user/profile');
// false

const actualEndpoints = await grep('router.get.*user', '**/routes/*.ts');
// Found: GET /api/user/:id

return {
  exists: false,
  severity: 'HIGH',
  message: 'Endpoint does not exist',
  actual: 'GET /api/user/:id',
  evidence: 'routes/user.ts, line 15'
};
```

**External API hallucinations**:
```
Service: Stripe
Hallucinated method: Stripe.users.create()
Reality: Stripe has Customers, not Users
Actual method: Stripe.customers.create()

Evidence: https://stripe.com/docs/api/customers/create
```
</api_hallucinations>

<schema_hallucinations>
**Duplicate entities**:
```
Suggested: Create User model
Reality: User model exists (prisma/schema.prisma, line 15)

Action: BLOCK duplicate entity creation
```

**Non-existent tables**:
```
Suggested: Add column to 'accounts' table
Reality: Table is 'users', not 'accounts' (check schema)

Correction: users table (actual table name)
```

**Database function hallucinations**:
```
Suggested: Use JSON_ARRAYAGG() (MySQL function)
Project uses: PostgreSQL 15.2
Actual function: ARRAY_AGG() (PostgreSQL equivalent)

Evidence:
- PostgreSQL 15.2 docs
- tech-stack.md: Database: PostgreSQL 15.2
```
</schema_hallucinations>

<cloud_service_hallucinations>
**Wrong cloud provider**:
```
Suggested: Google Cloud Storage
Tech stack: AWS (S3 for storage)

Correction: Use AWS S3 (project's cloud provider)
Evidence: tech-stack.md, infrastructure section
```

**Unavailable services**:
```
Suggested: Deploy to AWS Lambda
Project hosting: Vercel (frontend), Railway (backend)

Reality: Project doesn't use Lambda
Correction: Deploy backend to Railway (documented hosting)
```
</cloud_service_hallucinations>

<pattern_hallucinations>
**Architecture violations**:
```
Suggested: Add GraphQL endpoint
Tech stack: REST API (Express)
System architecture: RESTful architecture (system-architecture.md)

Correction: Implement as REST endpoint (project pattern)
```

**Convention violations**:
```
Suggested: Create service in /lib/services/
Convention: Services in /src/services/ (check existing code)

Correction: /src/services/ (project convention)
```
</pattern_hallucinations>
</detection_rules>

<auto_trigger_conditions>
<when_to_trigger>
**Technology suggestions**:
- "use [framework/library]"
- "install [package]"
- "import [module]"

**Implementation suggestions**:
- "create [model/entity]"
- "add [column/field]"
- "call [API endpoint]"

**Architecture suggestions**:
- "deploy to [service]"
- "use [cloud provider]"
- "follow [pattern]"

**Critical moments**:
- /plan phase (design decisions)
- /tasks phase (task breakdown with tech choices)
- /implement phase (actual code writing)
- Code review (validating implementation)
</when_to_trigger>

<when_not_to_trigger>
**Non-technical discussions**:
- User requirements
- Business logic
- UI/UX design
- Project management

**Documented exploration**:
- "Should we consider [alternative]?" (exploratory, not prescriptive)
- "What if we used [tech]?" (question, not suggestion)
</when_not_to_trigger>

<proactive_validation>
**Before /plan phase**:
```typescript
// Pre-load tech stack
const techStack = await loadTechStack('docs/project/tech-stack.md');

// Cache for phase
cache.set('tech-stack', techStack, { ttl: '1-hour' });
```

**During implementation**:
```typescript
// Before suggesting framework
if (suggestion.includes('use React')) {
  const validated = validateFramework('React');
  if (!validated.valid) {
    blockSuggestion(validated.message);
  }
}

// Before suggesting package
if (suggestion.includes('install')) {
  const pkg = extractPackageName(suggestion);
  const exists = await verifyPackageExists(pkg);
  if (!exists.exists) {
    blockSuggestion(`Package ${pkg} does not exist`);
  }
}

// Before creating entity
if (suggestion.includes('create') && suggestion.includes('model')) {
  const entity = extractEntityName(suggestion);
  const duplicate = await doesModelExist(entity);
  if (duplicate) {
    blockSuggestion(`${entity} model already exists`);
  }
}
```
</proactive_validation>
</auto_trigger_conditions>

<examples>
<example name="framework-hallucination">
**Scenario**: AI suggests wrong framework

**Conversation**:
```
User: "Add state management for user authentication"
AI: "I'll use Redux to manage authentication state"
```

**Hallucination detection**:
```typescript
// Load tech stack
const techStack = await loadTechStack('docs/project/tech-stack.md');
// → State Management: Zustand 4.4

// Detect suggestion
const suggestion = extractTech("use Redux");
// → { type: 'library', name: 'Redux', category: 'state-management' }

// Validate
const validation = validateLibrary('state-management', 'Redux');
// → { valid: false, documented: 'Zustand', severity: 'CRITICAL' }
```

**Blocked response**:
```
🚨 HALLUCINATION BLOCKED

Suggested: Redux for state management
Reality: Project uses Zustand (docs/project/tech-stack.md)

Why Zustand (from tech-stack.md):
- Simpler API than Redux
- Less boilerplate
- Better TypeScript support
- Already integrated throughout codebase

Corrected implementation:

import { create } from 'zustand';

interface AuthStore {
  user: User | null;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  login: async (credentials) => {
    const user = await authService.login(credentials);
    set({ user });
  },
  logout: () => set({ user: null })
}));

Evidence:
- Tech stack: docs/project/tech-stack.md, line 7
- Example: src/stores/userStore.ts
- Dependencies: package.json
```
</example>

<example name="duplicate-entity-hallucination">
**Scenario**: AI tries to create duplicate model

**Conversation**:
```
User: "Create a user authentication system"
AI: "First, I'll create the User model in Prisma schema"
```

**Hallucination detection**:
```typescript
// Check if User model exists
const exists = await doesModelExist('User');
// → true (found in prisma/schema.prisma)

// Read existing model
const schemaContent = await readFile('prisma/schema.prisma');
const userModel = extractModel(schemaContent, 'User');
```

**Blocked response**:
```
⚠️ HALLUCINATION DETECTED

Suggested: Create User model
Reality: User model already exists

Existing model (prisma/schema.prisma, lines 15-25):

model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String?
  password  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

Action: REUSE existing User model

For authentication, extend with:
- Add 'role' field if needed
- Create Session model (related to User)
- Add authentication methods to UserService

Do NOT create duplicate User model.
```
</example>

<example name="fake-api-hallucination">
**Scenario**: AI suggests non-existent API

**Conversation**:
```
User: "Integrate Stripe payments"
AI: "Call Stripe.charges.create() to create a payment"
```

**Hallucination detection**:
```typescript
// Verify Stripe API method
const stripeVersion = await getPackageVersion('stripe');
// → 14.0.0

// Check Stripe docs
const method = 'Stripe.charges.create';
const deprecated = isStripeMethodDeprecated(method, stripeVersion);
// → true (deprecated in favor of PaymentIntents API)
```

**Blocked response**:
```
🚨 HALLUCINATION DETECTED

Suggested: Stripe.charges.create()
Reality: Charges API is legacy (deprecated)
Current API: Payment Intents API

Modern approach (Stripe 14.x):

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

// Create PaymentIntent (NOT charge)
const paymentIntent = await stripe.paymentIntents.create({
  amount: 1000,
  currency: 'usd',
  payment_method_types: ['card']
});

Why PaymentIntents over Charges:
- Better error handling
- Supports 3D Secure authentication
- More flexible payment flows
- Required for SCA compliance

Evidence:
- Stripe docs: https://stripe.com/docs/payments/payment-intents
- Migration guide: https://stripe.com/docs/payments/payment-intents/migration
- Project Stripe version: package.json (stripe@14.0.0)
```
</example>

<example name="version-incompatibility-hallucination">
**Scenario**: AI suggests incompatible version

**Conversation**:
```
User: "Add React hooks for data fetching"
AI: "Use React.useFetch() hook"
```

**Hallucination detection**:
```typescript
// Check React version
const reactVersion = await getPackageVersion('react');
// → 18.2.0

// Verify hook exists
const hookExists = doesReactHookExist('useFetch', reactVersion);
// → false (useFetch doesn't exist in React)
```

**Blocked response**:
```
🚨 HALLUCINATION DETECTED

Suggested: React.useFetch() hook
Reality: useFetch() does not exist in React

React 18.2 built-in hooks:
- useState, useEffect, useContext
- useReducer, useCallback, useMemo
- useRef, useImperativeHandle
- useLayoutEffect, useDebugValue
- useId, useTransition, useDeferredValue

For data fetching, project uses:
- Custom hook: src/hooks/useFetch.ts
- Or: React Query (if installed)

Corrected implementation:

import { useFetch } from '@/hooks/useFetch';

function MyComponent() {
  const { data, loading, error } = useFetch('/api/users');

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return <div>{data.map(...)}</div>;
}

Evidence:
- React docs: https://react.dev/reference/react
- Custom hook: src/hooks/useFetch.ts
- React version: package.json (react@18.2.0)
```
</example>
</examples>

<anti_patterns>
<anti_pattern name="ignoring-tech-stack-docs">
**Problem**: Making suggestions without consulting tech-stack.md

**Bad approach**:
```
AI: "I'll use Redux for state management"
(Didn't check tech-stack.md first)
```

**Correct approach**:
```
AI: *Loads docs/project/tech-stack.md*
AI: "Tech stack specifies Zustand for state management. I'll use Zustand."
```

**Rule**: ALWAYS load and validate against tech-stack.md before suggesting technology.
</anti_pattern>

<anti_pattern name="assuming-package-exists">
**Problem**: Suggesting packages without verification

**Bad approach**:
```
AI: "Install react-super-hooks library"
(Package doesn't exist)
```

**Correct approach**:
```
AI: *Verifies package on npm registry*
AI: "Package 'react-super-hooks' not found. Did you mean 'react-use'?"
```

**Rule**: Verify package existence before suggesting installation.
</anti_pattern>

<anti_pattern name="creating-duplicate-entities">
**Problem**: Creating entities that already exist

**Bad approach**:
```
AI: "Create User model"
(User model already exists in schema)
```

**Correct approach**:
```
AI: *Searches codebase for User model*
AI: "User model already exists (prisma/schema.prisma). I'll reuse it."
```

**Rule**: Check for existing entities before creating new ones.
</anti_pattern>

<anti_pattern name="mixing-tech-stacks">
**Problem**: Suggesting technologies from different ecosystems

**Bad approach**:
```
Project uses: React
AI suggests: Vue components alongside React
```

**Correct approach**:
```
AI: "Project uses React. All components must be React components."
```

**Rule**: Maintain consistency with documented tech stack.
</anti_pattern>

<anti_pattern name="hallucinating-apis">
**Problem**: Inventing API methods that don't exist

**Bad approach**:
```
AI: "Call Stripe.users.create()"
(Stripe has customers, not users)
```

**Correct approach**:
```
AI: *Checks Stripe API documentation*
AI: "Use Stripe.customers.create() (Stripe uses 'customers' not 'users')"
```

**Rule**: Verify external API methods against official documentation.
</anti_pattern>
</anti_patterns>

<validation>
<success_indicators>
Hallucination-detector successfully applied when:

1. **Zero tech stack violations**: All suggestions match tech-stack.md
2. **Zero duplicate entities**: No redundant models/schemas created
3. **Zero fake packages**: All suggested packages exist and are verified
4. **Zero API hallucinations**: All API calls verified against documentation
5. **Evidence required**: Every technical claim backed by citation
6. **Proactive detection**: Triggers before suggestion, not after implementation
7. **Clear corrections**: Hallucinations blocked with correct alternatives provided
</success_indicators>

<metrics>
Track hallucination prevention:

**Detection metrics**:
```typescript
{
  totalSuggestions: 150,
  hallucinationsDetected: 12,
  hallucinationRate: 0.08,  // 8%
  byType: {
    wrongFramework: 3,
    duplicateEntity: 4,
    fakePackage: 2,
    fakeAPI: 3
  }
}
```

**Prevention metrics**:
```typescript
{
  hallucinationsBlocked: 12,
  hallucinationsCorrected: 12,
  implementationErrors: 0,  // No wrong tech made it to code
  refactorsAvoided: 12  // Would have needed refactoring
}
```

**Time savings**:
```typescript
{
  avgRefactorTime: 180,  // 3 hours per hallucination
  refactorsAvoided: 12,
  timeSaved: 2160,  // 36 hours saved
  timeSavedHours: 36
}
```
</metrics>

<validation_checklist>
Before allowing technical suggestion:

**Technology**:
- [ ] Validated against tech-stack.md
- [ ] Package exists on npm (if applicable)
- [ ] Version compatible with project
- [ ] No mixing of incompatible tech

**Entities/Schema**:
- [ ] Checked for duplicates in codebase
- [ ] Verified table/model names
- [ ] Confirmed database functions exist in project's DB version

**APIs**:
- [ ] Endpoint exists in routes (internal API)
- [ ] Method exists in official docs (external API)
- [ ] API version compatible

**Evidence**:
- [ ] Citation provided (file path, line number, or URL)
- [ ] Can be verified by developer
- [ ] Comes from authoritative source
</validation_checklist>
</validation>

<reference_guides>
For deeper topics, see reference files:

**Detection patterns**: [references/detection-patterns.md](references/detection-patterns.md)
- Complete regex patterns for all hallucination types
- Extraction logic for technical suggestions
- Confidence scoring

**Tech stack validation**: [references/tech-stack-validation.md](references/tech-stack-validation.md)
- Parsing tech-stack.md format
- Version compatibility checking
- Framework-specific validations

**Evidence requirements**: [references/evidence-requirements.md](references/evidence-requirements.md)
- What constitutes valid evidence
- Citation formats
- Verification procedures
</reference_guides>

<success_criteria>
The hallucination-detector skill is successfully applied when:

1. **Loaded tech stack**: docs/project/tech-stack.md loaded and parsed at workflow start
2. **Validated all suggestions**: Every tech suggestion checked against tech stack
3. **Verified existence**: Packages, APIs, entities verified before suggesting
4. **Required evidence**: Every claim backed by file path, line number, or URL
5. **Blocked violations**: CRITICAL hallucinations blocked immediately
6. **Corrected suggestions**: Wrong suggestions replaced with correct alternatives
7. **Zero implementation errors**: No hallucinated tech makes it to code
8. **Prevented refactoring**: No wasted time implementing wrong technology
9. **Maintained consistency**: All code follows documented architecture
10. **Measurable impact**: Metrics show hallucinations detected and prevented
</success_criteria>
