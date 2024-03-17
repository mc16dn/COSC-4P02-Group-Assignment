from ScraperClass import *
from banned_words import *
from mutagen.mp3 import MP3
from moviepy.editor import *
import os
import datetime
import re
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

#Inputs text
#Outputs text with swears replaced with the word REDACTED
def censorTTS(postedstring):
    words =postedstring.split()

    for i , word in enumerate(words):

        if "*" in word:
            words[i]= "REDACTED"
        censored_post = ' '.join(words)

    return censored_post
    
#input a string of text as the text parameter, voice will be either 1, 2 or 3 for different accents
# Will output an mp3 reading text
def textToSpeech(text, voice):

    text = censorTTS(text)
    
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


#Merges the audio and video while also creating subtitles
def merge(text, voice, video):

    #Censoring the text then dividing it into pauses (anything that causes the speaker to pause)
    #The subtitles and the audio are censored differently
    #The word fuck will be censored as f*** in the text but as REDACTED in the audio
    censortext = censorTTS(text)
    words = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\,)\s',text)
    censorwords = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\,)\s', censortext)
    
    #Keeping track of how long each sentence takes
    total = 0
    
    #Merging the audio and video and then cutting it down to the audio's length to make future changes faster
    clip = VideoFileClip(video).subclip(0, MP3("audio.mp3").info.length)
    #The progress bar is hidden for this save so that the user will not believe it is done here
    clip.write_videofile("temp.mp4", audio="audio.mp3", logger=None)
    
    #Creating the clips that make up individual subtitles then putting them in a list
    clip = VideoFileClip("temp.mp4")
    clips = [clip]
    
    #Determining how long a subtitle remains on screen
    for x, word in enumerate(words):
    
        if voice == 1:
            tts = gTTS(censorwords[x], lang="en", tld='us')
            tts.save('sub.mp3')
        
        elif voice == 2:
            tts = gTTS(censorwords[x], lang="en", tld='com.au')
            tts.save('sub.mp3')

        elif voice== 3:
            tts = gTTS(censorwords[x], lang="en", tld='co.uk')
            tts.save('sub.mp3')
        
        pre = total
        total += MP3("sub.mp3").info.length
        
        #Accounting for any pauses caused by commas
        if (words[x][-1] == ","):
            total -= 0.192
        
        #Creating the subtitle
        #This is where you make changes to edit the subtitles
        #https://moviepy-tburrows13.readthedocs.io/en/improve-docs/ref/VideoClip/TextClip.html
        sub = TextClip(words[x], fontsize = 90, color = 'black', size = (clip.w * 0.8,None), method = 'caption', bg_color = 'white')
        sub = sub.set_start(pre)
        sub = sub.set_pos('center').set_duration(total - pre)
        clips.append(sub)

    
    #Adding the clips that have the subtitles
    video = CompositeVideoClip(clips)
    video.write_videofile("end.mp4")
    
    #Removing all temporary data
    os.remove("temp.mp4")
    os.remove("sub.mp3")
    

#Takes the text "I fucking love cats. I love dogs. I love all animals.", cenosrs it, then creates a TTS audiofile that replaced the swear with REDACTED

text = "I fucking love cats. I love dogs. I love all animals."
text = censorText(text)
print(text)

text = Post('https://www.reddit.com/r/stories/comments/1ahp9d1/meditation_practise_has_made_taking_shits_1000x/.json').text
textToSpeech(text, 1)
merge(text, 1, "vid1.mp4")