from argparse import ArgumentParser, Namespace
from requests import Response
import sys  # added!

sys.path.append("..")  # added!

from lib.MediaTracker import MovieId, MovieSeenNow, ShowSeenNow, details, TvId


def AddMovieWatched(title, imdb_id="", themoviedb_id="", **_) -> Response | None:
    print(title, imdb_id, themoviedb_id)

    mt_id: int = MovieId(
        title,
        tmdbId=themoviedb_id,
        imdbId=imdb_id,
    )

    mt_info: dict = details(mt_id)

    if mt_info["seen"]:
        return

    return MovieSeenNow(mt_id)


def AddTvWatched(
    show_name, season_num, episode_num, thetvdb_id="", tvmaze_id="", **_
) -> Response | None:

    mt_id: int = TvId(
        show_name,
        tvdbId=thetvdb_id,
        tvmazeId=tvmaze_id,
    )

    mt_info: dict = details(mt_id)

    if mt_info["seen"]:
        return

    for season in mt_info["seasons"]:
        if season["seasonNumber"] != season_num:
            continue
        for episode in season["episodes"]:
            if episode["episodeNumber"] == episode_num:

                return ShowSeenNow(mt_id, season['id'], episode['id'])


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument("--media_type", required=True, type=str)
    parser.add_argument("--title", required=True, type=str)
    parser.add_argument("--imdb_id", type=str)

    ## movie arguments
    parser.add_argument("--themoviedb_id", type=int)

    ## tv arguments
    parser.add_argument("--show_name", type=str)
    parser.add_argument("--season_num", type=int)
    parser.add_argument("--episode_num", type=int)

    parser.add_argument("--thetvdb_id", type=int)
    parser.add_argument("--tvmaze_id", type=int)

    opts: dict = vars(parser.parse_args())
    print(opts['media_type'])

    if opts['media_type'] == 'show':
      AddTvWatched(**opts)
    if opts['media_type'] == 'movie':
      AddTvWatched(**opts)
    
    # AddMovieWatched(**opts)
