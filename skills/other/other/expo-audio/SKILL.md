---
name: expo-audio
description: Guide for using expo-audio to implement audio playback and recording in React Native apps. Apply when working with audio features, sound playback, recording, or text-to-speech functionality.
allowed-tools: Read, Edit, Write, Grep, Glob
---

# Expo Audio (expo-audio)

Guide for using `expo-audio` to implement audio playback and recording in React
Native apps.

## Overview

- **Package**: `expo-audio` (replaces deprecated `expo-av`)
- **Platform**: Android, iOS, tvOS, Web
- **Bundled version**: ~1.1.1
- **Documentation**: https://docs.expo.dev/versions/latest/sdk/audio/

## Installation

```bash
npx expo install expo-audio
```

## Configuration

### app.json Plugin Configuration

Add the `expo-audio` plugin to your `app.json`:

```json
{
 "expo": {
  "plugins": [
   [
    "expo-audio",
    {
     "microphonePermission": "Allow $(PRODUCT_NAME) to access your microphone.",
     "recordAudioAndroid": true
    }
   ]
  ]
 }
}
```

**Configurable properties:**

- `microphonePermission` (iOS only): String for NSMicrophoneUsageDescription.
  Set to `false` to disable.
- `recordAudioAndroid` (Android only): Boolean to enable RECORD_AUDIO permission
  (default: `true`)

### Background Audio (iOS)

For background audio playback on iOS, add `UIBackgroundModes` to `app.json`:

```json
{
 "expo": {
  "ios": {
   "infoPlist": {
    "UIBackgroundModes": ["audio"]
   }
  }
 }
}
```

## Core Concepts

### AudioPlayer

The `AudioPlayer` class handles audio playback. You can create players using:

- `useAudioPlayer()` hook (recommended for React components)
- `createAudioPlayer()` function (for imperative usage outside components)

### AudioRecorder

The `AudioRecorder` class handles audio recording. Use:

- `useAudioRecorder()` hook (recommended for React components)

## Usage Patterns

### Playing Sounds (React Hook - Recommended)

Use `useAudioPlayer` hook in React components:

```tsx
import { Button, View } from "react-native";
import { useAudioPlayer } from "expo-audio";

const audioSource = require("./assets/sound.mp3");

export default function App() {
 const player = useAudioPlayer(audioSource);

 return (
  <View>
   <Button title="Play" onPress={() => player.play()} />
   <Button title="Pause" onPress={() => player.pause()} />
   <Button
    title="Replay"
    onPress={() => {
     player.seekTo(0);
     player.play();
    }}
   />
  </View>
 );
}
```

**Important**: Unlike `expo-av`, `expo-audio` doesn't automatically reset
playback position when audio finishes. After `play()`, the player stays paused
at the end. To replay, call `seekTo(seconds)` to reset position.

### Playing Sounds (Imperative - Outside Components)

For imperative usage (e.g., utility functions), use `createAudioPlayer`:

```tsx
import { AudioPlayer, createAudioPlayer, setAudioModeAsync } from "expo-audio";

let player: AudioPlayer | null = null;

export async function loadSound(uri: string): Promise<void> {
 // Configure audio mode
 await setAudioModeAsync({
  playsInSilentMode: true,
  allowsRecording: false,
 });

 // Create player
 player = createAudioPlayer({ uri });
}

export async function playSound(volume: number = 1.0): Promise<void> {
 if (!player) {
  await loadSound("https://example.com/sound.mp3");
 }

 if (player) {
  player.volume = volume;
  player.seekTo(0);
  player.play();
 }
}

export async function releaseSound(): Promise<void> {
 if (player) {
  player.release();
  player = null;
 }
}
```

**⚠️ Memory Management**: When using `createAudioPlayer`, you must manually call
`release()` when done to prevent memory leaks.

### Recording Sounds

```tsx
import { useEffect, useState } from "react";
import { Button, View } from "react-native";
import {
 AudioModule,
 RecordingPresets,
 setAudioModeAsync,
 useAudioRecorder,
 useAudioRecorderState,
} from "expo-audio";

export default function App() {
 const audioRecorder = useAudioRecorder(RecordingPresets.HIGH_QUALITY);
 const recorderState = useAudioRecorderState(audioRecorder);

 const record = async () => {
  await audioRecorder.prepareToRecordAsync();
  audioRecorder.record();
 };

 const stopRecording = async () => {
  // Recording available on `audioRecorder.uri`
  await audioRecorder.stop();
 };

 useEffect(() => {
  (async () => {
   const status = await AudioModule.requestRecordingPermissionsAsync();
   if (!status.granted) {
    Alert.alert("Permission to access microphone was denied");
   }

   await setAudioModeAsync({
    playsInSilentMode: true,
    allowsRecording: true,
   });
  })();
 }, []);

 return (
  <View>
   <Button
    title={recorderState.isRecording ? "Stop Recording" : "Start Recording"}
    onPress={recorderState.isRecording ? stopRecording : record}
   />
  </View>
 );
}
```

## AudioPlayer API

### Properties

- `volume`: Number (0.0 to 1.0) - Current playback volume
- `isPlaying`: Boolean - Whether audio is currently playing
- `isLoaded`: Boolean - Whether audio source is loaded
- `duration`: Number - Total duration in seconds (null if not loaded)
- `currentTime`: Number - Current playback position in seconds

### Methods

- `play()`: Start or resume playback
- `pause()`: Pause playback
- `seekTo(seconds: number)`: Seek to specific position
- `release()`: Release player resources (required for `createAudioPlayer`)

### Event Listeners

Use `useAudioPlayerStatus()` hook to react to player state changes:

```tsx
import { useAudioPlayer, useAudioPlayerStatus } from "expo-audio";

const player = useAudioPlayer(source);
const status = useAudioPlayerStatus(player);

// status.isPlaying, status.currentTime, status.duration, etc.
```

## AudioRecorder API

### Methods

- `prepareToRecordAsync(options?)`: Prepare recorder with options
- `record()`: Start recording
- `stop()`: Stop recording (returns URI)
- `pause()`: Pause recording
- `release()`: Release recorder resources

### Recording Presets

```tsx
import { RecordingPresets } from "expo-audio";

// Available presets:
RecordingPresets.HIGH_QUALITY;
RecordingPresets.LOW_QUALITY;
```

## Audio Mode Configuration

Use `setAudioModeAsync()` to configure audio behavior:

```tsx
import { setAudioModeAsync } from "expo-audio";

await setAudioModeAsync({
 playsInSilentMode: true, // Play even when device is in silent mode
 allowsRecording: false, // Allow recording (required for recording)
 interruptionMode: "duck", // 'duck' | 'mix' | 'doNotMix'
});
```

## Common Patterns

### Preload Audio on App Start

```tsx
// app/_layout.tsx
import { useEffect } from "react";
import { loadGongSound, unloadGongSound } from "../lib/audio";

export default function RootLayout() {
 useEffect(() => {
  loadGongSound();
  return () => {
   unloadGongSound();
  };
 }, []);

 return <Stack />;
}
```

### Play Sound with Volume Control

```tsx
import { createAudioPlayer, setAudioModeAsync } from "expo-audio";

let player: AudioPlayer | null = null;

export async function playSound(volume: number = 1.0): Promise<void> {
 if (!player) {
  await setAudioModeAsync({ playsInSilentMode: true });
  player = createAudioPlayer({ uri: "https://example.com/sound.mp3" });
 }

 if (player) {
  player.volume = volume;
  player.seekTo(0);
  player.play();
 }
}
```

### Replay Sound (Reset Position)

```tsx
// Important: expo-audio doesn't auto-reset position
player.seekTo(0); // Reset to beginning
player.play(); // Play from start
```

## Migration from expo-av

### Key Differences

1. **No auto-reset**: `expo-audio` doesn't reset position when playback
   finishes. Call `seekTo(0)` to replay.
2. **Hook-based API**: Prefer `useAudioPlayer()` over
   `Audio.Sound.createAsync()`
3. **Direct property access**: Use `player.volume = 0.5` instead of
   `player.setVolumeAsync(0.5)`
4. **Simplified API**: Fewer methods, more direct property access

### Migration Example

**Before (expo-av):**

```tsx
const { sound } = await Audio.Sound.createAsync({ uri });
await sound.setVolumeAsync(0.5);
await sound.setPositionAsync(0);
await sound.playAsync();
```

**After (expo-audio):**

```tsx
const player = createAudioPlayer({ uri });
player.volume = 0.5;
player.seekTo(0);
player.play();
```

## Web Considerations

- MediaRecorder on Chrome may produce WebM files missing duration metadata
  (known Chromium issue)
- Consider using polyfills like `kbumsik/opus-media-recorder` for better browser
  compatibility
- Web browsers require HTTPS for microphone access (MediaDevices getUserMedia
  security)

## Permissions

### Request Recording Permissions

```tsx
import { AudioModule } from "expo-audio";

const status = await AudioModule.requestRecordingPermissionsAsync();
if (!status.granted) {
 // Handle permission denied
}
```

### Check Permission Status

```tsx
const status = await AudioModule.getRecordingPermissionsAsync();
// status.granted, status.canAskAgain, etc.
```

## Best Practices

1. **Use hooks in components**: Prefer `useAudioPlayer()` in React components
   for automatic lifecycle management
2. **Release resources**: Always call `release()` when using
   `createAudioPlayer()` manually
3. **Reset position for replay**: Call `seekTo(0)` before replaying sounds
4. **Configure audio mode**: Set `playsInSilentMode: true` for
   meditation/notification sounds
5. **Handle errors**: Wrap audio operations in try-catch blocks
6. **Preload sounds**: Load sounds on app start for better UX

## References

- [Expo Audio Documentation](https://docs.expo.dev/versions/latest/sdk/audio/)
- [Expo Audio GitHub](https://github.com/expo/expo/tree/main/packages/expo-audio)
- [Migration from expo-av](https://docs.expo.dev/versions/latest/sdk/audio/#migration-from-expo-av)
