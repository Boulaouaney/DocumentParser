"""
CatParser - A blazingly fast, cat-themed document parser 🐱

This package provides high-performance parsing of JSON Lines files
containing document metadata, with a special focus on arXiv papers.
The heavy lifting is done in Rust for maximum speed, with a friendly
Python interface.

Features:
- Blazingly fast parallel processing powered by Rust and Rayon
- Beautiful cat-themed terminal output with colors
- Easy-to-use Python API
- Memory-efficient streaming for large files
- Comprehensive error handling

Example:
    >>> from catparser import CatParser
    >>> parser = CatParser()
    >>> results = parser.parse("arxiv_data.jsonl")
    >>> print(f"Parsed {results['total_articles']} articles!")

    >>> # Or use the quick function
    >>> from catparser import parse_with_whiskers
    >>> results = parse_with_whiskers("arxiv_data.jsonl")
"""

__version__ = "0.1.0"
__author__ = "CatParser Team"

try:
    # Import the Rust extension module
    from catparser.catparser_rust import (
        parse_documents,
        parse_and_display,
        get_cpu_count,
    )
except ImportError as e:
    raise ImportError(
        "Failed to import the Rust extension module. "
        "Make sure you've built the extension with 'maturin develop' or 'pip install -e .'\n"
        f"Error: {e}"
    )


class CatParser:
    """
    A blazingly fast document parser with cat-themed output.

    This class provides a high-level interface to the Rust-powered
    parser with sensible defaults and easy configuration.

    Args:
        chunk_size (int): Number of lines to process in each parallel chunk.
                         Default: 10000
        verbose (bool): Whether to show colorful progress output.
                       Default: True

    Example:
        >>> parser = CatParser(chunk_size=50000, verbose=True)
        >>> results = parser.parse("data.jsonl")
        >>> print(f"Total: {results['total_articles']} articles")
    """

    def __init__(self, chunk_size: int = 10000, verbose: bool = True):
        """Initialize the CatParser with custom settings."""
        self.chunk_size = chunk_size
        self.verbose = verbose

    def parse(self, file_path: str) -> dict:
        """
        Parse a JSON Lines file containing document metadata.

        Args:
            file_path (str): Path to the JSON Lines file to parse

        Returns:
            dict: A dictionary containing:
                - year_counts: Dictionary mapping years to article counts
                - version_counts: Dictionary mapping version counts to article counts
                - total_articles: Total number of successfully parsed articles
                - total_errors: Total number of parsing errors
                - years_range: Tuple of (min_year, max_year) or None

        Raises:
            RuntimeError: If the file cannot be parsed
            FileNotFoundError: If the file doesn't exist

        Example:
            >>> parser = CatParser()
            >>> results = parser.parse("arxiv_data.jsonl")
            >>> print(f"Years: {results['years_range']}")
        """
        return parse_documents(file_path, self.chunk_size, self.verbose)

    def parse_and_display(self, file_path: str) -> dict:
        """
        Parse a file and display pretty results with cat-themed formatting.

        This is a convenience method that parses the file and automatically
        displays beautiful, colorful results with ASCII art cats.

        Args:
            file_path (str): Path to the JSON Lines file to parse

        Returns:
            dict: Same as parse()

        Example:
            >>> parser = CatParser()
            >>> results = parser.parse_and_display("arxiv_data.jsonl")
        """
        return parse_and_display(file_path, self.chunk_size)

    @staticmethod
    def get_optimal_chunk_size(file_lines: int, cpu_count: int = None) -> int:
        """
        Calculate an optimal chunk size based on file size and CPU count.

        Args:
            file_lines (int): Total number of lines in the file
            cpu_count (int, optional): Number of CPUs to use.
                                       If None, uses all available CPUs.

        Returns:
            int: Recommended chunk size

        Example:
            >>> optimal = CatParser.get_optimal_chunk_size(1000000)
            >>> parser = CatParser(chunk_size=optimal)
        """
        if cpu_count is None:
            cpu_count = get_cpu_count()

        # Aim for about 4x CPU count number of chunks for good load balancing
        target_chunks = cpu_count * 4
        chunk_size = max(1000, file_lines // target_chunks)

        return chunk_size


def parse_with_whiskers(
    file_path: str,
    chunk_size: int = 10000,
    verbose: bool = True,
    display: bool = False,
) -> dict:
    """
    Quick function to parse a file with sensible defaults.

    This is a convenience function for one-off parsing tasks.

    Args:
        file_path (str): Path to the JSON Lines file to parse
        chunk_size (int): Number of lines per chunk. Default: 10000
        verbose (bool): Show colorful progress output. Default: True
        display (bool): Display pretty results after parsing. Default: False

    Returns:
        dict: Parsing results dictionary

    Example:
        >>> # Quick parse with output
        >>> results = parse_with_whiskers("data.jsonl", display=True)
        >>>
        >>> # Silent parsing
        >>> results = parse_with_whiskers("data.jsonl", verbose=False)
    """
    if display:
        return parse_and_display(file_path, chunk_size)
    else:
        return parse_documents(file_path, chunk_size, verbose)


def get_system_info() -> dict:
    """
    Get information about the system for performance tuning.

    Returns:
        dict: System information including CPU count

    Example:
        >>> info = get_system_info()
        >>> print(f"CPUs available: {info['cpu_count']}")
    """
    return {
        "cpu_count": get_cpu_count(),
        "recommended_chunk_size": 10000,
    }


# Convenience exports
__all__ = [
    "CatParser",
    "parse_with_whiskers",
    "get_system_info",
    "parse_documents",
    "parse_and_display",
    "get_cpu_count",
]
