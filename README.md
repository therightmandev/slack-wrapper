slack-wrapper
=============

##Example:
	from slack_wrapper import SlackAPI, SlackRTM
	
	with open('token.txt') as f:
	        TOKEN = f.readlines()[0][:-1]
	
	# Create RTM and API instances:
	api = SlackAPI(TOKEN)
	rtm = SlackRTM(TOKEN)
	
	# ~~Using the API:~~ #
	#Get the list of channels:
	channel_list = api.get_channel_list()
	
	#Get a channel name:
	my_channel_name = api.get_channel_name('C0H0SR40J') # returns a name based on the ID
	
	#Get a channel id:
	my_channel_id = api.get_channel_id(my_channel_name) # returns "C0H0MG0F6"
	
	
	# ~~RTM~~ #
	rtm.connect() #connects to a Real Time Messaging websocket
	
	#the following loop receives 5 events and logs them on the terminal
	#usually this would be an infinite loop and the events would be handledapproprietly
	for x in range(5):
	        print(rtm.receive_dict())
	
	#send a message through RTM:
	rtm.msg("hey, sorry for spam, just testing", my_channel_id)
