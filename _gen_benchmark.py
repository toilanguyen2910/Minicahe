import json, os

SAMPLES_DATA = json.dumps([
    {'name':'Email','text':'test'}
])

HEADER = '# test'
path = r'C:\Users\Admin\OneDrive\Documents\Minicahe\tests\benchmark.py'
with open(path, 'w') as f:
    f.write(HEADER)
print('OK')
