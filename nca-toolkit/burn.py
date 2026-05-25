#!/usr/bin/env python3
"""
Burn styled .ass captions into a video -> final MP4.

burn(video) reads media/<name>.mp4 and its sibling media/<name>.ass and
writes output/<name>.mp4 with the captions burned in.

The caption_tmplt_*.py templates call this as their final step. Run it
directly to re-render after hand-editing the .ass, without re-styling:

    python3 burn.py clip_1.mp4

Needs ffmpeg on PATH.
"""
import os
import sys
import subprocess

MEDIA_DIR  = "media"     # source video + its styled .ass live here
OUTPUT_DIR = "output"    # finished videos go here
FONTS_DIR  = "fonts"     # font folder libass renders from


def burn(video):
    """Burn media/<name>.ass into media/<name>.mp4 -> output/<name>.mp4.

    `video` may be a filename or path; only its basename is used.
    Returns the path to the rendered video.
    """
    name      = os.path.splitext(os.path.basename(video))[0]
    video_in  = os.path.join(MEDIA_DIR, name + ".mp4")
    ass       = os.path.join(MEDIA_DIR, name + ".ass")
    video_out = os.path.join(OUTPUT_DIR, name + ".mp4")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-loglevel", "error", "-stats",
            "-i", video_in,
            "-vf", "subtitles=%s:fontsdir=%s" % (ass, FONTS_DIR),
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart",
            "-y", video_out,
        ],
        check=True,
    )
    print("Burned captions into video -> %s" % video_out)
    return video_out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: python3 burn.py <video>   (e.g. clip_1.mp4)")
    burn(sys.argv[1])
