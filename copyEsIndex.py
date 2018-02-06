import requests as req
import re
from datetime import datetime
from elasticsearch import Elasticsearch
import time
import configparser
import codecs
import sys

try:
	#处理在windows下编辑ini文件带Bom的情况
	with open('config.ini',encoding='utf-8') as file:
		config_data=file.read()
		config_data=config_data.replace('\ufeff','')
		with open('config.ini','w',encoding='utf-8') as file:
			file.write(config_data)

	#读取配置信息
	cf=configparser.ConfigParser()
	cf.read('config.ini',encoding='utf-8')
	sourceES_host=cf.get('sourceES', 'host')
	sourceES_port=cf.get('sourceES', 'port')
	sourceES_isCopyIndex=cf.get('sourceES', 'isCopyIndex')
	sourceES_include=cf.get('sourceES', 'include').strip().replace('，',',').split(',')
	sourceES_exclude=cf.get('sourceES', 'exclude').strip().replace('，',',').split(',')


	targetES_host=cf.get('targetES', 'host')
	targetES_port=cf.get('targetES', 'port')
	targetES_isDeleteIndex=cf.get('targetES', 'isDeleteIndex')
	targetES_include=cf.get('targetES', 'include').strip().replace('，',',').split(',')
	targetES_exclude=cf.get('targetES', 'exclude').strip().replace('，',',').split(',')

	if sourceES_host=='' and targetES_host=='':
		print('请先到config.ini下配置相关参数...')
		print('程序将在10秒后退出...')

		time.sleep(10)
		sys.exit(1)

	pattern="open   (.*?) "
	_index={"settings":{"index":{"number_of_shards":"6","number_of_replicas":"1"}},"mappings":''}

	if int(targetES_isDeleteIndex):
		if targetES_host=='':
			print('请先到config.ini下配置目标ES的地址...')
			time.sleep(10)
			sys.exit(1)			
		if targetES_include[0]!='':
			targetES_data=targetES_include
		else:
			resp=req.get('http://'+targetES_host+':'+targetES_port+'/_cat/indices?v')
			targetES_data=re.findall(pattern, resp.text)

		for i in targetES_exclude:
			try:
				targetES_data.remove(i)
			except:
				pass

		for x in targetES_data:
			print(datetime.now(),'正在删除:',x)
			req.delete('http://'+targetES_host+':'+targetES_port+'/'+x)


	#结构来源es
	if int(sourceES_isCopyIndex):

		#需要添加数据或删除结构的es
		es=Elasticsearch([{'host':targetES_host,'port':targetES_port}])		
		if len(sourceES_include)>0:
			sourceES_data=sourceES_include
		else:	
			resp=req.get('http://'+sourceES_host+':'+sourceES_port+'/_cat/indices?v')
			sourceES_data=re.findall(pattern, resp.text)

		for i in sourceES_exclude:
			try:
				sourceES_data.remove(i)
			except:
				pass

		#复制index和mapping结构
		for x in sourceES_data:
			try:
				if x=='':
					continue
				print(datetime.now(),'正在创建:',x)
				resp=req.get('http://'+sourceES_host+':'+sourceES_port+'/'+x+'/'+x+'/_mapping')
				_index['mappings']=resp.json()[x]["mappings"]
				resp=req.get('http://'+sourceES_host+':'+sourceES_port+'/'+x+'/_settings')
				_index['settings']['index']['number_of_shards']=resp.json()[x]['settings']['index']['number_of_shards']
				_index['settings']['index']['number_of_replicas']=resp.json()[x]['settings']['index']['number_of_replicas']
				if es.indices.exists(index=x) is not True:
					es.indices.create(index=x, body=_index) 
			except Exception as e:
				print(e)
except Exception as e:
	print(e)
	time.sleep(60)