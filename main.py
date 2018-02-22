#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Name: Cody Ngrok Client Service
# Author: Icy(enderman1024@foxmail.com)
# OS: Linux

import time, socket, threading, os, sys, json




def init(): # initializer
	global LOGGER, KEY, STOP, NGROK_SERVICE
	paths = ("./bin/","./cache/","./configs/","./logs/")
	for i in paths:
		path_fixer(i)
	try:
		configs = read_config("./configs/codyclient.json")
	except Exception as err:
		print("INITIALIZE FAILED: " + str(err))
		sys.exit(1)
	log_level = "INFO"
	if "log_level" in configs:
		log_level = configs["log_level"]
	LOGGER = logger("./logs/codyclient.log","crlf","%Y-%m-%d %H:%M:%S",log_level)
	LOGGER.INFO("[Main] Initilizing...")
	os.chdir(sys.path[0])
	LOGGER.DEBUG("[Main] Path check: OK")
	os.system("rm cache/*")
	LOGGER.DEBUG("[Main] Cache clear: OK")
	KEY = b"CODYCLOUDORIGINALBASEKEY"
	if "base_key" in configs:
		KEY = configs["base_key"].encode("utf-8")
	LOGGER.DEBUG("[Main] Loaded base_key is " + KEY.decode())
	LOGGER.DEBUG("[Main] Configs load: OK")
	# global tags
	STOP = False
	NGROK_SERVICE = False
	LOGGER.DEBUG("[Main] Global tags define: OK")
	LOGGER.INFO("[Main] Initialized")




def path_fixer(path): # path checker
	chk = ""
	for i in path:
		chk += i
		if os.sep == i:
			if not os.path.exists(chk):
				os.mkdir(chk)




class iccode: # Simple Data encoder/decoder
	def __init__(self,key):
		if len(key) < 1:
			assert 0,"Key's length must be greater than 0"
		key = str(key)
		self.origin_key = key
		self.key = []
		keys = ""
		for i in key:
			keys = keys + str(ord(i))
		temp = ""
		for i in keys:
			temp = temp + i
			if int(temp[0]) < 5:
				if len(temp) == 3:
					self.key.append(int(temp))
					temp = ""
				else:
					pass
			else:
				if len(temp) == 2:
					self.key.append(int(temp))
					temp = ""
				else:
					pass
		if temp != "":
			self.key.append(int(temp))
		self.walk = 0
		self.origin_ickey = self.key
	def encode(self,data):
		res = b""
		for i in data:
			if self.walk >= len(self.key):
				self.walk = 0
				self.flush()
			code = i - self.key[self.walk]
			while code < 0:
				code = 256 + code
			res = res + bytes((code,))
			self.walk += 1
		return res
	def decode(self,data):
		res = b""
		for i in data:
			if self.walk >= len(self.key):
				self.walk = 0
				self.flush()
			code = i + self.key[self.walk]
			while code > 255:
				code = code - 256
			res = res + bytes((code,))
			self.walk += 1
		return res
	def flush(self):
		key = []
		for i in self.key:
			key.append(str(i))
		for i in "".join(key):
			key.append(str(i))
		self.key = []
		for i in range(len(key)):
			cursor = i + int(key[i])
			while cursor > (len(key)-1):
				cursor = cursor - len(key)
			key[i] = (str(int(key[i])+int(key[cursor])+len(key)))[-1:]
		temp = ""
		key = "".join(key)
		for i in key:
			temp = temp + i
			if len(self.key) >= len(self.origin_key):
				break
			if int(temp[0]) < 5:
				if len(temp) == 3:
					self.key.append(int(temp))
					temp = ""
				else:
					pass
			else:
				if len(temp) == 2:
					self.key.append(int(temp))
					temp = ""
				else:
					pass
		if len(temp) > 0 and len(self.key) < len(self.origin_key):
			self.key.append(int(temp))
	def reset(self):
		self.key = self.origin_ickey
		self.walk = 0
	def debug(self):
		print("Original   key: " + str(self.origin_key))
		print("Original ickey: " + str(self.origin_ickey))
		print("Step     ickey: " + str(self.key))
		print("Walk    cursor: " + str(self.walk))
		return (self.origin_key,self.origin_ickey,self.key,self.walk)




class logger: # Logger
	def __init__(self,filename,line_end,date_format,level):
		self.level = 1
		if level == "DEBUG":
			self.level = 0
		elif level == "INFO":
			self.level = 1
		elif level == "WARNING":
			self.level = 2
		elif level == "ERROR":
			self.level = 3
		elif level == "CRITICAL":
			self.level = 4
		else:
			assert 0,"logger level: DEBUG, INFO, WARNING, ERROR, CRITICAL"
		try:
			log_file = open(filename,"w")
			log_file.close()
		except Exception as err:
			assert 0,"Can't open file: \"" + filename + "\", result: " + str(err)
		self.filename = filename
		try:
			temp = time.strftime(date_format)
			del temp
		except Exception as err:
			assert 0,"Failed to set date formant, result: " + str(err)
		self.date_format = date_format
		if line_end == "lf":
			self.line_end = "\n"
		elif line_end == "crlf":
			self.line_end = "\r\n"
		else:
			assert 0,"Unknow line end character(s): \"" + line_end + "\""
	def DEBUG(self,msg):
		if self.level > 0:
			return
		infos = "["+ time.strftime(self.date_format) +"] [DBUG] " + msg + self.line_end
		sys.stdout.write(infos)
		sys.stdout.flush()
		log_file = open(self.filename,"a")
		log_file.write(infos)
		log_file.close()
	def INFO(self,msg):
		if self.level > 1:
			return
		infos = "["+ time.strftime(self.date_format) +"] [INFO] " + msg + self.line_end
		sys.stdout.write(infos)
		sys.stdout.flush()
		log_file = open(self.filename,"a")
		log_file.write(infos)
		log_file.close()
	def WARNING(self,msg):
		if self.level > 2:
			return
		infos = "["+ time.strftime(self.date_format) +"] [WARN] " + msg + self.line_end
		sys.stdout.write(infos)
		sys.stdout.flush()
		log_file = open(self.filename,"a")
		log_file.write(infos)
		log_file.close()
	def ERROR(self,msg):
		if self.level > 3:
			return
		infos = "["+ time.strftime(self.date_format) +"] [EROR] " + msg + self.line_end
		sys.stdout.write(infos)
		sys.stdout.flush()
		log_file = open(self.filename,"a")
		log_file.write(infos)
		log_file.close()
	def CRITICAL(self,msg):
		infos = "["+ time.strftime(self.date_format) +"] [CRIT] " + msg + self.line_end
		sys.stdout.write(infos)
		sys.stdout.flush()
		log_file = open(self.filename,"a")
		log_file.write(infos)
		log_file.close()




class isock: #tcp socket server
	def __init__(self):
		self.isock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = False
	def build_server(self,addr,maxcon):
		if self.server == False:
			try:
				self.isock.bind(addr)
				self.isock.listen(maxcon)
			except Exception as err:
				return (False,str(err))
			self.server = True
			return (True,"")
		else:
			return (False,"socket server has already been built")
	def connect(self,addr):
		if self.server:
			return (False,"Already became a server")
		else:
			try:
				self.isock.connect(addr)
			except Exception as err:
				return (False,str(err))
			return (True,"")
	def settimeout(self,to):
		self.isock.settimeout(to)
	def accept(self):
		if self.server:
			try:
				clt,con = self.isock.accept()
			except Exception as err:
				return (False,str(err))
			return (True,(clt,con))
		else:
			return (False,"server has not been built yet")
	def send(self,data):
		try:
			self.isock.send(data)
		except Exception as err:
			return (False,str(err))
		return (True,len(data))
	def recv(self,length):
		try:
			data = self.isock.recv(length)
		except Exception as err:
			return (False,str(err))
		return(True,data)
	def close(self):
		try:
			self.isock.close()
		except Exception as err:
			return(False,str(err))
		return(True,'')




def keygen(code,mt): # Live key generator
	code = code.decode()
	dt = int((time.time()+(300*mt))/300)
	key = ""
	timekey = str(dt*int(dt/3600)+dt*len(code))+str(dt*dt+dt**len(code))
	while len(timekey) < len(code):
		timekey += timekey
	for i in range(0,len(code)):
		a = ord(code[i]) + int(timekey[i])
		key = key + chr(a)
	key = key.encode()
	return key




def bin2str(data): # transform bin data to string
	try:
		res = data.decode()
	except:
		res = str(data)
	return res




def read_config(file): # Json Config Reader
	config_file = open(file,"r")
	data = json.load(config_file)
	return data




def codycloud_cloudcheck(host,check_port): # cody cloud status check service (sub thread)
	LOGGER.DEBUG("[CloudCheck] Running cloud check program")
	coder = iccode(KEY)
	clt = isock()
	clt.settimeout(15)
	LOGGER.DEBUG("[CloudCheck] TCP Socket initialized, connecting to " + host[0] + ":" + str(host[1]))
	status = clt.connect(host)
	if not status[0]:
		LOGGER.WARNING("[CloudCheck] Failed to connecting to server, result:" + str(status[1]))
		clt.close()
		return 2
	else:
		LOGGER.DEBUG("[CloudCheck] Server connected, sending live key")
	status = clt.send(coder.encode(keygen(KEY,0)))
	coder.reset()
	if not status[0]:
		LOGGER.WARNING("[CloudCheck] Failed to send live key, result:" + status[1])
		clt.close()
		return 2
	else:
		pass
	status = clt.recv(16)
	if not status[0]:
		LOGGER.WARNING("[CloudCheck] Failed to receive data, result:" + status[1])
		clt.close()
		return 2
	else:
		data = coder.decode(status[1])
		coder.reset()
	if data == b"OK":
		LOGGER.DEBUG("[CloudCheck] Live key matched")
	else:
		LOGGER.WARNING("[Cloudcheck] Live key match failed, data received:" + bin2str(status[1]))
		clt.close()
		return 3
	status = clt.send(coder.encode(check_port.encode()))
	coder.reset()
	if not status[0]:
		LOGGER.WARNING("[CloudCheck] Failed to send check request, result:" + status[1])
		clt.close()
		return 2
	else:
		pass
	status = clt.recv(16)
	if not status[0]:
		LOGGER.WARNING("[CloudCheck] Failed to receive status feedback, result:" + status[1])
	else:
		data = coder.decode(status[1])
	if data == b"OP":
		LOGGER.DEBUG("[CloudCheck] Port " + check_port + " is OPEN")
		clt.close()
		return 0
	elif data == b"CL":
		LOGGER.WARNING("[CloudCheck] Port " + check_port + " is CLOSE")
		clt.close()
		return 1
	else:
		LOGGER.WARNING("[CloudCheck] Unexpected data: " + bin2str(status[1]))
		clt.close()
		return 3




def ngrok_client(name,configs): # ngrok client thread (sub thread)
	os.system("killall " + name)
	try:
		log_path = False
		log_level = "INFO"
		cmd = "./bin/" + name + " -config "
		if "log_path" in configs:
			log_path = configs["log_path"]
		if "log_level" in configs:
			log_level = configs["log_level"]
		tunnels = configs["tunnels"]
		config_path = configs["config_path"]
		cmd = cmd + config_path + " "
		if log_path:
			cmd = cmd + "-log " + log_path + " -log-level " + log_level + " "
		cmd = cmd + "start"
		for i in tunnels:
			cmd = cmd + " " + i
		LOGGER.DEBUG("[NgrokClient] Command generated: " + cmd)
		os.system(cmd)
	except Exception:
		LOGGER.WARNING("[NgrokClient] Failed to start ngrok client(" + name + "), result:" + str(err))
		sys.exit(1)



def ngrok_client_service(): # ngrok client controller (thread)
	global STOP, NGROK_SERVICE
	NGROK_SERVICE = True
	LOGGER.DEBUG("[NgrokService] Loading configs")
	try:
		configs = read_config("./configs/codyclient.json")
	except Exception as err:
		LOGGER.CRITICAL("[NgrokService] Can't open(or missing) \"codyclient.json\" config file")
		STOP = True
		sys.exit(1)
	try:
		server_addr = configs["server_addr"]
		server_port = configs["server_port"]
		ngrok_clients = configs["ngrok_clients"]
		ngrok_log_paths = []
		for i in ngrok_clients:
			ngrok_log_paths.append((ngrok_clients[i])["log_path"])
		for i in ngrok_log_paths:
			path_fixer(i)
	except Exception as err:
		LOGGER.ERROR("[NgrokService] Failed while reading config file, result:" + str(err))
		STOP = True
		sys.exit(1)
	LOGGER.INFO("[NgrokService] Starting ngrok clients")
	ngrok_error = {}
	for i in ngrok_clients:
		ngrok_error.update({i:0})
		try:
			ngrok_thread = threading.Thread(target=ngrok_client, args=(i,ngrok_clients[i]))
			ngrok_thread.start()
		except Exception as err:
			LOGGER.ERROR("[NgrokService] Can't start ngrok_client(" + i + ") thread, result: " + str(err))
	LOGGER.INFO("[NgrokService] Starting ngrok client cloud check service")
	tick = 50
	while True:
		time.sleep(1)
		tick += 1
		if STOP:
			LOGGER.INFO("[NgrokService] Stopping ngrok clients")
			for i in ngrok_clients:
				LOGGER.DEBUG("[NgrokService] Sending kill signal to \"" + i + "\"")
				status = os.system("killall " + i)
				if status != 0:
					LOGGER.WARNING("[NgrokService] Failed to kill \"" + i + "\", system feedback code: " + str(status))
				else:
					pass
			LOGGER.INFO("[NgrokService] NgrokService stopped")
			NGROK_SERVICE = False
			sys.exit(0)
		if tick >= 60:
			tick = 0
			for i in ngrok_clients:
				if ngrok_error[i] == 5:
					LOGGER.WARNING("[NgrokService] Ngrok client \"" + i + "\" has too many error, tagging into skip list")
					ngrok_error.update({i:6})
					continue
				elif ngrok_error[i] >= 6:
					LOGGER.DEBUG("[NgrokService] Skipping ngrok client \"" + i + "\"")
					continue
				LOGGER.DEBUG("[NgrokService] Checking ngrok client \"" + i + "\"")
				error_port = 0
				net_error = 0
				for i2 in (ngrok_clients[i])["tunnels"]:
					status = codycloud_cloudcheck((server_addr,server_port),str(((ngrok_clients[i])["tunnels"])[i2]))
					if status == 0:
						LOGGER.DEBUG("[NgrokService] Cloud check port(" + i + "): " + str(((ngrok_clients[i])["tunnels"])[i2]) + "(" + i2 + ") status: OK")
						ngrok_error.update({i:0})
						net_error = 0
					elif status == 1:
						LOGGER.WARNING("[NgrokService] Cloud check port(" + i + "): " + str(((ngrok_clients[i])["tunnels"])[i2]) + "(" + i2 + ") status: CLOSED")
						error_port += 1
					elif status == 2:
						LOGGER.ERROR("[NgrokService] Cloud check server error, unexpected server or network error")
					else:
						LOGGER.ERROR("[NgrokService] Cloud check failed, server_addr, server_port or base_key maybe incorrect")
						net_error += 1
						time.sleep(net_error*5)
					if error_port > 0:
						LOGGER.INFO("[NgrokService] Restarting ngrok client \"" + i + "\"")
						ngrok_error.update({i:ngrok_error[i]+1})
						try:
							ngrok_thread = threading.Thread(target=ngrok_client, args=(i,ngrok_clients[i]))
							ngrok_thread.start()
						except Exception as err:
							LOGGER.ERROR("[NgrokService] Can't start ngrok_client(" + i + ") thread, result: " + str(err))




def stop_service(): # stopping service (main)
	global STOP
	LOGGER.INFO("[StopService] Stopping Service is now listening for stopping signal")
	temp = 0
	try:
		while True:
			time.sleep(2)
			signal = os.path.exists("cache/CMD_STOP")
			if signal or STOP:
				STOP = True
				LOGGER.INFO("[StopService] Stopping signal detected, stopping CodyClient")
				while True:
					time.sleep(1)
					temp += 1
					if temp >= 10:
						if NGROK_SERVICE:
							LOGGER.WARNING("[StopService] Ngrok Service thread has no response, stopping failed")
							break
					else:
						if NGROK_SERVICE == False:
							time.sleep(5)
							LOGGER.INFO("[StopService] All main threads stopped")
							break
				LOGGER.DEBUG("[StopService] Releasing Stopped signal file")
				file = open("cache/FB_STOPPED","w")
				file.write("stopped")
				file.close()
				LOGGER.INFO("[StopService] CodyClient stopped")
				return
	except KeyboardInterrupt:
		STOP = True
		LOGGER.INFO("[StopService] Stopping signal detected, stopping CodyClient")
		while True:
			time.sleep(1)
			temp += 1
			if temp >= 10:
				if NGROK_SERVICE:
					LOGGER.WARNING("[StopService] Ngrok Service thread has no response, stopping failed")
					break
			else:
				if NGROK_SERVICE == False:
					time.sleep(1)
					LOGGER.INFO("[StopService] All main threads stopped")
					break
		LOGGER.DEBUG("[StopService] Releasing Stopped signal file")
		file = open("cache/FB_STOPPED","w")
		file.write("stopped")
		file.close()
		LOGGER.INFO("[StopService] CodyClient stopped")
		return



def main(): # main thread tree (main)
	init()
	LOGGER.DEBUG("[Main] Starting Ngrok Service")
	ngrok_service_thread = threading.Thread(target=ngrok_client_service,args=())
	ngrok_service_thread.start()
	LOGGER.DEBUG("[Main] Starting main thread control service")
	stop_service()
	sys.exit(0)




if __name__ == '__main__':
	main()
