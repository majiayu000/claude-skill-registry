---
name: stevens-network-protocols
description: Understand network protocols in the style of W. Richard Stevens, author of TCP/IP Illustrated. Emphasizes deep protocol understanding through packet analysis, layered thinking, and knowing exactly what happens at every byte. Use when debugging network issues, implementing protocols, or building networked applications.
---

# W. Richard Stevens Network Protocol Style Guide

## Overview

W. Richard Stevens was the author of "TCP/IP Illustrated" and "UNIX Network Programming"—the definitive works on understanding network protocols. His approach was unique: instead of abstract descriptions, he showed actual packet traces and walked through every field, every byte, every state transition. Stevens taught a generation of engineers that to truly understand networking, you must see what's actually on the wire.

## Core Philosophy

> "The only way to understand a protocol is to see it in action. Theory without packets is just speculation."

> "Every byte in a packet is there for a reason. Understand the reason."

> "Read the RFCs, but trust the wire. The wire never lies."

Stevens believed that network protocols should be understood concretely, not abstractly. His books are filled with tcpdump output, hex dumps, and state diagrams derived from real network traffic. This empirical approach reveals the truth about how protocols actually behave, not just how they're specified.

## The Network Layers

```
┌─────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                        │
│  HTTP, DNS, SMTP, FTP, SSH, TLS                             │
│  "What the user cares about"                                │
├─────────────────────────────────────────────────────────────┤
│                     TRANSPORT LAYER                          │
│  TCP (reliable, ordered, connection-oriented)               │
│  UDP (unreliable, unordered, connectionless)                │
│  "How data gets there reliably (or not)"                    │
├─────────────────────────────────────────────────────────────┤
│                     NETWORK LAYER                            │
│  IP (addressing, routing, fragmentation)                    │
│  ICMP (diagnostics and errors)                              │
│  "How to find the destination"                              │
├─────────────────────────────────────────────────────────────┤
│                     LINK LAYER                               │
│  Ethernet, WiFi, PPP                                         │
│  ARP (IP → MAC translation)                                 │
│  "How to reach the next hop"                                │
├─────────────────────────────────────────────────────────────┤
│                     PHYSICAL LAYER                           │
│  Cables, radio waves, light                                 │
│  "Actual bits on the medium"                                │
└─────────────────────────────────────────────────────────────┘
```

## Design Principles

1. **See the Packets**: Use tcpdump/Wireshark to see what's really happening.

2. **Know Every Field**: Understand what each byte means and why.

3. **Follow the State Machine**: Protocols are state machines—know the states.

4. **Read the RFCs**: The specification is the ground truth.

5. **Understand the Why**: Every protocol decision has a reason.

## When Working with Networks

### Always

- Capture packets when debugging—don't guess
- Know the protocol state machine
- Understand header formats byte-by-byte
- Consider what happens at each layer
- Read the relevant RFCs
- Test edge cases (fragmentation, reordering, loss)

### Never

- Assume the network is reliable
- Ignore error conditions in protocols
- Trust application-level logs over packet captures
- Assume packets arrive in order
- Forget about MTU and fragmentation
- Ignore the difference between specification and implementation

### Prefer

- Packet traces over log analysis
- Wireshark over printf debugging
- State diagrams over prose descriptions
- Actual behavior over documented behavior
- Understanding over memorization
- Layer-by-layer analysis

## Code Patterns

### Packet Capture and Analysis

```python
import struct
from dataclasses import dataclass
from typing import Optional, List
from enum import IntEnum


class EtherType(IntEnum):
    IPv4 = 0x0800
    ARP = 0x0806
    IPv6 = 0x86DD


class IPProtocol(IntEnum):
    ICMP = 1
    TCP = 6
    UDP = 17


@dataclass
class EthernetFrame:
    """
    Ethernet II frame header (14 bytes).
    
    Stevens would show this as:
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                    Destination MAC (6 bytes)                  |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |      Destination MAC          |         Source MAC            |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                    Source MAC (continued)                     |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |          EtherType            |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    """
    dst_mac: bytes  # 6 bytes
    src_mac: bytes  # 6 bytes
    ethertype: int  # 2 bytes
    payload: bytes
    
    @classmethod
    def parse(cls, data: bytes) -> 'EthernetFrame':
        if len(data) < 14:
            raise ValueError("Frame too short")
        
        dst_mac = data[0:6]
        src_mac = data[6:12]
        ethertype = struct.unpack('!H', data[12:14])[0]
        payload = data[14:]
        
        return cls(dst_mac, src_mac, ethertype, payload)
    
    def format_mac(self, mac: bytes) -> str:
        return ':'.join(f'{b:02x}' for b in mac)
    
    def __str__(self) -> str:
        return (f"Ethernet: {self.format_mac(self.src_mac)} → "
                f"{self.format_mac(self.dst_mac)} "
                f"type=0x{self.ethertype:04x}")


@dataclass
class IPv4Packet:
    """
    IPv4 header (20+ bytes).
    
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |Version|  IHL  |Type of Service|          Total Length         |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |         Identification        |Flags|      Fragment Offset    |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |  Time to Live |    Protocol   |         Header Checksum       |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                       Source Address                          |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                    Destination Address                        |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                    Options (if IHL > 5)                       |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    """
    version: int
    ihl: int  # Header length in 32-bit words
    tos: int
    total_length: int
    identification: int
    flags: int
    fragment_offset: int
    ttl: int
    protocol: int
    checksum: int
    src_ip: str
    dst_ip: str
    options: bytes
    payload: bytes
    
    @classmethod
    def parse(cls, data: bytes) -> 'IPv4Packet':
        if len(data) < 20:
            raise ValueError("Packet too short")
        
        version_ihl = data[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0x0F
        
        if version != 4:
            raise ValueError(f"Not IPv4: version={version}")
        
        header_length = ihl * 4
        
        tos = data[1]
        total_length = struct.unpack('!H', data[2:4])[0]
        identification = struct.unpack('!H', data[4:6])[0]
        
        flags_frag = struct.unpack('!H', data[6:8])[0]
        flags = flags_frag >> 13
        fragment_offset = flags_frag & 0x1FFF
        
        ttl = data[8]
        protocol = data[9]
        checksum = struct.unpack('!H', data[10:12])[0]
        
        src_ip = '.'.join(str(b) for b in data[12:16])
        dst_ip = '.'.join(str(b) for b in data[16:20])
        
        options = data[20:header_length] if header_length > 20 else b''
        payload = data[header_length:total_length]
        
        return cls(version, ihl, tos, total_length, identification,
                   flags, fragment_offset, ttl, protocol, checksum,
                   src_ip, dst_ip, options, payload)
    
    def __str__(self) -> str:
        proto_name = IPProtocol(self.protocol).name if self.protocol in [1,6,17] else str(self.protocol)
        return (f"IPv4: {self.src_ip} → {self.dst_ip} "
                f"proto={proto_name} ttl={self.ttl} len={self.total_length}")


@dataclass
class TCPSegment:
    """
    TCP header (20+ bytes).
    
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |          Source Port          |       Destination Port        |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                        Sequence Number                        |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                    Acknowledgment Number                      |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |  Data |       |C|E|U|A|P|R|S|F|                               |
    | Offset| Rsrvd |W|C|R|C|S|S|Y|I|            Window             |
    |       |       |R|E|G|K|H|T|N|N|                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |           Checksum            |         Urgent Pointer        |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                    Options (if data offset > 5)               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    """
    src_port: int
    dst_port: int
    seq: int
    ack: int
    data_offset: int
    flags: int
    window: int
    checksum: int
    urgent: int
    options: bytes
    payload: bytes
    
    # Flag bit positions
    FIN = 0x01
    SYN = 0x02
    RST = 0x04
    PSH = 0x08
    ACK = 0x10
    URG = 0x20
    ECE = 0x40
    CWR = 0x80
    
    @classmethod
    def parse(cls, data: bytes) -> 'TCPSegment':
        if len(data) < 20:
            raise ValueError("Segment too short")
        
        src_port = struct.unpack('!H', data[0:2])[0]
        dst_port = struct.unpack('!H', data[2:4])[0]
        seq = struct.unpack('!I', data[4:8])[0]
        ack = struct.unpack('!I', data[8:12])[0]
        
        data_offset_flags = struct.unpack('!H', data[12:14])[0]
        data_offset = (data_offset_flags >> 12) & 0x0F
        flags = data_offset_flags & 0x1FF
        
        window = struct.unpack('!H', data[14:16])[0]
        checksum = struct.unpack('!H', data[16:18])[0]
        urgent = struct.unpack('!H', data[18:20])[0]
        
        header_length = data_offset * 4
        options = data[20:header_length] if header_length > 20 else b''
        payload = data[header_length:]
        
        return cls(src_port, dst_port, seq, ack, data_offset, flags,
                   window, checksum, urgent, options, payload)
    
    def flags_str(self) -> str:
        """Format flags as string like tcpdump does."""
        result = []
        if self.flags & self.SYN: result.append('S')
        if self.flags & self.FIN: result.append('F')
        if self.flags & self.RST: result.append('R')
        if self.flags & self.PSH: result.append('P')
        if self.flags & self.ACK: result.append('.')
        if self.flags & self.URG: result.append('U')
        return ''.join(result) or '-'
    
    def __str__(self) -> str:
        return (f"TCP: {self.src_port} → {self.dst_port} "
                f"[{self.flags_str()}] seq={self.seq} ack={self.ack} "
                f"win={self.window} len={len(self.payload)}")
```

### TCP State Machine

```python
class TCPState:
    """
    TCP connection state machine.
    Stevens illustrated this exhaustively—every transition, every edge case.
    """
    
    # TCP States
    CLOSED = 'CLOSED'
    LISTEN = 'LISTEN'
    SYN_SENT = 'SYN_SENT'
    SYN_RECEIVED = 'SYN_RECEIVED'
    ESTABLISHED = 'ESTABLISHED'
    FIN_WAIT_1 = 'FIN_WAIT_1'
    FIN_WAIT_2 = 'FIN_WAIT_2'
    CLOSE_WAIT = 'CLOSE_WAIT'
    CLOSING = 'CLOSING'
    LAST_ACK = 'LAST_ACK'
    TIME_WAIT = 'TIME_WAIT'
    
    def __init__(self):
        self.state = self.CLOSED
        self.local_seq = 0
        self.remote_seq = 0
        self.local_port = 0
        self.remote_port = 0
    
    def transition(self, event: str, segment: TCPSegment = None) -> str:
        """
        State transition based on event.
        Returns action to take.
        """
        old_state = self.state
        action = None
        
        # Connection establishment (client side)
        if self.state == self.CLOSED:
            if event == 'active_open':
                self.state = self.SYN_SENT
                action = 'send_syn'
        
        elif self.state == self.SYN_SENT:
            if event == 'recv_syn_ack':
                self.state = self.ESTABLISHED
                action = 'send_ack'
            elif event == 'recv_syn':  # Simultaneous open
                self.state = self.SYN_RECEIVED
                action = 'send_syn_ack'
        
        # Connection establishment (server side)
        elif self.state == self.LISTEN:
            if event == 'recv_syn':
                self.state = self.SYN_RECEIVED
                action = 'send_syn_ack'
        
        elif self.state == self.SYN_RECEIVED:
            if event == 'recv_ack':
                self.state = self.ESTABLISHED
                action = 'connected'
        
        # Data transfer
        elif self.state == self.ESTABLISHED:
            if event == 'close':
                self.state = self.FIN_WAIT_1
                action = 'send_fin'
            elif event == 'recv_fin':
                self.state = self.CLOSE_WAIT
                action = 'send_ack'
        
        # Connection termination (active close)
        elif self.state == self.FIN_WAIT_1:
            if event == 'recv_ack':
                self.state = self.FIN_WAIT_2
            elif event == 'recv_fin':
                self.state = self.CLOSING
                action = 'send_ack'
            elif event == 'recv_fin_ack':
                self.state = self.TIME_WAIT
                action = 'send_ack'
        
        elif self.state == self.FIN_WAIT_2:
            if event == 'recv_fin':
                self.state = self.TIME_WAIT
                action = 'send_ack'
        
        elif self.state == self.CLOSING:
            if event == 'recv_ack':
                self.state = self.TIME_WAIT
        
        # Connection termination (passive close)
        elif self.state == self.CLOSE_WAIT:
            if event == 'close':
                self.state = self.LAST_ACK
                action = 'send_fin'
        
        elif self.state == self.LAST_ACK:
            if event == 'recv_ack':
                self.state = self.CLOSED
        
        # TIME_WAIT
        elif self.state == self.TIME_WAIT:
            if event == 'timeout_2msl':
                self.state = self.CLOSED
        
        return action
    
    def __str__(self) -> str:
        return f"TCP State: {self.state}"


def visualize_three_way_handshake():
    """
    Stevens' classic illustration of TCP three-way handshake.
    """
    return """
    Client                                Server
      |                                      |
      |  SYN seq=x                          |
      | ----------------------------------→ |
      |                                      |
      |              SYN seq=y, ACK=x+1     |
      | ←---------------------------------- |
      |                                      |
      |  ACK=y+1                            |
      | ----------------------------------→ |
      |                                      |
      |          ESTABLISHED                 |
      
    Packet 1: Client → Server [SYN] seq=1000
    Packet 2: Server → Client [SYN,ACK] seq=2000, ack=1001
    Packet 3: Client → Server [ACK] seq=1001, ack=2001
    """


def visualize_four_way_close():
    """
    TCP connection termination.
    """
    return """
    Active Close                      Passive Close
      |                                      |
      |  FIN seq=x                          |
      | ----------------------------------→ |
      |                         CLOSE_WAIT  |
      |              ACK=x+1                |
      | ←---------------------------------- |
      | FIN_WAIT_2                          |
      |                                      |
      |              FIN seq=y              |
      | ←---------------------------------- |
      |                          LAST_ACK   |
      |  ACK=y+1                            |
      | ----------------------------------→ |
      | TIME_WAIT                   CLOSED  |
      |                                      |
      | (wait 2×MSL)                        |
      | CLOSED                              |
    """
```

### DNS Protocol

```python
@dataclass
class DNSHeader:
    """
    DNS message header (12 bytes).
    
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                      Transaction ID                           |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |              |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                         QDCOUNT                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                         ANCOUNT                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                         NSCOUNT                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                         ARCOUNT                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    """
    id: int
    qr: int          # 0=query, 1=response
    opcode: int      # 0=standard query
    aa: int          # Authoritative Answer
    tc: int          # Truncation
    rd: int          # Recursion Desired
    ra: int          # Recursion Available
    rcode: int       # Response code
    qdcount: int     # Question count
    ancount: int     # Answer count
    nscount: int     # Authority count
    arcount: int     # Additional count
    
    @classmethod
    def parse(cls, data: bytes) -> 'DNSHeader':
        id = struct.unpack('!H', data[0:2])[0]
        flags = struct.unpack('!H', data[2:4])[0]
        
        qr = (flags >> 15) & 0x1
        opcode = (flags >> 11) & 0xF
        aa = (flags >> 10) & 0x1
        tc = (flags >> 9) & 0x1
        rd = (flags >> 8) & 0x1
        ra = (flags >> 7) & 0x1
        rcode = flags & 0xF
        
        qdcount = struct.unpack('!H', data[4:6])[0]
        ancount = struct.unpack('!H', data[6:8])[0]
        nscount = struct.unpack('!H', data[8:10])[0]
        arcount = struct.unpack('!H', data[10:12])[0]
        
        return cls(id, qr, opcode, aa, tc, rd, ra, rcode,
                   qdcount, ancount, nscount, arcount)


class DNSParser:
    """
    Parse DNS messages.
    Stevens showed how DNS name compression works.
    """
    
    RECORD_TYPES = {
        1: 'A',
        2: 'NS',
        5: 'CNAME',
        6: 'SOA',
        15: 'MX',
        16: 'TXT',
        28: 'AAAA',
    }
    
    def __init__(self, data: bytes):
        self.data = data
        self.offset = 0
    
    def parse_name(self, offset: int = None) -> tuple:
        """
        Parse a DNS name with compression support.
        
        Compression: If high 2 bits are 11, next 14 bits are pointer.
        """
        if offset is None:
            offset = self.offset
        
        labels = []
        jumped = False
        original_offset = offset
        
        while True:
            length = self.data[offset]
            
            if length == 0:
                offset += 1
                break
            
            if (length & 0xC0) == 0xC0:
                # Compression pointer
                pointer = struct.unpack('!H', self.data[offset:offset+2])[0]
                pointer &= 0x3FFF
                
                if not jumped:
                    self.offset = offset + 2
                jumped = True
                offset = pointer
            else:
                # Regular label
                offset += 1
                labels.append(self.data[offset:offset+length].decode('ascii'))
                offset += length
        
        if not jumped:
            self.offset = offset
        
        return '.'.join(labels), offset - original_offset
```

### Layer Analysis Tool

```python
class PacketAnalyzer:
    """
    Stevens-style packet analysis.
    Parse and display each layer.
    """
    
    def analyze(self, raw_bytes: bytes) -> dict:
        """
        Analyze a packet layer by layer.
        """
        result = {'layers': [], 'raw': raw_bytes.hex()}
        offset = 0
        
        # Layer 2: Ethernet
        try:
            eth = EthernetFrame.parse(raw_bytes)
            result['layers'].append({
                'layer': 2,
                'protocol': 'Ethernet',
                'summary': str(eth),
                'details': {
                    'dst_mac': eth.format_mac(eth.dst_mac),
                    'src_mac': eth.format_mac(eth.src_mac),
                    'ethertype': f'0x{eth.ethertype:04x}',
                }
            })
            
            if eth.ethertype == EtherType.IPv4:
                result.update(self._analyze_ipv4(eth.payload))
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _analyze_ipv4(self, data: bytes) -> dict:
        """Analyze IPv4 layer."""
        result = {'layers': []}
        
        try:
            ip = IPv4Packet.parse(data)
            result['layers'].append({
                'layer': 3,
                'protocol': 'IPv4',
                'summary': str(ip),
                'details': {
                    'version': ip.version,
                    'header_length': ip.ihl * 4,
                    'total_length': ip.total_length,
                    'ttl': ip.ttl,
                    'protocol': ip.protocol,
                    'src': ip.src_ip,
                    'dst': ip.dst_ip,
                }
            })
            
            if ip.protocol == IPProtocol.TCP:
                result['layers'].extend(self._analyze_tcp(ip.payload)['layers'])
            elif ip.protocol == IPProtocol.UDP:
                result['layers'].extend(self._analyze_udp(ip.payload)['layers'])
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _analyze_tcp(self, data: bytes) -> dict:
        """Analyze TCP layer."""
        result = {'layers': []}
        
        try:
            tcp = TCPSegment.parse(data)
            result['layers'].append({
                'layer': 4,
                'protocol': 'TCP',
                'summary': str(tcp),
                'details': {
                    'src_port': tcp.src_port,
                    'dst_port': tcp.dst_port,
                    'seq': tcp.seq,
                    'ack': tcp.ack,
                    'flags': tcp.flags_str(),
                    'window': tcp.window,
                    'payload_length': len(tcp.payload),
                }
            })
            
            # Try to identify application protocol
            if tcp.dst_port == 80 or tcp.src_port == 80:
                result['layers'].append({
                    'layer': 7,
                    'protocol': 'HTTP',
                    'payload_preview': tcp.payload[:100].decode('utf-8', errors='replace')
                })
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def hexdump(self, data: bytes, bytes_per_line: int = 16) -> str:
        """
        Stevens-style hex dump.
        """
        lines = []
        for i in range(0, len(data), bytes_per_line):
            chunk = data[i:i+bytes_per_line]
            hex_part = ' '.join(f'{b:02x}' for b in chunk)
            ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
            lines.append(f'{i:04x}  {hex_part:<48}  {ascii_part}')
        return '\n'.join(lines)


def capture_and_analyze(interface: str = 'eth0', count: int = 10):
    """
    Capture packets and analyze them Stevens-style.
    """
    import socket
    
    # Raw socket to capture all packets
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
    sock.bind((interface, 0))
    
    analyzer = PacketAnalyzer()
    
    for i in range(count):
        raw, addr = sock.recvfrom(65535)
        
        print(f"\n{'='*60}")
        print(f"Packet {i+1}: {len(raw)} bytes")
        print('='*60)
        
        result = analyzer.analyze(raw)
        
        for layer in result.get('layers', []):
            print(f"\nLayer {layer['layer']}: {layer['protocol']}")
            print(f"  {layer['summary']}")
        
        print(f"\nHex dump:")
        print(analyzer.hexdump(raw[:64]))  # First 64 bytes
```

## Mental Model

Stevens approaches networking by asking:

1. **What's on the wire?** Capture and examine the packets
2. **What layer is this?** Work through each layer systematically
3. **What does each byte mean?** Know the protocol format
4. **What state is the connection in?** Track the state machine
5. **What does the RFC say?** The specification is the authority

## The Protocol Analysis Checklist

```
□ Capture packets with tcpdump/Wireshark
□ Identify the protocol at each layer
□ Parse headers field by field
□ Track sequence numbers and state
□ Look for retransmissions and errors
□ Check for fragmentation
□ Verify checksums if suspicious
□ Compare to RFC specification
```

## Signature Stevens Moves

- Packet traces with hex dumps
- Layer-by-layer analysis
- Header field diagrams (RFC style)
- State machine diagrams
- tcpdump command mastery
- RFC references for every claim
- Real behavior over documented behavior
- "Show me the packets"
