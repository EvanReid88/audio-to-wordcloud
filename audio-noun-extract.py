import speech_recognition as sr
import nltk

r = sr.Recognizer()

# TODO allow recorded audio
audio_file = sr.AudioFile('harvard.wav')

with audio_file as source:
    r.adjust_for_ambient_noise(source, duration = .5)
    audio = r.record(source)

# TODO use pockedsphinx
audio_text = r.recognize_google(audio)

# function to test if something is a noun
is_noun = lambda pos: pos[:2] == 'NN'

# extract tokenized words
tokenized_text = nltk.word_tokenize(audio_text)

# extract nouns from list of tokenized words
nouns = [word for (word, pos) in nltk.pos_tag(tokenized_text) if is_noun(pos)]

print(nouns)