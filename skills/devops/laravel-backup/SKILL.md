---
name: laravel-backup
description: Configure, implement, and manage Laravel application backups using spatie/laravel-backup. Create automated backup schedules, configure file and database backups, set up backup storage (S3, local), manage cleanup policies, send notifications (mail, slack), monitor backup health, and handle advanced scenarios like encrypted backups and isolated mode. Use when setting up backup solutions, troubleshooting backup issues, configuring notifications, or monitoring backup health in Laravel projects.
---

# Laravel Backup Skill

Setup, configure, and manage automated backups for Laravel applications using the spatie/laravel-backup package. Handle file and database backups, storage destinations, cleanup policies, notifications, monitoring, and advanced features.

## Quick start

### 1. Install package
```bash
composer require spatie/laravel-backup
php artisan vendor:publish --provider="Spatie\Backup\BackupServiceProvider"
```

### 2. Publish and configure
```bash
# Publish configuration
php artisan vendor:publish --provider="Spatie\Backup\BackupServiceProvider"

# Publish translations
php artisan vendor:publish --provider="Spatie\Backup\BackupServiceProvider" --tag=translations
```

### 3. Run backup
```bash
php artisan backup:run
```

### 4. Clean old backups
```bash
php artisan backup:clean
```

### 5. Monitor backup health
```bash
php artisan backup:monitor
```

## Instructions

### 1. Installation & Setup

1. Install via Composer:
```bash
composer require spatie/laravel-backup
```

2. Publish configuration file to `config/backup.php`:
```bash
php artisan vendor:publish --provider="Spatie\Backup\BackupServiceProvider"
```

3. The config file contains all backup settings for files, databases, storage, notifications, and cleanup.

### 2. Configuring File Backups

In `config/backup.php`, configure the `include` and `exclude` arrays:

```php
'include' => [
    base_path('app'),
    base_path('config'),
    base_path('database'),
],

'exclude' => [
    base_path('vendor'),
    base_path('node_modules'),
    storage_path('logs'),
],
```

Options:
- `follow_links` - Follow symbolic links (true/false)
- `relative_path` - Include relative path in archive

### 3. Database Configuration

Configure database dumping in `config/backup.php`:

```php
'dump' => [
    'mysql' => [
        'dump_command_path' => '/usr/bin',
        'timeout' => 60,
        'dump_binary_path' => null,
    ],
    'pgsql' => [
        'dump_command_path' => '/usr/bin',
        'timeout' => 60,
    ],
],
```

For MySQL:
- Exclude specific tables with `exclude_tables`
- Add extra options with `extra_options`
- Bypass SSL errors with `use_ssl`

### 4. Storage Configuration

Specify destination filesystems in `config/backup.php`:

```php
'disks' => ['local', 's3', 'dropbox'],
```

Configure filesystem drivers in `config/filesystems.php`. Pass extra options via:

```php
'disks' => [
    's3' => [
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION'),
        'bucket' => env('AWS_BUCKET'),
    ],
],
```

### 5. Backup Archiving & Encryption

Configure temporary directory, password, and encryption:

```php
'temp_directory' => storage_path('temp'),
'password' => env('BACKUP_PASSWORD'),
'encryption' => env('BACKUP_ENCRYPTION', 'default'),
```

- Set `password` to null to disable encryption
- Set `encryption` to false to skip encryption entirely

### 6. Scheduling Backups

In `app/Console/Kernel.php`:

```php
protected function schedule(Schedule $schedule)
{
    $schedule->command('backup:run')->daily();
    $schedule->command('backup:clean')->daily()->at('01:00');
}
```

Or using console routes in Laravel 12:

```php
use Illuminate\Foundation\Inspiring;
use Illuminate\Support\Facades\Schedule;

Schedule::command('backup:run')->daily();
Schedule::command('backup:clean')->daily()->at('01:00');
```

### 7. Running Backups

Basic backup:
```bash
php artisan backup:run
```

Advanced options:
```bash
# Backup only to specific disk
php artisan backup:run --only-files

# Backup only database
php artisan backup:run --only-db

# Backup to specific disk
php artisan backup:run --disks=s3

# Isolated mode (single server execution)
php artisan backup:run --isolated
```

### 8. Cleanup Configuration

In `config/backup.php`, configure retention:

```php
'cleanup' => [
    'strategy' => \Spatie\Backup\Tasks\Cleanup\Strategies\DefaultStrategy::class,
    'default_strategy' => [
        'keep_all_backups_for_days' => 7,
        'keep_daily_backups_for_days' => 16,
        'keep_weekly_backups_for_weeks' => 8,
        'keep_monthly_backups_for_months' => 4,
        'keep_yearly_backups_for_year' => 7,
        'delete_oldest_backups_when_using_more_megabytes_than' => 5000,
    ],
],
```

### 9. Running Cleanup

```bash
php artisan backup:clean
```

The latest backup is always preserved.

### 10. Setting Up Notifications

Configure notification channels in `config/backup.php`:

```php
'notifications' => [
    'mail' => [
        'enabled' => true,
        'to' => 'admin@example.com',
    ],
    'slack' => [
        'enabled' => true,
        'webhook_url' => env('SLACK_WEBHOOK_URL'),
    ],
    'discord' => [
        'enabled' => true,
        'webhook_url' => env('DISCORD_WEBHOOK_URL'),
    ],
],
```

For Slack, install the notification channel:
```bash
composer require laravel/slack-notification-channel
```

### 11. Customizing Notifications

Create custom notifiable class:

```php
use Spatie\Backup\Notifications\Notifiable as BaseNotifiable;

class CustomBackupNotifiable extends BaseNotifiable
{
    // Custom notification logic
}
```

Register in `config/backup.php`:
```php
'notifiable' => \App\Notifications\CustomBackupNotifiable::class,
```

### 12. Monitoring Backup Health

Configure monitored backups in `config/backup.php`:

```php
'monitor_backups' => [
    [
        'name' => 'production',
        'disks' => ['s3'],
        'health_checks' => [
            \Spatie\Backup\Tasks\Monitor\HealthChecks\MaximumAgeInDays::class => 1,
            \Spatie\Backup\Tasks\Monitor\HealthChecks\MaximumStorageInMegabytes::class => 5000,
        ],
    ],
],
```

Schedule monitoring:
```bash
php artisan backup:monitor
```

### 13. Custom Health Checks

Extend the health check API:

```php
use Spatie\Backup\Tasks\Monitor\HealthCheck;

class CustomHealthCheck extends HealthCheck
{
    public function checkHealth(): void
    {
        // Your health check logic
    }
}
```

### 14. Backup Events

Listen to backup events:

```php
use Spatie\Backup\Events\BackupHasFailed;
use Spatie\Backup\Events\BackupWasSuccessful;
use Spatie\Backup\Events\BackupManifestWasCreated;

Event::listen(BackupWasSuccessful::class, function (BackupWasSuccessful $event) {
    // Handle successful backup
    // Access: $event->backupDestination
});
```

### 15. Isolated Mode

For distributed servers, ensure single execution:

```bash
# All three commands support --isolated flag
php artisan backup:run --isolated
php artisan backup:clean --isolated
php artisan backup:monitor --isolated
```

Uses atomic cache lock to prevent concurrent execution.

## Examples

### Complete Configuration Example

```php
// config/backup.php
return [
    'backup' => [
        'name' => env('APP_NAME', 'laravel-app'),
        'source' => [
            'files' => [
                'include' => [
                    base_path('app'),
                    base_path('config'),
                    base_path('database'),
                    base_path('resources'),
                ],
                'exclude' => [
                    base_path('vendor'),
                    base_path('node_modules'),
                ],
                'follow_links' => false,
            ],
            'databases' => [
                'mysql',
            ],
        ],
        'destination' => [
            'disks' => ['s3', 'local'],
        ],
        'temp_directory' => storage_path('temp'),
        'password' => env('BACKUP_PASSWORD'),
        'encryption' => 'default',
    ],
    'cleanup' => [
        'strategy' => \Spatie\Backup\Tasks\Cleanup\Strategies\DefaultStrategy::class,
        'default_strategy' => [
            'keep_all_backups_for_days' => 7,
            'keep_daily_backups_for_days' => 16,
            'keep_weekly_backups_for_weeks' => 8,
            'keep_monthly_backups_for_months' => 4,
            'delete_oldest_backups_when_using_more_megabytes_than' => 5000,
        ],
    ],
    'notifications' => [
        'mail' => [
            'enabled' => true,
            'to' => env('BACKUP_NOTIFICATION_EMAIL'),
        ],
    ],
    'monitor_backups' => [
        [
            'name' => 'production',
            'disks' => ['s3'],
            'health_checks' => [
                \Spatie\Backup\Tasks\Monitor\HealthChecks\MaximumAgeInDays::class => 1,
            ],
        ],
    ],
];
```

### Scheduling with Different Times

```php
// app/Console/Kernel.php
protected function schedule(Schedule $schedule)
{
    // Run backup at 2 AM daily
    $schedule->command('backup:run')->dailyAt('02:00');
    
    // Clean at 3 AM daily
    $schedule->command('backup:clean')->dailyAt('03:00');
    
    // Monitor at 4 AM daily
    $schedule->command('backup:monitor')->dailyAt('04:00');
    
    // Multiple backups per week
    $schedule->command('backup:run --disks=s3')->mondays()->at('02:00');
    $schedule->command('backup:run --disks=local')->saturdays()->at('02:00');
}
```

### Listening to Backup Events

```php
// app/Providers/EventServiceProvider.php
use Spatie\Backup\Events\BackupWasSuccessful;
use Spatie\Backup\Events\BackupHasFailed;
use Spatie\Backup\Events\UnHealthyBackupWasFound;

protected $listen = [
    BackupWasSuccessful::class => [
        'App\Listeners\NotifyBackupSuccess',
    ],
    BackupHasFailed::class => [
        'App\Listeners\NotifyBackupFailure',
    ],
    UnHealthyBackupWasFound::class => [
        'App\Listeners\NotifyUnhealthyBackup',
    ],
];
```

## Best practices

1. **Test restores regularly** - Verify backups can be restored
2. **Use multiple disks** - Never rely on single storage
3. **Encrypt sensitive data** - Always set backup password in production
4. **Monitor actively** - Set up health checks and notifications
5. **Schedule appropriately** - Consider database size and available resources
6. **Exclude large files** - Don't back up vendor or node_modules
7. **Use isolated mode** - Essential for distributed systems
8. **Handle failures gracefully** - Listen to failure events and notify
9. **Verify disk space** - Monitor storage to prevent failed backups
10. **Document retention policy** - Align with compliance requirements

## Requirements

- Laravel 8.0+
- PHP 8.0+
- Database: MySQL 5.7+, PostgreSQL 9.6+, or similar
- For Slack notifications: `laravel/slack-notification-channel`

## Advanced usage

For complex scenarios and detailed API reference, see:
- [reference.md](reference.md) - Complete API and advanced configuration
- [examples.md](examples.md) - Real-world implementation examples
