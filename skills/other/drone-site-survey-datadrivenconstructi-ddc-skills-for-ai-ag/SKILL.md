---
name: "drone-site-survey"
description: "Process drone survey data for construction sites. Generate orthomosaics, DEMs, point clouds, calculate volumes, track progress, and integrate with BIM models for comparison."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🚀", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Drone Site Survey Processing

## Overview

This skill implements drone data processing for construction site monitoring. Process aerial imagery to generate maps, measure volumes, track progress, and compare with design models.

**Capabilities:**
- Orthomosaic generation
- Digital Elevation Model (DEM) creation
- Point cloud processing
- Volume calculations
- Progress monitoring
- BIM comparison
- Stockpile measurement

## Quick Start

```python
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import numpy as np

@dataclass
class DroneImage:
    filename: str
    timestamp: datetime
    latitude: float
    longitude: float
    altitude: float
    heading: float
    pitch: float
    roll: float
    camera_model: str

@dataclass
class PointCloud:
    points: np.ndarray  # Nx3 array
    colors: Optional[np.ndarray] = None  # Nx3 RGB
    normals: Optional[np.ndarray] = None  # Nx3

@dataclass
class VolumeResult:
    volume_m3: float
    area_m2: float
    method: str
    reference_plane: str
    confidence: float

def calculate_volume_simple(point_cloud: PointCloud,
                           reference_z: float = None) -> VolumeResult:
    """Simple volume calculation from point cloud"""
    points = point_cloud.points

    if reference_z is None:
        reference_z = np.min(points[:, 2])

    # Grid-based volume calculation
    x_min, x_max = np.min(points[:, 0]), np.max(points[:, 0])
    y_min, y_max = np.min(points[:, 1]), np.max(points[:, 1])

    grid_size = 0.5  # 50cm grid
    x_bins = np.arange(x_min, x_max + grid_size, grid_size)
    y_bins = np.arange(y_min, y_max + grid_size, grid_size)

    volume = 0
    cell_area = grid_size ** 2

    for i in range(len(x_bins) - 1):
        for j in range(len(y_bins) - 1):
            mask = (
                (points[:, 0] >= x_bins[i]) & (points[:, 0] < x_bins[i + 1]) &
                (points[:, 1] >= y_bins[j]) & (points[:, 1] < y_bins[j + 1])
            )
            cell_points = points[mask]
            if len(cell_points) > 0:
                max_z = np.max(cell_points[:, 2])
                height = max_z - reference_z
                if height > 0:
                    volume += height * cell_area

    area = (x_max - x_min) * (y_max - y_min)

    return VolumeResult(
        volume_m3=volume,
        area_m2=area,
        method='grid_based',
        reference_plane=f'z={reference_z:.2f}',
        confidence=0.9
    )

# Example usage
sample_points = np.random.rand(10000, 3) * [100, 100, 10]  # 100x100m, 10m height
point_cloud = PointCloud(points=sample_points)
result = calculate_volume_simple(point_cloud)
print(f"Volume: {result.volume_m3:.2f} m³, Area: {result.area_m2:.2f} m²")
```

## Comprehensive Drone Survey System

### Image Processing Pipeline

```python
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import numpy as np
from pathlib import Path
import json

@dataclass
class CameraParameters:
    focal_length_mm: float
    sensor_width_mm: float
    sensor_height_mm: float
    image_width_px: int
    image_height_px: int

@dataclass
class GeoReference:
    crs: str  # Coordinate Reference System (e.g., "EPSG:4326")
    origin: Tuple[float, float, float]  # lat, lon, alt
    rotation: Tuple[float, float, float]  # heading, pitch, roll

@dataclass
class SurveyFlight:
    flight_id: str
    date: datetime
    site_name: str
    images: List[DroneImage]
    camera: CameraParameters
    geo_reference: GeoReference
    flight_altitude: float
    overlap_forward: float = 0.8
    overlap_side: float = 0.7
    gsd: float = 0  # Ground Sample Distance (cm/pixel)

    def __post_init__(self):
        if self.gsd == 0 and self.camera:
            # Calculate GSD
            sensor_width = self.camera.sensor_width_mm
            focal_length = self.camera.focal_length_mm
            image_width = self.camera.image_width_px
            altitude = self.flight_altitude

            self.gsd = (altitude * sensor_width) / (focal_length * image_width) * 100  # cm

@dataclass
class ProcessingResult:
    orthomosaic_path: Optional[str] = None
    dem_path: Optional[str] = None
    dsm_path: Optional[str] = None
    point_cloud_path: Optional[str] = None
    report_path: Optional[str] = None
    statistics: Dict = field(default_factory=dict)

class DroneDataProcessor:
    """Process drone survey data"""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def process_survey(self, flight: SurveyFlight,
                      generate_ortho: bool = True,
                      generate_dem: bool = True,
                      generate_pointcloud: bool = True) -> ProcessingResult:
        """Process drone survey data"""
        result = ProcessingResult()
        result.statistics['flight_id'] = flight.flight_id
        result.statistics['image_count'] = len(flight.images)
        result.statistics['gsd_cm'] = flight.gsd
        result.statistics['flight_date'] = flight.date.isoformat()

        # In production, these would call actual photogrammetry libraries
        # like OpenDroneMap, Pix4D API, or custom SfM pipeline

        if generate_ortho:
            result.orthomosaic_path = str(self.output_dir / f"{flight.flight_id}_ortho.tif")
            result.statistics['ortho_resolution'] = flight.gsd

        if generate_dem:
            result.dem_path = str(self.output_dir / f"{flight.flight_id}_dem.tif")
            result.dsm_path = str(self.output_dir / f"{flight.flight_id}_dsm.tif")

        if generate_pointcloud:
            result.point_cloud_path = str(self.output_dir / f"{flight.flight_id}_pointcloud.las")

        # Generate report
        result.report_path = str(self.output_dir / f"{flight.flight_id}_report.json")
        with open(result.report_path, 'w') as f:
            json.dump(result.statistics, f, indent=2)

        return result

    def extract_point_cloud(self, las_path: str) -> PointCloud:
        """Extract point cloud from LAS file"""
        # In production, use laspy or similar
        # Simulated point cloud for demonstration
        n_points = 100000
        points = np.random.rand(n_points, 3) * [100, 100, 20]
        colors = np.random.randint(0, 255, (n_points, 3), dtype=np.uint8)

        return PointCloud(points=points, colors=colors)

    def compare_surveys(self, survey1: ProcessingResult,
                       survey2: ProcessingResult) -> Dict:
        """Compare two surveys for change detection"""
        # Load point clouds
        pc1 = self.extract_point_cloud(survey1.point_cloud_path)
        pc2 = self.extract_point_cloud(survey2.point_cloud_path)

        # Calculate elevation differences
        # In production, use proper point cloud registration and comparison

        comparison = {
            'survey1_date': survey1.statistics.get('flight_date'),
            'survey2_date': survey2.statistics.get('flight_date'),
            'point_count_diff': len(pc2.points) - len(pc1.points),
            'changes_detected': []
        }

        return comparison
```

### Volume Calculation Engine

```python
from scipy.spatial import Delaunay
from scipy.interpolate import griddata
import numpy as np

class VolumeCalculator:
    """Advanced volume calculations from drone data"""

    def __init__(self, point_cloud: PointCloud):
        self.points = point_cloud.points
        self.colors = point_cloud.colors

    def calculate_cut_fill(self, design_surface: np.ndarray,
                          grid_size: float = 0.5) -> Dict:
        """Calculate cut and fill volumes compared to design surface"""
        # Create grid
        x_min, x_max = np.min(self.points[:, 0]), np.max(self.points[:, 0])
        y_min, y_max = np.min(self.points[:, 1]), np.max(self.points[:, 1])

        x_grid = np.arange(x_min, x_max, grid_size)
        y_grid = np.arange(y_min, y_max, grid_size)
        xx, yy = np.meshgrid(x_grid, y_grid)

        # Interpolate actual surface
        actual_z = griddata(
            self.points[:, :2],
            self.points[:, 2],
            (xx, yy),
            method='linear'
        )

        # Interpolate design surface
        design_z = griddata(
            design_surface[:, :2],
            design_surface[:, 2],
            (xx, yy),
            method='linear'
        )

        # Calculate differences
        diff = actual_z - design_z
        cell_area = grid_size ** 2

        cut_volume = np.nansum(diff[diff > 0]) * cell_area
        fill_volume = np.nansum(np.abs(diff[diff < 0])) * cell_area
        net_volume = cut_volume - fill_volume

        return {
            'cut_volume_m3': float(cut_volume),
            'fill_volume_m3': float(fill_volume),
            'net_volume_m3': float(net_volume),
            'balance': 'cut' if net_volume > 0 else 'fill',
            'grid_size_m': grid_size,
            'area_m2': float((x_max - x_min) * (y_max - y_min))
        }

    def calculate_stockpile_volume(self, base_method: str = 'lowest_perimeter') -> VolumeResult:
        """Calculate stockpile volume"""
        # Find boundary points
        from scipy.spatial import ConvexHull
        hull = ConvexHull(self.points[:, :2])
        boundary_points = self.points[hull.vertices]

        if base_method == 'lowest_perimeter':
            reference_z = np.min(boundary_points[:, 2])
        elif base_method == 'average_perimeter':
            reference_z = np.mean(boundary_points[:, 2])
        elif base_method == 'triangulated':
            # Create base triangulation from boundary
            reference_z = np.min(self.points[:, 2])
        else:
            reference_z = np.min(self.points[:, 2])

        # Calculate volume using triangulated surface
        volume = self._triangulated_volume(reference_z)

        hull_area = self._calculate_hull_area(boundary_points[:, :2])

        return VolumeResult(
            volume_m3=volume,
            area_m2=hull_area,
            method='triangulated_' + base_method,
            reference_plane=f'z={reference_z:.2f}',
            confidence=0.95
        )

    def _triangulated_volume(self, reference_z: float) -> float:
        """Calculate volume using Delaunay triangulation"""
        # Create 2D triangulation
        points_2d = self.points[:, :2]
        tri = Delaunay(points_2d)

        volume = 0
        for simplex in tri.simplices:
            # Get triangle vertices
            p1 = self.points[simplex[0]]
            p2 = self.points[simplex[1]]
            p3 = self.points[simplex[2]]

            # Calculate prism volume
            avg_height = (p1[2] + p2[2] + p3[2]) / 3 - reference_z
            if avg_height > 0:
                # Triangle area
                area = 0.5 * abs(
                    (p2[0] - p1[0]) * (p3[1] - p1[1]) -
                    (p3[0] - p1[0]) * (p2[1] - p1[1])
                )
                volume += area * avg_height

        return volume

    def _calculate_hull_area(self, points_2d: np.ndarray) -> float:
        """Calculate area of convex hull"""
        hull = ConvexHull(points_2d)
        return hull.volume  # In 2D, volume is actually area

    def generate_contours(self, interval: float = 1.0) -> List[Dict]:
        """Generate elevation contours"""
        z_min = np.min(self.points[:, 2])
        z_max = np.max(self.points[:, 2])

        contour_levels = np.arange(
            np.floor(z_min / interval) * interval,
            np.ceil(z_max / interval) * interval + interval,
            interval
        )

        contours = []
        for level in contour_levels:
            # In production, use proper contouring algorithm
            contours.append({
                'elevation': float(level),
                'type': 'major' if level % 5 == 0 else 'minor'
            })

        return contours
```

### Progress Monitoring

```python
from datetime import date
from typing import List, Dict

@dataclass
class ProgressPoint:
    date: date
    point_cloud: PointCloud
    orthomosaic_path: str
    annotations: Dict = field(default_factory=dict)

class ConstructionProgressMonitor:
    """Monitor construction progress from drone surveys"""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.surveys: List[ProgressPoint] = []
        self.volume_calculator = None

    def add_survey(self, survey_date: date, point_cloud: PointCloud,
                  orthomosaic_path: str):
        """Add survey for progress tracking"""
        self.surveys.append(ProgressPoint(
            date=survey_date,
            point_cloud=point_cloud,
            orthomosaic_path=orthomosaic_path
        ))
        self.surveys.sort(key=lambda x: x.date)

    def calculate_earthwork_progress(self, design_surface: np.ndarray) -> List[Dict]:
        """Calculate earthwork progress over time"""
        progress = []

        for i, survey in enumerate(self.surveys):
            calc = VolumeCalculator(survey.point_cloud)
            cut_fill = calc.calculate_cut_fill(design_surface)

            progress.append({
                'date': survey.date.isoformat(),
                'survey_index': i + 1,
                'cut_volume_m3': cut_fill['cut_volume_m3'],
                'fill_volume_m3': cut_fill['fill_volume_m3'],
                'net_volume_m3': cut_fill['net_volume_m3']
            })

        # Calculate progress percentages
        if len(progress) > 1:
            initial = progress[0]
            for p in progress[1:]:
                if initial['net_volume_m3'] != 0:
                    p['progress_pct'] = (
                        (initial['net_volume_m3'] - p['net_volume_m3']) /
                        abs(initial['net_volume_m3']) * 100
                    )
                else:
                    p['progress_pct'] = 0

        return progress

    def detect_changes(self, survey1_idx: int, survey2_idx: int,
                      threshold_m: float = 0.5) -> Dict:
        """Detect changes between two surveys"""
        pc1 = self.surveys[survey1_idx].point_cloud
        pc2 = self.surveys[survey2_idx].point_cloud

        # Create grids for comparison
        grid_size = 1.0  # 1m grid

        x_min = min(np.min(pc1.points[:, 0]), np.min(pc2.points[:, 0]))
        x_max = max(np.max(pc1.points[:, 0]), np.max(pc2.points[:, 0]))
        y_min = min(np.min(pc1.points[:, 1]), np.min(pc2.points[:, 1]))
        y_max = max(np.max(pc1.points[:, 1]), np.max(pc2.points[:, 1]))

        x_bins = np.arange(x_min, x_max + grid_size, grid_size)
        y_bins = np.arange(y_min, y_max + grid_size, grid_size)

        changes = {
            'increased': [],  # Areas where elevation increased
            'decreased': [],  # Areas where elevation decreased
            'unchanged': 0
        }

        for i in range(len(x_bins) - 1):
            for j in range(len(y_bins) - 1):
                # Get points in cell for both surveys
                cell_x = (x_bins[i] + x_bins[i + 1]) / 2
                cell_y = (y_bins[j] + y_bins[j + 1]) / 2

                mask1 = (
                    (pc1.points[:, 0] >= x_bins[i]) & (pc1.points[:, 0] < x_bins[i + 1]) &
                    (pc1.points[:, 1] >= y_bins[j]) & (pc1.points[:, 1] < y_bins[j + 1])
                )
                mask2 = (
                    (pc2.points[:, 0] >= x_bins[i]) & (pc2.points[:, 0] < x_bins[i + 1]) &
                    (pc2.points[:, 1] >= y_bins[j]) & (pc2.points[:, 1] < y_bins[j + 1])
                )

                if np.sum(mask1) > 0 and np.sum(mask2) > 0:
                    z1 = np.mean(pc1.points[mask1, 2])
                    z2 = np.mean(pc2.points[mask2, 2])
                    diff = z2 - z1

                    if diff > threshold_m:
                        changes['increased'].append({
                            'x': cell_x, 'y': cell_y, 'change_m': diff
                        })
                    elif diff < -threshold_m:
                        changes['decreased'].append({
                            'x': cell_x, 'y': cell_y, 'change_m': diff
                        })
                    else:
                        changes['unchanged'] += 1

        changes['summary'] = {
            'increased_cells': len(changes['increased']),
            'decreased_cells': len(changes['decreased']),
            'unchanged_cells': changes['unchanged'],
            'date_from': self.surveys[survey1_idx].date.isoformat(),
            'date_to': self.surveys[survey2_idx].date.isoformat()
        }

        return changes

    def generate_progress_report(self, output_path: str,
                                design_surface: np.ndarray = None) -> str:
        """Generate progress report"""
        import pandas as pd

        report_data = {
            'project': self.project_name,
            'surveys': len(self.surveys),
            'date_range': {
                'start': self.surveys[0].date.isoformat() if self.surveys else None,
                'end': self.surveys[-1].date.isoformat() if self.surveys else None
            }
        }

        if design_surface is not None:
            report_data['earthwork_progress'] = self.calculate_earthwork_progress(design_surface)

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            pd.DataFrame([report_data]).to_excel(writer, sheet_name='Summary', index=False)

            # Survey list
            survey_data = [{
                'Date': s.date,
                'Orthomosaic': s.orthomosaic_path
            } for s in self.surveys]
            pd.DataFrame(survey_data).to_excel(writer, sheet_name='Surveys', index=False)

            # Progress (if available)
            if 'earthwork_progress' in report_data:
                pd.DataFrame(report_data['earthwork_progress']).to_excel(
                    writer, sheet_name='Progress', index=False
                )

        return output_path
```

### BIM Comparison

```python
class BIMDroneComparator:
    """Compare drone survey with BIM model"""

    def __init__(self, bim_surface: np.ndarray, drone_pointcloud: PointCloud):
        self.bim = bim_surface
        self.drone = drone_pointcloud

    def compare_elevations(self, grid_size: float = 1.0) -> Dict:
        """Compare drone elevations with BIM design"""
        # Create comparison grid
        x_min = max(np.min(self.bim[:, 0]), np.min(self.drone.points[:, 0]))
        x_max = min(np.max(self.bim[:, 0]), np.max(self.drone.points[:, 0]))
        y_min = max(np.min(self.bim[:, 1]), np.min(self.drone.points[:, 1]))
        y_max = min(np.max(self.bim[:, 1]), np.max(self.drone.points[:, 1]))

        x_grid = np.arange(x_min, x_max, grid_size)
        y_grid = np.arange(y_min, y_max, grid_size)
        xx, yy = np.meshgrid(x_grid, y_grid)

        # Interpolate both surfaces
        bim_z = griddata(self.bim[:, :2], self.bim[:, 2], (xx, yy), method='linear')
        drone_z = griddata(
            self.drone.points[:, :2],
            self.drone.points[:, 2],
            (xx, yy),
            method='linear'
        )

        # Calculate differences
        diff = drone_z - bim_z

        valid_mask = ~np.isnan(diff)
        valid_diff = diff[valid_mask]

        return {
            'mean_diff_m': float(np.mean(valid_diff)),
            'std_diff_m': float(np.std(valid_diff)),
            'max_diff_m': float(np.max(valid_diff)),
            'min_diff_m': float(np.min(valid_diff)),
            'rmse_m': float(np.sqrt(np.mean(valid_diff ** 2))),
            'within_5cm': float(np.sum(np.abs(valid_diff) < 0.05) / len(valid_diff) * 100),
            'within_10cm': float(np.sum(np.abs(valid_diff) < 0.10) / len(valid_diff) * 100),
            'comparison_points': int(len(valid_diff))
        }

    def find_deviations(self, tolerance_m: float = 0.1) -> List[Dict]:
        """Find areas with significant deviations"""
        deviations = []
        grid_size = 1.0

        # Grid comparison
        x_min = max(np.min(self.bim[:, 0]), np.min(self.drone.points[:, 0]))
        x_max = min(np.max(self.bim[:, 0]), np.max(self.drone.points[:, 0]))
        y_min = max(np.min(self.bim[:, 1]), np.min(self.drone.points[:, 1]))
        y_max = min(np.max(self.bim[:, 1]), np.max(self.drone.points[:, 1]))

        for x in np.arange(x_min, x_max, grid_size):
            for y in np.arange(y_min, y_max, grid_size):
                # Get average elevations
                bim_mask = (
                    (self.bim[:, 0] >= x) & (self.bim[:, 0] < x + grid_size) &
                    (self.bim[:, 1] >= y) & (self.bim[:, 1] < y + grid_size)
                )
                drone_mask = (
                    (self.drone.points[:, 0] >= x) & (self.drone.points[:, 0] < x + grid_size) &
                    (self.drone.points[:, 1] >= y) & (self.drone.points[:, 1] < y + grid_size)
                )

                if np.sum(bim_mask) > 0 and np.sum(drone_mask) > 0:
                    bim_z = np.mean(self.bim[bim_mask, 2])
                    drone_z = np.mean(self.drone.points[drone_mask, 2])
                    diff = drone_z - bim_z

                    if abs(diff) > tolerance_m:
                        deviations.append({
                            'x': x + grid_size / 2,
                            'y': y + grid_size / 2,
                            'bim_elevation': bim_z,
                            'actual_elevation': drone_z,
                            'deviation_m': diff,
                            'type': 'high' if diff > 0 else 'low'
                        })

        return deviations
```

## Quick Reference

| Measurement | Method | Accuracy |
|-------------|--------|----------|
| Stockpile Volume | Triangulated | ±2-5% |
| Cut/Fill Volume | Grid comparison | ±5% |
| Area Measurement | Orthomosaic | <1cm GSD |
| Elevation (DEM) | Photogrammetry | ±2-5cm |
| Progress Tracking | Multi-temporal | Relative |

## Resources

- **OpenDroneMap**: https://www.opendronemap.org
- **Pix4D**: https://www.pix4d.com
- **LAStools**: https://rapidlasso.com/lastools/
- **DDC Website**: https://datadrivenconstruction.io

## Next Steps

- See `progress-monitoring-cv` for image-based progress
- See `bim-validation-pipeline` for model comparison
- See `data-visualization` for 3D visualization
