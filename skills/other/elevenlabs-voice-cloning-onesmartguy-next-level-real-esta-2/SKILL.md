---
name: elevenlabs-voice-cloning
description: ElevenLabs voice cloning techniques, audio quality requirements, recording best practices, and training data optimization for professional-quality voice clones. Use when creating custom voices, cloning voices, or optimizing voice clone quality.
---

# ElevenLabs Voice Cloning

## Recording Requirements (CRITICAL)

### Audio Quality

**Environment:**
- Acoustically-treated room (no echo/reverb)
- No background noise, music, or interference
- Professional or high-quality USB microphone
- Quiet location (no HVAC, traffic, roommates)

**Microphone Technique:**
- Distance: 2 fists from microphone
- Consistent positioning throughout
- Pop filter recommended
- Proper gain staging (not too loud/quiet)

### Training Data Specifications

**Length Requirements:**
```
Instant Cloning:    60 seconds minimum
Professional:       30 minutes minimum
Optimal Quality:    3 hours ideal
```

**Content Diversity:**
```
Include:
├─ Varied emotions (happy, sad, neutral, excited)
├─ Different speaking styles (casual, professional, energetic)
├─ Questions and statements
├─ Different paces (fast, slow, normal)
└─ Emphasis variations
```

**Language Considerations:**
- Record in target output language
- Cross-language may have accent
- Example: English sample → Spanish output = English accent

### Audio Characteristics

**What AI Learns:**
- Emotional range in samples
- Prosody variations
- Speaking pace patterns
- Voice timbre and characteristics
- Inflection patterns

**Important:** AI can only replicate what it's trained on. Flat, monotonous samples = flat, monotonous voice.

## Cloning Workflow

```javascript
// 1. Prepare samples (3+ files recommended)
const samples = [
  'sample1_conversational.mp3',
  'sample2_professional.mp3',
  'sample3_emotional.mp3'
]

// 2. Clone voice
await mcp__elevenlabs__voice_clone({
  name: "Professional Narrator",
  files: samples,
  description: "Warm, authoritative voice for educational content"
})

// 3. Test and refine
// Generate test samples
// Evaluate quality
// Re-record if needed
```

## Quality Optimization

### Pre-Recording Checklist

- [ ] Silent room test (record 10s silence, check for noise)
- [ ] Microphone positioned correctly
- [ ] Pop filter in place
- [ ] Recording levels set (-12dB to -6dB peaks)
- [ ] Script prepared with varied content
- [ ] Warm up voice (read aloud 5 minutes)

### Post-Recording

- [ ] Listen to each sample
- [ ] Remove takes with mistakes
- [ ] Normalize volume if needed
- [ ] Export as high-quality MP3 or WAV
- [ ] Verify no clipping or distortion

## Common Issues & Solutions

**Issue: Clone sounds robotic**
- Add more expressive samples
- Include varied emotional range
- Record longer samples (3+ hours)

**Issue: Inconsistent voice**
- Ensure consistent microphone technique
- Record all samples in one session
- Same environment/equipment

**Issue: Background noise**
- Re-record in quieter location
- Use noise reduction (carefully)
- Better microphone/acoustic treatment

## Resources

- ElevenLabs Voice Cloning Guide
- Recording Techniques for Voice Actors
- Microphone Setup Best Practices
