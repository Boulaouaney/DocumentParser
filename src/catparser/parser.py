"""
🐱 KittenParser - The Core Parsing Engine 🚀

Fast, efficient, and adorably themed document parsing with multiprocessing!
"""

import json
from collections import Counter
from datetime import datetime
from multiprocessing import Pool, cpu_count
from pathlib import Path
from typing import Dict, List, Tuple, Generator, Any
from functools import partial

from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
    TimeElapsedColumn,
)
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
import matplotlib.pyplot as plt

from catparser.cat_art import (
    get_random_pun,
    get_random_activity,
    show_success_cat,
    show_error_cat,
    print_cat_separator,
)

console = Console()


class KittenParser:
    """
    🐱 KittenParser - Purr-fectly fast document parser!

    This parser has nine lives worth of efficiency and lands on its feet every time!
    """

    def __init__(self, num_processes: int = None):
        """
        Initialize the KittenParser.

        Args:
            num_processes: Number of CPU cores to use. Defaults to cpu_count() // 4.
                          We leave some cores free so your cat videos can still play smoothly! 🎬
        """
        self.num_processes = num_processes or max(1, cpu_count() // 4)
        self.console = Console()

    def _process_chunk(self, lines: List[str]) -> Tuple[Counter, Counter, int, List[str]]:
        """
        Process a chunk of JSON lines with the precision of a cat hunting a laser pointer! 🔴

        Args:
            lines: List of JSON strings to process

        Returns:
            Tuple of (year_counter, version_counter, error_count, error_samples)
        """
        year_counter = Counter()
        version_counter = Counter()
        error_count = 0
        error_samples = []

        for line in lines:
            try:
                arxiv_file = json.loads(line)

                # Extract creation year like a cat extracts treats from a puzzle toy! 🧩
                if arxiv_file.get("versions") and len(arxiv_file["versions"]) > 0:
                    create_date_str = arxiv_file["versions"][0]["created"]
                    create_date = datetime.strptime(
                        create_date_str, "%a, %d %b %Y %H:%M:%S %Z"
                    )
                    year_counter[create_date.year] += 1
                    version_counter[len(arxiv_file["versions"])] += 1

            except Exception as e:
                error_count += 1
                if len(error_samples) < 5:  # Keep first 5 errors
                    error_samples.append(f"{str(e)[:100]}...")

        return year_counter, version_counter, error_count, error_samples

    def _read_in_chunks(
        self, file_path: Path, chunk_size: int = 50000
    ) -> Generator[List[str], None, None]:
        """
        Read file in chunks like a cat nibbling food throughout the day! 🍽️

        Args:
            file_path: Path to the file to read
            chunk_size: Number of lines per chunk

        Yields:
            Chunks of lines
        """
        with open(file_path, "r", encoding="utf-8") as f:
            chunk = []
            for line in f:
                chunk.append(line)
                if len(chunk) >= chunk_size:
                    yield chunk
                    chunk = []
            if chunk:
                yield chunk

    def parse(
        self, file_path: str, output_dir: str = ".", create_plots: bool = True
    ) -> Dict[str, Any]:
        """
        Parse documents with the grace and efficiency of a leaping cat! 🐈

        Args:
            file_path: Path to the JSON lines file
            output_dir: Directory to save output files
            create_plots: Whether to create visualization plots

        Returns:
            Dictionary with parsing results
        """
        file_path_obj = Path(file_path)
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True, parents=True)

        # Show working cat
        console.print(f"\n[bold cyan]🐱 {get_random_activity()}[/bold cyan]\n")

        # Display config
        config_table = Table(title="🐾 Parsing Configuration", border_style="cyan")
        config_table.add_column("Setting", style="magenta")
        config_table.add_column("Value", style="yellow")
        config_table.add_row("File", str(file_path_obj.name))
        config_table.add_row("CPU Cores (Paws)", str(self.num_processes))
        config_table.add_row("Output Directory", str(output_path))
        console.print(config_table)
        console.print()

        # Process with progress bar
        with Progress(
            SpinnerColumn(spinner_name="pong", style="cyan"),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(complete_style="cyan", finished_style="green"),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=console,
        ) as progress:

            # Count total chunks for progress tracking
            console.print("[dim]Counting chunks... (like counting sheep, but for cats!)[/dim]")
            chunks = list(self._read_in_chunks(file_path_obj))
            total_chunks = len(chunks)

            task = progress.add_task(
                f"[cyan]😸 Parsing documents with whiskers...", total=total_chunks
            )

            # Process chunks with multiprocessing
            with Pool(processes=self.num_processes) as pool:
                results = []
                for result in pool.imap_unordered(self._process_chunk, chunks, chunksize=1):
                    results.append(result)
                    progress.update(task, advance=1)

        # Aggregate results like a cat collecting all the toys! 🧸
        console.print(f"\n[bold cyan]😺 Aggregating results...[/bold cyan]")

        year_counts = Counter()
        version_counts = Counter()
        total_errors = 0
        all_error_samples = []

        for year_counter, version_counter, error_count, error_samples in results:
            year_counts.update(year_counter)
            version_counts.update(version_counter)
            total_errors += error_count
            all_error_samples.extend(error_samples)

        total_articles = sum(year_counts.values())

        # Display results
        self._display_results(year_counts, version_counts, total_articles, total_errors)

        # Create visualizations if requested
        if create_plots:
            console.print(f"\n[bold cyan]🎨 Creating purr-ty visualizations...[/bold cyan]")
            self._create_plots(
                year_counts, version_counts, output_path, total_articles
            )

        # Show success!
        print_cat_separator()
        show_success_cat()

        return {
            "total_articles": total_articles,
            "year_counts": dict(year_counts),
            "version_counts": dict(version_counts),
            "total_errors": total_errors,
            "error_samples": all_error_samples[:10],
        }

    def _display_results(
        self,
        year_counts: Counter,
        version_counts: Counter,
        total_articles: int,
        total_errors: int,
    ) -> None:
        """Display parsing results in a beautiful table."""
        print_cat_separator()

        # Summary table
        summary = Table(title="🐱 Parsing Summary", border_style="green")
        summary.add_column("Metric", style="cyan")
        summary.add_column("Value", style="yellow", justify="right")

        summary.add_row("Total Articles Processed", f"{total_articles:,}")
        summary.add_row("Total Errors (Hairballs)", f"{total_errors:,}")
        summary.add_row(
            "Success Rate", f"{((total_articles / (total_articles + total_errors)) * 100):.2f}%"
        )
        summary.add_row("Years Covered", f"{len(year_counts)}")
        summary.add_row("Version Range", f"1 to {max(version_counts.keys())}")

        console.print(summary)
        console.print()

        # Top years table
        top_years_table = Table(
            title="📅 Top Years (Most Active Catnip Years!)", border_style="magenta"
        )
        top_years_table.add_column("Year", style="cyan")
        top_years_table.add_column("Articles", style="yellow", justify="right")
        top_years_table.add_column("Percentage", style="green", justify="right")

        for year, count in year_counts.most_common(10):
            percentage = (count / total_articles) * 100
            top_years_table.add_row(str(year), f"{count:,}", f"{percentage:.2f}%")

        console.print(top_years_table)
        console.print()

    def _create_plots(
        self, year_counts: Counter, version_counts: Counter, output_path: Path, total_articles: int
    ) -> None:
        """Create visualization plots with style! 📊"""

        # Set up matplotlib with a nice style
        plt.style.use("seaborn-v0_8-darkgrid" if "seaborn-v0_8-darkgrid" in plt.style.available else "default")

        # Filter version counts (exclude rare versions)
        threshold = total_articles * 0.001
        filtered_versions = {v: c for v, c in version_counts.items() if c >= threshold}

        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        fig.suptitle("🐱 CatParser Analysis Results 🐾", fontsize=16, fontweight="bold")

        # Plot 1: Articles by Year
        years = sorted(year_counts.keys())
        counts = [year_counts[year] for year in years]

        ax1.bar(years, counts, color="skyblue", edgecolor="navy", alpha=0.7)
        ax1.set_xlabel("Year", fontsize=12)
        ax1.set_ylabel("Number of Articles", fontsize=12)
        ax1.set_title("📅 Articles Published Per Year (Purr Year!)", fontsize=14, pad=10)
        ax1.grid(axis="y", alpha=0.3)
        ax1.tick_params(axis="x", rotation=45)

        # Plot 2: Version Distribution
        versions = sorted(filtered_versions.keys())
        v_counts = [filtered_versions[v] for v in versions]

        ax2.bar(versions, v_counts, color="lightcoral", edgecolor="darkred", alpha=0.7)
        ax2.set_xlabel("Number of Versions", fontsize=12)
        ax2.set_ylabel("Number of Articles", fontsize=12)
        ax2.set_title(
            "🔄 Article Version Distribution (Nine Lives Edition!)", fontsize=14, pad=10
        )
        ax2.grid(axis="y", alpha=0.3)

        plt.tight_layout()

        # Save plot
        plot_path = output_path / "catparser_analysis.png"
        plt.savefig(plot_path, dpi=300, bbox_inches="tight")
        console.print(f"[green]✓[/green] Saved plot to: [cyan]{plot_path}[/cyan]")

        plt.close()


def parse_documents_with_whiskers(
    file_path: str,
    output_dir: str = ".",
    num_processes: int = None,
    create_plots: bool = True,
) -> Dict[str, Any]:
    """
    Convenience function to parse documents with maximum cuteness! 😻

    Args:
        file_path: Path to JSON lines file
        output_dir: Output directory for results
        num_processes: Number of CPU cores to use
        create_plots: Whether to create visualization plots

    Returns:
        Dictionary with parsing results
    """
    parser = KittenParser(num_processes=num_processes)
    return parser.parse(file_path, output_dir=output_dir, create_plots=create_plots)
