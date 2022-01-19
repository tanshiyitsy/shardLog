from socket import *
import json
import queue
import os
import logger
import  utils
import traceback


workQueue = queue.Queue(100)  # 用来暂时存放接收的消息



def recvData(ip="",port="8008"):
    tcp_server = socket(AF_INET, SOCK_STREAM)
    # tcp_server.bind((ip, int(port)))  # 绑定ip，port, 这里ip默认本机
    tcp_server.bind(("", int(port)))
    # 启动被动连接,多少个客户端可以连接
    # 使用socket创建的套接字默认的属性是主动的,使用listen将其变为被动的，这样就可以接收别人的链接了
    tcp_server.listen(1024)
    utils.ip = ip
    utils.port = port
    utils.shardId = getShard(ip,port)
    print("logger is ready, ip:" + ip + " port:" + port + " shardId:"+str(utils.shardId))

    if utils.shardNum == 1:
        utils.path = os.getcwd() + "\..\examData\logUpChainRate4(NoShard).txt"
    else:
        utils.path = os.getcwd() + "\..\examData\logUpChainRate4(Shard).txt"
    # 初始化文件
    fw = open(utils.path,"w")
    fw.write("start..." + "\n")
    fw.close()

    while True:
        # 创建接收
        # 如果有新的客户端来链接服务器，那么就产生一个新的套接字专门为这个客户端服务
        client_socket, clientAddr = tcp_server.accept()
        # print("ip:"+ip+" port:"+port+" accept new connect:" + str(clientAddr))

        from_client_msg = client_socket.recv(1024*1024)  # 接收1024给字节,这里recv接收的不再是元组，区别UDP
        from_client_msg = from_client_msg.decode("gbk")
        # print("接收的数据：", from_client_msg)

        # 判断请求
        # if from_client_msg == "exit":
        #     print("client_socket closed")
        #     client_socket.close()
        #     break
        commnicationData = utils.CommunicationData()
        try:
            tempData = json.loads(from_client_msg)
            commnicationData.__dict__.update(tempData)
            if commnicationData.type == 'M':
                # 临时方案，跳过PBFT步骤，接收到确定属于该server的log
                logger.writeLocal(commnicationData.content)
                pass
            elif commnicationData.type == 'W': # 写请求
                logger.handleWrite(commnicationData)
                pass
            elif commnicationData.type == 'R': # 读请求
                pass
            elif commnicationData.type == 'A': # 审计请求
                pass
            elif commnicationData.type == 'H': # 广播的区块hash消息
                utils.queueLock.acquire()
                workQueue.put(commnicationData)
                utils.queueLock.release()
                pass
            elif commnicationData.type == 'C':   # 广播的commit消息
                utils.queueLock.acquire()
                workQueue.put(commnicationData)
                utils.queueLock.release()
                pass
            else:
                pass
        except Exception as e:
            # 这里有可能是接收空间不够，被自动截断
            print("ERROR:   ip:"+ip+" port:"+port+" content:"+from_client_msg)
            print(e)
            traceback.print_exc()
        from_client_msg = ""
        client_socket.close()

def getShard(ip,port):
    shardId = 0
    shards = utils.mapTable[-1]['shards']
    for shard in shards:
        for node in shard:
            if node['ip'] == ip and node['port'] == port:
                return shardId
        shardId += 1
    return shardId

# if __name__ == '__main__':
#     pass