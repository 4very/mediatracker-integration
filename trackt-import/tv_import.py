from json import load
from pprint import pprint
from datetime import datetime

import sys  # added!

sys.path.append("..")  # added!

from lib.MediaTracker import TvId, ShowSeen, details

with open("./files/watched_shows.txt", "r") as f:
    show_history: dict = load(f)

#    "watched_at": "2022-07-09T21:53:06.000Z",
for show in show_history:

    mt_id: int = TvId(
        show["show"]["title"],
        tmdbId=show["show"]["ids"]["tmdb"],
        imdbId=show["show"]["ids"]["imdb"],
        traktId=show["show"]["ids"]["trakt"],
    )

    if mt_id == None: continue

    print(mt_id, show["show"]["title"])
    mt_info: dict = details(mt_id)

    if mt_info["seen"]:
        continue

    mt_show_seen_dict: dict = {}
    for season in mt_info["seasons"]:
        mt_show_seen_dict[season["seasonNumber"]] = {"id": season["id"]}
        for episode in season["episodes"]:
            mt_show_seen_dict[season["seasonNumber"]][episode["episodeNumber"]] = {
                "seen": episode["seen"],
                "id": episode["id"],
            }

    for season in show["seasons"]:
        season_id: int = season["number"]

        for episode in season["episodes"]:
            episode_id: int = episode["number"]

            if mt_show_seen_dict[season_id][episode_id]["seen"]:
                continue

            seen_time: int = (
                datetime.timestamp(
                    datetime.strptime(
                        episode["last_watched_at"], "%Y-%m-%dT%H:%M:%S.000Z"
                    )
                )
                - 14400
            ) * 1000

            print(
                ShowSeen(
                    mt_id,
                    seen_time,
                    mt_show_seen_dict[season_id]["id"],
                    mt_show_seen_dict[season_id][episode_id]["id"],
                )
            )
            print(mt_id, show["show"]["title"], season_id, episode_id)
