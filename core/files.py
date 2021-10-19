import json
from utils.request import make_web_request
import tornado
from tornado import ioloop

FILES_URL = "http://interview-api.snackable.ai/api/file/all?offset={offset}"

class Files():
	def __init__(self):
		self.ioloop = ioloop.IOLoop.current()
		self.ioloop.run_sync(self.get_from_url_files)
		
	async def get_from_url_files(self):
		files = []
		offset = 0
		while(True):
			url_with_offset = FILES_URL.format(offset = offset)
			r = await make_web_request(url_with_offset, {}, {})
			files_from_request = json.loads(r.body.decode('utf-8'))
			if len(files_from_request) == 0:
				break
			else:
				files += files_from_request
				offset += 5

		self.files = list(filter(lambda x: (x["processingStatus"] == "FINISHED"), files))## filter out finished files
		print(f"filtered files: {self.files}")


