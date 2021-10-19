import tornado.httpserver
import tornado.ioloop
import tornado.web
from server.handlers.get_file import FilesHandler

def get_app(files):
	routes = [
		("/get_files/?", FilesHandler, {'files': files}),
	]
	app_settings = {}
	application = tornado.web.Application(routes, **app_settings)
	return application

def start_server(files, port=8000):
	print(f"Starting server on port {port}")
	application = get_app(files)
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(port)
	tornado.ioloop.IOLoop.instance().start()
