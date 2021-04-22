# pip install pytchat
# pip install google_trans_new


from google_trans_new import google_translator  
import pytchat

translator = google_translator()  

link = input("Enter Youtube Stream Link: ") 
while 'watch?v=' not in link:
	link = input("No stream found. Link: ") 

link = link.split("watch?v=")[1]
chat = pytchat.create(video_id = link)

while chat.is_alive():
	try: 
		data = chat.get()
		items = data.items
		for c in data.items:
			translated = translator.translate(c.message, lang_tgt='en')
			print(f"{c.datetime} [{c.author.name}]- {c.message}")
			print(f"{translated}")
	except KeyboardInterrupt:
		chat.terminate()
		break

# Example with member emojis in c.messageEx
# translated
#	: _ Festival This is an idol :: _ Festival This is idol :: _ Festival This is idol :: _ Festival This is idol:
# actual
#	[{'id': '_LepXd3uBYep_AOBjq7oDA', 'txt': ':_まつりわですね:', 'url': 'https://yt3.ggpht.com/yAIfF4fV8GKWFcV9c7uO8DS6FCpjzsFU8DKr0vk1VEBkZqJj8p-L20eiMEm2nYB06Lz4UASLAfM=w24-h24-c-k-nd'}, {'id': '9bepXfmQJYep_AOBjq7oDA', 'txt': ':_まつりちいさいつ:', 'url': 'https://yt3.ggpht.com/7jxtg31N6dJNZ6sWbcD9yMYQ__soMWnOVjmJBPncWpGbsFFFccexkVx-cpGeRVBOaQpH5vchGIQ=w24-h24-c-k-nd'}, {'id': '-bepXdXnEoep_AOBjq7oDA', 'txt': ':_まつりしらしい:', 'url': 'https://yt3.ggpht.com/StfzyoOGvPTZGPrlEOc-wZDBmr43fswivUr3m6cU7EWjd6cLOYIPoE2klmuDzQPi8CTYd1Xz5A=w24-h24-c-k-nd'}, {'id': 'ALipXe65Noep_AOBjq7oDA', 'txt': ':_まつりちいさいよ:', 'url': 'https://yt3.ggpht.com/Qqy2AqsC6P1ierUWtsn0mbx4GshxzSxTMaL5DIUJB1lhk7z5-ssm9NpZWjhsj9Q_fA7K5BEi35M=w24-h24-c-k-nd'}, {'id': '8repXeX3D4ep_AOBjq7oDA', 'txt': ':_まつりいのもじ:', 'url': 'https://yt3.ggpht.com/rt4gq-zBF49Lf1aJw4a5w5-PAXSRVeaAZwOqWTvJ5SrQodYFvK4kCcKr2XTQs72gCZoJ2Hxwzw=w24-h24-c-k-nd'}]