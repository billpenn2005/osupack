# OSU Packer
* ## Environment
  * requirements.txt
* ## Usage
  * Pack multiple songs into one .osz file from target folder. (Note that each folder in target folder can only contain ont .osu file)
  * Need to set pack name,creator name,target folder path
  * Example
    * folder structure:
        ```
        TARGETFOLDER
        ├───SONG1
        │       SONG1.osu
        │
        └───SONG2
                SONG2.osu
        ```
    * code:
        ```
        (Cmd) set folderpath 'TARGETFOLDER'
        (Cmd) set packname PACKNAME
        (Cmd) set creator CREATOR
        (Cmd) run
        ```