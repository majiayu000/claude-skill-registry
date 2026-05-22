---
name: acc-create-psr16-simple-cache
description: Generates PSR-16 Simple Cache implementation for PHP 8.5. Creates CacheInterface with get/set/delete operations and TTL handling. Includes unit tests.
---

# PSR-16 Simple Cache Generator

## Overview

Generates PSR-16 compliant simple cache implementations for basic caching needs.

## When to Use

- Simple key-value caching
- Performance-critical code paths
- Minimal caching abstraction
- Quick cache integration

## Template: Array Cache

```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Cache;

use DateInterval;
use DateTimeImmutable;
use Psr\SimpleCache\CacheInterface;

final class ArrayCache implements CacheInterface
{
    /** @var array<string, array{value: mixed, expiration: ?int}> */
    private array $cache = [];

    public function get(string $key, mixed $default = null): mixed
    {
        $this->validateKey($key);

        if (!isset($this->cache[$key])) {
            return $default;
        }

        $item = $this->cache[$key];

        if ($item['expiration'] !== null && $item['expiration'] < time()) {
            unset($this->cache[$key]);

            return $default;
        }

        return $item['value'];
    }

    public function set(string $key, mixed $value, null|int|DateInterval $ttl = null): bool
    {
        $this->validateKey($key);

        $expiration = $this->calculateExpiration($ttl);

        $this->cache[$key] = [
            'value' => $value,
            'expiration' => $expiration,
        ];

        return true;
    }

    public function delete(string $key): bool
    {
        $this->validateKey($key);
        unset($this->cache[$key]);

        return true;
    }

    public function clear(): bool
    {
        $this->cache = [];

        return true;
    }

    public function getMultiple(iterable $keys, mixed $default = null): iterable
    {
        $result = [];

        foreach ($keys as $key) {
            $result[$key] = $this->get($key, $default);
        }

        return $result;
    }

    public function setMultiple(iterable $values, null|int|DateInterval $ttl = null): bool
    {
        foreach ($values as $key => $value) {
            $this->set($key, $value, $ttl);
        }

        return true;
    }

    public function deleteMultiple(iterable $keys): bool
    {
        foreach ($keys as $key) {
            $this->delete($key);
        }

        return true;
    }

    public function has(string $key): bool
    {
        return $this->get($key, $this) !== $this;
    }

    private function calculateExpiration(null|int|DateInterval $ttl): ?int
    {
        if ($ttl === null) {
            return null;
        }

        if ($ttl instanceof DateInterval) {
            return (new DateTimeImmutable())->add($ttl)->getTimestamp();
        }

        return time() + $ttl;
    }

    private function validateKey(string $key): void
    {
        if ($key === '' || preg_match('/[{}()\/\\\\@:]/', $key)) {
            throw new InvalidArgumentException("Invalid cache key: {$key}");
        }
    }
}
```

## Template: Redis Cache

```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Cache;

use DateInterval;
use DateTimeImmutable;
use Psr\SimpleCache\CacheInterface;
use Redis;

final readonly class RedisCache implements CacheInterface
{
    public function __construct(
        private Redis $redis,
        private string $prefix = 'cache:',
    ) {
    }

    public function get(string $key, mixed $default = null): mixed
    {
        $value = $this->redis->get($this->prefix . $key);

        if ($value === false) {
            return $default;
        }

        return unserialize($value);
    }

    public function set(string $key, mixed $value, null|int|DateInterval $ttl = null): bool
    {
        $serialized = serialize($value);
        $fullKey = $this->prefix . $key;

        if ($ttl === null) {
            return $this->redis->set($fullKey, $serialized);
        }

        $seconds = $ttl instanceof DateInterval
            ? (new DateTimeImmutable())->add($ttl)->getTimestamp() - time()
            : $ttl;

        return $this->redis->setex($fullKey, $seconds, $serialized);
    }

    public function delete(string $key): bool
    {
        return $this->redis->del($this->prefix . $key) > 0;
    }

    public function clear(): bool
    {
        $keys = $this->redis->keys($this->prefix . '*');

        if (!empty($keys)) {
            $this->redis->del($keys);
        }

        return true;
    }

    public function getMultiple(iterable $keys, mixed $default = null): iterable
    {
        $result = [];

        foreach ($keys as $key) {
            $result[$key] = $this->get($key, $default);
        }

        return $result;
    }

    public function setMultiple(iterable $values, null|int|DateInterval $ttl = null): bool
    {
        foreach ($values as $key => $value) {
            $this->set($key, $value, $ttl);
        }

        return true;
    }

    public function deleteMultiple(iterable $keys): bool
    {
        foreach ($keys as $key) {
            $this->delete($key);
        }

        return true;
    }

    public function has(string $key): bool
    {
        return $this->redis->exists($this->prefix . $key) > 0;
    }
}
```

## Template: Exceptions

```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Cache;

use Psr\SimpleCache\CacheException as PsrCacheException;
use Psr\SimpleCache\InvalidArgumentException as PsrInvalidArgumentException;

final class CacheException extends \RuntimeException implements PsrCacheException
{
}

final class InvalidArgumentException extends \InvalidArgumentException implements PsrInvalidArgumentException
{
}
```

## Usage Example

```php
<?php

use App\Infrastructure\Cache\RedisCache;

$cache = new RedisCache($redis);

// Simple operations
$cache->set('user:123', $userData, 3600);
$user = $cache->get('user:123');

// Check existence
if ($cache->has('user:123')) {
    $cache->delete('user:123');
}

// Multiple operations
$cache->setMultiple([
    'config:app' => $appConfig,
    'config:db' => $dbConfig,
], 86400);

$configs = $cache->getMultiple(['config:app', 'config:db']);
```

## Requirements

```json
{
    "require": {
        "psr/simple-cache": "^3.0"
    }
}
```
