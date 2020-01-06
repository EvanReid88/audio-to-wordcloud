import speech_recognition as sr
import nltk
from wordcloud import WordCloud as wc

from os import walk
import os

import youtube_dl

data_path = "/home/Projects/audio-noun-extract/data"

def youtubeToWav(url):
    data_path = "./data"
    os.chdir(data_path)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
           'key': 'FFmpegExtractAudio',
           'preferredcodec': 'wav',
           'preferredquality': '192',
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        filenames = [url]
        ydl.download(filenames)
    os.chdir("/home/Projects/audio-noun-extract")
    

r = sr.Recognizer()

youtubeToWav("https://www.youtube.com/watch?v=iRXXnMJH0kQ")

#audio_file = sr.AudioFile('harvard.wav')

for (dirpath, dirnames, filenames) in walk(data_path):
    audio_file = sr.AudioFile(data_path + "/" + filenames[0])
    break

# TODO allow user to enter start and stopping time on video
# use recognize_sphinx(audio, offset=X, duration=X)
with audio_file as source:
    r.adjust_for_ambient_noise(source)
    audio = r.record(source)

#os.remove(data_path + "/" + filenames[0])

# TODO use reliable text to speech
audio_text = r.recognize_sphinx(audio)

# function to test if something is a noun
is_noun = lambda pos: pos[:2] == 'NN'

# extract tokenized words
tokenized_text = nltk.word_tokenize(audio_text)
print(tokenized_text)

# extract nouns from list of tokenized words
nouns = [word for (word, pos) in nltk.pos_tag(tokenized_text) if is_noun(pos)]
nouns_text = " ".join(nouns)
print(nouns)

wordcloud = wc().generate(nouns_text)

# Display the generated wordcloud
import matplotlib.pyplot as plt
plt.figure()
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()