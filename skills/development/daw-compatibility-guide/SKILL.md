---
name: daw-compatibility-guide
description: DAW-specific quirks, known issues, and workarounds for Logic Pro, Ableton Live, Pro Tools, Cubase, Reaper, FL Studio, Bitwig with format-specific requirements (AU/VST3/AAX). Use when troubleshooting DAW compatibility, fixing host-specific bugs, implementing DAW workarounds, passing auval validation, or debugging automation issues.
allowed-tools: Read, Grep, Glob
---

# DAW Compatibility Guide

Comprehensive guide to DAW-specific quirks, known issues, and workarounds for ensuring your JUCE plugin works correctly across all major digital audio workstations.

## Overview

Each DAW has unique behaviors, assumptions, and quirks that can affect plugin operation. This guide documents common issues and proven solutions for Logic Pro, Ableton Live, Pro Tools, Cubase, Reaper, FL Studio, Bitwig, and others.

## When to Use This Guide

- Debugging DAW-specific issues reported by users
- Testing plugin compatibility across multiple DAWs
- Implementing DAW-specific workarounds
- Understanding format-specific requirements (AU, VST3, AAX)
- Planning cross-DAW automation and state compatibility

---

## Logic Pro (macOS - AU/VST3)

### Overview

- **Formats:** Audio Unit (preferred), VST3
- **Strictness:** Very strict AU validation (`auval`)
- **Automation:** Sample-accurate, works well
- **Unique Features:** AU-specific validation, side-chain routing

### AU Validation Requirements

**Issue:** Logic requires plugins to pass `auval` validation.

**Requirements:**
```cpp
// PluginProcessor.h - Ensure these are set correctly
#define JucePlugin_Name                 "MyPlugin"
#define JucePlugin_Desc                 "Description"
#define JucePlugin_Manufacturer         "YourCompany"
#define JucePlugin_ManufacturerCode     'Manu'  // 4 characters, unique!
#define JucePlugin_PluginCode           'Plug'  // 4 characters, unique!
#define JucePlugin_AUMainType           'aufx'  // Effect
// OR 'aumu' for MIDI effect
// OR 'aumf' for instrument
#define JucePlugin_AUSubType            JucePlugin_PluginCode
#define JucePlugin_AUExportPrefix       MyPluginAU
#define JucePlugin_AUExportPrefixQuoted "MyPluginAU"
```

**Validation Command:**
```bash
auval -v aufx Plug Manu
```

**Common auval Failures:**

1. **Failure: "FATAL ERROR: AudioUnitInitialize failed"**
   ```cpp
   // Cause: prepareToPlay() throws exception or asserts
   void prepareToPlay(double sampleRate, int samplesPerBlock) override {
       // ❌ Don't do this:
       jassert(sampleRate == 44100.0);  // Fails in auval!

       // ✅ Do this:
       if (sampleRate < 8000.0 || sampleRate > 192000.0)
           return;  // Handle gracefully
   }
   ```

2. **Failure: "FATAL ERROR: Property size is incorrect"**
   ```cpp
   // Cause: Incorrect I/O configuration
   bool isBusesLayoutSupported(const BusesLayout& layouts) const override {
       // Be permissive for auval
       if (layouts.getMainOutputChannelSet().isDisabled())
           return false;  // Must have output

       return true;  // Allow any channel config for auval
   }
   ```

3. **Failure: "FATAL ERROR: Render called with null buffer"**
   ```cpp
   void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) override {
       // auval sometimes passes zero-size buffers
       if (buffer.getNumSamples() == 0)
           return;  // Early exit for empty blocks
   }
   ```

**Run auval successfully:**
```bash
# Full validation (takes ~5 minutes)
auval -v aufx Plug Manu

# Strict validation (recommended)
auval -strict -v aufx Plug Manu

# If it passes, you'll see:
# * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# AU VALIDATION SUCCEEDED
# * * * * * * * * * * * * * * * * * * * * * * * * * * * *
```

### Logic-Specific Issues

**Issue: Automation writes incorrectly or doesn't play back**

**Cause:** Parameter smoothing interfering with Logic's automation.

**Solution:**
```cpp
// Don't smooth parameters that Logic is automating
void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) override {
    // ❌ Always smoothing
    float cutoff = smoother.getNextValue(*cutoffParam);

    // ✅ Only smooth if parameter changed recently
    if (cutoffParam->load() != lastCutoffValue) {
        smoother.setTargetValue(*cutoffParam);
        lastCutoffValue = *cutoffParam;
    }
    float cutoff = smoother.getNextValue();
}
```

**Issue: Offline bounce doesn't match realtime**

**Cause:** Tempo/time info assumptions.

**Solution:**
```cpp
void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) override {
    // ✅ Always query tempo from host
    auto playHead = getPlayHead();
    if (playHead != nullptr) {
        juce::AudioPlayHead::CurrentPositionInfo posInfo;
        playHead->getCurrentPosition(posInfo);

        float bpm = posInfo.bpm;
        double ppqPosition = posInfo.ppqPosition;
        bool isPlaying = posInfo.isPlaying;

        // Use this info, don't cache tempo!
    }
}
```

**Issue: Side-chain input doesn't work (AU)**

**Cause:** AU side-chain requires special bus configuration.

**Solution:**
```cpp
MyPluginProcessor::MyPluginProcessor()
    : AudioProcessor(BusesProperties()
        .withInput ("Input",  AudioChannelSet::stereo(), true)
        .withOutput("Output", AudioChannelSet::stereo(), true)
        .withInput ("Sidechain", AudioChannelSet::stereo(), false))  // Optional
{
}

void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) override {
    // Get sidechain bus
    auto mainInputOutput = getBusBuffer(buffer, true, 0);
    auto sidechain = getBusBuffer(buffer, true, 1);  // Second input bus

    if (!sidechain.getNumChannels())
        return;  // No sidechain connected

    // Process with sidechain...
}
```

---

## Ableton Live (VST3/AU)

### Overview

- **Formats:** VST3 (Windows/macOS), AU (macOS)
- **Automation:** Works well, supports breakpoint automation
- **Unique Features:** Max for Live integration, Device Racks, Macro mapping

### Live-Specific Issues

**Issue: Plugin doesn't appear in Live's browser**

**Cause:** VST3 not in correct folder or not scanned.

**Solution:**
```bash
# macOS VST3 path
~/Library/Audio/Plug-Ins/VST3/MyPlugin.vst3

# Windows VST3 path
C:\Program Files\Common Files\VST3\MyPlugin.vst3

# Rescan in Live:
# Preferences → Plug-Ins → "Rescan" button
```

**Issue: Undo/Redo causes parameter jumps**

**Cause:** Live's undo system conflicts with plugin parameter changes.

**Solution:**
```cpp
// Mark parameter changes as gestures to prevent undo conflicts
void parameterValueChanged(int parameterIndex, float newValue) override {
    // Notify host of parameter change
    auto* param = getParameters()[parameterIndex];
    param->beginChangeGesture();
    param->setValueNotifyingHost(newValue);
    param->endChangeGesture();
}
```

**Issue: Plugin latency not compensated correctly**

**Cause:** Plugin doesn't report latency.

**Solution:**
```cpp
int getLatencySamples() const override {
    return latencyInSamples;  // Report actual latency
}

void prepareToPlay(double sampleRate, int samplesPerBlock) override {
    // Update latency if it changes
    latencyInSamples = calculateLatency();
    setLatencySamples(latencyInSamples);
}
```

**Issue: Freeze/Flatten produces incorrect audio**

**Cause:** Non-deterministic behavior or offline/realtime mismatch.

**Solution:**
- Ensure processBlock is deterministic
- Reset all state in prepareToPlay()
- Don't use system time or random numbers without seeding

```cpp
void prepareToPlay(double sampleRate, int samplesPerBlock) override {
    // ✅ Reset all state for deterministic processing
    filter.reset();
    envelope.reset();
    rng.setSeed(12345);  // Seeded random for determinism
}
```

**Issue: Macro mapping doesn't work**

**Cause:** Parameter range or normalization issues.

**Solution:**
```cpp
// Ensure parameters use normalized 0-1 range internally
auto param = std::make_unique<AudioParameterFloat>(
    "cutoff",
    "Cutoff",
    NormalisableRange<float>(20.0f, 20000.0f, 0.01f, 0.3f),  // Skew
    1000.0f
);

// Live's macros expect normalized parameter access to work
```

---

## Pro Tools (AAX)

### Overview

- **Format:** AAX (PACE/iLok signed)
- **Strictness:** Very strict, requires code signing
- **Automation:** Sample-accurate, very robust
- **Unique Features:** AudioSuite (offline processing), HDX DSP

### AAX Requirements

**Issue: Plugin doesn't load - "damaged" or "unsigned" error**

**Cause:** AAX requires PACE signing with iLok account.

**Solution:**
1. Sign up for PACE iLok developer account
2. Get Developer ID certificate from PACE
3. Sign AAX bundle:
   ```bash
   wraptool sign --verbose \
       --account <your-ilok-account> \
       --password <password> \
       --wcguid <your-wcguid> \
       --dsig1-compat \
       --in MyPlugin.aaxplugin \
       --out MyPlugin.aaxplugin
   ```

**AAX Manifest:**
```cpp
// Required in CMakeLists.txt
juce_add_plugin(MyPlugin
    COMPANY_NAME "YourCompany"
    PLUGIN_MANUFACTURER_CODE Manu
    PLUGIN_CODE Plug
    FORMATS AAX
    AAX_IDENTIFIER com.yourcompany.myplugin
)
```

### Pro Tools-Specific Issues

**Issue: Plugin doesn't appear in correct category**

**Cause:** AAX category not set.

**Solution:**
```cpp
#define JucePlugin_AAXCategory AAX_ePlugInCategory_EQ  // For EQ
// Other categories:
// AAX_ePlugInCategory_Dynamics
// AAX_ePlugInCategory_PitchShift
// AAX_ePlugInCategory_Reverb
// AAX_ePlugInCategory_Delay
// AAX_ePlugInCategory_Modulation
// AAX_ePlugInCategory_Harmonic
// AAX_ePlugInCategory_SWGenerators
```

**Issue: AudioSuite (offline processing) produces different results**

**Cause:** AudioSuite processes entire selection at once.

**Solution:**
```cpp
void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) override {
    // AudioSuite may pass very large buffers (entire selection)
    // Must handle variable buffer sizes gracefully

    int numSamples = buffer.getNumSamples();
    // Process in chunks if needed for stability
    const int chunkSize = 512;

    for (int start = 0; start < numSamples; start += chunkSize) {
        int count = std::min(chunkSize, numSamples - start);
        AudioBuffer<float> chunk(buffer.getArrayOfWritePointers(),
                                  buffer.getNumChannels(),
                                  start, count);
        processChunk(chunk);
    }
}
```

**Issue: Session doesn't restore plugin state correctly**

**Cause:** State serialization issue specific to AAX.

**Solution:**
```cpp
void getStateInformation(MemoryBlock& destData) override {
    // AAX is very strict about state format
    // Use XML or ValueTree (both work reliably)
    auto state = apvts.copyState();
    std::unique_ptr<XmlElement> xml(state.createXml());

    // Ensure proper encoding
    copyXmlToBinary(*xml, destData);
}
```

**Issue: Delay compensation not working**

**Cause:** Pro Tools requires explicit latency reporting.

**Solution:**
```cpp
// Report latency during initialization
void prepareToPlay(double sampleRate, int samplesPerBlock) override {
    int latency = calculatePluginLatency();
    setLatencySamples(latency);
}

// Update if latency changes (rare)
void parameterChanged(const String& paramID, float newValue) override {
    if (paramID == "quality" && qualityAffectsLatency) {
        int newLatency = calculatePluginLatency();
        setLatencySamples(newLatency);
    }
}
```

---

## FL Studio (Windows - VST3)

### Overview

- **Format:** VST3 (VST2 deprecated)
- **Automation:** Works but has quirks
- **Unique Features:** Piano Roll, native wrapper

### FL Studio-Specific Issues

**Issue: Plugin state lost on crash**

**Cause:** FL Studio caches state, but doesn't always flush on crash.

**Solution:**
```cpp
// Save state more frequently
void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) override {
    static int counter = 0;
    if (++counter % 44100 == 0) {  // Every ~1 second @ 44.1kHz
        updateHostDisplay();  // Hint to FL to save state
    }
}
```

**Issue: Multiple instances interfere with each other**

**Cause:** Shared static data or singletons.

**Solution:**
```cpp
// ❌ Don't use static/global state
static float globalGain = 1.0f;  // BAD! Shared across instances

// ✅ Instance variables only
class MyPluginProcessor : public AudioProcessor {
    float instanceGain = 1.0f;  // Each instance has its own
};
```

**Issue: Wrapper shows generic UI instead of custom UI**

**Cause:** FL's wrapper can create generic UI if custom editor fails.

**Solution:**
```cpp
AudioProcessorEditor* createEditor() override {
    // Ensure editor constructor doesn't throw
    try {
        return new MyPluginEditor(*this);
    } catch (...) {
        jassertfalse;  // Debug: why did it fail?
        return nullptr;  // FL will show generic UI
    }
}
```

**Issue: Preset browser doesn't show presets**

**Cause:** FL looks for presets in specific format/location.

**Solution:**
```bash
# FL Studio preset path (Windows)
Documents\Image-Line\FL Studio\Presets\Plugin database\Generators\[Your Plugin]

# Save presets as .fst (FL's format)
# Or implement VST3 preset format (.vstpreset)
```

---

## Cubase/Nuendo (VST3)

### Overview

- **Format:** VST3 (Steinberg's own format)
- **Automation:** Excellent, sample-accurate
- **Unique Features:** Expression maps, VST3 spec reference implementation

### Cubase-Specific Issues

**Issue: Plugin doesn't load or shows "failed to load" error**

**Cause:** VST3 bundle structure incorrect.

**Solution:**
```bash
# Correct VST3 bundle structure:
MyPlugin.vst3/
  Contents/
    Resources/  # Optional: icons, documentation
    x86_64-win/
      MyPlugin.vst3  # Windows 64-bit
    x86-win/
      MyPlugin.vst3  # Windows 32-bit (optional)
    MacOS/
      MyPlugin  # macOS universal binary (arm64 + x86_64)

# Verify bundle with:
pluginval --strictness-level 10 MyPlugin.vst3
```

**Issue: Automation doesn't write or playback correctly**

**Cause:** Parameter flags not set correctly.

**Solution:**
```cpp
auto param = std::make_unique<AudioParameterFloat>(
    "cutoff",
    "Cutoff",
    NormalisableRange<float>(20.0f, 20000.0f),
    1000.0f
);

// Ensure automation is enabled
// (JUCE does this by default, but verify)
```

**Issue: Side-chain routing doesn't work**

**Cause:** VST3 side-chain requires specific bus configuration.

**Solution:**
```cpp
MyPluginProcessor()
    : AudioProcessor(BusesProperties()
        .withInput("Input", AudioChannelSet::stereo(), true)
        .withOutput("Output", AudioChannelSet::stereo(), true)
        .withInput("Sidechain", AudioChannelSet::stereo(), false))  // Aux input
{
}

bool isBusesLayoutSupported(const BusesLayout& layouts) const override {
    // Main input/output must match
    if (layouts.getMainInputChannelSet() != layouts.getMainOutputChannelSet())
        return false;

    // Sidechain is optional
    return true;
}
```

**Issue: Expression maps don't trigger MIDI correctly**

**Cause:** Plugin doesn't handle MIDI correctly.

**Solution:**
```cpp
void processBlock(AudioBuffer<float>& buffer, MidiBuffer& midi) override {
    // Ensure MIDI messages are processed at correct sample positions
    for (const auto metadata : midi) {
        auto message = metadata.getMessage();
        int samplePosition = metadata.samplePosition;

        // Process MIDI at exact sample position
        handleMidiMessage(message, samplePosition);
    }
}
```

---

## Reaper (VST3/AU)

### Overview

- **Formats:** VST3 (all platforms), AU (macOS)
- **Automation:** Highly flexible, supports both VST3 and AU
- **Unique Features:** Extremely permissive, good for testing

### Reaper-Specific Issues

**Issue: Plugin loads but doesn't process audio**

**Cause:** Reaper allows unusual configurations that other DAWs don't.

**Solution:**
```cpp
bool isBusesLayoutSupported(const BusesLayout& layouts) const override {
    // Reaper may try unusual layouts - be permissive
    auto mainIn = layouts.getMainInputChannelSet();
    auto mainOut = layouts.getMainOutputChannelSet();

    // Require at least mono or stereo
    if (mainIn == AudioChannelSet::disabled() ||
        mainOut == AudioChannelSet::disabled())
        return false;

    // Allow flexible channel counts
    return true;
}
```

**Issue: Offline render (Export) doesn't match realtime**

**Cause:** Reaper's offline render can use different buffer sizes.

**Solution:**
```cpp
void prepareToPlay(double sampleRate, int samplesPerBlock) override {
    // Don't assume fixed buffer size - handle variable sizes
    maxBufferSize = samplesPerBlock;

    // Allocate for worst case
    workBuffer.setSize(2, samplesPerBlock);
}

void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) override {
    // Handle any buffer size up to max
    jassert(buffer.getNumSamples() <= maxBufferSize);
}
```

**Issue: Plugin delay compensation incorrect**

**Cause:** Reaper is very strict about latency reporting.

**Solution:**
```cpp
void prepareToPlay(double sampleRate, int samplesPerBlock) override {
    // Calculate and report latency accurately
    int latency = fftSize / 2;  // Example: FFT-based effect
    setLatencySamples(latency);
}

// If latency changes dynamically
void setFFTSize(int newSize) {
    fftSize = newSize;
    setLatencySamples(fftSize / 2);
    // Reaper will adjust compensation
}
```

---

## Bitwig Studio (VST3)

### Overview

- **Format:** VST3
- **Automation:** Excellent, supports modulation
- **Unique Features:** Modulation system, Grid, Operator devices

### Bitwig-Specific Issues

**Issue: Bitwig's modulators don't affect plugin parameters**

**Cause:** Parameter update rate too slow.

**Solution:**
```cpp
// Bitwig can modulate at audio rate - ensure parameters respond
void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) override {
    auto cutoffParam = apvts.getRawParameterValue("cutoff");

    // Read parameter every sample if Bitwig is modulating
    for (int i = 0; i < buffer.getNumSamples(); ++i) {
        float cutoff = cutoffParam->load();  // Audio-rate read
        // Process sample with current value
    }
}

// Or use parameter smoothing:
smoother.reset(sampleRate, 0.005);  // 5ms smoothing
for (int i = 0; i < buffer.getNumSamples(); ++i) {
    float cutoff = smoother.getNextValue(cutoffParam->load());
}
```

**Issue: Plugin conflicts with Bitwig's Grid devices**

**Cause:** Unusual buffer configurations.

**Solution:**
```cpp
// Be very permissive with channel layouts for Bitwig
bool isBusesLayoutSupported(const BusesLayout& layouts) const override {
    // Bitwig may use unusual channel counts for CV/modulation
    return !layouts.getMainOutputChannelSet().isDisabled();
}
```

---

## Studio One (VST3)

### Overview

- **Format:** VST3
- **Automation:** Works well
- **Unique Features:** Scratch pads, arranger track

### Studio One-Specific Issues

**Issue: Plugin doesn't save/recall with song**

**Cause:** State information issue.

**Solution:**
```cpp
void getStateInformation(MemoryBlock& destData) override {
    // Studio One is strict about state consistency
    auto state = apvts.copyState();
    std::unique_ptr<XmlElement> xml(state.createXml());
    copyXmlToBinary(*xml, destData);
}

void setStateInformation(const void* data, int sizeInBytes) override {
    // Validate before loading
    std::unique_ptr<XmlElement> xml(getXmlFromBinary(data, sizeInBytes));
    if (!xml || !xml->hasTagName(apvts.state.getType()))
        return;  // Invalid state, don't crash

    apvts.replaceState(ValueTree::fromXml(*xml));
}
```

---

## Common Cross-DAW Issues

### Issue: Plugin crashes on load in specific DAW

**Debugging Steps:**
1. Check Console.app (macOS) or Event Viewer (Windows) for crash logs
2. Run plugin in debugger attached to DAW
3. Use Address Sanitizer to detect memory errors:
   ```bash
   cmake -B build -DCMAKE_CXX_FLAGS="-fsanitize=address"
   ```
4. Verify thread safety - most crashes are threading issues

**Common Causes:**
- Accessing UI from audio thread (or vice versa)
- Static initialization order issues
- Missing null checks
- Buffer overruns

**Solution Template:**
```cpp
void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) override {
    // ✅ Validate inputs
    if (buffer.getNumSamples() == 0)
        return;

    if (buffer.getNumChannels() == 0)
        return;

    // ✅ Null checks for all pointers
    if (auto* param = cutoffParam.load())
        float cutoff = param->load();

    // ✅ Bounds checking
    jassert(buffer.getNumSamples() <= maxBufferSize);
}
```

### Issue: Automation sounds different in different DAWs

**Cause:** Different automation smoothing or timing.

**Solution:**
```cpp
// Implement your own parameter smoothing
class ParameterSmoother {
public:
    void reset(double sampleRate, double timeSeconds = 0.05) {
        rampLength = static_cast<int>(sampleRate * timeSeconds);
        currentValue = targetValue = 0.0f;
        counter = 0;
    }

    void setTarget(float target) {
        targetValue = target;
        counter = rampLength;
    }

    float getNext() {
        if (counter > 0) {
            currentValue += (targetValue - currentValue) / counter;
            --counter;
        } else {
            currentValue = targetValue;
        }
        return currentValue;
    }

private:
    float currentValue = 0.0f, targetValue = 0.0f;
    int rampLength = 0, counter = 0;
};

// Use consistently across all DAWs
void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) override {
    smoother.setTarget(cutoffParam->load());

    for (int i = 0; i < buffer.getNumSamples(); ++i) {
        float smoothedCutoff = smoother.getNext();
        // Use smoothedCutoff for consistent automation across DAWs
    }
}
```

### Issue: State doesn't transfer between DAW sessions

**Cause:** Incompatible serialization formats.

**Solution:**
```cpp
// Use JUCE's ValueTree for reliable cross-DAW state
void getStateInformation(MemoryBlock& destData) override {
    ValueTree state("PluginState");
    state.setProperty("version", 1, nullptr);

    // Add parameter state
    state.appendChild(apvts.copyState(), nullptr);

    // Add custom state
    ValueTree customState("CustomState");
    customState.setProperty("uiWidth", uiWidth, nullptr);
    state.appendChild(customState, nullptr);

    // Serialize to XML (most compatible)
    std::unique_ptr<XmlElement> xml(state.createXml());
    copyXmlToBinary(*xml, destData);
}

void setStateInformation(const void* data, int sizeInBytes) override {
    std::unique_ptr<XmlElement> xml(getXmlFromBinary(data, sizeInBytes));
    if (!xml || !xml->hasTagName("PluginState"))
        return;

    ValueTree state = ValueTree::fromXml(*xml);

    // Check version for compatibility
    int version = state.getProperty("version", 0);
    if (version > 1)
        return;  // Future version, don't load

    // Restore state...
}
```

---

## Format-Specific Considerations

### AU (Audio Unit) - macOS Only

**Advantages:**
- Native to macOS
- Best integration with Logic Pro, GarageBand
- Sample-accurate automation

**Disadvantages:**
- Strict validation (`auval`)
- macOS-only
- Limited to Apple ecosystem

**Best Practices:**
```cpp
// Always pass auval before shipping
// Test on multiple macOS versions (10.13+)
// Verify on both Intel and Apple Silicon
```

### VST3 - Cross-Platform

**Advantages:**
- Cross-platform (macOS, Windows, Linux)
- Open specification
- Supported by most DAWs

**Disadvantages:**
- Some DAWs still prefer AU (macOS)
- Complex specification
- Side-chain setup can be tricky

**Best Practices:**
```cpp
// Validate with pluginval at strictness level 10
// Test side-chain routing thoroughly
// Ensure bundle structure is correct
```

### AAX - Pro Tools Only

**Advantages:**
- Pro Tools integration
- Professional studios standard

**Disadvantages:**
- Requires PACE/iLok signing ($$)
- Pro Tools-only
- Strict requirements

**Best Practices:**
```bash
# Always code-sign AAX bundles
# Test AudioSuite mode separately
# Verify delay compensation
```

---

## Testing Strategy for DAW Compatibility

### Minimum Test Matrix

| DAW | Format | Platform | Priority |
|-----|--------|----------|----------|
| Logic Pro | AU, VST3 | macOS | High |
| Ableton Live | VST3 | macOS, Windows | High |
| Pro Tools | AAX | macOS, Windows | High |
| Reaper | VST3 | macOS, Windows, Linux | Medium |
| FL Studio | VST3 | Windows | Medium |
| Cubase | VST3 | macOS, Windows | Medium |
| Bitwig | VST3 | macOS, Windows, Linux | Low |
| Studio One | VST3 | macOS, Windows | Low |

### Quick Compatibility Checklist

For each DAW:
- ✅ Plugin loads without errors
- ✅ Audio processes correctly
- ✅ Automation writes and plays back
- ✅ State saves and restores
- ✅ Offline render matches realtime
- ✅ No crashes after 5 minutes of use

---

## Emergency Fixes for Specific DAWs

### If plugin works everywhere except Logic:
```bash
# Run auval and fix reported issues
auval -strict -v aufx Plug Manu

# Common fix: handle zero-size buffers
if (buffer.getNumSamples() == 0) return;
```

### If plugin works everywhere except FL Studio:
```cpp
// Check for shared static state
// Ensure each instance is independent
```

### If plugin works everywhere except Pro Tools:
```cpp
// Verify AAX signing
# Check certificate:
codesign --display --verbose=4 MyPlugin.aaxplugin

// Ensure AudioSuite handles large buffers
```

---

## Summary

**Key Takeaways:**
- Test on at least 3 major DAWs before release
- Use automated validation tools (auval, pluginval)
- Implement consistent parameter smoothing
- Handle edge cases gracefully (zero-size buffers, unusual layouts)
- Use standard state serialization (ValueTree → XML)
- Report latency accurately for delay compensation
- Be permissive with bus layouts for compatibility

**DAW-Specific Priorities:**
1. **Logic Pro (macOS):** Pass `auval` validation
2. **Ableton Live:** Test Freeze/Flatten and undo/redo
3. **Pro Tools:** Sign with PACE, test AudioSuite
4. **Reaper:** Handle flexible configurations
5. **FL Studio:** Avoid shared state between instances

---

## Related Resources

- **/run-daw-tests** command - Automated DAW compatibility testing
- **TESTING_STRATEGY.md** - Comprehensive testing approach
- **RELEASE_CHECKLIST.md** - Pre-release DAW validation
- JUCE Forum - Search for DAW-specific issues

---

**Remember:** Every DAW is different, but following best practices (realtime safety, robust state management, proper latency reporting) will prevent 90% of compatibility issues. The remaining 10% require DAW-specific testing and workarounds documented here.
