import unittest, sys
from unittest.mock import MagicMock

import slack_wrapper, json
from slack_wrapper import API, RTM


class TestAPI(unittest.TestCase):

	def setUp(self):
		self.TOKEN = 'some_token'
		self.api = API(self.TOKEN)
		#Mock the API(these values are needed for other tests too):
		self.mock_response = MagicMock()
		self.original_mock_response = MagicMock()
		self.api.session = MagicMock()
		self.expected_value = {'ok': True, 'channels': [{'name': 'general', 'id': '123'}, {'name': 'off-topic', 'id': '456'}]}
		self.mock_response.json.return_value = self.expected_value
		self.api.session.get.return_value = self.mock_response
		self.test_channel_list = [{'id': 'C024BE91L', 'name': 'fun', 'created': '1360782804'}]
	
	def test_has_error_expecting_true(self):
		self.assertEqual(self.api.has_error({'ok': False, 'error': 'Some error'}), True)

	def test_has_error_expecting_false(self):
		self.assertEqual(self.api.has_error({'ok': True, 'error': 'Some error'}), False)

	def test_api_method_expecting_dict(self):
		self.tested_method = 'channels.list'
		self.extra_param_key = 'channel'
		self.extra_param_value = 'C024BE91L'
		self.assertEqual(self.api.api_method(self.tested_method, {self.extra_param_key: self.extra_param_value}), self.expected_value)
		self.assertEqual(
			self.api.session.get.call_args_list,
			[
				(
					(self.api.domain+self.tested_method,),
					{'params': {'token': self.TOKEN, self.extra_param_key: self.extra_param_value}}
				)
			]
		)

	def test_get_channel_list_expecting_list(self):
		self.assertEqual(self.api.get_channel_list(),self.expected_value['channels'])

	def test_get_channel_list_expecting_none(self):
		self.original_mock_response.json.return_value = self.mock_response.json.return_value
		self.mock_response.json.return_value = {'ok': False, 'error': 'Some error'}
		self.assertEqual(self.api.get_channel_list(), None)
		self.mock_response.json.return_value = self.original_mock_response.json.return_value

	def test_get_channel_name_and_get_channel_id(self):
		self.test_index = 0
		self.assertEqual(self.api.get_channel_id(self.api.get_channel_name(self.expected_value['channels'][self.test_index]['id'])), self.expected_value['channels'][self.test_index]['id'])


class TestRTM(unittest.TestCase):
    def setUp(self):
        self.mock_response = MagicMock()
        self.mock_response_dict = {'ok': True, 'url': 'http://example.com'}
        self.TOKEN = 'some_token'
        self.rtm = RTM(self.TOKEN)
        #mock requests session:
        self.mock_response.json.return_value = self.mock_response_dict
        self.rtm.session = MagicMock()
        self.rtm.session.get.return_value = self.mock_response
        #mock socket functions:
        self.rtm.ws = MagicMock()
        self.rtm.ws.connect.return_value = None

    def test_connect_expecting_true(self):
        self.rtm.ws.recv.return_value = json.dumps({'type': 'hello'})
        self.rtm.connect()
        self.rtm.ws.connect.assert_called_with((self.mock_response_dict['url']))
        self.assertEqual(self.rtm.connect(), True)

    def test_connect_expecting_false(self):
        sys.stdin = open('test_input.txt', 'r')
        self.rtm.ws.recv.return_value = json.dumps({
            'type': 'error',
            'error':{'msg': 'Some error'}
        })
        self.assertEqual(self.rtm.connect(), False)
        
        self.original_mock_response = self.mock_response
        self.original_mock_response_dict = self.mock_response_dict
        self.original_mock_response.json.return_value = self.mock_response.json.return_value
        self.rtm.original_session = self.rtm.session
        self.rtm.original_session.get.return_value = self.rtm.session.get.return_value
        self.mock_response = MagicMock()
        self.mock_response_dict = {'ok': False, 'error': 'Some error'}
        self.mock_response.json.return_value = self.mock_response_dict
        self.rtm.session = MagicMock()
        self.rtm.session.get.return_value = self.mock_response
        self.assertEqual(self.rtm.connect(), False)
        self.mock_response = self.original_mock_response
        self.mock_response_dict = self.original_mock_response_dict
        self.mock_response.json.return_value = self.original_mock_response.json.return_value
        self.rtm.session = self.rtm.original_session
        self.rtm.session.get.return_value = self.rtm.original_session.get.return_value

    def test_send_msg(self):
        self.test_channel = 'my_channel'
        self.test_msg = 'hey'
        self.rtm.msg(self.test_msg, channel=self.test_channel)
        self.rtm.ws.send.assert_called_with(json.dumps({
            'id': 1,
            'type': 'message',
            'channel': self.test_channel,
            'text': self.test_msg
        }))



if __name__=='__main__':
	unittest.main()

