---
name: update-grpc-proto
description: Update @dojoengine/grpc proto files from Torii repository
triggers:
  - update grpc proto
  - update proto files
  - sync torii proto
  - grpc proto update
  - torii proto sync
---

# Update gRPC Proto Files

Update the `@dojoengine/grpc` package with the latest proto files from the Torii repository.

## When to Use

Use this skill when:
- Torii has been updated with new RPC methods
- Proto definitions have changed upstream
- New features need to be exposed via gRPC
- Types need to be synchronized with Torii

## Step-by-Step Process

### Step 1: Update Proto Files

```bash
cd packages/grpc && bun run update:proto
```

This downloads the latest proto files from:
- `https://raw.githubusercontent.com/dojoengine/torii/main/crates/proto/proto/`

### Step 2: Review Proto Changes

```bash
git diff packages/grpc/proto/
```

Document what changed:
- New RPC methods
- Modified message types
- New fields on existing types

### Step 3: Rebuild TypeScript Bindings

```bash
cd packages/grpc && bun run build:proto
```

This generates TypeScript from proto files using protobuf-ts.

### Step 4: Identify New RPCs

Compare `src/generated/world.client.ts` with `src/torii-client.ts`:

```typescript
// Generated client interface - IWorldClient
interface IWorldClient {
    subscribeContracts(...): ServerStreamingCall<...>;
    worlds(...): UnaryCall<...>;
    // ... all RPC methods
}
```

Check which methods in `IWorldClient` are not yet wrapped in `ToriiGrpcClient`.

### Step 5: Implement Missing Methods

For each new RPC, follow these patterns:

#### 5a. Add Request Mapper (mappings/query.ts)

```typescript
export function createRetrieveNewThingRequest(
    query: NewThingQuery
): RetrieveNewThingRequest {
    return {
        query: {
            // Map SDK types to proto types
            field: query.field,
            pagination: mapPagination(query.pagination),
        },
    };
}
```

#### 5b. Add Response Mapper (mappings/types.ts)

```typescript
export function mapNewThingResponse(
    response: RetrieveNewThingResponse
): NewThingPage {
    return {
        items: response.items.map(mapNewThing),
        nextCursor: response.next_cursor || undefined,
    };
}

export function mapNewThing(thing: ProtoNewThing): NewThingView {
    return {
        id: thing.id,
        // Map proto fields to SDK types
        address: bufferToHex(thing.address),
    };
}
```

#### 5c. Add Types (types.ts)

```typescript
export interface NewThingView {
    id: string;
    address: string;
}

export interface NewThingPage {
    items: NewThingView[];
    nextCursor?: string;
}
```

#### 5d. Add Client Method (torii-client.ts)

For query methods:
```typescript
async getNewThings(query: NewThingQuery): Promise<NewThingPage> {
    const request = createRetrieveNewThingRequest(query);
    const response = await this.client.worldClient.retrieveNewThings(request).response;
    return this.mappers.newThingsResponse(response);
}
```

For subscription methods:
```typescript
async onNewThingUpdated(
    filters: string[] | null | undefined,
    callback: Function
): Promise<Subscription> {
    return this.createStreamSubscription({
        createStream: () =>
            this.client.worldClient.subscribeNewThings({
                filters: filters?.map(hexToBuffer) || [],
            }),
        onMessage: (response: SubscribeNewThingsResponse) => {
            if (response.thing) {
                callback(
                    this.mappers.newThing(response.thing),
                    response.subscription_id
                );
            }
        },
    });
}
```

For update subscription methods:
```typescript
async updateNewThingSubscription(
    subscription: Subscription,
    filters: string[]
): Promise<void> {
    const grpcSubscription = this.findSubscription(subscription);
    if (!grpcSubscription) {
        throw new Error("Subscription not found");
    }
    await this.client.worldClient.updateNewThingsSubscription({
        subscription_id: BigInt(grpcSubscription.id),
        filters: filters.map(hexToBuffer),
    }).response;
}
```

#### 5e. Export from index.ts

```typescript
export type { NewThingView, NewThingPage } from "./types";
```

### Step 6: Run Tests

```bash
cd packages/grpc && bun run test
```

Add new tests for new methods if needed.

### Step 7: Lint and Format

```bash
cd packages/grpc && bun run lint && bun run format
```

### Step 8: Build Package

```bash
cd packages/grpc && bun run build
```

### Step 9: Create Changeset

```bash
bun run changeset
```

Select `@dojoengine/grpc` and describe the proto updates.

## Key Files Reference

| File | Purpose |
|------|---------|
| `packages/grpc/scripts/update-proto.sh` | Downloads proto from Torii |
| `packages/grpc/scripts/build-proto.sh` | Generates TypeScript |
| `packages/grpc/proto/*.proto` | Proto definitions |
| `packages/grpc/src/generated/world.client.ts` | Generated gRPC client |
| `packages/grpc/src/torii-client.ts` | SDK client implementation |
| `packages/grpc/src/mappings/query.ts` | Request mappers |
| `packages/grpc/src/mappings/types.ts` | Response mappers |
| `packages/grpc/src/types.ts` | SDK type definitions |
| `packages/grpc/src/index.ts` | Package exports |

## Troubleshooting

### Proto download fails
Check network connectivity and verify Torii repo URL is correct.

### Build fails after proto update
Check for breaking changes in proto definitions. May need to update mappers.

### TypeScript errors in generated files
Re-run `bun run build:proto` to regenerate. Check protobuf-ts version compatibility.

### Tests fail
Update tests to match new proto structure. Check mapper implementations.
