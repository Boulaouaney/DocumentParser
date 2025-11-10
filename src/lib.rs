mod cat_theme;
mod parser;
mod types;

use pyo3::prelude::*;
use pyo3::types::PyDict;

use crate::parser::{display_results, parse_file};
use crate::types::ParseResults;

/// Convert Rust ParseResults to Python dictionary
fn results_to_pydict(py: Python, results: &ParseResults) -> PyResult<PyObject> {
    let dict = PyDict::new(py);

    // Convert year_counts HashMap to Python dict
    let year_counts = PyDict::new(py);
    for (year, count) in &results.year_counts {
        year_counts.set_item(year, count)?;
    }
    dict.set_item("year_counts", year_counts)?;

    // Convert version_counts HashMap to Python dict
    let version_counts = PyDict::new(py);
    for (versions, count) in &results.version_counts {
        version_counts.set_item(versions, count)?;
    }
    dict.set_item("version_counts", version_counts)?;

    dict.set_item("total_articles", results.total_articles)?;
    dict.set_item("total_errors", results.total_errors)?;

    if let Some((min_year, max_year)) = results.years_range {
        dict.set_item("years_range", (min_year, max_year))?;
    } else {
        dict.set_item("years_range", py.None())?;
    }

    Ok(dict.into())
}

/// Parse a JSON Lines file containing arXiv documents
///
/// Args:
///     file_path (str): Path to the JSON Lines file to parse
///     chunk_size (int, optional): Number of lines to process in each chunk. Default: 10000
///     verbose (bool, optional): Whether to print colorful progress messages. Default: True
///
/// Returns:
///     dict: A dictionary containing:
///         - year_counts: Dictionary mapping years to article counts
///         - version_counts: Dictionary mapping version counts to article counts
///         - total_articles: Total number of successfully parsed articles
///         - total_errors: Total number of parsing errors
///         - years_range: Tuple of (min_year, max_year) or None
///
/// Example:
///     >>> import catparser_rust
///     >>> results = catparser_rust.parse_documents("arxiv_data.jsonl")
///     >>> print(f"Total articles: {results['total_articles']}")
#[pyfunction]
#[pyo3(signature = (file_path, chunk_size=10000, verbose=true))]
fn parse_documents(
    py: Python,
    file_path: String,
    chunk_size: usize,
    verbose: bool,
) -> PyResult<PyObject> {
    // Release the GIL while doing heavy computation
    let results = py.allow_threads(|| {
        parse_file(&file_path, chunk_size, verbose)
            .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))
    })?;

    results_to_pydict(py, &results)
}

/// Parse and display results in one go
///
/// This is a convenience function that parses the file and displays
/// the results with pretty cat-themed formatting.
///
/// Args:
///     file_path (str): Path to the JSON Lines file to parse
///     chunk_size (int, optional): Number of lines to process in each chunk. Default: 10000
///
/// Returns:
///     dict: Same as parse_documents()
#[pyfunction]
#[pyo3(signature = (file_path, chunk_size=10000))]
fn parse_and_display(py: Python, file_path: String, chunk_size: usize) -> PyResult<PyObject> {
    let results = py.allow_threads(|| {
        parse_file(&file_path, chunk_size, true)
            .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))
    })?;

    // Display results with cat-themed formatting
    display_results(&results);

    results_to_pydict(py, &results)
}

/// Get the number of available CPU cores
///
/// This can be useful for determining optimal parallelism settings.
///
/// Returns:
///     int: Number of logical CPU cores
#[pyfunction]
fn get_cpu_count() -> usize {
    num_cpus::get()
}

/// CatParser module - A blazingly fast, cat-themed document parser
///
/// This module provides high-performance parsing of JSON Lines files
/// containing document metadata (especially arXiv papers). It uses
/// parallel processing with Rayon for maximum speed and features
/// delightful cat-themed output.
///
/// Functions:
///     parse_documents: Parse a JSON Lines file and return results
///     parse_and_display: Parse and display results with pretty formatting
///     get_cpu_count: Get the number of available CPU cores
///
/// Example:
///     >>> import catparser_rust
///     >>> # Parse with default settings
///     >>> results = catparser_rust.parse_documents("data.jsonl")
///     >>>
///     >>> # Parse with custom chunk size and no output
///     >>> results = catparser_rust.parse_documents("data.jsonl", chunk_size=50000, verbose=False)
///     >>>
///     >>> # Parse and display pretty results
///     >>> results = catparser_rust.parse_and_display("data.jsonl")
#[pymodule]
fn catparser_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse_documents, m)?)?;
    m.add_function(wrap_pyfunction!(parse_and_display, m)?)?;
    m.add_function(wrap_pyfunction!(get_cpu_count, m)?)?;
    Ok(())
}
