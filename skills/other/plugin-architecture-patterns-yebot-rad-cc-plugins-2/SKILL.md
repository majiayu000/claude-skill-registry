---
name: plugin-architecture-patterns
description: Clean architecture patterns for JUCE plugins including separation of concerns, APVTS patterns, state management, preset systems, MIDI handling, and modulation routing. Use when designing plugin architecture, refactoring code structure, implementing parameter systems, building preset managers, or scaling complex audio plugins.
allowed-tools: Read, Grep, Glob
---

# Plugin Architecture Patterns

Master architectural patterns for building maintainable, testable, and scalable audio plugins using clean architecture, separation of concerns, and JUCE best practices.

## Overview

This skill provides comprehensive guidance on structuring JUCE audio plugins using proven architectural patterns. It covers separation of DSP from UI, state management, preset systems, parameter handling, MIDI routing, and modulation architectures.

## When to Use This Skill

- Designing a new plugin architecture from scratch
- Refactoring an existing plugin for better maintainability
- Implementing complex state management or modulation routing
- Planning multi-format plugin support (VST3/AU/AAX)
- Building plugins that need to scale (many parameters, voices, effects)

## Core Architectural Principles

### 1. Separation of Concerns

Audio plugins have distinct responsibilities that should be isolated:

```
┌─────────────────────────────────────────────────┐
│                  Plugin Host                    │
└─────────────────────┬───────────────────────────┘
                      │
          ┌───────────┴───────────┐
          │                       │
    ┌─────▼──────┐         ┌─────▼──────┐
    │ Processor  │         │   Editor   │
    │  (Audio)   │◄────────┤    (UI)    │
    └─────┬──────┘         └────────────┘
          │
    ┌─────▼──────┐
    │ DSP Engine │
    └─────┬──────┘
          │
    ┌─────▼──────┬──────────┬───────────┐
    │   Filter   │ Envelope │ Oscillator│
    └────────────┴──────────┴───────────┘
```

**Key Separations:**
- **DSP Logic** - Pure audio processing, realtime-safe
- **Parameter Management** - Value storage, automation, presets
- **UI Layer** - Rendering, user interaction (not realtime-safe)
- **State Management** - Serialization, preset loading/saving

---

## Architecture Pattern 1: Clean Architecture

### Layer Structure

```
┌──────────────────────────────────────────┐
│         Presentation Layer (UI)          │  ← JUCE Components, Graphics
├──────────────────────────────────────────┤
│      Application Layer (Processor)       │  ← AudioProcessor, parameter handling
├──────────────────────────────────────────┤
│         Domain Layer (DSP Core)          │  ← Pure audio algorithms
├──────────────────────────────────────────┤
│     Infrastructure (JUCE Framework)      │  ← JUCE modules, OS/DAW interface
└──────────────────────────────────────────┘
```

**Dependency Rule:** Outer layers depend on inner layers, never the reverse.

### Example: Clean Architecture in JUCE

```cpp
// ============================================================================
// Domain Layer - Pure DSP (no JUCE dependencies except juce::dsp)
// ============================================================================

// Source/DSP/FilterCore.h
class FilterCore {
public:
    void setFrequency(float hz, float sampleRate) {
        // Pure calculation, no allocations
        coefficients = calculateCoefficients(hz, sampleRate);
    }

    float processSample(float input) noexcept {
        // Realtime-safe processing
        return filter.processSample(input, coefficients);
    }

    void reset() noexcept {
        filter.reset();
    }

private:
    struct Coefficients { float b0, b1, b2, a1, a2; };
    Coefficients coefficients;
    BiquadFilter filter;

    static Coefficients calculateCoefficients(float hz, float sampleRate);
};

// ============================================================================
// Application Layer - Parameter Management
// ============================================================================

// Source/PluginProcessor.h
class MyPluginProcessor : public juce::AudioProcessor {
public:
    MyPluginProcessor()
        : parameters(*this, nullptr, "Parameters", createParameterLayout())
    {
        // Connect parameters to DSP
        cutoffParam = parameters.getRawParameterValue("cutoff");
    }

    void prepareToPlay(double sampleRate, int samplesPerBlock) override {
        filterCore.reset();
        currentSampleRate = sampleRate;
    }

    void processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer&) override {
        // Update DSP from parameters (thread-safe)
        float cutoff = cutoffParam->load();
        filterCore.setFrequency(cutoff, currentSampleRate);

        // Process audio
        for (int ch = 0; ch < buffer.getNumChannels(); ++ch) {
            auto* data = buffer.getWritePointer(ch);
            for (int i = 0; i < buffer.getNumSamples(); ++i) {
                data[i] = filterCore.processSample(data[i]);
            }
        }
    }

    void getStateInformation(juce::MemoryBlock& destData) override {
        auto state = parameters.copyState();
        std::unique_ptr<juce::XmlElement> xml(state.createXml());
        copyXmlToBinary(*xml, destData);
    }

    void setStateInformation(const void* data, int sizeInBytes) override {
        std::unique_ptr<juce::XmlElement> xml(getXmlFromBinary(data, sizeInBytes));
        if (xml && xml->hasTagName(parameters.state.getType()))
            parameters.replaceState(juce::ValueTree::fromXml(*xml));
    }

private:
    juce::AudioProcessorValueTreeState parameters;
    std::atomic<float>* cutoffParam;

    FilterCore filterCore;  // Domain layer object
    double currentSampleRate = 44100.0;

    static juce::AudioProcessorValueTreeState::ParameterLayout createParameterLayout();
};

// ============================================================================
// Presentation Layer - UI
// ============================================================================

// Source/PluginEditor.h
class MyPluginEditor : public juce::AudioProcessorEditor {
public:
    MyPluginEditor(MyPluginProcessor& p)
        : AudioProcessorEditor(&p), processor(p)
    {
        // Attach UI to parameters (APVTS handles thread-safety)
        cutoffAttachment = std::make_unique<SliderAttachment>(
            processor.getParameters(), "cutoff", cutoffSlider
        );

        addAndMakeVisible(cutoffSlider);
    }

private:
    using SliderAttachment = juce::AudioProcessorValueTreeState::SliderAttachment;

    MyPluginProcessor& processor;
    juce::Slider cutoffSlider;
    std::unique_ptr<SliderAttachment> cutoffAttachment;
};
```

**Benefits:**
- ✅ DSP is testable without JUCE (can unit test `FilterCore` standalone)
- ✅ UI changes don't affect DSP
- ✅ Easy to swap DSP implementations
- ✅ Clear separation of realtime-safe vs non-realtime code

---

## Architecture Pattern 2: Parameter-Centric Architecture

### Using AudioProcessorValueTreeState (APVTS)

JUCE's APVTS is the recommended way to manage parameters:

```cpp
// Parameters.h - Centralized parameter definitions
namespace Parameters {
    inline const juce::ParameterID cutoff { "cutoff", 1 };
    inline const juce::ParameterID resonance { "resonance", 1 };
    inline const juce::ParameterID gain { "gain", 1 };

    inline juce::AudioProcessorValueTreeState::ParameterLayout createLayout() {
        std::vector<std::unique_ptr<juce::RangedAudioParameter>> params;

        params.push_back(std::make_unique<juce::AudioParameterFloat>(
            cutoff,
            "Cutoff",
            juce::NormalisableRange<float>(20.0f, 20000.0f, 0.01f, 0.3f),  // Skew for log
            1000.0f
        ));

        params.push_back(std::make_unique<juce::AudioParameterFloat>(
            resonance,
            "Resonance",
            juce::NormalisableRange<float>(0.1f, 10.0f),
            1.0f
        ));

        params.push_back(std::make_unique<juce::AudioParameterFloat>(
            gain,
            "Gain",
            juce::NormalisableRange<float>(-24.0f, 24.0f),
            0.0f
        ));

        return { params.begin(), params.end() };
    }
}

// PluginProcessor.h
class MyPluginProcessor : public juce::AudioProcessor {
public:
    MyPluginProcessor()
        : apvts(*this, nullptr, "Parameters", Parameters::createLayout())
    {
        // Get raw parameter pointers for realtime access
        cutoffParam = apvts.getRawParameterValue(Parameters::cutoff.getParamID());
        resonanceParam = apvts.getRawParameterValue(Parameters::resonance.getParamID());
        gainParam = apvts.getRawParameterValue(Parameters::gain.getParamID());
    }

    void processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer&) override {
        // Thread-safe parameter access
        float cutoff = cutoffParam->load();
        float resonance = resonanceParam->load();
        float gain = juce::Decibels::decibelsToGain(gainParam->load());

        // Use parameters in DSP...
    }

    juce::AudioProcessorValueTreeState& getAPVTS() { return apvts; }

private:
    juce::AudioProcessorValueTreeState apvts;

    // Cached parameter pointers (thread-safe atomics)
    std::atomic<float>* cutoffParam;
    std::atomic<float>* resonanceParam;
    std::atomic<float>* gainParam;
};
```

**Benefits:**
- ✅ Automatic thread-safe parameter updates
- ✅ Built-in automation support
- ✅ Easy preset save/load
- ✅ UI attachment without boilerplate

---

## Architecture Pattern 3: State Management

### Plugin State Architecture

```
┌────────────────────────────────────────────────┐
│            Plugin State                        │
├────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐   │
│  │   Parameters     │  │   Non-Param      │   │
│  │   (APVTS)        │  │   State          │   │
│  ├──────────────────┤  ├──────────────────┤   │
│  │ • Cutoff         │  │ • UI Size        │   │
│  │ • Resonance      │  │ • Preset Name    │   │
│  │ • Gain           │  │ • Favorited      │   │
│  │ • (Automated)    │  │ • (Not Automated)│   │
│  └──────────────────┘  └──────────────────┘   │
└────────────────────────────────────────────────┘
```

### Managing Non-Parameter State

Some state shouldn't be parameters (not automated):

```cpp
// PluginProcessor.h
class MyPluginProcessor : public juce::AudioProcessor {
public:
    void getStateInformation(juce::MemoryBlock& destData) override {
        // Create root ValueTree
        juce::ValueTree state("PluginState");

        // Add parameter state
        state.appendChild(apvts.copyState(), nullptr);

        // Add non-parameter state
        juce::ValueTree nonParamState("NonParameterState");
        nonParamState.setProperty("uiWidth", uiWidth, nullptr);
        nonParamState.setProperty("uiHeight", uiHeight, nullptr);
        nonParamState.setProperty("presetName", presetName, nullptr);
        state.appendChild(nonParamState, nullptr);

        // Serialize to XML
        std::unique_ptr<juce::XmlElement> xml(state.createXml());
        copyXmlToBinary(*xml, destData);
    }

    void setStateInformation(const void* data, int sizeInBytes) override {
        std::unique_ptr<juce::XmlElement> xml(getXmlFromBinary(data, sizeInBytes));
        if (!xml || !xml->hasTagName("PluginState"))
            return;

        juce::ValueTree state = juce::ValueTree::fromXml(*xml);

        // Restore parameter state
        auto paramState = state.getChildWithName("Parameters");
        if (paramState.isValid())
            apvts.replaceState(paramState);

        // Restore non-parameter state
        auto nonParamState = state.getChildWithName("NonParameterState");
        if (nonParamState.isValid()) {
            uiWidth = nonParamState.getProperty("uiWidth", 800);
            uiHeight = nonParamState.getProperty("uiHeight", 600);
            presetName = nonParamState.getProperty("presetName", "").toString();
        }
    }

private:
    juce::AudioProcessorValueTreeState apvts;
    int uiWidth = 800, uiHeight = 600;
    juce::String presetName;
};
```

---

## Architecture Pattern 4: Preset System Design

### User Preset Management

```cpp
// PresetManager.h
class PresetManager {
public:
    PresetManager(juce::AudioProcessor& processor)
        : processor(processor)
    {
        // Default preset location
        presetDirectory = juce::File::getSpecialLocation(
            juce::File::userApplicationDataDirectory
        ).getChildFile("MyPlugin/Presets");

        presetDirectory.createDirectory();
        loadPresetList();
    }

    void savePreset(const juce::String& name) {
        juce::MemoryBlock stateData;
        processor.getStateInformation(stateData);

        juce::File presetFile = presetDirectory.getChildFile(name + ".preset");
        presetFile.replaceWithData(stateData.getData(), stateData.getSize());

        loadPresetList();  // Refresh
    }

    void loadPreset(const juce::String& name) {
        juce::File presetFile = presetDirectory.getChildFile(name + ".preset");
        if (!presetFile.existsAsFile())
            return;

        juce::MemoryBlock stateData;
        presetFile.loadFileAsData(stateData);

        processor.setStateInformation(stateData.getData(),
                                       static_cast<int>(stateData.getSize()));

        currentPresetName = name;
    }

    juce::StringArray getPresetList() const {
        return presetNames;
    }

    juce::String getCurrentPresetName() const {
        return currentPresetName;
    }

private:
    juce::AudioProcessor& processor;
    juce::File presetDirectory;
    juce::StringArray presetNames;
    juce::String currentPresetName;

    void loadPresetList() {
        presetNames.clear();
        auto presetFiles = presetDirectory.findChildFiles(
            juce::File::findFiles, false, "*.preset"
        );

        for (const auto& file : presetFiles)
            presetNames.add(file.getFileNameWithoutExtension());

        presetNames.sort(true);
    }
};

// Usage in Editor
class MyPluginEditor : public juce::AudioProcessorEditor {
    void comboBoxChanged(juce::ComboBox* box) override {
        if (box == &presetComboBox) {
            presetManager.loadPreset(box->getText());
        }
    }

    void saveButtonClicked() {
        juce::String name = juce::AlertWindow::showInputBox(
            "Save Preset", "Enter preset name:", ""
        );
        if (name.isNotEmpty())
            presetManager.savePreset(name);
    }
};
```

### Factory Presets

```cpp
// FactoryPresets.h
struct FactoryPreset {
    juce::String name;
    std::function<void(juce::AudioProcessorValueTreeState&)> configure;
};

namespace FactoryPresets {
    inline std::vector<FactoryPreset> getPresets() {
        return {
            {
                "Warm Filter",
                [](juce::AudioProcessorValueTreeState& apvts) {
                    apvts.getParameter("cutoff")->setValueNotifyingHost(0.3f);
                    apvts.getParameter("resonance")->setValueNotifyingHost(0.7f);
                }
            },
            {
                "Bright Filter",
                [](juce::AudioProcessorValueTreeState& apvts) {
                    apvts.getParameter("cutoff")->setValueNotifyingHost(0.8f);
                    apvts.getParameter("resonance")->setValueNotifyingHost(0.3f);
                }
            }
        };
    }
}

// Initialize on first launch
if (isFirstLaunch) {
    for (const auto& preset : FactoryPresets::getPresets()) {
        preset.configure(apvts);
        presetManager.savePreset(preset.name);
    }
}
```

---

## Architecture Pattern 5: MIDI Handling

### MIDI Message Processing

```cpp
// MidiProcessor.h
class MidiProcessor {
public:
    struct MidiNote {
        int noteNumber;
        int velocity;
        bool isNoteOn;
    };

    void processMidiBuffer(juce::MidiBuffer& midiMessages, int numSamples) {
        for (const auto metadata : midiMessages) {
            auto message = metadata.getMessage();
            int samplePosition = metadata.samplePosition;

            if (message.isNoteOn()) {
                handleNoteOn(message.getNoteNumber(),
                            message.getVelocity(),
                            samplePosition);
            } else if (message.isNoteOff()) {
                handleNoteOff(message.getNoteNumber(), samplePosition);
            } else if (message.isPitchWheel()) {
                handlePitchBend(message.getPitchWheelValue(), samplePosition);
            } else if (message.isController()) {
                handleCC(message.getControllerNumber(),
                        message.getControllerValue(),
                        samplePosition);
            }
        }
    }

private:
    void handleNoteOn(int noteNumber, int velocity, int samplePos) {
        // Trigger voice
        for (auto& voice : voices) {
            if (!voice.isActive()) {
                voice.startNote(noteNumber, velocity, samplePos);
                break;
            }
        }
    }

    void handleNoteOff(int noteNumber, int samplePos) {
        for (auto& voice : voices) {
            if (voice.isActive() && voice.getNoteNumber() == noteNumber) {
                voice.stopNote(samplePos);
            }
        }
    }

    void handlePitchBend(int value, int samplePos) {
        float bendSemitones = ((value - 8192) / 8192.0f) * 2.0f;  // ±2 semitones
        for (auto& voice : voices) {
            if (voice.isActive())
                voice.setPitchBend(bendSemitones);
        }
    }

    void handleCC(int ccNumber, int ccValue, int samplePos) {
        if (ccNumber == 1) {  // Mod wheel
            float modulation = ccValue / 127.0f;
            for (auto& voice : voices)
                if (voice.isActive())
                    voice.setModulation(modulation);
        }
    }

    std::array<SynthVoice, 16> voices;
};
```

### MPE (MIDI Polyphonic Expression) Support

```cpp
class MPEProcessor {
public:
    MPEProcessor() {
        mpeZoneLayout.setLowerZone(15);  // 15 voice channels
    }

    void processMidiBuffer(juce::MidiBuffer& midiMessages, int numSamples) {
        for (const auto metadata : midiMessages) {
            auto message = metadata.getMessage();

            if (mpeZoneLayout.isNoteOn(message)) {
                int noteNumber = message.getNoteNumber();
                int channel = message.getChannel();
                int velocity = message.getVelocity();

                auto& voice = voices[channel - 1];
                voice.startNote(noteNumber, velocity);
            }
            else if (mpeZoneLayout.isNoteOff(message)) {
                auto& voice = voices[message.getChannel() - 1];
                voice.stopNote();
            }
            else if (message.isPitchWheel()) {
                // Per-note pitch bend!
                auto& voice = voices[message.getChannel() - 1];
                voice.setPitchBend(message.getPitchWheelValue());
            }
            else if (message.isChannelPressure()) {
                // Per-note pressure
                auto& voice = voices[message.getChannel() - 1];
                voice.setPressure(message.getChannelPressureValue() / 127.0f);
            }
        }
    }

private:
    juce::MPEZoneLayout mpeZoneLayout;
    std::array<SynthVoice, 15> voices;  // 15 MPE voice channels
};
```

---

## Architecture Pattern 6: Modulation Routing

### Modulation Matrix Architecture

```cpp
// ModulationSystem.h
class ModulationSystem {
public:
    enum class Source {
        LFO1, LFO2, LFO3,
        Envelope1, Envelope2,
        VelocityMIDI,
        ModWheelMIDI,
        PitchBendMIDI
    };

    enum class Destination {
        FilterCutoff,
        FilterResonance,
        OscPitch,
        OscShape,
        Gain
    };

    struct ModulationRoute {
        Source source;
        Destination destination;
        float amount;  // -1.0 to +1.0
        bool enabled = true;
    };

    void addRoute(Source src, Destination dst, float amount) {
        routes.push_back({ src, dst, amount, true });
    }

    void removeRoute(size_t index) {
        if (index < routes.size())
            routes.erase(routes.begin() + index);
    }

    void process(int numSamples) {
        // Update modulation sources
        for (int i = 0; i < numSamples; ++i) {
            sourceValues[Source::LFO1] = lfo1.getNextSample();
            sourceValues[Source::Envelope1] = envelope1.getNextSample();
            // ... other sources

            // Apply modulation to destinations
            applyModulation();
        }
    }

    float getModulatedValue(Destination dst, float baseValue) {
        float total = 0.0f;
        for (const auto& route : routes) {
            if (route.enabled && route.destination == dst) {
                total += sourceValues[route.source] * route.amount;
            }
        }
        return baseValue + total;
    }

private:
    std::vector<ModulationRoute> routes;
    std::unordered_map<Source, float> sourceValues;

    LFO lfo1, lfo2, lfo3;
    Envelope envelope1, envelope2;

    void applyModulation() {
        // Calculate modulated values for all destinations
    }
};

// Usage in DSP
void processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midi) {
    modulationSystem.process(buffer.getNumSamples());

    float baseCutoff = cutoffParam->load();
    float modulatedCutoff = modulationSystem.getModulatedValue(
        ModulationSystem::Destination::FilterCutoff,
        baseCutoff
    );

    filter.setCutoff(modulatedCutoff);
}
```

### Advanced Modulation: Per-Voice Modulation

```cpp
class Voice {
public:
    void startNote(int noteNumber, int velocity) {
        this->noteNumber = noteNumber;
        this->velocity = velocity / 127.0f;

        envelope.noteOn();
        isActive_ = true;
    }

    float processSample(float input, ModulationSystem& globalMod) {
        // Per-voice envelope
        float envValue = envelope.getNextSample();

        // Combine global and per-voice modulation
        float cutoff = globalMod.getModulatedValue(
            ModulationSystem::Destination::FilterCutoff,
            baseCutoff
        );
        cutoff += envValue * envelopeToFilterAmount;  // Per-voice mod

        filter.setCutoff(cutoff);
        return filter.processSample(input);
    }

private:
    int noteNumber;
    float velocity;
    bool isActive_ = false;

    Envelope envelope;
    Filter filter;

    float baseCutoff = 1000.0f;
    float envelopeToFilterAmount = 500.0f;  // Env mod depth
};
```

---

## Architecture Pattern 7: Voice Management (Polyphonic Synths)

### Voice Allocation Strategy

```cpp
class VoiceManager {
public:
    explicit VoiceManager(int numVoices)
        : voices(numVoices)
    {
    }

    void noteOn(int noteNumber, int velocity) {
        // Try to find inactive voice
        Voice* voiceToUse = findInactiveVoice();

        // If all voices active, steal oldest
        if (!voiceToUse)
            voiceToUse = findVoiceToSteal();

        voiceToUse->startNote(noteNumber, velocity);
    }

    void noteOff(int noteNumber) {
        for (auto& voice : voices) {
            if (voice.isActive() && voice.getNoteNumber() == noteNumber) {
                voice.stopNote();
            }
        }
    }

    void renderNextBlock(juce::AudioBuffer<float>& buffer) {
        for (auto& voice : voices) {
            if (voice.isActive()) {
                voice.renderNextBlock(buffer);
            }
        }
    }

private:
    std::vector<Voice> voices;

    Voice* findInactiveVoice() {
        for (auto& voice : voices) {
            if (!voice.isActive())
                return &voice;
        }
        return nullptr;
    }

    Voice* findVoiceToSteal() {
        // Strategy: Steal oldest note
        Voice* oldest = &voices[0];
        double oldestTime = oldest->getStartTime();

        for (auto& voice : voices) {
            if (voice.getStartTime() < oldestTime) {
                oldest = &voice;
                oldestTime = voice.getStartTime();
            }
        }

        return oldest;
    }
};
```

---

## Architecture Pattern 8: Multi-Format Support

### Format-Specific Code Isolation

```cpp
// PluginProcessor.h
class MyPluginProcessor : public juce::AudioProcessor {
public:
    const juce::String getName() const override {
        #if JucePlugin_IsSynth
            return "MySynth";
        #else
            return "MyEffect";
        #endif
    }

    bool acceptsMidi() const override {
        #if JucePlugin_WantsMidiInput
            return true;
        #else
            return false;
        #endif
    }

    bool producesMidi() const override {
        #if JucePlugin_ProducesMidiOutput
            return true;
        #else
            return false;
        #endif
    }

    bool isMidiEffect() const override {
        #if JucePlugin_IsMidiEffect
            return true;
        #else
            return false;
        #endif
    }

    // Format-specific behavior
    void processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midi) override {
        #if JucePlugin_IsSynth
            // Synth: Generate audio from MIDI
            buffer.clear();
            processMidi(midi);
            synthesizer.renderNextBlock(buffer, midi, 0, buffer.getNumSamples());
        #else
            // Effect: Process input audio
            processAudio(buffer);
        #endif
    }
};
```

---

## Testing Architecture

### Unit Testing DSP Components

```cpp
// Tests/FilterTests.cpp
#include <catch2/catch_test_macros.hpp>
#include "../Source/DSP/FilterCore.h"

TEST_CASE("FilterCore processes audio correctly", "[dsp]") {
    FilterCore filter;

    SECTION("Impulse response") {
        filter.reset();
        filter.setFrequency(1000.0f, 44100.0f);

        float impulse[128] = { 1.0f };  // Impulse
        float output[128];

        for (int i = 0; i < 128; ++i)
            output[i] = filter.processSample(impulse[i]);

        // Verify filter ring-down
        REQUIRE(output[0] != 0.0f);
        REQUIRE(std::abs(output[127]) < 0.01f);  // Should decay
    }

    SECTION("DC blocking") {
        filter.reset();
        filter.setFrequency(1000.0f, 44100.0f);

        // Feed DC signal
        for (int i = 0; i < 1000; ++i) {
            float out = filter.processSample(1.0f);
            if (i > 100)  // After transient
                REQUIRE(std::abs(out) < 0.1f);  // Should block DC
        }
    }
}
```

---

## Performance Considerations

### Object Lifetime and Allocation

```cpp
class MyPluginProcessor : public juce::AudioProcessor {
public:
    void prepareToPlay(double sampleRate, int samplesPerBlock) override {
        // ✅ Allocate buffers here (not in processBlock!)
        workBuffer.setSize(2, samplesPerBlock);
        delayBuffer.setSize(2, static_cast<int>(sampleRate * 2.0));  // 2 sec

        // ✅ Initialize DSP
        filter.prepare({ sampleRate, (juce::uint32)samplesPerBlock, 2 });
        filter.reset();
    }

    void processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer&) override {
        // ✅ No allocations here!
        // ✅ Use pre-allocated buffers

        // Process using workBuffer
        workBuffer.makeCopyOf(buffer);
        filter.process(juce::dsp::AudioBlock<float>(workBuffer));
        buffer.makeCopyOf(workBuffer);
    }

private:
    juce::AudioBuffer<float> workBuffer;
    juce::AudioBuffer<float> delayBuffer;
    juce::dsp::ProcessorDuplicator<juce::dsp::IIR::Filter<float>,
                                     juce::dsp::IIR::Coefficients<float>> filter;
};
```

---

## Summary

**Key Architectural Principles:**
- ✅ Separate DSP, parameters, state, and UI into distinct layers
- ✅ Use APVTS for parameter management
- ✅ Never allocate or lock in audio thread
- ✅ Test DSP components in isolation
- ✅ Design for multiple plugin formats (VST3/AU/AAX)
- ✅ Implement modulation routing as a separate system
- ✅ Use clean architecture patterns for maintainability

**When Designing a New Plugin:**
1. Start with domain layer (pure DSP algorithms)
2. Add application layer (parameters, processor)
3. Build presentation layer (UI)
4. Implement state management and presets
5. Add modulation routing (if needed)
6. Test each layer independently

---

## Related Resources

- **juce-best-practices** skill - Realtime safety, threading, memory management
- **dsp-cookbook** skill - DSP algorithm implementations
- **TESTING_STRATEGY.md** - Testing approach for plugins
- JUCE Documentation: ValueTreeState, AudioProcessor, AudioProcessorEditor

---

**Remember:** Good architecture is invisible to the user but makes development, testing, and maintenance exponentially easier. Invest time in architecture upfront to save countless hours debugging threading issues, state corruption, and spaghetti code later!
