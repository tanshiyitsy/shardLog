# -*- coding: UTF-8 -*-
import os
import json
import time
from threading import local
import threading

# 映射关系
# mapTable = [{'version':0,'startTime':0, 'endTime':0, 'shards':[[{'ip': "127.0.0.1", 'port': "8008"}]]}]
mapPath = os.getcwd() + "/../mapTable"
mapFile = open(mapPath, encoding="utf-8")
line = mapFile.readline()
mapTable = json.loads(line)

shardNum = len(mapTable[-1]['shards'])


#本node的ip和port
ip = local()
port = local()
shardId = local()
servers_socket = local()
path = local()

queueLock = threading.Lock()
rqueueLock = threading.RLock()

def generateStrTime():
    return str(time.time())

def generateFloatTime():
    return time.time()



class CommunicationData:
    type = '' # W,R,A(audit), H(对比hash）
    content = ''