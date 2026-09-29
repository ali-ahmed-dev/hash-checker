"""
Shared pytest fixtures for Hash Checker tests.

This file allows running existing unittest-based tests via pytest
without modifying the original test file.

Note: The project uses Python's built-in unittest framework.
      pytest is used only as a convenient test runner.
"""

import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def temp_dir():
    """
    Provide a temporary directory that is automatically cleaned up.
    
    Yields:
        Path: Path to the temporary directory.
    """
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


@pytest.fixture
def sample_file(temp_dir):
    """
    Create a sample file with known content for hashing tests.
    
    Yields:
        Path: Path to the sample file.
    """
    file = temp_dir / "sample.txt"
    file.write_text("hello", encoding="utf-8")
    yield file