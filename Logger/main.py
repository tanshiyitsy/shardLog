# -*- coding: UTF-8 -*-
import utils
import recvMsg
import os
from multiprocessing import Process


if __name__ == '__main__':
    # 初始化文件
    # fw = open(os.getcwd() + "\\logUpChainRate.txt", "w")
    # fw.write("start..." + "\n")
    # fw.close()

    recvDataThreads = []
    # 1. 启动当前shard中的所有node
    # 只模拟分片0的
    shards = utils.mapTable[-1]['shards']

    for shard in shards:
        for node in shard:
            # print("ip:" + node['ip'] + " port:" + node['port'] + " recvDataThread started,time=" + str(time.time()))
            process = Process(target=recvMsg.recvData, args=(node['ip'],node['port'],))
            recvDataThreads.append(process)
            # recvDataThread = threading.Thread(target=recvMsg.recvData, args=(node['ip'],node['port'],))
            # recvDataThreads.append(recvDataThread)
        break

    for recvDataThread in recvDataThreads:
        recvDataThread.start()


