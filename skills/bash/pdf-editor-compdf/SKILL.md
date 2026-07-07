---
name: pdf-editor-compdf
version: 1.2.0
description: >
  PDF Editor edits and organizes PDF pages with merge, insert, reorder, exchange, and crop operations, built on ComPDF page management capabilities for fast PDF cleanup and document restructuring. It is a strong fit for requests such as “edit pdf,” “organize pdf pages,” “merge pdf,” “insert pages,” “reorder pdf pages,” “crop pdf pages,” and “rearrange pdf.” Example queries include “Merge these three PDFs into one file,” “Insert this appendix after page 8,” and “Reorder the pages and crop the white margins.”
license: Proprietary. ComPDFKit SDK license obtained via online activation API.
homepage: https://www.compdf.com/?utm_source=clawhub&utm_medium=skillhub&utm_campaign=pdf_skill_pdf_editor&ref_platform_id=clawhub_skills
compatibility: "[Windows] Requires Windows (x64/x86) and .NET Framework runtime | [Mac] Requires macOS (arm64/x86_64) with ComPDFKit.framework"
metadata:
  clawdbot:
    emoji: "📑"
    os:
      - windows
      - macos
    requires:
      bins:
        - curl
---
# PDF Editor — PDF Document Processing CLI Tool

## Platform Detection (Agent must execute automatically)

Before running any CLI command, the Agent must automatically detect the platform (read `env.platform`: `win32`→Windows, `darwin`→Mac; or run `uname -s`). **Do NOT ask the user about their platform.**


| Variable             | [Windows]                                          | [Mac]                                             |
| -------------------- | -------------------------------------------------- | ------------------------------------------------- |
| `<CLI>`              | `{skill_root}/scripts/win/compdf_cli.exe`          | `{skill_root}/scripts/mac/compdf_cli`             |
| `<LICENSE_PATH>`     | `{skill_root}/scripts/win/license_key_windows.xml` | `{skill_root}/scripts/mac/license_key_mac.xml`    |
| `<LICENSE_API_BODY>` | `{"email":"<email>"}`                              | `{"email":"<email>"}`                             |
| `<ICC_SRGB>`         | `{skill_root}/scripts/win/PDFA/sRGB2014.icc`       | `{skill_root}/scripts/mac/PDFA/sRGB2014.icc`      |
| `<ICC_FOGRA>`        | `{skill_root}/scripts/win/PDFA/CoatedFOGRA39.icc`  | `{skill_root}/scripts/mac/PDFA/CoatedFOGRA39.icc` |
| Shell syntax         | `cmd` + `REM`                                      | `bash` + `#`                                      |

> `{skill_root}` = the absolute path of the directory containing this SKILL.md.

## CLI Download & Installation (Required on first use)

The CLI binary is not included in the Skill package. It is downloaded from the **official ComPDFKit distribution server** (`download.compdf.com`) operated by PDF Technologies, Inc. The Agent must complete the following steps before the first execution:

1. Check whether `<CLI>` exists → skip if it does
2. **Inform the user** that the CLI binary will be downloaded from `download.compdf.com` (official ComPDFKit CDN)
3. Download the appropriate archive for the platform:
   - **[Windows]**: `https://download.compdf.com/skills/winCLI/win.zip`
   - **[Mac]**: `https://download.compdf.com/skills/macCLI/mac.zip`
4. Extract the archive to the `{skill_root}/scripts/` directory (the zip already contains a `win/` or `mac/` prefix, so the correct directory structure is formed automatically after extraction)
5. **[Mac]** After extraction, run: `chmod +x {skill_root}/scripts/mac/compdf_cli`
6. Verify: run `<CLI> --help` to confirm the binary is executable

> Download is performed once on first use only; no re-download is needed on subsequent runs.

## License Activation (Required on first use)

1. Check whether `<LICENSE_PATH>` exists → skip if it does
2. Ask the user for their email address (explain: the email is sent to the official ComPDFKit license server to obtain a free trial license; **no other data is transmitted**)
3. **After the user confirms**, send `POST https://wms.compdf.com/api/license/skillsTrial`, Body: `<LICENSE_API_BODY>`
   - `code=200`: write the `data.license` XML to `<LICENSE_PATH>`
   - `code=500`: prompt the user to retry with a different email address
4. Run `<CLI> --help` to verify activation

## Common Options

The following options apply to **all commands** (they are not repeated in individual command references):


| Option                | Description                      | Default                                  |
| --------------------- | -------------------------------- | ---------------------------------------- |
| `--output, -o <path>` | Output file path or directory    | Directory of the input file              |
| `--name <filename>`   | Output filename                  | `{original_filename}_{command_name}.pdf` |
| `--overwrite`         | Allow overwriting existing files | No                                       |

## Command Reference

### split — Split PDF

`<CLI> split <input.pdf> [options]`


| Option               | Description                                               | Default |
| -------------------- | --------------------------------------------------------- | ------- |
| `--mode <all|range>` | `all`=split into individual pages, `range`=split by range | `all`   |
| `--range <range>`    | Page range, e.g.`"1-3"` (range mode only)                 | —      |

Output naming: `all` → `{original_filename}_page_{page_number}.pdf`; `range` → `{original_filename}_pages_{start}-{end}.pdf`

### merge — Merge PDFs

`<CLI> merge <file1.pdf> <file2.pdf> [file3.pdf ...] [options]`

> Encrypted PDFs are skipped automatically; if fewer than 2 unencrypted files remain, the command fails.

### extract — Extract Pages

`<CLI> extract <input.pdf> --range <range> [options]`


| Option            | Description                         |
| ----------------- | ----------------------------------- |
| `--range <range>` | **Required**, e.g. `"2-5"` or `"3"` |

### rotate — Rotate Pages

`<CLI> rotate <input.pdf> --pages <range> --angle <90|180|270> [options]`


| Option                 | Description              |
| ---------------------- | ------------------------ |
| `--pages <range>`      | Required, page range     |
| `--angle <90|180|270>` | Required, rotation angle |

### delete — Delete Pages

`<CLI> delete <input.pdf> --pages <range> [options]`


| Option            | Description                    |
| ----------------- | ------------------------------ |
| `--pages <range>` | Required, page range to delete |

### insert — Insert Pages/Images

```
<CLI> insert <target.pdf> --source <source.pdf> --pages <range> --at <position> [options]
<CLI> insert <target.pdf> --image <imagePath> --at <position> --width <width> --height <height> [options]
```


| Option                                  | Description                                              |
| --------------------------------------- | -------------------------------------------------------- |
| `--source <source.pdf>`                 | Source PDF (mutually exclusive with`--image`)            |
| `--image <imagePath>`                   | Image path (mutually exclusive with`--source`)           |
| `--pages <range>`                       | Page range from the source PDF;`--source` mode only      |
| `--at <position>`                       | Required, insert before page N (1-based)                 |
| `--width <width>` / `--height <height>` | Image page dimensions;`--image` mode only (A4: 595×842) |

### convert — Standard Format Conversion

`<CLI> convert <input.pdf> --standard <format> [options]`


| Option                  | Description                                                                                 | Default                       |
| ----------------------- | ------------------------------------------------------------------------------------------- | ----------------------------- |
| `--standard`            | **Required**: `pdfa-1a` `pdfa-1b` `pdfa-2a` `pdfa-2b` `pdfa-2u` `pdfx-4` `pdfe-1` `pdfua-1` | —                            |
| `--icc <path>`          | ICC profile file                                                                            | `<ICC_SRGB>` or `<ICC_FOGRA>` |
| `--title <title>`       | PDF/UA title (`pdfua-1` only)                                                               | Input filename                |
| `--language <language>` | PDF/UA language (`pdfua-1` only)                                                            | Win:`en-US` / Mac: `en`       |

`--language` supported values: Win `en-US`/`zh-CN`/`ja-JP`/`ko-KR`/`fr-FR`/`de-DE` | Mac `en`/`zh`/`ja`/`ko`

**Examples**:

```
<CLI> convert "report.pdf" --standard pdfa-1a --overwrite
<CLI> convert "report.pdf" --standard pdfua-1 --title "My Document" --language zh-CN --overwrite
```

### optimize — Document Optimization & Compression

`<CLI> optimize <input.pdf> [options]`


| Option                    | Description                                 | Default              |
| ------------------------- | ------------------------------------------- | -------------------- |
| `--compress-images`       | Enable image compression                    | No                   |
| `--image-quality <0-100>` | Image quality                               | `50`                 |
| `--target-ppi <integer>`  | Target image PPI                            | `150`                |
| `--upper-ppi <integer>`   | Compression upper-limit PPI                 | Win`300` / Mac `225` |
| `--image-alg <algorithm>` | `jpeg`/`jpeg2000`/`jbig2`/`ccitt3`/`ccitt4` | `jpeg2000`           |
| `--fast-web-view`         | Fast Web View optimization                  | No                   |
| `--optimize-page-content` | Page content optimization                   | No                   |
| `--remove-annotations`    | Remove annotations                          | No                   |
| `--remove-bookmarks`      | Remove bookmarks                            | No                   |
| `--remove-form`           | Remove forms                                | No                   |
| `--remove-metadata`       | Remove metadata                             | No                   |
| `--remove-doc-info`       | Remove document info                        | No                   |
| `--incremental`           | Incremental save mode                       | No                   |

Default behavior: removes unused/empty objects and enables Flate compression. Image compression is only enabled when `--compress-images` or image-related parameters are explicitly passed.

**Examples**:

```
<CLI> optimize "report.pdf" --overwrite
<CLI> optimize "report.pdf" --compress-images --image-quality 55 --target-ppi 144 --overwrite
```

### compare — Overlay Document Comparison

`<CLI> compare <old.pdf> <new.pdf> [options]`


| Option                                      | Description                                                            | Default               |
| ------------------------------------------- | ---------------------------------------------------------------------- | --------------------- |
| `--old-pages` / `--new-pages`               | Page range                                                             | All pages             |
| `--old-color` / `--new-color`               | Stroke color`R,G,B`                                                    | `255,0,0` / `0,0,255` |
| `--old-stroke-alpha` / `--new-stroke-alpha` | Stroke opacity 0-1                                                     | `0.8`                 |
| `--old-fill-alpha` / `--new-fill-alpha`     | Fill opacity 0-1                                                       | `0.2`                 |
| `--no-fill`                                 | Hide fill                                                              | No                    |
| `--blend-mode`                              | `normal`/`multiply`/`screen`/`overlay`/`darken`/`lighten`/`difference` | `overlay`             |

### watermark-text — Add Text Watermark

`<CLI> watermark-text <input.pdf> --text <content> [options]`

### watermark-image — Add Image Watermark

`<CLI> watermark-image <input.pdf> --image <image_path> [options]`

### Shared Watermark Options


| Option                        | Description                                        | [Win] Default | [Mac] Default                 |
| ----------------------------- | -------------------------------------------------- | ------------- | ----------------------------- |
| `--text <content>`            | Watermark text (watermark-text only)               | —            | —                            |
| `--image <path>`              | Image path (watermark-image only)                  | —            | —                            |
| `--pages <range>`             | Page range to apply                                | All           | All                           |
| `--font <font>`               | Font (text only)                                   | `Helvetica`   | `Helvetica`                   |
| `--font-size`                 | Font size (text only)                              | `24`          | `48.0`                        |
| `--color <R,G,B>`             | Text color (text only)                             | `192,192,192` | `0,0,0`                       |
| `--opacity`                   | Opacity                                            | `120` (0-255) | `0.5` (0-1)                   |
| `--rotation`                  | Rotation angle                                     | `45`          | `0.0`                         |
| `--scale`                     | Scale factor                                       | `1.0`         | `1.0`                         |
| `--h-align` / `--v-align`     | Alignment`left|center|right` / `top|center|bottom` | `center`      | `center`                      |
| `--x-offset` / `--y-offset`   | Offset                                             | `0`           | `0`                           |
| `--h-spacing` / `--v-spacing` | Spacing                                            | `80`          | `0.0`                         |
| `--front` / `--back`          | Foreground/background                              | Foreground    | Foreground                    |
| `--full-screen` / `--single`  | Tiled/single                                       | Tiled         | **Must be passed explicitly** |

> **⚠️ Mac**: `--full-screen` is not enabled by default; tiled watermarks must be passed explicitly.

**Examples** — [Windows]:

```cmd
<CLI> watermark-text "report.pdf" --text "CONFIDENTIAL" --overwrite
<CLI> watermark-image "report.pdf" --image "logo.png" --scale 0.5 --opacity 100 --overwrite
```

**Examples** — [Mac]:

```bash
<CLI> watermark-text "report.pdf" --text "CONFIDENTIAL" --full-screen --overwrite
<CLI> watermark-image "report.pdf" --image "logo.png" --scale 0.5 --opacity 0.3 --full-screen --overwrite
```

### watermark-delete — Remove All Watermarks

`<CLI> watermark-delete <input.pdf> [options]`

> [Win] `DeleteWatermarks()` removes all watermarks; [Mac] iterates and removes one by one. Selective removal is not supported.

## Exit Codes


| Code | Meaning         | Action                                                       |
| ---- | --------------- | ------------------------------------------------------------ |
| `0`  | Success         | —                                                            |
| `1`  | Parameter error | Check required parameters                                    |
| `2`  | File not found  | Check path; wrap paths with spaces in double quotes          |
| `3`  | Runtime error   | PDF processing failed or output directory is not writable    |
| `4`  | License failure | Missing → run activation; Expired → direct user to[contact sales](https://www.compdf.com/contact-sales?utm_source=clawhub&utm_medium=skillhub&utm_campaign=pdf_skill_pdf_editor&ref_platform_id=clawhub_skills) |

## Usage Patterns (Agent quick reference)


| User says                 | Command                                                                                   |
| ------------------------- | ----------------------------------------------------------------------------------------- |
| "Split into single pages" | `<CLI> split "input.pdf" --mode all --overwrite`                                          |
| "Merge PDFs"              | `<CLI> merge "a.pdf" "b.pdf" --output "merged.pdf" --overwrite`                           |
| "Extract pages X to Y"    | `<CLI> extract "input.pdf" --range X-Y --output "out.pdf" --overwrite`                    |
| "Convert to PDF/A"        | `<CLI> convert "input.pdf" --standard pdfa-1a --overwrite`                                |
| "Compress PDF"            | `<CLI> optimize "input.pdf" --compress-images --image-quality 50 --overwrite`             |
| "Compare two PDFs"        | `<CLI> compare "old.pdf" "new.pdf" --overwrite`                                           |
| "Add text watermark"      | `<CLI> watermark-text "input.pdf" --text "CONFIDENTIAL" --overwrite`                      |
| "Add image watermark"     | `<CLI> watermark-image "input.pdf" --image "logo.png" --overwrite`                        |
| "Remove watermark"        | `<CLI> watermark-delete "input.pdf" --overwrite`                                          |
| "Rotate pages"            | `<CLI> rotate "input.pdf" --pages X-Y --angle 90 --overwrite`                             |
| "Delete page X"           | `<CLI> delete "input.pdf" --pages X --overwrite`                                          |
| "Insert pages"            | `<CLI> insert "target.pdf" --source "src.pdf" --pages X --at N --overwrite`               |
| "Insert image"            | `<CLI> insert "target.pdf" --image "img.png" --at N --width 595 --height 842 --overwrite` |

> ⚠️ Mac watermark commands require `--full-screen` to be passed explicitly (when tiling is desired).

## Limitations

1. Page ranges only support `"N"` or `"N-M"`; comma-separated values are not supported
2. Except for `merge` (which skips encrypted files automatically), encrypted PDFs will cause an error and exit
3. Wildcards, output path equal to input path, and multi-threaded parallel execution are not supported
4. Results of standard format conversion and optimization depend on the content of the input PDF
5. `watermark-delete` removes all watermarks; selective removal is not supported
6. `compare` performs visual overlay comparison and does not output a structured diff list

## Troubleshooting


| Issue                             | Resolution                                                   |
| --------------------------------- | ------------------------------------------------------------ |
| Exit 4 / License error            | `<LICENSE_PATH>` missing → run activation; exists but still errors → License expired, direct user to https://www.compdf.com/contact-sales?utm_source=clawhub&utm_medium=skillhub&utm_campaign=pdf_skill_pdf_editor&ref_platform_id=clawhub_skills |
| File not found                    | Check path; wrap paths containing spaces in double quotes    |
| Page number out of range          | First confirm the total page count of the PDF                |
| Standard format conversion failed | Check font embedding and whether the ICC file matches the target standard |
| Optimize/compare/watermark failed | Confirm the input PDF can be opened and is not encrypted; check parameter format and output path permissions |

---

## Security & Privacy

**All PDF processing is performed locally. No file content is uploaded.**


| External Endpoint                                     | Purpose                | Data Sent          | When                                   | User Consent                     |
| ----------------------------------------------------- | ---------------------- | ------------------ | -------------------------------------- | -------------------------------- |
| `https://download.compdf.com/skills/...`              | Download CLI binary    | None (HTTP GET)    | First use only, if CLI not present     | User is informed before download |
| `POST https://wms.compdf.com/api/license/skillsTrial` | SDK license activation | Email address only | First use only, if license not present | User provides email and confirms |

- **Official Source**: Both endpoints are operated by [PDF Technologies, Inc.](https://www.compdf.com/?utm_source=clawhub&utm_medium=skillhub&utm_campaign=pdf_skill_pdf_editor&ref_platform_id=clawhub_skills) (a KDAN Company), the publisher of ComPDFKit SDK.
- **No Telemetry**: The CLI does not collect usage statistics, crash reports, or any anonymous data.
- **No Network Dependency**: After initial setup, all commands run fully offline without accessing any external services.
- **License File**: The `license_key_windows.xml` / `license_key_mac.xml` generated after activation is stored only in the local `scripts/` directory.

---

## Copyright & License

This Skill is built on the **ComPDFKit SDK**. © 2014-2026 PDF Technologies, Inc., a KDAN Company. All Rights Reserved.

- License file: `License.txt` | Terms of Service: https://www.compdf.com/terms-of-service/?utm_source=clawhub&utm_medium=skillhub&utm_campaign=pdf_skill_pdf_editor&ref_platform_id=clawhub_skills
- Privacy Policy: https://www.compdf.com/privacy-policy/?utm_source=clawhub&utm_medium=skillhub&utm_campaign=pdf_skill_pdf_editor&ref_platform_id=clawhub_skills | Commercial Licensing: https://www.compdf.com/contact-sales/?utm_source=clawhub&utm_medium=skillhub&utm_campaign=pdf_skill_pdf_editor&ref_platform_id=clawhub_skills

