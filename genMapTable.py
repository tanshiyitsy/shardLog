# -*- coding: UTF-8 -*-
import json
import os


class MapData:
    version = 0
    startTime = 0
    endTime = 0
    shards = []  # 分片数量


class Shard:
    servers = []
    # servers = [{'ip': "127.0.0.1", 'port': "8008"}, {'ip': "127.0.0.1", 'port': "8008"}]  # 一批节点的IP+port

class Server:
    ip = ''
    port = ''

if __name__ == '__main__':
    shardNums = int(input("input the shard nums please"))
    nodeNums = int(input("input the node nums please"))
    ip = '127.0.0.1'
    startPort = 5000
    fw = open(os.getcwd() + "/mapTable", "w")

    # [{"version": 0, "startTime": 0, "endTime": 0, "shards": [[{"ip": "127.0.0.1", "port": "4008"},{"ip": "127.0.0.1", "port": "4009"},{"ip": "127.0.0.1", "port": "4010"}],[{"ip": "127.0.0.1", "port": "4011"},{"ip": "127.0.0.1", "port": "4012"}],[{"ip": "127.0.0.1", "port": "4013"},{"ip": "127.0.0.1", "port": "4014"}],[{"ip": "127.0.0.1", "port": "4015"},{"ip": "127.0.0.1", "port": "4016"},{"ip": "127.0.0.1", "port": "4017"}],[{"ip": "127.0.0.1", "port": "4018"},{"ip": "127.0.0.1", "port": "4019"},{"ip": "127.0.0.1", "port": "4020"}],[{"ip": "127.0.0.1", "port": "4021"},{"ip": "127.0.0.1", "port": "4022"},{"ip": "127.0.0.1", "port": "4023"}],[{"ip": "127.0.0.1", "port": "4024"},{"ip": "127.0.0.1", "port": "4025"},{"ip": "127.0.0.1", "port": "4026"}]]}]
    mapTable = MapData()
    mapTable.version = 1
    mapTable.startTime = 0
    mapTable.endTime = 0
    mapTable.shards = []


    for shardNum in range(1, shardNums+1):
        shard = Shard()
        shard.servers = []
        for nodeNum in range(1,nodeNums+1):
            server = Server()
            server.ip = ip
            server.port = str(startPort)
            startPort += 1
            shard.servers.append(server)
        mapTable.shards.append(shard)

    mapTables = []
    mapTables.append(mapTable)

    content = json.dumps(mapTables, default=lambda o: o.__dict__)
    print(content)
    fw.write(content)
    fw.close()