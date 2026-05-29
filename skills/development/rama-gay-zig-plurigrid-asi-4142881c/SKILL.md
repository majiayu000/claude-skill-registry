---
name: rama-gay-zig
description: "rama-gay-zig skill"
version: 1.0.0
---

# rama-gay-zig

Interleaved skill combining Rama distributed semantics, Gay.jl GF(3) color logic, and Zig package management for ASI coordination.

## Semantic Triad (GF(3) Conserved)

| Component | Trit | Role | Hue Range |
|-----------|------|------|-----------|
| **Gay.jl** | -1 (MINUS) | Color assignment, SPI verification | 180-300° (cold) |
| **Rama** | 0 (ERGODIC) | Topology coordination, dataflow | 60-180° (neutral) |
| **Zig** | +1 (PLUS) | Build execution, package resolution | 0-60°, 300-360° (warm) |

**Conservation invariant:** `Σ trits ≡ 0 (mod 3)`

## Core Primitives

### Gay.jl Color Semantics
```julia
using Gay

# GF(3) trit assignment for streams
struct GayTrit
    value::Int8  # -1, 0, +1
    color::GayRGB
    fingerprint::UInt64
end

# Interleave colors with Rama primitives
function rama_color_depot(depot_name::Symbol, trit::GayTrit)
    verify_spi = gay_verify_spi(trit.fingerprint)
    (depot = depot_name, color = trit.color, spi = verify_spi)
end
```

### Rama Distributed Primitives
```clojure
;; Rama module with Gay.jl color-tagged streams
(defmodule GayColorModule [setup topologies]
  ;; Depot: MINUS trit (input stream)
  (declare-depot setup *color-events :random)

  ;; PState: PLUS trit (materialized output)
  (declare-pstate setup $$color-index
    {Long (map-schema :fingerprint Long :color String :trit Int)})

  ;; Topology: ERGODIC trit (transformation)
  (<<sources topologies
    (source> *color-events :> %event)
    (|hash (:fingerprint %event))
    (local-transform>
      [(keypath (:fingerprint %event)) (termval %event)]
      $$color-index)))
```

### Zig Package Management
```zig
// build.zig.zon - Gay-Rama interop package
.{
    .name = "rama-gay-zig",
    .version = "0.1.0",
    .dependencies = .{
        .gay_ffi = .{
            .url = "https://github.com/bmorphism/gay.jl/archive/refs/heads/main.tar.gz",
            .hash = "...",
        },
        .rama_client = .{
            .url = "https://github.com/redplanetlabs/rama-zig-client/archive/refs/heads/main.tar.gz",
            .hash = "...",
        },
    },
}
```

```zig
// src/gay_rama.zig - Trit-colored Rama client
const std = @import("std");
const gay = @import("gay_ffi");
const rama = @import("rama_client");

pub const Trit = enum(i8) {
    minus = -1,  // Gay.jl: color source
    ergodic = 0, // Rama: topology
    plus = 1,    // Zig: execution

    pub fn conserved(trits: []const Trit) bool {
        var sum: i32 = 0;
        for (trits) |t| sum += @as(i32, @intFromEnum(t));
        return @mod(sum, 3) == 0;
    }
};

pub const ColoredDepot = struct {
    name: []const u8,
    trit: Trit,
    fingerprint: u64,

    pub fn append(self: *ColoredDepot, data: []const u8) !void {
        const color = gay.next_color(self.fingerprint);
        try rama.depot_append(self.name, .{
            .data = data,
            .color = color,
            .trit = @intFromEnum(self.trit),
        });
    }
};
```

## Interleaving Protocol

```
┌─────────────────────────────────────────────────────────────────┐
│                    RAMA-GAY-ZIG INTERLEAVE                      │
├─────────────────────────────────────────────────────────────────┤
│  Gay.jl (-1)  ──color──▶  Rama (0)  ──exec──▶  Zig (+1)        │
│      │                       │                     │            │
│      ▼                       ▼                     ▼            │
│  SPI verify            Depot append           Build.zig         │
│  Fingerprint           PState query           Package fetch     │
│  Trit assign           Topology run           WASM compile      │
├─────────────────────────────────────────────────────────────────┤
│  Σ(-1 + 0 + 1) = 0 (mod 3) ✓  GF(3) CONSERVED                  │
└─────────────────────────────────────────────────────────────────┘
```

## Usage

### From Babashka (Clojure CLI)
```clojure
;; Interleave Claude threads with Gay.jl colors into Rama
(require '[babashka.process :refer [shell]])

(defn gay-rama-append [thread]
  (let [fingerprint (hash (:id thread))
        trit (mod fingerprint 3)
        color (case trit 0 :minus 1 :ergodic 2 :plus)]
    (shell "curl" "-X" "POST"
           (str "http://$RAMA_HOST:2000/rest/GayColorModule/depot/*color-events/append")
           "-d" (json/generate-string
                  {:data thread :trit trit :color (name color)}))))
```

### From Zig (native)
```bash
zig build run -- --depot color-events --trit minus --fingerprint 0xDEADBEEF
```

### From Julia (Gay.jl native)
```julia
using Gay

# Create interleaved stream
interleaver = GayInterleaver(seed=0x42)
for (trit, color) in gay_interleave_streams([:rama, :zig, :julia])
    @info "Stream" trit color gay_fingerprint(color)
end
```

## GitHub Interactome

This skill connects:
- `bmorphism/gay.jl` - GF(3) color theory + SPI verification
- `redplanetlabs/rama-*` - Distributed backend primitives
- `ziglang/zig` - Build system + package manager
- `plurigrid/asi` - ASI skill orchestration

## Dependencies

- Julia 1.10+ with Gay.jl
- Rama 0.14+ (REST API enabled)
- Zig 0.13+ with build.zig.zon support
- Babashka 1.4+ for Clojure scripting


## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 8. Degeneracy

**Concepts**: redundancy, fallback, multiple strategies, robustness

### GF(3) Balanced Triad

```
rama-gay-zig (−) + SDF.Ch8 (−) + [balancer] (−) = 0
```

**Skill Trit**: -1 (MINUS - verification)


### Connection Pattern

Degeneracy provides fallbacks. This skill offers redundant strategies.
