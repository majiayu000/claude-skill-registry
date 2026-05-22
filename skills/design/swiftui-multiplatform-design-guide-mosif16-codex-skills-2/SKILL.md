---
name: "SwiftUI Multiplatform Design Guide"
description: "Unified SwiftUI architecture for iOS, iPadOS, macOS, and visionOS with spatial design principles."
version: "1.0.0"
dependencies: []
tags:
  - swiftui
  - multiplatform
  - visionos
  - design
  - architecture
---

# Unified Architectures in SwiftUI: A Comprehensive Design Strategy for iOS, iPadOS, macOS, and visionOS

## 1. Introduction: The Convergence of Spatial and Flat Computing

The contemporary landscape of Apple software development is defined by a
radical convergence of interaction paradigms. Historically, the
demarcation lines between platforms were rigid: iOS was governed by the
touch target and the direct manipulation of glass; macOS was the domain
of the precise cursor and the indirect abstraction of the mouse; and
iPadOS occupied a liminal space, attempting to bridge the two. The
introduction of visionOS, however, has fundamentally disrupted this
tiered architecture. It has necessitated a new design language that is
not merely responsive in terms of screen size, but adaptive in terms of
physical dimension, input modality, and user intent.

This report provides an exhaustive analysis of the architectural
strategies required to build truly multiplatform applications using
SwiftUI. It moves beyond the superficial concept of \"cross-platform\"
code sharing---often synonymous with the \"lowest common denominator\"
approach---and instead advocates for a unified state-driven architecture
that respects the distinct ergonomics of each device. We will explore
the \"Liquid Glass\" metaphor that now underpins Apple's visual
language, the complex hierarchy of scenes and windows, and the unified
input models that allow a single semantic action to be triggered by a
tap, a click, or a gaze-driven pinch.

### 1.1 The Evolution of Human Interface Guidelines

The Apple Human Interface Guidelines (HIG) have evolved from static sets
of rules for distinct platforms into a fluid, overarching philosophy of
design. The core pillars of this philosophy---Space, Immersion,
Passthrough, and Spatial Audio---are no longer exclusive to the
headset.^1^ They represent a shift toward \"Spatial Computing\" that
influences even flat interfaces. For instance, the layering and depth
effects found in visionOS icons are conceptually linked to the parallax
effects on tvOS and the fluid animations of iOS.^2^

A critical insight from this evolution is the concept of
\"Pass-through\" design, not just in the optical sense of seeing the
real world, but in the interface sense of minimizing obstruction. On
iOS, this manifests as translucent materials and sheets; on visionOS, it
is literal transparency. Designing for this requires a \"content-first\"
approach where the \"chrome\" (interface elements) recedes. The HIG
explicitly advises using windows for UI-centric experiences while
reserving immersion for distinctive moments, a pattern that mirrors the
modal presentations on iOS.^1^

### 1.2 The Role of App Icons in Multiplatform Identity

The entry point to any application, the app icon, serves as the first
lesson in multiplatform adaptation. While often overlooked as a mere
asset, the icon's behavior dictates user expectations. On iOS, icons are
flattened super-ellipses that respond to home screen layout shifts. On
macOS, they act as uniform \"chicklets\" with drop shadows to imply a
desktop metaphor. However, on tvOS and visionOS, the icon becomes a
layered, three-dimensional object.

Research into the construction of these icons reveals a \"Liquid Glass\"
aesthetic where layers coalesce to create dimensionality. On visionOS,
an icon typically consists of a background layer and one or two
foreground layers. When the user gazes at the icon, the system applies
specular highlights and a parallax effect, physically lifting the
foreground layers to meet the user\'s eye.^2^ This is not merely
cosmetic; it acts as a primer for the user, teaching them that
\"looking\" is an interactive act. An effective multiplatform
architecture must therefore extend this layered thinking into the app
itself, treating UI elements not as flat pixels, but as planes floating
in a hierarchy, ready to react to the \"focus\" of the eye or the
pointer.

## 2. The Hierarchy of Scenes: Windows, Volumes, and Spaces

In the SwiftUI lifecycle, the Scene protocol has supplanted the View as
the fundamental unit of application structure. While the View defines
what the user sees, the Scene defines how the operating system manages
that content\'s existence, persistence, and lifecycle. A mastery of
Scene types---specifically WindowGroup, DocumentGroup, and
ImmersiveSpace---is the prerequisite for building apps that scale from
the iPhone SE to the Vision Pro.

### 2.1 The WindowGroup Paradigm and Lifecycle Management

The WindowGroup is the workhorse of SwiftUI. It defines a template for
the application\'s primary interface. However, its behavior is radically
polymorphic depending on the host platform. On iPhone, it generally
instantiates a single, persistent window. On iPadOS and macOS, it serves
as a factory for creating multiple, concurrent windows.^4^

This polymorphism introduces significant architectural complexity
regarding state management. A common anti-pattern in early SwiftUI
development was the reliance on a singleton AppState object injected at
the App level. While functional on a single-window iPhone, this
architecture collapses on iPadOS and macOS. If a user opens two windows
of the same application to compare data, a singleton architecture forces
both windows to share the same navigation path and selection state.
Navigating in Window A inadvertently drives navigation in Window B,
breaking the user\'s mental model of independent workspaces.

To address this, modern multiplatform architecture demands that state be
scoped to the Scene. Each time a WindowGroup instantiates a new window,
it must effectively spin up a fresh dependency graph for that window\'s
view hierarchy. This often involves creating a per-window ViewModel or
NavigationManager that is injected into the environment of the window\'s
root view, rather than the app\'s root.^6^

#### 2.1.1 Window Resizability and Geometry

The concept of a \"Window\" varies by physics. On macOS, a window is a
rect confined by the screen bezel, fully resizable by the user. On
visionOS, a window is a planar surface floating in 3D space, also
resizable, but with constraints dictated by legibility and the field of
view.

SwiftUI provides the .windowResizability and .defaultSize modifiers to
control this.

- **Content Size Strategy:** Using .windowResizability(.contentSize)
  allows the window to shrink-wrap its SwiftUI content. This is ideal
  for settings panels or utility dialogs.^4^

- **Automatic Strategy:** The system determines the size. On visionOS,
  this interacts with the user\'s distance. A window that appears
  \"small\" (in angular dimension) when far away might technically be
  rendering at the same pixel resolution as a \"large\" window close up.
  The system automatically scales content to maintain legibility
  (dynamic type), meaning developers must layout for \"points\" rather
  than pixels to avoid microscopic text in spatial environments.^1^

### 2.2 The DocumentGroup and File-Based Workflows

For productivity applications, the DocumentGroup scene type is
indispensable. It provides out-of-the-box integration with the
platform\'s file system (Finder on macOS, Files on iOS/iPadOS). More
importantly, it automates the complex \"Dirty State\" management and
file locking mechanisms required for desktop-class applications.^8^

When a DocumentGroup is deployed, SwiftUI automatically bridges the
application\'s document model (conforming to FileDocument) to the
system\'s standard menu commands. The \"File \> Open,\" \"File \>
Save,\" and \"File \> Duplicate\" menu items on macOS are automatically
wired to the active document scene. This is a crucial \"free\" feature
of SwiftUI that replicates hundreds of lines of AppKit boilerplate.

However, transitioning a standard app to a DocumentGroup app requires a
fundamental shift in data flow. The source of truth becomes the file on
disk, not a cloud database or a local cache. This has implications for
visionOS, where file manipulation might happen in a shared space
alongside other apps. The DocumentGroup on visionOS presents files as
floating windows, allowing users to arrange multiple documents (e.g.,
PDFs or spreadsheets) in the air around them, effectively turning their
physical room into a multi-monitor desktop.^8^

### 2.3 ImmersiveSpaces: The Exclusivity of Virtual Reality

The ImmersiveSpace scene type represents the most significant divergence
in the unified architecture. Unlike windows, which are containers *for*
content, an ImmersiveSpace allows the app to become the container *of*
the environment.

The critical architectural constraint of ImmersiveSpace is exclusivity.
On visionOS, multiple apps can have windows open in the \"Shared
Space,\" but only one app can occupy the \"Immersive Space\" at any
given time. If App A is immersive, App B\'s immersive content is hidden.
This necessitates a rigorous management of transition logic. Opening an
immersive space is an asynchronous operation (openImmersiveSpace) that
can fail or be cancelled by the system.^10^

#### 2.3.1 The \"Loading Window\" Transition Pattern

A specific challenge arises when transitioning between different
immersive contexts (e.g., moving from a \"Mars\" environment to a
\"Moon\" environment). Because only one space can be open, the
application must dismiss the current space before opening the next.
However, if the app dismisses the current space *before* a window is
opened, the app effectively has zero open scenes. In visionOS, an app
with zero open scenes is terminated by the system.

To mitigate this, expert developers employ the \"Loading Window\"
pattern.

1.  **Trigger:** User selects a new environment.

2.  **Action:** The app opens a small, transient window (e.g., a
    \"Loading\...\" spinner).

3.  **Synchronization:** Once the window is confirmed visible (via
    scenePhase or onAppear), the app dismisses the current
    ImmersiveSpace.

4.  **Transition:** The app requests the new ImmersiveSpace.

5.  **Cleanup:** Upon successful presentation of the new space, the app
    dismisses the loading window.

This \"Make-Before-Break\" logic is essential to prevent app crashes
during heavy context switching in VR environments.^12^ It highlights the
complexity of state management when dealing with asynchronous scene
topology, a problem nonexistent in the synchronous navigation stacks of
iOS.

### 2.4 The ScenePhase State Machine

Observing the lifecycle of these scenes is handled via ScenePhase. This
environment value reports whether a scene is .active, .inactive, or
.background.^13^

- **Active:** The scene is receiving input events.

- **Inactive:** The scene is visible but not focused. On macOS, this is
  a background window. On iPadOS, this is the non-interactive side of a
  Split View. On visionOS, this state is common when the user looks away
  from a window or interacts with a different app in the Shared Space.

- **Background:** The scene is invisible.

Handling .inactive is critical for battery life and performance,
especially in visionOS. If an app runs a heavy particle simulation in a
volumetric window, it should pause that simulation immediately upon
entering the .inactive state (i.e., when the user looks away). Failing
to do so wastes significant GPU resources on content the user is not
perceiving.^14^

**Table 1: Scene Capabilities and Constraints Across Platforms**

  ----------------------------------------------------------------------------------
  **Feature**       **iOS**         **iPadOS**         **macOS**      **visionOS**
  ----------------- --------------- ------------------ -------------- --------------
  **Concurrency**   Single Scene    Multiple Windows   Multiple       Multiple
                    (mostly)                           Windows        Windows &
                                                                      Volumes

  **Window          System Only     Split View / Stage User           User (Uniform
  Resizing**                        Manager            (Freeform)     Scale)

  **Coordinate      2D Screen       2D Screen          2D Screen      3D unbounded
  Space**                                                             (Shared Space)

  **Immersive       N/A             N/A                N/A            Exclusive (One
  Mode**                                                              App Only)

  **Termination**   On              On                 On Cmd+Q /     On Zero Scenes
                    Backgrounding   Swipe/Background   Last Window    Open
  ----------------------------------------------------------------------------------

## 3. Adaptive Layout Strategies: From Sidebars to Ornaments

The divergence in screen real estate---from the 5-inch iPhone to the
infinite canvas of the Vision Pro---demands a layout strategy that is
not just responsive (stretching content) but adaptive (changing
hierarchy). The historical approach of using NavigationSplitView for
everything has proven insufficient for complex, top-level navigation,
leading to the adoption of the new sidebarAdaptable paradigms.

### 3.1 The Decline of NavigationSplitView for Top-Level Navigation

For years, NavigationSplitView (and its predecessor NavigationView) was
the standard for \"Master-Detail\" interfaces. It provides a sidebar, a
content column, and a detail area. On iPad and macOS, this works well
for browsing hierarchal data (e.g., Mail, Notes).

However, NavigationSplitView struggles as a *root* navigation container
for apps with distinct, unrelated functional areas (e.g., a Music app
with \"Library,\" \"Radio,\" and \"Search\"). Using a Split View forces
these distinct areas into a single list, which often feels reductive on
mobile devices. Furthermore, on visionOS, NavigationSplitView renders
with a specific glass material where the sidebar is pushed slightly back
in Z-space. While beautiful, nesting Split Views (e.g., a Split View
inside a Tab View) can lead to visual clutter and, in some versions of
macOS, application crashes due to toolbar conflicts.^15^

### 3.2 The SidebarAdaptable Revolution

With iOS 18 and macOS 15, Apple introduced the
.tabViewStyle(.sidebarAdaptable) modifier for TabView. This represents a
fundamental shift in layout architecture, effectively merging the
concepts of the Tab Bar and the Sidebar into a single, fluid
component.^17^

This modifier allows a standard TabView to adapt its presentation mode
based on the horizontal size class:

- **Compact Width (iPhone/iPad Slide Over):** It renders as a
  traditional bottom Tab Bar.

- **Regular Width (iPad Full Screen):** It renders as a top-positioned
  tab bar that allows the user to toggle into a sidebar.

- **macOS:** It automatically renders as a sidebar, adopting the native
  translucent material.

- **visionOS:** It transforms into a vertical \"Ornament\" floating to
  the left of the main window.^17^

This unification solves the \"Sidebar vs. TabBar\" code-forking problem.
Developers no longer need to write if os(iOS) { TabView } else {
NavigationSplitView }. They can write a single TabView and trust the
system to render the ergonomically correct container.

#### 3.2.1 The TabSection for Hierarchical Density

A crucial companion to sidebarAdaptable is the TabSection. In a bottom
tab bar, space is premium; you can typically fit only 3-5 items. In a
sidebar, vertical scrolling allows for dozens of items. TabSection
allows developers to group tabs logically.^19^

- **Behavior on iOS:** TabSection headers are generally flattened or
  ignored, ensuring the bottom bar remains uncluttered.

- **Behavior on macOS/iPad (Sidebar):** TabSection headers appear as
  distinct, collapsible headers (e.g., \"Library,\" \"Playlists,\"
  \"Settings\").

This enables a \"Density-Adaptive\" design. An app can expose granular
navigation options (like specific folders) in the Sidebar mode while
collapsing them into a single \"Browse\" tab in the Tab Bar mode, simply
by structuring the hierarchy with TabSection.^20^

### 3.3 Deep Navigation State Preservation

One of the most difficult challenges in adaptive layouts is preserving
navigation state when the layout container changes. If a user is deep in
a navigation stack on their iPad (in Sidebar mode) and then creates a
Split View with another app, the iPad might crunch down to Compact
width, forcing the app to switch to a Bottom Tab Bar.

If the navigation state is stored inside the view hierarchy (e.g.,
\@State inside the view), this transition destroys the state, resetting
the user to the root view.

**Architectural Solution:** The Navigation State must be hoisted out of
the View and into the Model or Environment. By using
NavigationStack(path: \$navigationModel.path), the path of the
navigation stack is decoupled from the UI container. When the TabView
morphs from Sidebar to Tab Bar, the new NavigationStack instance binds
to the same persistent path object, allowing the user to seamlessly
\"land\" on the exact same detail screen they were viewing before the
transition.^21^

### 3.4 Micro-Layouts with ViewThatFits

While sidebarAdaptable handles the macro-structure, the layout of
individual cells and panels requires ViewThatFits. This container is
essentially a logic gate for layout: it takes a closure of views and
renders the first one that fits within the available space without
truncation.^23^

This is practically mandatory for visionOS. Unlike iOS devices with
fixed point dimensions, a visionOS window can be resized to nearly any
aspect ratio. A horizontal card layout that looks great at 1000pt width
might look broken at 400pt. ViewThatFits allows the developer to provide
a \"Horizontal\" version and a \"Vertical\" version of the same
component.

> Swift

ViewThatFits(in:.horizontal) {\
HStack { /\* Wide layout \*/ }\
VStack { /\* Tall layout \*/ }\
}

This declarative approach replaces the fragile GeometryReader patterns
of the past, which often caused layout cycles and performance
degradation.^23^ It ensures that the app\'s internal components are as
fluid as its outer container.

## 4. Input Models: The Tri-Modal Interaction System

The most profound difference between the platforms lies in how the user
expresses intent. The \"Tri-Modal\" system encompasses **Direct
Manipulation** (Touch), **Indirect Pointing** (Mouse/Trackpad), and
**Intent-Based Targeting** (Gaze/Pinch). A unified architecture must
abstract these physical differences into semantic actions.

### 4.1 The Unification of Tap and Spatial Interaction

In the early days of touch interfaces, the TapGesture was simple: a
coordinate on a 2D digitizer. visionOS complicates this. A \"tap\" on
visionOS is actually a complex sequence: The user\'s eye targets an
entity (Hover), and the user\'s fingers pinch (Commit). The \"location\"
of this tap is not on the screen, but at the intersection ray of the eye
gaze and the virtual object\'s collider.^25^

SwiftUI unifies this via the SpatialTapGesture.

- **On iOS/macOS:** It reports the 2D location of the click/tap relative
  to the view.

- **On visionOS:** It reports the 3D location of the raycast
  intersection on the entity surface.

This is vital for interactive 3D content. For example, in a volumetric
solar system app, a SpatialTapGesture allows the user to tap on a
specific crater on a 3D moon model. The code handling this can be shared
across platforms, with the iOS version simply interpreting the touch
coordinates on the flat projection of the 3D view.^26^

### 4.2 The Physics of Gaze and Hover Effects

On visionOS, the \"Cursor\" is the user\'s eye. However, unlike a mouse
cursor, the eye is jittery and unconscious. To prevent accidental
triggers (the \"Midas Touch\" problem), visionOS does not report gaze
coordinates to the application until a selection is made.

Instead, the system uses **Hover Effects** to provide feedback. When the
eye dwells on an interactive element, the system highlights it. This
feedback is *essential* for discoverability. A button without a hover
effect on visionOS feels \"dead\" and users will assume it is static
text.

**Architectural Requirement:** Every interactive custom view in a
multiplatform app must apply the .hoverEffect() modifier.

- **iPadOS:** This adds pointer magnetism and shape morphing.

- **visionOS:** This adds the translucent glow or \"lift\" effect.

- **macOS:** This is generally ignored or maps to standard cursor
  changes.

Apple\'s new CustomHoverEffect protocol (iOS 18+) allows for
fine-grained control. Developers can define exactly how a view scales,
dims, or creates a shadow when focused. This unifies the \"Focus\"
visual language across the pointer-driven Mac and the eye-driven
headset.^28^

**Privacy Implication:** Because the app cannot see where the user is
looking, mechanics that rely on \"hover to reveal\" (like tooltips) are
handled by the system or require a distinct gesture (like a long gaze).
Developers cannot programmatically trigger logic based on gaze dwell
time alone without the user\'s explicit interaction.^30^

### 4.3 Indirect Input: The Focus Engine

While touch is primary on iOS, keyboard interaction is primary on macOS
and arguably equal to gaze on visionOS (for productivity). The
FocusState API is the bridge here.

Properly implementing FocusState ensures that an app is navigable via
the Tab key. This is not just a macOS feature; connecting a Bluetooth
keyboard to a Vision Pro enables the same tabbing behavior. If an app
relies solely on onTapGesture, it becomes inaccessible to keyboard
users. Using Button and FocusState ensures that the \"focus ring\"
(macOS) or \"focus highlight\" (visionOS) moves logically through the
UI.^31^

### 4.4 Gesture Composition and Conflicts

Multiplatform apps frequently encounter gesture conflicts. A List on iOS
handles vertical scrolling. A List on visionOS handles \"pinch and
drag\" to scroll. If a developer places a custom DragGesture on a list
row (e.g., for a \"swipe to delete\" or a custom slider), it can block
the scroll gesture on visionOS.

**Best Practice:**

1.  **Use Standard Components:** Standard List swipe actions work
    automatically on all platforms.

2.  **Targeted Gestures:** On visionOS, use
    .gesture(MyGesture().targetedToEntity(myEntity)) when working in
    RealityView. This scopes the gesture to the specific 3D object,
    preventing it from consuming window-level swipes.^27^

3.  **Simultaneous Recognition:** Use .simultaneousGesture sparingly,
    but it is often necessary when a button inside a scroll view needs
    to register a tap before the scroll view registers a drag start.^33^

## 5. Command and Control Infrastructure

The divergence between the toolbar-driven iOS and the menu-driven macOS
is a major source of friction. A truly native macOS app relies on the
Menu Bar for command discovery, while iOS relies on visible buttons.

### 5.1 The Responder Chain Reimagined: FocusedValue

SwiftUI reintroduces the concept of the \"Responder Chain\" through
FocusedValue and Commands. This allows for a clean separation of the
*Trigger* (Menu Item) from the *Action* (View Logic).

Consider a \"Delete\" command.

1.  **The Trigger:** A \"Delete\" item in the \"Edit\" menu of the Menu
    Bar.

2.  **The Action:** A function inside a specific view that deletes the
    selected item.

In a multi-window app, the Menu Bar is global. How does it know which
window\'s content to delete?

The solution is FocusedValue.

- The View defines a struct conforming to FocusedValueKey.

- The View attaches .focusedValue(\\.deleteAction, deleteFunction) to
  itself.

- The Command reads \@FocusedValue(\\.deleteAction) var deleteAction.

When the user clicks \"Delete\" in the menu, the system traverses the
view hierarchy starting from the *focused* element, looking for the
nearest defined deleteAction. This \"Innermost Wins\" logic perfectly
mimics the AppKit responder chain but is type-safe and declarative.^34^

### 5.2 Context Menus vs. Menus

The contextMenu modifier maps to:

- **iOS:** Haptic Touch (Long Press).

- **macOS:** Right Click.

- **visionOS:** Long Pinch (or a dedicated button).

**VisionOS Warning:** Apple guidelines discourage the overuse of Context
Menus on visionOS because the \"Long Pinch\" gesture is physically more
taxing than a right-click or a tap. It requires holding a muscular
tension. Therefore, on visionOS, actions that are buried in context
menus on iOS should often be surfaced to the top-level UI, perhaps in an
Ornament or a dedicated \"More\" (\...) button.^19^

The modern .contextMenu(forSelectionType:) modifier is preferred over
attaching .contextMenu to every row in a list. This newer modifier
operates on the *selection* of the list, which is more performant and
aligns better with the multi-selection capabilities of macOS and
iPadOS.^36^

### 5.3 Ornaments: The Spatial Toolbar

visionOS replaces the Toolbar with **Ornaments**. While SwiftUI
automatically maps .toolbar content to a bottom ornament, developers can
explicitly create \"Side Ornaments\" using the
.ornament(attachmentAnchor:) modifier.

Architecturally, Ornaments are \"glued\" to the window but exist in a
separate Z-plane. They are the ideal location for tool palettes (e.g.,
brushes, colors) that need to be persistent but unobtrusive. Unlike
macOS toolbars which are rigid, Ornaments allow for a \"floating
palette\" feel that users intuitively understand they can grab (though
currently, they move with the window).^37^

## 6. VisionOS Specifics: The Coordinates of Shared Space

Developing for visionOS requires a mental shift from 2D coordinates to
3D transforms. Even in the \"Shared Space\" (where apps are windows),
coordinate systems matter.

### 6.1 Volumes and Z-Depth

A WindowGroup with .windowStyle(.volumetric) creates a **Volume**. This
is a bounded 3D box.

- **Clipping:** Content inside a volume is clipped to the volume\'s
  bounds. You cannot have a 3D character walk out of the volume box.

- **Interaction:** Users can rotate the entire volume. This means the
  app must handle orientation changes not of the device, but of the
  *container* relative to the user.

A common issue in volumes is **Scale**. If a developer imports a generic
USDZ model, it might be 100 meters tall in real-world units. In a
volume, this would be microscopic or strictly clipped. Developers must
normalize the scale of all 3D assets to fit within the standard volume
dimensions (typically 1-2 meters).^7^

### 6.2 The \"Front\" of the App

In iOS, \"Front\" is the screen. In visionOS, \"Front\" is relative to
the user\'s head at the moment the app launches.

The system provides a reset feature (long-pressing the Digital Crown)
that re-centers all apps. Applications must listen for this and ensure
their content re-aligns.

However, developers cannot programmatically force the window to move to
a specific coordinate in the user\'s room (in Shared Space). This is a
privacy constraint to prevent apps from overlaying spam on walls or
tracking the user\'s movement. The user owns the transform of the
window; the app only owns the content inside the window.1

## 7. Accessibility and Inclusion as Architecture

Accessibility in multiplatform design is often treated as compliance,
but in the context of SwiftUI and visionOS, it is a core architectural
pillar.

### 7.1 Target Sizing and Physics

- **iOS:** Minimum target size is 44x44 points.

- **visionOS:** Minimum target size is 60x60 points (virtual).

Why the difference? Eye tracking has a natural \"jitter\" (saccades). A
target smaller than 60pt is difficult to reliably fixate on. If an app
ports a dense iOS toolbar to visionOS without adjusting spacing, users
will constantly mis-click.

Solution: Use adaptive padding or ViewThatFits to increase spacing in
the visionOS layout.38

### 7.2 Accessibility Actions

The .accessibilityAction modifier allows developers to map complex
gestures to simple semantic actions.

- *Scenario:* A \"Shake to Undo\" gesture or a \"Three-finger swipe\" on
  iPad.

- *Problem:* A user with limited motor control cannot perform these. A
  visionOS user might find them tiring.

- *Solution:* .accessibilityAction(named: \"Undo\") { undo() }.

This exposes the action to Voice Control, Switch Control, and the
Accessibility Menu, ensuring that the app\'s functionality is available
regardless of the input method. On visionOS, this is critical because
some users may not be able to perform the \"Pinch\" gesture perfectly
and may rely on Dwell Control or Voice.^38^

## 8. Implementation Strategy: The Code Structure

To achieve this unified architecture, the codebase should follow a
specific structural pattern.

### 8.1 The \"Core-UI\" Separation

1.  **Core Logic (Model):** Pure Swift. No import SwiftUI (where
    possible). Handles data, persistence, and business logic.

2.  **State Layer (ViewModel):** ObservableObject or \@Observable.
    Handles the mapping of data to UI state (e.g., \"is the sidebar
    open?\", \"what is the current selection?\").

3.  **Interface Layer (Views):** Highly modular SwiftUI views.

    - **Atoms:** Buttons, Labels (Styled with .hoverEffect,
      .contentShape).

    - **Molecules:** List Rows, Cards (Using ViewThatFits for layout).

    - **Organisms:** NavigationSplitView / TabView (Using
      sidebarAdaptable).

### 8.2 Testing for Multiplatform

Testing must go beyond the Simulator.

- **Touch Simulation:** The Mac simulator for iPad is accurate for
  layout but fails to simulate the \"fat finger\" problem.

- **Gaze Simulation:** The visionOS simulator allows using the mouse to
  simulate eyes. This is useful for functional testing but terrible for
  usability testing. It is impossible to gauge eye-strain or target
  acquisition difficulty without the actual headset.

- **Pointer Simulation:** On iPad, the \"Hover\" effect must be tested
  with a trackpad connected. Many hover states look fine on Mac but feel
  \"sticky\" or wrong on iPad due to the magnetic effect.^39^

## 9. Conclusion

The convergence of iOS, iPadOS, macOS, and visionOS is not a convergence
of *hardware*---the devices remain physically distinct---but a
convergence of *architecture*. The \"Spatial\" design language
introduced by visionOS has bled back into the flat platforms,
introducing depth, layering, and intent-aware interactivity to the
entire ecosystem.

Constructing a coherent multiplatform app requires the developer to
abandon the \"Device-Centric\" mindset (e.g., \"If iPhone, do X\") and
adopt a \"Context-Centric\" mindset (e.g., \"If Compact Width, do X; If
Pointing Device attached, do Y\"). By leveraging the Scene hierarchy,
the sidebarAdaptable layout engine, the FocusedValue command chain, and
the unified SpatialTapGesture input model, developers can build
applications that feel native to the hand, the desk, and the room alike.
The future of Apple development is not just writing code that runs
everywhere, but writing code that belongs everywhere.

### **Table 2: Unified Input Mapping Strategy**

  --------------------------------------------------------------------------------------------
  **Semantic         **iOS          **iPadOS            **macOS                **visionOS
  Action**           (Touch)**      (Touch/Pointer)**   (Pointer/Keyboard)**   (Gaze/Hand)**
  ------------------ -------------- ------------------- ---------------------- ---------------
  **Primary Select** Tap            Tap / Click         Click                  Look + Pinch

  **Secondary        Long Press     Long Press / Right  Right Click            Long Pinch /
  Action**           (Haptic)       Click                                      \"More\" Btn

  **Scroll**         Swipe          Swipe / Two-finger  Scroll Wheel /         Pinch + Drag
                                    Pan                 Trackpad               Hand

  **Zoom**           Pinch Spread   Pinch Spread        Pinch (Trackpad)       Two-Handed
                                                                               Spread

  **Focus/Target**   N/A (Direct)   Hover (Magnetic)    Hover (Cursor)         Gaze (Hover
                                                                               Effect)

  **Text Entry**     Virtual        Virtual / Physical  Physical Keyboard      Virtual /
                     Keyboard       Key                                        Dictation
  --------------------------------------------------------------------------------------------

### **Table 3: Lifecycle State Implications**

  -----------------------------------------------------------------------
  **ScenePhase**          **System Behavior       **Developer
                          (General)**             Responsibility**
  ----------------------- ----------------------- -----------------------
  **Active**              App gets full CPU/GPU   Start animations,
                          priority.               connect sockets, enable
                                                  sensors.

  **Inactive**            App is visible but not  Pause heavy renders
                          focused (e.g., Mac      (games), save draft
                          background window).     state.

  **Background**          App is not visible. May **Critical:** Release
                          be suspended shortly.   heavy resources, close
                                                  file handles, stop
                                                  location updates. On
                                                  visionOS, pause all
                                                  ARKit sessions.
  -----------------------------------------------------------------------

### **Table 4: Command Infrastructure Implementation**

  -------------------------------------------------------------------------------
  **Component**             **Role**                **Implementation**
  ------------------------- ----------------------- -----------------------------
  **Menu Bar**              Global Command          .commands { CommandMenu(\...)
                            Discovery               } on WindowGroup.

  **FocusedValue**          The \"Responder Chain\" \@FocusedValue(\\.key) var
                            Link                    action in Commands;
                                                    .focusedValue(\\.key, value)
                                                    in Views.

  **KeyboardShortcut**      Power User Activation   .keyboardShortcut(\"s\",
                                                    modifiers:.command) on
                                                    Buttons.

  **AccessibilityAction**   Assistive Tech Trigger  .accessibilityAction(named:
                                                    \"Save\") { save() }.
  -------------------------------------------------------------------------------

#### Works cited

1.  Designing for visionOS \| Apple Developer Documentation, accessed
    November 24, 2025,
    [[https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos]{.underline}](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos)

2.  App icons \| Apple Developer Documentation, accessed November 24,
    2025,
    [[https://developer.apple.com/design/human-interface-guidelines/app-icons]{.underline}](https://developer.apple.com/design/human-interface-guidelines/app-icons)

3.  Human Interface Guidelines \| Apple Developer Documentation,
    accessed November 24, 2025,
    [[https://developer.apple.com/design/human-interface-guidelines]{.underline}](https://developer.apple.com/design/human-interface-guidelines)

4.  Presenting windows and spaces \| Apple Developer Documentation,
    accessed November 24, 2025,
    [[https://developer.apple.com/documentation/visionos/presenting-windows-and-spaces]{.underline}](https://developer.apple.com/documentation/visionos/presenting-windows-and-spaces)

5.  Supporting multiple windows --- App Dev Tutorials \| Apple Developer
    Documentation, accessed November 24, 2025,
    [[https://developer.apple.com/tutorials/app-dev-training/supporting-multiple-windows]{.underline}](https://developer.apple.com/tutorials/app-dev-training/supporting-multiple-windows)

6.  Scenes. Have you ever wondered how SwiftUI... \| by Michael-Andre
    Odusami - Medium, accessed November 24, 2025,
    [[https://medium.com/@michaelodusami/swiftui-scenes-29778723d48b]{.underline}](https://medium.com/@michaelodusami/swiftui-scenes-29778723d48b)

7.  How to add windows in an immersive space. - visionosdev - Reddit,
    accessed November 24, 2025,
    [[https://www.reddit.com/r/visionosdev/comments/1ctn03e/how_to_add_windows_in_an_immersive_space/]{.underline}](https://www.reddit.com/r/visionosdev/comments/1ctn03e/how_to_add_windows_in_an_immersive_space/)

8.  Building and customizing the menu bar with SwiftUI \| Apple
    Developer Documentation, accessed November 24, 2025,
    [[https://developer.apple.com/documentation/SwiftUI/Building-and-customizing-the-menu-bar-with-SwiftUI]{.underline}](https://developer.apple.com/documentation/SwiftUI/Building-and-customizing-the-menu-bar-with-SwiftUI)

9.  Enhancing your app\'s content with tab navigation \| Apple Developer
    Documentation, accessed November 24, 2025,
    [[https://developer.apple.com/documentation/SwiftUI/Enhancing-your-app-content-with-tab-navigation]{.underline}](https://developer.apple.com/documentation/SwiftUI/Enhancing-your-app-content-with-tab-navigation)

10. ImmersiveSpace \| Apple Developer Documentation, accessed November
    24, 2025,
    [[https://developer.apple.com/documentation/SwiftUI/ImmersiveSpace]{.underline}](https://developer.apple.com/documentation/SwiftUI/ImmersiveSpace)

11. Exploring immersive spaces in visionOS - Create with Swift, accessed
    November 24, 2025,
    [[https://www.createwithswift.com/exploring-immersive-spaces-in-visionos/]{.underline}](https://www.createwithswift.com/exploring-immersive-spaces-in-visionos/)

12. How to transition from one immersive space to another -- Part Two -
    Step Into Vision, accessed November 24, 2025,
    [[https://stepinto.vision/example-code/how-to-transition-from-one-immersive-space-to-another-part-two/]{.underline}](https://stepinto.vision/example-code/how-to-transition-from-one-immersive-space-to-another-part-two/)

13. ScenePhase \| Apple Developer Documentation, accessed November 24,
    2025,
    [[https://developer.apple.com/documentation/swiftui/scenephase]{.underline}](https://developer.apple.com/documentation/swiftui/scenephase)

14. Interactivity with Scene Phases: Harnessing
    \@Environment(.scenePhase) in SwiftUI \| by Wesley Matlock \|
    Medium, accessed November 24, 2025,
    [[https://medium.com/@wesleymatlock/interactivity-with-scene-phases-harnessing-environment-scenephase-in-swiftui-935da9c36874]{.underline}](https://medium.com/@wesleymatlock/interactivity-with-scene-phases-harnessing-environment-scenephase-in-swiftui-935da9c36874)

15. Exploring the Navigation Split View - Create with Swift, accessed
    November 24, 2025,
    [[https://www.createwithswift.com/exploring-the-navigationsplitview/]{.underline}](https://www.createwithswift.com/exploring-the-navigationsplitview/)

16. Axel Le Pennec: \"With the new TabView design on...\" - iOS Dev
    Space, accessed November 24, 2025,
    [[https://iosdev.space/@alpennec/113465183815948633]{.underline}](https://iosdev.space/@alpennec/113465183815948633)

17. sidebarAdaptable \| Apple Developer Documentation, accessed November
    24, 2025,
    [[https://developer.apple.com/documentation/SwiftUI/TabViewStyle/sidebarAdaptable]{.underline}](https://developer.apple.com/documentation/SwiftUI/TabViewStyle/sidebarAdaptable)

18. Using iOS 18\'s new TabView with a sidebar - Donny Wals, accessed
    November 24, 2025,
    [[https://www.donnywals.com/using-ios-18s-new-tabview-with-a-sidebar/]{.underline}](https://www.donnywals.com/using-ios-18s-new-tabview-with-a-sidebar/)

19. Using SwiftUI\'s Improved TabView with Sidebar on iOS 18 - iOS
    Coffee Break, accessed November 24, 2025,
    [[https://www.ioscoffeebreak.com/issue/issue34]{.underline}](https://www.ioscoffeebreak.com/issue/issue34)

20. From Top Bar To Sidebar With The sidebarAdaptable TabView Style -
    YouTube, accessed November 24, 2025,
    [[https://www.youtube.com/watch?v=YcrMLBmz0dA]{.underline}](https://www.youtube.com/watch?v=YcrMLBmz0dA)

21. Adopting both NavigationSplitView and TabView depending on
    Window/Screen Width, accessed November 24, 2025,
    [[https://stackoverflow.com/questions/79665096/adopting-both-navigationsplitview-and-tabview-depending-on-window-screen-width]{.underline}](https://stackoverflow.com/questions/79665096/adopting-both-navigationsplitview-and-tabview-depending-on-window-screen-width)

22. The Ideal TabView Behaviour With SwiftUI Navigation Stack \| by
    Akshay Mahajan, accessed November 24, 2025,
    [[https://betterprogramming.pub/swiftui-navigation-stack-and-ideal-tab-view-behaviour-e514cc41a029]{.underline}](https://betterprogramming.pub/swiftui-navigation-stack-and-ideal-tab-view-behaviour-e514cc41a029)

23. Mastering ViewThatFits in SwiftUI iOS 16 \| by Husnain Ali \|
    Medium, accessed November 24, 2025,
    [[https://medium.com/@husnainali593/mastering-viewthatfits-in-swiftui-ios-16-9af7e642a84a]{.underline}](https://medium.com/@husnainali593/mastering-viewthatfits-in-swiftui-ios-16-9af7e642a84a)

24. The Curious Case of SwiftUI Layout: Why That Spacer Isn\'t Doing
    What You Think \| by Wesley Matlock \| Medium, accessed November 24,
    2025,
    [[https://medium.com/@wesleymatlock/the-curious-case-of-swiftui-layout-why-that-spacer-isnt-doing-what-you-think-86d7cede277c]{.underline}](https://medium.com/@wesleymatlock/the-curious-case-of-swiftui-layout-why-that-spacer-isnt-doing-what-you-think-86d7cede277c)

25. Deep Dive into Manipulation on visionOS, accessed November 24, 2025,
    [[https://stepinto.vision/articles/deep-dive-into-manipulation-on-visionos/]{.underline}](https://stepinto.vision/articles/deep-dive-into-manipulation-on-visionos/)

26. SpatialTapGesture \| Apple Developer Documentation, accessed
    November 24, 2025,
    [[https://developer.apple.com/documentation/SwiftUI/SpatialTapGesture]{.underline}](https://developer.apple.com/documentation/SwiftUI/SpatialTapGesture)

27. Detect gesture in immersive space VisionOs SwiftUI - Stack Overflow,
    accessed November 24, 2025,
    [[https://stackoverflow.com/questions/77712163/detect-gesture-in-immersive-space-visionos-swiftui]{.underline}](https://stackoverflow.com/questions/77712163/detect-gesture-in-immersive-space-visionos-swiftui)

28. Spatial SwiftUI: hoverEffect modifier - Step Into Vision, accessed
    November 24, 2025,
    [[https://stepinto.vision/example-code/spatial-swiftui-hovereffect-modifier/]{.underline}](https://stepinto.vision/example-code/spatial-swiftui-hovereffect-modifier/)

29. CustomHoverEffect \| Apple Developer Documentation, accessed
    November 24, 2025,
    [[https://developer.apple.com/documentation/SwiftUI/CustomHoverEffect]{.underline}](https://developer.apple.com/documentation/SwiftUI/CustomHoverEffect)

30. Eyes \| Apple Developer Documentation, accessed November 24, 2025,
    [[https://developer.apple.com/design/human-interface-guidelines/eyes]{.underline}](https://developer.apple.com/design/human-interface-guidelines/eyes)

31. Mastering FocusState property wrapper in SwiftUI - Swift with Majid,
    accessed November 24, 2025,
    [[https://swiftwithmajid.com/2021/08/24/mastering-focusstate-property-wrapper-in-swiftui/]{.underline}](https://swiftwithmajid.com/2021/08/24/mastering-focusstate-property-wrapper-in-swiftui/)

32. How to detect pushing both of attachment view and spatial tap
    gesture - Reddit, accessed November 24, 2025,
    [[https://www.reddit.com/r/visionosdev/comments/1ezumz7/how_to_detect_pushing_both_of_attachment_view_and/]{.underline}](https://www.reddit.com/r/visionosdev/comments/1ezumz7/how_to_detect_pushing_both_of_attachment_view_and/)

33. Recognizing a multitouch gesture with SwiftUI - Stack Overflow,
    accessed November 24, 2025,
    [[https://stackoverflow.com/questions/74475743/recognizing-a-multitouch-gesture-with-swiftui]{.underline}](https://stackoverflow.com/questions/74475743/recognizing-a-multitouch-gesture-with-swiftui)

34. FocusedValues in SwiftUI - Shadowfacts, accessed November 24, 2025,
    [[https://shadowfacts.net/2025/focused-values/]{.underline}](https://shadowfacts.net/2025/focused-values/)

35. Creating advanced hover effects in visionOS - Create with Swift,
    accessed November 24, 2025,
    [[https://www.createwithswift.com/creating-advanced-hover-effects-in-visionos/]{.underline}](https://www.createwithswift.com/creating-advanced-hover-effects-in-visionos/)

36. Small modifier I found with the SwiftUI Menu. When a user taps
    instead of long press of a menu, you can have the menu act as a
    button. Long pressing then shows the menu actions. Been here since
    iOS 15 apparently - Reddit, accessed November 24, 2025,
    [[https://www.reddit.com/r/SwiftUI/comments/1i5hxlm/small_modifier_i_found_with_the_swiftui_menu_when/]{.underline}](https://www.reddit.com/r/SwiftUI/comments/1i5hxlm/small_modifier_i_found_with_the_swiftui_menu_when/)

37. Connection between WindowGroup and ImmersiveSpace Entity on
    visionOS, accessed November 24, 2025,
    [[https://stackoverflow.com/questions/78169409/connection-between-windowgroup-and-immersivespace-entity-on-visionos]{.underline}](https://stackoverflow.com/questions/78169409/connection-between-windowgroup-and-immersivespace-entity-on-visionos)

38. How to Address Common Accessibility Challenges in iOS Mobile Apps
    Using SwiftUI, accessed November 24, 2025,
    [[https://www.freecodecamp.org/news/how-to-address-ios-accessibility-challenges-using-swiftui/]{.underline}](https://www.freecodecamp.org/news/how-to-address-ios-accessibility-challenges-using-swiftui/)

39. Enabling Cross-Platform Touch Interactions: Pointer vs. Touch
    Events - Christian Liebel, accessed November 24, 2025,
    [[https://christianliebel.com/2015/05/enabling-cross-platform-touch-interactions-pointer-vs-touch-events/]{.underline}](https://christianliebel.com/2015/05/enabling-cross-platform-touch-interactions-pointer-vs-touch-events/)
