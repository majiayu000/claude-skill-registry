---
name: acc-create-psr7-http-message
description: Generates PSR-7 HTTP Message implementations for PHP 8.5. Creates Request, Response, Stream, Uri, and ServerRequest classes with immutability. Includes unit tests.
---

# PSR-7 HTTP Message Generator

## Overview

Generates PSR-7 compliant HTTP message implementations following `Psr\Http\Message` interfaces.

## When to Use

- Building custom HTTP framework
- Creating lightweight HTTP message handling
- Need for immutable request/response objects
- Testing HTTP interactions

## Generated Components

| Component | Interface | Location |
|-----------|-----------|----------|
| Request | `RequestInterface` | `src/Infrastructure/Http/Message/` |
| Response | `ResponseInterface` | `src/Infrastructure/Http/Message/` |
| ServerRequest | `ServerRequestInterface` | `src/Infrastructure/Http/Message/` |
| Stream | `StreamInterface` | `src/Infrastructure/Http/Message/` |
| Uri | `UriInterface` | `src/Infrastructure/Http/Message/` |
| UploadedFile | `UploadedFileInterface` | `src/Infrastructure/Http/Message/` |

## Quick Template: Response

```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Http\Message;

use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\StreamInterface;

final readonly class Response implements ResponseInterface
{
    private const PHRASES = [
        200 => 'OK', 201 => 'Created', 204 => 'No Content',
        400 => 'Bad Request', 401 => 'Unauthorized', 403 => 'Forbidden',
        404 => 'Not Found', 500 => 'Internal Server Error',
    ];

    public function __construct(
        private int $statusCode = 200,
        private string $reasonPhrase = '',
        private array $headers = [],
        private StreamInterface $body = new Stream(''),
        private string $protocolVersion = '1.1',
    ) {}

    public function getStatusCode(): int { return $this->statusCode; }
    public function getReasonPhrase(): string { return $this->reasonPhrase; }
    public function getHeaders(): array { return $this->headers; }
    public function getBody(): StreamInterface { return $this->body; }

    public function withStatus(int $code, string $reasonPhrase = ''): static
    {
        return new self($code, $reasonPhrase ?: (self::PHRASES[$code] ?? ''),
            $this->headers, $this->body, $this->protocolVersion);
    }

    public function withHeader(string $name, $value): static
    {
        $headers = $this->headers;
        $headers[strtolower($name)] = is_array($value) ? $value : [$value];
        return new self($this->statusCode, $this->reasonPhrase, $headers,
            $this->body, $this->protocolVersion);
    }

    public function withBody(StreamInterface $body): static
    {
        return new self($this->statusCode, $this->reasonPhrase,
            $this->headers, $body, $this->protocolVersion);
    }

    // ... other MessageInterface methods
}
```

## Usage Example

```php
<?php

use App\Infrastructure\Http\Message\Response;
use App\Infrastructure\Http\Message\Stream;

// Create response
$response = new Response(200);
$response = $response
    ->withHeader('Content-Type', 'application/json')
    ->withBody(new Stream(json_encode(['status' => 'ok'])));

// Read response
echo $response->getStatusCode();           // 200
echo $response->getHeaderLine('Content-Type'); // application/json
echo (string) $response->getBody();        // {"status":"ok"}
```

## Requirements

```json
{
    "require": {
        "psr/http-message": "^2.0"
    }
}
```

## See Also

- `references/templates.md` - Full Response, Stream, Uri, Request, ServerRequest, UploadedFile templates
- `references/examples.md` - Integration examples
