---
name: webarchive
description: Extract .webarchive files (saved from Safari) into plain HTML/assets using the WebArchiveExtractor CLI. Use when the user wants to unarchive, extract, or convert a .webarchive file.
---

The user wants to extract a `.webarchive` file using WebArchiveExtractor.

If arguments were provided (`$ARGUMENTS`), use them to infer the input file and optionally the output directory or URL prepend. Otherwise, ask the user for the path to the `.webarchive` file.

## How to run WebArchiveExtractor

```
/Applications/WebArchiveExtractor.app/Contents/MacOS/WebArchiveExtractor [-h] [-o <OutputDirectory>] [-p <URLPrepend>] -i <WebArchiveFile>
```

**Options:**
- `-i <WebArchiveFile>` — **required** — path to the `.webarchive` file
- `-o <OutputDirectory>` — directory to write extracted files into (optional; defaults to a directory named after the archive next to it)
- `-p <URLPrepend>` — URI prefix to prepend to all asset URLs in the extracted HTML (optional; useful when serving the result from a subdirectory)

**Shorthand (no flag):**
```
WebArchiveExtractor website.webarchive
```
A positional argument is treated as the `-i` value.

## Prerequisites

The app must be installed at `/Applications/WebArchiveExtractor.app`. Check with:

```sh
test -x /Applications/WebArchiveExtractor.app/Contents/MacOS/WebArchiveExtractor && echo "found" || echo "not installed"
```

If not found, tell the user to build and install from source (`xcodebuild -project WebArchiveExtractor.xcodeproj`) or drag a release build to `/Applications`.

To use `WebArchiveExtractor` without the full path, the user can add it to `PATH`:

```sh
export PATH="$PATH:/Applications/WebArchiveExtractor.app/Contents/MacOS/"
```

Or create a symlink:

```sh
ln -s /Applications/WebArchiveExtractor.app/Contents/MacOS/WebArchiveExtractor ~/.local/bin/WebArchiveExtractor
```

## Steps

1. Check the binary exists using the test command above. If not found, stop and direct the user to install the app.
2. Determine the input `.webarchive` file from `$ARGUMENTS` or ask the user.
3. Determine the output directory:
   - If the user explicitly provided one in `$ARGUMENTS`, use that.
   - Otherwise, default to `~/Downloads/<archive-name>` (where `<archive-name>` is the input filename without the `.webarchive` extension).
   - If the user asks why `~/Downloads` is the default, explain: macOS sandboxes the WebArchiveExtractor app, which restricts which directories the CLI can write to. The `~/Downloads` folder is one of the few locations reliably accessible, so it's used as the default to avoid silent failures.
4. Determine (optional) URL prepend from `$ARGUMENTS` or ask if needed.
5. Run the extractor using the Bash tool:
   ```sh
   /Applications/WebArchiveExtractor.app/Contents/MacOS/WebArchiveExtractor -i "<input>" -o "<output>" [-p "<prepend>"]
   ```
6. If successful, list the output directory contents with `ls` and summarise:
   - The output directory path
   - How many files were extracted
   - The main HTML file name (if identifiable)
7. Offer to open the extracted HTML in the browser with `open <file>`.

## Notes

- `.webarchive` is a macOS-specific binary plist format used by Safari's "Save As Web Archive" feature.
- The CLI and the GUI app are the same binary — running with `-i` suppresses the GUI.
- Running with no arguments launches the GUI instead of extracting anything.
