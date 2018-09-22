import requests
import json
from pprint import pprint as pp
import urllib
import config as cfg
import os


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def getAllAudiobooks():
    audiobooks = []

    url = "https://iceportal.de/api1/rs/pages/hoerbuecher_und_hoerspiele"
    response = requests.get(url, headers=cfg.headers)

    # extract titles
    json_data = json.loads(response.text)
    items = json_data["teasersMain"]["items"]

    for item in items:
        name = str(item["navigation"]["href"])[28:]
        audiobooks.append(name)

    return audiobooks


def downloadAudiobook(title):
    print("Downloading audiobook: {}".format(title))

    url = "https://iceportal.de/api1/rs/pages/hoerbuecher_und_hoerspiele/{}".format(
        title)
    responseChapter = requests.get(url, headers=cfg.headers)

    # extract chapters
    json_data = json.loads(responseChapter.text)
    playlist = json_data["modules"]["playlist"]

    # extract downloadPath for each chapter
    downloadPath = []
    for chapter in playlist:
        chapterPath = chapter["path"]

        url = "https://iceportal.de/api1/rs/audiobooks/path{}".format(
            chapterPath)
        responseDownloadPath = requests.get(
            url, headers=cfg.headers, cookies=cfg.cookies)

        path = json.loads(responseDownloadPath.text)["path"]
        downloadPath.append(path)

    createFolder('./audiobooks/{}'.format(title))

    # download each track
    for counter, track in enumerate(downloadPath):
        print("{}/{}".format(counter+1, len(downloadPath)))

        url = "https://iceportal.de{}".format(track)
        audio = requests.get(url)

        savePath = "audiobooks/{}/{}_".format(title,
                                              title)+str(counter+1)+".mp3"
        with open(savePath, "wb+") as code:
            code.write(audio.content)


# MAIN
# extract all audiobooks
audiobooks = getAllAudiobooks()
createFolder('./audiobooks')

# download all audibooks
for book in audiobooks:
    downloadAudiobook(str(book))
