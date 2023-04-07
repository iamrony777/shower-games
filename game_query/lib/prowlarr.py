from httpx import Client
from game_query import env

class torrent:
    def __init__(self, id, description, media_type, seeders, leechers, download, size):
        self.id = id
        self.media_type = media_type
        self.description = description
        self.seeders = seeders
        self.leechers = leechers
        self.download = download
        if(leechers > 0):
            self.ratio = self.seeders / self.leechers
        else:
            self.ratio = self.seeders
        self.size = size / 1000

def sort_torrents(torrents, sort: str):
    if sort == "seeders":
        return torrents.sort(key=lambda x: x.seeders, reverse=True)
    if sort == "leechers":
        return torrents.sort(key=lambda x: x.leechers, reverse=True)
    if sort == "size":
        return torrents.sort(key=lambda x: x.size, reverse=True)
    if sort == "ratio":
        return torrents.sort(key=lambda x: x.ratio, reverse=True)
    if sort == "description":
        return torrents.sort(key=lambda x: x.description, reverse=True)

def top_encoder(title: str):
    for encoder in env("ENCODERS"):
        if encoder.lower() in title.lower():
            return True
    return False

def search(query: str) -> torrent:
    url = "/api/v1/search"
    torrents = []
    client = Client(
        base_url=env("PROWLARR_APIHOST"),
        params={
            "categories": 4000,
            # "categories": 1000,
            "type": "search",
            "limit": env("PROWLARR_SEARCH_LIMIT")
        },
        headers={"Accept": "application/json", "x-api-key": env("PROWLARR_APIKEY")},
        verify=False
    )

    res =  client.get(url, params={"query": query}, timeout=10).json()
    id = 1
    for r in res:
        download_url = r['downloadUrl'] if 'downloadUrl' in r else r['magnetUrl']
        torrents.append(torrent(id, r['title'].encode(
            'ascii', errors='ignore'), r['categories'][0]["name"], r['seeders'], r['leechers'], download_url, r['size']))
        id += 1    

    # Sort torrents array
    sort_torrents(torrents, "seeders")

    for t in torrents:
        if query in t.description.decode("utf-8") and top_encoder(t.description.decode("utf-8")):
            return t

    for t in torrents:
        if top_encoder(t.description.decode("utf-8")):
            return t # return only 1st result, sorted by seeders

    return torrents[0:5] if len(torrents) >= 1 else {}
    # return torrents
        # 



if __name__ == "__main__":
    print(search("Forza Horizon 4"))