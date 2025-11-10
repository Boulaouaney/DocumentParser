"""
Unit tests for the CatParser Python wrapper
"""

import json
import os
import tempfile
import pytest
from pathlib import Path

# Import the catparser module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from catparser import CatParser, parse_with_whiskers, get_system_info


class TestCatParser:
    """Test suite for CatParser class"""

    @pytest.fixture
    def sample_data_file(self, tmp_path):
        """Create a temporary test file with sample data"""
        test_file = tmp_path / "test_data.jsonl"
        data = [
            {"id": "0001", "versions": [{"created": "Mon, 2 Apr 2007 19:18:42 GMT"}]},
            {"id": "0002", "versions": [{"created": "Tue, 1 Jan 2008 11:22:33 GMT"}]},
            {"id": "0003", "versions": [{"created": "Thu, 1 Jan 2009 09:30:45 GMT"}]},
        ]
        with open(test_file, 'w') as f:
            for item in data:
                f.write(json.dumps(item) + '\n')
        return str(test_file)

    @pytest.fixture
    def empty_file(self, tmp_path):
        """Create an empty test file"""
        test_file = tmp_path / "empty.jsonl"
        test_file.touch()
        return str(test_file)

    @pytest.fixture
    def error_data_file(self, tmp_path):
        """Create a test file with errors"""
        test_file = tmp_path / "error_data.jsonl"
        with open(test_file, 'w') as f:
            f.write('{"id": "0001", "versions": [{"created": "Mon, 2 Apr 2007 19:18:42 GMT"}]}\n')
            f.write('{"invalid json"}\n')
            f.write('{"id": "0002", "versions": []}\n')
            f.write('{"id": "0003", "versions": [{"created": "Tue, 1 Jan 2008 11:22:33 GMT"}]}\n')
        return str(test_file)

    def test_parser_initialization(self):
        """Test CatParser initialization with various settings"""
        # Default settings
        parser1 = CatParser()
        assert parser1.chunk_size == 10000
        assert parser1.verbose is True

        # Custom settings
        parser2 = CatParser(chunk_size=5000, verbose=False)
        assert parser2.chunk_size == 5000
        assert parser2.verbose is False

    def test_parse_valid_data(self, sample_data_file):
        """Test parsing valid data"""
        parser = CatParser(verbose=False)
        results = parser.parse(sample_data_file)

        assert results['total_articles'] == 3
        assert results['total_errors'] == 0
        assert results['years_range'] == (2007, 2009)
        assert 2007 in results['year_counts']
        assert 2008 in results['year_counts']
        assert 2009 in results['year_counts']
        assert results['year_counts'][2007] == 1
        assert results['year_counts'][2008] == 1
        assert results['year_counts'][2009] == 1

    def test_parse_empty_file(self, empty_file):
        """Test parsing an empty file"""
        parser = CatParser(verbose=False)
        results = parser.parse(empty_file)

        assert results['total_articles'] == 0
        assert results['total_errors'] == 0
        assert results['years_range'] is None

    def test_parse_with_errors(self, error_data_file):
        """Test parsing data with errors"""
        parser = CatParser(verbose=False)
        results = parser.parse(error_data_file)

        assert results['total_articles'] == 2  # Only 2 valid documents
        assert results['total_errors'] == 2    # 2 invalid documents

    def test_parse_with_different_chunk_sizes(self, sample_data_file):
        """Test parsing with different chunk sizes"""
        for chunk_size in [1, 2, 3, 10, 100]:
            parser = CatParser(chunk_size=chunk_size, verbose=False)
            results = parser.parse(sample_data_file)
            assert results['total_articles'] == 3

    def test_parse_nonexistent_file(self):
        """Test parsing a nonexistent file raises error"""
        parser = CatParser(verbose=False)
        with pytest.raises(Exception):
            parser.parse("/nonexistent/file.jsonl")

    def test_optimal_chunk_size_calculation(self):
        """Test optimal chunk size calculation"""
        # Test with known values
        chunk_size = CatParser.get_optimal_chunk_size(1000000, cpu_count=4)
        assert chunk_size >= 1000

        # Test that it scales with CPU count
        chunk_size_4 = CatParser.get_optimal_chunk_size(1000000, cpu_count=4)
        chunk_size_8 = CatParser.get_optimal_chunk_size(1000000, cpu_count=8)
        assert chunk_size_4 > chunk_size_8  # More CPUs = smaller chunks

    def test_verbose_mode(self, sample_data_file):
        """Test that verbose mode produces output"""
        # Note: Rust colored output goes directly to terminal,
        # so we just verify the function runs without error
        parser = CatParser(verbose=True)
        results = parser.parse(sample_data_file)
        assert results['total_articles'] == 3

    def test_silent_mode(self, sample_data_file):
        """Test that silent mode runs correctly"""
        parser = CatParser(verbose=False)
        results = parser.parse(sample_data_file)
        assert results['total_articles'] == 3


class TestConvenienceFunctions:
    """Test suite for convenience functions"""

    @pytest.fixture
    def sample_data_file(self, tmp_path):
        """Create a temporary test file"""
        test_file = tmp_path / "test_data.jsonl"
        data = [
            {"id": "0001", "versions": [{"created": "Mon, 2 Apr 2007 19:18:42 GMT"}]},
            {"id": "0002", "versions": [{"created": "Tue, 1 Jan 2008 11:22:33 GMT"}]},
        ]
        with open(test_file, 'w') as f:
            for item in data:
                f.write(json.dumps(item) + '\n')
        return str(test_file)

    def test_parse_with_whiskers(self, sample_data_file):
        """Test parse_with_whiskers convenience function"""
        results = parse_with_whiskers(sample_data_file, verbose=False)

        assert results['total_articles'] == 2
        assert results['total_errors'] == 0

    def test_parse_with_whiskers_display(self, sample_data_file):
        """Test parse_with_whiskers with display option"""
        # Note: Rust colored output goes directly to terminal
        results = parse_with_whiskers(sample_data_file, display=True, chunk_size=10)
        assert results['total_articles'] == 2

    def test_get_system_info(self):
        """Test get_system_info function"""
        info = get_system_info()

        assert 'cpu_count' in info
        assert 'recommended_chunk_size' in info
        assert isinstance(info['cpu_count'], int)
        assert info['cpu_count'] > 0
        assert isinstance(info['recommended_chunk_size'], int)


class TestResultsStructure:
    """Test the structure of returned results"""

    @pytest.fixture
    def sample_results(self, tmp_path):
        """Get sample results"""
        test_file = tmp_path / "test_data.jsonl"
        data = [
            {"id": "0001", "versions": [{"created": "Mon, 2 Apr 2007 19:18:42 GMT"}]},
            {"id": "0002", "versions": [{"created": "Mon, 2 Apr 2007 20:24:56 GMT"},
                                        {"created": "Tue, 3 Apr 2007 10:15:30 GMT"}]},
            {"id": "0003", "versions": [{"created": "Tue, 1 Jan 2008 11:22:33 GMT"}]},
        ]
        with open(test_file, 'w') as f:
            for item in data:
                f.write(json.dumps(item) + '\n')

        parser = CatParser(verbose=False)
        return parser.parse(str(test_file))

    def test_results_has_required_keys(self, sample_results):
        """Test that results have all required keys"""
        required_keys = ['year_counts', 'version_counts', 'total_articles',
                        'total_errors', 'years_range']
        for key in required_keys:
            assert key in sample_results

    def test_year_counts_structure(self, sample_results):
        """Test year_counts structure"""
        year_counts = sample_results['year_counts']
        assert isinstance(year_counts, dict)
        for year, count in year_counts.items():
            assert isinstance(year, int)
            assert isinstance(count, int)
            assert count > 0

    def test_version_counts_structure(self, sample_results):
        """Test version_counts structure"""
        version_counts = sample_results['version_counts']
        assert isinstance(version_counts, dict)
        for versions, count in version_counts.items():
            assert isinstance(versions, int)
            assert isinstance(count, int)
            assert count > 0
            assert versions > 0

    def test_years_range_structure(self, sample_results):
        """Test years_range structure"""
        years_range = sample_results['years_range']
        assert isinstance(years_range, tuple)
        assert len(years_range) == 2
        assert years_range[0] <= years_range[1]


class TestRealWorldScenarios:
    """Test real-world usage scenarios"""

    def test_large_dataset(self, tmp_path):
        """Test with a larger dataset"""
        test_file = tmp_path / "large_data.jsonl"

        # Generate 1000 documents
        with open(test_file, 'w') as f:
            for i in range(1000):
                year = 2000 + (i % 25)
                month = (i % 12) + 1
                day = (i % 28) + 1
                months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

                doc = {
                    "id": f"doc{i:04d}",
                    "versions": [{
                        "created": f"Mon, {day} {months[month-1]} {year} 12:00:00 GMT"
                    }]
                }
                f.write(json.dumps(doc) + '\n')

        parser = CatParser(chunk_size=100, verbose=False)
        results = parser.parse(str(test_file))

        assert results['total_articles'] == 1000
        assert results['total_errors'] == 0
        assert len(results['year_counts']) > 0

    def test_mixed_valid_invalid_data(self, tmp_path):
        """Test with mixed valid and invalid data"""
        test_file = tmp_path / "mixed_data.jsonl"

        with open(test_file, 'w') as f:
            # Valid
            f.write('{"id": "0001", "versions": [{"created": "Mon, 2 Apr 2007 19:18:42 GMT"}]}\n')
            # Invalid JSON
            f.write('not valid json\n')
            # Missing versions
            f.write('{"id": "0002"}\n')
            # Valid
            f.write('{"id": "0003", "versions": [{"created": "Tue, 1 Jan 2008 11:22:33 GMT"}]}\n')
            # Empty versions
            f.write('{"id": "0004", "versions": []}\n')
            # Valid
            f.write('{"id": "0005", "versions": [{"created": "Thu, 1 Jan 2009 09:30:45 GMT"}]}\n')

        parser = CatParser(verbose=False)
        results = parser.parse(str(test_file))

        assert results['total_articles'] == 3
        assert results['total_errors'] == 3

    def test_unicode_handling(self, tmp_path):
        """Test handling of unicode in documents"""
        test_file = tmp_path / "unicode_data.jsonl"

        data = [
            {"id": "0001", "title": "测试文档", "versions": [{"created": "Mon, 2 Apr 2007 19:18:42 GMT"}]},
            {"id": "0002", "title": "Тест документ", "versions": [{"created": "Tue, 1 Jan 2008 11:22:33 GMT"}]},
            {"id": "0003", "title": "🐱 Cat Doc", "versions": [{"created": "Thu, 1 Jan 2009 09:30:45 GMT"}]},
        ]

        with open(test_file, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

        parser = CatParser(verbose=False)
        results = parser.parse(str(test_file))

        assert results['total_articles'] == 3
        assert results['total_errors'] == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
