---
title: PRISM K1 Firmware Specification
slug: prism-k1-firmware
description: Complete technical specification for PRISM K1 ESP32-S3 LED controller firmware, including hardware constraints, FreeRTOS configuration, memory layout, WebSocket protocol, and real-time LED control parameters.
category: embedded
created: 2025-10-21
last_updated: 2025-10-21
source: firmware/PRISM.k1/.taskmaster/CANON.md (Generated from 8 ADRs)
---

# PRISM K1 Firmware Specification

**Authoritative Source:** Generated from Architecture Decision Records (ADRs 001-008)
**Updated:** 2025-10-18 06:33:29 UTC
**Status:** APPROVED for all production firmware

---

## 1. Hardware Specification

### Microcontroller
- **Chip:** ESP32-S3 dual-core processor
- **Flash:** 8MB total (4.75MB used, 3.25MB reserved)
- **RAM:** Dynamic allocation via memory pools (see Memory Management)
- **Built-in:** WiFi, Bluetooth LE, 802.15.4

### LED Configuration
- **LED Count:** 320 addressable LEDs (WS2812B compatible)
- **LED Type:** WS2812B RGB8 (3 bytes per pixel = 960 bytes per frame)
- **Mapping:** Concat-2x160 (dual GPIO parallel output)
  - GPIO 9: 0–159 (160 LEDs)
  - GPIO 10: 160–319 (160 LEDs)
- **Refresh Rate:** 120 FPS target (updated from 60 FPS)
  - Minimum frame time: 8.33ms per frame
  - Real-time task priority: HIGHEST (10)

### Power & Timing
- **Frame buffer size:** 320 × 3 bytes = 960 bytes per frame
- **WebSocket buffer:** 4096 bytes (4KB) per connection
- **Max concurrent WebSocket clients:** 2
- **WebSocket timeout:** 5000ms (5 seconds)

---

## 2. Flash Memory Layout (8MB Total)

### Partition Table (64KB-aligned offsets)

| Name | Type | SubType | Offset | Size | Purpose |
|------|------|---------|--------|------|---------|
| nvs | data | nvs | 0x9000 | 24KB | Non-Volatile Storage (WiFi settings) |
| otadata | data | ota | 0xF000 | 8KB | OTA metadata |
| app0 | app | ota_0 | 0x20000 | 1.5MB | Primary application image |
| app1 | app | ota_1 | 0x1A0000 | 1.5MB | OTA backup image |
| littlefs | data | 0x82 | 0x320000 | 1.5MB | Pattern/template storage |

### Memory Usage
- **End of littlefs:** 0x4A0000 = 4.75MB (absolute end)
- **Remaining free:** 3.25MB (reserved for expansion)
- **OTA capable:** Yes (dual app partition enables zero-downtime updates)

### Storage Constraints
- **Pattern max size:** 256KB per pattern file
- **Minimum patterns:** 15 templates must fit
- **Safety margin:** 100KB reserved for filesystem overhead
- **Usable littlefs space:** 1.5MB - 100KB - (15 × 100KB avg) ≈ 500KB headroom

---

## 3. FreeRTOS Task Configuration

### Task Priority Levels (Higher = More Real-Time)

| Task | Priority | Stack Size | Purpose | Notes |
|------|----------|-----------|---------|-------|
| **Playback** | 10 (HIGHEST) | 8KB | LED frame generation & I2S output | Real-time, 120 FPS |
| **Network** | 5 (Medium) | 8KB | WiFi & WebSocket communication | Handles rx/tx |
| **Storage** | 4 (Medium-low) | 6KB | Pattern file I/O | Blocking operations |
| **Templates** | 3 (Low) | 6KB | Pattern generation/processing | Background work |

### Key Constraints
- **Playback is HIGHEST priority** — Ensures 120 FPS LED refresh never starves
- **Stack allocation is conservative** — Prevents fragmentation
- **All tasks use memory pools** — Prevents uncontrolled malloc fragmentation
- **Memory pool init is CRITICAL** — Must run before any other allocation

### Real-Time Guarantees
- **Playback task never blocked** by file I/O, network, or template work
- **Frame deadline:** 8.33ms per frame (120 FPS)
- **Heap monitor running continuously** — Detects memory leaks in real-time

---

## 4. WebSocket Communication Protocol

### Connection Parameters
- **Port:** Configurable (typically 8080 or 9000)
- **Buffer per client:** 4096 bytes (4KB)
- **Max clients:** 2 simultaneous connections
- **Timeout:** 5000ms (auto-disconnect if no activity)
- **Frame format:** TLV (Type-Length-Value)

### TLV Message Types

| Type | Value | Purpose | Size |
|------|-------|---------|------|
| PUT_BEGIN (0x01) | 4 bytes | Indicate total payload size | Fixed |
| PUT_DATA (0x02) | 4089 bytes | Chunked pattern data | Variable |
| PUT_END (0x03) | 4 bytes | CRC32 checksum | Fixed |

### Message Constraints
- **Payload max:** 262,144 bytes (256KB = pattern_max_size)
- **Chunk size:** 4089 bytes per PUT_DATA message
- **CRC32 validation:** Mandatory on all payloads
- **Example:** 256KB pattern = 63 PUT_DATA chunks + BEGIN + END

### Connection Flow
1. Client opens WebSocket connection
2. Client sends PUT_BEGIN with total payload size
3. Client sends PUT_DATA messages (4089 bytes each)
4. Client sends PUT_END with CRC32 checksum
5. Firmware validates CRC32 and stores pattern
6. Firmware acknowledges with status response

---

## 5. LED Output Timing

### Refresh Rate Target
- **Target FPS:** 120 FPS (updated from 60 FPS)
- **Frame period:** 8.33ms
- **I2S clock:** WS2812B protocol timing (800kHz)
- **Frame data:** 320 pixels × 3 bytes = 960 bytes per frame

### I2S Configuration
- **DMA-driven output** via GPIO 9 & GPIO 10 (parallel)
- **Duty cycle:** 100% (continuous output stream)
- **Backpressure:** Network/storage tasks don't affect playback

### Color Format
- **RGB8:** 8-bit red, 8-bit green, 8-bit blue per pixel
- **Byte order:** RGB (red first, then green, then blue)
- **Mapping:** Pixels 0-159 via GPIO9, pixels 160-319 via GPIO10

---

## 6. Pattern Storage & Management

### LittleFS Mount Point
- **Path:** `/littlefs`
- **Size:** 1.5MB partition
- **Type:** LittleFS (wear-leveling, transaction support)
- **Features:** Survives power loss safely

### Pattern File Organization
- **Max pattern file size:** 256KB (262,144 bytes)
- **Minimum patterns to support:** 15 templates
- **Safety margin:** 100KB reserved for filesystem overhead
- **Typical pattern size:** ~100KB (allows ~15 patterns comfortably)

### Pattern Metadata
- **Pattern files:** Stored as binary blobs in `/littlefs`
- **Template system:** 15 predefined templates
- **Upload mechanism:** WebSocket TLV protocol (PUT_BEGIN/PUT_DATA/PUT_END)
- **Verification:** CRC32 checksum mandatory

---

## 7. Memory Management

### Memory Pool Architecture
- **Prism memory pool:** Custom allocator to prevent fragmentation
- **Initialization order:** FIRST before all other subsystems
- **Heap monitor:** Continuous tracking of allocations
- **Report frequency:** Every 30 seconds to UART log

### Memory Constraints
- **Playback task stack:** 8KB (frame generation only)
- **Network task stack:** 8KB (rx/tx buffers)
- **WebSocket frame buffer:** 4096 bytes per client
- **Total heap headroom:** Monitored continuously

### Free Heap Tracking
- **Free heap size:** Logged at startup
- **Minimum free heap:** Tracked across all time
- **Heap fragmentation:** Detected by monitor
- **Out-of-memory handling:** Graceful degradation

---

## 8. System Initialization Sequence

### Boot Order (CRITICAL)
1. **Memory pool init** ← MUST be first
2. **NVS flash init** (WiFi/settings storage)
3. **TCP/IP stack init**
4. **Event loop creation**
5. **Heap monitor init**
6. **Network manager start** (WiFi connection)
7. **Pattern storage mount** (LittleFS)
8. **LED playback task launch** (highest priority)
9. **Template manager init** (background)

### Firmware Version
- **Version:** 1.0.0
- **Build:** Timestamp embedded at compile time
- **OTA capable:** Yes (dual partition table)

---

## 9. Real-Time Constraints (ADR-008)

### LED Refresh Timing
- **Target:** 120 FPS (increased from 60 FPS)
- **Tolerance:** ±5% jitter acceptable
- **Hard deadline:** 8.33ms per frame
- **Overruns:** Logged, frame dropped if necessary

### Task Scheduling
- **Playback preempts all:** Priority 10 ensures real-time
- **Network (priority 5)** doesn't block playback
- **Storage (priority 4)** doesn't block playback
- **Templates (priority 3)** only run when higher priority tasks idle

---

## 10. Common Integration Points

### Connecting from PRISM.node (Web Editor)
```javascript
// 1. Connect WebSocket
const ws = new WebSocket('ws://device-ip:8080');

// 2. Create payload (262KB max)
const payload = /* pattern binary data */;

// 3. Create TLV plan (auto-chunks to 4089 bytes)
const plan = makePutPlan(payload);  // See: wsTlv.ts

// 4. Send over WebSocket
await sendPlanOverWs('ws://device-ip:8080', plan);

// 5. Firmware validates CRC32 and stores to /littlefs
// 6. LED playback reads pattern and displays at 120 FPS
```

### Debugging via UART
- **Baud rate:** 115200
- **Log tags:** PRISM-K1, memory_pool, network, playback, storage, templates
- **Output:** Memory stats every 30 seconds
- **Enable test mode:** `uart_test_start()`

### Memory Pool API
```c
// From prism_memory_pool.h
esp_err_t prism_pool_init(void);  // Call FIRST in system_init()
void prism_pool_dump_state(void);  // Debug: show allocations
void prism_heap_monitor_init(void);  // Continuous monitoring
void prism_heap_monitor_dump_stats(void);  // Debug: show stats
```

---

## 11. ADR Reference

| ADR | Title | Status | Key Decision |
|-----|-------|--------|--------------|
| 001 | ESP32-S3 Partition Table | APPROVED | OTA-enabled dual-app layout |
| 002 | WebSocket Buffer Size | APPROVED | 4KB buffer, 98% success rate |
| 003 | LED Count Standardization | APPROVED | 320 WS2812B LEDs |
| 004 | Pattern Maximum Size | APPROVED | 256KB per pattern file |
| 005 | Storage Mount Path | APPROVED | LittleFS at `/littlefs` |
| 006 | Pattern Count Revision | APPROVED | 15 templates minimum (was 25) |
| 007 | Partition Alignment Correction | APPROVED | 64KB-aligned offsets |
| 008 | LED FPS Increase | APPROVED | 120 FPS target (was 60) |

---

## 12. Quick Reference Table

| Parameter | Value | Notes |
|-----------|-------|-------|
| **LED Count** | 320 | WS2812B RGB8 |
| **LED FPS** | 120 | Real-time target |
| **Frame size** | 960 bytes | 320 × 3 bytes RGB8 |
| **Max pattern size** | 256KB | Per file |
| **Min patterns** | 15 | Templates |
| **Storage partition** | 1.5MB | LittleFS |
| **WebSocket buffer** | 4KB | Per client |
| **Max WebSocket clients** | 2 | Concurrent |
| **WS timeout** | 5s | Auto-disconnect |
| **Playback priority** | 10 | HIGHEST |
| **Playback stack** | 8KB | Real-time task |
| **Flash used** | 4.75MB | Of 8MB total |
| **OTA capable** | Yes | Dual partition |

---

## 13. Common Code Examples

### Reading Pattern from LittleFS
```c
#include "pattern_storage.h"

FILE *fp = fopen("/littlefs/pattern_001.bin", "rb");
uint8_t pattern[256 * 1024];
size_t bytes_read = fread(pattern, 1, sizeof(pattern), fp);
fclose(fp);
```

### Logging from Firmware
```c
#include "esp_log.h"

static const char *TAG = "MY_MODULE";
ESP_LOGI(TAG, "Starting playback: %d pixels at 120 FPS", led_count);
ESP_LOGE(TAG, "Memory pool init failed: %d", ret);
```

### Task Creation
```c
xTaskCreate(
    playback_task,              // Task function
    "playback",                 // Task name
    STACK_PLAYBACK,             // Stack size
    NULL,                       // Parameters
    PRIORITY_PLAYBACK,          // Priority
    NULL                        // Task handle
);
```

---

## 14. Troubleshooting Checklist

- [ ] Memory pool initialized first? (Check main.c system_init())
- [ ] NVS flash initialized? (Required for WiFi settings)
- [ ] LittleFS mounted? (Check fopen() returns non-NULL)
- [ ] Playback task priority = 10? (Not lower)
- [ ] WebSocket timeout < 5s? (Prevents stale connections)
- [ ] Pattern CRC32 validated? (Prevents corruption)
- [ ] LED FPS monitoring enabled? (Via heap monitor stats)
- [ ] Partition table aligned to 64KB? (ESP-IDF requirement)

---

## 15. External References

- **ESP-IDF:** FreeRTOS APIs, GPIO, I2S, NVS, LittleFS
- **WS2812B Protocol:** GPIO timing, DMA streaming
- **TLV Format:** Simple Type-Length-Value serialization
- **CRC32:** Polynomial 0xEDB88320 (standard)

---

**This specification is AUTHORITATIVE. All firmware code MUST match these parameters. Changes require ADR and CANON.md regeneration.**

*Last updated: 2025-10-21 by Claude Code Captain*
