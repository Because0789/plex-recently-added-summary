"""
    Use Examples:
        python plex_summary.py
            - Defaults to everything
            - 1 Day(1)
            - All notifiers(a)
            - 200 max tv show episodes(200)
            - 50 max movies(50)
            - 2 detailed tv episodes per show(2)
            - Don't test the script without sending the notifications(0)

        python plex_summary.py -d 5 -n fp -tv 500 -m 100 -nd 5 -t 1
            - Checks 5 days previous(-d 5)
            - Both Facebook and Pushbullet(-n fp)
            - Fetch the last 500 episodes added to the server to check(-tv 500)
            - Fetch the last 100 movies added to the server to check(-m 100)
            - Show the details for up to 5 episodes in each show before summarizing(-nd 5)
            - Don't send the notifications, instead print out the message created and other info,
              works with any non-zero(-t 1)
"""

import argparse
import datetime
import json
import os
import time
import sys
from collections import namedtuple
from facepy import GraphAPI
from itertools import groupby
from plexapi.myplex import MyPlexAccount
from pushbullet import Pushbullet

NOTIFIERS = ['a', 'f', 'p', 'e']
DATA_PATH = '/data'
SETTINGS_FILE = 'settings.json'
LOG_FILE = 'log.txt'

Settings = namedtuple('Settings', ['plex_username', 'plex_password', 'plex_servername', 'movie_library',
                                   'tvshow_library', 'pushbullet_apikey', 'fb_accesstoken', 'fb_groupid',
                                   'default_notifier'])

Episode = namedtuple('Episode', ['show_name', 'season_num00', 'episode_num00', 'episode_name'])
Season = namedtuple('Season',   ['show_name', 'season_num00', 'episodes', 'num_episodes'])
Show = namedtuple('Show',       ['show_name', 'seasons', 'num_episodes'])


def read_settings(_file_path):
    filename = '{0}/{1}/{2}'.format(_file_path, DATA_PATH, SETTINGS_FILE)
    with open(filename) as data_file:
        json_data = json.load(data_file)
        return Settings(
            json_data['plex_username'], json_data['plex_password'], json_data['plex_servername'],
            json_data['movie_library'], json_data['tvshow_library'], json_data['pushbullet_apikey'],
            json_data['fb_accesstoken'], json_data['fb_groupid'], json_data['default_notifier'])


def parse_intro(_days, _settings):
    # Different intros based on the number of days to summarize.
    if _days == 1:
        intro_ = 'The Daily Summary'
    else:
        intro_ = 'The Summary of the past {0} days'.format(str(_days))
    intro_ += ' of recently added Movies and TV Shows from {0}:\n'.format(_settings.plex_servername)
    return intro_


def parse_movies(_movies):
    # Check to see if we have any movies.
    if len(_movies) == 0:
        return 'No Movies Added.\n'
    else:
        movie_str_ = 'Movies:\n'
        # Loops through the movies concatenating the movie title and year
        for movie_item in _movies:
            movie_str_ += '-{0} ({1})\n'.format(movie_item.title, str(movie_item.year))
        return movie_str_


def parse_tvshows(_shows, _num_detailed):
    # Check to see if we have any movies.
    if len(_shows) == 0:
        return 'No Shows Added.'
    else:
        tvshow_str_ = 'TV Shows:\n'
        for show_item in _shows:
            tvshow_str_ += '-' + show_item.show_name + '-\n'
            # If the show has num_detailed or less shows added
            if show_item.num_episodes <= _num_detailed:
                # List out each individual episode with Show Name SXXEXX - Episode Name
                for season_item in show_item.seasons:
                    for episode_item in season_item.episodes:
                        tvshow_str_ += '--{0} S{1}E{2} - {3}\n'.format(
                            episode_item.show_name,
                            episode_item.season_num00,
                            episode_item.episode_num00,
                            episode_item.episode_name)
            else:
                # Otherwise just list how many episodes were added per season.
                for season_item in show_item.seasons:
                    tvshow_str_ += '--{0} episodes added in Season {1}.\n'.format(
                        str(season_item.num_episodes), season_item.season_num00)
        return tvshow_str_


def group_into_shows(_episodes):
    # Sort the list before groupby, otherwise bad things happen.
    sorted_episodes = sorted(_episodes, key=lambda x: (x.show_name.lower(), x.season_num00, x.episode_num00))
    lst_shows_ = []
    # Group the episodes by show
    for key, group in groupby(sorted_episodes, key=lambda x: x.show_name.lower()):
        lst_seasons = []
        grp_lst = list(group)
        # Group the episodes grouped into each show into seasons and add each group as a season in the current show
        for subkey, subgroup in groupby(grp_lst, key=lambda x: x.season_num00):
            grp_lst2 = list(subgroup)
            lst_seasons.append(Season(key, subkey, grp_lst2, len(grp_lst2)))
        # Add a show to the list with all the bits grouped up properly
        lst_shows_.append(Show(key, lst_seasons, len(grp_lst)))
    return lst_shows_


def send_pushbullet(_message, _settings):
    if _message is None:
        return
    # send
    Pushbullet(_settings.pushbullet_apikey).push_note('{0} Summary'.format(_settings.plex_servername), _message)


def post_facebook(_message, _settings):
    graph = GraphAPI(_settings.fb_accesstoken)
    graph.post(path='{0}/feed'.format(str(_settings.fb_groupid)), message=_message)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Post to a Facebook Group and/or send a Pushbullet notification with "
                                                 + "what was added to Plex within a certain time frame")
    parser.add_argument('-d', '--days', help='Time frame for which to check recently added to Plex.',
                        required=False, type=int, default=1)
    parser.add_argument('-n', '--notifiers', help='Which notification services to used, concatenated for multiple.  '
                                                  'Refer to documentation for full list. Default:a(all)',
                        required=False, default='a')
    parser.add_argument('-m', '--max_movies', help='Maximum number of movies to grab, default:50',
                        required=False, type=int, default=50)
    parser.add_argument('-tv', '--max_tv', help='Maximum number of episodes to grab, default:200',
                        required=False, type=int, default=200)
    parser.add_argument('-nd', '--num_detailed',
                        help='Maximum number of episodes to detail before collapsing down by season, default:2',
                        required=False, type=int, default=2)
    parser.add_argument('-t', '--test', help='If testing set to 1, otherwise 0.  Default is 0', required=False,
                        type=int, default=0)

    opts = parser.parse_args()

    # Grab the arguments/defaults
    num_days = opts.days
    notifiers = opts.notifiers
    max_movies = opts.max_movies
    max_tv = opts.max_tv
    num_detailed = opts.num_detailed
    test = opts.test

    # Read in the settings from the settings.json
    file_path = os.path.dirname(sys.argv[0])
    settings = read_settings(file_path)
    # Make sure the "default" is actually a valid option
    if not any(notif in settings.default_notifier for notif in NOTIFIERS):
        settings.default_notifier = 'a'

    # Create the times
    TODAY = int(time.time())
    LASTDATE = int(TODAY - num_days * 24 * 60 * 60)
    today_datetime = datetime.datetime.fromtimestamp(TODAY)
    lastdate_datetime = datetime.datetime.fromtimestamp(LASTDATE)

    # Get the Plex Server object
    account = MyPlexAccount.signin(settings.plex_username, settings.plex_password)
    plex = account.resource(settings.plex_servername).connect()

    # Get the Movies and TV sections of the library
    movies_section = plex.library.section(settings.movie_library)
    tvshows_section = plex.library.section(settings.tvshow_library)

    # Get the recently added movies and tv episodes
    movies = movies_section.recentlyAdded(max_movies)
    episodes = tvshows_section.recentlyAdded('episode', max_tv)

    # Filter the episodes based on the passed in time frame
    filtered_episodes = []
    for episode in episodes:
        if lastdate_datetime <= episode.addedAt <= today_datetime:
            filtered_episodes.append(Episode(episode.grandparentTitle, str(episode.parentIndex).zfill(2),
                                             str(episode.index).zfill(2), episode.title))

    # Filter the movies based on the passed in time frame
    filtered_movies = []
    for movie in movies:
        if lastdate_datetime <= movie.addedAt <= today_datetime:
            filtered_movies.append(movie)

    # If there are any episodes that have been added with the time frame sort them into shows
    shows = []
    if len(filtered_episodes) > 0:
        shows = group_into_shows(filtered_episodes)

    # Create the message for the post/push
    message = parse_intro(num_days, settings)
    message += parse_movies(filtered_movies)
    message += parse_tvshows(shows, num_detailed)

    if test == 0:
        # If the notify arg is invalid set it to both
        if not any(notif in notifiers for notif in NOTIFIERS):
            notifiers = settings.default_notifier

        # If the notify arg is PushBullet or both send PushBullet
        if 'p' in notifiers or 'a' in notifiers:
            send_pushbullet(message, settings)

        # If the notify arg is FB or both make the FB post
        if 'f' in notifiers or 'a' in notifiers:
            post_facebook(message, settings)

        # TODO: Send email.
        # If the notify arg is FB or both make the FB post
        # if 'e' in notifiers or 'a' in notifiers:
            # send_email(message)
    else:
        print num_days
        print notifiers
        print max_movies
        print max_tv
        print num_detailed
        print test
        print message
