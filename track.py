import json


class BSTrack:

    def __init__(self, filename):
        self.filename = filename
        self.data = self._load()

    def _load(self):
        with open(self.filename, mode='r') as fd:
            data = json.load(fd)

        types = set()
        for event in data['_events']:
            types.add(event['_type'])

        # print(types)

        return data
