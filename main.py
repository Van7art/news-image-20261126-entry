#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261126 bounty.

Copies the pre-rendered entry.png (a broadsheet summary of the world
news of Thursday 26 November 2026) into the output directory and
verifies the copy byte-for-byte with SHA-256.

Usage:
    python3 main.py

The output directory is taken from the MAKEFUN_OUTPUT_DIR environment
variable, or "output" when it is not set.
"""

import hashlib
import os
import shutil
import sys

SOURCE = "entry.png"
EXPECTED_SHA256 = "891033799687e3fcbeefc90c17a0e51bce2793bbd3b369e7d146b3614e765bd6"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path):
    """Read width/height from a PNG IHDR chunk (stdlib only)."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE)
    if not os.path.isfile(source):
        print("error: %s not found next to main.py" % SOURCE,
              file=sys.stderr)
        return 1

    size = os.path.getsize(source)
    if size > 1024 * 1024:
        print("error: %s is %d bytes, over the 1 MiB limit"
              % (SOURCE, size), file=sys.stderr)
        return 1
    dims = png_dimensions(source)
    if dims is None:
        print("error: %s is not a valid PNG file" % SOURCE,
              file=sys.stderr)
        return 1
    if dims != (1024, 1024):
        print("error: %s is %dx%d, expected 1024x1024"
              % (SOURCE, dims[0], dims[1]), file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, SOURCE)
    shutil.copyfile(source, dest)

    source_hash = sha256_of(source)
    dest_hash = sha256_of(dest)
    if source_hash != dest_hash:
        print("error: copy verification failed: %s != %s"
              % (source_hash, dest_hash), file=sys.stderr)
        return 1
    if source_hash != EXPECTED_SHA256:
        print("warning: source hash differs from the recorded hash: %s"
              % source_hash, file=sys.stderr)
    print("wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (dest, dims[0], dims[1], size, dest_hash))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
