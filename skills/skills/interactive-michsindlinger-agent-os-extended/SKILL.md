---
description: Generate and display skill preview for user review before saving
version: 1.0
encoding: UTF-8
---

# Skill Preview

## Overview

Generate a comprehensive preview of the skill file before saving, allowing the user to review the content, structure, and improvements that will be included.

## Preview Generation

<preview_flow>

<step number="1" name="generate_preview">

### Step 1: Generate Preview Content

Create abbreviated preview showing key sections.

<preview_structure>
  SECTIONS:
    1. Header (skill name, description, framework)
    2. Frontmatter preview
    3. Key patterns summary (top 5)
    4. Improvements applied
    5. File globs covered
    6. Statistics

  LENGTH: Approximately 100-150 lines
  PURPOSE: Give user quick overview without overwhelming detail
</preview_structure>

</step>

<step number="2" name="format_preview">

### Step 2: Format Preview Display

Create readable, formatted preview.

<preview_template>
  ═══════════════════════════════════════════════════════════════
  📄 SKILL PREVIEW
  ═══════════════════════════════════════════════════════════════

  Skill Name: {project_name}-{skill_type}-patterns
  Description: {framework} {skill_type} patterns for {project_name}
  Framework: {framework} {version}
  Generated: {timestamp}

  ───────────────────────────────────────────────────────────────
  📋 FRONTMATTER
  ───────────────────────────────────────────────────────────────

  ```yaml
  ---
  name: {skill_name}
  description: {description}
  version: {framework_version}
  framework: {framework}
  created: {date}
  globs:
    {glob_list}
  ---
  ```

  ───────────────────────────────────────────────────────────────
  🎯 KEY PATTERNS (Top 5)
  ───────────────────────────────────────────────────────────────

  1. ✅ {pattern_1_title}
     Category: {category}
     Status: {enhanced|original|added}
     Usage: Found in {file_count} files

     ```{language}
     {code_snippet_abbreviated}
     ```

  2. ✅ {pattern_2_title}
     ...

  [3 more patterns...]

  ───────────────────────────────────────────────────────────────
  ✨ IMPROVEMENTS APPLIED ({count})
  ───────────────────────────────────────────────────────────────

  Critical Improvements: {critical_count}
  ❌ {improvement_1_title}
  ❌ {improvement_2_title}

  Warnings Addressed: {warning_count}
  ⚠️ {improvement_3_title}
  ⚠️ {improvement_4_title}

  Info Suggestions: {info_count}
  ℹ️ {improvement_5_title}

  ───────────────────────────────────────────────────────────────
  📁 FILE COVERAGE
  ───────────────────────────────────────────────────────────────

  This skill will be active for files matching:
  - {glob_1}
  - {glob_2}
  - {glob_3}
  ...

  Estimated coverage: {file_count} files in your project

  ───────────────────────────────────────────────────────────────
  📊 STATISTICS
  ───────────────────────────────────────────────────────────────

  Total Patterns: {pattern_count}
  - Best Practices: {best_practice_count}
  - Common Patterns: {common_pattern_count}
  - Anti-Patterns Documented: {anti_pattern_count}

  Code Examples: {example_count}
  Improvements Applied: {improvement_count}
  Framework Version: {version}

  ───────────────────────────────────────────────────────────────
  📝 CONTENT SECTIONS
  ───────────────────────────────────────────────────────────────

  ✓ Framework Configuration
  ✓ Best Practices ({best_practice_count} patterns)
  ✓ Common Patterns ({common_pattern_count} patterns)
  ✓ Anti-Patterns to Avoid ({anti_pattern_count} items)
  ✓ Implementation Examples ({example_count} examples)
  ✓ Quick Reference
  ✓ References & Documentation

  ═══════════════════════════════════════════════════════════════
  END OF PREVIEW
  ═══════════════════════════════════════════════════════════════

  To view the full skill content, select "Show full content".
  To save this skill, select "Yes, save it".
</preview_template>

</step>

<step number="3" name="show_improvements_summary">

### Step 3: Show Improvements Summary

Highlight the improvements that were applied.

<improvements_summary>
  FORMAT:
    "✨ IMPROVEMENTS APPLIED

     You selected {accepted_count} out of {total_count} improvements.

     These improvements are now included in your skill as:

     BEST PRACTICES SECTION:
     - {improvement_1_title} (with before/after examples)
     - {improvement_2_title} (with implementation guide)

     ANTI-PATTERNS SECTION:
     - What NOT to do (based on discovered anti-patterns)
     - Safer alternatives with code examples

     IMPLEMENTATION EXAMPLES:
     - Side-by-side comparisons showing improvements
     - Benefits and rationale for each change

     {critical_warning}
     "

  CRITICAL_WARNING (if any critical rejected):
    "⚠️ NOTE: {count} critical issue(s) were skipped:
     - {critical_issue_1}

     These are documented in the 'Known Issues' section for
     your awareness."
</improvements_summary>

</step>

<step number="4" name="provide_options">

### Step 4: Provide User Options

Present actions user can take.

<user_options>
  QUESTION: "What would you like to do?"

  OPTIONS:
    1. "✅ Yes, save it" (Recommended)
       → Save skill to .claude/skills/
       → Show success message with next steps

    2. "📖 Show full content"
       → Display complete skill file
       → Return to this menu after

    3. "🔍 Show specific section"
       → Ask which section to view
       → Display selected section
       → Return to this menu

    4. "❌ No, cancel"
       → Confirm cancellation
       → Offer to start over or exit

    5. "✏️ Make changes"
       → Ask what to change
       → Options: "Review improvements again" | "Change project name" | "Cancel"

  DEFAULT: Option 1 (Save)
</user_options>

</step>

<step number="5" name="show_full_content">

### Step 5: Show Full Content (if requested)

Display complete skill file.

<full_content_display>
  IF user selects "Show full content":
    DISPLAY: Complete generated skill file
    FORMAT: Markdown with syntax highlighting

    HEADER:
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
       FULL SKILL CONTENT
       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

       {complete_skill_markdown}

       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
       END OF FULL CONTENT
       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
       "

    THEN: Show options again
      "Would you like to save this skill?"
      Options: "Yes, save it" | "No, cancel"
</full_content_display>

</step>

<step number="6" name="show_section">

### Step 6: Show Specific Section (if requested)

Display individual sections on demand.

<section_display>
  IF user selects "Show specific section":
    ASK: Which section?
    OPTIONS:
      - "Frontmatter"
      - "Best Practices"
      - "Common Patterns"
      - "Anti-Patterns"
      - "Implementation Examples"
      - "Quick Reference"
      - "Back to preview"

    DISPLAY: Selected section with context

    EXAMPLE (Best Practices):
      "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
       SECTION: BEST PRACTICES
       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

       {best_practices_section_content}

       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
       "

    THEN: Ask for next action
      "Show another section or return to preview?"
</section_display>

</step>

</preview_flow>

## Example Preview Output

<example_preview>
  ═══════════════════════════════════════════════════════════════
  📄 SKILL PREVIEW
  ═══════════════════════════════════════════════════════════════

  Skill Name: user-management-api-patterns
  Description: Spring Boot 3.2.0 API patterns for user-management-api
  Framework: Spring Boot 3.2.0
  Generated: 2025-12-31 10:45:00

  ───────────────────────────────────────────────────────────────
  📋 FRONTMATTER
  ───────────────────────────────────────────────────────────────

  ```yaml
  ---
  name: user-management-api-patterns
  description: Spring Boot 3.2.0 API patterns for user-management-api
  version: 3.2.0
  framework: spring-boot
  created: 2025-12-31
  globs:
    - "src/**/*Controller.java"
    - "src/**/*Service.java"
    - "src/**/*Repository.java"
    - "src/**/dto/**/*.java"
  ---
  ```

  ───────────────────────────────────────────────────────────────
  🎯 KEY PATTERNS (Top 5)
  ───────────────────────────────────────────────────────────────

  1. ✅ REST Endpoint with ResponseEntity
     Category: Routing
     Status: Enhanced (improvement applied)
     Usage: Found in 12 files

     ```java
     @GetMapping("/{id}")
     public ResponseEntity<UserResponse> getUser(@PathVariable Long id) {
         User user = userService.findById(id);
         return ResponseEntity.ok(toResponse(user));
     }
     ```

  2. ✅ Centralized Exception Handling
     Category: Error Handling
     Status: Added (from improvement)
     Usage: New pattern (replaces 15 individual handlers)

     ```java
     @ControllerAdvice
     public class GlobalExceptionHandler {
         @ExceptionHandler(UserNotFoundException.class)
         public ResponseEntity<ErrorResponse> handleUserNotFound(...) {
             // Consistent error handling
         }
     }
     ```

  3. ✅ Service Layer with Transactions
     Category: Business Logic
     Status: Enhanced
     Usage: Found in 8 files

     ```java
     @Service
     @Transactional(readOnly = true)
     public class UserService {
         @Transactional
         public User create(UserRequest request) { ... }
     }
     ```

  4. ✅ JPA Repository Query Methods
     Category: Data Access
     Status: Enhanced (security improvement)
     Usage: Found in 5 files

     ```java
     public interface UserRepository extends JpaRepository<User, Long> {
         Optional<User> findByEmail(String email);
         Page<User> findByActiveTrue(Pageable pageable);
     }
     ```

  5. ✅ Request Validation with Bean Validation
     Category: Validation
     Status: Original
     Usage: Found in 10 files

     ```java
     @PostMapping
     public ResponseEntity<?> create(@Valid @RequestBody UserRequest request) {
         // Validation handled by Spring
     }
     ```

  ───────────────────────────────────────────────────────────────
  ✨ IMPROVEMENTS APPLIED (8)
  ───────────────────────────────────────────────────────────────

  Critical Improvements: 2
  ❌ Fix SQL injection vulnerability (security)
  ❌ Implement centralized error handling (maintainability)

  Warnings Addressed: 5
  ⚠️ Add @Transactional to service methods
  ⚠️ Implement pagination with Pageable
  ⚠️ Use Optional for nullable returns
  ⚠️ Add request validation
  ⚠️ Implement proper logging

  Info Suggestions: 1
  ℹ️ Add API documentation with Swagger

  ───────────────────────────────────────────────────────────────
  📁 FILE COVERAGE
  ───────────────────────────────────────────────────────────────

  This skill will be active for files matching:
  - src/**/*Controller.java
  - src/**/*Service.java
  - src/**/*Repository.java
  - src/**/dto/**/*.java

  Estimated coverage: 45 files in your project

  ───────────────────────────────────────────────────────────────
  📊 STATISTICS
  ───────────────────────────────────────────────────────────────

  Total Patterns: 35
  - Best Practices: 12 (including 8 improvements)
  - Common Patterns: 20
  - Anti-Patterns Documented: 3

  Code Examples: 42
  Improvements Applied: 8
  Framework Version: Spring Boot 3.2.0

  ───────────────────────────────────────────────────────────────
  📝 CONTENT SECTIONS
  ───────────────────────────────────────────────────────────────

  ✓ Framework Configuration
  ✓ Best Practices (12 patterns)
  ✓ Common Patterns (20 patterns)
  ✓ Anti-Patterns to Avoid (3 items)
  ✓ Implementation Examples (8 before/after comparisons)
  ✓ Quick Reference
  ✓ References & Documentation

  ═══════════════════════════════════════════════════════════════
  END OF PREVIEW
  ═══════════════════════════════════════════════════════════════

  What would you like to do?
</example_preview>

## Output Format

<output>
  {
    preview_displayed: true,
    user_action: "save" | "view_full" | "view_section" | "cancel" | "modify",
    sections_viewed: ["best_practices", "implementation_examples"],
    timestamp: "2025-12-31T10:45:00Z"
  }
</output>

## Error Handling

<error_protocols>
  <preview_generation_failure>
    FALLBACK: Show basic summary
    MESSAGE: "Preview generation encountered an issue. Showing basic summary."
    OFFER: "View full content" | "Save anyway" | "Cancel"
  </preview_generation_failure>

  <large_skill_file>
    IF skill_content > 10000 lines:
      WARN: "Large skill file ({line_count} lines)"
      SUGGEST: "Showing abbreviated preview. Use 'Show full content' to see all."
  </large_skill_file>
</error_protocols>

## Related Utilities

- `@agent-os/workflows/skill/utils/assemble-skill.md`
- `@agent-os/workflows/skill/utils/generate-frontmatter.md`
