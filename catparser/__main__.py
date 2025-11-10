"""
Command-line interface for CatParser
"""

import argparse
import sys
from pathlib import Path

from catparser import CatParser, get_system_info


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="🐱 CatParser - A blazingly fast, cat-themed document parser",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Parse with default settings
  python -m catparser data.jsonl

  # Parse with custom chunk size
  python -m catparser data.jsonl --chunk-size 50000

  # Silent parsing (no output)
  python -m catparser data.jsonl --quiet

  # Show system info
  python -m catparser --info
        """,
    )

    parser.add_argument(
        "file",
        nargs="?",
        type=str,
        help="Path to the JSON Lines file to parse",
    )

    parser.add_argument(
        "--chunk-size",
        type=int,
        default=10000,
        help="Number of lines to process in each chunk (default: 10000)",
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Disable verbose output",
    )

    parser.add_argument(
        "--info",
        action="store_true",
        help="Show system information and exit",
    )

    args = parser.parse_args()

    # Show system info if requested
    if args.info:
        info = get_system_info()
        print("🐱 CatParser System Information")
        print("=" * 40)
        print(f"CPU Cores: {info['cpu_count']}")
        print(f"Recommended Chunk Size: {info['recommended_chunk_size']}")
        return 0

    # Validate file argument
    if not args.file:
        parser.print_help()
        return 1

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"❌ Error: File not found: {file_path}", file=sys.stderr)
        return 1

    # Parse the file
    try:
        cat_parser = CatParser(
            chunk_size=args.chunk_size,
            verbose=not args.quiet,
        )

        results = cat_parser.parse_and_display(str(file_path))

        # Print summary if quiet mode
        if args.quiet:
            print(f"\nTotal articles: {results['total_articles']}")
            print(f"Total errors: {results['total_errors']}")
            if results['years_range']:
                print(f"Years range: {results['years_range'][0]} - {results['years_range'][1]}")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
