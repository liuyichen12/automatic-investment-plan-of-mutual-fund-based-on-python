from jqdatasdk import *
import jqdatasdk as jq
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy as np
# from prettytable import PrettyTable
# from prettytable import MSWORD_FRIENDLY
import xlrd
from datetime import date,datetime


jq.auth('15510242299', '242299') #登录JQDATA
def CL(start_money=1000,code_id="161725",start_time=20200520,end_time=20210605,option=1):

    jq.auth('15510242299', '242299') #登录JQDATA
        
        
        
    #start_money=1000    #输入定投金额
        
   # code_id=161725        #选择基金代码
        
    #设置投资时间段   如2020-01-05~2021-05-21
   # start_time=20190609
    #end_time=20210609
        
    #选择定投方式  1. 按周定投   2.按双周定投    3.按月定投
    #option=1
        
    q=query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code==code_id,finance.FUND_NET_VALUE.day>start_time,finance.FUND_NET_VALUE.day<end_time).order_by(finance.FUND_NET_VALUE.day.desc()).limit(3000)
    nv=finance.run_query(q).net_value  #净值
            
    nv_np0=np.array(nv)      #提取净值数据
    nv_np=nv_np0[::-1]
            
    day_np=np.array(finance.run_query(q).day)   #提取日期数据
                
            
    max_id=len(nv)   #获取一共有多少个数据
            
    num=start_money/nv_np[0]        #购买的基金份额
            
    day_income=[0]   #定义收益空数组
    num_times=1    #定义投入基金的次数
            
            
            #按周定投
    if option==1:
        for i in range(1,max_id):   
                    
                    #计算投入的份额
            if i%5==1 and i>1:
                num=num+start_money/nv_np[i]
                num_times=num_times+1
                #每天当日收益
            oneweek_income=(nv_np[i]*num)-(start_money*num_times)
                    
            day_income.append(oneweek_income)    #将每天的收益导出
                
            #按双周定投
    if option==2:
        for i in range(1,max_id):   
                    
                    #计算投入的份额
            if i%10==1 and i>1:
                num=num+start_money/nv_np[i]
                num_times=num_times+1
                #每天当日收益
            oneweek_income=(nv_np[i]*num)-(start_money*num_times)
                    
            day_income.append(oneweek_income)    #将每天的收益导出
            
            #按月定投
    if option==3:
        for i in range(1,max_id):   
                    
                    #计算投入的份额
            if i%20==1 and i>1:
                num=num+start_money/nv_np[i]
                num_times=num_times+1
                    #每天当日收益
            oneweek_income=(nv_np[i]*num)-(start_money*num_times)
                    
            day_income.append(oneweek_income)    #将每天的收益导出        
            
            #设置鼠标与图像的交互
    def onMotion(event):
                #获取鼠标位置和标注可见性
        x=event.xdata
        y=event.ydata
        visible=annot.get_visible()
        if event.inaxes==ax:
                    #测试鼠标事件是否发生在曲线上
            contain,_=sinCurve.contains(event)
            if contain:
                annot.xy=(x,y)
                annot.set_text(str(y)) #设置标注文本
                annot.set_visible(True)
            else:
                if visible:
                    annot.set_visible(False)
            event.canvas.draw_idle()
            
            
            #绘制每日收益图    
    fig=plt.figure(figsize=(10,4),dpi=80)
    ax=fig.gca()
    x=day_np[::-1]      #日期
    y=day_income  #日收益
        #坐标轴设置
    font = {'family' : 'SimHei',
                'size':'16'
                          }
    plt.rc("font",**font)         #设置坐标轴中文显示
    plt.rc('axes', unicode_minus=False)
    plt.xlabel("data")
    plt.ylabel("income")
    plt.title("Accumulated income")
            
    sinCurve,=plt.plot(x,day_income,picker=2)
            
    annot=ax.annotate("",
                         xy=(0,0),xytext=(-50,50),textcoords="offset pixels",bbox=dict(boxstyle="round",fc="r"),arrowprops=dict(arrowstyle="<->"))
    annot.set_visible(False)
            
    fig.canvas.mpl_connect('motion_notify_event',onMotion)
             
         
    plt.show()
    
    '''
    table=PrettyTable(["定投方式", "普通定投"])
    table.add_row(["定投期数",num_times])
    table.add_row(["累计投入",(num_times*start_money)])
    table.add_row(["累计收益",round(day_income[max_id-1],2)])
    table.add_row(["累计收益率",('{:.2f}%'.format(day_income[max_id-1]/num_times/start_money*100))])
    table.set_style(MSWORD_FRIENDLY) 
    print(table)
    '''


def read_excel(option=1):

    start_money=1000    #输入定投金额
        
    #设置投资时间段   
    start_time=20210509
    end_time=20210609
    
    #选择定投方式  1. 按周定投   2.按双周定投    3.按月定投
    #option=1
    
    file = 'jjname.xlsx'   #基金名称表格

    wb = xlrd.open_workbook(filename=file)#打开文件


    sheet1 = wb.sheet_by_index(0)  #通过索引获取表格

    cols = sheet1.col_values(0)#获取列内容
    jjname=sheet1.col_values(1) #获取基金名称

   # day_np=np.array(finance.run_query(q).day)   #提取日期数据
    
    
    
    #num=start_money/nv_np[0]        #购买的基金份额
        
    day_income=[0]   #定义收益空数组
    num_times=1    #定义投入基金的次数
    jj_income=[]   #所有基金收益
    dict={}
    #每周
    if option==1:
        for k in range(1,99):
            code_id=cols[k]
            
            
            q=query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code==code_id,finance.FUND_NET_VALUE.day>start_time,finance.FUND_NET_VALUE.day<end_time).order_by(finance.FUND_NET_VALUE.day.desc()).limit(3000)
            nv=finance.run_query(q).net_value  #净值
            
            nv_np0=np.array(nv)      #提取净值数据
            nv_np=nv_np0[::-1]
            
            
            num=start_money/nv_np[0]        #购买的基金份额
            max_id=len(nv)   #获取一共有多少个数据
            for i in range(1,max_id):   
                        
                        #计算投入的份额
                if i%5==1 and i>1:
                    num=num+start_money/nv_np[i]
                    num_times=num_times+1
                    #每天当日收益
                oneweek_income=(nv_np[i]*num)-(start_money*num_times)
            num_times=1
           # jj_income.append(oneweek_income)  
            dict[jjname[k]] =round(oneweek_income,2)   # 添加
            
        
        #每双周
    if option==2:
        for k in range(1,8):
            code_id=cols[k]
            
            
            q=query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code==code_id,finance.FUND_NET_VALUE.day>start_time,finance.FUND_NET_VALUE.day<end_time).order_by(finance.FUND_NET_VALUE.day.desc()).limit(3000)
            nv=finance.run_query(q).net_value  #净值
     
            nv_np0=np.array(nv)      #提取净值数据
            nv_np=nv_np0[::-1]
            
            
            num=start_money/nv_np[0]        #购买的基金份额
            max_id=len(nv)   #获取一共有多少个数据
            for i in range(1,max_id):   
                        
                        #计算投入的份额
                if i%10==1 and i>1:
                    num=num+start_money/nv_np[i]
                    num_times=num_times+1
                    #每天当日收益
                oneweek_income=(nv_np[i]*num)-(start_money*num_times)
            num_times=1
            dict[jjname[k]] =round(oneweek_income,2)   # 添加    
            

     #每月
    if option==3:
        for k in range(1,8):
            code_id=cols[k]
            
            
            q=query(finance.FUND_NET_VALUE).filter(finance.FUND_NET_VALUE.code==code_id,finance.FUND_NET_VALUE.day>start_time,finance.FUND_NET_VALUE.day<end_time).order_by(finance.FUND_NET_VALUE.day.desc()).limit(3000)
            nv=finance.run_query(q).net_value  #净值
     
            nv_np0=np.array(nv)      #提取净值数据
            nv_np=nv_np0[::-1]
            
            
            num=start_money/nv_np[0]        #购买的基金份额
            max_id=len(nv)   #获取一共有多少个数据
            for i in range(1,max_id):   
                        
                        #计算投入的份额
                if i%20==1 and i>1:
                    num=num+start_money/nv_np[i]
                    num_times=num_times+1
                    #每天当日收益
                oneweek_income=(nv_np[i]*num)-(start_money*num_times)
            num_times=1
            dict[jjname[k]] =round(oneweek_income,2)   # 添加
            
   
    new_dict=sorted(dict.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)
    return new_dict
        
        

	
    



    


