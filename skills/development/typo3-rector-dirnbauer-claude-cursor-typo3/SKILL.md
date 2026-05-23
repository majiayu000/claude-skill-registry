---
name: typo3-rector
description: TYPO3 upgrade patterns using Rector, including automated refactoring rules and dual-version compatibility strategies for v13/v14.
version: 2.0.0
typo3_compatibility: "13.0 - 14.x"
triggers:
  - rector
  - upgrade
  - migration
  - refactoring
  - deprecation
---

# TYPO3 Rector Upgrade Patterns

> **Compatibility:** TYPO3 v13.x and v14.x (v14 preferred)
> This skill covers patterns for writing code that works on both v13 and v14.

## 1. Introduction to TYPO3 Rector

Rector is an automated refactoring tool that helps migrate TYPO3 extensions between major versions. It applies predefined rules to update deprecated code patterns.

### Installation

```bash
ddev composer require --dev ssch/typo3-rector
```

### Basic Configuration for Dual-Version Support

Create `rector.php` in your project root:

```php
<?php
declare(strict_types=1);

use Rector\Config\RectorConfig;
use Rector\Set\ValueObject\LevelSetList;
use Rector\ValueObject\PhpVersion;
use Ssch\TYPO3Rector\Set\Typo3LevelSetList;

return RectorConfig::configure()
    ->withPaths([
        __DIR__ . '/packages',
        __DIR__ . '/public/typo3conf/ext',
    ])
    ->withSkip([
        __DIR__ . '/public/typo3conf/ext/*/Resources/',
        __DIR__ . '/public/typo3conf/ext/*/Tests/',
    ])
    ->withPhpVersion(PhpVersion::PHP_82)
    ->withSets([
        // PHP upgrades
        LevelSetList::UP_TO_PHP_82,
        
        // TYPO3 v13 minimum (works on v14 too)
        Typo3LevelSetList::UP_TO_TYPO3_13,
    ])
    ->withImportNames();
```

## 2. Running Rector

### Dry Run (Preview Changes)

```bash
# Show what would be changed
ddev exec vendor/bin/rector process --dry-run

# For specific extension
ddev exec vendor/bin/rector process packages/my_extension --dry-run
```

### Apply Changes

```bash
# Apply all changes
ddev exec vendor/bin/rector process

# Apply to specific path
ddev exec vendor/bin/rector process packages/my_extension
```

### Clear Cache After

```bash
ddev typo3 cache:flush
ddev composer dump-autoload
```

## 3. Dual-Version Compatible Patterns

### Version Constraints

For extensions that must work on both v13 and v14:

```php
<?php
// ext_emconf.php
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
// composer.json
{
    "require": {
        "php": "^8.2",
        "typo3/cms-core": "^13.0 || ^14.0"
    }
}
```

### Rector Configuration for v13/v14 Dual Support

```php
<?php
declare(strict_types=1);

use Rector\Config\RectorConfig;
use Ssch\TYPO3Rector\Set\Typo3LevelSetList;
use Ssch\TYPO3Rector\Set\Typo3SetList;

return RectorConfig::configure()
    ->withPaths([__DIR__ . '/packages'])
    ->withSets([
        // Target v13 minimum - these patterns also work on v14
        Typo3LevelSetList::UP_TO_TYPO3_13,
        Typo3SetList::TYPO3_13,
    ]);
```

## 4. Key Migration Patterns (v13/v14 Compatible)

### Fluid ViewFactory (Replaces StandaloneView)

The ViewFactory approach works on both v13 and v14:

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

    public function render(ServerRequestInterface $request): string
    {
        $viewFactoryData = new ViewFactoryData(
            templateRootPaths: ['EXT:my_extension/Resources/Private/Templates'],
            partialRootPaths: ['EXT:my_extension/Resources/Private/Partials'],
            layoutRootPaths: ['EXT:my_extension/Resources/Private/Layouts'],
            request: $request,
        );
        
        $view = $this->viewFactory->create($viewFactoryData);
        $view->assign('data', ['key' => 'value']);
        $view->assignMultiple([
            'items' => [],
            'settings' => [],
        ]);
        
        return $view->render('MyTemplate');
    }
}
```

### ExtBase Controller Response (Required in v13+)

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\Controller;

use Psr\Http\Message\ResponseInterface;
use TYPO3\CMS\Extbase\Mvc\Controller\ActionController;

final class ItemController extends ActionController
{
    // ✅ Correct: Return ResponseInterface (required v13+)
    public function listAction(): ResponseInterface
    {
        $items = $this->itemRepository->findAll();
        $this->view->assign('items', $items);
        return $this->htmlResponse();
    }

    // ✅ Correct: JSON response
    public function apiAction(): ResponseInterface
    {
        $data = ['success' => true];
        return $this->jsonResponse(json_encode($data));
    }

    // ✅ Correct: Redirect
    public function createAction(Item $item): ResponseInterface
    {
        $this->itemRepository->add($item);
        return $this->redirect('list');
    }
}
```

### PSR-14 Events (Preferred over Hooks)

PSR-14 events work on both v13 and v14. Use them instead of legacy hooks:

```php
<?php
declare(strict_types=1);

namespace Vendor\Extension\EventListener;

use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Frontend\Event\ModifyPageLinkConfigurationEvent;

#[AsEventListener(identifier: 'vendor-extension/modify-pagelink')]
final class ModifyPageLinkListener
{
    public function __invoke(ModifyPageLinkConfigurationEvent $event): void
    {
        $configuration = $event->getConfiguration();
        // Modify link configuration
        $event->setConfiguration($configuration);
    }
}
```

### Backend Module Registration (v13/v14)

```php
<?php
// Configuration/Backend/Modules.php
return [
    'web_myextension_mymodule' => [
        'parent' => 'web',
        'position' => ['after' => 'web_info'],
        'access' => 'user,group',
        'iconIdentifier' => 'myextension-module',
        'path' => '/module/web/myextension',
        'labels' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang_mod.xlf',
        'extensionName' => 'MyExtension',
        'controllerActions' => [
            \Vendor\MyExtension\Controller\ModuleController::class => [
                'index',
                'edit',
            ],
        ],
    ],
];
```

### Service Configuration (Services.yaml)

```yaml
# Configuration/Services.yaml
services:
  _defaults:
    autowire: true
    autoconfigure: true
    public: false

  Vendor\MyExtension\:
    resource: '../Classes/*'
    exclude:
      - '../Classes/Domain/Model/*'
```

## 5. TCA Best Practices (v13/v14)

### Static TCA Only

In v14, `$GLOBALS['TCA']` becomes read-only after loading. Always use static TCA files:

```php
<?php
// Configuration/TCA/Overrides/tt_content.php
defined('TYPO3') or die();

// ✅ Correct: Static TCA configuration
\TYPO3\CMS\Core\Utility\ExtensionManagementUtility::addTcaSelectItem(
    'tt_content',
    'CType',
    [
        'label' => 'LLL:EXT:my_extension/Resources/Private/Language/locallang.xlf:mytype.title',
        'value' => 'myextension_mytype',
        'icon' => 'content-text',
        'group' => 'default',
    ]
);

$GLOBALS['TCA']['tt_content']['types']['myextension_mytype'] = [
    'showitem' => '
        --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:general,
            --palette--;;general,
            header;LLL:EXT:frontend/Resources/Private/Language/locallang_ttc.xlf:header_formlabel,
            bodytext,
        --div--;LLL:EXT:core/Resources/Private/Language/Form/locallang_tabs.xlf:access,
            --palette--;;hidden,
            --palette--;;access,
    ',
    'columnsOverrides' => [
        'bodytext' => [
            'config' => [
                'enableRichtext' => true,
            ],
        ],
    ],
];
```

## 6. Version Compatibility Table

| Feature | TYPO3 v13 | TYPO3 v14 | Notes |
|---------|-----------|-----------|-------|
| PHP 8.2 | Required | Required | Minimum for both |
| PHP 8.3 | Supported | Supported | Recommended |
| PHP 8.4 | Supported | Supported | Available |
| Symfony 7 | 7.1 | 7.2 | Minor differences |
| PSR-14 Events | Full | Full | Preferred pattern |
| Legacy Hooks | Working | Deprecated | Migrate to events |
| ViewFactory | Available | Available | Use this approach |
| StandaloneView | Deprecated | Removed | Migrate now |
| Content Blocks | Available | Enhanced | New features in v14 |
| TCA Runtime Changes | Deprecated | Forbidden | Use static TCA only |

## 7. Step-by-Step Migration Process

### 1. Prepare

```bash
# Create backup
ddev snapshot --name=before-migration

# Ensure tests pass
ddev exec vendor/bin/phpunit -c packages/my_extension/Tests/phpunit.xml

# Check deprecation log
tail -f var/log/typo3_deprecations_*.log
```

### 2. Configure Rector for Dual-Version

```php
<?php
declare(strict_types=1);

use Rector\Config\RectorConfig;
use Ssch\TYPO3Rector\Set\Typo3LevelSetList;

return RectorConfig::configure()
    ->withPaths([__DIR__ . '/packages/my_extension/Classes'])
    ->withSets([
        Typo3LevelSetList::UP_TO_TYPO3_13,
    ]);
```

### 3. Run Rector

```bash
# Dry run first
ddev exec vendor/bin/rector process --dry-run

# Apply changes
ddev exec vendor/bin/rector process

# Review changes
git diff
```

### 4. Manual Fixes

- Review Rector output for skipped files
- Check deprecation log for remaining issues
- Update TCA configurations manually
- Test all backend modules

### 5. Test on Both Versions

```bash
# Test on v13
ddev composer require "typo3/cms-core:^13.0" --no-update
ddev composer update
ddev typo3 cache:flush

# Run tests
ddev exec vendor/bin/phpunit

# Test on v14
ddev composer require "typo3/cms-core:^14.0" --no-update
ddev composer update
ddev typo3 cache:flush

# Run tests again
ddev exec vendor/bin/phpunit
```

### 6. Commit

```bash
git add -A
git commit -m "feat: Add TYPO3 v13/v14 dual-version support"
```

## 8. Troubleshooting

### Rector Fails

```bash
# Clear Rector cache
rm -rf .rector_cache/

# Run with verbose output
ddev exec vendor/bin/rector process --dry-run -vvv
```

### Extension Incompatibility

Check for updates:

```bash
ddev composer outdated
ddev composer show -l
```

Search for v13/v14-compatible alternatives on:
- https://extensions.typo3.org
- https://packagist.org

### Database Issues

```bash
# Check schema differences
ddev typo3 database:updateschema --verbose

# Safe schema update (add only)
ddev typo3 database:updateschema "*.add,*.change"

# Full update (includes destructive)
ddev typo3 database:updateschema "*"
```

## 9. Common Rector Rules

### Namespace Changes (Auto-Migrated)

Rector automatically handles namespace changes between versions.

### Utility Method Changes

```php
<?php
// ❌ Old (deprecated)
GeneralUtility::getIndpEnv('TYPO3_REQUEST_HOST');

// ✅ New (v13/v14 compatible)
$request = $GLOBALS['TYPO3_REQUEST'];
$normalizedParams = $request->getAttribute('normalizedParams');
$host = $normalizedParams->getRequestHost();
```

### ObjectManager Removal

```php
<?php
// ❌ Old (removed in v13+)
$objectManager = GeneralUtility::makeInstance(ObjectManager::class);
$service = $objectManager->get(MyService::class);

// ✅ New (Dependency Injection)
public function __construct(
    private readonly MyService $myService,
) {}
```

## 10. Resources

- **TYPO3 Rector**: https://github.com/sabbelasichon/typo3-rector
- **Upgrade Guide**: https://docs.typo3.org/m/typo3/reference-coreapi/main/en-us/ApiOverview/Upgrading/Index.html
- **v13 Changelog**: https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog-13/Index.html
- **v14 Changelog**: https://docs.typo3.org/c/typo3/cms-core/main/en-us/Changelog-14/Index.html

---

## Credits & Attribution

This skill is based on the excellent TYPO3 best practices and methodology developed by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**. We are deeply grateful for their
outstanding contributions to the TYPO3 community and their commitment to sharing knowledge.

Netresearch has been a leading force in TYPO3 development, and their expertise has been
invaluable in shaping these guidelines. Thank you, Netresearch, for your exceptional work!

**Copyright (c) Netresearch DTT GmbH** - Methodology and best practices  
Adapted by webconsulting.at for this skill collection
