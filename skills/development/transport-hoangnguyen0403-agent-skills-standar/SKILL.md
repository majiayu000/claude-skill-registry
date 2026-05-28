---
name: NestJS Microservices
description: gRPC, RabbitMQ standards and Monorepo contracts.
metadata:
  labels: [nestjs, microservices, grpc, rabbitmq]
  triggers:
    files: ['main.ts', '**/*.controller.ts']
    keywords: [Transport.GRPC, Transport.RMQ, MicroserviceOptions]
---

# Microservices & Transport Standards

## **Priority: P0 (FOUNDATIONAL)**

Microservices communication patterns and transport layer standards.

- **Synchronous (RPC)**: Use **gRPC** for low-latency, internal service-to-service calls.
  - **Why**: 10x faster than REST/JSON, centralized `.proto` contracts.
- **Asynchronous (Events)**: Use **RabbitMQ** or **Kafka** for decoupling domains.
  - **Pattern**: Fire-and-forget (`emit()`) for side effects (e.g., "UserCreated" -> "SendEmail").

## Monorepo Architecture

- **Contracts**:
  - **Pattern**: Store all DTOs, `.proto` files, and Interfaces in a **Shared Library** (`libs/contracts`).
  - **Rule**: Services never import code from other services. They only import from `contracts`.
- **Versioning**: Semantic versioning of messages is mandatory. Never change a field type; add a new field.

## Exception Handling

- **Propagation**: Standard `HttpException` is lost over Rpc/Tcp.
- **Standard**: Use `RpcException` and generic Filters.

  ```typescript
  // Global RPC Filter
  @Catch()
  export class RpcExceptionFilter implements RpcExceptionFilter<RpcException> {
    catch(exception: RpcException, host: ArgumentsHost): Observable<any> {
      return throwError(() => exception.getError());
    }
  }
  ```

## Serialization

- **Message DTOs**: Use `class-validator` just like HTTP.
  - **Config**: Apply `useGlobalPipes(new ValidationPipe({ transform: true }))` in the `MicroserviceOptions` setup, not just HTTP app setup.
