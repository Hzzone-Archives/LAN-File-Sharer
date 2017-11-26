import transfer
import config
import utils
import os
import socket

def init():
	if os.path.exists(config.default_save_folder):
		raise "save folder not exists"

def main():
	init()
	# transfer.Client_transfer((utils.get_internal_ip(), config.server_port), "/Users/HZzone/Desktop/template_2.jpg", "/Users/HZzone/Desktop/new_template_2.jpg").start()
	transfer.Client_transfer((utils.get_internal_ip(), config.server_port), "*").start()
	
if __name__ == "__main__":
	main()
	# print(socket.gethostbyaddr("192.168.21.101"))
	# print(socket.getaddrinfo("192.168.21.101", config.server_port))
