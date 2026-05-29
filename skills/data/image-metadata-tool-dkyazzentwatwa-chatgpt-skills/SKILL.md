---
name: image-metadata-tool
description: Extract EXIF metadata from images including GPS coordinates, camera settings, and timestamps. Map photo locations and strip metadata for privacy.
---

# Image Metadata Tool

Extract, analyze, and manage EXIF metadata from images with GPS mapping and privacy features.

## Features

- **EXIF Extraction**: Camera, lens, settings, timestamps
- **GPS Data**: Extract coordinates, map locations
- **Metadata Removal**: Strip EXIF for privacy
- **Batch Processing**: Process multiple images
- **Map Generation**: Create location maps from photos
- **Export**: JSON, CSV, HTML reports

## Quick Start

```python
from image_metadata import ImageMetadata

meta = ImageMetadata()
meta.load("photo.jpg")

# Get all metadata
info = meta.extract()
print(f"Camera: {info['camera']}")
print(f"Date: {info['datetime']}")

# Get GPS coordinates
gps = meta.get_gps()
if gps:
    print(f"Location: {gps['latitude']}, {gps['longitude']}")
```

## CLI Usage

```bash
# Extract metadata
python image_metadata.py --input photo.jpg

# Extract with GPS info
python image_metadata.py --input photo.jpg --gps

# Batch extract from folder
python image_metadata.py --input ./photos/ --output metadata.csv

# Generate location map
python image_metadata.py --input ./photos/ --map locations.html

# Strip metadata (create clean copy)
python image_metadata.py --input photo.jpg --strip --output clean_photo.jpg

# Batch strip metadata
python image_metadata.py --input ./photos/ --strip --output ./clean_photos/

# JSON output
python image_metadata.py --input photo.jpg --json

# Get specific fields
python image_metadata.py --input photo.jpg --fields camera,datetime,gps,dimensions
```

## API Reference

### ImageMetadata Class

```python
class ImageMetadata:
    def __init__(self)

    # Loading
    def load(self, filepath: str) -> 'ImageMetadata'

    # Extraction
    def extract(self) -> dict
    def get_camera_info(self) -> dict
    def get_datetime(self) -> dict
    def get_gps(self) -> dict
    def get_dimensions(self) -> dict
    def get_all_exif(self) -> dict

    # Privacy
    def strip_metadata(self, output: str, keep_orientation: bool = True) -> str
    def has_location(self) -> bool

    # Batch operations
    def extract_batch(self, folder: str, recursive: bool = False) -> list
    def strip_batch(self, input_folder: str, output_folder: str) -> list

    # Maps
    def generate_map(self, images: list, output: str) -> str

    # Export
    def to_json(self, output: str) -> str
    def to_csv(self, output: str) -> str
```

## Extracted Metadata

### Camera Information

```python
camera_info = meta.get_camera_info()

# Returns:
{
    "make": "Canon",
    "model": "EOS R5",
    "lens": "RF 24-70mm F2.8 L IS USM",
    "lens_id": "61",
    "software": "Adobe Photoshop 24.0",
    "serial_number": "012345678901"
}
```

### Capture Settings

```python
settings = meta.extract()["settings"]

# Returns:
{
    "exposure_time": "1/250",
    "f_number": 2.8,
    "iso": 400,
    "focal_length": 50,
    "focal_length_35mm": 50,
    "exposure_program": "Aperture priority",
    "metering_mode": "Pattern",
    "flash": "No flash",
    "white_balance": "Auto"
}
```

### GPS Data

```python
gps = meta.get_gps()

# Returns:
{
    "latitude": 37.7749,
    "longitude": -122.4194,
    "altitude": 10.5,
    "altitude_ref": "Above sea level",
    "timestamp": "2024-01-15 14:30:00",
    "direction": 180.5,
    "speed": 0,
    "maps_url": "https://maps.google.com/maps?q=37.7749,-122.4194"
}
```

### Timestamps

```python
datetime_info = meta.get_datetime()

# Returns:
{
    "original": "2024-01-15 14:30:00",
    "digitized": "2024-01-15 14:30:00",
    "modified": "2024-01-16 10:00:00",
    "timezone": "+00:00"
}
```

### Image Dimensions

```python
dims = meta.get_dimensions()

# Returns:
{
    "width": 8192,
    "height": 5464,
    "megapixels": 44.8,
    "orientation": "Horizontal",
    "resolution_x": 300,
    "resolution_y": 300,
    "resolution_unit": "inch"
}
```

## Full Output

```python
info = meta.extract()

# Returns:
{
    "file": {
        "name": "IMG_1234.jpg",
        "path": "/photos/IMG_1234.jpg",
        "size": 15234567,
        "format": "JPEG"
    },
    "camera": {
        "make": "Canon",
        "model": "EOS R5",
        "lens": "RF 24-70mm F2.8 L IS USM"
    },
    "settings": {
        "exposure_time": "1/250",
        "f_number": 2.8,
        "iso": 400,
        "focal_length": 50
    },
    "datetime": {
        "original": "2024-01-15 14:30:00"
    },
    "gps": {
        "latitude": 37.7749,
        "longitude": -122.4194
    },
    "dimensions": {
        "width": 8192,
        "height": 5464
    }
}
```

## Privacy Features

### Strip Metadata

Remove EXIF data for privacy:

```python
# Strip all metadata
meta.load("original.jpg")
meta.strip_metadata("clean.jpg")

# Keep orientation (prevents rotated images)
meta.strip_metadata("clean.jpg", keep_orientation=True)
```

### Check for Location Data

```python
meta.load("photo.jpg")
if meta.has_location():
    print("Warning: Photo contains GPS coordinates!")
```

### Batch Strip

```python
meta.strip_batch("./originals/", "./cleaned/")
```

## GPS Mapping

### Generate Location Map

Create an interactive map from geotagged photos:

```python
meta = ImageMetadata()

# Batch extract with GPS
images = meta.extract_batch("./vacation_photos/")

# Filter to only geotagged images
geotagged = [img for img in images if img.get("gps")]

# Generate map
meta.generate_map(geotagged, "photo_map.html")
```

The map includes:
- Markers for each photo location
- Popup with photo thumbnail and metadata
- Clustering for dense areas

## Batch Processing

### Extract from Folder

```python
meta = ImageMetadata()

# All images in folder
results = meta.extract_batch("./photos/")

# Recursive (include subfolders)
results = meta.extract_batch("./photos/", recursive=True)

# Export to CSV
df = pd.DataFrame(results)
df.to_csv("metadata.csv", index=False)
```

### Filter by Criteria

```python
results = meta.extract_batch("./photos/")

# Find high ISO photos
high_iso = [r for r in results if r.get("settings", {}).get("iso", 0) > 3200]

# Find photos from specific camera
canon_photos = [r for r in results if "Canon" in r.get("camera", {}).get("make", "")]

# Find photos with GPS
geotagged = [r for r in results if r.get("gps")]
```

## Example Workflows

### Photo Organization

```python
meta = ImageMetadata()
results = meta.extract_batch("./camera_import/")

for photo in results:
    date = photo.get("datetime", {}).get("original", "unknown")
    camera = photo.get("camera", {}).get("model", "unknown")
    print(f"{photo['file']['name']}: {date} - {camera}")
```

### Privacy Audit

```python
meta = ImageMetadata()
results = meta.extract_batch("./to_share/")

risky = []
for photo in results:
    if photo.get("gps"):
        risky.append({
            "file": photo["file"]["name"],
            "location": f"{photo['gps']['latitude']}, {photo['gps']['longitude']}"
        })

if risky:
    print(f"Warning: {len(risky)} photos contain location data!")
    for r in risky:
        print(f"  - {r['file']}: {r['location']}")
```

### Travel Photo Map

```python
meta = ImageMetadata()
results = meta.extract_batch("./trip_photos/", recursive=True)

# Generate interactive map
geotagged = [r for r in results if r.get("gps")]
print(f"Found {len(geotagged)} geotagged photos")

meta.generate_map(geotagged, "trip_map.html")
```

## Supported Formats

- JPEG/JPG (full EXIF support)
- TIFF (full EXIF support)
- PNG (limited metadata)
- HEIC/HEIF (iOS photos)
- WebP (limited metadata)
- RAW formats (CR2, NEF, ARW, etc.)

## Dependencies

- pillow>=10.0.0
- folium>=0.14.0 (for map generation)
