#!/usr/bin/env python3
"""
Basic usage examples for CatParser

This script demonstrates various ways to use the CatParser library.
"""

from catparser import CatParser, parse_with_whiskers, get_system_info


def example_1_basic_parsing():
    """Example 1: Basic parsing with default settings"""
    print("\n" + "=" * 60)
    print("Example 1: Basic Parsing")
    print("=" * 60)

    parser = CatParser()
    results = parser.parse("examples/sample_data.jsonl")

    print(f"\n📚 Total articles parsed: {results['total_articles']}")
    print(f"🤢 Total errors: {results['total_errors']}")
    print(f"📅 Years range: {results['years_range']}")


def example_2_custom_chunk_size():
    """Example 2: Parsing with custom chunk size"""
    print("\n" + "=" * 60)
    print("Example 2: Custom Chunk Size")
    print("=" * 60)

    # Use a smaller chunk size for demonstration
    parser = CatParser(chunk_size=5, verbose=False)
    results = parser.parse("examples/sample_data.jsonl")

    print(f"\n📚 Parsed {results['total_articles']} articles with chunk_size=5")


def example_3_silent_parsing():
    """Example 3: Silent parsing (no output)"""
    print("\n" + "=" * 60)
    print("Example 3: Silent Parsing")
    print("=" * 60)

    parser = CatParser(verbose=False)
    results = parser.parse("examples/sample_data.jsonl")

    print("\n✅ Parsing completed silently!")
    print(f"📊 Results: {results['total_articles']} articles")


def example_4_with_display():
    """Example 4: Parse and display pretty results"""
    print("\n" + "=" * 60)
    print("Example 4: Parse and Display")
    print("=" * 60)

    parser = CatParser(chunk_size=10)
    results = parser.parse_and_display("examples/sample_data.jsonl")


def example_5_convenience_function():
    """Example 5: Using the convenience function"""
    print("\n" + "=" * 60)
    print("Example 5: Convenience Function")
    print("=" * 60)

    # Quick parsing with display
    results = parse_with_whiskers(
        "examples/sample_data.jsonl",
        chunk_size=10,
        verbose=True,
        display=True
    )


def example_6_system_info():
    """Example 6: Get system information"""
    print("\n" + "=" * 60)
    print("Example 6: System Information")
    print("=" * 60)

    info = get_system_info()
    print(f"\n🖥️  CPU cores available: {info['cpu_count']}")
    print(f"💡 Recommended chunk size: {info['recommended_chunk_size']}")


def example_7_analyze_results():
    """Example 7: Analyze parsing results"""
    print("\n" + "=" * 60)
    print("Example 7: Analyzing Results")
    print("=" * 60)

    parser = CatParser(verbose=False)
    results = parser.parse("examples/sample_data.jsonl")

    # Analyze year distribution
    print("\n📅 Year Distribution:")
    sorted_years = sorted(results['year_counts'].items())
    for year, count in sorted_years:
        bar = "█" * count
        print(f"  {year}: {bar} ({count})")

    # Analyze version distribution
    print("\n📝 Version Distribution:")
    sorted_versions = sorted(results['version_counts'].items())
    for versions, count in sorted_versions:
        bar = "█" * count
        print(f"  {versions} version(s): {bar} ({count})")


def main():
    """Run all examples"""
    print("🐱 CatParser Examples")
    print("=" * 60)

    try:
        example_1_basic_parsing()
        example_2_custom_chunk_size()
        example_3_silent_parsing()
        example_4_with_display()
        example_5_convenience_function()
        example_6_system_info()
        example_7_analyze_results()

        print("\n" + "=" * 60)
        print("✨ All examples completed successfully! ✨")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        raise


if __name__ == "__main__":
    main()
