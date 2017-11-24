# -*- coding: UTF-8 -*-
import socket, os, struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 12306))
filepath = input('Please Enter chars:\r\n')
if os.path.isfile(filepath):
	fileinfo_size = struct.calcsize('128sl')  # 定义打包规则
	# 定义文件头信息，包含文件名和文件大小
	fhead = struct.pack('128sl', os.path.basename(filepath).encode(), os.stat(filepath).st_size)
	s.send(fhead)
	print('client filepath: ', filepath)
	# with open(filepath,'rb') as fo: 这样发送文件有问题，发送完成后还会发一些东西过去
	fo = open(filepath, 'rb')
	while True:
		filedata = fo.read(1024)
		if not filedata:
			break
		s.send(filedata)
	fo.close()
	print('send over...')
		# s.close()