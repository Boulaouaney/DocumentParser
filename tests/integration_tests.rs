// Integration tests for the catparser crate
use catparser_rust::{parse_file, ParseResults};
use std::fs::File;
use std::io::Write;
use tempfile::TempDir;

/// Helper function to create a temporary test file
fn create_test_file(contents: &str) -> (TempDir, String) {
    let dir = TempDir::new().unwrap();
    let file_path = dir.path().join("test.jsonl");
    let mut file = File::create(&file_path).unwrap();
    file.write_all(contents.as_bytes()).unwrap();
    (dir, file_path.to_str().unwrap().to_string())
}

#[test]
fn test_parse_valid_documents() {
    let data = r#"{"id":"0704.0001","versions":[{"created":"Mon, 2 Apr 2007 19:18:42 GMT"}]}
{"id":"0704.0002","versions":[{"created":"Mon, 2 Apr 2007 20:24:56 GMT"},{"created":"Tue, 3 Apr 2007 10:15:30 GMT"}]}
{"id":"0801.0001","versions":[{"created":"Tue, 1 Jan 2008 11:22:33 GMT"}]}
"#;

    let (_dir, path) = create_test_file(data);
    let results = parse_file(&path, 1000, false).unwrap();

    assert_eq!(results.total_articles, 3);
    assert_eq!(results.total_errors, 0);
    assert_eq!(results.year_counts.get(&2007), Some(&2));
    assert_eq!(results.year_counts.get(&2008), Some(&1));
    assert_eq!(results.version_counts.get(&1), Some(&2));
    assert_eq!(results.version_counts.get(&2), Some(&1));
    assert_eq!(results.years_range, Some((2007, 2008)));
}

#[test]
fn test_parse_with_errors() {
    let data = r#"{"id":"0704.0001","versions":[{"created":"Mon, 2 Apr 2007 19:18:42 GMT"}]}
{"invalid json"}
{"id":"0704.0002","versions":[]}
{"id":"0704.0003"}
{"id":"0704.0004","versions":[{"created":"Mon, 2 Apr 2007 20:24:56 GMT"}]}
"#;

    let (_dir, path) = create_test_file(data);
    let results = parse_file(&path, 1000, false).unwrap();

    assert_eq!(results.total_articles, 2); // Only 2 valid documents
    assert_eq!(results.total_errors, 3); // 3 invalid documents
    assert_eq!(results.year_counts.get(&2007), Some(&2));
}

#[test]
fn test_parse_empty_file() {
    let data = "";
    let (_dir, path) = create_test_file(data);
    let results = parse_file(&path, 1000, false).unwrap();

    assert_eq!(results.total_articles, 0);
    assert_eq!(results.total_errors, 0);
    assert_eq!(results.years_range, None);
}

#[test]
fn test_parse_multiple_years() {
    let data = r#"{"id":"0001","versions":[{"created":"Mon, 2 Apr 2007 19:18:42 GMT"}]}
{"id":"0002","versions":[{"created":"Tue, 1 Jan 2008 11:22:33 GMT"}]}
{"id":"0003","versions":[{"created":"Thu, 1 Jan 2009 09:30:45 GMT"}]}
{"id":"0004","versions":[{"created":"Fri, 1 Jan 2010 12:00:00 GMT"}]}
{"id":"0005","versions":[{"created":"Mon, 1 Jan 2024 12:00:00 GMT"}]}
"#;

    let (_dir, path) = create_test_file(data);
    let results = parse_file(&path, 1000, false).unwrap();

    assert_eq!(results.total_articles, 5);
    assert_eq!(results.total_errors, 0);
    assert_eq!(results.years_range, Some((2007, 2024)));
    assert_eq!(results.year_counts.len(), 5);
}

#[test]
fn test_parse_multiple_versions() {
    let data = r#"{"id":"0001","versions":[{"created":"Mon, 2 Apr 2007 19:18:42 GMT"}]}
{"id":"0002","versions":[{"created":"Mon, 2 Apr 2007 19:18:42 GMT"},{"created":"Tue, 3 Apr 2007 10:15:30 GMT"}]}
{"id":"0003","versions":[{"created":"Mon, 2 Apr 2007 19:18:42 GMT"},{"created":"Tue, 3 Apr 2007 10:15:30 GMT"},{"created":"Wed, 4 Apr 2007 10:15:30 GMT"}]}
{"id":"0004","versions":[{"created":"Mon, 2 Apr 2007 19:18:42 GMT"},{"created":"Tue, 3 Apr 2007 10:15:30 GMT"},{"created":"Wed, 4 Apr 2007 10:15:30 GMT"},{"created":"Thu, 5 Apr 2007 10:15:30 GMT"}]}
"#;

    let (_dir, path) = create_test_file(data);
    let results = parse_file(&path, 1000, false).unwrap();

    assert_eq!(results.total_articles, 4);
    assert_eq!(results.version_counts.get(&1), Some(&1));
    assert_eq!(results.version_counts.get(&2), Some(&1));
    assert_eq!(results.version_counts.get(&3), Some(&1));
    assert_eq!(results.version_counts.get(&4), Some(&1));
}

#[test]
fn test_parse_with_different_chunk_sizes() {
    let data = (0..100)
        .map(|i| format!(r#"{{"id":"{}","versions":[{{"created":"Mon, {} Apr 2007 19:18:42 GMT"}}]}}"#, i, (i % 28) + 1))
        .collect::<Vec<_>>()
        .join("\n");

    let (_dir, path) = create_test_file(&data);

    // Test with different chunk sizes
    for chunk_size in [1, 10, 50, 100, 1000] {
        let results = parse_file(&path, chunk_size, false).unwrap();
        assert_eq!(results.total_articles, 100, "Failed with chunk_size={}", chunk_size);
        assert_eq!(results.total_errors, 0, "Failed with chunk_size={}", chunk_size);
    }
}

#[test]
fn test_parse_results_merge() {
    let mut results1 = ParseResults::new();
    results1.year_counts.insert(2020, 10);
    results1.year_counts.insert(2021, 5);
    results1.version_counts.insert(1, 8);
    results1.version_counts.insert(2, 7);
    results1.total_articles = 15;
    results1.total_errors = 2;

    let mut results2 = ParseResults::new();
    results2.year_counts.insert(2020, 3);
    results2.year_counts.insert(2022, 8);
    results2.version_counts.insert(1, 5);
    results2.version_counts.insert(3, 6);
    results2.total_articles = 11;
    results2.total_errors = 1;

    results1.merge(results2);

    assert_eq!(results1.year_counts.get(&2020), Some(&13));
    assert_eq!(results1.year_counts.get(&2021), Some(&5));
    assert_eq!(results1.year_counts.get(&2022), Some(&8));
    assert_eq!(results1.version_counts.get(&1), Some(&13));
    assert_eq!(results1.version_counts.get(&2), Some(&7));
    assert_eq!(results1.version_counts.get(&3), Some(&6));
    assert_eq!(results1.total_articles, 26);
    assert_eq!(results1.total_errors, 3);
}

#[test]
fn test_parse_results_finalize() {
    let mut results = ParseResults::new();
    results.year_counts.insert(2020, 10);
    results.year_counts.insert(2018, 5);
    results.year_counts.insert(2023, 8);

    results.finalize();

    assert_eq!(results.years_range, Some((2018, 2023)));
}

#[test]
fn test_large_file_simulation() {
    // Generate a larger dataset
    let lines: Vec<String> = (0..10000)
        .map(|i| {
            let year = 2000 + (i % 25);
            let month = (i % 12) + 1;
            let day = (i % 28) + 1;
            format!(
                r#"{{"id":"{}","versions":[{{"created":"Mon, {} {} {} 19:18:42 GMT"}}]}}"#,
                i, day,
                ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][(month - 1) as usize],
                year
            )
        })
        .collect();

    let data = lines.join("\n");
    let (_dir, path) = create_test_file(&data);
    let results = parse_file(&path, 1000, false).unwrap();

    assert_eq!(results.total_articles, 10000);
    assert_eq!(results.total_errors, 0);
    assert!(results.year_counts.len() > 0);
}

#[test]
fn test_malformed_dates() {
    let data = r#"{"id":"0001","versions":[{"created":"Invalid Date"}]}
{"id":"0002","versions":[{"created":"Mon, 2 Apr 2007 19:18:42 GMT"}]}
{"id":"0003","versions":[{"created":"2007-04-02"}]}
{"id":"0004","versions":[{"created":""}]}
"#;

    let (_dir, path) = create_test_file(data);
    let results = parse_file(&path, 1000, false).unwrap();

    assert_eq!(results.total_articles, 1); // Only one valid document
    assert_eq!(results.total_errors, 3); // Three invalid
}

#[test]
fn test_unicode_content() {
    let data = r#"{"id":"0001","title":"测试文档","versions":[{"created":"Mon, 2 Apr 2007 19:18:42 GMT"}]}
{"id":"0002","title":"Тест документ","versions":[{"created":"Tue, 1 Jan 2008 11:22:33 GMT"}]}
{"id":"0003","title":"🐱 Cat Document","versions":[{"created":"Thu, 1 Jan 2009 09:30:45 GMT"}]}
"#;

    let (_dir, path) = create_test_file(data);
    let results = parse_file(&path, 1000, false).unwrap();

    assert_eq!(results.total_articles, 3);
    assert_eq!(results.total_errors, 0);
}
