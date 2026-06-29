#!/usr/bin/env python3
"""
Dependency checker for Web Asset Generator.
Verifies that all required and optional dependencies are installed.
"""

import sys

def check_dependencies():
    """Check all dependencies and report status."""
    results = {
        'required': [],
        'optional': [],
        'errors': []
    }

    print("=" * 70)
    print("Web Asset Generator - Dependency Check")
    print("=" * 70)
    print()

    # Check Python version
    print("Python Version:")
    py_version = sys.version_info
    if py_version >= (3, 6):
        print(f"  ✓ Python {py_version.major}.{py_version.minor}.{py_version.micro} (OK)")
        results['required'].append(('Python', True))
    else:
        print(f"  ❌ Python {py_version.major}.{py_version.minor}.{py_version.micro} (Requires 3.6+)")
        results['required'].append(('Python', False))
        results['errors'].append("Python version too old")
    print()

    # Check required dependencies
    print("Required Dependencies:")

    # Pillow
    try:
        from PIL import Image, ImageDraw, ImageFont
        import PIL
        print(f"  ✓ Pillow {PIL.__version__}")
        results['required'].append(('Pillow', True))
    except ImportError as e:
        print(f"  ❌ Pillow (NOT INSTALLED)")
        print(f"     Install with: pip install Pillow")
        results['required'].append(('Pillow', False))
        results['errors'].append("Pillow not installed")
    print()

    # Check optional dependencies
    print("Optional Dependencies (for emoji support):")

    # Pilmoji
    try:
        from pilmoji import Pilmoji
        print(f"  ✓ Pilmoji (OK)")
        results['optional'].append(('Pilmoji', True))
    except ImportError:
        print(f"  ⚠ Pilmoji (NOT INSTALLED)")
        print(f"     Install with: pip install pilmoji")
        results['optional'].append(('Pilmoji', False))
    except AttributeError:
        print(f"  ⚠ Pilmoji (INSTALLED but incompatible)")
        print(f"     Reinstall with: pip install pilmoji")
        results['optional'].append(('Pilmoji', False))

    # Emoji
    try:
        import emoji
        emoji_version = emoji.__version__ if hasattr(emoji, '__version__') else 'unknown'

        # Check version compatibility
        if emoji_version != 'unknown':
            major_version = int(emoji_version.split('.')[0])
            if major_version < 2:
                print(f"  ✓ emoji {emoji_version} (compatible with pilmoji)")
                results['optional'].append(('emoji', True))
            else:
                print(f"  ⚠ emoji {emoji_version} (incompatible with pilmoji)")
                print(f"     Install compatible version: pip install 'emoji<2.0.0'")
                results['optional'].append(('emoji', False))
        else:
            print(f"  ✓ emoji (version unknown)")
            results['optional'].append(('emoji', True))
    except ImportError:
        print(f"  ⚠ emoji (NOT INSTALLED)")
        print(f"     Install with: pip install 'emoji<2.0.0'")
        results['optional'].append(('emoji', False))

    print()

    # Check font availability
    print("Font Availability:")
    import os
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    if os.path.exists(font_path):
        print(f"  ✓ DejaVu Sans Bold found")
    else:
        print(f"  ⚠ DejaVu Sans Bold not found (will use default font)")
        print(f"     On macOS/Windows, this is expected and OK")
    print()

    # Summary
    print("=" * 70)
    print("Summary:")
    print("=" * 70)

    required_ok = all(status for _, status in results['required'])
    optional_ok = all(status for _, status in results['optional'])

    if required_ok:
        print("✓ All required dependencies are installed")
        print("  You can use basic features (image-based generation)")
    else:
        print("❌ Some required dependencies are missing")
        print("  Please install missing dependencies to use the tool")

    print()

    if optional_ok:
        print("✓ All optional dependencies are installed")
        print("  You can use all features including emoji generation")
    else:
        print("⚠ Some optional dependencies are missing")
        print("  Emoji features will not be available")
        print("  Install optional dependencies to enable emoji support")

    print()

    if results['errors']:
        print("Errors to fix:")
        for error in results['errors']:
            print(f"  - {error}")
        print()

    print("=" * 70)

    # Return exit code
    return 0 if required_ok else 1

if __name__ == '__main__':
    exit_code = check_dependencies()
    sys.exit(exit_code)
