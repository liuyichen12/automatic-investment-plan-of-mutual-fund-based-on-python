# -*- coding: utf-8 -*-

from jqdatasdk import *
import jqdatasdk as jq
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy as np
import matplotlib.dates as md


def Kline(start_money,code_id,start_time,end_time,option):
    jq.auth('15510242299', '242299')  # 登录JQDATA
    q = query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code == code_id,
                                             finance.FUND_NET_VALUE.day > start_time,
                                             finance.FUND_NET_VALUE.day < end_time).order_by(
                                             finance.FUND_NET_VALUE.day.desc()).limit(3000)
    nv = finance.run_query(q).net_value  # 净值
    nv_np = np.array(nv)  # 提取净值数据
    day_n = finance.run_query(q).day
    day_np = np.array(day_n)  # 提取日期数据

    max_id = len(nv)  # 获取一共有多少个数据
    close_price = nv_np

    open_price = np.array(nv.shift())

    # 开盘价为前一日的结算净值
    earlier_nv = query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code == code_id,
                                                      finance.FUND_NET_VALUE.day > start_time - 2,
                                                      finance.FUND_NET_VALUE.day < start_time).order_by(
        finance.FUND_NET_VALUE.day.desc()).limit(3000)
    e_n = finance.run_query(earlier_nv).net_value
    # open_price[len(open_price)-1] = e_n #替换定投当天开盘价为前一天结算数据

    # change type
    e_n = np.array(e_n)
    open_price = open_price.tolist()
    open_price.append(e_n[0])
    del open_price[0]
    open_price = np.array(open_price)

    plt.figure(" K Line", facecolor="lightgray")
    plt.title(" K Line", fontsize=16)
    plt.xlabel("Data", fontsize=14)
    plt.ylabel("Price", fontsize=14)

    # 3.x坐标（时间轴）轴修改
    ax = plt.gca()
    # 设置主刻度定位器为周定位器（每周一显示主刻度文本）
    ax.xaxis.set_major_locator(md.WeekdayLocator(byweekday=md.MO))
    ax.xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_minor_locator(md.DayLocator())

    plt.tick_params(labelsize=8)
    plt.grid(linestyle=":")

    # 4.判断收盘价与开盘价 确定蜡烛颜色
    for i in range(len(open_price) - 1):
        close_price[i] = open_price[i + 1]
    colors_bool = close_price >= open_price
    colors = np.zeros(colors_bool.size, dtype="U5")
    colors[:] = "r"
    colors[colors_bool] = "green"

    # 5.确定蜡烛边框颜色
    edge_colors = np.zeros(colors_bool.size, dtype="U1")
    edge_colors[:] = "r"
    edge_colors[colors_bool] = "green"

    # 绘制开盘价折线图片
    plt.plot(day_np, open_price, color="b", linestyle="--",
             linewidth=2, label="open", alpha=0.3)

    # 6.绘制蜡烛
    plt.bar(day_np, (close_price - open_price), 0.8, bottom=open_price, color=colors,
            edgecolor=edge_colors, zorder=3)

    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.show()

