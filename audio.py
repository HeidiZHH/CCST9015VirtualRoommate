#
# Name: audio.py
#
# Author: C.-H. Dominic HUNG <dominic@teli.hku.hk / chdhung@hku.hk>
#  Technology-Enriched Learning Initiative,
#  The University of Hong Kong
#
# Description: Library supporting audio acquisition/replay, load/save in
#  support of Classwork 4 of CCST9015 offered in Spring 2019.
#

import pyaudio
import os
import math

# PARAMETERS
# ====================
#
CHUNK_SIZE = 1024          # NUMBER OF SAMPLES FOR AGGREGATION
FORMAT = pyaudio.paInt16   # ACQUISITION FORMAT
SRATE = 44100              # SAMPLE RATE PER SECOND
BSIZE = SRATE / CHUNK_SIZE # BATCH SIZE PER SECOND OF SAMPLE

#
# AUDIO CAPTURE ROUTINES
#

"""def record_audio(file_name, duration = 5) :
    p = pyaudio.PyAudio()
    istream = p.open(format=FORMAT, channels=1, rate=SRATE, input=True) # frames_per_buffer=CHUNK_SIZE

    with open(file_name, 'wb') as fh:
        for i in range(math.ceil(BSIZE * duration)) :
            chunk = istream.read(num_frames=CHUNK_SIZE, exception_on_overflow=False)

            # DATA SIZE = CHUNK_SIZE * NUMBER OF BYTES FOR SELECTED FORMAT
            #
            fh.write(chunk)

        fh.close()

    # print(accumt)

    istream.stop_stream()
    istream.close()

    p.terminate()"""

# __GENERIC_CAPTURE
# ====================
#
# Record an audio from local microphone and return captured content as a stream.
#
# @param durationAn integer stating the number of seconds the recording should last.
# @param srate   An integer indicating the intended sampling rate of the recording.
#
def __generic_capture(duration = 5, srate = SRATE) :
    p = pyaudio.PyAudio()
    istream = p.open(format=FORMAT, channels=1, rate=srate, input=True) # frames_per_buffer=CHUNK_SIZE

    stream = bytes()

    for i in range(math.ceil(BSIZE * duration)) :
        stream += istream.read(num_frames=CHUNK_SIZE, exception_on_overflow=False)

    istream.stop_stream()
    istream.close()

    p.terminate()

    return stream

# RECORD_AUDIO
# ====================
#
# Record an audio from local microphone and save to local filesystem.
#
# @param ofile   A string of file location path where a WAV audio file is to be saved.
# @param durationAn integer stating the number of seconds the recording should last.
# @param srate   An integer indicating the intended sampling rate of the recording.
#
def record_audio(ofile, duration = 5, srate = SRATE) :
    save_audio(__generic_capture(duration, srate), ofile)

# CAPTURE_AUDIO
# ====================
#
# Record an audio from local microphone and return captured content as a stream.
#
# @param durationAn integer stating the number of seconds the recording should last.
# @param srate   An integer indicating the intended sampling rate of the recording.
#
def capture_audio(duration = 5, srate = SRATE) :
    return __generic_capture(duration, srate)

#
# (END OF) AUDIO CAPTURE ROUTINES
#

#
# AUDIO REPLAY ROUTINES
#

"""def replay_audio(file_name) :
    p = pyaudio.PyAudio()
    ostream = p.open(format=FORMAT, channels=1, rate=SRATE, output=True) # frames_per_buffer=CHUNK_SIZE

    # import wave
    #
    # wf = wave.open("output.wav", 'rb')
    #
    # data = wf.readframes(CHUNK_SIZE)
    #
    # while data != '' :
    #     ostream.write(data)
    #     data = wf.readframes(CHUNK_SIZE)

    with open(file_name, 'rb') as fh:
        while fh.tell() != os.path.getsize('output.wav') : # get the file-size from the os module
            chunk = fh.read(CHUNK_SIZE)
            ostream.write(chunk)

        fh.close()

    ostream.stop_stream()
    ostream.close()

    p.terminate()"""

# __GENERIC_STREAM
# ====================
#
# Replay an audio stream on local speaker.
#
# @param stream  A wave (.WAV) format audio stream object.
# @param srate   An integer indicating the sampling rate of the audio file.
#
def __generic_stream(stream, srate = SRATE) :
    p = pyaudio.PyAudio()
    ostream = p.open(format=FORMAT, channels=1, rate=srate, output=True) # frames_per_buffer=CHUNK_SIZE

    nbatch = int(math.floor(len(stream) / CHUNK_SIZE))

    for i in range(nbatch) :
        ostream.write(stream[i * CHUNK_SIZE : (i + 1) * CHUNK_SIZE - 1])

    if nbatch * CHUNK_SIZE < len(stream) :
        ostream.write(stream[nbatch * CHUNK_SIZE : ])

    ostream.stop_stream()
    ostream.close()

    p.terminate()

# REPLAY_AUDIO
# ====================
#
# Replay an audio file on local speaker.
#
# @param ifile   A string of file location path where a WAV audio file is stored.
# @param srate   An integer indicating the sampling rate of the audio file.
#
def replay_audio(ifile, srate = SRATE) :
    __generic_stream(load_audio(ifile), srate)

# STREAM_AUDIO
# ====================
#
# Replay an audio stream on local speaker.
#
# @param stream  A wave (.WAV) format audio stream object.
# @param srate   An integer indicating the sampling rate of the audio file.
#
def stream_audio(stream, srate = SRATE) :
    __generic_stream(stream, srate)

#
# (END OF) AUDIO REPLAY ROUTINES
#

#
# AUDIO FILES HANDLING ROUTINES
#

# LOAD_AUDIO
# ====================
#
# Load a wave (.WAV) audio file from the local filesystem to an audio stream object.
#
# @param ifile   A string of file location path where a WAV audio file is stored.
#
def load_audio(ifile) :
    with open(ifile, 'rb') as ifd :
        stream = ifd.read()

        ifd.close()

    return stream

# SAVE_AUDIO
# ====================
#
# Save a wave (.WAV) audio stream object into the local filesystem as a wave file.
#
# @param stream  A wave (.WAV) format audio stream object to be saved into filesystem.
# @param ofile   A string of file location path where a WAV audio file is to be saved.
#
def save_audio(stream, ofile) :
    with open(ofile, 'wb') as ofd :
        ofd.write(stream)

        ofd.close()

#
# (END OF) AUDIO FILES HANDLING ROUTINES
#

#
# USER ROUTINES
#

# MAIN
# ====================
#
# Main demonstration routine called when the module is ran in standalone mode.
#
# The default showcase routine is to record an approximately 2 seconds audio
#  from local microphone and replay on local speaker.
#
if __name__ == "__main__" :
    stream_audio(capture_audio())

#
# (END OF) USER ROUTINES
#