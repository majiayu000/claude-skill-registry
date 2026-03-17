---
name: human-extractor
description: GPU-accelerated pipeline for detecting, tracking, and classifying humans in dashcam footage. This skill should be used when users need to extract human presence from videos, analyze dashcam footage for people detection, perform investigative analysis of human subjects in recordings, or classify individuals with optional head covering detection.
---

# Human Extractor Skill

## Description
GPU-accelerated pipeline for detecting, tracking, and classifying humans in dashcam footage. Processes MP4 videos to extract human crops with optional CLIP-based head covering classification, saving all outputs to a unified directory with comprehensive indexing.

## Purpose
Extract visual evidence of human presence from dashcam recordings for investigative analysis. Optimized for high throughput using NVDEC decoding, batched YOLOv8 detection, ByteTrack multi-object tracking, and optional CLIP classification.

---

## Usage

### Basic Invocation
```
Extract humans from Park_R videos on October 6, 2025
```

### Advanced Invocation
```
Scan Park_R\20251006 and 20251007, keep only frames with people,
save all outputs in one folder, add one full-frame per timestamp with boxes,
use my GPU at max, filter for head-covered individuals at 80% confidence
```

---

## Input Parameters

### Required
- **roots** (list[str]): One or more source directories containing MP4 files
  - Example: `["G:\\My Drive\\PROJECTS\\INVESTIGATION\\DASHCAM\\Park_R\\20251006"]`

### Core Detection
- **confidence** (float, default: 0.35): YOLOv8 detection confidence threshold (0.0-1.0)
- **iou** (float, default: 0.50): IoU threshold for NMS (0.0-1.0)
- **yolo_batch** (int, default: 64): YOLOv8 batch size (32-128 depending on VRAM)

### CLIP Filtering (Optional)
- **clip_filter.enabled** (bool, default: false): Enable head covering classification
- **clip_filter.threshold** (float, default: 0.80): CLIP confidence threshold
- **clip_filter.batch** (int, default: 384): CLIP batch size (256-512)

### Hardware Acceleration
- **nvdec** (bool, default: true): Use NVIDIA hardware video decoding
- **gpu_id** (int, default: 0): CUDA device ID

### Output Control
- **single_output_dir** (str, default: "parsed\\ALL_CROPS"): Unified output directory
- **save_full_frame** (bool, default: false): Save one annotated full-frame per timestamp
- **full_frame_maxw** (int, default: 1280): Max width for full-frame saves
- **draw_boxes** (bool, default: true): Annotate boxes on full-frames

### Filename Convention
- **filename_version** (str, default: "v1"): Version tag for output filenames

### Deduplication
- **dedup.enabled** (bool, default: true): Enable similarity deduplication
- **dedup.ssim** (float, default: 0.92): SSIM threshold (0.0-1.0)
- **dedup.rate_cap_per_track_per_min** (int, default: 12): Max crops per track per minute

### Parallel Processing
- **parallel.dates** (list[str], optional): Process multiple dates concurrently
- **parallel.max_workers** (int, default: 3): Max parallel date workers

---

## Output Format

### Success Response
```json
{
  "status": "ok",
  "summary": {
    "videos_processed": 142,
    "crops_saved": 4414,
    "frames_saved": 728,
    "gpu_util_avg": 0.85,
    "processing_time_sec": 2847,
    "errors": 0
  },
  "artifacts": {
    "index_csv": "G:\\My Drive\\PROJECTS\\APPS\\Human_Detection\\parsed\\ALL_CROPS\\INDEX.csv",
    "output_dir": "G:\\My Drive\\PROJECTS\\APPS\\Human_Detection\\parsed\\ALL_CROPS",
    "log_file": "G:\\My Drive\\PROJECTS\\APPS\\Human_Detection\\parsed\\ALL_CROPS\\run_20251006_143022.log"
  },
  "performance": {
    "nvdec_active": true,
    "yolo_batch": 64,
    "clip_batch": 384,
    "avg_fps": 48.3,
    "vram_peak_gb": 9.2
  },
  "notes": [
    "NVDEC hardware decoding active",
    "Batched YOLO=64, CLIP=384",
    "GPU utilization: 85%"
  ]
}
```

### Error Response
```json
{
  "status": "error",
  "error": "CUDA out of memory",
  "suggestion": "Reduce batch sizes: yolo_batch=48, clip_batch=256",
  "partial_results": {
    "videos_processed": 67,
    "crops_saved": 2103
  }
}
```

---

## Output Structure

### Directory Layout
```
parsed\ALL_CROPS\
├── INDEX.csv                                    # Global master index
├── INDEX.20251006_pid1234.csv                   # Shard (pre-merge)
├── run_20251006_143022.log                      # Execution log
│
# Crop files (per person detection)
├── 20251006__20251006142644_070785B__t15234__f365__trk017__x1014y46w266h659__c85__v1.webp
├── 20251006__20251006143844_070787B__t8420__f202__trk003__x234y567w180h420__c92__v1.webp
│
# Full-frame files (optional, one per timestamp)
├── 20251006__20251006142644_070785B__t15234__FRAME__v1.webp
└── 20251006__20251006143844_070787B__t8420__FRAME__v1.webp
```

### Filename Convention

**Crop Format:**
```
<date>__<video_stem>__t<ts_ms>__f<frame_idx>__trk<track_id>__x<x1>y<y1>w<w>h<h>__c<covered_0to100>__v<ver>.webp

Example:
20251006__20251006142644_070785B__t15234__f365__trk017__x1014y46w266h659__c85__v1.webp

Decoded:
- Date: 2025-10-06
- Video: 20251006142644_070785B.MP4
- Timestamp: 15234 ms
- Frame: 365
- Track: 17
- BBox: x=1014, y=46, w=266, h=659
- CLIP confidence: 85% (head covering)
- Version: v1
```

**Full-Frame Format:**
```
<date>__<video_stem>__t<ts_ms>__FRAME__v<ver>.webp

Example:
20251006__20251006142644_070785B__t15234__FRAME__v1.webp
```

### INDEX.csv Schema

```csv
dataset,date,video_rel,video_stem,frame_idx,ts_ms,track_id,x1,y1,w,h,person_conf,covered_conf,file_type,crop_file,sha1,bboxes_json,annotated,pipeline_ver,yolo_batch,clip_batch,nvdec,created_utc

# Example rows:
Park_R,20251006,20251006\20251006142644_070785B.MP4,20251006142644_070785B,365,15234,17,1014,46,266,659,0.92,0.85,crop,20251006__20251006142644_070785B__t15234__f365__trk017__x1014y46w266h659__c85__v1.webp,a3f2c8b9...,,,v1,64,384,1,2025-10-06T14:30:22Z
Park_R,20251006,20251006\20251006142644_070785B.MP4,20251006142644_070785B,365,15234,,,,,,,frame,20251006__20251006142644_070785B__t15234__FRAME__v1.webp,d4e1a2c7...,"[{""x1"":1014,""y1"":46,""w"":266,""h"":659,""conf"":0.92,""track"":17}]",1,v1,64,384,1,2025-10-06T14:30:22Z
```

**Column Definitions:**
- **dataset**: Source camera (Park_R, Park_F, Movie_F, Movie_R)
- **date**: YYYYMMDD
- **video_rel**: Relative path from dataset root
- **video_stem**: Filename without .MP4 extension
- **frame_idx**: Frame number in video
- **ts_ms**: Timestamp in milliseconds
- **track_id**: ByteTrack ID (empty for FRAME rows)
- **x1,y1,w,h**: Bounding box (empty for FRAME rows)
- **person_conf**: YOLOv8 detection confidence
- **covered_conf**: CLIP head covering confidence (0-100 scale, empty if disabled)
- **file_type**: "crop" or "frame"
- **crop_file**: Relative filename
- **sha1**: File hash for integrity
- **bboxes_json**: All detections in frame (FRAME rows only)
- **annotated**: 1 if boxes drawn on frame, 0 otherwise
- **pipeline_ver**: Semantic version tag
- **yolo_batch**: YOLO batch size used
- **clip_batch**: CLIP batch size used (0 if disabled)
- **nvdec**: 1 if NVDEC used, 0 otherwise
- **created_utc**: ISO 8601 timestamp

---

## Implementation Details

### Processing Pipeline

```
[MP4 Videos]
     │
     ▼
[NVDEC Decoder (GPU)]
  RGB tensor → CUDA Stream A
     │
     ▼
[YOLOv8s Detection]
  Batched (64 frames)
  FP16, conf=0.35
     │
     ▼
[ByteTrack Tracking]
  IoU=0.5, max_age=10
     │
     ├──────────────────────► [Full-Frame Saver]
     │                        (optional, downscaled, annotated)
     ▼
[ROI Align (GPU)]
  Extract crops on GPU
     │
     ▼
[CLIP Classification]  ◄────── (optional)
  Batched (384 crops)
  FP16, threshold=0.80
     │
     ▼
[Deduplication Filter]
  SSIM ≥ 0.92
  Rate cap: 12/min/track
     │
     ▼
[Async I/O Thread Pool]
  WebP encode (q=85)
  Shard INDEX writes
     │
     ▼
[Final Merge]
  INDEX.csv
```

### GPU Optimization Strategy

**Dual CUDA Streams:**
- Stream A: YOLOv8 detection
- Stream B: CLIP classification
- Overlap compute + memory transfers

**Dynamic Batching:**
- Accumulate frames until batch size reached
- Process immediately on timeout (100ms)
- Keep GPU pipeline full (80-90% utilization)

**Memory Management:**
- Pinned memory for faster CPU↔GPU transfers
- Pre-allocated tensor buffers
- Stream-ordered operations

**Decoder Priority:**
1. NVDEC (GPU hardware decoder) - 5-10x faster
2. CPU fallback (OpenCV) if NVDEC unavailable
3. Multi-threaded DataLoader (8-12 workers)

### Performance Targets (RTX 4080 16GB)

| Metric | Target | Notes |
|--------|--------|-------|
| GPU Utilization | 80-90% | NVDEC + dual streams + large batches |
| Throughput | 3-4 videos/min | Parking videos (2 FPS sampling) |
| VRAM Usage | 6-10 GB | YOLO=64, CLIP=384 |
| Latency | <30s per video | Including decode, detect, track, classify |

### Configuration Tuning

**If GPU util < 70%:**
1. Increase batch sizes: `yolo_batch=80`, `clip_batch=448`
2. Verify NVDEC active (check `nvdec_active` in response)
3. Increase parallel workers: `max_workers=4`

**If CUDA OOM:**
1. Reduce CLIP batch first: `clip_batch=256`
2. Then reduce YOLO batch: `yolo_batch=48`
3. Disable full-frame saves: `save_full_frame=false`

**If disk I/O bottleneck:**
1. Disable full-frame: `save_full_frame=false`
2. Reduce quality: `full_frame_maxw=960`, WebP q=75
3. Use faster storage (NVMe SSD)

---

## CLI Equivalent

```bash
# Basic usage
python -m src.cli.run_multi_dates \
  --root "G:\My Drive\PROJECTS\INVESTIGATION\DASHCAM\Park_R" \
  --out parsed\ALL_CROPS \
  --dates 20251006 20251007 \
  --use-nvdec --conf 0.35 --iou 0.5

# Advanced usage with CLIP filtering
python -m src.cli.run_multi_dates \
  --root "G:\My Drive\PROJECTS\INVESTIGATION\DASHCAM\Park_R" \
  --out parsed\ALL_CROPS \
  --dates 20251006 20251007 20251008 \
  --use-nvdec \
  --yolo-batch 64 \
  --clip-batch 384 \
  --clip-threshold 0.80 \
  --conf 0.35 \
  --iou 0.5 \
  --save-full-frame \
  --draw-boxes \
  --parallel 3
```

---

## Example Interactions

### Example 1: Basic Detection
**User:** "Extract all humans from Park_R videos on October 6"

**Skill invokes:**
```json
{
  "mode": "extract_humans",
  "roots": ["G:\\My Drive\\PROJECTS\\INVESTIGATION\\DASHCAM\\Park_R\\20251006"],
  "confidence": 0.35,
  "single_output_dir": "parsed\\ALL_CROPS",
  "nvdec": true
}
```

### Example 2: Advanced with CLIP
**User:** "Scan Park_R for October 6-8, filter for people with head coverings at 80% confidence, save annotated frames, max GPU usage"

**Skill invokes:**
```json
{
  "mode": "extract_humans",
  "roots": [
    "G:\\My Drive\\PROJECTS\\INVESTIGATION\\DASHCAM\\Park_R\\20251006",
    "G:\\My Drive\\PROJECTS\\INVESTIGATION\\DASHCAM\\Park_R\\20251007",
    "G:\\My Drive\\PROJECTS\\INVESTIGATION\\DASHCAM\\Park_R\\20251008"
  ],
  "confidence": 0.35,
  "iou": 0.50,
  "yolo_batch": 64,
  "clip_filter": {
    "enabled": true,
    "threshold": 0.80,
    "batch": 384
  },
  "nvdec": true,
  "save_full_frame": true,
  "draw_boxes": true,
  "single_output_dir": "parsed\\ALL_CROPS",
  "parallel": {
    "max_workers": 3
  }
}
```

### Example 3: Low-Resource Mode
**User:** "Process Park_R October 6 with minimal GPU memory"

**Skill invokes:**
```json
{
  "mode": "extract_humans",
  "roots": ["G:\\My Drive\\PROJECTS\\INVESTIGATION\\DASHCAM\\Park_R\\20251006"],
  "confidence": 0.35,
  "yolo_batch": 32,
  "clip_filter": {
    "enabled": false
  },
  "nvdec": false,
  "save_full_frame": false,
  "single_output_dir": "parsed\\ALL_CROPS"
}
```

---

## Safety & Guardrails

### Do Not
- ❌ Move or delete source MP4 files
- ❌ Infer gender unless explicitly enabled (sensitive, noisy)
- ❌ Process videos without user consent
- ❌ Share outputs containing identifiable persons

### Do
- ✅ Verify GPU availability before processing
- ✅ Enforce longitude sign corrections for GPS overlays
- ✅ Maintain audit trail in INDEX.csv
- ✅ Log versions, batches, NVDEC usage
- ✅ Handle OOM gracefully with suggestions

### Resume Safety
- Idempotent: skip already-processed crops by filename
- Shard-based: partial runs can resume
- Index integrity: SHA1 hashes verify file correctness

---

## Testing & Verification

### Pre-Run Checks
```python
# GPU availability
assert torch.cuda.is_available(), "CUDA required"
assert torch.cuda.device_count() > 0, "No GPU found"

# Model files
assert Path("models/yolov8s.pt").exists(), "YOLOv8 model missing"

# Output directory writable
output_dir = Path("parsed/ALL_CROPS")
output_dir.mkdir(parents=True, exist_ok=True)
assert os.access(output_dir, os.W_OK), "Output dir not writable"
```

### Post-Run Verification
```python
# Check outputs exist
assert Path("parsed/ALL_CROPS/INDEX.csv").exists()
assert len(list(Path("parsed/ALL_CROPS").glob("*.webp"))) > 0

# Validate INDEX.csv
df = pd.read_csv("parsed/ALL_CROPS/INDEX.csv")
assert df['crop_file'].notna().all()
assert df['person_conf'].between(0, 1).all()

# Sample roundtrip
sample = df.sample(1).iloc[0]
assert Path(f"parsed/ALL_CROPS/{sample['crop_file']}").exists()

# GPU utilization check
assert gpu_util_avg > 0.70, f"Low GPU util: {gpu_util_avg}"
```

---

## Dependencies

### Required
- Python 3.10+
- PyTorch 2.0+ with CUDA 11.8+
- ultralytics (YOLOv8)
- transformers (CLIP)
- opencv-python
- pillow
- pandas
- numpy

### Optional (Performance)
- NVIDIA Video Codec SDK (NVDEC)
- TensorRT (future optimization)
- nvJPEG (GPU JPEG encoding)

### Installation
```bash
cd "G:\My Drive\PROJECTS\APPS\Human_Detection"
pip install -r requirements.txt
```

---

## Troubleshooting

### Common Issues

**1. CUDA Out of Memory**
```
Error: CUDA out of memory. Tried to allocate 2.50 GiB
Solution: Reduce batch sizes
  yolo_batch: 64 → 48 → 32
  clip_batch: 384 → 256 → 128
```

**2. NVDEC Not Available**
```
Warning: NVDEC unavailable, falling back to CPU decode
Solution: Check NVIDIA driver version (≥525.60)
  GPU must support Video Codec SDK
  Verify with: nvidia-smi --query-gpu=name --format=csv
```

**3. Low GPU Utilization**
```
Warning: GPU util only 45%
Solutions:
  1. Increase batch sizes (if VRAM allows)
  2. Enable NVDEC: nvdec=true
  3. Increase parallel workers: max_workers=4
  4. Check CPU bottleneck (use more DataLoader workers)
```

**4. Slow Processing**
```
Performance: 0.8 videos/min (expected 3-4)
Diagnostics:
  1. Check disk I/O (use SSD)
  2. Verify NVDEC active (5-10x faster than CPU)
  3. Profile with: python -m torch.utils.bottleneck script.py
```

---

## Future Enhancements

### Planned
- TensorRT optimization (2-4x CLIP speedup)
- Multi-GPU sharding (process different dates on different GPUs)
- GPU JPEG/WebP encoding (nvJPEG)
- Real-time streaming mode

### Under Consideration
- Face recognition integration
- Gender classification (opt-in only, with warnings)
- Action recognition (walking, standing, etc.)
- Multi-camera fusion (correlate detections across cameras)

---

## Version History

**v1.0** (Current)
- Initial release
- YOLOv8s + ByteTrack + CLIP
- NVDEC support
- Unified output directory
- Global INDEX.csv

---

## References

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [ByteTrack Paper](https://arxiv.org/abs/2110.06864)
- [CLIP Paper](https://arxiv.org/abs/2103.00020)
- [NVIDIA Video Codec SDK](https://developer.nvidia.com/video-codec-sdk)

---

## Contact & Support

For issues or questions:
1. Check `parsed/ALL_CROPS/run_*.log` for error details
2. Review GPU diagnostics: `nvidia-smi`
3. Validate input paths exist and are readable
4. Verify CUDA/PyTorch installation: `python -c "import torch; print(torch.cuda.is_available())"`
