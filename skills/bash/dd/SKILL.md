---
name: dd
description: Disk cloning, benchmarking, and file conversion tool with progress monitoring options.
---

# dd — Disk Benchmarking

**Basic Usage**

```bash
# Disk benchmarking (1GB file with direct I/O)
dd if=/dev/zero of=./testfile bs=1G count=1 oflag=direct
# Output: 1073741824 bytes (1.1 GB, 1.0 GiB) copied, 4.76527 s, 225 MB/s

# Read from /dev/urandom, 2*512 bytes
dd if=/dev/urandom of=/tmp/test.txt count=2 bs=512

# Create 1MB file with zero allocated blocks
dd if=/dev/zero of=foo1 seek=1 bs=1M count=0
```

**Progress Monitoring**

```bash
# Built-in progress (coreutils v8.24+)
dd if=/dev/zero of=/dev/null bs=128M status=progress

# Watch progress with USR1 signal
dd if=/dev/zero of=/dev/null bs=4KB &
pid=$!
kill -USR1 $pid

# Progress with pv and dialog
(pv -n /dev/zero | dd of=/dev/null bs=128M conv=notrunc,noerror) 2>&1 | \
  dialog --gauge "Running dd..." 10 70 0

# Progress with pv and zenity
(pv -n /dev/zero | dd of=/dev/null bs=128M conv=notrunc,noerror) 2>&1 | \
  zenity --title 'Cloning with dd' --progress
```

**Swap File Creation**

```bash
# Create 1GiB swap file
dd if=/dev/zero of=/swapfile count=1048576 bs=1024 status=progress
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
```

**Advanced Operations**

```bash
# Audio streaming over SSH (low quality)
dd if=/dev/dsp | ssh -c arcfour -C username@host dd of=/dev/dsp

# Clone disk to disk
dd if=/dev/sda of=/dev/sdb bs=64K conv=noerror,sync

# Create ISO from CD/DVD
dd if=/dev/cdrom of=image.iso bs=2048

# Convert DOS/Windows line endings to Linux
dd if=input.txt of=output.txt conv=unix
```

**Conversion Flags**

```bash
conv=notrunc    # Don't truncate output file
conv=noerror    # Continue on read errors
conv=sync       # Pad blocks with zeros
conv=ucase      # Convert to uppercase
conv=lcase      # Convert to lowercase
conv=ascii      # EBCDIC to ASCII
conv=ebcdic     # ASCII to EBCDIC
conv=block      # Convert to fixed-length records
conv=unblock    # Convert from fixed-length records
```