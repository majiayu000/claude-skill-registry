---
name: map-integration
description: Google Maps and Mapbox integration for Flutter applications
keywords: maps, google-maps, mapbox, location, geolocation, navigation
---

# Skill 18: Map Integration

## Overview

This skill enables map integration in Flutter applications using Google Maps and Mapbox. Includes features like markers, polylines, clustering, custom styles, and location tracking.

## Features

- Google Maps integration
- Mapbox integration
- Custom markers and clusters
- Location tracking
- Polylines and polygons
- Offline maps support
- Geocoding and reverse geocoding
- Directions and routing

## Installation

### Dependencies

```yaml
dependencies:
  google_maps_flutter: ^2.5.0
  mapbox_gl: ^0.16.0
  geolocator: ^10.1.0
  geocoding: ^2.1.1
  flutter_polyline_points: ^2.0.0
  maps_toolkit: ^3.0.0
```

## Google Maps Setup

### 1. Configuration

**Android:**
```xml
<!-- AndroidManifest.xml -->
<manifest>
  <application>
    <meta-data
      android:name="com.google.android.geo.API_KEY"
      android:value="YOUR_API_KEY" />
  </application>
</manifest>
```

**iOS:**
```xml
<!-- AppDelegate.swift -->
import GoogleMaps

GMSServices.provideAPIKey("YOUR_API_KEY")
```

### 2. Basic Map Widget

```dart
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:flutter/material.dart';

class MapPage extends StatefulWidget {
  const MapPage({super.key});

  @override
  State<MapPage> createState() => _MapPageState();
}

class _MapPageState extends State<MapPage> {
  GoogleMapController? _mapController;

  static const CameraPosition _initialPosition = CameraPosition(
    target: LatLng(37.7749, -122.4194), // San Francisco
    zoom: 12,
  );

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: GoogleMap(
        mapType: MapType.normal,
        initialCameraPosition: _initialPosition,
        onMapCreated: (controller) {
          _mapController = controller;
        },
        myLocationEnabled: true,
        myLocationButtonEnabled: true,
      ),
    );
  }

  @override
  void dispose() {
    _mapController?.dispose();
    super.dispose();
  }
}
```

### 3. Map Service

```dart
class MapService {
  GoogleMapController? _controller;

  void setController(GoogleMapController controller) {
    _controller = controller;
  }

  Future<void> animateToLocation(LatLng location, {double zoom = 15}) async {
    await _controller?.animateCamera(
      CameraUpdate.newCameraPosition(
        CameraPosition(target: location, zoom: zoom),
      ),
    );
  }

  Future<void> addMarker(Marker marker) async {
    // Implementation depends on your state management
  }

  Future<void> drawPolyline(List<LatLng> points) async {
    // Implementation
  }
}
```

## Markers and Clusters

```dart
class MarkerManager {
  final Set<Marker> _markers = {};

  Set<Marker> get markers => _markers;

  void addMarker({
    required String id,
    required LatLng position,
    String? title,
    String? snippet,
    BitmapDescriptor? icon,
  }) {
    final marker = Marker(
      markerId: MarkerId(id),
      position: position,
      infoWindow: InfoWindow(
        title: title,
        snippet: snippet,
      ),
      icon: icon ?? BitmapDescriptor.defaultMarker,
    );

    _markers.add(marker);
  }

  void removeMarker(String id) {
    _markers.removeWhere((marker) => marker.markerId.value == id);
  }

  void clearMarkers() {
    _markers.clear();
  }
}
```

## Location Tracking

```dart
import 'package:geolocator/geolocator.dart';

class LocationService {
  Future<Position> getCurrentLocation() async {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      throw Exception('Location services are disabled');
    }

    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        throw Exception('Location permissions are denied');
      }
    }

    return await Geolocator.getCurrentPosition();
  }

  Stream<Position> getLocationStream() {
    return Geolocator.getPositionStream(
      locationSettings: const LocationSettings(
        accuracy: LocationAccuracy.high,
        distanceFilter: 10, // meters
      ),
    );
  }
}

// Usage in a map
class TrackingMap extends ConsumerWidget {
  const TrackingMap({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final locationService = LocationService();

    return StreamBuilder<Position>(
      stream: locationService.getLocationStream(),
      builder: (context, snapshot) {
        if (!snapshot.hasData) {
          return const Center(child: CircularProgressIndicator());
        }

        final position = snapshot.data!;

        return GoogleMap(
          initialCameraPosition: CameraPosition(
            target: LatLng(position.latitude, position.longitude),
            zoom: 15,
          ),
          markers: {
            Marker(
              markerId: const MarkerId('currentLocation'),
              position: LatLng(position.latitude, position.longitude),
              icon: BitmapDescriptor.defaultMarkerWithHue(
                BitmapDescriptor.hueBlue,
              ),
            ),
          },
        );
      },
    );
  }
}
```

## Routing and Directions

```dart
import 'package:flutter_polyline_points/flutter_polyline_points.dart';

class RoutingService {
  final String apiKey;
  final PolylinePoints _polylinePoints = PolylinePoints();

  RoutingService({required this.apiKey});

  Future<List<LatLng>> getDirections(
    LatLng origin,
    LatLng destination,
  ) async {
    final result = await _polylinePoints.getRouteBetweenCoordinates(
      googleApiKey: apiKey,
      request: PolylineRequest(
        origin: PointLatLng(origin.latitude, origin.longitude),
        destination: PointLatLng(destination.latitude, destination.longitude),
        mode: TravelMode.driving,
      ),
    );

    if (result.points.isNotEmpty) {
      return result.points
          .map((point) => LatLng(point.latitude, point.longitude))
          .toList();
    }

    return [];
  }
}
```

## Complete Map Example

```dart
class RescueMapPage extends ConsumerStatefulWidget {
  const RescueMapPage({super.key});

  @override
  ConsumerState<RescueMapPage> createState() => _RescueMapPageState();
}

class _RescueMapPageState extends ConsumerState<RescueMapPage> {
  GoogleMapController? _controller;
  final Set<Marker> _markers = {};
  List<LatLng> _routePoints = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Rescue Map')),
      body: Stack(
        children: [
          GoogleMap(
            mapType: MapType.normal,
            initialCameraPosition: const CameraPosition(
              target: LatLng(37.7749, -122.4194),
              zoom: 12,
            ),
            markers: _markers,
            polylines: {
              Polyline(
                polylineId: const PolylineId('route'),
                points: _routePoints,
                color: Colors.blue,
                width: 5,
              ),
            },
            onMapCreated: (controller) {
              _controller = controller;
              _loadRescueLocations();
            },
            onTap: _handleMapTap,
          ),
          Positioned(
            bottom: 16,
            right: 16,
            child: FloatingActionButton(
              onPressed: _centerOnCurrentLocation,
              child: const Icon(Icons.my_location),
            ),
          ),
        ],
      ),
    );
  }

  void _loadRescueLocations() {
    // Add rescue markers
    setState(() {
      _markers.addAll([
        Marker(
          markerId: const MarkerId('rescue1'),
          position: const LatLng(37.7849, -122.4094),
          infoWindow: const InfoWindow(
            title: 'Dog Rescue',
            snippet: 'Urgent - Needs transport',
          ),
          icon: BitmapDescriptor.defaultMarkerWithHue(
            BitmapDescriptor.hueRed,
          ),
        ),
      ]);
    });
  }

  void _handleMapTap(LatLng position) {
    // Add marker at tap location
    setState(() {
      _markers.add(
        Marker(
          markerId: MarkerId('tap_${position.latitude}_${position.longitude}'),
          position: position,
        ),
      );
    });
  }

  Future<void> _centerOnCurrentLocation() async {
    final position = await LocationService().getCurrentLocation();
    _controller?.animateCamera(
      CameraUpdate.newLatLng(
        LatLng(position.latitude, position.longitude),
      ),
    );
  }
}
```

## Best Practices

1. **Request location permissions properly** - Handle all permission states
2. **Dispose controllers** - Always dispose map controllers
3. **Limit markers** - Use clustering for large numbers of markers
4. **Cache tiles** - Enable map tile caching for offline use
5. **Optimize updates** - Don't rebuild map on every state change

## Troubleshooting

### Map not showing
- Check API key is valid
- Verify billing is enabled on Google Cloud
- Enable Maps SDK for Android/iOS in Google Cloud Console

### Location not working
- Verify location permissions in manifest
- Check if location services are enabled
- Test on physical device (emulator may have issues)

### High memory usage
- Limit number of markers
- Use marker clustering
- Dispose controllers properly
- Clear cache when not needed
