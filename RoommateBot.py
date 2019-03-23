import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space

"""
$ python2.7 counter.py <token>
Counts number of messages a user has sent. Starts over if silent for 10 seconds.
Illustrates the basic usage of `DelegateBot` and `ChatHandler`.
"""
prev_reply = ""
class MessageCounter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self._count = 0

    def on_chat_message(self, msg): #msg["text"]
	global prev_reply
        reply = ""
        self._count += 1
        print(msg["text"])
        #print("Input your reply:")
        #reply = raw_input()
        print("Waiting for replay")
        f = open("msg.txt","w")
        f.write(msg["text"])
        f.close()
        #time.sleep(1)
        f = open("resp.txt","r")
        reply = f.readline()
        while(reply == prev_reply):
             reply=f.readline()
        if(reply==""):
            reply="It is good to talk with you"
        print(reply)
        prev_reply = reply
        self.sender.sendMessage(reply)
        f.close()
        print("Ready for next sentence")

TOKEN = '886340723:AAGsosJOvz0HQf4g9gDEFtFHXosZnqrByNQ' # get token from command-line

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=10
    ),
])
MessageLoop(bot).run_as_thread()
print('Listening ...')

while 1:
    pass
