from six.moves import filter
from twistdl import Slug
from twistdl.base import BaseTwistObject


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

    def fetch_sources(self):
        self._sources = self.client.anime_sources(self)

    @property
    def sources(self):
        if not self._sources:
            self.fetch_sources()
        return self._sources

    episodes = sources

    @property
    def slug_name(self):
        if not self.slug:
            return
        return self.slug.slug

    @property
    def total_episodes(self):
        return len(self.sources)

    @property
    def first_episode(self):
        return self.sources[0]

    @property
    def last_episode(self):
        return self.sources[-1]

    def episode(self, number):
        return next(iter(filter(lambda source: source.number == number, self.sources)), None)
