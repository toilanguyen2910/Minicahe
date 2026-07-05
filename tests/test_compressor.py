"""Tests for the compressor module."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from minicahe.compressor import Compressor, compress_text


def test_compress_empty():
    assert compress_text("") == ""
    assert compress_text(None) is None  # type: ignore
    print("[OK] test_compress_empty PASS")


def test_compress_phrase_replacement():
    compressor = Compressor()
    text = "in order to complete this task, we need to act"
    result = compressor.compress(text)
    assert "in order to" not in result, f"Expected 'in order to' removed, got: {result}"
    print(f"[OK] test_compress_phrase_replacement PASS -> '{result}'")


def test_compress_basic():
    result = compress_text("Hello world, this is a test")
    assert isinstance(result, str)
    assert len(result) > 0
    assert "Hello world" in result  # Should preserve core content
    print(f"[OK] test_compress_basic PASS -> '{result}'")


def test_compress_code_safe():
    """Code content should be preserved as much as possible."""
    code = '''
def hello(name):
    """Say hello to someone."""
    print(f"Hello, {name}!")
    return True
'''
    result = compress_text(code)
    assert "def hello" in result
    assert "print" in result
    print(f"[OK] test_compress_code_safe PASS -> preserved code structure")


def test_aggressive_mode():
    text = "I really want to please request that you basically provide assistance with this matter"
    result = compress_text(text, aggressive=True)
    orig_words = len(text.split())
    new_words = len(result.split())
    assert new_words < orig_words, f"Aggressive mode should produce shorter text: {result}"
    print(f"[OK] test_aggressive_mode PASS: {orig_words}->{new_words} words -> '{result}'")


def test_compressor_stats():
    compressor = Compressor(aggressive=True)
    compressor.compress("in order to make a decision about this in spite of the problems")
    stats = compressor.get_stats()
    assert stats["phrases_replaced"] >= 1
    print(f"[OK] test_compressor_stats PASS: {stats}")


def test_preserves_core_meaning():
    """Compression should keep the essential meaning."""
    text = "The system needs to be restarted due to the fact that it is running slowly"
    result = compress_text(text)
    # Core meaning: "system needs restart because running slowly"
    assert "system" in result.lower()
    assert "restart" in result.lower() or "slow" in result.lower()
    print(f"[OK] test_preserves_core_meaning PASS -> '{result}'")


def test_large_text():
    text = " ".join(["This is a test sentence with many filler words actually basically just really."] * 100)
    result = compress_text(text, aggressive=True)
    assert len(result) < len(text)
    print(f"[OK] test_large_text PASS: {len(text)}->{len(result)} chars")


if __name__ == "__main__":
    test_compress_empty()
    test_compress_basic()
    test_compress_phrase_replacement()
    test_compress_code_safe()
    test_aggressive_mode()
    test_compressor_stats()
    test_preserves_core_meaning()
    test_large_text()
    print("\n[DONE] All compressor tests passed!")
