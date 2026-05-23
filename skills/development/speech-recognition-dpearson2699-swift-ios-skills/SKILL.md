---
name: speech-recognition
description: "Transcribe speech to text using the Speech framework. Use when implementing live microphone transcription with AVAudioEngine, recognizing pre-recorded audio files, configuring on-device vs server-based recognition, handling authorization flows, or adopting the new SpeechAnalyzer API (iOS 26+) for modern async/await speech-to-text."
---

# Speech Recognition

Transcribe live and pre-recorded audio to text using Apple's Speech framework.
Covers `SFSpeechRecognizer` (iOS 10+) and the new `SpeechAnalyzer` API (iOS 26+).

## Contents

- [SpeechAnalyzer (iOS 26+)](#speechanalyzer-ios-26)
- [SFSpeechRecognizer Setup](#sfspeechrecognizer-setup)
- [Authorization](#authorization)
- [Live Microphone Transcription](#live-microphone-transcription)
- [Pre-Recorded Audio File Recognition](#pre-recorded-audio-file-recognition)
- [On-Device vs Server Recognition](#on-device-vs-server-recognition)
- [Handling Results](#handling-results)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## SpeechAnalyzer (iOS 26+)

`SpeechAnalyzer` is an actor-based API introduced in iOS 26 that replaces
`SFSpeechRecognizer` for new projects. It uses Swift concurrency, `AsyncSequence`
for results, and supports modular analysis via `SpeechTranscriber`.

### Basic transcription with SpeechAnalyzer

```swift
import Speech

// 1. Create a transcriber module
guard let locale = SpeechTranscriber.supportedLocale(
    equivalentTo: Locale.current
) else { return }
let transcriber = SpeechTranscriber(locale: locale, preset: .offlineTranscription)

// 2. Ensure assets are installed
if let request = try await AssetInventory.assetInstallationRequest(
    supporting: [transcriber]
) {
    try await request.downloadAndInstall()
}

// 3. Create input stream and analyzer
let (inputSequence, inputBuilder) = AsyncStream.makeStream(of: AnalyzerInput.self)
let audioFormat = await SpeechAnalyzer.bestAvailableAudioFormat(
    compatibleWith: [transcriber]
)
let analyzer = SpeechAnalyzer(modules: [transcriber])

// 4. Feed audio buffers (from AVAudioEngine or file)
Task {
    // Append PCM buffers converted to audioFormat
    let pcmBuffer: AVAudioPCMBuffer = // ... your audio buffer
    inputBuilder.yield(AnalyzerInput(buffer: pcmBuffer))
    inputBuilder.finish()
}

// 5. Consume results
Task {
    for try await result in transcriber.results {
        let text = String(result.text.characters)
        print(text)
    }
}

// 6. Run analysis
let lastSampleTime = try await analyzer.analyzeSequence(inputSequence)

// 7. Finalize
if let lastSampleTime {
    try await analyzer.finalizeAndFinish(through: lastSampleTime)
} else {
    try analyzer.cancelAndFinishNow()
}
```

### Transcribing an audio file with SpeechAnalyzer

```swift
let transcriber = SpeechTranscriber(locale: locale, preset: .offlineTranscription)
let audioFile = try AVAudioFile(forReading: fileURL)
let analyzer = SpeechAnalyzer(
    inputAudioFile: audioFile, modules: [transcriber], finishAfterFile: true
)
for try await result in transcriber.results {
    print(String(result.text.characters))
}
```

### Key differences from SFSpeechRecognizer

| Feature | SFSpeechRecognizer | SpeechAnalyzer |
|---|---|---|
| Concurrency | Callbacks/delegates | async/await + AsyncSequence |
| Type | `class` | `actor` |
| Modules | Monolithic | Composable (`SpeechTranscriber`, `SpeechDetector`) |
| Audio input | `append(_:)` on request | `AsyncStream<AnalyzerInput>` |
| Availability | iOS 10+ | iOS 26+ |
| On-device | `requiresOnDeviceRecognition` | Asset-based via `AssetInventory` |

## SFSpeechRecognizer Setup

### Creating a recognizer with locale

```swift
import Speech

// Default locale (user's current language)
let recognizer = SFSpeechRecognizer()

// Specific locale
let recognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US"))

// Check if recognition is available for this locale
guard let recognizer, recognizer.isAvailable else {
    print("Speech recognition not available")
    return
}
```

### Monitoring availability changes

```swift
final class SpeechManager: NSObject, SFSpeechRecognizerDelegate {
    private let recognizer = SFSpeechRecognizer()!

    override init() {
        super.init()
        recognizer.delegate = self
    }

    func speechRecognizer(
        _ speechRecognizer: SFSpeechRecognizer,
        availabilityDidChange available: Bool
    ) {
        // Update UI — disable record button when unavailable
    }
}
```

## Authorization

Request **both** speech recognition and microphone permissions before starting
live transcription. Add these keys to `Info.plist`:

- `NSSpeechRecognitionUsageDescription`
- `NSMicrophoneUsageDescription`

```swift
import Speech
import AVFoundation

func requestPermissions() async -> Bool {
    let speechStatus = await withCheckedContinuation { continuation in
        SFSpeechRecognizer.requestAuthorization { status in
            continuation.resume(returning: status)
        }
    }
    guard speechStatus == .authorized else { return false }

    let micStatus: Bool
    if #available(iOS 17, *) {
        micStatus = await AVAudioApplication.requestRecordPermission()
    } else {
        micStatus = await withCheckedContinuation { continuation in
            AVAudioSession.sharedInstance().requestRecordPermission { granted in
                continuation.resume(returning: granted)
            }
        }
    }
    return micStatus
}
```

## Live Microphone Transcription

The standard pattern: `AVAudioEngine` captures microphone audio → buffers are
appended to `SFSpeechAudioBufferRecognitionRequest` → results stream in.

```swift
import Speech
import AVFoundation

final class LiveTranscriber {
    private let recognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US"))!
    private let audioEngine = AVAudioEngine()
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    private var recognitionTask: SFSpeechRecognitionTask?

    func startTranscribing() throws {
        // Cancel any in-progress task
        recognitionTask?.cancel()
        recognitionTask = nil

        // Configure audio session
        let audioSession = AVAudioSession.sharedInstance()
        try audioSession.setCategory(.record, mode: .measurement, options: .duckOthers)
        try audioSession.setActive(true, options: .notifyOthersOnDeactivation)

        // Create request
        let request = SFSpeechAudioBufferRecognitionRequest()
        request.shouldReportPartialResults = true
        self.recognitionRequest = request

        // Start recognition task
        recognitionTask = recognizer.recognitionTask(with: request) { result, error in
            if let result {
                let text = result.bestTranscription.formattedString
                print("Transcription: \(text)")

                if result.isFinal {
                    self.stopTranscribing()
                }
            }
            if let error {
                print("Recognition error: \(error)")
                self.stopTranscribing()
            }
        }

        // Install audio tap
        let inputNode = audioEngine.inputNode
        let recordingFormat = inputNode.outputFormat(forBus: 0)
        inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) {
            buffer, _ in
            request.append(buffer)
        }

        audioEngine.prepare()
        try audioEngine.start()
    }

    func stopTranscribing() {
        audioEngine.stop()
        audioEngine.inputNode.removeTap(onBus: 0)
        recognitionRequest?.endAudio()
        recognitionRequest = nil
        recognitionTask?.cancel()
        recognitionTask = nil
    }
}
```

## Pre-Recorded Audio File Recognition

Use `SFSpeechURLRecognitionRequest` for audio files on disk:

```swift
func transcribeFile(at url: URL) async throws -> String {
    guard let recognizer = SFSpeechRecognizer(), recognizer.isAvailable else {
        throw SpeechError.unavailable
    }
    let request = SFSpeechURLRecognitionRequest(url: url)
    request.shouldReportPartialResults = false

    return try await withCheckedThrowingContinuation { continuation in
        recognizer.recognitionTask(with: request) { result, error in
            if let error {
                continuation.resume(throwing: error)
            } else if let result, result.isFinal {
                continuation.resume(
                    returning: result.bestTranscription.formattedString
                )
            }
        }
    }
}
```

## On-Device vs Server Recognition

On-device recognition (iOS 13+) works offline but supports fewer locales:

```swift
let recognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US"))!

// Check if on-device is supported for this locale
if recognizer.supportsOnDeviceRecognition {
    let request = SFSpeechAudioBufferRecognitionRequest()
    request.requiresOnDeviceRecognition = true  // Force on-device
}
```

> **Tip:** On-device recognition avoids network latency and the one-minute
> audio limit imposed by server-based recognition. However, accuracy may be
> lower and not all locales are supported. Check `supportsOnDeviceRecognition`
> before forcing on-device mode.

## Handling Results

### Partial vs final results

```swift
let request = SFSpeechAudioBufferRecognitionRequest()
request.shouldReportPartialResults = true  // default is true

recognizer.recognitionTask(with: request) { result, error in
    guard let result else { return }

    if result.isFinal {
        // Final transcription — recognition is complete
        let final = result.bestTranscription.formattedString
    } else {
        // Partial result — may change as more audio is processed
        let partial = result.bestTranscription.formattedString
    }
}
```

### Accessing alternative transcriptions and confidence

```swift
recognizer.recognitionTask(with: request) { result, error in
    guard let result else { return }

    // Best transcription
    let best = result.bestTranscription

    // All alternatives (sorted by confidence, descending)
    for transcription in result.transcriptions {
        for segment in transcription.segments {
            print("\(segment.substring): \(segment.confidence)")
        }
    }
}
```

### Adding punctuation (iOS 16+)

```swift
let request = SFSpeechAudioBufferRecognitionRequest()
request.addsPunctuation = true
```

### Contextual strings

Improve recognition of domain-specific terms:

```swift
let request = SFSpeechAudioBufferRecognitionRequest()
request.contextualStrings = ["SwiftUI", "Xcode", "CloudKit"]
```

## Common Mistakes

### Not requesting both speech and microphone authorization

```swift
// ❌ DON'T: Only request speech authorization for live audio
SFSpeechRecognizer.requestAuthorization { status in
    // Missing microphone permission — audio engine will fail
    self.startRecording()
}

// ✅ DO: Request both permissions before recording
SFSpeechRecognizer.requestAuthorization { status in
    guard status == .authorized else { return }
    AVAudioSession.sharedInstance().requestRecordPermission { granted in
        guard granted else { return }
        self.startRecording()
    }
}
```

### Not handling availability changes

```swift
// ❌ DON'T: Assume recognizer stays available after initial check
let recognizer = SFSpeechRecognizer()!
// Recognition may fail if network drops or locale changes

// ✅ DO: Monitor availability via delegate
recognizer.delegate = self
func speechRecognizer(
    _ speechRecognizer: SFSpeechRecognizer,
    availabilityDidChange available: Bool
) {
    recordButton.isEnabled = available
}
```

### Not stopping the audio engine when recognition ends

```swift
// ❌ DON'T: Leave audio engine running after recognition finishes
recognizer.recognitionTask(with: request) { result, error in
    if result?.isFinal == true {
        // Audio engine still running, wasting resources and battery
    }
}

// ✅ DO: Clean up all audio resources
recognizer.recognitionTask(with: request) { result, error in
    if result?.isFinal == true || error != nil {
        self.audioEngine.stop()
        self.audioEngine.inputNode.removeTap(onBus: 0)
        self.recognitionRequest?.endAudio()
        self.recognitionRequest = nil
    }
}
```

### Assuming on-device recognition is available for all locales

```swift
// ❌ DON'T: Force on-device without checking support
let request = SFSpeechAudioBufferRecognitionRequest()
request.requiresOnDeviceRecognition = true // May silently fail

// ✅ DO: Check support before requiring on-device
if recognizer.supportsOnDeviceRecognition {
    request.requiresOnDeviceRecognition = true
} else {
    // Fall back to server-based or inform user
}
```

### Not handling the one-minute recognition limit

```swift
// ❌ DON'T: Start one long continuous recognition session
func startRecording() {
    // This will be cut off after ~60 seconds (server-based)
}

// ✅ DO: Restart recognition when approaching the limit
func startRecording() {
    // Use a timer to restart before the limit
    recognitionTimer = Timer.scheduledTimer(withTimeInterval: 55, repeats: false) {
        [weak self] _ in
        self?.restartRecognition()
    }
}
```

### Creating multiple simultaneous recognition tasks

```swift
// ❌ DON'T: Start a new task without canceling the previous one
func startRecording() {
    recognitionTask = recognizer.recognitionTask(with: request) { ... }
    // Previous task is still running — undefined behavior
}

// ✅ DO: Cancel existing task before creating a new one
func startRecording() {
    recognitionTask?.cancel()
    recognitionTask = nil
    recognitionTask = recognizer.recognitionTask(with: request) { ... }
}
```

## Review Checklist

- [ ] `NSSpeechRecognitionUsageDescription` is in Info.plist
- [ ] `NSMicrophoneUsageDescription` is in Info.plist (if using live audio)
- [ ] Authorization is requested before starting recognition
- [ ] `SFSpeechRecognizerDelegate` is set to handle `availabilityDidChange`
- [ ] Audio engine is stopped and tap removed when recognition ends
- [ ] `recognitionRequest.endAudio()` is called when done recording
- [ ] Previous `recognitionTask` is canceled before starting a new one
- [ ] `supportsOnDeviceRecognition` is checked before requiring on-device mode
- [ ] Partial results are handled separately from final (`isFinal`) results
- [ ] One-minute limit is accounted for in server-based recognition
- [ ] For iOS 26+: `AssetInventory` assets are installed before using `SpeechAnalyzer`
- [ ] For iOS 26+: `SpeechTranscriber.supportedLocale(equivalentTo:)` is checked

## References

- [Speech framework](https://sosumi.ai/documentation/speech)
- [SpeechAnalyzer](https://sosumi.ai/documentation/speech/speechanalyzer)
- [SpeechTranscriber](https://sosumi.ai/documentation/speech/speechtranscriber)
- [SFSpeechRecognizer](https://sosumi.ai/documentation/speech/sfspeechrecognizer)
- [SFSpeechAudioBufferRecognitionRequest](https://sosumi.ai/documentation/speech/sfspeechaudiobufferrecognitionrequest)
- [SFSpeechURLRecognitionRequest](https://sosumi.ai/documentation/speech/sfspeechurlrecognitionrequest)
- [SFSpeechRecognitionResult](https://sosumi.ai/documentation/speech/sfspeechrecognitionresult)
- [SFSpeechRecognitionRequest](https://sosumi.ai/documentation/speech/sfspeechrecognitionrequest)
- [AssetInventory](https://sosumi.ai/documentation/speech/assetinventory)
- [Asking Permission to Use Speech Recognition](https://sosumi.ai/documentation/speech/asking-permission-to-use-speech-recognition)
- [Recognizing Speech in Live Audio](https://sosumi.ai/documentation/speech/recognizing-speech-in-live-audio)
