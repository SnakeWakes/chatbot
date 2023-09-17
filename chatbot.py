from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from cleaner import clean_corpus
from flask import Flask, render_template, request
import time
time.clock = time.time
import uuid

app = Flask(__name__) #Creating Flash init

# Generate a unique username for the chatbot
username = str(uuid.uuid4())

# Create a new chatbot with the unique username
chatbot = ChatBot(username)

# Train the chatbot on the default corpus and PersonaChat corpus
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')
trainer.train("chatterbot.corpus.english.conversations")

#TRAINING CUSTOM DATA SECTION
CORPUS_FILE = "chat.txt"
trainer = ListTrainer(chatbot)
cleaned_corpus = clean_corpus(CORPUS_FILE)
trainer.train(cleaned_corpus)
#TRAINING CUSTOM DATA SECTION

# Create a delay to simulate a human typing
def typing_delay(text):
    delay = len(text) * 0.05
    if delay < 1.5:
        delay = 1.5
    time.sleep(delay)

@app.route("/")
def home():
    return render_template("index.html")

# Start a conversation with the chatbot
print('You are connected to user {}. Type "bye" to exit.\n'.format(username))

@app.route("/get")
def get_bot_response():
    user_input = request.args.get('msg')
    typing_delay(user_input)
    return str(chatbot.get_response(user_input))
'''
    scores = []
    for statement in chatbot.storage.filter():
        scores.append(statement.confidence)
    plt.bar(range(len(scores)), scores)
    plt.xlabel('Response Index')
    plt.ylabel('Confidence Score')
    plt.title('Chatbot Response Confidence Scores')
    plt.show()
'''

    # Get a response from the chatbot
    #response = chatbot.get_response(user_input)

    # Print the response
    #print('{}: {}'.format(username, response.text))

if __name__ == "__main__":
    app.run()
