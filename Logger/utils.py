import os
import json
import time

ip = "127.0.0.1"
port = 8008

# 映射关系
# mapTable = [{'version':0,'startTime':0, 'endTime':0, 'shards':[[{'ip': "127.0.0.1", 'port': "8008"}]]}]
path = os.getcwd() + "\\..\\mapTable"
mapFile = open(path, encoding="utf-8")
line = mapFile.readline()
mapTable = json.loads(line)


def generateStrTime():
    return str(time.time())

def generateFloatTime():
    return time.time()


class MapData:
    version = 0
    startTime = 0
    endTime = 0
    shards = []  # 分片数量


class Shard:
    servers = [{'ip': "127.0.0.1", 'port': "8008"}, {'ip': "127.0.0.1", 'port': "8008"}]  # 一批节点的IP+port

class CommunicationData:
    type = '' # W,R,A(audit), H(对比hash）
    content = ''