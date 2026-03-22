---
name: permissionkit
description: "Create child communication safety experiences using PermissionKit to request parental permission for children. Use when building apps that involve child-to-contact communication, need to check communication limits, request parent/guardian approval, or handle permission responses for minors."
---

# PermissionKit

> **Note:** PermissionKit is new in iOS 26. Method signatures should be verified against the latest Xcode 26 beta SDK.

Request permission from a parent or guardian to modify a child's communication
rules. PermissionKit creates communication safety experiences that let children
ask for exceptions to communication limits set by their parents. Targets
Swift 6.2 / iOS 26+.

## Contents

- [Setup](#setup)
- [Core Concepts](#core-concepts)
- [Checking Communication Limits](#checking-communication-limits)
- [Creating Permission Questions](#creating-permission-questions)
- [Requesting Permission with AskCenter](#requesting-permission-with-askcenter)
- [SwiftUI Integration with PermissionButton](#swiftui-integration-with-permissionbutton)
- [Handling Responses](#handling-responses)
- [Significant App Update Topic](#significant-app-update-topic)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Setup

Import `PermissionKit`. No special entitlements are required.

```swift
import PermissionKit
```

**Platform availability:** iOS 26+, iPadOS 26+, macOS 26+.

## Core Concepts

PermissionKit manages a flow where:

1. A child encounters a communication limit in your app
2. Your app creates a `PermissionQuestion` describing the request
3. The system presents the question to the child for them to send to their parent
4. The parent reviews and approves or denies the request
5. Your app receives a `PermissionResponse` with the parent's decision

### Key Types

| Type | Role |
|---|---|
| `AskCenter` | Singleton that manages permission requests and responses |
| `PermissionQuestion` | Describes the permission being requested |
| `PermissionResponse` | The parent's decision (approval or denial) |
| `PermissionChoice` | The specific answer (approve/decline) |
| `PermissionButton` | SwiftUI button that triggers the permission flow |
| `CommunicationTopic` | Topic for communication-related permission requests |
| `CommunicationHandle` | A phone number, email, or custom identifier |
| `CommunicationLimits` | Checks whether communication limits apply |
| `SignificantAppUpdateTopic` | Topic for significant app update permission requests |

## Checking Communication Limits

Before presenting a permission request, check if communication limits are
enabled and whether the handle is known.

```swift
import PermissionKit

func checkCommunicationStatus(for handle: CommunicationHandle) async -> Bool {
    let limits = CommunicationLimits.current
    let isKnown = await limits.isKnownHandle(handle)
    return isKnown
}

// Check multiple handles at once
func filterKnownHandles(_ handles: Set<CommunicationHandle>) async -> Set<CommunicationHandle> {
    let limits = CommunicationLimits.current
    return await limits.knownHandles(in: handles)
}
```

### Creating Communication Handles

```swift
let phoneHandle = CommunicationHandle(
    value: "+1234567890",
    kind: .phoneNumber
)

let emailHandle = CommunicationHandle(
    value: "friend@example.com",
    kind: .emailAddress
)

let customHandle = CommunicationHandle(
    value: "user123",
    kind: .custom
)
```

## Creating Permission Questions

Build a `PermissionQuestion` with the contact information and communication
action type.

```swift
// Question for a single contact
let handle = CommunicationHandle(value: "+1234567890", kind: .phoneNumber)
let question = PermissionQuestion<CommunicationTopic>(handle: handle)

// Question for multiple contacts
let handles = [
    CommunicationHandle(value: "+1234567890", kind: .phoneNumber),
    CommunicationHandle(value: "friend@example.com", kind: .emailAddress)
]
let multiQuestion = PermissionQuestion<CommunicationTopic>(handles: handles)
```

### Using CommunicationTopic with Person Information

Provide display names and avatars for a richer permission prompt.

```swift
let personInfo = CommunicationTopic.PersonInformation(
    handle: CommunicationHandle(value: "+1234567890", kind: .phoneNumber),
    nameComponents: {
        var name = PersonNameComponents()
        name.givenName = "Alex"
        name.familyName = "Smith"
        return name
    }(),
    avatarImage: nil
)

let topic = CommunicationTopic(
    personInformation: [personInfo],
    actions: [.message, .audioCall]
)

let question = PermissionQuestion<CommunicationTopic>(communicationTopic: topic)
```

### Communication Actions

| Action | Description |
|---|---|
| `.message` | Text messaging |
| `.audioCall` | Voice call |
| `.videoCall` | Video call |
| `.call` | Generic call |
| `.chat` | Chat communication |
| `.follow` | Follow a user |
| `.beFollowed` | Allow being followed |
| `.friend` | Friend request |
| `.connect` | Connection request |
| `.communicate` | Generic communication |

## Requesting Permission with AskCenter

Use `AskCenter.shared` to present the permission request to the child.

```swift
import PermissionKit

func requestPermission(
    for question: PermissionQuestion<CommunicationTopic>,
    in viewController: UIViewController
) async {
    do {
        try await AskCenter.shared.ask(question, in: viewController)
        // Question was presented to the child
    } catch let error as AskError {
        switch error {
        case .communicationLimitsNotEnabled:
            // Communication limits not active -- no permission needed
            break
        case .contactSyncNotSetup:
            // Contact sync not configured
            break
        case .invalidQuestion:
            // Question is malformed
            break
        case .notAvailable:
            // PermissionKit not available on this device
            break
        case .systemError(let underlying):
            print("System error: \(underlying)")
        case .unknown:
            break
        @unknown default:
            break
        }
    }
}
```

## SwiftUI Integration with PermissionButton

`PermissionButton` is a SwiftUI view that triggers the permission flow
when tapped.

```swift
import SwiftUI
import PermissionKit

struct ContactPermissionView: View {
    let handle = CommunicationHandle(value: "+1234567890", kind: .phoneNumber)

    var body: some View {
        let question = PermissionQuestion<CommunicationTopic>(handle: handle)

        PermissionButton(question: question) {
            Label("Ask to Message", systemImage: "message")
        }
    }
}
```

### PermissionButton with Custom Topic

```swift
struct CustomPermissionView: View {
    var body: some View {
        let personInfo = CommunicationTopic.PersonInformation(
            handle: CommunicationHandle(value: "user456", kind: .custom),
            nameComponents: nil,
            avatarImage: nil
        )
        let topic = CommunicationTopic(
            personInformation: [personInfo],
            actions: [.follow]
        )
        let question = PermissionQuestion<CommunicationTopic>(
            communicationTopic: topic
        )

        PermissionButton(question: question) {
            Text("Ask to Follow")
        }
    }
}
```

## Handling Responses

Listen for permission responses asynchronously.

```swift
func observeResponses() async {
    let responses = AskCenter.shared.responses(for: CommunicationTopic.self)

    for await response in responses {
        let choice = response.choice
        let question = response.question

        switch choice.answer {
        case .approval:
            // Parent approved -- enable communication
            print("Approved for topic: \(question.topic)")
        case .denial:
            // Parent denied -- keep restriction
            print("Denied")
        @unknown default:
            break
        }
    }
}
```

### PermissionChoice Properties

```swift
let choice: PermissionChoice = response.choice
print("Answer: \(choice.answer)")  // .approval or .denial
print("Choice ID: \(choice.id)")
print("Title: \(choice.title)")

// Convenience statics
let approved = PermissionChoice.approve
let declined = PermissionChoice.decline
```

## Significant App Update Topic

Request permission for significant app updates that require parental approval.

```swift
let updateTopic = SignificantAppUpdateTopic(
    description: "This update adds multiplayer chat features"
)

let question = PermissionQuestion<SignificantAppUpdateTopic>(
    significantAppUpdateTopic: updateTopic
)

// Present the question
try await AskCenter.shared.ask(question, in: viewController)

// Listen for responses
for await response in AskCenter.shared.responses(for: SignificantAppUpdateTopic.self) {
    switch response.choice.answer {
    case .approval:
        // Proceed with update
        break
    case .denial:
        // Skip update
        break
    @unknown default:
        break
    }
}
```

## Common Mistakes

### DON'T: Skip checking if communication limits are enabled

If communication limits are not enabled, calling `ask` throws
`.communicationLimitsNotEnabled`. Check first or handle the error.

```swift
// WRONG: Assuming limits are always active
try await AskCenter.shared.ask(question, in: viewController)

// CORRECT: Handle the case where limits are not enabled
do {
    try await AskCenter.shared.ask(question, in: viewController)
} catch AskError.communicationLimitsNotEnabled {
    // Communication limits not active -- allow communication directly
    allowCommunication()
} catch {
    handleError(error)
}
```

### DON'T: Ignore AskError cases

Each error case requires different handling.

```swift
// WRONG: Catch-all with no user feedback
do {
    try await AskCenter.shared.ask(question, in: viewController)
} catch {
    print(error)
}

// CORRECT: Handle each case
do {
    try await AskCenter.shared.ask(question, in: viewController)
} catch let error as AskError {
    switch error {
    case .communicationLimitsNotEnabled:
        allowCommunication()
    case .contactSyncNotSetup:
        showContactSyncPrompt()
    case .invalidQuestion:
        showInvalidQuestionAlert()
    case .notAvailable:
        showUnavailableMessage()
    case .systemError(let underlying):
        showSystemError(underlying)
    case .unknown:
        showGenericError()
    @unknown default:
        break
    }
}
```

### DON'T: Create questions with empty handles

A question with no handles or person information is invalid.

```swift
// WRONG: Empty handles array
let question = PermissionQuestion<CommunicationTopic>(handles: [])  // Invalid

// CORRECT: Provide at least one handle
let handle = CommunicationHandle(value: "+1234567890", kind: .phoneNumber)
let question = PermissionQuestion<CommunicationTopic>(handle: handle)
```

### DON'T: Forget to observe responses

Presenting a question without listening for the response means you never
know if the parent approved.

```swift
// WRONG: Fire and forget
try await AskCenter.shared.ask(question, in: viewController)

// CORRECT: Observe responses
Task {
    for await response in AskCenter.shared.responses(for: CommunicationTopic.self) {
        handleResponse(response)
    }
}
try await AskCenter.shared.ask(question, in: viewController)
```

### DON'T: Use deprecated CommunicationLimitsButton

Use `PermissionButton` instead of the deprecated `CommunicationLimitsButton`.

```swift
// WRONG: Deprecated
CommunicationLimitsButton(question: question) {
    Text("Ask Permission")
}

// CORRECT: Use PermissionButton
PermissionButton(question: question) {
    Text("Ask Permission")
}
```

## Review Checklist

- [ ] `AskError.communicationLimitsNotEnabled` handled to allow fallback
- [ ] `AskError` cases handled individually with appropriate user feedback
- [ ] `CommunicationHandle` created with correct `Kind` (phone, email, custom)
- [ ] `PermissionQuestion` includes at least one handle or person information
- [ ] `AskCenter.shared.responses(for:)` observed to receive parent decisions
- [ ] `PermissionButton` used instead of deprecated `CommunicationLimitsButton`
- [ ] Person information includes name components for a clear permission prompt
- [ ] Communication actions match the app's actual communication capabilities
- [ ] Response handling updates UI on the main actor
- [ ] Error states provide clear guidance to the user

## References

- Extended patterns (response handling, multi-topic, UIKit): `references/permissionkit-patterns.md`
- [PermissionKit framework](https://sosumi.ai/documentation/permissionkit)
- [AskCenter](https://sosumi.ai/documentation/permissionkit/askcenter)
- [PermissionQuestion](https://sosumi.ai/documentation/permissionkit/permissionquestion)
- [PermissionButton](https://sosumi.ai/documentation/permissionkit/permissionbutton)
- [PermissionResponse](https://sosumi.ai/documentation/permissionkit/permissionresponse)
- [CommunicationTopic](https://sosumi.ai/documentation/permissionkit/communicationtopic)
- [CommunicationHandle](https://sosumi.ai/documentation/permissionkit/communicationhandle)
- [CommunicationLimits](https://sosumi.ai/documentation/permissionkit/communicationlimits)
- [SignificantAppUpdateTopic](https://sosumi.ai/documentation/permissionkit/significantappupdatetopic)
- [AskError](https://sosumi.ai/documentation/permissionkit/askerror)
- [Creating a communication experience](https://sosumi.ai/documentation/permissionkit/creating-a-communication-experience)
