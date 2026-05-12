# State Diagrams Reference

State diagrams model state machines -- lifecycle management, workflow states, session handling, and protocol states.

**Keyword:** `stateDiagram-v2` (always use v2 for modern syntax)

---

## Basic States

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Processing : start
    Processing --> Complete : finish
    Complete --> [*]
```

- `[*]` -- Start state (initial) or end state (final)
- `-->` -- Transition arrow
- `: label` -- Transition trigger/event

---

## State Descriptions

Add descriptions inside states:

```
state "Waiting for approval" as Waiting
```

Or with line breaks:

```mermaid
stateDiagram-v2
    state "Order Placed\n(awaiting payment)" as Placed
    [*] --> Placed
```

---

## Composite (Nested) States

States can contain sub-states:

```mermaid
stateDiagram-v2
    [*] --> Active

    state Active {
        [*] --> Running
        Running --> Paused : pause
        Paused --> Running : resume
    }

    Active --> Terminated : kill
    Terminated --> [*]
```

### Deeply Nested

```mermaid
stateDiagram-v2
    [*] --> First

    state First {
        [*] --> Second

        state Second {
            [*] --> third
            third --> third : loop
        }
    }
```

---

## Choice (Conditional Branching)

```mermaid
stateDiagram-v2
    state check <<choice>>

    [*] --> Validating
    Validating --> check
    check --> Approved : if valid
    check --> Rejected : if invalid
    Approved --> [*]
    Rejected --> [*]
```

---

## Fork and Join (Parallel States)

```mermaid
stateDiagram-v2
    state fork_state <<fork>>
    state join_state <<join>>

    [*] --> fork_state
    fork_state --> TaskA
    fork_state --> TaskB
    fork_state --> TaskC
    TaskA --> join_state
    TaskB --> join_state
    TaskC --> join_state
    join_state --> Complete
    Complete --> [*]
```

---

## Concurrent Regions

Use `--` to separate concurrent state regions within a composite state:

```mermaid
stateDiagram-v2
    [*] --> Active

    state Active {
        [*] --> NetworkConnected
        NetworkConnected --> NetworkDisconnected : disconnect
        NetworkDisconnected --> NetworkConnected : reconnect
        --
        [*] --> LoggedOut
        LoggedOut --> LoggedIn : login
        LoggedIn --> LoggedOut : logout
    }
```

---

## Notes

```
note right of StateName
    This is a note about the state.
    It can span multiple lines.
end note

note left of StateName : Short note
```

---

## Direction

```
stateDiagram-v2
    direction LR
```

Options: `TB` (default), `BT`, `LR`, `RL`

---

## Styling

### State-level styling via classDef

```mermaid
stateDiagram-v2
    [*] --> Active
    Active --> Inactive : deactivate

    classDef active fill:#dcfce7,stroke:#16a34a,color:#000
    classDef inactive fill:#fee2e2,stroke:#dc2626,color:#000

    class Active active
    class Inactive inactive
```

---

## Complete Examples

### Order Lifecycle

```mermaid
stateDiagram-v2
    direction LR

    [*] --> Draft

    state "Order Processing" as Processing {
        Draft --> Submitted : submit
        Submitted --> Confirmed : confirm

        state payment_check <<choice>>
        Confirmed --> payment_check
        payment_check --> Paid : payment success
        payment_check --> PaymentFailed : payment failed
        PaymentFailed --> Confirmed : retry
    }

    Paid --> Fulfilling

    state Fulfilling {
        [*] --> Picking
        Picking --> Packing : picked
        Packing --> Shipped : packed
    }

    Shipped --> Delivered : deliver
    Delivered --> [*]

    Draft --> Cancelled : cancel
    Submitted --> Cancelled : cancel
    Confirmed --> Cancelled : cancel
    Cancelled --> [*]

    classDef active fill:#dbeafe,stroke:#2563eb,color:#000
    classDef success fill:#dcfce7,stroke:#16a34a,color:#000
    classDef danger fill:#fee2e2,stroke:#dc2626,color:#000

    class Draft,Submitted,Confirmed,Paid active
    class Delivered success
    class Cancelled,PaymentFailed danger
```

### Authentication Session

```mermaid
stateDiagram-v2
    [*] --> Unauthenticated

    Unauthenticated --> Authenticating : login attempt

    state Authenticating {
        [*] --> ValidatingCredentials
        ValidatingCredentials --> CheckingMFA : credentials valid

        state mfa_check <<choice>>
        CheckingMFA --> mfa_check
        mfa_check --> MFARequired : MFA enabled
        mfa_check --> Authenticated : MFA not required

        MFARequired --> ValidatingMFA : submit code
        ValidatingMFA --> Authenticated : code valid
        ValidatingMFA --> MFARequired : code invalid (retry)
    }

    state Authenticated {
        [*] --> Active
        Active --> Idle : timeout
        Idle --> Active : activity
        --
        [*] --> TokenValid
        TokenValid --> TokenExpiring : near expiry
        TokenExpiring --> TokenValid : refresh
        TokenExpiring --> TokenExpired : timeout
    }

    Authenticated --> Unauthenticated : logout
    TokenExpired --> Unauthenticated : force logout
    ValidatingCredentials --> Unauthenticated : invalid

    classDef good fill:#dcfce7,stroke:#16a34a,color:#000
    classDef warn fill:#fef3c7,stroke:#d97706,color:#000
    classDef bad fill:#fee2e2,stroke:#dc2626,color:#000

    class Active,TokenValid good
    class Idle,TokenExpiring,MFARequired warn
    class Unauthenticated,TokenExpired bad
```
