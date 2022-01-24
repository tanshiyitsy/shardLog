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

# 读取IP + servers文件, 得到所有shards
mapPath = os.getcwd() + "/../mapTable"
mapFile = open(mapPath, encoding="utf-8")
mapTable = mapFile.readline()
shards = json.loads(mapTable)[-1]['shards']


def init():
    # 初始化日志生成文件
    fw = open(os.getcwd() + "/logGenerationData.txt", "w")
    fw.write("start...")
    fw.close()

    # 初始化日志上链文件
    if len(shards) == 1 :
        desPath = os.getcwd() + "/../Logger/logUpChainRateNoShard.txt"
    else:
        desPath = os.getcwd() + "/../Logger/logUpChainRateShard.txt"
    fw = open(desPath, "w")
    fw.write("start..." + "\n")
    fw.close()

def ts2Date(timestamp):
    strTime1 = time.localtime(timestamp) # 通过time.localtime将时间戳转换成时间组
    c = time.strftime("%Y-%m-%d %H:%M:%S", strTime1)  # 再将时间组转换成指定格式
    return c

def check5():
    # 检查分片和未分片的延时
    print("start check5.....")
    # 未分片的
    print("no shard")
    path1 = os.getcwd() + "/../Logger/logUpChainRateNoShard.txt"
    time1 = check5Core(path1)
    # 分片的
    print("sharded")
    path2 = os.getcwd() + "/../Logger/logUpChainRateShard.txt"
    time2 = check5Core(path2)

    print("time1=" + str(time1) + " time2:" + str(time2))

def check5Core(path):
    t11,t12 = 0,0
    f1 = open(path, encoding="utf-8")
    line1 = f1.readline()  # 跳过第一行的start
    line1 = f1.readline()
    if line1:
        t11 = float(line1.split("=")[-1])
        print("start time :"+ts2Date(t11))
        line1 = f1.readline()

    while line1:
        t12 = float(line1.split("=")[-1])
        line1 = f1.readline()

    print("end time :" + ts2Date(t12))
    time1 = t12 - t11
    return time1

def tail():
    # 收尾工作
    for port in range(5000,5400):
        path = os.getcwd() + "/../examData/blockFile" + str(port) + ".txt"
        if os.path.exists(path):
            os.remove(path)

    logGenerationPath = os.getcwd() + "/logGenerationData.txt"
    if os.path.exists(logGenerationPath):
        os.remove(logGenerationPath)


if __name__ == '__main__':
    init()

    logNums = int(input("input the num which is needed to processed:"))
    # 读取日志文件，模拟产生日志的过程
    f = open("/home/hduser/LogShard/allLog.txt", encoding = "utf-8")
    line = f.readline()
    i = 0
    print("start logSystem...time="+str(time.time()))  # 单位时间是秒
    shard0Num=0
    fw = open(os.getcwd() + "/logGenerationData.txt", "a")
    while line and i<logNums:
        # 这一行用于统计日志产生速率
        if i % 50 == 0:
            fw.write("logSystem,i="+str(i)+", time="+str(time.time())+"\n")
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
            # print("start to connect:"+ node['ip'] + " "+ node['port'])
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
    print("allNum is:"+str(i)+ "  shard0num is:"+str(shard0Num))
    check5()
    tail()

