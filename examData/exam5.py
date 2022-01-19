import os

# 求分片和不分片的对比数据

def check():
    # 未分片的
    print("check....")
    f1 = open(os.getcwd() + "\logUpChainRate4(NoShard).txt", encoding="utf-8")
    line1 = f1.readline()  # 跳过第一行的start
    line1 = f1.readline()
    t11 = float(line1.split("=")[-1])
    line1 = f1.readline()

    # 分了三个片的
    f2 = open(os.getcwd() + "\logUpChainRate4(Shard).txt", encoding="utf-8")
    line2 = f2.readline()  # 跳过第一行的start
    line2 = f2.readline()
    t21 = float(line2.split("=")[-1])
    line2 = f2.readline()

    num1 = 0
    sum1 = 0
    sum2 = 0

    while line1:
        t12 = float(line1.split("=")[-1])
        line1 = f1.readline()

    while line2:
        t22 = float(line2.split("=")[-1])
        line2 = f2.readline()

    time1 = t12 - t11
    time2 = t22 - t21
    print("time1=" + str(time1) + " time2:" + str(time2))

if __name__ == '__main__':
    check()