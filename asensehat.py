#
# Name: asensehat.py
#
# Author: C.-H. Dominic HUNG <dominic@teli.hku.hk / chdhung@hku.hk>
#  Technology-Enriched Learning Initiative,
#  The University of Hong Kong
#
# Description: TODO:
#

import time, copy, threading
import sense_hat

# PARAMETERS
# ====================
#
DISP_DIMX = 8              # NUMBER OF PIXELS (WIDTH)
DISP_DIMY = 8              # NUMBER OF PIXELS (HEIGHT)
RFSH_RATE = 1              # FRAME RATE (NUMBER OF FRAMES PER SECOND)
IFRM_DELY = 1 / RFSH_RATE  # INTER-FRAME SEPARATION (IN SECONDS)

#
# SENSE HAT DISPLAY ROUTINES
#

# __DISPLAY_1D
# ====================
#
# The function displays a frame presented as a 1-dimensional of size DISP_DIMY *
#  DISP_DIMX on the LED Matrix of the attached Sense Hat.
#
# @param frame   A 1-dimensional array of size DISP_DIMY * DISP_DIMX containing
#                 in each element a 3-integer tuple containing Red, Green and
#                 Blue colour components to be displayed as pixel on the Sense
#                 Hat LED Matrix. The x-axis pixels are listed in the array
#                 consecutively, with array index 0 storing the top-left most
#                 pixel colour.
#
# @sideef __sen_instis read and modified by this function
#
def __display_1D(frame) :
    global __sen_inst

    if __sen_inst is not None :
        pass
    else :
        raise ValueError("Sense Hat Module Not Instantiated")

    if frame is not None and type(frame) is list and len(frame) == DISP_DIMX * DISP_DIMY :
        for i in range(DISP_DIMX * DISP_DIMY) :
            if frame[i] is not None and (type(frame[i]) is tuple or type(frame[i]) is list) and len(frame[i]) == 3 :
                for c in [0, 1, 2] :
                    if frame[i][c] is not None and type(frame[i][c]) is int :
                        if frame[i][c] > -1 and frame[i][c] < 256 :
                            pass
                        else :
                            raise ValueError
                    else :
                        raise TypeError

                __sen_inst.set_pixel(i % DISP_DIMX, int(i / DISP_DIMX), frame[i])
            else :
                raise TypeError
    else :
        raise TypeError

# __DISPLAY_2D
# ====================
#
# The function displays a frame presented as a 2-dimensional of size [DISP_DIMY
#  * [DISP_DIMX]] on the LED Matrix of the attached Sense Hat.
#
# @param frame   A 2-dimensional array of size [DISP_DIMY * [DISP_DIMX]] with
#                 each element a 3-integer tuple containing Red, Green and Blue
#                 colour components to be displayed as pixel on the Sense Hat
#                 LED Matrix. The first sub-array, i.e., array index 0, concerns
#                 the top row of pixels on the LED Matrix. The index 0 element
#                 of this sub-array stores the left-most pixel of the LED row.
#
# @sideef __sen_instis read and modified by this function
#
def __display_2D(frame) :
    global __sen_inst

    if __sen_inst is not None :
        pass
    else :
        raise ValueError("Sense Hat Module Not Instantiated")

    if frame is not None and type(frame) is list and len(frame) == DISP_DIMY :
        for i in range(DISP_DIMY) :
            if frame[i] is not None and type(frame[i]) is list and len(frame[i]) == DISP_DIMX :
                for j in range(DISP_DIMX) :
                    if frame[i][j] is not None and (type(frame[i][j]) is tuple or type(frame[i][j]) is list) and len(frame[i][j]) == 3 :
                        for c in [0, 1, 2] :
                            if frame[i][j][c] is not None and type(frame[i][j][c]) is int :
                                if frame[i][j][c] > -1 and frame[i][j][c] < 256 :
                                    pass
                                else :
                                    raise ValueError
                            else :
                                raise TypeError

                        __sen_inst.set_pixel(i, j, frame[j][i])
                    else :
                        raise TypeError
            else :
                raise TypeError
    else :
        raise TypeError

# __ANIMATE_1D
# ====================
#
# The function displays a series of frames with time separation between frames
#  presented as an array of 1-dimensional of size [number of frames * [DISP_DIMY
#  * DISP_DIMX]] on the LED Matrix of the attached Sense Hat.
#
# @param anime   An array of varidic size, composed of display frames that are
#                 1-dimensional array of size [DISP_DIMY * DISP_DIMX] with each
#                 element a 3-integer tuple containing Red, Green and Blue
#                 colour components to be displayed as pixel on the Sense Hat
#                 LED Matrix. The first sub-array, i.e., array index 0, concerns
#                 the top row of pixels on the LED Matrix. The index 0 element
#                 of this sub-array stores the left-most pixel of the LED row.
# @param frm_sep  An integer or a floating-point number specifying the required
#                  time in number of seconds for inter-frame separation.
#
def __animate_1D(anime, frm_sep = IFRM_DELY) :
    # Record the Entrance Time of the first frame
    #
    ent = time.time()

    for i in range(len(anime)) :
        __display_1D(anime[i])

        # Calculate the End Time of the current frame against its Entrance Time
        #  to gurantee minimum inter-frame separation is achieved.
        #
        sep = frm_sep - (time.time() - ent)

        time.sleep(sep if sep > 0 else 0)

        # Record the Entrance Time of the next frame
        #
        ent = time.time()

# __ANIMATE_2D
# ====================
#
# The function displays a series of frames with time separation between frames
#  presented as an array of 2-dimensional arrays of size [number of frames *
#  [DISP_DIMY * [DISP_DIMX]]] on the LED Matrix of the attached Sense Hat.
#
# @param anime   An array of varidic size, composed of display frames that are
#                 2-dimensional arrays of size [DISP_DIMY * [DISP_DIMX]] with
#                 each element a 3-integer tuple containing Red, Green and Blue
#                 colour components to be displayed as pixel on the Sense Hat
#                 LED Matrix. The first sub-array, i.e., array index 0, concerns
#                 the top row of pixels on the LED Matrix. The index 0 element
#                 of this sub-array stores the left-most pixel of the LED row.
# @param frm_sep  An integer or a floating-point number specifying the required
#                  time in number of seconds for inter-frame separation.
#
def __animate_2D(anime, frm_sep = IFRM_DELY) :
    # Record the Entrance Time of the first frame
    #
    ent = time.time()

    for i in range(len(anime)) :
        __display_2D(anime[i])

        # Calculate the End Time of the current frame against its Entrance Time
        #  to gurantee minimum inter-frame separation is achieved.
        #
        sep = frm_sep - (time.time() - ent)

        time.sleep(sep if sep > 0 else 0)

        # Record the Entrance Time of the next frame
        #
        ent = time.time()

#
# (END OF) SENSE HAT DISPLAY ROUTINES
#

#
# SENSE HAT DISPLAY OUTPUT OBJECTS ASSERTION ROUTINES
#

# __RECURS_TEST
# ====================
#
# This function performs fast check on the data structure of display frames to
#  be served by the display handler. The routine checks on the first element
#  on every dimension of array it can find to identify structural conformance
#  and provide directives for subsequent service.
#
#  Supported data structures are,
#   1) single-frame 1-dimensional array of size [DISP_DIMY * DISP_DIMX], or
#   2) single-frame 2-dimensional array of size [DISP_DIMY * [DISP_DIMX]], or
#   3) multi-frame 1-dimensional array of size [DISP_DIMY * DISP_DIMX], or
#   4) multi-frame 2-dimensional array of size [DISP_DIMY * [DISP_DIMX]].
#
#  As the function is by no means exhausting all elements, sub-arrays and
#  elements of sub-arrays, functions along the call should ensure compliance in
#  data structure.
#
# @param frames  A 1-dimensional array of size [DISP_DIMY * DISP_DIMX] or a 2-
#                 dimensional array of size [DISP_DIMY * [DISP_DIMX]] or a 2-
#                 dimensional array of size [number of frames * [DISP_DIMY *
#                 DISP_DIMX]] or a 3-dimensional array of size [number of frames
#                 * [DISP_DIMY * [DISP_DIMX]]], with each element a 3-integer
#                 tuple containing Red, Green and Blue colour components to be
#                 displayed as pixel on the Sense Hat LED Matrix. The x-axis
#                 pixels are listed in the array consecutively for 1-dimensional
#                 array type input, with array index 0 storing the top-left most
#                 pixel colour. Meanwhile, for the 2-dimensional array type, the
#                 first sub-array of the , i.e., array index 0, concerns the top
#                 row of pixels on the LED Matrix. The index 0 element of this
#                 sub-array stores the left-most pixel of the LED row.
#
# @return A tuple of boolean signifying if the input frame being a frame burst
#  for showing animation and an integer of value 1 or 2 indicating the number of
#  dimensions in the array of a single frame
#
def __recurs_test(frames) :
    depth = []

    while frames is not None and (type(frames) is tuple or type(frames) is list) and len(frames) > 0 :
        depth += [len(frames)]

        frames = frames[0]

    if depth[-3 : ] == [DISP_DIMY, DISP_DIMX, 3] :
        if len(depth) == 3 :
            return (False, 2)
        elif len(depth) == 4 :
            return (True, 2)
        else :
            raise ValueError
    elif depth[-2 : ] == [DISP_DIMY * DISP_DIMX, 3] :
        if len(depth) == 2 :
            return (False, 1)
        elif len(depth) == 3 :
            return (True, 1)
        else :
            raise ValueError
    else :
        raise ValueError

#
# (END OF) SENSE HAT DISPLAY OUTPUT OBJECTS ASSERTION ROUTINES
#

def start(sense_hat) :
    global __sen_inst

    __sen_inst = sense_hat

    threading.Thread(target=display_handler).start()

#
# PRE-DEFINED RGB CODES FOR COMMON COLOURS
#
colour = dict()
colour["red"]    = [255, 000, 000]
colour["green"]  = [000, 255, 000]
colour["blue"]   = [000, 000, 255]
colour["yellow"] = [255, 255, 000]
colour["violet"] = [159, 000, 255]
colour["white"]  = [255, 255, 255]
colour["black"]  = [000, 000, 000]

# DISPLAY_HANDLER
# ====================
#
# This function TODO: Commenting
#
#  Supported data structures are,
#   1) single-frame 1-dimensional array of size [DISP_DIMY * DISP_DIMX], or
#   2) single-frame 2-dimensional array of size [DISP_DIMY * [DISP_DIMX]], or
#   3) multi-frame 1-dimensional array of size [DISP_DIMY * DISP_DIMX], or
#   4) multi-frame 2-dimensional array of size [DISP_DIMY * [DISP_DIMX]].
#
# @sideef __fready is read by this function
# @sideef __fserve is read and modified by this function
# @sideef oframe_incis read by this function
# @sideef __dhkill read by this function
#
def display_handler() :
    global __fready
    global __fserve
    global oframe_inc
    global __dhkill

    __dhkill = False

    # Acquire the value of the Display Frames-Ready Indicator for warm start
    #  to ensure stale frame burst is taken as new incoming.
    #
    __fserve = __fready

    # Generating the default display frame, i.e., all LED off.
    #
    out_frames = [[colour["black"] for _ in range(DISP_DIMX * DISP_DIMY)]]
    _ = 1
    frm_idx = 0

    # Record the Entrance Time of the first frame
    #
    ent = time.time()

    while __dhkill is not True :
        # The Display Frames-Served Indicator is matched with the Display Frames
        #  -Ready Indicator to reveal if a frame burst is ready and has not been
        #  served. As the initial value for both indicators at cold start are of
        #  the same value, that is to indicate no frame burst is available. If
        #  display frames are generated, the this handler will flip the Ready
        #  Indicator, __fready making the values differentiate. And if the frame
        #  burst is served, this handler thread will flip Serve Indicator,
        #  __fserve and the values reunite signifying no display frames are
        #  available again.
        #
        if __fready == __fserve :
            # Advance frame counter for playing animation frames.
            #
            frm_idx += 1
        else :
            out_frames = copy.copy(oframe_inc)
            _ = __recurs_test(out_frames)

            if _[0] == True :
                pass
            else :
                out_frames = [out_frames]

            _ = _[1]

            frm_idx = 0

            # Display Frames-Served Indicator, Flipped by the display handling
            #  thread when display frames are consumed by output buffer. If a
            #  frame burst is consumed or at cold start which no display frames
            #  are ready, the flag will match the value of the Display Frames-
            #  Ready Indicator, __fready.
            #
            __fserve = not __fserve

        if _ is 1 :
            __display_1D(out_frames[frm_idx % len(out_frames)])
        elif _ is 2 :
            __display_2D(out_frames[frm_idx % len(out_frames)])

        # Calculate the End Time of the current frame against its Entrance Time
        #  to gurantee minimum inter-frame separation is achieved.
        #
        sep = IFRM_DELY - (time.time() - ent)

        time.sleep(sep if sep > 0 else 0)

        # Record the Entrance Time of the next frame
        #
        ent = time.time()

# TODO: COMMENT
#
def display_async(output) :
    global __fready
    global __fserve
    global oframe_inc

    # The Display Frames-Ready Indicator is matched with the Display Frames
    #  -Served Indicator to check if a frame burst was readied and has not been
    #  served, therefore the output routine is unavailable in handling new
    #  frames. The routine will spin-wait here until the output routine is made
    #  available again.
    #
    while __fready != __fserve :
        pass

    if __fready == __fserve :
        # Put forward the output frames to `oframe_inc' for the display handler
        #  to crawl from.
        #
        oframe_inc = output

        # The indicator variable `__fready' is flipped to signal new
        #  display frames are ready at the variable `oframe_inc'.
        #
        __fready = not __fready

# TODO: COMMENT
# TODO: Can use a __fcompl Display-Completed flag to implement blocking display
#  without killing a thread instead. Later work.
#
def display_sync(output) :
    global __dhkill

    _ = threading.active_count()

    __dhkill = True

    while threading.active_count() >= _ :
        pass

    if output is not None and type(output) is str :
        global __sen_inst

        if __sen_inst is not None :
            __sen_inst.show_message(output)
        else :
            raise ValueError("Sense Hat Module Not Instantiated")
    elif output is not None and type(output) is tuple and len(output) == 2 \
        and type(output[0]) is str and (type(output[1]) is tuple or type(output[1]) is list) \
        and len(output[1]) == 3 and output[1][0] > -1 and output[1][0] < 256 \
        and output[1][1] > -1 and output[1][1] < 256 and output[1][2] > -1 and output[1][2] < 256 :
        global __sen_inst

        if __sen_inst is not None :
            __sen_inst.show_message(output[0], text_colour=output[1])
        else :
            raise ValueError("Sense Hat Module Not Instantiated")
    else :
        _ = __recurs_test(output)

        if _[0] == True :
            if _[1] == 1 :
                __animate_1D(output, IFRM_DELY)
            if _[1] == 2 :
                __animate_2D(output, IFRM_DELY)
        else :
            if _[1] == 1 :
                __display_1D(output)
            if _[1] == 2 :
                __display_2D(output)

    __dhkill = False

    threading.Thread(target=display_handler).start()

# TODO: COMMENT
#
def display_single(output) :
    if output is not None and type(output) is str :
        global __sen_inst

        if __sen_inst is not None :
            __sen_inst.show_message(output)
        else :
            raise ValueError("Sense Hat Module Not Instantiated")
    elif output is not None and type(output) is tuple and len(output) == 2 \
        and type(output[0]) is str and (type(output[1]) is tuple or type(output[1]) is list) \
        and len(output[1]) == 3 and output[1][0] > -1 and output[1][0] < 256 \
        and output[1][1] > -1 and output[1][1] < 256 and output[1][2] > -1 and output[1][2] < 256 :
        global __sen_inst

        if __sen_inst is not None :
            __sen_inst.show_message(output[0], text_colour=output[1])
        else :
            raise ValueError("Sense Hat Module Not Instantiated")
    else :
        _ = __recurs_test(output)

        if _[0] == True :
            if _[1] == 1 :
                __animate_1D(output, IFRM_DELY)
            if _[1] == 2 :
                __animate_2D(output, IFRM_DELY)
        else :
            if _[1] == 1 :
                __display_1D(output)
            if _[1] == 2 :
                __display_2D(output)

#
# INTERNAL TRANSIENT VARIABLES
#
__sen_inst = None

# Display Frames-Ready Indicator, Flipped by main thread or an interrupt handler
#  charged with frames generation when display frames are readied to be output
#  at global variable display_inc of this module scope.
#
__fready = False

# Display Frames-Served Indicator, Flipped by the display handling thread when
#  display frames are consumed by output buffer.
#
__fserve = False

oframe_inc = None

__dhkill = not True

#
# USER ROUTINES
#

# MAIN
# ====================
#
# Main demonstration routine called when the module is ran in standalone mode.
#
# TODO: 
#
if __name__ == "__main__" :
    import signal

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
        if __sen_inst is not None :
            __sen_inst.clear()

        # TODO: Terminate the Display Handler thread or it will write pixels on
        #  to the Sense Hat LED Matrix while clearing it.
        #

        quit()

    signal.signal(signal.SIGINT, __exit)

    __double = not True
    __delgte = not True
    __nopenb = not True

    #
    # SENSE HAT BUTTON EVENT HANDLER
    #
    def __response(event) :
        global __fready
        global __fserve
        global oframe_inc

        # The Display Frames-Ready Indicator is matched with the Display Frames
        #  -Served Indicator to check if a frame burst was readied and has not
        #  been served, therefore the output routine is unavailable in handling
        #  new frames.
        #
        if __fready == __fserve :
            if event.action == sense_hat.ACTION_PRESSED :
                # Start an asynchronous audio recording when any of the keys is
                #  pressed.
                #
                if event.direction == "up" :
                    if __delgte is not True :
                        # Generation of Single Frame Array for Displaying in
                        #  Sense Hat LED Matrix when up key is pressed.
                        #
                        oframe_inc = [[colour["violet"] for _ in range(DISP_DIMX)] for _ in range(DISP_DIMY)]

                        # The indicator variable `__fready' is flipped to signal
                        #   new display frames are ready at the public variable
                        #   `oframe_inc'.
                        #
                        __fready = not __fready
                    else :
                        display_async([[colour["violet"] for _ in range(DISP_DIMX)] for _ in range(DISP_DIMY)])

                    print("Displayed 2-D Frame of Violet")
                elif event.direction == "down" :
                    otext = "HKU"
                    # Performs synchronous output, the output will operate in
                    #  blocking mode.
                    #
                    display_sync(otext)

                    # The indicator variable `__fready' is NOT flipped as no new
                    #  display frames are produced.
                    #

                    print("Displayed Text \"" + otext + "\"")
                elif event.direction == "left" :
                    if __delgte is not True :
                        # Generation of Multi-Frame Array (Animation) for
                        #  Displaying in Sense Hat LED Matrix when left key is
                        #  pressed.
                        #
                        oframe_inc = [[[colour[name] for _ in range(DISP_DIMX)] for _ in range(DISP_DIMY)] for name in ["red", "green", "blue"]]

                        # The indicator variable `__fready' is flipped to signal
                        #   new display frames are ready at the public variable
                        #   `oframe_inc'.
                        #
                        __fready = not __fready
                    else :
                        display_async([[[colour[name] for _ in range(DISP_DIMX)] for _ in range(DISP_DIMY)] for name in ["red", "green", "blue"]])

                    print("Displayed 2-D Animation of RGB")
                elif event.direction == "right" :
                    if __delgte is not True :
                        # Generation of Multi-Frame Array (Animation) for
                        #  Displaying in Sense Hat LED Matrix when left key is
                        #  pressed.
                        #
                        oframe_inc = [[colour[name] for _ in range(DISP_DIMY * DISP_DIMX)] for name in ["yellow", "black", "red"]]

                        # The indicator variable `__fready' is flipped to signal
                        #   new display frames are ready at the public variable
                        #   `oframe_inc'.
                        #
                        __fready = not __fready
                    else :
                        display_async([[colour[name] for _ in range(DISP_DIMY * DISP_DIMX)] for name in ["yellow", "black", "red"]])

                    print("Displayed 1-D Animation of Belgium Flag Colours")
                else :
                    global __double

                    if __double is not True :
                        if __delgte is not True :
                            # Generation of Single Frame Array for Displaying in
                            #  Sense Hat LED Matrix when centre key is pressed.
                            #
                            oframe_inc = [colour["white"] for _ in range(DISP_DIMY * DISP_DIMX)]
                        else :
                            display_async([colour["white"] for _ in range(DISP_DIMY * DISP_DIMX)])
                    else :
                        if __delgte is not True :
                            # Generation of Single Frame Array for Displaying in
                            #  Sense Hat LED Matrix when down key is pressed.
                            #
                            oframe_inc = [colour["black"] for _ in range(DISP_DIMY * DISP_DIMX)]
                        else :
                            display_async([colour["black"] for _ in range(DISP_DIMY * DISP_DIMX)])

                    __double = not __double

                    if __delgte is not True :
                        # The indicator variable `__fready' is flipped to signal
                        #  new display frames are ready at the variable `oframe
                        #  _inc'.
                        #
                        __fready = not __fready

                    # The __double flag is inverted, therefore, the predicate
                    #  should be inverted, i.e., True when (255, 255, 255) and
                    #  False when (0, 0, 0).
                    #
                    print("Displayed 1-D Frame of {}".format("Full Brightness" if __double is True else "Full Darkness"))

    __sen_inst = sense_hat.SenseHat()

    # Generation of Single Frame Array for Displaying in Sense Hat LED Matrix.
    #
    frm_2d = [[colour["violet"] for _ in range(DISP_DIMX)] for _ in range(DISP_DIMY)]
    frm_1d = [colour["white"] for _ in range(DISP_DIMY * DISP_DIMX)]

    # Generation of Multi-Frame Array (Animation) for Displaying in Sense Hat LED Matrix.
    #
    ani_2d = [[[colour[name] for _ in range(DISP_DIMX)] for _ in range(DISP_DIMY)] for name in ["red", "green", "blue"]]
    ani_1d = [[colour[name] for _ in range(DISP_DIMY * DISP_DIMX)] for name in ["yellow", "black", "red"]]

    for i in [ani_2d, ani_1d] :
        display_single(i)

    for i in [frm_2d, frm_1d] :
        display_single(i)

        time.sleep(IFRM_DELY)

    # Register interrupt handler `__response()' to be triggered when any of the
    #  keys has event occurred.
    #
    __sen_inst.stick.direction_any = __response

    # TODO: Commenting
    #
    threading.Thread(target=display_handler).start()

    # A loop that runs forever without stopping
    #
    while True :
        if __nopenb is True :
            pass
        else :
            time.sleep(1)

#
# (END OF) USER ROUTINES
#