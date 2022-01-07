from socket import *
import random

# 1. 读取IP+servers文件, 得到可用的nodePool
nodePool = [{'ip':"127.0.0.1",'port':"8080"}]


# 3. 从nodePool里随机选取一个进行连接
node = random.choice(nodePool)
# 3.1 创建套接字
tcp_socket = socket(AF_INET, SOCK_STREAM)
tcp_socket.connect((node['ip'], node['port']))   # 连接服务器，建立连接,参数是元组形式
t1 = ""
t2 = ""
send_data = "R::"+t1+"-"+t2
tcp_socket.send(send_data.encode("gbk")) # 加上.decode("gbk")可以解决乱码
# 注意这个1024byte，大小根据需求自己设置
from_server_msg = tcp_socket.recv(1024) # 从服务器接收数据
print(from_server_msg.decode("gbk"))
# 关闭连接
tcp_socket.close()
