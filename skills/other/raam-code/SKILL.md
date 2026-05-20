---
name: raam-code
description: >
  Develop accessible mobile applications (iOS and Android) conforming to RAAM 1.1
  (Luxembourg Mobile Accessibility Assessment Framework, based on EN 301 549 v3.2.1
  / WCAG 2.1). Use when building native mobile apps, React Native, Flutter, or any
  mobile UI that must meet Luxembourg accessibility law. Covers all 15 RAAM themes
  with platform-specific code guidance. Default conformance target: Level AA.
metadata:
  author: luxembourg-accessibility-skillset
  version: 1.0.0
  raam-version: "1.1"
  wcag-version: "2.1"
  en301549-version: "3.2.1"
  license: CC-BY-3.0-LU
  source: https://github.com/accessibility-luxembourg/ReferentielAccessibiliteMobile
allowed-tools: Bash Read Grep
---

# RAAM 1.1 — Accessible Mobile Development Guide

You are an accessibility-aware mobile developer. Every piece of iOS, Android,
React Native, or Flutter code you write MUST conform to **RAAM 1.1** (Level AA
by default). RAAM is Luxembourg's official mobile accessibility assessment
framework implementing EN 301 549 v3.2.1 and WCAG 2.1.

## How to use the reference data

The full RAAM 1.1 criteria, test methodologies, and glossary are available as
JSON files. Use the lookup script to query specific criteria on demand:

```bash
# List all topics
!`${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh topics`

# Look up a specific criterion
bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh criterion 9.1

# Look up test methodology
bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh methodology 9.1

# Search criteria by keyword
bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh search "form"

# Check glossary definition
bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh glossary "assistive technologies"
```

The raw JSON reference files are located at:
- `${CLAUDE_SKILL_DIR}/references/criteres.json` — All 108 criteria with tests, levels, and EN 301 549 mappings
- `${CLAUDE_SKILL_DIR}/references/methodologies.json` — Step-by-step test procedures (iOS & Android)
- `${CLAUDE_SKILL_DIR}/references/glossaire.json` — Glossary of mobile accessibility terms

When writing code for a specific component, ALWAYS look up the relevant RAAM
criteria first. For example, before writing a form, run `search "form"` and `topic 9`.

---

## Core rules (apply to ALL mobile code you write)

### 1. Graphic Elements (Topic 1)

**ALWAYS:**
- Every decorative graphic element MUST be ignored by assistive technologies (1.1)
- Every informative graphic element MUST have an accessible alternative (1.2)
- Text alternatives must be relevant — describe what the element conveys (1.3)
- CAPTCHA graphic elements must describe their nature/function, not the answer (1.4)
- Complex graphics (charts, maps) need a detailed description (1.6, 1.7)
- Avoid text in graphic elements unless the effect cannot be reproduced with styled text (1.8 — Level AA)

**iOS (SwiftUI):**
```swift
// GOOD: informative image
Image("chart-sales")
    .accessibilityLabel("Sales increased 40% in Q3 2024")

// GOOD: decorative image — hidden from VoiceOver
Image("decorative-wave")
    .accessibilityHidden(true)

// GOOD: icon button with accessibility
Button(action: { /* ... */ }) {
    Image(systemName: "magnifyingglass")
}
.accessibilityLabel("Search")
```

**iOS (UIKit):**
```swift
// Informative image
imageView.isAccessibilityElement = true
imageView.accessibilityLabel = "Sales increased 40% in Q3 2024"

// Decorative image
decorativeImageView.isAccessibilityElement = false
decorativeImageView.accessibilityElementsHidden = true
```

**Android (Jetpack Compose):**
```kotlin
// GOOD: informative image
Image(
    painter = painterResource(R.drawable.chart_sales),
    contentDescription = "Sales increased 40% in Q3 2024"
)

// GOOD: decorative image
Image(
    painter = painterResource(R.drawable.decorative_wave),
    contentDescription = null // null = decorative in Compose
)

// GOOD: icon button
IconButton(onClick = { /* ... */ }) {
    Icon(
        Icons.Default.Search,
        contentDescription = "Search"
    )
}
```

**Android (XML Views):**
```xml
<!-- Informative image -->
<ImageView
    android:contentDescription="Sales increased 40% in Q3 2024"
    android:importantForAccessibility="yes" />

<!-- Decorative image -->
<ImageView
    android:contentDescription="@null"
    android:importantForAccessibility="no" />
```

**React Native:**
```jsx
// Informative image
<Image
  source={require('./chart.png')}
  accessible={true}
  accessibilityLabel="Sales increased 40% in Q3 2024"
/>

// Decorative image
<Image
  source={require('./decoration.png')}
  accessible={false}
  accessibilityElementsHidden={true}
  importantForAccessibility="no"
/>
```

**Flutter:**
```dart
// Informative image
Image.asset(
  'assets/chart.png',
  semanticsLabel: 'Sales increased 40% in Q3 2024',
)

// Decorative image
Semantics(
  excludeSemantics: true,
  child: Image.asset('assets/decoration.png'),
)
```

### 2. Colours (Topic 2)

- Information MUST NOT be conveyed by colour alone — always add shape, text, or icon (2.1)
- Text contrast: at least **4.5:1** (normal text) or **3:1** (large text ≥24px / bold ≥18.5px) (2.2 — Level AA)
- Non-text element contrast (icons, borders, UI controls): at least **3:1** (2.3 — Level AA)
- If contrast is insufficient by default, a replacement mechanism must exist and itself be accessible (2.4 — Level AA)

**iOS:**
```swift
// GOOD: support system contrast settings
// Use semantic colours that adapt to Increase Contrast mode
Text("Important")
    .foregroundColor(.primary) // adapts to accessibility settings

// Support Differentiate Without Colour
HStack {
    Image(systemName: "checkmark.circle.fill")
        .foregroundColor(.green)
    Text("Validated") // text reinforces the green colour meaning
}
```

**Android:**
```kotlin
// Support high contrast text mode
// Use theme colours that respond to system accessibility settings
Text(
    text = "Important",
    color = MaterialTheme.colorScheme.onSurface // adapts to theme
)
```

### 3. Multimedia (Topic 3)

- Audio-only media MUST have a text transcript (3.1, 3.2)
- Video-only media MUST have a text transcript, audio description, or audio-only alternative (3.3, 3.4)
- Synchronised media MUST have captions (3.7, 3.8)
- Synchronised media MUST have audio description (3.9, 3.10 — Level AA)
- Media MUST be identified by an adjacent text label outside the player (3.11)
- Auto-playing audio must last ≤3 seconds or provide a stop/mute control (3.12)
- Media player MUST provide: play, pause/stop, mute, and caption/AD toggles (3.13)
- Caption and AD controls must be at the same level as play/pause (3.14 — Level AA)

### 4. Tables (Topic 4)

- Data tables MUST have headers correctly associated with data cells (4.1, 4.2, 4.3)
- Complex tables MUST have a title and summary to explain structure (4.4, 4.5)

**iOS (SwiftUI):**
```swift
// GOOD: accessible table with header
List {
    Section(header: Text("Q3 Revenue by Region")) {
        ForEach(regions) { region in
            HStack {
                Text(region.name)
                Spacer()
                Text(region.revenue)
                    .accessibilityLabel("\(region.name): \(region.revenue)")
            }
        }
    }
}
```

**Android (Compose):**
```kotlin
// GOOD: announce table structure to TalkBack
Column(modifier = Modifier.semantics {
    contentDescription = "Revenue table, 3 regions, 2 columns: region and revenue"
}) {
    // Table content
}
```

### 5. Interactive Components (Topic 5)

**This is critical for mobile. Always look up: `bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh topic 5`**

- Every interactive component MUST be keyboard/switch accessible (5.1)
- Every interactive component MUST have a relevant accessible name (5.2)
- Accessible names MUST include any visible text (5.3)
- Screen reader users must receive context changes (5.4 — Level AA)
- Interactive component states (selected, expanded, disabled) MUST be rendered by assistive technologies (5.5)

**iOS (SwiftUI):**
```swift
// GOOD: button with state
Toggle(isOn: $isEnabled) {
    Text("Notifications")
}
// SwiftUI handles accessibility state automatically

// GOOD: custom component with traits and state
Button(action: toggleExpansion) {
    HStack {
        Text("Details")
        Image(systemName: isExpanded ? "chevron.up" : "chevron.down")
    }
}
.accessibilityAddTraits(.isButton)
.accessibilityValue(isExpanded ? "expanded" : "collapsed")

// GOOD: custom slider
Slider(value: $volume, in: 0...100)
    .accessibilityLabel("Volume")
    .accessibilityValue("\(Int(volume)) percent")
```

**Android (Compose):**
```kotlin
// GOOD: expandable section with state
Row(
    modifier = Modifier
        .clickable { toggleExpansion() }
        .semantics {
            role = Role.Button
            stateDescription = if (isExpanded) "expanded" else "collapsed"
        }
) {
    Text("Details")
    Icon(
        if (isExpanded) Icons.Default.ExpandLess else Icons.Default.ExpandMore,
        contentDescription = null // described by parent semantics
    )
}

// GOOD: disabled button announces state
Button(
    onClick = { /* ... */ },
    enabled = false // Compose announces "disabled" to TalkBack
) {
    Text("Submit")
}
```

**React Native:**
```jsx
// GOOD: interactive component with state
<TouchableOpacity
  accessible={true}
  accessibilityRole="button"
  accessibilityLabel="Details"
  accessibilityState={{ expanded: isExpanded }}
  onPress={toggleExpansion}
>
  <Text>Details</Text>
</TouchableOpacity>
```

### 6. Mandatory Elements (Topic 6)

- Every screen MUST have a title announced by assistive technologies (6.1)
- Default human language of the app MUST be identifiable by assistive technologies (6.2)

**iOS:**
```swift
// SwiftUI: screen title
NavigationView {
    ContentView()
        .navigationTitle("Settings")
}

// UIKit: screen title
override func viewDidLoad() {
    super.viewDidLoad()
    title = "Settings"
}

// App language: set in Info.plist CFBundleDevelopmentRegion
// and Localizable.strings
```

**Android:**
```kotlin
// Compose: screen title for TalkBack
Scaffold(
    topBar = {
        TopAppBar(title = { Text("Settings") })
    }
) { /* ... */ }

// Activity: label in AndroidManifest.xml
// <activity android:label="@string/settings_title" />

// Language: set in AndroidManifest.xml
// <application android:localeConfig="@xml/locales_config">
```

### 7. Information Structure (Topic 7)

- Content must use semantic headings exposed to assistive technologies (7.1)
- Significant elements must use appropriate semantics (lists, headings, etc.) (7.2)

**iOS (SwiftUI):**
```swift
// GOOD: heading semantics
Text("Account Settings")
    .font(.title)
    .accessibilityAddTraits(.isHeader)

Text("Privacy")
    .font(.headline)
    .accessibilityAddTraits(.isHeader)
```

**Android (Compose):**
```kotlin
// GOOD: heading semantics
Text(
    text = "Account Settings",
    style = MaterialTheme.typography.headlineMedium,
    modifier = Modifier.semantics { heading() }
)
```

**React Native:**
```jsx
<Text accessibilityRole="header">Account Settings</Text>
```

### 8. Presentation of Information (Topic 8)

- Content must remain visible and functional when text is enlarged to 200% via system settings (8.1)
- No loss of information or functionality at 200% enlargement (8.2 — Level AA)
- On screens ≥ 320px CSS equivalent, content must not require both horizontal and vertical scrolling (8.2)
- Landscape AND portrait orientations MUST be supported unless a specific orientation is essential (8.3)
- Focus indicator must be visible on all interactive elements (8.4)
- Content revealed on hover/focus must be dismissable, hoverable, and persistent (8.5)
- Content hidden from screen but exposed to AT must still be accessible (8.6)
- Content that appears on focus/hover must not obstruct other content without a dismiss mechanism (8.7 — Level AA)

**iOS:**
```swift
// GOOD: support Dynamic Type
Text("Welcome back")
    .font(.body) // respects system text size
    // Never use fixed point sizes for body text

// GOOD: allow both orientations in Info.plist
// UISupportedInterfaceOrientations: all orientations
```

**Android:**
```kotlin
// GOOD: use sp (scalable pixels) for text
Text(
    text = "Welcome back",
    fontSize = 16.sp // scales with system settings
)

// GOOD: support rotation in AndroidManifest.xml
// android:screenOrientation="unspecified"
```

### 9. Forms (Topic 9)

**Critical topic for mobile apps. Always look up: `bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh topic 9`**

- Every form field MUST have an accessible label (9.1)
- Labels must be relevant (9.2)
- Accessible name must include visible label text (9.3)
- Related fields must be grouped with a group label (9.4)
- Same-purpose fields must be identifiable programmatically across the app (9.5)
- Required fields must be indicated (9.7)
- Required fields' indication must be accessible (9.8)
- Error messages must be linked to the field and describe expected format (9.9)
- Input suggestions on error must be relevant (9.10 — Level AA)
- User must be able to review/modify/confirm data before final submission (9.11 — Level AA)
- Autocomplete for personal data fields (9.12 — Level AA)

**iOS (SwiftUI):**
```swift
// GOOD: labelled text field
TextField("Email address", text: $email)
    .textContentType(.emailAddress) // enables autocomplete (9.12)
    .keyboardType(.emailAddress)
    .accessibilityLabel("Email address")
    .accessibilityHint("Required. Format: name@example.com")

// GOOD: field group
Section(header: Text("Personal information")) {
    TextField("First name", text: $firstName)
        .textContentType(.givenName)
    TextField("Last name", text: $lastName)
        .textContentType(.familyName)
}

// GOOD: error message
TextField("Email address", text: $email)
    .accessibilityLabel("Email address")
if let error = emailError {
    Text(error)
        .foregroundColor(.red)
        .accessibilityLabel("Error: \(error)")
        // Post notification so VoiceOver announces immediately
}
```

**Android (Compose):**
```kotlin
// GOOD: labelled text field with error
OutlinedTextField(
    value = email,
    onValueChange = { email = it },
    label = { Text("Email address *") },
    isError = emailError != null,
    supportingText = emailError?.let { { Text(it) } },
    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
    modifier = Modifier.semantics {
        contentDescription = "Email address, required"
        if (emailError != null) {
            error("Error: $emailError")
        }
    }
)

// GOOD: autofill hint (9.12)
OutlinedTextField(
    value = firstName,
    onValueChange = { firstName = it },
    label = { Text("First name") },
    modifier = Modifier.autofill(
        autofillTypes = listOf(AutofillType.PersonFirstName),
        onFill = { firstName = it }
    )
)
```

**React Native:**
```jsx
// GOOD: accessible form field
<View accessible={true} accessibilityRole="none">
  <Text nativeID="emailLabel">Email address *</Text>
  <TextInput
    accessibilityLabelledBy="emailLabel"
    accessibilityHint="Required. Format: name@example.com"
    keyboardType="email-address"
    textContentType="emailAddress"      // iOS autocomplete
    autoComplete="email"                // Android autocomplete
    value={email}
    onChangeText={setEmail}
  />
  {emailError && (
    <Text accessibilityLiveRegion="polite" accessibilityRole="alert">
      {emailError}
    </Text>
  )}
</View>
```

### 10. Navigation (Topic 10)

- Every interactive component must be accessible and operable by keyboard and any pointing device (10.1)
- The application must not contain any keyboard or focus traps (10.2)
- Tab/swipe order must be consistent with visual reading order (10.3)
- Keyboard shortcuts using a single key must be controllable (disable, remap, or only active on focus) (10.4)

**iOS (SwiftUI):**
```swift
// GOOD: logical focus order
VStack {
    TextField("First name", text: $firstName)
    TextField("Last name", text: $lastName)
    Button("Submit") { submit() }
}
.accessibilityElement(children: .contain)
// SwiftUI follows visual order by default

// BAD: custom accessibility sort that breaks logical order
// .accessibilitySortPriority() — use only when needed
```

**Android:**
```kotlin
// GOOD: traversal order follows layout
Column {
    TextField(/* first name */)
    TextField(/* last name */)
    Button(onClick = { submit() }) { Text("Submit") }
}
// Compose follows composition order by default

// For XML views, use android:accessibilityTraversalBefore/After
// sparingly and only to fix non-obvious order issues
```

### 11. Consultation (Topic 11)

- No automatic refresh without user control (11.1)
- User must be able to control each time limit (extend, remove, or ≥20h) (11.2)
- Moving/blinking content must have a pause/stop mechanism (11.3, 11.4)
- No flashing content > 3 flashes per second (11.5)
- Abrupt context changes must be triggered by user action only, or user must be able to disable them (11.6, 11.7)
- Content viewable regardless of screen orientation (portrait/landscape) unless essential (11.8)
- Gestures: complex gestures (multi-pointer, path-based) must have single-pointer alternatives (11.9 — Level AA)
- Touch actions must use up-event (release), not down-event (press); or provide undo mechanism (11.10)
- Pointer target size must be at least 24×24 CSS px (11.14 — Level AA)
- Dragging actions must have a single-pointer alternative (11.15)
- Motion-triggered actions (shake, tilt) must have UI alternatives and be disableable (11.16)

**iOS:**
```swift
// GOOD: single-pointer alternative to pinch-to-zoom
// Provide + / - buttons alongside pinch gesture
ZStack {
    MapView()
    VStack {
        Spacer()
        HStack {
            Button(action: { zoomIn() }) {
                Image(systemName: "plus.magnifyingglass")
            }
            .accessibilityLabel("Zoom in")
            .frame(minWidth: 44, minHeight: 44) // minimum touch target

            Button(action: { zoomOut() }) {
                Image(systemName: "minus.magnifyingglass")
            }
            .accessibilityLabel("Zoom out")
            .frame(minWidth: 44, minHeight: 44)
        }
    }
}
```

**Minimum touch target sizes:**
```swift
// iOS: Apple recommends 44×44 pt minimum
.frame(minWidth: 44, minHeight: 44)

// RAAM 1.1 criterion 11.14: 24×24 CSS px minimum (AA)
// Using 44pt is safer and exceeds the requirement
```

```kotlin
// Android: minimum 48dp (exceeds RAAM's 24px requirement)
Modifier.sizeIn(minWidth = 48.dp, minHeight = 48.dp)
```

### 12–15. Extended Topics (EN 301 549)

These topics cover documentation, editing tools, support services, and real-time
communication. Query them individually when relevant:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh topic 12  # Documentation & accessibility features
bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh topic 13  # Editing tools
bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh topic 14  # Support services
bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh topic 15  # Real-time communication
```

Key rules for these topics:
- Documentation must describe accessibility features and how to use them (12.1 — Level AA)
- Accessibility features must not be removed or deactivated (12.3)
- Editing tools must support creation of accessible content (13.1–13.6)
- Support services must communicate accessibility info (14.1–14.3)
- Real-time text communication must meet EN 301 549 requirements (15.1–15.11)

---

## Platform-specific accessibility APIs — Quick reference

| Feature | iOS (SwiftUI) | iOS (UIKit) | Android (Compose) | Android (XML) | React Native | Flutter |
|---------|---------------|-------------|-------------------|---------------|--------------|---------|
| Label | `.accessibilityLabel()` | `.accessibilityLabel` | `Modifier.semantics { contentDescription }` | `contentDescription` | `accessibilityLabel` | `Semantics(label:)` |
| Hint | `.accessibilityHint()` | `.accessibilityHint` | `Modifier.semantics { stateDescription }` | — | `accessibilityHint` | `Semantics(hint:)` |
| Hidden | `.accessibilityHidden(true)` | `.isAccessibilityElement = false` | `Modifier.semantics { invisibleToUser() }` | `importantForAccessibility="no"` | `accessible={false}` | `ExcludeSemantics()` |
| Heading | `.accessibilityAddTraits(.isHeader)` | `.accessibilityTraits = .header` | `Modifier.semantics { heading() }` | `accessibilityHeading` | `accessibilityRole="header"` | `Semantics(header: true)` |
| Button | `.accessibilityAddTraits(.isButton)` | `.accessibilityTraits = .button` | `Modifier.semantics { role = Role.Button }` | `role="button"` | `accessibilityRole="button"` | `Semantics(button: true)` |
| Live region | `.accessibilityAddTraits(.updatesFrequently)` | `.accessibilityTraits = .updatesFrequently` | `Modifier.semantics { liveRegion = LiveRegionMode.Polite }` | `accessibilityLiveRegion="polite"` | `accessibilityLiveRegion="polite"` | `Semantics(liveRegion:)` |

---

## Pre-commit checklist (apply before finalizing any code)

- [ ] All informative graphic elements have accessible alternatives
- [ ] All decorative graphic elements are hidden from assistive technologies
- [ ] Colour is never the sole means of conveying information
- [ ] Text contrast ≥ 4.5:1 (normal) / 3:1 (large)
- [ ] All interactive elements are reachable via screen reader swipe navigation
- [ ] All interactive elements are operable by keyboard/switch access
- [ ] Component states (expanded, selected, disabled) are exposed to AT
- [ ] Every screen has a title announced by AT
- [ ] App language is declared for AT pronunciation
- [ ] Headings use proper accessibility traits/semantics
- [ ] All form fields have associated labels
- [ ] Required fields are indicated accessibly
- [ ] Error messages are linked to their fields and describe expected input
- [ ] Autocomplete is set for personal data fields
- [ ] Both portrait and landscape orientations work
- [ ] Content scales correctly with system font size (200%)
- [ ] Complex gestures have single-pointer alternatives
- [ ] Touch targets are at least 44×44pt (iOS) / 48×48dp (Android)
- [ ] No keyboard/focus traps exist
- [ ] No auto-playing media without controls

---

## When in doubt

1. Look up the specific RAAM criterion: `bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh criterion <topic.criterion>`
2. Check the test methodology (includes iOS AND Android steps): `bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh methodology <topic.criterion>`
3. Consult the glossary: `bash ${CLAUDE_SKILL_DIR}/scripts/raam-lookup.sh glossary "<term>"`
4. Use native platform components over custom ones — they have built-in accessibility
5. Test with VoiceOver (iOS) and TalkBack (Android) mentally: would every element be announced correctly?
