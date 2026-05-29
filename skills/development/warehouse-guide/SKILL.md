---
name: warehouse-guide
description: Reference for the warehouse/inventory tracking system. Use when working with stock management, warehouse status, inventory consumption, or understanding how sales affect stock levels.
user-invocable: false
---

# Warehouse System Guide

This POS system includes a complex warehouse management system for tracking inventory consumption.

## Core Concepts

### Warehouse Status Types
```php
// In WarehouseStatus model
const TYPE_IN = 0;      // Stock received (purchase/delivery)
const TYPE_OUT = 1;     // Stock consumed (from sales)
const TYPE_RESET = 2;   // Manual inventory count/reset
```

### Data Flow
```
Sale Created → SalesService::parseAndSaveOrder()
    → Creates Sales records
    → Calls populateWarehouse() for each item
        → Looks up WarehouseInventory mappings
        → Creates WarehouseStatus TYPE_OUT entries
```

## Key Models

### Warehouse
- Represents a storage location/category
- Has `name`, `unit`, `category_id`, `order`
- Related to WarehouseCategory (not product Category)

### WarehouseInventory
- Maps inventory items to warehouses
- Contains `norm` field: consumption rate per sale unit
- Example: If `norm = 2.5`, selling 1 unit consumes 2.5 warehouse units

### WarehouseStatus
- Ledger of all stock movements
- Fields: `warehouse_id`, `inventory_id`, `quantity`, `type`, `date`, `batch_id`
- `batch_id` links to invoice ID for TYPE_OUT entries

## Key Files

### Controllers
- `WarehouseController` - CRUD for warehouses
- `WarehouseStatusController` - Stock movements, imports, recalculation
- `WarehouseInventoryController` - Inventory-to-warehouse mappings
- `WarehouseCategoryController` - Warehouse categories

### Services
- `services/SalesService.php` - Contains `populateWarehouse()` method

## Important Patterns

### Stock Calculation Query
```php
// From WarehouseStatusController::index()
WarehouseStatus::selectRaw('
    warehouse_id,
    SUM(CASE WHEN type = 0 THEN quantity ELSE 0 END) as import_quantity,
    SUM(CASE WHEN type = 1 THEN quantity ELSE 0 END) as sale_quantity,
    SUM(CASE WHEN type = 2 THEN quantity ELSE 0 END) as reset_quantity
')
->groupBy('warehouse_id')
->whereBetween('date', $workingDayRange)
```

### Consumption Calculation
```php
// In SalesService::populateWarehouse()
$warehouseInventories = WarehouseInventory::where('inventory_id', $order['id'])->get();

foreach ($warehouseInventories as $wi) {
    WarehouseStatus::create([
        'warehouse_id' => $wi->warehouse_id,
        'inventory_id' => $order['id'],
        'quantity' => $order['qty'] * $wi->norm,  // qty * consumption rate
        'type' => WarehouseStatus::TYPE_OUT,
        'date' => WorkingDay::setCorrectDateForWorkingDay(),
        'batch_id' => $invoiceId,
    ]);
}
```

### Error Recovery
Failed warehouse operations are logged to `ExceptionLog` model and can be retried with:
```bash
php artisan command:process-unprocessed-imports
```

## API Endpoints

```
GET  /api/backoffice/warehouse              - List warehouses
POST /api/backoffice/warehouse              - Create warehouse
GET  /api/backoffice/warehouse-status       - List stock movements
POST /api/backoffice/warehouse-status       - Record stock movement
POST /api/backoffice/warehouse-status/recalculate/{id} - Recalculate stock
GET  /api/backoffice/warehouse-inventory    - List inventory mappings
POST /api/backoffice/warehouse-inventory    - Create/update mappings
```

## Working Day Integration

All warehouse dates use the "working day" concept (4am-4am):
```php
use Services\WorkingDay;

$date = WorkingDay::setCorrectDateForWorkingDay();
$range = WorkingDay::getWorkingDay();
```
