---
name: mathpix-ocr
description: Mathpix OCR for LaTeX extraction with balanced ternary checkpoints
---

# mathpix-ocr - Balanced Ternary OCR Pipeline for LaTeX → ACSet Extraction

## Overview

Integrates [TeglonLabs/mathpix-gem](https://github.com/TeglonLabs/mathpix-gem) for mathematical OCR with the music-topos ACSet parallel rewriting system. Uses seed 1069 balanced ternary checkpoints for resilient PDF batch processing.

## The 1069 Connection

mathpix-gem shares our canonical seed:

```ruby
# From mathpix-gem/lib/mathpix/balanced_ternary.rb
# 1×3⁶ - 1×3⁵ - 1×3⁴ + 1×3³ + 1×3² + 1×3¹ + 1×3⁰ = 1069
SEED_1069_PATTERN = [+1, -1, -1, +1, +1, +1, +1].freeze

# Semantics progression:
#   +1 (high confidence) → -1 (descent) → -1 (exploration) →
#   +1 (recovery) → +1 (convergence) → +1 (stability) → +1 (completion)
```

This maps directly to our TAP states and GF(3) arithmetic.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Mathpix OCR → ACSet Pipeline                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   PDF/Image                 Balanced Ternary              ACSet Schema      │
│      │                      Checkpoints                        │            │
│      ▼                           │                             ▼            │
│  ┌────────┐    ┌─────────────────┴─────────────────┐    ┌──────────────┐   │
│  │Mathpix │───▶│ +1 → -1 → -1 → +1 → +1 → +1 → +1 │───▶│ @present Sch │   │
│  │  OCR   │    │ ─── ─── ─── ─── ─── ─── ───       │    │   Type::Ob   │   │
│  └────────┘    │ 729  -243 -81  +27  +9   +3   +1  │    │   Term::Ob   │   │
│      │         └─────────────────┬─────────────────┘    └──────────────┘   │
│      │                           │                             │            │
│      ▼                           ▼                             ▼            │
│  LaTeX AST                 Confidence                   Colored ACSet       │
│  (extracted)               Sequence                    (with TAP states)    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## MCP Server Configuration

Add to `.ruler/ruler.toml`:

```toml
[mcp_servers.mathpix]
command = "ruby"
args = ["-I", "lib", "-r", "mathpix/mcp", "-e", "Mathpix::MCP.serve"]
env = { MATHPIX_APP_ID = "${MATHPIX_APP_ID}", MATHPIX_APP_KEY = "${MATHPIX_APP_KEY}" }
description = "Mathematical OCR with balanced ternary checkpoints"
```

Or via Claude MCP config:

```json
{
  "mcpServers": {
    "mathpix": {
      "command": "bundle",
      "args": ["exec", "ruby", "-r", "mathpix", "-e", "Mathpix::MCP.serve"],
      "env": {
        "MATHPIX_APP_ID": "${MATHPIX_APP_ID}",
        "MATHPIX_APP_KEY": "${MATHPIX_APP_KEY}",
        "GF3_SEED": "1069"
      }
    }
  }
}
```

## MCP Tools Available

| Tool | Description | TAP State |
|------|-------------|-----------|
| `convert_image` | Single image → LaTeX | LIVE |
| `convert_document` | PDF/DOCX → structured output | LIVE |
| `batch_convert` | Multiple files with checkpoints | VERIFY |
| `check_batch_status` | Poll batch progress | VERIFY |
| `get_batch_results` | Retrieve completed batch | BACKFILL |
| `list_conversions` | History of all conversions | BACKFILL |
| `configure` | Update API settings | VERIFY |
| `health_check` | Test API connectivity | ERGODIC |
| `smart_pdf_batch` | Auto-chunked large PDFs | LIVE → VERIFY → BACKFILL |

## LaTeX → ACSet Extraction

### Type Structure Mapping

```julia
# rama_acset_parallel.jl integration
struct LHoTTMapping
    latex::String
    type_structure::Dict{Symbol, Any}
    confidence::Float64
    tap_state::TAPState
    checkpoint_trit::Int  # -1, 0, or +1
end

function mathpix_to_acset(latex::String, seed::UInt64=0x42D)
    # Parse LaTeX to detect type-theoretic constructs
    constructs = extract_constructs(latex)

    # Create ACSet with colored parts
    @acset LHoTTACSet begin
        Type = length(constructs.types)
        Term = length(constructs.terms)
        typeof = constructs.type_assignments
        # Color each part via SplitMix64
    end
end
```

### Construct Detection

```ruby
# Ruby extraction layer
module Mathpix
  class LHoTTExtractor
    PATTERNS = {
      dependent_type: /\\Pi.*?:\\s*\\mathsf\{Type\}/,
      identity_type: /\\mathsf\{Id\}.*?\\left\(.*?\\right\)/,
      transport: /\\mathsf\{transport\}/,
      univalence: /\\mathsf\{ua\}/,
      fibration: /\\to\\s*\\mathsf\{Type\}/
    }.freeze

    def extract(latex)
      PATTERNS.map { |name, pattern|
        { construct: name, matches: latex.scan(pattern) }
      }.reject { |r| r[:matches].empty? }
    end
  end
end
```

## Balanced Ternary Checkpoints

For large PDFs, mathpix-gem uses 7-trit checkpoints:

```ruby
class BatchProcessor
  CHECKPOINT_PATTERN = BalancedTernary::SEED_1069_PATTERN

  def process_with_checkpoints(pages)
    pages.each_slice(chunk_size).with_index do |chunk, i|
      trit = CHECKPOINT_PATTERN[i % 7]
      confidence = case trit
        when +1 then 0.94  # High confidence phase
        when -1 then 0.90  # Exploration phase
        when 0  then 0.92  # Verification phase
      end

      result = process_chunk(chunk)
      checkpoint!(i, trit, result) if result.confidence >= confidence
    end
  end
end
```

### Checkpoint Recovery

```clojure
;; Babashka checkpoint recovery
(defn recover-from-checkpoint [batch-id]
  (let [checkpoints (db/query "SELECT * FROM checkpoints WHERE batch_id = ?" batch-id)
        last-valid (last (filter #(= 1 (:trit %)) checkpoints))]
    (when last-valid
      {:resume-from (:page last-valid)
       :accumulated-confidence (confidence-sequence (:index last-valid))
       :tap-state (trit-to-tap (:trit last-valid))})))
```

## Sonification Integration

Connect to skill_sonification.rb for audio feedback:

```ruby
# Skill availability maps to pitch via golden angle
class MathpixSkillVoice < SkillVoice
  def initialize
    super(
      skill_name: 'mathpix-ocr',
      index: 13,  # Position in skill registry
      tap_state: :LIVE
    )
  end

  # Confidence → amplitude mapping
  def amplitude_from_confidence(conf)
    (conf - 0.5) * 2.0  # Scale [0.5, 1.0] → [0.0, 1.0]
  end

  # Batch progress → duration
  def duration_from_progress(progress)
    0.1 + (progress * 0.4)  # 100ms base + up to 400ms
  end
end

# Generate Sonic Pi code for batch feedback
def sonify_batch_progress(batch)
  batch.checkpoints.map.with_index do |cp, i|
    <<~SONIC
      use_synth :#{TAP_WAVEFORMS[trit_to_tap(cp.trit)]}
      play #{pitch_from_index(i)}, amp: #{amplitude_from_confidence(cp.confidence)}, release: #{duration_from_progress(cp.progress)}
      sleep 0.125
    SONIC
  end.join("\n")
end
```

## ACSet Parallel Rewriting Integration

From `rama_acset_parallel.jl`:

```julia
# Create depot from Mathpix extraction
function mathpix_depot(extractions::Vector{LHoTTMapping}, seed::UInt64)
    depot = ColoredDepot{LHoTTMapping}(:mathpix, seed)

    for ex in extractions
        emit!(depot, ex)
    end

    # Apply rewrite rules for type normalization
    rules = [
        ColoredRewriteRule(:beta_reduce, is_beta_redex, reduce_beta, :rotate, nothing),
        ColoredRewriteRule(:eta_expand, needs_eta, add_eta, :complement, :VERIFY),
        ColoredRewriteRule(:transport_compose, has_transport_chain, compose_transports, :golden, :LIVE)
    ]

    rama_pipeline([depot], rules, seed)
end
```

### Vision Pro P3 Color Mapping

```julia
# Map LaTeX constructs to P3 color space
CONSTRUCT_COLORS = Dict(
    :dependent_type => p3_color(0.9, 0.3, 0.3),   # Red family
    :identity_type => p3_color(0.3, 0.9, 0.3),    # Green family
    :transport => p3_color(0.3, 0.3, 0.9),         # Blue family
    :univalence => p3_color(0.9, 0.9, 0.3),        # Yellow (special)
    :fibration => p3_color(0.9, 0.3, 0.9)          # Magenta (structural)
)
```

## World Integration

The mathpix-ocr skill is available in these Cat the Poetic Engineer worlds:

| World | Role | Harmonic Layer |
|-------|------|----------------|
| `type_theory_world` | Primary tool for HoTT extraction | Lydian mode |
| `sheaves_world` | Extract topos diagrams | Diminished chord |
| `spectral_world` | Parse spectral sequence diagrams | Cluster voicing |
| `paper_world` | General paper processing | Major 7th |

## Usage Examples

### Single Image Extraction

```bash
# Via MCP
claude mcp mathpix convert_image --path diagram.png --formats latex,asciimath

# Via CLI
bundle exec mathpix convert diagram.png --output-format latex
```

### Batch PDF with Checkpoints

```bash
# Start batch with 1069 checkpoint pattern
claude mcp mathpix smart_pdf_batch --path textbook.pdf --checkpoint-seed 1069

# Monitor progress
claude mcp mathpix check_batch_status --batch-id abc123

# Retrieve with sonification
claude mcp mathpix get_batch_results --batch-id abc123 --sonify true
```

### Direct ACSet Pipeline

```julia
using MathpixACSet

# Extract and convert to ACSet in one pipeline
acset = pdf_to_acset("hott_paper.pdf",
    seed=0x42D,
    checkpoint_pattern=SEED_1069,
    color_space=:display_p3
)

# Visualize with Clerk semantics
clerk_view(acset, palette=:golden_spiral)
```

## Error Recovery

### Confidence Sequence for Retry Logic

```ruby
module Mathpix
  class ResilientClient
    def convert_with_retry(input, max_retries: 7)
      confidences = BalancedTernary.confidence_sequence

      confidences.each_with_index do |threshold, i|
        result = convert(input)
        return result if result.confidence >= threshold

        # Adjust strategy based on trit
        case SEED_1069_PATTERN[i]
        when +1
          # High confidence phase - use aggressive settings
          input = preprocess_enhance(input)
        when -1
          # Exploration phase - try alternative formats
          input = try_alternative_format(input)
        when 0
          # Verification phase - validate partial results
          validate_partial(result)
        end
      end

      raise MaxRetriesExceeded
    end
  end
end
```

## See Also

- `acsets/SKILL.md` - ACSet algebraic databases
- `rama_acset_parallel.jl` - Data-parallel rewriting with R1 acceleration
- `skill_sonification.rb` - Audio feedback for skill availability
- `LHOTT_MATHPIX_EXTRACTION_GUIDE.md` - Comprehensive HoTT extraction guide
- [mathpix-gem README](https://github.com/TeglonLabs/mathpix-gem) - Full API documentation

## Commands

```bash
just mathpix-test          # Test API connectivity
just mathpix-extract       # Extract from sample image
just mathpix-batch         # Run batch with checkpoints
just mathpix-sonify        # Generate audio for batch
just mathpix-acset         # Full pipeline to ACSet
```
