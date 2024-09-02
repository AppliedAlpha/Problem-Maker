import os
import sys
import subprocess

process = subprocess.Popen(
    ["python" if os.name == "nt" else "python3", "sub.py"], 
    stdin=subprocess.PIPE, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE, 
    text=True
)

inputs = ["1 3", "4 6 7"]

stdout, stderr = process.communicate('\n'.join(inputs))
print(stdout)

if stderr:
    print("Subprocess error:", stderr)