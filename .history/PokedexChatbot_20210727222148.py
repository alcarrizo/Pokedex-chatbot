# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import random  # used to generate random responses
import string  # used to remove punctuationWaT




greetings = ["hello", "hi", "greetings", "sup", "what's up", "hey"]
greetingResponses = (["Hello, I'm Dexter, a pokedex programmed by professor oak for pokemon trainer Ash Ketchum of the town of Pallet. My funtion is to provide Ash with information and advice regarding pokemon and their training. If lost or stolen I can not be replaced."])

botID = "\nDexter The Pokedex: "

pokemonResponse = "Please enter the name or index number of the pokemon you would like me to find.Enter 'return' to return to previous menu"

typeResponse = "Please enter the pokemon type to get a list of corresponding pokemon (pokemon with multiple types will be list in each type). Enter 'return' to return to previous menu"

evolutionResponse ="Please enter the name of the pokemon whose evolution tree you would like to know about.Enter 'return' to return to previous menu"

evolutionOutputResponse = "As of the first generation of pokemon knowledge the evolution of "

confusedResponse = "This pokemon does not exist, or has not been added to my database."

typeConfusedResponse = "This Pokemon Type Doesn't exist."

thanks = ["thanks", "thank you", "cool", "awesome"]
welcomeResponse = "Thank You. GoodBye"

goodbyes = ["bye", "goodbye", "later", "lates", "cya", "cyas", "peace"]
goodbyeResponse = "Goodbye"

# used to consolidate different word forms
lemmer = nltk.stem.WordNetLemmatizer()

# returns cleaned list of consolidated tokens


def lemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

# different method for removing non-alphanumeric characters


def lemNormalize(text):
    return lemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# checks to see if the input text matches one of the greeting_inputs.  If so,
# return one of the random greeting_responses.


def greeting(sentence):
    for word in sentence.split():
        if word.lower() in greetings:
            return random.choice(greetingResponses)


pokemon_types = ["fire", "water", "grass", "fairy", "electric", "ground",
                 "ghost", "normal", "flying", "poison", "bug",
                 "psychic", "fighting", "rock", "steel", "ice", "dragon"]

# Used for identifying nidoran since there is a separate male and female nidoran entry in the pokedex
male_noun = ["male", "boy", "man", "guy"]

female_noun = ["female", "girl", "woman", "gal"]

nvm_word = ["neither", "nevermind", "both"]


def response(user_response):
    bot_response = ''
    TfidfVec = TfidfVectorizer(tokenizer=lemNormalize)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if(req_tfidf == 0):
        return None
    else:
        bot_response = bot_response + out_text[idx]
        return bot_response


def pokemonLookUp():

    # nidorans have different entries depending on if they are male or female
    
    lookup = True
    while lookup == True:
        print(botID + pokemonResponse)
        user_response = input(">>> ")
    
        user_response=user_response.lower()
        
        if(user_response == "return"):
            lookup = False
        elif(user_response in pokemon_types):
            print(botID + " " + confusedResponse)
        else:
            while(user_response == "nidoran"):
                print("\nDid you mean the male or female Nidoran(please enter a noun meaning male or female)")
                word = input().lower()
                if(word in male_noun):
                    user_response = "male nidoran"
                elif(word in female_noun):
                    user_response = "female nidoran"
                elif(word in nvm_word):
                    user_response = word
            if(user_response in nvm_word):
                continue
            
            sent_tokens.append(user_response)
            if(response(user_response) == None):
                print(botID + confusedResponse)
            else:
                print(botID ,end="")
                print(response(user_response))
            
            sent_tokens.remove(user_response)
        
    
def typeLookUp():
    lookup = True
    while lookup == True:
        print(botID + typeResponse)
        user_response = input(">>> ")

        user_response=user_response.lower()
        if(user_response == "return"):
            lookup = False
        elif(user_response not in pokemon_types):
            print(botID + " " + typeConfusedResponse)
        else:
            sent_tokens.append(user_response)
            if(response(user_response) == None):
                print(botID + typeConfusedResponse)
            else:
                print(botID ,end="")
                print(response(user_response))
            
            sent_tokens.remove(user_response)

        
def evolutions():
     
    lookup = True
    while lookup == True:
        print(botID + evolutionResponse)
        user_response = input(">>> ")
    
        user_response=user_response.lower()
        
        if(user_response == "return"):
            lookup = False
        elif(user_response in pokemon_types):
            print(botID + " " + confusedResponse)
        else:
            while(user_response == "nidoran"):
                print("\nDid you mean the male or female Nidoran(please enter a noun meaning male or female)")
                word = input().lower()
                if(word in male_noun):
                    user_response = "male nidoran"
                elif(word in female_noun):
                    user_response = "female nidoran"
                elif(word in nvm_word):
                    user_response = word
            if(user_response in nvm_word):
                continue
            
            sent_tokens.append(user_response)
            if(response(user_response) == None):
                print(botID + confusedResponse)
                
            else:
                print(botID ,end="")
                print(evolutionOutputResponse + user_response +" is " + response(user_response))
                
            sent_tokens.remove(user_response)
            


flag = True

while(flag == True):
    print()
    print("Welcome to the kanto Pokedex please choose one of the following:")
    print("1.Pokemon look-up")
    print("2.Pokemon Type")
    print("3.Pokemon evolutions")
    print("enter 'exit' to exit")
    print("You may also enter things unrelated to the above, but only the above will advance past this choice")
    
    choice = input(">>> ")
    choice = choice.lower()
    
    if(choice == "1"):
        
        with open("pokedexInput.txt", 'r') as myFile1:
            data1 = myFile1.read()

        sent_tokens = data1.split("@")
        
        with open("pokedexOutput.txt", 'r') as myFile2:
            data2 = myFile2.read()

        out_text = data2.split("@")
        
        pokemonLookUp()
    elif(choice == "2"):
        with open("pokedexTypeInput.txt", 'r') as myFile1:
            data1 = myFile1.read()

        sent_tokens = data1.split("@")
        
        with open("pokedexTypeOutput.txt", 'r') as myFile2:
            data2 = myFile2.read()

        out_text = data2.split("@")
        
        typeLookUp()
    elif(choice == "3"):
        with open("pokedexEvolutionInput.txt", 'r') as myFile1:
            data1 = myFile1.read()

        sent_tokens = data1.split("@")
        
        with open("pokedexEvolutionOutput.txt", 'r') as myFile2:
            data2 = myFile2.read()

        out_text = data2.split("@")

        out_text = data2.split("@")
        
        evolutions()
        
    elif(choice == "exit"):
        flag = False
    
    else:    
        if choice not in goodbyes:
            if choice in thanks:
                flag=False
                print(botID + welcomeResponse)
            else:
                if(greeting(choice)!=None):
                    print(botID + greeting(choice))
        else:
            flag=False
            print(botID + goodbyeResponse)
        
    # print(botID + normalResponse)
    # user_response = input(">>>")
    
    # user_response=user_response.lower()
    # # nidorans hae different entries depending on if they are male or female
    # if(user_response == "nidoran"):
    #     while(user_response == "nidoran"):
    #         print("\nDid you mean the male or female Nidoran(please enter a noun meaning male or female)")
    #         word = input().lower()
    #         if(word in male_noun):
    #             user_response = "male nidoran"
    #         elif(word in female_noun):
    #             user_response = "female nidoran"
    #         elif(word in nvm_word):
    #             user_response = word
    # if(user_response in nvm_word):
    #     continue            
    # if user_response not in goodbyes:
    #     if user_response in thanks:
    #         flag=False
    #         print(botID + welcomeResponse)
    #     else:
    #         if(greeting(user_response)!=None):
    #             print(botID + greeting(user_response))
    #         else:
    #             sent_tokens.append(user_response)
    #             print(botID ,end="")
    #             print(response(user_response))
    #             sent_tokens.remove(user_response)
    # else:
    #     flag=False
    #     print(botID + goodbyeResponse)
