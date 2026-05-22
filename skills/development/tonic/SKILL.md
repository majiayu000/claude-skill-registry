---
name: Tonic gRPC
description: gRPC framework for Rust built on Tokio and Tower.
metadata:
  labels: [rust, tonic, grpc, protobuf, rpc]
  triggers:
    files: ['**/*.proto', 'build.rs']
    keywords: [tonic, prost, Request, Response, Server, Channel]
---

# Tonic gRPC Standards

## Proto Definition

```protobuf
// proto/hello.proto
syntax = "proto3";
package hello;

service Greeter {
    rpc SayHello (HelloRequest) returns (HelloReply);
    rpc SayHelloStream (HelloRequest) returns (stream HelloReply);
}

message HelloRequest {
    string name = 1;
}

message HelloReply {
    string message = 1;
}
```

## Build Configuration

```rust
// build.rs
fn main() -> Result<(), Box<dyn std::error::Error>> {
    tonic_build::compile_protos("proto/hello.proto")?;
    Ok(())
}
```

```toml
# Cargo.toml
[dependencies]
tonic = "0.10"
prost = "0.12"
tokio = { version = "1", features = ["full"] }

[build-dependencies]
tonic-build = "0.10"
```

## Server Implementation

```rust
use tonic::{transport::Server, Request, Response, Status};
use hello::greeter_server::{Greeter, GreeterServer};
use hello::{HelloReply, HelloRequest};

pub mod hello {
    tonic::include_proto!("hello");
}

#[derive(Default)]
pub struct MyGreeter {}

#[tonic::async_trait]
impl Greeter for MyGreeter {
    async fn say_hello(
        &self,
        request: Request<HelloRequest>,
    ) -> Result<Response<HelloReply>, Status> {
        let name = request.into_inner().name;
        let reply = HelloReply {
            message: format!("Hello, {}!", name),
        };
        Ok(Response::new(reply))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "[::1]:50051".parse()?;
    let greeter = MyGreeter::default();

    Server::builder()
        .add_service(GreeterServer::new(greeter))
        .serve(addr)
        .await?;

    Ok(())
}
```

## Client

```rust
use hello::greeter_client::GreeterClient;
use hello::HelloRequest;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut client = GreeterClient::connect("http://[::1]:50051").await?;

    let request = tonic::Request::new(HelloRequest {
        name: "World".into(),
    });

    let response = client.say_hello(request).await?;
    println!("Response: {:?}", response);

    Ok(())
}
```

## Streaming

```rust
use tokio_stream::wrappers::ReceiverStream;
use futures_util::StreamExt;

#[tonic::async_trait]
impl Greeter for MyGreeter {
    // Server streaming
    type SayHelloStreamStream = ReceiverStream<Result<HelloReply, Status>>;

    async fn say_hello_stream(
        &self,
        request: Request<HelloRequest>,
    ) -> Result<Response<Self::SayHelloStreamStream>, Status> {
        let (tx, rx) = tokio::sync::mpsc::channel(4);
        let name = request.into_inner().name;

        tokio::spawn(async move {
            for i in 0..5 {
                tx.send(Ok(HelloReply {
                    message: format!("Hello #{}, {}!", i, name),
                })).await.unwrap();
                tokio::time::sleep(Duration::from_secs(1)).await;
            }
        });

        Ok(Response::new(ReceiverStream::new(rx)))
    }
}

// Client receiving stream
let mut stream = client.say_hello_stream(request).await?.into_inner();
while let Some(reply) = stream.next().await {
    println!("Reply: {:?}", reply?);
}
```

## Interceptors

```rust
use tonic::{Request, Status};

fn auth_interceptor(req: Request<()>) -> Result<Request<()>, Status> {
    let token = req.metadata()
        .get("authorization")
        .ok_or_else(|| Status::unauthenticated("No token"))?
        .to_str()
        .map_err(|_| Status::unauthenticated("Invalid token"))?;

    if !validate_token(token) {
        return Err(Status::unauthenticated("Invalid token"));
    }

    Ok(req)
}

// Apply interceptor
let greeter = GreeterServer::with_interceptor(MyGreeter::default(), auth_interceptor);

// Client with interceptor
let channel = Channel::from_static("http://[::1]:50051").connect().await?;
let client = GreeterClient::with_interceptor(channel, |mut req: Request<()>| {
    req.metadata_mut().insert("authorization", "Bearer token".parse().unwrap());
    Ok(req)
});
```

## Error Handling

```rust
use tonic::Status;

async fn my_method(&self, request: Request<Req>) -> Result<Response<Resp>, Status> {
    let data = fetch_data()
        .await
        .map_err(|e| Status::internal(format!("DB error: {}", e)))?;

    if data.is_empty() {
        return Err(Status::not_found("Resource not found"));
    }

    // Status codes: ok, cancelled, unknown, invalid_argument,
    // deadline_exceeded, not_found, already_exists, permission_denied,
    // resource_exhausted, failed_precondition, aborted, out_of_range,
    // unimplemented, internal, unavailable, data_loss, unauthenticated

    Ok(Response::new(resp))
}
```

## TLS

```rust
use tonic::transport::{Certificate, Identity, ServerTlsConfig};

let cert = std::fs::read_to_string("server.crt")?;
let key = std::fs::read_to_string("server.key")?;
let identity = Identity::from_pem(cert, key);

Server::builder()
    .tls_config(ServerTlsConfig::new().identity(identity))?
    .add_service(service)
    .serve(addr)
    .await?;
```

## Best Practices

1. **Proto first**: Design API in proto files
2. **Error codes**: Use appropriate Status codes
3. **Streaming**: Use for large data or real-time
4. **Interceptors**: Auth, logging, metrics
5. **Deadlines**: Set timeouts on client calls
