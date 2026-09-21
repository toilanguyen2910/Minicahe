"""Checks for meaning and code validity at the compression boundary."""

import ast

from minicahe.compressor import compress_text


def test_aggressive_keeps_numeric_values():
    result = compress_text("Set timeout to 30 seconds and retry 3 times.", aggressive=True)
    assert "30" in result
    assert "3" in result


def test_code_mode_keeps_executable_function_after_docstring_removal():
    source = 'def f():\n    """doc"""\n    return 1\n'
    result = compress_text(source, code=True)
    ast.parse(result)
    namespace = {}
    exec(result, namespace)
    assert namespace["f"]() == 1


def test_code_mode_keeps_docstring_only_function_valid():
    source = 'def f():\n    """doc"""\n'
    result = compress_text(source, code=True)
    ast.parse(result)


def test_code_mode_keeps_docstring_only_class_valid():
    source = 'class C:\n    """doc"""\n'
    result = compress_text(source, code=True)
    ast.parse(result)
