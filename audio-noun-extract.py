import speech_recognition as sr
import matplotlib.pyplot as plt
from wordcloud import WordCloud as wc
from pydub import AudioSegment 
from os import remove
import nltk
import argparse
import tempfile
import youtube_dl
# ffmpeg, pocketsphinx required

__author__ = 'Evan Reid'

tmp_filename = '/ytwctmp'

# TODO get directory using python commands
# TODO allow option to pass path for existing wav file
# TODO proper comments and method descriptions

def extract_nouns(text):
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
    r = sr.Recognizer()
    audio_file = sr.AudioFile(audio_path)

    # TODO allow user to enter start and stopping time on video
    # use record(audio, offset=X, duration=X)cd 
    with audio_file as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)

    # delete the original temporary wav file
    remove(audio_path)

    # speech to text
    return r.recognize_sphinx(audio)


def process_audio(out_path):
     # change to a single channel audio with 16000 frame rate (for pocketsphinx)
    audio = AudioSegment.from_wav(out_path + '.wav')
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
    audio.export(out_path + '.wav', format='wav')

def youtube_to_wav(url, out_path):
    # options for youtube_dl
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': out_path + '.webm', # TODO '/tmp/foo_%(title)s-%(id)s.%(ext)s'
        'postprocessors': [{
           'key': 'FFmpegExtractAudio',
           'preferredcodec': 'wav',
           'preferredquality': '192',
        }]
    }
    
    # download youtube video as audio file
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        filenames = [url]
        ydl.download(filenames)

def main():

    # parse arguments
    parser = argparse.ArgumentParser(description='Audio to wordcloud')
    parser.add_argument('url', type=str, help='url of youtube video')
    args = parser.parse_args()

    # get temprorary directory path
    tmp_path = tempfile.gettempdir() + tmp_filename

    # download youtube video and save as .wav audio file
    youtube_to_wav(args.url, tmp_path)

    # process audio to work correctly with pocketsphinx
    process_audio(tmp_path)
    
    # convert speech audio to text
    audio_text = audio_to_text(tmp_path + '.wav')    

    # extract nouns from text
    nouns_text = extract_nouns(audio_text)

    # generate wordcloud from nouns
    wordcloud = wc(background_color='white').generate(nouns_text)

    # Display the generated wordcloud
    plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

if __name__ ==  '__main__':
    main()