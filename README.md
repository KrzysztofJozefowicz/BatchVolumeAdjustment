# Batch Volume Adjustment
## Why
I listen my music mainly as mp3 files from my phone to save battery. Premade playlist tend to have different mean and max volume levels between songs which leads to constant volume adjustment when songs are too quiet or too loud. 
For given list of songs, max volume is adjusted so all songs will have the same peak level.

## What it does?
For given file list or folder, max and mean volume level is detected. Maximum volume across songs list is detected, volume gain is applied to all files to achieve the same level of max volume for song list. Songs with adjusted volume are saved to output directory.

## Usage
`
python adjustment.py --paths [set of paths to mp3 files or folders space separated] --output_dir [output folder]`

`
python adjustment.py --file [file which holds set of path entries] --output_dir [output folder]`
### Examples
`python adjustment.py --paths c:\my_mp3\my_song.mp3 c:\my_mp3\my_album\ --output_dir c:\output`

`python adjustment.py --file c:\my_mp3\my_file_with_paths.txt --output_dir c:\output`


## Requirements
[Python3](https://www.python.org/)

[Ffmpeg](http://ffmpeg.org/) binaries installed and included in path to be called by scripts as "ffmpeg"