from slack_rtm import SlackRTM
from slack_api import SlackAPI

with open('token.txt') as f:
	TOKEN = f.readlines()[0][:-1]

api = SlackAPI(TOKEN)
rtm = SlackRTM(TOKEN)
rtm.connect()

channel_list = api.get_channel_list()

for channel in channel_list:
	print(channel.keys())

