import subprocess
import sys
import os
from ScraperClass import *
from banned_words import *
import datetime
import re
from gtts import gTTS


#Checking if ImageMagick has been installed and if Moviepy is correctly pointing to ImageMagick
if not os.path.exists(os.environ["ProgramFiles"]+"\\ImageMagick-7.1.1-Q16-HDRI"):
    raise Exception("ImageMagick has not been installed, please use the EXE provided and select Install legacy untilities during Select Additional Tasks.")
elif not os.path.exists(os.environ["ProgramFiles"]+"\\ImageMagick-7.1.1-Q16-HDRI\\convert.exe"):
    raise Exception("ImageMagick has been installed but the legacy utilities have not been added, please reinstall and select Install legacy utilites during Select Additional Tasks.")

#Checking if moviepy exists and importing it if it doesn't
try:
    from moviepy.editor import *
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy"])
    out = subprocess.Popen([sys.executable, "-m", "pip", "show", "moviepy"])
    
    out = subprocess.check_output(["pip", "show", "moviepy"]).decode()
    out = out[out.find("Location")+10:out.find("Requires")-2]+"\\moviepy\\config_defaults.py"
    
    with open(out, 'r',encoding='utf-8') as file:
        data = file.readlines()
    data[-1] = "IMAGEMAGICK_BINARY = r"+'"'+ os.environ["ProgramFiles"]+"\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"+'"'

    with open(out, 'w',encoding='utf-8') as file:
        file.writelines(data)
    from moviepy.editor import *
except IOError:
    out = subprocess.Popen([sys.executable, "-m", "pip", "show", "moviepy"])
    
    out = subprocess.check_output(["pip", "show", "moviepy"]).decode()
    out = out[out.find("Location")+10:out.find("Requires")-2]+"\\moviepy\\config_defaults.py"
    
    with open(out, 'r',encoding='utf-8') as file:
        data = file.readlines()
    data[-1] = "IMAGEMAGICK_BINARY = r"+'"'+ os.environ["ProgramFiles"]+"\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"+'"'

    with open(out, 'w',encoding='utf-8') as file:
        file.writelines(data)
    from moviepy.editor import *


#Importing mutagen
try:
    from mutagen.mp3 import MP3
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mutagen"])
    from mutagen.mp3 import MP3
    

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
        
        out.append(Post(data[:data.find('", ')]+".json").url)
    
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

    elif voice== 4:
        tts = gTTS(text, lang="en", tld='ie')
        tts.save('audio.mp3')

    elif voice==5:
        tts = gTTS(text, lang="en", tld='co.in')
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
    if MP3(os.getcwd()+"\\audio.mp3").info.length < 120:
        #Merging the audio and video and then cutting it down to the audio's length to make future changes faster
        clip = VideoFileClip(os.getcwd()+"\\"+video).subclip(0, MP3(os.getcwd()+"\\audio.mp3").info.length)
    else:
        #If the audio is longer than the video then the video will loop until it reaches the same length
        clip = VideoFileClip(os.getcwd()+"\\"+video).loop(duration = MP3(os.getcwd()+"\\audio.mp3").info.length)
    #The progress bar is hidden for this save so that the user will not believe it is done here
    clip.write_videofile(os.getcwd()+"\\temp.mp4", audio=os.getcwd()+"\\audio.mp3", logger=None)
    
    #Creating the clips that make up individual subtitles then putting them in a list
    clip = VideoFileClip(os.getcwd()+"\\temp.mp4")
    clips = [clip]
    
    #Determining how long a subtitle remains on screen
    for x, word in enumerate(words):
    
        if voice == 1:
            tts = gTTS(censorwords[x], lang="en", tld='us')
            tts.save(os.getcwd()+'\\sub.mp3')
        
        elif voice == 2:
            tts = gTTS(censorwords[x], lang="en", tld='com.au')
            tts.save(os.getcwd()+'\\sub.mp3')

        elif voice== 3:
            tts = gTTS(censorwords[x], lang="en", tld='co.uk')
            tts.save(os.getcwd()+'\\sub.mp3')
        
        pre = total
        total += MP3(os.getcwd()+'\\sub.mp3').info.length
        
        #Accounting for any pauses caused by commas
        if (words[x][-1] == "," or words[x][-1] == "."):
            total -= 0.1
        
        #Creating the subtitle
        #This is where you make changes to edit the subtitles
        #https://moviepy-tburrows13.readthedocs.io/en/improve-docs/ref/VideoClip/TextClip.html
        sub = TextClip(words[x], fontsize = 110, color = 'white', size = (clip.w * 0.8,None), method = 'caption', stroke_color='black', stroke_width=4)
        sub = sub.set_start(pre)
        sub = sub.set_pos('top','center').margin(top=450, opacity=0).set_duration(total - pre)
        clips.append(sub)

    
    #Adding the clips that have the subtitles
    video = CompositeVideoClip(clips)
    video.write_videofile(os.getcwd()+"\\end.mp4")
    
    #Removing all temporary data
    os.remove(os.getcwd()+"\\temp.mp4")
    os.remove(os.getcwd()+"\\sub.mp3")
    

#Takes the text "I fucking love cats. I love dogs. I love all animals.", censors it, then creates a TTS audiofile that replaced the swear with REDACTED but still have the subtitles as f******

text = "I fucking love cats. I love dogs. I love all animals."
text = censorText(text)
print(text)
textToSpeech(text, 1)

#merge(text, voice option, video file)

t=grab_url("OffMyChest",1,"top")
t=t[0]

text = Post('https://www.reddit.com/r/offmychest/comments/184umwe/i_gotta_get_this_off_my_chest/.json').text
print(text)
text = censorText(text)
textToSpeech(text, 1)
merge(text, 1, "vid2.mp4")
