---
name: artisan-commands
description: Execute Laravel Artisan commands safely
triggers: [artisan, laravel, php artisan, make controller, migrate]
context_cost: low
---

# Artisan Commands Skill

## Goal
Execute Laravel Artisan commands to scaffold code, run migrations, or manage the application state.

## Steps

1. **Verify Context**
   - Ensure you are in the root of a Laravel project (look for `artisan` file).
   - If not found, stop and ask user for correct directory.

2. **Construct Command**
   - Use `php artisan <command> <arguments>`.
   - Examples:
     - `php artisan make:controller UserController`
     - `php artisan make:model Post -m`
     - `php artisan migrate:status`
   - NEVER run `migrate:fresh` or destructive commands without explicit user confirmation.

3. **Execute**
   - Run the command using `run_command`.
   - Capture output.

4. **Verify**
   - Check exit code is 0.
   - Verify the expected file was created (e.g., `app/Http/Controllers/UserController.php`).
   - If migration, verify table exists (using command output).

## Constraints
- Do NOT run commands that wipe data (`migrate:fresh`, `db:wipe`) without asking.
- Do NOT run `tinker` in a way that hangs the shell (interactive mode).
