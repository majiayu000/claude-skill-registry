---
name: typo3-update
description: Comprehensive guide for writing TYPO3 code compatible with both v13 and v14, with preference for v14. Covers version constraints, compatible patterns, and migration strategies.
version: 2.0.0
typo3_compatibility: "13.0 - 14.x"
triggers:
  - update
  - upgrade
  - v13
  - v14
  - migration
  - lts
  - compatibility
---

# TYPO3 Dual-Version Development: v13 & v14

> **Strategy:** Write code that works on both TYPO3 v13 and v14, with v14 as the preferred target.
> All patterns in this skill are designed for dual-version compatibility.

## 1. Version Strategy

### Target: TYPO3 v13 and v14

| Version | Status | PHP | Support Until |
|---------|--------|-----|---------------|
| v12.4 LTS | Maintenance | 8.1-8.3 | April 2026 |
| **v13.4 LTS** | **Active LTS** | 8.2-8.4 | ~2028 |
| **v14.x** | **Latest** | 8.2-8.4 | ~2029 |

**Best Practice:** Target both v13 and v14 for maximum compatibility. New projects should prefer v14.

### Version Constraints

```php
<?php
// ext_emconf.php - Dual version support
$EM_CONF[$_EXTKEY] = [
    'title' => 'My Extension',
    'version' => '2.0.0',
    'state' => 'stable',
    'constraints' => [
        'depends' => [
            'typo3' => '13.0.0-14.99.99',
            'php' => '8.2.0-8.4.99',
        ],
        'conflicts' => [],
        'suggests' => [],
    ],
];
```

```json
// composer.json - Dual version support
{
    "name": "vendor/my-extension",
    "type": "typo3-cms-extension",
    "require": {
        "php": "^8.2",
        "typo3/cms-core": "^13.0 || ^14.0"
    },
    "extra": {
        "typo3/cms": {
            "extension-key": "my_extension"
        }
    }
}
```

## 2. PHP Requirements

### Minimum PHP Version: 8.2

Both v13 and v14 require PHP 8.2+. Use modern PHP features:

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Service;

// ✅ Constructor property promotion (PHP 8.0+)
final class MyService
{
    public function __construct(
        private readonly SomeDependency $dependency,
        private readonly AnotherService $anotherService,
    ) {}
}

// ✅ Named arguments (PHP 8.0+)
$result = $this->doSomething(
    name: 'value',
    options: ['key' => 'value'],
);

// ✅ Match expressions (PHP 8.0+)
$type = match ($input) {
    'a' => 'Type A',
    'b' => 'Type B',
    default => 'Unknown',
};

// ✅ Enums (PHP 8.1+)
enum Status: string
{
    case Draft = 'draft';
    case Published = 'published';
}
```

## 3. Controller Patterns (v13/v14 Compatible)

### Extbase Action Controller

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Controller;

use Psr\Http\Message\ResponseInterface;
use TYPO3\CMS\Extbase\Mvc\Controller\ActionController;
use Vendor\Extension\Domain\Repository\ItemRepository;

final class ItemController extends ActionController
{
    public function __construct(
        private readonly ItemRepository $itemRepository,
    ) {}

    // ✅ Must return ResponseInterface (required since v13)
    public function listAction(): ResponseInterface
    {
        $items = $this->itemRepository->findAll();
        $this->view->assign('items', $items);
        return $this->htmlResponse();
    }

    public function showAction(int $item): ResponseInterface
    {
        $item = $this->itemRepository->findByUid($item);
        $this->view->assign('item', $item);
        return $this->htmlResponse();
    }

    // ✅ JSON response
    public function apiAction(): ResponseInterface
    {
        $data = ['success' => true, 'items' => []];
        return $this->jsonResponse(json_encode($data));
    }

    // ✅ Redirect
    public function createAction(): ResponseInterface
    {
        // Process creation...
        $this->addFlashMessage('Item created');
        return $this->redirect('list');
    }
}
```

### Backend Module Controller

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Controller;

use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;
use TYPO3\CMS\Backend\Attribute\AsController;
use TYPO3\CMS\Backend\Template\ModuleTemplateFactory;

#[AsController]
final class BackendModuleController
{
    public function __construct(
        private readonly ModuleTemplateFactory $moduleTemplateFactory,
    ) {}

    public function indexAction(ServerRequestInterface $request): ResponseInterface
    {
        $moduleTemplate = $this->moduleTemplateFactory->create($request);
        $moduleTemplate->assign('items', []);
        
        return $moduleTemplate->renderResponse('Backend/Index');
    }
}
```

## 4. View & Templating (v13/v14 Compatible)

### ViewFactory (Preferred Pattern)

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Service;

use Psr\Http\Message\ServerRequestInterface;
use TYPO3\CMS\Core\View\ViewFactoryData;
use TYPO3\CMS\Core\View\ViewFactoryInterface;

final class RenderingService
{
    public function __construct(
        private readonly ViewFactoryInterface $viewFactory,
    ) {}

    public function renderEmail(ServerRequestInterface $request, array $data): string
    {
        $viewFactoryData = new ViewFactoryData(
            templateRootPaths: ['EXT:my_extension/Resources/Private/Templates/Email'],
            partialRootPaths: ['EXT:my_extension/Resources/Private/Partials'],
            layoutRootPaths: ['EXT:my_extension/Resources/Private/Layouts'],
            request: $request,
        );
        
        $view = $this->viewFactory->create($viewFactoryData);
        $view->assignMultiple($data);
        
        return $view->render('Notification');
    }
}
```

### Fluid Template Best Practices

```html
<html xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
      xmlns:core="http://typo3.org/ns/TYPO3/CMS/Core/ViewHelpers"
      data-namespace-typo3-fluid="true">

<f:layout name="Default" />

<f:section name="Main">
    <div class="content">
        <!-- ✅ Auto-escaped output -->
        <h1>{item.title}</h1>
        
        <!-- ✅ Explicit HTML (use with caution) -->
        <f:format.html>{item.bodytext}</f:format.html>
        
        <!-- ✅ Conditional rendering -->
        <f:if condition="{items}">
            <f:then>
                <f:for each="{items}" as="item">
                    <f:render partial="Item" arguments="{item: item}" />
                </f:for>
            </f:then>
            <f:else>
                <p>No items found.</p>
            </f:else>
        </f:if>
        
        <!-- ✅ Link building -->
        <f:link.action action="show" arguments="{item: item.uid}">
            View Details
        </f:link.action>
    </div>
</f:section>

</html>
```

## 5. Event System (v13/v14 Compatible)

### PSR-14 Event Listeners

PSR-14 events are the standard in both v13 and v14. Always prefer events over hooks.

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\EventListener;

use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Frontend\Event\ModifyCacheLifetimeForPageEvent;

#[AsEventListener(identifier: 'vendor-extension/modify-cache-lifetime')]
final class ModifyCacheLifetimeListener
{
    public function __invoke(ModifyCacheLifetimeForPageEvent $event): void
    {
        // Reduce cache lifetime for certain pages
        if ($event->getPageId() === 123) {
            $event->setCacheLifetime(300); // 5 minutes
        }
    }
}
```

### Common Events (v13/v14)

| Event | Purpose |
|-------|---------|
| `BeforeRecordOperationEvent` | Before DataHandler operations |
| `AfterRecordOperationEvent` | After DataHandler operations |
| `ModifyPageLinkConfigurationEvent` | Modify link building |
| `ModifyCacheLifetimeForPageEvent` | Adjust page cache |
| `BeforeStdWrapFunctionsInitializedEvent` | Modify stdWrap |

### Services.yaml Registration

```yaml
# Configuration/Services.yaml
services:
  _defaults:
    autowire: true
    autoconfigure: true
    public: false

  Vendor\Extension\:
    resource: '../Classes/*'
    exclude:
      - '../Classes/Domain/Model/*'

  # Event listener (alternative to #[AsEventListener] attribute)
  Vendor\Extension\EventListener\MyListener:
    tags:
      - name: event.listener
        identifier: 'vendor-extension/my-listener'
```

## 6. Backend Module Registration (v13/v14)

### Configuration/Backend/Modules.php

```php
<?php
// Configuration/Backend/Modules.php
return [
    'web_myextension' => [
        'parent' => 'web',
        'position' => ['after' => 'web_info'],
        'access' => 'user,group',
        'iconIdentifier' => 'myextension-module',
        'path' => '/module/web/myextension',
        'labels' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_mod.xlf',
        'extensionName' => 'MyExtension',
        'controllerActions' => [
            \Vendor\MyExtension\Controller\BackendController::class => [
                'index',
                'list',
                'show',
            ],
        ],
    ],
];
```

### Icon Registration

```php
<?php
// Configuration/Icons.php
return [
    'myextension-module' => [
        'provider' => \TYPO3\CMS\Core\Imaging\IconProvider\SvgIconProvider::class,
        'source' => 'EXT:my_extension/Resources/Public/Icons/module.svg',
    ],
];
```

## 7. TCA Configuration (v13/v14 Compatible)

### Static TCA Only

In v14, runtime TCA modifications are forbidden. Always use static files:

```php
<?php
// Configuration/TCA/tx_myext_domain_model_item.php
return [
    'ctrl' => [
        'title' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_db.xlf:tx_myext_domain_model_item',
        'label' => 'title',
        'tstamp' => 'tstamp',
        'crdate' => 'crdate',
        'delete' => 'deleted',
        'enablecolumns' => [
            'disabled' => 'hidden',
            'starttime' => 'starttime',
            'endtime' => 'endtime',
        ],
        'searchFields' => 'title,description',
        'iconIdentifier' => 'myextension-item',
    ],
    'types' => [
        '1' => [
            'showitem' => '
                --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:general,
                    title, description,
                --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:access,
                    hidden, starttime, endtime,
            ',
        ],
    ],
    'columns' => [
        'title' => [
            'label' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_db.xlf:tx_myext_domain_model_item.title',
            'config' => [
                'type' => 'input',
                'size' => 50,
                'max' => 255,
                'required' => true,
            ],
        ],
        'description' => [
            'label' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_db.xlf:tx_myext_domain_model_item.description',
            'config' => [
                'type' => 'text',
                'cols' => 40,
                'rows' => 5,
                'enableRichtext' => true,
            ],
        ],
    ],
];
```

### TCA Overrides

```php
<?php
// Configuration/TCA/Overrides/tt_content.php
defined('TYPO3') or die();

\TYPO3\CMS\Core\Utility\ExtensionManagementUtility::addTcaSelectItem(
    'tt_content',
    'CType',
    [
        'label' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang.xlf:ctype.title',
        'value' => 'myextension_element',
        'icon' => 'content-text',
        'group' => 'default',
    ]
);

$GLOBALS['TCA']['tt_content']['types']['myextension_element'] = [
    'showitem' => '
        --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:general,
            --palette--;;general,
            header,
            bodytext,
        --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:access,
            --palette--;;hidden,
    ',
];
```

## 8. Database Operations (v13/v14 Compatible)

### QueryBuilder

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Repository;

use TYPO3\CMS\Core\Database\Connection;
use TYPO3\CMS\Core\Database\ConnectionPool;
use TYPO3\CMS\Core\Database\Query\QueryBuilder;

final class CustomRepository
{
    public function __construct(
        private readonly ConnectionPool $connectionPool,
    ) {}

    public function findByStatus(string $status): array
    {
        $queryBuilder = $this->connectionPool->getQueryBuilderForTable('tx_myext_items');
        
        return $queryBuilder
            ->select('*')
            ->from('tx_myext_items')
            ->where(
                $queryBuilder->expr()->eq(
                    'status',
                    $queryBuilder->createNamedParameter($status)
                )
            )
            ->orderBy('title', 'ASC')
            ->executeQuery()
            ->fetchAllAssociative();
    }

    public function countByPid(int $pid): int
    {
        $queryBuilder = $this->connectionPool->getQueryBuilderForTable('tx_myext_items');
        
        return (int)$queryBuilder
            ->count('uid')
            ->from('tx_myext_items')
            ->where(
                $queryBuilder->expr()->eq(
                    'pid',
                    $queryBuilder->createNamedParameter($pid, Connection::PARAM_INT)
                )
            )
            ->executeQuery()
            ->fetchOne();
    }
}
```

### Extbase Repository

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Domain\Repository;

use TYPO3\CMS\Extbase\Persistence\QueryInterface;
use TYPO3\CMS\Extbase\Persistence\Repository;

final class ItemRepository extends Repository
{
    protected $defaultOrderings = [
        'sorting' => QueryInterface::ORDER_ASCENDING,
    ];

    public function findPublished(): array
    {
        $query = $this->createQuery();
        $query->matching(
            $query->logicalAnd(
                $query->equals('hidden', false),
                $query->lessThanOrEqual('starttime', time()),
                $query->logicalOr(
                    $query->equals('endtime', 0),
                    $query->greaterThan('endtime', time())
                )
            )
        );
        
        return $query->execute()->toArray();
    }
}
```

## 9. CLI Commands (v13/v14 Compatible)

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Command;

use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Console\Style\SymfonyStyle;
use TYPO3\CMS\Core\Core\Bootstrap;

#[AsCommand(
    name: 'myext:process',
    description: 'Process items in the extension',
)]
final class ProcessCommand extends Command
{
    protected function configure(): void
    {
        $this
            ->addArgument('type', InputArgument::REQUIRED, 'The type to process')
            ->addOption('force', 'f', InputOption::VALUE_NONE, 'Force processing');
    }

    protected function execute(InputInterface $input, OutputInterface $output): int
    {
        $io = new SymfonyStyle($input, $output);
        
        // Initialize backend for DataHandler operations
        Bootstrap::initializeBackendAuthentication();
        
        $type = $input->getArgument('type');
        $force = $input->getOption('force');
        
        $io->title('Processing: ' . $type);
        
        // Your logic here...
        
        $io->success('Processing completed successfully');
        
        return Command::SUCCESS;
    }
}
```

### Command Registration

```yaml
# Configuration/Services.yaml
services:
  Vendor\Extension\Command\ProcessCommand:
    tags:
      - name: console.command
```

## 10. Testing for Dual-Version Compatibility

### PHPUnit Setup

```xml
<!-- phpunit.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="vendor/typo3/testing-framework/Resources/Core/Build/UnitTestsBootstrap.php"
         colors="true">
    <testsuites>
        <testsuite name="Unit">
            <directory>Tests/Unit</directory>
        </testsuite>
        <testsuite name="Functional">
            <directory>Tests/Functional</directory>
        </testsuite>
    </testsuites>
</phpunit>
```

### Test Both Versions in CI

```yaml
# .github/workflows/ci.yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        typo3: ['^13.0', '^14.0']
        php: ['8.2', '8.3']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ matrix.php }}
          extensions: intl, pdo_mysql
      
      - name: Install dependencies
        run: |
          composer require typo3/cms-core:${{ matrix.typo3 }} --no-update
          composer install --prefer-dist --no-progress
      
      - name: Run tests
        run: vendor/bin/phpunit
```

## 11. Upgrade Process

### From v12 to v13/v14

```bash
# 1. Create backup
ddev snapshot --name=before-upgrade

# 2. Update composer constraints
ddev composer require "typo3/cms-core:^13.0 || ^14.0" --no-update
ddev composer update "typo3/*" --with-all-dependencies

# 3. Run upgrade wizards
ddev typo3 upgrade:list
ddev typo3 upgrade:run

# 4. Clear caches
ddev typo3 cache:flush

# 5. Update database schema
ddev typo3 database:updateschema

# 6. Test thoroughly
```

## 12. Resources

- **v13 Documentation**: https://docs.typo3.org/m/typo3/reference-coreapi/13.4/en-us/
- **v14 Documentation**: https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/
- **v13 Changelog**: https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog-13/Index.html
- **v14 Changelog**: https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog-14/Index.html
- **TYPO3 Rector**: https://github.com/sabbelasichon/typo3-rector

---

## Credits & Attribution

This skill is based on the excellent TYPO3 best practices and methodology developed by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**. We are deeply grateful for their
outstanding contributions to the TYPO3 community and their commitment to sharing knowledge.

Netresearch has been a leading force in TYPO3 development, and their expertise has been
invaluable in shaping these guidelines. Thank you, Netresearch, for your exceptional work!

**Copyright (c) Netresearch DTT GmbH** - Methodology and best practices  
Adapted by webconsulting.at for this skill collection
