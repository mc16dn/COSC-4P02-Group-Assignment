from ScraperClass import *
from banned_words import *
import urllib.request
import os
import datetime
import numpy


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
        data = urllib.request.urlopen("https://www.reddit.com/r/"+sub+"/"+category+".json?t="+time).read().decode("utf-8")
    else:
        data = urllib.request.urlopen("https://www.reddit.com/r/"+sub+"/"+category+".json").read().decode("utf-8")
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
        out.append(data[:data.find('", ')])
    
    return (out)

#censors inputed text from urlgrabber then replace banned
#words with * and returns censored post
def censorText(postedstring):
    words =postedstring.split()

    for i , word in enumerate(words):

        if word.lower() in banned_words:
            words[i]= '*'*len(word)
        censored_post = ' '.join(words)

    return censored_post

#TESTS

print(censorText(" Input Banned words here for testing"))

#The following tests result in errors

#The category doesn't work
print(grab_url("AskReddit",10,"asdf", "asdf"))
#The time period doesn't work
print(grab_url("AskReddit",10,"top", "asdf"))
#The count is too low
print(grab_url("AskReddit",-10,"top", "month"))

#This will succeed but will only output the 25 avaliable
print(grab_url("AskReddit",100,"top", "month"))

#The following tests succeed

print(grab_url("AskReddit",0,"top", "month"))
print(grab_url("AskReddit",10,"top", "month"))
print(grab_url("AskReddit",20,"hot"))


#Known issues
#The maximum number of posts that can be retrieved is 25 but since that is in excess of a reasonable amount that may not be neccesary
#The function inputs assumes that the subreddit exists
#The function assumes that the input is the correct type
