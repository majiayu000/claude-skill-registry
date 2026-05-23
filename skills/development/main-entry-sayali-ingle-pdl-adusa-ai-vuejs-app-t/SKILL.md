---
name: main-entry
description: Generates src/main.ts application entry point. Creates different versions based on app type - micro-frontend with single-spa lifecycle or standalone SPA initialization.
---

# Main Entry Skill

## Purpose
Generate the application entry point file (`src/main.ts`). Creates different versions based on application architecture:
- **Micro-frontend**: Includes single-spa lifecycle methods and CSS isolation
- **Standalone**: Traditional Vue SPA initialization

## Input Parameters
- `application_type`: "micro-frontend" or "standalone"
- `application_id`: The application ID for CSS isolation and monitoring service name
- `enable_datadog`: Boolean to include Datadog RUM monitoring
- `state_management`: "vuex" or "pinia"

## Output
Create the file: `src/main.ts`

## Configuration Requirements

### Core Imports

#### Vue Essentials
- Import Vue's `createApp` function for application initialization
- For micro-frontends: Also import `h` (render function) for programmatic component rendering

#### Application Components
- Import root `App` component
- Import router instance from router configuration
- Import store instance (Vuex or Pinia depending on `state_management` parameter)

#### Monitoring (Optional)
If `enable_datadog` is true:
- Import Datadog RUM SDK
- Import environment constants for Datadog configuration (app ID, client token, environment, version)

#### Micro-Frontend Specific
If `application_type` is "micro-frontend":
- Import single-spa integration library for Vue
- Import application ID constant for CSS isolation

---

## Micro-Frontend Architecture

### Purpose
Enable the application to run as part of a larger single-spa ecosystem while maintaining CSS isolation and the ability to run independently.

### Single-SPA Lifecycle Setup

#### Lifecycle Configuration
Create lifecycle object using the single-spa Vue adapter with:

**App Options**
- Use render function to return the root App component
- Pass any necessary props to the App component

**Instance Handler**
- Register router plugin
- Register state management plugin (Vuex/Pinia)
- Register any other global plugins or configurations

#### Lifecycle Exports

**Bootstrap Export**
- Export the bootstrap lifecycle method
- Runs once when the micro-frontend is first loaded
- Initialize any one-time setup

**Mount Export**
- Export custom mount function
- **CSS Restoration Logic**:
  - Check if style tag with application ID exists in DOM
  - If exists and not cached: cache the style tag content
  - If doesn't exist but cached: recreate the style tag with cached content
  - Append style tag to document head
  - **Purpose**: Preserve CSS when navigating between micro-frontends
- Call the underlying single-spa mount lifecycle
- Application becomes active and visible

**Unmount Export**
- Export custom unmount function
- Call the underlying single-spa unmount lifecycle
- **CSS Cleanup Logic**:
  - Find and remove style tag with application ID from DOM
  - Keep cached version for restoration on next mount
  - **Purpose**: Prevent CSS conflicts with other micro-frontends
- Application becomes inactive

### CSS Isolation Strategy

**The Problem**: In micro-frontend architectures, multiple applications' CSS can conflict

**The Solution**: Style Tag Management
- Each micro-frontend has a unique style tag ID
- Cache style content on first mount
- Remove style tag on unmount (cleanup)
- Restore cached styles on remount (avoid re-download)
- Use unique ID derived from application identifier

**Key Concepts**:
- Styles are scoped by application
- No CSS pollution between micro-frontends
- Performance optimization through caching
- Seamless transitions between applications

### Standalone Fallback Mode

**Purpose**: Allow micro-frontend to run independently for development and testing

**Detection Logic**:
- Check if single-spa context exists (e.g., `window.singleSpaNavigate`)
- If single-spa is NOT present: mount application directly

**Fallback Initialization**:
- Create Vue app instance
- Register router plugin
- Register state management plugin
- Mount to DOM element (typically `#app`)

**Benefits**:
- Develop and test micro-frontend in isolation
- No need for full single-spa orchestrator during development
- Faster feedback loop
- Easier debugging

---

## Standalone Architecture

### Purpose
Traditional single-page application (SPA) with straightforward initialization.

### Application Initialization

**Create App Instance**
- Use `createApp` with root App component

**Register Plugins**
- Register router for navigation
- Register state management (Vuex/Pinia)
- Register any other global plugins

**Mount Application**
- Mount to DOM element (typically `#app`)
- Application becomes active immediately

**Key Differences from Micro-Frontend**:
- No lifecycle exports
- No CSS isolation logic
- No single-spa integration
- Simpler, more direct initialization

---

## Monitoring Integration (Optional)

### Datadog RUM Configuration

If `enable_datadog` is true, initialize Real User Monitoring:

#### Required Configuration

**Application Identification**
- Application ID: From environment variable
- Client Token: From environment variable (authentication)
- Site: Datadog site domain
- Service Name: Use `application_id` parameter for consistent identification
- Environment: From environment variable (dev, staging, prod)
- Version: Application version from package.json

#### Session Recording

**Sample Rates**
- Session Sample Rate: Percentage of sessions to track
- Session Replay Sample Rate: Percentage of sessions to record
- Start Manually: Control when recording starts (performance optimization)

#### Tracking Options

**User Interactions**
- Track clicks, form inputs, navigation
- Understand user behavior patterns

**Resources**
- Track API calls, asset loading
- Monitor performance and failures

**Long Tasks**
- Detect performance bottlenecks
- Identify slow operations

#### Privacy Settings

**Default Privacy Level**
- Mask sensitive user inputs
- Comply with privacy regulations
- Options: mask, mask-user-input, allow

**Experimental Features**
- Feature flags tracking
- A/B testing integration
- Enable as needed

### Monitoring Best Practices

- Initialize monitoring as early as possible in application lifecycle
- Use environment variables for configuration (never hardcode tokens)
- Set appropriate sample rates based on traffic volume
- Configure privacy settings according to compliance requirements
- Use service name consistently across all micro-frontends for correlation

---

## State Management Integration

### Vuex Integration
If `state_management` is "vuex":
- Import store from `./store` directory
- Store is typically a Vuex store instance with modules
- Register with `app.use(store)`

### Pinia Integration
If `state_management` is "pinia":
- Import Pinia instance from `./stores` directory
- Pinia is the modern, recommended state management for Vue 3
- Register with `app.use(pinia)`

### Key Differences
- **Vuex**: Module-based, mutations + actions pattern
- **Pinia**: Store-based, direct state mutation, better TypeScript support
- Both are registered the same way via `app.use()`

---

## Architecture Decision Logic

### When to Use Micro-Frontend Template

**Use Cases**:
- Part of a larger multi-application ecosystem
- Need to run alongside other micro-frontends
- Shared navigation/layout across multiple apps
- Team owns a specific domain/feature area
- Need independent deployment of features

**Requirements**:
- Single-spa orchestrator (root config)
- CSS isolation between applications
- Ability to run independently for development

### When to Use Standalone Template

**Use Cases**:
- Single application deployment
- Traditional SPA architecture
- No need for micro-frontend complexity
- Simpler deployment and hosting

**Benefits**:
- Simpler codebase
- Easier to understand
- Fewer dependencies
- Standard Vue patterns

---

## Validation

After generating the entry file:

### Micro-Frontend Validation
1. **Lifecycle Exports**: Verify bootstrap, mount, and unmount are exported
2. **CSS Isolation**: Confirm style tag is created with unique ID
3. **Standalone Mode**: Test that app runs without single-spa present
4. **Router Integration**: Verify navigation works in both modes
5. **Store Integration**: Confirm state management is accessible
6. **Monitoring**: Check Datadog RUM initializes if enabled

### Standalone Validation
1. **App Mounting**: Verify app mounts to DOM successfully
2. **Router Integration**: Test navigation works
3. **Store Integration**: Confirm state management is accessible
4. **Monitoring**: Check Datadog RUM initializes if enabled
5. **Console Errors**: Ensure no errors during initialization

---

## Best Practices

### Error Handling
- Wrap initialization in try-catch for production debugging
- Log errors to monitoring service
- Provide fallback UI for initialization failures

### Performance
- Initialize monitoring early but asynchronously if possible
- Lazy load non-critical plugins
- Keep main entry file focused and minimal

### Type Safety
- Use TypeScript for type checking
- Define types for single-spa lifecycle props
- Type environment constants properly

### Development Experience
- Support hot module replacement (HMR) in development
- Provide clear error messages for misconfiguration
- Enable source maps for debugging

---

## Philosophy

This entry file aims to:
- **Bootstrap the Application**: Initialize Vue and all necessary plugins
- **Support Multiple Architectures**: Work as micro-frontend or standalone SPA
- **Enable Monitoring**: Track performance and user behavior
- **Maintain Isolation**: Prevent conflicts in multi-app environments
- **Facilitate Development**: Allow independent development and testing
- **Stay Maintainable**: Clear, focused, easy to understand

---

## Future Compatibility

When Vue, single-spa, or monitoring tools evolve:
- Adopt new Vue initialization APIs as they become available
- Update single-spa integration to use modern lifecycle patterns
- Leverage improved CSS isolation techniques if introduced
- Update monitoring SDK to latest API versions
- Replace deprecated methods with modern equivalents
- Maintain core principles: clean initialization, proper lifecycle management, effective monitoring

---

## Common Variations

### Multiple Store Types
- May need to register multiple Pinia stores
- Could have both global and feature-specific stores
- Coordinate registration order if dependencies exist

### Additional Plugins
Consider registering:
- UI component libraries
- Icon libraries
- Form validation libraries
- Internationalization (i18n)
- Authentication plugins
- Custom directives

### Alternative Monitoring Solutions
- Google Analytics
- Sentry for error tracking
- Custom analytics solutions
- Application Performance Monitoring (APM) tools

### Environment-Specific Initialization
- Development: Enable debug tools, verbose logging
- Staging: Enable monitoring, disable debug tools
- Production: Full monitoring, error tracking, optimizations