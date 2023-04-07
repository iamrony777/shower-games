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
    url = "/indexers/all/results"
    torrents = []
    client = Client(
        base_url=env("JACKETT_API_URL"),
        params={
            "Category": "4050",
            "Tracker": ["1337x", "rarbg", "thepiratebay", "limetorrents", "bt4g"],
            "apikey": env("JACKETT_API_KEY")
        },
        headers={"Accept": "application/json"},
        verify=False
    )

    res =  client.get(url, params={"Query": query}, timeout=60).json()
    id = 1
    for r in res['Results']:
        download_url = r['MagnetUri'] if r['MagnetUri'] else r['Link']
        torrents.append(torrent(id, r['Title'].encode(
            'ascii', errors='ignore'), r['CategoryDesc'], r['Seeders'], r['Peers'], download_url, r['Size']))
        id += 1    

    # Sort torrents array
    sort_torrents(torrents, "seeders")

    for t in torrents:
        if query in t.description.decode("utf-8") and top_encoder(t.description.decode("utf-8")):
            return t

    # for t in torrents:
        # if top_encoder(t.description.decode("utf-8")):

            # return t # return only 1st result, sorted by seeders
    return torrents[0:5] if len(torrents) >= 1 else {}
        



if __name__ == "__main__":
    print(search("Forza Horizon 4 Delux edition"))