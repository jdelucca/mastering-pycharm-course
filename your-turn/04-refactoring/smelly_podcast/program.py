from collections import namedtuple
from xml.etree import ElementTree

import requests

Episode = namedtuple('Episode', 'title link pubdate show_id')
episode_data = {}


def main():
    show_header()
    download_data('https://talkpython.fm/episodes/rss')

    # GET LATEST SHOW ID
    latest_show_id, oldest_show_id = get_show_id_range()

    print("Working with total of {} episodes".format(latest_show_id))

    # DISPLAY RESULTS
    display_results(latest_show_id, oldest_show_id)


def display_results(latest_show_id, oldest_show_id):
    start = oldest_show_id
    end = latest_show_id + 1
    for show_id in range(start, end):
        # GET EPISODE
        info = get_episode(show_id)
        print("{}. {}".format(info.show_id, info.title))


def get_episode(show_id):
    return episode_data.get(show_id)


def get_show_id_range():
    latest_show_id = max(episode_data.keys())
    oldest_show_id = min(episode_data.keys())
    return latest_show_id, oldest_show_id


def download_data(url):
    resp = requests.get(url)
    resp.raise_for_status()
    dom = ElementTree.fromstring(resp.text)
    episode_count = len(dom.findall('channel/item'))
    for idx, item in enumerate(dom.findall('channel/item')):
        episode = Episode(
            item.find('title').text,
            item.find('link').text,
            item.find('pubDate').text,
            episode_count - idx - 1
        )
        episode_data[episode.show_id] = episode


def show_header():
    print("Welcome to the talk python info downloader.")
    print()


if __name__ == '__main__':
    main()
