# TLDR

Steps for setting up a project that uses `faster-whisper` to extract transcripts from videos

## Reference links

- https://github.com/SYSTRAN/faster-whisper
- https://docs.astral.sh/uv/
- https://github.com/openai/whisper
- https://github.com/MahmoudAshraf97/whisper-diarization

## HIGH LEVEL STEPS

- Download uv
- Install ffmpeg
- Install faster-whisper
- Add video
- Extract transcript from video

## Install and set up `uv`

- First install `uv`
- Verify `uv` installation -> 0.11.15
  - `uv --version`
- Initialize a `uv` project
  - `uv init .`
- Test the `uv` project
  - `uv run main.py`

## Install ffmpeg

- `ffmpeg -version`
- `brew install ffmpeg`
  - MacOS using Homebrew (https://brew.sh/)

## Good to know regarding installing Python

- View all installed Python versions
  - `uv python list`
- `uv python install 3.15`
- `uv run python15 --version`
- `uv run python --version`
- https://docs.astral.sh/uv/guides/install-python/
- https://www.python.org/
- https://www.python.org/downloads/
- https://github.com/SYSTRAN/faster-whisper#requirements

## Install faster-whisper

- `uv add faster-whisper`