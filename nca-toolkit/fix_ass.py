#!/usr/bin/env python3
r"""
Prepares a raw GCS-downloaded .ass file for use with the caption endpoint:
  1. Fixes double-escaped backslashes (\\c -> \c)
  2. Adds the standard ASS header if missing
  3. Rechunks dialogue into 2×2 blocks: 2 words per line, 2 lines visible at
     once. The block stays stable while the highlight moves through all 4
     words, then the block advances. This keeps centering consistent because
     the block dimensions don't change as the active word moves.

Usage: python3 fix_ass.py media/5.ass [media/6.ass ...]
"""

import sys
import re

HEADER = """\
[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,League Spartan,200,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,5,2,5,60,60,400,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

# Max characters (including the space) allowed on a single subtitle line.
# Words that would exceed this are placed alone on their line to prevent
# the ASS renderer from soft-wrapping and producing a 3rd visual line.
MAX_LINE_CHARS = 12


def to_sec(t):
    h, m, s = t.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)


def to_ts(s):
    h = int(s // 3600); s -= h * 3600
    m = int(s // 60);   s -= m * 60
    return f"{h}:{m:02d}:{s:05.2f}"


def pack_line(all_words, start_idx):
    """Return 1 or 2 words for a line, respecting MAX_LINE_CHARS."""
    if start_idx >= len(all_words):
        return []
    w1 = all_words[start_idx]
    if (start_idx + 1 < len(all_words)
            and len(w1) + 1 + len(all_words[start_idx + 1]) <= MAX_LINE_CHARS):
        return [w1, all_words[start_idx + 1]]
    return [w1]


def rechunk(dialogue_lines):
    """
    Extract per-word timings and rebuild as 2-line blocks where each line
    holds 1 or 2 words (capped by MAX_LINE_CHARS to prevent soft-wrapping).
    The active word is highlighted in cyan; the block is stable while the
    highlight moves through it, then advances to the next block.
    """
    word_timings = []
    for line in dialogue_lines:
        parts = line.split(',', 9)
        if len(parts) < 10:
            continue
        start = to_sec(parts[1])
        end   = to_sec(parts[2])
        text  = parts[9]
        m = re.search(r'\{\\c&H00FFFF&\}\s*([^\s{\\]+)', text)
        if m:
            word_timings.append((start, end, m.group(1)))

    if not word_timings:
        return dialogue_lines

    # Use the next word's start as the end of each event for tight transitions
    tightened = []
    for idx, (s, e, w) in enumerate(word_timings):
        if idx + 1 < len(word_timings):
            e = min(e, word_timings[idx + 1][0])
        tightened.append((s, e, w))
    word_timings = tightened

    all_words = [w for _, _, w in word_timings]

    def colorize(word, active):
        c = r'{\c&H00FFFF&}' if active else r'{\c&HFFFFFF&}'
        return f"{c}{word}"

    new_lines = []
    i = 0
    n = len(word_timings)

    while i < n:
        line1 = pack_line(all_words, i)
        line2 = pack_line(all_words, i + len(line1))
        block = line1 + line2
        block_size = len(block)

        for j in range(block_size):
            w_start, w_end, _ = word_timings[i + j]

            l1 = ' '.join(colorize(line1[k], j == k) for k in range(len(line1)))
            if line2:
                l2 = ' '.join(colorize(line2[k], j == len(line1) + k) for k in range(len(line2)))
                text = l1 + r'\N' + l2
            else:
                text = l1

            new_lines.append(
                f"Dialogue: 0,{to_ts(w_start)},{to_ts(w_end)},Default,,0,0,0,,{text}"
            )

        i += block_size

    return new_lines


for path in sys.argv[1:]:
    with open(path) as f:
        content = f.read()

    # 1. Fix double-escaped backslashes
    content = content.replace('\\\\c', '\\c')

    # 2. Strip any existing header so we always use the canonical one
    lines = content.splitlines()
    dialogue_lines = [l for l in lines if l.startswith('Dialogue:')]

    if not dialogue_lines:
        print(f"No Dialogue lines found, skipping: {path}")
        continue

    # 3. Rechunk into 2×2 blocks with karaoke highlighting
    new_dialogues = rechunk(dialogue_lines)

    result = HEADER + '\n'.join(new_dialogues) + '\n'

    with open(path, 'w') as f:
        f.write(result)

    print(f"Fixed ({len(new_dialogues)} lines): {path}")
