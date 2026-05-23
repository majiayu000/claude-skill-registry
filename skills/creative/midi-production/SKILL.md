---
name: midi-production
description: "Master MIDI production workflows including sequencing, automation, virtual instruments, and DAW techniques for professional music creation."
---

# MIDI Production

Professional MIDI sequencing and production techniques.

## Overview

MIDI (Musical Instrument Digital Interface) is a communication standard allowing digital music gear to communicate and enabling precise control over musical elements within a Digital Audio Workstation (DAW). MIDI production involves creating, editing, and manipulating musical data to control virtual instruments and hardware synthesizers, forming the foundation of modern music production.

This skill encompasses MIDI sequencing, automation, routing, virtual instrument programming, and workflow optimization techniques used by professional producers across genres from electronic music to orchestral composition.

## Core Concepts

### MIDI Data Types

**Note Messages** — Which notes are played, velocity (how hard), duration (note on/off)

**Continuous Controller (CC) Data** — Modulation wheel, pitch bend, expression, sustain pedal

**Program Change** — Switch between different sounds/patches on instruments

**System Exclusive (SysEx)** — Manufacturer-specific data for deep parameter control

### DAW MIDI Features

**Piano Roll** — Visual interface for viewing and editing MIDI notes

**MIDI Clips/Regions** — Containers for MIDI data on timeline

**Quantization** — Align notes to grid for rhythmic precision

**Velocity Editing** — Adjust note dynamics and expression

**MIDI Effects** — Arpeggiators, chord generators, randomizers, scale quantizers

## Professional Workflows

### Template-Based Production

Create project templates with pre-mapped MIDI inputs/outputs, virtual instruments loaded, and routing configured to save significant setup time for each new project.

### Reference Track Method

Import reference track of similar style, sync to project BPM, add markers for sections (intro, build, chorus) to structure composition and define energy levels for each section.

### Arrangement Techniques

**Muting for Experimentation** — Mute all tracks/clips and experiment bringing elements in and out to audition different configurations

**Starting from the Middle** — Begin arrangement from chorus (highest energy) then work backward to create intros and builds

**Four-Bar Sections** — Work in multiples of four bars, gradually introducing elements to build energy

### Automation Workflows

**Parameter Automation** — Automate volume, filter cutoff, effect sends for gradual sound evolution

**Drawing vs. Recording** — Draw automation curves or record in real-time using MIDI controllers

**Automation Lanes** — Organize multiple automation parameters per track

## Tools and Software

### Popular DAWs for MIDI

**Ableton Live** — Fast creative workflow, Session View, generative MIDI tools, excellent for electronic music

**FL Studio** — Intuitive step sequencer and piano roll, pattern-based workflow, strong for beat-making

**Logic Pro** — Comprehensive plugin suite, huge sound library, AI-powered MIDI tools, macOS only

**Cubase** — Strong MIDI composition features, advanced scoring, expression maps for orchestral

**Pro Tools** — Industry standard for audio, improved MIDI features in recent versions

**Reason** — Virtualized rack workflow, modular signal routing, extensive sound library

## Best Practices

### MIDI Programming

- Humanize MIDI by varying velocity and timing slightly
- Use velocity layers to access different samples in virtual instruments
- Quantize selectively; leave some human feel
- Layer multiple MIDI tracks for complex sounds
- Use MIDI sends for parallel processing

### Virtual Instrument Workflow

- Organize instruments by type (drums, bass, leads, pads)
- Use consistent naming conventions
- Freeze/bounce MIDI to audio to save CPU
- Create instrument racks/multi-instruments for layering
- Save custom presets for reuse

### Controller Integration

- Map MIDI controllers to frequently used parameters
- Use control surfaces for hands-on mixing
- Assign knobs/faders to virtual instrument controls
- Create controller templates for different workflows
- Use foot pedals for hands-free control

## Common Challenges

### MIDI Timing Issues

**Problem:** Notes sound late or early, timing feels off

**Solution:** Adjust MIDI track delay compensation, reduce buffer size for lower latency, use MIDI quantization, check for plugin latency

### CPU Overload from Virtual Instruments

**Problem:** System struggles with multiple instances

**Solution:** Freeze tracks to audio, increase buffer size, use lighter alternative plugins, bounce MIDI to audio stems, upgrade computer hardware

### Lifeless or Robotic Sound

**Problem:** MIDI performances sound mechanical

**Solution:** Vary note velocities, add subtle timing variations, use humanize functions, record MIDI in real-time, layer multiple takes

### Complex Routing Confusion

**Problem:** MIDI routing becomes difficult to manage

**Solution:** Use clear naming conventions, color-code tracks, document routing in session notes, use MIDI track folders, simplify when possible

## Using the Reference Files

**`/references/fundamentals.md`** — Core MIDI concepts, data types, DAW basics, and foundational sequencing techniques.

**`/references/advanced-techniques.md`** — Professional workflows for MIDI routing, generative techniques, hardware integration, and advanced automation.

**`/references/workflows-best-practices.md`** — Industry standards for MIDI programming, virtual instrument optimization, and genre-specific production techniques.

**`/references/troubleshooting.md`** — Common MIDI problems including latency, routing issues, and their solutions with practical examples.
