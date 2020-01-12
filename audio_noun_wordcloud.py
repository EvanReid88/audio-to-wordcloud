import speech_recognition as sr
import matplotlib.pyplot as plt
from wordcloud import WordCloud as wc
from pydub import AudioSegment 
from os import remove
import sys
import nltk
import argparse
import tempfile
import youtube_dl
# ffmpeg, pocketsphinx required

# TODO add usage, why, improvements, to readme

__author__ = 'evanreid88'

def extract_nouns(text):
    """A function which uses the nltk library to tokenize words and extract nouns"""

    # extracting plural and non plural nouns and proper nouns.
    word_types = ['NN', 'NNS', 'NNP', 'NNPS']

    # function to test if something is a noun
    is_noun = lambda pos: pos[:2] in word_types

    # extract tokenized words
    tokenized_text = nltk.word_tokenize(text)

    # extract nouns from list of tokenized words
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized_text) if is_noun(pos)]

    # filter out any words with a single character
    nouns = filter(lambda x: len(x) > 1, nouns)

    # join nouns into a single string
    return ' '.join(nouns)

def audio_to_text(audio_path):
    """A function which converts audio (speech) from .wav format into a string of words using pocketsphinx speech recognition"""

    r = sr.Recognizer()
    try:
        audio_file = sr.AudioFile(audio_path)
    except:
        raise Exception('Failed to convert audio to text from specified path')

    with audio_file as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)

    # speech to text
    return r.recognize_sphinx(audio)

def process_audio(in_path, out_path):
    """A function to process / resample audio into the format required for pocketsphinx speech recognition"""

    # change to a single channel audio with 16000 frame rate (for pocketsphinx)
    try:
        audio = AudioSegment.from_wav(in_path)
    except:
        raise Exception('Failed to process audio from specified path')

    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
    audio.export(out_path, format='wav')

def youtube_to_wav(url, out_path):
    """A function used to download a youtube video audio as a .wav file into the specified path"""

    # options for youtube_dl
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': out_path + '.webm',
        'postprocessors': [{
           'key': 'FFmpegExtractAudio',
           'preferredcodec': 'wav',
           'preferredquality': '192',
        }]
    }
    
    # download youtube video as audio file
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        filenames = [url]
        try:
            ydl.download(filenames)
        except:
            raise Exception('Failed to download youtube audio from specified url')

def main():

    # parse arguments. url or path to a .wav file must be provided
    parser = argparse.ArgumentParser(description='Audio to wordcloud')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', type=str, help='url of youtube video used to generate wordcloud')
    group.add_argument('--path', type=str, help='path of .wav file used to generate wordcloud')
    parser.add_argument('-s', '--save', type=str, help='out-path for exporting word cloud png')
    args = parser.parse_args()

    # temporary file for storing processed audio used in speech to text
    tmp_file = tempfile.NamedTemporaryFile()

    # temprorary directory path
    tmp_path = tempfile.gettempdir() + tmp_file.name + '.wav'

    try:
        if args.url != None:
            # download youtube video and save as .wav audio file
            youtube_to_wav(args.url, tmp_path[0:-4])
            in_path = tmp_path
       
        else:
            in_path = args.path

        # process audio to work correctly with pocketsphinx
        process_audio(in_path, tmp_path)

        # convert speech audio to text
        audio_text = audio_to_text(tmp_path) 
    except:
        # ensure temporary file is deleted if anything fails
        tmp_file.close()

    # delete the temporary wav file
    tmp_file.close()

    # extract nouns from text
    nouns_text = extract_nouns(audio_text)

    # generate wordcloud from nouns
    wordcloud = wc(background_color='white').generate(nouns_text)

    # display the generated wordcloud
    plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    # save wordcloud if user passes --save args
    if (args.save != None):
        try:
            plt.savefig(args.save + 'noun_wc.png', format='png')
        except:
            raise Exception('Failed to save png to specified out path')
    
    plt.show()

if __name__ ==  '__main__':
    main()