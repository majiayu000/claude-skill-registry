---
name: add-ui-tests
description: Add Selenium-based UI tests for NovaTune player and admin Vue SPAs against Aspire backend
user_invocable: true
arguments:
  - name: scope
    description: Test scope - player, admin, or both (default both)
    required: false
---

# Add UI Tests Skill

Add Selenium WebDriver + xUnit UI tests for NovaTune's Vue SPAs, running against an Aspire-hosted backend with Vite dev servers.

## Steps

1. **Read the execution plan** at `tasks/add_ui_tests/main_exec.md` for the full implementation specification including phases, code, and acceptance criteria.

2. **Read the planning doc** at `tasks/add_ui_tests/main.md` for architecture context and design rationale.

3. **Check current state** of the ui_tests directory and solution:
   - `ls src/ui_tests/` — check if project already exists
   - Check `src/NovaTuneApp/NovaTuneApp.sln` for existing ui_tests entries
   - Check Vue components for existing `data-testid` attributes

4. **Execute phases sequentially** as defined in `main_exec.md`:
   - Phase 0: Add `data-testid` attributes to Vue components
   - Phase 1: Bootstrap the xUnit + Selenium project
   - Phase 2: Create fixtures (UiTestFixture, WebDriverFactory, UiTestBase)
   - Phase 3: Player UI tests (auth, library, playlists)
   - Phase 4: Admin UI tests (auth, dashboard)
   - Phase 5: Gitignore + cleanup
   - Phase 6: Verify full suite

5. **Verify each phase** passes its acceptance criteria before proceeding.

## Key Patterns

### Project Structure
```
src/ui_tests/NovaTuneApp.UiTests/
    Fixtures/
        UiTestFixture.cs          # Aspire host + Vite processes + data seeding
        WebDriverFactory.cs       # ChromeDriver creation (headless by default)
        TestCollections.cs        # xUnit collection definition
    Infrastructure/
        WaitHelpers.cs            # Explicit waits (never Thread.Sleep)
        ScreenshotHelper.cs       # Screenshot on failure
        UiTestBase.cs             # Base class with driver lifecycle + login helpers
    Player/
        PlayerAuthTests.cs        # Login, register, redirect, error states
        PlayerLibraryTests.cs     # Track listing, empty state
        PlayerPlaylistsTests.cs   # Create playlist, empty state
    Admin/
        AdminAuthTests.cs         # Admin login, non-admin rejection, register
        AdminDashboardTests.cs    # Stat cards, sidebar navigation
```

### Test Convention
- Collection: `[Collection("UI Tests")]` — shared fixture, no parallel execution
- Traits: `[Trait("Category", "UI")]`, `[Trait("App", "Player")]` or `[Trait("App", "Admin")]`
- Base class: `UiTestBase` handles ChromeDriver lifecycle, `ClearDataAsync()`, screenshot-on-failure
- Login helpers: `PlayerLogin(email, password)` and `AdminLogin(email, password)` in base class
- Selectors: Prefer `data-testid` via `WaitHelpers.WaitForTestId()`, fall back to text via `WaitHelpers.WaitForText()`
- No `Thread.Sleep` — only explicit WebDriverWait via `WaitHelpers`

### Fixture Lifecycle
- `UiTestFixture` (collection-level): Starts Aspire + 2 Vite servers once per test run
- `UiTestBase` (per-class): Creates fresh ChromeDriver, clears DB, captures screenshot on failure
- Vite ports: 26173 (player), 26174 (admin) — offset from dev ports to avoid conflicts
- `VITE_API_BASE_URL` injected into Vite processes pointing to test API

### Data Seeding
- `SeedUserAsync(email, displayName, password)` — register via API
- `SeedAdminUserAsync(email, displayName, password)` — register + grant Admin role via RavenDB
- `SeedTracksForUserAsync(userId, count)` — batch insert Track documents
- `ClearDataAsync()` — wipe all users, tracks, playlists, audit logs

### data-testid Conventions
- Auth forms: `email`, `password`, `login-button`, `register-button`, `displayName`, `confirmPassword`
- Error states: `error-message`, `success-message`
- Page headings: `library-heading`, `playlists-heading`, `dashboard-heading`
- Empty states: `empty-state`
- Interactive: `create-playlist-button`, `playlist-name-input`, `playlist-submit-button`
- Lists: `track-list`

## Commands

```bash
# Build
dotnet build src/ui_tests/NovaTuneApp.UiTests/NovaTuneApp.UiTests.csproj

# Run all UI tests
dotnet test src/ui_tests/NovaTuneApp.UiTests/NovaTuneApp.UiTests.csproj -c Debug

# Player only
dotnet test src/ui_tests/NovaTuneApp.UiTests/NovaTuneApp.UiTests.csproj -c Debug \
  --filter "Trait=App&Value=Player"

# Admin only
dotnet test src/ui_tests/NovaTuneApp.UiTests/NovaTuneApp.UiTests.csproj -c Debug \
  --filter "Trait=App&Value=Admin"

# Headed mode (see browser)
UI_TESTS_HEADED=1 dotnet test src/ui_tests/NovaTuneApp.UiTests/NovaTuneApp.UiTests.csproj -c Debug

# Frontend lint/typecheck after adding data-testid
cd src/NovaTuneClient && pnpm lint && pnpm typecheck
```

## Prerequisites

- Docker/Podman running (for Aspire infrastructure containers)
- Chrome/Chromium installed (Selenium Manager handles chromedriver)
- `pnpm install` completed in `src/NovaTuneClient/`
- .NET 9 SDK installed
