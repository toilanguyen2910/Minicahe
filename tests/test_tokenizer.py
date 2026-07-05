"""Tests for the tokenizer module."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from minicahe.tokenizer import count_tokens, get_token_savings, _estimate_tokens


def test_count_empty():
    assert count_tokens("") == 0
    assert count_tokens(None) == 0  # type: ignore
    print("[OK] test_count_empty PASS")


def test_count_simple():
    count = count_tokens("Hello, world!")
    assert count > 0
    print(f"[OK] test_count_simple PASS: 'Hello, world!' -> {count} tokens")


def test_estimate_fallback():
    count = _estimate_tokens("Hello world this is a test sentence with some more words for counting")
    assert count > 0
    print(f"[OK] test_estimate_fallback PASS: ~{count} tokens")


def test_token_savings():
    original = "in order to complete this task, we need to make a decision"
    compressed = "to complete this task, we need to decide"
    savings = get_token_savings(original, compressed)
    assert savings["original_tokens"] > savings["compressed_tokens"]
    assert savings["savings"] > 0
    assert savings["savings_pct"] > 0
    print(f"[OK] test_token_savings PASS:")
    print(f"   Original: {savings['original_tokens']} tokens")
    print(f"   Compressed: {savings['compressed_tokens']} tokens")
    print(f"   Savings: {savings['savings']} tokens ({savings['savings_pct']}%)")


def test_large_count():
    text = "token " * 1000
    count = count_tokens(text)
    assert count > 100
    print(f"[OK] test_large_count PASS: ~1000 words -> {count} tokens")


if __name__ == "__main__":
    test_count_empty()
    test_count_simple()
    test_estimate_fallback()
    test_token_savings()
    test_large_count()
    print("\n[DONE] All tokenizer tests passed!")
