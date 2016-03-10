import os
import pyaudio
from pocketsphinx import pocketsphinx

MODELDIR = "pocketsphinx/model"
hmm_directory = os.path.join(MODELDIR, 'en-us/en-us')
dictionary_file = os.path.join(MODELDIR, 'en-us/cmudict-en-us.dict')
language_model_file = os.path.join(MODELDIR, 'en-us/en-us.lm.bin')

# check directories and files exist
directories = {'model': MODELDIR, 'hmm': hmm_directory}
files = {'dictionary': dictionary_file, 'language model': language_model_file}
for key, value in directories.items():
    if not os.path.isdir(value):
        raise RequestError("missing PocketSphinx "+key+" directory: \"{0}\"".format(value))
for key, value in files.items():
    if not os.path.isfile(value):
        raise RequestError("missing PocketSphinx "+key+" file: \"{0}\"".format(value))

# Create a decoder with certain model
config = pocketsphinx.Decoder.default_config()
config.set_string('-hmm', hmm_directory)
config.set_string('-dict', dictionary_file)
config.set_string("-logfn", os.devnull)
decoder = pocketsphinx.Decoder(config)

decoder.set_lm_file("lm", language_model_file)
decoder.set_keyphrase("kws", "hey ada")
decoder.set_search("kws")

FORMAT = pyaudio.paInt16
RATE = 16000
BUFFER_SIZE = 1024

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
        print ("Detected keyword, restarting search")
        decoder.end_utt()
        decoder.start_utt()
