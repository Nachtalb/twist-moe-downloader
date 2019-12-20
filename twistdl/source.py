from twistdl.base import BaseTwistObject
from twistdl.decrypt import decrypt


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
