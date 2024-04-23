import subprocess
import sys
import os

try:
    import pandas
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])
    import pandas

try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    
try:
    from analytix import Client
except:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "analytix"])
    from analytix import Client
    
from ScraperClass import *
from banned_words import *
from createAnalytics import*
import datetime
import re
import threading
from VideoPlayer import VideoPlayer

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

#Importing tkinter
import tkinter as tk
from tkinter import filedialog, ttk


#Importing playsound
try:
    import playsound as playsound
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install","--upgrade", "wheel"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playsound==1.2.2"])
    import playsound as playsound

#Importing mutagen
try:
    from mutagen.mp3 import MP3
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mutagen"])
    from mutagen.mp3 import MP3
    
#Importing gtts
try:
    from gtts import gTTS
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "gTTS"])
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
        y = data.find('url":')+7
        #In the case that there aren't enoug posts to fill the requested amount it will simply return what it could gather
        if (y == 6):
            print("{}{}{}".format("Error: There aren't enough entries, returning first ", x, " posts"))
            return (out)
        data = data[y:]
        out.append(Post(data[:data.find('", ')]+".json"))
    return (out)

#censors inputed text from urlgrabber then replace banned
#words with * and returns censored post

def censorText(postedstring):
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
        
        if word.lower() in banned_words:
            words[i]= "Redacted"
        censored_post = ' '.join(words)

    return censored_post
    
#input a string of text as the text parameter, voice will be either 1, 2 or 3 for different accents
# Will output an mp3 reading text
def textToSpeech(text, voice):
    print("Generating Audio")
    
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
#The categories for videos are lighthearted and seriuous
def merge(text, voice, video, category):

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
        clip = VideoFileClip(os.getcwd()+"\\videos\\"+category+"\\"+video).subclip(0, MP3(os.getcwd()+"\\audio.mp3").info.length)
    else:
        #If the audio is longer than the video then the video will loop until it reaches the same length
        clip = VideoFileClip(os.getcwd()+"\\videos\\"+category+"\\"+video).loop(duration = MP3(os.getcwd()+"\\audio.mp3").info.length)
    #The progress bar is hidden for this save so that the user will not believe it is done here
    clip.write_videofile(os.getcwd()+"\\temp.mp4", audio=os.getcwd()+"\\audio.mp3", logger=None)
    
    #Creating the clips that make up individual subtitles then putting them in a list
    clip = VideoFileClip(os.getcwd()+"\\temp.mp4")
    clips = [clip]
    
    #Determining how long a subtitle remains on screen
    for x, word in enumerate(words):
        
        print("Generating subtitles: " + str(x + 1) + " out of " + str(len(words)))
        
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
        total += MP3(os.getcwd()+'\\sub.mp3').info.length - 0.1
        
        #Creating the subtitle
        #This is where you make changes to edit the subtitles
        #https://moviepy-tburrows13.readthedocs.io/en/improve-docs/ref/VideoClip/TextClip.html
        sub = TextClip(words[x], fontsize = 80, color = 'white', size = (clip.w,None), method = 'caption',font='Arial-Bold', stroke_color='black', stroke_width=4)
        sub = sub.set_start(pre)
        sub = sub.set_pos('top','center').margin(top=450, opacity=0).set_duration(total - pre)
        clips.append(sub)

    
    #Adding the clips that have the subtitles
    video = CompositeVideoClip(clips)
    video.write_videofile(os.getcwd()+"\\end.mp4",logger="bar")
    
    #Removing all temporary data
    os.remove(os.getcwd()+"\\temp.mp4")
    os.remove(os.getcwd()+"\\sub.mp3")

def sub_category(title):
    global address
    address = []
    #lighthearted
    #Because there is some overlap it is not an elif
    if title in ["PettyRevenge", "NuclearRevenge", "TIFU", "TalesFromTechSupport", "TalesFromRetail", "EntitledParents"]:
        address.append("lighthearted")
    #Serious
    if title in ["TIFU", "confessions", "confession","OffMyChest","TrueOffMyChest","AmItheAsshole","LegalAdvice"]:
        address.append("serious")
        
    address.append("custom")
    x = 0
    
    out = []
    
    for i in address:
        address[x] = os.path.dirname(__file__) + '\\videos\\' + address[x]
        out.extend(os.listdir(address[x]))
        if "Read me.txt" in out:
            out.remove("Read me.txt")
        x += 1

    return out

#GUI
def cancel():
    window.destroy()

def play():
    if audio_dropdown.get() == "American":
        playsound.playsound(os.path.dirname(__file__) + '\\sample1.mp3')
    elif audio_dropdown.get() == "Australian":
        playsound.playsound(os.path.dirname(__file__) + '\\sample2.mp3')
    else:
        playsound.playsound(os.path.dirname(__file__) + '\\sample3.mp3')

def isint(entry):
    if entry == "":
        warning_label.config(text = "Warning: Number of Subreddits is empty")
        return True
    elif str.isdigit(entry):
        if int(entry)<= 20 and int(entry) >= 0:
            if int(entry)>=10:
                warning_label.config(text = "Warning: Due to long loading times it is recommended to grab less then 10 Subreddits")
            else:
                warning_label.config(text = "")
            return True
    return False

def change_page(frame):
    frame.tkraise()

def change_page_posts(frame):
    #selection modifer 
    if(date_var.get()=='past hour'):
        t="hour"
    elif(date_var.get()=='past day'):
        t="day"
    elif(date_var.get()=='past week'):
        t="week"
    elif(date_var.get()=='past month'):    
        t="month"    
    elif(date_var.get()=='past year'):
        t="year"

    subs = grab_url(sub_var.get(), int(sub_count_var.get()), type_var.get(),t)
    sub_titles = []
    global sub_list
    sub_list = []
    for temp in subs:
        sub_titles.append(temp.title)
        sub_list.append(temp.text)
    sub_choice_dropdown['values'] = (sub_titles)
    if len(sub_list) == 0:
        warning_label.config(text = "Warning: There are no posts that fit your requirements")
    else:
        text.delete('1.0', tk.END)
        text.insert(tk.END,sub_list[0])
        sub_choice_dropdown.current(0)
        frame.tkraise()

def descriptionchange(frame):
    global sub_list
    text.delete('1.0', tk.END)
    text.insert(tk.END,sub_list[sub_choice_dropdown.current()])

def change_page_template(frame):
    vid_dropdown['values'] = sub_category(sub_var.get())
    vid_dropdown.current(0)
    frame.tkraise()
def change_page_analytics(frame):
    if (os.path.isfile('secrets.json')):
        ytAnalytics() #This will get information from a youtube channel assuming a secrets.json file is supplied
    
    generateYTAnalytics(2023,5,4,categories)  
    graphsDir = os.listdir('./Outputs/')
    analytics_date_dropdown['values'] = graphsDir
    analytics_date_dropdown.current(0)
    frame.tkraise()

def openfile():
   global filepath
   filepath=filedialog.askopenfilename()
  

def open_video():

    if vid_dropdown.get()[:3] == "lig":
        path = "lighthearted"

    elif vid_dropdown.get()[:3] == "ser":
        path = "serious"
    
    else:
        path = "custom"
        
    vp=VideoPlayer(os.getcwd()+"\\videos\\"+path+"\\"+vid_dropdown.get())
    vp.mainloop()

def final_video(file):
    vp=VideoPlayer(file)
    vp.mainloop()
    
def change_final(frame):
    
    if vid_dropdown.get()[:3] == "lig":
        path = "lighthearted"
    
    else:
        path = "serious"

    text = censorText(sub_list[sub_choice_dropdown.current()])
    textToSpeech(text, audio_dropdown.current() + 1)
    merge(text, audio_dropdown.current() + 1,vid_dropdown.get(), path)
    vp=VideoPlayer(os.getcwd()+"\\end.mp4")
    vp.mainloop()

def createGraph(fileName, category):
    x=[]
    y=[]
    
    with open ('./Outputs/'+fileName, 'r') as csvFile:
        lines = csv.reader(csvFile)

        for row in lines:
            if (row[0] == 'day'):
                col = row.index(category)
            else:
             
                x.append(row[0])
                y.append(int(row[col]))

    ax.cla()
    ax.plot(x,y)
    
    ax.tick_params(axis = 'x', rotation=90)
    ax.set_xlabel('date')
    ax.set_ylabel(category)
    graph_canvas.draw()

# Create the main window
window = tk.Tk()
page_one = tk.Frame(window)
page_two = tk.Frame(window)
page_three = tk.Frame(window)
page_four = tk.Frame(window)
for frame in (page_one, page_two, page_three, page_four):
    frame.grid(row=0, column=0, stick="news")

window.title("Video and Permutation Selector")

# Set the default size of the window
window.geometry("650x700")  # Increased width to better fit the welcome text

# Configure grid layout
window.columnconfigure(0, weight=1)
window.rowconfigure([0, 1, 2, 3, 4, 5], weight=1)

# Variables for dropdowns
date_var = tk.StringVar()
vid_var = tk.StringVar()
perm_var = tk.StringVar()
audio_var = tk.StringVar()
sub_var = tk.StringVar()
sub_count_var = tk.StringVar()
title_var = tk.StringVar()
type_var = tk.StringVar()
global sub_list
sub_list = []

# Welcome text label
welcome_text = ("Welcome to our 4P02 final video production tool! This tool was developed in "
                "order to create a video production pipeline to create content for short form "
                "video platforms, as well as deployment and determining what performs well. "
                "Please use the following menus to move forward!")
welcome_label = ttk.Label(page_one, text=welcome_text, wraplength=550, justify="center")
welcome_label.grid(column=0, row=0, padx=10, pady=10, sticky=tk.EW)

# Page one for scrapping subreddits

sub_label = ttk.Label(page_one, text="Select Subreddit:")
sub_label.grid(column=0, row=1, padx=10, pady=5, sticky=tk.W)

sub_dropdown = ttk.Combobox(page_one, textvariable=sub_var)
sub_dropdown['values'] = ("PettyRevenge", "NuclearRevenge", "TIFU", "TalesFromTechSupport", "TalesFromRetail", "EntitledParents", "confessions", "confession","OffMyChest","TrueOffMyChest","AmItheAsshole","LegalAdvice")
sub_dropdown.current(0)
sub_dropdown['state'] = 'readonly'
sub_dropdown.grid(column=0, row=2, padx=10, pady=5, sticky=tk.EW)

type_label = ttk.Label(page_one, text="Select Sorting:")
type_label.grid(column=0, row=3, padx=10, pady=5, sticky=tk.W)

type_dropdown = ttk.Combobox(page_one, textvariable=type_var)
type_dropdown['values'] = ("top", "hot", "new")
type_dropdown.current(0)
type_dropdown['state'] = 'readonly'
type_dropdown.grid(column=0, row=4, padx=10, pady=5, sticky=tk.EW)

date_label = ttk.Label(page_one, text="Select time interval for post date (this will not do anything unless top is chosen):")
date_label.grid(column=0, row=5, padx=10, pady=5, sticky=tk.W)

date_dropdown = ttk.Combobox(page_one, textvariable=date_var)
date_dropdown['values'] = ('past hour', 'past day', 'past week', 'past month', 'past year', 'all')
date_dropdown.current(1)
date_dropdown['state'] = 'readonly'
date_dropdown.grid(column=0, row=6, padx=10, pady=5, sticky=tk.EW)


count_label = ttk.Label(page_one, text="Select 1-20 Subreddits:")
count_label.grid(column=0, row=7, padx=10, pady=5, sticky=tk.W)
count_entry = tk.Entry(page_one, textvariable = sub_count_var)
checkint = page_one.register(isint)
count_entry.config(validate="all", validatecommand = (checkint, '%P'))
count_entry.grid(column=0, row=8, padx=10, pady=5, sticky=tk.EW)

warning_label = ttk.Label(page_one, text="Warning: Number of Subreddits is empty")
warning_label.grid(column=0, row=9, padx=10, pady=5, sticky=tk.W)

disclaimer_label = warning_label = ttk.Label(page_one, text="If there is no secrets file in the project file, CheckAnalysis \nwill run with a randomly generated example")
disclaimer_label.grid(column = 0, row = 11, padx = 180, pady=9, sticky=tk.W)

# Buttons
cancel_button = ttk.Button(page_one, text="Cancel", command=cancel)
cancel_button.grid(column=0, row=10, padx=10, pady=10, sticky=tk.E)

next_one_button = ttk.Button(page_one, text="Grab Reddit posts", command=lambda:change_page_posts(page_two))
next_one_button.grid(column=0, row=10, padx=10, pady=10, sticky=tk.W)

sign_in_button = ttk.Button(page_one, text="Check Youtube Analytics", command=lambda:change_page_analytics(page_four))
sign_in_button.grid(column=0, row=10, padx=200, pady=10, sticky=tk.W)

#Page two for choosing the specific post

sub_choice_label = ttk.Label(page_two, text="Select Post:")
sub_choice_label.place(x = 10, y = 10)

sub_choice_dropdown = ttk.Combobox(page_two, textvariable=title_var, width = 85)
sub_choice_dropdown.bind("<<ComboboxSelected>>", descriptionchange)
sub_choice_dropdown['state'] = 'readonly'
sub_choice_dropdown.grid(column=0, row=0, padx=10, pady=5, sticky=tk.EW)

fr = tk.Frame(page_two)
fr.place(x = 10, y = 70)

scroll = tk.Scrollbar(fr)
text = tk.Text(fr, height = 20, width = 65, yscrollcommand=scroll.set)
scroll.config(command=text.yview)
text.pack(side="left")


back_button = ttk.Button(page_two, text="Back", command=lambda:change_page(page_one))
back_button.grid(column=0, row=1, padx=10, pady=10, sticky=tk.E)

next_two_button = ttk.Button(page_two, text="Next page", command=lambda:change_page_template(page_three))
next_two_button.grid(column=0, row=1, padx=10, pady=10, sticky=tk.W)

#Page three for choosing video templates and voice

vid_description = ttk.Label(page_three, text="Select Template:")
vid_description.grid(column = 1, row=0, padx=10, pady=5, sticky=tk.EW)

vid_dropdown = ttk.Combobox(page_three, textvariable=vid_var)
vid_dropdown['values'] = ()
vid_dropdown['state'] = 'readonly'
vid_dropdown.grid(column=1, row=1, padx=10, pady=5, sticky=tk.EW)


audio_label = ttk.Label(page_three, text="Select Voice:")
audio_label.grid(column=1, row=3, padx=10, pady=5, sticky="w")

audio_dropdown = ttk.Combobox(page_three, textvariable=audio_var)
audio_dropdown['values'] = ("American", "Australian", "British")
audio_dropdown.current(0)
audio_dropdown['state'] = 'readonly'
audio_dropdown.grid(column=1, row=5, padx=10, pady=5, sticky=tk.W)


audio_preview = ttk.Button(page_three, text="Sample", command=play)
audio_preview.grid(column=2, row=5, padx=10, pady=10, sticky=tk.W)

length_warning = ttk.Label(page_three, text="Warning: video generation can take 10-50 minutes")
length_warning.grid(column=1, row=6, padx=10, pady=10, sticky=tk.E)

back_three_button = ttk.Button(page_three, text="Back", command=lambda:change_page(page_two))
back_three_button.grid(column=2, row=7, padx=10, pady=20, sticky=tk.E)

next_three_button = ttk.Button(page_three, text="Generate Video", command=lambda:change_final(page_three))
next_three_button.grid(column=1, row=7, padx=10, pady=20, sticky=tk.W)

video_button =tk.Button(page_three, text="preview Video", command=lambda:open_video())
video_button.grid(column=2, row=1, padx=10, pady=5, sticky=tk.E)


#page four for generating analytics
fr = tk.Frame(page_four)

categories = []
with open('template.csv') as col:
    lines = csv.reader(col, delimiter = ',')
    categories = list(lines)[0]
   
date_label = ttk.Label (page_four, text="Select the date")
date_label.grid(column=1, row=1, padx=20, pady=5, sticky="w")

category_label = ttk.Label (page_four, text="Select the category")
category_label.grid(column=2, row=1, padx=10, pady=5, sticky="w")

analytics_date_dropdown = ttk.Combobox(page_four, width = 40)
analytics_date_dropdown.grid(column=1, row=50, padx= 20, pady=0, sticky=tk.EW)

analytics_date_dropdown['state'] = 'readonly'

analytics_category_dropdown = ttk.Combobox(page_four, values= categories[1:], width = 40)
analytics_category_dropdown.grid(column=2, row=50, padx= 10, pady=0, sticky=tk.EW)
analytics_category_dropdown.current(0)
analytics_category_dropdown['state'] = 'readonly'

analytics_confirmation_button = tk.Button(page_four, text="view graph", command=lambda:createGraph(str(analytics_date_dropdown.get()),analytics_category_dropdown.get()))
analytics_confirmation_button.grid (column=1, row=150, columnspan= 2,padx= 20, pady=0, sticky=tk.EW)

fig = Figure()
ax = fig.add_subplot()
graph_canvas = FigureCanvasTkAgg(fig, master = page_four)
graph_canvas.get_tk_widget().grid(column=0, row=250,columnspan=3, padx= 20, pady=20)
# Start the GUI event loop
change_page(page_one)
window.mainloop()
