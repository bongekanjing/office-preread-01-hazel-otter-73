"""Write the line to /output/entry.txt.

The line lives in LINE.txt so the bytes judged are the bytes committed:
nothing is assembled at run time and nothing is fetched over the network.
"""

import os

# The gate takes 1 to 200 characters of UTF-8 that is not only white space.
# Checked here so a bad LINE.txt fails loudly in the build log rather than
# scoring a silent zero on the board.
MAX_CHARS = 200

HERE = os.path.dirname(os.path.abspath(__file__))
LINE = os.path.join(HERE, "LINE.txt")
OUT_NAME = "entry.txt"

with open(LINE, "rb") as handle:
    raw = handle.read()

# A file that is not valid UTF-8 fails the gate: name the problem here rather
# than half-decode it into something that happens to fit.
try:
    text = raw.decode("utf-8")
except UnicodeDecodeError as exc:
    raise SystemExit("LINE.txt is not valid UTF-8: %s" % exc)

# A byte-order mark is an encoding artefact, not part of the line.
if text.startswith("\ufeff"):
    text = text[1:]

# Trailing newlines end the file; they are not part of the line.
line = text.rstrip("\r\n")

if not line.strip():
    raise SystemExit("LINE.txt is empty or only white space")
if "\n" in line or "\r" in line:
    raise SystemExit("LINE.txt holds more than one line")
if len(line) > MAX_CHARS:
    raise SystemExit("%d characters, over the %d allowed" % (len(line), MAX_CHARS))

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
# Write the bytes already checked, so what lands in /output is exactly the
# text measured above and not a second read of the file on disk.
with open(os.path.join(out_dir, OUT_NAME), "wb") as handle:
    handle.write(line.encode("utf-8"))
print("wrote %s: %d characters, %d bytes" % (OUT_NAME, len(line), len(line.encode("utf-8"))))
