use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Represents a version entry in the arXiv document
#[derive(Debug, Deserialize, Serialize)]
pub struct Version {
    pub created: String,
}

/// Represents an arXiv document with its versions
#[derive(Debug, Deserialize, Serialize)]
pub struct ArxivDocument {
    pub versions: Option<Vec<Version>>,
}

/// Results from parsing documents
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ParseResults {
    pub year_counts: HashMap<i32, usize>,
    pub version_counts: HashMap<usize, usize>,
    pub total_articles: usize,
    pub total_errors: usize,
    pub years_range: Option<(i32, i32)>,
}

impl ParseResults {
    pub fn new() -> Self {
        Self {
            year_counts: HashMap::new(),
            version_counts: HashMap::new(),
            total_articles: 0,
            total_errors: 0,
            years_range: None,
        }
    }

    pub fn merge(&mut self, other: ParseResults) {
        for (year, count) in other.year_counts {
            *self.year_counts.entry(year).or_insert(0) += count;
        }
        for (versions, count) in other.version_counts {
            *self.version_counts.entry(versions).or_insert(0) += count;
        }
        self.total_articles += other.total_articles;
        self.total_errors += other.total_errors;
    }

    pub fn finalize(&mut self) {
        if let (Some(&min_year), Some(&max_year)) = (
            self.year_counts.keys().min(),
            self.year_counts.keys().max(),
        ) {
            self.years_range = Some((min_year, max_year));
        }
    }
}

impl Default for ParseResults {
    fn default() -> Self {
        Self::new()
    }
}
