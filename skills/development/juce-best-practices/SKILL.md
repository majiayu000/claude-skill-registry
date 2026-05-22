---
name: juce-best-practices
description: Professional JUCE development guide covering realtime safety, threading, memory management, modern C++, and audio plugin best practices. Use when writing JUCE code, reviewing for realtime safety, implementing audio threads, managing parameters, or learning JUCE patterns and idioms.
allowed-tools: Read, Grep, Glob
---

# JUCE Best Practices

Comprehensive guide to professional JUCE framework development with modern C++ patterns, realtime safety, thread management, and audio plugin best practices.

## Table of Contents

1. [Realtime Safety](#realtime-safety)
2. [Thread Management](#thread-management)
3. [Memory Management](#memory-management)
4. [Modern C++ in JUCE](#modern-cpp-in-juce)
5. [JUCE Idioms and Conventions](#juce-idioms-and-conventions)
6. [Parameter Management](#parameter-management)
7. [State Management](#state-management)
8. [Performance Optimization](#performance-optimization)
9. [Common Pitfalls](#common-pitfalls)

---

## Realtime Safety

### The Golden Rule

**NEVER allocate, deallocate, lock, or block in the audio thread (processBlock).**

### What to Avoid in processBlock()

❌ **Memory Allocation**
```cpp
// BAD - allocates memory
void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) {
    std::vector<float> temp(buffer.getNumSamples()); // WRONG!
    auto dynamicArray = new float[buffer.getNumSamples()]; // WRONG!
}
```

✅ **Pre-allocate in prepare()**
```cpp
// GOOD - pre-allocate once
void prepareToPlay(double sampleRate, int maxBlockSize) {
    tempBuffer.setSize(2, maxBlockSize);
    workingMemory.resize(maxBlockSize);
}

void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) {
    // Use pre-allocated buffers
    tempBuffer.makeCopyOf(buffer);
}
```

❌ **Mutex Locks**
```cpp
// BAD - blocks audio thread
void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) {
    const ScopedLock lock(parameterLock); // WRONG!
    auto value = sharedParameter;
}
```

✅ **Use Atomics or Lock-Free Structures**
```cpp
// GOOD - lock-free communication
std::atomic<float> cutoffFrequency{1000.0f};

void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) {
    auto freq = cutoffFrequency.load(); // Lock-free!
    filter.setCutoff(freq);
}
```

❌ **System Calls and I/O**
```cpp
// BAD - system calls in audio thread
void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) {
    DBG("Processing " << buffer.getNumSamples()); // WRONG! (console I/O)
    saveAudioToFile(buffer); // WRONG! (file I/O)
}
```

### Realtime Safety Checklist

- [ ] No `new` or `delete`
- [ ] No `std::vector::push_back()` (may allocate)
- [ ] No mutex locks (`ScopedLock`, `std::lock_guard`)
- [ ] No file I/O
- [ ] No console output (`std::cout`, `DBG()`)
- [ ] No `malloc` or `free`
- [ ] No unbounded loops (always have max iterations)
- [ ] No exceptions (disable with `-fno-exceptions`)

---

## Thread Management

### The Two Worlds

JUCE audio plugins operate in **two separate thread contexts**:

1. **Message Thread** - UI, user interactions, file I/O, networking
2. **Audio Thread** - processBlock(), realtime audio processing

### Thread Communication

✅ **Message Thread → Audio Thread**
```cpp
// Use atomics for simple values
std::atomic<float> gain{1.0f};

// In UI (message thread)
void sliderValueChanged(Slider* slider) {
    gain.store(slider->getValue()); // Safe!
}

// In audio thread
void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) {
    auto currentGain = gain.load(); // Safe!
    buffer.applyGain(currentGain);
}
```

✅ **Audio Thread → Message Thread**
```cpp
// Use AsyncUpdater for async callbacks
class MyProcessor : public AudioProcessor,
                    private AsyncUpdater {
private:
    void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) override {
        // Process audio...
        if (needsUIUpdate) {
            triggerAsyncUpdate(); // Safe!
        }
    }

    void handleAsyncUpdate() override {
        // This runs on message thread - safe to update UI
        editor->updateDisplay();
    }
};
```

✅ **Complex Data with Lock-Free Queue**
```cpp
// For passing complex data (MIDI, analysis, etc.)
juce::AbstractFifo fifo;
std::vector<float> ringBuffer;

// Audio thread writes
void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) {
    int start1, size1, start2, size2;
    fifo.prepareToWrite(buffer.getNumSamples(), start1, size1, start2, size2);

    // Write to ring buffer...

    fifo.finishedWrite(size1 + size2);
}

// Message thread reads
void timerCallback() {
    int start1, size1, start2, size2;
    fifo.prepareToRead(fifo.getNumReady(), start1, size1, start2, size2);

    // Read from ring buffer...

    fifo.finishedRead(size1 + size2);
}
```

### Thread Safety Rules

| Action | Message Thread | Audio Thread |
|--------|----------------|--------------|
| Allocate memory | ✅ OK | ❌ Never |
| File I/O | ✅ OK | ❌ Never |
| Lock mutex | ✅ OK | ❌ Never |
| Update UI | ✅ OK | ❌ Never |
| Process audio | ❌ Never | ✅ OK |
| Use atomics | ✅ OK | ✅ OK |

---

## Memory Management

### RAII and Smart Pointers

✅ **Use RAII for Resource Management**
```cpp
// GOOD - automatic cleanup
class MyProcessor : public AudioProcessor {
private:
    std::unique_ptr<Reverb> reverb;
    std::vector<float> delayBuffer;

    void prepareToPlay(double sr, int maxBlockSize) override {
        reverb = std::make_unique<Reverb>(); // Auto-managed
        delayBuffer.resize(sr * 2.0); // Auto-managed
    }
    // No manual cleanup needed - automatic destruction
};
```

### Prefer Stack Allocation in processBlock()

✅ **Stack Allocation is Realtime-Safe**
```cpp
void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) {
    // OK - stack allocation
    float tempGain = 0.5f;
    int sampleCount = buffer.getNumSamples();

    // Process...
}
```

### Pre-allocate Buffers

✅ **Allocate Once, Reuse Many Times**
```cpp
class MyProcessor : public AudioProcessor {
private:
    AudioBuffer<float> tempBuffer;
    std::vector<float> fftData;

    void prepareToPlay(double sr, int maxBlockSize) override {
        // Allocate once
        tempBuffer.setSize(2, maxBlockSize);
        fftData.resize(2048);
    }

    void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) override {
        // Reuse pre-allocated buffers
        tempBuffer.makeCopyOf(buffer);
        // Process using tempBuffer...
    }
};
```

---

## Modern C++ in JUCE

### Use C++17/20 Features Appropriately

✅ **Structured Bindings (C++17)**
```cpp
auto [min, max] = buffer.findMinMax(0, buffer.getNumSamples());
```

✅ **if constexpr (C++17)**
```cpp
template<typename SampleType>
void process(AudioBuffer<SampleType>& buffer) {
    if constexpr (std::is_same_v<SampleType, float>) {
        // Float-specific optimizations
    } else {
        // Double-specific code
    }
}
```

✅ **std::optional (C++17)**
```cpp
std::optional<float> tryGetParameter(const String& id) {
    if (auto* param = parameters.getParameter(id))
        return param->getValue();
    return std::nullopt;
}
```

### Const Correctness

✅ **Mark Non-Mutating Methods const**
```cpp
class Filter {
public:
    float getCutoff() const { return cutoff; } // const!
    float getResonance() const { return resonance; }

    void setCutoff(float f) { cutoff = f; } // not const - mutates state

private:
    float cutoff = 1000.0f;
    float resonance = 0.707f;
};
```

### Range-Based For Loops

✅ **Cleaner Iteration**
```cpp
// OLD WAY
for (int ch = 0; ch < buffer.getNumChannels(); ++ch) {
    auto* channelData = buffer.getWritePointer(ch);
    for (int i = 0; i < buffer.getNumSamples(); ++i) {
        channelData[i] *= gain;
    }
}

// MODERN WAY
for (int ch = 0; ch < buffer.getNumChannels(); ++ch) {
    auto* data = buffer.getWritePointer(ch);
    for (int i = 0; i < buffer.getNumSamples(); ++i) {
        data[i] *= gain;
    }
}

// Or use JUCE's helpers
buffer.applyGain(gain);
```

---

## JUCE Idioms and Conventions

### Audio Buffer Operations

✅ **Use JUCE's Buffer Methods**
```cpp
// Apply gain
buffer.applyGain(0.5f);

// Clear buffer
buffer.clear();

// Copy buffer
AudioBuffer<float> copy;
copy.makeCopyOf(buffer);

// Add buffers
outputBuffer.addFrom(0, 0, inputBuffer, 0, 0, numSamples);
```

### Value Tree for State

✅ **Use ValueTree for Hierarchical State**
```cpp
ValueTree state("PluginState");
state.setProperty("version", "1.0.0", nullptr);

ValueTree parameters("Parameters");
parameters.setProperty("gain", 0.5f, nullptr);
parameters.setProperty("frequency", 1000.0f, nullptr);

state.appendChild(parameters, nullptr);

// Serialize
auto xml = state.toXmlString();

// Deserialize
auto loadedState = ValueTree::fromXml(xml);
```

### AudioProcessorValueTreeState for Parameters

✅ **Standard Parameter Management**
```cpp
class MyProcessor : public AudioProcessor {
public:
    MyProcessor()
        : parameters(*this, nullptr, "Parameters", createParameterLayout())
    {
    }

private:
    AudioProcessorValueTreeState parameters;

    static AudioProcessorValueTreeState::ParameterLayout createParameterLayout() {
        std::vector<std::unique_ptr<RangedAudioParameter>> params;

        params.push_back(std::make_unique<AudioParameterFloat>(
            "gain",
            "Gain",
            NormalisableRange<float>(0.0f, 1.0f),
            0.5f
        ));

        return { params.begin(), params.end() };
    }
};
```

---

## Parameter Management

### Parameter Smoothing

✅ **Smooth Parameter Changes to Avoid Zipper Noise**
```cpp
class MyProcessor : public AudioProcessor {
private:
    SmoothedValue<float> gainSmooth;

    void prepareToPlay(double sr, int maxBlockSize) override {
        gainSmooth.reset(sr, 0.05); // 50ms ramp time
    }

    void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) override {
        // Update target from parameter
        auto* gainParam = parameters.getRawParameterValue("gain");
        gainSmooth.setTargetValue(*gainParam);

        // Apply smoothed value
        for (int i = 0; i < buffer.getNumSamples(); ++i) {
            auto gain = gainSmooth.getNextValue();
            for (int ch = 0; ch < buffer.getNumChannels(); ++ch) {
                buffer.setSample(ch, i, buffer.getSample(ch, i) * gain);
            }
        }
    }
};
```

### Parameter Change Notifications

✅ **Efficient Parameter Updates**
```cpp
void parameterChanged(const String& parameterID, float newValue) override {
    if (parameterID == "cutoff") {
        cutoffFrequency.store(newValue);
    }
    // Don't do heavy processing here - mark for update instead
}
```

---

## State Management

### Save and Restore State

✅ **Implement getStateInformation/setStateInformation**
```cpp
void getStateInformation(MemoryBlock& destData) override {
    auto state = parameters.copyState();
    std::unique_ptr<XmlElement> xml(state.createXml());
    copyXmlToBinary(*xml, destData);
}

void setStateInformation(const void* data, int sizeInBytes) override {
    std::unique_ptr<XmlElement> xml(getXmlFromBinary(data, sizeInBytes));
    if (xml && xml->hasTagName(parameters.state.getType())) {
        parameters.replaceState(ValueTree::fromXml(*xml));
    }
}
```

### Version Your State

✅ **Handle Backward Compatibility**
```cpp
void setStateInformation(const void* data, int sizeInBytes) override {
    auto xml = getXmlFromBinary(data, sizeInBytes);

    int version = xml->getIntAttribute("version", 1);

    if (version == 1) {
        // Load v1 format and migrate
        migrateFromV1(xml);
    } else if (version == 2) {
        // Load v2 format
        parameters.replaceState(ValueTree::fromXml(*xml));
    }
}
```

---

## Performance Optimization

### Avoid Unnecessary Calculations

✅ **Calculate Once, Use Many Times**
```cpp
// BAD
for (int i = 0; i < buffer.getNumSamples(); ++i) {
    auto coeff = std::exp(-1.0f / (sampleRate * timeConstant)); // Recalculated every sample!
}

// GOOD
auto coeff = std::exp(-1.0f / (sampleRate * timeConstant)); // Calculate once
for (int i = 0; i < buffer.getNumSamples(); ++i) {
    // Use coeff
}
```

### Use SIMD When Appropriate

✅ **JUCE's dsp::SIMDRegister**
```cpp
void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) {
    auto* data = buffer.getWritePointer(0);
    auto gain = dsp::SIMDRegister<float>(0.5f);

    for (int i = 0; i < buffer.getNumSamples(); i += gain.size()) {
        auto samples = dsp::SIMDRegister<float>::fromRawArray(data + i);
        samples *= gain;
        samples.copyToRawArray(data + i);
    }
}
```

### Denormal Prevention

✅ **Prevent Denormals for CPU Performance**
```cpp
void prepareToPlay(double sr, int maxBlockSize) override {
    // Enable flush-to-zero
    juce::FloatVectorOperations::disableDenormalisedNumberSupport();
}

// Or add DC offset in feedback loops
float processSample(float input) {
    static constexpr float denormalPrevention = 1.0e-20f;
    feedbackState = input + feedbackState * 0.99f + denormalPrevention;
    return feedbackState;
}
```

---

## Common Pitfalls

### ❌ Pitfall 1: Calling `repaint()` from Audio Thread

```cpp
// WRONG
void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) {
    // Process...
    if (editor)
        editor->repaint(); // BAD! UI call from audio thread
}
```

✅ **Solution: Use AsyncUpdater**
```cpp
void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) {
    // Process...
    triggerAsyncUpdate(); // Schedules UI update for message thread
}

void handleAsyncUpdate() override {
    if (editor)
        editor->repaint(); // GOOD! On message thread
}
```

### ❌ Pitfall 2: Not Handling Sample Rate Changes

```cpp
// WRONG - assumes 44.1kHz
float delayTimeInSamples = 0.5f * 44100.0f;
```

✅ **Solution: Update in prepareToPlay**
```cpp
void prepareToPlay(double sampleRate, int maxBlockSize) override {
    delayTimeInSamples = 0.5f * sampleRate; // Correct for any sample rate
}
```

### ❌ Pitfall 3: Forgetting to Call Base Class Methods

```cpp
// WRONG
void prepareToPlay(double sr, int maxBlockSize) override {
    // Forgot to call base class!
    mySetup(sr, maxBlockSize);
}
```

✅ **Solution: Always Call Base**
```cpp
void prepareToPlay(double sr, int maxBlockSize) override {
    AudioProcessor::prepareToPlay(sr, maxBlockSize);
    mySetup(sr, maxBlockSize);
}
```

---

## Quick Reference

### Do's ✅

- Use `AudioProcessorValueTreeState` for parameters
- Pre-allocate buffers in `prepareToPlay()`
- Use atomics for simple thread communication
- Smooth parameter changes to avoid zipper noise
- Version your plugin state
- Handle all sample rates correctly
- Use RAII and smart pointers
- Mark const methods const
- Use JUCE's helper functions

### Don'ts ❌

- Allocate/deallocate in `processBlock()`
- Lock mutexes in audio thread
- Call UI methods from audio thread
- Use `DBG()` or logging in processBlock()
- Assume fixed sample rate or buffer size
- Forget to handle state save/load
- Use raw pointers for ownership
- Ignore const correctness
- Reinvent JUCE functionality

---

## Further Reading

- JUCE Documentation: https://docs.juce.com/
- JUCE Forum: https://forum.juce.com/
- JUCE Tutorials: https://juce.com/learn/tutorials
- Audio EQ Cookbook: /docs/dsp-resources/audio-eq-cookbook.html
- C++ Core Guidelines: https://isocpp.github.io/CppCoreGuidelines/

---

**Remember**: Audio plugins must be **realtime-safe**, **thread-aware**, and **robust**. Follow these best practices to create professional, stable plugins that work reliably across all DAWs and platforms.
