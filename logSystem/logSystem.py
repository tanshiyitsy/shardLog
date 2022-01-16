from socket import *
import random
import json
import os
import time
import hashlib

class CommunicationData:
    type = ''   # W,R,A(audit), H(对比hash）
    content = ''

#
fw = open(os.getcwd()+"\\logGenerationData.txt", "a")


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
    print("start logSystem...time="+str(time.time()))  # 单位时间是秒
    while line and i<1001:
        if i % 10 == 0:
            fw.write("logSystem,i="+str(i)+", time="+str(time.time())+"\n")
        # print("tantan ", line)                # 后面跟 ',' 将忽略换行符
        # 3. 从nodePool里随机选取一个进行连接
        # 修改成直接从目标分片里选取一个吧
        # hashLog = hashlib.sha256(line.encode('utf-8')).hexdigest()
        # targetShardId = int(hashLog[-2:], 16) % len(shards)  # 用日志hash的最后两位转换为10进制进行求余选择分片
        # shard = shards[targetShardId]
        shard = random.choice(shards)
        node = random.choice(shard)
        # print("hashLog is:"+hashLog)
        # print("this targetId is:"+str(targetShardId))

        # 3.1 创建套接字
        tcp_socket = socket(AF_INET, SOCK_STREAM)
        print("start to connect:"+ node['ip'] + " "+ node['port'])
        tcp_socket.connect((node['ip'], int(node['port'])))   # 连接服务器，建立连接,参数是元组形式
        # tcp_socket.connect(("", int(node['port'])))

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
        # print("close the connection")
        line = f.readline()
        i += 1