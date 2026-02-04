---
name: godot-setup-audio-buses
version: 1.0.0
displayName: Setup Audio Bus Architecture
description: >
  Use when configuring audio bus hierarchies in Godot, setting up AudioStreamPlayer
  pooling for performance, implementing 3D spatial audio, adding audio effect chains
  like reverb and EQ, or creating music crossfade systems. Provides complete audio
  architecture patterns for games with multiple audio categories and dynamic mixing.
author: Asreonn
license: MIT
category: game-development
type: tool
difficulty: intermediate
audience: [developers, audio-designers]
keywords:
  - godot
  - audio
  - sound
  - buses
  - mixing
  - reverb
  - eq
  - spatial-audio
  - 3d-audio
  - pooling
  - crossfade
  - music
  - sfx
platforms: [macos, linux, windows]
repository: https://github.com/asreonn/godot-superpowers
homepage: https://github.com/asreonn/godot-superpowers#readme

permissions:
  filesystem:
    read: [".gd", ".tscn", ".tres", "project.godot"]
    write: [".tscn", ".tres", ".gd", "project.godot"]
  git: true

behavior:
  auto_rollback: true
  validation: true
  git_commits: true

outputs: "Audio bus configuration in project.godot, AudioStreamPlayer pool scripts, 3D audio setup scenes, effect chain presets, crossfade controller scripts"
requirements: "Git repository, Godot 4.x"
execution: "Automatic bus setup, scene generation, and script creation with git commits"
integration: "Works with godot-extract-to-scenes for audio component library, godot-add-signals for audio events"
---

# Setup Audio Bus Architecture

## Core Principle

**Audio is a system, not an afterthought.** Use bus hierarchies for mixing control, pooling for performance, and effect chains for environmental audio. Never attach AudioStreamPlayers directly to transient nodes.

## What This Skill Does

Sets up complete audio systems:

1. **Bus Architecture** - Master/Music/SFX/Voice hierarchy with proper routing
2. **Audio Pooling** - Reusable AudioStreamPlayer pool for frequent sounds
3. **3D Spatial Audio** - Listener positioning and attenuation for immersive audio
4. **Effect Chains** - Reverb, EQ, and dynamic effects for environmental audio
5. **Music Crossfade** - Seamless track transitions with volume interpolation

## Bus Configuration

### Master/Music/SFX Bus Structure

**Before (Default Setup):**
```ini
# project.godot - Default single bus
[audio]
buses/0/name = "Master"
buses/0/solo = false
buses/0/mute = false
buses/0/bypass_fx = false
buses/0/volume_db = 0.0
```

**After (Hierarchical Bus Setup):**
```ini
# project.godot - Complete audio architecture
[audio]

; Master bus - all audio routes through here
buses/0/name = "Master"
buses/0/solo = false
buses/0/mute = false
buses/0/bypass_fx = false
buses/0/volume_db = 0.0
buses/0/send = ""

; Music bus - routes to Master
buses/1/name = "Music"
buses/1/solo = false
buses/1/mute = false
buses/1/bypass_fx = false
buses/1/volume_db = 0.0
buses/1/send = "Master"

; SFX bus - routes to Master
buses/2/name = "SFX"
buses/2/solo = false
buses/2/mute = false
buses/2/bypass_fx = false
buses/2/volume_db = 0.0
buses/2/send = "Master"

; Voice/UI bus - routes to Master
buses/3/name = "Voice"
buses/3/solo = false
buses/3/mute = false
buses/3/bypass_fx = false
buses/3/volume_db = 0.0
buses/3/send = "Master"

; Ambient bus - routes to Master with reverb
buses/4/name = "Ambient"
buses/4/solo = false
buses/4/mute = false
buses/4/bypass_fx = false
buses/4/volume_db = -6.0
buses/4/send = "Master"
```

**Runtime Bus Control:**
```gdscript
# audio_manager.gd
extends Node

const MASTER_BUS = "Master"
const MUSIC_BUS = "Music"
const SFX_BUS = "SFX"
const VOICE_BUS = "Voice"
const AMBIENT_BUS = "Ambient"

func _ready():
    # Ensure buses exist
    _setup_bus_indices()

func _setup_bus_indices():
    # Cache bus indices for performance
    master_bus_idx = AudioServer.get_bus_index(MASTER_BUS)
    music_bus_idx = AudioServer.get_bus_index(MUSIC_BUS)
    sfx_bus_idx = AudioServer.get_bus_index(SFX_BUS)
    voice_bus_idx = AudioServer.get_bus_index(VOICE_BUS)
    ambient_bus_idx = AudioServer.get_bus_index(AMBIENT_BUS)

func set_bus_volume(bus_name: String, volume_db: float):
    var bus_idx = AudioServer.get_bus_index(bus_name)
    if bus_idx >= 0:
        AudioServer.set_bus_volume_db(bus_idx, volume_db)

func mute_bus(bus_name: String, muted: bool):
    var bus_idx = AudioServer.get_bus_index(bus_name)
    if bus_idx >= 0:
        AudioServer.set_bus_mute(bus_idx, muted)

func get_bus_volume_linear(bus_name: String) -> float:
    var bus_idx = AudioServer.get_bus_index(bus_name)
    if bus_idx >= 0:
        return db_to_linear(AudioServer.get_bus_volume_db(bus_idx))
    return 1.0
```

### Volume Control System

**Linear Volume Slider (UI-friendly):**
```gdscript
# Convert slider 0.0-1.0 to decibels
func set_bus_volume_linear(bus_name: String, linear: float):
    var db = linear_to_db(clamp(linear, 0.0001, 1.0))
    set_bus_volume(bus_name, db)

# Smooth volume transition
func fade_bus_volume(bus_name: String, target_linear: float, duration: float):
    var bus_idx = AudioServer.get_bus_index(bus_name)
    if bus_idx < 0:
        return
    
    var start_db = AudioServer.get_bus_volume_db(bus_idx)
    var target_db = linear_to_db(clamp(target_linear, 0.0001, 1.0))
    
    var tween = create_tween()
    tween.tween_method(
        func(vol): AudioServer.set_bus_volume_db(bus_idx, vol),
        start_db,
        target_db,
        duration
    )
```

## AudioStreamPlayer Pooling

### Pool System Architecture

**Why Pooling Matters:**
- Creating/destroying AudioStreamPlayers causes stutter
- Frequent sounds (gunshots, footsteps) need instant playback
- Pool eliminates allocation overhead during gameplay

**Pool Implementation:**
```gdscript
# audio_pool.gd
extends Node

class_name AudioPool

@export var pool_size: int = 16
@export var bus: String = "SFX"

var _available: Array[AudioStreamPlayer] = []
var _in_use: Array[AudioStreamPlayer] = []

func _ready():
    _initialize_pool()

func _initialize_pool():
    for i in range(pool_size):
        var player = AudioStreamPlayer.new()
        player.name = "PooledAudio_%d" % i
        player.bus = bus
        player.finished.connect(_on_player_finished.bind(player))
        add_child(player)
        _available.append(player)

func play_sound(stream: AudioStream, volume_db: float = 0.0, pitch_scale: float = 1.0) -> AudioStreamPlayer:
    if _available.is_empty():
        # All players busy - steal oldest or skip
        if _in_use.is_empty():
            return null
        # Reuse the oldest playing sound
        var oldest = _in_use.pop_front()
        oldest.stop()
        _available.append(oldest)
    
    var player = _available.pop_back()
    _in_use.append(player)
    
    player.stream = stream
    player.volume_db = volume_db
    player.pitch_scale = pitch_scale
    player.play()
    
    return player

func play_sound_2d(stream: AudioStream, position: Vector2, volume_db: float = 0.0, pitch_scale: float = 1.0) -> AudioStreamPlayer2D:
    # Similar implementation for 2D spatial audio
    pass

func _on_player_finished(player: AudioStreamPlayer):
    _in_use.erase(player)
    _available.append(player)
    player.stream = null

func stop_all():
    for player in _in_use:
        player.stop()
    _available.append_array(_in_use)
    _in_use.clear()
```

**2D Audio Pool:**
```gdscript
# audio_pool_2d.gd
extends Node2D

class_name AudioPool2D

@export var pool_size: int = 16
@export var bus: String = "SFX"
@export var max_distance: float = 2000.0

var _available: Array[AudioStreamPlayer2D] = []
var _in_use: Array[AudioStreamPlayer2D] = []

func _ready():
    _initialize_pool()

func _initialize_pool():
    for i in range(pool_size):
        var player = AudioStreamPlayer2D.new()
        player.name = "PooledAudio2D_%d" % i
        player.bus = bus
        player.max_distance = max_distance
        player.attenuation = 1.0  # Linear attenuation
        player.finished.connect(_on_player_finished.bind(player))
        add_child(player)
        _available.append(player)

func play_sound_at(stream: AudioStream, global_pos: Vector2, volume_db: float = 0.0, pitch_scale: float = 1.0) -> AudioStreamPlayer2D:
    if _available.is_empty():
        return null
    
    var player = _available.pop_back()
    _in_use.append(player)
    
    player.global_position = global_pos
    player.stream = stream
    player.volume_db = volume_db
    player.pitch_scale = pitch_scale
    player.play()
    
    return player

func _on_player_finished(player: AudioStreamPlayer2D):
    _in_use.erase(player)
    _available.append(player)
    player.stream = null
```

### 3D Audio Spatial Setup

**AudioListener Configuration:**
```gdscript
# player_audio_listener.gd
extends AudioListener3D

# Attach to player camera or character controller
func _ready():
    # Make this the active listener
    make_current()

func _physics_process(delta):
    # Listener follows player position/rotation
    # Update rotation for HRTF spatial audio
    global_transform = get_parent().global_transform
```

**3D Spatial Audio Source:**
```gdscript
# spatial_audio_source.gd
extends AudioStreamPlayer3D

@export var play_on_ready: bool = false
@export var loop: bool = false
@export var stream_randomization: Array[AudioStream] = []

func _ready():
    # 3D audio configuration
    unit_size = 10.0  # Size of game world units per meter
    max_db = 0.0
    max_distance = 100.0
    attenuation_filter_db = -24.0
    attenuation_filter_cutoff_hz = 2050
    
    # Panning
    panning_strength = 1.0  # 0.0 = no pan, 1.0 = full HRTF
    
    if play_on_ready:
        play()

func play_random():
    if stream_randomization.is_empty():
        play()
    else:
        stream = stream_randomization.pick_random()
        play()

func play_with_pitch_variation(pitch_range: float = 0.1):
    pitch_scale = 1.0 + randf_range(-pitch_range, pitch_range)
    play()
```

**Generated Scene (3D Audio Source):**
```ini
# spatial_audio_source.tscn
[gd_scene load_steps=2 format=3]

[ext_resource type="Script" path="res://audio/spatial_audio_source.gd" id="1_abc123"]

[node name="SpatialAudioSource" type="AudioStreamPlayer3D"]
script = ExtResource("1_abc123")
bus = "SFX"
unit_size = 10.0
max_distance = 100.0
attenuation = 1.0
panning_strength = 1.0
emission_angle_enabled = true
emission_angle_degrees = 45.0
emission_angle_filter_attenuation_db = -12.0
attenuation_filter_cutoff_hz = 2050
attenuation_filter_db = -24.0
doppler_tracking = 2  # Fixed frame
```

## Audio Effect Chains

### Reverb Setup

**Adding Reverb to Ambient Bus:**
```gdscript
# audio_effects.gd
extends Node

func add_reverb_to_bus(bus_name: String, room_size: float = 0.8, damping: float = 0.5, wetness: float = 0.3):
    var bus_idx = AudioServer.get_bus_index(bus_name)
    if bus_idx < 0:
        push_error("Bus not found: %s" % bus_name)
        return
    
    var reverb = AudioEffectReverb.new()
    reverb.room_size = room_size      # 0.0 - 1.0
    reverb.damping = damping          # 0.0 - 1.0
    reverb.wet = wetness              # 0.0 - 1.0 (effect level)
    reverb.dry = 1.0 - wetness        # Original signal level
    reverb.hipass = 0.0               # 0.0 - 1.0 (filter low frequencies)
    reverb.predelay_msec = 20.0       # Pre-delay in milliseconds
    reverb.predelay_feedback = 0.4    # Pre-delay feedback
    
    AudioServer.add_bus_effect(bus_idx, reverb)
    return reverb

func remove_all_effects_from_bus(bus_name: String):
    var bus_idx = AudioServer.get_bus_index(bus_name)
    if bus_idx < 0:
        return
    
    var effect_count = AudioServer.get_bus_effect_count(bus_idx)
    for i in range(effect_count - 1, -1, -1):
        AudioServer.remove_bus_effect(bus_idx, i)
```

**Environment-Based Reverb Presets:**
```gdscript
# reverb_presets.gd
class_name ReverbPresets

static func apply_small_room(bus_idx: int):
    var reverb = AudioEffectReverb.new()
    reverb.room_size = 0.2
    reverb.damping = 0.8
    reverb.wet = 0.15
    reverb.dry = 0.85
    reverb.predelay_msec = 5.0
    AudioServer.add_bus_effect(bus_idx, reverb)
    return reverb

static func apply_cave(bus_idx: int):
    var reverb = AudioEffectReverb.new()
    reverb.room_size = 1.0
    reverb.damping = 0.3
    reverb.wet = 0.5
    reverb.dry = 0.5
    reverb.predelay_msec = 60.0
    reverb.predelay_feedback = 0.6
    AudioServer.add_bus_effect(bus_idx, reverb)
    return reverb

static func apply_cathedral(bus_idx: int):
    var reverb = AudioEffectReverb.new()
    reverb.room_size = 0.9
    reverb.damping = 0.2
    reverb.wet = 0.6
    reverb.dry = 0.4
    reverb.predelay_msec = 80.0
    reverb.predelay_feedback = 0.5
    AudioServer.add_bus_effect(bus_idx, reverb)
    return reverb

static func apply_underwater(bus_idx: int):
    var reverb = AudioEffectReverb.new()
    reverb.room_size = 0.6
    reverb.damping = 1.0
    reverb.wet = 0.4
    reverb.dry = 0.6
    reverb.hipass = 0.8  # Cut low frequencies
    AudioServer.add_bus_effect(bus_idx, reverb)
    
    # Add low-pass filter
    var eq = AudioEffectEQ.new()
    eq.set_band_gain_db(0, -20.0)  # Cut lowest frequencies
    AudioServer.add_bus_effect(bus_idx, eq)
    
    return reverb
```

### EQ (Equalizer) Setup

**Multi-Band EQ Configuration:**
```gdscript
# audio_eq.gd
extends Node

func add_eq_to_bus(bus_name: String) -> AudioEffectEQ:
    var bus_idx = AudioServer.get_bus_index(bus_name)
    if bus_idx < 0:
        return null
    
    var eq = AudioEffectEQ.new()
    
    # Godot EQ has 6 bands by default:
    # 0: 31 Hz (Sub-bass)
    # 1: 100 Hz (Bass)
    # 2: 320 Hz (Low-mid)
    # 3: 1 kHz (Mid)
    # 4: 3.2 kHz (High-mid)
    # 5: 10 kHz (Treble)
    
    # Example: Boost bass for music
    eq.set_band_gain_db(0, 3.0)   # +3dB sub-bass
    eq.set_band_gain_db(1, 2.0)   # +2dB bass
    eq.set_band_gain_db(5, -1.0)  # -1dB treble (reduce harshness)
    
    AudioServer.add_bus_effect(bus_idx, eq)
    return eq

func create_telephone_effect(bus_name: String):
    var bus_idx = AudioServer.get_bus_index(bus_name)
    if bus_idx < 0:
        return
    
    # Band-pass effect: cut lows and highs
    var eq = AudioEffectEQ.new()
    eq.set_band_gain_db(0, -60.0)  # Cut sub-bass
    eq.set_band_gain_db(1, -30.0)  # Cut bass
    eq.set_band_gain_db(4, -10.0)  # Slight cut high-mid
    eq.set_band_gain_db(5, -60.0)  # Cut treble
    
    AudioServer.add_bus_effect(bus_idx, eq)
```

**EQ Presets:**
```gdscript
# eq_presets.gd
class_name EQPresets

static func apply_bass_boost(eq: AudioEffectEQ, amount_db: float = 6.0):
    eq.set_band_gain_db(0, amount_db)
    eq.set_band_gain_db(1, amount_db * 0.7)

static func apply_vocal_clarity(eq: AudioEffectEQ):
    eq.set_band_gain_db(2, 2.0)   # Boost low-mid for presence
    eq.set_band_gain_db(3, 3.0)   # Boost mid for clarity
    eq.set_band_gain_db(4, 1.0)   # Slight high-mid boost

static func apply_loudness(eq: AudioEffectEQ):
    # Fletcher-Munson curve approximation
    eq.set_band_gain_db(0, 4.0)   # Boost sub-bass
    eq.set_band_gain_db(1, 2.0)   # Boost bass
    eq.set_band_gain_db(2, 0.0)   # Flat
    eq.set_band_gain_db(3, 0.0)   # Flat
    eq.set_band_gain_db(4, 1.0)   # Slight high-mid boost
    eq.set_band_gain_db(5, 2.0)   # Boost treble
```

### Dynamic Effects

**Compressor for Voice Bus:**
```gdscript
func add_compressor_to_bus(bus_name: String) -> AudioEffectCompressor:
    var bus_idx = AudioServer.get_bus_index(bus_name)
    if bus_idx < 0:
        return null
    
    var compressor = AudioEffectCompressor.new()
    compressor.threshold = -18.0  # dB
    compressor.ratio = 4.0        # Compression ratio
    compressor.attack_us = 20     # Attack time in microseconds
    compressor.release_ms = 250   # Release time in milliseconds
    compressor.mix = 1.0          # 100% wet
    
    AudioServer.add_bus_effect(bus_idx, compressor)
    return compressor
```

**Limiter on Master Bus:**
```gdscript
func add_limiter_to_master() -> AudioEffectLimiter:
    var master_idx = AudioServer.get_bus_index("Master")
    if master_idx < 0:
        return null
    
    var limiter = AudioEffectLimiter.new()
    limiter.ceiling_db = -1.0     # Output ceiling (prevent clipping)
    limiter.threshold_db = -6.0   # When limiting starts
    limiter.soft_clip_db = 2.0    # Soft clip amount
    limiter.soft_clip_ratio = 10.0
    
    # Add as last effect
    AudioServer.add_bus_effect(master_idx, limiter)
    return limiter
```

## Music Crossfade Implementation

### Crossfade Controller

**Basic Crossfade:**
```gdscript
# music_crossfader.gd
extends Node

class_name MusicCrossfader

@export var fade_duration: float = 2.0
@export var bus: String = "Music"

var _current_player: AudioStreamPlayer
var _previous_player: AudioStreamPlayer
var _tween: Tween

func _ready():
    # Ensure we have a bus
    if AudioServer.get_bus_index(bus) < 0:
        push_error("Music bus not found: %s" % bus)

func crossfade_to(stream: AudioStream, start_position: float = 0.0):
    if not stream:
        return
    
    # Stop any existing tween
    if _tween and _tween.is_valid():
        _tween.kill()
    
    # Create new player for incoming track
    var new_player = AudioStreamPlayer.new()
    new_player.bus = bus
    new_player.stream = stream
    new_player.volume_db = -80.0  # Start silent
    add_child(new_player)
    
    # Setup crossfade
    _tween = create_tween()
    _tween.set_parallel(true)
    
    # Fade in new track
    new_player.play(start_position)
    _tween.tween_property(new_player, "volume_db", 0.0, fade_duration)
    
    # Fade out current track
    if _current_player and _current_player.playing:
        _tween.tween_property(_current_player, "volume_db", -80.0, fade_duration)
        _tween.chain().tween_callback(_current_player.stop)
        _tween.chain().tween_callback(_current_player.queue_free)
        _previous_player = _current_player
    
    _current_player = new_player
    
    # Connect finished signal for looping
    new_player.finished.connect(_on_track_finished)

func _on_track_finished():
    if _current_player and _current_player.stream:
        _current_player.play(0.0)  # Loop

func stop_music(fade_out: bool = true):
    if not _current_player:
        return
    
    if fade_out:
        if _tween and _tween.is_valid():
            _tween.kill()
        
        _tween = create_tween()
        _tween.tween_property(_current_player, "volume_db", -80.0, fade_duration)
        _tween.tween_callback(_current_player.stop)
    else:
        _current_player.stop()

func set_volume_linear(linear: float):
    if _current_player:
        _current_player.volume_db = linear_to_db(clamp(linear, 0.0001, 1.0))
```

**Stinger/Overlay System:**
```gdscript
# music_stinger.gd
extends Node

class_name MusicStinger

@export var music_bus: String = "Music"
@export var stinger_bus: String = "SFX"  # Or dedicated stinger bus

var _music_player: AudioStreamPlayer
var _stinger_player: AudioStreamPlayer

func _ready():
    _setup_players()

func _setup_players():
    _music_player = AudioStreamPlayer.new()
    _music_player.bus = music_bus
    _music_player.name = "MusicPlayer"
    add_child(_music_player)
    
    _stinger_player = AudioStreamPlayer.new()
    _stinger_player.bus = stinger_bus
    _stinger_player.name = "StingerPlayer"
    add_child(_stinger_player)

func play_music(stream: AudioStream, loop: bool = true):
    _music_player.stream = stream
    _music_player.play()
    if loop:
        _music_player.finished.connect(_music_player.play, CONNECT_ONE_SHOT)

func play_stinger(stream: AudioStream, duck_music_db: float = -10.0, duration: float = 0.5):
    # Duck music volume
    var music_bus_idx = AudioServer.get_bus_index(music_bus)
    var original_db = AudioServer.get_bus_volume_db(music_bus_idx)
    
    var duck_tween = create_tween()
    duck_tween.tween_method(
        func(vol): AudioServer.set_bus_volume_db(music_bus_idx, vol),
        original_db,
        original_db + duck_music_db,
        0.1
    )
    
    # Play stinger
    _stinger_player.stream = stream
    _stinger_player.play()
    
    # Restore music after stinger
    await _stinger_player.finished
    
    var restore_tween = create_tween()
    restore_tween.tween_method(
        func(vol): AudioServer.set_bus_volume_db(music_bus_idx, vol),
        original_db + duck_music_db,
        original_db,
        duration
    )
```

**Adaptive Music System:**
```gdscript
# adaptive_music_controller.gd
extends Node

class_name AdaptiveMusicController

@export var intensity_tracks: Array[AudioStream] = []
@export var crossfade_time: float = 3.0

var _players: Array[AudioStreamPlayer] = []
var _current_intensity: int = 0

func _ready():
    _setup_players()

func _setup_players():
    for i in range(intensity_tracks.size()):
        var player = AudioStreamPlayer.new()
        player.bus = "Music"
        player.stream = intensity_tracks[i]
        player.volume_db = -80.0 if i != 0 else 0.0
        player.name = "Intensity_%d" % i
        add_child(player)
        _players.append(player)
        
        if i == 0:
            player.play()
            player.finished.connect(player.play)

func set_intensity(level: int):
    level = clamp(level, 0, _players.size() - 1)
    if level == _current_intensity:
        return
    
    var prev_player = _players[_current_intensity]
    var next_player = _players[level]
    
    # Sync playback position
    var playback_pos = prev_player.get_playback_position()
    next_player.play(playback_pos)
    next_player.finished.connect(next_player.play)
    
    # Crossfade
    var tween = create_tween()
    tween.set_parallel(true)
    tween.tween_property(prev_player, "volume_db", -80.0, crossfade_time)
    tween.tween_property(next_player, "volume_db", 0.0, crossfade_time)
    
    _current_intensity = level
```

## Examples

### Complete Audio Manager Setup

**Scene Structure:**
```ini
# audio_manager.tscn
[gd_scene load_steps=6 format=3]

[ext_resource type="Script" path="res://audio/audio_manager.gd" id="1_abc123"]
[ext_resource type="Script" path="res://audio/audio_pool.gd" id="2_def456"]
[ext_resource type="Script" path="res://audio/music_crossfader.gd" id="3_ghi789"]
[ext_resource type="Script" path="res://audio/audio_effects.gd" id="4_jkl012"]

[sub_resource type="AudioStreamRandomizer" id="AudioStreamRandomizer_sfx"]

[node name="AudioManager" type="Node"]
script = ExtResource("1_abc123")

[node name="SFXPool" type="Node" parent="."]
script = ExtResource("2_def456")
pool_size = 32
bus = "SFX"

[node name="MusicCrossfader" type="Node" parent="."]
script = ExtResource("3_ghi789")
bus = "Music"
fade_duration = 3.0

[node name="AudioEffects" type="Node" parent="."]
script = ExtResource("4_jkl012")

[node name="AmbientPlayer" type="AudioStreamPlayer" parent="."]
bus = "Ambient"
autoplay = true
```

**Audio Manager Script:**
```gdscript
# audio_manager.gd
extends Node

@onready var sfx_pool: AudioPool = $SFXPool
@onready var music_crossfader: MusicCrossfader = $MusicCrossfader
@onready var audio_effects: Node = $AudioEffects
@onready var ambient_player: AudioStreamPlayer = $AmbientPlayer

func _ready():
    # Setup bus effects
    audio_effects.add_reverb_to_bus("Ambient", 0.6, 0.4, 0.3)
    audio_effects.add_compressor_to_bus("Voice")
    audio_effects.add_limiter_to_master()
    
    print("Audio system initialized")

func play_sfx(stream: AudioStream, volume_db: float = 0.0):
    sfx_pool.play_sound(stream, volume_db)

func play_music(stream: AudioStream, crossfade: bool = true):
    if crossfade:
        music_crossfader.crossfade_to(stream)
    else:
        # Immediate switch
        pass

func set_master_volume(linear: float):
    var idx = AudioServer.get_bus_index("Master")
    AudioServer.set_bus_volume_db(idx, linear_to_db(clamp(linear, 0.0001, 1.0)))

func set_music_volume(linear: float):
    var idx = AudioServer.get_bus_index("Music")
    AudioServer.set_bus_volume_db(idx, linear_to_db(clamp(linear, 0.0001, 1.0)))

func set_sfx_volume(linear: float):
    var idx = AudioServer.get_bus_index("SFX")
    AudioServer.set_bus_volume_db(idx, linear_to_db(clamp(linear, 0.0001, 1.0)))

func set_ambient(stream: AudioStream):
    ambient_player.stream = stream
    ambient_player.play()
```

### Footstep System with Pooling

```gdscript
# footsteps_controller.gd
extends Node

@export var footstep_sounds: Array[AudioStream] = []
@export var min_interval: float = 0.3
@export var volume_range: Vector2 = Vector2(-10.0, -5.0)
@export var pitch_variation: float = 0.1

@onready var audio_pool: AudioPool2D = $"../AudioManager/SFXPool"

var _last_footstep_time: float = 0.0

func play_footstep(global_pos: Vector2):
    var current_time = Time.get_time_dict_from_system()["second"]
    if current_time - _last_footstep_time < min_interval:
        return
    
    _last_footstep_time = current_time
    
    if footstep_sounds.is_empty():
        return
    
    var sound = footstep_sounds.pick_random()
    var volume = randf_range(volume_range.x, volume_range.y)
    var pitch = 1.0 + randf_range(-pitch_variation, pitch_variation)
    
    audio_pool.play_sound_at(sound, global_pos, volume, pitch)
```

### Dynamic Environment Audio

```gdscript
# environment_audio.gd
extends Area2D

@export var reverb_preset: String = "cave"
@export var enter_music: AudioStream
@export var ambient_loop: AudioStream

@onready var audio_manager = get_node("/root/AudioManager")

func _on_body_entered(body):
    if not body.is_in_group("player"):
        return
    
    # Apply reverb to ambient bus
    var ambient_idx = AudioServer.get_bus_index("Ambient")
    match reverb_preset:
        "small_room": ReverbPresets.apply_small_room(ambient_idx)
        "cave": ReverbPresets.apply_cave(ambient_idx)
        "cathedral": ReverbPresets.apply_cathedral(ambient_idx)
        "underwater": ReverbPresets.apply_underwater(ambient_idx)
    
    # Crossfade to area music
    if enter_music:
        audio_manager.play_music(enter_music)
    
    # Change ambient
    if ambient_loop:
        audio_manager.set_ambient(ambient_loop)

func _on_body_exited(body):
    if not body.is_in_group("player"):
        return
    
    # Remove effects when leaving
    var ambient_idx = AudioServer.get_bus_index("Ambient")
    var effect_count = AudioServer.get_bus_effect_count(ambient_idx)
    for i in range(effect_count - 1, -1, -1):
        AudioServer.remove_bus_effect(ambient_idx, i)
```

## Integration Patterns

### With godot-add-signals

**Audio Event System:**
```gdscript
# Connect audio to game events
func _ready():
    EventBus.enemy_died.connect(_on_enemy_died)
    EventBus.player_took_damage.connect(_on_player_damage)
    EventBus.level_completed.connect(_on_level_complete)

func _on_enemy_died(pos: Vector2):
    play_sfx_at(enemy_death_sound, pos)

func _on_player_damage():
    play_sfx(player_hurt_sound, -5.0)
    # Screen shake or low-pass filter could go here

func _on_level_complete():
    music_crossfader.crossfade_to(victory_music)
```

### With godot-extract-to-scenes

**Reusable Audio Components:**
```gdscript
# Extract these to scenes:
# - audio_trigger_area.tscn (plays sound on enter)
# - spatial_audio_emitter.tscn (3D positioned looping sound)
# - music_zone.tscn (changes music when entered)
# - ambient_zone.tscn (changes ambient sounds)
```

## Safety

- Always check bus indices exist before operations
- Pool size should match max concurrent sounds needed
- Clean up finished audio players in pools
- Avoid creating AudioStreamPlayers in _process or _physics_process
- Use limiter on Master bus to prevent clipping
- Test audio at different volume levels

## Performance Tips

1. **Preload common sounds** - Don't load in play() callback
2. **Use pools for frequent sounds** - Gunshots, footsteps, UI clicks
3. **Limit concurrent sounds** - 3D audio has performance cost
4. **Reuse AudioStream resources** - Don't duplicate stream data
5. **Bus effects are expensive** - Use sparingly, especially on Master
6. **Stream long audio** - Use .ogg or .mp3 for music, not .wav

## Common Mistakes

### Mistake 1: Creating players in loops
```gdscript
# BAD - Creates garbage every frame
func _process(delta):
    if Input.is_action_just_pressed("shoot"):
        var player = AudioStreamPlayer.new()  # Don't do this!
        player.stream = shoot_sound
        add_child(player)
        player.play()
```

### Mistake 2: Not using bus hierarchy
```gdscript
# BAD - All sounds on Master bus
# No volume control per category
```

### Mistake 3: Forgetting to pool 2D/3D audio
```gdscript
# BAD - Spatial audio without pooling
# Position updates every frame with new players
```

## When NOT to Use

Don't use complex bus architecture when:
- Game has very few sounds (< 10 total)
- No need for dynamic mixing or effects
- Simple prototype where audio polish doesn't matter

Use simple direct playback instead:
```gdscript
# Simple approach for small projects
$AudioStreamPlayer.stream = sound
$AudioStreamPlayer.play()
```

