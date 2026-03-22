---
name: shareplay-activities
description: "Build shared real-time experiences using GroupActivities and SharePlay. Use when implementing shared media playback, collaborative app features, synchronized game state, or any FaceTime/iMessage-integrated group activity on iOS, macOS, tvOS, or visionOS."
---

# GroupActivities / SharePlay

Build shared real-time experiences using the GroupActivities framework. SharePlay
connects people over FaceTime or iMessage, synchronizing media playback, app state,
or custom data. Targets Swift 6.2 / iOS 26+.

## Contents

- [Setup](#setup)
- [Defining a GroupActivity](#defining-a-groupactivity)
- [Session Lifecycle](#session-lifecycle)
- [Sending and Receiving Messages](#sending-and-receiving-messages)
- [Coordinated Media Playback](#coordinated-media-playback)
- [Starting SharePlay from Your App](#starting-shareplay-from-your-app)
- [GroupSessionJournal: File Transfer](#groupsessionjournal-file-transfer)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Setup

### Entitlements

Add the Group Activities entitlement to your app:

```xml
<key>com.apple.developer.group-session</key>
<true/>
```

### Info.plist

For apps that start SharePlay without a FaceTime call (iOS 17+), add:

```xml
<key>NSSupportsGroupActivities</key>
<true/>
```

### Checking Eligibility

```swift
import GroupActivities

let observer = GroupStateObserver()

// Check if a FaceTime call or iMessage group is active
if observer.isEligibleForGroupSession {
    showSharePlayButton()
}
```

Observe changes reactively:

```swift
for await isEligible in observer.$isEligibleForGroupSession.values {
    showSharePlayButton(isEligible)
}
```

## Defining a GroupActivity

Conform to `GroupActivity` and provide metadata:

```swift
import GroupActivities
import CoreTransferable

struct WatchTogetherActivity: GroupActivity {
    let movieID: String
    let movieTitle: String

    var metadata: GroupActivityMetadata {
        var meta = GroupActivityMetadata()
        meta.title = movieTitle
        meta.type = .watchTogether
        meta.fallbackURL = URL(string: "https://example.com/movie/\(movieID)")
        return meta
    }
}
```

### Activity Types

| Type | Use Case |
|---|---|
| `.generic` | Default for custom activities |
| `.watchTogether` | Video playback |
| `.listenTogether` | Audio playback |
| `.createTogether` | Collaborative creation (drawing, editing) |
| `.workoutTogether` | Shared fitness sessions |

The activity struct must conform to `Codable` so the system can transfer it
between devices.

## Session Lifecycle

### Listening for Sessions

Set up a long-lived task to receive sessions when another participant starts
the activity:

```swift
@Observable
@MainActor
final class SharePlayManager {
    private var session: GroupSession<WatchTogetherActivity>?
    private var messenger: GroupSessionMessenger?
    private var tasks = TaskGroup()

    func observeSessions() {
        Task {
            for await session in WatchTogetherActivity.sessions() {
                self.configureSession(session)
            }
        }
    }

    private func configureSession(
        _ session: GroupSession<WatchTogetherActivity>
    ) {
        self.session = session
        self.messenger = GroupSessionMessenger(session: session)

        // Observe session state changes
        Task {
            for await state in session.$state.values {
                handleState(state)
            }
        }

        // Observe participant changes
        Task {
            for await participants in session.$activeParticipants.values {
                handleParticipants(participants)
            }
        }

        // Join the session
        session.join()
    }
}
```

### Session States

| State | Description |
|---|---|
| `.waiting` | Session exists but local participant has not joined |
| `.joined` | Local participant is actively in the session |
| `.invalidated(reason:)` | Session ended (check reason for details) |

### Handling State Changes

```swift
private func handleState(_ state: GroupSession<WatchTogetherActivity>.State) {
    switch state {
    case .waiting:
        print("Waiting to join")
    case .joined:
        print("Joined session")
        loadActivity(session?.activity)
    case .invalidated(let reason):
        print("Session ended: \(reason)")
        cleanUp()
    @unknown default:
        break
    }
}

private func handleParticipants(_ participants: Set<Participant>) {
    print("Active participants: \(participants.count)")
}
```

### Leaving and Ending

```swift
// Leave the session (other participants continue)
session?.leave()

// End the session for all participants
session?.end()
```

## Sending and Receiving Messages

Use `GroupSessionMessenger` to sync app state between participants.

### Defining Messages

Messages must be `Codable`:

```swift
struct SyncMessage: Codable {
    let action: String
    let timestamp: Date
    let data: [String: String]
}
```

### Sending

```swift
func sendSync(_ message: SyncMessage) async throws {
    guard let messenger else { return }

    try await messenger.send(message, to: .all)
}

// Send to specific participants
try await messenger.send(message, to: .only(participant))
```

### Receiving

```swift
func observeMessages() {
    guard let messenger else { return }

    Task {
        for await (message, context) in messenger.messages(of: SyncMessage.self) {
            let sender = context.source
            handleReceivedMessage(message, from: sender)
        }
    }
}
```

### Delivery Modes

```swift
// Reliable (default) -- guaranteed delivery, ordered
let reliableMessenger = GroupSessionMessenger(
    session: session,
    deliveryMode: .reliable
)

// Unreliable -- faster, no guarantees (good for frequent position updates)
let unreliableMessenger = GroupSessionMessenger(
    session: session,
    deliveryMode: .unreliable
)
```

Use `.reliable` for state-changing actions (play/pause, selections). Use
`.unreliable` for high-frequency ephemeral data (cursor positions, drawing strokes).

## Coordinated Media Playback

For video/audio, use `AVPlaybackCoordinator` with `AVPlayer`:

```swift
import AVFoundation
import GroupActivities

func configurePlayback(
    session: GroupSession<WatchTogetherActivity>,
    player: AVPlayer
) {
    // Connect the player's coordinator to the session
    let coordinator = player.playbackCoordinator
    coordinator.coordinateWithSession(session)
}
```

Once connected, play/pause/seek actions on any participant's player are
automatically synchronized to all other participants. No manual message
passing is needed for playback controls.

### Handling Playback Events

```swift
// Notify participants about playback events
let event = GroupSessionEvent(
    originator: session.localParticipant,
    action: .play,
    url: nil
)
session.showNotice(event)
```

## Starting SharePlay from Your App

### Using GroupActivitySharingController (UIKit)

```swift
import GroupActivities
import UIKit

func startSharePlay() async throws {
    let activity = WatchTogetherActivity(
        movieID: "123",
        movieTitle: "Great Movie"
    )

    switch await activity.prepareForActivation() {
    case .activationPreferred:
        // Present the sharing controller
        let controller = try GroupActivitySharingController(activity)
        present(controller, animated: true)

    case .activationDisabled:
        // SharePlay is disabled or unavailable
        print("SharePlay not available")

    case .cancelled:
        break

    @unknown default:
        break
    }
}
```

For `ShareLink` (SwiftUI) and direct `activity.activate()` patterns, see
`references/shareplay-patterns.md`.

## GroupSessionJournal: File Transfer

For large data (images, files), use `GroupSessionJournal` instead of
`GroupSessionMessenger` (which has a size limit):

```swift
import GroupActivities

let journal = GroupSessionJournal(session: session)

// Upload a file
let attachment = try await journal.add(imageData)

// Observe incoming attachments
Task {
    for await attachments in journal.attachments {
        for attachment in attachments {
            let data = try await attachment.load(Data.self)
            handleReceivedFile(data)
        }
    }
}
```

## Common Mistakes

### DON'T: Forget to call session.join()

```swift
// WRONG -- session is received but never joined
for await session in MyActivity.sessions() {
    self.session = session
    // Session stays in .waiting state forever
}

// CORRECT -- join after configuring
for await session in MyActivity.sessions() {
    self.session = session
    self.messenger = GroupSessionMessenger(session: session)
    session.join()
}
```

### DON'T: Forget to leave or end sessions

```swift
// WRONG -- session stays alive after the user navigates away
func viewDidDisappear() {
    // Nothing -- session leaks
}

// CORRECT -- leave when the view is dismissed
func viewDidDisappear() {
    session?.leave()
    session = nil
    messenger = nil
}
```

### DON'T: Assume all participants have the same state

```swift
// WRONG -- broadcasting state without handling late joiners
func onJoin() {
    // New participant has no idea what the current state is
}

// CORRECT -- send full state to new participants
func handleParticipants(_ participants: Set<Participant>) {
    let newParticipants = participants.subtracting(knownParticipants)
    for participant in newParticipants {
        Task {
            try await messenger?.send(currentState, to: .only(participant))
        }
    }
    knownParticipants = participants
}
```

### DON'T: Use GroupSessionMessenger for large data

```swift
// WRONG -- messenger has a per-message size limit
let largeImage = try Data(contentsOf: imageURL)  // 5 MB
try await messenger.send(largeImage, to: .all)    // May fail

// CORRECT -- use GroupSessionJournal for files
let journal = GroupSessionJournal(session: session)
try await journal.add(largeImage)
```

### DON'T: Send redundant messages for media playback

```swift
// WRONG -- manually syncing play/pause when using AVPlayer
func play() {
    player.play()
    try await messenger.send(PlayMessage(), to: .all)
}

// CORRECT -- let AVPlaybackCoordinator handle it
player.playbackCoordinator.coordinateWithSession(session)
player.play()  // Automatically synced to all participants
```

### DON'T: Observe sessions in a view that gets recreated

```swift
// WRONG -- each time the view appears, a new listener is created
struct MyView: View {
    var body: some View {
        Text("Hello")
            .task {
                for await session in MyActivity.sessions() { }
            }
    }
}

// CORRECT -- observe sessions in a long-lived manager
@Observable
final class ActivityManager {
    init() {
        Task {
            for await session in MyActivity.sessions() {
                configureSession(session)
            }
        }
    }
}
```

## Review Checklist

- [ ] Group Activities entitlement (`com.apple.developer.group-session`) added
- [ ] `GroupActivity` struct is `Codable` with meaningful metadata
- [ ] `sessions()` observed in a long-lived object (not a SwiftUI view body)
- [ ] `session.join()` called after receiving and configuring the session
- [ ] `session.leave()` called when the user navigates away or dismisses
- [ ] `GroupSessionMessenger` created with appropriate `deliveryMode`
- [ ] Late-joining participants receive current state on connection
- [ ] `$state` and `$activeParticipants` publishers observed for lifecycle changes
- [ ] `GroupSessionJournal` used for large file transfers instead of messenger
- [ ] `AVPlaybackCoordinator` used for media sync (not manual messages)
- [ ] `GroupStateObserver.isEligibleForGroupSession` checked before showing SharePlay UI
- [ ] `prepareForActivation()` called before presenting sharing controller
- [ ] Session invalidation handled with cleanup of messenger, journal, and tasks

## References

- Extended patterns (collaborative canvas, spatial Personas, custom templates): `references/shareplay-patterns.md`
- [GroupActivities framework](https://sosumi.ai/documentation/groupactivities)
- [GroupActivity protocol](https://sosumi.ai/documentation/groupactivities/groupactivity)
- [GroupSession](https://sosumi.ai/documentation/groupactivities/groupsession)
- [GroupSessionMessenger](https://sosumi.ai/documentation/groupactivities/groupsessionmessenger)
- [GroupSessionJournal](https://sosumi.ai/documentation/groupactivities/groupsessionjournal)
- [GroupStateObserver](https://sosumi.ai/documentation/groupactivities/groupstateobserver)
- [GroupActivitySharingController](https://sosumi.ai/documentation/groupactivities/groupactivitysharingcontroller-ybcy)
- [Defining your app's SharePlay activities](https://sosumi.ai/documentation/groupactivities/defining-your-apps-shareplay-activities)
- [Presenting SharePlay activities from your app's UI](https://sosumi.ai/documentation/groupactivities/promoting-shareplay-activities-from-your-apps-ui)
- [Synchronizing data during a SharePlay activity](https://sosumi.ai/documentation/groupactivities/synchronizing-data-during-a-shareplay-activity)
