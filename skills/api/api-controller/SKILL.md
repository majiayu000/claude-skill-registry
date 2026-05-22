---
name: api-controller
description: Create a new Laravel API controller following this project's patterns. Use when creating new API endpoints, CRUD controllers, or backoffice controllers.
argument-hint: [ResourceName]
disable-model-invocation: true
---

# Create API Controller

Create a new Laravel API controller for `$ARGUMENTS` following this project's established patterns.

## Project Patterns

### Controller Location
- Public API controllers: `app/Http/Controllers/`
- Auth controllers: `app/Http/Controllers/Auth/`

### Standard Controller Structure
```php
<?php

namespace App\Http\Controllers;

use App\Models\{ModelName};
use App\Http\Resources\{ModelName}Resource;
use App\Http\Resources\{ModelName}Collection;
use App\Http\Requests\{ModelName}StoreRequest;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Cache;

class {ModelName}Controller extends Controller
{
    // GET /api/{resource} - List all
    public function index()
    {
        return new {ModelName}Collection({ModelName}::all());
    }

    // GET /api/{resource}/{id} - Show one
    public function show($id)
    {
        return new {ModelName}Resource({ModelName}::findOrFail($id));
    }

    // POST /api/{resource} - Create
    public function store({ModelName}StoreRequest $request)
    {
        $model = {ModelName}::create($request->validated());

        // Invalidate cache if using caching
        Cache::forget('{resource}-all');

        return new {ModelName}Resource($model);
    }

    // PUT /api/{resource}/{id} - Update
    public function update(Request $request, $id)
    {
        $model = {ModelName}::findOrFail($id);
        $model->update($request->all());

        Cache::forget('{resource}-all');

        return new {ModelName}Resource($model);
    }

    // DELETE /api/{resource}/{id} - Delete
    public function destroy($id)
    {
        {ModelName}::destroy($id);
        Cache::forget('{resource}-all');

        return response()->json(['success' => true]);
    }
}
```

### Caching Pattern (used in InventoryController, CategoryController)
```php
public function all()
{
    return Cache::remember('inventory-all', 60, function() {
        return new InventoryCollection(Inventory::all());
    });
}
```

### Filtering Pattern (used in InvoiceController, SalesController)
```php
use App\Models\Traits\Revenue; // or SalesRevenue, InventoryFilters

public function index(Request $request)
{
    return Invoice::filter($request)->paginate(15);
}
```

### Pusher Broadcasting (for real-time updates)
```php
use Services\Pusher;

// After mutations that need real-time sync:
try {
    Pusher::trigger('tables-update', []);
} catch (\Exception $e) {
    \Log::error($e->getMessage());
}
```

### Backoffice Controller Pattern
Backoffice routes are prefixed with `/api/backoffice/` and may have different methods:
- `allBackoffice()` - Admin-specific listing with more details
- `export()` - Excel/CSV export functionality

## Steps

1. Create the controller in `app/Http/Controllers/`
2. Create corresponding Resource class in `app/Http/Resources/`
3. Create Collection class if needed
4. Create FormRequest for validation in `app/Http/Requests/`
5. Add routes to `routes/api.php`
6. Consider if caching is needed for read operations
7. Add Pusher triggers if real-time updates are needed

## Route Registration Pattern
```php
// In routes/api.php

// Public routes
Route::get('{resources}', [{ModelName}Controller::class, 'index']);
Route::get('{resource}/{id}', [{ModelName}Controller::class, 'show']);
Route::post('{resources}', [{ModelName}Controller::class, 'store']);

// Backoffice routes (in the backoffice prefix group)
Route::prefix('/backoffice')->group(function () {
    Route::put('/{resources}/{id}', [{ModelName}Controller::class, 'update']);
    Route::delete('/{resources}/{id}', [{ModelName}Controller::class, 'destroy']);
});
```
