---
name: frequency-lookup
description: Look up frequency allocations, band plans, and known stations for radio services (marine, aviation, amateur, broadcast, NOAA weather). Use when finding frequencies to monitor, verifying band allocations, or discovering channels in a frequency range.
---

# Frequency Lookup for WaveCap-SDR

This skill helps find frequencies and band plans for various radio services.

## When to Use This Skill

Use this skill when:
- Finding frequencies for marine/aviation/amateur bands
- Looking up broadcast stations by location
- Verifying frequency allocations
- Discovering what's on a frequency
- Planning SDR monitoring scenarios
- Creating new recipes for specific bands

## Common Frequency Bands

### VHF Marine (156-162 MHz)

**Channel 16 (156.800 MHz)** - International Distress/Safety/Calling
**Channel 9 (156.450 MHz)** - Recreational calling (US)
**Channel 6 (156.300 MHz)** - Intership safety

Full band plan: https://www.navcen.uscg.gov/marine-communications-channel-table

### Aviation (118-137 MHz)

**121.500 MHz** - Emergency frequency
**Typical ranges:**
- Tower: 118.0-121.4 MHz
- Ground: 121.6-121.9 MHz
- ATIS: Varies by airport

Find local frequencies: https://www.airnav.com

### NOAA Weather Radio (162-163 MHz)

**WX1: 162.550 MHz**
**WX2: 162.400 MHz**
**WX3: 162.475 MHz**
**WX4: 162.425 MHz**
**WX5: 162.450 MHz**
**WX6: 162.500 MHz**
**WX7: 162.525 MHz**

Coverage map: https://www.weather.gov/nwr/

### FM Broadcast (88-108 MHz)

**US band:** 88.1-107.9 MHz (odd tenths only)
**Europe/Asia:** 87.5-108.0 MHz

Find local stations:
- https://radio-locator.com
- https://fmscan.org

### Amateur Radio (Ham)

**2 meters:** 144-148 MHz (FM repeaters typically 145-147 MHz)
**70 cm:** 420-450 MHz
**HF bands:** 3.5, 7, 14, 21, 28 MHz

Repeater directory: https://www.repeaterbook.com

### Public Safety / Trunking

**VHF:** 150-174 MHz
**UHF:** 450-470 MHz, 806-824 MHz

Database: https://www.radioreference.com

## Online Resources

**RadioReference.com** - Comprehensive frequency database
- Trunked systems
- Talkgroup IDs
- Local agencies

**SignalWiki** - Signal identification
- Decode unknown signals
- Modulation types

**WebSDR** - Remote SDR receivers
- Listen without hardware
- Check propagation

**FlightAware/FlightRadar24** - Aviation tracking
- Find airport frequencies
- Track aircraft

## Usage Examples

### Find Marine Channels
```
VHF Marine channels are spaced 25 kHz apart
Channel number = (Frequency - 156.000) / 0.025
Channel 16 = 156.800 MHz
Channel 9 = 156.450 MHz
```

### Find Local FM Stations
Visit https://radio-locator.com and enter your ZIP code

### Find NOAA Weather
Find nearest transmitter at https://www.weather.gov/nwr/

### Find Aviation Frequencies
Visit https://www.airnav.com and search for airport code (e.g., KSEA)

## Integration with WaveCap-SDR

After finding frequencies, create a recipe:

```yaml
recipes:
  my_frequencies:
    name: "My Frequencies"
    capture:
      center_hz: 156800000  # Center on Ch 16
      sample_rate: 250000
      gain_db: 35
    channels:
      - {name: "Ch 16", offset_hz: 0, mode: "fm"}
      - {name: "Ch 9", offset_hz: -350000, mode: "fm"}
```

Or use presets for quick tuning.

## Band Plan Quick Reference

| Service | Frequency Range | Typical Use |
|---------|----------------|-------------|
| AM Broadcast | 530-1700 kHz | Radio stations |
| Ham 160m | 1.8-2.0 MHz | Amateur HF |
| Marine SSB | 2-4 MHz | Long-range marine |
| Ham 80m | 3.5-4.0 MHz | Amateur HF |
| Ham 40m | 7.0-7.3 MHz | Amateur HF |
| Ham 20m | 14.0-14.35 MHz | Amateur HF |
| Ham 10m | 28-29.7 MHz | Amateur HF |
| CB | 26.965-27.405 MHz | Citizens Band |
| Ham 6m | 50-54 MHz | Amateur VHF |
| FM Broadcast | 88-108 MHz | Radio stations |
| Aviation | 118-137 MHz | Air traffic control |
| Ham 2m | 144-148 MHz | Amateur VHF |
| Marine VHF | 156-162 MHz | Maritime |
| NOAA WX | 162.400-162.550 MHz | Weather |
| Ham 70cm | 420-450 MHz | Amateur UHF |
| GMRS/FRS | 462-467 MHz | Personal radio |

## Files in This Skill

- `SKILL.md`: This file - frequency reference and lookup guide

## Notes

- Frequencies vary by country (this guide is US-centric)
- Always check local regulations before transmitting
- Some frequencies require licenses (ham, marine, aviation)
- SDR receiving is legal, transmitting requires proper licensing
- Band plans change - verify with official sources
- Use RadioReference.com for most comprehensive database
