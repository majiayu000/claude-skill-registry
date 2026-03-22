---
name: "per-user-wix-msi-packaging"
description: "Package a WPF desktop app as a repo-buildable per-user MSI with WiX SDK"
domain: "desktop-packaging"
confidence: "high"
source: "bishop-per-user-msi"
---

## Context

Use this when a Windows desktop app needs a real `.msi` artifact, must install without admin elevation, and the repo does not already have an installer project.

## Patterns

1. Add a dedicated WiX SDK project to the repo and wire it into the solution so MSI generation is a first-class build path.
2. Keep packaging self-contained in the installer project: build any web assets, publish the desktop project to a staging folder, and harvest that staged payload instead of hand-copying binaries.
3. For WPF/WebView2 apps that ship placeholder web content in `WebApp`, overwrite the published `WebApp` folder with the real built `dist` output before packaging so installed bits do not fall back to placeholder UI.
4. Set the WiX package scope to `perUser` and install under a user-writable path such as `%LocalAppData%\Programs\{Product}`.
5. Add only user-scoped shell integration (for example, Start Menu shortcuts backed by `HKCU` key paths) so the installer stays non-admin.
6. Expect legacy MSI ICE validation noise when harvesting many files into a user-profile root; document and suppress the specific ICEs you intentionally accept rather than moving the install to a machine-wide folder.
7. If the installer publishes the desktop project directly, framework retargets usually belong in the application/test projects, not the WiX project; verify the staged publish output by checking `obj\desktop-publish\*.runtimeconfig.json` for the expected `runtimeOptions.tfm`.
8. If distribution must be a single `.msi`, do not rely on `Compressed="yes"` alone—set `<MediaTemplate EmbedCab="yes" />` so WiX embeds `cab1.cab` into the MSI instead of writing a sidecar cabinet. Validate by checking the release folder has no external `.cab` and, if needed, confirm the MSI `Media.Cabinet` value is `#cab1.cab`.
9. When the desktop app needs branding, generate one canonical multi-resolution `.ico` and reuse that exact file everywhere: WPF `<ApplicationIcon>` for the built `.exe`, `Window.Icon` for taskbar/Alt+Tab/native shell pickup, any custom titlebar image bound to `Window.Icon`, and WiX `<Icon>` + `ARPPRODUCTICON`/shortcut `Icon` so installer and uninstall surfaces stay consistent with the shipped executable.
10. For rebuild-only validation, prove the latest WebUI actually ships in the MSI with a two-step check: compare hashes between `src\PanelNester.WebUI\dist` and `installer\PanelNester.Installer\obj\desktop-publish\WebApp`, then query the built MSI `File` table through the Windows Installer COM API to confirm every current dist asset filename is present in the package.

## Examples

- `installer\PanelNester.Installer\PanelNester.Installer.wixproj`
- `installer\PanelNester.Installer\Product.wxs`
- `dotnet build .\installer\PanelNester.Installer\PanelNester.Installer.wixproj -c Release -nologo`
- `installer\PanelNester.Installer\obj\desktop-publish\PanelNester.Desktop.runtimeconfig.json`

## Anti-Patterns

- Requiring a manual Visual Studio publish step before the MSI can be built
- Packaging the desktop publish output without replacing placeholder `WebApp` content with the real web build
- Using `Program Files` for a supposedly per-user MSI
- Treating WiX ICE suppression as a default instead of a documented, intentional tradeoff tied to per-user harvested payloads
