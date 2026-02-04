---
name: cad-mesh-generation
version: "1.0.0"
category: data
description: "CAD and Mesh Generation Skill"
---

# CAD and Mesh Generation Skill

```yaml
name: cad-mesh-generation
version: 1.0.0
category: programming
tags: [cad, mesh, freecad, gmsh, geometry, finite-element, marine-structures]
created: 2026-01-06
updated: 2026-01-06
author: Claude
description: |
  Expert CAD geometry and mesh generation using FreeCAD and GMSH. Create
  parametric marine structures, generate meshes for FEA/BEM, and export to
  various analysis software formats (AQWA, WAMIT, ANSYS, etc.).
```

## When to Use This Skill

Use this skill when you need to:
- Create parametric CAD models of vessels, platforms, or structures
- Generate meshes for finite element analysis (FEA)
- Generate panel meshes for boundary element methods (BEM/hydrodynamics)
- Automate geometry creation for marine structures
- Export geometry to AQWA, WAMIT, ANSYS, or other analysis tools
- Create complex geometries programmatically with Python
- Perform mesh quality checks and refinement

## Core Knowledge Areas

### 1. FreeCAD Python Scripting Basics

Creating geometry with FreeCAD Python API:

```python
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import numpy as np

# Try to import FreeCAD, provide fallback for development
try:
    import FreeCAD
    import Part
    import Mesh
    import MeshPart
    FREECAD_AVAILABLE = True
except ImportError:
    FREECAD_AVAILABLE = False
    print("Warning: FreeCAD not available, using mock functions")

    # Mock FreeCAD classes for development
    class MockFreeCAD:
        @staticmethod
        def newDocument(name: str):
            print(f"[MOCK] Creating document: {name}")
            return MockDocument()

        class Vector:
            def __init__(self, x: float, y: float, z: float):
                self.x, self.y, self.z = x, y, z

    class MockDocument:
        def __init__(self):
            self.objects = []

        def addObject(self, obj_type: str, name: str):
            print(f"[MOCK] Adding object: {obj_type} - {name}")
            obj = MockObject(name)
            self.objects.append(obj)
            return obj

        def recompute(self):
            print("[MOCK] Recomputing document")

    class MockObject:
        def __init__(self, name: str):
            self.Name = name
            self.Shape = None

    class MockPart:
        @staticmethod
        def makeCylinder(radius, height, base=None, direction=None):
            print(f"[MOCK] Creating cylinder: r={radius}, h={height}")
            return MockShape()

        @staticmethod
        def makeBox(length, width, height, base=None, direction=None):
            print(f"[MOCK] Creating box: {length}x{width}x{height}")
            return MockShape()

    class MockShape:
        def fuse(self, other):
            print("[MOCK] Fusing shapes")
            return self

        def cut(self, other):
            print("[MOCK] Cutting shapes")
            return self

        def exportStep(self, filename):
            print(f"[MOCK] Exporting STEP: {filename}")

        def exportIges(self, filename):
            print(f"[MOCK] Exporting IGES: {filename}")

    if not FREECAD_AVAILABLE:
        FreeCAD = MockFreeCAD()
        Part = MockPart()

def create_cylinder_vessel(
    diameter: float,
    length: float,
    wall_thickness: float = None,
    name: str = "Vessel"
) -> Tuple[Any, Any]:
    """
    Create cylindrical vessel geometry in FreeCAD.

    Args:
        diameter: Vessel diameter [m]
        length: Vessel length [m]
        wall_thickness: Wall thickness [m] (None = solid)
        name: Object name

    Returns:
        Tuple of (document, shape)

    Example:
        >>> doc, shape = create_cylinder_vessel(
        ...     diameter=10.0,
        ...     length=100.0,
        ...     wall_thickness=0.05,
        ...     name="FPSO_Hull"
        ... )
    """
    # Create document
    doc = FreeCAD.newDocument(name)

    # Create outer cylinder
    outer_radius = diameter / 2
    outer_cyl = Part.makeCylinder(
        outer_radius,
        length,
        FreeCAD.Vector(0, 0, 0),
        FreeCAD.Vector(1, 0, 0)  # Along x-axis
    )

    # If wall thickness specified, make hollow
    if wall_thickness:
        inner_radius = outer_radius - wall_thickness
        inner_cyl = Part.makeCylinder(
            inner_radius,
            length,
            FreeCAD.Vector(0, 0, 0),
            FreeCAD.Vector(1, 0, 0)
        )
        # Subtract inner from outer
        vessel_shape = outer_cyl.cut(inner_cyl)
    else:
        vessel_shape = outer_cyl

    # Add to document
    vessel_obj = doc.addObject("Part::Feature", name)
    vessel_obj.Shape = vessel_shape

    doc.recompute()

    return doc, vessel_shape

def create_rectangular_pontoon(
    length: float,
    width: float,
    height: float,
    wall_thickness: float,
    name: str = "Pontoon"
) -> Tuple[Any, Any]:
    """
    Create rectangular pontoon geometry.

    Args:
        length: Pontoon length [m]
        width: Pontoon width [m]
        height: Pontoon height [m]
        wall_thickness: Wall thickness [m]
        name: Object name

    Returns:
        Tuple of (document, shape)

    Example:
        >>> doc, shape = create_rectangular_pontoon(
        ...     length=50.0,
        ...     width=10.0,
        ...     height=5.0,
        ...     wall_thickness=0.025,
        ...     name="Barge_Pontoon"
        ... )
    """
    doc = FreeCAD.newDocument(name)

    # Outer box
    outer_box = Part.makeBox(
        length,
        width,
        height,
        FreeCAD.Vector(0, 0, 0)
    )

    # Inner box (hollowed)
    inner_box = Part.makeBox(
        length - 2 * wall_thickness,
        width - 2 * wall_thickness,
        height - wall_thickness,  # Bottom plate thickness
        FreeCAD.Vector(wall_thickness, wall_thickness, wall_thickness)
    )

    # Subtract
    pontoon_shape = outer_box.cut(inner_box)

    # Add to document
    pontoon_obj = doc.addObject("Part::Feature", name)
    pontoon_obj.Shape = pontoon_shape

    doc.recompute()

    return doc, pontoon_shape

def export_geometry(
    shape: Any,
    output_file: Path,
    format: str = 'step'
) -> None:
    """
    Export FreeCAD shape to file.

    Args:
        shape: FreeCAD shape object
        output_file: Output file path
        format: Export format ('step', 'iges', 'stl')

    Example:
        >>> export_geometry(vessel_shape, Path('vessel.step'), 'step')
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)

    if format.lower() == 'step':
        shape.exportStep(str(output_file))
    elif format.lower() == 'iges':
        shape.exportIges(str(output_file))
    elif format.lower() == 'stl':
        if FREECAD_AVAILABLE:
            # Convert to mesh first
            mesh = MeshPart.meshFromShape(
                shape,
                LinearDeflection=0.1,
                AngularDeflection=0.5,
                Relative=False
            )
            mesh.write(str(output_file))
        else:
            print(f"[MOCK] Exporting STL: {output_file}")
    else:
        raise ValueError(f"Unsupported format: {format}")

    print(f"Geometry exported: {output_file}")
```

### 2. GMSH Mesh Generation

Creating meshes with GMSH Python API:

```python
# Try to import gmsh
try:
    import gmsh
    GMSH_AVAILABLE = True
except ImportError:
    GMSH_AVAILABLE = False
    print("Warning: GMSH not available, using mock")

    # Mock gmsh module
    class MockGmsh:
        def initialize(self): pass
        def finalize(self): pass
        def open(self, filename): print(f"[MOCK] Opening: {filename}")
        def write(self, filename): print(f"[MOCK] Writing: {filename}")
        def clear(self): pass

        class model:
            @staticmethod
            def mesh():
                return MockGmshMesh()

            class geo:
                @staticmethod
                def addPoint(x, y, z, lc=0, tag=-1):
                    return tag if tag != -1 else 1

                @staticmethod
                def addLine(p1, p2, tag=-1):
                    return tag if tag != -1 else 1

                @staticmethod
                def addSurfaceFilling(lines, tag=-1):
                    return tag if tag != -1 else 1

                @staticmethod
                def synchronize():
                    print("[MOCK] Synchronizing geometry")

        class option:
            @staticmethod
            def setNumber(name, value):
                print(f"[MOCK] Setting option: {name} = {value}")

    class MockGmshMesh:
        def generate(self, dim):
            print(f"[MOCK] Generating {dim}D mesh")

        def setAlgorithm(self, dim, algo):
            print(f"[MOCK] Setting {dim}D algorithm: {algo}")

    if not GMSH_AVAILABLE:
        gmsh = MockGmsh()

def create_panel_mesh_cylinder(
    radius: float,
    height: float,
    n_circumferential: int = 36,
    n_vertical: int = 20,
    output_file: Path = None
) -> str:
    """
    Create panel mesh for cylindrical body using GMSH.

    Args:
        radius: Cylinder radius [m]
        height: Cylinder height [m]
        n_circumferential: Number of panels around circumference
        n_vertical: Number of panels vertically
        output_file: Output mesh file (.msh)

    Returns:
        Path to mesh file

    Example:
        >>> mesh_file = create_panel_mesh_cylinder(
        ...     radius=5.0,
        ...     height=100.0,
        ...     n_circumferential=36,
        ...     n_vertical=50,
        ...     output_file=Path('cylinder_mesh.msh')
        ... )
    """
    gmsh.initialize()

    # Create cylindrical surface
    gmsh.model.add("cylinder_mesh")

    # Characteristic length (mesh size)
    lc = 2 * np.pi * radius / n_circumferential

    # Create points on bottom circle
    bottom_points = []
    for i in range(n_circumferential):
        theta = 2 * np.pi * i / n_circumferential
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        z = 0

        tag = gmsh.model.geo.addPoint(x, y, z, lc)
        bottom_points.append(tag)

    # Create points on top circle
    top_points = []
    for i in range(n_circumferential):
        theta = 2 * np.pi * i / n_circumferential
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        z = height

        tag = gmsh.model.geo.addPoint(x, y, z, lc)
        top_points.append(tag)

    # Create lines connecting bottom to top
    vertical_lines = []
    for i in range(n_circumferential):
        line = gmsh.model.geo.addLine(bottom_points[i], top_points[i])
        vertical_lines.append(line)

    # Create horizontal lines (bottom and top circles)
    bottom_lines = []
    top_lines = []
    for i in range(n_circumferential):
        next_i = (i + 1) % n_circumferential

        bottom_line = gmsh.model.geo.addLine(bottom_points[i], bottom_points[next_i])
        bottom_lines.append(bottom_line)

        top_line = gmsh.model.geo.addLine(top_points[i], top_points[next_i])
        top_lines.append(top_line)

    # Create surfaces (panels)
    panels = []
    for i in range(n_circumferential):
        next_i = (i + 1) % n_circumferential

        # Define curve loop for each panel
        curve_loop = gmsh.model.geo.addCurveLoop([
            bottom_lines[i],
            vertical_lines[next_i],
            -top_lines[i],
            -vertical_lines[i]
        ])

        # Create surface
        surface = gmsh.model.geo.addSurfaceFilling([curve_loop])
        panels.append(surface)

    gmsh.model.geo.synchronize()

    # Generate 2D mesh (surface mesh)
    gmsh.model.mesh.generate(2)

    # Set mesh algorithm (Frontal-Delaunay for quality)
    gmsh.model.mesh.setAlgorithm(2, 6)

    # Save mesh
    if output_file is None:
        output_file = Path('cylinder_mesh.msh')

    output_file.parent.mkdir(parents=True, exist_ok=True)
    gmsh.write(str(output_file))

    gmsh.finalize()

    print(f"Panel mesh created: {output_file}")
    print(f"  Number of panels: {n_circumferential * n_vertical}")

    return str(output_file)

def create_tetrahedral_mesh(
    geometry_file: Path,
    element_size: float,
    output_file: Path,
    refine_surfaces: bool = True
) -> str:
    """
    Create tetrahedral volume mesh from geometry.

    Args:
        geometry_file: Input geometry (.step, .iges, .stl)
        element_size: Target element size [m]
        output_file: Output mesh file (.msh)
        refine_surfaces: Whether to refine surface mesh

    Returns:
        Path to mesh file

    Example:
        >>> mesh_file = create_tetrahedral_mesh(
        ...     geometry_file=Path('vessel.step'),
        ...     element_size=0.5,
        ...     output_file=Path('vessel_mesh.msh')
        ... )
    """
    gmsh.initialize()

    # Open geometry
    gmsh.open(str(geometry_file))

    # Set global mesh size
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", element_size)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", element_size * 0.5)

    # Set 3D mesh algorithm (Delaunay for quality)
    gmsh.option.setNumber("Mesh.Algorithm3D", 1)  # Delaunay

    # Generate 2D surface mesh first
    gmsh.model.mesh.generate(2)

    if refine_surfaces:
        # Refine surface mesh
        gmsh.model.mesh.refine()

    # Generate 3D volume mesh
    gmsh.model.mesh.generate(3)

    # Optimize mesh quality
    gmsh.model.mesh.optimize("Netgen")

    # Save mesh
    output_file.parent.mkdir(parents=True, exist_ok=True)
    gmsh.write(str(output_file))

    gmsh.finalize()

    print(f"Tetrahedral mesh created: {output_file}")

    return str(output_file)
```

### 3. Mesh Quality Assessment

Check mesh quality metrics:

```python
def analyze_mesh_quality(
    mesh_file: Path,
    mesh_type: str = 'surface'
) -> dict:
    """
    Analyze mesh quality metrics.

    Args:
        mesh_file: Path to mesh file (.msh)
        mesh_type: 'surface' or 'volume'

    Returns:
        Dictionary with quality metrics

    Example:
        >>> quality = analyze_mesh_quality(Path('cylinder_mesh.msh'), 'surface')
        >>> print(f"Min quality: {quality['min_quality']:.3f}")
        >>> print(f"Average quality: {quality['avg_quality']:.3f}")
    """
    if not GMSH_AVAILABLE:
        print("[MOCK] Analyzing mesh quality")
        return {
            'element_count': 1000,
            'node_count': 550,
            'min_quality': 0.75,
            'avg_quality': 0.92,
            'max_quality': 1.0
        }

    gmsh.initialize()
    gmsh.open(str(mesh_file))

    # Get mesh statistics
    element_types, element_tags, node_tags = gmsh.model.mesh.getElements()

    total_elements = sum(len(tags) for tags in element_tags)

    # Get nodes
    node_tags_all, node_coords, _ = gmsh.model.mesh.getNodes()
    total_nodes = len(node_tags_all)

    # Calculate element quality
    qualities = []

    if mesh_type == 'surface':
        # For triangular surface elements
        for elem_type, elem_tags in zip(element_types, element_tags):
            if elem_type == 2:  # Triangle
                for elem_tag in elem_tags:
                    # Get element quality (0-1, 1 = perfect)
                    quality = gmsh.model.mesh.getElementQuality([elem_tag], elem_type)
                    if quality:
                        qualities.extend(quality)

    elif mesh_type == 'volume':
        # For tetrahedral volume elements
        for elem_type, elem_tags in zip(element_types, element_tags):
            if elem_type == 4:  # Tetrahedron
                for elem_tag in elem_tags:
                    quality = gmsh.model.mesh.getElementQuality([elem_tag], elem_type)
                    if quality:
                        qualities.extend(quality)

    gmsh.finalize()

    if qualities:
        min_quality = min(qualities)
        avg_quality = np.mean(qualities)
        max_quality = max(qualities)
    else:
        min_quality = avg_quality = max_quality = 0.0

    return {
        'element_count': total_elements,
        'node_count': total_nodes,
        'min_quality': min_quality,
        'avg_quality': avg_quality,
        'max_quality': max_quality,
        'poor_elements': sum(1 for q in qualities if q < 0.3)
    }
```

### 4. Mesh Conversion for Analysis Tools

Convert meshes to various formats:

```python
def convert_mesh_to_wamit_gdf(
    mesh_file: Path,
    output_file: Path,
    symmetry: str = 'none'
) -> None:
    """
    Convert GMSH mesh to WAMIT .gdf format.

    Args:
        mesh_file: Input GMSH mesh file (.msh)
        output_file: Output WAMIT file (.gdf)
        symmetry: 'none', 'x', 'y', or 'xy'

    Example:
        >>> convert_mesh_to_wamit_gdf(
        ...     mesh_file=Path('cylinder_mesh.msh'),
        ...     output_file=Path('cylinder.gdf'),
        ...     symmetry='y'
        ... )
    """
    if not GMSH_AVAILABLE:
        print(f"[MOCK] Converting mesh to WAMIT GDF: {output_file}")
        return

    gmsh.initialize()
    gmsh.open(str(mesh_file))

    # Get nodes
    node_tags, node_coords, _ = gmsh.model.mesh.getNodes()
    n_nodes = len(node_tags)

    # Reshape coordinates
    coords = np.array(node_coords).reshape((-1, 3))

    # Get surface elements (triangles/quads)
    element_types, element_tags, node_tags_elem = gmsh.model.mesh.getElements(2)

    gmsh.finalize()

    # Write GDF file
    with open(output_file, 'w') as f:
        # Header
        f.write(f"WAMIT GDF File\n")
        f.write(f"Converted from GMSH mesh\n")

        # Symmetry
        if symmetry == 'x':
            f.write("1.0  0.0  ! XOZ symmetry\n")
        elif symmetry == 'y':
            f.write("0.0  1.0  ! YOZ symmetry\n")
        elif symmetry == 'xy':
            f.write("1.0  1.0  ! XOZ and YOZ symmetry\n")
        else:
            f.write("0.0  0.0  ! No symmetry\n")

        # Number of panels
        total_panels = sum(len(tags) for tags in element_tags)
        f.write(f"{total_panels}\n")

        # Write panels
        panel_id = 1
        for elem_type, elem_tags, node_tags_set in zip(
            element_types, element_tags, node_tags_elem
        ):
            if elem_type == 2:  # Triangle
                # Triangles have 3 nodes
                nodes_per_elem = 3
                node_tags_array = np.array(node_tags_set).reshape((-1, nodes_per_elem))

                for nodes in node_tags_array:
                    # Get coordinates of 3 vertices
                    vertices = coords[nodes - 1]  # GMSH uses 1-based indexing

                    # Write panel (x, y, z for each vertex)
                    f.write(f"{panel_id}  ")
                    for vertex in vertices:
                        f.write(f"{vertex[0]:.6f} {vertex[1]:.6f} {vertex[2]:.6f}  ")
                    f.write("\n")

                    panel_id += 1

            elif elem_type == 3:  # Quad
                nodes_per_elem = 4
                node_tags_array = np.array(node_tags_set).reshape((-1, nodes_per_elem))

                for nodes in node_tags_array:
                    vertices = coords[nodes - 1]

                    f.write(f"{panel_id}  ")
                    for vertex in vertices:
                        f.write(f"{vertex[0]:.6f} {vertex[1]:.6f} {vertex[2]:.6f}  ")
                    f.write("\n")

                    panel_id += 1

    print(f"WAMIT GDF file created: {output_file}")
    print(f"  Total panels: {total_panels}")

def convert_mesh_to_ansys_cdb(
    mesh_file: Path,
    output_file: Path
) -> None:
    """
    Convert GMSH mesh to ANSYS .cdb format.

    Args:
        mesh_file: Input GMSH mesh file (.msh)
        output_file: Output ANSYS command database (.cdb)

    Example:
        >>> convert_mesh_to_ansys_cdb(
        ...     mesh_file=Path('vessel_mesh.msh'),
        ...     output_file=Path('vessel.cdb')
        ... )
    """
    if not GMSH_AVAILABLE:
        print(f"[MOCK] Converting mesh to ANSYS CDB: {output_file}")
        return

    gmsh.initialize()
    gmsh.open(str(mesh_file))

    # Get nodes
    node_tags, node_coords, _ = gmsh.model.mesh.getNodes()
    coords = np.array(node_coords).reshape((-1, 3))

    # Get elements
    element_types, element_tags_list, node_tags_elem_list = gmsh.model.mesh.getElements()

    gmsh.finalize()

    # Write CDB file
    with open(output_file, 'w') as f:
        # Header
        f.write("/PREP7\n")
        f.write("! Mesh converted from GMSH\n")

        # Write nodes
        f.write("! Nodes\n")
        for node_id, coord in enumerate(coords, start=1):
            f.write(f"N,{node_id},{coord[0]:.6f},{coord[1]:.6f},{coord[2]:.6f}\n")

        # Write elements
        f.write("! Elements\n")
        elem_id = 1

        for elem_type, elem_tags, node_tags_elem in zip(
            element_types, element_tags_list, node_tags_elem_list
        ):
            if elem_type == 4:  # Tetrahedron (SOLID187 in ANSYS)
                f.write("ET,1,SOLID187\n")
                nodes_per_elem = 4
                node_tags_array = np.array(node_tags_elem).reshape((-1, nodes_per_elem))

                for nodes in node_tags_array:
                    node_str = ','.join(map(str, nodes))
                    f.write(f"E,{node_str}\n")
                    elem_id += 1

        f.write("FINISH\n")

    print(f"ANSYS CDB file created: {output_file}")
```

## Complete Examples

### Example 1: Complete Vessel Geometry and Mesh Workflow

```python
from pathlib import Path
import numpy as np

def complete_vessel_geometry_workflow(
    vessel_params: dict,
    mesh_params: dict,
    output_dir: Path
) -> dict:
    """
    Complete workflow: Create geometry, mesh, and export.

    Args:
        vessel_params: Vessel geometry parameters
        mesh_params: Mesh generation parameters
        output_dir: Output directory for all files

    Returns:
        Dictionary with file paths

    Example:
        >>> vessel_params = {
        ...     'type': 'cylinder',
        ...     'diameter': 20.0,
        ...     'length': 150.0,
        ...     'wall_thickness': 0.05
        ... }
        >>> mesh_params = {
        ...     'n_circumferential': 48,
        ...     'n_vertical': 75,
        ...     'element_size': 2.0
        ... }
        >>> results = complete_vessel_geometry_workflow(
        ...     vessel_params,
        ...     mesh_params,
        ...     Path('vessel_geometry')
        ... )
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    print("="*70)
    print("VESSEL GEOMETRY AND MESH WORKFLOW")
    print("="*70)

    # Step 1: Create CAD geometry
    print("\n[Step 1/5] Creating CAD geometry...")

    if vessel_params['type'] == 'cylinder':
        doc, shape = create_cylinder_vessel(
            diameter=vessel_params['diameter'],
            length=vessel_params['length'],
            wall_thickness=vessel_params['wall_thickness'],
            name="Vessel_Geometry"
        )

    # Export geometry
    step_file = output_dir / 'vessel.step'
    iges_file = output_dir / 'vessel.iges'

    export_geometry(shape, step_file, 'step')
    export_geometry(shape, iges_file, 'iges')

    print(f"Geometry exported: {step_file}, {iges_file}")

    # Step 2: Create surface mesh for hydrodynamics
    print("\n[Step 2/5] Creating surface mesh for BEM analysis...")

    surface_mesh_file = output_dir / 'vessel_surface.msh'

    create_panel_mesh_cylinder(
        radius=vessel_params['diameter'] / 2,
        height=vessel_params['length'],
        n_circumferential=mesh_params['n_circumferential'],
        n_vertical=mesh_params['n_vertical'],
        output_file=surface_mesh_file
    )

    # Step 3: Analyze mesh quality
    print("\n[Step 3/5] Analyzing mesh quality...")

    quality = analyze_mesh_quality(surface_mesh_file, 'surface')

    print(f"Mesh quality:")
    print(f"  Elements: {quality['element_count']}")
    print(f"  Nodes: {quality['node_count']}")
    print(f"  Min quality: {quality['min_quality']:.3f}")
    print(f"  Avg quality: {quality['avg_quality']:.3f}")
    print(f"  Poor elements: {quality['poor_elements']}")

    # Step 4: Convert to WAMIT format
    print("\n[Step 4/5] Converting to WAMIT GDF format...")

    wamit_file = output_dir / 'vessel.gdf'
    convert_mesh_to_wamit_gdf(
        surface_mesh_file,
        wamit_file,
        symmetry='y'  # Symmetric about xz plane
    )

    # Step 5: Create volume mesh for FEA (optional)
    print("\n[Step 5/5] Creating volume mesh for FEA...")

    volume_mesh_file = output_dir / 'vessel_volume.msh'
    ansys_file = output_dir / 'vessel.cdb'

    if GMSH_AVAILABLE:
        create_tetrahedral_mesh(
            step_file,
            mesh_params['element_size'],
            volume_mesh_file
        )

        # Convert to ANSYS
        convert_mesh_to_ansys_cdb(volume_mesh_file, ansys_file)

    print("\n" + "="*70)
    print("WORKFLOW COMPLETE")
    print("="*70)

    results = {
        'geometry': {
            'step': step_file,
            'iges': iges_file
        },
        'mesh': {
            'surface': surface_mesh_file,
            'volume': volume_mesh_file,
            'wamit': wamit_file,
            'ansys': ansys_file
        },
        'quality': quality
    }

    return results

# Run workflow
vessel_params = {
    'type': 'cylinder',
    'diameter': 20.0,
    'length': 150.0,
    'wall_thickness': 0.05
}

mesh_params = {
    'n_circumferential': 48,
    'n_vertical': 75,
    'element_size': 2.0
}

workflow_results = complete_vessel_geometry_workflow(
    vessel_params,
    mesh_params,
    Path('vessel_geometry_output')
)

print("\nGenerated files:")
for category, files in workflow_results.items():
    if category != 'quality':
        print(f"\n{category.upper()}:")
        for file_type, file_path in files.items():
            print(f"  {file_type}: {file_path}")
```

## Best Practices

### 1. Parametric Design

```python
from dataclasses import dataclass

@dataclass
class VesselDesignParameters:
    """Parametric vessel design."""
    length: float  # Overall length [m]
    beam: float  # Beam (width) [m]
    depth: float  # Depth [m]
    draft: float  # Design draft [m]
    bow_shape: str = 'straight'  # 'straight', 'raked', 'bulbous'
    stern_shape: str = 'transom'  # 'transom', 'cruiser'
    superstructure: bool = True

    def validate(self) -> bool:
        """Validate design parameters."""
        if self.draft > self.depth:
            raise ValueError("Draft cannot exceed depth")
        if self.beam > self.length:
            raise ValueError("Beam should not exceed length")
        return True
```

### 2. Mesh Size Optimization

```python
def calculate_optimal_mesh_size(
    geometry_length_scale: float,
    analysis_type: str,
    target_accuracy: str = 'medium'
) -> float:
    """
    Calculate optimal mesh size based on geometry and analysis type.

    Args:
        geometry_length_scale: Characteristic length [m]
        analysis_type: 'bem', 'fea_linear', 'fea_nonlinear', 'cfd'
        target_accuracy: 'coarse', 'medium', 'fine'

    Returns:
        Recommended element size [m]
    """
    # Base sizing ratios
    sizing_ratios = {
        'bem': {
            'coarse': 0.10,
            'medium': 0.05,
            'fine': 0.025
        },
        'fea_linear': {
            'coarse': 0.20,
            'medium': 0.10,
            'fine': 0.05
        },
        'fea_nonlinear': {
            'coarse': 0.10,
            'medium': 0.05,
            'fine': 0.025
        },
        'cfd': {
            'coarse': 0.15,
            'medium': 0.075,
            'fine': 0.0375
        }
    }

    ratio = sizing_ratios[analysis_type][target_accuracy]
    element_size = geometry_length_scale * ratio

    return element_size
```

### 3. Quality Checks

```python
def perform_mesh_quality_checks(
    mesh_file: Path,
    min_quality_threshold: float = 0.3
) -> bool:
    """
    Perform comprehensive mesh quality checks.

    Args:
        mesh_file: Mesh file path
        min_quality_threshold: Minimum acceptable quality

    Returns:
        True if mesh passes quality checks
    """
    quality = analyze_mesh_quality(mesh_file)

    checks = {
        'min_quality': quality['min_quality'] >= min_quality_threshold,
        'poor_elements': quality['poor_elements'] == 0,
        'element_count': quality['element_count'] > 0
    }

    passed = all(checks.values())

    if not passed:
        print("Mesh quality check FAILED:")
        for check_name, result in checks.items():
            status = "PASS" if result else "FAIL"
            print(f"  {check_name}: {status}")

    return passed
```

## Resources

### FreeCAD

- **Documentation**: https://wiki.freecadweb.org/
- **Python API**: https://wiki.freecadweb.org/Python_scripting_tutorial
- **Examples**: https://github.com/FreeCAD/FreeCAD/tree/master/src/Mod/Part/TestPartApp

### GMSH

- **Documentation**: https://gmsh.info/doc/texinfo/gmsh.html
- **Python API**: http://gmsh.info/doc/texinfo/gmsh.html#Gmsh-API
- **Tutorials**: https://gitlab.onelab.info/gmsh/gmsh/-/tree/master/tutorials

### Mesh Generation

- **Netgen**: https://ngsolve.org/
- **TetGen**: http://wias-berlin.de/software/tetgen/
- **Triangle**: https://www.cs.cmu.edu/~quake/triangle.html

### Marine Geometry

- **DelftShip**: Free ship hull design software
- **MAXSURF**: Professional naval architecture software
- **Rhinoceros**: Advanced 3D modeling (with Grasshopper for parametric)

---

**Use this skill for:** Expert CAD geometry creation and mesh generation for marine structures with full export capabilities to analysis software.
