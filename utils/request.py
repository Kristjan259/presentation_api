import tornado.httpclient

async def make_web_request(url, headers, params, method="GET"):
	http_client = tornado.httpclient.AsyncHTTPClient()
	request = tornado.httpclient.HTTPRequest(
		url,
		method=method,
		headers=headers,
		connect_timeout=30.0,
		request_timeout=60.0,
		allow_nonstandard_methods=True
	)
	try:
		response = await http_client.fetch(request)
	except ConnectionRefusedError as e:
		raise
	except Exception as e:
		print(e)
		return e
	return response