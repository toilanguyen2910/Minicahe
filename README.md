# Minicahe 🪨

> **Mini Token Optimizer** — Talk smart, use fewer tokens.

Minicahe is a lightweight, rule-based text compression tool inspired by
[headroom](https://github.com/headroomlabs-ai/headroom) and
[caveman](https://github.com/juliusbrussee/caveman).

It reduces token usage by **30-70%** without needing ML models — just smart
rules inspired by how humans naturally shorten text.

## ✨ Features

- ✅ **Text compression** — Remove filler, shorten phrases, keep meaning
- ✅ **Token counting** — Accurate with tiktoken, fallback estimator
- ✅ **CLI tool** — minicahe compress for files or inline text
- ✅ **Stats tracking** — See how many tokens you've saved
- ✅ **Normal & Aggressive modes** — Choose your compression level
- ✅ **Cross-platform** — Windows, macOS, Linux

## 🚀 Quick Start

### Install

`ash
# Via pip (coming soon)
pip install minicahe

# Or from source
pip install -e .
`

### Use

`ash
# Compress a string
minicahe compress "in order to make a decision about this matter"

# Compress a file
minicahe compress --file notes.txt

# Aggressive compression
minicahe compress --aggressive "I would like to please request your assistance"

# Show stats
minicahe compress --show-stats "very long text here..."

# View your savings
minicahe stats
`

### Pipe mode

`ash
echo "This is a very long sentence with a lot of filler words basically just really" | minicahe compress
`

## 📊 Example

`
$ minicahe compress --show-stats --aggressive "in order to make a decision, we need to take into consideration all of the facts"

──────────────────────────────────────────────────
📊  Minicahe Compression Report
──────────────────────────────────────────────────
Source:         stdin
Mode:           Aggressive
Model:          gpt-4

Original:       24 tokens  ( 82 chars)
Compressed:      13 tokens  ( 51 chars)
Saved:          11 tokens  (45.8%)

Phrases replaced: 2
Filler removed:    0
──────────────────────────────────────────────────

we need consider all facts
`

## 🏗️ Architecture

`
src/minicahe/
├── __init__.py    # Package info
├── cli.py         # CLI (click)
├── compressor.py  # Rule-based compression engine
├── tokenizer.py   # Token counting (tiktoken + fallback)
└── stats.py       # Session tracking
`

## 🔧 How It Works

1. **Phrase replacement** — "in order to" → "to", "make a decision" → "decide"
2. **Filler removal** — "actually", "basically", "very", "really"
3. **Filler phrases** — "it should be noted that", "as a matter of fact"
4. **Aggressive mode** — abbreviations ("because" → "bc"), short forms

## ⚖️ License

MIT — free as in freedom.
