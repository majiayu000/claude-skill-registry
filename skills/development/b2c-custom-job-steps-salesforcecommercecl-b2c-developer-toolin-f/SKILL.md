---
name: b2c-custom-job-steps
description: Guide for creating custom job steps for batch processing, imports, exports, scheduled tasks, and data sync in Salesforce B2C Commerce. Use this when writing new job code.
keywords: [create job, new job, batch job, scheduled job, import job, export job, data sync, bulk processing, steptypes.json, job step code]
---

# Custom Job Steps Skill

This skill guides you through **creating new custom job steps** for Salesforce B2C Commerce batch processing.

> **Running an existing job?** If you need to execute jobs or import site archives via CLI, use the `b2c-cli:b2c-job` skill instead.

## When to Use This Skill

- Creating a **new scheduled job** for batch processing
- Building a **data import job** (customers, products, orders)
- Building a **data export job** (reports, feeds, sync)
- Implementing **data sync** between systems
- Creating **cleanup or maintenance tasks**

## Overview

Custom job steps allow you to execute custom business logic as part of B2C Commerce jobs. There are two execution models:

| Model | Use Case | Progress Tracking |
|-------|----------|-------------------|
| **Task-oriented** | Single operations (FTP, import/export) | Limited |
| **Chunk-oriented** | Bulk data processing | Fine-grained |

## File Structure

```
my_cartridge/
├── cartridge/
│   ├── scripts/
│   │   └── steps/
│   │       ├── myTaskStep.js       # Task-oriented script
│   │       └── myChunkStep.js      # Chunk-oriented script
│   └── my_cartridge.properties
└── steptypes.json                  # Step type definitions (at cartridge ROOT)
```

**Important:** The `steptypes.json` file must be placed in the **root** folder of the cartridge, not inside the `cartridge/` directory. Only one `steptypes.json` file per cartridge.

## Step Type Definition (steptypes.json)

```json
{
    "step-types": {
        "script-module-step": [
            {
                "@type-id": "custom.MyTaskStep",
                "@supports-parallel-execution": "false",
                "@supports-site-context": "true",
                "@supports-organization-context": "false",
                "description": "My custom task step",
                "module": "my_cartridge/cartridge/scripts/steps/myTaskStep.js",
                "function": "execute",
                "timeout-in-seconds": 900,
                "parameters": {
                    "parameter": [
                        {
                            "@name": "InputFile",
                            "@type": "string",
                            "@required": "true",
                            "description": "Path to input file"
                        },
                        {
                            "@name": "Enabled",
                            "@type": "boolean",
                            "@required": "false",
                            "default-value": "true",
                            "description": "Enable processing"
                        }
                    ]
                },
                "status-codes": {
                    "status": [
                        {
                            "@code": "OK",
                            "description": "Step completed successfully"
                        },
                        {
                            "@code": "ERROR",
                            "description": "Step failed"
                        },
                        {
                            "@code": "NO_DATA",
                            "description": "No data to process"
                        }
                    ]
                }
            }
        ],
        "chunk-script-module-step": [
            {
                "@type-id": "custom.MyChunkStep",
                "@supports-parallel-execution": "true",
                "@supports-site-context": "true",
                "@supports-organization-context": "false",
                "description": "Bulk data processing step",
                "module": "my_cartridge/cartridge/scripts/steps/myChunkStep.js",
                "before-step-function": "beforeStep",
                "read-function": "read",
                "process-function": "process",
                "write-function": "write",
                "after-step-function": "afterStep",
                "total-count-function": "getTotalCount",
                "chunk-size": 100,
                "transactional": "false",
                "timeout-in-seconds": 1800,
                "parameters": {
                    "parameter": [
                        {
                            "@name": "CategoryId",
                            "@type": "string",
                            "@required": "true"
                        }
                    ]
                }
            }
        ]
    }
}
```

## Task-Oriented Steps

Use for single operations like FTP transfers, file generation, or import/export.

### Script (scripts/steps/myTaskStep.js)

```javascript
'use strict';

var Status = require('dw/system/Status');
var Logger = require('dw/system/Logger');

/**
 * Execute the task step
 * @param {Object} parameters - Job step parameters
 * @param {dw.job.JobStepExecution} stepExecution - Step execution context
 * @returns {dw.system.Status} Execution status
 */
exports.execute = function (parameters, stepExecution) {
    var log = Logger.getLogger('job', 'MyTaskStep');

    try {
        var inputFile = parameters.InputFile;
        var enabled = parameters.Enabled;

        if (!enabled) {
            log.info('Step disabled, skipping');
            return new Status(Status.OK, 'SKIP', 'Step disabled');
        }

        // Your business logic here
        log.info('Processing file: ' + inputFile);

        // Return success
        return new Status(Status.OK);

    } catch (e) {
        log.error('Step failed: ' + e.message);
        return new Status(Status.ERROR, 'ERROR', e.message);
    }
};
```

### Status Codes

```javascript
// Success
return new Status(Status.OK);
return new Status(Status.OK, 'CUSTOM_CODE', 'Custom message');

// Error
return new Status(Status.ERROR);
return new Status(Status.ERROR, null, 'Error message');
```

**Important:** Custom status codes work **only** with OK status. If you use a custom code with ERROR status, it is replaced with ERROR. Custom status codes cannot contain commas, wildcards, leading/trailing whitespace, or exceed 100 characters.

## Chunk-Oriented Steps

Use for bulk processing of countable data (products, orders, customers).

**Important:** You cannot define custom exit status for chunk-oriented steps. Chunk modules always finish with either **OK** or **ERROR**.

### Required Functions

| Function | Purpose | Returns |
|----------|---------|---------|
| `read()` | Get next item | Item or nothing |
| `process(item)` | Transform item | Processed item or nothing (filters) |
| `write(items)` | Save chunk of items | Nothing |

### Optional Functions

| Function | Purpose | Returns |
|----------|---------|---------|
| `beforeStep()` | Initialize (open files, queries) | Nothing |
| `afterStep(success)` | Cleanup (close files) | Nothing |
| `getTotalCount()` | Return total items for progress | Number |
| `beforeChunk()` | Before each chunk | Nothing |
| `afterChunk()` | After each chunk | Nothing |

### Script (scripts/steps/myChunkStep.js)

```javascript
'use strict';

var ProductMgr = require('dw/catalog/ProductMgr');
var Transaction = require('dw/system/Transaction');
var Logger = require('dw/system/Logger');
var File = require('dw/io/File');
var FileWriter = require('dw/io/FileWriter');

var log = Logger.getLogger('job', 'MyChunkStep');
var products;
var fileWriter;

/**
 * Initialize before processing
 */
exports.beforeStep = function (parameters, stepExecution) {
    log.info('Starting chunk processing');

    // Open resources
    var outputFile = new File(File.IMPEX + '/export/products.csv');
    fileWriter = new FileWriter(outputFile);
    fileWriter.writeLine('ID,Name,Price');

    // Query products
    products = ProductMgr.queryAllSiteProducts();
};

/**
 * Get total count for progress tracking
 */
exports.getTotalCount = function (parameters, stepExecution) {
    return products.count;
};

/**
 * Read next item
 * Return nothing to signal end of data
 */
exports.read = function (parameters, stepExecution) {
    if (products.hasNext()) {
        return products.next();
    }
    // Return nothing = end of data
};

/**
 * Process single item
 * Return nothing to filter out item
 */
exports.process = function (product, parameters, stepExecution) {
    // Filter: skip offline products
    if (!product.online) {
        return;  // Filtered out
    }

    // Transform
    return {
        id: product.ID,
        name: product.name,
        price: product.priceModel.price.value
    };
};

/**
 * Write chunk of processed items
 */
exports.write = function (items, parameters, stepExecution) {
    for (var i = 0; i < items.size(); i++) {
        var item = items.get(i);
        fileWriter.writeLine(item.id + ',' + item.name + ',' + item.price);
    }
};

/**
 * Cleanup after all chunks
 */
exports.afterStep = function (success, parameters, stepExecution) {
    // Close resources
    if (fileWriter) {
        fileWriter.close();
    }
    if (products) {
        products.close();
    }

    if (success) {
        log.info('Chunk processing completed successfully');
    } else {
        log.error('Chunk processing failed');
    }
};
```

## Parameter Types

| Type | Description | Example Value |
|------|-------------|---------------|
| `string` | Text value | `"my-value"` |
| `boolean` | true/false | `true` |
| `long` | Integer | `12345` |
| `double` | Decimal | `123.45` |
| `datetime-string` | ISO datetime | `"2024-01-15T10:30:00Z"` |
| `date-string` | ISO date | `"2024-01-15"` |
| `time-string` | ISO time | `"10:30:00"` |

### Parameter Validation Attributes

| Attribute | Applies To | Description |
|-----------|------------|-------------|
| `@trim` | All | Trim whitespace before validation (default: `true`) |
| `@required` | All | Mark as required (default: `true`) |
| `@target-type` | datetime-string, date-string, time-string | Convert to `long` or `date` (default: `date`) |
| `pattern` | string | Regex pattern for validation |
| `min-length` | string | Minimum string length (must be ≥1) |
| `max-length` | string | Maximum string length (max 1000 chars total) |
| `min-value` | long, double, datetime-string, time-string | Minimum numeric value |
| `max-value` | long, double, datetime-string, time-string | Maximum numeric value |
| `enum-values` | All | Restrict to allowed values (dropdown in BM) |

## Configuration Options

### steptypes.json Attributes

| Attribute | Required | Description |
|-----------|----------|-------------|
| `@type-id` | Yes | Unique ID (must start with `custom.`, max 100 chars) |
| `@supports-parallel-execution` | No | Allow parallel execution (default: `true`) |
| `@supports-site-context` | No | Available in site-scoped jobs (default: `true`) |
| `@supports-organization-context` | No | Available in org-scoped jobs (default: `true`) |
| `module` | Yes | Path to script module |
| `function` | Yes | Function name to execute (task-oriented) |
| `timeout-in-seconds` | No | Step timeout (recommended to set) |
| `transactional` | No | Wrap in single transaction (default: `false`) |
| `chunk-size` | Yes* | Items per chunk (*required for chunk steps) |

**Context Constraints:** `@supports-site-context` and `@supports-organization-context` cannot both be `true` or both be `false` - one must be `true` and the other `false`.

## Best Practices

1. **Use chunk-oriented** for bulk data - better progress tracking and resumability
2. **Close resources** in `afterStep()` - queries, files, connections
3. **Set explicit timeouts** - default may be too short
4. **Log progress** - helps debugging
5. **Handle errors gracefully** - return proper Status objects
6. **Don't rely on transactional=true** - use `Transaction.wrap()` for control

## Related Skills

- `b2c-cli:b2c-job` - For **running** existing jobs and importing site archives via CLI
- `b2c:b2c-webservices` - When job steps need to call external HTTP services or APIs, use the webservices skill for service configuration and HTTP client patterns

## Detailed Reference

- [Task-Oriented Steps](references/TASK-ORIENTED.md) - Full task step patterns
- [Chunk-Oriented Steps](references/CHUNK-ORIENTED.md) - Full chunk step patterns
- [steptypes.json Reference](references/STEPTYPES-JSON.md) - Complete schema
