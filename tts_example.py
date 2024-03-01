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
