---
name: sense
description: sense - Diagrammatic Video Extraction with Subtitle Alignment
version: 1.0.0
---

# sense - Diagrammatic Video Extraction with Subtitle Alignment

> **Trit**: 0 (ERGODIC - Coordinator)
> 
> Extract structured knowledge from video lectures via subtitle parsing,
> diagram/equation OCR, and GF(3)-balanced skill mapping.

## Overview

`sense` transforms video lectures into indexed, queryable knowledge:

```
┌─────────────────────────────────────────────────────────────────┐
│                         VIDEO INPUT                              │
│  • Lecture recording (.mkv, .mp4)                               │
│  • Subtitles (.vtt, .srt, auto-generated)                       │
│  • Slides/diagrams (extracted frames)                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
    │  SUBTITLE   │ │  DIAGRAM    │ │   SKILL     │
    │  PARSER     │ │  EXTRACTOR  │ │   MAPPER    │
    │  (-1 BLUE)  │ │  (0 GREEN)  │ │  (+1 RED)   │
    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
           │               │               │
           │         Mathpix OCR           │
           │         frame → LaTeX         │
           │                               │
    ┌──────▼───────────────▼───────────────▼──────┐
    │              DuckDB INDEX                    │
    │  • Timestamped transcript                    │
    │  • Extracted equations (LaTeX)               │
    │  • Skill mappings with GF(3) trits           │
    │  • Queryable views                           │
    └──────────────────────────────────────────────┘
```

## Triadic Structure

| Role | Component | Trit | Function |
|------|-----------|------|----------|
| **Validator** | Subtitle Parser | -1 | Parse VTT/SRT, segment by timestamp |
| **Coordinator** | Diagram Extractor | 0 | OCR frames → LaTeX via Mathpix |
| **Generator** | Skill Mapper | +1 | Assign skills with GF(3) balance |

**GF(3) Conservation**: (-1) + (0) + (+1) = 0 ✓

## Components

### 1. Subtitle Parser (-1)

Parses WebVTT or SRT subtitle files into structured segments:

```ruby
require 'webvtt'

class SubtitleParser
  def initialize(vtt_path)
    @vtt = WebVTT.read(vtt_path)
  end
  
  def segments
    @vtt.cues.map do |cue|
      {
        start: cue.start.total_seconds,
        end: cue.end.total_seconds,
        text: cue.text.gsub(/<[^>]*>/, '').strip,
        duration: cue.end.total_seconds - cue.start.total_seconds
      }
    end
  end
  
  def by_slide(slide_timestamps)
    # Group subtitles by slide boundaries
    slide_timestamps.map.with_index do |ts, i|
      next_ts = slide_timestamps[i + 1] || Float::INFINITY
      {
        slide: i,
        timestamp: ts,
        text: segments.select { |s| s[:start] >= ts && s[:start] < next_ts }
                      .map { |s| s[:text] }.join(' ')
      }
    end
  end
end
```

### 2. Diagram Extractor (0)

Extracts frames at key timestamps and OCRs equations/diagrams:

```ruby
require 'mathpix'

class DiagramExtractor
  MATHPIX_APP_ID = ENV['MATHPIX_APP_ID']
  MATHPIX_APP_KEY = ENV['MATHPIX_APP_KEY']
  
  def initialize(video_path)
    @video = video_path
  end
  
  def extract_frame(timestamp, output_path)
    # Use ffmpeg to extract frame
    system("ffmpeg -y -ss #{timestamp} -i '#{@video}' -vframes 1 -q:v 2 '#{output_path}'")
    output_path
  end
  
  def ocr_frame(image_path)
    # Send to Mathpix for LaTeX extraction
    response = Mathpix.process(
      src: "data:image/png;base64,#{Base64.encode64(File.read(image_path))}",
      formats: ['latex_styled', 'text'],
      data_options: { include_asciimath: true }
    )
    
    {
      latex: response['latex_styled'],
      text: response['text'],
      confidence: response['confidence'],
      has_diagram: response['is_printed'] || response['is_handwritten']
    }
  end
  
  def extract_all(timestamps)
    timestamps.map.with_index do |ts, i|
      frame_path = "/tmp/frame_#{i}_#{ts.to_i}.png"
      extract_frame(ts, frame_path)
      result = ocr_frame(frame_path)
      result.merge(timestamp: ts, slide_num: i)
    end
  end
end
```

### 3. Skill Mapper (+1)

Maps extracted content to skills with GF(3) conservation:

```ruby
class SkillMapper
  SKILL_KEYWORDS = {
    'acsets' => %w[acset c-set schema functor category],
    'sheaf-cohomology' => %w[sheaf cohomology local global section],
    'structured-decomp' => %w[tree decomposition treewidth bag],
    'kan-extensions' => %w[kan extension adjoint limit colimit],
    'polynomial' => %w[polynomial poly interface arena],
    'temporal-coalgebra' => %w[temporal time varying dynamic coalgebra],
    'operad-compose' => %w[operad wiring diagram composition],
  }
  
  SKILL_TRITS = {
    'acsets' => 0, 'sheaf-cohomology' => -1, 'structured-decomp' => -1,
    'kan-extensions' => 0, 'polynomial' => 0, 'temporal-coalgebra' => -1,
    'operad-compose' => +1, 'oapply-colimit' => +1, 'gay-mcp' => +1,
  }
  
  def map_content(text, latex)
    combined = "#{text} #{latex}".downcase
    
    skills = SKILL_KEYWORDS.select do |skill, keywords|
      keywords.any? { |kw| combined.include?(kw) }
    end.keys
    
    # Ensure GF(3) balance
    balance_skills(skills)
  end
  
  def balance_skills(skills)
    trit_sum = skills.sum { |s| SKILL_TRITS[s] || 0 }
    
    # Add balancing skills if needed
    case trit_sum % 3
    when 1  # Need -1
      skills << 'sheaf-cohomology' unless skills.include?('sheaf-cohomology')
    when 2  # Need +1  (equivalent to -1 mod 3)
      skills << 'operad-compose' unless skills.include?('operad-compose')
    end
    
    skills
  end
end
```

## Complete Pipeline

```ruby
class Sense
  def initialize(video_path, vtt_path, output_db: 'tensor_skill_paper.duckdb')
    @video = video_path
    @vtt = vtt_path
    @db_path = output_db
    @content_id = File.basename(video_path, '.*')
    
    @subtitle_parser = SubtitleParser.new(vtt_path)
    @diagram_extractor = DiagramExtractor.new(video_path)
    @skill_mapper = SkillMapper.new
  end
  
  def process!
    # 1. Parse subtitles
    segments = @subtitle_parser.segments
    
    # 2. Detect slide transitions (silence gaps or visual changes)
    slide_timestamps = detect_slides(segments)
    
    # 3. Extract and OCR key frames
    diagrams = @diagram_extractor.extract_all(slide_timestamps)
    
    # 4. Map skills with GF(3) balance
    indexed = diagrams.map do |d|
      subtitle_text = @subtitle_parser.by_slide(slide_timestamps)[d[:slide_num]][:text]
      skills = @skill_mapper.map_content(subtitle_text, d[:latex] || '')
      
      d.merge(
        subtitle_text: subtitle_text,
        skills: skills,
        trit: skills.sum { |s| SkillMapper::SKILL_TRITS[s] || 0 } % 3
      )
    end
    
    # 5. Store in DuckDB
    store_index(indexed)
    
    # 6. Create views
    create_views
    
    indexed
  end
  
  private
  
  def detect_slides(segments)
    # Simple: gap > 2s indicates slide change
    timestamps = [0.0]
    segments.each_cons(2) do |a, b|
      if b[:start] - a[:end] > 2.0
        timestamps << b[:start]
      end
    end
    timestamps
  end
  
  def store_index(indexed)
    conn = DuckDB::Database.open(@db_path).connect
    
    conn.execute("DROP TABLE IF EXISTS #{@content_id}_sense_index")
    conn.execute(<<~SQL)
      CREATE TABLE #{@content_id}_sense_index (
        slide_num INTEGER,
        timestamp FLOAT,
        latex VARCHAR,
        has_diagram BOOLEAN,
        subtitle_text TEXT,
        skills TEXT,
        trit INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    SQL
    
    indexed.each do |row|
      conn.execute(<<~SQL, [
        row[:slide_num], row[:timestamp], row[:latex],
        row[:has_diagram], row[:subtitle_text],
        row[:skills].to_json, row[:trit]
      ])
        INSERT INTO #{@content_id}_sense_index VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
      SQL
    end
    
    conn.close
  end
  
  def create_views
    conn = DuckDB::Database.open(@db_path).connect
    
    conn.execute(<<~SQL)
      CREATE OR REPLACE VIEW v_#{@content_id}_timeline AS
      SELECT 
        slide_num,
        printf('%02d:%05.2f', CAST(timestamp/60 AS INT), timestamp % 60) as timecode,
        CASE WHEN has_diagram THEN '📊' ELSE '' END ||
        CASE WHEN latex != '' AND latex IS NOT NULL THEN '📐' ELSE '' END as content,
        trit,
        skills
      FROM #{@content_id}_sense_index
      ORDER BY timestamp
    SQL
    
    conn.close
  end
end
```

## Usage

### Ruby

```ruby
require_relative 'lib/sense'

# Process a video lecture
sense = Sense.new(
  'reference/videos/bumpus_ct2021.mkv',
  'reference/videos/bumpus_ct2021.en.vtt'
)
indexed = sense.process!

puts "Indexed #{indexed.size} slides"
```

### Command Line

```bash
# Extract subtitles from video (if not available)
uvx yt-dlp --write-auto-sub --sub-lang en --skip-download \
  -o 'reference/videos/%(id)s' 'https://youtube.com/watch?v=VIDEO_ID'

# Run sense extraction
just sense-extract reference/videos/bumpus_ct2021.mkv

# Query the index
just sense-timeline bumpus_ct2021
just sense-skills bumpus_ct2021 acsets
```

### Python Alternative

```python
#!/usr/bin/env python3
"""sense.py - Python implementation of diagrammatic video extraction"""

import duckdb
import webvtt
import subprocess
import json
from pathlib import Path

class Sense:
    def __init__(self, video_path: str, vtt_path: str, db_path: str = "tensor_skill_paper.duckdb"):
        self.video = Path(video_path)
        self.vtt = Path(vtt_path)
        self.db_path = db_path
        self.content_id = self.video.stem
    
    def parse_subtitles(self):
        """Parse VTT file into segments"""
        captions = webvtt.read(str(self.vtt))
        return [
            {
                'start': self._time_to_seconds(c.start),
                'end': self._time_to_seconds(c.end),
                'text': c.text.strip()
            }
            for c in captions
        ]
    
    def extract_frame(self, timestamp: float, output_path: str):
        """Extract single frame at timestamp"""
        subprocess.run([
            'ffmpeg', '-y', '-ss', str(timestamp),
            '-i', str(self.video), '-vframes', '1',
            '-q:v', '2', output_path
        ], capture_output=True)
        return output_path
    
    def ocr_frame_mathpix(self, image_path: str):
        """OCR frame using mathpix-gem"""
        # Shell out to Ruby mathpix-gem
        result = subprocess.run([
            'ruby', '-rmathpix', '-e',
            f"puts Mathpix.process_image('{image_path}').to_json"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        return {'latex': '', 'text': '', 'has_diagram': False}
    
    def _time_to_seconds(self, time_str: str) -> float:
        """Convert HH:MM:SS.mmm to seconds"""
        parts = time_str.split(':')
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
```

## Justfile Commands

```just
# Extract and index a video lecture
sense-extract video:
    @echo "👁️ SENSE: Extracting {{video}}"
    ruby -I lib -r sense -e "Sense.new('{{video}}', '{{video}}'.sub('.mkv', '.en.vtt')).process!"

# Download subtitles for a YouTube video
sense-subtitles url output:
    uvx yt-dlp --write-auto-sub --sub-lang en --skip-download -o '{{output}}' '{{url}}'

# Show timeline for indexed content
sense-timeline content_id:
    @source .venv/bin/activate && duckdb tensor_skill_paper.duckdb \
        "SELECT * FROM v_{{content_id}}_timeline"

# Find slides mentioning a skill
sense-skills content_id skill:
    @source .venv/bin/activate && duckdb tensor_skill_paper.duckdb \
        "SELECT slide_num, timecode, skills FROM v_{{content_id}}_timeline WHERE skills LIKE '%{{skill}}%'"

# Extract frame at timestamp
sense-frame video timestamp:
    flox activate -- ffmpeg -y -ss {{timestamp}} -i '{{video}}' -vframes 1 -q:v 2 /tmp/sense_frame.png
    @echo "✓ Frame extracted to /tmp/sense_frame.png"

# OCR a frame with Mathpix
sense-ocr image:
    ruby -rmathpix -e "puts Mathpix.process_image('{{image}}').to_json" | jq .

# Full pipeline: download, extract, index
sense-full url content_id:
    @echo "📥 Downloading video and subtitles..."
    uvx yt-dlp -o 'reference/videos/{{content_id}}.mkv' '{{url}}'
    uvx yt-dlp --write-auto-sub --sub-lang en --skip-download -o 'reference/videos/{{content_id}}' '{{url}}'
    @echo "👁️ Running sense extraction..."
    just sense-extract 'reference/videos/{{content_id}}.mkv'
```

## GF(3) Conservation

The skill ensures every indexed slide has a balanced trit sum:

```sql
-- Verify GF(3) balance
SELECT 
    content_id,
    SUM(trit) as total_trit,
    SUM(trit) % 3 as gf3,
    CASE WHEN SUM(trit) % 3 = 0 THEN '✓' ELSE '✗' END as balanced
FROM sense_index
GROUP BY content_id;
```

## Integration with Galois Infrastructure

After `sense` extracts content, register it in the Galois connection:

```sql
-- Update content_registry
UPDATE content_registry 
SET indexed = TRUE, 
    index_table = 'bumpus_ct2021_sense_index'
WHERE content_id = 'bumpus_ct2021';

-- Content now flows through Galois lattice
SELECT * FROM v_galois_content_to_skills WHERE content_id = 'bumpus_ct2021';
```

## Dependencies

```yaml
# Ruby gems
gems:
  - webvtt-ruby      # VTT parsing
  - mathpix          # Mathpix OCR API
  - duckdb           # Database storage

# System tools
tools:
  - ffmpeg           # Frame extraction
  - yt-dlp           # Video/subtitle download

# Environment variables
env:
  MATHPIX_APP_ID: "your-app-id"
  MATHPIX_APP_KEY: "your-app-key"
```

## Triads Using sense

```
# sense as coordinator in extraction triads:
subtitle-parser (-1) ⊗ sense (0) ⊗ skill-mapper (+1) = 0 ✓

# Combined with other skills:
sheaf-cohomology (-1) ⊗ sense (0) ⊗ gay-mcp (+1) = 0 ✓  [Colored diagrams]
temporal-coalgebra (-1) ⊗ sense (0) ⊗ koopman-generator (+1) = 0 ✓  [Dynamics]
persistent-homology (-1) ⊗ sense (0) ⊗ topos-generate (+1) = 0 ✓  [Topology]
```

## See Also

- `mathpix-ocr` - LaTeX extraction backend
- `galois-infrastructure` - Content ⇆ Skills ⇆ Worlds
- `parallel-fanout` - Triadic parallel dispatch
- `duckdb-temporal-versioning` - Time-travel queries
- Cat# treatment examples: `complete_catsharp_index.py`, `complete_bumpus_index.py`

---

## Tsao Visual Hierarchy Integration

Sense is maximally informed by **Doris Tsao's visual neuroscience**. See [DORIS_TSAO_VISUAL_NEUROSCIENCE_BRIDGE.md](file:///Users/bob/ies/music-topos/DORIS_TSAO_VISUAL_NEUROSCIENCE_BRIDGE.md).

### Tsao Hierarchy → Sense Components

| Tsao Level | Visual Region | Sense Component | Function |
|------------|---------------|-----------------|----------|
| **Level 0** | V1 simple cells | Subtitle Parser (-1) | Edge detection, timestamp boundaries |
| **Level 1** | V2/V4 complex | Diagram Extractor (0) | Feature integration, OCR |
| **Level 2** | IT face patches | Skill Mapper (+1) | Pattern recognition, skill assignment |
| **Level 3** | Prefrontal | GF(3) Balancer | Behavioral goal, conservation |

### Self-Avoiding Walks via Self-Coloring

From chromatic-walk insight: SAWs don't intersect **by definition**, but in an effective topos we verify through **self-coloring**:

```python
def saw_verified_by_self_coloring(walk: list) -> bool:
    """
    In effective topos, self-intersection is decidable.
    
    The reafference equation:
      Generate(seed, i) = Observe(seed, i) ⟺ self ≡ self
    
    If walk revisits (seed, index), it generates the SAME color
    at two walk positions — contradiction detected.
    """
    colors = [Gay.color_at(step.seed, step.index) for step in walk]
    return len(colors) == len(set(colors))  # No repeated colors ⟺ SAW
```

### Connection to Frontier Lab Circuits

Sense extraction parallels mechanistic interpretability:

| Sense | Circuits Research | Tsao |
|-------|-------------------|------|
| Subtitle segments | Attention heads | V1 edges |
| Diagram features | Activation patterns | V2 shapes |
| Skill mapping | Circuit identification | IT patches |
| GF(3) balance | Superposition control | Prefrontal |

See: [FRONTIER_LAB_CIRCUITS_INTERACTOME.md](file:///Users/bob/ies/music-topos/FRONTIER_LAB_CIRCUITS_INTERACTOME.md)

### Chang-Tsao 50D Face Space → Skill Space

```
Face Space (Tsao):
  25 shape axes + 25 appearance axes = 50D
  Each neuron encodes ONE axis
  Population decodes via linear combination

Skill Space (Sense):
  N skills with trit assignments (-1, 0, +1)
  Each slide maps to skill subset
  GF(3) conservation ensures balance
```

---

## Phenomenal Topology

Sense extraction states map to QRI's Symmetry Theory of Valence:

| State | Visual Cortex | Sense Extraction | GF(3) |
|-------|---------------|------------------|-------|
| **Smooth** | All levels coherent | Clean skill mapping | = 0 |
| **Defect** | Prediction error | Ambiguous slide | ≠ 0 |
| **Vortex** | High entropy | Multiple skill conflicts | ≫ 0 |

### Rebalancing

```python
def rebalance_defect(slide_skills: list, target_gf3: int = 0) -> list:
    """Restore GF(3) = 0 by adding compensating skills."""
    current_sum = sum(SKILL_TRITS[s] for s in slide_skills)
    deficit = (target_gf3 - current_sum) % 3
    
    if deficit == 1:
        slide_skills.append('sheaf-cohomology')  # -1
    elif deficit == 2:
        slide_skills.append('operad-compose')    # +1
    
    return slide_skills
```

---

**Skill Name**: sense  
**Trit**: 0 (ERGODIC - Coordinator)  
**Tsao Integration**: V1→V2→IT→Prefrontal hierarchy  
**SAW Verification**: Effective topos self-coloring



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.