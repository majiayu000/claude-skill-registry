---
name: commands
description: Artisan console command classes that serve as the CLI entry point for operations. Commands validate input and delegate all business logic to Actions or Services.
---

**Name:** Commands
**Description:** Artisan console command classes that serve as the CLI entry point for operations. Commands validate input and delegate all business logic to Actions or Services.
**Compatible Agents:** general-purpose, backend
**Tags:** app/Console/Commands/**/*.php, laravel, php, backend, artisan, cli, console

## Rules

- Command classes live in `app/Console/Commands/`
- Each command should have a single, clearly defined responsibility
- Complex logic belongs in **Actions** or **Services**, not in the command itself — commands are the entry point only
- Use descriptive verb-noun names: `SendInvoiceReminders`, `ImportProductCsv`, `PruneExpiredSessions`
- Command signatures follow the `namespace:action` pattern: `invoices:send-reminders`, `products:import`
- Every argument and option **must** have a clear description
- Validate all input using the `Validator` class — never trust raw input
- Use `--option` flags for optional behaviour; avoid positional ambiguity
- Implement `PromptsForMissingInput` so users receive clear prompts instead of silent failures
- Commands must **always** return either `self::SUCCESS` or `self::FAILURE` — never `void` or `null`

## Examples

```php
class SendInvoiceReminders extends Command implements PromptsForMissingInput
{
    protected $signature = 'invoices:send-reminders
                            {email : The email address to send the reminder to}
                            {--dry-run : Simulate the command without persisting changes}';

    protected $description = 'Send invoice payment reminders to a specific user.';

    public function __construct(private readonly SendInvoiceReminderAction $action)
    {
        parent::__construct();
    }

    public function handle(): int
    {
        $validated = validator(
            [
                'email'   => $this->argument('email'),
                'dry_run' => $this->option('dry-run'),
            ],
            [
                'email'   => ['required', 'email'],
                'dry_run' => ['boolean'],
            ]
        )->validate();

        try {
            $this->action->execute($validated['email']);
            $this->info("Reminder sent to {$validated['email']}.");

            return self::SUCCESS;
        } catch (Throwable $e) {
            $this->error("Failed: {$e->getMessage()}");

            return self::FAILURE;
        }
    }
}
```

## Anti-Patterns

- Putting business logic directly inside `handle()` instead of delegating to an Action or Service
- Not returning `self::SUCCESS` or `self::FAILURE` (e.g., returning `void` or `null`)
- Trusting raw `$this->argument()` / `$this->option()` values without validation
- Omitting descriptions from arguments and options in the signature
- Not implementing `PromptsForMissingInput`, causing silent failures for missing arguments

## References

- [Laravel Artisan Console](https://laravel.com/docs/artisan)
- Related: `Actions/SKILL.md` — for the business logic commands delegate to
