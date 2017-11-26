### File sharing based on python socket
局域网文件共享(pyqt, udp)
1. 获取内网ip, 扫描局域网开启文件共享的服务器
2. 作为服务器, 开启一个新线程循环接受和处理socket请求, 首先无论请求什么, 依次返回两条内容, 第一条是实际内容的大小, 第二条: 如果连接请求文件, 则返回文件字节流; 如果是文件夹, 则返回文件夹中的目录信息, 包括文件名, 是否是目录等.
3. 作为客户端, 开启新线程发送消息, 并循环接受服务器返回消息, 如果是文件, 则写入指定本地文件路径中, 并获取传输进度. 如果是目录, 则刷新ui.
4. UI部分, 基于PyQt.    
以上是基本思路.

translate qt .ui file to .py
```shell
python3 -m PyQt5.uic.pyuic $FileName$ -o $FileNameWithoutExtension$
```

How to use
```shell
$ python3 main.py -h
Usage: main.py [options]

Options:
  -h, --help            show this help message and exit
  -v SHAREFOLDER, --sharefolder=SHAREFOLDER
                        folder you tend to share, default current folder
  -p SERVER_PORT, --port=SERVER_PORT
                        server port you tend to open for socket, default 8888
  -s SAVEFOLDER, --savefolder=SAVEFOLDER
                        folder you tend to save the downloaded file, default
                        current folder/download
```