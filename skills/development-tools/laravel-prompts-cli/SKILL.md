---
name: laravel-prompts-cli
description: >-
  Builds interactive CLI commands with Laravel Prompts. Activates when creating Artisan commands
  with user input, interactive prompts, progress bars, or when user mentions CLI, command, prompt,
  interactive, terminal input, or Artisan command with user interaction.
---

# Laravel Prompts CLI Development

## When to Apply

Activate this skill when:

- Creating Artisan commands with interactive input
- Building CLI wizards or setup scripts
- Adding progress indicators to commands
- Collecting user input in terminal
- Creating confirmation dialogs

## Documentation

Use `search-docs` for detailed Laravel Prompts patterns and documentation.

## Basic Prompts

### Text Input

<code-snippet name="Text Prompt" lang="php">
use function Laravel\Prompts\text;

$name = text(
    label: 'What is your name?',
    placeholder: 'E.g. John Doe',
    default: '',
    required: true,
    validate: fn (string $value) => match (true) {
        strlen($value) < 2 => 'Name must be at least 2 characters.',
        default => null,
    },
    hint: 'This will be displayed publicly.',
);
</code-snippet>

### Password Input

<code-snippet name="Password Prompt" lang="php">
use function Laravel\Prompts\password;

$password = password(
    label: 'Enter your password',
    required: true,
    validate: fn (string $value) => match (true) {
        strlen($value) < 8 => 'Password must be at least 8 characters.',
        default => null,
    },
);
</code-snippet>

### Confirmation

<code-snippet name="Confirm Prompt" lang="php">
use function Laravel\Prompts\confirm;

$confirmed = confirm(
    label: 'Do you want to continue?',
    default: true,
    yes: 'Yes, proceed',
    no: 'No, cancel',
    hint: 'This action cannot be undone.',
);
</code-snippet>

### Select

<code-snippet name="Select Prompt" lang="php">
use function Laravel\Prompts\select;

$role = select(
    label: 'What role should the user have?',
    options: [
        'admin' => 'Administrator',
        'editor' => 'Editor',
        'viewer' => 'Viewer',
    ],
    default: 'viewer',
    hint: 'The role determines access permissions.',
);
</code-snippet>

### Multi-Select

<code-snippet name="Multi-Select Prompt" lang="php">
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'Select permissions',
    options: [
        'create' => 'Create',
        'read' => 'Read',
        'update' => 'Update',
        'delete' => 'Delete',
    ],
    default: ['read'],
    required: true,
    hint: 'Use space to select, enter to confirm.',
);
</code-snippet>

### Search

<code-snippet name="Search Prompt" lang="php">
use function Laravel\Prompts\search;

$userId = search(
    label: 'Search for a user',
    options: fn (string $value) => strlen($value) > 0
        ? User::where('name', 'like', "%{$value}%")
            ->pluck('name', 'id')
            ->all()
        : [],
    placeholder: 'Start typing to search...',
);
</code-snippet>

### Suggest (Autocomplete)

<code-snippet name="Suggest Prompt" lang="php">
use function Laravel\Prompts\suggest;

$framework = suggest(
    label: 'What is your favorite framework?',
    options: ['Laravel', 'Symfony', 'Rails', 'Django'],
    placeholder: 'E.g. Laravel',
);
</code-snippet>

## Progress Indicators

### Progress Bar

<code-snippet name="Progress Bar" lang="php">
use function Laravel\Prompts\progress;

$users = progress(
    label: 'Processing users',
    steps: User::all(),
    callback: fn (User $user) => $this->processUser($user),
    hint: 'This may take a while...',
);
</code-snippet>

### Spinner

<code-snippet name="Spinner" lang="php">
use function Laravel\Prompts\spin;

$response = spin(
    message: 'Fetching data from API...',
    callback: fn () => Http::get('https://api.example.com/data')->json(),
);
</code-snippet>

## Output

### Info, Warning, Error

<code-snippet name="Output Messages" lang="php">
use function Laravel\Prompts\info;
use function Laravel\Prompts\warning;
use function Laravel\Prompts\error;
use function Laravel\Prompts\alert;

info('Operation completed successfully.');
warning('This action is irreversible.');
error('Something went wrong.');
alert('Critical system alert!');
</code-snippet>

### Tables

<code-snippet name="Table Output" lang="php">
use function Laravel\Prompts\table;

table(
    headers: ['Name', 'Email', 'Role'],
    rows: User::all(['name', 'email', 'role'])->toArray(),
);
</code-snippet>

## Form Wizard

<code-snippet name="Form Wizard" lang="php">
use function Laravel\Prompts\form;

$responses = form()
    ->text('name', label: 'What is your name?', required: true)
    ->password('password', label: 'Create a password', required: true)
    ->confirm('newsletter', label: 'Subscribe to newsletter?')
    ->select('role', label: 'Select role', options: [
        'user' => 'User',
        'admin' => 'Admin',
    ])
    ->submit();

// Access: $responses['name'], $responses['password'], etc.
</code-snippet>

## In Artisan Commands

<code-snippet name="Artisan Command Example" lang="php">
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use function Laravel\Prompts\confirm;
use function Laravel\Prompts\select;
use function Laravel\Prompts\text;
use function Laravel\Prompts\info;

class CreateUserCommand extends Command
{
    protected $signature = 'user:create';
    protected $description = 'Create a new user interactively';

    public function handle(): int
    {
        $name = text('What is the user\'s name?', required: true);
        $email = text('What is their email?', required: true);
        $role = select('What role?', ['admin', 'editor', 'user']);

        if (confirm('Create this user?')) {
            User::create(compact('name', 'email', 'role'));
            info('User created successfully!');
            return self::SUCCESS;
        }

        return self::FAILURE;
    }
}
</code-snippet>

## Common Pitfalls

- Not importing prompt functions (`use function Laravel\Prompts\text`)
- Missing required validation for critical inputs
- Not providing hints for complex prompts
- Forgetting to handle cancellation (user pressing Ctrl+C)
- Using prompts in non-interactive environments (queues, cron)
