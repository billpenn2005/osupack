# OSU Packer

## Introduction
A tool for packing multiple OSU Mania beatmaps and their resources into a single .osz file, with automatic BBCode song list and tag file generation for easy sharing and archiving.

## Environment
- Python 3.x
- See `requirements.txt` for dependencies (if empty, no extra packages required)

## Features
- Batch process all subfolders in a target directory, each as a song.
- Each song folder **must contain exactly one `.osu` file**.
- You may add an empty file named `PACK` in a song folder to indicate the song comes from a pack; in this case, the beatmap's `Version` name will be used directly for display.
- You may add an empty file named `P_PACK` in a song folder to indicate the song comes from a personal pack; in this case, the display name will be the `Version` name plus the creator (e.g., `Version [Creator]`).
- If other issues occur, please manually edit the files in the OSU client.
- Automatically handle .osu, audio, and image resources for each song.
- Customizable pack name, creator, and extra tags.
- Generates BBCode song list (`bbcode.txt`) and tag file (`tags.txt`).
- Output is a standard .osz file compatible with OSU client.

## Usage

### 1. Prepare Folder Structure
Each subfolder under the target directory is treated as a song. **Each song folder must contain only one `.osu` file.**
You can add an empty file named `PACK` or `P_PACK` to control naming as described above.
```
TARGETFOLDER
├───SONG1
│       SONG1.osu
│       PACK           # (optional, for pack source)
│       cover.png
│       audio.mp3
├───SONG2
│       SONG2.osu
│       P_PACK         # (optional, for personal pack source)
│       ...
├───SONG3
│       SONG3.osu      # (no PACK or P_PACK, will use default naming)
│       ...
```

### 2. Command Line Arguments
- `--dir`: Target folder to pack (required)
- `--packname`: Name of the output pack (required)
- `--creator`: Name of the pack creator (required)
- `--extratags`: Extra tags (optional)

### 3. Example Command
```powershell
python osupack.py --dir "TARGETFOLDER" --packname "PACKNAME" --creator "CREATOR" --extratags "tag1 tag2"
```
You can omit `--extratags` if not needed.

### 4. Output Files
- `PACKNAME.osz`: The packed OSU beatmap file
- `bbcode.txt`: BBCode song list for forum sharing
- `tags.txt`: All tags collected from songs

---
For further customization or issues, please check the source code or contact the author. If you encounter any problems with the generated files, please manually edit them in the OSU client.