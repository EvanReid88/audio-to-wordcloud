import speech_recognition as sr
import nltk
from wordcloud import WordCloud as wc

from os import walk
import os

import youtube_dl

# TODO get directory using python commands
data_path = "/home/Projects/audio-noun-extract/data"

# TODO change to mono channel audio
# TODO change bitrate to sphinx
def youtubeToWav(url):
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

youtubeToWav("https://www.youtube.com/watch?v=_czhNhBXOD0")

#audio_file = sr.AudioFile('harvard.wav')

for (dirpath, dirnames, filenames) in walk(data_path):
    audio_file = sr.AudioFile(data_path + "/" + filenames[0])
    break


# TODO allow user to enter start and stopping time on video
# use record(audio, offset=X, duration=X)
with audio_file as source:
    r.adjust_for_ambient_noise(source)
    audio = r.record(source)

# TODO remove temp files
#os.remove(data_path + "/" + filenames[0])

audio_text = r.recognize_sphinx(audio)

# extracting plural and non plural nouns and proper nouns.
word_types = ['NN', 'NNS', 'NNP', 'NNPS']

# function to test if something is a noun
is_noun = lambda pos: pos[:2] in word_types

# extract tokenized words
tokenized_text = nltk.word_tokenize(audio_text)
print(nltk.pos_tag(tokenized_text))

# extract nouns from list of tokenized words
nouns = [word for (word, pos) in nltk.pos_tag(tokenized_text) if is_noun(pos)]

# filter out any words with a single character
nouns = filter(lambda x: len(x) > 1, nouns)

# join nouns into a single string
nouns_text = " ".join(nouns)
print(nouns)

# generate wordcloud from nouns
wordcloud = wc(background_color="white").generate(nouns_text)

# Display the generated wordcloud
import matplotlib.pyplot as plt
plt.figure()
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()