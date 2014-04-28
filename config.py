import json
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import logging
from uuid import uuid4
class IndexHandler (tornado.web.RequestHandler):
	def get(self):
		self.render("index.html")

class RenderSearchSuggest(tornado.web.RequestHandler):
	def get(self):
		self.render('search_suggest.js')
class RenderJquery(tornado.web.RequestHandler):
	def get(self):
		self.render('jquery.js')