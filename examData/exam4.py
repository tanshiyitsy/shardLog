import os

# 求分片和不分片的对比数据

if __name__ == '__main__':
    # 未分片的
    f1 = open(os.getcwd()+"/logUpChainRate4(NoShard).txt", encoding="utf-8")
    line1 = f1.readline()
    t11 = float(line1.split("=")[-1])
    line1 = f1.readline()

    # 分了三个片的
    f2 = open(os.getcwd()+"/logUpChainRate4(Shard).txt", encoding="utf-8")
    line2 = f2.readline()
    t21 = float(line2.split("=")[-1])
    line2 = f2.readline()

    num1 = 0
    sum1 = 0
    sum2 = 0
    while line1:
        num1 += 1
        t12 = float(line1.split("=")[-1])
        # 每产生500 条日志需要的时间 t12 - t11)/100 * 1000
        rate1 = (t12 - t11) * 10
        sum1 += rate1

        t11 = t12
        line1 = f1.readline()


    num2 = 0
    while line2:
        num2 += 1
        t22 = float(line2.split("=")[-1])
        # 每产生500 条日志需要的时间 t12 - t11)/100 * 1000
        rate2 = (t22 - t21) * 10
        sum2 += rate2
        t21 = t22
        line2 = f2.readline()


    time1 = sum1/num1
    time2 = sum2/num2
    print("time1="+str(time1)+ " time2:"+str(time2))