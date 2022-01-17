from socket import *
import utils

def sendData(node, send_data):
    try:
        tcp_socket = socket(AF_INET, SOCK_STREAM)
        tcp_socket.connect((node['ip'], int(node['port'])))  # 连接服务器，建立连接,参数是元组形式
        tcp_socket.send(send_data.encode("gbk"))  # 加上.decode("gbk")可以解决乱码
        # print("send msg:"+send_data)
        tcp_socket.close()
    except Exception as e:
        print("ip:"+utils.ip+" port:"+utils.port+" error:"+e)


