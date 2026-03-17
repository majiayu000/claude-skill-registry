---
name: documentation
description: Generate docstrings, JSDoc, API docs, and README updates that reflect current code
triggers: [docs, docstring, JSDoc, README, API docs, document this, add documentation]
context_cost: medium
---

# Documentation Skill

## Goal
Generate accurate, useful documentation for public APIs, modules, and the project README. Documentation describes WHY and WHAT (not HOW — the code shows how). All examples must be working code.

## Steps

1. **Identify what needs documentation**
   - Public functions, methods, and classes (not private internals)
   - API endpoints (generate from OpenAPI spec or create if missing)
   - Complex business logic with non-obvious behavior
   - README sections that are outdated or missing

2. **Write function/method docstrings**

   **TypeScript (JSDoc):**
   ```typescript
   /**
    * Creates a new user account and sends a verification email.
    *
    * @param dto - User creation data (email, name, password)
    * @returns The created user without sensitive fields
    * @throws {EmailAlreadyExistsError} If email is already registered
    * @throws {WeakPasswordError} If password doesn't meet requirements
    *
    * @example
    * const user = await createUser({
    *   email: 'alice@example.com',
    *   name: 'Alice',
    *   password: 'SecureP@ss123'
    * });
    * // Returns: { id: 'uuid', email: 'alice@example.com', name: 'Alice' }
    */
   async function createUser(dto: CreateUserDto): Promise<UserDto>
   ```

   **PHP (PHPDoc):**
   ```php
   /**
    * Creates a new user account and sends a verification email.
    *
    * @param CreateUserData $data User creation data
    * @return UserResource The created user resource
    * @throws EmailAlreadyExistsException If email is already registered
    *
    * @example
    * $user = $this->createUser->handle(new CreateUserData(
    *     email: 'alice@example.com',
    *     name: 'Alice',
    * ));
    */
   public function handle(CreateUserData $data): UserResource
   ```

   **Python (Google Style / Sphinx):**
   ```python
   def create_user(dto: CreateUserDto) -> UserDto:
       """Creates a new user account and sends a verification email.

       Args:
           dto (CreateUserDto): User creation data (email, name, password).

       Returns:
           UserDto: The created user without sensitive fields.

       Raises:
           ValueError: If email is already registered.

       Example:
           >>> user = create_user(CreateUserDto(email="alice@example.com", ...))
           >>> print(user.id)
       """
       ...
   ```

3. **Verify examples are working**
   - Every code example in documentation must actually work
   - Run the example code to verify it doesn't throw or produce wrong output
   - If the example would require a running server/DB: note the prerequisite clearly

4. **Update README_FULL.md**
   - README sections to check:
     - **Getting Started**: install + first run commands
     - **Available commands**: from AGENTS.md Section 2 (keep in sync)
     - **Architecture overview**: high-level description + link to C4 diagrams
     - **Contributing**: how to run tests, branch naming, PR process
     - **Environment variables**: list all required env vars with descriptions
   - README must reflect the CURRENT state of the project, not aspirations

5. **Generate API documentation**
   If OpenAPI spec exists at `docs/api/openapi.yaml`:
   ```bash
   # Scalar API docs (modern UI)
   npx @scalar/cli serve docs/api/openapi.yaml

   # Redoc (alternative)
   npx @redocly/cli preview-docs docs/api/openapi.yaml
   ```

6. **Generate module documentation** (if tooling configured)
   ```bash
   # TypeDoc for TypeScript
   npx typedoc src/ --out docs/typedoc/

   # JSDoc for JavaScript
   npx jsdoc src/ -r -d docs/jsdoc/

   # Laravel Scribe for PHP APIs
   php artisan scribe:generate

   # MkDocs (Python)
   uv run mkdocs build
   ```

7. **Check for outdated documentation**
   - Scan for function signatures in docs that don't match current code
   - Check for documented parameters that no longer exist
   - Check for examples that import from paths that have moved

## Constraints
- Only document PUBLIC API surface (not private implementation details)
- NEVER document what the code obviously does — document WHY it works that way
- All code examples must be verified working
- Do not create documentation files unless explicitly requested — update existing ones

## Output Format
Updated docstrings in modified files + updated README sections. Report: "[N] functions documented, README sections updated: [list]."
