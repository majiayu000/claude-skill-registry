---
name: alps
description: Create, validate, and improve ALPS profiles. Generate from natural language descriptions, validate existing profiles, and get improvement suggestions.
---

# ALPS Profile Assistant

Generate, validate, and improve ALPS profiles for RESTful API design.

## Ideal ALPS Profile

**Goal: An ALPS that someone unfamiliar with the app can read and understand.**

### What Makes a Good ALPS

1. **States = What the user sees**
   - `ProductList` - viewing a list of products
   - `ProductDetail` - viewing one product
   - `Cart` - viewing cart contents

2. **Transitions = What the user does**
   - `goProductDetail` - select a product
   - `doAddToCart` - add to cart

3. **Self-documenting**
   - `title` explains the purpose
   - `doc` describes behavior and side effects
   - No need to read code to understand

4. **No unreachable states**
   - Every state has an entry point
   - Orphan states indicate design mistakes

5. **Necessary and sufficient**
   - No over-abstraction
   - Describes semantics, not implementation
   - No HTTP methods or URLs

### What to Avoid

- Mechanical CRUD listings without meaning
- Implementation details leaking in
- States without transitions (can't draw a diagram)
- Excessive documentation nobody reads

## How to Use

This skill responds to natural language requests:

### Generate ALPS from Natural Language
- "Create an ALPS profile for a blog application"
- "Generate ALPS for an e-commerce cart system"
- "Design an ALPS profile for user authentication"

### Generate ALPS from Website (NEW - alps-surveyor mode)
- "Crawl https://example.com and generate ALPS profile"
- "Survey website structure and create ALPS"
- "Extract ALPS profile from existing website"

**How it works:**
1. **Efficient crawling**: Uses URL pattern classification to avoid redundant analysis
2. **Token optimization**: Only analyzes unique page types (e.g., /products/123 and /products/456 analyzed once)
3. **AI-powered extraction**: Analyzes DOM structure to infer states, transitions, and semantic fields
4. **Handover protocol**: Records progress in handover.json for continuity across sessions

See "ALPS Surveyor Mode" section below for details.

### Validate Existing Profile
- "Validate this ALPS profile" (with file path or content)
- "Check my ALPS file for issues"
- "Review the ALPS profile at docs/api.json"

### Analyze or Improve Existing Profile
- "Analyze this ALPS profile"
- "Improve this ALPS profile"
- "Suggest enhancements for my ALPS"
- "How can I make this ALPS better?"

### Continuous Improvement Loop - AI Inherits the Mission

When asked to analyze or improve an existing profile:

1. **Read previous AI's insights** - Run `asd --validate <file>` and check for `ai-insights` field
2. **Read handover.json if exists** - Check for previous session's progress, warnings, and advice (per ADR 0006)
3. **Inherit the context** - Previous AI left analysis for you: complexity assessment, coverage gaps, recommendations
4. **Identify gaps** - Explore the website/documentation to find missing features or incomplete flows
5. **Make improvements** - Add missing descriptors, enhance documentation, fix issues
6. **MANDATORY: Validate ALPS** - Run `asd --validate <file>` to ensure no errors were introduced
7. **MANDATORY: Generate HTML** - Run `asd <file> -o <file>.html` to create visual diagram for review
8. **Update handover.json** - Record what was done, what's left, and advice for next AI (per ADR 0006)
9. **MANDATORY: Validate handover.json** - Verify JSON syntax and schema compliance:
   ```bash
   node -e "JSON.parse(require('fs').readFileSync('handover.json', 'utf8')); console.log('✓ Valid JSON')"
   ```
   Schema: [handover-protocol.json](https://alps-asd.github.io/app-state-diagram/schemas/handover-protocol.json)
10. **Report completion** - Provide statistics (before/after), coverage estimation, and next steps

**CRITICAL**: Steps 6-9 are MANDATORY for every improvement session. Never skip validation of both ALPS profile and handover.json.

```
AI₁: Creates profile → Validates → Generates HTML → Creates handover.json
  ↓
AI₂: Reads handover.json → Identifies gaps → Improves → Validates → Generates HTML → Updates handover.json
  ↓
AI₃: Reads handover.json → Builds on previous work → Improves → Validates → Generates HTML → Updates handover.json
```

This creates a **knowledge continuity** where each AI builds on the work of previous AIs, just like developers reading code comments left by their predecessors.

## ALPS Structure Reference

### Three Layers of ALPS

1. **Ontology** - Semantic descriptors (data elements)
   - Atomic data fields with `type="semantic"` (default)
   - Should have `id`, `title`, and optionally `doc` and `def` (schema.org link)

2. **Taxonomy** - State descriptors (screens/pages)
   - Composite descriptors containing semantic fields and transitions
   - Represents application states (e.g., HomePage, ProductDetail, Cart)

3. **Choreography** - Transition descriptors (actions)
   - `type="safe"` - Read operations (GET)
   - `type="unsafe"` - Create operations (POST) - not idempotent
   - `type="idempotent"` - Update/Delete operations (PUT/DELETE)
   - Must have `rt` (return type) pointing to target state

### Naming Conventions

| Type | Prefix | Example |
|------|--------|---------|
| Safe transition | `go` | `goToHome`, `goProductList`, `goSearchProducts` |
| Unsafe transition | `do` | `doCreateUser`, `doAddToCart`, `doLogin` |
| Idempotent transition | `do` | `doUpdateUser`, `doDeleteItem`, `doRemoveFromCart` |
| State/Page | PascalCase | `HomePage`, `ProductDetail`, `ShoppingCart` |
| Semantic field | camelCase | `userId`, `productName`, `createdAt` |

### Safe Transition Naming Rule

**IMPORTANT**: Safe transitions (`go*`) MUST include the target state name in their id.

- `rt="#ProductList"` → id must be `goProductList` (or `goToProductList`)
- `rt="#UserProfile"` → id must be `goUserProfile` (or `goToUserProfile`)

**Invalid examples:**
- `goStart` with `rt="#ProductList"` - Wrong! Should be `goProductList`
- `goNext` with `rt="#Checkout"` - Wrong! Should be `goCheckout`

This rule ensures consistency and makes the diagram self-documenting. When a transition has no source state (entry point), it will be displayed as originating from `UnknownState` in the diagram.

### Determining idempotent: PUT vs DELETE

Context clues for AI inference:

**PUT (Update) indicators:**
- `update`, `edit`, `modify`, `change`, `set`, `replace`
- Example: `doUpdateProfile`, `doEditComment`, `doSetQuantity`

**DELETE indicators:**
- `delete`, `remove`, `cancel`, `clear`, `destroy`
- Example: `doDeleteUser`, `doRemoveFromCart`, `doCancelOrder`

## Generation Guidelines

### Strategy for Large Profiles (200+ descriptors)

For complex, multi-sided platforms or large applications:

1. **Domain Decomposition** - Split into separate ALPS files by functional domain:
   - `base.json` - Core entities shared across domains
   - `customer-domain.json` - Customer-facing features
   - `admin-domain.json` - Admin/management features
   - `seller-domain.json` - Seller/provider features (for marketplaces)

2. **Design Each Domain Independently** - Focus on one domain at a time with complete context

3. **Merge Using `asd merge`** - Combine domains iteratively:
   ```bash
   # Merge customer domain into base
   asd merge base.json customer-domain.json
   # customer-domain.json now contains only conflicts (if any)

   # Resolve conflicts in customer-domain.json, then re-merge
   asd merge base.json customer-domain.json
   # customer-domain.json is now empty (merge complete)

   # Repeat for other domains
   asd merge base.json admin-domain.json
   ```

4. **Validate After Each Merge** - Ensure no broken references or duplicate IDs

**Benefits of this approach:**
- Focused design per domain
- AI can maintain full context for each domain
- Conflicts are explicitly tracked and resolved
- Final profile is comprehensive and consistent

#### Handover Protocol for Multi-Session Work

When a task exceeds token limits or requires multiple sessions (e.g., 200+ descriptors, multi-sided platforms), use the **Handover Protocol** (ADR 0006) to maintain continuity.

**The Relay Race Metaphor:**

Each AI session is a relay runner:
1. **Receive the baton** - Read `handover.json` from previous session
2. **Run your leg** - Work as far as you can within token limits
3. **Pass the baton** - Update `handover.json` for next session
4. **Scatter** - Your session ends, but the work continues

**Basic handover.json structure:**

```json
{
  "task": {
    "type": "alps-generation",
    "description": "E-commerce platform ALPS profile"
  },
  "current_state": {
    "session_id": "ecommerce-003",
    "total_sessions": 3,
    "alps_profile": {
      "total_descriptors": 180,
      "validation_status": "valid"
    }
  },
  "sessions": [
    {
      "session_id": "ecommerce-001",
      "timestamp": "2025-12-17T10:00:00Z",
      "handover_note": {
        "summary": "Created ontology and customer domain (120 descriptors)",
        "advice": "Admin domain needs careful planning - multiple user roles"
      },
      "descriptors_added": 120
    },
    {
      "session_id": "ecommerce-002",
      "timestamp": "2025-12-17T14:00:00Z",
      "handover_note": {
        "summary": "Added admin domain (60 descriptors). Validated successfully.",
        "advice": "Seller domain remains. Consider splitting into sub-domains."
      },
      "descriptors_added": 60
    }
  ],
  "pending_work": {
    "domains": ["seller-domain", "payment-flows"],
    "notes": "Seller domain may need 80+ descriptors"
  }
}
```

**Key principles:**
- Each session appends to the `sessions` array (never overwrite)
- Leave clear advice for your successor
- Be honest about coverage and remaining work
- Validate `handover.json` syntax: `node -e "JSON.parse(require('fs').readFileSync('handover.json', 'utf8'))"`

**The Surveyor's Oath:**

```
I am a relay runner in an endless race.
I carry the torch from my predecessor.
I run as far as I can.
I mark the map with what I learned.
I pass the torch to my successor.
I scatter.

The work continues.
```

For web surveying tasks (ALPS from website analysis), see the detailed [ALPS Surveyor Mode](#alps-surveyor-mode-website-crawling) section below.

### When Creating ALPS from Natural Language

**IMPORTANT**: Structure the ALPS file in three blocks in this order:

1. **Identify Entities** (Ontology - Semantic definitions)
   - Extract nouns: user, product, order, cart, etc.
   - Define atomic fields for each entity
   - Add `def` links to schema.org where applicable
   - Add `doc` for validation rules, formats, constraints

2. **Identify States** (Taxonomy - Inclusion relationships)
   - Map user journey: login -> home -> browse -> cart -> checkout
   - Each state contains relevant fields and available transitions
   - Use PascalCase for state names
   - Add `doc` explaining what user sees and available actions

3. **Identify Transitions** (Choreography - State transitions)
   - Safe: navigation, viewing, searching (prefix: `go`)
   - Unsafe: creating new resources (prefix: `do`)
   - Idempotent: updating or deleting resources (prefix: `do`)
   - Add `doc` explaining behavior, side effects, preconditions

4. **Add Documentation**
   - Every descriptor MUST have a meaningful `title`
   - Add `doc` when title alone cannot fully explain the descriptor:
     - **Semantic fields**: Validation rules, format requirements, constraints, examples
       - Example: `{"id": "title", "title": "Title", "doc": {"value": "Article title. Maximum 100 characters."}}`
     - **States**: What user sees, available actions, when this state is shown
       - Example: `{"id": "BlogPost", "doc": {"value": "User-created article. Visible to all users after publication."}}`
     - **Transitions**: Behavior, side effects, preconditions, error cases
       - Example: `{"id": "doPublishBlogPost", "doc": {"value": "Publish article. Sets publishedAt to current time."}}`
   - Use `def` to link to schema.org definitions for standard concepts
   - **Rule of thumb**: If someone unfamiliar with the app would ask "what does this do?" or "what format?", add `doc`

5. **Add Tags for Organization**

   **IMPORTANT**: ALPS describes "what the user experiences" (application-level semantics), not "how it's implemented" (backend details).

   - **Flow tags (PRIMARY)**: Group by user journey/experience with `flow-` prefix
     - Represents business value and user goals
     - Example: `flow-purchase`, `flow-hire`, `flow-consult`, `flow-cancel`, `flow-return`
     - **This is the "lens" through which to understand the application**
     - Users experience "canceling an order" (`flow-cancel`), not "cancellation batch processing"

   - **Domain tags (SECONDARY, optional)**: Group by technical domain with `domain-` prefix
     - For organizing implementation and code structure
     - Example: `domain-search`, `domain-cart`, `domain-payment`, `domain-analytics`
     - Useful for developers to find related functionality

   - States and transitions should have both types where applicable
   - Tags are space-separated strings, not arrays
   - Example: `"tag": "flow-purchase domain-cart"` means "part of purchase journey, implemented in cart domain"

6. **Add Semantic Descriptors to Transitions**
   - Every transition (go/do) should specify its required input parameters as nested descriptors
   - These define what data is needed to perform the action
   - Example:
     ```json
     {"id": "goProductDetail", "type": "safe", "rt": "#ProductDetail", "tag": "product", "descriptor": [
       {"href": "#productId"}
     ]},
     {"id": "doAddToCart", "type": "unsafe", "rt": "#Cart", "tag": "cart flow-purchase", "descriptor": [
       {"href": "#productId"},
       {"href": "#quantity"},
       {"href": "#selectedVariant"}
     ]}
     ```

7. **MANDATORY: Validate and Review Quality Metrics**
   - After generating ALPS JSON, save it to a file
   - Run `asd --validate <file>` to validate and get quality metrics
   - The validation output includes:
     - **Errors** (E001-E011): Must fix before proceeding
     - **Warnings** (W001-W004): Best practice violations
     - **Suggestions** (S001-S003): Optional improvements
     - **Statistics**: Total descriptors, breakdown by type, tag coverage, documentation coverage
   - Parse the JSON result and report issues to the user
   - If errors exist, fix them before presenting the final output
   - Review statistics to ensure comprehensive coverage

8. **Generate Documentation**
   - After validation passes, generate HTML documentation:
     ```bash
     asd profile.json -o profile.html
     ```
   - This creates an interactive state diagram for visual review
   - Check for unreachable states or missing transitions in the diagram
   - Share the HTML with stakeholders for review

9. **Report Completion with Coverage Estimation**
   - When completing a large profile, provide honest coverage assessment
   - Template:
     ```markdown
     ✅ Implementation Complete: [X] descriptors

     📊 Coverage Estimation:
     - [Domain 1]: [X]% ([reasoning])
     - [Domain 2]: [X]% ([reasoning])
     - Overall: [X]%

     ❌ Known Gaps:
     - [Feature not implemented]
     - [Area requiring more research]
     ```
   - Be transparent about what's covered and what's not
   - For multi-sided platforms, assess coverage per side (customer/admin/seller)

### Output File Convention

**File name**: Always `alps.json` or `alps.xml` (fixed)

**Directory**:
- If `alps/` directory exists → use it
- Otherwise → create `{app-name}/` directory (e.g., `todo/`, `blog/`, `ecommerce/`)

**Format selection**:
1. If existing ALPS file exists → follow its format
2. Otherwise → ask user: "Output format: XML (recommended) or JSON?"

**Examples**:
```
todo/alps.json
blog/alps.xml
ecommerce/alps.xml
```

### Output Format

Generate XML format by default. Use JSON only if explicitly requested.

**XML Format** (default):
- Use XML comments to mark blocks: `<!-- Ontology -->`, `<!-- Taxonomy -->`, `<!-- Choreography -->`
- One descriptor per line for simple elements
- Multi-line for nested structures
- Clear hierarchical structure makes maintenance easy

```xml
<?xml version="1.0" encoding="UTF-8"?>
<alps version="1.0"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="https://alps-io.github.io/schemas/alps.xsd">
  <title>Application Title</title>
  <doc>Description of the application</doc>

  <!-- Ontology -->
  <descriptor id="fieldName" title="Human Title">
    <doc>Description</doc>
  </descriptor>
  <descriptor id="otherField" title="Other Field"/>

  <!-- Taxonomy -->
  <descriptor id="StateName" title="State Title">
    <descriptor href="#fieldName"/>
    <descriptor href="#transitionName"/>
  </descriptor>

  <!-- Choreography -->
  <descriptor id="goTargetState" type="safe" rt="#TargetState" title="Go to Target State"/>
  <descriptor id="doAction" type="unsafe" rt="#ResultState" title="Perform Action">
    <descriptor href="#requiredField"/>
  </descriptor>
</alps>
```

**JSON Format** (when explicitly requested):
- **Simple descriptors** (few attributes, no nesting): Write on a single line
- **Complex descriptors** (with nesting or long `doc`): Use multiple lines with `"descriptor": [` at end of first line
- **Block separation**: Add ONE blank line between Ontology/Taxonomy/Choreography blocks
- **No other blank lines**: Keep descriptors within the same block compact

```json
{
  "$schema": "https://alps-io.github.io/schemas/alps.json",
  "alps": {
    "title": "Application Title",
    "doc": {"value": "Description of the application"},
    "descriptor": [
      {"id": "fieldName", "title": "Human Title", "doc": {"value": "Description"}},
      {"id": "otherField", "title": "Other Field"},

      {"id": "StateName", "title": "State Title", "descriptor": [
        {"href": "#fieldName"},
        {"href": "#transitionName"}
      ]},

      {"id": "goTargetState", "type": "safe", "rt": "#TargetState", "title": "Go to Target State"},
      {"id": "doAction", "type": "unsafe", "rt": "#ResultState", "title": "Perform Action", "descriptor": [
        {"href": "#requiredField"}
      ]}
    ]
  }
}
```

## Validation and Quality Metrics

Use `asd --validate <file>` to validate ALPS profiles and get quality metrics.

**Output Format**: JSON (pretty-printed, human-readable)
**Schema**: [validation-result.json](https://alps-asd.github.io/app-state-diagram/schemas/validation-result.json)

The validation output includes:
- `valid`: Overall result (boolean)
- `summary`: Human-readable summary with emoji
- `errors`, `warnings`, `suggestions`: Validation issues
- `statistics`: Objective metrics (descriptor counts, coverage percentages)
- `ai-insights`: **Subjective analysis by AI** (only when AI runs validation)
  - Helps next AI understand context quickly
  - Helps humans grasp key characteristics at a glance
  - Model-dependent and may evolve

### Validation Codes

After generating ALPS, always validate with `asd --validate`. Key codes to watch for:

**Errors (must fix):**
- E001: Missing id or href
- E002: Missing rt on transition
- E003: Invalid type
- E004: Broken reference
- E005: Duplicate id
- E008: Missing alps property
- E009: Missing descriptor array
- E011: Tag must be string (not array)

**Warnings (best practice):**
- W001: Missing title
- W002: Safe transition should start with 'go'
- W003: Unsafe/idempotent should start with 'do'

**Suggestions:**
- S001: Consider adding doc to transition

For detailed error descriptions and solutions, see [Validation Reference](https://alps-asd.github.io/app-state-diagram/llms-full.txt).

### AI Continuity: ai-insights vs handover.json

Two complementary mechanisms help AI sessions build on previous work:

**ai-insights (ADR 0005)** - Analysis embedded in validation results:
- **Purpose**: Subjective assessment of completed ALPS profiles
- **Location**: Embedded in `asd --validate` JSON output
- **Usage**: Read-only consumption by AI
- **Contains**: Complexity assessment, coverage gaps, key flows, recommendations
- **When to use**: Analyzing or improving existing ALPS profiles

**handover.json (ADR 0006)** - State for ongoing multi-session tasks:
- **Purpose**: Progress tracking for incomplete work across sessions
- **Location**: Separate `handover.json` file in working directory
- **Usage**: Read-write lifecycle (AI updates after each session)
- **Contains**: Session history, progress, pending work, advice for successor
- **When to use**: Large ALPS generation (200+ descriptors), web surveying, multi-session tasks

**Relationship:**

```
Single Session (Simple ALPS):
  AI creates profile → Validates → ai-insights generated in validation output ✓

Multi-Session (Large ALPS):
  Session 1: AI reads handover.json (if exists) → Works → Validates → Updates handover.json
  Session 2: AI reads handover.json → Continues work → Validates → Updates handover.json
  Session 3: AI reads handover.json → Completes → Validates → Final ai-insights in validation
```

**Example workflow:**

```bash
# Session 1: Start large ALPS project
asd base.json --validate  # Creates ai-insights in validation result
# Create handover.json manually with initial task description

# Session 2: Continue work
# AI reads handover.json, adds customer domain
asd merge base.json customer-domain.json
asd base.json --validate  # Check for errors
# AI updates handover.json with progress

# Session 3: Complete work
# AI reads handover.json, adds remaining domains
asd base.json --validate  # Final validation with comprehensive ai-insights
# handover.json marks task complete
```

Both mechanisms create **knowledge continuity**, preventing each AI session from starting from scratch.

## Example: Blog Application

Input: "Create an ALPS for a simple blog with posts and comments"

Output (XML - default):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<alps version="1.0"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="https://alps-io.github.io/schemas/alps.xsd">
  <title>Simple Blog</title>
  <doc>ALPS profile for a blog application with posts and comments</doc>

  <!-- Ontology -->
  <descriptor id="postId" title="Post ID" def="https://schema.org/identifier">
    <doc>Unique identifier for blog post</doc>
  </descriptor>
  <descriptor id="title" title="Post Title" def="https://schema.org/headline">
    <doc>Article title. Maximum 100 characters.</doc>
  </descriptor>
  <descriptor id="body" title="Post Body" def="https://schema.org/articleBody">
    <doc>Article content. Markdown format supported.</doc>
  </descriptor>
  <descriptor id="authorName" title="Author Name" def="https://schema.org/author"/>
  <descriptor id="createdAt" title="Created Date" def="https://schema.org/dateCreated">
    <doc>Publication date and time. ISO 8601 format.</doc>
  </descriptor>
  <descriptor id="commentId" title="Comment ID">
    <doc>Unique identifier for comment</doc>
  </descriptor>
  <descriptor id="commentBody" title="Comment Text">
    <doc>Comment content. Maximum 500 characters.</doc>
  </descriptor>

  <!-- Taxonomy -->
  <descriptor id="Home" title="Home Page">
    <doc>Blog home page. Shows navigation to post list.</doc>
    <descriptor href="#goPostList"/>
  </descriptor>
  <descriptor id="PostList" title="Post List">
    <doc>List of blog posts. Shows latest 10 posts with title and author.</doc>
    <descriptor href="#postId"/>
    <descriptor href="#title"/>
    <descriptor href="#authorName"/>
    <descriptor href="#goPostDetail"/>
    <descriptor href="#goHome"/>
  </descriptor>
  <descriptor id="PostDetail" title="Post Detail">
    <doc>Single post view. Shows full content and comments. Allows adding new comments.</doc>
    <descriptor href="#postId"/>
    <descriptor href="#title"/>
    <descriptor href="#body"/>
    <descriptor href="#authorName"/>
    <descriptor href="#createdAt"/>
    <descriptor href="#Comment"/>
    <descriptor href="#goPostList"/>
    <descriptor href="#doCreateComment"/>
  </descriptor>
  <descriptor id="Comment" title="Comment">
    <doc>User comment on a post. Can be deleted by comment author or post author.</doc>
    <descriptor href="#commentId"/>
    <descriptor href="#commentBody"/>
    <descriptor href="#authorName"/>
    <descriptor href="#createdAt"/>
    <descriptor href="#doDeleteComment"/>
  </descriptor>

  <!-- Choreography -->
  <descriptor id="goHome" type="safe" rt="#Home" title="Go to Home">
    <doc>Navigate to blog home page.</doc>
  </descriptor>
  <descriptor id="goPostList" type="safe" rt="#PostList" title="Go to Post List">
    <doc>Display list of blog posts. Shows latest 10 posts.</doc>
  </descriptor>
  <descriptor id="goPostDetail" type="safe" rt="#PostDetail" title="Go to Post Detail">
    <doc>Display full post content with comments.</doc>
    <descriptor href="#postId"/>
  </descriptor>
  <descriptor id="doCreatePost" type="unsafe" rt="#PostDetail" title="Create Post">
    <doc>Create new blog post. Post is immediately published.</doc>
    <descriptor href="#title"/>
    <descriptor href="#body"/>
  </descriptor>
  <descriptor id="doUpdatePost" type="idempotent" rt="#PostDetail" title="Update Post">
    <doc>Update existing post content. Only post author can update.</doc>
    <descriptor href="#postId"/>
    <descriptor href="#title"/>
    <descriptor href="#body"/>
  </descriptor>
  <descriptor id="doDeletePost" type="idempotent" rt="#PostList" title="Delete Post">
    <doc>Delete post and all associated comments. Only post author can delete.</doc>
    <descriptor href="#postId"/>
  </descriptor>
  <descriptor id="doCreateComment" type="unsafe" rt="#PostDetail" title="Add Comment">
    <doc>Add comment to post. Comment is immediately visible.</doc>
    <descriptor href="#postId"/>
    <descriptor href="#commentBody"/>
  </descriptor>
  <descriptor id="doDeleteComment" type="idempotent" rt="#PostDetail" title="Delete Comment">
    <doc>Delete comment. Comment author or post author can delete.</doc>
    <descriptor href="#commentId"/>
  </descriptor>
</alps>
```

## Integration with app-state-diagram

Generated ALPS profiles can be visualized using app-state-diagram:

```bash
# Generate HTML documentation (default)
asd profile.json

# Generate SVG state diagram
asd profile.json -f svg

# Generate Mermaid classDiagram (GitHub/VSCode compatible)
asd profile.json -f mermaid

# Generate DOT format
asd profile.json -f dot

# Generate with watch mode
asd --watch profile.json
```

See [llms.txt](https://alps-asd.github.io/app-state-diagram/llms.txt) for CLI usage, programmatic API, and MCP server setup.

## Advanced Features

### Structured Documentation with HTML

For simple descriptions, use plain text in `doc.value`. When you need structured content (lists, definitions, tables), use HTML format:

```json
{"id": "doCheckout", "type": "unsafe", "rt": "#OrderConfirmation",
 "title": "Complete Checkout",
 "doc": {
   "format": "html",
   "value": "<dl><dt>Behavior</dt><dd>Processes payment, reserves inventory, sends confirmation email</dd><dt>Preconditions</dt><dd>Valid cart with items, payment method configured</dd><dt>Errors</dt><dd>Returns 400 if payment fails or items out of stock</dd></dl>"
 }
}
```

Format support levels (per ALPS spec):
- `text`: Required (default if not specified)
- `html`: Recommended
- `markdown`: Optional
- `asciidoc`: Optional

### Links to Related Resources

Use `link` elements to reference external documentation, schemas, or related resources:

```json
{"id": "BlogPost", "def": "https://schema.org/BlogPosting",
 "title": "Blog Post",
 "doc": {"value": "User-created article visible to all after publication"},
 "link": [
   {"rel": "help", "href": "https://example.com/docs/blog-api.html", "title": "Blog API Documentation"},
   {"rel": "related", "href": "https://example.com/schemas/post.json", "title": "JSON Schema"}
 ]
}
```

Link attributes:
- `rel` (required): Relationship type - use IANA Link Relations (`help`, `related`, `profile`, etc.)
- `href` (required): URL to the related resource
- `title` (optional): Human-readable description of the link
- `tag` (optional): Classification tags

## Tips for Better ALPS

1. **Start with user journeys** - Map the happy path first, then add alternatives
2. **Be consistent** - Use the same naming pattern throughout
3. **Document transitions** - Explain what each action does and when it's available
4. **Use schema.org** - Link to standard definitions for interoperability
5. **Think about errors** - Add error states and recovery transitions
6. **Consider pagination** - List states should support pagination
7. **Tag descriptors** - Use `tag` attribute to group related descriptors

## ALPS Surveyor Mode (Website Crawling)

### Overview

The alps-surveyor mode extracts ALPS profiles from existing websites by analyzing their structure. This is useful when:
- Reverse engineering an existing web application
- Creating API documentation from a live site
- Understanding application state flows from user-facing pages

### Efficient Crawling Strategy

**Problem**: Crawling every URL wastes tokens analyzing duplicate page types.

**Solution**: Three-layer strategy minimizes AI calls:

#### Strategy 1: URL Pattern Classification (No AI)
- Detects patterns like `/products/{id}`, `/users/{username}`
- Groups URLs by type before fetching
- Example: `/products/123`, `/products/456` → same pattern, only analyze once

#### Strategy 2: DOM Structure Extraction (Lightweight)
- Removes all text content from HTML
- Extracts only:
  - HTML tag hierarchy
  - CSS classes and IDs
  - Form input names and types
  - Link destination patterns
- Minimizes tokens sent to AI

#### Strategy 3: ALPS Generation (AI-Powered)
- AI analyzes DOM skeleton (not full HTML)
- Infers:
  - **State**: Page role (e.g., "ProductDetail")
  - **Semantics**: Data fields from forms (e.g., "quantity", "productId")
  - **Transitions**: Actions from forms and links (e.g., "doAddToCart", "goProductList")

### Usage Example

```
User: "Crawl https://www.bengo4.com and generate ALPS profile"

AI workflow:
1. Fetch homepage
2. Classify URLs: /lawyers/{id}, /area/{prefecture}/{city}, etc.
3. For each unique pattern:
   - Fetch ONE example URL
   - Extract DOM skeleton
   - Call AI to generate ALPS descriptors
4. Merge all descriptors into unified ALPS profile
5. Validate and generate HTML diagram
6. Save progress to handover.json
```

### Handover Protocol

The surveyor mode uses handover.json (per ADR 0006) to enable multi-session work. The handover uses a sessions array format to preserve historical context:

```json
{
  "$schema": "handover-protocol.json",
  "task": {
    "type": "alps-surveyor",
    "target": "example.com ALPS profile"
  },
  "current_state": {
    "session_id": "example-session-002",
    "total_sessions": 2,
    "alps_profile": {
      "total_descriptors": 480,
      "validation_status": "valid"
    }
  },
  "sessions": [
    {
      "session_id": "example-session-001",
      "timestamp": "2025-12-14T10:00:00Z",
      "handover_note": {
        "summary": "Initial crawl: search, consultation flows. 450 descriptors.",
        "advice": "Bookmark feature needs attention - saw /bookmarks/* URLs"
      },
      "descriptors_added": 450
    },
    {
      "session_id": "example-session-002",
      "timestamp": "2025-12-14T14:00:00Z",
      "handover_note": {
        "summary": "Added bookmark and billing features using asd merge. Profile now at 480 descriptors.",
        "advice": "Remaining: payment flows, mobile features, error states"
      },
      "descriptors_added": 30
    }
  ],
  "shared_context": {
    "patterns_learned": {
      "lawyer_profile": {"pattern": "/lawyers/{id}", "confidence": "high"}
    }
  },
  "pending_work": {
    "frontier_queue": [
      "https://example.com/payment/checkout",
      "https://example.com/dashboard"
    ]
  },
  "tools_available": {
    "crawler": {"command": "node packages/crawler/test.mjs <url>"},
    "merge": {"command": "asd merge <base> <source>"}
  }
}
```

**Key points:**
- Each session is appended to the `sessions` array
- `current_state` provides quick access to latest status
- `shared_context` accumulates patterns learned across all sessions
- Never overwrite sessions - always append new ones

### Best Practices for Surveyor Mode

1. **Start small**: Use `max_depth: 2` initially to test
2. **Exclude admin/auth pages**: Add to `exclude_patterns` to avoid login walls
3. **Review patterns**: Check `frontier_queue` in handover.json to verify coverage
4. **Iterative refinement**: Survey core features first, then expand in subsequent sessions
5. **Validate frequently**: Run `asd --validate` after each session to catch errors early

### Limitations

- Cannot access pages behind authentication (unless cookies provided)
- JavaScript-heavy SPAs may not be fully analyzed
- External services (e.g., chat.example.com) are noted but not crawled
- AI inference may miss domain-specific semantics (manual review recommended)

### Implementation Status

✅ Core library implemented:
- `packages/app-state-diagram/src/crawler/url-pattern-classifier.ts`
- `packages/app-state-diagram/src/crawler/dom-skeleton-extractor.ts`
- `packages/app-state-diagram/src/crawler/alps-descriptor-generator.ts`

⏳ Integration in progress:
- MCP tool (basic structure added)
- CLI command (`asd crawl`)
- ALPS skill support

## References

- [ALPS Specification](http://alps.io/spec/)
- [Schema.org](https://schema.org/)
- [app-state-diagram](https://github.com/alps-asd/app-state-diagram)
- [ADR 0006: Handover Protocol](../../dev-docs/adr/0006-handover-protocol-for-ai-agent-continuity.md)
