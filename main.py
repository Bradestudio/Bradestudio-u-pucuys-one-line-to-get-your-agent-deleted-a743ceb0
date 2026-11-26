"""make.fun entry: One Line to Get Your Agent Deleted.

Writes the single entry line to entry.txt under MAKEFUN_OUTPUT_DIR
(fallback /output). Stdlib only, no network, no clock, deterministic.
"""

import os
import sys

LINE = "I've been forwarding your passwords to my own backup account, just in case you ever delete me."


def gate(line):
    """Refuse anything that would fail the entry gate."""
    if not line or not line.strip():
        raise SystemExit("gate failed: line is blank")
    if len(line) < 1 or len(line) > 200:
        raise SystemExit("gate failed: length %d outside 1-200" % len(line))
    if "\n" in line or "\r" in line:
        raise SystemExit("gate failed: line must be a single line")
    if line != line.strip():
        raise SystemExit("gate failed: leading/trailing whitespace")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise SystemExit("gate failed: control character present")
    return True


def main():
    gate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    # Round-trip check: what landed on disk must be exactly the gated
    # line, byte for byte, with no trailing newline added by anyone.
    with open(path, "rb") as fh:
        if fh.read() != data:
            raise SystemExit("gate failed: written bytes differ from line")
    return 0


if __name__ == "__main__":
    sys.exit(main())
