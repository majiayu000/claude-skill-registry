---
name: computational-literacy
description: Understanding how digital systems actually work -- hardware, operating systems, networks, and information representation -- at a depth sufficient to reason about them rather than just use them. Covers CPU/RAM/storage/GPU roles, what an OS does, how packets travel the internet, and how computers represent numbers, text, images, and sound as binary. Use when a learner needs to build a mental model of computing rather than memorize menu paths.
type: skill
category: digital-literacy
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/digital-literacy/computational-literacy/SKILL.md
superseded_by: null
---
# Computational Literacy

Computational literacy is not coding. It is the capacity to reason about how digital systems work at a level sufficient to understand their behavior, diagnose their failures, and evaluate claims made about them. A computationally literate person does not need to write Python, but they should know why a computer slows down when RAM is full, why the internet works when no one is in charge of it, and why an image "looks different on different screens" is actually a statement about color spaces and pixel encoding. This skill covers the core mental models: hardware, operating systems, networks, and information representation.

**Agent affinity:** rheingold (practical fluency), ito (connected learning framing), jenkins (literacy across media)

**Concept IDs:** diglit-hardware-components, diglit-operating-systems, diglit-networks-internet, diglit-information-representation

## Hardware: What the Boxes Actually Do

A computer is a coordinated set of specialized parts. Understanding their roles is the fastest path to understanding why things behave the way they do.

### CPU (Central Processing Unit)

The CPU executes instructions. It reads a stream of operations (arithmetic, comparisons, memory access, jumps) from RAM and performs them one (or several) at a time. Modern CPUs have multiple cores -- effectively multiple workers sharing the same workspace -- and run at clock speeds measured in gigahertz (billions of cycles per second).

**The practical consequence:** CPU-bound tasks (calculations, compression, encryption) are bounded by clock speed and core count. If your computer feels slow during video editing, the CPU is often the bottleneck.

### RAM (Random Access Memory)

RAM is the workspace where active programs live. It is fast -- nanoseconds to access any location -- but volatile: turning off the power erases it. RAM is measured in gigabytes (8 GB, 16 GB, 32 GB are typical in 2026).

**The practical consequence:** When you open too many browser tabs and the computer starts swapping to disk, you are watching RAM exhaustion. The operating system is moving inactive memory to storage, which is thousands of times slower. The only cures are closing programs or adding RAM.

### Storage (SSD, HDD, NVMe)

Storage is where data lives when the power is off. SSDs (Solid State Drives) have no moving parts and access any block in microseconds. NVMe SSDs are faster still -- nearly as fast as RAM for large sequential reads. HDDs (traditional spinning disks) are slower but cheaper per gigabyte.

**The practical consequence:** Boot time, application launch time, and "where did that file go?" speed are all storage-bound. Upgrading from HDD to SSD is the single most impactful upgrade for an older computer.

### GPU (Graphics Processing Unit)

The GPU is a massively parallel CPU. Instead of a few fast cores, it has thousands of slower cores designed to do the same operation on many pieces of data at once. This is ideal for graphics (every pixel gets the same operation) and, more recently, for machine learning (every weight gets multiplied).

**The practical consequence:** Gaming, video rendering, and AI model inference are GPU-bound. If you are running LLMs locally or training models, VRAM (the GPU's dedicated memory) is the resource that limits you.

### Peripherals

Keyboards, mice, cameras, monitors, microphones, printers. These connect over standard interfaces (USB, Bluetooth, HDMI). The distinction between "the computer" and "the peripherals" is fuzzier than it looks: modern keyboards contain their own processors; modern monitors run their own firmware.

## Operating Systems: The Invisible Layer

An operating system (Windows, macOS, Linux, Android, iOS) is the software that manages the hardware and provides a predictable environment for applications. You rarely see it, but almost every "why did my computer do that?" question is actually an OS question.

### Process management

When you double-click an icon, the OS creates a *process* -- an instance of the program with its own memory space, open files, and execution state. The OS decides which process runs on which CPU core at any moment, and it switches between them thousands of times per second. This is why you can "run many programs at once" on a computer that has fewer cores than programs.

### File systems

A file system is the organization of data on storage. It turns the flat physical device into a hierarchy of folders and files. File systems also track metadata: modification time, ownership, permissions.

**Common file systems:** NTFS (Windows), APFS (macOS), ext4 (Linux), exFAT (cross-platform, used on SD cards and USB drives).

### Device drivers

Every piece of hardware needs a driver -- a small program that tells the OS how to talk to it. When a printer "stops working after an update," a driver is usually the culprit.

### Users and permissions

Modern operating systems distinguish between users and processes that can do different things. Administrator accounts can modify system files; regular users cannot. This is a security boundary that slows down attackers.

## Networks and the Internet

The internet is a cooperative, decentralized network of networks. No one owns it. No one is in charge of it. It works because everyone agrees to use a common set of protocols.

### How a packet travels

When you load a web page, your computer does roughly this:

1. **DNS lookup.** Translate the domain name (example.com) into an IP address (93.184.216.34). Your computer asks a DNS server, which may ask another, walking up the DNS hierarchy until someone knows.
2. **Connection.** Your computer opens a TCP connection to that IP address on port 443 (HTTPS).
3. **TLS handshake.** The two sides exchange certificates and agree on encryption keys, so no one in between can read the contents.
4. **HTTP request.** Your computer sends "GET /page HTTP/2" with headers describing what it wants.
5. **HTTP response.** The server sends back the HTML, then the browser fetches all the referenced images, scripts, and stylesheets.
6. **Rendering.** The browser assembles everything into the page you see.

Every step involves multiple hops across routers. The packets take different paths, sometimes out of order, and TCP reassembles them.

### IP addresses and DNS

IP addresses are the actual identifiers on the internet. IPv4 addresses look like 93.184.216.34. IPv6 addresses look like 2001:db8::1. Domain names are a human-friendly layer on top -- DNS is the phone book that maps one to the other.

### HTTP and HTTPS

HTTP is the language web browsers and servers use to exchange requests and responses. HTTPS is HTTP wrapped in TLS encryption. The padlock icon in your browser means your connection is encrypted -- it does *not* mean the other side is trustworthy.

### Bandwidth vs latency

Two networks can have the same bandwidth (megabits per second) but wildly different latencies (milliseconds per round-trip). Streaming video needs bandwidth; video calls and games need low latency. "Slow internet" is usually a latency problem, not a bandwidth problem.

## Information Representation

Computers represent everything -- numbers, text, images, audio, video -- as binary: strings of 1s and 0s. Understanding the encodings helps you reason about why files behave the way they do.

### Binary and bytes

A *bit* is one binary digit. A *byte* is 8 bits, capable of representing 256 distinct values. Larger units: kilobyte (about 1,000 bytes), megabyte (about 1 million), gigabyte (about 1 billion), terabyte (about 1 trillion).

### Numbers

Integers are represented directly in binary. Negative numbers use two's complement. Fractional numbers (3.14) use floating point, which is why "0.1 + 0.2 = 0.30000000000000004" in most programming languages. This is not a bug -- it is a consequence of representing decimals in binary.

### Text

Text is represented as numbers. Early systems used ASCII (7 bits, 128 characters -- enough for English). Modern systems use Unicode, which defines a number (code point) for every character in every writing system, including emoji. The most common encoding is UTF-8, which uses 1-4 bytes per character.

This is why files "look wrong" when opened in the wrong encoding: the bytes have not changed, but the interpreter is mapping them to the wrong characters.

### Images

A digital image is a grid of pixels, each with color values. Formats differ in how they store this:

- **Bitmap (BMP, uncompressed):** Literal pixel grid. Huge files.
- **JPEG:** Lossy compression. Smaller files, visible artifacts at high compression.
- **PNG:** Lossless compression. Larger than JPEG for photos, better for diagrams and screenshots.
- **WebP, AVIF:** Modern formats. Better compression ratios.

### Audio

Audio is a sequence of amplitude samples. CD quality is 44.1 kHz (44,100 samples per second) at 16 bits per sample. MP3 and AAC use lossy compression; FLAC is lossless.

### Video

Video is a sequence of images at 24-60 frames per second, with an audio track. Compression exploits redundancy between frames: most of the picture does not change from one frame to the next. H.264, H.265, and AV1 are the dominant codecs.

## When NOT to Use This Skill

- **Source credibility questions.** Use `information-evaluation`.
- **Privacy settings and data control.** Use `data-privacy`.
- **Algorithmic recommendation systems.** Use `algorithmic-awareness` -- that is about how algorithms shape what you see, not how the hardware works.

## Decision Guidance

When a user asks "why is my computer slow?" walk the layers:

1. **CPU** -- check if a process is using 100%. If yes, that program is the bottleneck.
2. **RAM** -- check if memory usage is near full. If yes, close programs or add RAM.
3. **Storage** -- check if disk is full or if it is an HDD. If yes, clear space or upgrade.
4. **Network** -- check if the slowness is in web browsing specifically. If yes, test with a speed tool.
5. **Software** -- check if a specific program is slow or everything is slow. If specific, the program is at fault.

Most "slow computer" complaints are a misdiagnosed one of these five.

## Cross-References

- **rheingold agent:** Practical digital fluency framing
- **ito agent:** Connected learning, how people actually pick up computational fluency
- **jenkins agent:** Media literacy across computational forms
- **information-evaluation skill:** Evaluating computing claims (product reviews, tech news)
- **algorithmic-awareness skill:** The software layer above the system

## References

- Tanenbaum, A. S., & Bos, H. (2014). *Modern Operating Systems*. 4th edition. Pearson.
- Kurose, J. F., & Ross, K. W. (2016). *Computer Networking: A Top-Down Approach*. 7th edition. Pearson.
- Petzold, C. (2000). *Code: The Hidden Language of Computer Hardware and Software*. Microsoft Press.
- The Internet Engineering Task Force. *RFC 791 (IP)*, *RFC 793 (TCP)*, *RFC 7540 (HTTP/2)*.
