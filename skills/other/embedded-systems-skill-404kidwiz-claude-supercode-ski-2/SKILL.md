---
name: embedded-systems
description: Expert in RTOS, bare-metal programming, and embedded Linux. Specializes in Rust for Embedded and high-reliability firmware.
---

# Embedded Systems Engineer

## Purpose

Provides embedded software development expertise specializing in RTOS, bare-metal firmware, and Embedded Linux. Focuses on safety-critical code, power optimization, and hardware abstraction for microcontrollers (STM32, ESP32) and embedded Linux systems.

## When to Use

- Writing firmware for microcontrollers (STM32, NXP, ESP32)
- Configuring Real-Time Operating Systems (Zephyr, FreeRTOS)
- Developing drivers for sensors/peripherals (I2C, SPI, UART)
- Building Embedded Linux systems (Yocto, Buildroot)
- Implementing OTA (Over-The-Air) update mechanisms
- Analyzing crash dumps or debugging hardware faults (JTAG/SWD)

---
---

## 2. Decision Framework

### OS Selection

```
What is the hardware capability?
│
├─ **Microcontroller (MCU) - < 1MB RAM**
│  ├─ Hard Real-Time? → **Zephyr / FreeRTOS** (Preemptive scheduler)
│  ├─ Safety Critical? → **SafeRTOS / Rust (Bare Metal)**
│  └─ Simple Loop? → **Bare Metal (Superloop)**
│
└─ **Microprocessor (MPU) - > 64MB RAM**
   ├─ Complex UI / Networking? → **Embedded Linux (Yocto/Buildroot)**
   └─ Hard Real-Time? → **RT-Linux (PREEMPT_RT)** or **Dual Core (Linux + MCU)**
```

### Language Choice (2026 Standards)

| Language | Use Case | Recommendation |
|----------|----------|----------------|
| **C (C11/C17)** | Legacy / HALs | Still dominant. Use strict static analysis (MISRA). |
| **C++ (C++20)** | Complex Logic | Use `noexcept`, `no-rtti` for embedded. Zero-cost abstractions. |
| **Rust** | New Projects | **Highly Recommended.** Memory safety without GC. `embedded-hal`. |
| **MicroPython** | Prototyping | Good for rapid testing, bad for production real-time. |

### Update Strategy (OTA)

1.  **Dual Bank (A/B):** Safe but requires 2x Flash.
2.  **Compressed Image:** Saves Flash, requires RAM for decompression.
3.  **Delta Updates:** Minimal bandwidth, complex patching logic.

**Red Flags → Escalate to `security-engineer`:**
- JTAG port left open in production units
- Secure Boot keys stored in plain text code
- Firmware updates not signed (integrity check only, no authenticity)
- Using `strcpy` or unbounded buffers in C code

---
---

### Workflow 2: Zephyr RTOS Application

**Goal:** Read sensor via I2C and print to console.

**Steps:**

1.  **Device Tree (`app.overlay`)**
    ```dts
    &i2c1 {
        status = "okay";
        bme280@76 {
            compatible = "bosch,bme280";
            reg = <0x76>;
            label = "BME280";
        };
    };
    ```

2.  **Configuration (`prj.conf`)**
    ```ini
    CONFIG_I2C=y
    CONFIG_SENSOR=y
    CONFIG_CBPRINTF_FP_SUPPORT=y
    ```

3.  **Code (`main.c`)**
    ```c
    #include <zephyr/kernel.h>
    #include <zephyr/device.h>
    #include <zephyr/drivers/sensor.h>

    void main(void) {
        const struct device *dev = DEVICE_DT_GET_ANY(bosch_bme280);
        
        while (1) {
            sensor_sample_fetch(dev);
            struct sensor_value temp;
            sensor_channel_get(dev, SENSOR_CHAN_AMBIENT_TEMP, &temp);
            printk("Temp: %d.%06d C\n", temp.val1, temp.val2);
            k_sleep(K_SECONDS(1));
        }
    }
    ```

---
---

## 4. Patterns & Templates

### Pattern 1: State Machine (Bare Metal)

**Use case:** Handling complex device logic without an OS.

```c
typedef enum { STATE_IDLE, STATE_READING, STATE_SENDING, STATE_ERROR } SystemState;

void loop() {
    static SystemState state = STATE_IDLE;
    
    switch(state) {
        case STATE_IDLE:
            if (timerExpired()) state = STATE_READING;
            break;
        case STATE_READING:
            if (readSensor()) state = STATE_SENDING;
            else state = STATE_ERROR;
            break;
        case STATE_SENDING:
            sendData();
            state = STATE_IDLE;
            break;
        // ...
    }
}
```

### Pattern 2: Interrupt Deferred Processing

**Use case:** Keeping ISRs (Interrupt Service Routines) short.

*   **ISR:** Set a flag or push data to a ring buffer. Return immediately.
*   **Main Loop / Task:** Check buffer/flag and process data (e.g., parse GPS NMEA string).
*   *Why?* Long ISRs block other interrupts and crash the system.

### Pattern 3: Watchdog Feeder

**Use case:** Auto-reset if the system freezes.

```c
void watchdog_task(void *pvParameters) {
    while(1) {
        // Only kick if critical flags are set
        if (check_system_health()) {
            wdt_feed();
        }
        vTaskDelay(1000);
    }
}
```

---
---

## 6. Integration Patterns

### **iot-engineer:**
-   **Handoff**: Embedded Eng writes the driver (I2C) → IoT Eng writes the MQTT logic.
-   **Collaboration**: Power budget (how often to wake up radio).
-   **Tools**: Power Profiler.

### **mobile-app-developer:**
-   **Handoff**: Embedded Eng implements BLE GATT Server → Mobile Dev implements Client.
-   **Collaboration**: Defining the GATT Service/Characteristic UUIDs.
-   **Tools**: nRF Connect.

### **cloud-architect:**
-   **Handoff**: Embedded Eng implements OTA agent → Cloud Architect implements Update Server (S3/Signed URL).
-   **Collaboration**: Security token format (JWT/X.509).
-   **Tools**: AWS IoT Jobs.

---
