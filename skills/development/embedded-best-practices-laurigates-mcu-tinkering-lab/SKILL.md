---
name: embedded-best-practices
description: Embedded systems development best practices for ESP32, FreeRTOS, and ESP-IDF. Use when writing firmware code, reviewing implementations, or learning about embedded patterns.
allowed-tools: Read, Grep, Glob
---

# Embedded Best Practices Skill

This skill provides comprehensive guidance for embedded systems development with a focus on ESP32 and ESP-IDF.

## When to Use
- Writing new firmware code
- Reviewing implementation approaches
- Learning embedded patterns
- Debugging issues
- Optimizing code

## ESP-IDF Project Structure

### Recommended Layout
```
project/
├── main/
│   ├── CMakeLists.txt
│   ├── main.c
│   ├── Kconfig.projbuild
│   └── include/
│       └── project.h
├── components/
│   └── custom_component/
│       ├── CMakeLists.txt
│       ├── component.c
│       └── include/
│           └── component.h
├── CMakeLists.txt
├── sdkconfig.defaults
├── partitions.csv
└── README.md
```

### Component Organization
- One responsibility per component
- Clear public interface in include/
- Private implementation in src/
- Document dependencies

## FreeRTOS Best Practices

### Task Design
```c
// Good: Proper task function
void sensor_task(void *pvParameters) {
    sensor_config_t *config = (sensor_config_t *)pvParameters;

    while (1) {
        // Do work
        read_sensor(config);

        // Must yield to prevent watchdog
        vTaskDelay(pdMS_TO_TICKS(100));
    }

    // Tasks should never return, but if they do:
    vTaskDelete(NULL);
}

// Create with appropriate stack
xTaskCreate(sensor_task, "sensor", 4096, &config, 5, &task_handle);
```

### Stack Sizing
- Start with 4096 bytes for typical tasks
- Use `uxTaskGetStackHighWaterMark()` to measure actual usage
- Add 25% safety margin
- Camera/network tasks may need 8192+

### Synchronization
```c
// Mutex for shared resource protection
SemaphoreHandle_t mutex = xSemaphoreCreateMutex();

// Use with timeout, never infinite wait in production
if (xSemaphoreTake(mutex, pdMS_TO_TICKS(1000)) == pdTRUE) {
    // Access shared resource
    xSemaphoreGive(mutex);
} else {
    ESP_LOGE(TAG, "Failed to acquire mutex");
}
```

### Queue Usage
```c
// Prefer queues for inter-task communication
QueueHandle_t data_queue = xQueueCreate(10, sizeof(sensor_data_t));

// Send with timeout
sensor_data_t data = {.value = 42};
if (xQueueSend(data_queue, &data, pdMS_TO_TICKS(100)) != pdTRUE) {
    ESP_LOGW(TAG, "Queue full, dropping data");
}

// Receive
sensor_data_t received;
if (xQueueReceive(data_queue, &received, portMAX_DELAY) == pdTRUE) {
    process_data(&received);
}
```

## Memory Management

### Static vs Dynamic Allocation
```c
// Prefer static for fixed resources
static StaticTask_t task_buffer;
static StackType_t task_stack[4096];
TaskHandle_t task = xTaskCreateStatic(
    task_func, "task", 4096, NULL, 5,
    task_stack, &task_buffer
);

// Dynamic for variable-size resources
char *buffer = heap_caps_malloc(size, MALLOC_CAP_DEFAULT);
if (buffer == NULL) {
    ESP_LOGE(TAG, "Allocation failed");
    return ESP_ERR_NO_MEM;
}
// ... use buffer ...
free(buffer);
```

### String Handling
```c
// Bad
char buf[64];
sprintf(buf, "Value: %d", value);

// Good - prevents buffer overflow
char buf[64];
snprintf(buf, sizeof(buf), "Value: %d", value);

// For const strings, keep in flash
static const char *TAG = "mymodule";
ESP_LOGI(TAG, "Starting");
```

## Error Handling

### ESP-IDF Error Pattern
```c
esp_err_t initialize_peripheral(void) {
    esp_err_t ret;

    ret = gpio_config(&io_conf);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "GPIO config failed: %s", esp_err_to_name(ret));
        return ret;
    }

    ret = spi_bus_initialize(SPI2_HOST, &bus_cfg, DMA_CHAN);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "SPI init failed: %s", esp_err_to_name(ret));
        // Clean up GPIO if needed
        return ret;
    }

    return ESP_OK;
}

// Use ESP_ERROR_CHECK for fatal errors only
ESP_ERROR_CHECK(nvs_flash_init());
```

### Graceful Degradation
```c
// Don't crash on non-fatal errors
if (wifi_connect() != ESP_OK) {
    ESP_LOGW(TAG, "WiFi failed, running in offline mode");
    run_offline_mode();
}
```

## Peripheral Initialization

### GPIO Configuration
```c
gpio_config_t io_conf = {
    .pin_bit_mask = (1ULL << GPIO_NUM_2),
    .mode = GPIO_MODE_OUTPUT,
    .pull_up_en = GPIO_PULLUP_DISABLE,
    .pull_down_en = GPIO_PULLDOWN_DISABLE,
    .intr_type = GPIO_INTR_DISABLE,
};
ESP_ERROR_CHECK(gpio_config(&io_conf));
```

### I2C Setup
```c
i2c_config_t conf = {
    .mode = I2C_MODE_MASTER,
    .sda_io_num = GPIO_NUM_21,
    .scl_io_num = GPIO_NUM_22,
    .sda_pullup_en = GPIO_PULLUP_ENABLE,
    .scl_pullup_en = GPIO_PULLUP_ENABLE,
    .master.clk_speed = 400000,
};
ESP_ERROR_CHECK(i2c_param_config(I2C_NUM_0, &conf));
ESP_ERROR_CHECK(i2c_driver_install(I2C_NUM_0, conf.mode, 0, 0, 0));
```

## Interrupt Handlers

### Keep ISRs Minimal
```c
// ISR - keep it SHORT
static void IRAM_ATTR gpio_isr_handler(void *arg) {
    uint32_t gpio_num = (uint32_t)arg;
    // Just signal, don't process
    xQueueSendFromISR(gpio_evt_queue, &gpio_num, NULL);
}

// Process in task
void gpio_task(void *arg) {
    uint32_t io_num;
    while (1) {
        if (xQueueReceive(gpio_evt_queue, &io_num, portMAX_DELAY)) {
            // Heavy processing here, not in ISR
            process_gpio_event(io_num);
        }
    }
}
```

### IRAM Considerations
- Mark ISR handlers with `IRAM_ATTR`
- Functions called from ISR also need `IRAM_ATTR`
- Minimize IRAM usage (limited to ~128KB)

## WiFi Best Practices

### Connection Handling
```c
// Use event loop for WiFi events
static void wifi_event_handler(void *arg, esp_event_base_t event_base,
                               int32_t event_id, void *event_data) {
    if (event_id == WIFI_EVENT_STA_START) {
        esp_wifi_connect();
    } else if (event_id == WIFI_EVENT_STA_DISCONNECTED) {
        ESP_LOGI(TAG, "Disconnected, retrying...");
        esp_wifi_connect();
    }
}

// Register handler
ESP_ERROR_CHECK(esp_event_handler_instance_register(
    WIFI_EVENT, ESP_EVENT_ANY_ID, &wifi_event_handler, NULL, NULL));
```

### PSRAM and WiFi
- WiFi uses significant memory
- Enable PSRAM for memory-intensive applications
- Use `CONFIG_SPIRAM_USE_MALLOC` to extend heap

## Logging

### Log Levels
```c
ESP_LOGE(TAG, "Error: critical failure");      // Always shown
ESP_LOGW(TAG, "Warning: unusual condition");   // Important
ESP_LOGI(TAG, "Info: normal operation");       // Default
ESP_LOGD(TAG, "Debug: detailed info");         // Development
ESP_LOGV(TAG, "Verbose: very detailed");       // Tracing
```

### Production Logging
- Set log level via menuconfig
- Reduce logging in production (ESP_LOGW minimum)
- Log strings consume flash space

## Power Management

### Light Sleep
```c
// Enable automatic light sleep
esp_pm_config_esp32_t pm_config = {
    .max_freq_mhz = 240,
    .min_freq_mhz = 80,
    .light_sleep_enable = true,
};
ESP_ERROR_CHECK(esp_pm_configure(&pm_config));
```

### Deep Sleep
```c
// Configure wakeup source
esp_sleep_enable_timer_wakeup(60 * 1000000);  // 60 seconds

// Enter deep sleep
esp_deep_sleep_start();
```

## Additional Resources

For more detailed information on specific topics, consult:
- ESP-IDF Programming Guide
- FreeRTOS documentation
- ESP32 Technical Reference Manual
