from __future__ import unicode_literals
import sys
import Convertor
import youtube_dl
import YoutubeSong
import logger


def getPlaylist(plUrl):
    playlistOptions = {
        'ignoreerrors': 'True',
        'progress_hooks': [],
        'logger': logger.PlaylistLogger(),
    }
    with youtube_dl.YoutubeDL(playlistOptions) as ydl:
        return ydl.extract_info(plUrl, download=False)


def downloadPlayList(playList):
    if playList is None:
        print("Playlist not found or has no items")
        exit(1)
    for item in playList['entries']:
        try:
            if item is None:
                continue
            getPlItem(item)
        except UnicodeEncodeError:
            print("UnicodeEncodeError during downloading video at Url: " + item['webpage_url'])
        except Exception as e:
            if not item['title'] is None:
                print("Error during downloading " + item['title'])
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


def checkParameters():
    if len(sys.argv) != 2:
        print("Add playlist url as second parameter")
        exit(1)


checkParameters()
pl = getPlaylist(sys.argv[1])
downloadPlayList(pl)
Convertor.convertDir(pl['title'])
