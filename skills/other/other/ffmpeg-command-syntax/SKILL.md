---
name: ffmpeg-command-syntax
description: Complete FFmpeg command syntax reference covering option ordering, input vs output options, stream specifiers, and position-sensitive options. PROACTIVELY activate for: (1) Command syntax questions, (2) Option placement issues, (3) Input vs output option confusion, (4) Stream specifier syntax, (5) -ss/-t/-to position questions, (6) Global vs per-file options, (7) Multiple input/output handling, (8) Option order errors. Provides: Correct option placement rules, input-only vs output-only options, position-sensitive option behavior, stream specifier syntax, common mistakes and fixes.
---

## CRITICAL: FFmpeg Option Ordering Rules

**The most common FFmpeg mistake is putting options in the wrong place.** Options in FFmpeg are position-sensitive and apply to the NEXT file specified after them.

### The Golden Rule

```
ffmpeg [global_options] {[input_options] -i input}... {[output_options] output}...
```

**Key principle**: Options are applied to the **next** file. They are **reset between files**.

---

## Option Categories

### 1. Global Options (First, Before Everything)

Global options affect the entire FFmpeg process and must come **first**, before any inputs:

| Option | Description | Example |
|--------|-------------|---------|
| `-y` | Overwrite output without asking | `ffmpeg -y -i in.mp4 out.mp4` |
| `-n` | Never overwrite output | `ffmpeg -n -i in.mp4 out.mp4` |
| `-v` / `-loglevel` | Set logging verbosity | `ffmpeg -v error -i in.mp4 out.mp4` |
| `-stats` | Print encoding progress | `ffmpeg -stats -i in.mp4 out.mp4` |
| `-progress` | Send progress to file/URL | `ffmpeg -progress - -i in.mp4 out.mp4` |
| `-report` | Generate ffmpeg-*.log file | `ffmpeg -report -i in.mp4 out.mp4` |
| `-hide_banner` | Suppress copyright banner | `ffmpeg -hide_banner -i in.mp4 out.mp4` |
| `-filter_complex` | Complex filtergraph (global) | `ffmpeg -i a.mp4 -i b.mp4 -filter_complex "[0][1]overlay" out.mp4` |
| `-filter_complex_threads` | Filtergraph thread count | `ffmpeg -filter_complex_threads 4 ...` |

```bash
# Correct: Global options first
ffmpeg -y -hide_banner -v warning -i input.mp4 output.mp4

# Wrong: Global option after -i
ffmpeg -i input.mp4 -y output.mp4  # -y works but is not idiomatic
```

### 2. Input Options (Before `-i`)

Input options affect how a file is **read/decoded**. They must be placed **immediately before** the `-i` for the file they apply to.

#### Input-Only Options

| Option | Description | Placement |
|--------|-------------|-----------|
| `-ss` (as input) | Seek position (fast, may be imprecise) | Before `-i` |
| `-t` (as input) | Limit input read duration | Before `-i` |
| `-to` (as input) | Read until timestamp | Before `-i` |
| `-itsoffset` | Time offset for input timestamps | Before `-i` |
| `-itsscale` | Input timestamp scale factor | Before `-i` |
| `-re` | Read input at native frame rate (streaming) | Before `-i` |
| `-readrate` | Read input at specified rate | Before `-i` |
| `-stream_loop` | Loop input N times (-1 = infinite) | Before `-i` |
| `-hwaccel` | Hardware acceleration method | Before `-i` |
| `-hwaccel_device` | Hardware device to use | Before `-i` |
| `-hwaccel_output_format` | Pixel format for hwaccel output | Before `-i` |
| `-c:v` (as decoder) | Video decoder selection | Before `-i` |
| `-c:a` (as decoder) | Audio decoder selection | Before `-i` |
| `-r` (as input) | Input frame rate (raw formats) | Before `-i` |
| `-s` (as input) | Input frame size (raw formats) | Before `-i` |
| `-pix_fmt` (as input) | Input pixel format (raw formats) | Before `-i` |
| `-f` (as input) | Force input format | Before `-i` |
| `-accurate_seek` | Enable accurate seeking (default) | Before `-i` |
| `-noaccurate_seek` | Disable accurate seeking | Before `-i` |
| `-seek_timestamp` | Seek by timestamp vs byte position | Before `-i` |
| `-thread_queue_size` | Input thread queue size | Before `-i` |
| `-guess_layout_max` | Max channels for layout guessing | Before `-i` |

```bash
# Correct: Input options before their -i
ffmpeg -ss 00:01:00 -t 30 -i input.mp4 output.mp4

# Wrong: Input options after -i
ffmpeg -i input.mp4 -ss 00:01:00 output.mp4  # -ss is now an OUTPUT option (slower!)
```

#### Hardware Acceleration Input Options

```bash
# Correct: hwaccel before -i
ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i input.mp4 \
  -c:v h264_nvenc output.mp4

# Correct: Different hwaccel per input
ffmpeg -hwaccel cuda -i input1.mp4 \
       -hwaccel vaapi -i input2.mp4 \
       -filter_complex "[0][1]overlay" output.mp4

# Wrong: hwaccel after -i (won't work)
ffmpeg -i input.mp4 -hwaccel cuda -c:v h264_nvenc output.mp4
```

### 3. Output Options (After Last `-i`, Before Output File)

Output options affect how a file is **encoded/written**. They must be placed **after all inputs** and **before the output file** they apply to.

#### Output-Only Options

| Option | Description | Placement |
|--------|-------------|-----------|
| `-c:v` (as encoder) | Video encoder selection | Before output |
| `-c:a` (as encoder) | Audio encoder selection | Before output |
| `-c:s` | Subtitle codec selection | Before output |
| `-b:v` | Video bitrate | Before output |
| `-b:a` | Audio bitrate | Before output |
| `-crf` | Constant Rate Factor (quality) | Before output |
| `-preset` | Encoding preset (speed/quality) | Before output |
| `-tune` | Encoding tuning profile | Before output |
| `-profile:v` | Video profile | Before output |
| `-level` | Codec level | Before output |
| `-r` (as output) | Output frame rate | Before output |
| `-s` (as output) | Output frame size | Before output |
| `-aspect` | Output aspect ratio | Before output |
| `-pix_fmt` (as output) | Output pixel format | Before output |
| `-vf` / `-filter:v` | Video filter chain | Before output |
| `-af` / `-filter:a` | Audio filter chain | Before output |
| `-map` | Stream mapping | Before output |
| `-ss` (as output) | Start time (accurate but slow) | Before output |
| `-t` (as output) | Output duration limit | Before output |
| `-to` (as output) | End time for output | Before output |
| `-fs` | File size limit (bytes) | Before output |
| `-frames:v` | Number of video frames to output | Before output |
| `-frames:a` | Number of audio frames to output | Before output |
| `-f` (as output) | Force output format | Before output |
| `-movflags` | MOV/MP4 muxer flags | Before output |
| `-metadata` | Set metadata | Before output |
| `-disposition` | Set stream disposition | Before output |
| `-shortest` | Stop when shortest stream ends | Before output |
| `-copyts` | Copy timestamps | Before output |
| `-start_at_zero` | Start timestamps at zero | Before output |
| `-avoid_negative_ts` | Handle negative timestamps | Before output |
| `-an` | Disable audio | Before output |
| `-vn` | Disable video | Before output |
| `-sn` | Disable subtitles | Before output |
| `-dn` | Disable data streams | Before output |

```bash
# Correct: Output options before output file
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium output.mp4

# With multiple outputs - each needs its own options
ffmpeg -i input.mp4 \
  -c:v libx264 -crf 23 output_h264.mp4 \
  -c:v libx265 -crf 28 output_h265.mp4
```

### 4. Options That Work as Both Input AND Output

Some options have different behavior depending on position:

#### `-ss` (Seek/Start Time) - **Position Critical**

```bash
# BEFORE -i (INPUT): Fast seek, may not be frame-accurate
# Seeks by keyframes, then decodes to precise position if -accurate_seek (default)
ffmpeg -ss 00:01:00 -i input.mp4 -t 30 -c copy output.mp4

# AFTER -i (OUTPUT): Frame-accurate but slower
# Decodes all frames from start, discards until seek point
ffmpeg -i input.mp4 -ss 00:01:00 -t 30 -c:v libx264 output.mp4

# BOTH (Recommended for accuracy + speed):
# Fast seek to near position, then accurate decode
ffmpeg -ss 00:00:55 -i input.mp4 -ss 00:00:05 -t 30 -c:v libx264 output.mp4
```

**Important**: When `-ss` is before `-i`, timestamps are reset to 0. Use `-copyts` to preserve original timestamps.

#### `-t` and `-to` (Duration/End Time)

```bash
# -t BEFORE -i: Limits how much of input to READ
ffmpeg -t 60 -i input.mp4 -c copy output.mp4  # Read first 60 seconds

# -t AFTER -i: Limits output DURATION
ffmpeg -i input.mp4 -t 60 -c copy output.mp4  # Output first 60 seconds

# -to: End timestamp (works with -ss timestamp reset)
# With -ss before -i, timestamps reset, so -to is relative to new zero
ffmpeg -ss 00:01:00 -i input.mp4 -to 00:00:30 output.mp4  # 30 seconds from seek point

# To get 1:00 to 1:30, use -t instead, or -copyts with -to
ffmpeg -ss 00:01:00 -i input.mp4 -t 00:00:30 output.mp4  # Correct: 30 sec duration
ffmpeg -ss 00:01:00 -copyts -i input.mp4 -to 00:01:30 output.mp4  # Also correct
```

#### `-r` (Frame Rate)

```bash
# BEFORE -i: Input frame rate (for raw/image sequences)
ffmpeg -r 30 -i frame_%04d.png output.mp4  # Input at 30fps

# AFTER -i: Output frame rate (adds/drops frames to match)
ffmpeg -i input.mp4 -r 24 output.mp4  # Convert to 24fps
```

#### `-s` (Size/Resolution)

```bash
# BEFORE -i: Input size (for raw formats)
ffmpeg -s 1920x1080 -pix_fmt yuv420p -i raw.yuv output.mp4

# AFTER -i: Output size (scales video) - prefer -vf scale instead
ffmpeg -i input.mp4 -s 1280x720 output.mp4
```

#### `-c` / `-codec` (Codec Selection)

```bash
# BEFORE -i: Selects DECODER (rarely needed)
ffmpeg -c:v h264_cuvid -i input.mp4 -c:v h264_nvenc output.mp4

# AFTER -i: Selects ENCODER (common usage)
ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4
```

---

## Stream Specifiers

Stream specifiers target specific streams for per-stream options. Appended with colon after option name.

### Syntax

```
-option[:stream_specifier] value
```

### Stream Specifier Types

| Specifier | Meaning | Example |
|-----------|---------|---------|
| `:v` | All video streams | `-c:v libx264` |
| `:V` | Video streams (not thumbnails/covers) | `-c:V libx264` |
| `:a` | All audio streams | `-c:a aac` |
| `:s` | All subtitle streams | `-c:s mov_text` |
| `:d` | All data streams | `-c:d copy` |
| `:t` | All attachment streams | `... ` |
| `:v:0` | First video stream | `-b:v:0 5M` |
| `:a:1` | Second audio stream | `-c:a:1 ac3` |
| `:0` | First stream (any type) | `-c:0 copy` |
| `:1` | Second stream (any type) | `-c:1 libx264` |
| `:#0x1234` | Stream with specific PID | `-c:#0x1234 copy` |
| `:i:0x100` | Stream with specific ID | `-c:i:0x100 copy` |
| `:m:key:value` | Stream with matching metadata | `-c:m:language:eng aac` |
| `:p:0` | Streams in program 0 | `-c:p:0 copy` |
| `:u` | Usable configuration streams | `-c:u copy` |

### Input Index Prefix

For multi-input commands, prefix with input index:

```bash
# Stream 0 from input 1
ffmpeg -i a.mp4 -i b.mp4 -map 1:0 -c copy output.mp4

# Video from input 0, audio from input 1
ffmpeg -i video.mp4 -i audio.mp3 -map 0:v -map 1:a output.mp4

# Second audio stream from third input
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 -map 2:a:1 output.mp4
```

### Per-Stream Option Examples

```bash
# Different codecs per stream type
ffmpeg -i input.mkv -c:v libx264 -c:a aac -c:s mov_text output.mp4

# Different bitrates per stream index
ffmpeg -i input.mkv -map 0 \
  -c:v libx264 -b:v:0 5M \
  -c:a:0 aac -b:a:0 192k \
  -c:a:1 ac3 -b:a:1 384k \
  output.mkv

# Different settings for each audio stream
ffmpeg -i multichannel.mxf -map 0:v:0 -map 0:a:0 -map 0:a:0 \
  -c:a:0 ac3 -b:a:0 640k \
  -ac:a:1 2 -c:a:1 aac -b:a:1 128k \
  output.mp4
```

---

## Multiple Inputs and Outputs

### Multiple Inputs

```bash
# Options apply to immediately following -i
ffmpeg \
  -ss 10 -i first.mp4 \      # Seek 10s in first input
  -ss 5 -i second.mp4 \      # Seek 5s in second input
  -filter_complex "[0:v][1:v]overlay" \
  output.mp4
```

### Multiple Outputs

```bash
# Each output needs its own options - they reset between outputs
ffmpeg -i input.mp4 \
  -c:v libx264 -crf 23 output_h264.mp4 \
  -c:v libx265 -crf 28 output_h265.mp4 \
  -c:v libvpx-vp9 -crf 30 output_vp9.webm

# Same codec, different resolutions
ffmpeg -i input.mp4 \
  -vf "scale=1920:1080" -c:v libx264 -crf 23 hd.mp4 \
  -vf "scale=1280:720" -c:v libx264 -crf 23 sd.mp4

# WRONG: Options don't carry over
ffmpeg -i input.mp4 -c:v libx264 -crf 23 out1.mp4 out2.mp4
# out2.mp4 will NOT have libx264/crf 23 settings!
```

---

## Common Mistakes and Fixes

### Mistake 1: Input Option After `-i`

```bash
# WRONG: -hwaccel after -i has no effect
ffmpeg -i input.mp4 -hwaccel cuda -c:v h264_nvenc output.mp4

# CORRECT: -hwaccel before -i
ffmpeg -hwaccel cuda -i input.mp4 -c:v h264_nvenc output.mp4
```

### Mistake 2: Output Option Before `-i`

```bash
# WRONG: -c:v before -i tries to select decoder (may fail)
ffmpeg -c:v libx264 -i input.mp4 output.mp4

# CORRECT: -c:v after -i selects encoder
ffmpeg -i input.mp4 -c:v libx264 output.mp4
```

### Mistake 3: Expecting Options to Persist Across Outputs

```bash
# WRONG: Second output won't have the encoding settings
ffmpeg -i input.mp4 -c:v libx264 -crf 23 out1.mp4 out2.mp4

# CORRECT: Repeat options for each output
ffmpeg -i input.mp4 \
  -c:v libx264 -crf 23 out1.mp4 \
  -c:v libx264 -crf 23 out2.mp4
```

### Mistake 4: Wrong `-ss` Position for Accuracy

```bash
# Fast but may be imprecise (seeks to keyframe)
ffmpeg -ss 00:05:00 -i input.mp4 -t 30 -c copy output.mp4

# Slow but frame-accurate (decodes everything)
ffmpeg -i input.mp4 -ss 00:05:00 -t 30 -c:v libx264 output.mp4

# BEST: Fast AND accurate (two-pass seek)
ffmpeg -ss 00:04:55 -i input.mp4 -ss 5 -t 30 -c:v libx264 output.mp4
```

### Mistake 5: Mixing Input/Output Files

```bash
# WRONG: Mixing inputs and outputs
ffmpeg -i input1.mp4 -c:v libx264 output1.mp4 -i input2.mp4 output2.mp4

# CORRECT: All inputs first, then all outputs
ffmpeg -i input1.mp4 -i input2.mp4 \
  -map 0 -c:v libx264 output1.mp4 \
  -map 1 -c:v libx264 output2.mp4
```

### Mistake 6: `-t` vs `-to` Confusion with `-ss`

```bash
# -ss before -i resets timestamps to 0
# -to 00:00:30 means 30 seconds from new timestamp 0
ffmpeg -ss 00:01:00 -i input.mp4 -to 00:00:30 output.mp4  # 30 sec clip

# To end at original timestamp, use -copyts
ffmpeg -ss 00:01:00 -copyts -i input.mp4 -to 00:01:30 output.mp4  # 30 sec clip

# Or use -t for duration (unaffected by timestamp reset)
ffmpeg -ss 00:01:00 -i input.mp4 -t 00:00:30 output.mp4  # 30 sec clip
```

### Mistake 7: Filter vs Global `-filter_complex`

```bash
# -vf is per-output, applies to single input
ffmpeg -i input.mp4 -vf "scale=1280:720" output.mp4

# -filter_complex is GLOBAL, for multi-input operations
ffmpeg -i video.mp4 -i overlay.png \
  -filter_complex "[0:v][1:v]overlay=10:10" \
  output.mp4

# WRONG: Using -vf with multiple inputs
ffmpeg -i video.mp4 -i overlay.png -vf "overlay=10:10" output.mp4  # Error!
```

---

## Command Structure Examples

### Basic Transcode

```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -c:a aac output.mp4
#      ^input       ^output options                 ^output
```

### With Input Seeking

```bash
ffmpeg -ss 60 -i input.mp4 -t 30 -c:v libx264 output.mp4
#      ^input opt ^input    ^output options    ^output
```

### Hardware Acceleration

```bash
ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i input.mp4 \
#      ^input options (must be before -i)        ^input
  -c:v h264_nvenc -preset p4 output.mp4
# ^output options            ^output
```

### Multiple Inputs with Filters

```bash
ffmpeg -i main.mp4 -i overlay.png \
#      ^input1     ^input2
  -filter_complex "[0:v][1:v]overlay=10:10[v]" \
# ^global option
  -map "[v]" -map 0:a -c:v libx264 -c:a copy output.mp4
# ^output options                            ^output
```

### Streaming with Real-time Read

```bash
ffmpeg -re -i input.mp4 -c:v libx264 -f flv rtmp://server/live/stream
#      ^input opt       ^output options      ^output
```

### Complete Structure

```bash
ffmpeg \
  -y -hide_banner \                           # Global options
  -hwaccel cuda -ss 10 -i input1.mp4 \        # Input 1 options + input
  -stream_loop -1 -i input2.mp4 \             # Input 2 options + input
  -filter_complex "[0:v][1:v]overlay[v]" \    # Global filter
  -map "[v]" -map 0:a \                       # Output mapping
  -c:v h264_nvenc -b:v 5M \                   # Output video options
  -c:a aac -b:a 192k \                        # Output audio options
  -movflags +faststart \                      # Output muxer options
  output.mp4                                  # Output file
```

---

## Quick Reference Card

### Option Placement Cheatsheet

| Option | Before `-i` | After `-i` | Notes |
|--------|-------------|------------|-------|
| `-ss` | Fast seek | Accurate seek | Before = keyframe seek, After = decode all |
| `-t` | Input limit | Output limit | Limits read vs write |
| `-to` | Input end | Output end | Affected by timestamp reset |
| `-r` | Input FPS | Output FPS | For raw/output conversion |
| `-s` | Input size | Output size | For raw/scaling |
| `-c:v` | Decoder | Encoder | Before = decode, After = encode |
| `-c:a` | Decoder | Encoder | Before = decode, After = encode |
| `-hwaccel` | **Required** | N/A | Must be before -i |
| `-re` | **Required** | N/A | Must be before -i |
| `-itsoffset` | **Required** | N/A | Must be before -i |
| `-stream_loop` | **Required** | N/A | Must be before -i |
| `-vf` | N/A | **Required** | Output filter only |
| `-af` | N/A | **Required** | Output filter only |
| `-map` | N/A | **Required** | Output option only |
| `-crf` | N/A | **Required** | Output option only |
| `-preset` | N/A | **Required** | Output option only |
| `-movflags` | N/A | **Required** | Output option only |
| `-y` | Global | Global | Can be anywhere (prefer first) |
| `-v` | Global | Global | Can be anywhere (prefer first) |
| `-filter_complex` | Global | Global | Must be used for multi-input |

---

## Complete FFmpeg 8.0+ Option Reference

### Global Options (Complete List)

| Option | Description |
|--------|-------------|
| `-y` | Overwrite output files without asking |
| `-n` | Never overwrite output files |
| `-v level` / `-loglevel level` | Set logging verbosity (quiet, panic, fatal, error, warning, info, verbose, debug, trace) |
| `-stats` | Print encoding progress statistics |
| `-stats_period time` | Set statistics output period |
| `-progress url` | Send progress info to URL/file |
| `-stdin` | Enable stdin interaction |
| `-nostdin` | Disable stdin interaction |
| `-report` | Generate ffmpeg-*.log debug file |
| `-hide_banner` | Suppress program banner |
| `-max_alloc bytes` | Maximum allocation size limit |
| `-cpuflags flags` | Set CPU flags mask |
| `-cpucount count` | Override CPU count detection |
| `-max_error_rate ratio` | Maximum decoding error ratio |
| `-xerror` | Exit on error |
| `-abort_on flags` | Conditions to abort (empty_output, empty_output_stream) |
| `-filter_complex graph` | Global complex filtergraph |
| `-filter_complex_threads n` | Filtergraph thread count |
| `-filter_threads n` | Set filter processing threads |
| `-filter_buffered_frames n` | Max buffered frames in filtergraph |
| `-lavfi graph` | Alias for -filter_complex |
| `-filter_complex_script file` | Read filtergraph from file |
| `-sdp_file file` | Write SDP info to file |
| `-init_hw_device type=name` | Initialize hardware device |
| `-filter_hw_device name` | Hardware device for filters |
| `-hwaccels` | List available hardware accelerations |
| `-benchmark` | Show benchmarking info |
| `-benchmark_all` | Show per-step benchmarking |
| `-timelimit duration` | Exit after duration seconds |
| `-dump` | Dump each input packet |
| `-hex` | Dump packets in hex |
| `-debug_ts` | Print timestamp/latency debugging info |
| `-recast_media` | Force decoder of different media type |
| `-vsync mode` | Video sync method (deprecated, use -fps_mode) |
| `-fps_mode mode` | Frame rate mode (passthrough, cfr, vfr, auto) |
| `-frame_drop_threshold threshold` | Frame drop threshold |
| `-async samples_per_second` | Audio sync method |
| `-adrift_threshold threshold` | Audio drift threshold |
| `-copyts` | Copy timestamps from input |
| `-start_at_zero` | Shift input timestamps to start at 0 |
| `-copytb mode` | Copy input timebase (0=decoder, 1=demuxer, -1=auto) |
| `-dts_delta_threshold threshold` | DTS discontinuity threshold |
| `-dts_error_threshold threshold` | DTS error timestamp threshold |
| `-muxdelay seconds` | Maximum mux delay |
| `-muxpreload seconds` | Initial mux delay |
| `-streamid output_index:new_id` | Set stream ID in output |
| `-override_ffserver` | Override ffserver input specifications |
| `-bitexact` | Use only bit-exact algorithms |
| `-default_mode mode` | Default stream selection mode |
| `-vstats` | Dump video coding stats to vstats_HHMMSS.log |
| `-vstats_file file` | Dump video coding stats to specified file |
| `-vstats_version n` | Set vstats format version |
| `-print_graphs` | Print execution graph to stderr |
| `-print_graphs_file file` | Write execution graph to file |
| `-print_graphs_format fmt` | Set graph output format (default, compact, json, mermaid)

### Input-Only Options (Complete List)

| Option | Description |
|--------|-------------|
| `-i url` | Input file URL |
| `-f fmt` | Force input format |
| `-c:v decoder` / `-vcodec decoder` | Video decoder |
| `-c:a decoder` / `-acodec decoder` | Audio decoder |
| `-c:s decoder` / `-scodec decoder` | Subtitle decoder |
| `-ss position` | Seek to position (fast, keyframe-based) |
| `-sseof position` | Seek relative to end of file (negative value) |
| `-t duration` | Limit input duration |
| `-to position` | Limit input to position |
| `-itsoffset offset` | Input timestamp offset |
| `-itsscale scale` | Input timestamp scale (per-stream) |
| `-isync input_index` | Assign input as sync source |
| `-re` | Read at native frame rate |
| `-readrate speed` | Read at specified rate |
| `-readrate_initial_burst duration` | Initial burst before rate limiting |
| `-readrate_catchup speed` | Catchup rate when behind |
| `-stream_loop count` | Loop input (-1 = infinite) |
| `-hwaccel method` | Hardware acceleration (none, auto, cuda, vaapi, qsv, d3d11va, dxva2, videotoolbox, vdpau, vulkan) |
| `-hwaccel_device device` | Hardware device path/name |
| `-hwaccel_output_format format` | Hardware output pixel format |
| `-autorotate` | Automatically rotate video (enabled by default) |
| `-noautorotate` | Disable automatic rotation |
| `-r fps` | Input frame rate (raw formats) |
| `-s size` | Input frame size (raw formats) |
| `-pix_fmt format` | Input pixel format (raw formats) |
| `-sample_fmt format` | Input sample format (raw audio) |
| `-ar rate` | Input audio sample rate |
| `-ac channels` | Input audio channel count |
| `-channel_layout layout` | Input audio channel layout |
| `-accurate_seek` | Enable accurate seeking (default) |
| `-noaccurate_seek` | Disable accurate seeking |
| `-seek_timestamp` | Enable seeking by timestamp |
| `-thread_queue_size count` | Input thread queue size |
| `-guess_layout_max channels` | Max channels for layout guessing |
| `-discard mode` | Discard frames (none, default, noref, bidir, nokey, all) |
| `-reinit_filter` | Reinitialize filters on input change (per-stream) |
| `-drop_changed` | Drop frames with changed parameters (per-stream) |
| `-display_rotation degrees` | Set display rotation metadata |
| `-display_hflip` | Set horizontal flip metadata |
| `-display_vflip` | Set vertical flip metadata |
| `-fix_sub_duration` | Fix subtitle durations |
| `-canvas_size size` | Subtitle canvas size |
| `-ignore_loop` | Ignore loop metadata (GIF) |
| `-dump_attachment:stream filename` | Extract attachment to file (per-stream) |

### Output-Only Options (Complete List)

| Option | Description |
|--------|-------------|
| `-f fmt` | Force output format |
| `-c:v encoder` / `-vcodec encoder` | Video encoder (or `copy`) |
| `-c:a encoder` / `-acodec encoder` | Audio encoder (or `copy`) |
| `-c:s encoder` / `-scodec encoder` | Subtitle encoder (or `copy`) |
| `-c:d codec` / `-dcodec codec` | Data stream codec |
| `-ss position` | Start time (accurate, slow) |
| `-t duration` | Output duration limit |
| `-to position` | Output end position |
| `-fs size` | File size limit (bytes) |
| `-frames:v count` / `-vframes count` | Video frame count limit |
| `-frames:a count` / `-aframes count` | Audio frame count limit |
| `-frames:d count` / `-dframes count` | Data frame count limit |
| `-r fps` | Output frame rate |
| `-fpsmax fps` | Maximum output frame rate |
| `-s size` | Output frame size |
| `-aspect ratio` | Display aspect ratio |
| `-pix_fmt format` | Output pixel format |
| `-sample_fmt format` | Output sample format |
| `-ar rate` | Output audio sample rate |
| `-ac channels` | Output audio channel count |
| `-channel_layout layout` | Output audio channel layout |
| `-vf filtergraph` / `-filter:v` | Video filter chain |
| `-af filtergraph` / `-filter:a` | Audio filter chain |
| `-map input:stream` | Stream mapping |
| `-map_metadata specifier` | Metadata mapping (see below) |
| `-map_chapters input_index` | Chapter mapping from input |
| `-b:v bitrate` | Video bitrate |
| `-b:a bitrate` | Audio bitrate |
| `-maxrate bitrate` | Maximum bitrate |
| `-minrate bitrate` | Minimum bitrate |
| `-bufsize size` | Rate control buffer size |
| `-crf value` | Constant Rate Factor (quality) |
| `-qp value` | Constant QP value |
| `-q:v value` / `-qscale:v value` | Video quality scale (VBR) |
| `-q:a value` / `-qscale:a value` | Audio quality scale (VBR) |
| `-preset name` | Encoder preset |
| `-tune name` | Encoder tuning |
| `-profile:v name` | Video profile |
| `-level value` | Codec level |
| `-g frames` | GOP size / keyframe interval |
| `-keyint_min frames` | Minimum keyframe interval |
| `-sc_threshold value` | Scene change threshold |
| `-bf frames` | B-frame count |
| `-refs frames` | Reference frames |
| `-pass n` | Multi-pass encoding (1 or 2) |
| `-passlogfile prefix` | Pass log file prefix |
| `-rc_lookahead frames` | Rate control lookahead |
| `-an` | Disable audio output |
| `-vn` | Disable video output |
| `-sn` | Disable subtitle output |
| `-dn` | Disable data stream output |
| `-metadata key=value` | Set global metadata |
| `-metadata:s:v key=value` | Set video stream metadata |
| `-metadata:s:a key=value` | Set audio stream metadata |
| `-metadata:c:0 key=value` | Set chapter metadata |
| `-disposition:s:0 flags` | Set stream disposition |
| `-program title=name:st=0:st=1` | Create program in output |
| `-stream_group type=value:...` | Create stream group |
| `-target type` | Target format (vcd, svcd, dvd, dv, dv50) |
| `-shortest` | Stop at shortest stream |
| `-shortest_buf_duration duration` | Buffer for shortest detection |
| `-apad` | Pad audio to match video (use with -shortest) |
| `-copypriorss n` | Copy frames before start time (0=no, 1=yes, -1=auto) |
| `-avoid_negative_ts mode` | Handle negative timestamps (make_non_negative, make_zero, auto, disabled) |
| `-timestamp date` | Set recording timestamp |
| `-movflags flags` | MOV/MP4 flags (+faststart, +frag_keyframe, etc.) |
| `-fflags flags` | Format flags (+genpts, +igndts, +discardcorrupt, etc.) |
| `-bsf:v filter` | Video bitstream filter |
| `-bsf:a filter` | Audio bitstream filter |
| `-tag:v fourcc` / `-vtag fourcc` | Video tag/fourcc |
| `-tag:a fourcc` / `-atag fourcc` | Audio tag/fourcc |
| `-timecode hh:mm:ss:ff` | Set initial timecode |
| `-force_key_frames expr` | Force keyframe positions |
| `-copyinkf` | Copy initial non-keyframes (stream copy) |
| `-init_hw_device type=name` | Initialize hw device for output |
| `-enc_time_base mode` | Encoder timebase (demux, filter, auto) |
| `-attach filename` | Add attachment (fonts, images) |
| `-pre preset_name` | Use preset file (per-stream) |
| `-fpre preset_file` | Use preset file (per-file) |
| `-max_muxing_queue_size packets` | Muxing queue size |
| `-muxing_queue_data_threshold bytes` | Queue data threshold |
| `-dcodec codec` | Data stream codec (alias for -c:d) |
| `-intra` | Use only intra frames (deprecated, use -g 1) |
| `-vol volume` | Audio volume (256=normal, deprecated, use -af volume) |
| `-autoscale` | Auto-scale video (enabled by default) |
| `-noautoscale` | Disable auto-scaling |
| `-autorotate` | Auto-rotate video on output (enabled by default) |
| `-noautorotate` | Disable auto-rotation on output |

### Video Color/HDR Options (Output)

| Option | Description |
|--------|-------------|
| `-color_range range` | Color range (tv/pc, limited/full, mpeg/jpeg) |
| `-color_primaries primaries` | Color primaries (bt709, bt2020, smpte170m, etc.) |
| `-color_trc trc` | Transfer characteristics (bt709, smpte2084/pq, arib-std-b67/hlg, etc.) |
| `-colorspace space` | Colorspace (bt709, bt2020nc, smpte170m, etc.) |
| `-chroma_sample_location loc` | Chroma sample location |
| `-top n` | Top field first (1) or bottom field first (0) |
| `-bits_per_raw_sample n` | Bits per raw sample |
| `-dc precision` | Intra DC precision |
| `-qphist` | Show QP histogram |

### Subtitle Options

| Option | Description | Type |
|--------|-------------|------|
| `-sn` | Disable subtitles | Input/Output |
| `-scodec codec` | Subtitle codec | Input/Output |
| `-stag fourcc` | Subtitle tag/fourcc | Output |
| `-fix_sub_duration` | Fix subtitle durations | Input |
| `-canvas_size size` | Subtitle canvas size | Input |

### FFmpeg 8.0+ Specific Options

| Option | Description | Type |
|--------|-------------|------|
| `-vaapi_device path` | VAAPI device path | Input/Global |
| `-qsv_device path` | Intel QSV device | Input/Global |
| `-vulkan_device device` | Vulkan device selection | Input/Global |
| `-fps_mode mode` | Frame rate mode (replaces -vsync) | Output |
| `-enc_stats_pre file` | Pre-encoding stats output | Output |
| `-enc_stats_post file` | Post-encoding stats output | Output |
| `-enc_stats_pre_fmt fmt` | Pre-encoding stats format | Output |
| `-enc_stats_post_fmt fmt` | Post-encoding stats format | Output |
| `-autoscale` | Auto-scale to encoder (default) | Output |
| `-noautoscale` | Disable auto-scaling | Output |
| `-bits_per_raw_sample n` | Set bits per raw sample | Output |

### Threading Options

| Option | Description | Type |
|--------|-------------|------|
| `-threads n` | Encoding/decoding threads (0=auto) | Per-stream/Output |
| `-thread_type type` | Thread type (frame, slice) | Per-stream |
| `-filter_threads n` | Filter processing threads | Global |
| `-filter_complex_threads n` | Complex filtergraph threads | Global |

```bash
# Auto-detect threads for encoding
ffmpeg -i input.mp4 -c:v libx264 -threads 0 output.mp4

# Specific thread count
ffmpeg -i input.mp4 -c:v libx264 -threads 8 output.mp4

# Per-stream threading
ffmpeg -i input.mp4 -threads:v 8 -threads:a 2 -c:v libx264 -c:a aac output.mp4

# Filter threads
ffmpeg -filter_threads 4 -i input.mp4 -vf "scale=1920:1080" output.mp4
```

### Format Flags (-fflags)

| Flag | Description |
|------|-------------|
| `+genpts` | Generate PTS if missing |
| `+igndts` | Ignore DTS (use PTS only) |
| `+ignidx` | Ignore index |
| `+discardcorrupt` | Discard corrupted frames |
| `+sortdts` | Sort packets by DTS |
| `+fastseek` | Enable fast seeking |
| `+nobuffer` | Disable buffering |
| `+flush_packets` | Flush packets immediately |
| `+bitexact` | Bit-exact output |
| `+shortest` | Stop at shortest stream |
| `+autobsf` | Auto-insert bitstream filters |

---

## Format-Specific Options (Not Main Options)

These options belong to **specific muxers/demuxers/protocols**, not the main FFmpeg options. They are passed using `-option value` syntax but only work with their specific format.

### HLS Muxer Options (Output)

```bash
ffmpeg -i input.mp4 -c copy \
  -hls_time 10 \               # Segment duration (seconds)
  -hls_list_size 6 \           # Playlist entries (0=all)
  -hls_segment_filename "seg_%03d.ts" \
  -hls_flags delete_segments \
  playlist.m3u8
```

### Segment Muxer Options (Output)

```bash
ffmpeg -i input.mp4 -c copy \
  -f segment \
  -segment_time 60 \           # Segment duration
  -segment_list playlist.txt \
  -segment_format mp4 \
  output_%03d.mp4
```

### DASH Muxer Options (Output)

```bash
ffmpeg -i input.mp4 -c copy \
  -f dash \
  -seg_duration 4 \
  -init_seg_name "init_$RepresentationID$.m4s" \
  manifest.mpd
```

### RTSP/RTMP Protocol Options (Input)

```bash
ffmpeg -rtsp_transport tcp -i "rtsp://server/stream" output.mp4
ffmpeg -rtmp_buffer 1000 -i "rtmp://server/live/stream" output.mp4
```

### Raw Video Input Options

```bash
ffmpeg -f rawvideo -video_size 1920x1080 -pix_fmt yuv420p -framerate 30 \
  -i input.yuv output.mp4
```

**Important**: These are NOT position-sensitive like main options. They are format/protocol parameters and only apply when using that specific format.

---

## Hardware Acceleration Device Initialization

### CUDA (NVIDIA)

```bash
# Basic CUDA
ffmpeg -hwaccel cuda -i input.mp4 -c:v h264_nvenc output.mp4

# Specify device
ffmpeg -hwaccel cuda -hwaccel_device 0 -i input.mp4 -c:v h264_nvenc output.mp4

# Full GPU pipeline (decode + filter + encode on GPU)
ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i input.mp4 \
  -vf "scale_cuda=1920:1080" -c:v h264_nvenc output.mp4

# Initialize named device for filters
ffmpeg -init_hw_device cuda=gpu0:0 -filter_hw_device gpu0 \
  -i input.mp4 -vf "hwupload_cuda,scale_cuda=1920:1080,hwdownload" \
  -c:v libx264 output.mp4
```

### VAAPI (AMD/Intel Linux)

```bash
# Basic VAAPI
ffmpeg -hwaccel vaapi -hwaccel_device /dev/dri/renderD128 -i input.mp4 \
  -c:v h264_vaapi output.mp4

# VAAPI with output format
ffmpeg -hwaccel vaapi -hwaccel_output_format vaapi \
  -hwaccel_device /dev/dri/renderD128 -i input.mp4 \
  -vf "scale_vaapi=1920:1080" -c:v h264_vaapi output.mp4

# Using -vaapi_device shortcut
ffmpeg -vaapi_device /dev/dri/renderD128 -i input.mp4 \
  -vf "hwupload,scale_vaapi=1920:1080" -c:v h264_vaapi output.mp4
```

### QSV (Intel)

```bash
# Basic QSV
ffmpeg -hwaccel qsv -i input.mp4 -c:v h264_qsv output.mp4

# QSV with device specification
ffmpeg -qsv_device /dev/dri/renderD128 -hwaccel qsv \
  -i input.mp4 -c:v h264_qsv output.mp4

# Full QSV pipeline
ffmpeg -hwaccel qsv -hwaccel_output_format qsv -i input.mp4 \
  -vf "scale_qsv=1920:1080" -c:v h264_qsv output.mp4
```

### Vulkan (Cross-platform FFmpeg 7.1+/8.0+)

```bash
# Vulkan hardware acceleration
ffmpeg -init_hw_device vulkan=vk:0 -filter_hw_device vk \
  -i input.mp4 -vf "hwupload,scale_vulkan=1920:1080,hwdownload" \
  -c:v libx264 output.mp4

# Vulkan encoder (FFmpeg 8.0+)
ffmpeg -hwaccel vulkan -hwaccel_output_format vulkan -i input.mp4 \
  -c:v h264_vulkan output.mp4
```

### D3D11VA (Windows)

```bash
# D3D11 hardware acceleration
ffmpeg -hwaccel d3d11va -i input.mp4 -c:v h264_nvenc output.mp4

# With specific adapter
ffmpeg -hwaccel d3d11va -hwaccel_device 0 -i input.mp4 \
  -c:v hevc_amf output.mp4
```

### VideoToolbox (macOS)

```bash
# VideoToolbox decode + encode
ffmpeg -hwaccel videotoolbox -i input.mp4 \
  -c:v h264_videotoolbox output.mp4

# With ProRes
ffmpeg -i input.mov -c:v prores_videotoolbox output.mov
```

---

## Advanced Timestamp Handling

### Timestamp Options Explained

```bash
# Copy timestamps exactly from input
ffmpeg -copyts -i input.mp4 -c copy output.mp4

# Shift timestamps to start at zero
ffmpeg -start_at_zero -i input.mp4 -c copy output.mp4

# Both: copy but start at zero
ffmpeg -copyts -start_at_zero -i input.mp4 -c copy output.mp4

# Offset input timestamps
ffmpeg -itsoffset 5 -i input.mp4 -c copy output.mp4  # Delay by 5 seconds

# Scale input timestamps (2x speed)
ffmpeg -itsscale 0.5 -i input.mp4 -c copy output.mp4

# Handle negative timestamps
ffmpeg -i input.mp4 -avoid_negative_ts make_zero output.mp4
```

### Timestamp Modes

| Mode | Description |
|------|-------------|
| `make_non_negative` | Shift timestamps to be non-negative |
| `make_zero` | Shift to start at exactly zero |
| `auto` | Auto-select based on format |
| `disabled` | Don't adjust timestamps |

---

## Muxer-Specific Options

### MP4/MOV Muxer Flags (-movflags)

```bash
# Fast start (move moov atom to beginning for web)
ffmpeg -i input.mp4 -c copy -movflags +faststart output.mp4

# Fragmented MP4 (for DASH/streaming)
ffmpeg -i input.mp4 -c copy -movflags +frag_keyframe+empty_moov output.mp4

# Separate moov atom
ffmpeg -i input.mp4 -c copy -movflags +frag_keyframe+separate_moof output.mp4

# All common streaming flags
ffmpeg -i input.mp4 -c copy \
  -movflags +faststart+frag_keyframe+empty_moov+default_base_moof \
  output.mp4
```

| Flag | Description |
|------|-------------|
| `faststart` | Move moov before mdat (web streaming) |
| `frag_keyframe` | Fragment at each keyframe |
| `empty_moov` | Empty initial moov (DASH) |
| `separate_moof` | Separate moof for each track |
| `default_base_moof` | Base offset at moof (DASH) |
| `negative_cts_offsets` | Allow negative CTS offsets |
| `isml` | IIS Smooth Streaming |
| `omit_tfhd_offset` | Omit offset in tfhd |
| `disable_chpl` | Disable chapter track |
| `write_colr` | Write colr atom |
| `write_gama` | Write gama atom |

### MPEG-TS Muxer Options

```bash
# MPEG-TS with PCR
ffmpeg -i input.mp4 -c copy -mpegts_copyts 1 output.ts

# Set service info
ffmpeg -i input.mp4 -c copy \
  -mpegts_service_id 1 \
  -mpegts_service_type digital_tv \
  output.ts
```

### Matroska/WebM Muxer Options

```bash
# Cue points at clusters
ffmpeg -i input.mp4 -c:v libvpx-vp9 -cues_to_front 1 output.webm

# Set cluster size
ffmpeg -i input.mp4 -c copy -cluster_size_limit 2M output.mkv
```

---

## Bitstream Filters (-bsf)

```bash
# Extract AnnexB NAL units for H.264
ffmpeg -i input.mp4 -c:v copy -bsf:v h264_mp4toannexb output.h264

# Add SEI recovery point for broadcast
ffmpeg -i input.mp4 -c:v copy -bsf:v h264_redundant_pps output.mp4

# HEVC HVC1 to HEV1
ffmpeg -i input.mp4 -c:v copy -bsf:v hevc_mp4toannexb output.hevc

# Insert ADTS headers for AAC
ffmpeg -i input.mp4 -c:a copy -bsf:a aac_adtstoasc output.aac

# Remove filler data
ffmpeg -i input.mp4 -c:v copy -bsf:v filter_units=remove_types=6 output.mp4

# Metadata injection
ffmpeg -i input.mp4 -c:v copy -bsf:v h264_metadata=level=4.1 output.mp4
```

### Common Bitstream Filters

| Filter | Description |
|--------|-------------|
| `h264_mp4toannexb` | Convert H.264 to AnnexB format |
| `hevc_mp4toannexb` | Convert HEVC to AnnexB format |
| `aac_adtstoasc` | Convert AAC ADTS to ASC |
| `extract_extradata` | Extract codec extradata |
| `h264_redundant_pps` | Add redundant PPS |
| `h264_metadata` | Modify H.264 metadata |
| `hevc_metadata` | Modify HEVC metadata |
| `filter_units` | Filter NAL units |
| `dump_extra` | Dump extradata to packets |
| `prores_metadata` | Modify ProRes metadata |
| `vp9_superframe` | VP9 superframe handling |
| `av1_metadata` | Modify AV1 metadata |

---

## Metadata Mapping (-map_metadata)

The `-map_metadata` option copies metadata between files with fine-grained control.

### Syntax

```bash
-map_metadata[:metadata_spec_out] infile[:metadata_spec_in]
```

### Metadata Specifiers

| Specifier | Target |
|-----------|--------|
| `g` | Global file metadata |
| `s:stream_index` | Stream metadata |
| `s:v` / `s:a` / `s:s` | All video/audio/subtitle streams |
| `c:chapter_index` | Chapter metadata |
| `p:program_index` | Program metadata |

### Examples

```bash
# Copy all metadata from input to output
ffmpeg -i input.mp4 -map_metadata 0 -c copy output.mp4

# Copy global metadata only
ffmpeg -i input.mp4 -map_metadata:g 0:g -c copy output.mp4

# Strip all metadata
ffmpeg -i input.mp4 -map_metadata -1 -c copy output.mp4

# Copy metadata from second input file
ffmpeg -i video.mp4 -i metadata_source.mp4 -map 0 -map_metadata 1 -c copy output.mp4

# Copy stream metadata from input stream 0 to output stream 0
ffmpeg -i input.mp4 -map_metadata:s:0 0:s:0 -c copy output.mp4

# Copy chapter metadata
ffmpeg -i input.mp4 -map_metadata:c 0:c -map_chapters 0 -c copy output.mp4

# Copy all metadata, but set specific values
ffmpeg -i input.mp4 -map_metadata 0 -metadata title="New Title" -c copy output.mp4
```

### Metadata Manipulation

```bash
# Add/modify metadata
ffmpeg -i input.mp4 -metadata title="Video Title" -metadata artist="Creator" output.mp4

# Set stream-specific metadata
ffmpeg -i input.mp4 -metadata:s:v:0 title="Main Video" -metadata:s:a:0 language=eng output.mp4

# Set chapter metadata
ffmpeg -i input.mp4 -metadata:c:0 title="Chapter 1" output.mp4

# Remove specific metadata (set to empty)
ffmpeg -i input.mp4 -metadata comment= -c copy output.mp4
```

---

## Attachments

### Adding Attachments (-attach)

```bash
# Attach font file (for subtitles)
ffmpeg -i input.mkv -attach DejaVuSans.ttf \
  -metadata:s:t:0 mimetype=application/x-truetype-font \
  -c copy output.mkv

# Attach cover art
ffmpeg -i input.mp4 -attach cover.jpg \
  -metadata:s:t:0 mimetype=image/jpeg \
  -c copy output.mkv

# Multiple attachments
ffmpeg -i input.mkv \
  -attach font1.ttf -metadata:s:t:0 mimetype=application/x-truetype-font \
  -attach font2.ttf -metadata:s:t:1 mimetype=application/x-truetype-font \
  -c copy output.mkv
```

### Extracting Attachments (-dump_attachment)

```bash
# Extract first attachment to specific file
ffmpeg -dump_attachment:t:0 extracted_font.ttf -i input.mkv

# Extract all attachments (uses filename metadata)
ffmpeg -dump_attachment:t "" -i input.mkv

# Extract specific stream by index
ffmpeg -dump_attachment:3 attachment.bin -i input.mkv
```

---

## Disposition Flags

```bash
# Set stream as default
ffmpeg -i input.mkv -c copy -disposition:a:0 default output.mkv

# Set as default and forced subtitle
ffmpeg -i input.mkv -c copy -disposition:s:0 default+forced output.mkv

# Clear all dispositions
ffmpeg -i input.mkv -c copy -disposition:a:1 0 output.mkv

# Multiple dispositions
ffmpeg -i input.mkv -c copy \
  -disposition:v:0 default \
  -disposition:a:0 default \
  -disposition:a:1 0 \
  output.mkv
```

### Disposition Values

| Value | Description |
|-------|-------------|
| `default` | Default stream for playback |
| `dub` | Dubbed audio track |
| `original` | Original language |
| `comment` | Commentary track |
| `lyrics` | Lyrics track |
| `karaoke` | Karaoke version |
| `forced` | Forced subtitles |
| `hearing_impaired` | Subtitles for hearing impaired |
| `visual_impaired` | Audio for visually impaired |
| `clean_effects` | Clean audio effects |
| `attached_pic` | Attached picture (cover art) |
| `captions` | Closed captions |
| `descriptions` | Audio descriptions |
| `metadata` | Metadata stream |
| `dependent` | Dependent stream |
| `still_image` | Still image stream |

---

## References

- [FFmpeg Documentation](https://ffmpeg.org/ffmpeg.html)
- [FFmpeg Wiki - Seeking](https://fftrac-bg.ffmpeg.org/wiki/Seeking)
- [Stream Specifiers](https://ffmpeg.org/ffmpeg.html#Stream-specifiers)
- [FFmpeg Formats Documentation](https://ffmpeg.org/ffmpeg-formats.html)
- [FFmpeg Bitstream Filters](https://ffmpeg.org/ffmpeg-bitstream-filters.html)
