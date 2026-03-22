---
name: expert-rmt5
description: ESP-IDF v5.x RMT5 API expert for LED protocols, encoders, and multi-channel control. Use when working with RMT peripheral programming, LED strip control, or migrating from RMT4 to RMT5.
context: fork
agent: expert-rmt5-agent
---

Get expert guidance on ESP-IDF v5.x RMT (Remote Control Transceiver) peripheral programming.

$ARGUMENTS

## What This Expert Covers

### Implementation & Design
- **LED Strip Control**: WS2812, SK6812, APA106, and custom LED protocols
- **Encoder Architecture**: Copy, Bytes, Simple Callback, and Custom Composite encoders
- **Multi-Channel Sync**: Coordinated transmission across multiple outputs
- **IR Remote Control**: NEC, RC5, and other infrared protocols

### Migration & Modernization
- **RMT4 to RMT5 Migration**: Convert legacy code to new encoder-based architecture
- **API Translation**: Channel handles, symbol structures, clock configuration

### Debugging & Troubleshooting
- Common errors: encoding artifacts, clock source mismatch, timing inaccuracies
- System crashes: Cache safety, IRAM placement, flash operation conflicts
- Performance issues: DMA configuration, encoder optimization

### Configuration & Optimization
- Timing calculations, resolution selection, duration encoding
- DMA setup, buffer sizing, alignment requirements
- Hardware limits across ESP32 family (ESP32, S2, S3, C3, C6, H2)

## What You'll Get

- Complete code examples with detailed comments
- Timing calculations showing duration/resolution conversions
- State machine diagrams for custom encoders
- Hardware compatibility analysis for your target chip
- Testing strategies with edge cases and validation steps
