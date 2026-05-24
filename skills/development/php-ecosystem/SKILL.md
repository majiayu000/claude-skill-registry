---
name: PHP Ecosystem
description: This skill should be used when the user asks to "write php", "php 8", "composer", "phpunit", "pest", "phpstan", "psalm", "psr", or works with modern PHP language patterns and configuration. Provides comprehensive modern PHP ecosystem patterns and best practices.
---

<purpose>
  Provide comprehensive patterns for modern PHP (8.1+) language features, PSR standards, testing, static analysis, and package development in a framework-agnostic approach.
</purpose>

<php_version>
  <version_mapping>
    <description>PHP version-specific feature availability</description>
    <version php="8.3" released="2023-11">
      <feature>Typed class constants</feature>
      <feature>json_validate() function</feature>
      <feature>Randomizer::getFloat() and nextFloat()</feature>
      <feature>Deep cloning of readonly properties</feature>
      <feature>Override attribute</feature>
      <feature>Granular DateTime exceptions</feature>
    </version>
    <version php="8.2" released="2022-12">
      <feature>Readonly classes</feature>
      <feature>DNF types (Disjunctive Normal Form)</feature>
      <feature>null, false, true as standalone types</feature>
      <feature>Constants in traits</feature>
      <feature>Deprecate dynamic properties</feature>
    </version>
    <version php="8.1" released="2021-11">
      <feature>Enums (backed and unit)</feature>
      <feature>Readonly properties</feature>
      <feature>Fibers</feature>
      <feature>Intersection types</feature>
      <feature>never return type</feature>
      <feature>First-class callable syntax</feature>
      <feature>New in initializers</feature>
    </version>
    <version php="8.0" released="2020-11">
      <feature>Named arguments</feature>
      <feature>Attributes</feature>
      <feature>Constructor property promotion</feature>
      <feature>Union types</feature>
      <feature>Match expression</feature>
      <feature>Nullsafe operator</feature>
      <feature>mixed type</feature>
    </version>
  </version_mapping>

  <recommended_config>
    <description>php.ini recommended settings for development</description>
    <config>
      error_reporting = E_ALL
      display_errors = On
      log_errors = On
      opcache.enable = 1
      opcache.validate_timestamps = 1
    </config>
  </recommended_config>
</php_version>

<type_system>
  <union_types>
    <pattern name="basic">
      <description>Multiple types for parameter or return</description>
      <example>
        function process(string|int $value): string|null
        {
            return is_string($value) ? $value : (string) $value;
        }
      </example>
    </pattern>
  </union_types>

  <intersection_types>
    <pattern name="basic">
      <description>Value must satisfy all types (PHP 8.1+)</description>
      <example>
        function process(Countable&amp;Iterator $collection): int
        {
            return count($collection);
        }
      </example>
    </pattern>
  </intersection_types>

  <dnf_types>
    <pattern name="disjunctive-normal-form">
      <description>Combine union and intersection types (PHP 8.2+)</description>
      <example>
        function handle((Countable&amp;Iterator)|null $items): void
        {
            if ($items === null) {
                return;
            }
            foreach ($items as $item) {
                // process
            }
        }
      </example>
    </pattern>
  </dnf_types>

  <enums>
    <pattern name="backed-enum">
      <description>Enum with scalar backing (PHP 8.1+)</description>
      <example>
        enum Status: string
        {
            case Draft = 'draft';
            case Published = 'published';
            case Archived = 'archived';

            public function label(): string
            {
                return match($this) {
                    self::Draft =&gt; 'Draft',
                    self::Published =&gt; 'Published',
                    self::Archived =&gt; 'Archived',
                };
            }
        }

        // Usage
        $status = Status::from('published');
        $value = $status-&gt;value; // 'published'
      </example>
    </pattern>

    <pattern name="unit-enum">
      <description>Enum without backing value</description>
      <example>
        enum Suit
        {
            case Hearts;
            case Diamonds;
            case Clubs;
            case Spades;

            public function color(): string
            {
                return match($this) {
                    self::Hearts, self::Diamonds =&gt; 'red',
                    self::Clubs, self::Spades =&gt; 'black',
                };
            }
        }
      </example>
    </pattern>
  </enums>

  <readonly>
    <pattern name="readonly-property">
      <description>Immutable property (PHP 8.1+)</description>
      <example>
        class User
        {
            public function __construct(
                public readonly string $id,
                public readonly string $email,
            ) {}
        }
      </example>
    </pattern>

    <pattern name="readonly-class">
      <description>All properties become readonly (PHP 8.2+)</description>
      <example>
        readonly class ValueObject
        {
            public function __construct(
                public string $name,
                public int $value,
            ) {}
        }
      </example>
    </pattern>
  </readonly>

  <attributes>
    <pattern name="custom-attribute">
      <description>Define and use custom attributes (PHP 8.0+)</description>
      <example>
        #[Attribute(Attribute::TARGET_METHOD | Attribute::TARGET_FUNCTION)]
        class Route
        {
            public function __construct(
                public string $path,
                public string $method = 'GET',
            ) {}
        }

        class UserController
        {
            #[Route('/users', 'GET')]
            public function index(): array
            {
                return [];
            }
        }

        // Reading attributes via reflection
        $method = new ReflectionMethod(UserController::class, 'index');
        $attributes = $method-&gt;getAttributes(Route::class);
        foreach ($attributes as $attribute) {
            $route = $attribute-&gt;newInstance();
            echo $route-&gt;path; // '/users'
        }
      </example>
    </pattern>
  </attributes>

  <constructor_promotion>
    <pattern name="basic">
      <description>Declare and assign properties in constructor (PHP 8.0+)</description>
      <example>
        class Product
        {
            public function __construct(
                private string $name,
                private float $price,
                private int $quantity = 0,
            ) {}

            public function getName(): string
            {
                return $this-&gt;name;
            }
        }
      </example>
    </pattern>
  </constructor_promotion>

  <named_arguments>
    <pattern name="basic">
      <description>Pass arguments by name (PHP 8.0+)</description>
      <example>
        function createUser(
            string $name,
            string $email,
            bool $active = true,
            ?string $role = null,
        ): User {
            // ...
        }

        // Usage with named arguments
        $user = createUser(
            email: 'user@example.com',
            name: 'John Doe',
            role: 'admin',
        );
      </example>
      <decision_tree name="when_to_use">
        <question>Are you skipping optional parameters or improving readability?</question>
        <if_yes>Use named arguments</if_yes>
        <if_no>Use positional arguments for simple calls</if_no>
      </decision_tree>
    </pattern>
  </named_arguments>

  <typed_class_constants>
    <pattern name="basic">
      <description>Type declarations for class constants (PHP 8.3+)</description>
      <example>
        class Config
        {
            public const string VERSION = '1.0.0';
            public const int MAX_RETRIES = 3;
            public const array ALLOWED_METHODS = ['GET', 'POST', 'PUT', 'DELETE'];
        }
      </example>
    </pattern>
  </typed_class_constants>
</type_system>

<psr_standards>
  <psr name="PSR-1" title="Basic Coding Standard">
    <description>Basic coding standards for PHP files</description>
    <rules>
      <rule>Files MUST use only &lt;?php and &lt;?= tags</rule>
      <rule>Files MUST use only UTF-8 without BOM</rule>
      <rule>Class names MUST be declared in StudlyCaps</rule>
      <rule>Class constants MUST be declared in UPPER_CASE</rule>
      <rule>Method names MUST be declared in camelCase</rule>
    </rules>
  </psr>

  <psr name="PSR-4" title="Autoloading Standard">
    <description>Autoloading classes from file paths</description>
    <example>
      // composer.json
      {
          "autoload": {
              "psr-4": {
                  "App\\": "src/",
                  "App\\Tests\\": "tests/"
              }
          }
      }

      // File: src/Domain/User/Entity/User.php
      namespace App\Domain\User\Entity;

      class User
      {
          // Fully qualified: App\Domain\User\Entity\User
      }
    </example>
  </psr>

  <psr name="PSR-3" title="Logger Interface">
    <description>Common interface for logging libraries</description>
    <example>
      use Psr\Log\LoggerInterface;
      use Psr\Log\LogLevel;

      class UserService
      {
          public function __construct(
              private LoggerInterface $logger,
          ) {}

          public function create(array $data): User
          {
              $this-&gt;logger-&gt;info('Creating user', ['email' =&gt; $data['email']]);

              try {
                  $user = new User($data);
                  $this-&gt;logger-&gt;debug('User created', ['id' =&gt; $user-&gt;getId()]);
                  return $user;
              } catch (\Exception $e) {
                  $this-&gt;logger-&gt;error('Failed to create user', [
                      'exception' =&gt; $e,
                      'data' =&gt; $data,
                  ]);
                  throw $e;
              }
          }
      }
    </example>
  </psr>

  <psr name="PSR-7" title="HTTP Message Interface">
    <description>Common interfaces for HTTP messages</description>
    <example>
      use Psr\Http\Message\ServerRequestInterface;
      use Psr\Http\Message\ResponseInterface;

      function handleRequest(ServerRequestInterface $request): ResponseInterface
      {
          $method = $request-&gt;getMethod();
          $uri = $request-&gt;getUri();
          $body = $request-&gt;getParsedBody();
          $query = $request-&gt;getQueryParams();

          // PSR-7 messages are immutable
          $response = new Response();
          return $response
              -&gt;withStatus(200)
              -&gt;withHeader('Content-Type', 'application/json');
      }
    </example>
  </psr>

  <psr name="PSR-11" title="Container Interface">
    <description>Common interface for dependency injection containers</description>
    <example>
      use Psr\Container\ContainerInterface;

      class ServiceLocator
      {
          public function __construct(
              private ContainerInterface $container,
          ) {}

          public function getUserService(): UserService
          {
              return $this-&gt;container-&gt;get(UserService::class);
          }
      }
    </example>
  </psr>

  <psr name="PSR-12" title="Extended Coding Style">
    <description>Extends PSR-1 with detailed formatting rules</description>
    <rules>
      <rule>Code MUST follow PSR-1</rule>
      <rule>Code MUST use 4 spaces for indenting</rule>
      <rule>Lines SHOULD be 80 characters or less</rule>
      <rule>There MUST be one blank line after namespace declaration</rule>
      <rule>Opening braces for classes MUST go on next line</rule>
      <rule>Opening braces for methods MUST go on next line</rule>
      <rule>Visibility MUST be declared on all properties and methods</rule>
    </rules>
  </psr>

  <psr name="PSR-15" title="HTTP Server Request Handlers">
    <description>Interfaces for HTTP server request handlers and middleware</description>
    <example>
      use Psr\Http\Message\ResponseInterface;
      use Psr\Http\Message\ServerRequestInterface;
      use Psr\Http\Server\RequestHandlerInterface;
      use Psr\Http\Server\MiddlewareInterface;

      class AuthMiddleware implements MiddlewareInterface
      {
          public function process(
              ServerRequestInterface $request,
              RequestHandlerInterface $handler
          ): ResponseInterface {
              $token = $request-&gt;getHeaderLine('Authorization');

              if (!$this-&gt;validateToken($token)) {
                  return new Response(401);
              }

              return $handler-&gt;handle($request);
          }
      }
    </example>
  </psr>

  <psr name="PSR-17" title="HTTP Factories">
    <description>Factory interfaces for creating PSR-7 objects</description>
    <example>
      use Psr\Http\Message\ResponseFactoryInterface;
      use Psr\Http\Message\StreamFactoryInterface;

      class JsonResponder
      {
          public function __construct(
              private ResponseFactoryInterface $responseFactory,
              private StreamFactoryInterface $streamFactory,
          ) {}

          public function respond(array $data, int $status = 200): ResponseInterface
          {
              $json = json_encode($data, JSON_THROW_ON_ERROR);
              $body = $this-&gt;streamFactory-&gt;createStream($json);

              return $this-&gt;responseFactory-&gt;createResponse($status)
                  -&gt;withHeader('Content-Type', 'application/json')
                  -&gt;withBody($body);
          }
      }
    </example>
  </psr>

  <psr name="PSR-18" title="HTTP Client">
    <description>Common interface for HTTP clients</description>
    <example>
      use Psr\Http\Client\ClientInterface;
      use Psr\Http\Message\RequestFactoryInterface;

      class ApiClient
      {
          public function __construct(
              private ClientInterface $httpClient,
              private RequestFactoryInterface $requestFactory,
          ) {}

          public function get(string $url): array
          {
              $request = $this-&gt;requestFactory-&gt;createRequest('GET', $url);
              $response = $this-&gt;httpClient-&gt;sendRequest($request);

              return json_decode(
                  $response-&gt;getBody()-&gt;getContents(),
                  true,
                  512,
                  JSON_THROW_ON_ERROR
              );
          }
      }
    </example>
  </psr>
</psr_standards>

<design_patterns>
  <pattern name="value-object">
    <description>Immutable objects representing a value</description>
    <example>
      readonly class Money
      {
          public function __construct(
              public int $amount,
              public string $currency,
          ) {
              if ($amount &lt; 0) {
                  throw new InvalidArgumentException('Amount cannot be negative');
              }
          }

          public function add(Money $other): self
          {
              if ($this-&gt;currency !== $other-&gt;currency) {
                  throw new InvalidArgumentException('Currency mismatch');
              }
              return new self($this-&gt;amount + $other-&gt;amount, $this-&gt;currency);
          }

          public function equals(Money $other): bool
          {
              return $this-&gt;amount === $other-&gt;amount
                  &amp;&amp; $this-&gt;currency === $other-&gt;currency;
          }
      }
    </example>
  </pattern>

  <pattern name="repository">
    <description>Abstract data persistence behind an interface</description>
    <example>
      interface UserRepositoryInterface
      {
          public function find(UserId $id): ?User;
          public function findByEmail(Email $email): ?User;
          public function save(User $user): void;
          public function remove(User $user): void;
      }

      class PdoUserRepository implements UserRepositoryInterface
      {
          public function __construct(
              private PDO $pdo,
          ) {}

          public function find(UserId $id): ?User
          {
              $stmt = $this-&gt;pdo-&gt;prepare(
                  'SELECT * FROM users WHERE id = :id'
              );
              $stmt-&gt;execute(['id' =&gt; $id-&gt;toString()]);
              $row = $stmt-&gt;fetch(PDO::FETCH_ASSOC);

              return $row ? $this-&gt;hydrate($row) : null;
          }

          public function save(User $user): void
          {
              $stmt = $this-&gt;pdo-&gt;prepare(
                  'INSERT INTO users (id, email, name)
                   VALUES (:id, :email, :name)
                   ON DUPLICATE KEY UPDATE email = :email, name = :name'
              );
              $stmt-&gt;execute([
                  'id' =&gt; $user-&gt;getId()-&gt;toString(),
                  'email' =&gt; $user-&gt;getEmail()-&gt;toString(),
                  'name' =&gt; $user-&gt;getName(),
              ]);
          }
      }
    </example>
    <decision_tree name="when_to_use">
      <question>Do you need to abstract persistence details from domain logic?</question>
      <if_yes>Use Repository pattern</if_yes>
      <if_no>Direct database access may be sufficient for simple CRUD</if_no>
    </decision_tree>
  </pattern>

  <pattern name="service-layer">
    <description>Coordinate use cases and transactions</description>
    <example>
      class CreateUserHandler
      {
          public function __construct(
              private UserRepositoryInterface $userRepository,
              private PasswordHasherInterface $passwordHasher,
              private EventDispatcherInterface $eventDispatcher,
          ) {}

          public function handle(CreateUserCommand $command): UserId
          {
              $email = new Email($command-&gt;email);

              if ($this-&gt;userRepository-&gt;findByEmail($email) !== null) {
                  throw new UserAlreadyExistsException($email);
              }

              $user = User::create(
                  UserId::generate(),
                  $email,
                  $command-&gt;name,
                  $this-&gt;passwordHasher-&gt;hash($command-&gt;password),
              );

              $this-&gt;userRepository-&gt;save($user);
              $this-&gt;eventDispatcher-&gt;dispatch(new UserCreatedEvent($user));

              return $user-&gt;getId();
          }
      }
    </example>
  </pattern>

  <pattern name="dependency-injection">
    <description>Inject dependencies through constructor</description>
    <example>
      // Interface for abstraction
      interface CacheInterface
      {
          public function get(string $key): mixed;
          public function set(string $key, mixed $value, int $ttl = 3600): void;
      }

      // Concrete implementation
      class RedisCache implements CacheInterface
      {
          public function __construct(
              private \Redis $redis,
          ) {}

          public function get(string $key): mixed
          {
              $value = $this-&gt;redis-&gt;get($key);
              return $value !== false ? unserialize($value) : null;
          }

          public function set(string $key, mixed $value, int $ttl = 3600): void
          {
              $this-&gt;redis-&gt;setex($key, $ttl, serialize($value));
          }
      }

      // Service depending on abstraction
      class ProductService
      {
          public function __construct(
              private ProductRepositoryInterface $repository,
              private CacheInterface $cache,
          ) {}
      }
    </example>
  </pattern>
</design_patterns>

<composer>
  <package_management>
    <pattern name="require">
      <description>Add production dependencies</description>
      <example>
        composer require psr/log
        composer require guzzlehttp/guzzle
        composer require symfony/http-foundation
      </example>
    </pattern>

    <pattern name="require-dev">
      <description>Add development dependencies</description>
      <example>
        composer require --dev phpunit/phpunit
        composer require --dev phpstan/phpstan
        composer require --dev friendsofphp/php-cs-fixer
      </example>
    </pattern>

    <pattern name="version-constraints">
      <description>Specify version requirements</description>
      <example>
        {
            "require": {
                "php": "^8.2",
                "psr/log": "^3.0",
                "guzzlehttp/guzzle": "^7.0"
            },
            "require-dev": {
                "phpunit/phpunit": "^10.0 || ^11.0",
                "phpstan/phpstan": "^1.10"
            }
        }
      </example>
      <note>^ allows minor version updates, ~ allows patch updates only</note>
    </pattern>
  </package_management>

  <package_development>
    <pattern name="library-structure">
      <description>Standard library package structure</description>
      <example>
        my-package/
        ├── src/
        │   └── MyClass.php
        ├── tests/
        │   └── MyClassTest.php
        ├── composer.json
        ├── phpunit.xml.dist
        ├── phpstan.neon
        ├── .php-cs-fixer.dist.php
        ├── LICENSE
        └── README.md
      </example>
    </pattern>

    <pattern name="composer-json">
      <description>Complete composer.json for library</description>
      <example>
        {
            "name": "vendor/my-package",
            "description": "My awesome PHP package",
            "type": "library",
            "license": "MIT",
            "authors": [
                {
                    "name": "Your Name",
                    "email": "you@example.com"
                }
            ],
            "require": {
                "php": "^8.2"
            },
            "require-dev": {
                "phpunit/phpunit": "^11.0",
                "phpstan/phpstan": "^1.10"
            },
            "autoload": {
                "psr-4": {
                    "Vendor\\MyPackage\\": "src/"
                }
            },
            "autoload-dev": {
                "psr-4": {
                    "Vendor\\MyPackage\\Tests\\": "tests/"
                }
            },
            "scripts": {
                "test": "phpunit",
                "analyse": "phpstan analyse",
                "cs-fix": "php-cs-fixer fix"
            },
            "config": {
                "sort-packages": true
            }
        }
      </example>
    </pattern>

    <pattern name="scripts">
      <description>Automate common tasks with Composer scripts</description>
      <example>
        {
            "scripts": {
                "test": "phpunit --colors=always",
                "test:coverage": "phpunit --coverage-html coverage",
                "analyse": "phpstan analyse --memory-limit=512M",
                "cs-check": "php-cs-fixer fix --dry-run --diff",
                "cs-fix": "php-cs-fixer fix",
                "ci": [
                    "@cs-check",
                    "@analyse",
                    "@test"
                ]
            }
        }
      </example>
    </pattern>
  </package_development>
</composer>

<testing>
  <phpunit>
    <pattern name="test-case">
      <description>Basic PHPUnit test structure</description>
      <example>
        use PHPUnit\Framework\TestCase;
        use PHPUnit\Framework\Attributes\Test;
        use PHPUnit\Framework\Attributes\DataProvider;

        class CalculatorTest extends TestCase
        {
            private Calculator $calculator;

            protected function setUp(): void
            {
                $this-&gt;calculator = new Calculator();
            }

            #[Test]
            public function itAddsNumbers(): void
            {
                $result = $this-&gt;calculator-&gt;add(2, 3);

                $this-&gt;assertSame(5, $result);
            }

            #[Test]
            #[DataProvider('additionProvider')]
            public function itAddsVariousNumbers(int $a, int $b, int $expected): void
            {
                $this-&gt;assertSame($expected, $this-&gt;calculator-&gt;add($a, $b));
            }

            public static function additionProvider(): array
            {
                return [
                    'positive numbers' =&gt; [1, 2, 3],
                    'negative numbers' =&gt; [-1, -2, -3],
                    'mixed numbers' =&gt; [-1, 2, 1],
                    'zeros' =&gt; [0, 0, 0],
                ];
            }
        }
      </example>
    </pattern>

    <pattern name="mocking">
      <description>Create test doubles with PHPUnit</description>
      <example>
        use PHPUnit\Framework\TestCase;

        class UserServiceTest extends TestCase
        {
            #[Test]
            public function itCreatesUser(): void
            {
                // Arrange
                $repository = $this-&gt;createMock(UserRepositoryInterface::class);
                $repository
                    -&gt;expects($this-&gt;once())
                    -&gt;method('save')
                    -&gt;with($this-&gt;isInstanceOf(User::class));

                $hasher = $this-&gt;createMock(PasswordHasherInterface::class);
                $hasher
                    -&gt;method('hash')
                    -&gt;willReturn('hashed_password');

                $service = new UserService($repository, $hasher);

                // Act
                $userId = $service-&gt;create('test@example.com', 'password');

                // Assert
                $this-&gt;assertInstanceOf(UserId::class, $userId);
            }
        }
      </example>
    </pattern>

    <pattern name="config">
      <description>PHPUnit configuration file</description>
      <example>
        &lt;!-- phpunit.xml.dist --&gt;
        &lt;?xml version="1.0" encoding="UTF-8"?&gt;
        &lt;phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
                 bootstrap="vendor/autoload.php"
                 colors="true"
                 cacheDirectory=".phpunit.cache"&gt;
            &lt;testsuites&gt;
                &lt;testsuite name="Unit"&gt;
                    &lt;directory&gt;tests/Unit&lt;/directory&gt;
                &lt;/testsuite&gt;
                &lt;testsuite name="Integration"&gt;
                    &lt;directory&gt;tests/Integration&lt;/directory&gt;
                &lt;/testsuite&gt;
            &lt;/testsuites&gt;
            &lt;source&gt;
                &lt;include&gt;
                    &lt;directory&gt;src&lt;/directory&gt;
                &lt;/include&gt;
            &lt;/source&gt;
        &lt;/phpunit&gt;
      </example>
    </pattern>
  </phpunit>

  <pest>
    <pattern name="basic">
      <description>Pest PHP test syntax</description>
      <example>
        // tests/Unit/CalculatorTest.php
        use App\Calculator;

        beforeEach(function () {
            $this-&gt;calculator = new Calculator();
        });

        test('it adds numbers', function () {
            expect($this-&gt;calculator-&gt;add(2, 3))-&gt;toBe(5);
        });

        test('it subtracts numbers', function () {
            expect($this-&gt;calculator-&gt;subtract(5, 3))-&gt;toBe(2);
        });

        it('throws on division by zero', function () {
            $this-&gt;calculator-&gt;divide(10, 0);
        })-&gt;throws(DivisionByZeroError::class);
      </example>
    </pattern>

    <pattern name="datasets">
      <description>Pest datasets for parameterized tests</description>
      <example>
        dataset('addition', [
            'positive' =&gt; [1, 2, 3],
            'negative' =&gt; [-1, -2, -3],
            'mixed' =&gt; [-1, 2, 1],
        ]);

        test('it adds numbers correctly', function (int $a, int $b, int $expected) {
            expect($this-&gt;calculator-&gt;add($a, $b))-&gt;toBe($expected);
        })-&gt;with('addition');
      </example>
    </pattern>

    <pattern name="expectations">
      <description>Pest expectation API</description>
      <example>
        test('user properties', function () {
            $user = new User('john@example.com', 'John Doe');

            expect($user)
                -&gt;toBeInstanceOf(User::class)
                -&gt;email-&gt;toBe('john@example.com')
                -&gt;name-&gt;toBe('John Doe')
                -&gt;isActive()-&gt;toBeTrue();
        });
      </example>
    </pattern>
  </pest>
</testing>

<static_analysis>
  <phpstan>
    <pattern name="config">
      <description>PHPStan configuration</description>
      <example>
        # phpstan.neon
        parameters:
            level: 8
            paths:
                - src
                - tests
            excludePaths:
                - vendor
            checkMissingIterableValueType: true
            checkGenericClassInNonGenericObjectType: true
            reportUnmatchedIgnoredErrors: true
      </example>
    </pattern>

    <pattern name="levels">
      <description>PHPStan strictness levels (0-9)</description>
      <levels>
        <level number="0">Basic checks</level>
        <level number="1">Possibly undefined variables</level>
        <level number="2">Unknown methods on $this</level>
        <level number="3">Wrong return types</level>
        <level number="4">Dead code</level>
        <level number="5">Argument types</level>
        <level number="6">Missing type hints</level>
        <level number="7">Partial union types</level>
        <level number="8">No mixed types</level>
        <level number="9">Mixed type operations</level>
        <level number="10">Stricter implicit mixed (PHPStan 2.0+)</level>
      </levels>
      <note>Start at level 5-6 for existing projects, level 9-10 for new projects. Use --level max for highest available.</note>
    </pattern>

    <pattern name="generics">
      <description>Generic types with PHPStan annotations</description>
      <example>
        /**
         * @template T
         * @param class-string&lt;T&gt; $class
         * @return T
         */
        public function create(string $class): object
        {
            return new $class();
        }

        /**
         * @template T of object
         * @param T $entity
         * @return T
         */
        public function save(object $entity): object
        {
            // persist
            return $entity;
        }
      </example>
    </pattern>
  </phpstan>

  <psalm>
    <pattern name="config">
      <description>Psalm configuration</description>
      <example>
        &lt;!-- psalm.xml --&gt;
        &lt;?xml version="1.0"?&gt;
        &lt;psalm
            errorLevel="1"
            resolveFromConfigFile="true"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="https://getpsalm.org/schema/config"
            xsi:schemaLocation="https://getpsalm.org/schema/config vendor/vimeo/psalm/config.xsd"
        &gt;
            &lt;projectFiles&gt;
                &lt;directory name="src" /&gt;
                &lt;ignoreFiles&gt;
                    &lt;directory name="vendor" /&gt;
                &lt;/ignoreFiles&gt;
            &lt;/projectFiles&gt;
        &lt;/psalm&gt;
      </example>
    </pattern>

    <pattern name="annotations">
      <description>Psalm-specific annotations</description>
      <example>
        /**
         * @psalm-immutable
         */
        readonly class ImmutableValue
        {
            public function __construct(
                public string $value,
            ) {}
        }

        /**
         * @psalm-assert-if-true User $user
         */
        function isActiveUser(?User $user): bool
        {
            return $user !== null &amp;&amp; $user-&gt;isActive();
        }
      </example>
    </pattern>
  </psalm>

  <php_cs_fixer>
    <pattern name="config">
      <description>PHP CS Fixer configuration</description>
      <example>
        &lt;?php
        // .php-cs-fixer.dist.php
        $finder = PhpCsFixer\Finder::create()
            -&gt;in(__DIR__ . '/src')
            -&gt;in(__DIR__ . '/tests');

        return (new PhpCsFixer\Config())
            -&gt;setRules([
                '@PER-CS2.0' =&gt; true,
                '@PHP82Migration' =&gt; true,
                'strict_types' =&gt; true,
                'declare_strict_types' =&gt; true,
                'array_syntax' =&gt; ['syntax' =&gt; 'short'],
                'no_unused_imports' =&gt; true,
                'ordered_imports' =&gt; ['sort_algorithm' =&gt; 'alpha'],
                'trailing_comma_in_multiline' =&gt; true,
            ])
            -&gt;setFinder($finder)
            -&gt;setRiskyAllowed(true);
      </example>
    </pattern>
  </php_cs_fixer>

  <rector>
    <pattern name="config">
      <description>Rector automated refactoring configuration</description>
      <example>
        &lt;?php
        // rector.php
        use Rector\Config\RectorConfig;
        use Rector\Set\ValueObject\SetList;

        return RectorConfig::configure()
            -&gt;withPaths([
                __DIR__ . '/src',
                __DIR__ . '/tests',
            ])
            -&gt;withSets([
                SetList::CODE_QUALITY,
                SetList::DEAD_CODE,
                SetList::TYPE_DECLARATION,
            ])
            -&gt;withPhpSets(php83: true);
      </example>
      <note>LevelSetList (e.g., UP_TO_PHP_83) deprecated since Rector 0.19.2. Use -&gt;withPhpSets() instead.</note>
    </pattern>
  </rector>
</static_analysis>

<database>
  <pdo>
    <pattern name="connection">
      <description>PDO database connection</description>
      <example>
        $dsn = 'mysql:host=localhost;dbname=myapp;charset=utf8mb4';
        $options = [
            PDO::ATTR_ERRMODE =&gt; PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE =&gt; PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES =&gt; false,
        ];

        $pdo = new PDO($dsn, $username, $password, $options);
      </example>
    </pattern>

    <pattern name="prepared-statements">
      <description>Secure parameterized queries</description>
      <example>
        // Named parameters
        $stmt = $pdo-&gt;prepare('SELECT * FROM users WHERE email = :email');
        $stmt-&gt;execute(['email' =&gt; $email]);
        $user = $stmt-&gt;fetch();

        // Positional parameters
        $stmt = $pdo-&gt;prepare('INSERT INTO users (email, name) VALUES (?, ?)');
        $stmt-&gt;execute([$email, $name]);
        $id = $pdo-&gt;lastInsertId();
      </example>
      <warning>Never concatenate user input into SQL queries</warning>
    </pattern>

    <pattern name="transactions">
      <description>Database transactions with PDO</description>
      <example>
        try {
            $pdo-&gt;beginTransaction();

            $stmt = $pdo-&gt;prepare('UPDATE accounts SET balance = balance - ? WHERE id = ?');
            $stmt-&gt;execute([$amount, $fromAccount]);

            $stmt = $pdo-&gt;prepare('UPDATE accounts SET balance = balance + ? WHERE id = ?');
            $stmt-&gt;execute([$amount, $toAccount]);

            $pdo-&gt;commit();
        } catch (\Exception $e) {
            $pdo-&gt;rollBack();
            throw $e;
        }
      </example>
    </pattern>
  </pdo>
</database>

<performance>
  <opcache>
    <pattern name="production-config">
      <description>OPcache settings for production</description>
      <example>
        ; php.ini production settings
        opcache.enable=1
        opcache.memory_consumption=256
        opcache.interned_strings_buffer=16
        opcache.max_accelerated_files=10000
        opcache.validate_timestamps=0
        opcache.save_comments=1
        opcache.enable_file_override=1
      </example>
      <note>Set validate_timestamps=0 in production, clear cache on deploy</note>
    </pattern>
  </opcache>

  <jit>
    <pattern name="jit-config">
      <description>JIT compiler settings (PHP 8.0+)</description>
      <example>
        ; php.ini JIT settings
        opcache.jit=1255
        opcache.jit_buffer_size=128M
      </example>
      <note>JIT provides most benefit for CPU-intensive tasks, less for I/O-bound web apps</note>
    </pattern>
  </jit>

  <preloading>
    <pattern name="preload-script">
      <description>Preload classes at startup (PHP 7.4+)</description>
      <example>
        &lt;?php
        // preload.php
        require __DIR__ . '/vendor/autoload.php';

        // Preload commonly used classes
        $classesToPreload = [
            App\Domain\User\User::class,
            App\Domain\Order\Order::class,
        ];

        foreach ($classesToPreload as $class) {
            class_exists($class);
        }
      </example>
      <config>
        ; php.ini
        opcache.preload=/path/to/preload.php
        opcache.preload_user=www-data
      </config>
    </pattern>
  </preloading>
</performance>

<error_handling>
  <pattern name="exception-hierarchy">
    <description>Custom exception hierarchy</description>
    <example>
      // Base domain exception
      abstract class DomainException extends \Exception {}

      // Specific exceptions
      class EntityNotFoundException extends DomainException
      {
          public static function forClass(string $class, string $id): self
          {
              return new self(sprintf('%s with id "%s" not found', $class, $id));
          }
      }

      class ValidationException extends DomainException
      {
          public function __construct(
              string $message,
              public readonly array $errors = [],
          ) {
              parent::__construct($message);
          }
      }

      // Usage
      throw EntityNotFoundException::forClass(User::class, $userId);
    </example>
  </pattern>

  <pattern name="result-type">
    <description>Result type for error handling without exceptions</description>
    <example>
      /**
       * @template T
       * @template E
       */
      readonly class Result
      {
          private function __construct(
              private bool $success,
              private mixed $value,
          ) {}

          /** @return self&lt;T, never&gt; */
          public static function ok(mixed $value): self
          {
              return new self(true, $value);
          }

          /** @return self&lt;never, E&gt; */
          public static function error(mixed $error): self
          {
              return new self(false, $error);
          }

          public function isSuccess(): bool { return $this-&gt;success; }
          public function isError(): bool { return !$this-&gt;success; }
          public function getValue(): mixed { return $this-&gt;value; }
      }

      // Usage
      function divide(int $a, int $b): Result
      {
          if ($b === 0) {
              return Result::error('Division by zero');
          }
          return Result::ok($a / $b);
      }
    </example>
  </pattern>
</error_handling>

<anti_patterns>
  <avoid name="god_class">
    <description>Classes that do too much</description>
    <instead>Split into focused single-responsibility classes</instead>
  </avoid>

  <avoid name="service_locator">
    <description>Global service container access</description>
    <instead>Use constructor injection for explicit dependencies</instead>
  </avoid>

  <avoid name="array_shape_everywhere">
    <description>Using arrays instead of typed objects</description>
    <instead>Create value objects or DTOs with typed properties</instead>
  </avoid>

  <avoid name="mixed_type_abuse">
    <description>Using mixed to avoid proper typing</description>
    <instead>Use union types, generics, or proper type narrowing</instead>
  </avoid>

  <avoid name="static_method_abuse">
    <description>Overusing static methods making testing difficult</description>
    <instead>Use instance methods with dependency injection</instead>
  </avoid>

  <avoid name="null_returns">
    <description>Returning null for error conditions</description>
    <instead>Throw exceptions or use Result type</instead>
  </avoid>

  <avoid name="sql_concatenation">
    <description>Building SQL with string concatenation</description>
    <instead>Always use prepared statements with parameters</instead>
    <example>
      // Bad
      $sql = "SELECT * FROM users WHERE email = '$email'";

      // Good
      $stmt = $pdo-&gt;prepare('SELECT * FROM users WHERE email = ?');
      $stmt-&gt;execute([$email]);
    </example>
  </avoid>
</anti_patterns>

<best_practices>
  <practice priority="critical">Enable strict_types in all PHP files</practice>
  <practice priority="critical">Use prepared statements for all database queries</practice>
  <practice priority="critical">Use PHPStan level 6+ for type safety</practice>
  <practice priority="high">Use readonly classes for value objects</practice>
  <practice priority="high">Follow PSR-12 coding style</practice>
  <practice priority="high">Use enums instead of string/int constants</practice>
  <practice priority="high">Inject dependencies through constructor</practice>
  <practice priority="medium">Use named arguments for complex function calls</practice>
  <practice priority="medium">Create custom exceptions for domain errors</practice>
  <practice priority="medium">Use attributes for metadata instead of docblock annotations</practice>
</best_practices>

<workflow>
  <phase name="analyze">
    <objective>Understand PHP code requirements</objective>
    <step>1. Check PHP version constraints in composer.json</step>
    <step>2. Review existing type patterns in project</step>
    <step>3. Identify PSR standards in use</step>
  </phase>
  <phase name="implement">
    <objective>Write type-safe PHP code</objective>
    <step>1. Add declare(strict_types=1) at file start</step>
    <step>2. Define interfaces before implementations</step>
    <step>3. Use constructor property promotion</step>
    <step>4. Add return types to all methods</step>
  </phase>
  <phase name="validate">
    <objective>Verify PHP correctness</objective>
    <step>1. Run PHPStan for type checking</step>
    <step>2. Run PHP CS Fixer for style</step>
    <step>3. Run PHPUnit/Pest for tests</step>
  </phase>
</workflow>

<error_escalation>
  <level severity="low">
    <example>Minor coding style issue</example>
    <action>Auto-fix with PHP CS Fixer</action>
  </level>
  <level severity="medium">
    <example>PHPStan error or missing type</example>
    <action>Fix type, verify with static analysis</action>
  </level>
  <level severity="high">
    <example>Breaking API change or security issue</example>
    <action>Stop, present options to user</action>
  </level>
  <level severity="critical">
    <example>SQL injection or authentication bypass</example>
    <action>Block operation, require immediate fix</action>
  </level>
</error_escalation>

<constraints>
  <must>Add declare(strict_types=1) to all PHP files</must>
  <must>Use prepared statements for database queries</must>
  <must>Define explicit return types on all methods</must>
  <must>Follow PSR-12 coding style</must>
  <avoid>Using mixed type without justification</avoid>
  <avoid>Suppressing PHPStan errors without documentation</avoid>
  <avoid>Using @ error suppression operator</avoid>
</constraints>

<related_agents>
  <agent name="design">API design, architecture, and module structure planning</agent>
  <agent name="execute">PHP implementation with strict typing and PSR compliance</agent>
  <agent name="code-quality">PHPStan validation, type safety, and best practices</agent>
  <agent name="test">PHPUnit and Pest test creation and coverage</agent>
  <agent name="security">SQL injection, XSS, and authentication vulnerabilities</agent>
</related_agents>

<related_skills>
  <skill name="serena-usage">Symbol-level navigation for class and interface definitions</skill>
  <skill name="context7-usage">Fetch latest PHP and library documentation</skill>
  <skill name="testing-patterns">Test strategy and coverage patterns</skill>
  <skill name="database">PDO patterns and query optimization</skill>
</related_skills>
