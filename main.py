#!/usr/bin/env python3

import server.server as server
from core.files import Files


if __name__ == "__main__":
	port = 8000
	files = Files()
	server.start_server(files ,port)
