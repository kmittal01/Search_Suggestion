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
import config
from uuid import uuid4
from sets import Set
db = torndb.Connection("localhost", "tordata",user="root",password="ksh")
class DbInsert(tornado.web.RequestHandler):
	
	def prefix_array(self,json_string):
		begin_pos=json_string.find(':')+2
		end_pos=json_string.find('"',begin_pos)
		text_str=json_string[begin_pos:end_pos]
		word_list=text_str.split()
		arr=[]
		for j in range (len(word_list)):
			prefix_str=str('')
			for i in range (len(word_list[j])):
				if i == len(word_list[j])-1:
					prefix_str=str(prefix_str+word_list[j][i])
					indices = [i for i, x in enumerate(word_list) if x == prefix_str]
					# logging.info(indices)
					# logging.info(prefix_str)
					# logging.info("indices length:" + str(len(indices)))
					prefix_arr=[prefix_str,str(len(indices))]
					arr.append(prefix_arr)
				else:
					prefix_str=str(prefix_str+word_list[j][i])
					prefix_arr=[prefix_str,'0']
					arr.append(prefix_arr)
		logging.info(arr)
		return arr

	def insert_in_hsets(self,json_string):
		r=redis.StrictRedis(host='localhost',port=6379,db=2)
		key=r.hlen("search_suggest:terms")+1
		r.hset("search_suggest:terms",str(key),json_string)
		ins_str=r.hget("search_suggest:terms",str(key))
		return str(key)

	def insert_in_zsets(self,arr,key):
		r=redis.StrictRedis(host='localhost',port=6379,db=2)
		# logging.info(arr)
		# logging.info(len(arr))
		for i in range (len(arr)):
			r.zadd("search_suggest:prefix:"+str(arr[i][0]),arr[i][1],key)
		# logging.info("logging in search_suggest:prefix:"+str(arr[i])+"done")	

	def post(self):
		json_string=self.get_argument('json_string')
		arr=self.prefix_array(json_string)
		# logging.info("checking array return")		
		# logging.info(arr)
		key=self.insert_in_hsets(json_string)
		self.insert_in_zsets(arr,key)

class DbSearch(tornado.web.RequestHandler):
	def post(self):
		r=redis.StrictRedis(host='localhost',port=6379,db=2)
		prefix=self.get_argument('prefix')
		prefix_array=prefix.split()
		prefix_array_length=len(prefix_array)
		logging.info(prefix_array_length)
		for i in range(prefix_array_length):
		 	r.zinterstore("dest",["search_suggest:prefix:"+str(prefix_array[0]),"search_suggest:prefix:"+str(prefix_array[i])],aggregate='sum')
		key_array=r.zrange("dest",0,-1)
		logging.info(key_array)
		json_return=r.hmget('search_suggest:terms',reversed(key_array))
		json_return_str=''.join(json_return)
		key_array_str=''.join(key_array)
		self.write(json_return_str)


