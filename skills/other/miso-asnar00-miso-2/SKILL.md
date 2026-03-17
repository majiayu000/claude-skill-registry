---
name: miso
description: Implement feature changes by updating pseudocode, platform code, and product code from modified feature markdown files. Use when user asks to "implement features", "run miso", "update implementations", or "sync code with features".
---

# Miso Implementation Skill

## Overview

This skill implements the miso feature-to-code workflow. When feature markdown files change, it automatically propagates those changes through the implementation chain: pseudocode → platform-specific code → product code.

## Understanding Miso Features

Miso specifies programs as a tree of **features**: short (<300 word) natural-language markdown files that specify behavior.

**Feature Format**:
- Start with a `#` title
- Followed by an *emphasized* one-line summary
- Up to 300 words of natural language
- Use simple language understandable by users
- Avoid technical jargon and code

**Feature Structure**:
Each feature lives in its own folder containing:
- `spec.md`: The feature specification
- `pseudocode.md`: Natural-language function definitions and patching instructions
- `ios.md`, `android.md`, `py.md`: Platform-specific implementations with actual code
- `imp/`: Folder for other artifacts (logs, debugging notes, test data)

**Feature Hierarchy**:
- To add detail to feature `A/spec.md`, create subfeature `A/B/spec.md`
- To add detail to `A/B/spec.md`, create subfeature `A/B/C/spec.md`
- Keep manageable: no more than 4-6 children per feature
- Group and summarize if children get out of control

## The Implementation Process

When a user changes feature `A/B/spec.md` or adds a subfeature, the implementation process ensures code is created following this routine:

**Step 1: Pseudocode**
- Check if `A/B/pseudocode.md` is up-to-date
- If not, ensure changes to the feature are reflected in pseudocode
- Pseudocode uses natural language function definitions
- Include patching instructions (where/how to integrate into product)

**Step 2: Platform Code**
- Check if platform implementations (`ios.md`, `android.md`, etc.) are up-to-date vs pseudocode
- If not, edit them to reflect the most recent pseudocode changes
- Use platform-appropriate actual code syntax (Swift, Kotlin, Python)

**Step 3: Product Code**
- Check if actual target product code is up-to-date vs platform implementations
- If not, make appropriate modifications to product code
- Follow patching instructions from platform implementation files

**Step 4: Build, Deploy, Test**
- Build and deploy the changed feature to devices/servers
- Run tests if available

## When to Use

Invoke this skill when the user:
- Says "implement features" or "run miso"
- Asks to "update implementations" or "sync code"
- Mentions implementing or deploying feature changes
- Wants to propagate feature changes to code

## Implementation Workflow

The miso implementation process follows this sequence:

### 1. Detect Changed Features

Find all feature `spec.md` files that have changed since the last run:
- Use `git diff` to find modified feature files in `apps/` and `miso/` directories
- Look for files matching pattern `**/spec.md`
- Track the last run timestamp (stored in `.claude/skills/miso/.last-run`)

### 2. Update Pseudocode

For each changed feature `A/B/spec.md`:
- Check if `A/B/pseudocode.md` exists
- If it exists, read both the spec and pseudocode
- Determine if pseudocode needs updating based on spec changes
- If needed, update `A/B/pseudocode.md` to reflect the spec changes
- Use natural language function definitions and patching instructions

### 3. Update Platform Implementations

For each feature with updated pseudocode:
- Check for platform-specific implementations: `A/B/ios.md`, `A/B/android.md`, `A/B/py.md`
- For each existing platform file:
  - Read the pseudocode and platform implementation
  - Determine if platform code needs updating
  - Update platform implementation to match pseudocode
  - Use actual code syntax appropriate for the platform (Swift, Kotlin, Python)

### 4. Update Product Code

For each updated platform implementation:
- Identify the target product (look in `apps/` hierarchy to find the product path)
- Read the patching instructions from the platform implementation
- Locate the actual product code files that need modification
- Apply the changes to product code following the patching instructions
- Make minimal, targeted edits to existing code

### 5. Build, Deploy, and Test

After updating product code:
- Determine which platform was modified (iOS, Android, Python)
- Build and deploy using appropriate scripts:
  - iOS: `./install-device.sh` from product client imp/ios directory
  - Android: `export JAVA_HOME="/opt/homebrew/opt/openjdk" && ./gradlew assembleDebug && adb install -r app/build/outputs/apk/debug/app-debug.apk`
  - Python: `./remote-shutdown.sh && scp && ssh` for remote server deployment
- If a test exists for the feature, run it using `./test-feature.sh <feature-name>`

### 6. Visual Verification and Iterative Debugging (for UI changes)

For features that affect visual appearance (colors, layouts, UI elements), use an **iterative debugging cycle**:

**iOS Visual Verification Cycle**:

1. **Take Screenshot**:
   ```bash
   cd apps/firefly/product/client/imp/ios
   ./restart-app.sh
   sleep 3
   cd /Users/asnaroo/Desktop/experiments/miso/miso/platforms/ios/development/screen-capture/imp
   ./screenshot.sh /tmp/verification-screenshot.png
   ```

2. **Verify Against Specification**:
   - Read the screenshot image
   - Compare what you see to what the feature specification says
   - For color changes: Check if expected color is visible
   - For layout changes: Check if elements are positioned correctly
   - For UI elements: Check if components appear as specified

3. **If Verification PASSES**:
   - Proceed to step 7 (Update Implementation Documentation)

4. **If Verification FAILS**:
   - **Investigate**: Search for ALL files that might contain the old implementation
   - **Example**: For background color, search: `grep -r "Color(red: 64/255" NoobTest/`
   - **Discovery**: You may find the change is needed in multiple files, not just the ones initially updated
   - **Document findings**: Note which files were missed

5. **Fix All Instances**:
   - Update ALL files that need the change
   - Rebuild: `./install-device.sh`
   - Restart: `./restart-app.sh && sleep 3`
   - **Take another screenshot**
   - Read and verify again

6. **Iterate Until Success**:
   - Repeat steps 4-5 until visual verification passes
   - Don't stop at the first failed attempt
   - Each failure teaches you about files that need updating

**Android Visual Verification Cycle**:
1. Restart: `adb shell am force-stop com.miso.noobtest && adb shell am start -n com.miso.noobtest/.MainActivity`
2. Wait: `sleep 3`
3. Screenshot: `adb exec-out screencap -p > /tmp/verification-screenshot.png`
4. Read and verify (same logic as iOS)
5. If fails: Search for missed files, fix, rebuild, repeat

**Key Insight**: Initial implementation often misses files. Visual verification catches this and drives iteration until the visible result matches the specification.

### 7. Post-Debug Cleanup

After visual verification succeeds and the feature works correctly, **update all documentation to accurately reflect what was actually built**. This is critical because the initial implementation often differs from the final working version due to debugging discoveries.

**Run the post-debug cleanup process:**

1. **Review what was actually changed**:
   ```bash
   git diff apps/firefly/product/client/imp/ios/
   ```

2. **Update the feature specification** (`spec.md`):
   - Ensure user-facing description matches final behavior
   - Update visual details (exact colors, sizes, positions)
   - Describe final gesture interactions (thresholds discovered during debugging)
   - Keep <300 words, user-focused language

3. **Update the pseudocode** (`pseudocode.md`):
   - Capture exact specifications discovered during debugging:
     - Gesture thresholds (e.g., "30pt minimum for left swipe", "100pt for right swipe")
     - UI measurements (e.g., "32pt icon with -8pt trailing padding")
     - API endpoints with correct paths and response formats
     - Visual specs (exact RGB values, font sizes, weights)
   - Update patching instructions to reflect ALL files that need changes
   - Include data structures that were added (e.g., new response types)

4. **Update platform implementations** (`ios.md`, `android.md`, etc.):
   - Replace stub code with complete, working code from actual product files
   - Include ALL target files that needed changes (discovered during debugging)
   - Add exact file paths and line numbers
   - Document any platform-specific workarounds (e.g., `.highPriorityGesture` for SwiftUI)
   - Include complete API response structures with correct field names

5. **Example Updates**:

   **Feature spec (`explore-posts/spec.md`)**:
   ```markdown
   **Navigate to Children**: Swipe left on a post with children to navigate to a view showing all its child posts.

   **Navigate Back**: Either tap the back button or swipe right anywhere in the child view to return to the parent view.
   ```

   **Pseudocode (`explore-posts/pseudocode.md`)**:
   ```markdown
   ## Gesture Handling

   **Swipe Left on Post with Children:**
   - Minimum distance: 30pt
   - Condition: Post must have children (childCount > 0)

   **Swipe Right in Child View:**
   - Minimum distance: 100pt
   - Start position: Anywhere in view (not just left edge)
   - Priority: High priority gesture to override ScrollView
   ```

   **Platform spec (`explore-posts/ios.md`)**:
   ```swift
   // Complete working code with exact measurements
   .gesture(
       DragGesture(minimumDistance: 30)
           .onEnded { value in
               if value.translation.width < -30 && (post.childCount ?? 0) > 0 {
                   onNavigateToChildren?(post.id)
               }
           }
   )

   // In ChildPostsView - swipe right from anywhere
   .highPriorityGesture(
       DragGesture()
           .onEnded { value in
               if value.translation.width > 100 {
                   navigationPath.removeLast()
               }
           }
   )
   ```

6. **Why This Matters**:
   - Next time miso runs, the documentation will generate complete, working code immediately
   - All debugging discoveries (exact thresholds, workarounds, edge cases) are preserved
   - Another developer can implement the feature correctly from the docs
   - If product code is deleted, specs can rebuild it without re-debugging
   - The implementation documentation becomes an accurate, tested source of truth

## State Tracking

Store the last run timestamp in `.claude/skills/miso/.last-run`:
- Before starting, read this file to get the baseline for comparison
- After successful completion, update it with the current timestamp
- If the file doesn't exist, compare against the last git commit

## Key Principles

1. **Incremental**: Only process features that have actually changed
2. **Chain of Trust**: Each level (pseudocode → platform → product) builds on the previous
3. **Minimal Edits**: Make targeted changes to existing code, don't rewrite unnecessarily
4. **Verify Visually**: For UI changes, take screenshots and iterate until the result matches the spec
5. **Learn from Failures**: Each visual verification failure reveals files that were missed
6. **Update Documentation**: Capture all discovered changes in implementation files so next time is complete
7. **Track State**: Remember what was last processed to avoid redundant work

## Example Workflow

User modifies `apps/firefly/features/background/spec.md` (changes color from turquoise to mauve):

1. **Detect**: `background/spec.md` changed since last run
2. **Update Pseudocode**: `apps/firefly/features/background/pseudocode.md` to reflect mauve color
3. **Update Platform Spec**: `apps/firefly/features/background/ios.md` with new RGB values
4. **Update Product Code**: Initial change to `ContentView.swift` with RGB(224, 176, 255)
5. **Build & Deploy**: `./install-device.sh`
6. **Visual Verify (Attempt 1)**:
   - Restart app, take screenshot
   - **FAILS**: Still shows turquoise
   - Investigation: App is showing PostsView, not ContentView!
7. **Fix & Rebuild**:
   - Update `PostsView.swift` with mauve color
   - Rebuild and redeploy
8. **Visual Verify (Attempt 2)**:
   - Take screenshot again
   - **SUCCESS**: Shows mauve background
9. **Search for Remaining Instances**:
   - `grep -r "Color(red: 64/255" NoobTest/`
   - Find 5 more files with old color
10. **Post-Debug Cleanup**:
    - Edit `background/spec.md`: Describe grey/dark-red colors as user sees them
    - Edit `background/pseudocode.md`: Add exact RGB values (128,128,128) and (139,0,0)
    - Edit `background/ios.md`: List all 6 target files with line numbers and complete code examples
    - Include search pattern: "Search for all instances of `Color(red:` and replace..."
11. **Test**: Run `./test-feature.sh background` if test exists
12. **Track**: Update `.last-run` timestamp

**Result**: The documentation now accurately reflects the final implementation. All 6 files are documented with exact values. Next time miso runs, it will update all 6 files on the first attempt, with no debugging needed.

## Important Notes

- Always read before writing - understand existing code structure
- Follow platform conventions (SwiftUI for iOS, Jetpack Compose for Android)
- Respect the JAVA_HOME requirement for Android builds
- Use LD="clang" for iOS builds to avoid Homebrew linker issues
- Check git status to understand what changed in the working directory
