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

### Validate Existing Profile
- "Validate this ALPS profile" (with file path or content)
- "Check my ALPS file for issues"
- "Review the ALPS profile at docs/api.json"

### Get Improvement Suggestions
- "Improve this ALPS profile"
- "Suggest enhancements for my ALPS"
- "How can I make this ALPS better?"

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
   - **Functional area tags**: Group by feature domain (e.g., `search`, `product`, `cart`, `checkout`, `order`, `account`, `review`)
   - **Flow tags**: Group by user journey with `flow-` prefix (e.g., `flow-purchase`, `flow-register`, `flow-return`)
   - States and transitions should have both types where applicable
   - Tags are space-separated strings, not arrays
   - Example: A cart-related transition might have `"tag": "cart flow-purchase"`

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

7. **MANDATORY: Validate After Generation**
   - After generating ALPS JSON, save it to a temporary file
   - Run `asd --validate <file>` to validate (outputs JSON per validation-result.json schema)
   - Parse the JSON result and report issues to the user
   - If errors exist, fix them before presenting the final output

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

## Validation

Use `asd --validate <file>` to validate ALPS profiles. Output conforms to the [validation-result.json schema](https://alps-asd.github.io/app-state-diagram/schemas/validation-result.json).

### Error Codes (E)
- E001: Missing id or href
- E002: Missing rt on transition
- E003: Invalid type
- E004: Broken reference
- E005: Duplicate id
- E006: Invalid href
- E007: Invalid rt format
- E008: Missing alps property in document
- E009: Descriptor must be an array
- E010: Invalid XML character in descriptor title
- E011: Tag must be a string (space-separated), not an array

### Warning Codes (W)
- W001: Missing title
- W002: Safe transition naming (should start with 'go')
- W003: Unsafe/idempotent naming (should start with 'do')
- W004: Orphan descriptor
- W005: Safe transition id does not match rt target (e.g., `goStart` with `rt="#ProductList"` should be `goProductList`)
- W006: Tag contains comma - may be confused with space-separated format

### Suggestion Codes (S)
- S001: Missing doc on transition
- S002: Missing ALPS title
- S003: Missing ALPS doc

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
# Generate HTML diagram
asd profile.json

# Generate with watch mode
asd --watch profile.json

# Generate markdown documentation
asd --mode=markdown profile.json
```

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

## References

- [ALPS Specification](http://alps.io/spec/)
- [Schema.org](https://schema.org/)
- [app-state-diagram](https://github.com/alps-asd/app-state-diagram)
