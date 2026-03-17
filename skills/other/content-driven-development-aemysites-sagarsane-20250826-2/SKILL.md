---
name: Using Content Driven Development
description: Apply a Content Driven Development process to AEM Edge Delivery Services development. Use for all development tasks, including building new blocks, modifying existing blocks, making changes to core decoration functionality, etc.
---

# Using Content Driven Development (CDD)

Content Driven Development is a mandatory process for AEM Edge Delivery Services development that prioritizes content and author needs over developer convenience. This skill orchestrates the development workflow to ensure code is built against real content with author-friendly content models.

## Why Content-First Matters

**Author needs come before developer needs.** When building for AEM Edge Delivery, authors are the primary users of the structures we create. Content models must be intuitive and easy to work with, even if that means more complex decoration code.

**Efficiency through preparation.** Creating or identifying test content before coding provides:
- **Immediate testing capability**: No need to stop development to create test content
- **Better PR workflows**: Test content doubles as PR validation links for PSI checks
- **Living documentation**: Test content often serves as author documentation and examples
- **Fewer assumptions**: Real content reveals edge cases code-first approaches miss

**NEVER start writing or modifying code without first identifying or creating the content you will use to test your changes.**

## When to Apply This Skill

Apply Content Driven Development principles to ALL AEM development tasks:

- ✅ Creating new blocks
- ✅ Modifying existing blocks (structural or functional changes)
- ✅ Changes to core decoration functionality
- ✅ Bug fixes that require validation
- ✅ Any code that affects how authors create or structure content

Skip CDD only for:
- ⚠️ Trivial CSS-only styling tweaks (but still identify test content for validation)
- ⚠️ Configuration changes that don't affect authoring

When in doubt, follow the CDD process. The time invested pays dividends in quality and efficiency.

## Related Skills

This skill orchestrates other skills at the appropriate stages:

- **content-modeling**: Invoked when new content models need to be designed or existing models modified
- **building-blocks**: Invoked during implementation phase for block creation or modification
- **testing-blocks**: Referenced during validation phase for comprehensive testing
- **block-collection-and-party**: Used to find similar blocks and reference implementations

## The Content-First Process

Follow these phases in order. Do not skip steps.

### Phase 1: Content Discovery and Modeling

The first phase establishes what content you're working with and ensures the content model is author-friendly.

#### Step 1.1: Determine Content Availability

**For new blocks:**

Skip to Step 1.2 (Content Model Design). Searching for content that doesn't exist is a waste of time.

**For modifications to existing blocks:**

Ask the user: "Does content using this block already exist that we can use for testing?"

- **YES** → Identify existing content to test against
  - Use the `scripts/find-block-content.js` script to search for pages containing the block
  - Or ask the user: "What are the path(s) to page(s) with this block?"
  - Validate the content loads correctly in your local dev environment
  - Proceed to Phase 2 (skip content modeling if structure isn't changing)

- **NO existing content** → Proceed to Step 1.2

#### Step 1.2: Content Model Design

**REQUIRED for:**
- All new blocks
- Structural changes to existing blocks (adding/removing/modifying sections, variants, or the authoring structure)

**Ask the user:**
"This requires a new content model. Would you like me to use the content-modeling skill to design an author-friendly content model now?"

- **YES** → Invoke the **content-modeling** skill
  - Follow the content modeling process completely
  - Return to this skill when content model is defined
  - Proceed to Step 1.3

- **NO** → The user may want to define it themselves
  - Ask: "Please describe the content structure authors will use"
  - Document their description for reference
  - Proceed to Step 1.3

#### Step 1.3: Content Creation

Once the content model is defined (from Step 1.2), you need test content.

**Ask the user:**
"We need test content for development and validation. This content will serve multiple purposes:
- Testing during development
- PR validation link for PSI checks
- Author documentation and examples

Would you like to:
1. Create this content in the CMS now (Google Drive/SharePoint/DA/Universal Editor)
2. Create temporary local HTML files for testing (will need CMS content before PR)"

**Option 1: CMS Content (Recommended)**
- Guide the user through creating content in their CMS
- Wait for user confirmation that content is created and published
- Get the content URL(s) from the user
- Validate content loads in local dev environment
- Proceed to Phase 2

**Option 2: Local HTML Files (Temporary)**
- Create HTML file(s) in `drafts/` folder matching the content model structure
- Reference the [HTML Structure Guide](resources/html-structure.md) for proper file format
- Remind user: "Restart your dev server with: `aem up --html-folder drafts`"
- Note: "You will need to create actual CMS content before raising a PR"
- Proceed to Phase 2

##### Making Test Content Serve as Author Documentation

Test content can often double as author-facing documentation, saving time and keeping documentation current. Consider this when creating test content:

**When test content IS sufficient as author documentation:**
- The block is straightforward with clear patterns
- Test content shows all variants and use cases
- Content demonstrates best practices authors should follow
- Examples are realistic and relatable to actual use cases

**When separate author documentation is needed:**
- Block has complex configuration or many variants requiring explanation
- There are edge cases or gotchas authors need to understand
- Project standards require formal documentation in a specific location/format
- Block behavior isn't self-evident from examples alone

**Structuring test content to serve both purposes:**
1. **Create comprehensive examples**: Show all variants, edge cases, and common patterns
2. **Use realistic content**: Avoid "lorem ipsum" or technical placeholders
3. **Demonstrate best practices**: Structure content the way authors should
4. **Consider location**: Place content where it can serve as documentation
   - Sidekick Library projects: Consider creating in `/tools/sidekick/library/` or appropriate library location
   - Document Authoring: Place in DA Library structure
   - Simple documentation: Use `/drafts/docs/` or `/drafts/library/`
   - Universal Editor: Follow project-specific documentation patterns

**Ask the user about documentation approach:**
"Should this test content also serve as author documentation? If so, we can structure it accordingly and place it in an appropriate location (e.g., `/drafts/library/{block-name}` or your project's library system)."

If yes, guide content creation with documentation in mind. If no, proceed with test-focused content and note that author documentation will be needed later.

### Phase 2: Implementation

**CRITICAL: Do not begin Phase 2 until you have confirmed test content exists and is accessible.**

Now that test content exists, proceed with implementation:

#### For Block Development

Invoke the **building-blocks** skill:
- Provide the skill with the content model and test content URL(s)
- Follow the building-blocks process for implementation
- Return to this skill when implementation is complete
- Proceed to Phase 3

#### For Core Functionality Changes

Follow standard development practices:
- Make changes to scripts, styles, or configuration
- Test against the identified content throughout development
- Ensure changes don't break existing blocks or content models
- Proceed to Phase 3

### Phase 3: Validation

The final phase ensures the implementation works correctly with real content.

#### Step 3.1: Test with Real Content

**Mandatory testing:**
- ✅ View test content in local dev environment
- ✅ Verify all variants render correctly
- ✅ Check responsive behavior (mobile, tablet, desktop)
- ✅ Test edge cases revealed by the actual content
- ✅ Validate accessibility basics (keyboard navigation, screen reader friendly)

#### Step 3.2: Run Quality Checks

**Required before considering implementation complete:**

```bash
npm run lint
```

If linting fails, fix issues with:
```bash
npm run lint:fix
```

#### Step 3.3: Comprehensive Testing

**The testing-blocks skill is automatically invoked by building-blocks** for block development.

For other code changes, or for additional testing guidance, invoke the **testing-blocks** skill which provides:
- Unit testing strategies for logic-heavy utilities
- Browser testing with Playwright/Puppeteer
- Linting and code quality checks
- Performance validation with GitHub checks
- Guidance on keeper vs throwaway tests

#### Step 3.4: PR Preparation

**Before raising a PR, ensure:**
- ✅ Test content exists in the CMS (not just local HTML)
- ✅ Test content URL is accessible for PSI checks
- ✅ All linting passes
- ✅ Author documentation is updated (if applicable)

The test content URL will be used as the PR validation link.

## Anti-Patterns to Avoid

**Common mistakes:**
- ❌ Starting with code before understanding the content model
- ❌ Making assumptions about content structure without seeing real examples
- ❌ Creating developer-friendly but author-hostile content models
- ❌ Skipping content creation "to save time" (costs more time later)
- ❌ Testing against imagined content instead of real content
- ❌ Treating test content creation as separate from development workflow

## Workflow Summary

**Quick reference for the CDD process:**

```
1. CONTENT DISCOVERY
   └─ Existing content? → Use it
   └─ New block/structure? → Design content model → Create test content

2. IMPLEMENTATION
   └─ Build code against the real content model
   └─ Test continuously with actual content

3. VALIDATION
   └─ Comprehensive testing with test content
   └─ Quality checks (linting, accessibility)
   └─ PR preparation with test URL

KEY RULE: Never proceed to implementation without test content
```

## Scripts and Tools

### Finding Existing Block Content

Use the provided script to search for pages containing a specific block:

```bash
# Search on localhost (default)
node .claude/skills/content-driven-development/scripts/find-block-content.js <block-name>

# Search for specific variant
node .claude/skills/content-driven-development/scripts/find-block-content.js <block-name> localhost:3000 <variant>

# Search on live site
node .claude/skills/content-driven-development/scripts/find-block-content.js <block-name> main--repo--owner.aem.live

# Search on preview with variant
node .claude/skills/content-driven-development/scripts/find-block-content.js <block-name> main--repo--owner.aem.page <variant>
```

**Examples:**
```bash
node .claude/skills/content-driven-development/scripts/find-block-content.js hero
node .claude/skills/content-driven-development/scripts/find-block-content.js hero localhost:3000 dark
node .claude/skills/content-driven-development/scripts/find-block-content.js cards main--site--owner.aem.live three-up
```

This script queries the site's query-index to find all pages containing the specified block (and optional variant) and returns their URLs. The script uses proper DOM parsing to accurately identify blocks.

## Integration with Other Skills

This skill acts as the orchestrator for AEM development workflows:

**At Content Modeling stage:**
→ Invoke **content-modeling** skill for author-friendly design

**At Implementation stage:**
→ Invoke **building-blocks** skill for block development
→ Reference **block-collection-and-party** skill for patterns

**At Validation stage:**
→ Reference **testing-blocks** skill for comprehensive testing

Following this orchestration ensures all development follows content-first principles.
