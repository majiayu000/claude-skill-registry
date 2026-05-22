---
name: acc-create-psr17-http-factory
description: Generates PSR-17 HTTP Factories implementation for PHP 8.5. Creates RequestFactoryInterface, ResponseFactoryInterface, StreamFactoryInterface, UriFactoryInterface, ServerRequestFactoryInterface, UploadedFileFactoryInterface. Includes unit tests.
---

# PSR-17 HTTP Factories Generator

## Overview

Generates PSR-17 compliant HTTP factory implementations for creating PSR-7 objects.

## When to Use

- Creating PSR-7 messages in DI containers
- Testing HTTP interactions
- Building HTTP frameworks
- Decoupling from specific PSR-7 implementations

## Template: HTTP Factory

```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Http\Factory;

use App\Infrastructure\Http\Message\Request;
use App\Infrastructure\Http\Message\Response;
use App\Infrastructure\Http\Message\ServerRequest;
use App\Infrastructure\Http\Message\Stream;
use App\Infrastructure\Http\Message\UploadedFile;
use App\Infrastructure\Http\Message\Uri;
use Psr\Http\Message\RequestFactoryInterface;
use Psr\Http\Message\RequestInterface;
use Psr\Http\Message\ResponseFactoryInterface;
use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestFactoryInterface;
use Psr\Http\Message\ServerRequestInterface;
use Psr\Http\Message\StreamFactoryInterface;
use Psr\Http\Message\StreamInterface;
use Psr\Http\Message\UploadedFileFactoryInterface;
use Psr\Http\Message\UploadedFileInterface;
use Psr\Http\Message\UriFactoryInterface;
use Psr\Http\Message\UriInterface;

final readonly class HttpFactory implements
    RequestFactoryInterface,
    ResponseFactoryInterface,
    ServerRequestFactoryInterface,
    StreamFactoryInterface,
    UploadedFileFactoryInterface,
    UriFactoryInterface
{
    public function createRequest(string $method, $uri): RequestInterface
    {
        return new Request(
            $method,
            $uri instanceof UriInterface ? $uri : $this->createUri($uri),
        );
    }

    public function createResponse(int $code = 200, string $reasonPhrase = ''): ResponseInterface
    {
        return new Response($code, $reasonPhrase);
    }

    public function createServerRequest(
        string $method,
        $uri,
        array $serverParams = [],
    ): ServerRequestInterface {
        return new ServerRequest(
            $method,
            $uri instanceof UriInterface ? $uri : $this->createUri($uri),
            serverParams: $serverParams,
        );
    }

    public function createStream(string $content = ''): StreamInterface
    {
        return new Stream($content);
    }

    public function createStreamFromFile(string $filename, string $mode = 'r'): StreamInterface
    {
        $resource = fopen($filename, $mode);

        if ($resource === false) {
            throw new \RuntimeException("Cannot open file: {$filename}");
        }

        return $this->createStreamFromResource($resource);
    }

    public function createStreamFromResource($resource): StreamInterface
    {
        $content = stream_get_contents($resource);

        if ($content === false) {
            throw new \RuntimeException('Cannot read from resource');
        }

        return new Stream($content);
    }

    public function createUploadedFile(
        StreamInterface $stream,
        ?int $size = null,
        int $error = UPLOAD_ERR_OK,
        ?string $clientFilename = null,
        ?string $clientMediaType = null,
    ): UploadedFileInterface {
        $tmpFile = tempnam(sys_get_temp_dir(), 'upload_');
        file_put_contents($tmpFile, (string) $stream);

        return new UploadedFile(
            $tmpFile,
            $size ?? $stream->getSize(),
            $error,
            $clientFilename,
            $clientMediaType,
        );
    }

    public function createUri(string $uri = ''): UriInterface
    {
        return Uri::fromString($uri);
    }
}
```

## Usage Example

```php
<?php

use App\Infrastructure\Http\Factory\HttpFactory;

$factory = new HttpFactory();

// Create request
$request = $factory->createRequest('GET', 'https://api.example.com/users');
$request = $request->withHeader('Accept', 'application/json');

// Create response
$response = $factory->createResponse(200);
$response = $response
    ->withHeader('Content-Type', 'application/json')
    ->withBody($factory->createStream(json_encode(['status' => 'ok'])));

// Create server request
$serverRequest = $factory->createServerRequest('POST', '/api/users', $_SERVER);

// Create URI
$uri = $factory->createUri('https://example.com/path?query=value');

// Create stream from file
$stream = $factory->createStreamFromFile('/path/to/file.txt');
```

## DI Container Registration

```php
<?php

// Symfony services.yaml
services:
    App\Infrastructure\Http\Factory\HttpFactory:
        public: true

    Psr\Http\Message\RequestFactoryInterface:
        alias: App\Infrastructure\Http\Factory\HttpFactory

    Psr\Http\Message\ResponseFactoryInterface:
        alias: App\Infrastructure\Http\Factory\HttpFactory

    Psr\Http\Message\StreamFactoryInterface:
        alias: App\Infrastructure\Http\Factory\HttpFactory

    Psr\Http\Message\UriFactoryInterface:
        alias: App\Infrastructure\Http\Factory\HttpFactory

    Psr\Http\Message\ServerRequestFactoryInterface:
        alias: App\Infrastructure\Http\Factory\HttpFactory

    Psr\Http\Message\UploadedFileFactoryInterface:
        alias: App\Infrastructure\Http\Factory\HttpFactory
```

## Requirements

```json
{
    "require": {
        "psr/http-factory": "^1.1",
        "psr/http-message": "^2.0"
    }
}
```
