# -*- coding: UTF-8 -*-
from socket import *
import random
import json
import os
import time
import hashlib


class CommunicationData:
    type = ''   # W,R,A(audit), H(对比hash）
    content = ''


fw = open(os.getcwd()+"/logGenerationData.txt", "a")


def check5():
    # 未分片的
    f1 = open(os.getcwd() + "/../examData/logUpChainRate4(NoShard).txt", encoding="utf-8")
    line1 = f1.readline()  # 跳过第一行的start
    line1 = f1.readline()
    t11 = float(line1.split("=")[-1])
    line1 = f1.readline()

    # 分了三个片的
    f2 = open(os.getcwd() + "/../examData/logUpChainRate4(Shard).txt", encoding="utf-8")
    line2 = f2.readline()  # 跳过第一行的start
    line2 = f2.readline()
    t21 = float(line2.split("=")[-1])
    line2 = f2.readline()

    while line1:
        t12 = float(line1.split("=")[-1])
        line1 = f1.readline()

    while line2:
        t22 = float(line2.split("=")[-1])
        line2 = f2.readline()

    time1 = t12 - t11
    time2 = t22 - t21
    print("time1=" + str(time1) + " time2:" + str(time2))

if __name__ == '__main__':
    # 1. 读取IP+servers文件, 得到所有shards
    path = os.getcwd() + "/../mapTable"
    mapFile = open(path, encoding="utf-8")
    mapTable = mapFile.readline()
    shards = json.loads(mapTable)[-1]['shards']

    # 2. 读取日志文件，模拟产生日志的过程
    f = open("/home/hduser/LogShard/Hadoop.log", encoding = "utf-8")
    line = f.readline()
    i = 0
    print("start logSystem...time="+str(time.time()))  # 单位时间是秒
    shard0Num=0
    while line and i<1000:
        # 这一行用于统计日志产生速率
        # if i % 50 == 0:
        #     fw.write("logSystem,i="+str(i)+", time="+str(time.time())+"\n")
        # 3. 从nodePool里随机选取一个进行连接
        # 修改成直接从目标分片里选取一个吧
        hashLog = hashlib.sha256(line.encode('utf-8')).hexdigest()
        targetShardId = int(hashLog[-2:], 16) % len(shards)  # 用日志hash的最后两位转换为10进制进行求余选择分片
        if targetShardId != 0:
            # 只发送分片0 的数据
            line = f.readline()
            i += 1
            continue
        shard0Num += 1
        shard = shards[targetShardId]
        # shard = random.choice(shards)
        nodes = shard['servers']
        node = random.choice(nodes)

        try:
            # 3.1 创建套接字
            tcp_socket = socket(AF_INET, SOCK_STREAM)
            print("start to connect:"+ node['ip'] + " "+ node['port'])
            tcp_socket.connect((node['ip'], int(node['port'])))   # 连接服务器，建立连接,参数是元组形式
            # tcp_socket.connect(("192.168.8.5", int(node['port'])))  # 连接服务器，建立连接,参数是元组形式

            # 3.2 发送数据
            conmmunicationData = CommunicationData()
            conmmunicationData.type = 'W'
            conmmunicationData.content = line
            send_data = json.dumps(conmmunicationData.__dict__)
            tcp_socket.send(send_data.encode("gbk")) # 加上.decode("gbk")可以解决乱码

            # 注意这个1024byte，大小根据需求自己设置
            # from_server_msg = tcp_socket.recv(1024) # 从服务器接收数据
            # print(from_server_msg.decode("gbk"))
        except Exception as e:
            print(e)
            pass
        finally:
            # tcp_socket.send("exit".encode("gbk"))
            # 关闭连接
            tcp_socket.close()
            line = f.readline()
            i += 1
    print("shard0num is:"+str(shard0Num))
    check5()

