import json
import os
import re
import requests
import sys
import tqdm

from argparse import ArgumentParser
from decrypt import decrypt
from six.moves import input
from pathlib2 import Path


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


class Slug(BaseTwistObject):
    def __init__(self,
                 anime_id,
                 id,
                 slug,
                 updated_at=None,
                 **kwargs):
        super(Slug, self).__init__(**kwargs)

        self.anime_id = anime_id
        self.id = id
        self.slug = slug

        self.updated_at = updated_at

    @classmethod
    def de_json(cls, data, request, client):
        super(Slug, cls).de_json(data, request, client)
        return cls(client=client, request=request, **data)


class Anime(BaseTwistObject):
    def __init__(self,
                 title,
                 id,
                 ongoing,
                 alt_title=None,
                 mal_id=None,
                 hb_id=None,
                 season=None,
                 created_at=None,
                 updated_at=None,
                 slug=None,
                 **kwargs):
        super(Anime, self).__init__(**kwargs)

        self.title = title
        self.id = id
        self.alt_title = alt_title
        self.mal_id = mal_id
        self.hb_id = hb_id
        self.ongoing = ongoing
        self.season = season

        self.created_at = created_at
        self.updated_at = updated_at
        self.slug = slug

    @classmethod
    def de_json(cls, data, request, client):
        if not data:
            return None

        data = super(Anime, cls).de_json(data, request, client)
        data['slug'] = Slug.de_json(data['slug'], request, client)

        return cls(client=client, request=request, **data)

    def to_dict(self):
        data = super(Anime, self).to_dict()

        data['slug'] = self.slug.to_dict()
        return data


class TwistDL(object):
    base_url = 'https://twist.moe'
    api_path = 'api'

    default_api_token = '1rj2vRtegS8Y60B3w3qNZm5T2Q0TN2NR'
    default_source_key = 'LXgIVP&PorO68Rq7dTx8N^lP!Fa5sGJ^*XK'

    _animes = None

    def __init__(self, api_token=None, source_key=None):
        self.api_token = api_token or self.default_api_token
        self.source_key = source_key or self.default_source_key

        self.headers = {'x-access-token': self.api_token}

    def _request(self, endpoint, headers=None, data=None):
        data = data or {}
        headers = headers or {}

        built_url = f'{self.base_url}/{self.api_path}/{endpoint}'

        headers.update({'x-access-token': self.api_token})

        response = requests.get(url=built_url, data=data, headers=headers)
        response.raise_for_status()

        return response.json(), built_url

    def animes(self, hard_reload=False):
        if not self._animes or hard_reload:
            response_data, url = self._request(endpoint='anime')
            self._animes = list(map(lambda anime: Anime.de_json(anime, (url, {}), self), response_data))
        return self._animes

    def search_animes(self, title=None, slug=None):
        result = []

        title = (title or '').lower()
        slug = (slug or '').lower()

        for anime in self.animes():
            if title and title in anime.title.lower():
                result.append(anime)
                continue
            if slug and slug in anime.slug.slug:
                result.append(anime)
        return result
