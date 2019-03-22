#
# Name: cw3.py
#
# Author: C.-H. Dominic HUNG <dominic@teli.hku.hk / chdhung@hku.hk>
#  Technology-Enriched Learning Initiative,
#  The University of Hong Kong
#
# Description: Demonstration program for classwork 3 of CCST9015 offered in
#  Spring 2019. The program showcasts text transcription from audio recording
#  captured by local microphone by Google Cloud Speech to Text service and the
#  system responds by parsing the recognised text for applicable actions.
#  Message and synthesised verbal production is output by the attached Sense Hat
#  LED matrix display and local speaker if response can be returned.
#

import gtexttospeech, gspeechtotext, audio, aaudio, asensehat
import sense_hat
import os, time, re, signal
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

#
# USER LOGIC
#
chatbot = ChatBot('Ron Obvious')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
trainer.train("chatterbot.corpus.english")
#
# SENSE HAT BUTTON EVENT HANDLER
#
def __response(event) :
    if __aready == __aserve :
        if event.action == sense_hat.ACTION_PRESSED :
            # Start an asynchronous audio recording when centre-key is pressed.
            #
            aaudio.arecord_start()
        elif event.action == sense_hat.ACTION_HELD :
            # Steps an asynchronous audio recording, i.e., fetch from audio
            #  device buffer and accumulates the short portion in transient
            #  storage.
            #
            # [WARNING]: This state maybe entered prematurely, i.e., when
            #  `arecord_start()' is not triggered. This is as the block is
            #  guarded by __aready variable and an early triggered event by user
            #  pressing the centre key before the variable is flipped back to
            #  `False' is possible.
            #
            #  Extra precautions is to be implemented in the called function to
            #  avoid exceptions to occur.
            #
            aaudio.arecord_step()
        elif event.action == sense_hat.ACTION_RELEASED :
            global __aready
            # Fetch the last part of an asynchronous audio capture from the
            #  audio device buffer and accumulates the portion in transient
            #  storage.
            #
            #  End the asynchronous audio capture session by closing the
            #  relevant device and file descriptor and finalise the audio stream
            #  data by pushing the accumulated audio data to a public variable
            #  `arecord_ret'. The indicator variable `__aready' is flipped to
            #  signal new audio stream is ready at the public variable
            #  `arecord_ret'. The indicator is left untouched if no valid
            #  recording is being finalised, e.g., too short duration between
            #  centre-key press and release.
            #
            # [WARNING]: This state maybe entered prematurely, i.e., when
            #  `arecord_start()' is not triggered. This is as the block is
            #  guarded by __aready variable and an early triggered event by user
            #  pressing the centre key before the variable is flipped back to
            #  `False' is possible.
            #
            #  Extra precautions is to be implemented in the called function to
            #  avoid exceptions to occur.
            #
            aaudio.arecord_step()
            aaudio.arecord_end()

            if aaudio.arecord_finalise() is None :
                pass
            else :
                __aready = not __aready

SD_CORNER = (4, 4)
__sdial = [(1, 0), (2, 0), (3, 1), (3, 2), (2, 3), (1, 3), (0, 2), (0, 1)]
__sdial = [(SD_CORNER[0] + x, SD_CORNER[1] + y) for x, y in __sdial]
__sdidx = 1
DRAG_RATIO = 200

# SPIN_DIAL
# ====================
#
# Visualise the current form of a spin-dial of which the strokes are defined by
#  global variable __sdial on the LED matrix of the attached Sense Hat.
#
# The illuminated strokes are determined by global variable spin-dial index,
#  `__spidx' that is advanced by the main thread upon progress.
#
# @sideef __senhat is read and modified by this function
# @sideef __sdial is read by this function
# @sideef __sdidx is read by this function
#
def spin_dial() :
    if aaudio.__iaudstr is True :
        # When Asynchronous Audio Capture is in progress, spins a red circle
        #
        __senhat.set_pixel(__sdial[(int(__sdidx / DRAG_RATIO) + 0) % 8][0], __sdial[(int(__sdidx / DRAG_RATIO) + 0) % 8][1], (255, 000, 000))
        __senhat.set_pixel(__sdial[(int(__sdidx / DRAG_RATIO) - 1) % 8][0], __sdial[(int(__sdidx / DRAG_RATIO) - 1) % 8][1], (127, 000, 000))
    else :
        global __return
        global __easter

        # When system is idle,
        #  1) if the device is operating in Normal mode, spins,
        #   a) a white circle at cold boot or the last query uncomprehendible
        #   b) a green circle and the last query was successfully recognised by the parser
        #  2) If the device is operating in Easter Egg mode, spins,
        #   a) a violet circle at cold boot or the last query uncomprehendible
        #   b) a gold circle and the last query was successfully recognised by the parser
        #
        if __easter is True :
            if __return is True :
                __senhat.set_pixel(__sdial[(int(__sdidx / DRAG_RATIO) + 0) % 8][0], __sdial[(int(__sdidx / DRAG_RATIO) + 0) % 8][1], (231, 219, 116))
                __senhat.set_pixel(__sdial[(int(__sdidx / DRAG_RATIO) - 1) % 8][0], __sdial[(int(__sdidx / DRAG_RATIO) - 1) % 8][1], (114, 109,  58))
            else :
                __senhat.set_pixel(__sdial[(int(__sdidx / DRAG_RATIO) + 0) % 8][0], __sdial[(int(__sdidx / DRAG_RATIO) + 0) % 8][1], (159, 000, 255))
                __senhat.set_pixel(__sdial[(int(__sdidx / DRAG_RATIO) - 1) % 8][0], __sdial[(int(__sdidx / DRAG_RATIO) - 1) % 8][1], ( 79, 000, 127))
        else :
            if __return is True :
                __senhat.set_pixel(__sdial[(int(__sdidx / DRAG_RATIO) + 0) % 8][0], __sdial[(int(__sdidx / DRAG_RATIO) + 0) % 8][1], (000, 255, 000))
                __senhat.set_pixel(__sdial[(int(__sdidx / DRAG_RATIO) - 1) % 8][0], __sdial[(int(__sdidx / DRAG_RATIO) - 1) % 8][1], (000, 127, 000))
            else :
                __senhat.set_pixel(__sdial[(int(__sdidx / DRAG_RATIO) + 0) % 8][0], __sdial[(int(__sdidx / DRAG_RATIO) + 0) % 8][1], (255, 255, 255))
                __senhat.set_pixel(__sdial[(int(__sdidx / DRAG_RATIO) - 1) % 8][0], __sdial[(int(__sdidx / DRAG_RATIO) - 1) % 8][1], (127, 127, 127))

    # Clear the trailing stroke of the last spin
    #
    __senhat.set_pixel(__sdial[(int(__sdidx / DRAG_RATIO) - 2) % 8][0], __sdial[(int(__sdidx / DRAG_RATIO) - 2) % 8][1], (000, 000, 000))

#
# PRE-DEFINED RGB CODES FOR COMMON COLOURS
#
colour = dict()

for i in range(8) :
    colour["red"    + str(i)] = [255 - 32 * i, 000, 000]
    colour["green"  + str(i)] = [000, 255 - 32 * i, 000]
    colour["blue"   + str(i)] = [000, 000, 255 - 32 * i]
    colour["yellow" + str(i)] = [255 - 32 * i, 255 - 32 * i, 000]
    colour["cyan"   + str(i)] = [000, 255 - 32 * i, 255 - 32 * i]
    colour["magenta"+ str(i)] = [255 - 32 * i, 000, 255 - 32 * i]
    colour["white"  + str(i)] = [255 - 32 * i, 255 - 32 * i, 255 - 32 * i]

colour["red"]    = colour["red0"]
colour["green"]  = colour["green0"]
colour["blue"]   = colour["blue0"]
colour["yellow"] = colour["yellow0"]
colour["cyan"]   = colour["cyan0"]
colour["magenta"]= colour["magenta0"]
colour["white"]  = colour["white0"]
colour["lgrey"]  = colour["white2"]
colour["grey"]   = colour["white4"]
colour["dgrey"]  = colour["white6"]
colour["violet"] = [159, 000, 255]
colour["purple"] = colour["violet"]
colour["black"]  = [000, 000, 000]

prev_reply = ""
#
# DEFAULT INTERNAL SETTINGS
#
__senhat = None
__dcolor = colour["white"]
__tcscal = False              # TEMPERATURE IN CELCIUS SCALE
__adisab = False
__vdisab = False
__easter = False
__return = False

#
# INTERNAL VARIABLES
#
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# ACTION_PARSER
# ====================
#
# Visualise the current form of a spin-dial of which the strokes are defined by
#  global variable __sdial on the LED matrix of the attached Sense Hat.
#
# TODO: Return the spans of identified keywords.
#
# @param trans   A text string for parsing action command.
#         _cript
#
# @return A tuple of text response for verbal production and for message display
#  in strings.
#
# @sideef __senhat is read and modified by this function
# @sideef __dcolor is read and modified by this function
# @sideef __tcscal is read and modified by this function
#
def action_parser(transcript) :
    global colour
    global __senhat
    global __dcolor
    global __tcscal
    global __easter
    global __return
    global __adisab
    global __vdisab
    global prev_reply
    vtext = None
    dtext = None
    aresp = None
    vresp = None
    '''
    if re.search("What|Show|Tell|Know|Display", transcript, re.I) :
        if re.search(r'\b(temperature)\b', transcript, re.I) :
            _ = round(__senhat.get_temperature(), 1)

            tcscal = __tcscal

            if re.search(r'\b(celsius)\b', transcript, re.I) :
                tcscal = True

            elif re.search(r'\b(fahrenheit)\b', transcript, re.I) :
                tcscal = False

            _ = (_ if tcscal is True else round((_ * 9 / 5) + 32, 1))

            vtext = str(_) + " degree " + ("Celsius" if tcscal is True else "Fahrenheit")
            dtext = str(_) + "\"" + ("C" if tcscal is True else "F")

        if re.search(r'\b(humidity)\b', transcript, re.I) :
            _ = int(__senhat.get_humidity())

            vtext = str(_) + " percent"
            dtext = str(_) + "%"

        if re.search(r'\b(date|today)\b', transcript, re.I) :
            vtext = time.strftime("%Y-%m-%d")

        if re.search(r'\b(time|clock)\b', transcript, re.I) :
            vtext = time.strftime("%H:%M")

        if re.search(r'\b(days of week|weekday|day)\b', transcript, re.I) :
            vtext = time.strftime("%A")

    if re.search("Set|Change|Configure|Modify", transcript, re.I) :
        if re.search(r'\b(celsius)\b', transcript, re.I) :
            vtext = "Changing Temperature Scale to Degree Celsius"

            __tcscal = True
            dtext = "-> \"C"

        if re.search(r'\b(fahrenheit)\b', transcript, re.I) :
            vtext = "Changing Temperature Scale to Degree Fahrenheit"

            __tcscal = False
            dtext = "-> \"F"

        for colour_i in ["red", "green", "blue", "yellow", "cyan", "magenta", "white", "grey", "violet", "purple"] :
            if re.search(colour_i, transcript, re.I) :
                vtext = "Changing Text Colour to " + colour_i.title()

                __dcolor = colour[colour_i]
                dtext = colour_i.title()
        '''
        # if re.search(r'\b(red)\b', transcript, re.I) :
        #     vtext = "Changing text colour to red"

        #     __dcolor = colour["red"]
        #     dtext = "Red"

        # if re.search(r'\b(blue)\b', transcript, re.I) :
        #     vtext = "Changing text colour to blue"

        #     __dcolor = colour["blue"]
        #     dtext = "Blue"

        # if re.search(r'\b(green)\b', transcript, re.I) :
        #     vtext = "Changing text colour to green"

        #     __dcolor = colour["green"]
        #     dtext = "Green"

        # if re.search(r'\b(yellow)\b', transcript, re.I) :
        #     vtext = "Changing text colour to yellow"

        #     __dcolor = colour["yellow"]
        #     dtext = "Yellow"

        # if re.search(r'\b(violet)\b', transcript, re.I) :
        #     vtext = "Changing text colour to violet"

        #     __dcolor = colour["violet"]
        #     dtext = "Violet"
    '''
    if re.search("Reset|Rejuvenate|Clear|Forget", transcript, re.I) :
        vtext = "Clearing Device Settings"

        __dcolor = colour["white"]
        __tcscal = not False
        __vdisab = False
        __adisab = False
    '''
    # if re.search("Hello|Hallo|Hi|Hey", transcript, re.I) :
    #     vtext = "Hello"
    vtext=str(chatbot.get_response(transcript))
    print(vtext)
    if dtext is None :
        vresp = vtext
    else :
        vresp = dtext
    
    
    if vtext is not None :
        aresp = gtexttospeech.gtexttospeech(vtext)

    transcript = transcript.title()

    if __easter is True :
        _ = HP_Parser(transcript)

        if _[0] is not None or _[1] is not None :
            vtext = "Easter Egg Mode Command Triggered"
            aresp = _[0]
            vresp = _[1]

    if transcript == "I Am Half-Blood Prince" or transcript == "I Am Half Blood Prince" or transcript == "Alohomora" :
        __easter = True

        vtext = "Enabling Easter Egg Mode"
        aresp = audio.load_audio(BASE_PATH + "/.audio/24000/Lead-In_Music.wav")

    if aresp is None and vtext is None and vresp is None :
        __return = False
    else :
        __return = True

    if __adisab is True and __vdisab is True :
        return (None, vtext, [colour["black"] for _ in range(8 * 8)])
    elif __adisab is True :
        return (None, vtext, vresp)
    elif __vdisab is True :
        return (aresp, vtext, [colour["black"] for _ in range(8 * 8)])
    else :
        return (aresp, vtext, vresp)

def HP_Parser(transcript) :
    global __easter
    global __adisab
    global __vdisab

    transcript = transcript.title()

    aresp = None
    vresp = None

    if transcript == "Sectumsempra" :
        aresp = audio.load_audio(BASE_PATH + "/.audio/24000/Half-Blood_Prince.wav")

    #
    # Student to Implement "Reveal Your Secret"
    #  Use "./.audio/24000/Out-of-Other_Business-I.wav" and "./.audio/24000/Out-of-Other_Business-II.wav/"
    #
    elif transcript == "Reveal Your Secret" or transcript == "Review Your Secret" :
        aresp = audio.load_audio(BASE_PATH + "/.audio/24000/Out-of-Other_Business-I.wav") + audio.load_audio(BASE_PATH + "/.audio/24000/Out-of-Other_Business-II.wav")

    #
    # Student to Implement "Lumos Maxima"
    #
    elif transcript == "Lumos Maxima" :
        aresp = audio.load_audio(BASE_PATH + "/.audio/24000/Wand_Swing.wav")

        vresp = [colour["grey"] for _ in range(8 * 8)]
    elif transcript == "Lumos Solem" :
        aresp = audio.load_audio(BASE_PATH + "/.audio/24000/Wand_Swing.wav")

        vresp = [[colour[name] for _ in range(8 * 8)] for name in ["lgrey", "white", "white", "white", "white", "white", "white", "lgrey", "white"]]

    #
    # Student to Implement "Incendio"
    #
    elif transcript == "Incendio" :
        aresp = audio.load_audio(BASE_PATH + "/.audio/24000/Wand_Swing.wav")

        vresp = [colour["red"] for _ in range(8 * 8)]
    elif transcript == "Nox" or transcript == "Knox" :
        aresp = audio.load_audio(BASE_PATH + "/.audio/24000/Wand_Swing.wav")

        __vdisab = True

    #
    # Student to Implement "Silencio"
    #
    elif transcript == "Silencio" :
        aresp = audio.load_audio(BASE_PATH + "/.audio/24000/Wand_Swing.wav")

        __adisab = True
    elif transcript == "Obliviate" or transcript == "Alleviate" :
        aresp = audio.load_audio(BASE_PATH + "/.audio/24000/Wand_Swing.wav")

        __easter = False

    return (aresp, vresp)

# MAIN
# ====================
#

# __exit
# ====================
#
# Perform clean up tasks upon receiving termination signals and exit gracefully.
#
# @param signum  Signal dispatched to current process and passed to this handler
# @param curstackCurrent stack frame (Not usually used)
#
def __exit(signum, curstack) :
    if __senhat is not None :
        __senhat.clear()

    quit()

signal.signal(signal.SIGINT, __exit)

# audio.stream_audio(audio.load_audio(BASE_PATH + "/.audio/24000/Subtle_Science_Exact_Art.wav"), 24000)

__senhat = sense_hat.SenseHat()
asensehat.start(__senhat)
asensehat.RFSH_RATE = 5
asensehat.IFRM_DELY = 1 / asensehat.RFSH_RATE

# Register interrupt handler `__response()' to be triggered when centre-key
#  event occur.
#
__senhat.stick.direction_up = __response

# Audio Stream-Ready Indicator, Flipped by interrupt handler when audio stream
#  is finalised and fetch-able from global variable arecord_ret of this module
#  scope.
#
__aready = False

# Audio Stream-Served Indicator, Flipped by the main thread when audio stream
#  is consumed.
#
__aserve = False

# A loop that runs forever without stopping
#
while True :
    # Blocking loop spin-waits on `__aready' variable for audio stream ready
    #  indication. The loop will break when the `__aready' is not flipped by the
    #  interrupt handler.
    #
    while True :
        # Advance spin-dial counter and visualise on Sense Hat LED the system is
        #  idling or listening for voice commands.
        #
        # The spin-dial would be in white colour during idling and red upon
        #  listening for voice commands. The distinct colour also helps identify
        #  pre-mature race user interrupt, i.e., __aready is not flipped upon
        #  key press.
        # 
        __sdidx = __sdidx +  1

        spin_dial()

        # The Audio Stream-Served Indicator is matched with the Audio Stream-
        #  Ready Indicator to reveal if an audio stream is ready and has not
        #  been served. As the initial value for both indicators at cold start
        #  are of the same value, that is to indicate no audio stream available.
        #  If an audio stream is captured, the interrupt handler will flip the
        #  Ready Indicator, __aready making the values differentiate. And if the
        #  audio stream is served, the main thread will flip Serve Indicator,
        #  __aserve and the values reunite signifying no audio stream available
        #  again.
        #
        if __aserve == __aready :
            pass
        else :
            break

    # Submit the audio stream stored in the public variable `arecord_ret' to
    #  Google Speech to Text for transcription.
    #
    transcript = gspeechtotext.gspeechtotext(aaudio.arecord_ret)

    print("User Command:", transcript)

    if transcript is not None :
        #(aresp, cresp, vresp) = action_parser(transcript)
        (aresp, cresp, vresp) = action_parser(transcript)
        
        if cresp is not None and type(cresp) is str :
            print("Response:", cresp)
        if aresp is not None :
            # Submit system response to Google Text to Speech for synthesising
            #  verbal production.
            #
            # [NOTE] Audio stream generated from Google Text to Speech is at
            #  24 kHz.
            #
            audio.stream_audio(aresp, 24000)
        if vresp is not None and type(vresp) is str :
            asensehat.display_sync((vresp, __dcolor))
        elif vresp is not None :
            asensehat.display_async(vresp)



    # Audio Stream-Served Indicator, flipped by the main thread when the audio
    #  stream is consumed. If a stream is consumed or at cold start which no
    #  audio stream is ready, the flag will match the value of the Audio Stream-
    #  Ready Indicator, __aready.
    #
    __aserve = not __aserve

#
# (END OF) USER ROUTINES
#