# Minicahe 🪨

> **Rule-based text compressor for LLM prompts and logs**

Minicahe is a rule-based text compression tool inspired by [headroom](https://github.com/headroomlabs-ai/headroom), [codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp), and [caveman](https://github.com/JuliusBrussee/caveman).

Use the CLI or Python API to shorten text before sending it to an LLM. The
aggressive mode can remove useful context, so review its output before using
it for instructions, legal text, code, or other high-stakes material.

The four bundled benchmark samples currently average **45.8% token reduction**
in aggressive mode. This is a small sample, not a guarantee for other inputs.

---

## ✨ Features

- 🚀 **Configurable reduction**: Choose normal, conservative, or aggressive mode according to your tolerance for information loss.
- 🧠 **Code compression**: A Python-focused mode removes comments and some standalone strings; run your tests on the result before executing it.
- 🔄 **Auto-Acronymizer**: Automatically finds frequent long phrases and replaces them with acronyms.
- 🔑 **Aims to preserve key domain terms**: Protects critical domain-specific keywords from being lost, and allows user whitelists.
- ⚡ **Local processing**: Compression itself makes no LLM calls; runtime depends on input size.
- 📊 **Tiktoken Integration**: Counts tokens for supported model encodings, with an approximate fallback estimator.
- 🛠️ **CLI Ready**: Compress strings, files, or pipe data directly from your terminal.

## 🔬 How It Works (The Magic)

Aggressive mode uses the following text transformations. They are lossy and
can change meaning, especially in short instructions or repeated statements:

1. **Keyword Deduplication**: 
   Repeated long words can be removed within a sentence. This can change emphasis or relationships.
   
2. **Auto-Acronymizer**: 
   Repeated phrases can be replaced with generated acronyms. Review unfamiliar abbreviations in the result.

3. **Extreme Lexical Trimming**: 
   Short and common words are removed except protected words and numeric values. This can remove conditions or grammatical relationships.
   
4. **Whitespace Optimization**: 
   Collapses repeated whitespace in text mode.

## 🚀 Quick Start

### Installation

For the GitHub `v1.0.1` fixes, install from the tagged source:

```bash
python -m pip install "git+https://github.com/toilanguyen2910/Minicahe.git@v1.0.1"
```

The PyPI package is still at 1.0.0 until a separate PyPI upload is made.
For local development, clone and install in editable mode:

```bash
# Clone the repository
git clone https://github.com/toilanguyen2910/Minicahe.git
cd Minicahe

# Install from source
pip install -e .
```

### CLI Usage

```bash
# Compress an inline string (Aggressive Mode)
minicahe compress --aggressive "In the field of natural language processing, transformer-based models have become the dominant approach for a wide range of tasks."

# Compress a text file
minicahe compress --file data/long_log.txt --aggressive

# Compress a Python codebase file (Strips comments & docstrings)
minicahe compress --file src/main.py --code

# Pipe mode (Great for CI/CD or logging)
cat my_code.py | minicahe compress --code > compressed_code.py

# View your overall token savings stats
minicahe stats
```

## 📊 Benchmark

Run the four bundled samples with `python tests/benchmark.py`. Results from
Python 3.11 with `tiktoken` installed:

| Mode | Average token reduction | Average lexical recall |
| --- | ---: | ---: |
| Normal | 4.4% | 99.7% |
| Aggressive | 45.8% | 76.9% |

Lexical recall is the share of unique, non-stop words of four or more letters
that remain in the output. It does **not** measure preserved meaning or LLM
answer quality. The benchmark contains only four hand-written samples, one of
which is Python code. Results will vary with the text and tokenizer. Test on
your own data before using compressed text in a production workflow.

## 🏗️ Architecture

```text
src/minicahe/
├── __init__.py          # Package initialization
├── cli.py               # Click CLI application
├── compressor.py        # Core Engine (Deduplication, Trimming, Phrase mapping)
├── code_compressor.py   # Specialized Python AST/Token compressor
├── tokenizer.py         # Token calculation (Tiktoken + fallback)
└── stats.py             # Global savings tracker
```

## 💡 Use Cases

- **RAG Pipelines**: Experiment with shortening retrieved documents while checking whether answers remain grounded in the source.
- **Agent Memory**: Reduce repetitive logs after separating facts that must be retained.
- **Codebase Analysis**: Shorten snippets for exploration; keep the original source available for verification.

## ⚖️ License

MIT License. See `LICENSE` for more information.
