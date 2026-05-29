---
name: transferable-sharing
description: Transferable protocol for drag and drop, copy/paste, ShareLink, and data transfer. Use when user asks about sharing, drag and drop, copy paste, ShareLink, Transferable, or clipboard operations.
allowed-tools: Bash, Read, Write, Edit
---

# Transferable and Sharing

Comprehensive guide to the Transferable protocol for drag and drop, copy/paste, ShareLink, and cross-app data transfer in SwiftUI.

## Prerequisites

- iOS 16+ for Transferable (iOS 26 recommended)
- Xcode 26+

---

## Transferable Protocol

### Overview

`Transferable` is Swift's declarative way to make types shareable across apps and system features:
- Drag and drop
- Copy/paste
- Share sheets
- Universal clipboard

### Built-in Conformances

```swift
// Already Transferable
String.self
Data.self
URL.self
Image.self
AttributedString.self
```

### Basic Conformance

```swift
import CoreTransferable

struct Note: Transferable {
    var id: UUID
    var title: String
    var content: String

    static var transferRepresentation: some TransferRepresentation {
        CodableRepresentation(contentType: .note)
    }
}

// Define custom UTType
import UniformTypeIdentifiers

extension UTType {
    static var note: UTType {
        UTType(exportedAs: "com.yourapp.note")
    }
}
```

### Info.plist UTType Declaration

```xml
<key>UTExportedTypeDeclarations</key>
<array>
    <dict>
        <key>UTTypeConformsTo</key>
        <array>
            <string>public.data</string>
            <string>public.content</string>
        </array>
        <key>UTTypeDescription</key>
        <string>Note Document</string>
        <key>UTTypeIdentifier</key>
        <string>com.yourapp.note</string>
        <key>UTTypeTagSpecification</key>
        <dict>
            <key>public.filename-extension</key>
            <array>
                <string>note</string>
            </array>
        </dict>
    </dict>
</array>
```

---

## Transfer Representations

### CodableRepresentation

For Codable types:

```swift
struct Task: Codable, Transferable {
    var id: UUID
    var title: String
    var isComplete: Bool

    static var transferRepresentation: some TransferRepresentation {
        CodableRepresentation(contentType: .task)
    }
}
```

### DataRepresentation

For raw data conversion:

```swift
struct ImageItem: Transferable {
    var imageData: Data

    static var transferRepresentation: some TransferRepresentation {
        DataRepresentation(contentType: .png) { item in
            item.imageData
        } importing: { data in
            ImageItem(imageData: data)
        }
    }
}
```

### FileRepresentation

For file-based transfer:

```swift
struct Document: Transferable {
    var url: URL

    static var transferRepresentation: some TransferRepresentation {
        FileRepresentation(contentType: .pdf) { document in
            SentTransferredFile(document.url)
        } importing: { received in
            let destination = FileManager.default.temporaryDirectory
                .appendingPathComponent(received.file.lastPathComponent)
            try FileManager.default.copyItem(at: received.file, to: destination)
            return Document(url: destination)
        }
    }
}
```

### ProxyRepresentation

Export as another type:

```swift
struct Note: Transferable {
    var title: String
    var content: String

    static var transferRepresentation: some TransferRepresentation {
        // Primary: full note data
        CodableRepresentation(contentType: .note)

        // Fallback: plain text
        ProxyRepresentation(exporting: \.plainText)
    }

    var plainText: String {
        "\(title)\n\n\(content)"
    }
}
```

---

## Multiple Representations

### Order Matters

```swift
struct RichContent: Transferable {
    var title: String
    var htmlContent: String
    var plainContent: String

    static var transferRepresentation: some TransferRepresentation {
        // Most specific first
        CodableRepresentation(contentType: .richContent)

        // HTML fallback
        DataRepresentation(contentType: .html) { content in
            content.htmlContent.data(using: .utf8)!
        } importing: { data in
            RichContent(
                title: "Imported",
                htmlContent: String(data: data, encoding: .utf8) ?? "",
                plainContent: ""
            )
        }

        // Plain text fallback
        ProxyRepresentation(exporting: \.plainContent)
    }
}
```

### Conditional Representations

```swift
struct MediaItem: Transferable {
    var imageData: Data?
    var videoURL: URL?

    static var transferRepresentation: some TransferRepresentation {
        DataRepresentation(contentType: .png) { item in
            guard let data = item.imageData else {
                throw TransferError.noImageData
            }
            return data
        } importing: { data in
            MediaItem(imageData: data, videoURL: nil)
        }

        FileRepresentation(contentType: .movie) { item in
            guard let url = item.videoURL else {
                throw TransferError.noVideoURL
            }
            return SentTransferredFile(url)
        } importing: { received in
            MediaItem(imageData: nil, videoURL: received.file)
        }
    }
}
```

---

## ShareLink

### Basic ShareLink

```swift
struct ContentView: View {
    let note: Note

    var body: some View {
        ShareLink(item: note)
    }
}
```

### Custom Label

```swift
ShareLink(item: note) {
    Label("Share Note", systemImage: "square.and.arrow.up")
}
```

### With Preview

```swift
ShareLink(
    item: note,
    preview: SharePreview(
        note.title,
        image: Image(systemName: "doc.text")
    )
)
```

### Sharing URL

```swift
ShareLink(
    item: URL(string: "https://yourapp.com/note/123")!,
    subject: Text("Check out this note"),
    message: Text("I thought you might find this interesting")
)
```

### Sharing Image

```swift
struct PhotoView: View {
    let image: Image

    var body: some View {
        image
            .contextMenu {
                ShareLink(
                    item: image,
                    preview: SharePreview("Photo", image: image)
                )
            }
    }
}
```

### Multiple Items

```swift
struct NotesListView: View {
    @State private var selectedNotes: Set<Note.ID> = []
    let notes: [Note]

    var body: some View {
        List(notes, selection: $selectedNotes) { note in
            Text(note.title)
        }
        .toolbar {
            ShareLink(
                items: notes.filter { selectedNotes.contains($0.id) }
            ) { note in
                SharePreview(note.title)
            }
        }
    }
}
```

---

## Drag and Drop

### Draggable

```swift
struct DraggableNoteView: View {
    let note: Note

    var body: some View {
        VStack {
            Text(note.title)
                .font(.headline)
            Text(note.content)
                .font(.body)
        }
        .draggable(note)
    }
}
```

### Drop Destination

```swift
struct NoteDropZone: View {
    @State private var droppedNotes: [Note] = []

    var body: some View {
        VStack {
            Text("Drop notes here")
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .background(Color.gray.opacity(0.2))
        }
        .dropDestination(for: Note.self) { items, location in
            droppedNotes.append(contentsOf: items)
            return true
        } isTargeted: { isTargeted in
            // Visual feedback
        }
    }
}
```

### Drop with Position

```swift
struct CanvasView: View {
    @State private var items: [(Note, CGPoint)] = []

    var body: some View {
        ZStack {
            ForEach(items, id: \.0.id) { item, position in
                NoteCard(note: item)
                    .position(position)
            }
        }
        .dropDestination(for: Note.self) { notes, location in
            for note in notes {
                items.append((note, location))
            }
            return true
        }
    }
}
```

### Drag Preview

```swift
Text(note.title)
    .draggable(note) {
        // Custom drag preview
        VStack {
            Image(systemName: "doc.text")
                .font(.largeTitle)
            Text(note.title)
        }
        .padding()
        .background(.regularMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 8))
    }
```

### List Reordering

```swift
struct ReorderableList: View {
    @State private var items = ["Item 1", "Item 2", "Item 3"]

    var body: some View {
        List {
            ForEach(items, id: \.self) { item in
                Text(item)
            }
            .onMove { from, to in
                items.move(fromOffsets: from, toOffset: to)
            }
        }
    }
}
```

---

## Copy and Paste

### Copyable

```swift
struct CopyableText: View {
    let text: String

    var body: some View {
        Text(text)
            .textSelection(.enabled)  // Built-in copy
    }
}

// Or with custom type
struct NoteCard: View {
    let note: Note

    var body: some View {
        VStack {
            Text(note.title)
            Text(note.content)
        }
        .contextMenu {
            Button {
                UIPasteboard.general.string = note.plainText
            } label: {
                Label("Copy", systemImage: "doc.on.doc")
            }
        }
    }
}
```

### PasteButton

```swift
struct PasteDestination: View {
    @State private var pastedNote: Note?

    var body: some View {
        VStack {
            if let note = pastedNote {
                NoteCard(note: note)
            } else {
                Text("No note pasted")
            }

            PasteButton(payloadType: Note.self) { notes in
                pastedNote = notes.first
            }
        }
    }
}
```

### Pasteable Modifier

```swift
struct NoteEditor: View {
    @State private var content = ""

    var body: some View {
        TextEditor(text: $content)
            .pasteDestination(for: String.self) { strings in
                content += strings.joined(separator: "\n")
            }
    }
}
```

---

## Exportable

### File Exporter

```swift
struct DocumentView: View {
    @State private var showExporter = false
    let document: TextDocument

    var body: some View {
        Button("Export") {
            showExporter = true
        }
        .fileExporter(
            isPresented: $showExporter,
            document: document,
            contentType: .plainText,
            defaultFilename: "document.txt"
        ) { result in
            switch result {
            case .success(let url):
                print("Exported to: \(url)")
            case .failure(let error):
                print("Export failed: \(error)")
            }
        }
    }
}

struct TextDocument: FileDocument {
    static var readableContentTypes: [UTType] { [.plainText] }

    var text: String

    init(text: String = "") {
        self.text = text
    }

    init(configuration: ReadConfiguration) throws {
        if let data = configuration.file.regularFileContents {
            text = String(data: data, encoding: .utf8) ?? ""
        } else {
            text = ""
        }
    }

    func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper {
        FileWrapper(regularFileWithContents: text.data(using: .utf8)!)
    }
}
```

### File Importer

```swift
struct ImporterView: View {
    @State private var showImporter = false
    @State private var importedContent = ""

    var body: some View {
        VStack {
            Text(importedContent)

            Button("Import") {
                showImporter = true
            }
        }
        .fileImporter(
            isPresented: $showImporter,
            allowedContentTypes: [.plainText],
            allowsMultipleSelection: false
        ) { result in
            switch result {
            case .success(let urls):
                guard let url = urls.first else { return }
                if url.startAccessingSecurityScopedResource() {
                    defer { url.stopAccessingSecurityScopedResource() }
                    importedContent = (try? String(contentsOf: url)) ?? ""
                }
            case .failure(let error):
                print("Import failed: \(error)")
            }
        }
    }
}
```

---

## Universal Clipboard

### Automatic with Transferable

When your type conforms to `Transferable`, it automatically works with Universal Clipboard across Apple devices with the same iCloud account.

```swift
// Copy on Mac
let note = Note(title: "Test", content: "Content")
NSPasteboard.general.writeObjects([note])

// Paste on iPhone
let notes = UIPasteboard.general.itemProviders
    .compactMap { try? await $0.loadTransferable(type: Note.self) }
```

### Handoff Integration

```swift
struct NoteDetailView: View {
    let note: Note

    var body: some View {
        VStack {
            Text(note.title)
            Text(note.content)
        }
        .userActivity("com.yourapp.viewNote") { activity in
            activity.isEligibleForHandoff = true
            activity.userInfo = ["noteId": note.id.uuidString]
        }
    }
}
```

---

## Best Practices

### 1. Order Representations by Specificity

```swift
static var transferRepresentation: some TransferRepresentation {
    // Most specific (native format)
    CodableRepresentation(contentType: .myCustomType)

    // Rich fallback
    DataRepresentation(contentType: .rtf) { ... }

    // Universal fallback
    ProxyRepresentation(exporting: \.plainText)
}
```

### 2. Provide Good Previews

```swift
ShareLink(
    item: photo,
    preview: SharePreview(
        photo.title,
        image: photo.thumbnail,  // Use thumbnail, not full image
        icon: Image(systemName: "photo")
    )
)
```

### 3. Handle Errors Gracefully

```swift
.dropDestination(for: Note.self) { items, location in
    do {
        try processDroppedItems(items)
        return true
    } catch {
        showError(error)
        return false
    }
}
```

### 4. Visual Drop Feedback

```swift
@State private var isTargeted = false

VStack { ... }
    .background(isTargeted ? Color.accentColor.opacity(0.2) : Color.clear)
    .dropDestination(for: Note.self) { items, location in
        // Handle drop
        return true
    } isTargeted: { targeted in
        withAnimation {
            isTargeted = targeted
        }
    }
```

### 5. Support Multiple Types

```swift
.dropDestination(for: String.self) { strings, _ in
    handleText(strings)
    return true
}
.dropDestination(for: URL.self) { urls, _ in
    handleURLs(urls)
    return true
}
.dropDestination(for: Data.self) { dataItems, _ in
    handleData(dataItems)
    return true
}
```

---

## Official Resources

- [Transferable Documentation](https://developer.apple.com/documentation/coretransferable/transferable)
- [ShareLink Documentation](https://developer.apple.com/documentation/swiftui/sharelink)
- [WWDC22: Meet Transferable](https://developer.apple.com/videos/play/wwdc2022/10062/)
- [Drag and Drop Documentation](https://developer.apple.com/documentation/swiftui/view/draggable(_:preview:))
