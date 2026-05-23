---
name: impl-wrapper
description: Connector wrapper (Impl) class patterns and delegation rules
---

# Impl Wrapper Patterns

## 🚨 CRITICAL RULES

### 1. Impl is ONLY a Wrapper
The `<Service>Impl.ts` class is a thin wrapper that:
- Implements the generated `<Service>Connector` interface
- Delegates ALL actual work to `<Service>Client`
- Contains ZERO business logic
- Contains ZERO HTTP calls
- Contains ZERO authentication logic

**Violation = FAIL**

### 2. Two-Class Pattern is MANDATORY
Every module MUST have both classes:

```
src/
├── <Service>Impl.ts      # Wrapper (implements Connector interface)
└── <Service>Client.ts    # Real implementation (connection, HTTP, auth)
```

**Why:**
- `<Service>Impl` satisfies the Connector interface contract
- `<Service>Client` does the actual work
- Separation of concerns: interface vs implementation
- `Impl` provides metadata(), isSupported() - framework requirements
- `Client` does connect(), API calls, state management

### 3. Required Impl Methods
`<Service>Impl` MUST implement these methods (from Connector interface):

```typescript
// Framework methods (Impl implements directly)
metadata(): Promise<ConnectionMetadata>
isSupported(operationId: string): Promise<OperationSupportStatusDef>

// Delegated methods (pass through to Client)
connect(profile: ConnectionProfile): Promise<ConnectionState>
refresh(profile: ConnectionProfile, state: ConnectionState): Promise<ConnectionState>
isConnected(): Promise<boolean>
disconnect(): Promise<void>

// Producer getters (lazy initialization + wrapping)
get<Resource>Api(): <Resource>Api
```

## 🟡 STANDARD RULES

### Impl Class Structure

**Standard template:**

```typescript
import {
  <Service>Connector,
  <Resource>Api,
  wrap<Resource>Producer
} from '../generated/api';
import { ConnectionProfile } from '../generated/model/ConnectionProfile';
import {
  ConnectionMetadata,
  OperationSupportStatus,
  OperationSupportStatusDef,
  ConnectionStatus
} from '@zerobias-org/types-core-js';
import { <Service>Client } from './<Service>Client';
import { <Resource>ProducerApiImpl } from './<Resource>ProducerApiImpl';
import { ConnectionState } from '../generated/model';

export class <Service>Impl implements <Service>Connector {
  private client: <Service>Client;
  private userApiProducer?: <Resource>Api;

  constructor() {
    this.client = new <Service>Client();
  }

  // ========================================
  // Framework Methods (Impl implements)
  // ========================================

  async metadata(): Promise<ConnectionMetadata> {
    // ALWAYS return ConnectionStatus.Down - replaced by platform
    return new ConnectionMetadata(ConnectionStatus.Down);
  }

  async isSupported(operationId: string): Promise<OperationSupportStatusDef> {
    // ALWAYS return OperationSupportStatus.Maybe - replaced by platform
    return OperationSupportStatus.Maybe;
  }

  // ========================================
  // Connection Methods (Delegate to Client)
  // ========================================

  async connect(connectionProfile: ConnectionProfile): Promise<ConnectionState> {
    return this.client.connect(connectionProfile);
  }

  async refresh(
    connectionProfile: ConnectionProfile,
    connectionState: ConnectionState
  ): Promise<ConnectionState> {
    return this.client.refresh(connectionProfile, connectionState);
  }

  async isConnected(): Promise<boolean> {
    return this.client.isConnected();
  }

  async disconnect(): Promise<void> {
    return this.client.disconnect();
  }

  // ========================================
  // Producer Getters (Lazy init + wrap)
  // ========================================

  get<Resource>Api(): <Resource>Api {
    if (!this.userApiProducer) {
      const producer = new <Resource>ProducerApiImpl(this.client);
      this.userApiProducer = wrap<Resource>Producer(producer);
    }
    return this.userApiProducer;
  }
}
```

### Client Class Structure

**Standard template:**

```typescript
import axios, { AxiosInstance } from 'axios';
import {
  InvalidCredentialsError,
  UnauthorizedError,
  NotConnectedError
} from '@zerobias-org/types-core-js';
import { ConnectionProfile } from '../generated/model/ConnectionProfile';
import { ConnectionState } from '../generated/model';

export class <Service>Client {
  private httpClient: AxiosInstance | null = null;
  private connected = false;
  private baseUrl = 'https://api.service.com';
  private accessToken: string | null = null;

  async connect(profile: ConnectionProfile): Promise<ConnectionState> {
    // Validate credentials
    if (!profile.apiKey) {
      throw new InvalidCredentialsError();
    }

    // Create HTTP client
    this.httpClient = axios.create({
      baseURL: this.baseUrl,
      headers: {
        Authorization: `Bearer ${profile.apiKey}`
      }
    });

    // Test connection
    try {
      await this.httpClient.get('/auth/test');
      this.connected = true;
      this.accessToken = profile.apiKey;

      return {
        accessToken: this.accessToken
      };
    } catch (error) {
      throw new InvalidCredentialsError();
    }
  }

  async refresh(
    profile: ConnectionProfile,
    state: ConnectionState
  ): Promise<ConnectionState> {
    // Implement token refresh if supported
    throw new Error('Refresh not supported');
  }

  async isConnected(): Promise<boolean> {
    return this.connected && this.httpClient !== null;
  }

  async disconnect(): Promise<void> {
    this.httpClient = null;
    this.connected = false;
    this.accessToken = null;
  }

  getHttpClient(): AxiosInstance {
    if (!this.httpClient) {
      throw new NotConnectedError();
    }
    return this.httpClient;
  }
}
```

### Delegation Pattern

**Every connection/producer method in Impl MUST delegate to Client:**

```typescript
// ✅ CORRECT: Simple delegation
async connect(profile: ConnectionProfile): Promise<ConnectionState> {
  return this.client.connect(profile);
}

// ❌ WRONG: Business logic in Impl
async connect(profile: ConnectionProfile): Promise<ConnectionState> {
  if (!profile.apiKey) {
    throw new InvalidCredentialsError();
  }
  return this.client.connect(profile);
}

// ✅ CORRECT: Validation in Client
// <Service>Client.ts
async connect(profile: ConnectionProfile): Promise<ConnectionState> {
  if (!profile.apiKey) {
    throw new InvalidCredentialsError();
  }
  // ... rest of connection logic
}
```

### Producer Getter Pattern

**Lazy initialization + wrapping:**

```typescript
export class ServiceImpl implements ServiceConnector {
  private client: ServiceClient;
  private userApiProducer?: UserApi;
  private groupApiProducer?: GroupApi;

  constructor() {
    this.client = new ServiceClient();
  }

  getUserApi(): UserApi {
    if (!this.userApiProducer) {
      // 1. Create implementation
      const producer = new UserProducerApiImpl(this.client);

      // 2. Wrap with generated wrapper
      this.userApiProducer = wrapUserProducer(producer);
    }
    return this.userApiProducer;
  }

  getGroupApi(): GroupApi {
    if (!this.groupApiProducer) {
      const producer = new GroupProducerApiImpl(this.client);
      this.groupApiProducer = wrapGroupProducer(producer);
    }
    return this.groupApiProducer;
  }
}
```

**Why:**
- Lazy initialization - only create when needed
- Wrap producer with generated wrapper (adds error handling, logging)
- Cache wrapped instance - don't recreate on each call
- Pass Client to producer - producer uses Client's httpClient

### Framework Methods (Impl-Specific)

#### metadata() Method

```typescript
async metadata(): Promise<ConnectionMetadata> {
  // ALWAYS return ConnectionStatus.Down
  // The platform replaces this with real status
  return new ConnectionMetadata(ConnectionStatus.Down);
}
```

**Rules:**
- ✅ ALWAYS return `new ConnectionMetadata(ConnectionStatus.Down)`
- ❌ NEVER try to determine real connection status here
- ❌ NEVER call Client methods from metadata()
- **Why:** Platform handles metadata, this is just a placeholder

#### isSupported() Method

```typescript
async isSupported(operationId: string): Promise<OperationSupportStatusDef> {
  // ALWAYS return OperationSupportStatus.Maybe
  // The platform replaces this with real support status
  return OperationSupportStatus.Maybe;
}
```

**Rules:**
- ✅ ALWAYS return `OperationSupportStatus.Maybe`
- ❌ NEVER try to determine operation support here
- ❌ NEVER use the operationId parameter
- **Why:** Platform handles operation support, this is just a placeholder

### Impl Constructor

**Standard constructor:**

```typescript
export class ServiceImpl implements ServiceConnector {
  private client: ServiceClient;
  private userApiProducer?: UserApi;
  // ... other producer caches

  constructor() {
    this.client = new ServiceClient();
  }
}
```

**Rules:**
- ✅ Create Client instance
- ✅ Initialize producer caches as undefined
- ❌ NEVER accept parameters
- ❌ NEVER perform initialization logic
- ❌ NEVER make async calls
- **Why:** Factory function creates Impl, constructor should be simple

## 🟢 GUIDELINES

### When to Add Logic to Impl vs Client

**Add to Impl:**
- ❌ Never (Impl should only delegate)

**Add to Client:**
- ✅ Connection logic
- ✅ Authentication
- ✅ HTTP client creation
- ✅ Token refresh
- ✅ State management
- ✅ Error handling
- ✅ Credential validation

**Impl is dumb delegation, Client is smart implementation**

### Producer Impl Pattern

Producers also delegate to Client:

```typescript
// UserProducerApiImpl.ts
export class UserProducerApiImpl implements UserProducer {
  constructor(private client: ServiceClient) {}

  async listUsers(): Promise<UserResponse> {
    const httpClient = this.client.getHttpClient();
    const response = await httpClient.get('/users');
    return mapToUserResponse(response.data);
  }
}
```

**Pattern:**
1. Producer receives Client in constructor
2. Producer calls `client.getHttpClient()` to get axios instance
3. Producer makes HTTP calls
4. Producer maps responses

### Error Handling

**Client handles errors:**

```typescript
// ServiceClient.ts
export class ServiceClient {
  private static handleError(error: AxiosError): never {
    const status = error.response?.status || 500;

    switch (status) {
      case 401:
        throw new InvalidCredentialsError();
      case 403:
        throw new UnauthorizedError();
      case 404:
        throw new NoSuchObjectError('resource', 'unknown');
      default:
        throw new UnexpectedError(error.message, status);
    }
  }

  async connect(profile: ConnectionProfile): Promise<ConnectionState> {
    try {
      // ... connection logic
    } catch (error) {
      if (axios.isAxiosError(error)) {
        ServiceClient.handleError(error);
      }
      throw new InvalidCredentialsError();
    }
  }
}
```

**Impl does NOT handle errors:**

```typescript
// ServiceImpl.ts
async connect(profile: ConnectionProfile): Promise<ConnectionState> {
  // Just delegate - Client handles errors
  return this.client.connect(profile);
}
```

### Naming Conventions

**Files:**
- `<Service>Impl.ts` - Wrapper class
- `<Service>Client.ts` - Implementation class
- `<Resource>ProducerApiImpl.ts` - Producer implementation

**Classes:**
- `<Service>Impl` - Implements `<Service>Connector`
- `<Service>Client` - No interface (internal implementation)
- `<Resource>ProducerApiImpl` - Implements `<Resource>Producer`

**Examples:**
- `AccessImpl.ts` / `AccessClient.ts`
- `GitHubImpl.ts` / `GitHubClient.ts`
- `UserProducerApiImpl.ts`

## Validation

### Check Impl File Structure
```bash
# Check Impl file exists
IMPL_FILE=$(find src -name "*Impl.ts" -not -name "*ProducerApiImpl.ts" | head -1)

if [ -n "$IMPL_FILE" ]; then
  echo "✅ PASS: Found Impl file: $IMPL_FILE"
else
  echo "❌ FAIL: No Impl file found"
  exit 1
fi

# Check Client file exists
CLIENT_FILE=$(find src -name "*Client.ts" | head -1)

if [ -n "$CLIENT_FILE" ]; then
  echo "✅ PASS: Found Client file: $CLIENT_FILE"
else
  echo "❌ FAIL: No Client file found"
  exit 1
fi
```

### Check Impl Implements Connector
```bash
# Check Impl implements Connector interface
if [ -n "$IMPL_FILE" ]; then
  if grep -q "implements.*Connector" "$IMPL_FILE"; then
    echo "✅ PASS: Impl implements Connector"
  else
    echo "❌ FAIL: Impl must implement Connector interface"
    exit 1
  fi
fi
```

### Check Required Methods
```bash
# Check Impl has required methods
REQUIRED_METHODS=(
  "metadata()"
  "isSupported("
  "connect("
  "disconnect()"
  "isConnected()"
)

MISSING=0
for method in "${REQUIRED_METHODS[@]}"; do
  if grep -q "$method" "$IMPL_FILE"; then
    echo "  ✅ $method"
  else
    echo "  ❌ Missing: $method"
    MISSING=1
  fi
done

if [ $MISSING -eq 0 ]; then
  echo "✅ PASS: All required methods present"
fi
```

### Check Delegation Pattern
```bash
# Check Impl delegates to client
DELEGATION_COUNT=$(grep -c "this.client\." "$IMPL_FILE" 2>/dev/null || echo "0")

if [ "$DELEGATION_COUNT" -ge 3 ]; then
  echo "✅ PASS: Impl delegates to client ($DELEGATION_COUNT calls)"
else
  echo "⚠️ WARN: Only $DELEGATION_COUNT delegation calls found"
fi
```

### Check No Business Logic in Impl
```bash
# Check Impl doesn't have axios imports (should be in Client)
if grep -q "import.*axios" "$IMPL_FILE"; then
  echo "❌ FAIL: Impl should not import axios (use Client)"
  exit 1
else
  echo "✅ PASS: No axios imports in Impl"
fi

# Check Impl doesn't make HTTP calls
if grep -q "\.get(\|\.post(\|\.put(\|\.delete(" "$IMPL_FILE"; then
  echo "❌ FAIL: Impl should not make HTTP calls (use Client)"
  exit 1
else
  echo "✅ PASS: No HTTP calls in Impl"
fi
```

### Check Client Has Connection Logic
```bash
# Check Client has axios
if grep -q "import.*axios" "$CLIENT_FILE"; then
  echo "✅ PASS: Client imports axios"
else
  echo "⚠️ WARN: Client should import axios"
fi

# Check Client has connection logic
if grep -q "async connect(" "$CLIENT_FILE"; then
  echo "✅ PASS: Client has connect method"
else
  echo "❌ FAIL: Client missing connect method"
  exit 1
fi

# Check Client has getHttpClient
if grep -q "getHttpClient()" "$CLIENT_FILE"; then
  echo "✅ PASS: Client has getHttpClient method"
else
  echo "❌ FAIL: Client should have getHttpClient method"
fi
```

### Complete Validation Script
```bash
#!/bin/bash
# validate-impl-client.sh - Validate Impl/Client pattern

echo "=== Impl/Client Pattern Validation ==="
echo ""

# Find files
IMPL_FILE=$(find src -name "*Impl.ts" -not -name "*ProducerApiImpl.ts" | head -1)
CLIENT_FILE=$(find src -name "*Client.ts" | head -1)

if [ -z "$IMPL_FILE" ]; then
  echo "❌ FAIL: No Impl file found"
  exit 1
fi

if [ -z "$CLIENT_FILE" ]; then
  echo "❌ FAIL: No Client file found"
  exit 1
fi

echo "Impl file: $IMPL_FILE"
echo "Client file: $CLIENT_FILE"
echo ""

ERRORS=0

# 1. Check Impl implements Connector
echo "1. Impl Interface:"
if grep -q "implements.*Connector" "$IMPL_FILE"; then
  echo "  ✅ Implements Connector"
else
  echo "  ❌ Must implement Connector"
  ERRORS=$((ERRORS + 1))
fi
echo ""

# 2. Check required methods
echo "2. Required Methods:"
METHODS=("metadata()" "isSupported(" "connect(" "disconnect()" "isConnected()")
for method in "${METHODS[@]}"; do
  if grep -q "$method" "$IMPL_FILE"; then
    echo "  ✅ $method"
  else
    echo "  ❌ $method (missing)"
    ERRORS=$((ERRORS + 1))
  fi
done
echo ""

# 3. Check delegation
echo "3. Delegation Pattern:"
DELEGATION=$(grep -c "this.client\." "$IMPL_FILE" 2>/dev/null || echo "0")
if [ "$DELEGATION" -ge 3 ]; then
  echo "  ✅ Delegates to client ($DELEGATION times)"
else
  echo "  ⚠️  Limited delegation ($DELEGATION times)"
fi
echo ""

# 4. Check no business logic in Impl
echo "4. Impl Purity:"
if grep -q "import.*axios" "$IMPL_FILE"; then
  echo "  ❌ Impl imports axios (should use Client)"
  ERRORS=$((ERRORS + 1))
else
  echo "  ✅ No axios in Impl"
fi

if grep -q "\.get(\|\.post(\|\.put(\|\.delete(" "$IMPL_FILE"; then
  echo "  ❌ Impl makes HTTP calls (should use Client)"
  ERRORS=$((ERRORS + 1))
else
  echo "  ✅ No HTTP calls in Impl"
fi
echo ""

# 5. Check Client has implementation
echo "5. Client Implementation:"
if grep -q "import.*axios" "$CLIENT_FILE"; then
  echo "  ✅ Client imports axios"
else
  echo "  ⚠️  Client should import axios"
fi

if grep -q "async connect(" "$CLIENT_FILE"; then
  echo "  ✅ Client has connect method"
else
  echo "  ❌ Client missing connect method"
  ERRORS=$((ERRORS + 1))
fi

if grep -q "getHttpClient()" "$CLIENT_FILE"; then
  echo "  ✅ Client has getHttpClient"
else
  echo "  ⚠️  Client should have getHttpClient"
fi
echo ""

# Summary
if [ $ERRORS -eq 0 ]; then
  echo "=== ✅ VALIDATION PASSED ==="
  exit 0
else
  echo "=== ❌ VALIDATION FAILED ($ERRORS errors) ==="
  exit 1
fi
```

## Common Issues

### Issue: Impl has business logic
**Problem:**
```typescript
// ServiceImpl.ts ❌ WRONG
async connect(profile: ConnectionProfile): Promise<ConnectionState> {
  if (!profile.apiKey) {
    throw new InvalidCredentialsError();
  }
  return this.client.connect(profile);
}
```

**Solution:**
```typescript
// ServiceImpl.ts ✅ CORRECT
async connect(profile: ConnectionProfile): Promise<ConnectionState> {
  return this.client.connect(profile);
}

// ServiceClient.ts ✅ CORRECT
async connect(profile: ConnectionProfile): Promise<ConnectionState> {
  if (!profile.apiKey) {
    throw new InvalidCredentialsError();
  }
  // ... connection logic
}
```

### Issue: Impl makes HTTP calls
**Problem:**
```typescript
// ServiceImpl.ts ❌ WRONG
getUserApi(): UserApi {
  return {
    listUsers: async () => {
      const response = await axios.get('/users');
      return response.data;
    }
  };
}
```

**Solution:**
```typescript
// ServiceImpl.ts ✅ CORRECT
getUserApi(): UserApi {
  if (!this.userApiProducer) {
    const producer = new UserProducerApiImpl(this.client);
    this.userApiProducer = wrapUserProducer(producer);
  }
  return this.userApiProducer;
}

// UserProducerApiImpl.ts ✅ CORRECT
async listUsers(): Promise<UserResponse> {
  const httpClient = this.client.getHttpClient();
  const response = await httpClient.get('/users');
  return mapToUserResponse(response.data);
}
```

### Issue: Producer not wrapped
**Problem:**
```typescript
getUserApi(): UserApi {
  if (!this.userApiProducer) {
    this.userApiProducer = new UserProducerApiImpl(this.client);  // ❌ Not wrapped
  }
  return this.userApiProducer;
}
```

**Solution:**
```typescript
getUserApi(): UserApi {
  if (!this.userApiProducer) {
    const producer = new UserProducerApiImpl(this.client);
    this.userApiProducer = wrapUserProducer(producer);  // ✅ Wrapped
  }
  return this.userApiProducer;
}
```

### Issue: metadata() tries to return real status
**Problem:**
```typescript
async metadata(): Promise<ConnectionMetadata> {
  const isConnected = await this.client.isConnected();  // ❌ WRONG
  const status = isConnected ? ConnectionStatus.Up : ConnectionStatus.Down;
  return new ConnectionMetadata(status);
}
```

**Solution:**
```typescript
async metadata(): Promise<ConnectionMetadata> {
  // ✅ ALWAYS return Down - platform handles this
  return new ConnectionMetadata(ConnectionStatus.Down);
}
```

## Anti-Patterns

### ❌ BAD: Single class (no separation)
```typescript
// ServiceImpl.ts - doing everything
export class ServiceImpl implements ServiceConnector {
  private httpClient?: AxiosInstance;

  async connect(profile: ConnectionProfile) {
    this.httpClient = axios.create({ /* ... */ });
    // ... connection logic in Impl
  }
}
```

### ✅ GOOD: Separate Impl and Client
```typescript
// ServiceImpl.ts - wrapper
export class ServiceImpl implements ServiceConnector {
  private client: ServiceClient;
  async connect(profile: ConnectionProfile) {
    return this.client.connect(profile);
  }
}

// ServiceClient.ts - implementation
export class ServiceClient {
  private httpClient?: AxiosInstance;
  async connect(profile: ConnectionProfile) {
    this.httpClient = axios.create({ /* ... */ });
  }
}
```

### ❌ BAD: Impl without Client
```typescript
// Only ServiceImpl.ts exists
export class ServiceImpl implements ServiceConnector {
  // Everything in one class
}
```

### ✅ GOOD: Both Impl and Client
```typescript
// ServiceImpl.ts + ServiceClient.ts
// Clear separation of concerns
```
