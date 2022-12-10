# beatsaber

![](https://raw.githubusercontent.com/einarf/beatsaber/master/screenshots/screenshot.PNG)

Beat Saber light shows player
using [moderngl](https://github.com/moderngl/moderngl) and [moderngl-window](https://github.com/moderngl/moderngl-window).

Music player provided by [pyglet](https://github.com/pyglet/pyglet)

## Install

```bash
$ git clone https://github.com/einarf/beatsaber.git
cd beatsaber
$ pip install --user .
```

This should give you access to the `beatsaber` command.

## Run

Run with default song:

```bash
$ beatsaber

# Optionally from source directory
python beatsaber/main.py
python -m beatsaber.main
```

Running custom song:

```bash
cd song_directory
beatsaber --song song.wav --track Expert.dat --info info.dat
```

You may have to convert the song file to wav depending on your setup.
This can easily be done with vlc or other popular media apps.

## Controls

```
SPACE: Pause music
RIGHT: Skip 10 seconds forward
LEFT: Skip 10 seconds backwards
```

Debug controls:

```
C: Toggle camera
Mouse: Rotate camera
WASD: Move camera
```

## Run tests

```
pytest
```

## Attributions

* Test song: https://bsaber.com/songs/63e1/
* Platforms by: https://bsaber.com/members/pixelguymm/
* Inspiration from: https://skystudioapps.com/bs-viewer/?id=63e1&difficulty=0
