---
name: location-ar-experience
description: Designs location-based augmented reality experiences with geospatial anchoring, GPS integration, and real-world interactive overlays.
license: MIT
---

# Location-Based AR Experience

This skill provides guidance for designing augmented reality experiences anchored to real-world locations, combining GPS, computer vision, and spatial computing.

## Core Competencies

- **Geospatial Anchoring**: GPS, geofencing, coordinate systems
- **Visual Positioning**: SLAM, image recognition, cloud anchors
- **Content Placement**: World-scale AR, occlusion, persistence
- **Mobile AR Platforms**: ARKit, ARCore, WebXR

## Location-Based AR Fundamentals

### AR Experience Types

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Location-Based AR Spectrum                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  GPS-Only          Hybrid              Vision-Based                 │
│  ┌─────────┐      ┌─────────┐         ┌─────────┐                  │
│  │ ~10m    │      │ ~1m     │         │ ~1cm    │                  │
│  │accuracy │      │accuracy │         │accuracy │                  │
│  └─────────┘      └─────────┘         └─────────┘                  │
│      │                │                    │                        │
│      ▼                ▼                    ▼                        │
│  City-scale      Building-scale      Room-scale                    │
│  navigation      experiences         precision                      │
│  games           POI overlays        installations                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Accuracy Requirements by Experience Type

| Experience | Required Accuracy | Positioning Method |
|------------|-------------------|-------------------|
| City navigation | 5-15 meters | GPS |
| POI discovery | 3-5 meters | GPS + Wi-Fi |
| Building entrance | 1-2 meters | GPS + Vision |
| Indoor navigation | 0.5-1 meter | Vision + beacons |
| Object placement | 1-10 cm | Pure visual SLAM |

## Geospatial Systems

### Coordinate Systems

```python
from dataclasses import dataclass
import math

@dataclass
class GeoCoordinate:
    """WGS84 coordinate"""
    latitude: float   # -90 to 90
    longitude: float  # -180 to 180
    altitude: float = 0  # meters above sea level

    def distance_to(self, other: 'GeoCoordinate') -> float:
        """Haversine distance in meters"""
        R = 6371000  # Earth radius in meters

        lat1, lat2 = math.radians(self.latitude), math.radians(other.latitude)
        dlat = math.radians(other.latitude - self.latitude)
        dlon = math.radians(other.longitude - self.longitude)

        a = (math.sin(dlat/2)**2 +
             math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return R * c

    def bearing_to(self, other: 'GeoCoordinate') -> float:
        """Bearing in degrees (0-360)"""
        lat1 = math.radians(self.latitude)
        lat2 = math.radians(other.latitude)
        dlon = math.radians(other.longitude - self.longitude)

        x = math.sin(dlon) * math.cos(lat2)
        y = (math.cos(lat1) * math.sin(lat2) -
             math.sin(lat1) * math.cos(lat2) * math.cos(dlon))

        bearing = math.degrees(math.atan2(x, y))
        return (bearing + 360) % 360


@dataclass
class ARWorldCoordinate:
    """Local AR coordinate (meters from origin)"""
    x: float  # East
    y: float  # Up
    z: float  # North


def geo_to_local(geo: GeoCoordinate, origin: GeoCoordinate) -> ARWorldCoordinate:
    """Convert geographic to local AR coordinates"""
    # Simplified planar projection (accurate for small areas)
    lat_scale = 111320  # meters per degree latitude
    lon_scale = 111320 * math.cos(math.radians(origin.latitude))

    x = (geo.longitude - origin.longitude) * lon_scale  # East
    z = (geo.latitude - origin.latitude) * lat_scale    # North
    y = geo.altitude - origin.altitude                   # Up

    return ARWorldCoordinate(x, y, z)
```

### Geofencing

```python
from enum import Enum
from typing import List, Callable

class GeofenceShape(Enum):
    CIRCLE = "circle"
    POLYGON = "polygon"

class Geofence:
    """Define trigger zones for AR content"""

    def __init__(self, id: str, center: GeoCoordinate, radius: float):
        self.id = id
        self.center = center
        self.radius = radius  # meters
        self.shape = GeofenceShape.CIRCLE
        self.on_enter: List[Callable] = []
        self.on_exit: List[Callable] = []
        self.on_dwell: List[Callable] = []
        self.dwell_time = 30  # seconds

    def contains(self, point: GeoCoordinate) -> bool:
        """Check if point is inside geofence"""
        return self.center.distance_to(point) <= self.radius

    def add_enter_handler(self, callback: Callable):
        self.on_enter.append(callback)


class GeofenceManager:
    """Manage multiple geofences"""

    def __init__(self):
        self.fences: dict[str, Geofence] = {}
        self.active_fences: set[str] = set()
        self.entry_times: dict[str, float] = {}

    def add_fence(self, fence: Geofence):
        self.fences[fence.id] = fence

    def update_position(self, position: GeoCoordinate, timestamp: float):
        """Check geofences and trigger callbacks"""
        currently_inside = set()

        for fence_id, fence in self.fences.items():
            if fence.contains(position):
                currently_inside.add(fence_id)

                # Trigger enter event
                if fence_id not in self.active_fences:
                    self.entry_times[fence_id] = timestamp
                    for callback in fence.on_enter:
                        callback(fence, position)

                # Check dwell time
                elif timestamp - self.entry_times[fence_id] >= fence.dwell_time:
                    for callback in fence.on_dwell:
                        callback(fence, position)

        # Trigger exit events
        for fence_id in self.active_fences - currently_inside:
            fence = self.fences[fence_id]
            for callback in fence.on_exit:
                callback(fence, position)
            del self.entry_times[fence_id]

        self.active_fences = currently_inside
```

## Visual Positioning

### ARCore Geospatial API Pattern

```kotlin
// Android/Kotlin with ARCore Geospatial API
class GeospatialManager(private val session: Session) {

    fun placeAnchorAtLocation(
        latitude: Double,
        longitude: Double,
        altitude: Double,
        heading: Float
    ): Anchor? {
        val earth = session.earth ?: return null

        // Check tracking quality
        if (earth.trackingState != TrackingState.TRACKING) {
            return null
        }

        // Check horizontal accuracy
        val pose = earth.cameraGeospatialPose
        if (pose.horizontalAccuracy > 10) {  // meters
            return null  // Not accurate enough
        }

        // Create geospatial anchor
        val quaternion = Quaternion.axisAngle(
            Vector3(0f, 1f, 0f),
            Math.toRadians(heading.toDouble()).toFloat()
        )

        return earth.createAnchor(
            latitude, longitude, altitude,
            quaternion.x, quaternion.y, quaternion.z, quaternion.w
        )
    }

    fun resolveTerrainAnchor(
        latitude: Double,
        longitude: Double,
        heading: Float,
        callback: (Anchor?) -> Unit
    ) {
        val earth = session.earth ?: return callback(null)

        // Terrain anchor automatically determines altitude
        val future = earth.resolveAnchorOnTerrainAsync(
            latitude, longitude,
            0.0,  // altitude above terrain
            /* quaternion */ 0f, 0f, 0f, 1f,
            { anchor, state ->
                when (state) {
                    Anchor.TerrainAnchorState.SUCCESS -> callback(anchor)
                    else -> callback(null)
                }
            }
        )
    }
}
```

### Cloud Anchors for Persistence

```swift
// iOS/Swift with ARKit Cloud Anchors
class CloudAnchorManager {
    var arView: ARView
    var anchorStore: [String: ARAnchor] = [:]

    func saveAnchor(_ anchor: ARAnchor, completion: @escaping (String?) -> Void) {
        // Upload anchor to cloud service
        let anchorData = AnchorData(
            transform: anchor.transform,
            identifier: anchor.identifier.uuidString
        )

        CloudService.shared.uploadAnchor(anchorData) { cloudId in
            if let id = cloudId {
                self.anchorStore[id] = anchor
            }
            completion(cloudId)
        }
    }

    func resolveAnchor(cloudId: String, completion: @escaping (ARAnchor?) -> Void) {
        CloudService.shared.downloadAnchor(cloudId) { anchorData in
            guard let data = anchorData else {
                completion(nil)
                return
            }

            let anchor = ARAnchor(transform: data.transform)
            self.arView.session.add(anchor: anchor)
            completion(anchor)
        }
    }
}
```

## Content Management

### AR Content Data Model

```python
from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum

class ContentType(Enum):
    MODEL_3D = "model_3d"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    TEXT = "text"
    INTERACTIVE = "interactive"

@dataclass
class ARContent:
    """AR content anchored to location"""
    id: str
    content_type: ContentType
    location: GeoCoordinate

    # Asset references
    asset_url: str
    thumbnail_url: Optional[str] = None

    # Spatial properties
    scale: float = 1.0
    rotation_y: float = 0.0  # Heading in degrees
    offset_y: float = 0.0    # Height offset from ground

    # Visibility rules
    min_distance: float = 0.0
    max_distance: float = 100.0
    visible_hours: Optional[tuple[int, int]] = None  # Start, end hour

    # Interaction
    interactive: bool = False
    trigger_radius: float = 5.0

    # Metadata
    title: str = ""
    description: str = ""
    tags: List[str] = field(default_factory=list)


@dataclass
class ARExperience:
    """Collection of AR content forming an experience"""
    id: str
    name: str
    description: str

    # Bounds
    center: GeoCoordinate
    radius: float  # meters

    # Content
    contents: List[ARContent] = field(default_factory=list)

    # Experience flow
    ordered: bool = False  # Sequential vs free exploration
    start_content_id: Optional[str] = None

    def get_visible_content(
        self,
        user_position: GeoCoordinate,
        current_hour: int
    ) -> List[ARContent]:
        """Filter content visible from user position"""
        visible = []

        for content in self.contents:
            distance = user_position.distance_to(content.location)

            # Distance check
            if distance < content.min_distance or distance > content.max_distance:
                continue

            # Time check
            if content.visible_hours:
                start, end = content.visible_hours
                if not (start <= current_hour < end):
                    continue

            visible.append(content)

        return visible
```

### Spatial Data Loading Strategy

```python
class SpatialContentLoader:
    """Efficiently load content near user"""

    def __init__(self, api_client):
        self.api = api_client
        self.cache: dict[str, ARContent] = {}
        self.loaded_tiles: set[str] = set()
        self.tile_size = 0.001  # ~111 meters at equator

    def get_tile_key(self, coord: GeoCoordinate) -> str:
        """Get tile identifier for coordinate"""
        lat_tile = int(coord.latitude / self.tile_size)
        lon_tile = int(coord.longitude / self.tile_size)
        return f"{lat_tile}:{lon_tile}"

    async def update_position(self, position: GeoCoordinate):
        """Load content for position and surrounding tiles"""
        # Get 3x3 grid of tiles around user
        tiles_needed = set()
        for dlat in [-1, 0, 1]:
            for dlon in [-1, 0, 1]:
                adjusted = GeoCoordinate(
                    position.latitude + dlat * self.tile_size,
                    position.longitude + dlon * self.tile_size
                )
                tiles_needed.add(self.get_tile_key(adjusted))

        # Load new tiles
        new_tiles = tiles_needed - self.loaded_tiles
        for tile in new_tiles:
            content = await self.api.get_content_for_tile(tile)
            for item in content:
                self.cache[item.id] = item
            self.loaded_tiles.add(tile)

        # Unload distant tiles (keep only 5x5 grid)
        # ... cleanup logic

    def get_nearby_content(
        self,
        position: GeoCoordinate,
        radius: float
    ) -> List[ARContent]:
        """Get cached content within radius"""
        return [
            content for content in self.cache.values()
            if position.distance_to(content.location) <= radius
        ]
```

## User Experience Patterns

### Wayfinding

```python
class ARWayfinder:
    """Guide user to AR content"""

    def __init__(self):
        self.current_target: Optional[ARContent] = None
        self.path: List[GeoCoordinate] = []

    def set_target(self, content: ARContent, user_position: GeoCoordinate):
        """Set navigation target"""
        self.current_target = content
        self.path = self._calculate_path(user_position, content.location)

    def get_direction_indicator(
        self,
        user_position: GeoCoordinate,
        user_heading: float
    ) -> dict:
        """Get AR direction indicator data"""
        if not self.current_target:
            return None

        target_bearing = user_position.bearing_to(self.current_target.location)
        relative_bearing = (target_bearing - user_heading + 360) % 360

        distance = user_position.distance_to(self.current_target.location)

        return {
            'type': 'direction_arrow',
            'bearing': relative_bearing,  # 0 = straight ahead
            'distance': distance,
            'distance_text': self._format_distance(distance),
            'in_view': -30 <= relative_bearing <= 30 or relative_bearing >= 330
        }

    def _format_distance(self, meters: float) -> str:
        if meters < 100:
            return f"{int(meters)}m"
        elif meters < 1000:
            return f"{int(meters/10)*10}m"
        else:
            return f"{meters/1000:.1f}km"
```

### Content Discovery

```
User Approaching Content:

100m away:  [Map indicator only]
            "5 AR experiences nearby"

50m away:   [Floating label appears]
            "Historic Building - 50m"
                    ▼

20m away:   [Label grows, thumbnail shows]
            ┌──────────────┐
            │   [image]    │
            │ Historic     │
            │ Building     │
            │    20m →     │
            └──────────────┘

5m away:    [Full AR content triggers]
            3D model appears at location
            Info panel available
```

### Interaction Zones

```python
class InteractionZone:
    """Define how users interact with AR content"""

    def __init__(self, content: ARContent):
        self.content = content

        # Zone radii (meters)
        self.awareness_radius = 100  # Show on map
        self.preview_radius = 50     # Show floating label
        self.activation_radius = 20  # Show full AR
        self.interaction_radius = 5  # Can interact

    def get_interaction_state(
        self,
        user_position: GeoCoordinate
    ) -> str:
        """Determine current interaction state"""
        distance = user_position.distance_to(self.content.location)

        if distance <= self.interaction_radius:
            return "interactive"
        elif distance <= self.activation_radius:
            return "active"
        elif distance <= self.preview_radius:
            return "preview"
        elif distance <= self.awareness_radius:
            return "aware"
        else:
            return "hidden"
```

## Performance Optimization

### LOD (Level of Detail)

```python
class LODManager:
    """Manage content detail based on distance"""

    LOD_LEVELS = {
        'full': {'max_distance': 10, 'quality': 'high'},
        'medium': {'max_distance': 30, 'quality': 'medium'},
        'low': {'max_distance': 100, 'quality': 'low'},
        'billboard': {'max_distance': float('inf'), 'quality': 'billboard'}
    }

    def get_lod_for_distance(self, distance: float) -> str:
        for level, config in self.LOD_LEVELS.items():
            if distance <= config['max_distance']:
                return level
        return 'billboard'

    def get_asset_url(self, content: ARContent, lod: str) -> str:
        """Get appropriate asset for LOD level"""
        base_url = content.asset_url.rsplit('.', 1)[0]

        if lod == 'billboard':
            return content.thumbnail_url
        elif lod == 'low':
            return f"{base_url}_low.glb"
        elif lod == 'medium':
            return f"{base_url}_med.glb"
        else:
            return content.asset_url
```

### Battery and Data Conservation

```python
class LocationOptimizer:
    """Optimize location updates for battery life"""

    def __init__(self):
        self.high_accuracy_mode = False
        self.last_position: Optional[GeoCoordinate] = None
        self.movement_threshold = 5  # meters

    def should_update_ar(self, new_position: GeoCoordinate) -> bool:
        """Determine if AR scene needs update"""
        if not self.last_position:
            self.last_position = new_position
            return True

        distance_moved = self.last_position.distance_to(new_position)

        if distance_moved > self.movement_threshold:
            self.last_position = new_position
            return True

        return False

    def get_location_config(self, near_content: bool) -> dict:
        """Get GPS configuration based on context"""
        if near_content:
            return {
                'accuracy': 'high',
                'interval_ms': 1000,
                'distance_filter': 1
            }
        else:
            return {
                'accuracy': 'balanced',
                'interval_ms': 5000,
                'distance_filter': 10
            }
```

## Best Practices

### Design Guidelines

1. **Respect physical space**: Don't place AR content blocking paths or in dangerous locations
2. **Consider lighting**: Outdoor AR needs to handle bright sun and shadows
3. **Provide fallbacks**: Show 2D map when AR isn't possible
4. **Clear affordances**: Users should know what's interactive
5. **Graceful degradation**: Work with varying GPS accuracy

### Testing Considerations

- Test with real GPS, not just simulated coordinates
- Test in different weather and lighting conditions
- Test battery drain over extended sessions
- Test with poor network connectivity

## References

- `references/arcore-geospatial.md` - ARCore Geospatial API guide
- `references/arkit-location.md` - ARKit location anchoring
- `references/coordinate-systems.md` - Geospatial coordinate conversions
