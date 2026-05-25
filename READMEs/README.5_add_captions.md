# TLDR

Info regarding the included scripts related to The NCA Toolkit API

## Relevant links

- https://github.com/stephengpope/no-code-architects-toolkit
- https://www.docker.com/products/docker-desktop/

## Info about the provided scripts

The `nca-toolkit` folder holds several utility Python that you can add into your local NCA Toolkit repo

### For adding captions styled according to a template

```sh
.venv/bin/python caption_tmplt_1.py edited_clip.mp4
```

### For burning in captions onto a video after manual edits made to .ass

```sh
.venv/bin/python burn.py edited_clip.mp4
```

### For running local file server for the nca-toolkit-fork

```sh
python3 -m http.server 9000 --directory ~/src/actual_projects/MARKETING_AUTOMATION/nca-toolkit-fork/media
```

### Regarding fixing issues with generated captions

Fix any issues by prompting Claude Code
