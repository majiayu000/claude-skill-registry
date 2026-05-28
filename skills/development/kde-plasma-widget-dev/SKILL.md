---
name: kde-plasma-widget-dev
description: This skill should be used when developing, debugging, or fixing KDE Plasma 6 widgets (plasmoids). Triggers on QML widget issues, compactRepresentation not showing, system tray integration, Kirigami.Icon usage, plasmoidviewer testing, and Plasma 6 widget development. Covers common issues like emoji not rendering, widget not appearing in panel, and proper imports for Plasma 6.
---

# KDE Plasma 6 Widget Development

Comprehensive skill for developing and debugging KDE Plasma 6 widgets (plasmoids).

## When to Use

- Developing new KDE Plasma 6 widgets
- Debugging widget display issues (empty space, no icon, not rendering)
- System tray integration problems
- QML syntax and import errors for Plasma 6
- Widget not appearing in panel or "Add Widgets" menu
- Emoji/text not rendering in compactRepresentation

## Plasma 6 Required Structure

### File Structure
```
widget-name/
├── metadata.json           # Widget metadata (REQUIRED)
└── contents/
    ├── ui/
    │   ├── main.qml       # Main widget (REQUIRED)
    │   └── configGeneral.qml  # Settings UI (optional)
    └── config/
        ├── main.xml       # Config schema (optional)
        └── config.qml     # Config categories (optional)
```

### metadata.json (REQUIRED)
```json
{
    "KPlugin": {
        "Authors": [{"Email": "dev@example.com", "Name": "Developer"}],
        "Category": "Utilities",
        "Description": "Widget description",
        "EnabledByDefault": true,
        "Icon": "chronometer",
        "Id": "com.example.widget",
        "Name": "Widget Name",
        "Version": "1.0.0"
    },
    "X-Plasma-API-Minimum-Version": "6.0",
    "KPackageStructure": "Plasma/Applet"
}
```

### For System Tray Placement (optional)
Add these to metadata.json to appear in system tray area:
```json
{
    "X-Plasma-NotificationArea": "true",
    "X-Plasma-NotificationAreaCategory": "ApplicationStatus"
}
```

Categories: `ApplicationStatus`, `Communications`, `Hardware`, `SystemServices`

## Plasma 6 Imports (CRITICAL)

```qml
import QtQuick
import QtQuick.Layouts
import org.kde.plasma.plasmoid
import org.kde.plasma.core as PlasmaCore
import org.kde.plasma.components as PlasmaComponents
import org.kde.kirigami as Kirigami
```

### Import Changes from Plasma 5 to 6

| Plasma 5 | Plasma 6 |
|----------|----------|
| `org.kde.plasma.core 2.0` | `org.kde.plasma.core` |
| `org.kde.plasma.plasmoid 2.0` | `org.kde.plasma.plasmoid` |
| `PlasmaCore.Theme` | `Kirigami.Theme` |
| `PlasmaCore.Units` | `Kirigami.Units` |
| `PlasmaCore.IconItem` | `Kirigami.Icon` |
| `Item` (root) | `PlasmoidItem` (root) |

## Basic Widget Template

```qml
import QtQuick
import QtQuick.Layouts
import org.kde.plasma.plasmoid
import org.kde.plasma.core as PlasmaCore
import org.kde.plasma.components as PlasmaComponents
import org.kde.kirigami as Kirigami

PlasmoidItem {
    id: root

    // Compact view (panel/taskbar)
    compactRepresentation: MouseArea {
        Layout.minimumWidth: row.implicitWidth + Kirigami.Units.smallSpacing * 2
        Layout.minimumHeight: Kirigami.Units.iconSizes.medium

        implicitWidth: Layout.minimumWidth
        implicitHeight: Layout.minimumHeight

        hoverEnabled: true
        property bool wasExpanded: false
        onPressed: wasExpanded = root.expanded
        onClicked: root.expanded = !wasExpanded

        RowLayout {
            id: row
            anchors.centerIn: parent
            spacing: Kirigami.Units.smallSpacing

            Kirigami.Icon {
                source: "chronometer"
                Layout.preferredWidth: Kirigami.Units.iconSizes.small
                Layout.preferredHeight: Kirigami.Units.iconSizes.small
            }

            PlasmaComponents.Label {
                text: "25:00"
                font.family: "monospace"
            }
        }
    }

    // Popup view
    fullRepresentation: Item {
        Layout.preferredWidth: 300
        Layout.preferredHeight: 400

        // Popup content here
    }
}
```

## Common Issues & Solutions

### Issue 1: Widget Shows Empty Space (No Icon/Text)

**Cause**: Emoji characters don't render in Plasma widgets.

**Solution**: Use `Kirigami.Icon` with system icon names instead of emoji:

```qml
// WRONG - emoji won't render
PlasmaComponents.Label {
    text: "🍅"  // Will show blank
}

// CORRECT - use system icons
Kirigami.Icon {
    source: "chronometer"           // Timer icon
    source: "appointment-soon"      // Clock/appointment
    source: "preferences-desktop-screensaver"  // Break/rest
    Layout.preferredWidth: Kirigami.Units.iconSizes.small
    Layout.preferredHeight: Kirigami.Units.iconSizes.small
}
```

### Issue 2: Widget Not Appearing in Panel

**Causes**:
1. Missing `Layout.minimumWidth`/`Layout.minimumHeight`
2. Missing `implicitWidth`/`implicitHeight`
3. Root element not `PlasmoidItem`

**Solution**:
```qml
compactRepresentation: MouseArea {
    // REQUIRED for panel display
    Layout.minimumWidth: content.implicitWidth + Kirigami.Units.smallSpacing * 2
    Layout.minimumHeight: Kirigami.Units.iconSizes.medium

    implicitWidth: Layout.minimumWidth
    implicitHeight: Layout.minimumHeight

    // ... content
}
```

### Issue 3: Widget Not in "Add Widgets" Menu

**Solutions**:
1. Verify `metadata.json` has `"X-Plasma-API-Minimum-Version": "6.0"`
2. Refresh KDE cache: `kbuildsycoca6`
3. Restart Plasma: `plasmashell --replace &`
4. Check widget is installed at: `~/.local/share/plasma/plasmoids/com.widget.id/`

### Issue 4: Click Doesn't Open Popup

**Cause**: Missing or incorrect MouseArea setup.

**Solution**: Follow KDE's official pattern:
```qml
compactRepresentation: MouseArea {
    hoverEnabled: true
    property bool wasExpanded: false
    onPressed: wasExpanded = root.expanded
    onClicked: root.expanded = !wasExpanded

    // Content inside...
}
```

### Issue 5: Colors Don't Match Theme

**Solution**: Use Kirigami.Theme colors:
```qml
PlasmaComponents.Label {
    color: Kirigami.Theme.textColor        // Normal text
    color: Kirigami.Theme.highlightColor   // Accent
    color: Kirigami.Theme.disabledTextColor // Muted
}
```

## Testing Commands

### Test with plasmoidviewer
```bash
cd widget-directory
plasmoidviewer -a package
```

### Install widget
```bash
mkdir -p ~/.local/share/plasma/plasmoids
cp -r package ~/.local/share/plasma/plasmoids/com.widget.id
```

### Refresh KDE cache
```bash
kbuildsycoca6
```

### Restart Plasma
```bash
plasmashell --replace &
```

### Check for QML errors
```bash
timeout 5 plasmoidviewer -a package 2>&1 | grep -i "error\|qml"
```

## Common Icon Names

| Purpose | Icon Name |
|---------|-----------|
| Timer/Clock | `chronometer`, `appointment-soon` |
| Play | `media-playback-start` |
| Pause | `media-playback-pause` |
| Stop | `media-playback-stop` |
| Skip | `media-skip-forward` |
| Refresh | `view-refresh` |
| Settings | `configure` |
| Check/Done | `checkmark`, `dialog-ok` |
| Error | `dialog-error` |
| Warning | `dialog-warning` |
| Info | `dialog-information` |

## Panel Form Factor Handling

```qml
compactRepresentation: Item {
    readonly property bool isVertical: Plasmoid.formFactor === PlasmaCore.Types.Vertical

    Layout.minimumWidth: isVertical ? 0 : content.implicitWidth
    Layout.minimumHeight: isVertical ? content.implicitHeight : 0

    // Adapt layout based on orientation
}
```

## Configuration Integration

### config/main.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<kcfg xmlns="http://www.kde.org/standards/kcfg/1.0">
    <kcfgfile name=""/>
    <group name="General">
        <entry name="myOption" type="Int">
            <default>25</default>
        </entry>
    </group>
</kcfg>
```

### Access in QML
```qml
PlasmoidItem {
    readonly property int myValue: plasmoid.configuration.myOption
}
```

## HTTP Requests in QML

```qml
function fetchData() {
    var xhr = new XMLHttpRequest()
    xhr.open("GET", "https://api.example.com/data", true)
    xhr.setRequestHeader("Content-Type", "application/json")

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var data = JSON.parse(xhr.responseText)
                // Handle data
            } else {
                console.error("Request failed:", xhr.status)
            }
        }
    }
    xhr.send()
}
```

## Sources

- [KDE Developer Docs - Widget Properties](https://develop.kde.org/docs/plasma/widget/properties/)
- [KDE Developer Docs - Porting to KF6](https://develop.kde.org/docs/plasma/widget/porting_kf6/)
- [Zren's Plasma Widget Tutorial](https://zren.github.io/kde/docs/widget/)
- [KDE plasma-desktop DefaultCompactRepresentation](https://github.com/KDE/plasma-desktop/blob/master/desktoppackage/contents/applet/DefaultCompactRepresentation.qml)
