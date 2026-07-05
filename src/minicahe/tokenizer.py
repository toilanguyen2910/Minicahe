"""Tokenizer module for Minicahe.

Handles token counting using tiktoken with fallback.
"""

import re
import logging
from typing import Optional

try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False

logger = logging.getLogger(__name__)


# Rough token estimation for non-OpenAI models / fallback
# English: ~4 chars per token, code: ~3 chars per token
# This is a rough heuristic


def _estimate_tokens(text: str) -> int:
    """Estimate token count using character-based heuristic."""
    # Count words (split by whitespace)
    words = len(text.split())
    # Count chars excluding whitespace
    chars_no_space = len(re.sub(r"\s+", "", text))
    
    # Heuristic: ~1.3 tokens per word or ~4 chars per token
    word_estimate = words * 1.3
    char_estimate = chars_no_space / 4.0
    
    return max(int(min(word_estimate, char_estimate)), 0)


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens in text. Uses tiktoken if available, falls back to estimation.
    
    Args:
        text: The text to count tokens in.
        model: Model name for encoding (default: gpt-4).
    
    Returns:
        Number of tokens.
    """
    if not text:
        return 0
    
    if HAS_TIKTOKEN:
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except Exception:
            try:
                # Fallback to cl100k_base (used by GPT-4, GPT-3.5-turbo)
                encoding = tiktoken.get_encoding("cl100k_base")
                return len(encoding.encode(text))
            except Exception:
                pass
    
    return _estimate_tokens(text)


def count_tokens_batch(texts: list[str], model: str = "gpt-4") -> list[int]:
    """Count tokens for multiple texts."""
    return [count_tokens(t, model) for t in texts]


def get_token_savings(original: str, compressed: str, model: str = "gpt-4") -> dict:
    """Calculate token savings between original and compressed text.
    
    Returns:
        Dict with original_tokens, compressed_tokens, savings, savings_pct.
    """
    orig_tokens = count_tokens(original, model)
    comp_tokens = count_tokens(compressed, model)
    
    savings = orig_tokens - comp_tokens
    savings_pct = (savings / orig_tokens * 100) if orig_tokens > 0 else 0
    
    return {
        "original_tokens": orig_tokens,
        "compressed_tokens": comp_tokens,
        "savings": savings,
        "savings_pct": round(savings_pct, 1),
        "original_chars": len(original),
        "compressed_chars": len(compressed),
    }
