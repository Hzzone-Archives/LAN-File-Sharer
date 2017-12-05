import socket
import threading
import config
import os
import logging
import struct
import json
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S')
'''
服务器端
发送文件和目录信息的函数, 首先判断是否是目录, 如果是则发送文件, 否则发送目录下的信息, json字符串
'''
class Server_transfer(threading.Thread):
	def __init__(self, connection, content):
		threading.Thread.__init__(self)
		self.connection = connection
		if content.decode() == "*":
			self.content = "*"
		else:
			data = json.loads(content.decode())
			self.content = os.path.join(config.shared_folder, os.path.sep.join(data))

	def run(self):
		'''
		传输文件
		'''
		if os.path.isfile(self.content):
			# fileinfo_size = struct.calcsize('128sl')  # 定义打包规则
			# 定义文件头信息，包含文件名和文件大小
			fhead = struct.pack('128sl', os.path.basename(self.content).encode(), os.stat(self.content).st_size)
			self.connection.send(fhead)
			# with open(filepath,'rb') as fo: 这样发送文件有问题，发送完成后还会发一些东西过去
			try:
				fo = open(self.content, 'rb')
			except FileNotFoundError as e:
				raise "File not found"
			while True:
				filedata = fo.read(1024)
				if not filedata:
					break
				self.connection.send(filedata)
			fo.close()
			logging.debug("server has sent %s to %s" % (self.content, self.connection.getpeername()))
		# 传输目录信息 or 初始化时传输共享文件的目录
		## 目前以这样的方式传输, folde/file, 为了安全不包含全部路径
		elif os.path.isdir(self.content) or self.content == "*":
			# path = os.path.join(config.shared_folder, self.content.decode())
			shared_files = {}
			if self.content == "*":
				# shared_folder = [os.path.join(config.shared_folder, shared_file) for shared_file in os.listdir(config.shared_folder)]
				# for root, dirs, files in os.walk(config.shared_folder):
				# 	for each_file in files:
				# 		path = os.path.join(root, each_file)
				# 		# print(path.strip(config.shared_folder+os.path.sep))
				# 		shared_files.append(path.replace(config.shared_folder+os.path.sep, "").split(os.path.sep))
				for p in os.listdir(config.shared_folder):
					path = os.path.join(config.shared_folder, p)
					if os.path.isfile(path):
						shared_files[p] = os.path.isdir(path)
					elif os.listdir(path):
						shared_files[p] = os.path.isdir(path)
			else:
				# path = os.path.join(config.shared_folder, os.path.sep.join(json.loads(self.content.decode())))
				for p in os.listdir(self.content):
					path = os.path.join(self.content, p)
					if os.path.isfile(path):
						shared_files[p] = os.path.isdir(path)
					elif os.listdir(path):
						shared_files[p] = os.path.isdir(path)
			send_content = json.dumps(shared_files).encode()
			fhead = struct.pack('128sl', self.content.encode(), len(send_content))
			self.connection.send(fhead)
			for x in range(0, len(send_content), 1024):
				if len(send_content)-x < 1024:
					self.connection.send(send_content[x:len(send_content)])
				else:
					self.connection.send(send_content[x:x+1024])
			logging.debug("server has sent %s to %s" % (self.content, self.connection.getpeername()))
		else:
			raise "send data is not a dir or file"
	
	
'''
将要发送的服务器的地址, 和内容(文件或目录)
服务器返回文件结构或文件内容
'''
class Client_transfer(threading.Thread):
	def __init__(self, address, content, save_path=None):
		threading.Thread.__init__(self)
		self.address = address
		self.content = content
		self.save_path = save_path
		self.postgress = 0
		self.recvd_content = ""
	
	def run(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(self.address)
		s.send(self.content.encode())
		logging.debug("client send to %s content: %s" % (self.address, self.content))
		s.settimeout(600)
		fileinfo_size = struct.calcsize('128sl')
		buf = s.recv(fileinfo_size)
		if buf:  # 如果不加这个if，第一个文件传输完成后会自动走到下一句
			filename, filesize = struct.unpack('128sl', buf)
			# print(data.decode())
			filename_str = filename.decode("utf-8").strip('\x00')
			logging.debug("received from %s: %s and size: %s" % (self.address, filename_str, filesize))
			recvd_size = 0  # 定义接收了的文件大小
			'''
			接受文件并保存
			'''
			if self.save_path:
				file = open(self.save_path, 'wb')
				while not recvd_size == filesize:
					if filesize - recvd_size > 1024:
						rdata = s.recv(1024)
						recvd_size += len(rdata)
					else:
						rdata = s.recv(filesize - recvd_size)
						recvd_size = filesize
					self.postgress = recvd_size/filesize
					file.write(rdata)
				file.close()
				logging.debug("save received file to %s" % self.save_path)
			### 接受目录信息
			else:
				while not recvd_size == filesize:
					if filesize - recvd_size > 1024:
						rdata = s.recv(1024)
						recvd_size += len(rdata)
					else:
						rdata = s.recv(filesize - recvd_size)
						recvd_size = filesize
					self.recvd_content += rdata.decode()
				logging.debug("received folder info: %s" % self.recvd_content)
			
			s.close()
	
	def getPostgres(self):
		if not self.save_path:
			raise "before getting postgress, save path shouldn't be None"
		return self.postgress

if __name__ == "__main__":
	pass
