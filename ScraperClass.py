import json
from urllib.request import urlopen

class Post: 
    def __init__(self, url): 
        self.url = url
        self.subreddit = None
        self.text = None
        self.upvotes = None
        self.get_data()

    def get_data(self):
        # Fetch and load the JSON data from the URL
        connect = False
        while not connect:
            try:
                response = urlopen(self.url)
                connect = True
            except:
                pass
        data_json = json.loads(response.read())

        # Extract data from the first post in the JSON data
        if data_json and 'data' in data_json[0]:
            for child in data_json[0]['data'].get('children', []):
                post_data = child.get('data', {})
                
                # Set the instance attributes based on the data
                self.upvotes = post_data.get('ups', 0)  # Replace 'ups' with the correct key if different
                self.subreddit = post_data.get('subreddit', 'Unknown Subreddit')
                self.title = post_data.get('title', 'No Title')
                self.text = post_data.get('selftext', 'No Text')

# example of how to run this
#test_post = Post('https://www.reddit.com/r/stories/comments/1ahp9d1/meditation_practise_has_made_taking_shits_1000x/.json')

#print("URL:", test_post.url)
#print("Subreddit:", test_post.subreddit)
#print("Text:", test_post.text)
#print("Upvotes:", test_post.upvotes)
