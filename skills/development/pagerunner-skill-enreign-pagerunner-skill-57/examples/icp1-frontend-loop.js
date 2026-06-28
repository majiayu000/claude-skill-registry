/**
 * ICP 1: Solo Developer
 *
 * Close the implementation loop: edit code → see result in browser → iterate
 *
 * Use this when developing a frontend locally (localhost:3000) and want Claude
 * to verify visual changes in real-time.
 *
 * Requirements:
 * - Pagerunner installed and registered with Claude Code
 * - Chrome browser with "personal" profile (or any profile you use for dev)
 * - A dev server running on localhost:3000 (or adjust URL below)
 */

async function verifyFrontendChange() {
  // 1. Open a session with your personal Chrome profile
  const sessionId = await open_session({
    profile: "personal"
  });

  // 2. Get the first open tab (or create one)
  const tabs = await list_tabs(sessionId);
  const tabId = tabs[0].target_id;

  // 3. Navigate to your local dev server
  await navigate(sessionId, tabId, "http://localhost:3000");

  // 4. Wait for the page to load (optional but recommended for React/Vue apps)
  await wait_for(sessionId, tabId, {
    selector: ".app-ready", // or any selector that indicates the app is loaded
    ms: 5000
  });

  // 5. Take a screenshot to verify the change
  const screenshot = await screenshot(sessionId, tabId);

  console.log("Screenshot saved to temp file or returned as base64");
  console.log("Claude can now verify: button color, layout, spacing, etc.");

  // 6. Close the session when done
  await close_session(sessionId);

  return screenshot;
}

/**
 * Real-world example: Verify button styling after CSS change
 *
 * Workflow:
 * 1. You edit button.css: color: red → color: green
 * 2. Dev server reloads (hot module replacement)
 * 3. Claude runs this script
 * 4. Screenshot shows the green button
 * 5. Claude confirms: "✓ Button is now green, padding looks good"
 */

// Call the function
// verifyFrontendChange()
//   .then(() => console.log("Verification complete"))
//   .catch(err => console.error("Error:", err));
