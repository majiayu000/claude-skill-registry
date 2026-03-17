---
name: aws-lambda-php-integration
description: Provides AWS Lambda integration patterns for PHP with Symfony using the Bref framework. Use when deploying PHP/Symfony applications to AWS Lambda, optimizing cold starts, configuring API Gateway integration, or implementing serverless PHP applications with Bref. Triggers include "create lambda php", "deploy symfony lambda", "bref lambda aws", "php lambda cold start", "aws lambda php performance", "symfony serverless", "php serverless framework".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# AWS Lambda PHP Integration

Patterns for deploying PHP and Symfony applications on AWS Lambda using the Bref framework.

## Overview

This skill provides complete patterns for AWS Lambda PHP development with two main approaches:

1. **Bref Framework** - The standard solution for PHP on Lambda with Symfony support, built-in routing, and cold start optimization
2. **Raw PHP** - Minimal overhead approach with maximum control

Both approaches support API Gateway integration with production-ready configurations.

## When to Use

Use this skill when:
- Creating new Lambda functions in PHP
- Migrating existing Symfony applications to Lambda
- Optimizing cold start performance for PHP Lambda
- Choosing between Bref-based and minimal PHP approaches
- Configuring API Gateway integration
- Setting up deployment pipelines for PHP Lambda

## Instructions

### 1. Choose Your Approach

| Approach | Cold Start | Best For | Complexity |
|----------|------------|----------|------------|
| Bref | < 2s | Symfony apps, full-featured APIs | Medium |
| Raw PHP | < 500ms | Simple handlers, maximum control | Low |

### 2. Project Structure

#### Symfony with Bref Structure
```
my-symfony-lambda/
├── composer.json
├── serverless.yml
├── public/
│   └── index.php         # Lambda entry point
├── src/
│   └── Kernel.php        # Symfony Kernel
├── config/
│   ├── bundles.php
│   ├── routes.yaml
│   └── services.yaml
└── templates/
```

#### Raw PHP Structure
```
my-lambda-function/
├── public/
│   └── index.php         # Handler entry point
├── composer.json
├── serverless.yml
└── src/
    └── Services/
```

### 3. Implementation Examples

**Symfony with Bref:**
```php
// public/index.php
use Bref\Symfony\Bref;
use App\Kernel;
use Symfony\Component\HttpFoundation\Request;

require __DIR__.'/../vendor/autoload.php';

$kernel = new Kernel($_SERVER['APP_ENV'] ?? 'dev', $_SERVER['APP_DEBUG'] ?? true);
$kernel->boot();

$bref = new Bref($kernel);
return $bref->run($event, $context);
```

**Raw PHP Handler:**
```php
// public/index.php
use function Bref\Lambda\main;

main(function ($event) {
    $path = $event['path'] ?? '/';
    $method = $event['httpMethod'] ?? 'GET';

    return [
        'statusCode' => 200,
        'body' => json_encode(['message' => 'Hello from PHP Lambda!'])
    ];
});
```

## Core Concepts

### Cold Start Optimization

PHP cold start depends on framework initialization. Key strategies:

1. **Lazy loading** - Defer heavy services until needed
2. **Disable unused Symfony features** - Turn off validation, annotations, etc.
3. **Optimize composer autoload** - Use classmap for production
4. **Use Bref optimized runtime** - Leverage PHP 8.x optimizations

### Connection Management

```php
// Cache AWS clients at function level
use Aws\DynamoDb\DynamoDbClient;

class DatabaseService
{
    private static ?DynamoDbClient $client = null;

    public static function getClient(): DynamoDbClient
    {
        if (self::$client === null) {
            self::$client = new DynamoDbClient([
                'region' => getenv('AWS_REGION'),
                'version' => 'latest'
            ]);
        }
        return self::$client;
    }
}
```

### Environment Configuration

```php
// config/services.yaml
parameters:
    env(DATABASE_URL): null
    env(APP_ENV): 'dev'

services:
    App\Service\Configuration:
        arguments:
            $tableName: '%env(DATABASE_URL)%'
```

## Best Practices

### Memory and Timeout Configuration

- **Memory**: Start with 512MB for Symfony, 256MB for raw PHP
- **Timeout**: Set based on expected processing time
  - Symfony: 10-30 seconds for cold start buffer
  - Raw PHP: 3-10 seconds typically sufficient

### Dependencies

Keep `composer.json` minimal:

```json
{
    "require": {
        "php": "^8.2",
        "bref/bref": "^2.0",
        "symfony/framework-bundle": "^6.0"
    },
    "config": {
        "optimize-autoloader": true,
        "preferred-install": "dist"
    }
}
```

### Error Handling

Return proper Lambda responses:

```php
try {
    $result = processRequest($event);
    return [
        'statusCode' => 200,
        'body' => json_encode($result)
    ];
} catch (ValidationException $e) {
    return [
        'statusCode' => 400,
        'body' => json_encode(['error' => $e->getMessage()])
    ];
} catch (Exception $e) {
    error_log($e->getMessage());
    return [
        'statusCode' => 500,
        'body' => json_encode(['error' => 'Internal error'])
    ];
}
```

### Logging

Use structured logging:

```php
error_log(json_encode([
    'level' => 'info',
    'message' => 'Request processed',
    'request_id' => $context->getAwsRequestId(),
    'path' => $event['path'] ?? '/'
]));
```

## Deployment Options

### Quick Start

**Serverless Framework:**
```yaml
# serverless.yml
service: symfony-lambda-api

provider:
  name: aws
  runtime: php-82
  memorySize: 512
  timeout: 20

package:
  individually: true
  exclude:
    - '**/node_modules/**'
    - '**/.git/**'

functions:
  api:
    handler: public/index.php
    events:
      - http:
          path: /{proxy+}
          method: ANY
      - http:
          path: /
          method: ANY
```

**Deploy with Bref:**
```bash
composer require bref/bref --dev
vendor/bin/bref deploy
```

### Symfony Full Configuration

```yaml
# serverless.yml for Symfony
service: symfony-lambda-api

provider:
  name: aws
  runtime: php-82
  stage: ${self:custom.stage}
  region: ${self:custom.region}
  environment:
    APP_ENV: ${self:custom.stage}
    APP_DEBUG: ${self:custom.isLocal}
  iam:
    role:
      statements:
        - Effect: Allow
          Action:
            - dynamodb:GetItem
            - dynamodb:PutItem
          Resource: '*'

functions:
  web:
    handler: public/index.php
    timeout: 30
    memorySize: 1024
    events:
      - http:
          path: /{proxy+}
          method: ANY

  console:
    handler: bin/console
    timeout: 300
    events:
      - schedule: rate(1 day)

plugins:
  - ./vendor/bref/bref

custom:
  stage: dev
  region: us-east-1
  isLocal: false
```

## Constraints and Warnings

### Lambda Limits

- **Deployment package**: 250MB unzipped maximum (50MB zipped)
- **Memory**: 128MB to 10GB
- **Timeout**: 29 seconds (API Gateway), 15 minutes for async
- **Concurrent executions**: 1000 default

### PHP-Specific Considerations

- **Cold start**: PHP has moderate cold start; use Bref for optimized runtimes
- **Dependencies**: Keep composer.json minimal; use Lambda Layers for shared deps
- **PHP version**: Use PHP 8.2+ for best Lambda performance
- **No local storage**: Lambda containers are ephemeral; use S3/DynamoDB for persistence

### Common Pitfalls

1. **Large vendor folder** - Exclude dev dependencies; use --no-dev
2. **Session storage** - Don't use local file storage; use DynamoDB
3. **Long-running processes** - Not suitable for Lambda; use ECS instead
4. **Websockets** - Use API Gateway WebSockets or AppSync instead

### Security Considerations

- Never hardcode credentials; use IAM roles and SSM Parameter Store
- Validate all input data
- Use least privilege IAM policies
- Enable CloudTrail for audit logging
- Set proper CORS headers

## References

For detailed guidance on specific topics:

- **[Bref Lambda](references/bref-lambda.md)** - Complete Bref setup, Symfony integration, routing
- **[Raw PHP Lambda](references/raw-php-lambda.md)** - Minimal handler patterns, caching, packaging
- **[Serverless Deployment](references/serverless-deployment.md)** - Serverless Framework, SAM, CI/CD pipelines
- **[Testing Lambda](references/testing-lambda.md)** - PHPUnit, SAM Local, integration testing

## Examples

### Example 1: Create a Symfony Lambda API

**Input:**
```
Create a Symfony Lambda REST API using Bref for a todo application
```

**Process:**
1. Initialize Symfony project with `composer create-project`
2. Install Bref: `composer require bref/bref`
3. Configure serverless.yml
4. Set up routes in config/routes.yaml
5. Configure deployment with `vendor/bin/bref deploy`

**Output:**
- Complete Symfony project structure
- REST API with CRUD endpoints
- DynamoDB integration
- Deployment configuration

### Example 2: Optimize Cold Start for Symfony

**Input:**
```
My Symfony Lambda has 5 second cold start, how do I optimize it?
```

**Process:**
1. Analyze services loaded at startup
2. Disable unused Symfony features (validation, annotations)
3. Use lazy loading for heavy services
4. Optimize composer autoload
5. Consider using raw PHP if full framework not needed

**Output:**
- Refactored Symfony configuration
- Optimized cold start < 2s
- Service analysis report

### Example 3: Deploy with GitHub Actions

**Input:**
```
Configure CI/CD for Symfony Lambda with Serverless Framework
```

**Process:**
1. Create GitHub Actions workflow
2. Set up PHP environment with composer
3. Run PHPUnit tests
4. Deploy with Serverless Framework
5. Configure environment protection for prod

**Output:**
- Complete .github/workflows/deploy.yml
- Multi-stage pipeline
- Integrated test automation

## Version

Version: 1.0.0
