import json
import collections

genresSet = collections.defaultdict(int)

class Song:
    title = ''
    length = ''
    artist = ''
    genres = []
    mood = ''
    download_link = ''

    def __init__(self, data):
        global genresSet
        data[3] = data[3].split(' & ')
        if 'Country and Folk' in data[3] or 'Country Folk' in data[3]: data[3] = ['Country', 'Folk']
        for genre in data[3]:
            genresSet[genre] += 1
        if len(data) == 5:
            self.title = data[0]
            self.length = data[1]
            self.artist = data[2]
            self.genres = data[3]
            self.download_link = data[4]
        elif len(data) == 6:
            self.title = data[0]
            self.length = data[1]
            self.artist = data[2]
            self.genres = data[3]
            self.mood = data[4]
            self.download_link = data[5]

    def __str__(self):
        return str(self.__dict__)

    def dict(self):
        return self.__dict__


songs = []

songDataBuffer = []

for line in open('songdata.txt', 'r').readlines():
    if line == '\n':
        songs.append(Song(songDataBuffer))
        songDataBuffer = []
    else: songDataBuffer += [line.strip()]

outfile = open('songdata.json', 'w+')
for song in songs:
    outfile.write(json.dumps(song.__dict__, indent=4) + ',\n')

print(genresSet)
print(len(genresSet))