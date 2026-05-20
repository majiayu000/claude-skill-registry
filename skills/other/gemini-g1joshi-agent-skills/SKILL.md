---
name: gemini
description: Google Gemini AI models for multimodal tasks. Use for multimodal AI.
---

# Gemini

Gemini is Google's native multimodal model. Uniquely, it accepts **video** and huge context (2M+ tokens) natively. 2025 sees Gemini 2.0/3.0.

## When to Use

- **Massive Context**: "Here is a 1-hour video. Find the timestamp where..."
- **Multimodal Live**: Real-time voice/video interaction.
- **Google Ecosystem**: Integrated with Vertex AI, Search (Grounding), and Workspace.

## Core Concepts

### Models

- **Pro**: The best all-rounder.
- **Flash**: Extremely fast and cheap. High throughput.
- **Ultra**: The largest reasoning model.

### Grounding

Connects the model to Google Search to provide citations and up-to-date info.

### Context Initial Caching

Cache the context (e.g., a massive manual) to reduce cost/latency on subsequent queries.

## Best Practices (2025)

**Do**:

- **Use Flash for RAG**: 2.0 Flash is smart enough for most RAG & cheaper/faster.
- **Use Grounding**: Eliminate hallucinations by enforcing "Google Search" grounding.
- **Upload Video**: Don't transcribe video manually; Gemini watches it.

**Don't**:

- **Don't confuse with PaLM**: Gemini replaced PaLM 2 completely.

## References

- [Gemini API Documentation](https://ai.google.dev/)
