use crate::cat_theme::*;
use crate::types::{ArxivDocument, ParseResults};
use anyhow::{Context, Result};
use chrono::{Datelike, NaiveDateTime};
use colored::*;
use rayon::prelude::*;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use std::time::Instant;

/// Parse a single line of JSON and extract year and version count
fn parse_line(line: &str) -> Result<(i32, usize), Box<dyn std::error::Error + Send + Sync>> {
    let doc: ArxivDocument = serde_json::from_str(line)?;

    if let Some(versions) = &doc.versions {
        if let Some(first_version) = versions.first() {
            // Parse date format: "Mon, DD MMM YYYY HH:MM:SS TZ"
            // Example: "Mon, 2 Apr 2007 19:18:42 GMT"
            let date_str = &first_version.created;

            // Try parsing with timezone
            let year = if let Ok(dt) = NaiveDateTime::parse_from_str(date_str, "%a, %d %b %Y %H:%M:%S %Z") {
                dt.year()
            } else if let Ok(dt) = NaiveDateTime::parse_from_str(date_str, "%a, %d %b %Y %H:%M:%S GMT") {
                dt.year()
            } else {
                // Fallback: try to extract year manually
                let parts: Vec<&str> = date_str.split_whitespace().collect();
                if parts.len() >= 4 {
                    parts[3].parse::<i32>()?
                } else {
                    return Err("Could not parse date".into());
                }
            };

            let version_count = versions.len();
            return Ok((year, version_count));
        }
    }

    Err("No versions found".into())
}

/// Process a chunk of lines in parallel
fn process_chunk(lines: &[String]) -> ParseResults {
    let results: Vec<_> = lines
        .par_iter()
        .map(|line| parse_line(line))
        .collect();

    let mut parse_results = ParseResults::new();

    for result in results {
        match result {
            Ok((year, version_count)) => {
                *parse_results.year_counts.entry(year).or_insert(0) += 1;
                *parse_results.version_counts.entry(version_count).or_insert(0) += 1;
                parse_results.total_articles += 1;
            }
            Err(_) => {
                parse_results.total_errors += 1;
            }
        }
    }

    parse_results
}

/// Main parsing function with progress indication
pub fn parse_file<P: AsRef<Path>>(
    path: P,
    chunk_size: usize,
    verbose: bool,
) -> Result<ParseResults> {
    let path = path.as_ref();

    if verbose {
        print_banner();
        print_random_pun();
        print_cat_message(CAT_WORKING, "Starting paw-some parsing...", Color::Cyan);
    }

    let start_time = Instant::now();

    // Open and read file
    let file = File::open(path)
        .with_context(|| format!("Failed to open file: {}", path.display()))?;
    let reader = BufReader::new(file);

    if verbose {
        print_progress(&format!("Reading file: {}", path.display()));
    }

    // Read all lines into memory (for small to medium files)
    // For very large files, we could process in streaming chunks
    let lines: Vec<String> = reader
        .lines()
        .filter_map(|line| line.ok())
        .collect();

    let total_lines = lines.len();

    if verbose {
        print_progress(&format!("Loaded {} lines into memory", total_lines));
        print_progress("Engaging parallel purr-ocessing with Rayon...");
    }

    // Process in chunks using parallel processing
    let chunks: Vec<_> = lines.chunks(chunk_size).collect();
    let num_chunks = chunks.len();

    if verbose {
        print_progress(&format!(
            "Processing {} chunks with chunk size {}",
            num_chunks, chunk_size
        ));
    }

    // Atomic counter for progress tracking
    let processed = Arc::new(AtomicUsize::new(0));

    // Process chunks in parallel
    let results: Vec<ParseResults> = chunks
        .par_iter()
        .map(|chunk| {
            let result = process_chunk(chunk);

            if verbose {
                let current = processed.fetch_add(1, Ordering::Relaxed) + 1;
                if current % 10 == 0 || current == num_chunks {
                    let progress = (current as f64 / num_chunks as f64) * 100.0;
                    print_progress(&format!(
                        "Progress: {}/{} chunks ({:.1}%)",
                        current, num_chunks, progress
                    ));
                }
            }

            result
        })
        .collect();

    // Merge all results
    if verbose {
        print_progress("Merging results from all cat workers...");
    }

    let mut final_results = ParseResults::new();
    for result in results {
        final_results.merge(result);
    }

    final_results.finalize();

    let elapsed = start_time.elapsed().as_secs_f64();

    if verbose {
        print_results_summary(
            final_results.total_articles,
            final_results.total_errors,
            final_results.years_range,
            elapsed,
        );
    }

    Ok(final_results)
}

/// Get top N items from year counts
pub fn get_top_years(results: &ParseResults, limit: usize) -> Vec<(String, usize)> {
    let mut items: Vec<_> = results
        .year_counts
        .iter()
        .map(|(year, count)| (year.to_string(), *count))
        .collect();
    items.sort_by(|a, b| b.1.cmp(&a.1));
    items.into_iter().take(limit).collect()
}

/// Get version distribution
pub fn get_version_distribution(results: &ParseResults, limit: usize) -> Vec<(String, usize)> {
    let mut items: Vec<_> = results
        .version_counts
        .iter()
        .map(|(versions, count)| (format!("{} version(s)", versions), *count))
        .collect();
    items.sort_by(|a, b| b.1.cmp(&a.1));
    items.into_iter().take(limit).collect()
}

/// Display results in a pretty format
pub fn display_results(results: &ParseResults) {
    // Top years
    let top_years = get_top_years(results, 10);
    print_top_items("📅 Top 10 Years by Article Count", &top_years, 10);

    // Version distribution
    let version_dist = get_version_distribution(results, 10);
    print_top_items("📝 Top 10 Version Distributions", &version_dist, 10);

    print_divider();
    print_success("✨ Purr-fectly done! ✨");
    println!("{}", CAT_CELEBRATING.bright_green());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_line() {
        let line = r#"{"versions":[{"created":"Mon, 2 Apr 2007 19:18:42 GMT"}]}"#;
        let result = parse_line(line);
        assert!(result.is_ok());
        let (year, version_count) = result.unwrap();
        assert_eq!(year, 2007);
        assert_eq!(version_count, 1);
    }

    #[test]
    fn test_parse_results_merge() {
        let mut results1 = ParseResults::new();
        results1.year_counts.insert(2020, 10);
        results1.total_articles = 10;

        let mut results2 = ParseResults::new();
        results2.year_counts.insert(2020, 5);
        results2.year_counts.insert(2021, 8);
        results2.total_articles = 13;

        results1.merge(results2);

        assert_eq!(results1.year_counts.get(&2020), Some(&15));
        assert_eq!(results1.year_counts.get(&2021), Some(&8));
        assert_eq!(results1.total_articles, 23);
    }
}
