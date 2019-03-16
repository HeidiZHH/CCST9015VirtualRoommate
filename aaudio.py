#
# Name: aaudio.py
#
# Author: C.-H. Dominic HUNG <dominic@teli.hku.hk / chdhung@hku.hk>
#  Technology-Enriched Learning Initiative,
#  The University of Hong Kong
#
# Description: Library supporting audio acquisition control by asynchronous
#  callback in support of Classwork 4 of CCST9015 offered in Spring 2019.
#

import pyaudio

# PARAMETERS
# ====================
#
CHUNK_SIZE = 4096          # NUMBER OF SAMPLES FOR AGGREGATION
FORMAT = pyaudio.paInt16   # ACQUISITION FORMAT
SRATE = 44100              # SAMPLE RATE PER SECOND
BSIZE = SRATE / CHUNK_SIZE # BATCH SIZE PER SECOND OF SAMPLE

#
# AUDIO CAPTURE ROUTINES
#

#
# INTERNAL TRANSIENT VARIABLES
#
__iauddev = None           # AUDIO DEVICE
__iaudfds = None           # AUDIO DEVICE FILE DESCRIPTOR
__iaudstm = None           # INTERMEDIATE AUDIO STREAM FOR ACCUMULATION
__iaudstr = False          # FUNCTION ENTRANCE LOCK
arecord_ret = None         # POINT OF FINALISED AUDIO STREAM

# ARECORD_STEP
# ====================
#
# Fetch captured audio stream from the audio device buffer to a transient data
#  aggregation variable `__iaudstm' to accumulate till `arecord_finalise()' is
#  executed that clear such aggregation variable.
#
# @sideef __iaudstr is read and modified by this function
# @sideef __iaudfds is read and modified by this function
# @sideef __iaudstm is read and modified by this function
#
def arecord_step() :
    global __iaudstr

    # Guarding function entrance against user-interrupt race condition. The
    #  conditional is to make sure `arecord_start()' is called that initialises
    #  all relevant device variables before calling this function.
    #
    if __iaudstr is False :
        return

    global __iaudfds
    global __iaudstm

    if __iaudstm is None :
        __iaudstm = bytes()

    __iaudstm += __iaudfds.read(CHUNK_SIZE, False)

# ARECORD_FINALISE
# ====================
#
# Push the current contents in the transient audio stream aggregation variable
#  `__iaudstm' into the global variable `arecord_ret' making the capture final.
#  And reset the `__iaudstm' variable for the next capture.
#
# @sideef arecord_ret is modified by this function
# @sideef __iaudstm is read and modified by this function
#
# @return None or a wave (.wav) formatted audio stream
#
def arecord_finalise() :
    global arecord_ret
    global __iaudstm

    arecord_ret = __iaudstm

    __iaudstm = None

    return arecord_ret

# ARECORD_START
# ====================
#
# Starts an asynchronous audio stream capture and opens the local microphone
#  device and file descriptor.
#
# @sideef __iaudstr is read and modified by this function
# @sideef __iauddev is read and modified by this function
# @sideef __iaudfds is read and modified by this function
#
def arecord_start() :
    global __iaudstr

    # Guarding function entrance against user-interrupt race condition. The
    #  conditional makes sure `arecord_start()' is not called twice to over-
    #  write all relevant device variables when the function is accidentally
    #  triggered by premature asynchronous user event.
    #
    if __iaudstr is True :
        return

    __iaudstr = True

    global __iauddev
    global __iaudfds

    # Open local audio device and file descriptor, the audio stream is opened
    #  automatically upon calling PyAudio().open().
    #
    if __iauddev is None :
        __iauddev = pyaudio.PyAudio()

    if __iaudfds is None :
        __iaudfds = __iauddev.open(format=FORMAT, channels=1, rate=SRATE, input=True, frames_per_buffer=CHUNK_SIZE)

# ARECORD_END
# ====================
#
# Ends an asynchronous audio stream capture and closes all relevant files and
#  devices of the local microphone.
#
# @sideef __iaudstr is read and modified by this function
# @sideef __iauddev is read and modified by this function
# @sideef __iaudfds is read and modified by this function
#
def arecord_end() :
    global __iaudstr

    # Guarding function entrance against user-interrupt race condition. The
    #  conditional is to make sure `arecord_start()' is called that initialises
    #  all relevant device variables before calling this function.
    #
    if __iaudstr is False :
        return

    # Stop audio stream capture and close file descriptor and device of the
    #  local microphone.
    #
    global __iauddev
    global __iaudfds

    __iaudfds.stop_stream()
    __iaudfds.close()
    __iaudfds = None

    __iauddev.terminate()
    __iauddev = None

    __iaudstr = False

#
# (END OF) AUDIO CAPTURE ROUTINES
#

#
# USER ROUTINES
#

# MAIN
# ====================
#
# Main demonstration routine called when the module is ran in standalone mode.
#
# The default showcase routine is to record audio from the local microphone when
#  the middle key of the Sense Hat joystick is pushed. The recorded audio is
#  played at the release of the middle key.
#
if __name__ == "__main__" :
    import sense_hat, audio, signal

    # __exit
    # ====================
    #
    # Perform clean up tasks upon receiving termination signals and exit
    #  gracefully.
    #
    # @param signum  A signal.Signals enums of the signal dispatched to current
    #                 process and passed to this handler
    # @param curstackCurrent stack frame (Not usually used)
    #
    def __exit(signum, curstack) :
        quit()

    signal.signal(signal.SIGINT, __exit)

    # Audio Stream-Ready Indicator, Flipped by interrupt handler when audio
    #  stream is finalised and fetch-able from global variable arecord_ret of
    #  this module scope.
    #
    __aready = False

    # Audio Stream-Served Indicator, Flipped by the main thread when audio
    #  stream is consumed.
    #
    __aserve = False

    #
    # SENSE HAT BUTTON EVENT HANDLER
    #
    def __response(event) :
        if __aready == __aserve :
            if event.action == sense_hat.ACTION_PRESSED :
                # Start an asynchronous audio recording when centre-key is
                #  pressed.
                #
                arecord_start()
            elif event.action == sense_hat.ACTION_HELD :
                # Steps an asynchronous audio recording, i.e., fetch from audio
                #  device buffer and accumulates the short portion in transient
                #  storage.
                #
                # [WARNING]: This state maybe entered prematurely, i.e., when
                #  `arecord_start()' is not triggered. This is as the block is
                #  guarded by __aready variable and an early triggered event by
                #  user pressing the centre key before the variable is flipped
                #  back to `False' is possible.
                #
                #  Extra precautions is to be implemented in the called function
                #  to avoid exceptions to occur.
                #
                arecord_step()
            elif event.action == sense_hat.ACTION_RELEASED :
                global __aready

                # Fetch the last part of an asynchronous audio capture from the
                #  audio device buffer and accumulates the portion in transient
                #  storage.
                #
                #  End the asynchronous audio capture session by closing the
                #  relevant device and file descriptor and finalise the audio
                #  stream data by pushing the accumulated audio data to a public
                #  variable `arecord_ret'. The indicator variable `__aready' is
                #  flipped to signal new audio stream is ready at the public
                #  variable `arecord_ret'. The indicator is left untouched if no
                #  valid recording is being finalised, e.g., too short duration
                #  between centre-key press and release.
                #
                # [WARNING]: This state maybe entered prematurely, i.e., when
                #  `arecord_start()' is not triggered. This is as the block is
                #  guarded by __aready variable and an early triggered event by
                #  user pressing the centre key before the variable is flipped
                #  back to `False' is possible.
                #
                #  Extra precautions is to be implemented in the called function
                #  to avoid exceptions to occur.
                #
                arecord_step()
                arecord_end()

                if arecord_finalise() is None :
                    pass
                else :
                    __aready = not __aready

    s = sense_hat.SenseHat()

    # Register interrupt handler `__response()' to be triggered when centre-key
    #  event occur.
    #
    s.stick.direction_up = __response

    # A loop that runs forever without stopping
    #
    while True :
        # Blocking loop spin-waits on `__aready' variable for audio stream ready
        #  indication. The loop will break when the `__aready' is not flipped by
        #  the interrupt handler.
        #
        while True :
            # The Audio Stream-Served Indicator is matched with the Audio Stream
            #  -Ready Indicator to reveal if an audio stream is ready and has
            #  not been served. As the initial value for both indicators at cold
            #  start are of the same value, that is to indicate no audio stream
            #  available. If an audio stream is captured, the interrupt handler
            #  will flip the Ready Indicator, __aready making the values differ-
            #  entiate. And if the audio stream is served, the main thread will
            #  flip Serve Indicator, __aserve and the values reunite signifying
            #  no audio stream available again.
            #
            if __aserve == __aready :
                pass
            else :
                break

        # Consume the audio stream stored in the public variable `arecord_ret'.
        #
        audio.stream_audio(arecord_ret)

        # Audio Stream-Served Indicator, flipped by the main thread when the
        #  audio stream is consumed. If a stream is consumed or at cold start
        #  which no audio stream is ready, the flag will match the value of the
        #  Audio Stream-Ready Indicator, __aready.
        #
        __aserve = not __aserve

#
# (END OF) USER ROUTINES
#