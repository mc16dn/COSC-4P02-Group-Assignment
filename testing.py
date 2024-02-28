from ScraperClass import *
from banned_words import *
from MainApp import *

#TESTS

#Censoring

print( "\n" + "Censored text: " + "\n")
print(censorText(Post('https://www.reddit.com/r/stories/comments/1ahp9d1/meditation_practise_has_made_taking_shits_1000x/.json').text))

test_post = Post('https://www.reddit.com/r/stories/comments/1ahp9d1/meditation_practise_has_made_taking_shits_1000x/.json')

#Scrapper
print("URL:", test_post.url)
print("Subreddit:", test_post.subreddit)
print("Text:", test_post.text)
print("Upvotes:", test_post.upvotes)

#URL grabber

#The following tests result in errors

# The category doesn't work
print(grab_url("AskReddit",10,"asdf", "asdf"))
# The time period doesn't work
print(grab_url("AskReddit",10,"top", "asdf"))
# The count is too low
print(grab_url("AskReddit",-10,"top", "month"))
#This will succeed but will only output the 25 avaliable
print(grab_url("AskReddit",10,"top", "month"))

#The following tests succeed

print(grab_url("AskReddit",0,"top", "month"))
print(grab_url("AskReddit",100,"top", "month"))
print(grab_url("AskReddit",5,"hot"))


#Known issues
#The maximum number of posts that can be retrieved is 25 but since that is in excess of a reasonable amount that may not be neccesary
#The function inputs assumes that the subreddit exists
#The function assumes that the input is the correct type

title = "test"
lan = "en"
accent = 'us'
postText = test_post.text


createTTS (postText, title, lan,accent)

words_per_minute = 160 #approximately how fast the us accents talks
maxtime = 60 #max time for youtube shorts is 60seconds
mintime = 15  #a set min time to ensure quality post

print (checkduration (postText, words_per_minute,maxtime,mintime))
