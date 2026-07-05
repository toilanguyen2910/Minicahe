"""Compressor module for Minicahe v3 - Extreme compression engine.
Target: >50% token reduction while preserving >90% quality.
"""

import re
from collections import Counter
from minicahe.tokenizer import count_tokens
from minicahe.code_compressor import CodeCompressor

PHRASE_MAP_V2 = {
    "in order to": "to"
}

TECH_WHITELIST = {'api', 'id', 'url', 'sql', 'get', 'put', 'post', 'app', 'v2', 'v3', 'key', 'use', 'was'}
LOGICAL_WORDS = {'not', 'no', 'nor', 'none', 'never', 'off', 'out'}

class CompressorV2:
    def __init__(self, mode="normal", aggressive=False, code=False, preserve_words=None, no_acronym=False, mask_pii=False):
        # Support legacy aggressive flag
        self.mode = "aggressive" if aggressive else mode
        self.code = code
        self.no_acronym = no_acronym
        self.mask_pii = mask_pii
        self.preserve_words = set(preserve_words) if preserve_words else set()
        self.preserve_words.update(TECH_WHITELIST)
        self.preserve_words.update(LOGICAL_WORDS)
        
        self._stats = {"phrases_replaced": 0, "filler_removed": 0,
                       "acronym_injected": 0, "whitespace_normalized": 0}
        self.drop_list = {
            'the', 'a', 'an', 'to', 'of', 'in', 'is', 'it', 'we', 'on', 'at', 'by', 'as', 'or', 'for', 'be', 'and', 'with', 'that', 'this', 'have', 'from', 'they', 'are', 'were', 'been', 'some', 'very', 'really', 'just', 'actually', 'basically', 'which', 'could', 'would', 'should', 'there', 'their', 'about', 'these', 'those', 'then', 'than', 'can', 'will', 'has', 'had', 'do', 'does', 'did', 'but', 'if', 'so', 'out', 'up', 'down', 'over', 'under', 'again', 'further', 'once', 'here', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'too', 's', 't', 'don', 'now', 'am', 'also', 'into', 'first', 'said', 'new', 'one', 'two', 'what', 'who', 'whom', 'whose', 'our', 'my', 'your', 'his', 'her', 'its', 'et', 'al', 'way'
        }

    def compress(self, text):
        if not text: return text
        if self.code:
            cc = CodeCompressor()
            res = cc.compress(text)
            self._stats.update(cc.get_stats())
            return res
            
        original = text
        
        # Phase 1: Phrase replacements
        for phrase, replacement in PHRASE_MAP_V2.items():
            pattern = re.compile(re.escape(phrase), re.IGNORECASE)
            count = len(pattern.findall(text))
            if count:
                text = pattern.sub(replacement, text)
                self._stats["phrases_replaced"] += count

        # Optional PII Masking
        if self.mask_pii:
            # Mask emails
            text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[EMAIL]', text)
            # Mask phone numbers and credit cards (simple heuristic)
            text = re.sub(r'(?<!\d)(?:\+?\(?\d[ \-\.\(\)]*){9,15}\d(?!\d)', '[REDACTED]', text)

        # Phase 2 & 3: Extreme compression (Aggressive or Conservative)
        if self.mode in ("aggressive", "conservative"):
            if not self.no_acronym:
                text = self._auto_acronymize(text)
            words = text.split()
            
            kept = []
            seen_keywords = set()
            for w in words:
                # Keep alphanumeric for whitelist checking (Bug #3 fix)
                clean_alnum = re.sub(r'[^a-zA-Z0-9]', '', w).lower()
                
                # Protect whitelisted words (length < 4 won't matter, dedup won't affect them)
                if clean_alnum in self.preserve_words:
                    kept.append(w)
                    if w.endswith('.') or w.endswith('!') or w.endswith('?'):
                        seen_keywords.clear()
                    continue

                # Strip numbers for aggressive filtering / dedup logic
                clean = re.sub(r'[^a-zA-Z]', '', w).lower()

                # In aggressive mode, drop all words < 4 letters, and filter common long words
                if self.mode == "aggressive":
                    if len(clean) < 4:
                        self._stats["filler_removed"] += 1
                        continue
                        
                    if clean in self.drop_list:
                        self._stats["filler_removed"] += 1
                        continue
                
                # In both aggressive and conservative mode, deduplicate long words
                if len(clean) >= 4:
                    if clean in seen_keywords:
                        # Drop duplicate keyword to save tokens!
                        self._stats["filler_removed"] += 1
                        continue
                    seen_keywords.add(clean)
                    
                kept.append(w)
                
                # Reset keyword deduplication on sentence boundaries
                if w.endswith('.') or w.endswith('!') or w.endswith('?'):
                    seen_keywords.clear()
            
            text = " ".join(kept)

        text = re.sub(r"\s+", " ", text).strip()
        if text != original:
            self._stats["whitespace_normalized"] += 1
        return text

    def get_stats(self):
        return dict(self._stats)

    def reset_stats(self):
        self._stats = {"phrases_replaced": 0, "filler_removed": 0, "acronym_injected": 0, "whitespace_normalized": 0}

    def _auto_acronymize(self, text):
        words = text.split()
        if len(words) < 10: return text
        
        # Build a set of all original words to avoid acronym collisions with real words
        original_words = {re.sub(r'[^a-zA-Z]', '', w).lower() for w in words}
        
        candidates = []
        for n in [4, 3]:
            ngrams = []
            for i in range(len(words)-n+1):
                gram = words[i:i+n]
                if all(w.isalpha() for w in gram):
                    ngrams.append(" ".join(gram).lower())
            
            counts = Counter(ngrams)
            for ngram, count in counts.items():
                if count >= 2:
                    gram_words = ngram.split()
                    if gram_words[0] not in self.drop_list and gram_words[-1] not in self.drop_list:
                        candidates.append(ngram)
                        
        used_acronyms = set()
        for ngram in candidates:
            acronym = "".join([w[0].upper() for w in ngram.split()])
            
            # Prevent acronym collisions (Bug #4 and #5)
            if acronym.lower() in original_words or acronym in used_acronyms:
                continue
                
            used_acronyms.add(acronym)
            
            pattern = re.compile(re.escape(ngram), re.IGNORECASE)
            # count occurrences
            matches = len(pattern.findall(text))
            if matches > 0:
                text = pattern.sub(acronym, text)
                self.preserve_words.add(acronym.lower())
                self._stats["acronym_injected"] += matches
                
        return text

Compressor = CompressorV2

def compress_text(text: str, mode: str = "normal", aggressive: bool = False, code: bool = False, preserve_words: list = None, no_acronym: bool = False, mask_pii: bool = False) -> str:
    compressor = CompressorV2(mode=mode, aggressive=aggressive, code=code, preserve_words=preserve_words, no_acronym=no_acronym, mask_pii=mask_pii)
    return compressor.compress(text)
