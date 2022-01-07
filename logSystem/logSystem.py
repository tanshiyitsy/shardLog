from socket import *
import random
import json
import os

class CommunicationData:
    type = ''   # W,R,A(audit), H(对比hash）
    content = ''


if __name__ == '__main__':
    # 1. 读取IP+servers文件, 得到所有shards
    path = os.getcwd() + "\\..\\mapTable"
    mapFile = open(path, encoding="utf-8")
    mapTable = mapFile.readline()
    shards = json.loads(mapTable)[-1]['shards']

    # 2. 读取日志文件，模拟产生日志的过程
    f = open("D:\Hadoop.log", encoding = "utf-8")
    line = f.readline()
    i = 0
    while line and i<4:
        i += 1
        # print("tantan ", line)                # 后面跟 ',' 将忽略换行符
        # 3. 从nodePool里随机选取一个进行连接
        shard = random.choice(shards)
        node = random.choice(shard)

        # 3.1 创建套接字
        tcp_socket = socket(AF_INET, SOCK_STREAM)
        print("start to connect:"+ node['ip'] + " "+ node['port'])
        tcp_socket.connect((node['ip'], int(node['port'])))   # 连接服务器，建立连接,参数是元组形式

        # 3.2 发送数据
        conmmunicationData = CommunicationData()
        conmmunicationData.type = 'W'
        conmmunicationData.content = line
        send_data = json.dumps(conmmunicationData.__dict__)
        tcp_socket.send(send_data.encode("gbk")) # 加上.decode("gbk")可以解决乱码

        # 注意这个1024byte，大小根据需求自己设置
        # from_server_msg = tcp_socket.recv(1024) # 从服务器接收数据
        # print(from_server_msg.decode("gbk"))

        # tcp_socket.send("exit".encode("gbk"))
        # 关闭连接
        tcp_socket.close()
        print("close the connection")
