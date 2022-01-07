import threading
import sys
import recvMsg
import time


if __name__ == '__main__':
    # sys.path.append('/e/pycharm/workspace/shardLog/Logger')
    # print(sys.path)
    # 1. 启动接收消息的线程
    print("start recvDataThread....,time="+str(time.time()))
    recvDataThread = threading.Thread(target=recvMsg.recvData(), args=())
    recvDataThread.start()
    pass
