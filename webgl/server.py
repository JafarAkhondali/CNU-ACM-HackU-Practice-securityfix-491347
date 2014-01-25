#Http server for serving files locally. Required for testing webgl resources offline. By Juan Vallejo
import os
from wsgiref.simple_server import make_server

def MainHandler(env,response):
	path = 'threejs.html' if env['PATH_INFO'] == '/' else env['PATH_INFO'][1:]
	filetype = path.split('.')
	filetype = filetype[len(filetype)-1]

	type = {
			'css':'text/css',
			'dae':'model/vnd.collada+xml',
			'html':'text/html',
			'jpg':'image/jpeg',
			'js':'application/javascript',
			'json':'application/json',
			'svg':'image/svg+xml',
			'png':'image/png',
			'text':'text/plain',
			'woff':'application/x-woff-font',
			'xml':'application/xml'
	}

	status = '200 OK'
	headers = [('Content-Type',(type[filetype] or type['text']))]

	response(status,headers)

	file = open(os.path.dirname(__file__)+path,'r')
	return file.read()

server = make_server('',8000,MainHandler)
server.serve_forever()
