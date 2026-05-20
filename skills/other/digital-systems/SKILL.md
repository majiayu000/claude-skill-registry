---
name: digital-systems
description: Foundational digital technology literacy covering binary and data representation, computer architecture (CPU, memory, storage, I/O), networking fundamentals (protocols, the internet, LAN/WAN), operating systems, and software concepts. Use when explaining how computers work, how data is stored and transmitted, how networks operate, or how hardware and software interact. Distinct from programming -- this skill covers what digital systems are and how they function, not how to write code for them.
type: skill
category: technology
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/technology/digital-systems/SKILL.md
superseded_by: null
---
# Digital Systems

Digital systems are the foundation of modern technology. Every device that processes information -- from a calculator to a supercomputer -- operates on the same basic principles: binary representation, stored-program execution, and layered abstraction. This skill covers how digital systems work at each layer, from transistors to applications, so that a learner can reason about technology rather than merely use it.

**Agent affinity:** berners-lee (information architecture, networking), borg (systems infrastructure), norman (user-facing software concepts)

**Concept IDs:** tech-binary-data, tech-computer-architecture, tech-networking-basics, tech-software-concepts

## Part I -- Binary and Data Representation

### Why Binary

Digital computers use binary (base-2) because transistors have two reliable states: on and off. All data -- numbers, text, images, audio, video -- must be encoded as sequences of 0s and 1s. Understanding binary is not about memorizing conversion tables; it is about grasping that every piece of information in a computer is a pattern of bits, and every operation is a transformation of those patterns.

### Number Representation

| System | Base | Digits | Use |
|---|---|---|---|
| Binary | 2 | 0, 1 | Internal machine representation |
| Octal | 8 | 0-7 | Compact binary shorthand (Unix permissions) |
| Decimal | 10 | 0-9 | Human-readable numbers |
| Hexadecimal | 16 | 0-9, A-F | Memory addresses, color codes, compact binary |

**Conversion example.** The decimal number 42 in binary:

42 / 2 = 21 remainder 0
21 / 2 = 10 remainder 1
10 / 2 = 5 remainder 0
5 / 2 = 2 remainder 1
2 / 2 = 1 remainder 0
1 / 2 = 0 remainder 1

Reading remainders bottom-to-top: 101010. So 42 in decimal is 101010 in binary.

### Text Encoding

Characters are mapped to numbers via encoding standards:

- **ASCII** (1963): 128 characters, 7 bits. English letters, digits, punctuation, control characters.
- **Unicode** (1991-present): 149,813+ characters across 161 scripts. Encodes every writing system in active use.
- **UTF-8** (1993): Variable-length encoding of Unicode. ASCII-compatible (English text is identical in ASCII and UTF-8). The dominant encoding on the web.

### Images, Audio, and Video

- **Images:** Grids of pixels, each pixel a color value. RGB uses three 8-bit channels (16.7 million colors). Resolution = pixels per dimension. Compression: lossless (PNG) vs lossy (JPEG).
- **Audio:** Sampled waveforms. CD quality = 44,100 samples/second, 16 bits per sample, 2 channels. Higher sample rates and bit depths capture more detail.
- **Video:** Sequences of images (frames) plus audio. 30 or 60 frames per second. Compression is essential -- raw 1080p video is ~1.5 Gbps.

The fundamental insight: all media types reduce to numbers, and all numbers reduce to bits.

## Part II -- Computer Architecture

### The Von Neumann Model

Nearly all modern computers follow the von Neumann architecture (1945): a central processing unit (CPU) that executes instructions stored in the same memory as data. The four components:

1. **CPU (Central Processing Unit):** Fetches, decodes, and executes instructions. Contains an arithmetic logic unit (ALU) for computation and a control unit for sequencing.
2. **Memory (RAM):** Volatile storage that holds running programs and their data. Fast but loses contents when powered off.
3. **Storage:** Non-volatile storage (SSD, HDD) that persists data across power cycles. Slower than RAM but permanent.
4. **Input/Output (I/O):** Devices that move data between the computer and the outside world -- keyboard, display, network interface, sensors.

### The Fetch-Decode-Execute Cycle

The CPU repeats three steps continuously:

1. **Fetch:** Read the next instruction from memory at the address in the program counter.
2. **Decode:** Interpret the instruction (what operation, which operands).
3. **Execute:** Perform the operation (arithmetic, data movement, control flow).

Modern CPUs execute billions of these cycles per second. Clock speed (measured in GHz) indicates how many cycles occur per second, though actual throughput depends on pipeline depth, cache behavior, and instruction-level parallelism.

### Memory Hierarchy

| Level | Typical size | Typical latency | Volatile? |
|---|---|---|---|
| CPU registers | ~1 KB | < 1 ns | Yes |
| L1 cache | 64-128 KB | ~1 ns | Yes |
| L2 cache | 256 KB - 1 MB | ~3-5 ns | Yes |
| L3 cache | 4-64 MB | ~10-20 ns | Yes |
| RAM | 8-128 GB | ~50-100 ns | Yes |
| SSD | 256 GB - 4 TB | ~50-100 us | No |
| HDD | 1-20 TB | ~5-10 ms | No |

The hierarchy exists because fast storage is expensive and small, while cheap storage is large and slow. Caches automatically keep frequently-accessed data close to the CPU.

## Part III -- Networking Fundamentals

### What a Network Is

A network is two or more devices connected to exchange data. The internet is a network of networks -- billions of devices connected through a hierarchy of local, regional, and global links.

### The Protocol Stack

Networks use layered protocols. The TCP/IP model has four layers:

| Layer | Purpose | Example protocols |
|---|---|---|
| Application | User-facing services | HTTP, SMTP, DNS, FTP |
| Transport | Reliable delivery between processes | TCP (reliable), UDP (fast) |
| Internet | Routing between networks | IP (addressing), ICMP (diagnostics) |
| Link | Physical transmission on a single link | Ethernet, Wi-Fi, Bluetooth |

Each layer adds a header to the data, creating an "envelope inside an envelope" structure. This layering means application developers do not need to know whether data travels over fiber optic cable or Wi-Fi -- the lower layers handle it.

### IP Addresses and DNS

Every device on the internet has an IP address (IPv4: 10.0.0.1; IPv6: FD00::1/7). The Domain Name System (DNS) translates human-readable names (example.com) into IP addresses. DNS is distributed -- no single server holds all mappings.

### How the Web Works

Tim Berners-Lee invented the World Wide Web in 1989 at CERN, building on three pillars:

1. **URLs:** Uniform Resource Locators -- addresses for web resources.
2. **HTTP:** Hypertext Transfer Protocol -- the request/response protocol for fetching resources.
3. **HTML:** Hypertext Markup Language -- the format for web documents, with links connecting them.

A web browser sends an HTTP request to a server, which returns an HTML document. The browser renders the document and follows links to fetch additional resources (images, stylesheets, scripts). This request-response cycle is the heartbeat of the web.

## Part IV -- Operating Systems and Software

### What an Operating System Does

An operating system (OS) is the software layer between hardware and applications. It manages:

- **Processes:** Running programs, scheduling CPU time, isolating memory.
- **Memory:** Allocating RAM to processes, virtual memory, paging.
- **File systems:** Organizing persistent storage into files and directories.
- **I/O:** Device drivers, buffering, interrupt handling.
- **Security:** User accounts, permissions, access control.

### Software Layers

| Layer | Examples | Role |
|---|---|---|
| Hardware | CPU, RAM, disk, NIC | Physical computation and storage |
| Firmware | BIOS/UEFI | Hardware initialization |
| OS kernel | Linux, Windows NT, XNU | Resource management, hardware abstraction |
| System utilities | Shell, file manager, task manager | OS-level user tools |
| Applications | Browser, editor, game | User-facing software |

### Algorithms and Data Structures (Conceptual)

Software solves problems through algorithms -- step-by-step procedures that transform input into output. The efficiency of an algorithm determines whether a task completes in milliseconds or hours. Data structures (lists, trees, hash tables) organize information for efficient access. These concepts are foundational to understanding why some software is fast and some is slow, even for non-programmers.

## Part V -- System Thinking for Digital Technology

### Inputs, Processes, Outputs, Feedback

Every digital system can be analyzed as a system with these four components:

- **Inputs:** Data or commands entering the system (keystrokes, sensor readings, network packets).
- **Processes:** Transformations applied to inputs (computation, filtering, routing).
- **Outputs:** Results produced (display, stored files, transmitted data).
- **Feedback:** Output that influences future input (error messages, adaptive algorithms, user corrections).

This framework applies at every scale: a single function, a program, a server, a global platform.

### Abstraction as a Design Tool

Abstraction hides complexity behind simple interfaces. A user clicks "Send" without knowing about TCP segmentation, IP routing, or Ethernet framing. A programmer calls `sort()` without implementing quicksort. Abstraction layers are what make complex systems usable, but understanding what lies beneath the abstraction is what makes a person technologically literate rather than merely a technology consumer.

## Cross-References

- **berners-lee agent:** Web architecture, information systems, open standards. Primary agent for networking and web questions.
- **borg agent:** Systems infrastructure, operating systems, system administration. Primary agent for OS and hardware questions.
- **norman agent:** Human-computer interaction aspects of digital systems -- how interfaces expose system behavior to users.
- **cybersecurity-basics skill:** Security aspects of digital systems (encryption, authentication, threats).
- **design-thinking skill:** How digital systems are designed to meet user needs.

## References

- Petzold, C. (2000). *Code: The Hidden Language of Computer Hardware and Software*. Microsoft Press.
- Tanenbaum, A. S. & Austin, T. (2012). *Structured Computer Organization*. 6th edition. Pearson.
- Kurose, J. F. & Ross, K. W. (2021). *Computer Networking: A Top-Down Approach*. 8th edition. Pearson.
- Berners-Lee, T. (1999). *Weaving the Web*. HarperBusiness.
- Abelson, H. & Sussman, G. J. (1996). *Structure and Interpretation of Computer Programs*. 2nd edition. MIT Press.
