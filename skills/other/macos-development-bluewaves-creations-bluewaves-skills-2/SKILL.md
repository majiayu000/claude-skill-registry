---
name: macos-development
description: macOS Tahoe development patterns including window management, menu bars, NSWindow integration, Mac Catalyst, status bar items, document-based apps, and macOS-specific SwiftUI modifiers. Use when user asks about macOS development, window management, menu bar, status items, Mac Catalyst, document apps, or macOS-specific patterns.
allowed-tools: Bash, Read, Write, Edit
license: MIT
compatibility: Xcode 26+ with Swift 6 toolchain on macOS
---

# macOS Development Patterns

Comprehensive guide to macOS Tahoe development, window management, menu bars, document-based apps, and macOS-specific SwiftUI patterns.

## Prerequisites

- macOS Tahoe (macOS 26) or later
- Xcode 26+

---

## Window Management

### Window Styles

```swift
import SwiftUI

@main
struct MyMacApp: App {
    var body: some Scene {
        // Standard window
        WindowGroup {
            ContentView()
        }
        .windowStyle(.automatic)  // Default

        // Hideable title bar (content extends to top)
        WindowGroup("Editor", id: "editor") {
            EditorView()
        }
        .windowStyle(.hiddenTitleBar)

        // Plain window (no chrome)
        WindowGroup("Floating", id: "floating") {
            FloatingView()
        }
        .windowStyle(.plain)
    }
}
```

### Window Size and Position

```swift
WindowGroup {
    ContentView()
}
// Default size
.defaultSize(width: 800, height: 600)

// Size constraints
.windowResizability(.contentSize)  // Fit content
.windowResizability(.contentMinSize)  // Min = content, resizable larger
.windowResizability(.automatic)  // System decides

// Fixed size window
.windowResizability(.contentSize)
.frame(width: 400, height: 300)

// Position
.defaultPosition(.center)
.defaultPosition(.topLeading)
.defaultPosition(UnitPoint(x: 0.75, y: 0.25))
```

### Multiple Windows

```swift
@main
struct MultiWindowApp: App {
    @Environment(\.openWindow) private var openWindow

    var body: some Scene {
        // Main window
        WindowGroup {
            MainView()
                .toolbar {
                    Button("New Editor") {
                        openWindow(id: "editor")
                    }
                }
        }
        .commands {
            CommandGroup(after: .newItem) {
                Button("New Editor Window") {
                    openWindow(id: "editor")
                }
                .keyboardShortcut("e", modifiers: [.command, .shift])
            }
        }

        // Secondary window type
        WindowGroup("Editor", id: "editor") {
            EditorView()
        }
        .defaultSize(width: 600, height: 400)

        // Single instance window
        Window("Settings", id: "settings") {
            SettingsView()
        }
        .keyboardShortcut(",", modifiers: .command)
        .defaultSize(width: 500, height: 400)
    }
}
```

### Window with Data

```swift
// Define window value type
struct DocumentInfo: Codable, Hashable {
    let id: UUID
    let title: String
}

@main
struct DocumentApp: App {
    var body: some Scene {
        WindowGroup(for: DocumentInfo.self) { $document in
            if let document {
                DocumentView(info: document)
            }
        }
    }
}

// Open with specific data
struct ContentView: View {
    @Environment(\.openWindow) private var openWindow

    var body: some View {
        Button("Open Document") {
            openWindow(value: DocumentInfo(id: UUID(), title: "New Doc"))
        }
    }
}
```

### NSWindow Integration

```swift
import AppKit
import SwiftUI

struct WindowAccessor: NSViewRepresentable {
    let callback: (NSWindow?) -> Void

    func makeNSView(context: Context) -> NSView {
        let view = NSView()
        DispatchQueue.main.async {
            callback(view.window)
        }
        return view
    }

    func updateNSView(_ nsView: NSView, context: Context) {}
}

// Usage
struct ContentView: View {
    @State private var window: NSWindow?

    var body: some View {
        Text("Hello")
            .background(WindowAccessor { window in
                self.window = window

                // Customize window
                window?.titlebarAppearsTransparent = true
                window?.titleVisibility = .hidden
                window?.styleMask.insert(.fullSizeContentView)
                window?.isMovableByWindowBackground = true
            })
    }
}
```

---

## Menu Bar

### App Menu Customization

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .commands {
            // Replace existing menu group
            CommandGroup(replacing: .newItem) {
                Button("New Document") {
                    // Create new document
                }
                .keyboardShortcut("n")

                Button("New from Template...") {
                    // Show template picker
                }
                .keyboardShortcut("n", modifiers: [.command, .shift])
            }

            // Add to existing menu
            CommandGroup(after: .sidebar) {
                Divider()
                Button("Toggle Inspector") {
                    // Toggle inspector
                }
                .keyboardShortcut("i", modifiers: [.command, .option])
            }

            // Custom menu
            CommandMenu("Canvas") {
                Button("Zoom In") { }
                    .keyboardShortcut("+")
                Button("Zoom Out") { }
                    .keyboardShortcut("-")
                Divider()
                Button("Fit to Window") { }
                    .keyboardShortcut("0")
            }
        }
    }
}
```

### Context Menus (Right-Click)

```swift
struct ItemView: View {
    let item: Item
    @State private var isRenaming = false

    var body: some View {
        Text(item.title)
            .contextMenu {
                Button("Open") {
                    // Open action
                }

                Button("Open in New Window") {
                    // Open in new window
                }

                Divider()

                Button("Rename") {
                    isRenaming = true
                }

                Button("Duplicate") {
                    // Duplicate action
                }

                Divider()

                Button("Delete", role: .destructive) {
                    // Delete action
                }
            }
    }
}
```

### Menu Bar Extra (Status Bar Items)

```swift
@main
struct StatusBarApp: App {
    var body: some Scene {
        // Optional main window
        WindowGroup {
            ContentView()
        }

        // Status bar item
        MenuBarExtra("My App", systemImage: "star.fill") {
            Button("Show Dashboard") {
                // Open main window
            }
            .keyboardShortcut("d")

            Divider()

            Menu("Recent Items") {
                ForEach(recentItems) { item in
                    Button(item.name) {
                        // Open item
                    }
                }
            }

            Divider()

            Button("Preferences...") {
                // Open preferences
            }
            .keyboardShortcut(",")

            Button("Quit") {
                NSApplication.shared.terminate(nil)
            }
            .keyboardShortcut("q")
        }
    }

    @State private var recentItems: [RecentItem] = []
}

// Custom status bar view
struct StatusBarApp2: App {
    var body: some Scene {
        MenuBarExtra {
            StatusBarPopover()
        } label: {
            HStack(spacing: 4) {
                Image(systemName: "cpu")
                Text("45%")
                    .font(.caption)
            }
        }
        .menuBarExtraStyle(.window)  // Popover style
    }
}

struct StatusBarPopover: View {
    var body: some View {
        VStack(spacing: 16) {
            Text("System Status")
                .font(.headline)

            // Status content
            StatusRow(title: "CPU", value: "45%")
            StatusRow(title: "Memory", value: "8.2 GB")
            StatusRow(title: "Storage", value: "234 GB")

            Divider()

            Button("Open Activity Monitor") {
                // Open Activity Monitor
            }
        }
        .padding()
        .frame(width: 200)
    }
}
```

---

## Document-Based Apps

### Document Type Definition

```swift
import SwiftUI
import UniformTypeIdentifiers

// Define document type
extension UTType {
    static var myDocument: UTType {
        UTType(exportedAs: "com.mycompany.mydocument")
    }
}

// Document model
struct MyDocument: FileDocument {
    static var readableContentTypes: [UTType] { [.myDocument, .plainText] }
    static var writableContentTypes: [UTType] { [.myDocument] }

    var content: String

    init(content: String = "") {
        self.content = content
    }

    init(configuration: ReadConfiguration) throws {
        guard let data = configuration.file.regularFileContents,
              let string = String(data: data, encoding: .utf8) else {
            throw CocoaError(.fileReadCorruptFile)
        }
        content = string
    }

    func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper {
        let data = content.data(using: .utf8)!
        return FileWrapper(regularFileWithContents: data)
    }
}

// Document-based app
@main
struct DocumentApp: App {
    var body: some Scene {
        DocumentGroup(newDocument: MyDocument()) { file in
            DocumentView(document: file.$document)
        }
        .commands {
            // Document-specific commands
            CommandGroup(after: .saveItem) {
                Button("Export as PDF...") {
                    // Export
                }
                .keyboardShortcut("e", modifiers: [.command, .shift])
            }
        }
    }
}

struct DocumentView: View {
    @Binding var document: MyDocument
    @FocusedValue(\.document) private var focusedDocument

    var body: some View {
        TextEditor(text: $document.content)
            .font(.body.monospaced())
            .focusedValue(\.document, $document)
    }
}
```

### Reference File Documents (Large Files)

```swift
import SwiftUI
import UniformTypeIdentifiers

// For large files, use ReferenceFileDocument
@Observable
class ImageDocument: ReferenceFileDocument {
    static var readableContentTypes: [UTType] { [.png, .jpeg] }
    static var writableContentTypes: [UTType] { [.png] }

    var image: NSImage?
    var annotations: [Annotation] = []

    init() {}

    required init(configuration: ReadConfiguration) throws {
        guard let data = configuration.file.regularFileContents else {
            throw CocoaError(.fileReadCorruptFile)
        }
        image = NSImage(data: data)
    }

    func snapshot(contentType: UTType) throws -> Data {
        guard let image, let data = image.tiffRepresentation else {
            throw CocoaError(.fileWriteUnknown)
        }
        return data
    }

    func fileWrapper(snapshot: Data, configuration: WriteConfiguration) throws -> FileWrapper {
        FileWrapper(regularFileWithContents: snapshot)
    }
}

@main
struct ImageEditorApp: App {
    var body: some Scene {
        DocumentGroup(newDocument: { ImageDocument() }) { file in
            ImageEditorView(document: file.document)
        }
    }
}
```

---

## Mac Catalyst

### Enabling Mac Catalyst

In Xcode: Target → General → Deployment Info → Mac (Mac Catalyst)

### Platform-Specific Code

```swift
struct ContentView: View {
    var body: some View {
        VStack {
            #if targetEnvironment(macCatalyst)
            // Mac Catalyst specific UI
            MacToolbar()
            #else
            // iOS specific UI
            iOSToolbar()
            #endif

            MainContent()
        }
    }
}

// Check at runtime
struct PlatformAwareView: View {
    var body: some View {
        Group {
            if ProcessInfo.processInfo.isMacCatalystApp {
                MacLayout()
            } else {
                iOSLayout()
            }
        }
    }
}
```

### Catalyst-Specific Features

```swift
#if targetEnvironment(macCatalyst)
import AppKit

extension View {
    func configureMacWindow() -> some View {
        self.onAppear {
            guard let windowScene = UIApplication.shared.connectedScenes.first as? UIWindowScene else { return }

            // Window size
            windowScene.sizeRestrictions?.minimumSize = CGSize(width: 800, height: 600)
            windowScene.sizeRestrictions?.maximumSize = CGSize(width: 1920, height: 1080)

            // Title bar
            if let titlebar = windowScene.titlebar {
                titlebar.titleVisibility = .hidden
                titlebar.toolbar = nil
            }
        }
    }
}
#endif
```

### Optimizing for Mac

```swift
struct CatalystOptimizedApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                #if targetEnvironment(macCatalyst)
                .frame(minWidth: 800, minHeight: 600)
                .onAppear(perform: setupMacEnvironment)
                #endif
        }
        #if targetEnvironment(macCatalyst)
        .commands {
            // Mac-specific menu commands
            CommandGroup(replacing: .help) {
                Button("MyApp Help") {
                    // Open help
                }
            }
        }
        #endif
    }

    #if targetEnvironment(macCatalyst)
    private func setupMacEnvironment() {
        // Enable hover effects
        // Configure pointer interactions
        // Set up keyboard shortcuts
    }
    #endif
}

// Pointer/hover support
struct HoverButton: View {
    @State private var isHovered = false

    var body: some View {
        Button("Click Me") { }
            .buttonStyle(.borderedProminent)
            .scaleEffect(isHovered ? 1.05 : 1.0)
            .onHover { hovering in
                withAnimation(.easeInOut(duration: 0.15)) {
                    isHovered = hovering
                }
            }
    }
}
```

---

## macOS-Specific Modifiers

### Toolbar Customization

```swift
struct MacToolbarView: View {
    @State private var searchText = ""

    var body: some View {
        NavigationSplitView {
            Sidebar()
        } detail: {
            DetailView()
        }
        .toolbar {
            // Leading items
            ToolbarItem(placement: .navigation) {
                Button(action: {}) {
                    Image(systemName: "sidebar.left")
                }
            }

            // Principal (center)
            ToolbarItem(placement: .principal) {
                Picker("View", selection: .constant(0)) {
                    Text("Grid").tag(0)
                    Text("List").tag(1)
                }
                .pickerStyle(.segmented)
                .frame(width: 150)
            }

            // Trailing items
            ToolbarItemGroup(placement: .primaryAction) {
                Button(action: {}) {
                    Image(systemName: "plus")
                }

                Button(action: {}) {
                    Image(systemName: "square.and.arrow.up")
                }
            }

            // Search field (trailing)
            ToolbarItem(placement: .automatic) {
                TextField("Search", text: $searchText)
                    .textFieldStyle(.roundedBorder)
                    .frame(width: 200)
            }
        }
        .toolbarBackground(.visible, for: .windowToolbar)
    }
}
```

### Sidebar and Split View

```swift
struct ThreeColumnLayout: View {
    @State private var selectedFolder: Folder?
    @State private var selectedItem: Item?
    @State private var columnVisibility: NavigationSplitViewVisibility = .all

    var body: some View {
        NavigationSplitView(columnVisibility: $columnVisibility) {
            // Sidebar (first column)
            List(folders, selection: $selectedFolder) { folder in
                NavigationLink(value: folder) {
                    Label(folder.name, systemImage: folder.icon)
                }
            }
            .navigationSplitViewColumnWidth(min: 180, ideal: 200, max: 250)

        } content: {
            // Content (second column)
            if let folder = selectedFolder {
                List(folder.items, selection: $selectedItem) { item in
                    NavigationLink(value: item) {
                        ItemRow(item: item)
                    }
                }
            } else {
                ContentUnavailableView("Select a Folder", systemImage: "folder")
            }

        } detail: {
            // Detail (third column)
            if let item = selectedItem {
                ItemDetailView(item: item)
            } else {
                ContentUnavailableView("Select an Item", systemImage: "doc")
            }
        }
        .navigationSplitViewStyle(.balanced)
    }

    @State private var folders: [Folder] = []
}
```

### Settings/Preferences Window

```swift
@main
struct PreferencesApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }

        #if os(macOS)
        Settings {
            SettingsView()
        }
        #endif
    }
}

struct SettingsView: View {
    var body: some View {
        TabView {
            GeneralSettings()
                .tabItem {
                    Label("General", systemImage: "gear")
                }

            AppearanceSettings()
                .tabItem {
                    Label("Appearance", systemImage: "paintbrush")
                }

            AccountSettings()
                .tabItem {
                    Label("Account", systemImage: "person.crop.circle")
                }

            AdvancedSettings()
                .tabItem {
                    Label("Advanced", systemImage: "gearshape.2")
                }
        }
        .frame(width: 450, height: 300)
    }
}

struct GeneralSettings: View {
    @AppStorage("launchAtLogin") private var launchAtLogin = false
    @AppStorage("checkForUpdates") private var checkForUpdates = true

    var body: some View {
        Form {
            Toggle("Launch at Login", isOn: $launchAtLogin)
            Toggle("Check for Updates Automatically", isOn: $checkForUpdates)
        }
        .padding()
    }
}
```

### Inspector Panel

```swift
struct InspectorView: View {
    @State private var showInspector = true
    @State private var selectedItem: Item?

    var body: some View {
        NavigationStack {
            ContentList(selection: $selectedItem)
        }
        .inspector(isPresented: $showInspector) {
            if let item = selectedItem {
                ItemInspector(item: item)
            } else {
                ContentUnavailableView("No Selection", systemImage: "sidebar.right")
            }
        }
        .inspectorColumnWidth(min: 250, ideal: 300, max: 400)
        .toolbar {
            ToolbarItem {
                Button {
                    showInspector.toggle()
                } label: {
                    Image(systemName: "sidebar.right")
                }
            }
        }
    }
}
```

---

## Keyboard Shortcuts

### Custom Keyboard Shortcuts

```swift
struct KeyboardShortcutDemo: View {
    @State private var text = ""

    var body: some View {
        TextEditor(text: $text)
            .toolbar {
                // Toolbar button with shortcut
                Button("Bold") {
                    makeBold()
                }
                .keyboardShortcut("b", modifiers: .command)

                Button("Italic") {
                    makeItalic()
                }
                .keyboardShortcut("i", modifiers: .command)
            }
            // Background keyboard shortcuts
            .background {
                Group {
                    Button("") { duplicateLine() }
                        .keyboardShortcut("d", modifiers: [.command, .shift])

                    Button("") { deleteLine() }
                        .keyboardShortcut(.delete, modifiers: [.command, .shift])
                }
                .frame(width: 0, height: 0)
                .opacity(0)
            }
    }

    private func makeBold() {}
    private func makeItalic() {}
    private func duplicateLine() {}
    private func deleteLine() {}
}
```

### Focus-Based Commands

```swift
struct FocusedDocument: FocusedValueKey {
    typealias Value = Binding<MyDocument>
}

extension FocusedValues {
    var document: Binding<MyDocument>? {
        get { self[FocusedDocument.self] }
        set { self[FocusedDocument.self] = newValue }
    }
}

struct DocumentCommands: Commands {
    @FocusedValue(\.document) var document

    var body: some Commands {
        CommandGroup(after: .textEditing) {
            Button("Word Count") {
                if let doc = document?.wrappedValue {
                    let count = doc.content.split(separator: " ").count
                    print("Words: \(count)")
                }
            }
            .keyboardShortcut("w", modifiers: [.command, .shift])
            .disabled(document == nil)
        }
    }
}
```

---

## Best Practices

### DO

```swift
// ✓ Use native macOS controls
NavigationSplitView { ... }

// ✓ Support keyboard navigation
.focusable()
.onKeyPress(.tab) { ... }

// ✓ Respect system appearance
@Environment(\.colorScheme) var colorScheme

// ✓ Use Settings scene for preferences
Settings { SettingsView() }

// ✓ Support window restoration
.handlesExternalEvents(matching: ["main"])
```

### DON'T

```swift
// ✗ Don't use iOS-only patterns
.navigationBarHidden(true)  // Use .toolbar instead

// ✗ Don't ignore keyboard shortcuts
// Always add for common actions

// ✗ Don't hardcode window sizes
.frame(width: 800, height: 600)  // Use defaultSize instead

// ✗ Don't forget right-click menus
// Add contextMenu to interactive elements
```

---

## Official Resources

- [Mac App Documentation](https://developer.apple.com/documentation/swiftui/building-a-great-mac-app-with-swiftui)
- [Human Interface Guidelines - macOS](https://developer.apple.com/design/human-interface-guidelines/macos)
- [Mac Catalyst Documentation](https://developer.apple.com/documentation/uikit/mac_catalyst)
- [WWDC23: Build programmatic UI with Xcode Previews](https://developer.apple.com/videos/play/wwdc2023/10252/)
