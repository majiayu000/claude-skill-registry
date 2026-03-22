---
name: embedded-testing
description: Embedded systems testing patterns, hardware-in-the-loop
category: Testing-BDD
---

# Skill: embedded-testing

## What I do

I provide expertise in embedded systems and firmware testing: hardware abstraction (HAL), mocking peripherals (ArduinoFake), host-based unit testing (GTest/GMock), and Hardware-in-the-Loop (HIL) patterns.

## When to use me

- Testing firmware without physical hardware (native/host tests)
- Mocking hardware dependencies (GPIO, SPI, I2C, UART)
- Setting up HIL (Hardware-in-the-Loop) test suites
- Designing testable embedded architectures using HAL and DI
- Debugging timing-critical or peripheral integration issues

## Core principles

1. **Test on Host First** - Execute business logic on the development machine for fast feedback loops.
2. **HAL Abstraction** - Separate hardware access from logic using interfaces to enable mocking.
3. **Dependency Injection** - Inject hardware interfaces into devices to make them testable.
4. **Deterministic Timing** - Use controlled clocks/delays in tests to avoid hardware-induced flakiness.
5. **HIL for Critical Paths** - Reserve actual hardware tests for timing, peripherals, and integration.

## Patterns & examples

**Hardware Abstraction Layer (HAL):**
```cpp
// Logic depends on interface, not direct register access
class GPIOInterface {
public:
    virtual void digitalWrite(uint8_t pin, uint8_t value) = 0;
};

class LED {
    GPIOInterface* gpio;
public:
    LED(GPIOInterface* g) : gpio(g) {}
    void on() { gpio->digitalWrite(13, HIGH); }
};
```

**Mocking with Google Mock:**
```cpp
class MockGPIO : public GPIOInterface {
public:
    MOCK_METHOD(void, digitalWrite, (uint8_t pin, uint8_t value), (override));
};

TEST(LEDTest, TurnsOn) {
    MockGPIO mock;
    LED led(&mock);
    EXPECT_CALL(mock, digitalWrite(13, HIGH)).Times(1);
    led.on();
}
```

**Hardware-in-the-Loop (HIL):**
```cpp
// Test frequency accuracy on real silicon
TEST(PWMTest, FrequencyAccuracy) {
    PWMController pwm(PIN_PWM);
    pwm.setFrequency(1000);
    pwm.start();
    // Measure actual period with hardware timers...
    EXPECT_NEAR(measurePeriod(), 1000, 50); // 5% tolerance
}
```

## Anti-patterns to avoid

- ❌ **Direct Register Access in Logic** - Makes code untestable without hardware.
- ❌ **Testing via Serial/Printf** - Slow, brittle, and non-automated (use GTest).
- ❌ **Arbitrary Delays** - `delay(100)` makes tests slow and flaky; use event-based waiting.
- ❌ **Only Testing on Hardware** - Slow feedback cycle; test logic on host first.
- ❌ **Implementation Testing** - Testing private methods instead of visible behaviour.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Testing-BDD/Embedded Testing.md`

## Related skills

- `cpp` - Core C++ idioms and patterns
- `platformio` - Build and test runner for embedded
- `bdd-workflow` - Red-Green-Refactor cycle
- `clean-code` - SOLID for embedded systems
