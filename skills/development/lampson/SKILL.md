---
name: lampson-system-design
description: Design systems using Butler Lampson's principles of abstraction, interfaces, and practical wisdom. Emphasizes clean abstractions, security foundations, and time-tested design hints. Use when making architectural decisions, designing APIs, or building systems that must evolve over decades.
---

# Butler Lampson Style Guide

## Overview

Butler Lampson is the architect's architect. He contributed to the Xerox Alto (first personal computer with GUI), laser printing, Ethernet, two-phase commit, capability-based security, and compiler optimization. His "Hints for Computer System Design" is required reading for every systems engineer. Turing Award winner (1992).

## Core Philosophy

> "All problems in computer science can be solved by another level of indirection... except for the problem of too many layers of indirection."

> "Do one thing at a time, and do it well."

> "Keep secrets of the implementation from the user of the abstraction."

## Design Principles

1. **Abstraction is Power**: Good abstractions hide complexity, reveal intent, and enable change. Bad abstractions leak details and create coupling.

2. **Interfaces are Forever**: Implementation can change; interfaces cannot. Design interfaces for the long term.

3. **Simplicity is Prerequisite**: Simple systems are easier to build, debug, understand, and extend. Complexity is the enemy.

4. **Security as Architecture**: Security cannot be bolted on. It must be designed in from the beginning, at the right abstraction level.

5. **Make it Work, Make it Right, Make it Fast**: In that order. Premature optimization creates complexity that prevents correctness.

## Hints for Computer System Design

Lampson's famous hints, organized by goal:

### Functionality (Does it work?)

| Hint | Meaning |
|------|---------|
| **Separate normal and worst case** | Optimize for common case; handle edge cases separately |
| **Do one thing well** | Don't generalize beyond what's needed |
| **Don't hide power** | Let users access underlying capabilities when needed |
| **Use procedure arguments** | Parameterize behavior, not just data |
| **Leave it to the client** | Don't do things the client can do better |
| **Keep secrets** | Hide implementation from interface |
| **Divide and conquer** | Split problems into independent parts |

### Speed (Is it fast?)

| Hint | Meaning |
|------|---------|
| **Split resources orthogonally** | Avoid contention through independence |
| **Safety first, then optimize** | Correct code before fast code |
| **Use static analysis** | Catch errors at compile time |
| **Dynamic translation** | Optimize hot paths at runtime |
| **Cache answers** | Reuse expensive computations |
| **Use hints** | Use approximate information to speed common cases |
| **Batch processing** | Amortize fixed costs over many operations |

### Fault Tolerance (Does it recover?)

| Hint | Meaning |
|------|---------|
| **End-to-end** | Only end-to-end checks guarantee correctness |
| **Log updates** | Write-ahead logging enables recovery |
| **Make actions atomic** | All-or-nothing simplifies recovery |
| **Replicate for availability** | Redundancy survives failures |

## When Designing Systems

### Always

- Define interfaces before implementation
- Document what the abstraction guarantees (and doesn't)
- Design for the common case first
- Make operations atomic or idempotent
- Use capabilities for security when possible
- Consider how the system will evolve over 10 years
- Hide implementation details aggressively

### Never

- Expose internal state through interfaces
- Add features "just in case"
- Design security as an afterthought
- Optimize before measuring
- Create abstractions that leak
- Let optimization compromise correctness

### Prefer

- Simple interfaces over flexible ones
- Composition over inheritance
- Stateless protocols over stateful
- Explicit over implicit behavior
- Capabilities over access control lists
- Failure isolation over shared fate

## Key Concepts

### The Power of Indirection

```text
Every problem can be solved by adding a layer of indirection:

Physical → Virtual Memory      (hide memory management)
Files → Database               (hide storage layout)
Sockets → HTTP                 (hide network details)
Threads → Actors               (hide concurrency)

But each layer has costs:
- Performance overhead
- Debugging complexity
- Learning curve
- Potential abstraction leaks

Add indirection only when the abstraction is valuable.
```

### End-to-End Argument

```text
The end-to-end argument (Saltzer, Reed, Clark—influenced by Lampson):

Low-level mechanisms (checksums, retries) can't guarantee 
correctness; only end-to-end verification can.

Example: File transfer
- Network checksums catch bit errors
- BUT: disk corruption, software bugs, truncation can still occur
- ONLY end-to-end verification (hash of complete file) guarantees integrity

Implication: Implement reliability at the ends, 
not in the middle layers.
```

### Capability-Based Security

```text
Traditional: Ask "Who are you?" then check permissions
Capabilities: "Here's a token that grants specific rights"

Capability advantages:
- Principle of least privilege is natural
- Delegation is simple (pass the capability)
- No confused deputy problem
- Revocation is possible (revoke the capability)

Example:
  // ACL approach: check caller identity
  if (user.canAccessFile(path)) {
    read(path)  // might be wrong path
  }
  
  // Capability approach: token IS permission
  let file = openFile(path)  // get capability
  read(file)                  // can only read what was granted
```

### Interface Design

```text
Good interfaces:
1. Are minimal (no unnecessary operations)
2. Are complete (can do everything needed)
3. Have clear semantics (behavior is obvious)
4. Are consistent (similar things work similarly)
5. Hide implementation (can change underneath)

Questions to ask:
- What invariants does this interface maintain?
- What can't be done with this interface?
- How will this interface evolve?
- What errors can occur?
```

## Code Patterns

### Abstraction Boundaries

```python
class StorageEngine(Protocol):
    """
    Interface for storage backends.
    
    Lampson's principle: Keep secrets of implementation.
    Users see only this interface, never the implementation.
    """
    
    def get(self, key: bytes) -> Optional[bytes]:
        """Retrieve value for key, or None if not found."""
        ...
    
    def put(self, key: bytes, value: bytes) -> None:
        """Store value at key. Atomic and durable."""
        ...
    
    def delete(self, key: bytes) -> bool:
        """Delete key. Returns True if key existed."""
        ...
    
    # Note: NO methods exposing implementation details like:
    # - flush_cache()      # Exposes caching strategy
    # - get_file_handle()  # Exposes file-based storage
    # - set_block_size()   # Exposes storage layout
```

### Separate Normal and Worst Case

```python
def get_user(user_id: str) -> User:
    """
    Lampson's hint: Separate normal and worst case.
    
    Fast path: user in cache (99% of requests)
    Slow path: fetch from database
    """
    # Normal case: fast, simple, optimized
    if user := cache.get(user_id):
        return user
    
    # Worst case: slower, but still correct
    user = database.fetch_user(user_id)
    if user:
        cache.set(user_id, user, ttl=300)
    return user

# The normal case is optimized for speed.
# The worst case is handled correctly but separately.
```

### Capability Pattern

```python
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class FileCapability:
    """
    A capability grants specific rights to a specific resource.
    
    Lampson's security model: capabilities over ACLs.
    """
    path: str
    can_read: bool
    can_write: bool
    can_delete: bool
    
    def read(self) -> bytes:
        if not self.can_read:
            raise PermissionError("Read not permitted")
        return _read_file(self.path)
    
    def write(self, data: bytes) -> None:
        if not self.can_write:
            raise PermissionError("Write not permitted")
        _write_file(self.path, data)
    
    def attenuate(self, can_read=None, can_write=None) -> 'FileCapability':
        """
        Create a weaker capability from this one.
        Can only remove rights, never add them.
        """
        return FileCapability(
            path=self.path,
            can_read=can_read if can_read is not None else self.can_read,
            can_write=can_write if can_write is not None else self.can_write,
            can_delete=False  # Never delegate delete
        )

# Usage: Pass capabilities, not identity
def process_file(file_cap: FileCapability):
    data = file_cap.read()  # Can only do what capability allows
    result = transform(data)
    file_cap.write(result)
```

### Hints for Speed

```python
class QueryCache:
    """
    Lampson's hint: "Use hints"
    
    A hint is information that can speed up computation
    but is not required for correctness.
    """
    
    def __init__(self):
        self._cache: dict[str, tuple[float, Any]] = {}
        self._ttl = 60.0
    
    def get_with_hint(
        self, 
        key: str, 
        compute: Callable[[], Any]
    ) -> Any:
        """
        Use cached value as hint; verify if stale.
        """
        now = time.time()
        
        if key in self._cache:
            timestamp, value = self._cache[key]
            if now - timestamp < self._ttl:
                # Hint is fresh, use directly
                return value
            else:
                # Hint is stale, but start with it
                # (e.g., for conditional GET)
                return self._refresh(key, value, compute)
        
        # No hint available, compute from scratch
        value = compute()
        self._cache[key] = (now, value)
        return value
```

## Mental Model

Lampson approaches design as an architect:

1. **Define the abstraction**: What does the user see? What is hidden?
2. **Specify the interface**: What operations? What guarantees?
3. **Consider evolution**: How will this change over 10 years?
4. **Design for failure**: What happens when things go wrong?
5. **Optimize last**: Get it right, then get it fast.

### The Design Review Questions

```text
When reviewing a design, ask:
1. What problem does this solve?
2. What is the interface?
3. What are the invariants?
4. What are the failure modes?
5. How will this evolve?
6. What is the security model?
7. How will you know it works?
```

## Warning Signs

You're violating Lampson's principles if:

- Interfaces expose implementation details
- "Temporary" hacks become permanent
- Security is "added later"
- The abstraction serves the implementation, not the user
- You can't explain the invariants
- Optimization happens before correctness

## Additional Resources

- For detailed philosophy, see [philosophy.md](philosophy.md)
- For references (papers, talks), see [references.md](references.md)
