---
name: athena-framework
description: "Use this skill when working with Athena Framework for Crystal. Athena is a modular ecosystem of independent, reusable components including: Framework (ATH) for web apps, DependencyInjection (ADI) for IoC containers, Routing (ART) for HTTP routing, Serializer (ASR) for object serialization, Validator (AVD) for validation, Console (ACON) for CLI tools, EventDispatcher (AED) for event-driven architecture, and more. Use for building Crystal web applications, REST APIs, CLI tools, or integrating individual components."
---

# Athena Framework Skill

Athena Framework is a modular web framework for Crystal, inspired by Symfony. It consists of independent, reusable components that can be used together or à la carte.

## When to Use This Skill

Use this skill when you are:
- **Building web applications** with the Athena Framework (ATH)
- **Creating REST APIs** using Athena's routing and controller system
- **Implementing dependency injection** with ADI (Athena DependencyInjection)
- **Adding HTTP routing** with ART (Athena Routing)
- **Serializing objects** with ASR (Athena Serializer)
- **Validating data** with AVD (Athena Validator)
- **Writing CLI commands** with ACON (Athena Console)
- **Implementing event-driven architecture** with AED (Athena EventDispatcher)
- **Working with individual Athena components** in any Crystal project
- **Debugging Athena applications**
- **Learning Crystal web development patterns**

## Key Concepts

### Component Overview

| Component | Alias | Purpose |
|-----------|-------|---------|
| Framework | `ATH` | Full-stack web framework with controllers, middleware, responses |
| DependencyInjection | `ADI` | IoC container for managing service dependencies |
| Routing | `ART` | HTTP routing with annotations, requirements, and matching |
| Serializer | `ASR` | Object (de)serialization to JSON, YAML, etc. |
| Validator | `AVD` | Declarative object validation with constraints |
| Console | `ACON` | CLI command framework with styled output |
| EventDispatcher | `AED` | Event-driven architecture with listeners/dispatchers |
| Negotiation | `ANEG` | Content negotiation for requests/responses |
| ImageSize | `AIS` | Get image dimensions without processing |
| Clock | `ACLK` | Time abstraction for testing |

## Quick Reference

### HTTP Routing (ART)

**Define a route with requirements:**

```crystal
class ExampleController < ATH::Controller
  @[ARTA::Get("/user/{id}")]
  def get_user(id : Int64) : Int64
    id
  end

  @[ARTA::Get("/article/{slug}")]
  def get_article(slug : String) : String
    slug
  end
end
```

**Built-in route requirements:**

```crystal
# Only matches digits
ART::Requirement::DIGITS        # /[0-9]+/

# Matches URL-safe slugs
ART::Requirement::ASCII_SLUG    # /[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*/

# Date format YYYY-MM-DD
ART::Requirement::DATE_YMD      # /[0-9]{4}-(?:0[1-9]|1[012])-(?:0[1-9]|[12][0-9]|(?<!02-)3[01])/

# UUID formats
ART::Requirement::UID_BASE32    # /[0-9A-HJKMNP-TV-Z]{26}/
ART::Requirement::UID_BASE58    # /[1-9A-HJ-NP-Za-km-z]{22}/
ART::Requirement::UID_RFC4122   # /[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}/
```

**Route with optional parameters:**

```crystal
# /blog would match with default page=1
# /blog/10 would match with page=10
ART::Route.new "/blog/{page}", {"page" => 1}, {"page" => /\d+/}
```

**Route with custom conditions:**

```crystal
route = ART::Route.new "/contact"
route.condition do |context, request|
  request.headers["user-agent"].includes? "Firefox"
end
```

### Dependency Injection (ADI)

**Register and inject services:**

```crystal
# Register a service with constructor injection
@[ADI::Register(public: true)]
class DatabaseService
  def initialize(@connection_string : String); end
end

# Use ADI::Inject to specify which constructor to use
@[ADI::Register(_value: 2, public: true)]
class SomeService
  @active : Bool = false

  # Regular constructor
  def initialize(value : String, @active : Bool)
    @value = value.to_i
  end

  # DI-specific constructor
  @[ADI::Inject]
  def initialize(@value : Int32); end
end
```

### Event Dispatcher (AED)

**Create and dispatch events:**

```crystal
# Define a custom event
class MyEvent < AED::Event
  property data : String

  def initialize(@data)
  end
end

# Register a listener
dispatcher = AED::EventDispatcher.new
dispatcher.listener(MyEvent) do |event|
  puts "Event received: #{event.data}"
end

# Dispatch the event
dispatcher.dispatch(MyEvent.new("Hello World"))
```

**Using generic events:**

```crystal
# Generic event with type safety
dispatcher.listener AED::GenericEvent(User, Int32) do |e|
  e["counter"] += 1
end

dispatcher.dispatch AED::GenericEvent.new user, data = {"counter" => 0}
```

**Callable listeners with priority:**

```crystal
callable = MyEvent.callable(priority: 10) do |event, dispatcher|
  # Handle event
end

dispatcher.listener callable
```

### Serializer (ASR)

**Serialize/deserialize objects:**

```crystal
require "athena-serializer"

record Example, id : Int32, name : String do
  include ASR::Serializable
end

# Deserialize from JSON
obj = ASR.serializer.deserialize Example, %({"id":1,"name":"George"}), :json

# Serialize to YAML
ASR.serializer.serialize obj, :yaml
# =>
# ---
# id: 1
# name: George
```

### Console (ACON)

**Create a CLI command:**

```crystal
class GreetCommand < ACON::Command
  def configure : Nil
    self
      .name("greet")
      .description("Greets someone")
      .argument("name", ACON::Input::Argument::Mode::REQUIRED, "Who to greet")
      .option("yell", mode: ACON::Input::Option::Mode::NONE, description: "Yell in uppercase")
  end

  def execute(input : ACON::Input::Interface, output : ACON::Output::Interface) : ACON::Command::Status
    name = input.argument("name", String)
    message = "Hello #{name}"

    if input.option("yell", Bool)
      message = message.upcase
    end

    output.puts message
    ACON::Command::Status::SUCCESS
  end
end
```

### Framework Controller (ATH)

**Basic controller with responses:**

```crystal
class ApiController < ATH::Controller
  # Returns JSON response
  @[ATHA::Get("/api/users")]
  @[ATHA::View("user_list.json.ecr")]
  def list_users : Iterable(User)
    UserRepository.all
  end

  # Returns plain text
  @[ATHA::Get("/health")]
  def health_check : String
    "OK"
  end

  # Custom response with headers
  @[ATHA::Post("/data")]
  def create_data(body : DataRequest) : ATH::Response
    ATH::Response.new(
      "Created",
      status: :created,
      headers: HTTP::Headers{"X-Custom" => "value"}
    )
  end
end
```

**HTTP testing expectations:**

```crystal
# In your specs
include ATH::Spec::Expectations::HTTP

client = ATH::Spec::APIClient.new(APP)

# Test response status
client.get("/health").assert_response_is_successful

# Test response headers
client.get("/api/data").assert_response_has_header("content-type")

# Test response body
client.get("/api/users").assert_json_contains({"users" => [...]})
```

### Testing Utilities (ASPEC)

**Compile-time and runtime assertions:**

```crystal
# Assert code fails to compile with specific message
ASPEC::Methods.assert_compile_time_error "can't instantiate abstract class Foo", <<-CR
  abstract class Foo; end
  Foo.new
CR

# Assert code compiles successfully
ASPEC::Methods.assert_compiles <<-CR
  puts 2 + 2
CR

# Assert code executes without error
ASPEC::Methods.assert_executes <<-CR
  puts "Running fine"
CR

# Assert code raises specific runtime error
ASPEC::Methods.assert_runtime_error "Oh noes!", <<-CR
  raise "Oh noes!"
CR
```

### CORS Configuration

The framework includes built-in CORS support:

```crystal
# Configure CORS in your application
ATH::Listeners::CORS is enabled by default
# Uses SAFELISTED_HEADERS and SAFELISTED_METHODS for standard browser requests
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

| File | Description | Pages | Source |
|------|-------------|-------|--------|
| **framework.md** | Core framework API documentation | 332 | Official |
| **getting_started.md** | Getting started guides and routing | 44 | Official |
| **index.md** | Documentation index | - | Official |

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners

1. Start with **getting_started.md** for foundational routing concepts
2. Review the Quick Reference examples above for common patterns
3. Use the official [Athena Framework documentation](https://athenaframework.org) for tutorials

### For Intermediate Users

1. Explore **framework.md** for specific component APIs
2. Check the Console and EventDispatcher sections for advanced patterns
3. Look at testing utilities for writing specs

### For Advanced Users

1. Dive into specific component documentation for edge cases
2. Study the annotation system for metaprogramming patterns
3. Reference the testing modules for advanced assertion patterns

### Navigation Tips

- The reference files are organized by component (Framework, Getting Started)
- Each section includes URL references to the official documentation
- Code examples in references preserve their original language formatting
- Use pattern matching (e.g., `ART::` for Routing, `ADI::` for Dependency Injection)

## Common Use Cases

### REST API

```crystal
class UsersController < ATH::Controller
  @[ATHA::Get("/users")]
  def index : Iterable(User)
    UserRepository.all
  end

  @[ATHA::Get("/users/{id}")]
  def show(id : Int64) : User?
    UserRepository.find id
  end

  @[ATHA::Post("/users")]
  def create(body : UserRequest) : ATH::Response
    user = UserRepository.create(body)
    ATH::Response.new(
      ASR.serializer.serialize(user, :json),
      status: :created,
      headers: HTTP::Headers{"Location" => "/users/#{user.id}"}
    )
  end
end
```

### JSON API with Validation

```crystal
class CreateUserRequest
  include AVD::Validatable

  property name : String
  property email : String

  # Apply validation constraints
  @[AVD::Assert::NotBlank]
  @[AVD::Assert::Length(min: 2, max: 100)]
  property name : String

  @[AVD::Assert::Email]
  property email : String
end
```

### Background Job Processing

```crystal
# Define events
class JobCompletedEvent < AED::Event
  property job_id : String

  def initialize(@job_id)
  end
end

# Create listener
class JobListener
  def self.register(dispatcher : AED::EventDispatcherInterface)
    dispatcher.listener(JobCompletedEvent, priority: 10) do |event|
      puts "Job #{event.job_id} completed!"
    end
  end
end
```

## Notes

- This skill combines knowledge from official Athena Framework documentation
- All components are designed to work independently or together
- Crystal syntax highlighting uses the `crystal` language tag
- Code examples are extracted from official documentation and real-world usage

## Updating

To refresh this skill with updated documentation:
1. Re-run the documentation scraper
2. The skill will be rebuilt with the latest API information
3. Check the [Athena Framework GitHub](https://github.com/athena-framework) for releases
