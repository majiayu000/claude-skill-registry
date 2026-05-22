---
name: microcontroller-firmware
description: Embedded firmware development for microcontrollers including memory-mapped I/O, GPIO, interrupts, timers, UART/SPI/I2C serial protocols, PWM generation, ADC sampling, interrupt-driven versus polled architectures, RTOS fundamentals, and the bring-up sequence from power-on reset through first printf. Covers AVR/Arduino, ARM Cortex-M, and ESP32 patterns. Use when writing, porting, debugging, or reviewing firmware that directly manipulates hardware peripherals.
type: skill
category: electronics
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/electronics/microcontroller-firmware/SKILL.md
superseded_by: null
---
# Microcontroller Firmware

Firmware is the software layer that sits between hardware peripherals and the application logic. It is simultaneously the lowest-level code most engineers ever write and the most consequential: a firmware bug can brick a board, corrupt sensor data, or cause a motor to spin the wrong direction at full power. This skill covers what every firmware author needs to know before writing their first interrupt handler — the register model, the bring-up sequence, the standard peripheral set, and the decision points where architectural choices become hard to undo.

**Agent affinity:** shima (microprocessor architecture and instruction-level behavior), horowitz (practical bring-up and debugging)

**Concept IDs:** elec-microcontroller-interfacing, elec-sensor-actuator-systems

## The Microcontroller Model

A microcontroller is a single chip containing a CPU core, RAM, nonvolatile program memory (typically flash), and a collection of peripherals (GPIO, timers, UART, SPI, I2C, ADC, PWM, DMA, and others). The CPU, memory, and peripherals share a bus — usually via memory-mapped I/O, where reading and writing specific addresses communicates with specific peripheral registers.

**The three regions of memory:**

| Region | Typical size | Contents |
|---|---|---|
| Flash | 16 KB - 2 MB | Program code, constant data, interrupt vectors |
| SRAM | 1 KB - 512 KB | Variables, stack, heap if used |
| Peripheral | a few KB mapped | GPIO, UART, timer registers |

**Memory-mapped I/O.** Writing to address 0x40020014 might set the output latch of GPIO port A. Reading from 0x4001200C might return the status register of a UART. Peripheral addresses are defined in the vendor's device header file and never overlap RAM or flash.

## Technique 1 — The Bring-Up Sequence

On power-on reset, a microcontroller performs a fixed sequence before any user code runs:

1. **Hardware reset.** CPU registers initialize, program counter jumps to the reset vector (in flash at a vendor-specific address).
2. **Clock initialization.** The firmware typically switches the CPU from a slow internal oscillator to a faster internal or external oscillator, possibly through a PLL.
3. **Memory initialization.** The `.data` segment is copied from flash to RAM; the `.bss` segment is zeroed. These are usually the first lines of the reset handler, before `main()`.
4. **Peripheral clock enable.** Every peripheral has its clock gated at reset to save power; it must be explicitly enabled before its registers can be accessed.
5. **GPIO configuration.** Pins are configured as input, output, analog, or alternate function, with pull-ups/pull-downs as needed.
6. **Interrupt configuration.** Enable relevant interrupts in the peripheral and in the CPU's interrupt controller (NVIC on ARM Cortex-M).
7. **First printf or LED blink.** The first observable output, confirming the bring-up reached this point.

The single most useful first sign of life is a blinking LED. If you can toggle a GPIO in a loop, the reset handler is working, the clock tree is functional, flash is being read, and the GPIO peripheral is clocked. Everything else is incremental.

## Technique 2 — GPIO Basics

**Output.** Configure the pin as a push-pull or open-drain output. Push-pull drives both high and low. Open-drain only pulls low; an external pull-up (or another device) supplies the high level. Open-drain is required for wire-OR signaling and for I2C.

**Input.** Configure the pin as input. Enable the internal pull-up or pull-down if the external circuit does not guarantee a defined level when nothing is driving the line. Floating inputs are the single largest source of mystery bugs in embedded firmware.

**Reading an input.** Read the input data register. The value reflects the instantaneous pin state, not what the output latch last wrote.

**Bouncing.** Mechanical switches bounce for several milliseconds when pressed. Debounce in software by either sampling in a timer interrupt and requiring the value to be stable for several consecutive samples, or by using an RC filter and a Schmitt-trigger input.

## Technique 3 — Timers and PWM

A timer is a counter that increments (or decrements) on every cycle of its clock. When it reaches a configured limit, it rolls over and optionally fires an interrupt. Timers are the most versatile peripheral in a microcontroller.

**Common uses:**

- **Periodic tick.** Set the timer to roll over at a known frequency (e.g., 1 kHz) and fire an interrupt. This is the heartbeat for RTOS schedulers and for periodic sensor polling.
- **Pulse-width modulation (PWM).** Compare the counter against a configurable threshold. Output is high while counter < threshold, low otherwise. Varying the threshold varies the duty cycle. PWM drives motors, LEDs, and audio at low cost.
- **Input capture.** Record the counter value when an external event (edge on a GPIO) occurs. Used for measuring pulse widths, decoding quadrature encoders, and time-stamping events.
- **Output compare.** Trigger an action (toggle pin, fire interrupt, DMA request) when the counter matches a configured value.

**Worked example.** To generate a 50% duty cycle PWM at 1 kHz from a 16 MHz clock, configure the timer with a prescaler of 1, a period of 16000 (for 1 kHz = 16 MHz / 16000), and a compare threshold of 8000. The output pin is high for 8000 counts and low for 8000 counts, producing 50% at 1 kHz.

## Technique 4 — Serial Protocols: UART, SPI, I2C

### UART

Asynchronous, point-to-point, full-duplex. Two wires (TX, RX) plus a common ground. Each byte is framed by a start bit and one or more stop bits; there is no shared clock, so both ends must agree on the baud rate (9600, 115200, 921600, etc.). Simple, widely supported, the default for debug console output.

### SPI

Synchronous, multi-peripheral, full-duplex. Four wires (MOSI, MISO, SCK, CS) — chip select selects which peripheral responds. The master generates the clock, so no baud rate negotiation. Fast (10+ MHz common, 100 MHz possible). Used for flash memory, SD cards, displays, and high-rate sensors.

### I2C

Synchronous, multi-peripheral, half-duplex. Two wires (SDA, SCL) with external pull-ups; addressing selects the peripheral. Slower than SPI (typically 100-400 kHz, 1 MHz "fast-mode plus", 3.4 MHz "high-speed"). Used for low-rate sensors, EEPROMs, small displays. Supports clock stretching (peripheral holds SCL low to pause master).

**Choosing between them.**

| Need | Use |
|---|---|
| Human-readable console, simple two-party | UART |
| High speed, small number of peripherals | SPI |
| Many peripherals on a shared bus, low speed | I2C |

## Technique 5 — Interrupts vs Polling

**Polling.** The main loop repeatedly checks a status register to see if a peripheral needs service. Simple, deterministic, but wastes CPU cycles when nothing is happening and can miss events if the loop is doing something else.

**Interrupts.** The peripheral raises a signal when it needs service; the CPU jumps to the corresponding handler, executes it, and returns to what it was doing. Efficient, responsive, but harder to reason about because interrupt handlers run asynchronously and can race with the main code.

**Interrupt handler rules:**

1. **Keep handlers short.** Do the minimum necessary to acknowledge the event and queue work for the main loop.
2. **Declare shared variables volatile.** The compiler must re-read them every access because an interrupt might have changed them.
3. **Protect shared state with interrupt disables or atomic operations.** A read-modify-write of a shared variable can be interrupted halfway through.
4. **Never call blocking functions from within an interrupt handler.** No waiting on semaphores, no printf, no malloc.
5. **Clear the interrupt flag.** Or the handler will fire again immediately. Vendor headers often provide a specific sequence.

## Technique 6 — ADC Sampling

An ADC (analog-to-digital converter) samples an analog voltage and produces a digital code. Key parameters:

- **Resolution.** 8, 10, 12, 16 bits common. A 12-bit ADC produces codes 0-4095 for its full-scale range.
- **Sampling rate.** Samples per second. Must satisfy Nyquist for the signal of interest (rate > 2 * highest frequency).
- **Reference voltage.** Sets the full-scale range. A noisy reference ruins absolute accuracy.
- **Input impedance.** The source must be low enough impedance to charge the sample-and-hold capacitor within the sampling time, or the reading is wrong.

**Common patterns:**

- **Polled single sample.** Start conversion, wait for end-of-conversion flag, read result. Simple but blocks.
- **Interrupt-driven continuous.** Start continuous conversion; each end-of-conversion fires an interrupt that stores the sample and queues the next.
- **DMA-driven.** ADC transfers samples directly into a RAM buffer without CPU involvement. The CPU is notified only when a buffer is full. Essential for high-rate audio and sensor fusion.

## Technique 7 — RTOS vs Superloop

A superloop is a `while(1)` that services peripherals and application logic in sequence. Simple, predictable, and sufficient for most sensor-and-LED-level projects.

An RTOS (real-time operating system — FreeRTOS, Zephyr, ChibiOS, etc.) provides threads, queues, mutexes, and a scheduler. Worth the complexity when you have:

- Multiple independent tasks with different periods and priorities.
- Network stacks (TCP/IP, Bluetooth, Wi-Fi) that expect a threading environment.
- Complex event-driven logic that becomes a spaghetti state machine in a superloop.

**Don't reach for an RTOS on day one.** Start with a superloop; migrate to an RTOS only when the superloop genuinely becomes unmaintainable.

## Cross-References

- **digital-logic-design skill:** Explains the sequential logic implementing every peripheral inside the MCU.
- **shima agent:** Primary agent for microprocessor architecture and instruction-level questions.
- **horowitz agent:** Primary agent for practical bring-up and debugging guidance.
- **test-and-measurement skill:** Covers the oscilloscope and logic analyzer techniques needed to debug firmware against hardware.

## References

- Yiu, J. (2014). *The Definitive Guide to ARM Cortex-M3 and Cortex-M4 Processors*. 3rd ed. Newnes.
- White, E. (2011). *Making Embedded Systems*. O'Reilly.
- Barr, M. & Massa, A. (2006). *Programming Embedded Systems*. 2nd ed. O'Reilly.
- Buxton, J. (2019). *Mastering STM32*. Leanpub.
- Faggin, F., Hoff, M., Mazor, S., & Shima, M. (1996). "The history of the 4004." *IEEE Micro*, 16(6), 10-20.
