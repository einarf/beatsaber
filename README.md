# beatsaber

![](https://raw.githubusercontent.com/einarf/beatsaber/master/screenshots/screenshot.PNG)

Beat Saber light shows player
using [moderngl](https://github.com/moderngl/moderngl) and [moderngl-window](https://github.com/moderngl/moderngl-window).

Music player provided by [pyglet](https://github.com/pyglet/pyglet)

## Install

This project is using unreleased versions of pyglet and moderngl-window.
See `requirements.txt`.

Currently requires python 3.7.

```bash
$ pip install -e .
$ pip install -r requirements.txt
```

## Run

During installation the `beatsaber` command should be available.

```bash
$ beatsaber

# Optionally
python beatsaber\main.py
python -m beatsaber.main
```

## Controls

```
SPACE: Pause music
RIGHT: Skip 10 seconds forward
LEFT: Skip 10 seconds backwards
```

## Run tests

```
pytest
```

## Attributions

* Test song: https://bsaber.com/songs/63e1/
* Platforms by: https://bsaber.com/members/pixelguymm/
* Inspiration from: https://skystudioapps.com/bs-viewer/?id=63e1&difficulty=0
