from tornado import gen
import tornado.web
from utils.request import make_web_request

import json


additional_file_details_url = "http://interview-api.snackable.ai/api/file/details/{snackableFileId}"
file_segment_url = "http://interview-api.snackable.ai/api/file/segments/{snackableFileId}"
PREFIX = "Bearer "

class FilesHandler(tornado.web.RequestHandler):
	"""
		Listens to queries made to /get_files
	"""
	def initialize(self, files):
		self.files = files.files
		self.secret = "MYREALLYSECRETTOKEN"		

	async def get(self):
		file_id = self.get_argument("fileId", None, True)
		token = get_token(self.request.headers.get('Authorization'))
		result = {}
		
		if not (token == self.secret):
			self.set_status(403)## unauthorized
			self.finish()
			return

		print("Token is correct")
		if file_id:
			if self.if_exist_with_the_given_file_id(file_id):
				print("file with the given ID exists")
				file_details_url = additional_file_details_url.format(snackableFileId = file_id)
				file_segments_uri = file_segment_url.format(snackableFileId = file_id)
				file_details_data = await make_web_request(file_details_url, {}, {})
				result["file details"] = json.loads(file_details_data.body.decode('utf-8'))
				file_segment_data = await make_web_request(file_segments_uri, {}, {})
				result["file segments"] =  json.loads(file_segment_data.body.decode('utf-8'))
				self.write(json.dumps(result))
				self.set_status(200)
				self.finish()
				return

		self.set_status(400)## bad request
		self.finish()
		##return error

	def if_exist_with_the_given_file_id(self, file_id):
		for f in self.files:
			if f["fileId"] == file_id:
				return True
		return False

def get_token(header):
	if header == None or not header.startswith(PREFIX):
		return ""
	return header[len(PREFIX):]