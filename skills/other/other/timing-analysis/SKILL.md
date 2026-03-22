---
name: timing-analysis
description: Analyze real-time constraints, ISR latency, DMA transfer times, and LED protocol timing for embedded systems. Use when debugging timing-sensitive code, optimizing frame rates, or verifying protocol compliance.
argument-hint: <component, function, or timing issue to analyze>
context: fork
agent: timing-analysis-agent
---

Analyze timing-critical code paths for real-time constraint violations and optimization opportunities.

$ARGUMENTS

## What This Skill Analyzes

### LED Protocol Timing
- WS2812/SK6812/APA106 bit timing compliance (T0H, T0L, T1H, T1L, reset)
- SPI clock rate calculations for wave8 encoding
- RMT resolution and duration encoding accuracy
- Reset pulse duration adequacy across chipsets

### Frame Rate Analysis
- Total frame time budget (show() to DMA complete to reset delay)
- Per-LED encoding time multiplied by LED count = encoding phase duration
- DMA transfer time at configured clock rate
- Inter-frame gap and CPU availability

### ISR Latency
- Interrupt response time constraints
- ISR execution time (must be <10us for most applications)
- Priority inversion risks from ISR-held resources
- Nested interrupt handling

### DMA Transfer Timing
- Transfer size multiplied by clock period = transfer duration
- Double-buffer swap timing and pipeline stalls
- Chunk encoding overlap with DMA transmission
- SPI/I2S/RMT peripheral clock configuration

## How To Use

```
/timing-analysis src/platforms/esp/32/drivers/spi/
/timing-analysis What is the maximum frame rate for 300 WS2812 LEDs on ESP32-S3 using SPI?
/timing-analysis Check if the RMT timing meets WS2812 spec
```

## What You'll Get

- Timing breakdown with calculated durations (ns/us/ms precision)
- Protocol compliance verification against LED chipset datasheets
- Frame rate estimates for given LED counts
- Bottleneck identification and optimization suggestions
- Clock configuration recommendations
