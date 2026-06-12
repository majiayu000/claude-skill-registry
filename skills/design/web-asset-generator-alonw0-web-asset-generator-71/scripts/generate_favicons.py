#!/usr/bin/env python3
"""
Generate favicon and app icon files from a source image or emoji.
Supports standard favicon sizes and PWA icon sizes.
"""

import sys
import argparse
import re
from pathlib import Path
from PIL import Image
import io

# Import emoji utilities
try:
    from emoji_utils import generate_emoji_icon, suggest_emojis, get_emoji_name, PILMOJI_AVAILABLE
except ImportError:
    # If running from different directory, try absolute import
    try:
        import os
        sys.path.insert(0, os.path.dirname(__file__))
        from emoji_utils import generate_emoji_icon, suggest_emojis, get_emoji_name, PILMOJI_AVAILABLE
    except ImportError:
        # Emoji support not available
        generate_emoji_icon = None
        suggest_emojis = None
        get_emoji_name = None
        PILMOJI_AVAILABLE = False

# Import validation utilities
try:
    from lib.validators import validate_file_size, validate_dimensions, validate_format, ValidationResult
except ImportError:
    # If running from a different directory, try alternative import
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from lib.validators import validate_file_size, validate_dimensions, validate_format, ValidationResult
    except ImportError:
        # Validation not available
        validate_file_size = None
        validate_dimensions = None
        validate_format = None
        ValidationResult = None

# Standard favicon sizes
FAVICON_SIZES = {
    'favicon-16x16.png': (16, 16),
    'favicon-32x32.png': (32, 32),
    'favicon-96x96.png': (96, 96),
}

# PWA/App icon sizes
APP_ICON_SIZES = {
    'apple-touch-icon.png': (180, 180),
    'android-chrome-192x192.png': (192, 192),
    'android-chrome-512x512.png': (512, 512),
}

def generate_icons(source_path=None, output_dir=None, icon_types='all', emoji=None, emoji_bg=None, validate=False):
    """
    Generate icon files from a source image or emoji.

    Args:
        source_path: Path to source image (optional if emoji is provided)
        output_dir: Directory to save generated icons
        icon_types: 'favicon', 'app', or 'all'
        emoji: Emoji character to use instead of image (optional)
        emoji_bg: Background color for emoji (hex or color name, optional)
        validate: If True, run validation checks on generated icons (default: False)

    Returns:
        Dictionary with 'files' and optional 'validation_results'
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine if using emoji or image
    if emoji:
        if not generate_emoji_icon:
            raise ImportError(
                "Emoji support requires emoji_utils.py and pilmoji library. "
                "Install pilmoji with: pip install pilmoji"
            )

        # For app icons, use solid background (iOS doesn't support transparency)
        # For favicons, use transparent background unless specified
        needs_solid_bg = (icon_types in ['app', 'all'])

        if needs_solid_bg and not emoji_bg:
            emoji_bg = 'white'  # Default background for app icons

        # Generate a large emoji image that we'll resize
        # Use 512x512 as base size (largest needed)
        base_img = generate_emoji_icon(emoji, (512, 512), emoji_bg)
        img = base_img

        print(f"Using emoji: {emoji} {get_emoji_name(emoji) if get_emoji_name else ''}")

    else:
        # Load from image file
        if not source_path:
            raise ValueError("Either source_path or emoji must be provided")

        source_path = Path(source_path)
        img = Image.open(source_path)
        print(f"Generating icons from {source_path}...")

    # Convert to RGBA if necessary (unless using solid background with emoji)
    if img.mode != 'RGBA' and not (emoji and emoji_bg):
        img = img.convert('RGBA')

    # Determine which sizes to generate
    sizes_to_generate = {}
    if icon_types in ['favicon', 'all']:
        sizes_to_generate.update(FAVICON_SIZES)
    if icon_types in ['app', 'all']:
        sizes_to_generate.update(APP_ICON_SIZES)

    # Generate each size
    generated_files = []
    for filename, size in sizes_to_generate.items():
        # Resize with high-quality resampling
        resized = img.resize(size, Image.Resampling.LANCZOS)

        # Save
        output_path = output_dir / filename
        resized.save(output_path, 'PNG', optimize=True)
        generated_files.append(str(output_path))
        print(f"✓ Generated {filename} ({size[0]}x{size[1]})")

    # Generate .ico file for browsers (contains 16x16 and 32x32)
    if icon_types in ['favicon', 'all']:
        ico_path = output_dir / 'favicon.ico'
        icon_16 = img.resize((16, 16), Image.Resampling.LANCZOS)
        icon_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
        icon_16.save(ico_path, format='ICO', sizes=[(16, 16), (32, 32)])
        generated_files.append(str(ico_path))
        print(f"✓ Generated favicon.ico (16x16, 32x32)")

    result = {'files': generated_files}

    # Run validation if requested
    if validate and generated_files and validate_file_size:
        print("\n" + "=" * 70)
        print("Running validation checks...")
        print("=" * 70)

        validation_results = []

        # Validate PNG files (skip .ico as it has different requirements)
        png_files = [f for f in generated_files if f.endswith('.png')]

        for file_path in png_files:
            filename = Path(file_path).name
            print(f"\n{filename}:")

            # Get actual file size
            import os
            file_size_kb = os.path.getsize(file_path) / 1024

            # Custom validation for favicons and app icons
            if 'favicon' in filename.lower():
                # File size check
                if file_size_kb > 100:
                    size_result = ValidationResult(
                        True,
                        f"  ⚠ File size {file_size_kb:.1f}KB is large for a favicon (recommended <100KB)",
                        'warning'
                    )
                else:
                    size_result = ValidationResult(
                        True,
                        f"  ✓ File size {file_size_kb:.1f}KB is good for a favicon",
                        'success'
                    )

                # Dimension check - just verify it matches expected size from filename
                expected_sizes = {'16': 16, '32': 32, '96': 96}
                size_match = re.search(r'(\d+)x(\d+)', filename)
                if size_match:
                    w, h = int(size_match.group(1)), int(size_match.group(2))
                    if w == h:
                        dim_result = ValidationResult(
                            True,
                            f"  ✓ Dimensions {w}x{h} are correct for favicon",
                            'success'
                        )
                    else:
                        dim_result = ValidationResult(
                            False,
                            f"  ❌ Favicon must be square, got {w}x{h}",
                            'error'
                        )
                else:
                    dim_result = ValidationResult(True, "  ✓ Dimensions OK", 'success')

                # Format check
                fmt_result = ValidationResult(True, "  ✓ Format PNG is correct", 'success')

            else:  # App icon
                # File size check
                if file_size_kb > 500:
                    size_result = ValidationResult(
                        True,
                        f"  ⚠ File size {file_size_kb:.1f}KB is large for an app icon (recommended <500KB)",
                        'warning'
                    )
                else:
                    size_result = ValidationResult(
                        True,
                        f"  ✓ File size {file_size_kb:.1f}KB is good for an app icon",
                        'success'
                    )

                # Dimension check - verify square and correct size
                size_match = re.search(r'(\d+)x(\d+)', filename)
                if size_match:
                    w, h = int(size_match.group(1)), int(size_match.group(2))
                    if w == h:
                        dim_result = ValidationResult(
                            True,
                            f"  ✓ Dimensions {w}x{h} are correct for app icon",
                            'success'
                        )
                    else:
                        dim_result = ValidationResult(
                            False,
                            f"  ❌ App icon must be square, got {w}x{h}",
                            'error'
                        )
                else:
                    dim_result = ValidationResult(True, "  ✓ Dimensions OK", 'success')

                # Format check
                fmt_result = ValidationResult(True, "  ✓ Format PNG is correct", 'success')

            print(f"{size_result}")
            print(f"{dim_result}")
            print(f"{fmt_result}")

            validation_results.append({
                'file': filename,
                'size': size_result,
                'dimensions': dim_result,
                'format': fmt_result
            })

        result['validation_results'] = validation_results

    return result

def generate_html_tags(icon_types='all'):
    """Generate HTML tags for the icons."""
    tags = []
    
    if icon_types in ['favicon', 'all']:
        tags.extend([
            '<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">',
            '<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">',
            '<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png">',
        ])
    
    if icon_types in ['app', 'all']:
        tags.extend([
            '<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">',
            '<link rel="icon" type="image/png" sizes="192x192" href="/android-chrome-192x192.png">',
            '<link rel="icon" type="image/png" sizes="512x512" href="/android-chrome-512x512.png">',
        ])
    
    return '\n'.join(tags)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate favicon and app icon files from a source image or emoji',
        epilog='Examples:\n'
               '  python generate_favicons.py logo.png output/ all\n'
               '  python generate_favicons.py --emoji "🚀" output/ all\n'
               '  python generate_favicons.py --emoji "☕" --emoji-bg "#F5DEB3" output/ favicon\n'
               '  python generate_favicons.py --suggest "coffee shop" output/ all',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Positional arguments
    parser.add_argument('source_image', nargs='?', help='Path to source image file (not needed with --emoji or --suggest)')
    parser.add_argument('output_dir', help='Output directory for generated icons')
    parser.add_argument('icon_type', nargs='?', default='all',
                        choices=['favicon', 'app', 'all'],
                        help="Icon type to generate: 'favicon', 'app', or 'all' (default: all)")

    # Source options (mutually exclusive with source_image)
    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument('--emoji', metavar='EMOJI', help='Emoji character to use (e.g., "🚀")')
    source_group.add_argument('--suggest', metavar='DESCRIPTION',
                              help='Get emoji suggestions based on project description')

    # Optional arguments
    parser.add_argument('--emoji-bg', metavar='COLOR',
                        help='Background color for emoji icons (hex or color name). '
                             'Default: transparent for favicons, white for app icons')
    parser.add_argument('--validate', action='store_true',
                        help='Run validation checks on generated icons (file size, dimensions, format)')

    args = parser.parse_args()

    # Handle emoji suggestions
    if args.suggest:
        if not suggest_emojis:
            print("❌ Error: Emoji suggestion requires emoji_utils.py")
            print("Make sure emoji_utils.py is in the same directory")
            sys.exit(1)

        print(f"🔍 Finding emoji suggestions for: '{args.suggest}'")
        print()

        suggestions = suggest_emojis(args.suggest, count=4)

        print("Here are the top 4 emoji suggestions:")
        print("=" * 70)
        for i, emoji_data in enumerate(suggestions, 1):
            print(f"{i}. {emoji_data['emoji']}  {emoji_data['name']:<25} - {emoji_data['description']}")

        print()
        print("To use one of these emojis, run:")
        print(f"  python generate_favicons.py --emoji \"EMOJI\" {args.output_dir} {args.icon_type}")
        sys.exit(0)

    # Validate input
    if not args.source_image and not args.emoji:
        parser.error("Either source_image or --emoji must be provided")

    # Generate icons
    try:
        result = generate_icons(
            source_path=args.source_image,
            output_dir=args.output_dir,
            icon_types=args.icon_type,
            emoji=args.emoji,
            emoji_bg=args.emoji_bg,
            validate=args.validate
        )

        files = result['files']
        print(f"\n✅ Generated {len(files)} icon files in {args.output_dir}/")

        if not args.validate and validate_file_size:
            print("\n💡 Tip: Use --validate to check file sizes and formats")

        print("\nHTML tags to include in your <head>:")
        print(generate_html_tags(args.icon_type))

    except ImportError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error generating icons: {e}")
        sys.exit(1)
