---
name: Guided Mode Expert
description: Work with Leavn guided meditation features - audio orchestration, phase management, caption sync, ambient audio, scripture meditation flows
allowed-tools: Read, Edit, Grep
---

# Guided Mode Expert

Expert in guided meditation system:

**Components**:
- GuidedModeViewModel - Phase management
- GuidedAudioOrchestrator - Audio coordination
- CaptionSyncEngine - Real-time captions
- Guided scripts - JSON-based content

**Phases**: idle → generating → synthesizing → ready → playing → completed

**Audio stack**: TTS + ambient + music + captions

Use when: Guided mode bugs, audio conflicts, phase transitions, caption sync
