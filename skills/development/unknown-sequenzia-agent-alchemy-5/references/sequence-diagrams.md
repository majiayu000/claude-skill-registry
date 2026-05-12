# Sequence Diagrams Reference

Sequence diagrams visualize interactions between components over time -- API calls, message passing, authentication flows, and protocol exchanges.

**Keyword:** `sequenceDiagram`

---

## Participants and Actors

### Participants (box shape)

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant D as Database
    C->>S: Request
    S->>D: Query
```

### Actors (person shape)

```mermaid
sequenceDiagram
    actor U as User
    participant S as System
    U->>S: Interact
```

Participants appear in the order they are declared. Use `as` for short aliases.

---

## Message Types

| Syntax | Description | Use For |
|--------|-------------|---------|
| `A->>B: msg` | Solid arrow | Synchronous request |
| `A-->>B: msg` | Dotted arrow | Asynchronous response |
| `A-xB: msg` | Solid cross | Failed/rejected message |
| `A--xB: msg` | Dotted cross | Failed async response |
| `A-)B: msg` | Solid open | Async fire-and-forget |
| `A--)B: msg` | Dotted open | Async notification |

---

## Activation

Show when a participant is actively processing:

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server

    C->>S: POST /api/data
    activate S
    S-->>C: 201 Created
    deactivate S
```

### Shorthand with `+` / `-`

```
C->>+S: Request     %% activates S
S-->>-C: Response   %% deactivates S
```

### Nested Activation

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant D as Database

    C->>+S: Request
    S->>+D: Query
    D-->>-S: Results
    S-->>-C: Response
```

---

## Control Structures

### alt / else -- Conditional

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server

    C->>S: GET /resource/123
    alt Found
        S-->>C: 200 OK + data
    else Not Found
        S-->>C: 404 Not Found
    end
```

### opt -- Optional

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant Cache as Cache

    C->>S: Request
    opt Cache available
        S->>Cache: Check cache
        Cache-->>S: Cached result
    end
    S-->>C: Response
```

### loop -- Repetition

```mermaid
sequenceDiagram
    participant W as Worker
    participant Q as Queue

    loop Every 5 seconds
        W->>Q: Poll for messages
        Q-->>W: Messages (if any)
    end
```

### par -- Parallel

```mermaid
sequenceDiagram
    participant C as Client
    participant A as Service A
    participant B as Service B

    par Fetch data
        C->>A: GET /users
        A-->>C: User list
    and
        C->>B: GET /products
        B-->>C: Product list
    end
```

### critical -- Critical Region

```mermaid
sequenceDiagram
    participant S as Server
    participant D as Database

    critical Acquire lock
        S->>D: BEGIN TRANSACTION
        S->>D: UPDATE accounts
        S->>D: COMMIT
    option Lock timeout
        S->>D: ROLLBACK
    end
```

### break -- Early Exit

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server

    C->>S: Request
    break Invalid token
        S-->>C: 401 Unauthorized
    end
    S-->>C: 200 OK
```

---

## Notes

```
Note right of A: Single participant note
Note left of A: Left-side note
Note over A: Above participant
Note over A,B: Spanning multiple participants
```

---

## Autonumber

Add sequential numbers to all messages:

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant S as Server
    C->>S: Step 1
    S-->>C: Step 2
    C->>S: Step 3
```

---

## Styling

### Participant colors

Use `box` to group and color participants:

```mermaid
sequenceDiagram
    box rgb(219, 234, 254) Frontend
        participant C as Client
    end
    box rgb(243, 232, 255) Backend
        participant S as Server
        participant D as Database
    end
    C->>S: Request
    S->>D: Query
```

---

## Complete Examples

### OAuth2 Authorization Code Flow

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant C as Client App
    participant A as Auth Server
    participant R as Resource Server

    U->>C: Click "Login"
    C->>A: Redirect to /authorize
    A->>U: Show login form
    U->>A: Enter credentials
    alt Valid credentials
        A-->>C: Redirect with auth code
        C->>+A: POST /token (code + secret)
        A-->>-C: Access token + refresh token
        C->>+R: GET /api/data (Bearer token)
        R-->>-C: Protected resource
        C-->>U: Display data
    else Invalid credentials
        A-->>U: Show error
    end
```

### Microservice Request with Fallback

```mermaid
sequenceDiagram
    autonumber
    participant GW as API Gateway
    participant Auth as Auth Service
    participant US as User Service
    participant Cache as Redis Cache
    participant DB as PostgreSQL

    GW->>+Auth: Validate token
    Auth-->>-GW: Token valid

    GW->>+US: GET /users/123
    US->>+Cache: Get user:123
    alt Cache hit
        Cache-->>-US: Cached user data
    else Cache miss
        Cache-->>US: null
        US->>+DB: SELECT * FROM users WHERE id=123
        DB-->>-US: User record
        US-)Cache: SET user:123 (async)
    end
    US-->>-GW: User data
```
