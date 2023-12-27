# Qidi Thumbnails Post Processing Script For Orca Slicer

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

## General Info

This is a fork of [ElegooNeptuneThumbnails-Prusa](https://github.com/Molodos/ElegooNeptuneThumbnails-Prusa). 
That developer took the time to reverse engineer the library everyone uses for this operation. They did the hard work. All I did was modify their work for Qidi printers. 
I looked at some Qidi source code for their thumbnail generation, modified a few things, and went full send. I guess also thank Qidi for releasing their software source.

Orca Slicer post processing script for adding gcode thumbnail images for Qidi printers. The following models
are supported:

- Qidi XSmart 3
- Qidi XPlus 3
- Qidi XMax 3

## Installation

1) You have to compile the script yourself as described in [Packaging Guide](#packaging-guide). I am not pre-building anything...probably.
2) Place the binary somewhere on your system and remember the path (`/Users/sparky/sandbox/QidiThumbnails-OrcaSlicer/dist/QidiThumbnails-OrcaSlicer`)
3) Set the thumbnail size in Orca Slicer as desired (default is 300x300 and will work). The largest thumbnail used by the printer is 380x380 so you might want to set Orca at least that big if you want to avoid minor scaling quality loss. Click on the little pencil icon to the right of the printer drop-down if you want to change it.
4) Configure the path to the post processing script binary. Under the Process section, click Others and scroll down to Post-processing Scripts. Add the full path
   to your executable. Orca will automatically send the path to the gcode it generates so you only need the path to the executable.
5) If it isn't working, check the [FAQ](#faq)

## FAQ

### Why?

I prefer to use Orca Slicer over Qidi Slicer but the base64 PNG that Orca puts in gcode does not display on the printer front panel

### What printers have you tested on?

This has only been tested on a Qidi XMax 3 with a binary built on a Mac M2. You are on your own for Python support.

### Do you like Python?

No. Python support is better coming from Google than myself. I am an SDE but I do not have much need for Python in my daily life at this time.
My brain can only fit immediately relevant knowledge and completely useless knowledge.

### Are you sure the thumbnail dimensions are correct?

No. I simply used the sizes I found in Qidi Slicer. If you find sizes that work better then simply modify the dimensions in the script and recompile.
 Also, please file an issue and I will verify and update the codebase.

## Packaging Guide

### For Macs with M-series chips
If you have an arm64 mac, you will need to build an executable inside of a x86_64 python environment. The easiest way is with [miniconda](https://formulae.brew.sh/cask/miniconda):

After installing miniconda you need to init your shell:
```
conda init "$(basename "${SHELL}")"
```

Setup the env:
```
conda create -p ./my_x86_env -y
conda activate ./my_x86_env
conda config --env --set subdir osx-64
conda install python=3.11 -y
```
Then, follow the steps for other systems.

### Other systems

1) Install requirements `pip install -r requirements.txt`
2) Create binary for your system
   
   Windows:
   ```shell
   pyinstaller --onefile --name="QidiThumbnails-OrcaSlicer" qidi_thumbnails.py
   ```
   Mac/Linux:
      ```shell
   pyinstaller --onefile --name="QidiThumbnails-OrcaSlicer" qidi_thumbnails.py
   ```
3) Binary is in `dist` folder

## License

This repository uses code snippets and image encoding binaries from Elegoo Cura MKS Plugin and is therefore released
under the **AGPL v3** license. Shamelessly forked from [ElegooNeptuneThumbnails-Prusa](https://github.com/Molodos/ElegooNeptuneThumbnails-Prusa)
