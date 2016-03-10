import os
import pyaudio
import houndify
from pocketsphinx import pocketsphinx

FORMAT = pyaudio.paInt16
RATE = 16000
BUFFER_SIZE = 1024
MODELDIR = "pocketsphinx/model"

class KeywordDetection:
    def __init__(self, key, id):
        self.houndClient = houndify.VoiceQuery(key, id)

        self.hmm_directory = os.path.join(MODELDIR, 'en-us/en-us')
        self.dictionary_file = os.path.join(MODELDIR, 'en-us/cmudict-en-us.dict')
        self.language_model_file = os.path.join(MODELDIR, 'en-us/en-us.lm.bin')

        # check directories and files exist
        directories = {'model': MODELDIR, 'hmm': self.hmm_directory}
        files = {'dictionary': self.dictionary_file, 'language model': self.language_model_file}
        for key, value in directories.items():
            if not os.path.isdir(value):
                raise RequestError("missing PocketSphinx "+key+" directory: \"{0}\"".format(value))
        for key, value in files.items():
            if not os.path.isfile(value):
                raise RequestError("missing PocketSphinx "+key+" file: \"{0}\"".format(value))

    def start(self):
        # Create a decoder with certain model
        config = pocketsphinx.Decoder.default_config()
        config.set_string('-hmm', self.hmm_directory)
        config.set_string('-dict', self.dictionary_file)
        config.set_string("-logfn", os.devnull)
        decoder = pocketsphinx.Decoder(config)

        decoder.set_lm_file("lm", self.language_model_file)
        decoder.set_keyphrase("kws", "hey ada")
        decoder.set_search("kws")

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=1, rate=RATE, input=True, output=True, frames_per_buffer=BUFFER_SIZE)
        stream.start_stream()

        # Process audio chunk by chunk. On keyword detected perform action and restart search
        decoder.start_utt()
        while True:
            buf = stream.read(BUFFER_SIZE)
            if buf:
                decoder.process_raw(buf, False, False)
            else:
                 break
            if decoder.hyp() != None:
                print decoder.hyp().hypstr
                stream.stop_stream()
                decoder.end_utt()
                print '1'
                self.houndClient.query()
                print '2'
                decoder.start_utt()
