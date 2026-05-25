#!/usr/bin/env python3
"""
Shared transcription step: a video file -> a raw .ass subtitle file.

transcribe(video) POSTs the video to the NCA toolkit /transcribe-media
endpoint, downloads the resulting .ass into MEDIA_DIR, repairs it with
fix_ass.py, and returns its path.

The result is cached: if MEDIA_DIR/<name>.ass already exists the API call
is skipped -- so re-runs, and every caption_tmplt_*.py template, reuse one
transcription instead of transcribing the same video again.

Configure via environment variables (defaults shown):
  API_KEY     your_api_key
  API_BASE    http://localhost:8080
  MEDIA_BASE  http://host.docker.internal:9000   (URL the API fetches from)
  MEDIA_DIR   media
"""
import os
import sys
import json
import subprocess
import urllib.request

API_KEY    = os.environ.get("API_KEY",    "your_api_key")
API_BASE   = os.environ.get("API_BASE",   "http://localhost:8080")
MEDIA_BASE = os.environ.get("MEDIA_BASE", "http://host.docker.internal:9000")
MEDIA_DIR  = os.environ.get("MEDIA_DIR",  "media")

FIX_ASS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fix_ass.py")


def transcribe(video, force=False):
    """Return the path to the raw .ass transcription for `video`.

    `video` may be a filename or path; only its basename (without
    extension) is used. The .ass is cached at MEDIA_DIR/<name>.ass --
    if it exists and `force` is False, the API call is skipped.
    """
    name     = os.path.splitext(os.path.basename(video))[0]
    ass_path = os.path.join(MEDIA_DIR, name + ".ass")

    if os.path.exists(ass_path) and not force:
        print("transcribe: using cached %s" % ass_path)
        return ass_path

    os.makedirs(MEDIA_DIR, exist_ok=True)
    media_url = "%s/%s.mp4" % (MEDIA_BASE, name)
    print("transcribe: %s ..." % media_url)

    req = urllib.request.Request(
        "%s/transcribe-media" % API_BASE,
        data=json.dumps({"media_url": media_url, "output": "ass"}).encode(),
        headers={"Content-Type": "application/json", "x-api-key": API_KEY},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    if result.get("code") != 200:
        raise SystemExit("transcribe-media failed: %s" % result)

    urllib.request.urlretrieve(result["response"], ass_path)
    subprocess.run([sys.executable, FIX_ASS, ass_path], check=True)
    print("transcribe: saved %s" % ass_path)
    return ass_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: python3 transcribe.py <video> [--force]")
    print(transcribe(sys.argv[1], force="--force" in sys.argv))
