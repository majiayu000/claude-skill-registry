---
name: ai-voice-bots
description: "Builds production voice bots and IVR with Python STT/TTS pipelines. Use when designing telephony, streaming audio, latency budgets, or voice quality monitoring."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# AI Voice Bots

Use this skill to build, ship, and tune voice bots — phone IVR, real-time speech agents, and voice-first customer interactions — using pure Python frameworks.

This skill owns the voice-specific pipeline: STT, TTS, telephony platforms, latency engineering, and voice quality. For conversation design, persona, and escalation patterns, use `ai-bot-builder`.

Default posture for Jul 2026: Pipecat as default framework, sub-700ms total turn latency, streaming STT→LLM→TTS pipeline, deterministic VAD, and voice quality metrics from day one. S2S (speech-to-speech) via OpenAI Realtime API or Gemini Live is available as a latency-first alternative — see Framework Selection and `references/s2s-and-native-voice-apis.md`.

## When to Use This Skill

- Building a voice bot for phone, IVR, or real-time speech
- Choosing a telephony platform (Twilio, Vapi, Bland.ai, Retell, Telnyx, Vonage)
- Choosing a voice pipeline framework (Pipecat, LiveKit Agents, Vocode)
- Engineering latency budgets for voice (TTFB, total turn latency)
- Selecting and configuring STT/TTS providers (Deepgram, ElevenLabs, Cartesia, Azure)
- Monitoring voice quality (MOS, WER, call completion rate)
- Designing IVR flows with DTMF and voice hybrid
- Building outbound dialing campaigns

## When NOT to Use This Skill

| Need | Route to |
|------|----------|
| Bot conversation design, persona, escalation | `ai-bot-builder` |
| Text-only bot architecture | `ai-bot-builder` |
| General agent architecture | [`../ai-agents/SKILL.md`](../ai-agents/SKILL.md) |
| WebSocket/SSE infrastructure (non-voice) | [`../software-realtime/SKILL.md`](../software-realtime/SKILL.md) |
| Voice/multimodal reference material | [`../ai-agents/references/voice-multimodal-agents.md`](../ai-agents/references/voice-multimodal-agents.md) |

## Quick Reference

| Need | Default | Notes |
|------|---------|-------|
| Choose telephony platform | `references/telephony-platform-selection.md` | Twilio, Vapi, Bland.ai, Retell, Telnyx, Vonage |
| Design voice pipeline | `references/voice-pipeline-architecture.md` | STT→LLM→TTS streaming, codec selection |
| Build with Pipecat | `references/pipecat-patterns.md` | Processors, transports, production deployment |
| Build with LiveKit Agents | `references/livekit-agents-patterns.md` | VoicePipelineAgent, rooms, plugins |
| Optimize latency | `references/latency-engineering.md` | Component budgets, edge deployment, caching |
| Monitor voice quality | `references/voice-quality-metrics.md` | MOS, WER, dashboards, alerting |
| Design IVR flows | `references/ivr-design.md` | DTMF, menu trees, hybrid voice+keypad |
| Voice compliance | `references/voice-safety-compliance.md` | Recording consent, PCI, TCPA, GDPR |
| Deploy voice bot to 24/7 production | `references/production-deployment.md` | Concurrent-call capacity, SIP/PSTN HA, autoscaling, drain, recording compliance, cost model |
| Pick a hosting platform (LiveKit Cloud + Fly.io, Pipecat Cloud, etc.) | [`../software-paas-hosting/references/agent-hosting-matrix.md`](../software-paas-hosting/references/agent-hosting-matrix.md) | Voice stacks BV1–BV3 + what does NOT host voice |

## Default Workflow

1. **Define call flow** — inbound vs outbound, IVR menu tree, conversation states.
2. **Choose telephony platform** — by volume, region, compliance, and API quality.
3. **Choose voice pipeline framework** — Pipecat (default) or LiveKit Agents.
4. **Set latency budgets** — per pipeline stage, total turn latency < 700ms target.
5. **Select STT/TTS providers** — by language support, latency, quality, and cost.
6. **Integrate conversation logic** — use `ai-bot-builder` patterns for the LLM "brain."
7. **Add voice-specific guardrails** — recording consent, PII in speech, barge-in safety.
8. **Instrument voice quality metrics** — MOS, WER, call completion, latency percentiles.
9. **Load test and tune** — verify latency under concurrent call load.

## ASCII Flow

```text
voice bot request
  -> call flow: inbound, outbound, IVR, or real-time agent
  -> platform choice: telephony, WebRTC, or managed voice API
  -> pipeline choice
     +-- cascading -> STT -> LLM -> TTS
     +-- speech-to-speech -> native real-time voice API
  -> latency budget and provider selection
  -> conversation brain via ai-bot-builder
  -> consent, PII, barge-in, and transfer guardrails
  -> MOS, WER, completion rate, and p95/p99 latency monitoring
  -> load test, fallback path, and launch decision
```

## Voice Pipeline Architecture

```
Phone/WebRTC → Transport → STT → LLM → TTS → Transport → Phone/WebRTC
                  │          │      │      │         │
                  │          │      │      │         └── Audio codec encoding
                  │          │      │      └── Text-to-speech streaming
                  │          │      └── Conversation logic (ai-bot-builder)
                  │          └── Speech-to-text streaming
                  └── WebSocket / WebRTC / SIP
```

**Pipeline latency budget (target: < 700ms total):**

| Component | Budget | Notes |
|-----------|--------|-------|
| VAD (voice activity detection) | 200-300ms | End-of-speech detection delay |
| STT (speech-to-text) | 100-200ms | Streaming reduces this vs batch |
| LLM (first token) | 100-300ms | TTFB; use streaming + fast models |
| TTS (first audio chunk) | 50-150ms | Streaming synthesis |
| Network round-trip | 20-50ms | Edge deployment reduces this |

Full depth → [`references/voice-pipeline-architecture.md`](references/voice-pipeline-architecture.md)

## Telephony Platform Selection

| Platform | Best for | Pricing model | Global coverage | S2S support |
|----------|----------|---------------|-----------------|-------------|
| **Twilio** | Full control, custom pipeline | Per-minute + per-number | 100+ countries | Via Pipecat/LiveKit integration |
| **Vapi** | Rapid prototyping, managed pipeline | $0.05/min + provider costs | US/EU primary | Native (OpenAI Realtime) |
| **Bland.ai** | Outbound campaigns, simple IVR | Per-minute | US primary | No |
| **Retell** | Enterprise voice agents | Per-minute + platform fee | US/EU/APAC | Native (OpenAI Realtime) |
| **Telnyx** | Cost-efficient, global SIP | Per-minute (lower rates) | 80+ countries | Via Pipecat integration |
| **Vonage** | Enterprise, omnichannel | Per-minute + platform | Global | No |

Default: **Twilio** for maximum control and global reach. **Vapi** for fastest time-to-market. **Retell** for managed S2S without infrastructure work.

Full comparison → [`references/telephony-platform-selection.md`](references/telephony-platform-selection.md)

## Framework Selection

| Framework | Best for | Transport | S2S support | Ecosystem |
|-----------|----------|-----------|-------------|-----------|
| **Pipecat** (default) | Custom voice pipelines, multi-transport | WebSocket, Twilio, Daily, WebRTC | Yes (OpenAI Realtime, Gemini Live) | Deepgram, ElevenLabs, Cartesia, Anthropic, OpenAI |
| **LiveKit Agents** | Room-based voice, recording, multi-party | LiveKit (WebRTC) | Yes (OpenAI Realtime) | LiveKit Cloud, STT/TTS plugins |
| **Vocode** | Simple voice bots, telephony focus | Twilio, Vonage, WebSocket | No | Deepgram, Azure, ElevenLabs |

Default: **Pipecat** — strongest Python ecosystem, composable pipeline processors, multi-transport support, and broadest S2S provider coverage.

Use **LiveKit Agents** when: multi-participant calls, built-in recording, or already using LiveKit infrastructure.

### S2S vs Cascading Decision Tree

```
Is latency < 500ms (p50) a hard requirement?
├── No → Cascading (STT→LLM→TTS)
│         Reasons: text-layer compliance, guardrails, PII redaction, logging, debugging
└── Yes → Do you need text-layer inspection?
          ├── Yes (compliance, PII, guardrails) → Cascading — latency goal may need re-negotiation
          └── No → Speech-to-speech (S2S)
                   ├── OpenAI Realtime API (GA, out of beta; `gpt-4o-realtime-preview` retired) —
                   │     `gpt-realtime-2.1` / `gpt-realtime-2.1-mini` (reasoning + tool use in both tiers,
                   │     ~25% lower p95 latency than the prior `gpt-realtime-2` generation), plus
                   │     `gpt-realtime-translate` (70+ input / 13 output languages, live speech translation) and
                   │     `gpt-realtime-whisper` (streaming STT, controllable latency/quality tradeoff).
                   │     Verify current model names before use — this line moves every few months.
                   └── Gemini Live — Google ecosystem, good for long sessions
```

**S2S trade-offs**: audio-in → audio-out bypasses the text layer entirely (~500ms vs ~700ms cascading). You lose: text-layer compliance filtering, PII detection/redaction, guardrail injection, intermediate transcript logging, and the ability to inspect model reasoning. Some teams ship S2S for the product experience and add a parallel transcript path (Deepgram streaming alongside) to recover the audit trail — but this adds cost and complexity.

Full S2S reference → [`references/s2s-and-native-voice-apis.md`](references/s2s-and-native-voice-apis.md)

## Production Defaults

- **Framework:** Pipecat with streaming pipeline
- **STT:** Deepgram Nova-3 for transcription-only pipelines (54% WER reduction over Nova-2). For conversational pipelines, prefer Deepgram Flux (`flux-general-en` / `flux-general-multi`, multilingual GA Apr 2026) — fuses STT + turn detection in one `/v2/listen` call (~260ms median EoT), removing the stacked STT→VAD→endpointing layers. See `references/voice-pipeline-architecture.md`.
- **TTS:** ElevenLabs Flash v2.5 (`eleven_flash_v2_5`, ~75ms model inference, 32 languages) for real-time conversations, or Cartesia for ultra-low latency — Sonic-3 (~40ms TTFA on Turbo, independent benchmarks show higher variance) or the newer Sonic-3.5 + Ink-2 streaming STT/TTS stack (shipped Jun 2026; verify current benchmark numbers before committing). Note: `eleven_turbo_v2_5` is functionally equivalent (Flash has lower average latency); Eleven v3 (GA Mar 2026) adds expressive control but is **not** suitable for real-time/conversational use.
- **LLM:** Claude Sonnet for complex conversations, Haiku for simple routing
- **Transport:** Twilio for phone, Daily/WebRTC for web
- **Latency target:** < 700ms total turn latency (p90). Top-tier: < 500ms (p50)
- **Quality monitoring:** MOS tracking, WER sampling, call completion rate
- **Compliance:** Recording consent per jurisdiction, PII redaction from transcripts

## Expert Judgment: Latency Budget and Barge-In

**Decompose the budget before you optimize.** "700ms feels slow" is not actionable; "TTS first-chunk is 320ms of our 700ms" is. Attribute every millisecond to VAD, STT, LLM TTFB, TTS first-chunk, or network before touching code — teams that skip this step optimize the component that's easiest to change (usually the LLM prompt) instead of the one that's actually the bottleneck (usually VAD end-of-speech wait or a cold TTS connection). Full worked budget and instrumentation → `references/latency-engineering.md`; queueing-theory-grounded budget partitioning → `references/queueing-theory-applied.md`.

**Barge-in is a pre-emption problem, not a VAD-tuning problem.** A user talking over the bot must cancel in-flight TTS and the pending LLM stream within one residual service period (~150-300ms for a typical TTS chunk) or the interruption reads as broken, even if VAD detected it instantly. Don't use a fixed silence timeout for barge-in — set it from observed per-stage latency percentiles, and monitor barge-in success rate (bot audio actually stops within ~350ms) as its own SLO, separately from turn latency. See `references/queueing-theory-applied.md` (P3, A3) for the pre-emption pattern and its failure mode.

**S2S vs cascading is a latency-vs-control trade, re-evaluated per release, not a one-time architecture choice.** Cascading gives you the text layer (compliance, PII redaction, guardrails, debuggability) at the cost of ~150-300ms extra hops. S2S buys latency but forces either giving up the text layer or paying for it back with a parallel transcript track — which can erase the simplicity gain that made S2S attractive. Because S2S providers now ship a new generation roughly every 8-10 weeks (see `references/s2s-and-native-voice-apis.md`), a "cascading was necessary for latency" decision from two quarters ago may no longer hold — re-check the current-generation p50/p95 numbers before defending a standing architecture choice on stale benchmarks.

## Known Traps

- proving latency with synthetic lab prompts instead of real barge-in, interruption, packet-loss, and handset-network conditions
- treating telephony acceptance as conversation success when the real failure is post-answer latency, bad turn segmentation, or TTS overlap
- mixing recording, transcript retention, PCI redaction, and consent rules across regions without one explicit policy owner
- optimizing only average latency while ignoring p95 or p99 tails that make production calls feel broken
- shipping one STT or TTS provider path with no fallback, rollback, or degraded-mode behavior for provider incidents
- **S2S session-state loss on model switch**: switching between S2S model versions mid-session (any provider — OpenAI Realtime, Gemini Live) drops all ephemeral session state — voice, tone configuration, conversation history, and tool state are not carried over. Resolution: persist conversation state to an external store (Redis or Postgres) after every turn; reload from the store when resuming or switching models. Do not rely on the S2S session as a state store for anything you cannot afford to lose. See `references/s2s-and-native-voice-apis.md` for the full session management pattern.

## Common Anti-Patterns

- **Batch-style voice pipelines** — waiting for full utterances or full synthesis destroys turn-taking and makes the bot feel laggy
- **LLM-first architecture with no deterministic call state** — IVR routing, transfers, and compliance prompts need explicit state machines, not only prompt logic
- **One-metric quality reporting** — MOS alone or WER alone hides interruption quality, completion failures, and escalation pain
- **Treating outbound voice like chat automation** — dialing, consent, voicemail handling, and retry policy need channel-specific controls
- **Using text-bot guardrails unchanged for speech** — voice bots need barge-in, silence, DTMF, and speaking-over-user protections

## Navigation

**References**
- [references/index.md](references/index.md) — Reference navigation map
- [references/s2s-and-native-voice-apis.md](references/s2s-and-native-voice-apis.md) — S2S vs cascading, OpenAI Realtime API, Gemini Live, session management (Jul 2026)
- [references/telephony-platform-selection.md](references/telephony-platform-selection.md) — Platform comparison
- [references/voice-pipeline-architecture.md](references/voice-pipeline-architecture.md) — Pipeline design
- [references/pipecat-patterns.md](references/pipecat-patterns.md) — Pipecat deep dive
- [references/livekit-agents-patterns.md](references/livekit-agents-patterns.md) — LiveKit Agents deep dive
- [references/latency-engineering.md](references/latency-engineering.md) — Latency optimization
- [references/voice-quality-metrics.md](references/voice-quality-metrics.md) — Quality monitoring
- [references/ivr-design.md](references/ivr-design.md) — IVR flow design
- [references/voice-safety-compliance.md](references/voice-safety-compliance.md) — Voice compliance
- [references/queueing-theory-applied.md](references/queueing-theory-applied.md) — Queueing theory applied to voice: latency budget partitioning, jitter buffer sizing, Erlang-C IVR capacity, barge-in priority, TTS streaming targets

**Assets**
- [assets/voice-bot-spec.md](assets/voice-bot-spec.md) — Voice bot specification template
- [assets/voice-latency-budget.md](assets/voice-latency-budget.md) — Latency budget worksheet
- [assets/voice-quality-checklist.md](assets/voice-quality-checklist.md) — Pre-launch quality gate
- [assets/voice-eval-scenarios.md](assets/voice-eval-scenarios.md) — End-to-end voice-agent eval scenario template

**Scripts**
- `python3 scripts/voice_latency_audit.py --input pipeline_logs.jsonl` — Pipeline latency breakdown
- `python3 scripts/call_quality_scorer.py --input calls.jsonl` — Call quality scoring

**Data**
- [data/sources.json](data/sources.json) — Curated voice-specific sources

## Related Skills

- `ai-bot-builder` — Conversation design, persona, escalation, LangGraph
- [../ai-context-layer/references/conversational-surfaces-cross-platform.md](../ai-context-layer/references/conversational-surfaces-cross-platform.md) — Cross-platform composition recipe; voice section specifies the RA13 hot/cold memory tier split required for sub-300 ms turn latency
- [../ai-agents/SKILL.md](../ai-agents/SKILL.md) — Agent architecture decisions
- [../ai-agents/references/voice-multimodal-agents.md](../ai-agents/references/voice-multimodal-agents.md) — Voice/multimodal agent reference
- [../software-realtime/SKILL.md](../software-realtime/SKILL.md) — WebSocket/SSE infrastructure
- [../qa-agent-testing/SKILL.md](../qa-agent-testing/SKILL.md) — Agent eval harnesses
- [../qa-observability/SKILL.md](../qa-observability/SKILL.md) — Pipeline telemetry

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Start from `data/sources.json` for voice framework docs and provider references.
- Verify current STT/TTS provider APIs, latency benchmarks, and pricing before citing specifics.
- Telephony platform features and pricing change frequently — verify before recommending.
- If live verification is unavailable, mark provider-specific guidance as unverified.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
