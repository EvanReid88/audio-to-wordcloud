import unittest
import tempfile
import os.path
from os import path, remove
from pydub import AudioSegment
from audio_noun_wordcloud import extract_nouns, audio_to_text, process_audio, youtube_to_wav

class AudioNounExtractTest(unittest.TestCase):

    # TODO add comments and test descriptions

    # not testing cases for library logic

    def test_extract_nouns(self):
        # not testing nltk library functionality
        input_text = 'boat is a boat bike car z s x v '
        output_text = extract_nouns(input_text)

        self.assertTrue(len(output_text) > 0)

    def test_audio_to_text(self):
        # not testing SpeechRecognizer functionality
        path = 'test_data/harvard.wav'
        output = audio_to_text(path)

        self.assertTrue(len(output) > 0)
    
    def test_audio_to_text_invalid_path(self):
        invalid_path = 'bad_path_777'
        
        self.assertRaises(Exception, lambda:audio_to_text(invalid_path))

    def test_process_audio_file(self):
        test_path = 'test_data/harvard.wav'
        tmp_path = tempfile.gettempdir() + '/harvard_test.wav'
        process_audio(test_path, tmp_path)
        audio = AudioSegment.from_wav(tmp_path)

        self.assertTrue(path.exists(tmp_path))
        self.assertTrue(audio.channels == 1)
        self.assertTrue(audio.frame_rate == 16000)

        # remove temporary processed test .wav 
        if (path.exists(tmp_path)):
            remove(tmp_path)
    
    def test_process_audio_invalid_path(self):
        invalid_path = 'bad_path777'
        tmp_path = tempfile.gettempdir() + '/temp.wav' # won't be used 

        self.assertRaises(Exception, lambda:process_audio(invalid_path, tmp_path))

        # remove temp path just in case
        if (path.exists(tmp_path)):
            remove(tmp_path)

    # not testing youtube_to_wav functionality (connects to internet)

if __name__ == '__main__':
    unittest.main()