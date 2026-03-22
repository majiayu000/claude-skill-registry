---
name: "project-conventions"
description: "Core conventions and patterns for PanelNester codebase"
domain: "project-conventions"
confidence: "high"
source: "design-review"
---

## Context

PanelNester is a WPF desktop app with a WebView2-hosted React UI. Domain logic lives in .NET; visualization in TypeScript/React/Three.js.

## Patterns

### Bridge Communication

All WPF↔WebView2 communication uses JSON-over-postMessage with type/payload envelope:

```typescript
interface BridgeMessage {
  type: string;
  requestId?: string;
  payload: unknown;
}
```

- WPF dispatches by `type` without deserializing `payload` first
- Use `requestId` for request/response correlation
- Keep payloads serializable (no functions, circular refs)

### Domain Isolation

Domain project has zero dependencies on WPF, WebView2, or persistence:
- Models in `PanelNester.Domain/Models/`
- Contracts (interfaces) in `PanelNester.Domain/Contracts/`
- Services implement contracts in `PanelNester.Services/`

### Error Handling

- Domain returns result objects with `success`, `errors`, `warnings` arrays
- Bridge handlers catch exceptions and return error responses
- WebUI displays validation messages inline, critical errors as toasts

### Testing

- Framework: xUnit for .NET, Vitest for TypeScript
- Location: `tests/PanelNester.*.Tests/` for .NET, `src/PanelNester.WebUI/src/**/*.test.ts` for TS
- Run: `dotnet test` for .NET, `npm test` in WebUI directory

### Code Style

- .NET: C# 12, nullable enabled, file-scoped namespaces
- TypeScript: Strict mode, no `any` without justification
- Naming: PascalCase for .NET public members, camelCase for TS

### File Structure

```
src/
├── PanelNester.Desktop/    # WPF shell, bridge
├── PanelNester.Domain/     # Pure models, interfaces
├── PanelNester.Services/   # Application services
└── PanelNester.WebUI/      # React frontend
tests/
├── PanelNester.Domain.Tests/
├── PanelNester.Services.Tests/
└── PanelNester.Desktop.Tests/
```

## Examples

```csharp
// Bridge handler registration
handlers.Register("import-csv", async (payload) => {
    var request = Deserialize<ImportRequest>(payload);
    var result = await importService.ImportAsync(request.FilePath);
    return new ImportResponse(result);
});
```

```typescript
// Calling .NET from React
const result = await hostBridge.invoke<NestResponse>('run-nesting', {
  parts: validParts,
  material: selectedMaterial,
  kerfWidth: 0.125
});
```

## Anti-Patterns

- **Domain depending on WPF** — Keep domain pure; inject dependencies via interfaces.
- **Binary payloads over bridge** — Stick to JSON; no ArrayBuffer or Blob.
- **Tight coupling between pages** — Use shared types from `contracts.ts`, not direct imports across pages.
- **Hardcoding file paths** — Always use bridge to request native file dialogs.
