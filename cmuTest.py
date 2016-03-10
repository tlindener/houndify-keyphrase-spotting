# ====================================================================
# Copyright (c) 2013 Carnegie Mellon University.  All rights
# reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# This work was supported in part by funding from the Defense Advanced
# Research Projects Agency and the National Science Foundation of the
# United States of America, and the CMU Sphinx Speech Consortium.
#
# THIS SOFTWARE IS PROVIDED BY CARNEGIE MELLON UNIVERSITY ``AS IS'' AND
# ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL CARNEGIE MELLON UNIVERSITY
# NOR ITS EMPLOYEES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# ====================================================================


import sys, os
import pyaudio
from pocketsphinx import pocketsphinx
from sphinxbase import sphinxbase

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
print 'terminated'
