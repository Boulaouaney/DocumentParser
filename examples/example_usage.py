#!/usr/bin/env python3
"""
🐱 Example Usage of CatParser

This script shows different ways to use CatParser in your Python code!
"""

from catparser import KittenParser, parse_documents_with_whiskers
from catparser.cat_art import show_cat_banner, get_random_pun
from rich.console import Console

console = Console()


def example_1_quick_parse():
    """Example 1: Quick and easy parsing with the convenience function."""
    console.print("\n[bold cyan]Example 1: Quick Parse 🚀[/bold cyan]\n")

    results = parse_documents_with_whiskers(
        file_path="examples/sample_data.jsonl",
        output_dir="./results",
        num_processes=2,
        create_plots=True,
    )

    console.print(f"\n[green]✓[/green] Processed {results['total_articles']:,} articles!")
    console.print(f"[green]✓[/green] Found {len(results['year_counts'])} unique years")
    console.print(f"[yellow]![/yellow] Had {results['total_errors']:,} errors")


def example_2_class_usage():
    """Example 2: Using the KittenParser class directly."""
    console.print("\n[bold cyan]Example 2: Class-Based Usage 🐱[/bold cyan]\n")

    # Create parser instance
    parser = KittenParser(num_processes=4)

    # Parse documents
    results = parser.parse(
        file_path="examples/sample_data.jsonl",
        output_dir="./results",
        create_plots=False,  # Skip plots this time
    )

    # Access detailed results
    console.print("\n[bold]Year Distribution:[/bold]")
    for year, count in sorted(results["year_counts"].items())[:5]:
        console.print(f"  {year}: {count:,} articles")


def example_3_custom_processing():
    """Example 3: Custom processing of results."""
    console.print("\n[bold cyan]Example 3: Custom Processing 📊[/bold cyan]\n")

    parser = KittenParser(num_processes=2)
    results = parser.parse("examples/sample_data.jsonl", create_plots=False)

    # Find the most productive year
    year_counts = results["year_counts"]
    if year_counts:
        best_year = max(year_counts.items(), key=lambda x: x[1])
        console.print(
            f"\n[bold green]🏆 Most productive year:[/bold green] "
            f"{best_year[0]} with {best_year[1]:,} articles!"
        )

    # Calculate average versions
    version_counts = results["version_counts"]
    if version_counts:
        total_versions = sum(v * c for v, c in version_counts.items())
        total_articles = sum(version_counts.values())
        avg_versions = total_versions / total_articles if total_articles > 0 else 0
        console.print(
            f"[bold blue]📊 Average versions per article:[/bold blue] {avg_versions:.2f}"
        )


def main():
    """Run all examples."""
    show_cat_banner("CatParser Examples", "Learn how to use the purrfect parser! 😺")

    try:
        # Run examples
        example_1_quick_parse()
        example_2_class_usage()
        example_3_custom_processing()

        # Success!
        console.print(f"\n[bold green]✨ All examples completed! {get_random_pun()} ✨[/bold green]\n")

    except FileNotFoundError:
        console.print(
            "\n[yellow]⚠️  Sample data file not found![/yellow]"
        )
        console.print(
            "[dim]Create examples/sample_data.jsonl or use your own data file![/dim]\n"
        )
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]\n")


if __name__ == "__main__":
    main()
