import transfer
import config
import utils
import os
import ui
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from optparse import OptionParser
import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S')


def init():
	parse = OptionParser()
	parse.add_option('-v', '--sharefolder', dest='sharefolder', help='folder you tend to share, default current folder')
	parse.add_option('-p', '--port', dest='server_port', help='server port you tend to open for socket, default 8888')
	parse.add_option('-s', '--savefolder', dest='savefolder', help='folder you tend to save the downloaded file, default current folder/download')
	options = parse.parse_args()[0]#这里参数值对应的参数名存储在这个options字典里
	if options.savefolder:
		config.default_save_folder = options.savefolder
	if options.server_port:
		config.server_port = options.server_port
	if options.sharefolder:
		config.shared_folder = options.sharefolder
	if not os.path.exists(config.default_save_folder):
		raise "save folder not exists"
	if not os.path.exists(config.shared_folder):
		raise "shared folder not exists"
	logging.debug("shared_folder: %s, default_save_folder: %s" % (config.shared_folder, config.default_save_folder))

def main():
	init()
	# transfer.Client_transfer((utils.get_internal_ip(), config.server_port), "/Users/HZzone/Desktop/template_2.jpg", "/Users/HZzone/Desktop/new_template_2.jpg").start()
	# transfer.Client_transfer((utils.get_internal_ip(), config.server_port), ".git").start()
	# transfer.Client_transfer((utils.get_internal_ip(), config.server_port), "*").start()
	# transfer.Client_transfer((utils.get_internal_ip(), config.server_port), ".uit").start()
	app = QApplication(sys.argv)
	MainWindow = QMainWindow()
	window_ui = ui.Ui_MainWindow()
	window_ui.setupUi(MainWindow)
	MainWindow.show()
	app.exec_()
	app.exit()
	
if __name__ == "__main__":
	main()
	# print(socket.gethostbyaddr("192.168.21.101"))
	# print(socket.getaddrinfo("192.168.21.101", config.server_port))
