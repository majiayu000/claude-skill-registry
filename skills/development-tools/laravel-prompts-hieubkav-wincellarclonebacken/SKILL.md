---
name: laravel-prompts
description: Laravel Prompts - Beautiful and user-friendly forms for command-line applications with browser-like features including placeholder text and validation
---
## When to Use This Skill

This skill should be triggered when:
- Building Laravel Artisan commands with interactive prompts
- Creating user-friendly CLI applications in PHP
- Implementing form validation in command-line tools
- Adding text input, select menus, or confirmation dialogs to console commands
- Working with progress bars, loading spinners, or tables in CLI applications
- Testing Laravel console commands with prompts
- Converting simple console input to modern, validated, interactive prompts

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **other.md** - Complete Laravel Prompts documentation including:
  - All prompt types (text, password, select, search, etc.)
  - Validation strategies and examples
  - Form API for multi-step input
  - Progress bars and loading indicators
  - Informational messages (info, warning, error, alert)
  - Tables for displaying data
  - Testing strategies for console commands
  - Fallback configuration for unsupported environments

Use `view` to read the reference file when detailed information is needed.

## Testing

Test commands with prompts using Laravel's built-in assertions:

```php
use function Pest\Laravel\artisan;

test('user creation command', function () {
    artisan('users:create')
        ->expectsQuestion('What is your name?', 'Taylor Otwell')
        ->expectsQuestion('What is your email?', '[email protected]')
        ->expectsConfirmation('Create this user?', 'yes')
        ->expectsPromptsInfo('User created successfully!')
        ->assertExitCode(0);
});

test('displays warnings and errors', function () {
    artisan('report:generate')
        ->expectsPromptsWarning('This action cannot be undone')
        ->expectsPromptsError('Something went wrong')
        ->expectsPromptsTable(
            headers: ['Name', 'Email'],
            rows: [
                ['Taylor Otwell', '[email protected]'],
                ['Jason Beggs', '[email protected]'],
            ]
        )
        ->assertExitCode(0);
});
```

## Best Practices

### Design Guidelines
- Keep labels concise (under 74 characters for 80-column terminals)
- Use `hint` parameter for additional context
- Set appropriate `default` values when sensible
- Configure `scroll` for lists with many options (default: 5)

### Validation Strategy
- Use `required: true` for mandatory fields
- Apply Laravel validation rules for standard checks (email, min/max, etc.)
- Use closures for complex business logic validation
- Provide clear, actionable error messages

### User Experience
- Add placeholders to show expected input format
- Use `pause()` before destructive operations
- Show progress bars for operations taking >2 seconds
- Display informational messages after actions complete
- Group related prompts in forms for better flow

### Performance
- Use `search()` callbacks with length checks to avoid expensive queries:
  ```php
  options: fn (string $value) => strlen($value) > 0
      ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
      : []
  ```
- Limit database results with pagination or top-N queries
- Cache frequently-accessed option lists
- Use `spin()` for HTTP requests and long operations

## Common Patterns

### User Registration Flow
```php
$responses = form()
    ->text('Name', required: true, name: 'name')
    ->text('Email', validate: ['email' => 'required|email|unique:users'], name: 'email')
    ->password('Password', validate: ['password' => 'required|min:8'], name: 'password')
    ->submit();
```

### Confirmation Before Destructive Action
```php
$confirmed = confirm(
    label: 'Are you sure you want to delete all users?',
    default: false,
    hint: 'This action cannot be undone.'
);

if (! $confirmed) {
    $this->info('Operation cancelled.');
    return;
}
```

### Dynamic Multi-step Form
```php
$responses = form()
    ->select('User type', options: ['Regular', 'Admin'], name: 'type')
    ->add(function ($responses) {
        if ($responses['type'] === 'Admin') {
            return password('Admin password', required: true);
        }
    }, name: 'admin_password')
    ->submit();
```

### Batch Processing with Progress
```php
$items = Item::all();

$results = progress(
    label: 'Processing items',
    steps: $items,
    callback: function ($item, $progress) {
        $progress->hint("Processing: {$item->name}");
        return $this->process($item);
    }
);
```

## Resources

### Official Documentation
- Laravel Prompts Documentation: https://laravel.com/docs/12.x/prompts
- Laravel Console Testing: https://laravel.com/docs/12.x/console-tests

### Platform Support
- **Supported**: macOS, Linux, Windows with WSL
- **Fallback**: Configure fallback behavior for unsupported environments

## Notes

- Laravel Prompts is pre-installed in Laravel framework
- Supports Laravel validation rules for easy integration
- Uses terminal control codes for interactive UI
- All prompts return values that can be used immediately
- Forms support revisiting previous prompts with CTRL + U
- Validation runs on every input change for immediate feedback
- Progress bars can be manually controlled or automated

## Updating

This skill was generated from the official Laravel Prompts documentation. To refresh with updated information, re-scrape the Laravel documentation site.


---

## References

**Quick Reference:** `read .claude/skills/laravel-prompts/references/quick-reference.md`
**Key Concepts:** `read .claude/skills/laravel-prompts/references/key-concepts.md`
**Working with This Skill:** `read .claude/skills/laravel-prompts/references/working-with-this-skill.md`
