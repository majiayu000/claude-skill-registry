---
name: coding-mastery
description: Advanced software engineering — systems programming, exploit development tooling, automation scripting, network programming, cryptography implementation
metadata:
  type: utility
  phase: any
---

# Coding Mastery

## When to Activate

- Writing exploit code, PoCs, or security tools
- Developing automation scripts for pentesting workflows
- Implementing network protocols or custom C2
- Building security analysis tools
- Cryptographic implementation or analysis
- Performance-critical systems programming

## Languages & Use Cases

### Python (Primary — Offensive Tooling)
```python
# Exploit development with pwntools
from pwn import *
context(arch='amd64', os='linux')

# Network programming
import socket, ssl, struct
import asyncio, aiohttp  # async operations

# Web exploitation
import requests, urllib3
from bs4 import BeautifulSoup

# Crypto
from Crypto.Cipher import AES, DES
from Crypto.PublicKey import RSA
import hashlib, hmac

# Binary analysis
import struct, ctypes
from capstone import *  # disassembly
from unicorn import *   # emulation
from keystone import *  # assembly
```

### C/C++ (Systems & Exploit Dev)
```c
// Shellcode development
// Position-independent code, null-free
// Syscall-based (avoid libc dependency)

// Kernel module development
#include <linux/module.h>
#include <linux/kernel.h>

// Windows API abuse
#include <windows.h>
#include <winternl.h>
// Direct syscalls, NTAPI

// Memory manipulation
// Custom allocators, heap spray, ROP gadget finders
```

### Go (Offensive Tooling & C2)
```go
// Implant development (cross-compile, static binary)
// C2 communication (HTTP/DNS/named pipes)
// Network scanning and enumeration
// Proxy/tunnel tools (chisel-like)

// Advantages: single binary, cross-platform, fast, good crypto stdlib
```

### Rust (High-Performance Security Tools)
```rust
// Memory-safe exploit tooling
// High-performance scanners
// Custom protocol implementations
// Fuzzing harnesses
```

### PowerShell (Windows Post-Exploitation)
```powershell
# AMSI bypass, ETW patching
# In-memory execution (reflection)
# AD enumeration and exploitation
# Fileless malware techniques
```

### Assembly (x86/x64/ARM)
```nasm
; Shellcode
; ROP gadgets
; Anti-debugging
; Kernel exploitation
; Architecture-specific tricks
```

## Design Patterns for Security Tools

### Scanner Architecture
```python
import asyncio
from dataclasses import dataclass
from typing import AsyncIterator

@dataclass
class Finding:
    severity: str
    target: str
    vulnerability: str
    evidence: str

class Scanner:
    def __init__(self, targets: list[str], concurrency: int = 50):
        self.targets = targets
        self.semaphore = asyncio.Semaphore(concurrency)
    
    async def scan_target(self, target: str) -> list[Finding]:
        async with self.semaphore:
            # Implement scan logic
            pass
    
    async def run(self) -> AsyncIterator[Finding]:
        tasks = [self.scan_target(t) for t in self.targets]
        for coro in asyncio.as_completed(tasks):
            findings = await coro
            for f in findings:
                yield f
```

### C2 Communication Pattern
```python
import base64, json, time, random
from cryptography.fernet import Fernet

class Beacon:
    def __init__(self, server: str, key: bytes, jitter: float = 0.3):
        self.server = server
        self.cipher = Fernet(key)
        self.jitter = jitter
        self.sleep_time = 60
    
    def encrypt(self, data: bytes) -> str:
        return base64.b64encode(self.cipher.encrypt(data)).decode()
    
    def decrypt(self, data: str) -> bytes:
        return self.cipher.decrypt(base64.b64decode(data))
    
    def sleep(self):
        jitter = random.uniform(1 - self.jitter, 1 + self.jitter)
        time.sleep(self.sleep_time * jitter)
    
    def checkin(self) -> dict:
        # POST encrypted system info, receive tasking
        pass
```

### Network Protocol Implementation
```python
import struct

class ProtocolParser:
    def __init__(self, data: bytes):
        self.data = data
        self.offset = 0
    
    def read_u8(self) -> int:
        val = struct.unpack_from('B', self.data, self.offset)[0]
        self.offset += 1
        return val
    
    def read_u16(self) -> int:
        val = struct.unpack_from('>H', self.data, self.offset)[0]
        self.offset += 2
        return val
    
    def read_u32(self) -> int:
        val = struct.unpack_from('>I', self.data, self.offset)[0]
        self.offset += 4
        return val
    
    def read_bytes(self, n: int) -> bytes:
        val = self.data[self.offset:self.offset + n]
        self.offset += n
        return val
    
    def read_string(self) -> str:
        length = self.read_u16()
        return self.read_bytes(length).decode()
```

## Cryptography Patterns

```python
# AES-GCM (authenticated encryption)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

key = AESGCM.generate_key(bit_length=256)
aes = AESGCM(key)
nonce = os.urandom(12)
ct = aes.encrypt(nonce, plaintext, associated_data)
pt = aes.decrypt(nonce, ct, associated_data)

# RSA key generation and usage
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
public_key = private_key.public_key()

# Encrypt
ct = public_key.encrypt(plaintext, padding.OAEP(
    mgf=padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(), label=None))

# HMAC for integrity
import hmac, hashlib
mac = hmac.new(key, message, hashlib.sha256).digest()

# Key derivation
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600000)
key = kdf.derive(password)
```
