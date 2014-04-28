import json
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import torndb
import time
import redis
from tornado.options import define,options
import logging
from uuid import uuid4
from sets import Set
import config
import database

define("port",default=8002,help="tornado will run on the given port",type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers=[(r"/",config.IndexHandler),(r"/insert",database.DbInsert),
		(r"/search",database.DbSearch),
		(r"/search_suggest.js",config.RenderSearchSuggest),(r"/jquery.js",config.RenderJquery)] 

		settings =  {
		'template_path':'templates',
		'static_path':'static',
		'debug':True
		}

		tornado.web.Application.__init__(self,handlers,**settings)

if __name__=='__main__':
	tornado.options.parse_command_line	()
	db = torndb.Connection("localhost", "tordata",user="root",password="ksh")
	app=Application()
	server=tornado.httpserver.HTTPServer(app)
	server.listen(8002)
	tornado.ioloop.IOLoop.instance().start()