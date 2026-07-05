"""CLI module for Minicahe.

Command-line interface using click.
"""

import sys
import os
from pathlib import Path

import click

from .compressor import Compressor, compress_text
from .tokenizer import count_tokens, get_token_savings
from .stats import StatsTracker
from . import __version__


@click.group()
@click.version_option(version=__version__)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def cli(verbose):
    """Minicahe - Mini Token Optimizer.

    Talk smart, use fewer tokens.
    """
    pass


@cli.command()
@click.argument("text", required=False)
@click.option("--file", "-f", type=click.Path(exists=True), help="Path to file to compress")
@click.option("--aggressive", "-a", is_flag=True, help="Use aggressive compression")
@click.option("--code", "-c", is_flag=True, help="Use code-specific compression (strip comments/docstrings)")
@click.option("--preserve-words", "-p", multiple=True, help="Protect specific words from being stripped (can be used multiple times)")
@click.option("--no-acronym", is_flag=True, help="Disable Auto-Acronymizer in aggressive mode")
@click.option("--show-stats", "-s", is_flag=True, help="Show compression statistics")
@click.option("--model", "-m", default="gpt-4", help="Model for token counting (default: gpt-4)")
def compress(text, file, aggressive, code, preserve_words, no_acronym, show_stats, model):
    """Compress text to use fewer tokens.

    Provide TEXT as a string or use --file to compress a file.
    """
    if file:
        with open(file, "r", encoding="utf-8") as f:
            original = f.read()
        source = file
    elif text:
        original = text
        source = "stdin"
    else:
        # Read from stdin
        original = sys.stdin.read().strip()
        source = "stdin"

    if not original:
        click.echo("Error: No input provided.", err=True)
        sys.exit(1)

    # Compress
    compressor = Compressor(aggressive=aggressive, code=code, preserve_words=preserve_words, no_acronym=no_acronym)
    compressed = compressor.compress(original)

    # Calculate savings
    savings = get_token_savings(original, compressed, model)

    # Output
    if show_stats:
        click.echo(f"{'-' * 50}")
        click.echo(f"[Stats]  Minicahe Compression Report")
        click.echo(f"{'-' * 50}")
        click.echo(f"Source:         {source}")
        click.echo(f"Mode:           {'Aggressive' if aggressive else 'Normal'}")
        click.echo(f"Model:          {model}")
        click.echo()
        click.echo(f"Original:       {savings['original_tokens']:>8} tokens  ({savings['original_chars']:>6} chars)")
        click.echo(f"Compressed:     {savings['compressed_tokens']:>8} tokens  ({savings['compressed_chars']:>6} chars)")
        click.echo(f"Saved:          {savings['savings']:>8} tokens  ({savings['savings_pct']}%)")
        click.echo()
        click.echo(f"Phrases replaced: {compressor.get_stats().get('phrases_replaced', 0)}")
        click.echo(f"Filler removed:    {compressor.get_stats().get('filler_removed', 0)}")
        click.echo(f"Acronyms injected: {compressor.get_stats().get('acronym_injected', 0)}")
        if code:
            click.echo(f"Comments removed:  {compressor.get_stats().get('comments_removed', 0)}")
            click.echo(f"Docstrings rm:     {compressor.get_stats().get('docstrings_removed', 0)}")
        click.echo(f"{'-' * 50}")
        click.echo()
        click.echo(compressed)
    else:
        # Just print compressed text
        click.echo(compressed)

    # Record stats
    try:
        tracker = StatsTracker()
        tracker.record_compression(
            savings["original_tokens"],
            savings["compressed_tokens"],
            context=source,
        )
    except Exception:
        pass  # Stats are non-critical


@cli.command()
@click.option("--model", "-m", default="gpt-4", help="Model for token counting")
def stats(model):
    """Show compression statistics."""
    tracker = StatsTracker()
    summary = tracker.get_summary()

    click.echo(f"{'-' * 50}")
    click.echo(f"[Stats]  Minicahe Stats Summary")
    click.echo(f"{'-' * 50}")
    click.echo(f"Total compressions:  {summary['total_compressions']}")
    click.echo(f"Total tokens saved:  {summary['total_tokens_saved']:,}")
    click.echo(f"Overall savings:     {summary['overall_savings_pct']}%")
    click.echo()
    click.echo(f"Database: {summary['db_path']}")

    if summary["sessions"]:
        click.echo()
        click.echo("Recent sessions:")
        click.echo(f"{'-' * 50}")
        for s in reversed(summary["sessions"]):
            click.echo(f"  {s['timestamp'][:19]}  |  {s['savings']:+d} tokens  ({s['savings_pct']}%)")


@cli.command()
def info():
    """Show system information."""
    click.echo(f"Minicahe v{__version__}")
    click.echo(f"Python: {sys.version}")
    click.echo(f"Platform: {sys.platform}")

    # Check tiktoken
    try:
        import tiktoken
        click.echo("tiktoken: [OK] available")
    except ImportError:
        click.echo("tiktoken: [X] not installed (using fallback estimator)")

    # Check click
    click.echo(f"click: [OK] available (v{click.__version__})")

    # Stats db
    tracker = StatsTracker()
    summary = tracker.get_summary()
    click.echo(f"Stats DB: {summary['db_path']}")


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
