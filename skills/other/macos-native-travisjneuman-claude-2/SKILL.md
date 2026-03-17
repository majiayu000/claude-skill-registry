---
name: macos-native
description: Native macOS development with AppKit, Catalyst, and macOS-specific APIs. Use when building Mac-native apps, menu bar apps, system extensions, or macOS-specific features.
---

# macOS Native Development

Comprehensive guide for building native macOS applications with AppKit and modern macOS APIs.

## Framework Overview

| Framework            | Use Case             | Notes                       |
| -------------------- | -------------------- | --------------------------- |
| **AppKit**           | Traditional Mac apps | Full control, mature        |
| **SwiftUI**          | Modern Mac apps      | Cross-platform, declarative |
| **Catalyst**         | iPad apps on Mac     | Quick port, limitations     |
| **AppKit + SwiftUI** | Hybrid approach      | Best of both worlds         |

---

## AppKit Fundamentals

### Application Structure

```swift
// AppDelegate.swift
import Cocoa

@main
class AppDelegate: NSObject, NSApplicationDelegate {
    var mainWindow: NSWindow?

    func applicationDidFinishLaunching(_ notification: Notification) {
        setupMainWindow()
        setupMainMenu()
    }

    func applicationWillTerminate(_ notification: Notification) {
        // Cleanup
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        return true
    }

    private func setupMainWindow() {
        let contentRect = NSRect(x: 0, y: 0, width: 800, height: 600)
        let styleMask: NSWindow.StyleMask = [
            .titled, .closable, .miniaturizable, .resizable
        ]

        mainWindow = NSWindow(
            contentRect: contentRect,
            styleMask: styleMask,
            backing: .buffered,
            defer: false
        )

        mainWindow?.title = "My Mac App"
        mainWindow?.contentViewController = MainViewController()
        mainWindow?.center()
        mainWindow?.makeKeyAndOrderFront(nil)
    }
}
```

### View Controller

```swift
import Cocoa

class MainViewController: NSViewController {
    private let tableView = NSTableView()
    private let scrollView = NSScrollView()
    private var items: [String] = []

    override func loadView() {
        view = NSView(frame: NSRect(x: 0, y: 0, width: 800, height: 600))
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        loadData()
    }

    private func setupUI() {
        // Setup scroll view
        scrollView.translatesAutoresizingMaskIntoConstraints = false
        scrollView.hasVerticalScroller = true
        scrollView.documentView = tableView
        view.addSubview(scrollView)

        // Setup table view
        let column = NSTableColumn(identifier: NSUserInterfaceItemIdentifier("main"))
        column.title = "Items"
        column.width = 200
        tableView.addTableColumn(column)
        tableView.delegate = self
        tableView.dataSource = self

        // Constraints
        NSLayoutConstraint.activate([
            scrollView.topAnchor.constraint(equalTo: view.topAnchor, constant: 20),
            scrollView.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20),
            scrollView.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -20),
            scrollView.bottomAnchor.constraint(equalTo: view.bottomAnchor, constant: -20),
        ])
    }

    private func loadData() {
        items = ["Item 1", "Item 2", "Item 3"]
        tableView.reloadData()
    }
}

extension MainViewController: NSTableViewDataSource, NSTableViewDelegate {
    func numberOfRows(in tableView: NSTableView) -> Int {
        return items.count
    }

    func tableView(_ tableView: NSTableView, viewFor tableColumn: NSTableColumn?, row: Int) -> NSView? {
        let identifier = NSUserInterfaceItemIdentifier("cell")
        var cell = tableView.makeView(withIdentifier: identifier, owner: nil) as? NSTextField

        if cell == nil {
            cell = NSTextField(labelWithString: "")
            cell?.identifier = identifier
        }

        cell?.stringValue = items[row]
        return cell
    }
}
```

---

## Menu Bar Apps

### Status Item

```swift
import Cocoa

class StatusBarController {
    private var statusItem: NSStatusItem?
    private var popover: NSPopover?

    init() {
        setupStatusItem()
        setupPopover()
    }

    private func setupStatusItem() {
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)

        if let button = statusItem?.button {
            button.image = NSImage(systemSymbolName: "star.fill", accessibilityDescription: "App")
            button.action = #selector(togglePopover)
            button.target = self
        }
    }

    private func setupPopover() {
        popover = NSPopover()
        popover?.contentViewController = PopoverViewController()
        popover?.behavior = .transient
    }

    @objc private func togglePopover() {
        guard let button = statusItem?.button, let popover = popover else { return }

        if popover.isShown {
            popover.performClose(nil)
        } else {
            popover.show(relativeTo: button.bounds, of: button, preferredEdge: .minY)
            NSApp.activate(ignoringOtherApps: true)
        }
    }
}

class PopoverViewController: NSViewController {
    override func loadView() {
        view = NSView(frame: NSRect(x: 0, y: 0, width: 300, height: 200))
    }

    override func viewDidLoad() {
        super.viewDidLoad()

        let label = NSTextField(labelWithString: "Menu Bar App Content")
        label.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(label)

        NSLayoutConstraint.activate([
            label.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            label.centerYAnchor.constraint(equalTo: view.centerYAnchor),
        ])
    }
}
```

### Menu Construction

```swift
func setupMainMenu() {
    let mainMenu = NSMenu()

    // App Menu
    let appMenu = NSMenu()
    let appMenuItem = NSMenuItem()
    appMenuItem.submenu = appMenu

    appMenu.addItem(withTitle: "About My App", action: #selector(NSApplication.orderFrontStandardAboutPanel(_:)), keyEquivalent: "")
    appMenu.addItem(NSMenuItem.separator())
    appMenu.addItem(withTitle: "Preferences...", action: #selector(showPreferences), keyEquivalent: ",")
    appMenu.addItem(NSMenuItem.separator())
    appMenu.addItem(withTitle: "Quit My App", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "q")

    mainMenu.addItem(appMenuItem)

    // File Menu
    let fileMenu = NSMenu(title: "File")
    let fileMenuItem = NSMenuItem()
    fileMenuItem.submenu = fileMenu

    fileMenu.addItem(withTitle: "New", action: #selector(newDocument), keyEquivalent: "n")
    fileMenu.addItem(withTitle: "Open...", action: #selector(openDocument), keyEquivalent: "o")
    fileMenu.addItem(NSMenuItem.separator())
    fileMenu.addItem(withTitle: "Save", action: #selector(saveDocument), keyEquivalent: "s")

    mainMenu.addItem(fileMenuItem)

    // Edit Menu
    let editMenu = NSMenu(title: "Edit")
    let editMenuItem = NSMenuItem()
    editMenuItem.submenu = editMenu

    editMenu.addItem(withTitle: "Undo", action: Selector(("undo:")), keyEquivalent: "z")
    editMenu.addItem(withTitle: "Redo", action: Selector(("redo:")), keyEquivalent: "Z")
    editMenu.addItem(NSMenuItem.separator())
    editMenu.addItem(withTitle: "Cut", action: #selector(NSText.cut(_:)), keyEquivalent: "x")
    editMenu.addItem(withTitle: "Copy", action: #selector(NSText.copy(_:)), keyEquivalent: "c")
    editMenu.addItem(withTitle: "Paste", action: #selector(NSText.paste(_:)), keyEquivalent: "v")

    mainMenu.addItem(editMenuItem)

    NSApp.mainMenu = mainMenu
}
```

---

## Document-Based Apps

### Document Controller

```swift
import Cocoa
import UniformTypeIdentifiers

class MyDocument: NSDocument {
    var content: String = ""

    override class var autosavesInPlace: Bool { true }

    override func makeWindowControllers() {
        let storyboard = NSStoryboard(name: "Main", bundle: nil)
        let windowController = storyboard.instantiateController(
            withIdentifier: "Document Window Controller"
        ) as! NSWindowController
        addWindowController(windowController)
    }

    override func data(ofType typeName: String) throws -> Data {
        guard let data = content.data(using: .utf8) else {
            throw NSError(domain: NSOSStatusErrorDomain, code: unimpErr)
        }
        return data
    }

    override func read(from data: Data, ofType typeName: String) throws {
        guard let content = String(data: data, encoding: .utf8) else {
            throw NSError(domain: NSOSStatusErrorDomain, code: unimpErr)
        }
        self.content = content
    }
}

// Info.plist Document Types
/*
<key>CFBundleDocumentTypes</key>
<array>
    <dict>
        <key>CFBundleTypeName</key>
        <string>My Document</string>
        <key>CFBundleTypeRole</key>
        <string>Editor</string>
        <key>LSHandlerRank</key>
        <string>Owner</string>
        <key>LSItemContentTypes</key>
        <array>
            <string>com.example.mydocument</string>
        </array>
    </dict>
</array>
*/
```

---

## System Integration

### Services

```swift
// Providing a service
class ServiceProvider: NSObject {
    @objc func processText(_ pboard: NSPasteboard, userData: String, error: AutoreleasingUnsafeMutablePointer<NSString?>) {
        guard let text = pboard.string(forType: .string) else { return }

        let processed = text.uppercased()

        pboard.clearContents()
        pboard.setString(processed, forType: .string)
    }
}

// Register in Info.plist
/*
<key>NSServices</key>
<array>
    <dict>
        <key>NSMenuItem</key>
        <dict>
            <key>default</key>
            <string>Process with My App</string>
        </dict>
        <key>NSMessage</key>
        <string>processText</string>
        <key>NSPortName</key>
        <string>MyApp</string>
        <key>NSSendTypes</key>
        <array>
            <string>NSStringPboardType</string>
        </array>
        <key>NSReturnTypes</key>
        <array>
            <string>NSStringPboardType</string>
        </array>
    </dict>
</array>
*/
```

### Drag and Drop

```swift
class DropView: NSView {
    override init(frame frameRect: NSRect) {
        super.init(frame: frameRect)
        registerForDraggedTypes([.fileURL, .string])
    }

    required init?(coder: NSCoder) {
        super.init(coder: coder)
        registerForDraggedTypes([.fileURL, .string])
    }

    override func draggingEntered(_ sender: NSDraggingInfo) -> NSDragOperation {
        return .copy
    }

    override func performDragOperation(_ sender: NSDraggingInfo) -> Bool {
        let pasteboard = sender.draggingPasteboard

        if let urls = pasteboard.readObjects(forClasses: [NSURL.self]) as? [URL] {
            for url in urls {
                handleDroppedFile(url)
            }
            return true
        }

        if let strings = pasteboard.readObjects(forClasses: [NSString.self]) as? [String] {
            for string in strings {
                handleDroppedText(string)
            }
            return true
        }

        return false
    }

    private func handleDroppedFile(_ url: URL) {
        print("Dropped file: \(url)")
    }

    private func handleDroppedText(_ text: String) {
        print("Dropped text: \(text)")
    }
}
```

### Notifications

```swift
import UserNotifications

class NotificationManager {
    static let shared = NotificationManager()

    func requestAuthorization() {
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .sound, .badge]) { granted, error in
            if granted {
                print("Notification permission granted")
            }
        }
    }

    func scheduleNotification(title: String, body: String, delay: TimeInterval = 5) {
        let content = UNMutableNotificationContent()
        content.title = title
        content.body = body
        content.sound = .default

        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: delay, repeats: false)
        let request = UNNotificationRequest(
            identifier: UUID().uuidString,
            content: content,
            trigger: trigger
        )

        UNUserNotificationCenter.current().add(request)
    }
}
```

---

## Sandboxing & Entitlements

### Common Entitlements

```xml
<!-- MyApp.entitlements -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- App Sandbox -->
    <key>com.apple.security.app-sandbox</key>
    <true/>

    <!-- Network -->
    <key>com.apple.security.network.client</key>
    <true/>
    <key>com.apple.security.network.server</key>
    <true/>

    <!-- File Access -->
    <key>com.apple.security.files.user-selected.read-write</key>
    <true/>
    <key>com.apple.security.files.downloads.read-write</key>
    <true/>

    <!-- Hardware -->
    <key>com.apple.security.device.camera</key>
    <true/>
    <key>com.apple.security.device.microphone</key>
    <true/>

    <!-- Hardened Runtime -->
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
</dict>
</plist>
```

### Security-Scoped Bookmarks

```swift
class BookmarkManager {
    private let bookmarksKey = "securityScopedBookmarks"

    func saveBookmark(for url: URL) throws {
        let bookmarkData = try url.bookmarkData(
            options: .withSecurityScope,
            includingResourceValuesForKeys: nil,
            relativeTo: nil
        )

        var bookmarks = UserDefaults.standard.dictionary(forKey: bookmarksKey) ?? [:]
        bookmarks[url.path] = bookmarkData
        UserDefaults.standard.set(bookmarks, forKey: bookmarksKey)
    }

    func resolveBookmark(for path: String) -> URL? {
        guard let bookmarks = UserDefaults.standard.dictionary(forKey: bookmarksKey),
              let bookmarkData = bookmarks[path] as? Data else {
            return nil
        }

        var isStale = false
        guard let url = try? URL(
            resolvingBookmarkData: bookmarkData,
            options: .withSecurityScope,
            relativeTo: nil,
            bookmarkDataIsStale: &isStale
        ) else {
            return nil
        }

        if isStale {
            try? saveBookmark(for: url)
        }

        return url
    }

    func accessSecurityScopedResource(_ url: URL, action: (URL) throws -> Void) rethrows {
        guard url.startAccessingSecurityScopedResource() else {
            return
        }
        defer { url.stopAccessingSecurityScopedResource() }
        try action(url)
    }
}
```

---

## Checklist

### Mac App Store Submission

- [ ] App Sandbox enabled
- [ ] Hardened Runtime enabled
- [ ] All entitlements justified
- [ ] Privacy descriptions in Info.plist
- [ ] App icon (all sizes)
- [ ] Screenshots for App Store
- [ ] No private API usage

### Best Practices

- [ ] Support keyboard navigation
- [ ] Respect system appearance (dark/light)
- [ ] Support Full Screen
- [ ] Handle window restoration
- [ ] Implement proper undo/redo
- [ ] Support standard keyboard shortcuts
