---
name: audiobook-ingest
description: >
  Process audiobooks from the inbox: transcribe to text and organize audio
  for voice training.
triggers:
  - ingest audiobook
  - process library inbox
  - transcribe book
  - organize audiobooks
  - download audible books
allowed-tools:
  - Bash
metadata:
  clawdbot:
    emoji: "📚"
    requires:
      bins:
        - uv
        - ffmpeg
---

# Audiobook Ingest (The Black Library)

Process and organize your audiobook collection. This skill uses `uvx` to run its tools, making it self-contained and portable.

## Workflow

1.  **Sync/Download**: Use `uvx audible-cli` to download books.
2.  **Decrypt**: AAX/AAXC files are automatically decrypted using your Audible activation bytes.
3.  **Transcribe**: Use `uvx openai-whisper` (Whisper CLI) to convert audio to text.
4.  **Organize**: Moves files to `~/clawd/library/books/<Title>/`.

## Commands

### `list-warhammer`

List all Warhammer 40k books in your Audible library (searches for Warhammer, Horus, Gaunt, Siege of Terra, etc.).

### `download-warhammer`

Download ONLY your Warhammer 40k books. Perfect for building the Horus Lupercal voice model.

1. Exports your library
2. Finds all Warhammer-related books
3. Downloads each one in AAX format to the inbox (Audible's native format)

### `download-all`

Download all books from your Audible library.

1. Downloads in AAX format (Audible's native encrypted format)

### `ingest <filename>`

Process a single file from `~/clawd/library/inbox/`.

1.  Check if `~/clawd/library/inbox/<filename>` exists.
2.  Create directory `~/clawd/library/books/<filename_no_ext>`.
3.  If AAX/AAXC: Fetch activation bytes and decrypt to M4B using ffmpeg.
4.  Run `uvx --from openai-whisper whisper "<audio_file>" --model turbo --output_format txt --output_dir "~/clawd/library/books/<filename_no_ext>"`
5.  Move the audio file to `~/clawd/library/books/<filename_no_ext>/audio.<ext>` (decrypted version for AAX/AAXC).
6.  Rename output: `mv "~/clawd/library/books/<filename_no_ext>/<filename>.txt" "~/clawd/library/books/<filename_no_ext>/text.md"`

### `ingest-all`

Process all audio files found in `~/clawd/library/inbox/`.

1. List all `.mp3`, `.m4a`, `.m4b`, `.wav`, `.aax`, and `.aaxc` files in the inbox.
2. For each file, run the `ingest` workflow.

## Setup & First Run

1.  **Audible Login**:
    Ask Horus: "Help me log in to Audible" or run this manually:

    ```bash
    uvx --from audible-cli audible quickstart
    ```

    Follow the prompts to authorize.

2.  **Download Your Books**:

    ```bash
    # Download all Warhammer 40k books
    ./run.sh download-warhammer

    # Or download everything
    ./run.sh download-all
    ```

3.  **Transcribe**:
    Ask Horus: "Ingest all audiobooks" or "Process my library inbox".

## Tips

- **Portable**: Since this uses `uvx`, you don't need to manually install `whisper` or `audible-cli`. `uv` will download and cache them on first use.
- **Character Names**: Whisper's `turbo` model is specifically great for the complex names found in Warhammer legends.
