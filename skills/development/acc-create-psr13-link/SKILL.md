---
name: acc-create-psr13-link
description: Generates PSR-13 Hypermedia Links implementation for PHP 8.5. Creates LinkInterface, EvolvableLinkInterface, and LinkProviderInterface for HATEOAS support. Includes unit tests.
---

# PSR-13 Hypermedia Links Generator

## Overview

Generates PSR-13 compliant hypermedia link implementations for HATEOAS REST APIs.

## When to Use

- Building REST APIs with HATEOAS
- Creating hypermedia-driven resources
- Link relation management
- URI templates

## Generated Components

| Component | Description | Location |
|-----------|-------------|----------|
| Link | LinkInterface impl | `src/Infrastructure/Http/Link/` |
| LinkProvider | Provider impl | `src/Infrastructure/Http/Link/` |
| Unit Tests | PHPUnit tests | `tests/Unit/Infrastructure/Http/Link/` |

## Template: Link

```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Http\Link;

use Psr\Link\EvolvableLinkInterface;
use Stringable;

final readonly class Link implements EvolvableLinkInterface
{
    /** @param string[] $rels */
    public function __construct(
        private string $href,
        private array $rels = [],
        private array $attributes = [],
        private bool $templated = false,
    ) {
    }

    public function getHref(): string
    {
        return $this->href;
    }

    public function isTemplated(): bool
    {
        return $this->templated || str_contains($this->href, '{');
    }

    public function getRels(): array
    {
        return $this->rels;
    }

    public function getAttributes(): array
    {
        return $this->attributes;
    }

    public function withHref(string|Stringable $href): static
    {
        return new self((string) $href, $this->rels, $this->attributes, $this->templated);
    }

    public function withRel(string $rel): static
    {
        $rels = [...$this->rels, $rel];

        return new self($this->href, array_unique($rels), $this->attributes, $this->templated);
    }

    public function withoutRel(string $rel): static
    {
        $rels = array_filter($this->rels, fn($r) => $r !== $rel);

        return new self($this->href, array_values($rels), $this->attributes, $this->templated);
    }

    public function withAttribute(string $attribute, string|Stringable $value): static
    {
        $attributes = $this->attributes;
        $attributes[$attribute] = (string) $value;

        return new self($this->href, $this->rels, $attributes, $this->templated);
    }

    public function withoutAttribute(string $attribute): static
    {
        $attributes = $this->attributes;
        unset($attributes[$attribute]);

        return new self($this->href, $this->rels, $attributes, $this->templated);
    }
}
```

## Template: Link Provider

```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Http\Link;

use Psr\Link\EvolvableLinkProviderInterface;
use Psr\Link\LinkInterface;

final readonly class LinkProvider implements EvolvableLinkProviderInterface
{
    /** @param LinkInterface[] $links */
    public function __construct(
        private array $links = [],
    ) {
    }

    public function getLinks(): iterable
    {
        return $this->links;
    }

    public function getLinksByRel(string $rel): iterable
    {
        foreach ($this->links as $link) {
            if (in_array($rel, $link->getRels(), true)) {
                yield $link;
            }
        }
    }

    public function withLink(LinkInterface $link): static
    {
        return new self([...$this->links, $link]);
    }

    public function withoutLink(LinkInterface $link): static
    {
        $links = array_filter(
            $this->links,
            fn($l) => $l !== $link,
        );

        return new self(array_values($links));
    }
}
```

## Template: Resource with Links

```php
<?php

declare(strict_types=1);

namespace App\Presentation\Api\Resource;

use App\Domain\User\Entity\User;
use App\Infrastructure\Http\Link\Link;
use App\Infrastructure\Http\Link\LinkProvider;
use Psr\Link\LinkProviderInterface;

final readonly class UserResource implements LinkProviderInterface
{
    private LinkProvider $linkProvider;

    public function __construct(
        public string $id,
        public string $email,
        public string $name,
    ) {
        $this->linkProvider = new LinkProvider([
            (new Link("/api/users/{$this->id}"))->withRel('self'),
            (new Link("/api/users/{$this->id}/posts"))->withRel('posts'),
            (new Link('/api/users'))->withRel('collection'),
        ]);
    }

    public static function fromEntity(User $user): self
    {
        return new self(
            $user->getId()->toString(),
            $user->getEmail()->toString(),
            $user->getName(),
        );
    }

    public function getLinks(): iterable
    {
        return $this->linkProvider->getLinks();
    }

    public function getLinksByRel(string $rel): iterable
    {
        return $this->linkProvider->getLinksByRel($rel);
    }

    public function toArray(): array
    {
        $data = [
            'id' => $this->id,
            'email' => $this->email,
            'name' => $this->name,
            '_links' => [],
        ];

        foreach ($this->getLinks() as $link) {
            foreach ($link->getRels() as $rel) {
                $data['_links'][$rel] = [
                    'href' => $link->getHref(),
                    'templated' => $link->isTemplated(),
                ];
            }
        }

        return $data;
    }
}
```

## Usage Example

```php
<?php

use App\Infrastructure\Http\Link\Link;
use App\Infrastructure\Http\Link\LinkProvider;

// Create links
$selfLink = (new Link('/api/users/123'))
    ->withRel('self')
    ->withAttribute('title', 'User Profile');

$collectionLink = (new Link('/api/users'))
    ->withRel('collection');

$templateLink = (new Link('/api/users/{id}'))
    ->withRel('user');

// Create provider
$provider = (new LinkProvider())
    ->withLink($selfLink)
    ->withLink($collectionLink)
    ->withLink($templateLink);

// Get links by relation
foreach ($provider->getLinksByRel('self') as $link) {
    echo $link->getHref(); // /api/users/123
}
```

## Requirements

```json
{
    "require": {
        "psr/link": "^2.0"
    }
}
```
