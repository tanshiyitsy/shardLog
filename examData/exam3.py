import os
# rate代表产生500条日志数据需要的时间，单位是秒
# 第一列是日志的产生速率，第二列是日志的上链速率

if __name__ == '__main__':
    f1 = open(os.getcwd()+"/../logSystem\logGenerationData.txt", encoding="utf-8")
    line1 = f1.readline()
    t11 = float(line1.split("=")[-1])
    line1 = f1.readline()

    f2 = open(os.getcwd()+"/../Logger\logUpChainRate.txt", encoding="utf-8")
    line2 = f2.readline()
    t21 = float(line2.split("=")[-1])
    line2 = f2.readline()

    while line1 and line2:
        t12 = float(line1.split("=")[-1])
        t22 = float(line2.split("=")[-1])
        # 每产生500条日志需要的时间 t12 - t11)/100 * 1000
        rate1 = (t12 - t11) * 10
        rate2 = (t22 - t21) * 10
        print("rate1=" + str(rate1) + " rate2=" + str(rate2))
        t11 = t12
        t21 = t22
        line1 = f1.readline()
        line2 = f2.readline()