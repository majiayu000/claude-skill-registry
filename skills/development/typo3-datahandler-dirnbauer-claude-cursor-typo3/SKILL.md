---
name: typo3-datahandler
description: Expert guidance on manipulating TYPO3 records via the DataHandler, ensuring transactional safety, PSR-14 event handling, and reference index integrity.
version: 2.0.0
typo3_compatibility: "13.0 - 14.x"
triggers:
  - database
  - datahandler
  - tcemain
  - records
  - content
  - pages
---

# TYPO3 DataHandler Operations

> **Compatibility:** TYPO3 v13.x and v14.x (v14 preferred)
> All code examples in this skill are designed to work on both TYPO3 v13 and v14.

## 1. The Prime Directive

**NEVER** use raw SQL (`INSERT`, `UPDATE`, `DELETE`) for `pages`, `tt_content`, or any TCA-configured table.

You **MUST** use the `DataHandler` to ensure:

- Reference Index updates (`sys_refindex`)
- Cache clearing
- Version history (`sys_history`)
- Workspace compatibility
- PSR-14 event dispatching
- FlexForm handling
- MM relation management

### Exceptions (Raw SQL Allowed)

- Custom logging tables without TCA
- Bulk analytics/reporting queries (read-only)
- Migration scripts with explicit reference index rebuild

## 2. Structure of Arrays

### The DataMap ($data)

Used for **creating** or **updating** records.

**Syntax:** `$data[tableName][uid][fieldName] = value`

**Creating a New Record:**

Use a unique string starting with `NEW` as the UID:

```php
<?php
declare(strict_types=1);

$data = [
    'tt_content' => [
        'NEW_1' => [
            'pid' => 1,
            'CType' => 'text',
            'header' => 'My New Content Element',
            'bodytext' => '<p>Content goes here</p>',
            'sys_language_uid' => 0,
        ],
    ],
];
```

**Updating an Existing Record:**

Use the numeric UID:

```php
<?php
declare(strict_types=1);

$data = [
    'tt_content' => [
        123 => [
            'header' => 'Updated Header',
            'hidden' => 0,
        ],
    ],
];
```

**Referencing NEW Records:**

```php
<?php
declare(strict_types=1);

$data = [
    'pages' => [
        'NEW_page' => [
            'pid' => 1,
            'title' => 'New Page',
        ],
    ],
    'tt_content' => [
        'NEW_content' => [
            'pid' => 'NEW_page', // References the new page
            'CType' => 'text',
            'header' => 'Content on new page',
        ],
    ],
];
```

### The CmdMap ($cmd)

Used for **moving**, **copying**, **deleting**, or **undeleting** records.

**Syntax:** `$cmd[tableName][uid][command] = value`

**Delete a Record:**

```php
<?php
declare(strict_types=1);

$cmd = [
    'tt_content' => [
        123 => ['delete' => 1],
    ],
];
```

**Move a Record:**

```php
<?php
declare(strict_types=1);

$cmd = [
    'tt_content' => [
        123 => ['move' => 456], // Target page UID; use negative UID to place after record
    ],
];
```

**Copy a Record:**

```php
<?php
declare(strict_types=1);

$cmd = [
    'tt_content' => [
        123 => ['copy' => 1], // Target page UID
    ],
];
```

**Localize a Record:**

```php
<?php
declare(strict_types=1);

$cmd = [
    'tt_content' => [
        123 => [
            'localize' => 1, // Target language UID
        ],
    ],
];
```

## 3. Transactional Execution Pattern (Mandatory)

DataHandler already wraps its own database writes in transactions. Only wrap the call yourself when you have to bundle multiple DataHandler runs or adjacent custom writes on the **same** connection. Do not mix different connections inside one transaction.

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Service;

use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\Utility\GeneralUtility;

final class ContentService
{
    public function __construct(
        private readonly ConnectionPool $connectionPool,
    ) {}

    public function createContentWithTransaction(array $data, array $cmd = []): array
    {
        $dataHandler = GeneralUtility::makeInstance(DataHandler::class);
        
        // 1. Prepare
        $dataHandler->start($data, $cmd);

        // 2. Get Connection & Start Transaction
        $connection = $this->connectionPool->getConnectionForTable('tt_content');
        $connection->beginTransaction();

        try {
            // 3. Process DataMap
            if (!empty($data)) {
                $dataHandler->process_datamap();
            }

            // 4. Process CmdMap
            if (!empty($cmd)) {
                $dataHandler->process_cmdmap();
            }

            // 5. Validate
            if (!empty($dataHandler->errorLog)) {
                throw new \RuntimeException(
                    'DataHandler Error: ' . implode(', ', $dataHandler->errorLog),
                    1700000001
                );
            }

            // 6. Commit
            $connection->commit();

            // 7. Return substituted UIDs for NEW records
            return $dataHandler->substNEWwithIDs;

        } catch (\Throwable $e) {
            // 8. Rollback on Failure
            $connection->rollBack();
            
            // Log and re-throw
            throw $e;
        }
    }
}
```

## 4. Admin Context

When running from CLI (Symfony Command) or scheduler tasks, you **MUST** ensure the backend user has admin privileges:

```php
<?php
declare(strict_types=1);

// Set admin context for DataHandler operations
$GLOBALS['BE_USER']->user['admin'] = 1;
$GLOBALS['BE_USER']->workspace = 0; // Live workspace

// Alternative: Use the BackendUserAuthentication properly
$backendUser = $GLOBALS['BE_USER'];
$backendUser->setWorkspace(0);
```

### CLI Command Setup (v13/v14 Compatible)

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Command;

use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use TYPO3\CMS\Core\Core\Bootstrap;

#[AsCommand(
    name: 'myext:import',
    description: 'Import data using DataHandler',
)]
final class ImportCommand extends Command
{
    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        // Initialize backend for DataHandler operations
        Bootstrap::initializeBackendAuthentication();
        
        // Your DataHandler logic here...
        
        return Command::SUCCESS;
    }
}
```

## 5. Reference Index Handling

After bulk operations, always update the reference index:

```php
<?php
declare(strict_types=1);

use TYPO3\CMS\Core\Database\ReferenceIndex;
use TYPO3\CMS\Core\Utility\GeneralUtility;

$referenceIndex = GeneralUtility::makeInstance(ReferenceIndex::class);

// Update for a specific record
$referenceIndex->updateRefIndexTable('tt_content', 123);

// Or update all (for migrations)
// Run via CLI: vendor/bin/typo3 referenceindex:update
```

## 6. Common Pitfalls

### Pitfall 1: Missing PID for New Records

```php
// ❌ WRONG - Missing pid
$data = ['tt_content' => ['NEW_1' => ['header' => 'Test']]];

// ✅ CORRECT - Always include pid
$data = ['tt_content' => ['NEW_1' => ['pid' => 1, 'header' => 'Test']]];
```

### Pitfall 2: Using String UIDs for Existing Records

```php
// ❌ WRONG - String UID for existing record
$data = ['tt_content' => ['123' => ['header' => 'Test']]];

// ✅ CORRECT - Integer UID for existing record
$data = ['tt_content' => [123 => ['header' => 'Test']]];
```

### Pitfall 3: Forgetting process_datamap() / process_cmdmap()

```php
// ❌ WRONG - Nothing happens
$dataHandler->start($data, $cmd);

// ✅ CORRECT - Actually process the data
$dataHandler->start($data, $cmd);
$dataHandler->process_datamap();
$dataHandler->process_cmdmap();
```

### Pitfall 4: Ignoring Error Log

```php
// ❌ WRONG - Silently ignoring errors
$dataHandler->process_datamap();

// ✅ CORRECT - Check for errors
$dataHandler->process_datamap();
if (!empty($dataHandler->errorLog)) {
    // Handle errors appropriately
    throw new \RuntimeException(implode(', ', $dataHandler->errorLog));
}
```

## 7. Retrieving New Record UIDs

After processing, get the real UIDs for NEW records:

```php
<?php
declare(strict_types=1);

$dataHandler->process_datamap();

// Get the real UID for 'NEW_1'
$newContentUid = $dataHandler->substNEWwithIDs['NEW_1'] ?? null;

if ($newContentUid === null) {
    throw new \RuntimeException('Failed to create content element');
}
```

## 8. Workspace-Aware Operations

When working with workspaces:

```php
<?php
declare(strict_types=1);

// Check if we're in a workspace
$workspaceId = $GLOBALS['BE_USER']->workspace;

if ($workspaceId > 0) {
    // In workspace - DataHandler will create versioned records
    // Use the wsol (workspace overlay) for reading
}

// Force live workspace for specific operations
$previousWorkspace = $GLOBALS['BE_USER']->workspace;
$GLOBALS['BE_USER']->setWorkspace(0);

// ... perform operations ...

$GLOBALS['BE_USER']->setWorkspace($previousWorkspace);
```

## 9. PSR-14 Events (Preferred Pattern)

> **Important:** PSR-14 events are the preferred way to react to DataHandler operations in TYPO3 v13/v14. Legacy hooks still work in v13 but should be migrated to events.

### Available DataHandler Events

| Event | Triggered When |
|-------|----------------|
| `BeforeRecordOperationEvent` | Before any record operation |
| `AfterRecordOperationEvent` | After any record operation |
| `AfterDatabaseOperationsEvent` | After database operations complete |
| `ModifyRecordBeforeInsertEvent` | Before a new record is inserted |

### Event Listener Registration (Services.yaml)

```yaml
# Configuration/Services.yaml
services:
  Vendor\Extension\EventListener\ContentCreatedListener:
    tags:
      - name: event.listener
        identifier: 'vendor-extension/content-created'
```

### Event Listener Implementation (v13/v14 Compatible)

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\EventListener;

use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\DataHandling\Event\AfterDatabaseOperationsEvent;

#[AsEventListener(identifier: 'vendor-extension/content-created')]
final class ContentCreatedListener
{
    public function __invoke(AfterDatabaseOperationsEvent $event): void
    {
        $table = $event->getTable();
        $status = $event->getStatus();
        $recordUid = $event->getRecordUid();
        $fields = $event->getFields();
        $dataHandler = $event->getDataHandler();

        if ($table !== 'tt_content') {
            return;
        }

        if ($status === 'new') {
            // Handle new record creation
            $newUid = $dataHandler->substNEWwithIDs[$recordUid] ?? $recordUid;
            // Your logic here...
        }

        if ($status === 'update') {
            // Handle record update
        }
    }
}
```

### Modifying Records Before Insert

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\EventListener;

use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Core\DataHandling\Event\ModifyRecordBeforeInsertEvent;

#[AsEventListener(identifier: 'vendor-extension/modify-before-insert')]
final class ModifyBeforeInsertListener
{
    public function __invoke(ModifyRecordBeforeInsertEvent $event): void
    {
        if ($event->getTable() !== 'tx_myext_domain_model_item') {
            return;
        }

        $record = $event->getRecord();
        
        // Modify the record before it's inserted
        $record['crdate'] = time();
        $record['tstamp'] = time();
        
        $event->setRecord($record);
    }
}
```

## 10. Legacy Hooks (Deprecated, v13 Only)

> **Warning:** Legacy hooks are deprecated in TYPO3 v14. Use PSR-14 events instead. The following is for reference when maintaining legacy code.

Register hooks in `ext_localconf.php`:

```php
<?php
declare(strict_types=1);

// ⚠️ DEPRECATED - Use PSR-14 events for new code
$GLOBALS['TYPO3_CONF_VARS']['SC_OPTIONS']['t3lib/class.t3lib_tcemain.php']['processDatamapClass'][]
    = \Vendor\Extension\Hooks\DataHandlerHook::class;

$GLOBALS['TYPO3_CONF_VARS']['SC_OPTIONS']['t3lib/class.t3lib_tcemain.php']['processCmdmapClass'][]
    = \Vendor\Extension\Hooks\DataHandlerHook::class;
```

Hook implementation:

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Hooks;

use TYPO3\CMS\Core\DataHandling\DataHandler;

/**
 * @deprecated Use PSR-14 events instead. This hook works in v13 but should be migrated.
 */
final class DataHandlerHook
{
    public function processDatamap_afterDatabaseOperations(
        string $status,
        string $table,
        string|int $id,
        array $fieldArray,
        DataHandler $dataHandler
    ): void {
        if ($table !== 'tt_content') {
            return;
        }

        if ($status === 'new') {
            // Handle new record creation
            $newUid = $dataHandler->substNEWwithIDs[$id] ?? $id;
        }

        if ($status === 'update') {
            // Handle record update
        }
    }
}
```

## 11. Version Constraints for Extensions

When creating extensions that use DataHandler, ensure proper version constraints:

```php
<?php
// ext_emconf.php
$EM_CONF[$_EXTKEY] = [
    'title' => 'My Extension',
    'version' => '1.0.0',
    'state' => 'stable',
    'constraints' => [
        'depends' => [
            'typo3' => '13.0.0-14.99.99',
            'php' => '8.2.0-8.4.99',
        ],
    ],
];
```

---

## Credits & Attribution

This skill is based on the excellent TYPO3 best practices and methodology developed by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**. We are deeply grateful for their
outstanding contributions to the TYPO3 community and their commitment to sharing knowledge.

Netresearch has been a leading force in TYPO3 development, and their expertise has been
invaluable in shaping these guidelines. Thank you, Netresearch, for your exceptional work!

**Copyright (c) Netresearch DTT GmbH** - Methodology and best practices  
Adapted by webconsulting.at for this skill collection
