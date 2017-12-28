from __future__ import unicode_literals
import sys
import argparse
import Convertor
import youtube_dl
import YoutubeSong
from PlayListItemFilter import PlayListItemFilter
import logger


def getPlaylist(url):
    playlistOptions = {
        'ignoreerrors': 'True',
        'progress_hooks': [],
        'logger': logger.PlaylistLogger(),
    }
    with youtube_dl.YoutubeDL(playlistOptions) as ydl:
        return ydl.extract_info(url, download=False)


def downloadPlayList(playList, itemsFilter):
    if playList is None:
        print("Playlist not found or has no items")
        exit(1)
    for item in playList['entries']:
        try:
            if itemsFilter.checkItem(item) is False:
                continue
            getPlItem(item)
        except UnicodeEncodeError:
            print("UnicodeEncodeError during downloading video at Url: " + item['webpage_url'])
        except Exception as e:
            if not item['title'] is None:
                print("Error during downloading " + item['title'])
                print(e)
            else:
                print("Error during downloading item at " + item['webpage_url'])
                print("Exception caught " + str(e))
                continue


def download_hook(d):
    if d['status'] != 'downloading' and d['status'] != 'finished':
        print(d['status'])
    elif d['status'] == 'finished':
        print("Downloaded " + d['filename'])


def getPlItem(plItem):
    song = YoutubeSong.YouTubeSong()
    if not plItem['title'] is None:
        song.title = plItem['title']
    pl_title = plItem['playlist_title']
    out_tmp = "./" + pl_title + "/%(title)s.%(ext)s"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': out_tmp,
        'progress_hooks': [download_hook],
        'logger': logger.YoutubeLogger(),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        url = plItem['webpage_url']
        a = ydl.download([url])


def getUrl(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': './out/%(title)s.%(ext)s'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def getParameters():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('--path', help='path to download folder', default='./', dest='userPath')
    parser.add_argument('--search', nargs='*', help='Select the songs containing this keywords')
    parser.add_argument('--min',  type=int, default=0)
    parser.add_argument('--max', type=int, default=999)
    args = parser.parse_args()
    return args


itemsFilter = PlayListItemFilter()
userParams = getParameters()
itemsFilter.addFiltersFromArguments(userParams)
pl = getPlaylist(userParams.url)
downloadPlayList(pl, itemsFilter)
Convertor.convertDir(pl['title'])
