---
name: shareplay-developer
description: Build, integrate, and troubleshoot SharePlay GroupActivities features,
  including GroupActivity definitions, activation flows, GroupSession lifecycle, messaging
  and journals, ShareLink and SharePlay UI
---

---

## name: shareplay-developer
description: Build, integrate, and troubleshoot SharePlay GroupActivities features, including GroupActivity definitions, activation flows, GroupSession lifecycle, messaging and journals, ShareLink and SharePlay UI surfaces, and visionOS spatial coordination. Use when implementing or debugging SharePlay experiences across Apple platforms, especially visionOS.

# SharePlay Developer

## Description and Goals

This skill provides comprehensive guidance for implementing SharePlay experiences with the GroupActivities framework. It covers activity definition, session lifecycle, state synchronization, UI surfaces, and visionOS spatial coordination.

### Goals

- Enable developers to build SharePlay experiences across Apple platforms
- Guide proper GroupActivity definition and activation
- Support GroupSession lifecycle management
- Help implement state synchronization with messaging and journals
- Enable spatial coordination for visionOS experiences

## What This Skill Should Do

When implementing SharePlay features, this skill should:

1. **Guide activity setup** - Help you define GroupActivity types and metadata
2. **Handle activation** - Show how to check eligibility and activate SharePlay
3. **Manage sessions** - Demonstrate GroupSession lifecycle and participant management
4. **Sync state** - Provide patterns for messaging and journal-based synchronization
5. **Coordinate spatially** - Show how to use SystemCoordinator for visionOS spatial experiences
6. **Present UI** - Guide use of ShareLink and other SharePlay UI surfaces

Load the appropriate reference file from the tables below for detailed usage, code examples, and best practices.

### Quick Start Workflow

1. Add the Group Activities capability and `com.apple.developer.group-session` entitlement in Xcode.
2. Define a `GroupActivity` type per experience and keep its data minimal and `Codable`.
3. Provide `GroupActivityMetadata` with a clear title, type, and fallback URL.
4. Check `GroupStateObserver.isEligibleForGroupSession` and activate or present SharePlay UI.
5. Listen for sessions with `for await session in Activity.sessions()` and store the session strongly.
6. Configure `SystemCoordinator` before `join()` when spatial personas or immersive spaces are involved.
7. Call `session.join()` only after UI and state are ready.
8. Sync state with `GroupSessionMessenger` (small, time-sensitive) or `GroupSessionJournal` (attachments).
9. Observe `activeParticipants` and send a state snapshot for late joiners.
10. Call `leave()` or `end()` and cancel tasks when the session invalidates.

## Information About the Skill

### Core Concepts

#### Activity Definition

- Use `GroupActivity` to define the shareable experience and keep payloads minimal.
- Provide `GroupActivity.metadata` with title, subtitle, preview image, and fallback URL.
- Set `GroupActivityMetadata.type` to a matching `ActivityType` value.
- Use `GroupActivityActivationResult` from `prepareForActivation()` to decide activation.
- Use `GroupActivityTransferRepresentation` for `ShareLink` and share sheets.

#### Session Lifecycle and Participants

- Use `GroupSession` to manage the live activity; call `join()`, `leave()`, or `end()`.
- Observe `GroupSession.state`, `activeParticipants`, and `isLocallyInitiated` to drive UI.
- Use `GroupSession.sceneSessionIdentifier` to map sessions to scenes when needed.
- Call `requestForegroundPresentation()` when the activity needs the app visible.
- Use `GroupSession.showNotice(_:)` or `postEvent(_:)` for system playback notices.

#### Messaging and Transfer

- Use `GroupSessionMessenger` for small messages (<= 256 KB).
- Use `.reliable` delivery for critical state and `.unreliable` for high-frequency updates.
- Use `GroupSessionJournal` for attachments and large data (<= 100 MB).

#### UI Surfaces to Start SharePlay

- Use `ShareLink` with `Transferable` + `GroupActivityTransferRepresentation` in SwiftUI.
- Use `GroupActivitySharingController` in UIKit/AppKit when no FaceTime call is active.
- Use `NSItemProvider.registerGroupActivity(...)` in share sheets when needed.

#### visionOS Spatial Coordination

- Use `SystemCoordinator` from `GroupSession.systemCoordinator` for spatial layout.
- Set `spatialTemplatePreference` and `supportsGroupImmersiveSpace` as needed.
- Use `localParticipantStates` and `remoteParticipantStates` to track poses.
- Use `groupActivityAssociation(_:)` to choose the primary scene.

### Reference Files


| Reference                                 | When to Use                                                         |
| ----------------------------------------- | ------------------------------------------------------------------- |
| `[REFERENCE.md](references/REFERENCE.md)` | When looking for GroupActivities-focused code samples and excerpts. |


### Implementation Patterns

- Send a full state snapshot when new participants join.
- Keep UI state separate from shared game state to reduce message churn.
- Use `GroupSessionMessenger` for transient actions and `GroupSessionJournal` for durable data.
- Prefer AVFoundation coordinated playback for media sync.

### Pitfalls and Checks

- Keep `GroupActivity` data minimal; send state changes via messenger or journal.
- Store strong references to `GroupSession`, `GroupSessionMessenger`, and `GroupSessionJournal`.
- Join only when UI and state are ready; call `leave()` on teardown.
- Handle late joiners by sending the current state snapshot on `activeParticipants` change.

