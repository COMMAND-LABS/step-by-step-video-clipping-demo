#!/usr/bin/env python3
"""
Cut moments out of a video using its moments.json.

Writes:  clips/clip_NN.mp4
"""

import json
import subprocess
from pathlib import Path

VIDEO_FILE = Path(__file__).parent / "media" / "parsity_group_call.mp4"
MOMENTS_JSON = Path(__file__).parent / "media" / "parsity_group_call.moments.json"
CLIPS_DIR = Path(__file__).parent / "clips"
PADDING_SEC = 30.0  # extra seconds added before start and after end of each clip


def hms_to_sec(ts: str) -> float:
    h, m, s = ts.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def main() -> None:
    moments = json.loads(MOMENTS_JSON.read_text())["moments"]
    CLIPS_DIR.mkdir(exist_ok=True)

    for i, m in enumerate(moments, 1):
        start = max(0.0, hms_to_sec(m["start_timestamp"]) - PADDING_SEC)
        end = hms_to_sec(m["end_timestamp"]) + PADDING_SEC
        out = CLIPS_DIR / f"clip_{i:02d}.mp4"

        print(f"[{i:02d}/{len(moments)}] {m['title']}  ({end - start:.1f}s)")
        subprocess.run(
            [
                "ffmpeg", "-y",
                "-ss", f"{start:.3f}",
                "-i", str(VIDEO_FILE),
                "-t", f"{end - start:.3f}",
                "-c:v", "libx264", "-preset", "fast", "-crf", "20",
                "-c:a", "aac", "-b:a", "192k",
                str(out),
            ],
            check=True,
        )


if __name__ == "__main__":
    main()
