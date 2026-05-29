---
name: SPH0645-Microphone-Integration
keywords: SPH0645, I2S, microphone, audio input, PDM, PCM, ADC, I2S clock, DMA buffer, noise floor, gain, calibration, audio capture
---

# SPH0645 Microphone Integration

## Quick Reference

SPH0645 is a digital MEMS microphone that outputs PDM (Pulse Density Modulation) audio via I2S interface. Convert PDM to PCM for DSP processing.

## SPH0645 Pin Configuration

| Pin | Function | Notes |
|-----|----------|-------|
| VDD | Power (3.3V) | Bypass capacitor recommended |
| GND | Ground | Power ground |
| CLK | I2S Clock Input | From ESP32 I2S_CLK |
| DIN | Data Out (PDM) | To ESP32 I2S_DIN |
| CS | Chip Select | Usually pulled HIGH or tied to VDD |
| L/R | Channel Select | LOW=left, HIGH=right (tie to GND for mono) |

## I2S Configuration for PDM Input

### 1. I2S Driver Setup
```c
#include "driver/i2s.h"

i2s_config_t i2s_config = {
    .mode = I2S_MODE_MASTER | I2S_MODE_RX,
    .sample_rate = 16000,              // PCM output rate (after decimation)
    .bits_per_sample = I2S_BITS_16,
    .channel_format = I2S_CHANNEL_MONO,
    .communication_format = I2S_COMM_FORMAT_I2S_MSB,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 2,                // Double buffering
    .dma_buf_len = 256,                // Samples per DMA buffer
    .use_apll = false,
    .tx_desc_auto_clear = true,
    .fixed_mclk = 0,
};

i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
```

### 2. Pin Configuration
```c
i2s_pin_config_t pin_config = {
    .bck_io_num = GPIO_NUM_14,         // I2S Bit Clock
    .ws_io_num = GPIO_NUM_13,          // I2S Word Select (not used in PDM, but required)
    .data_out_num = I2S_PIN_NO_CHANGE, // Not used for input
    .data_in_num = GPIO_NUM_12,        // PDM data from SPH0645
};

i2s_set_pin(I2S_NUM_0, &pin_config);
```

### 3. Start I2S Capture
```c
i2s_start(I2S_NUM_0);
```

## PDM to PCM Decimation

PDM stream at 2.4MHz requires decimation filter to convert to usable PCM:

### Simple Moving Average Filter
```c
#define PDM_SAMPLE_RATE 2400000      // 2.4MHz PDM
#define PCM_SAMPLE_RATE 16000        // Target 16kHz PCM
#define DECIMATION_RATIO (PDM_SAMPLE_RATE / PCM_SAMPLE_RATE)  // 150

int16_t pdm_to_pcm(const int16_t *pdm_samples, size_t pdm_count,
                    int16_t *pcm_out) {
    static int32_t accumulator = 0;
    static int count = 0;
    int16_t pcm_sample_count = 0;

    for (size_t i = 0; i < pdm_count; i++) {
        accumulator += pdm_samples[i];
        count++;

        if (count == DECIMATION_RATIO) {
            pcm_out[pcm_sample_count++] = (int16_t)(accumulator / DECIMATION_RATIO);
            accumulator = 0;
            count = 0;
        }
    }

    return pcm_sample_count;  // Number of PCM samples produced
}
```

## Audio Capture with DMA Buffers

### Circular Dual-Buffer Pattern
```c
#define DMA_BUF_SIZE 512
static int16_t dma_buf1[DMA_BUF_SIZE];
static int16_t dma_buf2[DMA_BUF_SIZE];
static int16_t *current_read_buf = dma_buf1;
static int16_t *current_capture_buf = dma_buf2;

void audio_capture_task(void *arg) {
    size_t bytes_read;

    while (1) {
        // Read from I2S DMA buffer
        i2s_read(I2S_NUM_0, current_capture_buf,
                DMA_BUF_SIZE * sizeof(int16_t), &bytes_read, portMAX_DELAY);

        // Switch buffers for processing
        int16_t *temp = current_read_buf;
        current_read_buf = current_capture_buf;
        current_capture_buf = temp;

        // Signal processing task that data is ready
        BaseType_t xHigherPriorityTaskWoken = pdFALSE;
        xTaskNotifyFromISR(dsp_task_handle, 1, eSetBits, &xHigherPriorityTaskWoken);
        portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
    }
}

void dsp_processing_task(void *arg) {
    int16_t pcm_buf[DMA_BUF_SIZE / DECIMATION_RATIO];

    while (1) {
        ulTaskNotifyTake(pdTRUE, portMAX_DELAY);  // Wait for audio data

        // Convert PDM to PCM
        int pcm_count = pdm_to_pcm(current_read_buf, DMA_BUF_SIZE, pcm_buf);

        // Send to FFT/beat detection pipeline
        process_audio_samples(pcm_buf, pcm_count);
    }
}
```

## Noise Floor Calibration

### Calibration on Startup
```c
#define CALIBRATION_SAMPLES 2000

int16_t noise_floor = 0;

void calibrate_microphone(void) {
    int32_t sum = 0;
    int16_t max_amplitude = 0;

    ESP_LOGI(TAG, "Calibrating microphone (quiet environment required)...");

    for (int i = 0; i < CALIBRATION_SAMPLES; i++) {
        size_t bytes_read;
        int16_t sample;
        i2s_read(I2S_NUM_0, &sample, sizeof(int16_t), &bytes_read, portMAX_DELAY);

        int16_t abs_sample = (sample < 0) ? -sample : sample;
        sum += abs_sample;
        if (abs_sample > max_amplitude) max_amplitude = abs_sample;
    }

    int16_t avg_amplitude = sum / CALIBRATION_SAMPLES;
    noise_floor = avg_amplitude * 2;  // 2x average = threshold

    ESP_LOGI(TAG, "Noise floor: %d (max observed: %d)", noise_floor, max_amplitude);
}
```

### Dynamic Gain Control
```c
#define TARGET_LEVEL 20000  // Target RMS level
#define GAIN_FACTOR 1.5f

float calculate_gain(int16_t current_rms) {
    if (current_rms == 0) return 1.0f;

    float gain = (float)TARGET_LEVEL / current_rms;
    return (gain > GAIN_FACTOR) ? GAIN_FACTOR : gain;  // Limit max gain
}

void apply_gain(int16_t *samples, size_t count, float gain) {
    for (size_t i = 0; i < count; i++) {
        int32_t amplified = (int32_t)samples[i] * gain;

        // Clip to prevent overflow
        if (amplified > INT16_MAX) {
            samples[i] = INT16_MAX;
        } else if (amplified < INT16_MIN) {
            samples[i] = INT16_MIN;
        } else {
            samples[i] = (int16_t)amplified;
        }
    }
}
```

## Audio Level Monitoring

### RMS Calculation
```c
int16_t calculate_rms(const int16_t *samples, size_t count) {
    int64_t sum_squares = 0;

    for (size_t i = 0; i < count; i++) {
        int32_t sample = samples[i];
        sum_squares += sample * sample;
    }

    int32_t mean_square = sum_squares / count;
    return (int16_t)sqrt(mean_square);
}
```

### Peak Detection
```c
int16_t find_peak(const int16_t *samples, size_t count) {
    int16_t peak = 0;

    for (size_t i = 0; i < count; i++) {
        int16_t abs_sample = (samples[i] < 0) ? -samples[i] : samples[i];
        if (abs_sample > peak) peak = abs_sample;
    }

    return peak;
}
```

### dB Conversion
```c
float sample_to_db(int16_t sample) {
    if (sample == 0) return -96.0f;  // Min for 16-bit
    float normalized = (float)sample / 32768.0f;
    return 20.0f * log10(normalized);
}
```

## Anti-Patterns to Avoid

### ❌ WRONG: Blocking I2S read in main loop
```c
void bad_audio_capture(void) {
    int16_t sample;
    size_t bytes_read;
    i2s_read(I2S_NUM_0, &sample, 2, &bytes_read, portMAX_DELAY);
    // ← Blocks for 125µs per sample!
}
```

### ✅ CORRECT: DMA-based capture with task notification
```c
void good_audio_capture(void) {
    // i2s_read() with DMA handles buffering automatically
    // Process in separate task, no blocking on main thread
}
```

### ❌ WRONG: Allocating audio buffers on stack
```c
void bad_buffer_allocation(void) {
    int16_t audio_buf[4096];  // ← Stack overflow!
    i2s_read(I2S_NUM_0, audio_buf, 8192, ...);
}
```

### ✅ CORRECT: Static/global buffers
```c
static int16_t audio_buf[4096];  // Global memory
void good_buffer_allocation(void) {
    i2s_read(I2S_NUM_0, audio_buf, 8192, ...);
}
```

## Troubleshooting

### No Audio Captured
- Check I2S pins are correct (CLK on GPIO_NUM_14, DIN on GPIO_NUM_12)
- Verify SPH0645 power supply (3.3V stable)
- Check L/R pin (should be tied LOW for mono left channel)
- Test with oscilloscope: verify CLK frequency

### Only Silence Captured
- Verify microphone PCB assembly (check solder joints)
- SPH0645 might need power-up delay (add 100ms)
- Check I2S sample rate configuration

### Audio Distortion/Clipping
- Reduce gain or check for input overload
- Verify audio buffer size (larger buffer = lower dropout risk)
- Check DMA buffer count (2 buffers minimum)

### Noise Too High
- Run calibration in quiet environment
- Check for RF interference near microphone
- Verify power supply filtering

## Performance Notes

| Configuration | Latency | CPU Load |
|---|---|---|
| PDM raw (2.4MHz) | <1ms | ~5% |
| PDM→PCM decimation | ~1-5ms | ~8% |
| Full pipeline (capture+DSP) | ~10-20ms | ~15% |

## Key Parameters to Tune

```c
#define I2S_SAMPLE_RATE 16000          // PCM output rate
#define DMA_BUF_SIZE 512               // Increase for stability
#define DMA_BUF_COUNT 2                // Minimum 2 for double-buffering
#define NOISE_FLOOR_THRESHOLD 2.0f     // Multiplier above baseline
#define GAIN_TARGET 20000              // Target RMS level
#define MAX_GAIN 1.5f                  // Prevent over-amplification
```

## References

- SPH0645 Datasheet: Timing, pinout, electrical specifications
- ESP32-S3 I2S Driver: https://github.com/espressif/esp-idf/tree/master/components/driver/i2s
- PDM Filtering Theory: https://en.wikipedia.org/wiki/Pulse-density_modulation
