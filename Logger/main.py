import threading
import utils
import recvMsg
import time
import json


if __name__ == '__main__':
    recvDataThreads = []
    # 1. 启动当前shard中的所有node
    shards = utils.mapTable[-1]['shards']
    for shard in shards:
        for node in shard:
            recvDataThread = threading.Thread(target=recvMsg.recvData(), args=(node['ip'],node['port'],))
            recvDataThreads.append(recvDataThread)
            recvDataThread.start()

    for recvDataThread in recvDataThreads:
        print("ip:" + node['ip'] + " port:" + node['port'] + " recvDataThread started,time=" + str(time.time()))
        recvDataThread.start()