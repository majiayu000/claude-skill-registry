---
name: feature-test
description: Create a PHPUnit feature test for API endpoints following this project's patterns. Use when testing controllers, API responses, and database interactions.
argument-hint: [ControllerName or endpoint]
disable-model-invocation: true
---

# Create Feature Test

Create a PHPUnit feature test for `$ARGUMENTS` following Laravel testing conventions.

## Test Location
`tests/Feature/`

## Current Test Setup
- PHPUnit 9.5.10
- Uses `RefreshDatabase` trait for clean DB state
- Environment: testing (defined in phpunit.xml)
- Factories available: `UserFactory` (others need to be created)

## Standard API Test Structure

```php
<?php

namespace Tests\Feature;

use App\Models\User;
use App\Models\{ModelName};
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class {ModelName}ControllerTest extends TestCase
{
    use RefreshDatabase;

    protected User $user;

    protected function setUp(): void
    {
        parent::setUp();
        $this->user = User::factory()->create();
    }

    /** @test */
    public function it_can_list_all_resources()
    {
        // Arrange
        {ModelName}::factory()->count(3)->create();

        // Act
        $response = $this->actingAs($this->user)
            ->getJson('/api/{resources}');

        // Assert
        $response->assertStatus(200)
            ->assertJsonCount(3, 'data');
    }

    /** @test */
    public function it_can_show_a_single_resource()
    {
        $resource = {ModelName}::factory()->create();

        $response = $this->actingAs($this->user)
            ->getJson("/api/{resource}/{$resource->id}");

        $response->assertStatus(200)
            ->assertJsonPath('data.id', $resource->id);
    }

    /** @test */
    public function it_can_create_a_resource()
    {
        $data = [
            'name' => 'Test Resource',
            'category_id' => 1,
            // ... other required fields
        ];

        $response = $this->actingAs($this->user)
            ->postJson('/api/{resources}', $data);

        $response->assertStatus(201);
        $this->assertDatabaseHas('{table_name}', ['name' => 'Test Resource']);
    }

    /** @test */
    public function it_validates_required_fields_on_create()
    {
        $response = $this->actingAs($this->user)
            ->postJson('/api/{resources}', []);

        $response->assertStatus(422)
            ->assertJsonValidationErrors(['name', 'category_id']);
    }

    /** @test */
    public function it_can_update_a_resource()
    {
        $resource = {ModelName}::factory()->create();

        $response = $this->actingAs($this->user)
            ->putJson("/api/backoffice/{resources}/{$resource->id}", [
                'name' => 'Updated Name'
            ]);

        $response->assertStatus(200);
        $this->assertDatabaseHas('{table_name}', ['name' => 'Updated Name']);
    }

    /** @test */
    public function it_can_delete_a_resource()
    {
        $resource = {ModelName}::factory()->create();

        $response = $this->actingAs($this->user)
            ->deleteJson("/api/backoffice/{resources}/{$resource->id}");

        $response->assertStatus(200);
        $this->assertDatabaseMissing('{table_name}', ['id' => $resource->id]);
    }
}
```

## Testing POS-Specific Flows

### Order Creation Test
```php
/** @test */
public function it_can_create_an_order_for_table()
{
    $table = Table::factory()->create();
    $inventory = Inventory::factory()->create(['price' => 100]);

    $orderData = [
        'table_id' => $table->id,
        'order' => [
            [
                'id' => $inventory->id,
                'name' => $inventory->name,
                'price' => $inventory->price,
                'qty' => 2,
            ]
        ]
    ];

    $response = $this->actingAs($this->user)
        ->postJson('/api/orders', $orderData);

    $response->assertStatus(201);
    $this->assertDatabaseHas('orders', ['table_id' => $table->id]);
}
```

### Invoice Creation Test
```php
/** @test */
public function it_can_create_invoice_from_order()
{
    $table = Table::factory()->create();
    $order = Order::factory()->create(['table_id' => $table->id]);

    $invoiceData = [
        'user_id' => $this->user->id,
        'table_id' => $table->id,
        'order' => $order->order,
        'total' => 500,
    ];

    $response = $this->actingAs($this->user)
        ->postJson('/api/invoices', $invoiceData);

    $response->assertStatus(201);
    // Order should be deleted after invoice creation
    $this->assertDatabaseMissing('orders', ['id' => $order->id]);
}
```

### Refund Test
```php
/** @test */
public function it_can_refund_an_invoice()
{
    $invoice = Invoice::factory()->create([
        'status' => Invoice::STATUS_PAYED
    ]);
    $refundReason = RefundReason::factory()->create();

    $response = $this->actingAs($this->user)
        ->postJson("/api/invoices/{$invoice->id}/refund", [
            'refund_reason_id' => $refundReason->id
        ]);

    $response->assertStatus(200);
    $this->assertDatabaseHas('invoices', [
        'id' => $invoice->id,
        'status' => Invoice::STATUS_REFUNDED
    ]);
}
```

## Factory Creation Pattern

Create factories in `database/factories/`:

```php
<?php

namespace Database\Factories;

use App\Models\{ModelName};
use Illuminate\Database\Eloquent\Factories\Factory;

class {ModelName}Factory extends Factory
{
    protected $model = {ModelName}::class;

    public function definition()
    {
        return [
            'name' => $this->faker->word(),
            'description' => $this->faker->sentence(),
            'price' => $this->faker->numberBetween(100, 10000),
            'status' => 1,
            'category_id' => Category::factory(),
        ];
    }

    // State methods
    public function inactive()
    {
        return $this->state(['status' => 0]);
    }
}
```

## Running Tests

```bash
# Run all tests
./vendor/bin/phpunit

# Run specific test file
./vendor/bin/phpunit tests/Feature/InvoiceControllerTest.php

# Run specific test method
./vendor/bin/phpunit --filter=it_can_create_an_order

# Run with coverage
./vendor/bin/phpunit --coverage-html coverage/
```

## Steps

1. Create test file in `tests/Feature/`
2. Create necessary factories in `database/factories/`
3. Use `RefreshDatabase` trait
4. Test all CRUD operations
5. Test validation rules
6. Test business logic (refunds, status changes, etc.)
7. Run tests to verify
