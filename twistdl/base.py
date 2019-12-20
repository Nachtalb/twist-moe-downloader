import json


class BaseTwistObject(object):

    def __init__(self, **kwargs) -> None:
        self.client = kwargs.get('client')
        self.request = kwargs.get('request')

    @classmethod
    def de_json(cls, data, request, client):
        if not data:
            return None

        data = data.copy()

        return data

    def to_json(self):
        """Return object as JSON

        Returns:
            :obj:`str`: JSON object reversed from the original request
        """

        return json.dumps(self.to_dict())

    def to_dict(self):
        data = dict()

        for key in iter(self.__dict__):
            if key in ('client', 'request'):
                continue

            value = self.__dict__[key]
            if value is not None:
                if hasattr(value, 'to_dict'):
                    data[key] = value.to_dict()
                else:
                    data[key] = value
        return data
