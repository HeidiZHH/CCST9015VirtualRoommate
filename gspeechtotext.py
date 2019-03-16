#
# Name: gspeechtotext.py
#
# Author: C.-H. Dominic HUNG <dominic@teli.hku.hk / chdhung@hku.hk>
#  Technology-Enriched Learning Initiative,
#  The University of Hong Kong
#
# Description: Library wrapping Google Speech to Text API in support of
#  Classwork 4 of CCST9015 offered in Spring 2019.
#

# TODO: REPLACE WITH A SHARED HEADER FILE THAT HOLDS THE PATH
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/usr/share/ccst9015/gcloud_ccst9015_sp19.json"

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# PARAMETERS
# ====================
#
SRATE = 44100              # SAMPLE RATE PER SECOND

#
# GOOGLE CLOUD SERVICES WRAPPING ROUTINES
#

# GSPEECHTOTEXT
# ====================
#
# The function will submit an audio stream to Google Speech to Text API to obtain a
#  textual transcription of recognisable words.
#
# @param stream  A wave (.WAV) audio object presented for Google Speech to Text tran-
#                 scription service
# @param locale  A string holding a BCP-47 identifier for specifying the language
#                 (and accent) used for speech recognition over the Google Cloud
#                 Speech to Text API. User should observe the most up-to-date list of
#                 supported languages from Google Cloud documentations for possible
#                 language options.
#
# @ret           A string containing transcribed text of the processed audio stream
#
def gspeechtotext(stream, locale="en-GB") :
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(content=stream)

    if locale is not None and type(locale) is str :
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=SRATE,
            language_code=locale)
    else :
        raise TypeError

    response = client.recognize(config, audio)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.

    ret = ""

    for result in response.results:
        # The first alternative is the most likely one for this portion.
        # print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        ret += result.alternatives[0].transcript

    return ret

#
# (END OF) GOOGLE CLOUD SERVICES WRAPPING ROUTINES
#

#
# USER ROUTINES
#

# MAIN
# ====================
#
# Main demonstration routine called when the module is ran in standalone mode.
#
# The default showcase routine is to make 10 second recording by local micro-
#  phone and submit to Google Cloud service for transcription.
#
if __name__ == "__main__" :
    # RECORD SPEECH FOR TRANSCRITION
    #
    import time
    import audio

    cap = audio.capture_audio(duration=10)

    ent = time.time()

    print("Response: " + gspeechtotext(cap) + "(Latency: " + str(time.time() - ent) + "s)")

#
# (END OF) USER ROUTINES
#