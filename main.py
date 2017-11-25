import transfer
import config
import utils

def main():
	transfer.Client_transfer((utils.get_internal_ip(), config.server_port), "/home/hzzone/install.sh", "/home/hzzone/new_install.sh").start()
	
if __name__ == "__main__":
	main()