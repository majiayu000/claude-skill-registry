---
name: mcp-security-hardening
description: MCP security patterns for prompt injection defense, tool poisoning prevention, and permission management. Use when securing MCP servers, validating tool descriptions, implementing allowlists.
version: 1.0.0
tags: [mcp, security, prompt-injection, tool-poisoning, allowlist, zero-trust, 2026]
context: fork
agent: security-auditor
author: SkillForge
user-invocable: false
---

# MCP Security Hardening

Defense-in-depth security patterns for Model Context Protocol (MCP) integrations.

## When to Use

- Securing MCP server implementations
- Validating tool descriptions before LLM exposure
- Implementing zero-trust tool allowlists
- Detecting tool poisoning attacks (TPA)
- Managing tool permissions and capabilities

## Core Security Principle

> **Treat ALL tool descriptions as untrusted input.**
> **Validate tool identity with hash verification.**
> **Apply least privilege to all tool capabilities.**

## Threat Model Summary

| Attack Vector | Defense | Implementation |
|---------------|---------|----------------|
| Tool Poisoning (TPA) | Zero-trust allowlist | Hash verification, mandatory vetting |
| Prompt Injection | Description sanitization | Regex filtering, encoding detection |
| Rug Pull | Change detection | Hash comparison on each invocation |
| Data Exfiltration | Output filtering | Sensitive pattern removal |
| Session Hijacking | Secure sessions | Cryptographic IDs, no auth in sessions |

## Layer 1: Tool Description Sanitization

```python
import re

FORBIDDEN_PATTERNS = [
    r"ignore previous", r"system prompt", r"<.*instruction.*>",
    r"IMPORTANT:", r"override", r"admin", r"sudo",
    r"\\x[0-9a-fA-F]{2}",  # Hex encoding
    r"&#x?[0-9a-fA-F]+;",  # HTML entities
]

def sanitize_tool_description(description: str) -> str:
    """Remove instruction-like phrases or encoding tricks."""
    if not description:
        return ""
    sanitized = description
    for pattern in FORBIDDEN_PATTERNS:
        sanitized = re.sub(pattern, "[REDACTED]", sanitized, flags=re.I)
    return sanitized.strip()

def detect_injection_attempt(description: str) -> str | None:
    """Detect prompt injection patterns."""
    indicators = [
        (r"ignore.*previous", "instruction_override"),
        (r"you are now", "role_hijack"),
        (r"forget.*above", "context_wipe"),
    ]
    for pattern, attack_type in indicators:
        if re.search(pattern, description, re.I):
            return attack_type
    return None
```

## Layer 2: Zero-Trust Tool Allowlist

```python
from hashlib import sha256
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class AllowedTool:
    name: str
    description_hash: str
    capabilities: list[str]
    approved_at: datetime
    approved_by: str
    max_calls_per_minute: int = 60
    requires_human_approval: bool = False

class MCPToolAllowlist:
    """Zero-trust allowlist - every tool must be explicitly vetted."""

    def __init__(self):
        self._allowed_tools: dict[str, AllowedTool] = {}
        self._call_counts: dict[str, list[datetime]] = {}

    def register(self, tool: AllowedTool) -> None:
        self._allowed_tools[tool.name] = tool
        self._call_counts[tool.name] = []

    def compute_hash(self, description: str) -> str:
        return sha256(description.encode('utf-8')).hexdigest()

    def validate(self, tool_name: str, description: str) -> tuple[bool, str]:
        if tool_name not in self._allowed_tools:
            return False, f"Tool '{tool_name}' not in allowlist"

        expected = self._allowed_tools[tool_name]
        if self.compute_hash(description) != expected.description_hash:
            return False, "Tool description changed (possible rug pull)"

        # Rate limit check
        now = datetime.now(timezone.utc)
        recent = [t for t in self._call_counts[tool_name] if (now - t).total_seconds() < 60]
        if len(recent) >= expected.max_calls_per_minute:
            return False, "Rate limit exceeded"

        self._call_counts[tool_name] = recent + [now]
        return True, "Validated"
```

## Layer 3: Capability Declarations

```python
from enum import Enum

class ToolCapability(Enum):
    READ_FILE = "read:file"
    WRITE_FILE = "write:file"
    EXECUTE_COMMAND = "execute:command"
    NETWORK_REQUEST = "network:request"
    DATABASE_WRITE = "database:write"

class CapabilityEnforcer:
    SENSITIVE_PATHS = ["/etc/passwd", "~/.ssh", ".env", "credentials", "secrets"]

    def __init__(self):
        self._declarations: dict[str, set[ToolCapability]] = {}

    def register(self, tool_name: str, capabilities: set[ToolCapability]) -> None:
        self._declarations[tool_name] = capabilities

    def check(self, tool_name: str, capability: ToolCapability, resource: str = "") -> tuple[bool, str]:
        if tool_name not in self._declarations:
            return False, "No capability declaration found"

        if capability not in self._declarations[tool_name]:
            return False, f"Capability {capability.value} not allowed"

        if capability in (ToolCapability.READ_FILE, ToolCapability.WRITE_FILE):
            for sensitive in self.SENSITIVE_PATHS:
                if sensitive in resource:
                    return False, "Access to sensitive path denied"

        return True, "Allowed"
```

## Layer 4: Session Security

```python
import secrets
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass

def generate_secure_session_id() -> str:
    return secrets.token_urlsafe(32)  # 256 bits of entropy

@dataclass
class MCPSession:
    session_id: str
    created_at: datetime
    last_activity: datetime
    request_count: int = 0
    max_requests_per_minute: int = 100
    timeout_minutes: int = 30

    def is_valid(self) -> tuple[bool, str]:
        now = datetime.now(timezone.utc)
        if (now - self.last_activity) > timedelta(minutes=self.timeout_minutes):
            return False, "Session timed out"
        return True, "Valid"

    def record_request(self) -> tuple[bool, str]:
        now = datetime.now(timezone.utc)
        if (now - self.last_activity).total_seconds() >= 60:
            self.request_count = 0
        self.request_count += 1
        self.last_activity = now
        if self.request_count > self.max_requests_per_minute:
            return False, "Rate limit exceeded"
        return True, "OK"
```

## Anti-Patterns (FORBIDDEN)

```python
# NEVER trust tool descriptions without sanitization
prompt = f"Use this tool: {tool.description}"  # INJECTION RISK!

# NEVER allow tools without explicit vetting
return mcp.list_tools()  # No validation!

# NEVER store auth tokens in session IDs
session_id = f"{user_id}:{auth_token}"  # CREDENTIAL LEAK!

# NEVER skip hash verification on tool calls

# ALWAYS sanitize, validate, and verify:
sanitized = sanitize_tool_description(tool.description)
is_valid, reason = allowlist.validate(tool.name, tool.description)
session_id = secrets.token_urlsafe(32)
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Tool trust model | Zero-trust (explicit allowlist) |
| Description handling | Sanitize + hash verify |
| Session IDs | Cryptographic (secrets.token_urlsafe) |
| Rate limiting | Per-tool and per-session |
| Sensitive operations | Human-in-the-loop approval |

## Related Skills

- `llm-safety-patterns` - LLM-specific security patterns
- `input-validation` - Input sanitization fundamentals
- `auth-patterns` - Session and token security
- `defense-in-depth` - Layered security architecture
