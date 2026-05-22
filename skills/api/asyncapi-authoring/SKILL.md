---
name: asyncapi-authoring
description: Author and validate AsyncAPI 3.0 specifications for event-driven API design, message brokers, and async communication patterns
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# AsyncAPI Authoring Skill

## When to Use This Skill

Use this skill when:

- **Asyncapi Authoring tasks** - Working on author and validate asyncapi 3.0 specifications for event-driven api design, message brokers, and async communication patterns
- **Planning or design** - Need guidance on Asyncapi Authoring approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Author AsyncAPI 3.0 specifications for event-driven architectures and async communication patterns.

## AsyncAPI 3.0 Structure

### Root Document

```yaml
asyncapi: "3.0.0"

info:
  title: "{Service Name} Events API"
  version: "1.0.0"
  description: |
    Event-driven API for {service} domain events and commands.
  contact:
    name: "{Team Name}"
    email: "{team@company.com}"
  license:
    name: "MIT"

servers:
  production:
    host: "kafka.example.com:9092"
    protocol: "kafka"
    description: "Production Kafka cluster"
    security:
      - $ref: "#/components/securitySchemes/sasl"

  development:
    host: "localhost:9092"
    protocol: "kafka"
    description: "Local development"

defaultContentType: "application/json"

channels:
  # Channel definitions

operations:
  # Operation definitions

components:
  # Reusable components
```

### Channels (AsyncAPI 3.0)

```yaml
channels:
  orderEvents:
    address: "orders.events.{orderId}"
    description: "Channel for order lifecycle events"
    parameters:
      orderId:
        description: "Order unique identifier"
        schema:
          type: string
          format: uuid
    messages:
      orderCreated:
        $ref: "#/components/messages/OrderCreated"
      orderShipped:
        $ref: "#/components/messages/OrderShipped"
      orderDelivered:
        $ref: "#/components/messages/OrderDelivered"
      orderCancelled:
        $ref: "#/components/messages/OrderCancelled"

  orderCommands:
    address: "orders.commands"
    description: "Channel for order command messages"
    messages:
      createOrder:
        $ref: "#/components/messages/CreateOrderCommand"
      cancelOrder:
        $ref: "#/components/messages/CancelOrderCommand"

  inventoryUpdates:
    address: "inventory.updates.{productId}"
    description: "Real-time inventory level updates"
    parameters:
      productId:
        schema:
          type: string
    messages:
      inventoryChanged:
        $ref: "#/components/messages/InventoryChanged"
```

### Operations (AsyncAPI 3.0)

```yaml
operations:
  # Publishing operations (this service sends)
  publishOrderCreated:
    action: send
    channel:
      $ref: "#/channels/orderEvents"
    summary: "Publish order created event"
    description: |
      Published when a new order is successfully created.
      Consumers should use this to trigger downstream processes.
    messages:
      - $ref: "#/channels/orderEvents/messages/orderCreated"
    tags:
      - name: "orders"
      - name: "lifecycle"

  publishOrderShipped:
    action: send
    channel:
      $ref: "#/channels/orderEvents"
    summary: "Publish order shipped event"
    messages:
      - $ref: "#/channels/orderEvents/messages/orderShipped"

  # Receiving operations (this service receives)
  receiveCreateOrderCommand:
    action: receive
    channel:
      $ref: "#/channels/orderCommands"
    summary: "Process create order commands"
    description: |
      Receives commands to create new orders.
      Will publish OrderCreated event on success.
    messages:
      - $ref: "#/channels/orderCommands/messages/createOrder"

  # Subscription operations
  subscribeInventoryUpdates:
    action: receive
    channel:
      $ref: "#/channels/inventoryUpdates"
    summary: "Subscribe to inventory changes"
    description: |
      Subscribes to real-time inventory updates.
      Used to maintain local inventory cache.
    messages:
      - $ref: "#/channels/inventoryUpdates/messages/inventoryChanged"
```

### Message Definitions

```yaml
components:
  messages:
    OrderCreated:
      name: "OrderCreated"
      title: "Order Created Event"
      summary: "Indicates a new order has been created"
      contentType: "application/json"
      headers:
        $ref: "#/components/schemas/EventHeaders"
      payload:
        $ref: "#/components/schemas/OrderCreatedPayload"
      correlationId:
        location: "$message.header#/correlationId"
      traits:
        - $ref: "#/components/messageTraits/commonHeaders"

    OrderShipped:
      name: "OrderShipped"
      title: "Order Shipped Event"
      summary: "Indicates an order has been shipped"
      contentType: "application/json"
      headers:
        $ref: "#/components/schemas/EventHeaders"
      payload:
        $ref: "#/components/schemas/OrderShippedPayload"
      traits:
        - $ref: "#/components/messageTraits/commonHeaders"

    OrderCancelled:
      name: "OrderCancelled"
      title: "Order Cancelled Event"
      summary: "Indicates an order has been cancelled"
      contentType: "application/json"
      headers:
        $ref: "#/components/schemas/EventHeaders"
      payload:
        $ref: "#/components/schemas/OrderCancelledPayload"

    CreateOrderCommand:
      name: "CreateOrderCommand"
      title: "Create Order Command"
      summary: "Command to create a new order"
      contentType: "application/json"
      headers:
        $ref: "#/components/schemas/CommandHeaders"
      payload:
        $ref: "#/components/schemas/CreateOrderPayload"

    InventoryChanged:
      name: "InventoryChanged"
      title: "Inventory Changed Event"
      summary: "Real-time inventory level update"
      contentType: "application/json"
      payload:
        $ref: "#/components/schemas/InventoryChangedPayload"
```

### Payload Schemas

```yaml
components:
  schemas:
    # Event headers
    EventHeaders:
      type: object
      required:
        - eventId
        - eventType
        - timestamp
        - version
      properties:
        eventId:
          type: string
          format: uuid
          description: "Unique event identifier"
        eventType:
          type: string
          description: "Event type name"
        timestamp:
          type: string
          format: date-time
          description: "Event timestamp (ISO 8601)"
        version:
          type: string
          description: "Event schema version"
          example: "1.0"
        correlationId:
          type: string
          format: uuid
          description: "Correlation ID for tracing"
        causationId:
          type: string
          format: uuid
          description: "ID of the event/command that caused this"

    CommandHeaders:
      type: object
      required:
        - commandId
        - commandType
        - timestamp
      properties:
        commandId:
          type: string
          format: uuid
          description: "Unique command identifier"
        commandType:
          type: string
          description: "Command type name"
        timestamp:
          type: string
          format: date-time
        correlationId:
          type: string
          format: uuid
        userId:
          type: string
          description: "User initiating the command"

    # Event payloads
    OrderCreatedPayload:
      type: object
      required:
        - orderId
        - customerId
        - items
        - totalAmount
        - createdAt
      properties:
        orderId:
          type: string
          format: uuid
        customerId:
          type: string
          format: uuid
        items:
          type: array
          items:
            $ref: "#/components/schemas/OrderItem"
        totalAmount:
          $ref: "#/components/schemas/Money"
        shippingAddress:
          $ref: "#/components/schemas/Address"
        createdAt:
          type: string
          format: date-time

    OrderShippedPayload:
      type: object
      required:
        - orderId
        - trackingNumber
        - carrier
        - shippedAt
      properties:
        orderId:
          type: string
          format: uuid
        trackingNumber:
          type: string
        carrier:
          type: string
          enum:
            - "fedex"
            - "ups"
            - "usps"
            - "dhl"
        estimatedDelivery:
          type: string
          format: date
        shippedAt:
          type: string
          format: date-time

    OrderCancelledPayload:
      type: object
      required:
        - orderId
        - reason
        - cancelledAt
      properties:
        orderId:
          type: string
          format: uuid
        reason:
          type: string
          enum:
            - "customer_request"
            - "payment_failed"
            - "out_of_stock"
            - "fraud_detected"
        refundAmount:
          $ref: "#/components/schemas/Money"
        cancelledAt:
          type: string
          format: date-time
        cancelledBy:
          type: string
          description: "User or system that cancelled"

    # Command payloads
    CreateOrderPayload:
      type: object
      required:
        - customerId
        - items
      properties:
        customerId:
          type: string
          format: uuid
        items:
          type: array
          minItems: 1
          items:
            $ref: "#/components/schemas/OrderItemRequest"
        shippingAddress:
          $ref: "#/components/schemas/Address"
        billingAddress:
          $ref: "#/components/schemas/Address"
        couponCode:
          type: string

    # Domain schemas
    OrderItem:
      type: object
      required:
        - productId
        - productName
        - quantity
        - unitPrice
      properties:
        productId:
          type: string
          format: uuid
        productName:
          type: string
        quantity:
          type: integer
          minimum: 1
        unitPrice:
          $ref: "#/components/schemas/Money"

    OrderItemRequest:
      type: object
      required:
        - productId
        - quantity
      properties:
        productId:
          type: string
          format: uuid
        quantity:
          type: integer
          minimum: 1

    Money:
      type: object
      required:
        - amount
        - currency
      properties:
        amount:
          type: number
          format: decimal
          minimum: 0
        currency:
          type: string
          pattern: "^[A-Z]{3}$"
          example: "USD"

    Address:
      type: object
      required:
        - street
        - city
        - country
      properties:
        street:
          type: string
        city:
          type: string
        state:
          type: string
        postalCode:
          type: string
        country:
          type: string
          pattern: "^[A-Z]{2}$"

    InventoryChangedPayload:
      type: object
      required:
        - productId
        - previousQuantity
        - newQuantity
        - reason
        - changedAt
      properties:
        productId:
          type: string
          format: uuid
        previousQuantity:
          type: integer
        newQuantity:
          type: integer
        reason:
          type: string
          enum:
            - "sale"
            - "return"
            - "restock"
            - "adjustment"
            - "reservation"
        changedAt:
          type: string
          format: date-time
```

### Message Traits and Security

```yaml
components:
  messageTraits:
    commonHeaders:
      headers:
        type: object
        properties:
          x-trace-id:
            type: string
            description: "Distributed tracing ID"
          x-span-id:
            type: string
            description: "Span ID for tracing"

  securitySchemes:
    sasl:
      type: scramSha256
      description: "SASL/SCRAM-SHA-256 authentication"

    apiKey:
      type: apiKey
      in: user
      description: "API key authentication"

    oauth2:
      type: oauth2
      flows:
        clientCredentials:
          tokenUrl: "https://auth.example.com/token"
          scopes:
            "events:publish": "Publish events"
            "events:subscribe": "Subscribe to events"

  serverBindings:
    kafka:
      schemaRegistryUrl: "https://schema-registry.example.com"
      schemaRegistryVendor: "confluent"
```

## C# Models for AsyncAPI

```csharp
namespace SpecDrivenDevelopment.AsyncApi;

/// <summary>
/// Represents an AsyncAPI 3.0 specification document
/// </summary>
public record AsyncApiSpec
{
    public required string AsyncApi { get; init; } = "3.0.0";
    public required AsyncApiInfo Info { get; init; }
    public Dictionary<string, AsyncApiServer> Servers { get; init; } = [];
    public string? DefaultContentType { get; init; }
    public Dictionary<string, AsyncApiChannel> Channels { get; init; } = [];
    public Dictionary<string, AsyncApiOperation> Operations { get; init; } = [];
    public AsyncApiComponents? Components { get; init; }
}

public record AsyncApiInfo
{
    public required string Title { get; init; }
    public required string Version { get; init; }
    public string? Description { get; init; }
    public AsyncApiContact? Contact { get; init; }
    public AsyncApiLicense? License { get; init; }
}

public record AsyncApiContact
{
    public string? Name { get; init; }
    public string? Email { get; init; }
    public string? Url { get; init; }
}

public record AsyncApiLicense
{
    public required string Name { get; init; }
    public string? Url { get; init; }
}

public record AsyncApiServer
{
    public required string Host { get; init; }
    public required string Protocol { get; init; }
    public string? ProtocolVersion { get; init; }
    public string? Description { get; init; }
    public List<Dictionary<string, List<string>>>? Security { get; init; }
    public Dictionary<string, object>? Bindings { get; init; }
}

public record AsyncApiChannel
{
    public required string Address { get; init; }
    public string? Description { get; init; }
    public Dictionary<string, AsyncApiParameter>? Parameters { get; init; }
    public Dictionary<string, AsyncApiMessage>? Messages { get; init; }
    public Dictionary<string, object>? Bindings { get; init; }
}

public record AsyncApiParameter
{
    public string? Description { get; init; }
    public AsyncApiSchema? Schema { get; init; }
    public string? Location { get; init; }
}

public record AsyncApiOperation
{
    public required OperationAction Action { get; init; }
    public required AsyncApiChannelRef Channel { get; init; }
    public string? Summary { get; init; }
    public string? Description { get; init; }
    public List<AsyncApiMessageRef>? Messages { get; init; }
    public List<AsyncApiTag>? Tags { get; init; }
    public List<Dictionary<string, List<string>>>? Security { get; init; }
    public Dictionary<string, object>? Bindings { get; init; }
}

public enum OperationAction
{
    Send,
    Receive
}

public record AsyncApiChannelRef
{
    public string? Ref { get; init; }
}

public record AsyncApiMessageRef
{
    public string? Ref { get; init; }
}

public record AsyncApiMessage
{
    public string? Name { get; init; }
    public string? Title { get; init; }
    public string? Summary { get; init; }
    public string? Description { get; init; }
    public string? ContentType { get; init; }
    public AsyncApiSchema? Headers { get; init; }
    public AsyncApiSchema? Payload { get; init; }
    public AsyncApiCorrelationId? CorrelationId { get; init; }
    public List<AsyncApiMessageTraitRef>? Traits { get; init; }
    public Dictionary<string, object>? Bindings { get; init; }
}

public record AsyncApiCorrelationId
{
    public string? Description { get; init; }
    public required string Location { get; init; }
}

public record AsyncApiMessageTraitRef
{
    public string? Ref { get; init; }
}

public record AsyncApiTag
{
    public required string Name { get; init; }
    public string? Description { get; init; }
}

public record AsyncApiSchema
{
    public string? Type { get; init; }
    public string? Format { get; init; }
    public string? Description { get; init; }
    public List<string>? Enum { get; init; }
    public object? Default { get; init; }
    public object? Example { get; init; }
    public List<string>? Required { get; init; }
    public Dictionary<string, AsyncApiSchema>? Properties { get; init; }
    public AsyncApiSchema? Items { get; init; }
    public int? MinItems { get; init; }
    public int? MaxItems { get; init; }
    public int? MinLength { get; init; }
    public int? MaxLength { get; init; }
    public decimal? Minimum { get; init; }
    public decimal? Maximum { get; init; }
    public string? Pattern { get; init; }
    public List<AsyncApiSchema>? AllOf { get; init; }
    public List<AsyncApiSchema>? OneOf { get; init; }
    public List<AsyncApiSchema>? AnyOf { get; init; }
    public string? Ref { get; init; }
}

public record AsyncApiComponents
{
    public Dictionary<string, AsyncApiSchema>? Schemas { get; init; }
    public Dictionary<string, AsyncApiMessage>? Messages { get; init; }
    public Dictionary<string, AsyncApiParameter>? Parameters { get; init; }
    public Dictionary<string, AsyncApiSecurityScheme>? SecuritySchemes { get; init; }
    public Dictionary<string, AsyncApiMessageTrait>? MessageTraits { get; init; }
    public Dictionary<string, AsyncApiOperationTrait>? OperationTraits { get; init; }
}

public record AsyncApiSecurityScheme
{
    public required string Type { get; init; }
    public string? Description { get; init; }
    public string? In { get; init; }
    public string? Name { get; init; }
    public AsyncApiOAuthFlows? Flows { get; init; }
}

public record AsyncApiOAuthFlows
{
    public AsyncApiOAuthFlow? ClientCredentials { get; init; }
}

public record AsyncApiOAuthFlow
{
    public required string TokenUrl { get; init; }
    public required Dictionary<string, string> Scopes { get; init; }
}

public record AsyncApiMessageTrait
{
    public AsyncApiSchema? Headers { get; init; }
    public string? ContentType { get; init; }
}

public record AsyncApiOperationTrait
{
    public string? Summary { get; init; }
    public string? Description { get; init; }
    public List<AsyncApiTag>? Tags { get; init; }
}
```

## Event Design Patterns

### Event Naming Conventions

```yaml
event_naming:
  format: "{Aggregate}{Action}"

  past_tense_events:
    description: "Events describe something that happened"
    examples:
      - "OrderCreated"
      - "OrderShipped"
      - "PaymentProcessed"
      - "UserRegistered"
      - "InventoryReserved"

  command_naming:
    format: "{Action}{Aggregate}Command"
    examples:
      - "CreateOrderCommand"
      - "CancelOrderCommand"
      - "ProcessPaymentCommand"

  channel_naming:
    pattern: "{domain}.{type}.{resource}"
    examples:
      - "orders.events" (all order events)
      - "orders.events.{orderId}" (specific order)
      - "orders.commands" (order commands)
      - "inventory.updates.{productId}" (inventory changes)
```

### Event Envelope Pattern

```yaml
event_envelope:
  description: "Standardized wrapper for all events"

  structure:
    metadata:
      eventId: "UUID - unique event ID"
      eventType: "String - event type name"
      version: "String - schema version"
      timestamp: "ISO 8601 timestamp"
      correlationId: "UUID - request correlation"
      causationId: "UUID - causing event ID"
      source: "String - producing service"

    data: "Actual event payload"

  example:
    metadata:
      eventId: "550e8400-e29b-41d4-a716-446655440000"
      eventType: "OrderCreated"
      version: "1.0"
      timestamp: "2025-01-15T10:30:00Z"
      correlationId: "660e8400-e29b-41d4-a716-446655440001"
      source: "order-service"
    data:
      orderId: "order-123"
      customerId: "customer-456"
      totalAmount:
        amount: 99.99
        currency: "USD"
```

### Schema Evolution

```yaml
schema_evolution:
  strategies:
    backward_compatible:
      description: "New schema can read old data"
      allowed_changes:
        - "Add optional fields"
        - "Add new enum values at end"
        - "Widen numeric ranges"
      disallowed_changes:
        - "Remove required fields"
        - "Change field types"
        - "Rename fields"

    forward_compatible:
      description: "Old schema can read new data"
      approach: "Ignore unknown fields"

    full_compatible:
      description: "Both directions work"
      best_practice: "Default for most systems"

  versioning:
    header_based:
      example: "version: '1.0'"

    channel_based:
      example: "orders.events.v2"

    semantic:
      format: "major.minor"
      major: "Breaking changes"
      minor: "Backward-compatible additions"
```

## Validation Checklist

```yaml
asyncapi_validation_checklist:
  structure:
    - "Valid AsyncAPI 3.0.0 syntax"
    - "All required fields present"
    - "No undefined $ref references"
    - "Consistent naming conventions"

  channels:
    - "Clear channel addressing scheme"
    - "Parameters defined for dynamic channels"
    - "All messages referenced exist"

  operations:
    - "Action (send/receive) correctly specified"
    - "Channel reference valid"
    - "Summary and description provided"
    - "Appropriate tags assigned"

  messages:
    - "Unique message names"
    - "Clear title and summary"
    - "Headers schema defined"
    - "Payload schema complete"
    - "Correlation ID specified where needed"

  schemas:
    - "All required fields listed"
    - "Types and formats specified"
    - "Examples provided"
    - "Validation constraints appropriate"

  security:
    - "Security schemes defined for production"
    - "Operations specify security requirements"

  documentation:
    - "API description explains purpose"
    - "Contact information provided"
    - "Server URLs for all environments"
```

## References

- `references/messaging-patterns.md` - Event-driven messaging patterns
- `references/protocol-bindings.md` - Protocol-specific configurations

---

**Last Updated:** 2025-12-26
