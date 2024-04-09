import requests
import tts
import torch


url = "https://tts-tiktok.p.rapidapi.com/tts/v1/tts-tiktok-1"

querystring = {"response":"url"}

payload = {
	"lang": "english_us",
	"voice": "female_1",
	"text": "Welcome to TTS TikTok API! Transform your text into engaging voiceovers with TikTok-style voices. Create captivating content for your videos, podcasts, and more. Try it now!"
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
	"X-RapidAPI-Host": "tts-tiktok.p.rapidapi.com"
}

response = requests.post(url, json=payload, headers=headers, params=querystring)

print(response.json())