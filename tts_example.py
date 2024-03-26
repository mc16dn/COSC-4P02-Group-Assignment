from gtts import gTTS
import requests

#lang is language, should always be en
#tld is accent, us is american, com.au is Australian, and co.uk is British
#for more options https://gtts.readthedocs.io/en/latest/module.html#localized-accents

tts = gTTS("The quick brown fox jumps over the lazy dog", lang="en", tld='us')
tts.save('first.mp3')
tts = gTTS("The quick brown fox jumps over the lazy dog", lang="en", tld='com.au')
tts.save('second.mp3')
tts = gTTS("The quick brown fox jumps over the lazy dog", lang="en", tld='co.uk')
tts.save('third.mp3')

#input a string of text as the text parameter, voice will be either 1, 2 or 3 for different accents
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
