from json import load
from pprint import pprint
from datetime import datetime

import sys  # added!

sys.path.append("..")  # added!

from lib.MediaTracker import MovieId, MovieSeen, details

with open("./files/watched_movies.txt", "r") as f:
    movie_history: dict = load(f)

#    "watched_at": "2022-07-09T21:53:06.000Z",
for movie in movie_history:

    mt_id: int = MovieId(
        movie["movie"]["title"],
        tmdbId=movie["movie"]["ids"]["tmdb"],
        imdbId=movie["movie"]["ids"]["imdb"],
    )
    mt_info: dict = details(mt_id)

    if mt_info["seen"]:
      continue
   
    seen_time: int = (datetime.timestamp(
        datetime.strptime(movie["last_watched_at"], "%Y-%m-%dT%H:%M:%S.000Z")
    ) - 14400) * 1000

    print(MovieSeen(mt_id, seen_time))
    print(mt_id, movie['movie']['title'])

