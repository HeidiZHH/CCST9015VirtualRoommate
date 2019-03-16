#
# Name: gtexttospeech.py
#
# Author: C.-H. Dominic HUNG <dominic@teli.hku.hk / chdhung@hku.hk>
#  Technology-Enriched Learning Initiative,
#  The University of Hong Kong
#
# Description: Library wrapping Google Text to Speech API in support of
#  Classwork 4 of CCST9015 offered in Spring 2019.
#

# TODO: REPLACE WITH A SHARED HEADER FILE THAT HOLDS THE PATH
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/usr/share/ccst9015/gcloud_ccst9015_sp19.json"

from google.cloud import texttospeech

#
# GOOGLE CLOUD SERVICES WRAPPING ROUTINES
#

# GTEXTTOSPEECH
# ====================
#
# The function will send a text stream to Google Text to Speech API for synthesising
#  a verbal production of the text in wave (.WAV) audio stream.
#
# @param stream  A string containing English text for producing a verbal production
# @param locale  A string holding a BCP-47 identifier for specifying the language
#                 (and accent) used for speech synthesis over the Google Cloud Text
#                 to Speech API. User should observe the most up-to-date list of
#                 supported languages from Google Cloud documentations for possible
#                 language options.
#
# @ret           A wave (.WAV) audio stream object bearing the spoken production of the
#                 submitted text
#
def gtexttospeech(text, locale="en-GB") :
    if text is not None and type(text) is str :
        pass
    else :
        raise TypeError

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    if locale is not None and type(locale) is str :
        voice = texttospeech.types.VoiceSelectionParams(
            language_code=locale,
            ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
    else :
        raise TypeError

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    return response.audio_content

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
# The default showcase routine sends an example text to Google Text-to-Speech
#  services and plays the responding audio stream to local speaker.
#
if __name__ == "__main__" :
    # REPLAY TEXT-TO-SPEECH RESULT
    #
    import time
    import audio

    ent = time.time()

    aresp = gtexttospeech("Hello Sexy!")

    print("Response Latency: " + str(time.time() - ent) + "s")

    # [WARNING] The resulting wave audio from Google API is produced with a
    #  2.4kHz sampling rate
    audio.stream_audio(aresp, 24000)

#
# (END OF) USER ROUTINES
#