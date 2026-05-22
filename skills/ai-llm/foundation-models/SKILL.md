---
name: foundation-models
description: Apple Foundation Models framework for on-device AI, @Generable macro, guided generation, tool calling, and streaming. Use when user asks about on-device AI, Apple Intelligence, Foundation Models, @Generable, LLM, or local machine learning.
allowed-tools: Bash, Read, Write, Edit
---

# Apple Foundation Models Framework

Comprehensive guide to Apple's Foundation Models framework for on-device AI inference, structured output generation, tool calling, and streaming responses in iOS 26.

## Prerequisites

- iOS 26+, macOS Tahoe+, iPadOS 26+, or visionOS 26+
- Device with Apple Intelligence support (A17 Pro or later, M-series)
- Xcode 26+

---

## Framework Overview

### What is Foundation Models?

Apple's Foundation Models framework provides:
- **~3B parameter on-device LLM** powered by Apple Intelligence
- **Privacy-first**: All inference runs locally, no data leaves device
- **Cost-free**: No API fees, no cloud dependency
- **Offline-capable**: Works without network connection
- **Low-latency**: Direct device access for fast responses

### Import

```swift
import FoundationModels
```

### Basic Usage

```swift
let session = LanguageModelSession()

let response = try await session.respond(
    to: "What's the capital of France?"
)
print(response.content)  // "Paris is the capital of France."
```

---

## LanguageModelSession

### Creating a Session

```swift
// Default session
let session = LanguageModelSession()

// With custom configuration
let config = LanguageModelSession.Configuration(
    maxTokens: 1000,
    temperature: 0.7
)
let configuredSession = LanguageModelSession(configuration: config)
```

### Session Configuration Options

```swift
LanguageModelSession.Configuration(
    // Maximum tokens in response
    maxTokens: 500,

    // Randomness (0.0 = deterministic, 1.0 = creative)
    temperature: 0.7,

    // Top-p nucleus sampling
    topP: 0.9,

    // Penalty for repeating tokens
    frequencyPenalty: 0.5,

    // Penalty for tokens already in context
    presencePenalty: 0.5
)
```

### Simple Text Response

```swift
let session = LanguageModelSession()

do {
    let response = try await session.respond(to: "Explain quantum computing in simple terms")
    print(response.content)
} catch {
    print("Error: \(error)")
}
```

### Check Availability

```swift
if LanguageModelSession.isAvailable {
    // Foundation Models is available
    let session = LanguageModelSession()
} else {
    // Fall back to alternative approach
    showUnsupportedDeviceMessage()
}
```

---

## @Generable Macro

### Basic Structured Output

The `@Generable` macro enables type-safe AI output:

```swift
import FoundationModels

@Generable
struct MovieRecommendation {
    var title: String
    var year: Int
    var genre: String
    var reason: String
}

// Usage
let session = LanguageModelSession()
let recommendation: MovieRecommendation = try await session.respond(
    to: "Recommend a sci-fi movie from the 2020s"
)

print(recommendation.title)   // "Dune"
print(recommendation.year)    // 2021
print(recommendation.genre)   // "Science Fiction"
print(recommendation.reason)  // "Epic visuals and compelling story..."
```

### @Generable Requirements

```swift
// Supported property types:
@Generable
struct ValidExample {
    var text: String           // ✓
    var number: Int            // ✓
    var decimal: Double        // ✓
    var flag: Bool             // ✓
    var items: [String]        // ✓ Arrays
    var optional: String?      // ✓ Optionals
    var nested: NestedType     // ✓ Other @Generable types
    var choice: MyEnum         // ✓ Enums (with raw values)
}

// Enums must have raw values
@Generable
enum Sentiment: String {
    case positive
    case negative
    case neutral
}
```

### Complex Nested Structures

```swift
@Generable
struct RecipeAnalysis {
    var name: String
    var difficulty: Difficulty
    var ingredients: [Ingredient]
    var nutritionInfo: NutritionInfo
    var tips: [String]
}

@Generable
struct Ingredient {
    var name: String
    var amount: String
    var isOptional: Bool
}

@Generable
struct NutritionInfo {
    var calories: Int
    var protein: Int
    var carbs: Int
    var fat: Int
}

@Generable
enum Difficulty: String {
    case easy
    case medium
    case hard
}

// Usage
let session = LanguageModelSession()
let analysis: RecipeAnalysis = try await session.respond(
    to: "Analyze this recipe: [recipe text here]"
)
```

### Adding Descriptions

```swift
@Generable
struct TaskExtraction {
    /// The main task to be completed
    var task: String

    /// Priority level from 1 (low) to 5 (urgent)
    var priority: Int

    /// Estimated time in minutes
    var estimatedMinutes: Int

    /// Categories this task belongs to
    var categories: [String]
}
```

---

## Guided Generation

### System Instructions

```swift
let session = LanguageModelSession()

let instructions = """
You are a helpful cooking assistant. Provide recipes that are:
- Easy to follow
- Use common ingredients
- Include timing for each step
"""

let response = try await session.respond(
    to: "How do I make pasta carbonara?",
    systemInstructions: instructions
)
```

### With Structured Output

```swift
@Generable
struct Recipe {
    var name: String
    var prepTime: Int
    var cookTime: Int
    var servings: Int
    var ingredients: [String]
    var steps: [String]
}

let session = LanguageModelSession()

let recipe: Recipe = try await session.respond(
    to: "Give me a recipe for chocolate chip cookies",
    systemInstructions: "You are a professional baker. Provide precise measurements."
)
```

### Constraining Output

```swift
@Generable
enum ResponseCategory: String {
    case question
    case statement
    case request
    case greeting
}

@Generable
struct ClassifiedInput {
    var category: ResponseCategory
    var confidence: Double
    var explanation: String
}

let classification: ClassifiedInput = try await session.respond(
    to: "Classify this input: 'Could you help me with my homework?'"
)
// classification.category == .request
```

---

## Tool Calling

### Defining Tools

```swift
import FoundationModels

@Tool
struct WeatherTool {
    /// Get the current weather for a location
    /// - Parameter location: The city name to check weather for
    @ToolFunction
    func getWeather(location: String) async throws -> String {
        // Call your weather API
        let weather = try await weatherService.fetch(for: location)
        return "The weather in \(location) is \(weather.condition), \(weather.temperature)°F"
    }
}
```

### Using Tools in Session

```swift
let session = LanguageModelSession()
let weatherTool = WeatherTool()

let response = try await session.respond(
    to: "What's the weather like in San Francisco?",
    tools: [weatherTool]
)
// Model automatically calls getWeather(location: "San Francisco")
// and incorporates result into response
```

### Multiple Tools

```swift
@Tool
struct RestaurantTool {
    @ToolFunction
    func searchRestaurants(cuisine: String, location: String) async throws -> [Restaurant] {
        // Search logic
    }

    @ToolFunction
    func getRestaurantDetails(id: String) async throws -> RestaurantDetails {
        // Fetch details
    }
}

@Tool
struct ReservationTool {
    @ToolFunction
    func makeReservation(restaurantId: String, date: Date, partySize: Int) async throws -> Confirmation {
        // Booking logic
    }
}

let session = LanguageModelSession()
let response = try await session.respond(
    to: "Find an Italian restaurant in NYC and make a reservation for 4 people tonight",
    tools: [RestaurantTool(), ReservationTool()]
)
```

### Tool Parameters

```swift
@Tool
struct CalculatorTool {
    /// Perform basic arithmetic
    /// - Parameters:
    ///   - operation: The operation to perform (add, subtract, multiply, divide)
    ///   - a: First number
    ///   - b: Second number
    @ToolFunction
    func calculate(operation: Operation, a: Double, b: Double) -> Double {
        switch operation {
        case .add: return a + b
        case .subtract: return a - b
        case .multiply: return a * b
        case .divide: return a / b
        }
    }

    enum Operation: String, Codable {
        case add, subtract, multiply, divide
    }
}
```

---

## Streaming Responses

### Basic Streaming

```swift
let session = LanguageModelSession()

for try await partial in session.streamResponse(to: "Write a short story about a robot") {
    print(partial.content, terminator: "")
    // Prints incrementally as tokens arrive
}
```

### Streaming with SwiftUI

```swift
struct ChatView: View {
    @State private var response = ""
    @State private var isStreaming = false
    let session = LanguageModelSession()

    var body: some View {
        VStack {
            ScrollView {
                Text(response)
                    .padding()
            }

            Button(isStreaming ? "Generating..." : "Generate Story") {
                generateStory()
            }
            .disabled(isStreaming)
        }
    }

    func generateStory() {
        isStreaming = true
        response = ""

        Task {
            do {
                for try await partial in session.streamResponse(to: "Write a haiku about coding") {
                    response = partial.content
                }
            } catch {
                response = "Error: \(error.localizedDescription)"
            }
            isStreaming = false
        }
    }
}
```

### Streaming Structured Output

```swift
@Generable
struct Story {
    var title: String
    var chapters: [Chapter]
}

@Generable
struct Chapter {
    var title: String
    var content: String
}

// Stream partial structure updates
for try await partial: PartiallyGenerated<Story> in session.streamResponse(
    to: "Write a short story with 3 chapters"
) {
    // partial.value contains filled-in fields so far
    if let title = partial.value.title {
        print("Title: \(title)")
    }

    // Check completion status
    print("Progress: \(partial.progress)")
}
```

---

## Multi-Turn Conversations

### Maintaining Context

```swift
let session = LanguageModelSession()

// First turn
let response1 = try await session.respond(to: "My name is Alice")

// Second turn - session remembers context
let response2 = try await session.respond(to: "What's my name?")
// Response includes "Alice"

// Third turn
let response3 = try await session.respond(to: "Tell me a joke using my name")
// Uses "Alice" in the joke
```

### Explicit Message History

```swift
let session = LanguageModelSession()

var messages: [LanguageModelSession.Message] = [
    .user("You are a helpful assistant that speaks like a pirate."),
    .assistant("Ahoy! I be ready to help ye, matey!"),
    .user("What's the weather like?")
]

let response = try await session.respond(messages: messages)
// Response in pirate speak
```

### Chat Interface Example

```swift
struct ChatMessage: Identifiable {
    let id = UUID()
    let role: Role
    var content: String

    enum Role {
        case user, assistant
    }
}

@Observable
class ChatViewModel {
    var messages: [ChatMessage] = []
    var isGenerating = false
    private let session = LanguageModelSession()

    func send(_ text: String) async {
        let userMessage = ChatMessage(role: .user, content: text)
        messages.append(userMessage)

        isGenerating = true
        defer { isGenerating = false }

        do {
            var assistantContent = ""
            messages.append(ChatMessage(role: .assistant, content: ""))

            for try await partial in session.streamResponse(to: text) {
                assistantContent = partial.content
                messages[messages.count - 1].content = assistantContent
            }
        } catch {
            messages[messages.count - 1].content = "Error: \(error.localizedDescription)"
        }
    }
}
```

---

## Error Handling

### Common Errors

```swift
do {
    let response = try await session.respond(to: prompt)
} catch LanguageModelError.unavailable {
    // Device doesn't support Foundation Models
    showFallbackUI()
} catch LanguageModelError.contentFiltered {
    // Response filtered for safety
    showContentFilteredMessage()
} catch LanguageModelError.contextLengthExceeded {
    // Input too long
    showTruncationWarning()
} catch LanguageModelError.cancelled {
    // Request was cancelled
    // Handle gracefully
} catch {
    // Other errors
    showGenericError(error)
}
```

### Timeout Handling

```swift
let session = LanguageModelSession()

let response = try await withTimeout(seconds: 30) {
    try await session.respond(to: longPrompt)
}

func withTimeout<T>(seconds: Double, operation: @escaping () async throws -> T) async throws -> T {
    try await withThrowingTaskGroup(of: T.self) { group in
        group.addTask {
            try await operation()
        }

        group.addTask {
            try await Task.sleep(for: .seconds(seconds))
            throw TimeoutError()
        }

        let result = try await group.next()!
        group.cancelAll()
        return result
    }
}
```

---

## SwiftUI Integration

### Complete Chat Interface

```swift
import SwiftUI
import FoundationModels

struct AIChatView: View {
    @State private var viewModel = ChatViewModel()
    @State private var inputText = ""
    @FocusState private var isInputFocused: Bool

    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // Messages
                ScrollViewReader { proxy in
                    ScrollView {
                        LazyVStack(alignment: .leading, spacing: 12) {
                            ForEach(viewModel.messages) { message in
                                MessageBubble(message: message)
                                    .id(message.id)
                            }
                        }
                        .padding()
                    }
                    .onChange(of: viewModel.messages.count) {
                        if let lastId = viewModel.messages.last?.id {
                            withAnimation {
                                proxy.scrollTo(lastId, anchor: .bottom)
                            }
                        }
                    }
                }

                // Input
                HStack {
                    TextField("Ask anything...", text: $inputText)
                        .textFieldStyle(.roundedBorder)
                        .focused($isInputFocused)
                        .onSubmit { sendMessage() }

                    Button {
                        sendMessage()
                    } label: {
                        Image(systemName: "arrow.up.circle.fill")
                            .font(.title2)
                    }
                    .disabled(inputText.isEmpty || viewModel.isGenerating)
                }
                .padding()
            }
            .navigationTitle("AI Chat")
        }
    }

    func sendMessage() {
        let text = inputText
        inputText = ""
        Task {
            await viewModel.send(text)
        }
    }
}

struct MessageBubble: View {
    let message: ChatMessage

    var body: some View {
        HStack {
            if message.role == .user { Spacer() }

            Text(message.content)
                .padding(12)
                .background(message.role == .user ? Color.blue : Color.gray.opacity(0.2))
                .foregroundStyle(message.role == .user ? .white : .primary)
                .clipShape(RoundedRectangle(cornerRadius: 16))

            if message.role == .assistant { Spacer() }
        }
    }
}
```

### Structured Output in UI

```swift
@Generable
struct TaskSuggestion {
    var title: String
    var description: String
    var priority: Priority
    var estimatedMinutes: Int
}

@Generable
enum Priority: String {
    case low, medium, high
}

struct TaskSuggestionsView: View {
    @State private var suggestions: [TaskSuggestion] = []
    @State private var isLoading = false

    var body: some View {
        List(suggestions, id: \.title) { task in
            VStack(alignment: .leading) {
                HStack {
                    Text(task.title)
                        .font(.headline)
                    Spacer()
                    PriorityBadge(priority: task.priority)
                }
                Text(task.description)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
                Text("\(task.estimatedMinutes) min")
                    .font(.caption)
            }
        }
        .task {
            await loadSuggestions()
        }
        .overlay {
            if isLoading {
                ProgressView()
            }
        }
    }

    func loadSuggestions() async {
        isLoading = true
        defer { isLoading = false }

        let session = LanguageModelSession()
        do {
            suggestions = try await session.respond(
                to: "Suggest 5 productivity tasks for a software developer",
                returning: [TaskSuggestion].self
            )
        } catch {
            print("Error: \(error)")
        }
    }
}
```

---

## Best Practices

### 1. Check Availability

```swift
guard LanguageModelSession.isAvailable else {
    // Provide alternative experience
    return
}
```

### 2. Use Structured Output for Reliability

```swift
// GOOD: Type-safe structured output
@Generable
struct Analysis {
    var sentiment: Sentiment
    var confidence: Double
}

let result: Analysis = try await session.respond(to: input)

// AVOID: Parsing free-form text
let text = try await session.respond(to: input)
// Then trying to parse the text...
```

### 3. Stream for Long Responses

```swift
// GOOD: Stream for better UX
for try await partial in session.streamResponse(to: longPrompt) {
    updateUI(partial.content)
}

// AVOID: Blocking wait for long responses
let response = try await session.respond(to: longPrompt)
```

### 4. Handle Errors Gracefully

```swift
do {
    let response = try await session.respond(to: prompt)
} catch {
    // Always have a fallback
    showFallbackContent()
}
```

### 5. Respect User Privacy

```swift
// Don't log or transmit user queries
// Foundation Models runs entirely on-device for privacy
```

---

## Official Resources

- [Foundation Models Documentation](https://developer.apple.com/documentation/FoundationModels)
- [WWDC25: Meet the Foundation Models framework](https://developer.apple.com/videos/play/wwdc2025/286/)
- [WWDC25: Deep dive into Foundation Models](https://developer.apple.com/videos/play/wwdc2025/301/)
- [WWDC25: Code-along: Bring on-device AI to your app](https://developer.apple.com/videos/play/wwdc2025/259/)
