# from socket import *
import hashlib
import time
import json
import utils
import sendMsg
import os
import random


class Block:
    version = 1
    hashPrevBlock = ''  # 前一个区块的hash
    hashMerkleRoot = ''  # 当前区块的merkle树根
    timestamp = 0  # float
    logs = []  # 区块体数据


class Log:
    hash = ''
    rawData = ''


# 这个是每个进程单独的(经过测试)
log_queue = []


def handleWrite(conmmunicationData):
    # print("handle write...")
    logData = conmmunicationData.content
    hashLog = hashlib.sha256(logData.encode('utf-8')).hexdigest()
    targetShardId = int(hashLog[-2:],16) % utils.shardNum  # 用日志hash的最后两位转换为10进制进行求余选择分片
    # print("hashLog is:"+hashLog)

    if targetShardId == utils.shardId:
        conmmunicationData.type = 'M'  # 将其从W修改为M
        send_data = json.dumps(conmmunicationData.__dict__)
        # 分片内广播这条日志
        # 按理这里需要把所有的日志内容广播给分片里的所有节点，但是实际运行中大量连接把目标端口占满挂掉，显示“目标主机积极拒绝”
        # 所以这一步暂时不完成，可用sleep代替；或者建立一个套接字池
        for node in utils.mapTable[-1]['shards'][utils.shardId]:
            if node['ip'] == utils.ip and node['port'] == str(utils.port):  # 不用给自己发送
                continue
            sendMsg.sendData(node, send_data)
        writeLocal(logData)

    else:
        send_data = json.dumps(conmmunicationData.__dict__)
        # 转发到对应分片
        # print("this shardId is:"+str(utils.shardId)+" targetShardId is :"+str(targetShardId)+" ip:"+utils.ip + " port:"+utils.port)
        node = random.choice(utils.mapTable[-1]['shards'][targetShardId])
        sendMsg.sendData(node, send_data)


def writeLocal(logData): # 确定属于该server, 不用再次广播
    # print("write local...")
    # 序列化到本地
    hashLog = hashlib.sha256(logData.encode('utf-8')).hexdigest()
    log = Log()
    log.hash = hashLog
    log.rawData = logData
    log_queue.append(log.__dict__)
    # print("ip:"+utils.ip+" port:"+utils.port+" logQueue.len+"+str(len(log_queue)))

    if len(log_queue) >= 10:  # 可以形成一个块了, 然后把块内容序列化到本地
        utils.queueLock.acquire()
        fw = open(os.getcwd() + "\\logUpChainRate.txt", "a")
        fw.write("shardId:" + str(
            utils.shardId) + " ip:" + utils.ip + " port:" + utils.port + " generated a block,time=" + utils.generateStrTime() + "\n")
        print("shardId:" + str(
            utils.shardId) + " ip:" + utils.ip + " port:" + utils.port + " generated a block,time=" + utils.generateStrTime())
        fw.close()
        utils.queueLock.release()
        # print("generated a block,time="+utils.generateStrTime())


        block = Block()
        block.hashPrevBlock = ''
        block.hashMerkleRoot = calMerkleRoot(log_queue)
        block.timestamp = utils.generateFloatTime()
        block.logs = log_queue
        # print("up chain...+"+json.dumps(block.__dict__))
        PBFT(block)
        log_queue.clear()


def calMerkleRoot(log_queue):
    pass
    merkleRootHash = ''
    return merkleRootHash


def PBFT(block):
    # 假设已经经过了PBFT步骤
    # 发送给每个节点这条消息
    communicationMsg = utils.CommunicationData()
    communicationMsg.type = 'B'
    communicationMsg.content = json.dumps(block.__dict__)

    time.sleep(0.01)  # 1/1000 = 0.01 ms
    path = "D:\BlocksFile" + utils.ip + " " + str(utils.port)

    blocksFile = open(path, "a")
    blocksFile.write(communicationMsg.content + '\n')



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

