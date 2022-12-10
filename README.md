# beatsaber

![](https://raw.githubusercontent.com/einarf/beatsaber/master/screenshots/screenshot.PNG)

Beat Saber light shows player
using [moderngl](https://github.com/moderngl/moderngl) and [moderngl-window](https://github.com/moderngl/moderngl-window).

Music player provided by [pyglet](https://github.com/pyglet/pyglet)

## Install


```bash
$ pip install -e .
```

## Run

During installation the `beatsaber` command should be available.

```bash
$ beatsaber

# Optionally
python beatsaber/main.py
python -m beatsaber.main
```

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
