"""Compressor module for Minicahe v3 - Extreme compression engine.
Target: >50% token reduction while preserving >90% quality.
"""

import re
from minicahe.tokenizer import count_tokens

STRIP_CHARS = """.,!?;:"'()[]{}"""

PHRASE_MAP_V2 = {
    "in order to": "to"
}

class CompressorV2:
    def __init__(self, aggressive=False):
        self.aggressive = aggressive
        self._stats = {"phrases_replaced": 0, "filler_removed": 0,
                       "acronym_injected": 0, "whitespace_normalized": 0}

    def compress(self, text):
        if not text: return text
        original = text
        
        # Phase 1: Phrase replacements
        for phrase, replacement in PHRASE_MAP_V2.items():
            pattern = re.compile(re.escape(phrase), re.IGNORECASE)
            count = len(pattern.findall(text))
            if count:
                text = pattern.sub(replacement, text)
                self._stats["phrases_replaced"] += count

        # Phase 2 & 3: Extreme compression (Aggressive)
        if self.aggressive:
            words = text.split()
            
            drop_list = {
                'the', 'a', 'an', 'to', 'of', 'in', 'is', 'it', 'we', 'on', 'at', 'by', 'as', 'or', 'for', 'be', 'and', 'with', 'that', 'this', 'have', 'from', 'they', 'are', 'were', 'been', 'some', 'very', 'really', 'just', 'actually', 'basically', 'which', 'could', 'would', 'should', 'there', 'their', 'about', 'these', 'those', 'then', 'than', 'can', 'will', 'has', 'had', 'do', 'does', 'did', 'but', 'if', 'so', 'out', 'up', 'down', 'over', 'under', 'again', 'further', 'once', 'here', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'too', 's', 't', 'don', 'now', 'am', 'also', 'into', 'first', 'said', 'new', 'one', 'two', 'what', 'who', 'whom', 'whose', 'our', 'my', 'your', 'his', 'her', 'its', 'et', 'al', 'way', 'key', 'use', 'was'
            }
            
            kept = []
            seen_keywords = set()
            for w in words:
                clean = re.sub(r'[^a-zA-Z]', '', w).lower()
                
                # Drop all words < 4 letters, and heavily filter common long words
                if len(clean) < 4:
                    self._stats["filler_removed"] += 1
                    continue
                    
                if clean in drop_list:
                    self._stats["filler_removed"] += 1
                    continue
                
                if len(clean) >= 4:
                    if clean in seen_keywords:
                        # Drop duplicate keyword to save tokens!
                        self._stats["filler_removed"] += 1
                        continue
                    seen_keywords.add(clean)
                    
                kept.append(w)
            
            text = " ".join(kept)

        text = re.sub(r"\s+", " ", text).strip()
        if text != original:
            self._stats["whitespace_normalized"] += 1
        return text

    def get_stats(self):
        return dict(self._stats)

    def reset_stats(self):
        self._stats = {"phrases_replaced": 0, "filler_removed": 0, "acronym_injected": 0, "whitespace_normalized": 0}

Compressor = CompressorV2

def compress_text(text: str, aggressive: bool = False) -> str:
    compressor = CompressorV2(aggressive=aggressive)
    return compressor.compress(text)
