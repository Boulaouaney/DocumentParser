"""
🐱 CatParser CLI - Command Line Interface with Maximum Purr-sonality! 🎯

Run your document parsing with style and whiskers!
"""

from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich import print as rprint

from catparser import __version__
from catparser.cat_art import show_cat_banner, get_random_pun, print_cat_separator
from catparser.parser import KittenParser

app = typer.Typer(
    name="catparser",
    help="🐱 CatParser - A purr-fectly fast document parser with whisker-sharp analysis! 🐾",
    add_completion=True,
)
console = Console()


def version_callback(value: bool) -> None:
    """Show version information."""
    if value:
        rprint(f"[bold cyan]🐱 CatParser[/bold cyan] version [yellow]{__version__}[/yellow]")
        rprint(f"[dim]{get_random_pun()}[/dim]")
        raise typer.Exit()


@app.command()
def parse(
    file_path: str = typer.Argument(
        ...,
        help="Path to the JSON lines file to parse (feed me documents! 😺)",
        exists=True,
    ),
    output_dir: str = typer.Option(
        ".",
        "--output",
        "-o",
        help="Output directory for results and plots 📁",
    ),
    num_processes: Optional[int] = typer.Option(
        None,
        "--processes",
        "-p",
        help="Number of CPU cores to use (default: cpu_count // 4) 🐾",
        min=1,
    ),
    no_plots: bool = typer.Option(
        False,
        "--no-plots",
        help="Skip creating visualization plots 🚫",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Quiet mode - less meowing 🤫",
    ),
) -> None:
    """
    Parse a JSON lines document file with the power of a thousand kittens! 🐱⚡

    Examples:

        # Basic usage - let the cats do their magic!
        catparser parse data.jsonl

        # Specify output directory
        catparser parse data.jsonl --output ./results

        # Use more CPU cores (more paws!)
        catparser parse data.jsonl --processes 8

        # Skip plots (boring but faster)
        catparser parse data.jsonl --no-plots

        # Quiet mode (less fun, but professional)
        catparser parse data.jsonl --quiet
    """
    try:
        # Show banner unless quiet mode
        if not quiet:
            show_cat_banner("CatParser", "Whisker-sharp document analysis! 🎯")
            print_cat_separator()

        # Initialize parser
        parser = KittenParser(num_processes=num_processes)

        # Parse documents
        results = parser.parse(
            file_path=file_path,
            output_dir=output_dir,
            create_plots=not no_plots,
        )

        # Show final summary
        if not quiet:
            console.print()
            console.print("[bold green]🎉 Purr-sing complete! All done! 🎉[/bold green]")
            console.print(f"[dim]Processed {results['total_articles']:,} articles[/dim]")

    except FileNotFoundError:
        console.print(
            f"[bold red]😿 Oh no! File not found: {file_path}[/bold red]"
        )
        console.print("[yellow]Make sure the file path is correct and try again![/yellow]")
        raise typer.Exit(code=1)
    except KeyboardInterrupt:
        console.print("\n[yellow]😾 Interrupted by human! Cats don't like that...[/yellow]")
        raise typer.Exit(code=130)
    except Exception as e:
        console.print(f"[bold red]😿 Cat-astrophic error: {e}[/bold red]")
        if not quiet:
            console.print_exception()
        raise typer.Exit(code=1)


@app.command()
def meow() -> None:
    """
    Just meow at you! Because why not? 😸
    """
    meows = [
        "Meow! 😺",
        "Meoooow! 😻",
        "Mew mew! 🐱",
        "Purrrr... 😸",
        "Mrow! 😼",
        "Nya~! 😽",
        "Meow meow meow! 😺😺😺",
    ]
    import random

    show_cat_banner("MEOW", random.choice(meows))


@app.command()
def purrformance(
    file_path: str = typer.Argument(
        ...,
        help="Path to the JSON lines file to benchmark",
        exists=True,
    ),
) -> None:
    """
    Test the purr-formance with different core counts! 🚀

    This will run the parser with 1, 2, 4, and max cores to show
    how scaling works. Great for finding the optimal number of paws!
    """
    import time
    from multiprocessing import cpu_count
    from rich.table import Table

    show_cat_banner("Purrformance Test", "Finding optimal number of paws! 🐾")

    max_cores = cpu_count()
    test_configs = [1, 2, 4, max_cores // 2, max_cores]
    test_configs = sorted(list(set([c for c in test_configs if 0 < c <= max_cores])))

    results_table = Table(title="🚀 Performance Results", border_style="cyan")
    results_table.add_column("Cores (Paws)", style="magenta")
    results_table.add_column("Time", style="yellow")
    results_table.add_column("Speed", style="green")

    baseline_time = None

    for cores in test_configs:
        console.print(f"\n[cyan]Testing with {cores} cores...[/cyan]")

        parser = KittenParser(num_processes=cores)
        start_time = time.time()

        parser.parse(file_path=file_path, create_plots=False)

        elapsed = time.time() - start_time

        if baseline_time is None:
            baseline_time = elapsed
            speedup = "1.00x (baseline)"
        else:
            speedup = f"{baseline_time / elapsed:.2f}x faster!"

        results_table.add_row(
            f"{cores} paws 🐾",
            f"{elapsed:.2f}s",
            speedup,
        )

    console.print()
    console.print(results_table)
    console.print()
    console.print("[bold green]✨ More cores = More paws = More speed! ✨[/bold green]")


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """
    🐱 CatParser - A purr-fectly fast document parser! 🐾

    Parse JSON lines documents with the speed of a cat and the accuracy of... also a cat!
    """
    pass


if __name__ == "__main__":
    app()
