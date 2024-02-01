# import urllib library 
from urllib.request import urlopen 
  
# import json 
import json 
# store the URL in url as  
# parameter for urlopen 
url = "https://www.reddit.com/r/offmychest/comments/1ad4kiv/my_sister_is_disgusting_and_i_will_never_be_able/.json"
  
# store the response of URL 
response = urlopen(url) 
  
# storing the JSON response  
# from url in data 
data_json = json.loads(response.read()) 
  
# print the json response 
print(data_json) 