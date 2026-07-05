import os, json

path = r"C:\Users\Admin\OneDrive\Documents\Minicahe\tests\benchmark.py"

content = '''\"\"\"Minicahe Benchmark\"\"\"
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from minicahe.compressor import compress_text
from minicahe.tokenizer import count_tokens, HAS_TIKTOKEN
import difflib, re

SAMPLES = []

'''

samples = []
samples.append({"name": "Email", "text": "test"})
content += 'SAMPLES = ' + json.dumps(samples, indent=2)

with open(path, 'w') as f:
    f.write(content)
print("OK")
