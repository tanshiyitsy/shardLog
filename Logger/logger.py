# from socket import *
import hashlib
import time
import json
import utils
import sendMsg
import os

'''
ip = "127.0.0.1"
port = 8008
tcp_server = socket(AF_INET, SOCK_STREAM)
tcp_server.bind(('', port))  # 绑定ip，port, 这里ip默认本机
# 启动被动连接,多少个客户端可以连接
# 使用socket创建的套接字默认的属性是主动的,使用listen将其变为被动的，这样就可以接收别人的链接了
tcp_server.listen(128)
print("logger is ready, port:" + str(port))

while True:
    # 创建接收
    # 如果有新的客户端来链接服务器，那么就产生一个新的套接字专门为这个客户端服务
    client_socket, clientAddr = tcp_server.accept()
    print("accept new connect" + str(clientAddr))

    from_client_msg = client_socket.recv(1024)  # 接收1024给字节,这里recv接收的不再是元组，区别UDP
    from_client_msg = from_client_msg.decode("gbk")

    # 判断请求
    if from_client_msg == "exit":
        print("client_socket closed")
        client_socket.close()
        break
    print("接收的数据：", from_client_msg)
    # 发送数据给客户端
    # send_data = client_socket.send("客户端你好，服务器端收到，公众号【Python研究者】".encode("gbk"))
'''

class Block:
    version = 1
    hashPrevBlock = ''  # 前一个区块的hash
    hashMerkleRoot = ''  # 当前区块的merkle树根
    timestamp = 0  # float
    logs = []  # 区块体数据


class Log:
    hash = ''
    rawData = ''



fw = open(os.getcwd()+"\\logUpChainRate.txt", "a")

log_queue = []


def handleWrite(logData):
    hashLog = hashlib.sha256(logData.encode('utf-8')).hexdigest()

    # 判断如果是当前分片处理
    log = Log()
    log.hash = hashLog
    log.rawData = logData
    log_queue.append(log.__dict__)

    if len(log_queue) >= 100:
        fw.write("generated a block,time="+utils.generateStrTime()+"\n")
        print("generated a block,time="+utils.generateStrTime())
        block = Block()
        block.hashPrevBlock = ''
        block.hashMerkleRoot = calMerkleRoot(log_queue)
        block.timestamp = utils.generateFloatTime()
        block.logs = log_queue
        # print("up chain...+"+json.dumps(block.__dict__))
        PBFT(block, 0)
        log_queue.clear()


def calMerkleRoot(log_queue):
    pass
    merkleRootHash = ''
    return merkleRootHash

def PBFT(block, shardId):
    # 假设已经经过了PBFT步骤
    # 发送给每个节点这条消息
    communicationMsg = utils.CommunicationData()
    communicationMsg.type = 'M'
    communicationMsg.content = json.dumps(block.__dict__)
    sendMsg = json.dumps(communicationMsg.__dict__)

    servers = utils.mapTable[-1]['shards'][shardId]
    for server in servers:
        if server['ip'] == utils.ip and server['port'] == str(utils.port):  # 不用给自己发送
            continue
        sendMsg.sendData(server, sendMsg)
    writeLocal(communicationMsg)


def writeLocal(communicationMsg):
    time.sleep(0.01)  # 1/1000 = 0.01 ms
    path = "D:\BlocksFile" + utils.ip + " " + str(utils.port)

    blocksFile = open(path, "a")
    blocksFile.write(communicationMsg.content+'\n')


'''
def PBFT(block, shardId):
    sendMsg = json.dumps(block.__dict__)
    # 1. pre-prepare, 将当前区块内容广播到其它节点
    servers = utils.mapTable[-1].shards[shardId]
    for server in servers:
        if server['ip'] == ip and server['port'] == str(port):  # 不用给自己发送
            continue
        connection.sendData(server, sendMsg)

    # 2. prepare, 交换视图
    currentBlockHash = hashlib.sha256(sendMsg.encode('utf-8')).hexdigest()
    for server in servers:
        if server['ip'] == ip and server['port'] == str(port):  # 不用给自己发送
            continue
        connection.sendData(server, currentBlockHash)
    othersView = []

    # 3. 比对一致则持久化到本地
    targetView = othersView[0]
    tag = True
    for view in othersView:
        if view != targetView:
            tag = False
            break
    if tag == True:
        # 持久化到本地
        pass
'''

