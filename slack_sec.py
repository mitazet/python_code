from slacker import Slacker

token = "set_your_token"
slacker = Slacker(token)
channel_name = "#" + "general"

message = '侵入者あり!!'

if message != '' :
	slacker.chat.post_message(channel_name, message)
