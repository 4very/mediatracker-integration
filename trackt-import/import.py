from json import load, loads, dump
from requests import get, exceptions
from pprint import pprint

#region generics
def mt_all_items(t):
    response = get(
        url="http://192.168.0.201:7481/api/items",
        params={
            "token": "AdHkIF_Cx75LmDC-4lGmHaGJRletpl",
            "mediaType": t
        },
    )

    return loads(response.content)

def mt_search(t, q):
    response = get(
        url="http://192.168.0.201:7481/api/search",
        params={
            "token": "AdHkIF_Cx75LmDC-4lGmHaGJRletpl",
            "mediaType": t,
            "q": q
        },
    )

    return loads(response.content)


def mt_details(id):
    response = get(
        url=f"http://192.168.0.201:7481/api/details/{id}",
        params={
            "token": "AdHkIF_Cx75LmDC-4lGmHaGJRletpl",
        },
    )

    return loads(response.content)

#endregion


#region Movie items
def mt_movie_items():
    return mt_all_items('movie')

def mt_movie_search(q):
    mt_search("movie", q)

def get_movie_mid(title, tmdbid = '', imdbid = ''):
    for item in mt_movie_items():
        if item['imdbId'] == imdbid or item['tmdbId'] == tmdbid:
            return item['id']
    
    for item in mt_movie_search(title):
        if item['imdbId'] == imdbid or item['tmdbId'] == tmdbid:
            return item['id']    
    
    return None
#endregion


#region tv functions
def mt_tv_items():
    return mt_all_items('tv')

def mt_tv_search(q):
    mt_search("tv", q)

def get_movie_mid(title, tmdbid = '', imdbid = ''):
    for item in mt_movie_items():
        if item['imdbId'] == imdbid or item['tmdbId'] == tmdbid:
            return item['id']
    
    for item in mt_movie_search(title):
        if item['imdbId'] == imdbid or item['tmdbId'] == tmdbid:
            return item['id']    
    
    return None
#endregion

with open('example.json', 'w') as f:
    dump(mt_details(74), f, indent=4)
pprint(mt_tv_items())

# with open("./files/history_shows.txt", 'r') as f:
#     pprint(load(f))