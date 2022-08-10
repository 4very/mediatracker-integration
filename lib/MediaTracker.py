from inspect import stack
from json import loads, dump
from os import environ
from requests import get, put, Response
from dotenv import load_dotenv

from pprint import pprint

load_dotenv()

url = environ.get("MT_BASE_URL")
token = environ.get("MT_TOKEN")


def __baseRequest(urlext, header={}) -> dict:
    response = get(url="{}{}".format(url, urlext), params={**header})
    return loads(response.content)


def __baseAuthRequest(urlext, header={}) -> dict:
    return __baseRequest(urlext, {"token": token, **header})


def __mediaTypeRequest(url, mediaType, header={}) -> dict:
    return __baseAuthRequest(url, {"mediaType": mediaType, **header})


def __basePut(urlext, header={}) -> Response:
    response: Response = put(
        url="{}{}".format(url, urlext), params={"token": token, **header}
    )
    return response


def __items(mediatype) -> dict:
    return __mediaTypeRequest("/api/items", mediatype)


def details(itemid) -> dict:
    return __baseAuthRequest("/api/details/{}".format(itemid))


def __search(mediatype, query) -> dict:
    return __mediaTypeRequest("/api/search", mediatype, {"q": query})


def __joinArgs(local, defargs) -> dict:
    joins: dict = {}
    for key in defargs.keys():
        joins[key] = local[key]
    return joins


def __getId(title, mediatype, local, defargs) -> int:
    args: dict = __joinArgs(local, defargs)
    search: dict = __search(mediatype, title)

    for item in search:
        for key, val in args.items():
            if key in item and item[key] == val:
                return item["id"]

    return None


def TvId(title, *args, tvdbId=0, traktId=0, tvmazeId=0, imdbId="", tmdbId=0) -> int:
    return __getId(title, "tv", locals(), TvId.__kwdefaults__)


def MovieId(title, *args, imdbId="", tmdbId=0, traktId=0) -> int:
    return __getId(title, "movie", locals(), MovieId.__kwdefaults__)


def AudiobookId(title, *args, audibleId=0, goodreadsId=0) -> int:
    return __getId(title, "audiobook", locals(), AudiobookId.__kwdefaults__)


def BookId(title, *args, audibleId=0, goodreadsId=0) -> int:
    return __getId(title, "book", locals(), BookId.__kwdefaults__)


def GameId(title, *args, igdbId=0) -> int:
    return __getId(title, "video_game", locals(), GameId.__kwdefaults__)


def MovieSeen(mtid, date) -> Response:
    return __basePut(
        "/api/seen", {"mediaItemId": mtid, "lastSeenAt": "custom_date", "date": date}
    )

def MovieSeenNow(mtid) -> Response:
    return __basePut(
        "/api/seen", {"mediaItemId": mtid, "lastSeenAt": "now"}
    )

def ShowSeen(mtid, date, seasonNum, epNum) -> Response:
    return __basePut(
        "/api/seen",
        {
            "mediaItemId": mtid,
            "lastSeenAt": "custom_date",
            "date": date,
            "seasonId": seasonNum,
            "episodeId": epNum,
        },
    )


def ShowSeenNow(mtid, seasonNum, epNum) -> Response:
    return __basePut(
        "/api/seen",
        {
            "mediaItemId": mtid,
            "lastSeenAt": "now",
            "seasonId": seasonNum,
            "episodeId": epNum,
        },
    )

if __name__ == "__main__":
    with open("example.json", "w") as f:
        dump(details(TvId("lost", imdbId="tt0411008")), f, indent=4)
    
    pprint(__search('tv', 'severance'))
