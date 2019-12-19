import json
import requests
import six

from decrypt import decrypt
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

    @property
    def anime(self):
        self.client.get_anime_by_id(self.anime_id)


class Anime(BaseTwistObject):

    _sources = None

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

    def sources(self, hard_reload=False):
        if not self._sources or hard_reload:
            self._sources = self.client.anime_sources(self)
        return self._sources


class Source(BaseTwistObject):

    _path = None

    def __init__(self,
                 anime_id,
                 id,
                 number,
                 source,
                 created_at=None,
                 updated_at=None,
                 slug=None,
                 **kwargs):
        super(Source, self).__init__(**kwargs)

        self.anime_id = anime_id
        self.id = id
        self.number = number
        self.source = source

        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def de_json(cls, data, request, client):
        if not data:
            return None

        data = super(Source, cls).de_json(data, request, client)

        return cls(client=client, request=request, **data)

    @property
    def anime(self):
        self.client.get_anime_by_id(self.anime_id)

    @property
    def url(self):
        return self.client.base_url + self.path

    @property
    def path(self):
        if not self._path:
            self._path = self.decrypt_url_path()
        return self._path

    def decrypt_url_path(self):
        encrypted = self.source.encode('utf-8')
        passphrase = self.client.source_key.encode('utf-8')

        decrypted_path = decrypt(encrypted, passphrase)
        path = decrypted_path.decode('utf-8').lstrip()

        return path

    def download_stream(self, file, **kwargs):
        return self.client.download_stream(self, file, **kwargs)


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

    def anime_sources(self, anime):
        endpoint = 'anime/{}/sources'.format(anime.slug.slug)

        response_data, url = self._request(endpoint=endpoint)
        return list(map(lambda source: Source.de_json(source, (url, {}), self), response_data))

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

    def get_anime_by_id(self, anime_id):
        return next(iter(filter(lambda anime: anime.id == anime_id, self.animes())), None)

    def download_stream(self, source, file, chunk_size=1024):
        """Download source to file and get download progress through generator

        Args:
            file: Can either be a pathlike obj, str or filelike obj

        Yield:
            Tuple like (chunks downloaded, total chunks)
        """
        file_obj = None
        if isinstance(file, Path):
            pass
        elif isinstance(file, six.string_types):
            file = Path(file)
        elif hasattr(file, 'write'):
            file_obj = file
        else:
            raise TypeError('File is neither pathlike, filelike or a sring')

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Referer': self.base_url
        }

        response = requests.get(source.url, headers=headers, stream=True)

        file_size = int(response.headers['Content-Length'])
        toatal_chunks = int(file_size / chunk_size)

        yield 0, toatal_chunks

        if file_obj:
            for chunks_downloaded, chunk in enumerate(response.iter_content(chunk_size=chunk_size), 1):
                file_obj.write(chunk)
                yield chunks_downloaded, toatal_chunks
        else:
            file.touch()
            with file.open('wb') as file_obj:
                for chunks_downloaded, chunk in enumerate(response.iter_content(chunk_size=chunk_size), 1):
                    file_obj.write(chunk)
                    yield chunks_downloaded, toatal_chunks
