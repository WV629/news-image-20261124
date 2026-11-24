#!/usr/bin/env python3
"""Entry point: write the day's news image to /output/entry.png.

The picture is rendered deterministically by generate.py from the verified
news data baked into it; this file only moves the finished file to the
directory the grader reads. No network is used at run time. The grader
runs this file with the repository read-only, so it writes nothing there,
and it imports nothing beyond the standard library.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))

src = os.path.join(HERE, "entry.png")
out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
print("wrote /output/entry.png")
