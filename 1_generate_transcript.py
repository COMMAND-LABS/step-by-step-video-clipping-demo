#!/usr/bin/env python3
"""
Extract audio from a video and transcribe it with faster-whisper.

Usage:
    uv run python generate_transcript.py <video_path>
"""

import json
import subprocess
import sys
from pathlib import Path

from faster_whisper import WhisperModel

WHISPER_MODEL   = "large-v2"
WHISPER_DEVICE  = "cpu"
WHISPER_COMPUTE = "int8"


def extract_audio(video: Path, audio: Path) -> None:
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(video),
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            str(audio),
        ],
        check=True,
    )


def transcribe(audio: Path) -> dict:
    model = WhisperModel(WHISPER_MODEL, device=WHISPER_DEVICE, compute_type=WHISPER_COMPUTE)
    segments, info = model.transcribe(str(audio), beam_size=5, language="en", vad_filter=True)

    total = info.duration
    segs = []
    for s in segments:
        segs.append({"start": s.start, "end": s.end, "text": s.text})
        pct = s.end / total * 100
        print(f"\r  [{s.end/60:6.1f} / {total/60:.1f} min  {pct:5.1f}%]", end="", flush=True)
    print()

    return {"language": info.language, "duration": total, "segments": segs}


def hms(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 generate_transcript.py <video_path>")
        sys.exit(1)

    video = Path(sys.argv[1])
    if not video.exists():
        print(f"Video not found: {video}")
        sys.exit(1)

    stem = video.with_suffix("")
    audio = stem.with_name(stem.name + ".wav")
    transcript_json = stem.with_name(stem.name + ".transcript.json")
    transcript_txt  = stem.with_name(stem.name + ".transcript.txt")

    print(f"Extracting audio → {audio.name}")
    extract_audio(video, audio)

    print(f"Transcribing with faster-whisper ({WHISPER_MODEL}, {WHISPER_COMPUTE}) …")
    result = transcribe(audio)

    transcript_json.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    transcript_txt.write_text(
        "\n".join(f"[{hms(s['start'])}] {s['text'].strip()}" for s in result["segments"])
    )

    print(f"Done → {transcript_json.name}, {transcript_txt.name}")


if __name__ == "__main__":
    main()
