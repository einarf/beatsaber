import bisect
from enum import Enum

from moderngl_window import resources
from moderngl_window.meta import DataDescription


class EventType(Enum):
    """Beat Saber event types"""
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
    """Beat Saber light event types"""
    OFF = 0
    BLUE_ON = 1
    BLUE_FLASH = 2
    BLUE_FADE = 3
    RED_ON = 5
    RED_FLASH = 6
    RED_FADE = 7


LIGHT_VALUE_TO_ROTATION_DEGREES = [-60, -45, -30, -15, 15, 30, 45, 60]
LIGHT_EVENTS = [
    EventType.BACK_LASERS,
    EventType.RING_LIGHTS,
    EventType.LEFT_LASERS,
    EventType.RIGHT_LASERS,
    EventType.ROAD_LIGHTS,
]
LASER_SPEED_EVENTS = [EventType.LEFT_LASERS_SPEED, EventType.RIGHT_LASERS_SPEED]


class BSTrack:

    def __init__(self, filename, bpm):
        self.filename = filename
        self.bpm = bpm
        self.channels = {e.value: BSChannel(e) for e in EventType}
        self._load()

    def get_channel(self, type):
        return self.channels[type]

    def get_value(self, channel, time):
        channel = self.channels[channel.value]
        return channel.get_value(time)

    def _load(self):
        data = resources.data.load(DataDescription(self.filename, kind='json'))

        for event in data['_events']:
            try:
                event_type = EventType(event['_type'])
            except ValueError:
                print("Event type {} not supported".format(event['_type']))
                continue
                # raise ValueError("Event type {} not supported".format(event['_type']))

            channel = self.channels.get(event_type.value)
            if not channel:
                # print("Event {} not supported".format(event_type.value))
                continue

            # Transform events if needed for easy access
            value = event['_value']
            # If value is greater or equal to 255 we are dealing with a color value
            # FIXME: We discard these events for now
            if value >= 255 and event_type.value < 5:
                continue

            channel.add_event(BSEvent(
                event_type,
                int(event['_time'] * 1000 / (self.bpm / 60)),
                value,
            ))

        # Ensure all channels have events sorted by time
        for channel in self.channels.values():
            channel.sort()


class BSChannel:

    def __init__(self, event_type):
        self.event_type = event_type
        self.events = []
        self.current_color = (1.0, 1.0, 1.0, 1.0)

    def sort(self):
        self.events.sort()

    def get_value(self, time: int):
        if len(self.events) == 0:
            return 0, 0
        index = bisect.bisect_left(self.events, time)
        if index >= len(self.events):
            index = len(self.events) - 1
        event = self.events[index]
        if time < event.time:
            if index <= 0:
                if event.type in LIGHT_EVENTS:
                    return (0, 0, 0, 0), 0
                elif event.type == EventType.RINGS_ROTATE:
                    return 0, 0
                elif event.type == EventType.RINGS_ZOOM:
                    return 0, 0
                elif event.type in LASER_SPEED_EVENTS:
                    return 0, 0
                else:
                    return None
            else:
                event = self.events[index - 1]

        color = None
        if event.type in LIGHT_EVENTS:
            # Lights off
            if event.value == 0:
                color = (0, 0, 0, 0)
            # Blue lights on
            elif event.value == 1:
                color = (0, 0, 1, 1)
            # Blue flash
            elif event.value == 2:
                color = (0, 0, 1.0 - (time - event.time)/500, 1)
            # Blue Fade (3s)
            elif event.value == 3:
                color = (0, 0, 1.0 - (time - event.time)/2000, 1)
            # Red lights on
            elif event.value == 5:
                color = (1, 0, 0, 1)
            # Red flash
            elif event.value == 6:
                color = (1.0 - (time - event.time)/1000, 0, 0, 1)
            # Red fade (3s)
            elif event.value == 7:
                color = (1.0 - (time - event.time)/2500, 0, 0, 1)

            return color, event.time
        elif event.type == EventType.RINGS_ROTATE:
            return event.time, event.value
        elif event.type == EventType.RINGS_ZOOM:
            if index < len(self.events) - 1:
                next_event = self.events[index + 1]
                value = (time - event.time) / (next_event.time - event.time)
                return event.time, value
            return event.type, 0
        elif event.type in LASER_SPEED_EVENTS:
            return event.time, event.value
        else:
            return None

    def add_event(self, event):
        self.events.append(event)


class BSEvent:

    def __init__(self, type, time, value):
        self.type = type
        self.time = time
        self.value = value

    def __lt__(self, other):
        if isinstance(other, int):
            return self.time < other
        elif isinstance(other, BSEvent):
            return self.time < other.time

    def __ge__(self, other):
        if isinstance(other, int):
            return self.time > other
        elif isinstance(other, BSEvent):
            return self.time > other.time

    def __repr__(self):
        return "<BSEvent type={} time={} value={}".format(
            self.type, self.time, self.value)
