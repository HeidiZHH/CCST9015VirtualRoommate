from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import time

prev_msg = ""
chatbot = ChatBot('Ron Obvious')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
trainer.train("chatterbot.corpus.english")

def getResponse(msg):
    global prev_msg, chatbot
    # Get a response to an input statement
    if(not msg == prev_msg):
        #print(type(resp))
        prev_msg = msg
        f = open("resp.txt", "w")
        f.write(str(chatbot.get_response(msg)))
        f.close()
        

print("Waiting msg income")
while(1):
    fin = open("msg.txt", "r")
    msg = fin.readline()
    if(not msg == prev_msg):
        print(msg)
    getResponse(msg)
    time.sleep(0.5)
