from socket import *
import json
import queue
import threading
import logger
import  utils


workQueue = queue.Queue(100)  # 用来暂时存放接收的消息
queueLock = threading.Lock()
rqueueLock = threading.RLock()


def recvData(ip="127.0.0.1",port="8008"):
    tcp_server = socket(AF_INET, SOCK_STREAM)
    tcp_server.bind((ip, int(port)))  # 绑定ip，port, 这里ip默认本机
    # 启动被动连接,多少个客户端可以连接
    # 使用socket创建的套接字默认的属性是主动的,使用listen将其变为被动的，这样就可以接收别人的链接了
    tcp_server.listen(128)
    print("logger is ready, port:" + port)
    utils.ip = ip
    utils.port = port

    while True:
        # 创建接收
        # 如果有新的客户端来链接服务器，那么就产生一个新的套接字专门为这个客户端服务
        client_socket, clientAddr = tcp_server.accept()
        # print("accept new connect" + str(clientAddr))

        from_client_msg = client_socket.recv(2048)  # 接收1024给字节,这里recv接收的不再是元组，区别UDP
        from_client_msg = from_client_msg.decode("gbk")
        # print("接收的数据：", from_client_msg)

        # 判断请求
        if from_client_msg == "exit":
            print("client_socket closed")
            client_socket.close()
            break
        commnicationData = utils.CommunicationData()
        tempData = json.loads(from_client_msg)
        commnicationData.__dict__.update(tempData)
        if commnicationData.type == 'M':
            # 临时方案，跳过PBFT步骤，接收到日志原文就序列化到本地
            logger.writeLocal(commnicationData)
            pass
        elif commnicationData.type == 'W':
            logger.handleWrite(commnicationData.content)
            pass
        elif commnicationData.type == 'R':
            pass
        elif commnicationData.type == 'A':
            pass
        elif commnicationData.type == 'H':
            queueLock.acquire()
            workQueue.put(commnicationData)
            queueLock.release()
            pass
        elif commnicationData.type == 'C':
            queueLock.acquire()
            workQueue.put(commnicationData)
            queueLock.release()
            pass


# if __name__ == '__main__':
#     pass