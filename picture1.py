# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import os
# x轴刻度标签
# x_ticks = ['a', 'b', 'c', 'd', 'e', 'f']
# x_ticks = ['50','100','150','200','250','300','350','400','450','500','550','600','650','700','750','800','850']
x_ticks = np.arange(50, 9750, 50)
# # x轴范围（0, 1, ..., len(x_ticks)-1）
x = np.arange(len(x_ticks))
# 第1条折线数据
# y1 = [5, 3, 2, 4, 1, 6]
y1 = []
y2 = []
f = open(os.getcwd()+"\\p1", "r")
line = f.readline()
while line:
    time1 = line.split(" ")[0]
    time2 = line.split(" ")[1]
    time1 = time1.split("=")[1]
    time2 = time2.split("=")[1]
    time1 = round(float(time1),4)
    time2 = round(float(time2),4)
    y1.append(time1)
    y2.append(time2)
    line = f.readline()

# 第2条折线数据
# y2 = [3, 1, 6, 5, 2, 4]

print(y1)
print(y2)
plt.figure(figsize=(10, 6))
# 画第1条折线，参数看名字就懂，还可以自定义数据点样式等等。
plt.plot(x, y1, color='#FF0000', label='log generation delay', linewidth=1.0)
# 画第2条折线
plt.plot(x, y2, color='#00FF00', label='log storage delay', linewidth=1.0)
# 给第1条折线数据点加上数值，前两个参数是坐标，第三个是数值，ha和va分别是水平和垂直位置（数据点相对数值）。
# for a, b in zip(x, y1):
#     plt.text(a, b, '%d'%b, ha='center', va= 'bottom', fontsize=18)
# 给第2条折线数据点加上数值
# for a, b in zip(x, y2):
#     plt.text(a, b, '%d'%b, ha='center', va= 'bottom', fontsize=18)
# 画水平横线，参数分别表示在y=3，x=0~len(x)-1处画直线。
# plt.hlines(3, 0, len(x)-1, colors = "#000000", linestyles = "dashed")

plt.xticks([r for r in x], x_ticks, fontsize=18, rotation=20)
plt.yticks(fontsize=18)
# 添加x轴和y轴标签
# plt.xlabel(u'x_label', fontsize=18)
# plt.ylabel(u'y_label', fontsize=18)
plt.xlabel(u'Number of logs processed', fontsize=18)
plt.ylabel(u'Delay(Second)', fontsize=18)

# 标题
# plt.title(u'Delay Comparison between Log Generation interval and Log Storage', fontsize=18)
# 图例
plt.legend(fontsize=18)

plt.show()