import speech_recognition as sr
import matplotlib.pyplot as plt
from wordcloud import WordCloud as wc
from pydub import AudioSegment 
import nltk
# ffmpeg, pocketsphinx required

from os import walk
import os

import youtube_dl

data_path = os.getcwd()

# TODO get directory using python commands

def extract_nouns(text):
    # extracting plural and non plural nouns and proper nouns.
    word_types = ['NN', 'NNS', 'NNP', 'NNPS']

    # function to test if something is a noun
    is_noun = lambda pos: pos[:2] in word_types

    # extract tokenized words
    tokenized_text = nltk.word_tokenize(audio_text)

    # extract nouns from list of tokenized words
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized_text) if is_noun(pos)]

    # filter out any words with a single character
    nouns = filter(lambda x: len(x) > 1, nouns)

    # join nouns into a single string
    return " ".join(nouns)


def youtube_to_wav(url, out_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': data_path + '/data/test.webm', # TODO '/tmp/foo_%(title)s-%(id)s.%(ext)s'
        'postprocessors': [{
           'key': 'FFmpegExtractAudio',
           'preferredcodec': 'wav',
           'preferredquality': '192',
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        filenames = [url]
        ydl.download(filenames)
    
    audio = AudioSegment.from_wav(data_path + "/data/test.wav")
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
    audio.export(data_path + "/data/" + "test.wav", format="wav")
    
r = sr.Recognizer()

youtube_to_wav("https://www.youtube.com/watch?v=UTm3Q0giBY4", data_path)

for (dirpath, dirnames, filenames) in walk(data_path + "/data/"):
    audio_file = sr.AudioFile(data_path + "/data/" + filenames[0])
    break

# TODO allow user to enter start and stopping time on video
# use record(audio, offset=X, duration=X)cd 
with audio_file as source:
    r.adjust_for_ambient_noise(source)
    audio = r.record(source)

# delete the original temporary wav file
os.remove(data_path + "/data/test.wav")

# speech to text
audio_text = r.recognize_sphinx(audio)

# extract nouns from text
nouns_text = extract_nouns(audio_text)

# generate wordcloud from nouns
wordcloud = wc(background_color="white").generate(nouns_text)

# Display the generated wordcloud
plt.figure()
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()