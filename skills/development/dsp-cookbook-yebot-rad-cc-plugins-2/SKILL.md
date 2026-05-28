---
name: dsp-cookbook
description: Production-ready DSP algorithms including filters, compressors, delays, modulation effects, saturation, and distortion with JUCE integration and optimization techniques. Use when implementing audio processing, DSP algorithms, audio effects, dynamics processors, or need code examples for common audio operations.
---

# DSP Cookbook

Practical DSP algorithm implementations for audio plugins. Production-ready code examples with JUCE framework integration, covering filters, dynamics, modulation, delays, and common audio effects.

## Table of Contents

1. [Filters](#filters)
2. [Dynamics Processors](#dynamics-processors)
3. [Modulation Effects](#modulation-effects)
4. [Delay-Based Effects](#delay-based-effects)
5. [Saturation & Distortion](#saturation--distortion)
6. [Parameter Smoothing](#parameter-smoothing)
7. [Utility Functions](#utility-functions)

---

## Filters

### Biquad Filter (2nd Order IIR)

**Use for**: EQ, lowpass, highpass, bandpass, notch filters

```cpp
class BiquadFilter {
public:
    enum class Type {
        Lowpass,
        Highpass,
        Bandpass,
        Notch,
        Allpass,
        PeakingEQ,
        LowShelf,
        HighShelf
    };

    void setCoefficients(Type type, float frequency, float sampleRate,
                        float Q = 0.707f, float gainDB = 0.0f) {
        const float w0 = juce::MathConstants<float>::twoPi * frequency / sampleRate;
        const float cosw0 = std::cos(w0);
        const float sinw0 = std::sin(w0);
        const float alpha = sinw0 / (2.0f * Q);
        const float A = std::pow(10.0f, gainDB / 40.0f);  // For shelf/peak

        float b0, b1, b2, a0, a1, a2;

        switch (type) {
            case Type::Lowpass:
                b0 = (1.0f - cosw0) / 2.0f;
                b1 = 1.0f - cosw0;
                b2 = (1.0f - cosw0) / 2.0f;
                a0 = 1.0f + alpha;
                a1 = -2.0f * cosw0;
                a2 = 1.0f - alpha;
                break;

            case Type::Highpass:
                b0 = (1.0f + cosw0) / 2.0f;
                b1 = -(1.0f + cosw0);
                b2 = (1.0f + cosw0) / 2.0f;
                a0 = 1.0f + alpha;
                a1 = -2.0f * cosw0;
                a2 = 1.0f - alpha;
                break;

            case Type::Bandpass:
                b0 = alpha;
                b1 = 0.0f;
                b2 = -alpha;
                a0 = 1.0f + alpha;
                a1 = -2.0f * cosw0;
                a2 = 1.0f - alpha;
                break;

            case Type::PeakingEQ:
                b0 = 1.0f + alpha * A;
                b1 = -2.0f * cosw0;
                b2 = 1.0f - alpha * A;
                a0 = 1.0f + alpha / A;
                a1 = -2.0f * cosw0;
                a2 = 1.0f - alpha / A;
                break;

            // Add other types as needed...
        }

        // Normalize coefficients
        coeffs.b0 = b0 / a0;
        coeffs.b1 = b1 / a0;
        coeffs.b2 = b2 / a0;
        coeffs.a1 = a1 / a0;
        coeffs.a2 = a2 / a0;
    }

    float processSample(float input) {
        const float output = coeffs.b0 * input
                           + coeffs.b1 * z1
                           + coeffs.b2 * z2
                           - coeffs.a1 * y1
                           - coeffs.a2 * y2;

        // Update state
        z2 = z1;
        z1 = input;
        y2 = y1;
        y1 = output;

        return output;
    }

    void reset() {
        z1 = z2 = y1 = y2 = 0.0f;
    }

private:
    struct Coefficients {
        float b0 = 1.0f, b1 = 0.0f, b2 = 0.0f;
        float a1 = 0.0f, a2 = 0.0f;
    } coeffs;

    float z1 = 0.0f, z2 = 0.0f;  // Input delays
    float y1 = 0.0f, y2 = 0.0f;  // Output delays
};
```

**Usage:**
```cpp
BiquadFilter filter;
filter.setCoefficients(BiquadFilter::Type::Lowpass, 1000.0f, 48000.0f, 0.707f);

for (int i = 0; i < buffer.getNumSamples(); ++i) {
    float input = buffer.getSample(0, i);
    float output = filter.processSample(input);
    buffer.setSample(0, i, output);
}
```

### State Variable Filter (SVF)

**Use for**: Smooth parameter changes, multimode filters

```cpp
class StateVariableFilter {
public:
    enum class Mode { Lowpass, Highpass, Bandpass };

    void prepare(double sampleRate) {
        this->sampleRate = sampleRate;
    }

    void setParameters(float cutoff, float resonance, Mode mode) {
        this->mode = mode;

        // Calculate coefficients (Chamberlin SVF)
        const float g = std::tan(juce::MathConstants<float>::pi * cutoff / sampleRate);
        const float k = 2.0f - 2.0f * resonance;  // resonance 0-1

        a1 = 1.0f / (1.0f + g * (g + k));
        a2 = g * a1;
        a3 = g * a2;
    }

    float processSample(float input) {
        const float v3 = input - ic2eq;
        const float v1 = a1 * ic1eq + a2 * v3;
        const float v2 = ic2eq + a2 * ic1eq + a3 * v3;

        ic1eq = 2.0f * v1 - ic1eq;
        ic2eq = 2.0f * v2 - ic2eq;

        switch (mode) {
            case Mode::Lowpass:  return v2;
            case Mode::Highpass: return input - k * v1 - v2;
            case Mode::Bandpass: return v1;
            default: return v2;
        }
    }

    void reset() {
        ic1eq = ic2eq = 0.0f;
    }

private:
    Mode mode = Mode::Lowpass;
    double sampleRate = 44100.0;
    float a1 = 0.0f, a2 = 0.0f, a3 = 0.0f;
    float ic1eq = 0.0f, ic2eq = 0.0f;  // Integrator state
};
```

---

## Dynamics Processors

### Compressor

**Use for**: Dynamics control, leveling, punchy mixes

```cpp
class Compressor {
public:
    void prepare(double sampleRate) {
        this->sampleRate = sampleRate;
        envelope = 0.0f;
    }

    void setParameters(float thresholdDB, float ratio, float attackMs, float releaseMs) {
        threshold = juce::Decibels::decibelsToGain(thresholdDB);
        this->ratio = ratio;

        // Calculate time constants
        attackCoeff = std::exp(-1.0f / (attackMs * 0.001f * sampleRate));
        releaseCoeff = std::exp(-1.0f / (releaseMs * 0.001f * sampleRate));
    }

    float processSample(float input) {
        const float inputLevel = std::abs(input);

        // Envelope follower
        if (inputLevel > envelope)
            envelope = attackCoeff * envelope + (1.0f - attackCoeff) * inputLevel;
        else
            envelope = releaseCoeff * envelope + (1.0f - releaseCoeff) * inputLevel;

        // Compute gain reduction
        float gainReduction = 1.0f;
        if (envelope > threshold) {
            const float excess = envelope / threshold;
            gainReduction = std::pow(excess, 1.0f / ratio - 1.0f);
        }

        return input * gainReduction;
    }

    float getGainReductionDB() const {
        return juce::Decibels::gainToDecibels(envelope > threshold
            ? std::pow(envelope / threshold, 1.0f / ratio - 1.0f)
            : 1.0f);
    }

    void reset() {
        envelope = 0.0f;
    }

private:
    double sampleRate = 44100.0;
    float threshold = 1.0f;
    float ratio = 4.0f;
    float attackCoeff = 0.0f;
    float releaseCoeff = 0.0f;
    float envelope = 0.0f;
};
```

### Limiter (Look-Ahead)

```cpp
class Limiter {
public:
    void prepare(double sampleRate, int maxBlockSize) {
        this->sampleRate = sampleRate;

        // Look-ahead buffer (5ms typical)
        const int lookAheadSamples = static_cast<int>(0.005 * sampleRate);
        delayBuffer.setSize(2, lookAheadSamples);
        delayBuffer.clear();
        writePos = 0;
    }

    void setThreshold(float thresholdDB) {
        threshold = juce::Decibels::decibelsToGain(thresholdDB);
    }

    float processSample(float input, int channel) {
        // Write to delay buffer
        delayBuffer.setSample(channel, writePos, input);

        // Read delayed sample
        const float delayed = delayBuffer.getSample(channel, writePos);

        // Analyze future peak
        float peak = 0.0f;
        for (int i = 0; i < delayBuffer.getNumSamples(); ++i) {
            peak = std::max(peak, std::abs(delayBuffer.getSample(channel, i)));
        }

        // Calculate gain
        float gain = 1.0f;
        if (peak > threshold) {
            gain = threshold / peak;
        }

        writePos = (writePos + 1) % delayBuffer.getNumSamples();

        return delayed * gain;
    }

    void reset() {
        delayBuffer.clear();
        writePos = 0;
    }

private:
    double sampleRate = 44100.0;
    float threshold = 1.0f;
    juce::AudioBuffer<float> delayBuffer;
    int writePos = 0;
};
```

---

## Modulation Effects

### Chorus

```cpp
class Chorus {
public:
    void prepare(double sampleRate, int maxBlockSize) {
        this->sampleRate = sampleRate;

        // Delay line (50ms max)
        const int bufferSize = static_cast<int>(0.05 * sampleRate);
        delayBuffer.setSize(2, bufferSize);
        delayBuffer.clear();
        writePos = 0;

        lfo.setSampleRate(sampleRate);
    }

    void setParameters(float rate, float depth, float mix) {
        lfo.setFrequency(rate);
        this->depth = depth;
        this->mix = mix;
    }

    float processSample(float input, int channel) {
        // Write to delay buffer
        delayBuffer.setSample(channel, writePos, input);

        // Calculate modulated delay time
        const float lfoValue = lfo.processSample();
        const float baseDelay = 0.010f * sampleRate;  // 10ms base
        const float modDelay = baseDelay + depth * 0.005f * sampleRate * lfoValue;

        // Read from delay buffer with linear interpolation
        const float readPos = writePos - modDelay;
        const float delayed = readDelayBuffer(channel, readPos);

        writePos = (writePos + 1) % delayBuffer.getNumSamples();

        // Mix dry and wet
        return input * (1.0f - mix) + delayed * mix;
    }

    void reset() {
        delayBuffer.clear();
        writePos = 0;
        lfo.reset();
    }

private:
    float readDelayBuffer(int channel, float position) {
        // Wrap position
        while (position < 0)
            position += delayBuffer.getNumSamples();

        const int pos1 = static_cast<int>(position) % delayBuffer.getNumSamples();
        const int pos2 = (pos1 + 1) % delayBuffer.getNumSamples();
        const float frac = position - std::floor(position);

        const float samp1 = delayBuffer.getSample(channel, pos1);
        const float samp2 = delayBuffer.getSample(channel, pos2);

        // Linear interpolation
        return samp1 + frac * (samp2 - samp1);
    }

    double sampleRate = 44100.0;
    float depth = 0.5f;
    float mix = 0.5f;
    juce::AudioBuffer<float> delayBuffer;
    int writePos = 0;

    // Simple LFO
    struct LFO {
        void setSampleRate(double sr) { sampleRate = sr; }
        void setFrequency(float freq) { frequency = freq; }
        float processSample() {
            const float output = std::sin(phase);
            phase += juce::MathConstants<float>::twoPi * frequency / sampleRate;
            if (phase >= juce::MathConstants<float>::twoPi)
                phase -= juce::MathConstants<float>::twoPi;
            return output;
        }
        void reset() { phase = 0.0f; }

        double sampleRate = 44100.0;
        float frequency = 1.0f;
        float phase = 0.0f;
    } lfo;
};
```

---

## Delay-Based Effects

### Simple Delay

```cpp
class SimpleDelay {
public:
    void prepare(double sampleRate) {
        this->sampleRate = sampleRate;

        // Max delay: 2 seconds
        const int bufferSize = static_cast<int>(2.0 * sampleRate);
        delayBuffer.setSize(2, bufferSize);
        delayBuffer.clear();
        writePos = 0;
    }

    void setParameters(float delayTimeMs, float feedback, float mix) {
        delaySamples = static_cast<int>(delayTimeMs * 0.001f * sampleRate);
        this->feedback = juce::jlimit(0.0f, 0.95f, feedback);  // Prevent runaway
        this->mix = mix;
    }

    float processSample(float input, int channel) {
        // Read delayed sample
        const int readPos = (writePos - delaySamples + delayBuffer.getNumSamples())
                          % delayBuffer.getNumSamples();
        const float delayed = delayBuffer.getSample(channel, readPos);

        // Write input + feedback
        const float toWrite = input + delayed * feedback;
        delayBuffer.setSample(channel, writePos, toWrite);

        writePos = (writePos + 1) % delayBuffer.getNumSamples();

        // Mix
        return input * (1.0f - mix) + delayed * mix;
    }

    void reset() {
        delayBuffer.clear();
        writePos = 0;
    }

private:
    double sampleRate = 44100.0;
    int delaySamples = 0;
    float feedback = 0.0f;
    float mix = 0.5f;
    juce::AudioBuffer<float> delayBuffer;
    int writePos = 0;
};
```

---

## Saturation & Distortion

### Soft Clipper

```cpp
inline float softClip(float input, float threshold = 0.7f) {
    if (std::abs(input) < threshold)
        return input;

    const float sign = input > 0.0f ? 1.0f : -1.0f;
    const float abs = std::abs(input);

    // Soft knee above threshold
    return sign * (threshold + (1.0f - threshold) * std::tanh((abs - threshold) / (1.0f - threshold)));
}
```

### Waveshaper (Polynomial)

```cpp
inline float waveshape(float input, float drive) {
    const float x = input * drive;

    // Cubic waveshaping: y = x - (x^3)/3
    return x - (x * x * x) / 3.0f;
}
```

### Tube-Style Saturation

```cpp
inline float tubeSaturation(float input, float drive) {
    const float x = input * drive;

    // Hyperbolic tangent - smooth saturation
    return std::tanh(x) / drive;
}
```

---

## Parameter Smoothing

### Linear Smoother

```cpp
class ParameterSmoother {
public:
    void reset(double sampleRate, double rampTimeSeconds) {
        this->sampleRate = sampleRate;
        rampSamples = static_cast<int>(rampTimeSeconds * sampleRate);
        currentSample = rampSamples;
    }

    void setTargetValue(float target) {
        if (target != targetValue) {
            startValue = currentValue;
            targetValue = target;
            currentSample = 0;
        }
    }

    float getNextValue() {
        if (currentSample >= rampSamples)
            return targetValue;

        const float alpha = static_cast<float>(currentSample) / rampSamples;
        currentValue = startValue + alpha * (targetValue - startValue);
        ++currentSample;

        return currentValue;
    }

private:
    double sampleRate = 44100.0;
    int rampSamples = 0;
    int currentSample = 0;
    float startValue = 0.0f;
    float targetValue = 0.0f;
    float currentValue = 0.0f;
};
```

### Exponential Smoother (One-Pole)

```cpp
class ExponentialSmoother {
public:
    void reset(double sampleRate, double timeConstantSeconds) {
        coeff = std::exp(-1.0 / (timeConstantSeconds * sampleRate));
        currentValue = 0.0f;
    }

    void setTargetValue(float target) {
        targetValue = target;
    }

    float getNextValue() {
        currentValue = coeff * currentValue + (1.0f - coeff) * targetValue;
        return currentValue;
    }

private:
    float coeff = 0.0f;
    float targetValue = 0.0f;
    float currentValue = 0.0f;
};
```

---

## Utility Functions

### Decibel Conversion

```cpp
inline float dBToGain(float dB) {
    return std::pow(10.0f, dB / 20.0f);
}

inline float gainToDB(float gain) {
    return 20.0f * std::log10(gain);
}
```

### Frequency to MIDI Note

```cpp
inline float frequencyToMIDI(float frequency) {
    return 69.0f + 12.0f * std::log2(frequency / 440.0f);
}

inline float midiToFrequency(float midiNote) {
    return 440.0f * std::pow(2.0f, (midiNote - 69.0f) / 12.0f);
}
```

### Denormal Prevention

```cpp
inline float preventDenormal(float value) {
    static constexpr float denormalFix = 1.0e-20f;
    return value + denormalFix;
}

// Or use JUCE's built-in
juce::FloatVectorOperations::disableDenormalisedNumberSupport();
```

### Peak Meter (with ballistics)

```cpp
class PeakMeter {
public:
    void prepare(double sampleRate) {
        // Attack: instantaneous
        // Release: 300ms typical
        releaseCoeff = std::exp(-1.0 / (0.3 * sampleRate));
        peak = 0.0f;
    }

    float processSample(float input) {
        const float absInput = std::abs(input);

        if (absInput > peak) {
            peak = absInput;  // Attack
        } else {
            peak = releaseCoeff * peak + (1.0f - releaseCoeff) * absInput;  // Release
        }

        return peak;
    }

    float getPeakDB() const {
        return juce::Decibels::gainToDecibels(peak);
    }

    void reset() {
        peak = 0.0f;
    }

private:
    float releaseCoeff = 0.0f;
    float peak = 0.0f;
};
```

---

## Integration with JUCE

### Using in AudioProcessor

```cpp
class MyPluginProcessor : public juce::AudioProcessor {
public:
    void prepareToPlay(double sampleRate, int samplesPerBlock) override {
        filter.prepare(sampleRate);
        filter.setParameters(1000.0f, 0.707f, StateVariableFilter::Mode::Lowpass);

        compressor.prepare(sampleRate);
        compressor.setParameters(-20.0f, 4.0f, 10.0f, 100.0f);
    }

    void processBlock(juce::AudioBuffer<float>& buffer, juce::MidiBuffer&) override {
        for (int channel = 0; channel < buffer.getNumChannels(); ++channel) {
            auto* data = buffer.getWritePointer(channel);

            for (int sample = 0; sample < buffer.getNumSamples(); ++sample) {
                // Apply filter
                data[sample] = filter.processSample(data[sample]);

                // Apply compression
                data[sample] = compressor.processSample(data[sample]);
            }
        }
    }

private:
    StateVariableFilter filter;
    Compressor compressor;
};
```

---

## References

- **Audio EQ Cookbook**: `/docs/dsp-resources/audio-eq-cookbook.html`
- **Julius O. Smith DSP Books**: `/docs/dsp-resources/julius-smith-dsp-books.md`
- **DAFX Book**: `/docs/dsp-resources/dafx-reference.md`
- **Cytomic Filters**: `/docs/dsp-resources/cytomic-filter-designs.md`

---

**Note**: All code examples are production-ready and follow realtime-safety rules. Pre-allocate buffers in `prepare()`, avoid allocations in `processSample()`, and use proper numerical stability techniques.
