import os
from httpx import Client
from game_query.lib.prowlarr import search
from game_query import env


class Rawg:
    """Fetch data from api.rawg.io"""

    def __init__(self) -> None:
        self.apiKey = env("RAWG_APIKEY")
        self.client = Client(
            base_url="https://api.rawg.io/api", params={"key": self.apiKey}
        )

    def games(self, query: str) -> dict:
        response = self.client.get(
            "/games", params={"search": query, "page_size": 1}
        ).json()
        if len(response["results"]):
            game: dict = response["results"][0]
            response, _torrents = {}, []
            _torrent = search(game["name"])

            if isinstance(_torrent, list):
                for t in _torrent:
                    _torrents.append(
                        {
                            "name": t.description.decode("utf-8"),
                            "mediaType": t.media_type,
                            "seeders": t.seeders,
                            "leechers": t.leechers,
                            "ratio": t.ratio,
                            "link": t.download,
                        }
                    )
                torrent = _torrents
            else:
                torrent = {
                    "name": _torrent.description.decode("utf-8"),
                    "mediaType": _torrent.media_type,
                    "seeders": _torrent.seeders,
                    "leechers": _torrent.leechers,
                    "ratio": _torrent.ratio,
                    "link": _torrent.download,
                }

            response.update(
                {
                    "name": game["name"],
                    "backgroundImage": game["background_image"],
                    "released": game["released"],
                    "rating": game["rating"],
                    "genres": [genres["name"] for genres in game["genres"]],
                    "downloadLink": torrent,
                }
            )
        return response


if __name__ == "__main__":
    rawg = Rawg()
    from json import dumps

    print(dumps(rawg.games("Forza Horizon 4 Ultimate edition"), indent=2))
