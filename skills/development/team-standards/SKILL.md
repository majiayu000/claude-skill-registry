---
name: team-standards
description: Team coding standards, conventions, and collaboration guidelines for WordPress development. Use when starting new projects, onboarding team members, or ensuring code consistency across the team.
---

# Team Coding Standards

Unified coding standards and collaboration practices for WordPress development teams.

## Core Principles

### 1. Code Quality First
- Write code that your teammates will thank you for
- If it's hard to explain, it's probably too complex
- Leave the codebase better than you found it

### 2. Communication is Key
- Comment the "why", not the "what"
- Use descriptive names that tell a story
- Document decisions in commit messages

### 3. Review with Kindness
- Assume positive intent
- Suggest improvements, don't demand them
- Celebrate good solutions

## WordPress Coding Standards

### PHP Conventions

```php
<?php
/**
 * Function description.
 *
 * @since 1.0.0
 *
 * @param int    $post_id Post ID.
 * @param string $context Optional. Context for the action. Default 'view'.
 * @return array|WP_Error Data array on success, WP_Error on failure.
 */
function prefix_get_post_data( $post_id, $context = 'view' ) {
    // Validate input early.
    if ( ! $post_id || $post_id < 1 ) {
        return new WP_Error( 'invalid_id', __( 'Invalid post ID provided.', 'textdomain' ) );
    }

    // Check capabilities.
    if ( 'edit' === $context && ! current_user_can( 'edit_post', $post_id ) ) {
        return new WP_Error( 'unauthorized', __( 'You do not have permission to edit this post.', 'textdomain' ) );
    }

    // Get the post.
    $post = get_post( $post_id );

    if ( ! $post ) {
        return new WP_Error( 'not_found', __( 'Post not found.', 'textdomain' ) );
    }

    return array(
        'id'      => $post->ID,
        'title'   => $post->post_title,
        'content' => $post->post_content,
    );
}
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Functions | `prefix_verb_noun` | `theme_get_featured_posts()` |
| Classes | `Prefix_Noun_Noun` | `Theme_Post_Handler` |
| Constants | `PREFIX_UPPER_CASE` | `THEME_VERSION` |
| Hooks | `prefix_context_action` | `theme_before_header` |
| Options | `prefix_setting_name` | `theme_primary_color` |
| Meta keys | `_prefix_meta_name` | `_theme_custom_field` |

### File Organization

```
plugin-name/
├── plugin-name.php          # Main file, minimal code
├── includes/
│   ├── class-plugin-name.php    # Main class
│   ├── class-admin.php          # Admin functionality
│   ├── class-public.php         # Frontend functionality
│   └── functions.php            # Helper functions
├── admin/
│   └── views/                   # Admin templates
├── public/
│   └── views/                   # Frontend templates
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
└── languages/
```

## Security Checklist (Every PR)

### Input/Output

- [ ] All user input sanitized (`sanitize_text_field()`, `absint()`, etc.)
- [ ] All output escaped (`esc_html()`, `esc_attr()`, `esc_url()`)
- [ ] SQL queries use `$wpdb->prepare()`
- [ ] File paths validated against allowed locations

### Authentication

- [ ] Forms include nonce fields (`wp_nonce_field()`)
- [ ] Form handlers verify nonce (`wp_verify_nonce()`)
- [ ] Capability checks before actions (`current_user_can()`)
- [ ] AJAX handlers use `check_ajax_referer()`

### Data Protection

- [ ] No sensitive data in error messages
- [ ] No debug output in production code
- [ ] API keys stored in options, not hardcoded
- [ ] User data handling follows privacy practices

## Code Review Process

### Before Submitting PR

1. **Self-Review Checklist**
   - [ ] Code follows team standards
   - [ ] Security checklist passed
   - [ ] No `var_dump()`, `console.log()` left behind
   - [ ] Functions are under 50 lines
   - [ ] Complex logic has comments explaining "why"

2. **Test Locally**
   - [ ] Works in target environment
   - [ ] No PHP errors/warnings
   - [ ] No JavaScript console errors
   - [ ] Tested on mobile (if frontend)

3. **Write Good PR Description**
   - What does this change?
   - Why is it needed?
   - How can it be tested?
   - Any concerns or areas to focus review?

### Reviewing Others' Code

**Tone Guidelines:**
- ✅ "What do you think about using X here? It might help with Y."
- ✅ "Nice solution! One small suggestion..."
- ✅ "I'm curious about this approach - could you explain the reasoning?"
- ❌ "This is wrong."
- ❌ "You should have done X."
- ❌ "Why didn't you just...?"

**Focus Areas:**
1. **Security** - Always check first
2. **Logic** - Does it do what it should?
3. **Performance** - Any obvious issues?
4. **Maintainability** - Will future devs understand?
5. **Standards** - Follows conventions?

**Approval Levels:**
- **Approve** - Ready to merge
- **Approve with suggestions** - Can merge, but consider improvements
- **Request changes** - Must fix before merge (security/bugs only)

## Git Workflow

### Branch Naming

```bash
feature/add-user-dashboard
fix/checkout-validation-error
hotfix/security-patch-v1.2.1
release/v2.0.0
```

### Commit Messages

```bash
# Format
type(scope): brief description

# Examples
feat(checkout): add express payment option
fix(cart): resolve quantity update on mobile
docs(readme): update installation steps
refactor(api): simplify error response handling
```

### PR Workflow

1. Create feature branch from `main`
2. Make changes with atomic commits
3. Push and create PR
4. Request review from at least 1 teammate
5. Address feedback
6. Squash and merge when approved

## Documentation Standards

### Code Comments

```php
<?php
// Single line for brief notes.

/*
 * Multi-line for longer explanations.
 * Especially useful for complex logic.
 */

/**
 * DocBlocks for functions, classes, and methods.
 * These appear in IDE tooltips and generated docs.
 */
```

### README Template

```markdown
# Plugin/Theme Name

Brief description of what this does.

## Requirements

- WordPress 6.0+
- PHP 8.0+
- [Any dependencies]

## Installation

1. Step one
2. Step two
3. Step three

## Configuration

How to configure after installation.

## Usage

Common use cases with examples.

## Hooks Reference

### Actions
- `prefix_action_name` - When it fires, what it's for

### Filters
- `prefix_filter_name` - What it filters, expected return

## Changelog

### 1.0.0
- Initial release

## Support

How to get help.
```

## Communication Guidelines

### In Code Reviews

**Asking for Changes:**
> "Hey! This looks great overall. I noticed the SQL query on line 45 might benefit from `$wpdb->prepare()` for security. Would you mind updating that? Happy to help if you'd like to pair on it!"

**Suggesting Improvements:**
> "Nice work on this feature! One thought - we could potentially use `wp_cache_get()` here to avoid repeated database calls. What do you think? Not blocking, just an idea for future optimization."

**Approving:**
> "Looks great! Clean code and well-documented. Approved! 🎉"

### In Documentation

- Use "you" to address the reader directly
- Use "we" when referring to the team/product
- Keep sentences short and scannable
- Include examples for complex features
- Add helpful tips with friendly icons (💡, ✅, ⚠️)

### With Clients

- Lead with solutions, not problems
- Explain technical concepts in plain language
- Set clear expectations with timelines
- Celebrate wins and milestones together

## Quick Reference Cards

### Security Quick Check

```
✅ Sanitize: sanitize_text_field(), absint(), sanitize_email()
✅ Escape: esc_html(), esc_attr(), esc_url(), wp_kses_post()
✅ Validate: is_email(), wp_verify_nonce(), current_user_can()
✅ Prepare: $wpdb->prepare() for all SQL with variables
```

### Performance Quick Check

```
✅ Use transients/cache for expensive operations
✅ Limit queries with posts_per_page (never -1 on frontend)
✅ Use no_found_rows => true when not paginating
✅ Lazy load images and defer non-critical JS
✅ Conditionally enqueue assets only where needed
```

### Accessibility Quick Check

```
✅ All images have alt text
✅ Form inputs have labels
✅ Color contrast meets WCAG AA
✅ Keyboard navigation works
✅ Skip link present in themes
```
