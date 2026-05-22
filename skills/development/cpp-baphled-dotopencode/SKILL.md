---
name: cpp
description: C++ for embedded systems, Arduino, ESP8266/ESP32, PlatformIO, and modern C++ idioms
category: Languages
---

# Skill: cpp

## What I do

I provide C++ expertise for embedded systems: modern C++ idioms, RAII patterns, Arduino/ESP8266/ESP32 development, PlatformIO workflows, and best practices for writing safe, efficient embedded code.

## When to use me

- Writing C++ for embedded systems or microcontrollers
- Working with Arduino, ESP8266, ESP32, or PlatformIO
- Understanding RAII, smart pointers, or memory safety
- Optimising C++ for embedded constraints
- Debugging hardware interactions

## Core principles

1. **RAII (Resource Acquisition Is Initialization)** - Constructor acquires, destructor releases
2. **Prefer smart pointers** - Use unique_ptr, shared_ptr; avoid raw new/delete
3. **Use modern C++** - C++11/14/17 idioms, not C-style code
4. **Embed efficiently** - Constrain memory use, minimise allocations
5. **Hardware safety first** - Understand timing, ISRs, hardware constraints

## Patterns & examples

**RAII pattern (fundamental for safety):**
```cpp
// ✅ Correct: RAII ensures cleanup
class SerialConnection {
private:
  int fd;
public:
  SerialConnection(const char* port) {
    fd = open(port);  // acquire
  }
  ~SerialConnection() {
    close(fd);  // release (always happens)
  }
  // disabled to prevent dangling
  SerialConnection(const SerialConnection&) = delete;
};

// ❌ Wrong: manual cleanup, easy to forget
void connect(const char* port) {
  int fd = open(port);
  // ... do stuff ...
  close(fd);  // might not run if exception thrown
}
```

**Smart pointers over raw pointers:**
```cpp
// ✅ Correct: unique_ptr for exclusive ownership
std::unique_ptr<Sensor> sensor(new TemperatureSensor(A0));
sensor->read();
// sensor auto-deleted when out of scope

// ❌ Wrong: raw pointer, manual deletion
Sensor* sensor = new TemperatureSensor(A0);
sensor->read();
delete sensor;  // easy to forget or double-delete
```

**Embedded memory constraint pattern:**
```cpp
// ✅ Correct: pre-allocate, avoid dynamic alloc
class DataBuffer {
  static const size_t BUFFER_SIZE = 256;
  uint8_t buffer[BUFFER_SIZE];  // stack allocation
};

// ❌ Wrong: dynamic allocation in loops drains heap
for (int i = 0; i < 100; i++) {
  std::vector<int> data(1000);  // allocate 100x times
}
```

**Arduino ISR safety:**
```cpp
// ✅ Correct: minimal ISR, flag for main loop
volatile bool new_data = false;

ISR(TIMER1_COMPA_vect) {
  new_data = true;  // just set flag
}

void loop() {
  if (new_data) {
    process_data();  // do heavy work here
    new_data = false;
  }
}

// ❌ Wrong: heavy work in ISR blocks everything
ISR(TIMER1_COMPA_vect) {
  for (int i = 0; i < 1000; i++) {
    // blocks other interrupts
  }
}
```

## Anti-patterns to avoid

- ❌ Raw `new`/`delete` (use smart pointers)
- ❌ String manipulation in ISRs (too slow, can deadlock)
- ❌ Unbounded heap allocation (embedded systems have limited RAM)
- ❌ Floating-point arithmetic on hardware without FPU (slow)
- ❌ Blocking calls in ISRs (prevents other interrupts)

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Languages/Cpp.md`

## Related skills

- `clean-code` - SOLID principles in C++
- `bdd-workflow` - Test-driven embedded development
- `embedded-testing` - Hardware-in-the-loop testing
- `performance` - Profiling embedded code
