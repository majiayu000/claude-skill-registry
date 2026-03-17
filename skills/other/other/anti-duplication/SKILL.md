---
name: anti-duplication
description: Before implementing new code (endpoints, components, services, models), search the codebase for existing patterns to reuse. Prevent code duplication by finding and suggesting similar implementations. Auto-trigger when user asks to create, implement, add, or build new functionality.
---

<objective>
The anti-duplication skill enforces the DRY (Don't Repeat Yourself) principle by proactively searching the codebase for existing patterns before writing new code. This prevents code duplication, reduces maintenance burden, and promotes code reuse.

Code duplication creates maintenance nightmares:
- Bug fixes must be applied in multiple places
- Features evolve inconsistently across duplicates
- Refactoring becomes exponentially harder
- Codebase grows unnecessarily large
- Onboarding takes longer (more code to learn)

This skill transforms "implement X" requests into a two-phase workflow:
1. **Search phase**: Find existing similar implementations (endpoints, components, services, models)
2. **Reuse or justify**: Either reuse/extend existing code OR justify why new implementation is necessary

The result: Codebases stay DRY, maintainable, and consistent.
</objective>

<quick_start>
<trigger_pattern>
When user says "create", "implement", "add", or "build" new functionality, **IMMEDIATELY** search for existing similar code before writing anything new.

**Trigger phrases**:
- "Create a new API endpoint for..."
- "Implement a component that..."
- "Add a service to handle..."
- "Build a model for..."
- "Write a function that..."
</trigger_pattern>

<basic_workflow>
**Step 1**: Extract search keywords from request
- User: "Create an API endpoint to fetch user profile"
- Keywords: "API endpoint", "fetch", "user", "profile", "GET"

**Step 2**: Search codebase for similar patterns

**PRIMARY: Semantic search (mgrep)**
- mgrep for: "API endpoints that fetch user data", "profile retrieval handlers"
- Finds similar implementations by meaning, not exact text

**SECONDARY: Literal search (Grep/Glob)**
- Grep for: "router.get", "app.get", "/api/user", "profile"
- Glob for: "**/*user*.ts", "**/*profile*.ts", "**/routes/**"

**Step 3**: Analyze findings
- Found 3 similar endpoints: GET /api/user/:id, GET /api/user/settings, GET /api/admin/users
- All use same auth middleware, validation pattern, error handling

**Step 4**: Present reuse options
- **Option A**: Extend existing GET /api/user/:id to include profile data
- **Option B**: Create new endpoint using same patterns as existing user endpoints
- **Option C**: Justify why completely new approach is needed

**Step 5**: Implement chosen option (with existing patterns as template)
</basic_workflow>

<immediate_value>
**Before anti-duplication skill**:
User: "Create an API endpoint to update user email"
Claude: *Writes new endpoint from scratch with different auth, validation, error handling*
Result: 5th variation of similar endpoint, inconsistent patterns

**After anti-duplication skill**:
User: "Create an API endpoint to update user email"
Claude: *Searches codebase, finds 4 existing user endpoints with consistent patterns*
Claude: "Found 4 similar user endpoints. They all use: authMiddleware, validateUserInput, standardErrorHandler. I'll create the new endpoint following this established pattern."
Result: Consistent implementation, reused middleware, maintainable code
</immediate_value>
</quick_start>

<workflow>
<step number="1">
**Parse the implementation request**

Extract key information:
- **Type**: What are they building? (endpoint, component, service, model, function, utility)
- **Domain**: What business domain? (user, product, order, payment, auth)
- **Operation**: What action? (create, read, update, delete, fetch, validate, transform)
- **Technology**: What stack? (React, Express, TypeScript, SQL, GraphQL)

Example parsing:
```
Request: "Create a React component to display product details"

Parsed:
- Type: React component
- Domain: Product
- Operation: Display/render
- Technology: React, TypeScript (likely)
```
</step>

<step number="2">
**Generate search strategies**

Create multiple search approaches to maximize coverage:

**PRIMARY: Semantic search (mgrep)**
Use mgrep FIRST for pattern discovery - finds similar code by meaning:
- "components that display product information"
- "services that handle email sending"
- "validation logic for user input"
- "error handling patterns in API routes"

mgrep finds UserCard, ProductCard, ProfileView when searching for "display user details" even if names don't match.

**SECONDARY: Literal searches (when mgrep insufficient)**

**A. Keyword-based searches** (Grep):
- Core domain terms: "product", "Product", "PRODUCT"
- Operation terms: "display", "render", "show", "view"
- Technology patterns: "React.FC", "function Component", "const.*=.*=>"

**B. File pattern searches** (Glob):
- Domain files: "**/*product*.tsx", "**/*Product*.tsx"
- Location patterns: "**/components/**/*Detail*.tsx", "**/components/**/Product*"
- Type-specific: "**/models/Product*", "**/services/product*"

**C. Structural searches** (Grep with regex):
- Class definitions: "class.*Product"
- Function exports: "export (function|const).*product"
- API patterns: "router\.(get|post|put|delete).*product"

See [references/search-strategies.md](references/search-strategies.md) for detailed patterns.
</step>

<step number="3">
**Execute searches in parallel**

Run multiple searches concurrently for speed:

**Phase 1: Semantic search (mgrep)**
```
mgrep "components that display product details"
mgrep "detail card patterns for entities"
```
Reviews results - if sufficient matches found, skip to Step 4.

**Phase 2: Literal searches (if needed)**
1. Grep: "product" in **/*.tsx (find all product-related components)
2. Grep: "ProductDetail" (find similar detail components)
3. Glob: "**/components/**/Product*.tsx" (find product component files)
4. Grep: "interface.*Product" (find product type definitions)
5. Grep: "display.*product.*props" (find rendering logic)

All searches run in parallel (see parallel-execution-optimizer skill).

**Time**: ~5-10 seconds for comprehensive search across large codebase.
</step>

<step number="4">
**Analyze search results**

Categorize findings:

**Exact matches**: Nearly identical implementations
- Example: Found ProductDetailCard, ProductSummaryCard, ProductPreviewCard
- All render product data with similar structure

**Close matches**: Similar domain, different operation
- Example: Found ProductList (renders multiple products)
- Could extract shared rendering logic

**Pattern matches**: Similar operation, different domain
- Example: Found UserDetailCard, OrderDetailCard
- Consistent pattern: DetailCard component for entities

**Anti-patterns**: What NOT to do
- Example: Found ProductView with 500-line monolithic component
- Shows what to avoid when implementing new component

Rank by relevance:
1. Exact matches (highest reuse potential)
2. Close matches (partial reuse)
3. Pattern matches (pattern consistency)
4. Anti-patterns (learn from mistakes)
</step>

<step number="5">
**Present reuse options**

Provide user with informed choices:

**Option A: Reuse existing implementation**
"Found ProductDetailCard component that already displays product details. Can we use this directly or does your use case differ?"

**Option B: Extend existing implementation**
"Found ProductSummaryCard (displays basic product info). We can extend it to show full details rather than creating a new component."

**Option C: Extract shared pattern**
"Found 3 similar DetailCard components (Product, User, Order). We can create a generic DetailCard<T> and use it for products."

**Option D: Follow established pattern**
"Found consistent pattern across User/Order detail components. I'll create ProductDetailCard following the same structure for consistency."

**Option E: Justify new approach**
"Existing ProductView is a 500-line monolith with poor separation of concerns. I'll create a new modular ProductDetailCard instead. Here's why the new approach is necessary: [justification]"

Always present Options A-D before suggesting new implementation.
</step>

<step number="6">
**Implement with reuse**

Based on chosen option:

**If reusing**: Import and use existing code
```typescript
import { ProductDetailCard } from '@/components/products/ProductDetailCard';

// Use directly
<ProductDetailCard product={product} />
```

**If extending**: Modify existing component
```typescript
// Extend ProductSummaryCard with additional fields
// Before: Shows name, price
// After: Shows name, price, description, images
```

**If extracting pattern**: Create generic abstraction
```typescript
// Create DetailCard<T> generic component
// Reuse for Product, User, Order
```

**If following pattern**: Use existing as template
```typescript
// Copy structure from UserDetailCard
// Adapt for Product domain
// Maintain consistency (same props pattern, same styling, same error handling)
```

**If new approach**: Document justification
```typescript
/**
 * ProductDetailCard
 *
 * NEW IMPLEMENTATION (does not reuse ProductView)
 *
 * Justification:
 * - Existing ProductView is 500-line monolith
 * - Poor separation of concerns (mixing data fetching, rendering, business logic)
 * - Hard to test and maintain
 *
 * This implementation:
 * - Separates concerns (presentational component only)
 * - Reusable across product catalog and cart
 * - Follows established DetailCard pattern from User/Order
 */
```
</step>
</workflow>

<search_strategies>
<semantic_search_first>
**Always start with mgrep for semantic discovery:**

mgrep finds code by meaning, not exact text. This catches similar implementations even when naming conventions differ.

**mgrep query patterns by artifact type:**

| Artifact | mgrep Query Examples |
|----------|---------------------|
| API Endpoint | "endpoints that handle user authentication", "API routes for data retrieval" |
| Component | "components that display lists", "form components with validation" |
| Service | "services that send emails", "business logic for order processing" |
| Model | "database models for user data", "entities with timestamps" |
| Utility | "helper functions for date formatting", "validation utilities" |

**When to fall back to Grep/Glob:**
- mgrep returns no results (niche terminology)
- Need exact text match (specific function name)
- File pattern search (find all *.test.ts files)
</semantic_search_first>

<by_artifact_type>
Different artifact types require different search strategies.

**API Endpoints** (Express, Fastify, NestJS):
```
Keywords: router.get, router.post, app.get, @Get, @Post, /api/
Patterns: HTTP methods + route paths + domain terms
Files: **/routes/**, **/controllers/**, **/api/**

Example search for "user profile endpoint":
- Grep: "router\.(get|put).*profile" in **/*routes*.ts
- Grep: "/api/user" in **/*.ts
- Glob: "**/routes/**/user*.ts"
- Grep: "getUserProfile|updateUserProfile" (common naming)
```

**React Components** (functional, class):
```
Keywords: React.FC, function Component, class.*extends React
Patterns: export function ComponentName, const ComponentName =
Files: **/components/**, **/*.tsx, **/*.jsx

Example search for "product card component":
- Grep: "function.*Product.*Card" in **/*.tsx
- Grep: "ProductCard.*=.*=>" in **/*.tsx
- Glob: "**/components/**/Product*.tsx"
- Grep: "export.*ProductCard" in **/*.tsx
```

**Services/Business Logic**:
```
Keywords: class.*Service, export.*service, provide, inject
Patterns: Service naming convention, dependency injection
Files: **/services/**, **/lib/**, **/utils/**

Example search for "email service":
- Grep: "class.*Email.*Service" in **/*.ts
- Grep: "sendEmail|emailService" in **/*.ts
- Glob: "**/services/**/*email*.ts"
- Grep: "nodemailer|sendgrid|aws-ses" (common email libs)
```

**Database Models** (Prisma, TypeORM, Sequelize):
```
Keywords: model, schema, entity, @Entity, interface.*Model
Patterns: Database column definitions, relationships
Files: **/models/**, **/entities/**, **/schema/**

Example search for "user model":
- Grep: "model User" in **/*.prisma
- Grep: "@Entity.*User|class User.*extends" in **/*.ts
- Glob: "**/models/**/user*.ts"
- Grep: "interface User.*{" in **/*.ts
```

See [references/search-strategies.md](references/search-strategies.md) for comprehensive patterns.
</by_artifact_type>

<domain_specific_searches>
Search within business domains to find related code:

**E-commerce domains**:
- User: authentication, profile, preferences
- Product: catalog, details, inventory
- Order: cart, checkout, payment
- Shipping: address, tracking, fulfillment

**Search strategy**: Start with domain term, expand to related terms
```
Domain: Product
Primary: "product", "Product", "PRODUCT"
Related: "item", "catalog", "inventory", "SKU"
Operations: "addProduct", "getProduct", "updateProduct", "deleteProduct"
```

**Cross-domain patterns**:
Look for similar operations across different domains:
```
Operation: "Detail view"
Search: "*DetailCard", "*DetailView", "*Detail.tsx"
Finds: UserDetailCard, ProductDetailCard, OrderDetailCard
Pattern: Consistent structure for entity detail components
```
</domain_specific_searches>

<technology_specific_searches>
Tailor searches to technology stack:

**TypeScript**:
```
- "interface Product" (type definitions)
- "type Product = " (type aliases)
- "Product extends " (inheritance)
- "as Product" (type assertions)
```

**GraphQL**:
```
- "type Product" (schema definitions)
- "Query.product" (query resolvers)
- "Mutation.createProduct" (mutation resolvers)
- "gql\`.*product" (query strings)
```

**SQL/Prisma**:
```
- "model Product" (Prisma schema)
- "CREATE TABLE product" (SQL migrations)
- "SELECT.*FROM product" (raw queries)
- "prisma.product.findMany" (Prisma client)
```

**React Query/SWR**:
```
- "useQuery.*product" (data fetching hooks)
- "useMutation.*product" (mutation hooks)
- "queryKey:.*product" (cache keys)
```
</technology_specific_searches>
</search_strategies>

<auto_trigger_conditions>
<when_to_trigger>
Automatically apply anti-duplication search when detecting these phrases:

**Explicit creation intent**:
- "Create a new [artifact]"
- "Implement a [artifact]"
- "Add a [artifact]"
- "Build a [artifact]"
- "Write a [artifact]"
- "Generate a [artifact]"

**Examples**:
- "Create a new API endpoint to fetch orders"
- "Implement a login component"
- "Add a service to handle payments"
- "Build a User model with email and password"
- "Write a function to validate user input"

**Implicit creation** (inferred from context):
- "I need to [do something]" → May require new code
- "How do I [accomplish task]" → May require new implementation
- "Can you [build feature]" → Definitely requires code

**During /implement phase**:
- Every task that involves writing new code
- Before writing first line of implementation
- Even for "simple" tasks (search takes <10 seconds)
</when_to_trigger>

<when_not_to_trigger>
Skip anti-duplication search when:

**User explicitly requests new approach**:
- "Create a new implementation (don't reuse existing)"
- "I know there's X, but I want a different approach"
- "Ignore existing code and start fresh"

**Modifying existing code**:
- "Update the UserController to add validation"
- "Fix the bug in ProductCard component"
- "Refactor the OrderService to use async/await"

**Non-code tasks**:
- "Explain how authentication works"
- "Review the ProductCard component"
- "Run the test suite"

**Configuration/data files**:
- "Add a new npm package"
- "Update the .env file"
- "Create a migration file" (different from creating models)
</when_not_to_trigger>

<proactive_trigger_logic>
When user says "Create an API endpoint to update user email":

1. **Immediately pause** before writing any code
2. **Announce search**: "Before implementing, let me search for existing user endpoints to ensure consistency..."
3. **Run searches** (5-10 seconds)
4. **Present findings**: "Found 4 existing user endpoints following a consistent pattern. I'll use the same structure."
5. **Implement** using discovered pattern

This becomes automatic—user doesn't need to ask for the search, it happens proactively.
</proactive_trigger_logic>
</auto_trigger_conditions>

<reuse_decision_framework>
<decision_tree>
After search completes, use this decision tree:

**Q1: Found exact match?**
- YES → Reuse directly (Option A)
- NO → Go to Q2

**Q2: Found close match (same domain, similar operation)?**
- YES → Can we extend it? (Option B)
  - If yes → Extend existing
  - If no → Go to Q3
- NO → Go to Q3

**Q3: Found pattern match (similar structure, different domain)?**
- YES → Extract generic abstraction? (Option C)
  - If yes → Create generic version
  - If abstraction too complex → Follow pattern (Option D)
- NO → Go to Q4

**Q4: Existing implementations are anti-patterns?**
- YES → Justify new approach (Option E) + document why existing code should be refactored
- NO → Follow established patterns if any, otherwise implement new

**Final check**: Before implementing new code, answer:
- "Why can't we reuse existing code?"
- "What makes this implementation different?"
- "Will this create duplication?"
</decision_tree>

<reuse_threshold>
**High reuse potential** (≥80% similar):
→ Reuse directly or extend

**Medium reuse potential** (50-79% similar):
→ Extract shared logic into utility/helper
→ Adapt existing pattern

**Low reuse potential** (30-49% similar):
→ Follow established patterns for consistency
→ Document differences

**No reuse potential** (<30% similar):
→ Implement new, but document why it's different
→ Consider if this signals missing abstraction
</reuse_threshold>
</reuse_decision_framework>

<examples>
<example name="api-endpoint-duplication-prevented">
**Request**: "Create an API endpoint to update user email"

**Search phase**:
```
Searches:
1. Grep "router\.(put|patch).*user" → Found 3 endpoints
2. Grep "/api/user.*email" → Found 1 endpoint (GET /api/user/email)
3. Glob "**/routes/**/user*.ts" → Found routes/user.ts

Results:
- PATCH /api/user/profile (updates name, bio)
- PATCH /api/user/password (updates password)
- PUT /api/user/settings (updates preferences)
```

**Analysis**:
All 3 endpoints follow same pattern:
```typescript
router.patch('/api/user/:field',
  authMiddleware,           // JWT authentication
  validateUserInput,        // Schema validation
  userController.update,    // Controller method
  standardErrorHandler      // Error handling
);
```

**Recommendation**:
"Found 3 existing user update endpoints. They all use:
- authMiddleware (JWT auth)
- validateUserInput (Joi schema validation)
- userController.update (centralized controller)
- standardErrorHandler (consistent errors)

**Option A**: Extend userController.update to handle email updates
**Option B**: Create new endpoint following the same pattern

I recommend **Option A** (extend existing controller) to avoid endpoint proliferation. The controller already handles profile/password/settings updates, email fits the same pattern."

**Implementation** (Option A):
```typescript
// userController.ts (extend existing)
async update(req, res) {
  const { field } = req.params;
  const allowedFields = ['profile', 'password', 'settings', 'email']; // ADD email

  if (!allowedFields.includes(field)) {
    return res.status(400).json({ error: 'Invalid field' });
  }

  // Add email-specific validation
  if (field === 'email') {
    await this.validateEmail(req.body.email);
  }

  // Existing update logic
  await this.userService.update(req.user.id, field, req.body);
  res.json({ success: true });
}
```

**Duplication prevented**: No new endpoint created, reused existing pattern, consistent auth/validation.

See [examples/api-endpoint-reuse.md](examples/api-endpoint-reuse.md) for full example.
</example>

<example name="component-pattern-extraction">
**Request**: "Create a React component to display product details"

**Search phase**:
```
Searches:
1. Grep "ProductDetail|ProductCard" in **/*.tsx → Found 2 components
2. Glob "**/components/**/Product*.tsx" → Found 5 product components
3. Grep "function.*Detail.*Card" in **/*.tsx → Found 8 DetailCard components

Results:
- UserDetailCard: Displays user info in card layout
- OrderDetailCard: Displays order info in card layout
- ProductSummaryCard: Displays product summary (not full details)
- ProductListItem: Displays product in list (minimal info)
```

**Analysis**:
Found **pattern**: All "DetailCard" components share structure:
```typescript
interface DetailCardProps<T> {
  data: T;
  loading?: boolean;
  onEdit?: () => void;
  onDelete?: () => void;
}

function DetailCard<T>({ data, loading, onEdit, onDelete }) {
  if (loading) return <Skeleton />;

  return (
    <Card>
      <CardHeader>
        {/* Title */}
      </CardHeader>
      <CardBody>
        {/* Fields */}
      </CardBody>
      <CardActions>
        {onEdit && <Button onClick={onEdit}>Edit</Button>}
        {onDelete && <Button onClick={onDelete}>Delete</Button>}
      </CardActions>
    </Card>
  );
}
```

**Recommendation**:
"Found consistent DetailCard pattern used for User and Order entities. Rather than creating ProductDetailCard from scratch, I'll extract the pattern into a generic DetailCard<T> component."

**Implementation** (Option C - Extract pattern):
```typescript
// components/common/DetailCard.tsx (NEW generic component)
interface DetailCardProps<T> {
  data: T;
  fields: Array<{ label: string; key: keyof T; render?: (value: any) => ReactNode }>;
  loading?: boolean;
  onEdit?: () => void;
  onDelete?: () => void;
}

export function DetailCard<T>({ data, fields, loading, onEdit, onDelete }: DetailCardProps<T>) {
  if (loading) return <Skeleton />;

  return (
    <Card>
      <CardBody>
        {fields.map(field => (
          <div key={String(field.key)}>
            <label>{field.label}</label>
            <div>{field.render ? field.render(data[field.key]) : data[field.key]}</div>
          </div>
        ))}
      </CardBody>
      <CardActions>
        {onEdit && <Button onClick={onEdit}>Edit</Button>}
        {onDelete && <Button onClick={onDelete}>Delete</Button>}
      </CardActions>
    </Card>
  );
}

// components/products/ProductDetailCard.tsx (USE generic)
export function ProductDetailCard({ product, loading, onEdit, onDelete }: Props) {
  return (
    <DetailCard
      data={product}
      loading={loading}
      fields={[
        { label: 'Name', key: 'name' },
        { label: 'Price', key: 'price', render: (val) => `$${val}` },
        { label: 'Description', key: 'description' },
        { label: 'Stock', key: 'stock', render: (val) => `${val} units` },
      ]}
      onEdit={onEdit}
      onDelete={onDelete}
    />
  );
}
```

**Duplication prevented**:
- No duplicate DetailCard implementations
- Generic component reusable for all entities
- Consistent UI/UX across User, Order, Product
- Refactored existing UserDetailCard and OrderDetailCard to use generic

See [examples/component-pattern-extraction.md](examples/component-pattern-extraction.md) for full example.
</example>

<example name="service-reuse">
**Request**: "Add a service to send password reset emails"

**Search phase**:
```
Searches:
1. Grep "sendEmail|emailService" → Found EmailService class
2. Grep "nodemailer|sendgrid" → Found nodemailer setup
3. Glob "**/services/**/*email*.ts" → Found services/EmailService.ts

Results:
- EmailService class with sendEmail() method
- Already sends: welcome emails, order confirmations, notifications
- Uses nodemailer + AWS SES
```

**Analysis**:
EmailService already exists and is well-structured:
```typescript
class EmailService {
  async sendEmail(to: string, subject: string, template: string, data: any) {
    const html = this.renderTemplate(template, data);
    await this.transporter.sendMail({ to, subject, html });
  }

  async sendWelcomeEmail(user: User) { ... }
  async sendOrderConfirmation(order: Order) { ... }
}
```

**Recommendation**:
"Found existing EmailService that already sends 3 types of emails. Rather than creating a new service, I'll add a sendPasswordResetEmail method to the existing service."

**Implementation** (Option B - Extend existing):
```typescript
// services/EmailService.ts (extend existing class)
class EmailService {
  // ... existing methods ...

  async sendPasswordResetEmail(user: User, resetToken: string) {
    const resetUrl = `${process.env.APP_URL}/reset-password?token=${resetToken}`;

    await this.sendEmail(
      user.email,
      'Password Reset Request',
      'password-reset',  // template name
      { userName: user.name, resetUrl, expiresIn: '1 hour' }
    );
  }
}
```

**Duplication prevented**:
- No new email service created
- Reused existing nodemailer configuration
- Reused template rendering logic
- Consistent email sending across app

See [examples/service-extension.md](examples/service-extension.md) for full example.
</example>
</examples>

<anti_patterns>
<anti_pattern name="skipping-search">
**Problem**: Implementing without searching first

**Bad approach**:
```
User: "Create an API endpoint to update user email"
Claude: *Immediately writes new endpoint from scratch*
```

Result: Duplicate endpoint with different auth, validation, error handling from existing user endpoints.

**Correct approach**:
```
User: "Create an API endpoint to update user email"
Claude: "Let me search for existing user endpoints first..."
Claude: *Finds 3 similar endpoints*
Claude: "Found existing pattern. I'll follow it for consistency."
```

**Rule**: ALWAYS search before implementing. Takes 5-10 seconds, prevents hours of refactoring later.
</anti_pattern>

<anti_pattern name="ignoring-search-results">
**Problem**: Finding existing code but implementing new anyway

**Bad approach**:
```
Search: Found ProductSummaryCard component
Claude: "Found ProductSummaryCard, but I'll create ProductDetailCard from scratch"
*Creates duplicate card component with different styling, props, structure*
```

Result: Two similar components that should be one, inconsistent UI, double maintenance.

**Correct approach**:
```
Search: Found ProductSummaryCard component
Claude: "Found ProductSummaryCard showing basic info. Should we extend it to show full details, or do you need a separate component? The summary version could potentially be enhanced rather than creating a duplicate."
```

**Rule**: When search finds similar code, default to reuse/extend. Only create new if justified.
</anti_pattern>

<anti_pattern name="shallow-search">
**Problem**: Searching only for exact matches, missing similar patterns

**Bad approach**:
```
Request: "Create endpoint GET /api/products/:id"
Search: Only "GET /api/products" (too specific)
Misses: All other GET endpoints with similar structure
```

Result: Misses established patterns for GET /:id endpoints across User, Order, etc.

**Correct approach**:
```
Request: "Create endpoint GET /api/products/:id"
Searches:
- "router.get.*:id" (find all parameterized GET endpoints)
- "/api/.*/:id" (find all resource-by-id patterns)
- "products" (find all product-related code)
```

**Rule**: Use multiple search strategies (keywords, patterns, files). Cast wide net, filter results.
</anti_pattern>

<anti_pattern name="copy-paste-without-understanding">
**Problem**: Copying existing code without understanding it

**Bad approach**:
```
Found: Complex UserDetailCard with 15 props, internal state, side effects
Claude: *Copies entire component, renames User → Product*
Result: Cargo-culted complexity, unnecessary props, confusing code
```

**Correct approach**:
```
Found: Complex UserDetailCard
Claude: "This component is complex (15 props, internal state). Let me analyze what's actually needed for Product use case..."
Claude: "Product details only need 5 props. I'll create simplified version following the core pattern but without unnecessary complexity."
```

**Rule**: Understand existing code before reusing. Don't cargo-cult complexity.
</anti_pattern>

<anti_pattern name="premature-abstraction">
**Problem**: Creating generic abstraction after finding only 1-2 similar pieces

**Bad approach**:
```
Found: UserDetailCard, ProductDetailCard (2 components)
Claude: "Let me create DetailCard<T> generic component with 20 configuration options to handle all possible cases..."
```

Result: Over-engineered abstraction that's harder to use than copying code.

**Correct approach**:
```
Found: UserDetailCard, ProductDetailCard (2 components)
Claude: "Found 2 similar components. They're simple enough that keeping them separate is fine for now. If we add a 3rd entity (Order), then we'll extract the pattern."
```

**Rule**: Abstraction requires 3+ similar pieces (Rule of Three). Two instances don't justify generic abstraction yet.
</anti_pattern>
</anti_patterns>

<validation>
<success_indicators>
Anti-duplication skill successfully applied when:

1. **Search executed before implementation**: Every "create/implement" request triggers search first
2. **Results presented to user**: User sees what was found and why reuse is/isn't appropriate
3. **Reuse justified**: If reusing, explain what's being reused. If not, explain why not.
4. **Patterns maintained**: New code follows established patterns in codebase
5. **Duplication avoided**: No near-identical code exists in multiple places
6. **Abstractions appropriate**: Generic code created only when 3+ similar pieces exist (Rule of Three)
</success_indicators>

<metrics>
Track anti-duplication effectiveness:

**Process metrics**:
- % of "create" requests that trigger search (target: 100%)
- Average search time (target: <10 seconds)
- % of searches that find relevant results (target: >60%)

**Outcome metrics**:
- % of implementations that reuse existing code (target: >40%)
- % of implementations that follow existing patterns (target: >80%)
- Lines of code prevented (compared to from-scratch implementation)

**Quality metrics**:
- Consistency score: How similar are similar artifacts? (target: >80% structural similarity)
- DRY violations: How many near-duplicates exist? (target: <3 copies of any pattern)
- Refactoring burden: How often do bug fixes need to be applied in multiple places? (target: declining)
</metrics>

<validation_checklist>
Before completing implementation, verify:

- [ ] Search was executed (not skipped)
- [ ] Search covered multiple strategies (keywords, files, patterns)
- [ ] Results were analyzed (exact, close, pattern matches identified)
- [ ] Reuse options were considered (A, B, C, D, E)
- [ ] If reusing: Existing code was understood (not blindly copied)
- [ ] If extending: Extension fits naturally (not forced)
- [ ] If new: Justification documented (why existing code doesn't work)
- [ ] Patterns followed: New code consistent with existing similar code
- [ ] Abstraction appropriate: Generic code only if 3+ similar pieces
</validation_checklist>
</validation>

<reference_guides>
For deeper topics, see reference files:

**Search strategies**: [references/search-strategies.md](references/search-strategies.md)
- Comprehensive search patterns by artifact type
- Technology-specific search strategies
- Domain-driven search approaches
- Advanced regex patterns

**Reuse patterns**: [references/reuse-patterns.md](references/reuse-patterns.md)
- When to reuse directly vs extend
- Extracting shared logic
- Creating generic abstractions
- Refactoring for reusability

**Decision framework**: [references/decision-framework.md](references/decision-framework.md)
- Decision tree for reuse vs new implementation
- Calculating similarity scores
- Justifying new code
- Documenting decisions

**Integration with phases**: [references/phase-integration.md](references/phase-integration.md)
- Using anti-duplication in /plan phase
- Using anti-duplication in /implement phase
- Updating plan.md with discovered patterns
- Documenting reuse decisions in NOTES.md
</reference_guides>

<success_criteria>
The anti-duplication skill is successfully applied when:

1. **Proactive search**: Search triggered automatically before any "create/implement" request
2. **Comprehensive coverage**: Multiple search strategies used (keywords, files, patterns, domain, technology)
3. **Results analyzed**: Findings categorized (exact, close, pattern matches) and relevance scored
4. **Reuse prioritized**: Options A-D (reuse, extend, extract, follow pattern) considered before Option E (new)
5. **Patterns maintained**: New implementations follow established codebase patterns
6. **Justification documented**: If creating new code despite similar existing code, justification clearly stated
7. **DRY principle upheld**: No unnecessary duplication introduced
8. **Abstractions appropriate**: Generic code created only when justified (Rule of Three: 3+ similar pieces)
9. **User informed**: User understands what was found and why reuse is/isn't happening
10. **Time efficient**: Search completes in <10 seconds, doesn't slow down development
</success_criteria>
