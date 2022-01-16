import threading
import utils
import recvMsg
import time
from multiprocessing import Process


if __name__ == '__main__':
    recvDataThreads = []
    # 1. 启动当前shard中的所有node
    shards = utils.mapTable[-1]['shards']
    for shard in shards:
        for node in shard:
            # print("ip:" + node['ip'] + " port:" + node['port'] + " recvDataThread started,time=" + str(time.time()))
            process = Process(target=recvMsg.recvData, args=(node['ip'],node['port'],))
            recvDataThreads.append(process)
            # recvDataThread = threading.Thread(target=recvMsg.recvData, args=(node['ip'],node['port'],))
            # recvDataThreads.append(recvDataThread)

    for recvDataThread in recvDataThreads:
        recvDataThread.start()


