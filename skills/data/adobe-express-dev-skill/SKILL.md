---
name: adobe-express-dev
description: 'Expert guidance for Adobe Express add-on development using Document APIs, Add-on UI SDK, and Document Sandbox. Use when building Adobe Express extensions, creating add-ons, working with express-document-sdk, implementing document manipulation, designing add-on UIs with Spectrum Web Components, troubleshooting iframe/sandbox communication, or accessing Adobe Express documentation and API references via MCP server.'
---

# Adobe Express Add-on Development Skill

Expert knowledge and tooling for developing Adobe Express add-ons. This skill leverages the Adobe Express MCP server to provide accurate, up-to-date API references, documentation, and best practices.

## When to Use This Skill

Use this skill when:
- **Building add-ons** for Adobe Express
- **Creating or modifying document content** (shapes, text, images, media)
- **Implementing UI panels** with Spectrum Web Components
- **Setting up communication** between iframe runtime and document sandbox
- **Troubleshooting** add-on development issues
- **Understanding project structure** and file organization
- **Accessing API documentation** for Express Document SDK or Add-on UI SDK
- **Working with OAuth**, client storage, or add-on permissions
- User mentions: "Adobe Express", "add-on", "express-document-sdk", "document sandbox", "iframe runtime", "Spectrum Web Components"

## Prerequisites

- **Adobe Express MCP Server** must be configured in `.vscode/mcp.json` or IDE settings
- **Node.js 18+** for local development
- **Basic understanding** of HTML, CSS, and JavaScript
- **Adobe Express account** for testing add-ons

## Key Concepts

### Two-Runtime Architecture

Adobe Express add-ons run in **two separate environments**:

1. **Iframe Runtime**
   - Runs your UI (HTML, CSS, JavaScript)
   - Has access to Add-on UI SDK (`addOnUISdk`)
   - Can use standard Web APIs and DOM
   - Handles user interactions, OAuth, file imports/exports

2. **Document Sandbox** (optional)
   - Runs document manipulation code
   - Has access to Express Document SDK (`editor`, `colorUtils`, `constants`, etc.)
   - Limited Web APIs for security
   - Creates/modifies shapes, text, images, audio, video

**Communication**: Use Document Sandbox SDK (`runtime.exposeApi()`, `runtime.apiProxy()`) to bridge between the two.

### Import Patterns

**Always follow these patterns:**

```javascript
// Iframe Runtime (index.html, index.js, ui/ folder)
import addOnUISdk from "https://express.adobe.com/static/add-on-sdk/sdk.js";

// Document Sandbox (code.js, sandbox/code.js)
import addOnSandboxSdk from "add-on-sdk-document-sandbox";
import { editor, colorUtils, constants, fonts, viewport } from "express-document-sdk";
```

**Critical**: 
- Add-on UI SDK and Document Sandbox SDK are **default imports** (no curly braces)
- Express Document SDK uses **named imports** (with curly braces)
- All SDKs use **singleton pattern** - never create new instances

## Step-by-Step Workflows

### Workflow 1: Access API Documentation

**When you need**: API references, type definitions, or documentation for Adobe Express add-on development.

**Steps**:
1. Use `mcp_adobe-express_get_relevant_documentations` tool with your query
2. Review the returned documentation snippets
3. For TypeScript definitions, use `mcp_adobe-express_get_typedefinitions` with appropriate `api_type`:
   - `express-document-sdk` - Document manipulation APIs
   - `add-on-sdk-document-sandbox` - Communication between runtimes
   - `iframe-ui` - UI SDK and iframe runtime APIs

**Example queries**:
- "How to create text in Adobe Express"
- "Document sandbox communication APIs"
- "Add-on manifest configuration"
- "Spectrum Web Components usage in add-ons"

### Workflow 2: Understand Project Structure

**When you need**: To organize files, understand folder structure, or set up a new add-on.

**Key principles**:
- **UI code** (HTML, CSS, JS) → Iframe runtime (`src/index.html`, `src/ui/`)
- **Document manipulation** → Document sandbox (`src/sandbox/code.js`)
- **Never mix**: UI code cannot go in sandbox, sandbox code cannot access DOM

**Typical structure**:
```
my-addon/
├── src/
│   ├── index.html              # UI entry point
│   ├── manifest.json           # Add-on config
│   ├── ui/
│   │   ├── index.js           # UI logic
│   │   └── styles.css         # Styles
│   └── sandbox/
│       └── code.js            # Document manipulation
├── webpack.config.js           # Build config (if using build templates)
└── package.json
```

**Manifest configuration**:
- UI-only: `"main": "index.html"`
- With document sandbox: Add `"documentSandbox": "code.js"` (build) or `"sandbox/code.js"` (no-build)

### Workflow 3: Create Document Content

**When you need**: To add shapes, text, images, audio, or video to Adobe Express documents.

**Steps**:
1. Ensure code runs in **document sandbox** (not iframe runtime)
2. Import necessary modules from `express-document-sdk`
3. Use `editor` singleton for document operations
4. Wrap operations in async functions

**Common APIs**:
```javascript
// Text
import { editor, text } from "express-document-sdk";
const textNode = text.createText({content: "Hello", fontSize: 24});
editor.context.insertionParent.children.append(textNode);

// Shapes
import { editor, RectangleNode } from "express-document-sdk";
const rect = editor.createRectangle();
rect.width = 100;
rect.height = 50;

// Images
import addOnUISdk from "https://express.adobe.com/static/add-on-sdk/sdk.js";
const blob = await fetch(imageUrl).then(r => r.blob());
await addOnUISdk.app.document.addImage(blob);

// Audio (title is MANDATORY)
await addOnUISdk.app.document.addAudio(audioBlob, {
  title: "Audio Title"
});

// Video (title is OPTIONAL)
await addOnUISdk.app.document.addVideo(videoBlob, {
  title: "Video Title"
});
```

### Workflow 4: Build Add-on UI with Spectrum

**When you need**: To create user interfaces that match Adobe Express design language.

**Steps**:
1. Use [Spectrum Web Components](https://opensource.adobe.com/spectrum-web-components/)
2. Import components in HTML or via npm
3. Follow [UX Guidelines](https://developer.adobe.com/express/add-ons/docs/guides/build/design/ux_guidelines/)

**Common components**:
- `<sp-button>` - Buttons
- `<sp-textfield>` - Input fields
- `<sp-dropdown>` - Dropdowns
- `<sp-divider>` - Dividers
- `<sp-progress-circle>` - Loading indicators

**Example**:
```html
<sp-theme theme="express" scale="medium" color="light">
  <sp-button variant="primary" onclick="handleClick()">
    Click Me
  </sp-button>
  <sp-textfield placeholder="Enter text..."></sp-textfield>
</sp-theme>
```

### Workflow 5: Implement OAuth Authentication

**When you need**: To connect to cloud storage services (Dropbox, OneDrive, Google Drive) or authenticate users.

**Quick start**:
1. Read `references/oauth-implementation.md` for complete guide
2. Copy [OAuthUtils.js](https://github.com/AdobeDocs/express-add-on-samples/blob/main/samples/import-images-using-oauth/src/utils/OAuthUtils.js) from import-images-using-oauth sample
3. See `references/code-samples.md` → "import-images-using-oauth" for full example

**Steps**:
1. **Configure OAuth provider** (e.g., Dropbox Developer Console)
   - Create web application
   - Add redirect URIs: `https://express.adobe.com/static/oauth-redirect.html` AND `https://new.express.adobe.com/static/oauth-redirect.html`
   - Note Client ID

2. **Update manifest.json**:
```json
{
  "permissions": {
    "oauth": ["www.dropbox.com", "login.microsoftonline.com"]
  }
}
```

3. **Implement PKCE flow**:
```javascript
import addOnUISdk from "https://express.adobe.com/static/add-on-sdk/sdk.js";
// Import OAuthUtils helper (copy from sample)

// Generate PKCE challenge
const challenge = await oauthUtils.generateChallenge();

// Authorize with provider
const { id, code, redirectUri, result } = await addOnUISdk.app.oauth.authorize({
  authorizationUrl: "https://www.dropbox.com/oauth2/authorize",
  clientId: "YOUR_CLIENT_ID",
  scope: "files.content.read",
  codeChallenge: challenge.codeChallenge
});

// Exchange for access token
await oauthUtils.generateAccessToken({
  id, clientId: "YOUR_CLIENT_ID",
  codeVerifier: challenge.codeVerifier,
  code, tokenUrl: "https://api.dropboxapi.com/oauth2/token",
  redirectUri
});

// Get token (always valid - handles refresh)
const accessToken = await oauthUtils.getAccessToken(id);
```

4. **Store tokens persistently**:
```javascript
await addOnUISdk.instance.clientStorage.setItem("oauth_token", accessToken);
```

**Reference**: See `references/oauth-implementation.md` for provider configs, error handling, and logout patterns.

### Workflow 6: Implement Iframe ↔ Sandbox Communication

**When you need**: To pass data between UI and document manipulation code.

**Pattern**:

**In Document Sandbox (code.js)**:
```javascript
import addOnSandboxSdk from "add-on-sdk-document-sandbox";

const api = {
  async addTextToDocument(text) {
    // Document manipulation logic
  }
};

addOnSandboxSdk.instance.runtime.exposeApi(api);
```

**In Iframe Runtime (index.js)**:
```javascript
import addOnUISdk from "https://express.adobe.com/static/add-on-sdk/sdk.js";

const sandboxApi = await addOnUISdk.instance.runtime.apiProxy("documentSandbox");
await sandboxApi.addTextToDocument("Hello World");
```

### Workflow 6: Implement Iframe ↔ Sandbox Communication

**When you need**: To pass data between UI and document manipulation code.

**Pattern**:

**In Document Sandbox (code.js)**:
```javascript
import addOnSandboxSdk from "add-on-sdk-document-sandbox";

const api = {
  async addTextToDocument(text) {
    // Document manipulation logic
  }
};

addOnSandboxSdk.instance.runtime.exposeApi(api);
```

**In Iframe Runtime (index.js)**:
```javascript
import addOnUISdk from "https://express.adobe.com/static/add-on-sdk/sdk.js";

const sandboxApi = await addOnUISdk.instance.runtime.apiProxy("documentSandbox");
await sandboxApi.addTextToDocument("Hello World");
```

### Workflow 7: Use Code Samples as Starting Points

**When you need**: Implementation examples, starter code, or best practices.

**Steps**:
1. Read `references/code-samples.md` to find relevant sample
2. Clone sample repo: `git clone https://github.com/AdobeDocs/express-add-on-samples.git`
3. Navigate to sample: `cd express-add-on-samples/samples/<sample-name>`
4. Install and run: `npm install && npm run build && npm run start`
5. Study the code and adapt to your needs

**Recommended samples**:
- **OAuth/Cloud Storage**: `import-images-using-oauth` (copy OAuthUtils.js!)
- **Data Persistence**: `use-client-storage`
- **Export Renditions**: `export-sample`
- **Audio Handling**: `audio-recording-addon`
- **React + Spectrum**: `swc-react-theme-sampler`
- **Vanilla JS**: `swc`

### Workflow 8: Debug Common Issues

**Issue**: `undefined` when accessing SDK properties
- **Solution**: Check import pattern (default vs named)
- Verify you're using the correct SDK for the runtime environment

**Issue**: "Cannot access DOM" in document sandbox
- **Solution**: Move DOM code to iframe runtime; pass data via communication APIs

**Issue**: API not working as expected
- **Solution**: Query MCP server for latest documentation
- Check if API is marked as experimental (requires manifest permissions)

**Issue**: Manifest errors
- **Solution**: Verify `"documentSandbox"` path matches your build setup
- No-build: `"sandbox/code.js"` (full path)
- Build: `"code.js"` (webpack output)

## Best Practices

1. **Always query MCP server** for latest API documentation before implementing features
2. **Separate concerns**: UI in iframe runtime, document manipulation in sandbox
3. **Use TypeScript definitions** for better IDE support and error catching
4. **Follow Spectrum design** for consistent user experience
5. **Test in Adobe Express** development mode early and often
6. **Handle errors gracefully** with user-friendly messages
7. **Respect permissions** - request only what you need in manifest.json
8. **Cache intelligently** - use ClientStorage for user preferences

## MCP Server Tools Available

| Tool | Purpose | Example Query |
|------|---------|---------------|
| `get_relevant_documentations` | Search Adobe Express docs | "How to create rectangles" |
| `get_typedefinitions` | Get TypeScript definitions | `api_type: "express-document-sdk"` |

## Common File Paths

- **Manifest**: `src/manifest.json`
- **Iframe UI**: `src/index.html`, `src/ui/index.js`
- **Document Sandbox**: `src/sandbox/code.js`
- **Styles**: `src/ui/styles.css` (never in sandbox)
- **Config**: `webpack.config.js`, `tsconfig.json`

## Troubleshooting

| Problem | Solution |
|---------|----------|
| MCP server not responding | Check `.vscode/mcp.json` configuration |
| Import errors | Verify default vs named import patterns |
| Runtime errors | Ensure code runs in correct environment (iframe vs sandbox) |
| API not found | Query MCP server for latest documentation |
| Build errors | Check webpack config and Node.js version (18+) |

## Bundled References

This skill includes detailed reference documentation in the `references/` folder:

### OAuth Implementation Guide
**File**: `references/oauth-implementation.md`

Complete OAuth 2.0 implementation guide with:
- PKCE flow step-by-step
- OAuthUtils.js helper module documentation
- Provider configurations (Dropbox, OneDrive, Google Drive, Box)
- Token storage patterns
- Login/logout UI examples
- Error handling patterns

**Use when**: Implementing OAuth authentication, cloud storage integration, or user authentication.

### Code Samples Index
**File**: `references/code-samples.md`

Comprehensive catalog of 13 official Adobe Express add-on samples:
- **import-images-using-oauth** ⭐ - Complete OAuth + cloud storage example (COPY OAuthUtils.js from here!)
- **use-client-storage** - Data persistence patterns
- **export-sample** - Export renditions in multiple formats
- **audio-recording-addon** - Media handling
- **pix** - Advanced canvas-based editor
- Plus 8 more samples covering React, Vue, Spectrum, and more

**Use when**: Looking for implementation examples, starter code, or best practices.

## External References

- **Adobe Express Add-ons Docs**: [developer.adobe.com/express/add-ons](https://developer.adobe.com/express/add-ons/)
- **Spectrum Web Components**: [opensource.adobe.com/spectrum-web-components](https://opensource.adobe.com/spectrum-web-components/)
- **Code Samples Repository**: [github.com/AdobeDocs/express-add-on-samples](https://github.com/AdobeDocs/express-add-on-samples)
- **OAuthUtils.js Source**: [OAuthUtils.js](https://github.com/AdobeDocs/express-add-on-samples/blob/main/samples/import-images-using-oauth/src/utils/OAuthUtils.js)
- **Code Playground**: Test add-on code directly in Adobe Express
- **CLI Tool**: `npx @adobe/create-express-add-on` for scaffolding projects

## Quick Tips

- **Global await**: Only works in Code Playground Script Mode, not in actual add-ons
- **CSS location**: ALWAYS in iframe runtime, NEVER in document sandbox
- **Singleton SDKs**: Import once, use throughout - never instantiate
- **OAuth domains**: Add to `manifest.json` permissions before using
- **Audio API**: `title` parameter is MANDATORY
- **Video API**: `title` parameter is OPTIONAL
- **Build vs No-build**: Build templates support JSX, TypeScript, modern JavaScript
