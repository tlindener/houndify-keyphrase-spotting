import os
import pyaudio
import houndify
from pocketsphinx import pocketsphinx
import paho.mqtt.client as mqtt

FORMAT = pyaudio.paInt16
RATE = 16000
BUFFER_SIZE = 1024
MODELDIR = "pocketsphinx/model"

class KeywordDetector:
    def __init__(self):
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("192.168.178.44", 1883, 60)
        client.loop_start()

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
        decoder.set_keyphrase("kws", "hey emma")
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
                # self.houndClient.query()
                stream.start_stream()
                decoder.start_utt()

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("home/speech/local/action")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        if str(msg.payload)=="on":


if __name__ == '__main__':
    import sys

    # if len(sys.argv) < 3:
    #     print "Usage: %s <client key> <client ID>" % sys.argv[0]
    #     sys.exit(0)
    #
    # CLIENT_KEY = sys.argv[1]
    # CLIENT_ID = sys.argv[2]

    kd = KeywordDetector()
    kd.start()
