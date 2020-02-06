# Track format

* Song: Megalovania - Camellia)
* Duration: 04:27 (267s)
* BPM: 242
* URL: https://skystudioapps.com/bs-viewer/?id=63e1&difficulty=0

Possible test song : https://www.youtube.com/watch?v=J6C8ehSdbm0

## Time

Time in events is in beats of the global bpm

## Event types

High event values refers to light colors.
For example `2002171391` is `0x7756b5ff` (purple).

https://github.com/Caeden117/ChroMapper/blob/master/Assets/__Scripts/Map/Events/MapEvent.cs#L12

```cpp
public const int EVENT_TYPE_BACK_LASERS = 0;
public const int EVENT_TYPE_RING_LIGHTS = 1;
public const int EVENT_TYPE_LEFT_LASERS = 2;
public const int EVENT_TYPE_RIGHT_LASERS = 3;
public const int EVENT_TYPE_ROAD_LIGHTS = 4;
//5
//6
//7
public const int EVENT_TYPE_RINGS_ROTATE = 8;
public const int EVENT_TYPE_RINGS_ZOOM = 9;
//10
//11
public const int EVENT_TYPE_LEFT_LASERS_SPEED = 12;
public const int EVENT_TYPE_RIGHT_LASERS_SPEED = 13;
public const int EVENT_TYPE_EARLY_ROTATION = 14;
public const int EVENT_TYPE_LATE_ROTATION = 15;

/*
* Light value constants
*/

public const int LIGHT_VALUE_OFF = 0;

public const int LIGHT_VALUE_BLUE_ON = 1;
public const int LIGHT_VALUE_BLUE_FLASH = 2;
public const int LIGHT_VALUE_BLUE_FADE = 3;

public const int LIGHT_VALUE_RED_ON = 5;
public const int LIGHT_VALUE_RED_FLASH = 6;
public const int LIGHT_VALUE_RED_FADE = 7;

public static readonly int[] LIGHT_VALUE_TO_ROTATION_DEGREES = { -60, -45, -30, -15, 15, 30, 45, 60 };
```

## Event Details

