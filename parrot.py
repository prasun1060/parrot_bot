print('Made with passion by AG36147')
print('Loading...')
import nltk
import random
import string
import re, string, unicodedata
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
import warnings
warnings.filterwarnings("ignore")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
print('Hmmm let me check the PI...')
with open('raw.txt', 'r') as f:
    raw = f.read()
print('Ok lets chat now!')
sent_tokens = nltk.sent_tokenize(raw)

def Normalize(text):
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    #Word Tokenization
    word_token = nltk.word_tokenize(text.lower().translate(remove_punct_dict))
    #Remove ASCII
    new_words = []
    for word in word_token:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    #Remove Tags
    rmv = []
    for word in new_words:
        text = re.sub("&lt;/?.*?&gt;","&lt;&gt;",word)
        rmv.append(text)
    #pos tagging and lemmatization
    tag_map = defaultdict(lambda:wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV
    lmtzr = WordNetLemmatizer()
    lemma_list = []
    rmv = [i for i in rmv if i]
    for token, tag in nltk.pos_tag(rmv):
        lemma = lmtzr.lemmatize(token, tag_map[tag[0]])
        lemma_list.append(lemma)
    return lemma_list

welcome_input = ("hello", "hi", "greetings", "sup", "what's up","hey",)
welcome_response = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
def welcome(user_response):
    for word in user_response.split():
        if word.lower() in welcome_input:
            return random.choice(welcome_response)

def generateResponse(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=Normalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    #vals = cosine_similarity(tfidf[-1], tfidf)
    vals = linear_kernel(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0) or "tell me about" in user_response:
        print("Sorry I donot know that")
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response#wikipedia search

flag=True
print("\n\n\n\nParrot : Hello I am your Parrot. Your virtual SME. Ask me anything and If you want to exit, type Bye!")
while(flag==True):
    user_response = input("You : ")
    user_response=user_response.lower()
    if(user_response not in ['bye','shutdown','exit', 'quit']):
        if(user_response=='thanks' or user_response=='thank you' ):
            print("Parrot : You are welcome..")
        else:
            if(welcome(user_response)!=None):
                print("Parrot : "+welcome(user_response))
            else:
                print("Parrot : ",end="")
                print(generateResponse(user_response))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("Parrot : Bye!!! ")