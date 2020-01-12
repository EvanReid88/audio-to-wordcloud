# Audio / Youtube to Noun Word-Cloud
### Generate wordcloud from extracted nouns from speech audio
This is a python3 program used for generating a word cloud of the most commonly used nouns and proper nouns said in a particular youtube video or audio file (containing spoken word). This program utilizes pocketsphinx for speech-to-text and nltk for word tokenizing.  
  
To generate a wordcloud from a youtube video:
```
python3 audio_noun_wordcloud.py --url=<youtube_video_url>
```
To generate a wordcloud from an audio .wav file on disk:
```
python3 audio_noun_wordcloud.py --path=<path_to_wav>
```
## Options
Use the `--save` flag to save the generated word-cloud as a .png image to a specified path:
```
python3 audio_noun_wordcloud.py --url=<youtube_video_url> --save path/
```
# Dependencies
- SpeechRecognition 
- pocketsphinx
- ffmpeg
- youtube_dl
- nltk
- matplotlib
- wordcloud
- pydub
