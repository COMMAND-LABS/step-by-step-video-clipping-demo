#!/usr/bin/env python3
r"""
Caption Template One  --  single-line word pairs, lower-centred.

    python3 caption_tmplt_1.py clip_1.mp4

Three steps, run from one input video:

  1. transcribe  -- video to a raw .ass        (transcribe.py -- shared, cached)
  2. style       -- re-chunk + reposition the .ass in place (this template)
  3. burn        -- captions into the final MP4 (burn.py -- shared)

This script owns step 2; steps 1 and 3 are shared modules every template
reuses. The caption style:

  - ONE line of text at a time (no \N line break).
  - 1-2 words on that line -- a pair is kept only when it actually fits
    the video width at the caption font size (measured against the real
    font), so a long word falls back to one word on its own line.
  - Centred horizontally on the video's vertical axis and anchored
    Y_OFFSET px below the video's vertical centre, via {\an5\pos(...)}.
  - Drawn in Glacial Indifference Bold at NEW_FONT px.
  - Keeps the per-word yellow highlight and per-word timing.

For media/<name>.mp4 it writes:
  - media/<name>.ass    styled subtitles, beside the video (hand-edit if needed)
  - output/<name>.mp4   final video, captions burned in

Needs ffmpeg and Pillow; the first transcription also needs the NCA
toolkit API. See README.caption_templates.md for the template catalogue.
"""
import re
import sys
from PIL import ImageFont
from transcribe import transcribe
from burn import burn

FONT_TTF  = "fonts/GlacialIndifference-Bold.ttf"   # font file (rendering + measuring)
FONT_NAME = "Glacial Indifference"                 # ASS Style "Fontname" (font family)
NEW_FONT  = 161     # caption font size, px
Y_OFFSET  = 360     # pixels below the vertical centre of the video (smaller = higher)
SAFE_PAD  = 70      # px kept clear on each side; a pair wider than this wraps

YELLOW = r"{\c&H00FFFF&}"   # highlighted (active) word
WHITE  = r"{\c&HFFFFFF&}"   # context word

if len(sys.argv) < 2:
    raise SystemExit("usage: python3 caption_tmplt_1.py <video>   (e.g. clip_1.mp4)")

# ---- 1. transcribe (shared module, cached) -------------------------------
ass = transcribe(sys.argv[1])           # -> media/<name>.ass

# ---- 2. style: re-chunk + reposition, written back to the same .ass ------
src = open(ass, encoding="utf-8").read().splitlines()

# resolution + caption position
play_x = play_y = None
for line in src:
    if line.startswith("PlayResX:"):
        play_x = int(line.split(":")[1])
    elif line.startswith("PlayResY:"):
        play_y = int(line.split(":")[1])

POS    = r"{\an5\pos(%d,%d)}" % (play_x // 2, play_y // 2 + Y_OFFSET)
budget = play_x - 2 * SAFE_PAD          # widest a one-line caption may be

font = ImageFont.truetype(FONT_TTF, NEW_FONT)
def fits(text):
    return font.getlength(text) <= budget

# highlighted word + timing for every event
hl_re = re.compile(r"\{\\c&H00FFFF&\}([^{\\ ]+)")
events = []                             # [start, end, word] in file order
for line in src:
    if not line.startswith("Dialogue:"):
        continue
    f = line.split(",", 9)              # field 10 (text) may contain commas
    m = hl_re.search(f[9])
    if not m:
        raise SystemExit("No highlighted word in: " + line)
    events.append([f[1], f[2], m.group(1)])

words = [e[2] for e in events]
n = len(words)

# greedy 1-2 word chunks that each fit on one line
chunks, chunk_of = [], [None] * n
i = 0
while i < n:
    if i + 1 < n and fits(words[i] + " " + words[i + 1]):
        c = [i, i + 1]
    else:
        c = [i]
    chunks.append(c)
    for idx in c:
        chunk_of[idx] = c
    i += len(c)

# rebuild the .ass and write it back in place
out = []
ev  = 0
for line in src:
    if line.startswith("Style: Default,"):
        fields = line.split(",")
        fields[1] = FONT_NAME           # Fontname is the 2nd Style field
        fields[2] = str(NEW_FONT)       # Fontsize is the 3rd Style field
        out.append(",".join(fields))
    elif line.startswith("Dialogue:"):
        start, end, _ = events[ev]
        text = POS + " ".join(
            (YELLOW if idx == ev else WHITE) + words[idx]
            for idx in chunk_of[ev]
        )
        out.append("Dialogue: 0,%s,%s,Default,,0,0,0,,%s" % (start, end, text))
        ev += 1
    else:
        out.append(line)

open(ass, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("Styled %d events into %d chunks -> %s" % (n, len(chunks), ass))

# ---- 3. burn the styled captions into the video (shared module) ----------
burn(sys.argv[1])
