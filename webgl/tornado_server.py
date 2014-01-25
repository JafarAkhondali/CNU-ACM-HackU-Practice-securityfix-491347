import os.path
import re
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

class MainHandler(tornado.web.RequestHandler):
	def get(self,url):
		path = 'threejs.html' if self.request.uri == '/' else self.request.uri[1:]

		if(len(path.split('?')) > 1):
			path = path.split('?')[0]

		pathsplit = path.split('.')

		filetype = pathsplit[len(pathsplit)-1]

	 	type = {
			'css':'text/css',
			'dae':'model/vnd.collada+xml',
			'dds':'x-image/dds',
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

		try:
			self.set_status(200,'OK')
			self.set_header('Content-Type',(type[filetype] or type['text']))

			file = open(os.path.dirname(__file__)+path,'r')

			self.write(file.read())
		except:
			self.set_status(404,'Not Found')
			print '404 '+type[filetype]

def Main():
	tornado.options.parse_command_line()

	application = tornado.web.Application([
		(r'/(.*)',MainHandler),
	])

	server = tornado.httpserver.HTTPServer(application)
	server.listen(8000)

	tornado.ioloop.IOLoop.instance().start()

if(__name__ == '__main__'):
	Main()