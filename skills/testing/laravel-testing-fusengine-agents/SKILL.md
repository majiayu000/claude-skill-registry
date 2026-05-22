---
name: laravel-testing
description: Write tests with Pest/PHPUnit, feature tests, unit tests, mocking, and factories. Use when testing controllers, services, models, or implementing TDD.
user-invocable: false
---

# Laravel Testing

## Documentation

### Testing
- [testing.md](docs/testing.md) - Testing basics
- [http-tests.md](docs/http-tests.md) - HTTP feature tests
- [database-testing.md](docs/database-testing.md) - Database testing
- [console-tests.md](docs/console-tests.md) - Console tests
- [mocking.md](docs/mocking.md) - Mocking & fakes
- [dusk.md](docs/dusk.md) - Browser testing

### Code Quality
- [pint.md](docs/pint.md) - Code style fixer

## Pest Feature Test

```php
<?php

declare(strict_types=1);

use App\Models\Post;
use App\Models\User;

describe('PostController', function () {
    beforeEach(function () {
        $this->user = User::factory()->create();
    });

    it('lists all posts', function () {
        Post::factory()->count(3)->create();

        $this->getJson('/api/v1/posts')
            ->assertOk()
            ->assertJsonCount(3, 'data');
    });

    it('creates a post when authenticated', function () {
        $data = ['title' => 'Test', 'content' => 'Content', 'status' => 'draft'];

        $this->actingAs($this->user)
            ->postJson('/api/v1/posts', $data)
            ->assertCreated()
            ->assertJsonPath('data.title', 'Test');

        $this->assertDatabaseHas('posts', ['title' => 'Test']);
    });

    it('returns 401 for unauthenticated users', function () {
        $this->postJson('/api/v1/posts', [])
            ->assertUnauthorized();
    });

    it('validates required fields', function () {
        $this->actingAs($this->user)
            ->postJson('/api/v1/posts', [])
            ->assertUnprocessable()
            ->assertJsonValidationErrors(['title', 'content']);
    });
});
```

## Unit Test with Mocking

```php
<?php

declare(strict_types=1);

use App\Services\PostService;
use App\Repositories\Contracts\PostRepositoryInterface;

describe('PostService', function () {
    it('creates a post with valid data', function () {
        $repository = Mockery::mock(PostRepositoryInterface::class);
        $repository->shouldReceive('create')
            ->once()
            ->andReturn(new Post(['title' => 'Test']));

        $service = new PostService($repository);
        $post = $service->create(['title' => 'Test']);

        expect($post->title)->toBe('Test');
    });
});
```

## Factory

```php
<?php

declare(strict_types=1);

namespace Database\Factories;

final class PostFactory extends Factory
{
    public function definition(): array
    {
        return [
            'title' => fake()->sentence(),
            'content' => fake()->paragraphs(3, true),
            'status' => PostStatus::Draft,
            'user_id' => User::factory(),
        ];
    }

    public function published(): static
    {
        return $this->state([
            'status' => PostStatus::Published,
            'published_at' => now(),
        ]);
    }
}
```

## Assertions

```php
// Response
$response->assertOk();           // 200
$response->assertCreated();      // 201
$response->assertUnauthorized(); // 401
$response->assertUnprocessable(); // 422

// JSON
$response->assertJson(['key' => 'value']);
$response->assertJsonPath('data.id', 1);
$response->assertJsonCount(3, 'data');

// Database
$this->assertDatabaseHas('posts', ['title' => 'Test']);
$this->assertDatabaseMissing('posts', ['title' => 'Deleted']);
$this->assertSoftDeleted('posts', ['id' => 1]);
```

## Mocking

```php
// Mock HTTP
Http::fake([
    'api.example.com/*' => Http::response(['data' => 'test'], 200),
]);

// Mock service
$this->mock(PaymentService::class, function ($mock) {
    $mock->shouldReceive('charge')->once()->andReturn(true);
});
```
