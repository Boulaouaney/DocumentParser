"""
🐱 Tests for CatParser

Making sure our cats are behaving properly!
"""

import json
import tempfile
from pathlib import Path
from datetime import datetime

import pytest

from catparser import KittenParser, parse_documents_with_whiskers
from catparser.cat_art import get_random_pun, get_cat_emotion, CAT_EMOTIONS


class TestCatArt:
    """Test cat ASCII art and decorations."""

    def test_get_random_pun(self):
        """Test that we get a pun."""
        pun = get_random_pun()
        assert isinstance(pun, str)
        assert len(pun) > 0

    def test_get_cat_emotion(self):
        """Test cat emotion retrieval."""
        for emotion in ["happy", "working", "excited", "sleeping", "default"]:
            cat = get_cat_emotion(emotion)
            assert isinstance(cat, str)
            assert len(cat) > 0

    def test_cat_emotions_dict(self):
        """Test CAT_EMOTIONS dictionary."""
        assert "happy" in CAT_EMOTIONS
        assert "working" in CAT_EMOTIONS
        assert "default" in CAT_EMOTIONS


class TestKittenParser:
    """Test the main KittenParser class."""

    @pytest.fixture
    def sample_data_file(self):
        """Create a temporary sample data file."""
        data = [
            {
                "id": "test.0001",
                "title": "Test Article 1",
                "versions": [{"version": "v1", "created": "Mon, 1 Jan 2020 10:00:00 GMT"}],
            },
            {
                "id": "test.0002",
                "title": "Test Article 2",
                "versions": [
                    {"version": "v1", "created": "Tue, 2 Jan 2020 10:00:00 GMT"},
                    {"version": "v2", "created": "Wed, 3 Jan 2020 10:00:00 GMT"},
                ],
            },
            {
                "id": "test.0003",
                "title": "Test Article 3",
                "versions": [{"version": "v1", "created": "Thu, 1 Jan 2021 10:00:00 GMT"}],
            },
        ]

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".jsonl") as f:
            for item in data:
                f.write(json.dumps(item) + "\n")
            temp_path = f.name

        yield temp_path

        # Cleanup
        Path(temp_path).unlink(missing_ok=True)

    def test_parser_initialization(self):
        """Test parser can be initialized."""
        parser = KittenParser(num_processes=2)
        assert parser.num_processes == 2

    def test_parser_default_processes(self):
        """Test parser uses sensible default for processes."""
        parser = KittenParser()
        assert parser.num_processes >= 1

    def test_parse_sample_data(self, sample_data_file, tmp_path):
        """Test parsing sample data."""
        parser = KittenParser(num_processes=1)
        results = parser.parse(
            file_path=sample_data_file, output_dir=str(tmp_path), create_plots=False
        )

        # Check results structure
        assert "total_articles" in results
        assert "year_counts" in results
        assert "version_counts" in results
        assert "total_errors" in results

        # Check counts
        assert results["total_articles"] == 3
        assert 2020 in results["year_counts"]
        assert 2021 in results["year_counts"]
        assert results["year_counts"][2020] == 2
        assert results["year_counts"][2021] == 1

        # Check versions
        assert 1 in results["version_counts"]
        assert 2 in results["version_counts"]
        assert results["version_counts"][1] == 2
        assert results["version_counts"][2] == 1

    def test_parse_with_convenience_function(self, sample_data_file, tmp_path):
        """Test the convenience parsing function."""
        results = parse_documents_with_whiskers(
            file_path=sample_data_file,
            output_dir=str(tmp_path),
            num_processes=1,
            create_plots=False,
        )

        assert results["total_articles"] == 3
        assert results["total_errors"] == 0

    def test_chunk_reading(self, sample_data_file):
        """Test reading file in chunks."""
        parser = KittenParser(num_processes=1)
        chunks = list(parser._read_in_chunks(Path(sample_data_file), chunk_size=2))

        # Should have 2 chunks (2 items + 1 item)
        assert len(chunks) == 2
        assert len(chunks[0]) == 2
        assert len(chunks[1]) == 1

    def test_error_handling(self, tmp_path):
        """Test handling of malformed JSON."""
        # Create file with some invalid JSON
        test_file = tmp_path / "invalid.jsonl"
        with open(test_file, "w") as f:
            f.write('{"valid": "json", "versions": [{"version": "v1", "created": "Mon, 1 Jan 2020 10:00:00 GMT"}]}\n')
            f.write("invalid json line\n")
            f.write('{"another": "valid", "versions": [{"version": "v1", "created": "Tue, 2 Jan 2020 10:00:00 GMT"}]}\n')

        parser = KittenParser(num_processes=1)
        results = parser.parse(file_path=str(test_file), create_plots=False)

        # Should have processed valid lines and counted errors
        assert results["total_articles"] == 2
        assert results["total_errors"] == 1


class TestIntegration:
    """Integration tests."""

    def test_full_pipeline_with_example_data(self):
        """Test with the actual example data if it exists."""
        example_file = Path("examples/sample_data.jsonl")

        if not example_file.exists():
            pytest.skip("Example data file not found")

        parser = KittenParser(num_processes=1)
        results = parser.parse(file_path=str(example_file), create_plots=False)

        # Basic sanity checks
        assert results["total_articles"] > 0
        assert len(results["year_counts"]) > 0
        assert len(results["version_counts"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
