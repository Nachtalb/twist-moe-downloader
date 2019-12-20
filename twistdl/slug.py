from twistdl.base import BaseTwistObject


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
