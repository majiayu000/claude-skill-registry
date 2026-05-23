---
name: drupal-standards
description: Automatically applies Drupal coding standards when developing PHP modules, JavaScript, CSS, SQL queries, Twig templates, or YAML configs. Activates when creating/editing .php, .js, .css, .sql, .twig, .yml files or when user mentions "module", "query", "template", "form", or "custom code".
---

# Drupal Coding Standards

Apply Drupal coding standards based on the development context.

## Core Principles

From `coding_standards/index.md`:
- All code must follow Drupal coding standards (version-independent)
- Use US English spelling in all comments and names
- Standards are "always-current" and apply to all new code
- Follow Boy Scout Rule: leave code better than you found it

## Context Detection & Standard Loading

### PHP Development (.php files, modules, services, plugins)

When working with PHP code, **ALWAYS read these standards FIRST**:

1. **Core Standards**: Read `coding_standards/php/coding.md`
2. **Documentation**: Read `coding_standards/php/documentation.md`
3. **Namespaces**: Read `coding_standards/php/namespaces.md`
4. **PSR-4**: Read `coding_standards/php/psr4.md`

Additionally, based on specific needs:
- Creating services → Read `coding_standards/php/naming-services.md`
- Exception handling → Read `coding_standards/php/exceptions.md`
- Using placeholders → Read `coding_standards/php/placeholders-delimiters.md`
- Error handling → Read `coding_standards/php/e_all.md`
- Documentation examples → Read `coding_standards/php/documentation-examples.md`

### JavaScript Development (.js files)

**ALWAYS read these standards FIRST**:

1. **Core Standards**: Read `coding_standards/javascript/coding.md`
2. **Documentation**: Read `coding_standards/javascript/documentation.md`
3. **Best Practices**: Read `coding_standards/javascript/best-practice.md`
4. **ESLint Config**: Read `coding_standards/javascript/eslint.md`

If using jQuery:
- Read `coding_standards/javascript/jquery.md`

### CSS Development (.css, .scss files, styling)

**ALWAYS read these standards FIRST**:

1. **Core Standards**: Read `coding_standards/css/coding.md`
2. **Formatting**: Read `coding_standards/css/format.md`
3. **File Organization**: Read `coding_standards/css/file-organization.md`
4. **Architecture**: Read `coding_standards/css/architecture.md`

For tool configuration:
- Read `coding_standards/css/csscomb.md`
- Read `coding_standards/css/review.md`

### SQL Queries (database operations)

**ALWAYS read these standards FIRST**:

1. **Conventions**: Read `coding_standards/sql/conventions.md`
2. **Keywords**: Read `coding_standards/sql/keywords.md`
3. **SELECT Queries**: Read `coding_standards/sql/select-from.md`

### Twig Templates (.twig files)

**ALWAYS read these standards**:

1. **Twig Standards**: Read `coding_standards/twig/coding.md`
2. **Markup Standards**: Read `coding_standards/markup/style.md`

### YAML Configuration (.yml, .yaml files)

**ALWAYS read**:
- Read `coding_standards/yaml/configuration-files.md`

### Composer Packages (composer.json)

**ALWAYS read**:
- Read `coding_standards/composer/package-name.md`

### Accessibility (forms, UI components, interactive elements)

**ALWAYS read**:
- Read `coding_standards/accessibility/accessibility.md`

### Spelling & General

**ALWAYS apply**:
- Read `coding_standards/spelling/spelling.md` (US English required)

## Workflow

```
1. User requests development task
   ↓
2. Identify file types/context (PHP, JS, CSS, SQL, etc.)
   ↓
3. Read ALL relevant standard files from coding_standards/
   ↓
4. Apply standards while writing code
   ↓
5. Validate code against standards
   ↓
6. Complete task with compliant code
```

## Multi-Context Tasks

For tasks involving multiple file types, load **ALL** relevant standards:

**Example: Creating a custom module**
- PHP standards (module code)
- JavaScript standards (if includes JS)
- CSS standards (if includes styling)
- Twig standards (if includes templates)
- YAML standards (for .info.yml and config files)
- Accessibility standards (if includes UI)

## Application Rules

1. **Read First, Write Second**: Always read relevant standards before generating code
2. **No Assumptions**: Never assume standards—always verify from files
3. **Exact Compliance**: Follow standards exactly as written
4. **US English Only**: All comments, variable names, and documentation
5. **Complete Coverage**: If working with multiple file types, apply all relevant standards
6. **Validation**: Before completing, verify code against loaded standards

## Examples

### Example 1: Creating a PHP Service

```
User: "Create a service to handle user notifications"

Actions:
1. Identify: PHP service development
2. Read standards:
   - coding_standards/php/coding.md
   - coding_standards/php/documentation.md
   - coding_standards/php/namespaces.md
   - coding_standards/php/naming-services.md
3. Generate code following all standards
4. Include proper docblocks, namespaces, service naming
```

### Example 2: Writing Database Query

```
User: "Write a query to get active users with roles"

Actions:
1. Identify: SQL query
2. Read standards:
   - coding_standards/sql/conventions.md
   - coding_standards/sql/keywords.md
   - coding_standards/sql/select-from.md
3. Write query with proper keyword capitalization and formatting
```

### Example 3: Building an Accessible Form

```
User: "Create a contact form with validation"

Actions:
1. Identify: Multi-context (PHP form API, JavaScript validation, accessibility)
2. Read standards:
   - coding_standards/php/coding.md
   - coding_standards/php/documentation.md
   - coding_standards/javascript/coding.md
   - coding_standards/markup/style.md
   - coding_standards/accessibility/accessibility.md
3. Build form with all standards applied
4. Ensure full accessibility compliance
```

## Critical Reminders

- **Never skip reading standards** - always load them before coding
- **Standards override preferences** - follow Drupal standards exactly
- **When uncertain** - read additional related standard files
- **Multi-file tasks** - load standards for ALL file types involved
- **US English spelling** - non-negotiable requirement
