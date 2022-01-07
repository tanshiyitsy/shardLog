from . import sendMsg
from . import utils


workQueue = sendMsg.workQueue


def consume():
    rqueueLock = sendMsg.rqueueLock
    commitData = {}
    verifyData = {}
    # 消费队列里面的数据
    rqueueLock.acquire()
    while not workQueue.empty():
        data = workQueue.get()  # 拿出来的就是communication类型的
        if data.type == 'H':
            if verifyData.__contains__(data.content):
                verifyData[data.content] += 1
                if verifyData[data.content] == 1:
                    # 满足一定量的hash 验证消息，可以提交commit消息
                    communicationData = sendMsg.CommunicationData()
                    communicationData.type = 'C'
                    communicationData.content = data.content
                    servers = utils.MapData.shards[-1].servers
                    for server in servers:
                        sendMsg.sendData(server, communicationData)
                    verifyData.pop(data.content)   # 删除该条记录
            else:
                verifyData[data.content] = 1
            pass
        elif data.type == 'C':
            if commitData.__contains__(data.content):
                commitData[data.content] += 1
                if commitData[data.content] == 1:
                    pass  # 满足一定量的commit消息，可以持久化到本地
            else:
                commitData[data.content] = 1
    rqueueLock.release()