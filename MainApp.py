from ScraperClass import *
from banned_words import *
from urllib.request import urlopen
import os
import datetime
import numpy
from gtts import gTTS

#Inputs subreddit name, the number of post taken, ordering used, and how far back posts go
#Outputs a list of strings that contains the URLs of each posts
def grab_url(sub, count, category, time=None):

    #Preventing bad inputs from being used
    if category not in ['top', 'hot', 'new']:
        print("Error: The category "+category+" does not exist")
        return None
    if (count < 0):
        print("Error: Please input a count higher than 0")
        return None
    if time not in ['hour', 'day', 'week', 'month', 'year', 'all', None]:
        print("Error: The time "+time+" does not exist")
        return None

    #Retrieving the json data
    #If no time is given for a top then it defaults to a month
    if category == "top":
        if time == None:
            time = "month"
        
        connect = False
        while not connect:
            try:
                data = urlopen("https://www.reddit.com/r/"+sub+"/"+category+".json?t="+time).read().decode("utf-8")
                connect = True
            except:
                pass
            
    else:
        connect = False
        while not connect:
            try:
                data = urlopen("https://www.reddit.com/r/"+sub+"/"+category+".json").read().decode("utf-8")
                connect = True
            except:
                pass
                
    out = []

    #Retrieving the URLs and removing all useless data as it loops
    for x in range(count):
        y = 0
        y = data.find("url")+7

        #In the case that there aren't enoug posts to fill the requested amount it will simply return what it could gather
        if (y == 6):
            print("{}{}{}".format("Error: There aren't enough entries, returning first ", x, " posts"))
            return (out)
        data = data[y:]
        
        out.append(Post(data[:data.find('", ')]+".json"))
    
    return (out)

#censors inputed text from urlgrabber then replace banned
#words with * and returns censored post

def  censorText(postedstring):
    words =postedstring.split()

    for i , word in enumerate(words):

        if word.lower() in banned_words:
            words[i]= words[i][0]+'*'*(len(word)-1)
        censored_post = ' '.join(words)

    return censored_post



#Creates a tts given a string of the text fro mthe posts and creates a mp3 file of it
#Title: the title of the post
def createTTS(postedstring,title, lan, accent):
    tts = gTTS (postedstring, lang =lan, tld=accent)
    tts.save(title+'.mp3')



#Will return true if the duration is within the constraints and false if it is not. 
#The constraints are set by the words_per_minute parameter and can be adjusted accordingly
#maxTime: maximum amount of time of a video given in seconds. 
#fileName: name or location of the txt file that will be read
def checkduration(postedstring, words_per_minute, maxTime, minTime):
    words_per_second = words_per_minute / 60    #used to calculate the maxlength of  the video below
    maxLength = maxTime * (words_per_minute/60) #This will calculate the maximum number of words in the video

    length = len(postedstring.split())

    if (length <= maxLength):
        return True
    else:
        return False


#input a string of text as the text parameter, voice will be either 1, 2 or 3 for different accents
# Will output an mp3 reading text
def textToSpeech(text, voice):

    if voice == 1:
        tts = gTTS(text, lang="en", tld='us')
        tts.save('audio.mp3')
        

    elif voice == 2:
        tts = gTTS(text, lang="en", tld='com.au')
        tts.save('audio.mp3')

    elif voice== 3:

        tts = gTTS(text, lang="en", tld='co.uk')
        tts.save('audio.mp3')

    else:
        # Default case if param is not 1, 2, or 3
        return "Invalid entry to text to voice function"
    


textToSpeech("I love cats", 1)
