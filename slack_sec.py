from slacker import Slacker

token = "xoxb-87096200673-iz0rDH8bKYieCGojbrrncmyZ"
slacker = Slacker(token)
channel_name = "#" + "general"

message = '侵入者あり!!'

if message != '' :
	slacker.chat.post_message(channel_name, message)
