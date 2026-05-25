#!/usr/bin/env python3
"""
Identify viral moments in a transcript using Claude.

Reads:   TRANSCRIPT_FILE
Writes:  <transcript_stem>.moments.json (alongside the transcript)
"""

import json
import subprocess
import sys
from pathlib import Path

TRANSCRIPT_FILE = Path(__file__).parent / "media" / "zoom_group_call.transcript.txt"
OUT_FILE = Path(__file__).parent / "media" / "zoom_group_call.moments.json"
PROMPT_FILE = Path(__file__).parent / "prompts" / "identify_best_moments.md"

def main() -> None:
    print(f"[1/4] reading {TRANSCRIPT_FILE.name}", flush=True)
    transcript = TRANSCRIPT_FILE.read_text()
    print(f"[2/4] launching claude ({len(transcript)} chars of input)", flush=True)

    proc = subprocess.Popen(
        ["claude", "-p",
         "--model", "sonnet",
         "--output-format", "stream-json",
         "--include-partial-messages",
         "--verbose",
         "--append-system-prompt", PROMPT_FILE.read_text()],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1,
    )
    proc.stdin.write(transcript)
    proc.stdin.close()
    print("[3/4] waiting for Claude...\n", flush=True)

    result_text = ""
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            sys.stdout.write(line)
            sys.stdout.flush()
            continue
        etype = event.get("type")
        if etype == "system":
            print(f"  · {event.get('subtype', '?')}", flush=True)
        elif etype == "stream_event":
            delta = event.get("event", {}).get("delta", {})
            if delta.get("type") == "text_delta":
                sys.stdout.write(delta["text"])
                sys.stdout.flush()
        elif etype == "result":
            result_text = event.get("result", "")
    proc.wait()

    text = result_text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    OUT_FILE.write_text(text)
    print(f"\n\n[4/4] wrote {OUT_FILE.name} ({len(json.loads(text)['moments'])} moments)")


if __name__ == "__main__":
    main()
