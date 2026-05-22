---
name: acc-create-psr18-http-client
description: Generates PSR-18 HTTP Client implementation for PHP 8.5. Creates ClientInterface with request sending and exception handling. Includes unit tests.
---

# PSR-18 HTTP Client Generator

## Overview

Generates PSR-18 compliant HTTP client implementations for external API communication.

## When to Use

- External API integrations
- Microservice communication
- HTTP-based service calls
- Building HTTP client wrappers

## Template: HTTP Client

```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Http\Client;

use Psr\Http\Client\ClientInterface;
use Psr\Http\Message\RequestInterface;
use Psr\Http\Message\ResponseInterface;

final readonly class CurlHttpClient implements ClientInterface
{
    public function __construct(
        private array $options = [],
    ) {
    }

    public function sendRequest(RequestInterface $request): ResponseInterface
    {
        $ch = curl_init();

        try {
            $this->configureCurl($ch, $request);
            $response = curl_exec($ch);

            if ($response === false) {
                throw new NetworkException(
                    $request,
                    curl_error($ch),
                    curl_errno($ch),
                );
            }

            $headerSize = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
            $statusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

            $headerString = substr($response, 0, $headerSize);
            $body = substr($response, $headerSize);

            return $this->buildResponse($statusCode, $headerString, $body);
        } finally {
            curl_close($ch);
        }
    }

    private function configureCurl($ch, RequestInterface $request): void
    {
        $options = [
            CURLOPT_URL => (string) $request->getUri(),
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_HEADER => true,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_MAXREDIRS => 5,
            CURLOPT_TIMEOUT => $this->options['timeout'] ?? 30,
            CURLOPT_CONNECTTIMEOUT => $this->options['connect_timeout'] ?? 10,
            CURLOPT_CUSTOMREQUEST => $request->getMethod(),
        ];

        // Set headers
        $headers = [];
        foreach ($request->getHeaders() as $name => $values) {
            $headers[] = $name . ': ' . implode(', ', $values);
        }
        $options[CURLOPT_HTTPHEADER] = $headers;

        // Set body
        $body = (string) $request->getBody();
        if ($body !== '') {
            $options[CURLOPT_POSTFIELDS] = $body;
        }

        // SSL options
        if (isset($this->options['verify_ssl']) && !$this->options['verify_ssl']) {
            $options[CURLOPT_SSL_VERIFYPEER] = false;
            $options[CURLOPT_SSL_VERIFYHOST] = 0;
        }

        curl_setopt_array($ch, $options);
    }

    private function buildResponse(int $statusCode, string $headerString, string $body): ResponseInterface
    {
        $headers = $this->parseHeaders($headerString);

        return (new Response($statusCode))
            ->withBody(new Stream($body))
            ->withHeaders($headers);
    }

    private function parseHeaders(string $headerString): array
    {
        $headers = [];
        $lines = explode("\r\n", trim($headerString));

        foreach ($lines as $line) {
            if (str_contains($line, ':')) {
                [$name, $value] = explode(':', $line, 2);
                $headers[trim($name)] = [trim($value)];
            }
        }

        return $headers;
    }
}
```

## Template: Exceptions

```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Http\Client;

use Psr\Http\Client\ClientExceptionInterface;
use Psr\Http\Client\NetworkExceptionInterface;
use Psr\Http\Client\RequestExceptionInterface;
use Psr\Http\Message\RequestInterface;

final class ClientException extends \RuntimeException implements ClientExceptionInterface
{
}

final class NetworkException extends \RuntimeException implements NetworkExceptionInterface
{
    public function __construct(
        private readonly RequestInterface $request,
        string $message = '',
        int $code = 0,
        ?\Throwable $previous = null,
    ) {
        parent::__construct($message, $code, $previous);
    }

    public function getRequest(): RequestInterface
    {
        return $this->request;
    }
}

final class RequestException extends \RuntimeException implements RequestExceptionInterface
{
    public function __construct(
        private readonly RequestInterface $request,
        string $message = '',
        int $code = 0,
        ?\Throwable $previous = null,
    ) {
        parent::__construct($message, $code, $previous);
    }

    public function getRequest(): RequestInterface
    {
        return $this->request;
    }
}
```

## Template: Logging Client Decorator

```php
<?php

declare(strict_types=1);

namespace App\Infrastructure\Http\Client;

use Psr\Http\Client\ClientInterface;
use Psr\Http\Message\RequestInterface;
use Psr\Http\Message\ResponseInterface;
use Psr\Log\LoggerInterface;

final readonly class LoggingHttpClient implements ClientInterface
{
    public function __construct(
        private ClientInterface $client,
        private LoggerInterface $logger,
    ) {
    }

    public function sendRequest(RequestInterface $request): ResponseInterface
    {
        $context = [
            'method' => $request->getMethod(),
            'uri' => (string) $request->getUri(),
        ];

        $this->logger->info('HTTP request starting', $context);

        $startTime = microtime(true);

        try {
            $response = $this->client->sendRequest($request);
            $duration = microtime(true) - $startTime;

            $this->logger->info('HTTP request completed', [
                ...$context,
                'status' => $response->getStatusCode(),
                'duration_ms' => round($duration * 1000, 2),
            ]);

            return $response;
        } catch (\Throwable $e) {
            $this->logger->error('HTTP request failed', [
                ...$context,
                'error' => $e->getMessage(),
            ]);

            throw $e;
        }
    }
}
```

## Usage Example

```php
<?php

use App\Infrastructure\Http\Client\CurlHttpClient;
use App\Infrastructure\Http\Client\LoggingHttpClient;
use App\Infrastructure\Http\Factory\HttpFactory;

$factory = new HttpFactory();
$client = new LoggingHttpClient(
    new CurlHttpClient(['timeout' => 30]),
    $logger,
);

// Send GET request
$request = $factory->createRequest('GET', 'https://api.example.com/users')
    ->withHeader('Authorization', 'Bearer token');

$response = $client->sendRequest($request);
$data = json_decode((string) $response->getBody(), true);

// Send POST request
$request = $factory->createRequest('POST', 'https://api.example.com/users')
    ->withHeader('Content-Type', 'application/json')
    ->withBody($factory->createStream(json_encode(['name' => 'John'])));

$response = $client->sendRequest($request);
```

## Requirements

```json
{
    "require": {
        "psr/http-client": "^1.0",
        "psr/http-message": "^2.0"
    }
}
```
