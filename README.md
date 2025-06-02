# OSU Packer
* ## Introduction
  * Packer for OSU Mania
* ## Environment
  * requirements.txt
* ## Usage
  * Pack multiple songs into one .osz file from a target folder.
  * Provide the following command line arguments: --dir, --packname, --creator.
  * Example:
    * Folder structure:
        ```
        TARGETFOLDER
        ├───SONG1
        │       SONG1.osu
        └───SONG2
                SONG2.osu
        ```
    * Command:
        ```
        python osupack.py --dir "TARGETFOLDER" --packname "PACKNAME" --creator "CREATOR"
        ```