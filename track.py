import json
from enum import Enum


class EventType(Enum):
    BACK_LASERS = 0
    RING_LIGHTS = 1
    LEFT_LASERS = 2
    RIGHT_LASERS = 3
    ROAD_LIGHTS = 4
    RINGS_ROTATE = 8
    RINGS_ZOOM = 9
    LEFT_LASERS_SPEED = 12
    RIGHT_LASERS_SPEED = 13
    EARLY_ROTATION = 14
    LATE_ROTATION = 15


class LightValue(Enum):
    OFF = 0
    BLUE_ON = 1
    BLUE_FLASH = 2
    BLUE_FADE = 3
    RED_ON = 5
    RED_FLASH = 6
    RED_FADE = 7

LIGHT_VALUE_TO_ROTATION_DEGREES = [-60, -45, -30, -15, 15, 30, 45, 60]


class BSTrack:

    def __init__(self, filename):
        self.filename = filename
        self.channels = {e.value: BSChannel(e) for e in EventType}
        self.data = self._load()

    def get_channel(self, type):
        return self.channels[type]

    def _load(self):
        with open(self.filename, mode='r') as fd:
            data = json.load(fd)

        for event in data['_events']:
            try:
                event_type = EventType(event['_type'])
            except ValueError as ex:
                raise ValueError("Event type {} not supported".format(event['_type']))

            channel = self.channels.get(event_type.value)
            if not channel:
                print("Event {} not supported".format(event_type.value))
                continue

            channel.add_event(BSEvent(
                event_type,
                int(event['_time'] * 1000 / (267 / 60)),
                event['_value']
            ))

        return data


class BSChannel:

    def __init__(self, event_type):
        self.event_type = event_type
        self.events = []

    def get_value(self, time: int):
        index = bisect.bisect_left(self.events, time)
        return self.events[index].value

    def add_event(self, event):
        self.events.append(event)


class BSEvent:

    def __init__(self, type, time, value):
        self.type = type
        self.time = time
        self.value = value

    def __lt__(self, other):
        return self.time < other.time

    def __ge__(self, other):
        return self.time > other.time
