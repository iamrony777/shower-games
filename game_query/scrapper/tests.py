# import html module
from json import dumps
from lxml import html

# request.Session() == httpx.Client()
from httpx import Client

# fetch
with Client() as client:
    response = client.get("https://fitgirl-repacks.site/", params={"s": "House Party"})

    tree: html.HtmlElement = html.fromstring(
        html=response.content,
        base_url="https://fitgirl-repacks.site/",
        parser=html.HTMLParser(encoding="utf-8"),
    )

    data = {}
    for result in tree.findall(".//article"):
        data["name"] = result.find("header/h1[@class='entry-title']/a").text.encode("ascii", "ignore").decode()
        data["page"] = result.find("header/h1[@class='entry-title']/a").get("href")
        data["download"] = {}
        response = client.get(data["page"], follow_redirects=True)

        tree: html.HtmlElement = html.fromstring(
            html=response.content,
            base_url=data["page"],
            parser=html.HTMLParser(encoding="utf-8"),
        )

        for mirrors in tree.findall(".//div[@class='entry-content']/ul[1]/li"):
            for a in mirrors.findall(".//a"):
                if a.text == "1337x":
                    data["download"].update({"page_link": a.get("href")})
                if a.text == "magnet":
                    data["download"].update({"magnet": a.get("href")})
                if a.text == ".torrent file only":
                    data["download"].update({"torrent": a.get("href")})

        print(dumps(data, indent=2))
        exit(0)
