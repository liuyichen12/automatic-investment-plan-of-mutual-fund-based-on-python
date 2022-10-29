# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 16:41:08 2021

@author: 97065
"""
from jqdatasdk import *
import jqdatasdk as jq
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy as np
import matplotlib.dates as md


def junxianDT(start_money, code_id, start_time, end_time,option):
    #start_money=1000#输入定投金额
    #start_time=20200520
    #end_time=20210605
    #code_id="100053"#选择基金代码
    jq.auth('15510242299', '242299')  # 登录JQDATA
    q = query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code == code_id,
                                             finance.FUND_NET_VALUE.day > start_time,
                                             finance.FUND_NET_VALUE.day < end_time).order_by(
        finance.FUND_NET_VALUE.day.desc()).limit(3000)
    nv = finance.run_query(q).net_value  # 净值
    nv_np0 = np.array(nv)  # 提取净值数据
    nv_np = nv_np0[::-1]
    day_n = finance.run_query(q).day
    day_np = np.array(day_n)  # 提取日期数据

    num = start_money / nv_np[0]
    max_id = len(nv)  # 获取一共有多少个数据
    close_price = nv_np
    num_times = 1  # 定义投入基金的次数#####################################
    N = 250  # 开始日期之前的250交易日数据作为投资参考
    p_t = query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code == code_id,
                                               finance.FUND_NET_VALUE.day < start_time
                                               ).order_by(
        finance.FUND_NET_VALUE.day.desc()).limit(N)

    p_t_value = finance.run_query(q).net_value  # 净值
    ave_val = np.mean(p_t_value)  # 250日均线值
    option = 1
    day_income = [0]  # 定义收益空数组
    # 每周定投
    sum_ = start_money
    if option == 1:
        for i in range(1, max_id):
            # 计算投入的份额

            if i % 5 == 1 and i > 1:
                market_ref = (ave_val - nv_np[i]) / ave_val
                adj_money = (market_ref + 1) * start_money
                num = num + adj_money / nv_np[i]
                #                num_times=num_times+1
                # 每天当日收益

                if market_ref < 0.05:  # 根据设置定投的交易日根据均线进行投入调整,实现多涨少投,越跌越投,以降低平均成本
                    adj_money = adj_money / 2
                sum_ = sum_ + adj_money
            oneweek_income = (nv_np[i] * num) - sum_

            day_income.append(oneweek_income)  # 将每天的收益导出
    # 双周定投
    if option == 2:
        for i in range(1, max_id):
            # 计算投入的份额

            if i % 10 == 1 and i > 1:
                market_ref = (ave_val - nv_np[i]) / ave_val
                adj_money = (market_ref + 1) * start_money
                num = num + adj_money / nv_np[i]
                #                num_times=num_times+1
                # 每天当日收益

                if market_ref < 0.05:  # 根据设置定投的交易日根据均线进行投入调整,实现多涨少投,越跌越投,以降低平均成本
                    adj_money = adj_money / 2
                sum_ = sum_ + adj_money
            oneweek_income = (nv_np[i] * num) - sum_

            day_income.append(oneweek_income)  # 将每天的收益导出
    # 每月定投
    if option == 3:
        for i in range(1, max_id):
            # 计算投入的份额
            market_ref = (ave_val - nv_np[i]) / ave_val
            adj_money = (market_ref + 1) * start_money
            if i % 20 == 1 and i > 1:
                market_ref = (ave_val - nv_np[i]) / ave_val
                adj_money = (market_ref + 1) * start_money
                num = num + adj_money / nv_np[i]
                #                num_times=num_times+1
                # 每天当日收益

                if market_ref < 0.05:  # 根据设置定投的交易日根据均线进行投入调整,实现多涨少投,越跌越投,以降低平均成本
                    adj_money = adj_money / 2
                sum_ = sum_ + adj_money
            oneweek_income = (nv_np[i] * num) - sum_

            day_income.append(oneweek_income)  # 将每天的收益导出
        # 设置鼠标与图像的交互

    def onMotion(event):
        # 获取鼠标位置和标注可见性
        x = event.xdata
        y = event.ydata
        visible = annot.get_visible()
        if event.inaxes == ax:
            # 测试鼠标事件是否发生在曲线上
            contain, _ = sinCurve.contains(event)
            if contain:
                annot.xy = (x, y)
                annot.set_text(str(y))  # 设置标注文本
                annot.set_visible(True)
            else:
                if visible:
                    annot.set_visible(False)
            event.canvas.draw_idle()

    # 绘制每日收益图
    fig = plt.figure(figsize=(10, 4), dpi=80)
    ax = fig.gca()
    x = day_np[::-1]  # 日期
    y = day_income  # 日收益
    # 坐标轴设置
    font = {'family': 'SimHei',
            'size': '16'
            }
    plt.rc("font", **font)
    plt.rc('axes', unicode_minus=False)
    plt.xlabel("data")
    plt.ylabel("accumulated income")
    plt.title("accumulated income chart")

    sinCurve, = plt.plot(x, day_income, picker=2)

    annot = ax.annotate("",
                        xy=(0, 0), xytext=(-50, 50), textcoords="offset pixels", bbox=dict(boxstyle="round", fc="r"),
                        arrowprops=dict(arrowstyle="<->"))
    annot.set_visible(False)

    fig.canvas.mpl_connect('motion_notify_event', onMotion)

    plt.show()


